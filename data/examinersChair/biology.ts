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

export const BIOLOGY_CHAIR: ChairSubject = {
  id: 'biology',
  label: 'Biology',
  tagline: 'Points, context and the penalty rules that quietly cost marks.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [BIO1, BIO2, BIO3],
  sources: [
    { label: 'SEC LC Biology HL marking scheme 2023, Deferred sitting (examiner-reports/biology/2023-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach Biology’s general marking conventions — the points notation, the context rule, and the Section A / Sections B/C penalty rules — which the scheme applies at both Higher and Ordinary level. They are verified against the 2023 Higher Level scheme; level-specific worked questions are being added.',
};
