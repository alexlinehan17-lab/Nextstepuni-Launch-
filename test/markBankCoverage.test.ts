/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The paper-coverage ratchet's CI half.
 *
 * The full ledger (scripts/markbank/authoring/reconcile.py) reads the exam
 * PDFs, so it runs locally, not here. What CI can hold is the coupling: the
 * committed baseline (scripts/markbank/coverage-baseline.json) records each
 * deck's card count at the moment its coverage was last measured, and this
 * test pins the shipped decks to those counts — so ANY deck change fails here
 * until `reconcile.py --all --baseline write` is re-run, and that regeneration
 * runs the ledger, which is where a coverage drop becomes loud
 * (`--baseline check`). A deck can no longer drift away from its measurement.
 *
 * It also parses every shipped questionRef under the citation grammar. An
 * unparseable citation can never be reconciled against a paper, which is how
 * cards rot invisibly — the "orphan" class of bug that once mis-addressed 19
 * Business cards.
 */
import { describe, expect, it } from 'vitest';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

import baseline from '../scripts/markbank/coverage-baseline.json';

const SUBJECTS = Object.keys(baseline) as (keyof typeof baseline)[];

const deckCards = (subject: string): { id: string; ref: string }[] => {
  const out: { id: string; ref: string }[] = [];
  for (const level of ['higher', 'ordinary']) {
    const path = resolve(
      __dirname, '..', 'components', 'MarkBank', 'cards', subject, `${level}.ts`);
    let text: string;
    try {
      text = readFileSync(path, 'utf8');
    } catch {
      continue;
    }
    for (const chunk of text.split(/\.\.\.base,\s*kind:/).slice(1)) {
      const id = chunk.match(/\bid: "([^"]+)"/);
      const ref = chunk.match(/questionRef: "([^"]+)"/);
      if (id && ref) out.push({ id: id[1], ref: ref[1] });
    }
  }
  return out;
};

// The head of the citation grammar, mirrored from reconcile.py. After the
// head and its part tokens, anything whitespace- or digit-led is a per-ask
// disambiguating suffix ("Q13(a)(iii) Name", "Q12(b)(ii) 1–2") — reconcile
// parses the address and ignores the suffix, and this mirror does the same.
// What CANNOT pass is a ref with no parseable address at all.
const HEAD =
  /^(\d{4}) (HL|OL)(?: Paper (\d))?(?: Section ([A-Za-z0-9]+))?(?: E(\d))? (?:Q(\d{1,2})(-alt)?|ABQ)/;
// The bare A/B between tokens is Chemistry's printed option question —
// "Q11(d)A(i)" answers option A of part (d).
const TAIL =
  /^(?:\s*(?:\(\s*[A-Za-z]{1,4}\s*\)|[AB]\b|[,–—-]|and\b))*(?:[\s\d].*)?$/;

describe('Mark Bank paper-coverage ratchet', () => {
  it.each(SUBJECTS)('%s deck matches its measured baseline', (subject) => {
    const cards = deckCards(subject);
    const remeasure =
      `Re-measure before shipping: python3 scripts/markbank/authoring/` +
      `reconcile.py --all --baseline write (and read what --baseline check ` +
      `says about the change).`;
    expect(
      cards.length,
      `${subject}: deck has ${cards.length} cards but the coverage baseline ` +
      `recorded ${baseline[subject].cards}. ${remeasure}`,
    ).toBe(baseline[subject].cards);
    // The count alone leaves a hole: a re-cited card changes coverage with
    // no size change. The hash moves when any citation does.
    const digest = createHash('sha256')
      .update(cards.map(({ id, ref }) => `${id}\t${ref}`).join('\n'))
      .digest('hex').slice(0, 16);
    expect(
      digest,
      `${subject}: a questionRef changed since coverage was measured. ${remeasure}`,
    ).toBe((baseline[subject] as { refsHash?: string }).refsHash);
  });

  it.each(SUBJECTS)('%s citations all parse under the grammar', (subject) => {
    const bad = deckCards(subject)
      .filter(({ ref }) => {
        const core = ref.split(/\s+[—–-]\s+/)[0];
        const m = core.match(HEAD);
        return !m || !TAIL.test(core.slice(m[0].length));
      })
      .map(({ id, ref }) => `${id}: "${ref}"`);
    expect(bad, `${subject}: unparseable questionRef(s)`).toEqual([]);
  });

  it('every subject with a deck is measured', () => {
    // A tenth subject added without entering the ledger would ship unmeasured.
    expect(SUBJECTS.length).toBeGreaterThanOrEqual(9);
  });
});
