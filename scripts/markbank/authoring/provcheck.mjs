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
import { comparableScheme, claimTraces, normalise } from '../schemeText.mjs';

/** Mirrors UNPRINTED_ANSWER in types/markBank.ts and build-deck.mjs. */
const UNPRINTED_ANSWER = 'The scheme prints no answer for this part.';
/** Mirrors LEVEL_TOKEN in build-deck.mjs. */
const LEVEL_TOKEN = { higher: 'hl', ordinary: 'ol', common: 'cl' };
const cards = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const fallbackSubject = (process.argv[2].split('/').pop() ?? '').replace(/\.json$/, '');
const cache = new Map();
let bad = 0, checked = 0;
for (const c of cards) {
  // The subject comes from the CARD. This was hard-coded to home-economics,
  // which is invisible while only one subject is authored this way and reports
  // every claim of the second one as untraceable the moment there is another —
  // against a scheme for a different subject entirely.
  // The build's own stem: LCVP's Link Modules paper is Common level, filed as
  // "-cl", and this read "-ol" for it and threw.
  const stem = `${c.year ?? 2025}-${LEVEL_TOKEN[c.level ?? 'higher'] ?? 'hl'}`;
  // Biology's authored file carries no subjectId at all, so this read for
  // 'examiner-reports/undefined/...' and threw — which is why that subject has
  // never been pre-checked. Fall back to the file name, the way build-deck does.
  const f = `examiner-reports/${c.subjectId ?? fallbackSubject}/schemes/${stem}.md`;
  if (!cache.has(f)) cache.set(f, comparableScheme(readFileSync(f, 'utf8')));
  const scheme = cache.get(f);
  // The build checks answer-variant rows and the question bonus too.
  for (const r of [c.rows, ...(c.answerVariants ?? []).map(variant => variant.rows), ...(c.questionBonus ? [[c.questionBonus]] : [])].flat()) {
    // A row that claims nothing from the scheme, held to the build's own
    // conditions instead: the fixed unprinted wording as the card's one
    // criterion row, or an ask row that is the card's own question text (the
    // build also requires a scheme solution figure, which this file cannot see).
    if (r.unprinted) {
      checked++;
      if (r.verbatim !== UNPRINTED_ANSWER || r.kind !== 'criterion' || c.rows.length !== 1 || c.answerVariants?.length || !c.rows.includes(r)) {
        bad++; console.log(`UNTRACEABLE ${c.id} :: an unprinted row must be the card's one criterion row, reading "${UNPRINTED_ANSWER}"`);
      }
      continue;
    }
    if (r.ask) {
      checked++;
      if (!normalise(c.questionText ?? '').includes(normalise(r.verbatim))) {
        bad++; console.log(`UNTRACEABLE ${c.id} :: an ask row that is not the card's question text: ${String(r.verbatim).slice(0, 80)}`);
      }
      continue;
    }
    // EXACTLY what build-deck.mjs checks, including the label convention: a row
    // verbatim written "<label> — <marking point>" is checked on the marking
    // point, because the label names which alternative the row answers and is
    // often the paper's word rather than the scheme's. This file drifted from the
    // build and reported 114 Agricultural Science claims as untraceable that the
    // build accepts and ships. A pre-check stricter than the gate it stands in
    // for is worse than no pre-check: it sends you to fix cards that are fine.
    const claims = r.kind === 'anyN' && r.group
      ? [...r.group.options]
      : [String(r.verbatim).split(/\s[—-]\s/).pop()];
    for (const claim of claims) {
      checked++;
      // claimTraces, not a private copy of the build's rule: the build compares
      // around font defects this file knew nothing about, and it lets a menu
      // option that pairs a label with its value trace by halves -- without
      // that this file reported 24 Economics 2019 Ordinary options the build
      // accepts and ships as untraceable.
      if (!claimTraces(scheme, claim, { menuOption: r.kind === 'anyN' })) { bad++; console.log(`UNTRACEABLE ${c.id} :: ${String(claim).slice(0,110)}`); }
    }
  }
}
console.log(`checked ${checked} claims, ${bad} untraceable`);
