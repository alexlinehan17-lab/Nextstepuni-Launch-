/** Resolve deferred Physics cards from their reviewed source pair, never a Q-number match. */
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
let sources;
let metadata;

/** Validate committed review identities without requiring the optional PDF corpus. */
export function physicsSourceMetadataMap(audit) {
  const result = new Map();
  for (const [key, review] of Object.entries(audit.sittings)) {
    if (review.sitting !== 'deferred') continue;
    if (!/^\d{4}-(?:hl|ol)-deferred$/.test(key) || review.status !== 'reviewed') {
      throw new Error(`Unreviewed Physics sitting: ${key}`);
    }
    const [year, level] = key.split('-');
    const fileid = `LC021${level === 'hl' ? 'A' : 'G'}LP000EV.pdf`;
    for (const [kind, folder] of [['paper', 'deferredexams'], ['scheme', 'deferredmarkingschemes']]) {
      const source = review.sources[kind];
      const expected = `paper-trail-corpus/${folder}/${year}/${source.fileid}`;
      if (source.path !== expected || source.fileid !== fileid) {
        throw new Error(`${key}: wrong ${kind} archive identity`);
      }
      if (!/^[a-f0-9]{64}$/.test(source.sha256)) throw new Error(`${key}: invalid ${kind} source hash`);
    }
    const source = {
      sitting: 'deferred', lang: 'ev',
      paperFileid: review.sources.paper.fileid.replace(/\.pdf$/, '-deferred.pdf'),
      schemeFileid: review.sources.scheme.fileid.replace(/\.pdf$/, '-deferred.pdf'),
    };
    for (const task of review.tasks) {
      if (!task.id.startsWith(`phys-${key}-`) || task.status !== 'carded' || result.has(task.id)) {
        throw new Error(`${key}: invalid deferred task ${task.id}`);
      }
      result.set(task.id, source);
    }
  }
  return result;
}

/** Authoring remains strict: every original must exist and match its reviewed hash. */
export function physicsSourceMap(audit, readSource = path => readFileSync(resolve(root, path))) {
  const result = physicsSourceMetadataMap(audit);
  for (const [key, review] of Object.entries(audit.sittings)) {
    if (review.sitting !== 'deferred') continue;
    for (const kind of ['paper', 'scheme']) {
      const source = review.sources[kind];
      if (createHash('sha256').update(readSource(source.path)).digest('hex') !== source.sha256) {
        throw new Error(`${key}: ${kind} bytes differ from visual review`);
      }
    }
  }
  return result;
}

const readAudit = () => JSON.parse(readFileSync(resolve(root, 'scripts/markbank/authored/physics-review-audit.json')));
const findSource = (map, cardId) => {
  const source = map.get(cardId);
  if (!source) throw new Error(`Deferred Physics card lacks reviewed sources: ${cardId}`);
  return source;
};

export function reviewedPhysicsSource(cardId) {
  if (!/^phys-\d{4}-(?:hl|ol)-deferred-/.test(cardId)) return undefined;
  // Publish the cache only after every source passes; a failed read is retryable.
  sources ??= physicsSourceMap(readAudit());
  return findSource(sources, cardId);
}

export function reviewedPhysicsSourceMetadata(cardId) {
  if (!/^phys-\d{4}-(?:hl|ol)-deferred-/.test(cardId)) return undefined;
  metadata ??= physicsSourceMetadataMap(readAudit());
  return findSource(metadata, cardId);
}
