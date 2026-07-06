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
const MS24 = (p: string) => ({ label: `SEC DCG HL marking scheme 2024, ${p}` });

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

// ─────────────── DCG8 · Indicate the measured answer ───────────────

const DCG8: GridSession = {
  mode: 'grid',
  id: 'dcg-indicate-value',
  subject: 'dcg',
  level: 'common',
  title: 'The construction isn’t the answer — indicate the value',
  cue: 'Determine and indicate the height',
  question:
    'A part gives 3 marks for the construction that establishes the height of point C and a separate 2 marks for indicating its correct measured height. A candidate builds the full construction perfectly but, treating the drawing as the answer, never writes down the height it produces.',
  questionNote:
    'Scenario authored for this exercise. DCG questions that ask you to “determine AND indicate” a length, height or angle itemise the indicated numeric value as its own granule, separate from the construction that finds it.',
  grid: {
    perPoint: [
      { id: 'establish', label: 'Establish height for point C', marks: 3 },
      { id: 'indicate', label: 'Correct height of point C indicated', marks: 2 },
    ],
    shorthand: 'establish height 3 + indicate value 2',
    ruleNote:
      'When a step says “determine AND indicate”, the indicated value is a separate mark from the construction that finds it. Finishing the construction but never writing the measurement leaves that granule with nothing to award. Read the value off and state it, in mm or degrees, every time.',
    cite: MS('p.8 (B-3(c): establish height for point C 3, correct height of point C 2)'),
  },
  scripts: [
    {
      id: 'dcg8-a',
      label: 'Script A',
      persona: 'Built it, never stated it',
      attempts: [
        {
          id: 'dcg8-a-1',
          text: 'The construction that establishes the height of point C is drawn correctly, but the measured height is never written on the sheet.',
          key: { establish: 3, indicate: 0 },
          keyNote:
            'The construction earns its 3, but “indicate the height” is a separate 2-mark granule and there is no figure written down to award it to. 3 of 5. When a question says “determine and indicate”, the number is part of the answer — measure it off and state it.',
        },
      ],
      embodies: {
        behaviour: 'Completes the construction but omits the separately-marked indicated value.',
        cite: MS('p.8'),
      },
    },
    {
      id: 'dcg8-b',
      label: 'Script B',
      persona: 'Stated the measurement',
      attempts: [
        {
          id: 'dcg8-b-1',
          text: 'The construction is drawn and the resulting height of point C is measured and written on the sheet in millimetres.',
          key: { establish: 3, indicate: 2 },
          keyNote:
            'Both granules are satisfied — the construction and the indicated value. Full 5. Writing the number took seconds and banked a mark reserved for exactly that.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-dcg8',
    rule: 'When a step says “indicate”, write the value down.',
    detail:
      'DCG “determine and indicate” questions score the indicated number as its own granule, separate from the construction that produces it. The geometry alone doesn’t claim it — read the length, height or angle off your drawing and state it in mm or degrees, or that mark goes unawarded.',
    cite: MS('p.8'),
  },
};

// ─────────────── DCG9 · The reference lines are marks of their own ───────────────

const DCG9: GridSession = {
  mode: 'grid',
  id: 'dcg-reference-lines',
  subject: 'dcg',
  level: 'common',
  title: 'In an auxiliary view, the reference lines are the marks',
  cue: 'Determine the dihedral angle',
  question:
    'A dihedral-angle construction scores its two auxiliary reference lines as separate steps: 4 marks for drawing X1Y1 parallel to the line of intersection, and 4 marks for drawing X2Y2 perpendicular to it. A candidate lays down X1Y1 correctly parallel, then draws X2Y2 parallel as well instead of perpendicular.',
  questionNote:
    'Scenario authored for this exercise. DCG auxiliary-view questions (dihedral angle, true shape) itemise each reference line as its own granule, and the mark depends on orienting it correctly — one parallel to a given line, the next perpendicular to it.',
  grid: {
    perPoint: [
      { id: 'x1y1', label: 'X1Y1 parallel to the line of intersection', marks: 4 },
      { id: 'x2y2', label: 'X2Y2 perpendicular to the line of intersection', marks: 4 },
    ],
    shorthand: 'X1Y1 parallel 4 + X2Y2 perpendicular 4',
    ruleNote:
      'Each auxiliary reference line is a separate granule, and the mark turns on its orientation — the first parallel to the line of intersection, the second perpendicular to it. Drawing the second line at the wrong orientation forfeits its mark even though the line is on the page. Keep the parallel-then-perpendicular sequence straight.',
    cite: MS('p.7 (B-2(b): X1Y1 parallel to line of intersection 4, X2Y2 perpendicular to line of intersection 4)'),
  },
  scripts: [
    {
      id: 'dcg9-a',
      label: 'Script A',
      persona: 'Second reference line wrong',
      attempts: [
        {
          id: 'dcg9-a-1',
          text: 'X1Y1 is drawn correctly parallel to the line of intersection, but X2Y2 is drawn parallel to it as well, not perpendicular.',
          key: { x1y1: 4, x2y2: 0 },
          keyNote:
            'X1Y1 is correctly oriented, so its 4 marks are banked — the reference lines are scored individually. But X2Y2 had to be perpendicular to the line of intersection to earn its granule, and it’s parallel instead. 4 of 8. The orientation of each reference line is the mark; a line in the wrong direction scores nothing.',
        },
      ],
      embodies: {
        behaviour: 'Orients the second auxiliary reference line incorrectly, forfeiting its granule.',
        cite: MS('p.7'),
      },
    },
    {
      id: 'dcg9-b',
      label: 'Script B',
      persona: 'Both lines oriented correctly',
      attempts: [
        {
          id: 'dcg9-b-1',
          text: 'X1Y1 is drawn parallel to the line of intersection and X2Y2 is drawn perpendicular to it, as the construction requires.',
          key: { x1y1: 4, x2y2: 4 },
          keyNote:
            'Both reference lines are oriented correctly — parallel, then perpendicular. Full 8. Getting the direction of each line right is what the two granules reward.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-dcg9',
    rule: 'Get every auxiliary reference line’s orientation right.',
    detail:
      'DCG auxiliary-view constructions score each reference line (X1Y1, X2Y2) as its own granule, and the mark depends on its orientation — parallel to a given line, then perpendicular to it. A reference line drawn in the wrong direction forfeits its mark even though it’s on the page. Track the parallel-then-perpendicular sequence carefully.',
    cite: MS('p.7'),
  },
};

// ─────────────── DCG10 · Hatching and centre lines are a granule ───────────────

const DCG10: ScaleSession = {
  mode: 'scale',
  id: 'dcg-hatching',
  subject: 'dcg',
  level: 'common',
  title: 'Hatching and centre lines are their own 6 marks',
  cue: 'Complete the sectional elevation',
  question:
    'A 60-mark sectional assembly reserves a final 6-mark granule for “presentation, hatching and centre lines”, separate from drawing the components. A candidate draws every component of the section cleanly but leaves the cut faces un-hatched and puts in no centre lines — the parts are all there, so surely that’s enough?',
  questionNote:
    'Scenario authored for this exercise. In a DCG sectional-assembly question the sectioning conventions — hatching the cut faces and adding centre lines — are itemised as a dedicated completion granule, separate from drawing the parts themselves.',
  scale: {
    name: 'Section completion · hatching & centre lines',
    levels: ladder([0, 6]),
    notes: [
      'A dedicated 6-mark granule covers presentation, hatching and centre lines.',
      'It is scored separately from drawing the assembly’s components.',
      'A section drawn without hatching or centre lines forfeits all 6, however clean the parts are.',
    ],
    cite: MS('p.13 (C-5(xvi): presentation, hatching and centre lines 6)'),
  },
  scripts: [
    {
      id: 'dcg10-a',
      label: 'The answer',
      persona: 'All parts, no hatching',
      work: [
        'Draws every component of the sectional assembly cleanly and in position.',
        'Leaves the cut faces un-hatched and adds no centre lines.',
      ],
      keyLevelId: 'm0',
      keyNote:
        '0 for this granule — “presentation, hatching and centre lines” is a dedicated 6-mark award, and with no hatching on the cut faces and no centre lines there is nothing for it to reward. The components score under their own granules, but these 6 marks are separate and guaranteed. Hatch the section and add centre lines: it’s free marks a finished-looking drawing routinely drops.',
      embodies: {
        behaviour: 'Draws the section but omits the hatching and centre lines that form the dedicated completion granule.',
        cite: MS('p.13'),
      },
    },
  ],
  takeaway: {
    id: 'codex-dcg10',
    rule: 'Always hatch the section and add centre lines.',
    detail:
      'DCG sectional-assembly questions reserve a dedicated 6-mark granule for presentation, hatching and centre lines, separate from drawing the parts. A section left un-hatched with no centre lines forfeits all six however clean the components look. Hatch the cut faces and add the centre lines every time — it’s guaranteed marks.',
    cite: MS('p.13'),
  },
};

// ─────────────── DCG11 · Any reasonable curve floors a mark ───────────────

const DCG11: ScaleSession = {
  mode: 'scale',
  id: 'dcg-curve-floor',
  subject: 'dcg',
  level: 'common',
  title: 'Never leave the final curve blank',
  cue: 'Draw the required curve',
  question:
    'The last step of a plotted-curve question is worth 4 marks for drawing the curve, and the scheme annotates it “(any = 1)” — any reasonable attempt at the curve is worth at least 1, with the rest for accuracy. A candidate locates the points but, unsure the curve will be neat, leaves the final line undrawn.',
  questionNote:
    'Scenario authored for this exercise. DCG plotted-curve steps (epicycloid, ellipse, spiral) are annotated “(any = 1)”: the final draw-the-curve granule floors a mark for any genuine attempt, so a blank is the one result that scores nothing.',
  scale: {
    name: 'Draw the curve · (any = 1) · /4',
    levels: ladder([0, 1, 4]),
    notes: [
      'The draw-the-curve granule is annotated “(any = 1)”.',
      'Any reasonable attempt at the curve scores at least 1; accuracy earns the rest.',
      'A blank scores 0 — leaving the curve undrawn is the only way to get nothing here.',
    ],
    cite: MS24('p.12 (C-4(a)(v): “Draw required epicycloid ……(any = 1)” 4)'),
  },
  scripts: [
    {
      id: 'dcg11-a',
      label: 'The answer',
      persona: 'Left the curve undrawn',
      work: [
        'Locates the points along the required curve correctly.',
        'Leaves the final curve undrawn for fear of a wobbly line.',
      ],
      keyLevelId: 'm0',
      keyNote:
        '0 for the draw-the-curve granule — a blank is the one outcome the “(any = 1)” floor can’t rescue. Any genuine attempt to draw the curve through the located points would have banked at least 1, with the rest for how accurately it follows them. Always sketch the curve in: a wobbly line scores, a missing line doesn’t.',
      embodies: {
        behaviour: 'Leaves the final curve blank, forfeiting the guaranteed floor mark on the draw-the-curve granule.',
        cite: MS24('p.12'),
      },
    },
  ],
  takeaway: {
    id: 'codex-dcg11',
    rule: 'Always draw the curve — any attempt floors a mark.',
    detail:
      'DCG plotted-curve steps are annotated “(any = 1)”: the draw-the-curve granule guarantees at least 1 mark for any reasonable attempt, with the balance for accuracy. A blank is the only result that scores nothing. Once your points are located, sketch the curve through them — a slightly wobbly line still banks marks a missing one throws away.',
    cite: MS24('p.12'),
  },
};

// ─────────────── DCG12 · Design intent is scored on its own ───────────────

const DCG12: GridSession = {
  mode: 'grid',
  id: 'dcg-design-intent',
  subject: 'dcg',
  level: 'common',
  title: 'The CAD sheet pays for design intent, not just clean parts',
  cue: 'Model the SolidWorks parts',
  question:
    'On the Student Assignment, the SolidWorks part models carry 15 marks for modelling proficiency (fully-defined sketches, appropriate features) and a separate 5 marks for demonstrated design intent and factor of difficulty. A candidate models tidy, fully-defined parts but keeps every feature simple, showing no design intent or ambition.',
  questionNote:
    'Scenario authored for this exercise. The DCG Student Assignment assessment sheet marks part-modelling proficiency and demonstrated design intent / factor of difficulty as two separate budgets.',
  grid: {
    perPoint: [
      { id: 'modelling', label: 'Part-modelling proficiency (fully-defined sketches, features)', marks: 15 },
      { id: 'intent', label: 'Design intent / factor of difficulty demonstrated', marks: 5 },
    ],
    shorthand: 'modelling proficiency 15 + design intent 5',
    ruleNote:
      'Design intent and factor of difficulty are marked separately from clean modelling. Tidy, fully-defined parts earn the proficiency marks, but the 5 marks for design intent need visible ambition — parametric relations, a genuinely challenging feature — not just a defined sketch. Build in a factor of difficulty on purpose.',
    cite: MS('p.25 (Student Assignment: part-modelling proficiency 15, design intent / factor of difficulty 5)'),
  },
  scripts: [
    {
      id: 'dcg12-a',
      label: 'Script A',
      persona: 'Clean parts, no ambition',
      attempts: [
        {
          id: 'dcg12-a-1',
          text: 'Every part is modelled tidily with fully-defined sketches and appropriate features, but all the geometry is kept simple with no relations and no challenging features.',
          key: { modelling: 15, intent: 0 },
          keyNote:
            'The clean, fully-defined modelling earns the 15-mark proficiency budget. But design intent and factor of difficulty are a separate 5-mark granule, and simple geometry with no relations or ambition gives it nothing to reward. Build a genuine factor of difficulty into the model — it’s marks the tidy-but-safe candidate leaves on the table.',
        },
      ],
      embodies: {
        behaviour: 'Models proficiently but demonstrates no design intent, forfeiting the separate factor-of-difficulty budget.',
        cite: MS('p.25'),
      },
    },
    {
      id: 'dcg12-b',
      label: 'Script B',
      persona: 'Ambition built in',
      attempts: [
        {
          id: 'dcg12-b-1',
          text: 'The parts are modelled with fully-defined sketches and, deliberately, a challenging feature and parametric relations that show clear design intent.',
          key: { modelling: 15, intent: 5 },
          keyNote:
            'Both budgets are satisfied — clean modelling and demonstrated design intent. Full 20. The factor of difficulty was designed in, not hoped for.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-dcg12',
    rule: 'Design intent is marked separately — build in a factor of difficulty.',
    detail:
      'The DCG assignment scores demonstrated design intent and factor of difficulty as their own budget, apart from clean part-modelling. Tidy fully-defined parts earn the proficiency marks; the design-intent marks need visible ambition — relations, a challenging feature. Plan a factor of difficulty into the model rather than playing it safe.',
    cite: MS('p.25'),
  },
};

// ─────────────── DCG13 · Earthworks: the interval is half the marks ───────────────

const DCG13: GridSession = {
  mode: 'grid',
  id: 'dcg-earthworks-interval',
  subject: 'dcg',
  level: 'common',
  title: 'In earthworks, the interval is half the marks',
  cue: 'Draw the earthworks',
  question:
    'An earthworks segment is scored as a two-step pair: 4 marks for drawing the graded parallel lines at the correct interval (7.5 mm), and a separate 4 marks for identifying where they intersect the contours and drawing the curve. A candidate, keen to get to the curve, sets the parallel lines at a guessed spacing rather than the 7.5 mm the gradient requires.',
  questionNote:
    'Scenario authored for this exercise. DCG Geologic-Geometry (earthworks) questions repeat a two-granule pattern for each segment — draw the graded parallel lines at a specified interval, then find their intersections with the contours — with the interval spacing scored in its own right.',
  grid: {
    perPoint: [
      { id: 'interval', label: 'Draw parallel lines at the correct interval (7.5 mm)', marks: 4 },
      { id: 'intersections', label: 'Identify intersections with contours and draw curve', marks: 4 },
    ],
    shorthand: 'graded lines at 7.5 mm 4 + contour intersections 4',
    ruleNote:
      'The graded parallel lines at the correct interval are their own 4-mark granule — half the segment. Guess the spacing and both the interval mark and the intersections that depend on it fall away. The interval is set by the gradient; step it out at exactly the stated value before you chase the curve.',
    cite: MS('p.9 (C-1(a): draw parallel lines at 7.5 mm intervals 4, identify intersections with contours and draw curves 4)'),
  },
  scripts: [
    {
      id: 'dcg13-a',
      label: 'Script A',
      persona: 'Guessed the spacing',
      attempts: [
        {
          id: 'dcg13-a-1',
          text: 'The graded parallel lines are drawn at a guessed spacing instead of the required 7.5 mm interval, and the contour intersections are read off those mis-spaced lines.',
          key: { interval: 0, intersections: 0 },
          keyNote:
            'The interval granule needs the lines at the correct 7.5 mm spacing, and a guessed spacing earns it nothing. Worse, the intersections are taken from the wrong lines, so that granule falls too — 0 of 8. In earthworks the interval is the gradient; set it exactly before anything downstream can score.',
        },
      ],
      embodies: {
        behaviour: 'Uses a guessed interval, forfeiting the spacing granule and the intersections that depend on it.',
        cite: MS('p.9'),
      },
    },
    {
      id: 'dcg13-b',
      label: 'Script B',
      persona: 'Stepped the interval exactly',
      attempts: [
        {
          id: 'dcg13-b-1',
          text: 'The graded parallel lines are stepped out at exactly 7.5 mm, then their intersections with the contours are identified and the curve drawn.',
          key: { interval: 4, intersections: 4 },
          keyNote:
            'The correct interval banks its 4, and the intersections read off those lines bank the other 4. Full 8. Getting the spacing right first made everything downstream scorable.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-dcg13',
    rule: 'In earthworks, step the interval out exactly first.',
    detail:
      'DCG earthworks questions score the graded parallel lines at a specified interval as their own granule — half of each segment — with the contour intersections a second granule that depends on them. The interval is set by the gradient, so a guessed spacing loses its own marks and poisons the intersections. Step the stated interval out precisely before drawing the curve.',
    cite: MS('p.9'),
  },
};

// ─────────────── DCG14 · A valid alternative construction is credited ───────────────

const DCG14: ScaleSession = {
  mode: 'scale',
  id: 'dcg-valid-alternative',
  subject: 'dcg',
  level: 'common',
  title: 'A valid alternative construction scores full',
  cue: 'Construct by a valid method',
  question:
    'A 2-mark granule reads “draw line from Sh parallel to RfSf (or Sf parallel to RhSh)” — the “or” builds an alternative construction into the mark, and the scheme’s header states other valid solutions are acceptable. A candidate uses the second form of the construction, not the one shown in the model solution. Does taking the alternative route cost marks?',
  questionNote:
    'Scenario authored for this exercise. DCG marking scheme headers state “Other valid solutions are acceptable and are marked accordingly”, and individual granules encode this with an explicit “or” between equivalent constructions.',
  scale: {
    name: 'Valid alternative construction · /2',
    levels: ladder([0, 2]),
    notes: [
      'The granule offers two equivalent constructions with an explicit “or”.',
      'The scheme header: “Other valid solutions are acceptable and are marked accordingly.”',
      'A correct alternative construction scores full — the model solution is not the only route.',
    ],
    cite: MS('p.9 (C-1(b)(xi): “…parallel to RfSf (or Sf parallel to RhSh)…” 2; header p.3)'),
  },
  scripts: [
    {
      id: 'dcg14-a',
      label: 'The answer',
      persona: 'Took the other valid route',
      work: [
        'Uses the second form of the construction (Sf parallel to RhSh), not the one in the model solution.',
        'The construction is geometrically correct and reaches the same result.',
      ],
      keyLevelId: 'm2',
      keyNote:
        'Full 2 — the granule itself names both routes with an “or”, and the scheme header says other valid solutions are marked accordingly. A correct alternative construction is credited exactly like the model one. Use the method you can execute cleanly rather than second-guessing the “expected” route; DCG rewards a valid construction, not a prescribed one.',
      embodies: {
        behaviour: 'Uses a valid alternative construction rather than the model solution’s — and is fully credited.',
        cite: MS('p.9'),
      },
    },
  ],
  takeaway: {
    id: 'codex-dcg14',
    rule: 'A valid alternative construction earns full marks.',
    detail:
      'DCG schemes state “other valid solutions are acceptable and are marked accordingly”, and granules often name two equivalent routes with an explicit “or”. A correct alternative construction scores the same as the model one. Use the method you can carry out cleanly instead of second-guessing an “expected” approach — the marks are for a valid construction, not a prescribed one.',
    cite: MS('p.9'),
  },
};

// ─────────────── DCG15 · Assembly and eDrawing are their own marks ───────────────

const DCG15: GridSession = {
  mode: 'grid',
  id: 'dcg-assembly-file',
  subject: 'dcg',
  level: 'common',
  title: 'The assembly and the eDrawing are their own marks',
  cue: 'Assemble the SolidWorks parts',
  question:
    'On the Student Assignment, the SolidWorks assembly is worth 7 marks for creating it from the parts with correct, appropriate mating, and a further 2 marks for the eDrawing of the CAD assembly. A candidate mates the parts into a correct assembly but, out of time, never exports the eDrawing file the brief asks for.',
  questionNote:
    'Scenario authored for this exercise. The DCG Student Assignment assessment sheet itemises the assembly (correct mating of parts) and the eDrawing of the CAD assembly as two separate marked deliverables.',
  grid: {
    perPoint: [
      { id: 'assembly', label: 'Assembly created with correct, appropriate mating', marks: 7 },
      { id: 'edrawing', label: 'eDrawing of the CAD assembly', marks: 2 },
    ],
    shorthand: 'correct mating 7 + eDrawing file 2',
    ruleNote:
      'The eDrawing is a separately-marked deliverable, not a by-product of the assembly. A correctly mated assembly earns its 7, but the 2 eDrawing marks need the file itself exported and submitted. Produce and file the eDrawing — it’s a quick export that banks marks a finished assembly alone doesn’t claim.',
    cite: MS('p.25 (Student Assignment: assembly with correct mating 7, eDrawing of CAD model assembly 2)'),
  },
  scripts: [
    {
      id: 'dcg15-a',
      label: 'Script A',
      persona: 'Assembled, no eDrawing',
      attempts: [
        {
          id: 'dcg15-a-1',
          text: 'The parts are mated into a correct, appropriately constrained assembly, but no eDrawing of the assembly is ever exported or submitted.',
          key: { assembly: 7, edrawing: 0 },
          keyNote:
            'The correctly mated assembly earns its 7. But the eDrawing is a separate 2-mark deliverable, and with no file exported there is nothing to award. 7 of 9. The eDrawing is a quick export — produce and submit it rather than leaving two guaranteed marks in the software.',
        },
      ],
      embodies: {
        behaviour: 'Builds the assembly but never exports the separately-marked eDrawing file.',
        cite: MS('p.25'),
      },
    },
    {
      id: 'dcg15-b',
      label: 'Script B',
      persona: 'Exported the eDrawing too',
      attempts: [
        {
          id: 'dcg15-b-1',
          text: 'The assembly is mated correctly and the eDrawing of the CAD assembly is exported and filed as required.',
          key: { assembly: 7, edrawing: 2 },
          keyNote:
            'Both deliverables are there — the correctly mated assembly and its eDrawing. Full 9. The export took moments and secured the marks the brief set aside for it.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-dcg15',
    rule: 'Export the eDrawing — it’s a separate marked deliverable.',
    detail:
      'The DCG assignment marks the SolidWorks assembly (correct mating) and the eDrawing of that assembly as two separate deliverables. A correctly built assembly doesn’t claim the eDrawing marks — the file has to be exported and submitted. It’s a quick export that banks guaranteed marks time-pressed candidates leave in the software.',
    cite: MS('p.25'),
  },
};

export const DCG_CHAIR: ChairSubject = {
  id: 'dcg',
  label: 'Design & Communication Graphics',
  tagline: 'Construction over curve, every step scores, method pays, and every convention, value and file is its own mark.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [DCG1, DCG2, DCG3, DCG4, DCG5, DCG6, DCG7, DCG8, DCG9, DCG10, DCG11, DCG12, DCG13, DCG14, DCG15],
  sources: [
    { label: 'SEC LC DCG HL marking scheme 2025 (examiner-reports/dcg/2025-marking-scheme)' },
    { label: 'SEC LC DCG HL marking scheme 2024 (examiner-reports/dcg/2024-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the general drawing-marking conventions — construction marked above the finished curve, independently-scored steps, standalone method marks, itemised presentation granules (hidden detail; hatching and centre lines), the separately-marked indicated value, auxiliary-view reference-line orientation, assembly relative-positioning, the true-length scaffold behind a surface development, specified-minimum circle divisions, the “(any = 1)” curve floor, credit for valid alternative constructions, the earthworks interval granule, and the Student Assignment’s CAD budgets (design intent / factor of difficulty, assembly mating, the eDrawing) — which apply at both Higher and Ordinary level. Verified against the 2025 Higher Level scheme, with the “(any = 1)” convention cited to the 2024 scheme (assembly and development conventions recur across both years); level-specific worked drawings are being added.',
};
