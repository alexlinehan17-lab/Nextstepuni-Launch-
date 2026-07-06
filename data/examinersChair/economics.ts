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

// ─────────────── EC5 · Answer the number asked — extras are Surplus ───────────────

const EC5: GridSession = {
  mode: 'grid',
  id: 'ec-surplus',
  subject: 'economics',
  level: 'higher',
  title: 'Two means two',
  cue: 'Outline two',
  question: 'An “Outline two factors” part is marked 2 @ 6 — two named, developed points, each out of 6. The scheme’s annotation table lists a “Surplus answer or part of answer” mark (N/A): material beyond the required number is seen and ignored, not credited. A candidate writes four points hoping quantity helps; another writes only one, very deeply. How does each fare?',
  questionNote:
    'Scenario authored for this exercise. The N @ M template caps the count at N; extra points are annotated “Surplus … N/A” (seen, ignored, not credited), and answering fewer than N caps the total.',
  grid: {
    perPoint: [
      { id: 'p1', label: '1st point (developed)', marks: 6 },
      { id: 'p2', label: '2nd point (developed)', marks: 6 },
    ],
    shorthand: '2 @ 6 · extras are Surplus',
    ruleNote:
      'Only the first two points are marked; a third or fourth is annotated “Surplus” and earns nothing — the time on it is wasted. Answering only one point caps the total at 6 of 12, because the second point’s marks have nothing to attach to. Match the count to the number asked: no more, no fewer.',
    cite: MS('p.3 (Surplus annotation) + 2 @ M grids throughout'),
  },
  scripts: [
    {
      id: 'ec5-a',
      label: 'Script A',
      persona: 'Four points, hoping quantity helps',
      attempts: [
        {
          id: 'ec5-a-1',
          text: 'First point — named and developed with a mechanism.',
          key: { p1: 6, p2: 0 },
          keyNote: 'A fully developed first point — banks its 6.',
        },
        {
          id: 'ec5-a-2',
          text: 'Second point — named and developed.',
          key: { p1: 0, p2: 6 },
          keyNote: 'A solid second point — banks its 6. The part is now full at 12/12.',
        },
        {
          id: 'ec5-a-3',
          text: 'Third and fourth points — also developed, but the part asked for two.',
          key: { p1: 0, p2: 0 },
          keyNote: 'Surplus. The scheme annotates anything beyond the required number “Surplus answer … N/A” — seen and ignored. However good they are, they add nothing; the effort would have banked more spent deepening the first two.',
        },
      ],
      embodies: {
        behaviour: 'Over-supplies points on a capped N @ M part; the extras are marked Surplus and earn nothing.',
        cite: MS('p.3'),
      },
    },
    {
      id: 'ec5-b',
      label: 'Script B',
      persona: 'One deep point, no second',
      attempts: [
        {
          id: 'ec5-b-1',
          text: 'A single point, developed very thoroughly — but no second point is offered.',
          key: { p1: 6, p2: 0 },
          keyNote: 'The one point earns its full 6, but there is nothing for the second 6 to attach to, so the part caps at 6/12. Depth can max one point; it cannot substitute for a missing one.',
        },
      ],
      embodies: {
        behaviour: 'Under-supplies on an N @ M part, forfeiting the marks reserved for the missing point.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ec5',
    rule: 'Answer the number asked — no more, no fewer.',
    detail:
      'The N @ M template caps the count: extra points are annotated “Surplus” and earn nothing, while answering too few forfeits the missing point’s marks. Give exactly N points and put the spare effort into developing them.',
    cite: MS('p.3'),
  },
};

// ─────────────── EC6 · The key phrase must appear — and not be contradicted ───────────────

const EC6: GridSession = {
  mode: 'grid',
  id: 'ec-keyphrase',
  subject: 'economics',
  level: 'higher',
  title: 'Say the words, and mean them',
  cue: 'Outline the term',
  question: 'The scheme states its support notes “may contain key phrases which must appear in the candidate’s answer in order to merit the assigned marks”, and that words “must be correctly used in context and not contradicted … where there is evidence of incorrect use or contradictions the marks may not be awarded.” A definition is marked 2 (key phrase) + 4 (correct development). Three candidates: one names the term and stops, one states it then contradicts it, one states and develops it correctly.',
  questionNote:
    'Scenario authored for this exercise. The marking grammar is real: the scheme lists key phrases that must appear to merit the marks, and self-contradiction or incorrect use can forfeit them.',
  grid: {
    perPoint: [
      { id: 'phrase', label: 'Required key phrase present', marks: 2 },
      { id: 'context', label: 'Developed correctly, not contradicted', marks: 4 },
    ],
    shorthand: '2 (key phrase) + 4 (correct development)',
    ruleNote:
      'The key phrase is a gate: without it, the marks can’t be merited. But a phrase that is then contradicted or misused forfeits even its own mark — “the marks may not be awarded.” The safe answer states the required term and then develops it in a way that stays consistent with what it means.',
    cite: MS('p.2 (key phrases must appear; correctly used in context and not contradicted)'),
  },
  scripts: [
    {
      id: 'ec6-a',
      label: 'Script A',
      persona: 'Names it, then stops',
      attempts: [
        {
          id: 'ec6-a-1',
          text: 'States the required key phrase correctly, but adds no explanation or development.',
          key: { phrase: 2, context: 0 },
          keyNote: 'The key phrase appears, so it merits its 2 marks — but the development marks need an actual explanation. Naming the term is the gate, not the whole answer.',
        },
      ],
      embodies: {
        behaviour: 'Includes the required key phrase but leaves the development marks unearned.',
        cite: MS('p.2'),
      },
    },
    {
      id: 'ec6-b',
      label: 'Script B',
      persona: 'Right words, wrong meaning',
      attempts: [
        {
          id: 'ec6-b-1',
          text: 'States the key phrase, then a following sentence describes it in a way that contradicts what the term actually means.',
          key: { phrase: 0, context: 0 },
          keyNote: 'The contradiction is fatal: the scheme says where there is evidence of contradiction “the marks may not be awarded.” The correct phrase does not rescue an answer that then undoes it — this forfeits even the phrase mark.',
        },
      ],
      embodies: {
        behaviour: 'Uses the key phrase but contradicts it in context — a documented forfeiting behaviour.',
        cite: MS('p.2'),
      },
    },
    {
      id: 'ec6-c',
      label: 'Script C',
      persona: 'States it and develops it',
      attempts: [
        {
          id: 'ec6-c-1',
          text: 'States the required key phrase and develops it correctly and consistently.',
          key: { phrase: 2, context: 4 },
          keyNote: 'The phrase is present and the development stays true to it. Full marks — the gate and the explanation, both intact.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-ec6',
    rule: 'Use the exact term — and never contradict it.',
    detail:
      'The scheme lists key phrases that must appear to merit the marks, and self-contradiction or incorrect use can forfeit them. State the required term precisely, then develop it in a way that stays consistent with its meaning.',
    cite: MS('p.2'),
  },
};

// ─────────────── EC7 · SRP — marks follow analysis, not length ───────────────

const EC7: ScaleSession = {
  mode: 'scale',
  id: 'ec-srp-length',
  subject: 'economics',
  level: 'higher',
  title: 'Volume is not value',
  cue: 'Student Research Project',
  question: 'The Student Research Project is marked on five qualitative descriptor bands (Excellent / Very Good / Good / Fair / Weak), and the examiner is told: “Be careful not to penalise skilful brevity, nor to reward unwarranted length.” The top bands are reserved for critical analysis, objective evaluation, and judgements supported by data. A candidate submits a section that runs to twice the expected length, restating the data tables and quoting sources — but thin on genuine interpretation. Where does it land?',
  questionNote:
    'Scenario authored for this exercise. The SRP descriptor bands and the “skilful brevity / unwarranted length” instruction are the real HL marking grammar (pp.71–74).',
  scale: {
    name: 'SRP descriptor band /10',
    levels: [
      { id: 'weak', label: 'Weak (0–2)', annotation: '0–2', marks: 2 },
      { id: 'fair', label: 'Fair (3–4)', annotation: '3–4', marks: 4 },
      { id: 'good', label: 'Good (5–6)', annotation: '5–6', marks: 6 },
      { id: 'vgood', label: 'Very Good (7–8)', annotation: '7–8', marks: 8 },
      { id: 'excellent', label: 'Excellent (9–10)', annotation: '9–10', marks: 10 },
    ],
    notes: [
      'Marked on qualitative bands, not by counting facts or pages.',
      'Explicit instruction: “Be careful not to penalise skilful brevity, nor to reward unwarranted length.”',
      'The top bands need critical analysis, evaluation, and judgements supported by data — not description.',
    ],
    cite: MS('p.71 (SRP descriptor bands; skilful brevity / unwarranted length)'),
  },
  scripts: [
    {
      id: 'ec7-a',
      label: 'The submission',
      persona: 'Long, but describing not analysing',
      work: [
        'Runs to roughly twice the expected length; restates the data tables and quotes the sources at length.',
        'Description and summary dominate — little genuine interpretation, evaluation, or data-supported judgement.',
      ],
      keyLevelId: 'fair',
      keyNote:
        'Fair band — the length buys nothing. The examiner is explicitly told not to reward unwarranted length nor penalise skilful brevity, and the top bands are reserved for critical analysis and evaluation supported by data. A shorter section that actually interpreted and evaluated the evidence would reach Very Good or Excellent. Volume is not value.',
      embodies: {
        behaviour: 'Pads the study with length and restated data instead of analysis — length the scheme explicitly does not reward.',
        cite: MS('p.71'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ec7',
    rule: 'In the SRP, marks follow analysis, not length.',
    detail:
      'The SRP bands reward critical analysis, evaluation, and data-supported judgement — and the scheme explicitly refuses to reward unwarranted length or penalise skilful brevity. Interpret and evaluate the evidence; don’t pad with description.',
    cite: MS('p.71'),
  },
};

export const ECONOMICS_CHAIR: ChairSubject = {
  id: 'economics',
  label: 'Economics',
  tagline: 'Develop your points, label your diagrams, show your workings.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [EC1, EC2, EC3, EC4, EC5, EC6, EC7],
  sources: [
    { label: 'SEC LC Economics HL marking scheme 2025 (examiner-reports/economics/2025-marking-scheme)' },
    { label: 'SEC LC Economics OL marking scheme 2025 (examiner-reports/economics/2025-ol-marking-scheme)' },
  ],
  coverageNote:
    'The develop-your-points, diagram-label, show-your-workings, count-the-points (Surplus), key-phrase and SRP sessions apply at Higher Level. The Ordinary session captures an OL-specific difference: two-point questions are front-loaded (1st @ 8 / 2nd @ 4), so the first point banks the most marks. Verified against the 2025 (and 2023) HL and OL schemes.',
};
