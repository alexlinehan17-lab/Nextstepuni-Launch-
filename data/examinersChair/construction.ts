/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Construction Studies (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (drawings marked as a checklist of named elements with a
 * fixed draw+annotation split, the note+sketch split that halves text-only
 * answers, and per-step calculation marking) is the real SEC system, cited to:
 *  - SEC LC Construction Studies HL marking scheme 2025 —
 *    examiner-reports/construction-studies/2025-marking-scheme.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC Construction Studies HL marking scheme 2025, ${p}` });

const ladder = (marks: number[]): ScaleLevel[] =>
  marks.map(m => ({ id: `m${m}`, label: `${m} marks`, annotation: `${m}`, marks: m }));

// ─────────────── CS1 · Labels are a quarter of every element ───────────────

const CS1: GridSession = {
  mode: 'grid',
  id: 'cs-labels',
  subject: 'construction-studies',
  level: 'common',
  title: 'A quarter of the marks are labels',
  cue: 'Draw the detail',
  question: 'A sectional detail is marked element by element, and each element is worth 3 for the drawing plus 1 for its annotation. A candidate draws four elements beautifully and correctly — but labels none of them.',
  questionNote:
    'Scenario authored for this exercise. Construction Studies marks big drawings as a checklist of named elements, each split 3 (drawing) + 1 (annotation); rubric makes labelling mandatory.',
  grid: {
    perPoint: [
      { id: 'e1', label: 'Element 1 — annotation', marks: 1 },
      { id: 'e2', label: 'Element 2 — annotation', marks: 1 },
      { id: 'e3', label: 'Element 3 — annotation', marks: 1 },
      { id: 'e4', label: 'Element 4 — annotation', marks: 1 },
    ],
    shorthand: 'each element: draw 3 + annotate 1',
    ruleNote:
      'The annotation is a quarter of every element’s marks, and it’s marked separately from the line-work. A flawless but unlabelled section forfeits every annotation mark — a routine, avoidable loss on every drawing.',
    cite: MS('p.37, p.43 (draw + annotation split)'),
  },
  scripts: [
    {
      id: 'cs1-a',
      label: 'Script A',
      persona: 'Perfect drawing, no labels',
      attempts: [
        {
          id: 'cs1-a-1',
          text: 'Four elements drawn accurately and neatly — none labelled or annotated.',
          key: { e1: 0, e2: 0, e3: 0, e4: 0 },
          keyNote: 'The drawing marks are earned, but every annotation mark — a quarter of each element — is gone. Naming each element (DPC, insulation, wall tie, lintel) would have added them for a few seconds’ writing. Labelling is mandatory and it’s free marks.',
        },
      ],
      embodies: {
        behaviour: 'Draws elements well but leaves them unlabelled, forfeiting the separate annotation marks.',
        cite: MS('p.37'),
      },
    },
    {
      id: 'cs1-b',
      label: 'Script B',
      persona: 'Drawn and labelled',
      attempts: [
        {
          id: 'cs1-b-1',
          text: 'The same four elements, each clearly labelled — DPC, insulation, wall tie, lintel.',
          key: { e1: 1, e2: 1, e3: 1, e4: 1 },
          keyNote: 'Every annotation mark banked on top of the drawing marks. The labels cost seconds and are guaranteed marks.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-cs1',
    rule: 'Label every element — a quarter of the marks depend on it.',
    detail:
      'Construction Studies drawings split each element into drawing (3) and annotation (1). Unlabelled drawings forfeit every annotation mark however good the line-work. Name every component you draw.',
    cite: MS('p.37'),
  },
};

// ─────────────── CS2 · The sketch is half the marks ───────────────

const CS2: ScaleSession = {
  mode: 'scale',
  id: 'cs-sketch',
  subject: 'construction-studies',
  level: 'common',
  title: 'No sketch, half the marks',
  cue: 'Describe with the aid of a sketch',
  question: 'A “describe, with the aid of a sketch” sub-part is marked 3 for the note and 3 for the sketch. A candidate writes an excellent, detailed note — but draws no sketch. What’s the maximum they can score?',
  questionNote:
    'Scenario authored for this exercise. Construction Studies “describe with a sketch” parts default to a 3 (note) + 3 (sketch) split; a text-only answer forfeits the sketch half.',
  scale: {
    name: 'Note + sketch · /6',
    levels: ladder([3, 6]),
    notes: [
      'The default split is note 3 + sketch 3.',
      'The question explicitly asks for a sketch — the words “with the aid of a sketch” are a mark instruction.',
      'A text-only answer, however good, caps at 3 of 6.',
    ],
    cite: MS('p.38, p.40 (note + sketch split)'),
  },
  scripts: [
    {
      id: 'cs2-a',
      label: 'The answer',
      persona: 'Great note, no sketch',
      work: ['A detailed, accurate written description.', 'No sketch drawn.'],
      keyLevelId: 'm3',
      keyNote:
        'Capped at 3 of 6 — the sketch is half the marks, and “with the aid of a sketch” is a mark instruction, not a suggestion. A rough, labelled sketch alongside the note would have doubled the score. When a question asks for a sketch, always draw one, however quick.',
      embodies: {
        behaviour: 'Answers a “describe with a sketch” part in text only — capping at half marks.',
        cite: MS('p.38'),
      },
    },
  ],
  takeaway: {
    id: 'codex-cs2',
    rule: 'If it asks for a sketch, the sketch is half the marks.',
    detail:
      '“Describe with the aid of a sketch” splits 3 note + 3 sketch — a text-only answer forfeits half. Always draw the sketch, even a rough labelled one; the words are a mark instruction.',
    cite: MS('p.38'),
  },
};

// ─────────────── CS3 · Show the U-value working ───────────────

const CS3: ScaleSession = {
  mode: 'scale',
  id: 'cs-uvalue',
  subject: 'construction-studies',
  level: 'higher',
  title: 'Every layer is a mark',
  cue: 'Calculate the U-value',
  question: 'A U-value calculation is marked per step: each material layer’s thermal resistance is its own 3-mark tick, and each substitution scores separately — around 33 marks across the working. A candidate writes only the correct final U-value, with no working. Roughly what does it score?',
  questionNote:
    'Scenario authored for this exercise. The U-value question is marked step-by-step — each resistance and each substitution is its own tick — so a bare answer forfeits the bulk of the marks.',
  scale: {
    name: 'U-value · per-step',
    levels: ladder([3, 20, 33]),
    notes: [
      'Each material-layer resistance = its own 3-mark tick; each substitution scores separately.',
      'The marks are spread across ~11 steps, not attached to the final number.',
      'A correct final U-value with no working banks almost none of them.',
    ],
    cite: MS('p.41 (per-step U-value marking, Q5)'),
  },
  scripts: [
    {
      id: 'cs3-a',
      label: 'The answer',
      persona: 'Final answer only',
      work: ['U = 0.24 W/m²K', '(correct — but no working shown)'],
      keyLevelId: 'm3',
      keyNote:
        'Almost nothing — the marks live in each layer’s resistance and each substitution, and none are on the page. A correct final number can’t reclaim the ~33 marks spread across the steps that produced it. Lay out every layer’s resistance and every substitution; it’s where the marks are.',
      embodies: {
        behaviour: 'Writes only the final U-value with no working — forfeiting the per-step marks.',
        cite: MS('p.41'),
      },
    },
  ],
  takeaway: {
    id: 'codex-cs3',
    rule: 'Show every layer — the U-value marks are in the steps.',
    detail:
      'The U-value question ticks each material layer’s resistance and each substitution separately (~33 marks), not the final number. Set out every layer and every substitution; a bare answer banks almost nothing.',
    cite: MS('p.41'),
  },
};

export const CONSTRUCTION_CHAIR: ChairSubject = {
  id: 'construction-studies',
  label: 'Construction Studies',
  tagline: 'Label every element, sketch when asked, show every layer.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [CS1, CS2, CS3],
  sources: [
    { label: 'SEC LC Construction Studies HL marking scheme 2025 (examiner-reports/construction-studies/2025-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the general conventions — the element draw+annotation split, the note+sketch split and per-step calculation marking — which apply at both Higher and Ordinary level. Verified against the 2025 Higher Level scheme; level-specific worked questions are being added.',
};
