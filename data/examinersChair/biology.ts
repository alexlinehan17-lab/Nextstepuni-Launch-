/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Biology (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * points-based marking grammar (the notation, the context rule, the Section A
 * surplus-answer penalty and the Sections B/C asterisk nullification) is the
 * real SEC system, cited to:
 *  - SEC LC Biology HL marking scheme 2023 (Deferred sitting) —
 *    examiner-reports/biology/2023-marking-scheme.*
 * The general marking conventions are the SEC's standard framework (identical
 * across sittings); only per-question model answers are specific to a paper.
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC Biology HL marking scheme 2023, ${p}` });
const MS25 = (p: string) => ({ label: `SEC Biology HL marking scheme 2025, ${p}` });

// A two-outcome "how many marks?" ladder for the penalty sessions.
const totalScale = (marks: number[]): ScaleLevel[] =>
  marks.map(m => ({ id: `m${m}`, label: `${m} marks`, annotation: `${m}m`, marks: m }));

// ───────────────── Bio1 · Right word, wrong sentence (context) ─────────────────

const BIO1: GridSession = {
  mode: 'grid',
  id: 'bio-context',
  subject: 'biology',
  level: 'common',
  title: 'Right word, wrong sentence',
  cue: 'Explain',
  question: 'Explain how water moves from the soil into a root hair cell.',
  questionNote:
    'Question authored for this exercise. Marked points-based at 3 marks per correct point; the context rule is the SEC general convention — a key term only scores when it appears in a correct statement.',
  grid: {
    perPoint: [{ id: 'mark', label: 'Point', marks: 3 }],
    shorthand: 'each correct point · 3m',
    ruleNote:
      'Synonyms are accepted unless an exact term is demanded, but a key term only earns the mark inside a correct statement. A right word in a wrong sentence scores nothing — the examiner marks the biology, not the vocabulary.',
    cite: MS('p.3–4 (marking notation and context rule)'),
  },
  scripts: [
    {
      id: 'bio1-a',
      label: 'Script A',
      persona: 'Keyword-spotter',
      attempts: [
        {
          id: 'bio1-a-1',
          text: 'Water moves in by osmosis because the soil has a lower water concentration than the cell.',
          key: { mark: 0 },
          keyNote: 'The right term — osmosis — sits in a reversed statement: soil water is HIGHER, the cell is lower, which is why water moves in. Correct word, wrong biology: 0. Naming the process does not rescue a false explanation.',
        },
        {
          id: 'bio1-a-2',
          text: 'It happens through the cell wall which is fully permeable.',
          key: { mark: 0 },
          keyNote: 'Osmosis is across the selectively permeable cell membrane, not simply “the cell wall” — and the claim as written is not the mechanism. No mark.',
        },
      ],
      embodies: {
        behaviour: 'Writes correct key terms inside incorrect statements — the scheme credits terms only in a correct context.',
        cite: MS('p.4'),
      },
    },
    {
      id: 'bio1-b',
      label: 'Script B',
      persona: 'Plain but correct',
      attempts: [
        {
          id: 'bio1-b-1',
          text: 'Water moves in by osmosis, from the soil where water is in higher concentration to the cell where it is lower.',
          key: { mark: 3 },
          keyNote: 'Correct process in a correct statement — the direction of the gradient is right. Full 3 marks, even though the language is simple.',
        },
        {
          id: 'bio1-b-2',
          text: 'It crosses the selectively permeable cell membrane.',
          key: { mark: 3 },
          keyNote: 'A second, distinct correct point, correctly stated. 3 marks.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-bio1',
    rule: 'A key term only scores in a correct sentence.',
    detail:
      'In Biology, the examiner marks the statement, not the vocabulary. The right word in a wrong explanation earns nothing — get the direction, structure and logic right around the term.',
    cite: MS('p.4'),
  },
};

// ───────────────── Bio2 · The surplus penalty (Section A) ─────────────────

const BIO2: ScaleSession = {
  mode: 'scale',
  id: 'bio-surplus',
  subject: 'biology',
  level: 'common',
  title: 'When a guess costs you',
  cue: 'Name (Section A)',
  question: 'Name two carbohydrates that are structural (not energy-storage) molecules. [The candidate wrote: “Cellulose, glycogen”.]',
  questionNote:
    'Question authored for this exercise. The Section A surplus-answer rule is the SEC general convention: a surplus wrong answer cancels the marks for a correct one. Cellulose is structural; glycogen is a storage carbohydrate, so it is the surplus wrong answer here.',
  scale: {
    name: 'Section A · 2 × 3m',
    levels: totalScale([0, 3, 6]),
    notes: [
      'Each correct carbohydrate is worth 3 marks.',
      'Section A rule: “A surplus wrong answer cancels the marks awarded for a correct answer.”',
      'Cellulose (structural) is correct = 3. Glycogen is a storage carbohydrate — a surplus wrong answer.',
      'So the wrong answer cancels the right one: 3 − 3 = 0.',
    ],
    cite: MS('p.4–5 (surplus wrong answer rule, Section A)'),
  },
  scripts: [
    {
      id: 'bio2-a',
      label: 'The script',
      persona: 'Right one, plus a guess',
      work: ['Cellulose, glycogen'],
      keyLevelId: 'm0',
      keyNote:
        'Cellulose earns 3 — but glycogen is a storage carbohydrate, a surplus WRONG answer, and in Section A a surplus wrong answer cancels a correct one. 3 − 3 = 0. The safe move was to write only what you are sure of: “Cellulose” alone would have scored 3.',
      embodies: {
        behaviour: 'Adds an unsure extra answer in Section A, where a surplus wrong answer cancels a correct one.',
        cite: MS('p.4–5'),
      },
    },
  ],
  takeaway: {
    id: 'codex-bio2',
    rule: 'In Section A, a wrong extra answer can cancel a right one.',
    detail:
      'The surplus-wrong-answer rule means padding a short answer with a guess is not free — it can wipe out a mark you had earned. Give exactly the number asked, and only answers you are sure of.',
    cite: MS('p.4–5'),
  },
};

// ───────────────── Bio3 · The asterisk trap (Sections B/C) ─────────────────

const BIO3: ScaleSession = {
  mode: 'scale',
  id: 'bio-asterisk',
  subject: 'biology',
  level: 'common',
  title: 'The one-answer trap',
  cue: 'Name (Sections B/C)',
  question: 'Name the product, other than ethanol, formed when yeast respires anaerobically. [The candidate wrote: “Carbon dioxide or lactic acid”.]',
  questionNote:
    'Question authored for this exercise. The asterisk-nullification rule is the SEC general convention for single-term answers in Sections B and C: where only one specific term is acceptable, adding a wrong alternative nullifies the correct one.',
  scale: {
    name: 'Sections B/C · single term · 3m',
    levels: totalScale([0, 3]),
    notes: [
      'The only acceptable answer here is carbon dioxide (3 marks).',
      'For such single-term answers, the scheme flags the item with * : an added wrong alternative nullifies the correct one.',
      'Yeast produces CO₂ and ethanol; lactic acid is the wrong fermentation pathway (that is muscle, not yeast).',
      '“Carbon dioxide OR lactic acid” therefore nullifies to 0.',
    ],
    cite: MS('p.5 (asterisk nullification, Sections B/C)'),
  },
  scripts: [
    {
      id: 'bio3-a',
      label: 'The script',
      persona: 'Hedges the single answer',
      work: ['Carbon dioxide or lactic acid'],
      keyLevelId: 'm0',
      keyNote:
        'Carbon dioxide is correct — but this is a single-term answer, so the “or lactic acid” hedge nullifies it entirely. 0 marks. Committing to “Carbon dioxide” alone scores the full 3. Hedging reads to the examiner as not knowing.',
      embodies: {
        behaviour: 'Adds a wrong alternative to a single-term answer, where the asterisk rule nullifies the correct term.',
        cite: MS('p.5'),
      },
    },
  ],
  takeaway: {
    id: 'codex-bio3',
    rule: 'On single-answer questions, don’t hedge.',
    detail:
      'Where only one term is acceptable (the asterisk cases), writing “X or Y” with a wrong Y nullifies the correct X. Commit to the answer you mean — an “or” can cost you the whole mark.',
    cite: MS('p.5'),
  },
};

// ───────────────── Bio4 · Read the marks-per-point ─────────────────

const BIO4: GridSession = {
  mode: 'grid',
  id: 'bio-marks-per-point',
  subject: 'biology',
  level: 'common',
  title: 'Read the marks-per-point',
  cue: 'Label (Sections B/C)',
  question:
    'The diagram shows a sperm cell. Label THREE of its parts. The scheme prints the demand as “Any three · 3(1)”. One candidate labels two parts and writes a careful sentence about each, expecting more for the detail.',
  questionNote:
    'Question authored for this exercise. The “N(M)” notation is the SEC general convention: the bracket is the marks PER point. Labels here are 3(1) — three of them, one mark each — cited to the real 2023 sperm-cell item.',
  grid: {
    perPoint: [
      { id: 'l1', label: 'First correct label', marks: 1 },
      { id: 'l2', label: 'Second correct label', marks: 1 },
      { id: 'l3', label: 'Third correct label', marks: 1 },
    ],
    shorthand: 'labels · 3(1) — three at 1m each',
    ruleNote:
      'The bracket in “3(1)” is the marks per point: each label is worth one mark, so the marks are in the count, not the detail. A “6(3)” definition is the opposite — few developed points. Read the notation before you decide how much to write.',
    cite: MS('p.16 (sperm-cell labels, 3(1)); p.4 and p.11 (6(3) and 3(3) notation)'),
  },
  scripts: [
    {
      id: 'bio4-a',
      label: 'Script A',
      persona: 'Develops two, skips the third',
      attempts: [
        {
          id: 'bio4-a-1',
          text: 'Labels the head and the tail, and writes a sentence on each explaining its job — but stops at two labels.',
          key: { l1: 1, l2: 1, l3: 0 },
          keyNote:
            'Two correct labels earn two marks — but each label is worth only 1, so the extra sentences add nothing, and the untaken third label is a mark simply left behind. On a 3(1) item the marks are in the count: name the third part.',
        },
      ],
      embodies: {
        behaviour: 'Over-develops a 1-mark label and gives fewer labels than asked — misreading the marks-per-point notation.',
        cite: MS('p.16'),
      },
    },
    {
      id: 'bio4-b',
      label: 'Script B',
      persona: 'Three quick labels',
      attempts: [
        {
          id: 'bio4-b-1',
          text: 'Labels head, midpiece and tail — three parts, named plainly.',
          key: { l1: 1, l2: 1, l3: 1 },
          keyNote:
            'Three correct labels, one mark each — full 3 marks. Plain naming is exactly right for a 3(1) item; the notation told the candidate to go for count, not depth.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-bio4',
    rule: 'The bracket is the marks per point — let it set your depth.',
    detail:
      'In “N(M)” the bracket is marks per point: 3(1) wants three quick labels, 6(3) wants two developed points. Read it before answering — it tells you whether to go for count or for depth, and stops you over-writing a 1-mark label or under-developing a 3-mark one.',
    cite: MS('p.16'),
  },
};

// ───────────────── Bio5 · The answer you crossed out (cancelled answers) ─────────────────

const BIO5: ScaleSession = {
  mode: 'scale',
  id: 'bio-cancelled',
  subject: 'biology',
  level: 'common',
  title: 'The answer you crossed out',
  cue: 'Define (cancelled answers)',
  question:
    'What is pollination? [The candidate wrote the full answer, then drew a line through all of it and moved on — with no second version written.]',
  questionNote:
    'Question and script authored for this exercise. The cancelled-answer rule is the SEC general convention: an answer written once and then cancelled with no replacement is marked as if it had not been cancelled. Taken from the worked pollination example in the 2023 scheme.',
  scale: {
    name: 'Define · 3(3) — three points at 3m',
    levels: totalScale([0, 3, 6, 9]),
    notes: [
      'Pollination scores on three points: transfer of pollen / from anther / to stigma. 3(3) — 9 marks in all.',
      'The rule (p.4): “Where a candidate answers a question … once only and then cancels the answer, you should ignore the cancelling and treat the answer as if the candidate had not cancelled it.”',
      'So a correct answer the candidate struck out — with no second version — is still marked in full.',
      'Three correct points, cancelled once and not replaced: 3 × 3 = 9.',
    ],
    cite: MS('p.4 (cancelled answers rule)'),
  },
  scripts: [
    {
      id: 'bio5-a',
      label: 'Script A',
      persona: 'The full, correct answer — then crossed out',
      work: [
        'Transfer of pollen, from anther, to stigma',
        '(all of the above struck through — no replacement written)',
      ],
      keyLevelId: 'm9',
      keyNote:
        'All three points are there — transfer of pollen, from anther, to stigma — and the candidate then cancelled the lot. Because it was answered once only and not replaced, the examiner ignores the cancelling and marks it as written: full 9. Crossing out your only answer does not un-write it.',
      embodies: {
        behaviour: 'Cancels a correct single answer with no replacement — the scheme marks it as if uncancelled.',
        cite: MS('p.4'),
      },
    },
    {
      id: 'bio5-b',
      label: 'Script B',
      persona: 'Two different versions, hoping both count',
      work: [
        'Version 1: Transfer of pollen to the stigma',
        'Version 2: Transfer of pollen from the anther',
      ],
      keyLevelId: 'm6',
      keyNote:
        'Two un-cancelled versions. Version 1 gives two points (transfer of pollen, to stigma); version 2 gives two (transfer of pollen, from anther). The scheme marks each version and takes the greater — it does NOT stitch them into a manufactured “all three”. Best single version = 2 points = 6. Points from separate versions cannot be pooled.',
      embodies: {
        behaviour: 'Splits points across two versions expecting them to be summed — the scheme takes the greater version, not a combined total.',
        cite: MS('p.4'),
      },
    },
  ],
  takeaway: {
    id: 'codex-bio5',
    rule: 'Crossing out your only answer doesn’t delete it — but you can’t pool two versions.',
    detail:
      'If you answer once and cancel it with no replacement, the examiner marks it as if uncancelled, so a struck-out correct answer still scores. But where you give two versions, the scheme takes the better one whole — it will not combine points from both into a total. Commit to one complete answer.',
    cite: MS('p.4'),
  },
};

// ───────────────── Bio6 · It has to match what you named (must-match dependency) ─────────────────

const BIO6: GridSession = {
  mode: 'grid',
  id: 'bio-must-match',
  subject: 'biology',
  level: 'common',
  title: 'It has to match what you named',
  cue: 'Name (must match)',
  question:
    'For your investigation into the effect of denaturation on an enzyme, name the enzyme you used, its substrate and its product.',
  questionNote:
    'Question authored for this exercise; the answer structure and the “must match named enzyme” dependency are taken from the 2023 enzyme-investigation item (Q9(b)(i)). The substrate and product marks are awarded only where they match the enzyme the candidate named.',
  grid: {
    perPoint: [
      { id: 'enzyme', label: 'Named enzyme', marks: 3 },
      { id: 'substrate', label: 'Substrate (must match enzyme)', marks: 3 },
      { id: 'product', label: 'Product (must match enzyme)', marks: 3 },
    ],
    shorthand: 'enzyme + substrate + product · 3 + 3 + 3 (substrate & product must match the enzyme)',
    ruleNote:
      'The substrate and product marks are conditional: the scheme prints “must match named enzyme”. Name amylase and your substrate must be starch and your product maltose; pair it with “protein” and the substrate mark is gone — even though protein is a real substrate, it belongs to a different enzyme. Internal consistency, not just plausibility, is what scores.',
    cite: MS('p.11 (enzyme investigation — substrate/product must match named enzyme)'),
  },
  scripts: [
    {
      id: 'bio6-a',
      label: 'Script A',
      persona: 'Right enzyme, mismatched pair',
      attempts: [
        {
          id: 'bio6-a-1',
          text: 'Enzyme: amylase. Substrate: protein. Product: amino acids.',
          key: { enzyme: 3, substrate: 0, product: 0 },
          keyNote:
            'Amylase is a valid enzyme — 3 marks. But amylase acts on starch to give maltose; “protein” and “amino acids” belong to a protease. Both are real biology, yet neither matches the enzyme named, so both marks are lost. 3 only.',
        },
      ],
      embodies: {
        behaviour: 'Names a correct enzyme but gives a substrate and product from a different pathway, where the scheme requires them to match the named enzyme.',
        cite: MS('p.11'),
      },
    },
    {
      id: 'bio6-b',
      label: 'Script B',
      persona: 'Consistent throughout',
      attempts: [
        {
          id: 'bio6-b-1',
          text: 'Enzyme: amylase. Substrate: starch. Product: maltose.',
          key: { enzyme: 3, substrate: 3, product: 3 },
          keyNote:
            'Amylase, starch, maltose — a single consistent pathway. All three match, all three score: full 9.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-bio6',
    rule: 'Where the scheme says “must match”, the answer has to be internally consistent.',
    detail:
      'Some marks are conditional on an earlier choice: a substrate or product only scores if it matches the enzyme you named. A true fact from a different pathway earns nothing. Pick one example and keep every part of the answer consistent with it.',
    cite: MS('p.11'),
  },
};

// ───────────────── Bio7 · One missing part, half the marks (diagram threshold) ─────────────────

const BIO7: ScaleSession = {
  mode: 'scale',
  id: 'bio-diagram-threshold',
  subject: 'biology',
  level: 'common',
  title: 'One missing part, half the marks',
  cue: 'Draw (diagram)',
  question:
    'Draw a labelled diagram of the human female reproductive system. [The scheme awards the diagram mark for showing: vagina and uterus and fallopian tube and ovary.] The candidate’s diagram shows the vagina, uterus and ovary — but no fallopian tube.',
  questionNote:
    'Question authored for this exercise; the diagram mark and its “any one missing = 3 marks” threshold are taken from the 2023 female-reproductive-system item (Q14(c)(i)). Only the diagram mark is modelled here, not the separate labels mark. The 2025 scheme prints the same threshold as explicit bands “6, 3, 0”.',
  scale: {
    name: 'Diagram · 6, any one missing = 3',
    levels: totalScale([0, 3, 6]),
    notes: [
      'The diagram mark requires four structures: vagina and uterus and fallopian tube and ovary — 6 marks for all four.',
      'The scheme’s threshold: “(any one missing = 3 marks)”. One structure short drops the whole diagram from 6 to 3.',
      'Equivalent 2025 items print the bands explicitly as “6, 3, 0” — all four = 6, one missing = 3, none of it shown = 0.',
      'This diagram omits the fallopian tube — one structure missing — so the mark is the flat 3 the threshold sets, not a proportional “¾ of 6”.',
    ],
    cite: MS('p.16 (female reproductive system diagram — any one missing = 3)'),
  },
  scripts: [
    {
      id: 'bio7-a',
      label: 'The script',
      persona: 'Three of the four structures',
      work: [
        'Diagram showing the vagina, uterus and ovary',
        'No fallopian tube drawn',
      ],
      keyLevelId: 'm3',
      keyNote:
        'Three of the four required structures are there, but the fallopian tube is missing. The scheme does not scale the mark to “¾ of 6” — its threshold is flat: any one missing = 3. One omission costs half the diagram. Check the required structures are all present before you move on.',
      embodies: {
        behaviour: 'Omits one required structure from a diagram scored on a fixed “any one missing = 3” threshold.',
        cite: MS25('p.33 and p.35 (long-bone & male-reproductive diagrams — bands printed “6, 3, 0”)'),
      },
    },
  ],
  takeaway: {
    id: 'codex-bio7',
    rule: 'A diagram mark can be threshold-based, not proportional.',
    detail:
      'Where the scheme says “any one missing = 3”, leaving out a single required structure drops the whole diagram to the lower band — three-quarters right still scores half. Before moving on, check every structure the scheme wants is actually on your drawing.',
    cite: MS('p.16'),
  },
};

export const BIOLOGY_CHAIR: ChairSubject = {
  id: 'biology',
  label: 'Biology',
  tagline: 'Points, context and the penalty rules that quietly cost marks.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [BIO1, BIO2, BIO3, BIO4, BIO5, BIO6, BIO7],
  sources: [
    { label: 'SEC LC Biology HL marking scheme 2023, Deferred sitting (examiner-reports/biology/2023-marking-scheme)' },
    { label: 'SEC LC Biology HL marking scheme 2025 (examiner-reports/biology/2025-hl-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach Biology’s general marking conventions — the points notation, the context rule, the cancelled-answer and “must match” consistency rules, the diagram thresholds, and the Section A / Sections B/C penalty rules — which the scheme applies at both Higher and Ordinary level. They are verified against the 2023 Higher Level scheme (the diagram-threshold bands corroborated by the 2025 scheme); level-specific worked questions are being added.',
};
