/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Provenance pre-check: `node provcheck.mjs /tmp/out.json`
 *
 * Runs the build's own provenance gate against an authoring script's output
 * BEFORE it is merged into the authored file. Same normaliser, same rule: every
 * anyN option, and every non-anyN row verbatim, must appear in that card's own
 * scheme.
 *
 * Worth its own step because the failures are invisible by eye and all have the
 * same cause -- a bundled option that skipped something. Authoring 2022 HL it
 * caught four: a heading anchor longer than the label, so the strip ate the
 * first words of the description; a chunk that ran past its section and
 * swallowed the "and" connector into 3.(b); a Builder chunk that ran on into the
 * bare-name list, where the stripped "etc." broke contiguity; and an "e.g."
 * fragment dropped out of the middle of a marking point.
 *
 * Run from the repo root.
 */
import { readFileSync } from 'node:fs';
import { comparableScheme, normalise } from '../schemeText.mjs';
const cards = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const cache = new Map();
let bad = 0, checked = 0;
for (const c of cards) {
  const stem = `${c.year}-${c.level === 'higher' ? 'hl' : 'ol'}`;
  const f = `examiner-reports/home-economics/schemes/${stem}.md`;
  if (!cache.has(f)) cache.set(f, comparableScheme(readFileSync(f, 'utf8')));
  const scheme = cache.get(f);
  for (const r of c.rows) {
    const claims = [...(r.group?.options ?? [])];
    if (r.kind !== 'anyN') claims.push(r.verbatim);
    for (const claim of claims) {
      checked++;
      if (!scheme.includes(normalise(claim))) { bad++; console.log(`UNTRACEABLE ${c.id} :: ${claim.slice(0,110)}`); }
    }
  }
}
console.log(`checked ${checked} claims, ${bad} untraceable`);
