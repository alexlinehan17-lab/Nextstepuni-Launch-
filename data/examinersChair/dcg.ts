/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Design & Communication Graphics (HL) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (drawings decomposed into independently-scored construction
 * steps, construction marked separately from and above the finished curve, and
 * standalone "use of appropriate method" granules) is the real SEC system,
 * cited to:
 *  - SEC LC DCG HL marking scheme 2025 —
 *    examiner-reports/dcg/2025-marking-scheme.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC DCG HL marking scheme 2025, ${p}` });

const ladder = (marks: number[]): ScaleLevel[] =>
  marks.map(m => ({ id: `m${m}`, label: `${m} marks`, annotation: `${m}`, marks: m }));

// ─────────────── DCG1 · Construction outscores the curve ───────────────

const DCG1: GridSession = {
  mode: 'grid',
  id: 'dcg-construction',
  subject: 'dcg',
  level: 'common',
  title: 'The construction lines are the marks',
  cue: 'Draw the locus',
  question: 'A part is worth 12 marks: 8 for the construction that locates the points, and 4 for drawing the final smooth curve through them. A candidate, wanting a clean sheet, does the construction lightly then erases all of it, leaving only the neat final curve.',
  questionNote:
    'Scenario authored for this exercise. DCG marks the construction separately from — and above — the finished curve; the construction that locates the points is the larger award.',
  grid: {
    perPoint: [
      { id: 'construction', label: 'Construction to locate points', marks: 8 },
      { id: 'curve', label: 'Draw the final curve', marks: 4 },
    ],
    shorthand: 'construction 8 + curve 4',
    ruleNote:
      'The construction is worth twice the finished curve, and it is marked on what’s visible on the page. Erasing your construction lines erases the marks that reward them — leave them in, lightly but clearly.',
    cite: MS('p.4 (construction vs curve split, A-2)'),
  },
  scripts: [
    {
      id: 'dcg1-a',
      label: 'Script A',
      persona: 'Erased the construction',
      attempts: [
        {
          id: 'dcg1-a-1',
          text: 'A neat final curve — but every construction line has been rubbed out for a clean look.',
          key: { construction: 0, curve: 4 },
          keyNote: 'The curve earns its 4, but the 8 construction marks are gone — the examiner marks what’s on the page, and the construction that located the points isn’t there. 4 of 12. A clean sheet cost two-thirds of the marks. Leave the construction lines in.',
        },
      ],
      embodies: {
        behaviour: 'Erases the construction lines, forfeiting the larger construction award.',
        cite: MS('p.4'),
      },
    },
    {
      id: 'dcg1-b',
      label: 'Script B',
      persona: 'Construction left visible',
      attempts: [
        {
          id: 'dcg1-b-1',
          text: 'The construction lines that locate the points are left in place, with the final curve drawn through them.',
          key: { construction: 8, curve: 4 },
          keyNote: 'Both the construction and the curve are on the page. Full 12 — the visible construction is what carries most of the marks.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-dcg1',
    rule: 'Never erase your construction lines.',
    detail:
      'In DCG the construction is marked separately from the finished drawing — and it’s usually worth more. Erasing your construction for a tidy sheet erases those marks. Leave the lines in, lightly but visible.',
    cite: MS('p.4'),
  },
};

// ─────────────── DCG2 · Every step scores ───────────────

const DCG2: ScaleSession = {
  mode: 'scale',
  id: 'dcg-steps',
  subject: 'dcg',
  level: 'common',
  title: 'No drawing is all-or-nothing',
  cue: 'Solve the drawing',
  question: 'A hard 20-mark drawing is decomposed into several named construction steps, each scored independently. A candidate can’t see how to finish it, so leaves the whole part blank. They could have completed the first few steps. What does the blank score versus a genuine partial attempt?',
  questionNote:
    'Scenario authored for this exercise. Every DCG question is broken into named steps that each score on their own — there are no all-or-nothing drawing parts.',
  scale: {
    name: 'Stepped drawing · /20',
    levels: ladder([0, 12, 20]),
    notes: [
      'The drawing is decomposed into named steps, each scored independently.',
      'Completing the early steps banks their marks even if you can’t finish.',
      'A blank scores 0; a genuine partial attempt scores every step it reaches.',
    ],
    cite: MS('p.4–5 (stepped drawing questions)'),
  },
  scripts: [
    {
      id: 'dcg2-a',
      label: 'The answer',
      persona: 'Blanks the hard part',
      work: ['Couldn’t see how to finish, so left the whole part blank.', 'The first few steps were within reach.'],
      keyLevelId: 'm0',
      keyNote:
        '0 — a blank scores nothing, but this part was never all-or-nothing. The setup steps (datum lines, locating the given points, the first construction) each carry their own marks, and a partial attempt would have banked them. In DCG, always start the drawing: the early steps are the reachable marks.',
      embodies: {
        behaviour: 'Leaves a hard drawing blank instead of banking the independently-scored early steps.',
        cite: MS('p.4'),
      },
    },
  ],
  takeaway: {
    id: 'codex-dcg2',
    rule: 'Start every drawing — the early steps score on their own.',
    detail:
      'DCG questions are built from named steps, each marked independently, so no drawing is all-or-nothing. Even if you can’t finish, set up the datums and do the first constructions — those steps bank real marks a blank throws away.',
    cite: MS('p.4'),
  },
};

// ─────────────── DCG3 · Method scores ───────────────

const DCG3: ScaleSession = {
  mode: 'scale',
  id: 'dcg-method',
  subject: 'dcg',
  level: 'common',
  title: 'Show the method, score the method',
  cue: 'Determine',
  question: 'A part carries a standalone mark for “use of appropriate method to determine the true length”, separate from getting the final answer. A candidate sets up the correct method (rotation/auxiliary view) but runs out of time before finishing. Does the method score on its own?',
  questionNote:
    'Scenario authored for this exercise. DCG schemes include standalone “use of appropriate method” granules that reward the technique chosen, independent of the finished result.',
  scale: {
    name: 'Method granule',
    levels: ladder([0, 4]),
    notes: [
      'The scheme awards a standalone mark for using the appropriate method.',
      'This granule rewards the technique you set up, not only the final result.',
      'So a correct method, clearly shown, scores even if the part isn’t finished.',
    ],
    cite: MS('p.4 (standalone “use of appropriate method” marks, A-4)'),
  },
  scripts: [
    {
      id: 'dcg3-a',
      label: 'The answer',
      persona: 'Right method, out of time',
      work: ['Sets up the correct true-length method (auxiliary view).', 'Runs out of time before completing it.'],
      keyLevelId: 'm4',
      keyNote:
        'The method mark is banked — the scheme rewards choosing and showing the right technique, separately from the finished answer. So even an unfinished part pays if the approach is visibly correct. Always commit your method to the page early; it scores on its own.',
      embodies: {
        behaviour: 'Sets up the correct method but doesn’t finish — the standalone method mark still scores.',
        cite: MS('p.4'),
      },
    },
  ],
  takeaway: {
    id: 'codex-dcg3',
    rule: 'The method scores separately from the answer.',
    detail:
      'DCG gives standalone marks for using the appropriate method, independent of the finished result. Set up and show your technique early — it banks marks even when you run out of time to complete the drawing.',
    cite: MS('p.4'),
  },
};

export const DCG_CHAIR: ChairSubject = {
  id: 'dcg',
  label: 'Design & Communication Graphics',
  tagline: 'Construction over curve, every step scores, method pays.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [DCG1, DCG2, DCG3],
  sources: [
    { label: 'SEC LC DCG HL marking scheme 2025 (examiner-reports/dcg/2025-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the general drawing-marking conventions — construction marked above the finished curve, independently-scored steps and standalone method marks — which apply at both Higher and Ordinary level. Verified against the 2025 Higher Level scheme; level-specific worked drawings are being added.',
};
