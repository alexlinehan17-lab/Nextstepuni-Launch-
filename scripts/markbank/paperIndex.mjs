/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — read Paper Trail's harvested paper index.
 *
 * The SEC file id of the paper a card came from is RESOLVED from this index,
 * never typed by an author. The first Biology build defaulted the field to a
 * literal instead, and that literal turned out to be the id of the marking
 * SCHEME — so 1,104 cards would have deep-linked a student straight to the
 * answers. One implementation lives here so the build script and the test that
 * polices it cannot drift apart.
 */

import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

/** Paper Trail's index, keyed by subject id. */
export const paperIndex = (() => {
  const text = readFileSync(resolve(ROOT, 'paperTrailData.ts'), 'utf8');
  const start = text.indexOf('{', text.indexOf('export const PAPER_TRAIL_INDEX'));
  if (start < 0) throw new Error('PAPER_TRAIL_INDEX not found in paperTrailData.ts');

  // The literal is JSON apart from TypeScript's trailing commas, and its strings
  // hold prose that could contain a brace — so scan with string awareness rather
  // than counting braces blind, and drop trailing commas as we go.
  let depth = 0, inString = false, escaped = false;
  const kept = [];
  let pendingComma = -1;
  for (let i = start; i < text.length; i++) {
    const ch = text[i];
    if (inString) {
      if (escaped) escaped = false;
      else if (ch === '\\') escaped = true;
      else if (ch === '"') inString = false;
      kept.push(ch);
      continue;
    }
    if (ch === '"') { inString = true; pendingComma = -1; }
    else if (ch === '{' || ch === '[') { depth++; pendingComma = -1; }
    else if (ch === '}' || ch === ']') {
      if (pendingComma >= 0) { kept[pendingComma] = ''; pendingComma = -1; }
      depth--;
    } else if (ch === ',') pendingComma = kept.length;
    else if (!/\s/.test(ch)) pendingComma = -1;
    kept.push(ch);
    if (depth === 0) return JSON.parse(kept.join(''));
  }
  throw new Error('PAPER_TRAIL_INDEX is not closed in paperTrailData.ts');
})();

/** The English-language sitting of one subject, year and level. */
export const paperEntry = (subjectId, year, level) =>
  (paperIndex[subjectId] ?? []).find(e => e.year === year && e.level === level && e.lang === 'ev');

/** The section letters a paper's label covers: "Section A&B" -> {A, B}. */
const labelCovers = (label) => new Set((String(label).match(/\b[ABC]\b/g) ?? []));

const stripPdf = (f) => (f ? String(f).replace(/\.pdf$/, '') : null);

/**
 * The file id of the QUESTION PAPER holding a card's section, or null.
 *
 * Null rather than a guess: a wrong id sends a student to the wrong document,
 * and for the section-split subjects the nearest wrong answer is the scheme.
 */
export function resolvePaperFileid(subjectId, year, level, section) {
  const entry = paperEntry(subjectId, year, level);
  if (!entry?.papers?.length) return null;
  // One paper for the year means there is nothing to choose between.
  if (entry.papers.length === 1) return stripPdf(entry.papers[0].doc?.f);
  return stripPdf(entry.papers.find(p => labelCovers(p.label).has(section))?.doc?.f);
}
