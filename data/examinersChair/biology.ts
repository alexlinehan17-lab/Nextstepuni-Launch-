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

// ───────────────── Bio8 · Not every mark is worth the same (graduated marks) ─────────────────

const BIO8: ScaleSession = {
  mode: 'scale',
  id: 'bio-graduated',
  subject: 'biology',
  level: 'common',
  title: 'Not every mark is worth the same',
  cue: 'Name / State (graduated marks)',
  question:
    'A six-part short question is worth 20 marks and the scheme prints its marking as “2(4) + 4(3)”. A candidate answers four of the six parts correctly (the first four encountered) and leaves the last two blank. How many marks?',
  questionNote:
    'Question authored for this exercise. The graduated “2(4) + 4(3)” notation is the SEC general convention, quoted verbatim from the marking-scheme introduction: the first two correct answers are worth 4 each and each later correct answer 3.',
  scale: {
    name: '20 marks · 2(4) + 4(3)',
    levels: totalScale([0, 8, 14, 20]),
    notes: [
      'The scheme states: “2(4) + 4(3). This means that the first two correct answers encountered are awarded 4 marks each and each subsequent correct answer is awarded 3 marks.”',
      'So the marks are front-loaded: your first two right answers carry 4 apiece, everything after that carries 3.',
      'Four correct here = 4 + 4 (first two) + 3 + 3 (next two) = 14.',
      'All six correct would be 4 + 4 + 3 + 3 + 3 + 3 = 20; two correct would be just 8.',
    ],
    cite: MS('p.3 (graduated marks — “2(4) + 4(3)”, first two correct 4 each, rest 3)'),
  },
  scripts: [
    {
      id: 'bio8-a',
      label: 'The script',
      persona: 'Four right, two blank',
      work: [
        'Parts (a)–(d): four correct answers',
        'Parts (e)–(f): left blank',
      ],
      keyLevelId: 'm14',
      keyNote:
        'Four correct answers, but not four equal marks. Under 2(4) + 4(3) the first two correct score 4 each and the next two score 3 each: 4 + 4 + 3 + 3 = 14. The notation tells you the early answers are worth most — never skip the opening parts of a graduated question to chase the later ones.',
      embodies: {
        behaviour: 'Treats every correct answer in a “2(4) + 4(3)” item as equal, missing that the first two carry more marks than the rest.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-bio8',
    rule: 'In a graduated “N(x) + M(y)” item, the first answers are worth most.',
    detail:
      'Where the scheme reads “2(4) + 4(3)”, your first two correct answers score 4 each and each later one scores 3 — the marks are front-loaded. Answer the early parts first and don’t leave them for a lower-value part you feel surer of.',
    cite: MS('p.3'),
  },
};

// ───────────────── Bio9 · Best-of selection — the dropped answer (Section A/B/C) ─────────────────

const BIO9: ScaleSession = {
  mode: 'scale',
  id: 'bio-best-of',
  subject: 'biology',
  level: 'common',
  title: 'The answer that gets dropped',
  cue: 'Name / State (Best-of selection)',
  question:
    'Section A, Question 1 offers six short parts (a)–(f), each worth 4 marks, and the rubric marks your BEST FIVE. A candidate attempts all six: five are correct and one (part f) is wrong. How many marks?',
  questionNote:
    'Question authored for this exercise. The Best-of selection rubric is the SEC general structure, printed on every paper: Section A “Best five answers from (a) – (f)”, Section B “Best 2”, Section C “Best 4”. Each Section A part here is 4 marks (2025 structure).',
  scale: {
    name: 'Section A · Best 5 of 6 · each 4',
    levels: totalScale([0, 16, 20]),
    notes: [
      'The rubric marks the “Best five answers from (a) – (f)”, each worth 4 marks — 20 in all.',
      'Five parts are correct = 5 × 4 = 20. The one wrong part is simply not among your best five, so it is dropped.',
      'This is whole-part selection, NOT the Section A surplus rule: a wrong SEPARATE part just fails to be selected — it does not cancel a correct part. (A surplus wrong answer only cancels when it is an extra answer INSIDE one part.)',
      'So the wrong sixth part costs nothing here: 20.',
    ],
    cite: MS25('p.8 (Section A — “Best five answers from (a) – (f)”, each 4)'),
  },
  scripts: [
    {
      id: 'bio9-a',
      label: 'The script',
      persona: 'Five right, one wrong — all six attempted',
      work: [
        'Parts (a)–(e): five correct answers',
        'Part (f): a wrong answer',
      ],
      keyLevelId: 'm20',
      keyNote:
        'Five correct parts at 4 each = 20 — full marks — and the wrong sixth part is dropped, because only your best five parts count. Attempting the extra part was free: on a Best-of item a weak whole answer can only fail to be selected, it cannot pull down a correct one. (Contrast the surplus rule: that bites only when the extra is a second answer inside a single part.)',
      embodies: {
        behaviour: 'Attempts more parts than required under a Best-of rubric — the weakest is dropped without penalty, unlike a surplus answer inside one part.',
        cite: MS('p.11, p.13 (Section B “Best 2”, Section C “Best 4”)'),
      },
    },
  ],
  takeaway: {
    id: 'codex-bio9',
    rule: 'Under a “Best-of” rubric, your weakest whole answer is dropped, not penalised.',
    detail:
      'Section A marks your best five parts, Section B your best two questions, Section C your best four. A wrong or weak SEPARATE answer simply isn’t selected — it costs nothing. That is different from the surplus rule, which only cancels when the extra is a second answer inside one part. So attempt everything you can; just don’t hedge within a single answer.',
    cite: MS25('p.8'),
  },
};

// ───────────────── Bio10 · The experiment is a checklist, not an essay ─────────────────

const BIO10: GridSession = {
  mode: 'grid',
  id: 'bio-experiment-checklist',
  subject: 'biology',
  level: 'common',
  title: 'The experiment is a checklist, not an essay',
  cue: 'Describe (mandatory experiment)',
  question:
    'Describe how you carried out your investigation into the effect of denaturation on an enzyme. [Marked on specific creditable steps — three of them here.]',
  questionNote:
    'Question authored for this exercise; the creditable-step marking is taken verbatim from the 2023 enzyme-denaturation write-up (Q9(b)(ii), “named vessel / water bath at 25°C / left for a time … Any three 3(3)”) and the 2025 osmosis activity (Q9(b)(ii)), where a control, a named apparatus and a timing step are each their own 3-mark point.',
  grid: {
    perPoint: [
      { id: 'control', label: 'Control named & set up', marks: 3 },
      { id: 'apparatus', label: 'Named piece of apparatus', marks: 3 },
      { id: 'time', label: 'Left for a (suitable) time', marks: 3 },
    ],
    shorthand: 'creditable steps · 3 + 3 + 3 (Any three · 3(3))',
    ruleNote:
      'A “describe how you carried out” answer is marked against a list of specific steps — name a control, name the apparatus, state that it was left for a time, give the matching result — each worth its own 3 marks. Flowing prose that mentions none of the listed steps scores nothing; a plain answer that ticks them scores in full. Write to the checklist, not for style.',
    cite: MS('p.11 (enzyme investigation — named vessel / water bath at 25°C / left for a time, Any three 3(3))'),
  },
  scripts: [
    {
      id: 'bio10-a',
      label: 'Script A',
      persona: 'The storyteller',
      attempts: [
        {
          id: 'bio10-a-1',
          text: 'A flowing paragraph: “I was very careful and methodical, I made sure everything was accurate and I watched closely for the reaction to happen, recording what I saw.” No control, no apparatus, no timing named.',
          key: { control: 0, apparatus: 0, time: 0 },
          keyNote:
            'Reads well and says almost nothing markable. None of the creditable steps — a named control, a named piece of apparatus, a timing step — is present, so none of the three points is earned. 0. The examiner marks the steps, not the atmosphere.',
        },
      ],
      embodies: {
        behaviour: 'Writes an eloquent but step-free experiment description, missing the specific creditable points the scheme lists.',
        cite: MS25('p.16 (osmosis activity — Control named / Named apparatus / Left for a time, each 3)'),
      },
    },
    {
      id: 'bio10-b',
      label: 'Script B',
      persona: 'The checklist',
      attempts: [
        {
          id: 'bio10-b-1',
          text: 'Set up a boiled enzyme and an unboiled enzyme as a control, in labelled test tubes, in a water bath at 25 °C, and left both for ten minutes before measuring activity.',
          key: { control: 3, apparatus: 3, time: 3 },
          keyNote:
            'Plain, but every listed step is there: a control (unboiled enzyme), named apparatus (test tubes / water bath), and a timing step (left for ten minutes). Three points, 3 each — full 9. Ticking the checklist beats writing beautifully.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-bio10',
    rule: 'Experiment write-ups are marked on named steps — control, apparatus, timing, result.',
    detail:
      'A “describe how you carried out” answer scores against a checklist: name a control, name your apparatus, say it was left for a time, give the matching result — each is a separate mark. Careful narrative that omits these earns nothing. List the steps plainly; don’t write an essay.',
    cite: MS('p.11'),
  },
};

// ───────────────── Bio11 · A labelled diagram can earn the marks ─────────────────

const BIO11: ScaleSession = {
  mode: 'scale',
  id: 'bio-diagram-in-lieu',
  subject: 'biology',
  level: 'common',
  title: 'A diagram can earn the marks',
  cue: 'Describe (with optional diagram)',
  question:
    'Describe how you carried out the osmosis activity — “you may include a labelled diagram if you wish.” Two candidates answer only with a drawing. Which one scores?',
  questionNote:
    'Question authored for this exercise. The rule is the SEC’s own line on these activity questions, quoted verbatim: “Points may be obtained from an appropriately labelled diagram.” The word that carries the condition is APPROPRIATELY LABELLED.',
  scale: {
    name: 'Activity · 3(3) · diagram permitted',
    levels: totalScale([0, 3, 6, 9]),
    notes: [
      'The scheme prints: “Points may be obtained from an appropriately labelled diagram.”',
      'So a clearly labelled diagram of the set-up can earn the same creditable points as sentences — set-up, control, apparatus.',
      'But the credit depends on the word appropriately LABELLED: an unlabelled sketch, however neat, carries no marks.',
      'A fully labelled set-up diagram here scores its three points (9); an unlabelled one scores 0.',
    ],
    cite: MS25('p.16 and p.17 (“Points may be obtained from an appropriately labelled diagram”)'),
  },
  scripts: [
    {
      id: 'bio11-a',
      label: 'Script A',
      persona: 'Fully labelled drawing, no prose',
      work: [
        'A clear diagram of the set-up:',
        '— Visking tubing labelled, containing sugar solution (labelled)',
        '— beaker of water labelled as the control set-up',
        'No written description.',
      ],
      keyLevelId: 'm9',
      keyNote:
        'No sentences at all — and full marks. The scheme lets you earn the points from an appropriately labelled diagram, and every element here is labelled, so the set-up, the control and the apparatus each score. 9. A good labelled diagram is worth exactly as much as the prose.',
      embodies: {
        behaviour: 'Answers a “describe” activity with a fully labelled diagram, which the scheme credits in place of prose.',
        cite: MS25('p.17'),
      },
    },
    {
      id: 'bio11-b',
      label: 'Script B',
      persona: 'Neat drawing, nothing labelled',
      work: [
        'A tidy, well-drawn sketch of tubing in a beaker.',
        'No labels on any part.',
      ],
      keyLevelId: 'm0',
      keyNote:
        'Just as neat — and 0. The concession is for an APPROPRIATELY LABELLED diagram; with no labels there is nothing for the examiner to credit. A picture only scores when its parts are named.',
      embodies: {
        behaviour: 'Submits an unlabelled diagram where the scheme requires an appropriately labelled one.',
        cite: MS25('p.16'),
      },
    },
  ],
  takeaway: {
    id: 'codex-bio11',
    rule: 'A labelled diagram can earn the write-up marks — but only if it is labelled.',
    detail:
      'On “describe” activities the scheme says points may be obtained from an appropriately labelled diagram, so a well-labelled drawing scores like the prose. The condition is the labels: an unlabelled sketch, however neat, earns nothing. If you draw instead of write, label every part.',
    cite: MS25('p.16 and p.17'),
  },
};

// ───────────────── Bio12 · A definition’s marks live in the qualifier ─────────────────

const BIO12: GridSession = {
  mode: 'grid',
  id: 'bio-definition-split',
  subject: 'biology',
  level: 'common',
  title: 'The definition’s marks are in the qualifier',
  cue: 'Explain the term',
  question: 'Explain the term osmosis.',
  questionNote:
    'Question authored for this exercise; the 2 + 4 split is taken verbatim from the 2025 osmosis definition (Q9(a)): “Movement of water 2 / from a region of higher water concentration to a region of lower water concentration across a selectively permeable membrane 4.”',
  grid: {
    perPoint: [
      { id: 'opener', label: 'Opening idea (“movement of water”)', marks: 2 },
      { id: 'qualifier', label: 'Precise qualifier (gradient + membrane)', marks: 4 },
    ],
    shorthand: 'definition · 2 + 4 (opener 2, qualifier 4)',
    ruleNote:
      'A six-mark definition need not split evenly. Here the easy opener — “movement of water” — is worth only 2; the precise qualifier — down the concentration gradient, across a selectively permeable membrane — carries 4. Stopping at the opener leaves two-thirds of the marks on the table. The precision is where the marks are.',
    cite: MS25('p.16 (osmosis definition — opener 2 + qualifier 4)'),
  },
  scripts: [
    {
      id: 'bio12-a',
      label: 'Script A',
      persona: 'Stops at the easy opener',
      attempts: [
        {
          id: 'bio12-a-1',
          text: 'Osmosis is the movement of water.',
          key: { opener: 2, qualifier: 0 },
          keyNote:
            'The opener is correct — 2 marks — but that is all it is. Without the gradient and the selectively permeable membrane, the 4-mark qualifier is untouched. A true but bare definition scores a third of the marks.',
        },
      ],
      embodies: {
        behaviour: 'Gives the easy opening idea of a definition and stops before the precise qualifier that carries most of the marks.',
        cite: MS25('p.16'),
      },
    },
    {
      id: 'bio12-b',
      label: 'Script B',
      persona: 'Full, precise definition',
      attempts: [
        {
          id: 'bio12-b-1',
          text: 'Osmosis is the movement of water from a region of higher water concentration to a region of lower water concentration across a selectively permeable membrane.',
          key: { opener: 2, qualifier: 4 },
          keyNote:
            'Opener plus the full qualifier — the gradient direction and the selectively permeable membrane. Both parts scored: 2 + 4 = 6. The marks were always in the precise second half.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-bio12',
    rule: 'A definition’s marks are usually in the qualifying clause, not the opener.',
    detail:
      'Definitions are often split unevenly — the easy opening idea is worth little and the precise qualifier carries most of the marks. “Movement of water” is 2; the gradient-and-membrane clause is 4. Always add the precise, qualifying detail — that is where the marks live.',
    cite: MS25('p.16'),
  },
};

// ───────────────── Bio13 · A graph is two marks — axes and type ─────────────────

const BIO13: GridSession = {
  mode: 'grid',
  id: 'bio-graph-parts',
  subject: 'biology',
  level: 'common',
  title: 'A graph is two marks, not one',
  cue: 'Draw (graph)',
  question:
    'Draw a suitable graph to represent the data of pulse rate against level of exercise (Resting, Moderate, Intense).',
  questionNote:
    'Question authored for this exercise; the two separate graph marks are taken verbatim from the 2023 exercise-physiology item (Q10(b)(ii)): “PR or BR on the y-axis and Resting, Moderate exercise and Intense exercise on the x-axis 3 / Bar chart or line graph or dot plot or other suitable graph drawn 3.”',
  grid: {
    perPoint: [
      { id: 'axes', label: 'Correct variables on correct axes', marks: 3 },
      { id: 'type', label: 'Suitable graph type drawn', marks: 3 },
    ],
    shorthand: 'graph · 3 + 3 (axes 3, type 3)',
    ruleNote:
      'A graph is not one holistic mark. One point is for the right variables on the right axes; a separate point is for drawing a suitable type of graph. A beautifully drawn chart with the axes unlabelled or swapped loses the axis mark; a correctly labelled but sloppy attempt still banks it. Label the axes AND choose a sensible chart.',
    cite: MS('p.12 (graph — correct axes 3 + suitable graph drawn 3)'),
  },
  scripts: [
    {
      id: 'bio13-a',
      label: 'Script A',
      persona: 'Beautiful bars, no axis labels',
      attempts: [
        {
          id: 'bio13-a-1',
          text: 'A neat, evenly-spaced bar chart — but neither axis is labelled with its variable.',
          key: { axes: 0, type: 3 },
          keyNote:
            'A suitable graph type is drawn, so the drawing mark is earned — 3. But with no variables named on the axes, the axis point is gone. Half the marks for a chart that looks finished but is not labelled.',
        },
      ],
      embodies: {
        behaviour: 'Draws a tidy graph but leaves the axes unlabelled, forfeiting the separate axis mark.',
        cite: MS('p.12'),
      },
    },
    {
      id: 'bio13-b',
      label: 'Script B',
      persona: 'Labelled axes, sensible chart',
      attempts: [
        {
          id: 'bio13-b-1',
          text: 'A bar chart with pulse rate on the y-axis and Resting / Moderate / Intense on the x-axis.',
          key: { axes: 3, type: 3 },
          keyNote:
            'Right variables on the right axes (3) and a suitable graph type drawn (3) — the two marks are independent, and both are here. Full 6.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-bio13',
    rule: 'A graph scores separately for its axes and for its type — label both.',
    detail:
      'The scheme marks a graph in two parts: one for the correct variables on the correct axes, one for drawing a suitable type of graph. A gorgeous chart with unlabelled axes loses half. Always name both axes and pick a sensible chart.',
    cite: MS('p.12'),
  },
};

// ───────────────── Bio14 · An equation is formulae + balancing ─────────────────

const BIO14: GridSession = {
  mode: 'grid',
  id: 'bio-equation-parts',
  subject: 'biology',
  level: 'common',
  title: 'An equation is two marks',
  cue: 'Write a balanced equation',
  question: 'Write a balanced chemical equation for photosynthesis.',
  questionNote:
    'Question authored for this exercise; the two-part marking is taken verbatim from the 2023 photosynthesis item (Q4(d)) — “(one point for correct formulas + one point for correct balancing)” — and the 2025 item (Q13(a)(ii)): “First point: formulae; second point: balancing 2(3).”',
  grid: {
    perPoint: [
      { id: 'formulae', label: 'Correct formulae', marks: 3 },
      { id: 'balancing', label: 'Correct balancing', marks: 3 },
    ],
    shorthand: 'equation · 3 + 3 (formulae 3, balancing 3)',
    ruleNote:
      'A balanced equation earns on two separate points: one for the correct chemical formulae, one for balancing them. Get the formulae right but miscount the coefficients and you still bank the formulae mark — a balancing slip does not wipe out the whole answer. So always write the reactants and products correctly first; then balance.',
    cite: MS('p.9 (photosynthesis equation — one point for correct formulae + one for correct balancing)'),
  },
  scripts: [
    {
      id: 'bio14-a',
      label: 'Script A',
      persona: 'Right formulae, unbalanced',
      attempts: [
        {
          id: 'bio14-a-1',
          text: 'CO₂ + H₂O → C₆H₁₂O₆ + O₂',
          key: { formulae: 3, balancing: 0 },
          keyNote:
            'Every formula is correct — reactants and products are right — so the formulae point is earned: 3. But the equation is not balanced (the coefficients are missing), so the balancing point is lost. A balancing slip costs one mark, not both.',
        },
      ],
      embodies: {
        behaviour: 'Writes correct formulae but forgets to balance, keeping one of the two available marks.',
        cite: MS25('p.22 (“First point: formulae; second point: balancing”, 2(3))'),
      },
    },
    {
      id: 'bio14-b',
      label: 'Script B',
      persona: 'Correct and balanced',
      attempts: [
        {
          id: 'bio14-b-1',
          text: '6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂',
          key: { formulae: 3, balancing: 3 },
          keyNote:
            'Correct formulae (3) and correctly balanced coefficients (3). Both points, full 6.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-bio14',
    rule: 'An equation scores separately for correct formulae and for balancing.',
    detail:
      'A chemical equation is two marks: one for the right formulae, one for balancing them. A balancing slip only costs the balancing mark — you keep the formulae mark. Write the reactants and products correctly first, then balance; don’t abandon an equation you can’t balance.',
    cite: MS('p.9'),
  },
};

// ───────────────── Bio15 · Name + Justify — the justification carries the marks ─────────────────

const BIO15: GridSession = {
  mode: 'grid',
  id: 'bio-name-justify',
  subject: 'biology',
  level: 'common',
  title: 'Naming it is the cheap part',
  cue: 'Identify & justify',
  question:
    'Which eye, A or B, is exposed to low light levels? Justify your answer.',
  questionNote:
    'Question authored for this exercise; the 1 + 2 mark split is taken verbatim from the 2025 eye item (Q14(b)(ii)) — “*B 1 / Justify: The pupil is larger (dilated) 2” — and the neuron item (Q14(c)(i)): “*X 1 / Justify … 2.” The identification is 1 mark; the justification is 2.',
  grid: {
    perPoint: [
      { id: 'name', label: 'Correct identification', marks: 1 },
      { id: 'justify', label: 'Correct justification', marks: 2 },
    ],
    shorthand: 'identify & justify · 1 + 2 (name 1, justify 2)',
    ruleNote:
      'On “name it and justify” the identification is often just 1 mark and the justification is worth 2 — twice as much. Guessing the right letter with no reason banks the small mark and forfeits the larger one. The “justify your answer” is not a courtesy; it is where most of the marks are.',
    cite: MS25('p.24 (eye — “*B 1 / Justify … 2”)'),
  },
  scripts: [
    {
      id: 'bio15-a',
      label: 'Script A',
      persona: 'Names it, gives no reason',
      attempts: [
        {
          id: 'bio15-a-1',
          text: 'B.',
          key: { name: 1, justify: 0 },
          keyNote:
            'The right eye is named — 1 mark — but “justify your answer” is left blank, and that was the 2-mark part. 1 of 3. A correct one-word answer here throws away two-thirds of the marks.',
        },
      ],
      embodies: {
        behaviour: 'Gives the correct identification but omits the justification, which carries the larger mark.',
        cite: MS25('p.25 (neuron — “*X 1 / Justify … 2”)'),
      },
    },
    {
      id: 'bio15-b',
      label: 'Script B',
      persona: 'Names it and justifies',
      attempts: [
        {
          id: 'bio15-b-1',
          text: 'B — its pupil is larger (dilated), so it is letting in more light, which means it was in low light.',
          key: { name: 1, justify: 2 },
          keyNote:
            'The identification (1) plus a correct justification — the dilated pupil (2). Both parts scored: full 3. The reason was worth more than the answer.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-bio15',
    rule: 'On “identify and justify”, the justification usually carries most of the marks.',
    detail:
      'Naming the right letter is often only 1 mark; the “justify your answer” is worth 2. A bare correct answer banks a third of the marks and leaves the rest. Always give the reason — it is the bigger half of the question.',
    cite: MS25('p.24 and p.25'),
  },
};

export const BIOLOGY_CHAIR: ChairSubject = {
  id: 'biology',
  label: 'Biology',
  tagline: 'Points, context, notation and the penalty rules that quietly cost marks.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [BIO1, BIO2, BIO3, BIO4, BIO5, BIO6, BIO7, BIO8, BIO9, BIO10, BIO11, BIO12, BIO13, BIO14, BIO15],
  sources: [
    { label: 'SEC LC Biology HL marking scheme 2023, Deferred sitting (examiner-reports/biology/2023-marking-scheme)' },
    { label: 'SEC LC Biology HL marking scheme 2025 (examiner-reports/biology/2025-hl-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach Biology’s general marking conventions — the points and graduated-mark notation, the context rule, the cancelled-answer and “must match” consistency rules, the Best-of selection rubric, the diagram thresholds and the labelled-diagram concession, the experiment-checklist and split-mark structures (definition, graph, equation, name-and-justify), and the Section A / Sections B/C penalty rules — which the scheme applies at both Higher and Ordinary level. They are verified against the 2023 and 2025 Higher Level schemes; level-specific worked questions are being added.',
};
