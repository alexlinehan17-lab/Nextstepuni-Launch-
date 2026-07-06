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

// ─────────────── DCG4 · Hidden detail is its own mark ───────────────

const DCG4: GridSession = {
  mode: 'grid',
  id: 'dcg-hidden-detail',
  subject: 'dcg',
  level: 'common',
  title: 'The dashed lines are worth a mark',
  cue: 'Complete the elevation',
  question: 'Completing an elevation is worth 4 marks: 3 for drawing the visible outline, and a separate 1 for showing the hidden detail as dashed lines. A candidate draws a crisp, correct visible outline but leaves the hidden edges off — they looked cluttered, and it’s "only one mark".',
  questionNote:
    'Scenario authored for this exercise. In DCG, presentation conventions like hidden detail are itemised as their own small granules — usually 1 mark — separate from the visible drawing.',
  grid: {
    perPoint: [
      { id: 'elevation', label: 'Draw the visible elevation', marks: 3 },
      { id: 'hidden', label: 'Show the hidden detail (dashed)', marks: 1 },
    ],
    shorthand: 'elevation 3 + hidden detail 1',
    ruleNote:
      'Hidden detail is scored as its own granule, separate from the visible outline. Leaving the dashed lines off doesn’t cost style points — it forfeits a specific, guaranteed mark the scheme has set aside for them. Put the hidden edges in every time.',
    cite: MS('p.5 (A-3(a)(v) hidden-detail granule)'),
  },
  scripts: [
    {
      id: 'dcg4-a',
      label: 'Script A',
      persona: 'Leaves the hidden edges off',
      attempts: [
        {
          id: 'dcg4-a-1',
          text: 'A crisp, correct visible outline — but the hidden edges are left off to keep the view clean.',
          key: { elevation: 3, hidden: 0 },
          keyNote: 'The visible outline earns its 3, but the hidden-detail mark is a separate granule and there are no dashed lines to award it to. 3 of 4 — a guaranteed mark thrown away for tidiness. Hidden detail is never optional decoration; it’s itemised in the scheme.',
        },
      ],
      embodies: {
        behaviour: 'Omits hidden detail, forfeiting the itemised presentation-convention mark.',
        cite: MS('p.5'),
      },
    },
    {
      id: 'dcg4-b',
      label: 'Script B',
      persona: 'Adds the hidden detail',
      attempts: [
        {
          id: 'dcg4-b-1',
          text: 'The visible outline is drawn, then the hidden edges are added as dashed lines.',
          key: { elevation: 3, hidden: 1 },
          keyNote: 'Both granules are on the page — outline and hidden detail. Full 4. The dashed lines take seconds and bank a mark the scheme has reserved for exactly that.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-dcg4',
    rule: 'Always add the hidden detail — it’s a mark of its own.',
    detail:
      'DCG itemises presentation conventions like hidden detail as their own small granules, separate from the visible drawing. The dashed hidden edges are a guaranteed mark that time-pressed candidates routinely skip. Draw them in every time — they cost seconds and pay a mark.',
    cite: MS('p.5'),
  },
};

// ─────────────── DCG5 · Assembly: position beats polish ───────────────

const DCG5: GridSession = {
  mode: 'grid',
  id: 'dcg-assembly',
  subject: 'dcg',
  level: 'common',
  title: 'In an assembly, position beats polish',
  cue: 'Complete the sectional assembly',
  question:
    'A 60-mark sectional assembly gives 7 marks for the relative positioning of the main components and a separate 5 marks for the inner detail of the main body. A candidate renders the inner detail of one part beautifully but seats the components in the wrong positions relative to each other.',
  questionNote:
    'Scenario authored for this exercise. In a DCG sectional-assembly drawing the relative positioning of the components is itemised as its own granule — the single largest in the question — separate from the detail of any one part.',
  grid: {
    perPoint: [
      { id: 'positioning', label: 'Relative positioning of main components', marks: 7 },
      { id: 'detail', label: 'Inner detail of the main body', marks: 5 },
    ],
    shorthand: 'relative positioning 7 + inner detail 5',
    ruleNote:
      'The relative positioning of the components is scored on its own — and it is the biggest single granule in the assembly. Detailing one part perfectly while the parts sit in the wrong places banks the detail mark but forfeits the larger positioning mark. Get the layout of the components right first, then detail them.',
    cite: MS('p.13 (C-5 assembly: relative positioning of main components 7, inner detail of main body 5)'),
  },
  scripts: [
    {
      id: 'dcg5-a',
      label: 'Script A',
      persona: 'Detail first, layout wrong',
      attempts: [
        {
          id: 'dcg5-a-1',
          text: 'The inner detail of the main body is drawn cleanly and correctly, but the components are seated in the wrong positions relative to each other.',
          key: { positioning: 0, detail: 5 },
          keyNote:
            'The inner detail earns its 5, but the relative positioning of the components is a separate — and larger — granule, and the parts are in the wrong places. 5 of 12. The single biggest mark in an assembly is arranging the components correctly; polish on one part can’t buy it back.',
        },
      ],
      embodies: {
        behaviour: 'Details one part well but mispositions the components, forfeiting the larger relative-positioning granule.',
        cite: MS('p.13'),
      },
    },
    {
      id: 'dcg5-b',
      label: 'Script B',
      persona: 'Layout first',
      attempts: [
        {
          id: 'dcg5-b-1',
          text: 'The components are seated in their correct relative positions, then the inner detail of the main body is drawn.',
          key: { positioning: 7, detail: 5 },
          keyNote:
            'Both granules are on the page — correct relative positioning and the inner detail. Full 12. Fixing the layout first secured the largest mark before any detail was drawn.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-dcg5',
    rule: 'In an assembly, get the components’ positions right first.',
    detail:
      'DCG scores the relative positioning of an assembly’s components as its own granule — usually the single largest in the question — separate from the detail of any one part. Seat the components correctly before you detail them; a beautifully drawn part in the wrong place still forfeits the bigger positioning mark.',
    cite: MS('p.13'),
  },
};

// ─────────────── DCG6 · A development is true lengths, not a sketch ───────────────

const DCG6: ScaleSession = {
  mode: 'scale',
  id: 'dcg-development',
  subject: 'dcg',
  level: 'common',
  title: 'A development is true lengths, not a sketch',
  cue: 'Develop the surface',
  question:
    'A surface development is scored for its accuracy scaffold: locating the apex (1), transferring the longest true generator length (2), establishing the elements (4), then completing it. A candidate, short on time, sketches a development that looks the right shape by eye without transferring any true lengths.',
  questionNote:
    'Scenario authored for this exercise. In DCG the surface-development marks are attached to the accuracy scaffold — transferred true lengths and set-up elements — not to a shape that merely looks right.',
  scale: {
    name: 'Surface development · /10',
    levels: ladder([0, 7, 10]),
    notes: [
      'The development is scored for transferred true lengths, not for looking right.',
      'Locating the apex, transferring the true generator length and establishing the elements each carry their own marks — the setup banks 7 before the outline is completed.',
      'A shape sketched by eye without the transfers scores 0; do the transfers to bank the setup, then complete the outline to finish.',
    ],
    cite: MS('p.11 (C-3(c) surface development: apex 1, longest generator 2, 12 elements 4, complete 2)'),
  },
  scripts: [
    {
      id: 'dcg6-a',
      label: 'The answer',
      persona: 'Sketched it by eye',
      work: [
        'Draws a development that looks the right shape.',
        'Never transfers the true generator lengths or steps out the elements.',
      ],
      keyLevelId: 'm0',
      keyNote:
        '0 — the development marks live in the accuracy scaffold, not the outline. With no true-length transfers and no elements established, there is nothing for the apex, generator and element granules to reward, however right the shape looks. Transfer the true lengths and step out the elements first: that setup banks 7 before you complete the outline.',
      embodies: {
        behaviour: 'Sketches a development by eye instead of transferring the scored true lengths and establishing the elements.',
        cite: MS('p.11'),
      },
    },
  ],
  takeaway: {
    id: 'codex-dcg6',
    rule: 'A development scores the true-length transfers, not the shape.',
    detail:
      'DCG attaches surface-development marks to the accuracy scaffold — locating the apex, transferring the true generator length, establishing the elements — not to an outline that merely looks right. Step the transfers out on the page; that setup banks most of the marks before you complete the development.',
    cite: MS('p.11'),
  },
};

// ─────────────── DCG7 · Divide into the number it asks for ───────────────

const DCG7: GridSession = {
  mode: 'grid',
  id: 'dcg-divisions',
  subject: 'dcg',
  level: 'common',
  title: 'Divide into the number it asks for',
  cue: 'Divide the circle',
  question:
    'A locus construction gives 8 marks for drawing the given diagram and a separate 3 marks for “division of circle into equal parts (12 minimum)”. A candidate draws the diagram correctly but, rushing, divides the circle into only 8 equal parts instead of the required 12.',
  questionNote:
    'Scenario authored for this exercise. DCG construction steps that divide a circle or diagram into equal parts specify a minimum count (e.g. “12 minimum”, “min. 7 incl. end points”); the division granule is earned only when that count is reached.',
  grid: {
    perPoint: [
      { id: 'diagram', label: 'Draw the given diagram', marks: 8 },
      { id: 'divisions', label: 'Division of circle into equal parts (12 minimum)', marks: 3 },
    ],
    shorthand: 'given diagram 8 + division into ≥12 parts 3',
    ruleNote:
      'The division into equal parts is its own granule, and the scheme states a minimum count — “12 minimum”. Divide into fewer and the granule isn’t satisfied, even though the diagram itself is fine. When a construction step names a number of parts, reach it exactly.',
    cite: MS('p.12 (C-4 locus: given diagram 8, division of circle into equal parts (12 minimum) 3)'),
  },
  scripts: [
    {
      id: 'dcg7-a',
      label: 'Script A',
      persona: 'Divided into too few',
      attempts: [
        {
          id: 'dcg7-a-1',
          text: 'The given diagram is drawn correctly, but the circle is divided into only 8 equal parts, not the 12 the step requires.',
          key: { diagram: 8, divisions: 0 },
          keyNote:
            'The diagram earns its 8, but the division granule specifies “12 minimum” and 8 parts doesn’t meet it — 0 for that step. 8 of 11. The count in the instruction is the pass mark for the granule: divide into exactly what it names.',
        },
      ],
      embodies: {
        behaviour: 'Divides the circle into fewer than the required number of equal parts, missing the specified-minimum division granule.',
        cite: MS('p.12'),
      },
    },
    {
      id: 'dcg7-b',
      label: 'Script B',
      persona: 'Divided into 12',
      attempts: [
        {
          id: 'dcg7-b-1',
          text: 'The diagram is drawn and the circle is divided into 12 equal parts, as the step requires.',
          key: { diagram: 8, divisions: 3 },
          keyNote:
            'The diagram and the correct 12-part division are both there. Full 11 — reaching the stated count is all the granule asks.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-dcg7',
    rule: 'When a step names a number of divisions, hit it.',
    detail:
      'DCG steps that divide a circle or diagram into equal parts carry a specified minimum count (“12 minimum”, “min. 7 incl. end points”). The division is its own granule and it’s earned only when you reach that count — dividing into fewer forfeits it even when the rest of the work is right.',
    cite: MS('p.12'),
  },
};

export const DCG_CHAIR: ChairSubject = {
  id: 'dcg',
  label: 'Design & Communication Graphics',
  tagline: 'Construction over curve, every step scores, method pays, conventions and setup count.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [DCG1, DCG2, DCG3, DCG4, DCG5, DCG6, DCG7],
  sources: [
    { label: 'SEC LC DCG HL marking scheme 2025 (examiner-reports/dcg/2025-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the general drawing-marking conventions — construction marked above the finished curve, independently-scored steps, standalone method marks, itemised presentation granules like hidden detail, assembly relative-positioning, the true-length scaffold behind a surface development, and specified-minimum circle divisions — which apply at both Higher and Ordinary level. Verified against the 2025 Higher Level scheme (assembly and development conventions also recur in the 2024 scheme); level-specific worked drawings are being added.',
};
