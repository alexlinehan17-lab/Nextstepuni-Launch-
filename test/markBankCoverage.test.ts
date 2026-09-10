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
import { readFileSync, readdirSync } from 'node:fs';
import { resolve } from 'node:path';

import baseline from '../scripts/markbank/coverage-baseline.json';
import { CARDS as ENGLISH_HIGHER } from '../components/MarkBank/cards/english/higher';
import { CARDS as ENGLISH_ORDINARY } from '../components/MarkBank/cards/english/ordinary';
import { CARDS as IRISH_HIGHER } from '../components/MarkBank/cards/irish/higher';
import { CARDS as IRISH_ORDINARY } from '../components/MarkBank/cards/irish/ordinary';
import { CARDS as ART_HIGHER } from '../components/MarkBank/cards/art/higher';
import { CARDS as ART_ORDINARY } from '../components/MarkBank/cards/art/ordinary';
import { CARDS as GEOGRAPHY_HIGHER } from '../components/MarkBank/cards/geography/higher';
import { CARDS as GEOGRAPHY_ORDINARY } from '../components/MarkBank/cards/geography/ordinary';

const SUBJECTS = Object.keys(baseline) as (keyof typeof baseline)[];

const deckCards = (subject: string): { id: string; ref: string }[] => {
  if (subject === 'english') {
    return [...ENGLISH_HIGHER, ...ENGLISH_ORDINARY]
      .map(({ id, questionRef: ref }) => ({ id, ref }));
  }
  if (subject === 'irish') {
    return [...IRISH_HIGHER, ...IRISH_ORDINARY]
      .map(({ id, questionRef: ref }) => ({ id, ref }));
  }
  if (subject === 'art') {
    return [...ART_HIGHER, ...ART_ORDINARY]
      .map(({ id, questionRef: ref }) => ({ id, ref }));
  }
  if (subject === 'geography') {
    return [...GEOGRAPHY_HIGHER, ...GEOGRAPHY_ORDINARY]
      .map(({ id, questionRef: ref }) => ({ id, ref }));
  }
  const out: { id: string; ref: string }[] = [];
  // 'common' is the level a one-level subject ships under — LCVP's Link
  // Modules. Leaving it out of this walk reported the whole deck as missing.
  for (const level of ['higher', 'ordinary', 'common']) {
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
// The question number is OPTIONAL: Religious Education's Sections B-J print
// none, so its citations read "2023 HL Section E Q(b)(ii)".
// CL is LCVP's common level, the third the SEC prints.
// History adds two things. Its two FIELDS OF STUDY are separate papers a
// candidate chooses between, so the citation names one — "2021 HL Early
// Modern ...". And its Sections 2 and 3 restart their numbering inside every
// TOPIC, so the section token carries the topic and, at Ordinary, the A/B/C
// part: "Section 2 Topic 1 A Q1". A part priced whole with nothing numbered
// beneath it drops the Q entirely ("Section 2 Topic 1 B"), and the extra Part
// A of 2023-2025 Ordinary is cited "Section Extra A Q1".
// Classical Studies' syllabus to 2022 prints no sections and no question
// numbers: ten TOPICS, each setting questions "(i)" to "(iv)" with lettered
// parts under them, so the topic and the roman together are the address and
// the citation reads "2021 HL Topic 1(i) Q(a)". Its 2023 paper numbers
// Questions 1-16 straight through Sections A and B and cites "2024 HL Q3(b)".
const ADDRESS =
  '^(\\d{4}) (HL|OL|CL)'
  + '(?: (?:Later|Early) Modern)?'
  + '(?: Paper (\\d))?'
  + '(?: Topic \\d{1,2}\\((?:i{1,3}|iv|v)\\))?'
  + '(?: Section ((?:Extra )?[A-Za-z0-9]+(?: Topic \\d{1,2})?(?: [A-C]\\b)?))?'
  + '(?: E(\\d))?';
const QTOKEN = '(?: (?:Q(\\d{1,2})?(-alt)?|ABQ))';
// Either the citation carries a question token, or it ENDS at its section —
// which only a unit the paper numbers nothing beneath may do. Anchoring the
// second form is what stops "2021 HL" alone from matching every citation and
// letting the whole address through as an ignorable suffix.
const HEAD = new RegExp(`${ADDRESS}${QTOKEN}|${ADDRESS}$`);
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
    const identities = cards.map(({ id, ref }) => `${id}\t${ref}`);
    // English overlays 19 hand-enriched cards onto a generated corpus, so its
    // display ordering is not the manifest ordering. Coverage pins identity,
    // not presentation order.
    if (subject === 'english' || subject === 'irish' || subject === 'art'
      || subject === 'geography') identities.sort();
    const digest = createHash('sha256')
      .update(identities.join('\n'))
      .digest('hex').slice(0, 16);
    expect(
      digest,
      `${subject}: a questionRef changed since coverage was measured. ${remeasure}`,
    ).toBe((baseline[subject] as { refsHash?: string }).refsHash);
  });

  it.each(SUBJECTS)('%s citations all parse under the grammar', (subject) => {
    const bad = deckCards(subject)
      .filter(({ ref }) => {
        if (subject === 'english') {
          return !/^\d{4} (?:HL|OL) Paper [12] (?:Text [1-3] QA\((?:i|ii|iii)(?:\)\((?:a|b))?\)|Text [1-3] QB|Composing [1-7]|Single Text [A-I](?:\((?:i|ii)\)| Q[1-4])|Comparative [A-C] Q[12]|Unseen Poetry Q[12]|Prescribed Poetry (?:[1-5]|[A-F] Q(?:1|2\((?:i|ii|iii)\))))$/.test(ref);
        }
        if (subject === 'irish') {
          return !/^\d{4} (?:HL|OL) Paper [12] (?:Cluastuiscint Cuid [ABC] · .+|Ceapadóireacht [A-D]\((?:[a-e]|i{1,3})\)|Léamhthuiscint [AB] · Ceist [1-6]|(?:Prose|Poetry) [23][AB]\([a-c]\)|Literature 4\([a-f]\))$/.test(ref);
        }
        if (subject === 'geography') {
          return !/^\d{4} (?:HL|OL) Part [12] Q(?:[1-9]|1\d|2[0-4])(?:[ABC])?(?: · .+)?$/.test(ref);
        }
        const core = ref.split(/\s+[—–-]\s+/)[0];
        const m = core.match(HEAD);
        return !m || !TAIL.test(core.slice(m[0].length));
      })
      .map(({ id, ref }) => `${id}: "${ref}"`);
    expect(bad, `${subject}: unparseable questionRef(s)`).toEqual([]);
  });

  it('every subject with a deck is measured', () => {
    // A tenth subject added without entering the ledger would ship unmeasured
    // — enumerate the actual deck directories, not the baseline's own keys.
    const dirs = readdirSync(resolve(__dirname, '..', 'components', 'MarkBank', 'cards'),
      { withFileTypes: true })
      .filter((d) => d.isDirectory())
      .map((d) => d.name);
    const unmeasured = dirs.filter((d) => !(d in baseline));
    expect(unmeasured, 'deck directories with no coverage baseline entry').toEqual([]);
  });

  it.each(SUBJECTS)('%s deck content matches its measured baseline', (subject) => {
    // The refs hash pins addresses; this pins everything else — questionText,
    // rows, figure bindings. A card gutted in place trips here.
    const h = createHash('sha256');
    for (const level of ['higher', 'ordinary', 'common']) {
      const path = resolve(
        __dirname, '..', 'components', 'MarkBank', 'cards', subject, `${level}.ts`);
      try { h.update(readFileSync(path)); } catch { /* single-level deck */ }
    }
    if (subject === 'english' || subject === 'irish' || subject === 'art'
      || subject === 'geography') {
      for (const name of ['factory.ts', 'authored.json']) {
        h.update(readFileSync(resolve(
          __dirname, '..', 'components', 'MarkBank', 'cards', subject, name)));
      }
    }
    expect(
      h.digest('hex').slice(0, 16),
      `${subject}: deck content changed since coverage was measured — ` +
      `python3 scripts/markbank/authoring/reconcile.py --all --baseline write`,
    ).toBe((baseline[subject] as { contentHash?: string }).contentHash);
  });
});
