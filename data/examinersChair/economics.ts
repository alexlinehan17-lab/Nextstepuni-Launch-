/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Economics (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the developed-point descriptor bands with repetition scoring
 * zero, the itemised diagram marks where labels are their own component, and
 * the step-marked calculation with the named "omission of %" deduction) is the
 * real SEC system, cited to:
 *  - SEC LC Economics HL marking scheme 2025 —
 *    examiner-reports/economics/2025-marking-scheme.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC Economics HL marking scheme 2025, ${p}` });
const MSOL = (p: string) => ({ label: `SEC Economics OL marking scheme 2025, ${p}` });

const ladder = (marks: number[]): ScaleLevel[] =>
  marks.map(m => ({ id: `m${m}`, label: `${m} marks`, annotation: `${m}`, marks: m }));

// ─────────────── Ec1 · Develop, don't repeat ───────────────

const EC1: ScaleSession = {
  mode: 'scale',
  id: 'ec-develop',
  subject: 'economics',
  level: 'higher',
  title: 'Restating isn’t developing',
  cue: 'Discuss',
  question: 'A developed economics point is graded on a band out of 4: Excellent 3, Good 2, Fair 1, Weak 0 — and “repetition of statement” is a Weak descriptor. A candidate states a valid point, then “develops” it by rephrasing the same sentence twice. What band does the development earn?',
  questionNote:
    'Scenario authored for this exercise. Developed points are graded on descriptor bands (e.g. 3/2/1/0), where restating or repeating the point is an explicit Weak/zero descriptor.',
  scale: {
    name: 'Developed point · band /3',
    levels: ladder([0, 1, 2, 3]),
    notes: [
      'Development is banded: Excellent 3 / Good 2 / Fair 1 / Weak 0.',
      '“Repetition of statement” is an explicit Weak (0) descriptor.',
      'Marks come from developing the point — a mechanism, a consequence, an example — not restating it.',
    ],
    cite: MS('p.2 (developed-point descriptor bands)'),
  },
  scripts: [
    {
      id: 'ec1-a',
      label: 'The answer',
      persona: 'Says it three ways',
      work: [
        'States a valid point.',
        '“Develops” it by rephrasing the same sentence twice more.',
      ],
      keyLevelId: 'm0',
      keyNote:
        'Weak band, 0 for the development — repetition is named as a zero descriptor. Rewording a point isn’t developing it. One line explaining the mechanism (why it happens) or its consequence would lift it to Good or Excellent. Development means adding something new, not saying the same thing again.',
      embodies: {
        behaviour: 'Repeats the statement instead of developing it — an explicit Weak-band descriptor.',
        cite: MS('p.2'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ec1',
    rule: 'Development adds something; repetition adds nothing.',
    detail:
      'Economics grades developed points on a band where restating the point scores Weak/0. To develop, add a mechanism, a consequence, or an example — rewording the same sentence earns nothing.',
    cite: MS('p.2'),
  },
};

// ─────────────── Ec2 · Diagram labels are the marks ───────────────

const EC2: GridSession = {
  mode: 'grid',
  id: 'ec-diagram-labels',
  subject: 'economics',
  level: 'higher',
  title: 'Labels are the marks',
  cue: 'Draw the diagram',
  question: 'A supply-and-demand diagram is marked with itemised marks: the axes, the demand curve, the supply curve, and the labelled equilibrium (price and quantity) are each their own marks. A candidate draws the curves perfectly but labels nothing — no axes, no equilibrium.',
  questionNote:
    'Scenario authored for this exercise. Economics diagrams carry itemised marks, and the labels (axes, curves, equilibrium point) are separate, forfeitable components — on the S&D graph the labels are several of the marks.',
  grid: {
    perPoint: [
      { id: 'axes', label: 'Axes labelled (P, Q)', marks: 2 },
      { id: 'demand', label: 'Demand curve (drawn + labelled)', marks: 3 },
      { id: 'supply', label: 'Supply curve (drawn + labelled)', marks: 3 },
      { id: 'equilibrium', label: 'Equilibrium marked & labelled', marks: 3 },
    ],
    shorthand: 'itemised · labels are separate marks',
    ruleNote:
      'Each element is its own mark, and the labels are counted separately from the lines. A beautifully drawn but unlabelled diagram forfeits every label mark — often a third or more of the total. The graph is only worth its marks once it’s labelled.',
    cite: MS('p.50 (S&D graph itemised marks and labels)'),
  },
  scripts: [
    {
      id: 'ec2-a',
      label: 'The diagram',
      persona: 'Perfect curves, no labels',
      attempts: [
        {
          id: 'ec2-a-1',
          text: 'Two correctly shaped curves crossing — but no axis labels, no curve labels, and the equilibrium point unmarked.',
          key: { axes: 0, demand: 0, supply: 0, equilibrium: 0 },
          keyNote: 'The curves are right, but the marks are attached to the labels — axes (P and Q), each curve named, the equilibrium marked. With none of them, the diagram scores near zero despite looking correct. Labelling is not decoration in Economics; it is where most of the diagram’s marks live.',
        },
      ],
      embodies: {
        behaviour: 'Draws accurate curves but omits the labels, which carry their own itemised marks.',
        cite: MS('p.50'),
      },
    },
    {
      id: 'ec2-b',
      label: 'The diagram',
      persona: 'Drawn and fully labelled',
      attempts: [
        {
          id: 'ec2-b-1',
          text: 'Axes labelled Price and Quantity; demand and supply curves each labelled; equilibrium marked with Pₑ and Qₑ.',
          key: { axes: 2, demand: 3, supply: 3, equilibrium: 3 },
          keyNote: 'Every itemised element present and labelled. Full marks — the same drawing as Script A, plus the labels that actually carry the marks.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-ec2',
    rule: 'In Economics diagrams, the labels carry the marks.',
    detail:
      'Diagram marks are itemised, and axis/curve/equilibrium labels are counted separately — an unlabelled diagram forfeits a large share of the marks however well it’s drawn. Label the axes, name every curve, and mark the equilibrium.',
    cite: MS('p.50'),
  },
};

// ─────────────── Ec3 · Show workings, keep the % ───────────────

const EC3: ScaleSession = {
  mode: 'scale',
  id: 'ec-workings',
  subject: 'economics',
  level: 'higher',
  title: 'Workings and the missing %',
  cue: 'Calculate',
  question: 'A calculation is step-marked: formula, substitution, answer. A candidate reaches the correct value — 32 — with full workings, but writes it as “32”, omitting the “%” the answer needed. The scheme prints “Deduct 1 mark for omission of %”. How does it fare versus a bare correct “32%” with no workings?',
  questionNote:
    'Scenario authored for this exercise. Economics calculations are step-marked (formula + substitution + answer), and the scheme carries a named deduction “Deduct 1 mark for omission of %”. An answer-only response never scores full marks.',
  scale: {
    name: 'Calculation · workings + unit',
    levels: [
      { id: 'm2', label: '2 (answer only, no workings)', annotation: '2', marks: 2 },
      { id: 'm5', label: '5 (workings, missing %)', annotation: '5', marks: 5 },
      { id: 'm6', label: '6 (workings + %)', annotation: '6', marks: 6 },
    ],
    notes: [
      'Calculations are step-marked: formula + substitution + answer.',
      'Named deduction: “Deduct 1 mark for omission of %.”',
      'An answer-only response forfeits the method marks and never scores full.',
    ],
    cite: MS('p.5, p.57 (step-marking and omission-of-% deduction)'),
  },
  scripts: [
    {
      id: 'ec3-a',
      label: 'The answer',
      persona: 'Full workings, forgot the %',
      work: ['Formula and substitution shown correctly.', 'Answer written as “32” — the “%” is missing.'],
      keyLevelId: 'm5',
      keyNote:
        '5 of 6 — the workings bank the method marks, and only the named one-mark “omission of %” deduction applies. Compare the candidate who writes a bare “32%” with no workings: they forfeit the method marks and can’t reach full either. Show the steps AND write the unit — each protects a different mark.',
      embodies: {
        behaviour: 'Shows workings but omits the % — a named one-mark deduction, not a wipeout.',
        cite: MS('p.5'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ec3',
    rule: 'Show the workings, and never drop the %.',
    detail:
      'Economics calculations are step-marked, so a bare answer forfeits the method marks — and omitting the % is a named one-mark deduction. Write the formula and substitution, then the answer with its unit.',
    cite: MS('p.5'),
  },
};

// ─────────────── EC4 · OL — the first point is worth more ───────────────

const EC4: GridSession = {
  mode: 'grid',
  id: 'ec-ol-frontload',
  subject: 'economics',
  level: 'ordinary',
  title: 'Develop the first point deeply',
  cue: 'Explain two (OL)',
  question: 'An Ordinary Level “explain two” part is front-loaded: the first point is worth 8 and the second only 4. A candidate spreads their effort evenly, giving two half-developed points instead of one deep one and one brief one.',
  questionNote:
    'Scenario authored for this exercise. Unlike HL’s symmetric “2 @ M” split, OL Economics front-loads: the first point is worth more (e.g. 1st @ 8 / 2nd @ 4), so a deep first point banks the most.',
  grid: {
    perPoint: [
      { id: 'p1', label: '1st point (developed)', marks: 8 },
      { id: 'p2', label: '2nd point (developed)', marks: 4 },
    ],
    shorthand: '1st @ 8 / 2nd @ 4',
    ruleNote:
      'The first point carries twice the second. A deeply developed first point banks 8; the second, worth 4, only needs to be solid. Spreading effort evenly under-develops the point that matters most.',
    cite: MSOL('p.22, p.25 (front-loaded 1st @ 8 / 2nd @ 4)'),
  },
  scripts: [
    {
      id: 'ec4-a',
      label: 'Script A',
      persona: 'Two half-developed points',
      attempts: [
        {
          id: 'ec4-a-1',
          text: 'First point — only half-developed (a mechanism started but not finished), because effort was split evenly across both.',
          key: { p1: 0, p2: 0 },
          keyNote: 'The first point is worth 8 — the biggest single mark in the part — but it’s under-developed, so it doesn’t reach its band. Splitting effort evenly starved the point that mattered most.',
        },
        {
          id: 'ec4-a-2',
          text: 'Second point — also only half-developed.',
          key: { p1: 0, p2: 0 },
          keyNote: 'The second point is only worth 4, and it too is thin. Two half-points score far less than one deep point plus one solid one.',
        },
      ],
      embodies: {
        behaviour: 'Splits effort evenly on a front-loaded part, under-developing the high-value first point.',
        cite: MSOL('p.22'),
      },
    },
    {
      id: 'ec4-b',
      label: 'Script B',
      persona: 'Deep first, solid second',
      attempts: [
        {
          id: 'ec4-b-1',
          text: 'First point — fully developed with mechanism and example.',
          key: { p1: 8, p2: 0 },
          keyNote: 'The 8-mark first point, fully developed. Banks the biggest mark in the part.',
        },
        {
          id: 'ec4-b-2',
          text: 'Second point — solid and clear, appropriate to its 4 marks.',
          key: { p1: 0, p2: 4 },
          keyNote: 'A solid second point for its 4 marks. 12/12 — the effort matched where the marks were.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-ec4',
    rule: 'At OL, develop the first point deepest.',
    detail:
      'Ordinary Level Economics front-loads two-point questions (1st @ 8 / 2nd @ 4). Put your deepest development into the first point — it’s worth the most — and give the second a solid but briefer treatment.',
    cite: MSOL('p.22'),
  },
};

export const ECONOMICS_CHAIR: ChairSubject = {
  id: 'economics',
  label: 'Economics',
  tagline: 'Develop your points, label your diagrams, show your workings.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [EC1, EC2, EC3, EC4],
  sources: [
    { label: 'SEC LC Economics HL marking scheme 2025 (examiner-reports/economics/2025-marking-scheme)' },
    { label: 'SEC LC Economics OL marking scheme 2025 (examiner-reports/economics/2025-ol-marking-scheme)' },
  ],
  coverageNote:
    'The develop-your-points, diagram-label and show-your-workings sessions apply at both levels. The Ordinary session captures an OL-specific difference: two-point questions are front-loaded (1st @ 8 / 2nd @ 4), so the first point banks the most marks. Verified against the 2025 and 2023 OL schemes.',
};
