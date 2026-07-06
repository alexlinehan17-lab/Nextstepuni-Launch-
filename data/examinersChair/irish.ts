/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Irish / Gaeilge (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the composition's Stíl + Ionramháil + Cumas Gaeilge split
 * with language as 80 of 100, the wrong-genre Stíl-zero rule, and the
 * comprehension "own words" gate) is the real SEC system, cited to:
 *  - SEC LC Irish HL marking scheme 2025 (An Ardteistiméireacht, Scéim
 *    Mharcála, Ardleibhéal, Gaeilge) — examiner-reports/irish/2025-marking-scheme.*
 * (Note: the oral / Béaltriail is marked on a separate scheme not covered here.)
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC Irish HL marking scheme 2025, ${p}` });

// ─────────────── Ir1 · Language is the mark ───────────────

const GAEILGE_BANDS: ScaleLevel[] = [
  { id: 'iseal', label: 'Íseal (low)', annotation: '25', marks: 25 },
  { id: 'mean', label: 'Meánach (middle)', annotation: '48', marks: 48 },
  { id: 'ard', label: 'Ard (high)', annotation: '72', marks: 72 },
];

const IR1: ScaleSession = {
  mode: 'scale',
  id: 'ir-cumas-gaeilge',
  subject: 'irish',
  level: 'common',
  title: 'Great ideas, shaky Irish',
  cue: 'Ceapadóireacht',
  question: 'A composition has genuinely interesting, well-organised ideas — but the Irish itself is error-strewn: wrong verb tenses, shaky syntax, misused prepositions. Of the 100 composition marks, 80 are for Cumas Gaeilge (command of Irish). Which Cumas Gaeilge band does it land in?',
  questionNote:
    'Scenario authored for this exercise. The composition is marked Stíl 5 + Ionramháil Ábhair 15 + Cumas Gaeilge 80 — so command of the language is 80 of the 100 marks, driven by vocabulary range and accuracy.',
  scale: {
    name: 'Cumas Gaeilge · /80 · bands',
    levels: GAEILGE_BANDS,
    notes: [
      'Composition = Stíl 5 + Ionramháil Ábhair 15 + Cumas Gaeilge 80.',
      'Cumas Gaeilge (80 marks) is judged on richness AND accuracy of the Irish.',
      'Repeated errors in tense, syntax and prepositions hold the answer in the lower band, however good the ideas.',
      'Ideas are rewarded under Ionramháil (15) — but they can’t rescue the 80-mark language band.',
    ],
    cite: MS('p.13 (Cumas Gaeilge weighting and bands)'),
  },
  scripts: [
    {
      id: 'ir1-a',
      label: 'The composition',
      persona: 'Ideas strong, Irish weak',
      work: [
        'Interesting, well-structured ideas.',
        'But frequent errors: wrong tenses, weak syntax, misused prepositions.',
      ],
      keyLevelId: 'iseal',
      keyNote:
        'Lower Cumas Gaeilge band — because 80 of the 100 marks reward command of Irish, and repeated accuracy errors are exactly what that band measures. The ideas earn their marks under Ionramháil (15), but they can’t lift the language score. In Irish composition, the surest marks come from writing accurate Irish you control, not ambitious Irish you don’t.',
      embodies: {
        behaviour: 'Strong ideas undermined by weak language accuracy — where 80% of the mark lives.',
        cite: MS('p.13'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ir1',
    rule: 'In Irish composition, the language is the mark.',
    detail:
      'Cumas Gaeilge is 80 of the 100 composition marks — accuracy and range of Irish. Write Irish you control: reliable tenses, syntax and prepositions beat ambitious sentences riddled with errors. Ideas alone can’t lift the language band.',
    cite: MS('p.13'),
  },
};

// ─────────────── Ir2 · Wrong genre = Style 0 ───────────────

const IR2: ScaleSession = {
  mode: 'scale',
  id: 'ir-genre',
  subject: 'irish',
  level: 'common',
  title: 'Right title, wrong form',
  cue: 'Ceapadóireacht',
  question: 'The chosen composition title asks for a speech (óráid). The candidate writes a fluent, accurate piece — but as a personal essay (aiste), with none of the features of a speech (no address to an audience, no rhetorical opening). What does the Stíl (Style) mark, out of 5, become?',
  questionNote:
    'Scenario authored for this exercise. Style marks genre discipline, not quality: writing the wrong genre for the chosen title scores Stíl 0.',
  scale: {
    name: 'Stíl · /5',
    levels: [
      { id: 'm0', label: '0 (wrong genre)', annotation: '0', marks: 0 },
      { id: 'm5', label: '5 (correct genre)', annotation: '5', marks: 5 },
    ],
    notes: [
      'Stíl (5 marks) rewards using the right genre for the chosen title — not the quality of writing.',
      'A speech title needs the features of a speech; written as an essay, Stíl = 0.',
      'The Cumas Gaeilge and Ionramháil marks are judged separately.',
    ],
    cite: MS('p.14 (Stíl / genre rule)'),
  },
  scripts: [
    {
      id: 'ir2-a',
      label: 'The composition',
      persona: 'Fluent — wrong form',
      work: [
        'Fluent, accurate Irish.',
        'Title asked for a speech (óráid); written as a personal essay (aiste).',
        'No audience address, no rhetorical features.',
      ],
      keyLevelId: 'm0',
      keyNote:
        'Stíl 0 — the genre is wrong for the title, and Style marks the form, not the fluency. The language marks may still be strong, but 5 easy marks are gone for want of a speech’s opening and audience address. Match the form the title asks for: speech, letter, diary, debate, essay.',
      embodies: {
        behaviour: 'Writes the wrong genre for the chosen title — Stíl scores 0.',
        cite: MS('p.14'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ir2',
    rule: 'Write the genre the title asks for.',
    detail:
      'Stíl rewards using the correct form — speech, letter, diary, debate — not how well you write. Pick a title whose genre you can produce, and build in that genre’s features. Wrong form is an automatic Stíl 0.',
    cite: MS('p.14'),
  },
};

// ─────────────── Ir3 · Own words gate ───────────────

const IR3: ScaleSession = {
  mode: 'scale',
  id: 'ir-own-words',
  subject: 'irish',
  level: 'common',
  title: 'In your own words',
  cue: 'Léamhthuiscint',
  question: 'A reading-comprehension question (worth 12 marks) explicitly requires the answer in the candidate’s own words. The relevant idea is clearly in the passage, and the candidate copies the sentence out word for word. What does it score?',
  questionNote:
    'Scenario authored for this exercise. Comprehension Q6(b) is worth 12 marks and must be in the candidate’s own words; lifting the passage verbatim there scores nothing.',
  scale: {
    name: 'Comprehension (own words) · /12',
    levels: [
      { id: 'm0', label: '0 (copied)', annotation: '0', marks: 0 },
      { id: 'm7', label: '7 (partly reworded)', annotation: '7', marks: 7 },
      { id: 'm12', label: '12 (own words)', annotation: '12', marks: 12 },
    ],
    notes: [
      'This 12-mark question requires the answer in the candidate’s own words.',
      'Copying the passage verbatim does not demonstrate understanding — it scores nothing here.',
      'Rewording the idea in controlled Irish is what unlocks the marks.',
    ],
    cite: MS('p.16 (Q6(b), own words, 12 marks)'),
  },
  scripts: [
    {
      id: 'ir3-a',
      label: 'The answer',
      persona: 'Copies the passage',
      work: ['Lifts the relevant sentence from the text, word for word.'],
      keyLevelId: 'm0',
      keyNote:
        '0 of 12 — the question is gated behind “own words”, and a verbatim lift shows nothing about understanding. Even a simple reworded version in accurate Irish would score. On “own words” questions, never copy: paraphrase the idea in language you control.',
      embodies: {
        behaviour: 'Copies the passage on an “own words” question — which scores 0.',
        cite: MS('p.16'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ir3',
    rule: 'On “own words” questions, never copy.',
    detail:
      'Irish comprehension gates some marks behind answering in your own words — a verbatim lift scores 0 there. Reword the idea in accurate, controlled Irish; understanding shown is what the marks reward.',
    cite: MS('p.16'),
  },
};

export const IRISH_CHAIR: ChairSubject = {
  id: 'irish',
  label: 'Irish',
  tagline: 'Where language accuracy, genre and “own words” win the marks.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [IR1, IR2, IR3],
  sources: [
    { label: 'SEC LC Irish HL marking scheme 2025 (examiner-reports/irish/2025-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the written-paper marking conventions — the language-weighted composition, genre discipline and the “own words” rule — which apply at both Higher and Ordinary level (the oral is marked on a separate scheme). Verified against the 2025 Higher Level scheme; level-specific worked examples are being added.',
};
