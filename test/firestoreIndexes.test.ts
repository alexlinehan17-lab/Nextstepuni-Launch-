/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Static guard: every collection-GROUP query that filters or orders on a field
 * must have an index for that field at COLLECTION_GROUP scope in
 * firestore.indexes.json.
 *
 * Firestore builds single-field indexes automatically, but only at COLLECTION
 * scope. A collection-group query needs a COLLECTION_GROUP index nobody builds
 * for you, and without one it fails at RUNTIME with FAILED_PRECONDITION. Every
 * emulator and unit test passes, because the emulator does not enforce indexes.
 *
 * That is how GDPR erasure broke in production. The cascade in
 * functions/src/dataRights.ts gained
 *   db.collectionGroup("members").where("uid", "==", uid)
 * with no index behind it. From then on every account deletion (a student's
 * own, the GC dashboard's, the admin's) disabled the account, deleted most of
 * its data, then threw at that line and left it half-erased. The one real
 * request in that window failed five times and was abandoned by the retry job.
 */
import { describe, it, expect } from 'vitest';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';

const ROOT = resolve(__dirname, '..');
const SOURCE_DIRS = ['functions/src', 'components', 'hooks', 'utils', 'contexts', 'services'];
const SKIP = new Set(['node_modules', 'lib', 'dist']);

function sourceFiles(dir: string): string[] {
  const abs = join(ROOT, dir);
  let entries: string[];
  try { entries = readdirSync(abs); } catch { return []; }
  return entries.flatMap(name => {
    if (SKIP.has(name)) return [];
    const rel = join(dir, name);
    if (statSync(join(ROOT, rel)).isDirectory()) return sourceFiles(rel);
    return /\.(ts|tsx)$/.test(name) && !/\.test\.tsx?$/.test(name) ? [rel] : [];
  });
}

interface GroupQuery { file: string; group: string; field: string }

/**
 * Collection-group queries and the fields they filter or order on, in both
 * the Admin SDK chain form and the modular client form:
 *   db.collectionGroup("members").where("uid", "==", uid)
 *   query(collectionGroup(db, 'members'), where('uid', '==', uid), orderBy('at'))
 * The statement is read up to its closing semicolon, so a chain broken across
 * lines is still seen.
 */
function groupQueries(): GroupQuery[] {
  const found: GroupQuery[] = [];
  for (const file of SOURCE_DIRS.flatMap(sourceFiles)) {
    const src = readFileSync(join(ROOT, file), 'utf8');
    const opener = /collectionGroup\(\s*(?:[A-Za-z_$][\w$]*\s*,\s*)?["'`]([^"'`]+)["'`]\s*\)/g;
    for (let m = opener.exec(src); m; m = opener.exec(src)) {
      const end = src.indexOf(';', m.index);
      const statement = src.slice(m.index, end === -1 ? undefined : end);
      const fields = /(?:\.|\b)(?:where|orderBy)\(\s*["'`]([^"'`]+)["'`]/g;
      for (let f = fields.exec(statement); f; f = fields.exec(statement)) {
        found.push({ file, group: m[1], field: f[1] });
      }
    }
  }
  return found;
}

interface IndexField { fieldPath: string }
interface IndexFile {
  indexes: Array<{ collectionGroup: string; queryScope?: string; fields: IndexField[] }>;
  fieldOverrides?: Array<{ collectionGroup: string; fieldPath: string; indexes: Array<{ queryScope?: string }> }>;
}

function hasGroupIndex(ix: IndexFile, group: string, field: string): boolean {
  const override = (ix.fieldOverrides ?? []).some(o =>
    o.collectionGroup === group && o.fieldPath === field
    && o.indexes.some(i => i.queryScope === 'COLLECTION_GROUP'));
  const composite = ix.indexes.some(i =>
    i.collectionGroup === group && i.queryScope === 'COLLECTION_GROUP'
    && i.fields.some(f => f.fieldPath === field));
  return override || composite;
}

describe('collection-group queries have COLLECTION_GROUP indexes', () => {
  const ix = JSON.parse(readFileSync(join(ROOT, 'firestore.indexes.json'), 'utf8')) as IndexFile;
  const queries = groupQueries();

  it('finds the erasure cascade query, so the scan itself is working', () => {
    expect(queries).toContainEqual({ file: 'functions/src/dataRights.ts', group: 'members', field: 'uid' });
  });

  it.each(queries.map(q => [`${q.group}.${q.field} (${q.file})`, q] as const))(
    '%s is indexed at COLLECTION_GROUP scope',
    (_label, q) => {
      expect(hasGroupIndex(ix, q.group, q.field), `Add a fieldOverride for ${q.group}.${q.field} with queryScope COLLECTION_GROUP to firestore.indexes.json`).toBe(true);
    },
  );

  it('keeps the automatic COLLECTION-scope indexes on any field it overrides', () => {
    // A fieldOverride REPLACES Firestore's automatic single-field indexes for
    // that field. Listing only the COLLECTION_GROUP entry would silently drop
    // the ascending/descending/array-contains indexes that ordinary
    // collection queries on the same field rely on.
    for (const o of ix.fieldOverrides ?? []) {
      if (!o.indexes.some(i => i.queryScope === 'COLLECTION_GROUP')) continue;
      const scopes = o.indexes.filter(i => i.queryScope === 'COLLECTION');
      expect(scopes.length, `${o.collectionGroup}.${o.fieldPath} override drops collection-scope indexes`).toBe(3);
    }
  });
});
