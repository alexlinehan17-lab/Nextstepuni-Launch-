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

// ─────────────── EC8 · Write it in full — abbreviations score nothing ───────────────

const EC8: GridSession = {
  mode: 'grid',
  id: 'ec-in-full',
  subject: 'economics',
  level: 'higher',
  title: 'Spell it out',
  cue: 'Write out in full',
  question: 'A “read the diagram” part gives you a labelled curve and asks you to write out in full what each numbered item represents. The instruction is explicit: “Do not use abbreviations.” The three items are Marginal cost, Average revenue = Demand, and Marginal revenue. A candidate writes “MC”, “AR = D”, “MR” — the right terms, in shorthand.',
  questionNote:
    'Scenario authored for this exercise. The instruction “Write out in full … Do not use abbreviations” is real HL marking grammar — an abbreviation of a correct term does not satisfy the cue for that item.',
  grid: {
    perPoint: [
      { id: 'item1', label: 'Item 1 — Marginal cost (in full)', marks: 2 },
      { id: 'item2', label: 'Item 2 — Average revenue = Demand (in full)', marks: 2 },
      { id: 'item3', label: 'Item 3 — Marginal revenue (in full)', marks: 2 },
    ],
    shorthand: 'write out in full · abbreviations N/A',
    ruleNote:
      'Each item is its own mark, and the cue demands the full term. “MC” is the correct concept but the wrong form — the scheme says “Do not use abbreviations”, so shorthand forfeits that item’s mark even though the candidate clearly knows it. Being right is not enough when the form is specified.',
    cite: MS('p.20 (write out in full; do not use abbreviations)'),
  },
  scripts: [
    {
      id: 'ec8-a',
      label: 'Script A',
      persona: 'Right terms, in shorthand',
      attempts: [
        {
          id: 'ec8-a-1',
          text: '“1. MC   2. AR = D   3. MR” — the correct concepts, but abbreviated.',
          key: { item1: 0, item2: 0, item3: 0 },
          keyNote: 'The candidate plainly knows the terms, but the cue said “write out in full … do not use abbreviations.” Each abbreviated item forfeits its mark. Correct knowledge in the wrong form scores nothing here — the instruction is the mark.',
        },
      ],
      embodies: {
        behaviour: 'Abbreviates correct terms where the cue demands them written out in full — a documented forfeiting form.',
        cite: MS('p.20'),
      },
    },
    {
      id: 'ec8-b',
      label: 'Script B',
      persona: 'Written out in full',
      attempts: [
        {
          id: 'ec8-b-1',
          text: '“1. Marginal cost   2. Average revenue = Demand   3. Marginal revenue.”',
          key: { item1: 2, item2: 2, item3: 2 },
          keyNote: 'Every item spelled out as the cue demanded. Full marks — the same knowledge as Script A, in the form the scheme requires.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-ec8',
    rule: 'When it says “in full”, abbreviations score nothing.',
    detail:
      'Some diagram-reading parts demand the term written out in full and say so — “Do not use abbreviations.” Writing “MC” for Marginal cost forfeits the mark however clearly you know it. Read the cue’s form, not just its content.',
    cite: MS('p.20'),
  },
};

// ─────────────── EC9 · For AND against — the balance is the mark ───────────────

const EC9: GridSession = {
  mode: 'grid',
  id: 'ec-both-sides',
  subject: 'economics',
  level: 'higher',
  title: 'Both sides, or half the marks',
  cue: 'Discuss one for and one against',
  question: 'A part asks: “Discuss one argument for and one argument against” a view. The marks split evenly — one developed point for the “for” side, one for the “against” side. A candidate who feels strongly writes two excellent “for” arguments and no “against”. How does that fare against a candidate who gives one of each?',
  questionNote:
    'Scenario authored for this exercise. When a cue asks for one argument for AND one against, the balance is required: both sides must appear, and a second same-side point cannot substitute for the missing opposite side.',
  grid: {
    perPoint: [
      { id: 'forSide', label: 'Argument FOR (developed)', marks: 5 },
      { id: 'againstSide', label: 'Argument AGAINST (developed)', marks: 5 },
    ],
    shorthand: 'one FOR + one AGAINST · balance required',
    ruleNote:
      'The two marks are reserved one per side. A brilliant second “for” argument earns nothing — there is no second “for” mark, and it cannot fill the empty “against” slot. Two points on one side caps you at half; one solid point on each side banks it all. The cue asked for balance, so balance is where the marks are.',
    cite: MS('p.4 (Discuss one argument for and one argument against)'),
  },
  scripts: [
    {
      id: 'ec9-a',
      label: 'Script A',
      persona: 'Two arguments, both “for”',
      attempts: [
        {
          id: 'ec9-a-1',
          text: 'First “for” argument — developed with a clear mechanism.',
          key: { forSide: 5, againstSide: 0 },
          keyNote: 'A fully developed “for” argument — banks the 5 marks reserved for the “for” side.',
        },
        {
          id: 'ec9-a-2',
          text: 'Second “for” argument — also excellent, but still a “for”.',
          key: { forSide: 0, againstSide: 0 },
          keyNote: 'There is only one “for” mark, and it is already earned; a second same-side point is surplus. It cannot claim the “against” marks, which sit empty. The part caps at 5/10 — half the marks, for ignoring half the question.',
        },
      ],
      embodies: {
        behaviour: 'Answers a for-and-against cue with two same-side points, forfeiting the opposite side’s reserved marks.',
        cite: MS('p.4'),
      },
    },
    {
      id: 'ec9-b',
      label: 'Script B',
      persona: 'One each side',
      attempts: [
        {
          id: 'ec9-b-1',
          text: '“For” argument — developed.',
          key: { forSide: 5, againstSide: 0 },
          keyNote: 'The “for” side, banked.',
        },
        {
          id: 'ec9-b-2',
          text: '“Against” argument — developed.',
          key: { forSide: 0, againstSide: 5 },
          keyNote: 'The “against” side, banked. 10/10 — the balance the cue demanded, both sides present.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-ec9',
    rule: 'For-and-against means both — one great side is half the marks.',
    detail:
      'When the cue asks for an argument for AND one against, the marks are reserved one per side. A second point on the side you like earns nothing; the opposite-side marks stay empty. Give one developed point on each side.',
    cite: MS('p.4'),
  },
};

// ─────────────── EC10 · Table completion — each cell shows its own workings ───────────────

const EC10: GridSession = {
  mode: 'grid',
  id: 'ec-cost-table',
  subject: 'economics',
  level: 'higher',
  title: 'Every cell shows its working',
  cue: 'Complete the table',
  question: 'A costs table has two blank cells to fill — Label A (Variable Cost) and Label B (Average Cost) — and the cue says “Show all your workings.” Each cell is a separate step-marked calculation: A is Total cost − Fixed cost; B is Total cost ÷ Output. A candidate works out A in full but writes B as a bare number with no working shown.',
  questionNote:
    'Scenario authored for this exercise. Table-completion parts step-mark each labelled cell independently — the workings line and the value are separate marks, and a missing cell’s working forfeits only that cell’s method mark.',
  grid: {
    perPoint: [
      { id: 'aWork', label: 'Cell A — workings shown (Total − Fixed)', marks: 1 },
      { id: 'aVal', label: 'Cell A — correct value (€10)', marks: 1 },
      { id: 'bWork', label: 'Cell B — workings shown (Total ÷ Output)', marks: 1 },
      { id: 'bVal', label: 'Cell B — correct value (€1.92)', marks: 1 },
    ],
    shorthand: 'each cell · workings + value, marked apart',
    ruleNote:
      'Each cell is its own mini-calculation with its own method mark and answer mark. Filling A perfectly does not carry B, and a bare correct number in B still forfeits B’s workings mark, because the cue said “show all your workings.” The cells are independent — you bank each one on its own.',
    cite: MS('p.64 (complete the table, labelled cells A and B; show all your workings)'),
  },
  scripts: [
    {
      id: 'ec10-a',
      label: 'Script A',
      persona: 'Shows A, guesses B',
      attempts: [
        {
          id: 'ec10-a-1',
          text: 'Cell A: “Total cost − Fixed cost = €70 − €60 = €10”, fully shown. Cell B: just “€1.92” written in, no working.',
          key: { aWork: 1, aVal: 1, bWork: 0, bVal: 1 },
          keyNote: 'A is fully banked — working and value. B’s value is right, so it earns its answer mark, but the missing “Total ÷ Output” working forfeits B’s method mark. 3 of 4 — the only mark lost is the one the cue explicitly asked for: the workings.',
        },
      ],
      embodies: {
        behaviour: 'Writes a bare value into a step-marked table cell without the working the cue demanded.',
        cite: MS('p.64'),
      },
    },
    {
      id: 'ec10-b',
      label: 'Script B',
      persona: 'Both cells worked',
      attempts: [
        {
          id: 'ec10-b-1',
          text: 'Cell A: “€70 − €60 = €10.” Cell B: “€115 ÷ 60 = €1.92.” Both workings and both values written in.',
          key: { aWork: 1, aVal: 1, bWork: 1, bVal: 1 },
          keyNote: 'Every cell shown and correct. 4/4 — the same answers as Script A, plus the one working it left out.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-ec10',
    rule: 'In a table, show the working for every cell.',
    detail:
      'Table-completion parts step-mark each labelled cell independently: workings and value are separate marks. A right number with no working still loses the method mark for that cell. Write the operation into every blank, not just the answer.',
    cite: MS('p.64'),
  },
};

// ─────────────── EC11 · SRP data — the two avoidable deductions ───────────────

const EC11: GridSession = {
  mode: 'grid',
  id: 'ec-srp-data',
  subject: 'economics',
  level: 'higher',
  title: 'The data box you can’t fake',
  cue: 'SRP · Evidence of Data',
  question: 'The Student Research Project’s “Evidence of Data” row is worth 5 marks and carries two flat, printed deductions: “Deduct 1m if no quantitative data. Deduct 1m if 2 sources not included.” A candidate’s study is thoughtfully written but leans entirely on description — no numbers — and cites a single source. How does the data row score?',
  questionNote:
    'Scenario authored for this exercise. The two SRP data deductions are real, printed marking rules — they are checklist gates, not quality judgements: missing quantitative data and fewer than two sources each cost a flat mark.',
  grid: {
    perPoint: [
      { id: 'quant', label: 'Quantitative data included', marks: 1 },
      { id: 'sources', label: 'At least two sources included', marks: 1 },
      { id: 'evidence', label: 'Data evidenced & relevant', marks: 3 },
    ],
    shorthand: '5m · −1 no quant data · −1 if <2 sources',
    ruleNote:
      'Two of the five marks are pure checklist: include at least one piece of quantitative (numeric) data, and cite at least two sources. These are flat deductions — no amount of good writing earns them back. They cost nothing to secure and a full point to miss, so they are the easiest marks in the whole project to protect.',
    cite: MS('p.71 (Evidence of Data: deduct 1m if no quantitative data / if 2 sources not included)'),
  },
  scripts: [
    {
      id: 'ec11-a',
      label: 'Script A',
      persona: 'Well written, no numbers',
      attempts: [
        {
          id: 'ec11-a-1',
          text: 'A carefully argued study — but entirely descriptive, with no quantitative data, and only one source cited.',
          key: { quant: 0, sources: 0, evidence: 3 },
          keyNote: '3 of 5. The writing earns the substantive evidence marks, but both flat deductions bite: no quantitative data (−1) and fewer than two sources (−1). Neither is a quality judgement — a single table of figures and a second citation would have banked them outright.',
        },
      ],
      embodies: {
        behaviour: 'Submits a data section with no quantitative data and a single source — the two named flat deductions.',
        cite: MS('p.71'),
      },
    },
    {
      id: 'ec11-b',
      label: 'Script B',
      persona: 'Numbers and two sources',
      attempts: [
        {
          id: 'ec11-b-1',
          text: 'The same study, but with a quantitative table drawn from the data and two named sources cited.',
          key: { quant: 1, sources: 1, evidence: 3 },
          keyNote: 'Full 5. Neither deduction applies — the numbers and the second source close both gates. The extra effort was tiny; the marks it protected were not.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-ec11',
    rule: 'Bank the SRP data marks: include numbers and two sources.',
    detail:
      'The SRP data row deducts a flat mark for no quantitative data and another for fewer than two sources. These are checklist gates, not quality calls — include at least one numeric figure and cite at least two sources, and neither deduction can touch you.',
    cite: MS('p.71'),
  },
};

// ─────────────── EC12 · The tariff tells you how much to write ───────────────

const EC12: ScaleSession = {
  mode: 'scale',
  id: 'ec-tariff-depth',
  subject: 'economics',
  level: 'higher',
  title: 'Read the marks, gauge the depth',
  cue: 'Explain (developed point)',
  question: 'The scheme states: “The detail required in any answer is determined by … the number of marks assigned to the answer.” A single developed point is worth 7 marks here — the scheme’s deepest per-point tariff, the size that wants a short developed paragraph (statement → mechanism → consequence). A candidate answers it with one bare sentence — the kind that would fully satisfy a 3-mark point. Where does it land on the band?',
  questionNote:
    'Scenario authored for this exercise. The rule is real: the detail required is set by the mark value (a @3 point wants a sentence; a @7 point wants a developed paragraph), and points are graded on the descriptor band scaled to the tariff.',
  scale: {
    name: 'Developed point · band on a 7-mark part',
    levels: [
      { id: 'weak', label: 'Weak (1)', annotation: '1', marks: 1 },
      { id: 'fair', label: 'Fair (3)', annotation: '3', marks: 3 },
      { id: 'good', label: 'Good (5)', annotation: '5', marks: 5 },
      { id: 'excellent', label: 'Excellent (7)', annotation: '7', marks: 7 },
    ],
    notes: [
      'The mark value is the depth instruction: “the detail required … is determined by … the number of marks assigned.”',
      'A @7 point is graded on the descriptor band scaled to the tariff — it wants a developed paragraph, not a line.',
      'A one-sentence statement, correct but undeveloped, sits low on the band however true it is.',
    ],
    cite: MS('p.2 (detail required determined by the marks assigned; developed-point bands)'),
  },
  scripts: [
    {
      id: 'ec12-a',
      label: 'The answer',
      persona: 'One line for a paragraph’s marks',
      work: [
        'States a single correct sentence — the point named, with no mechanism and no consequence.',
        'Would earn full marks on a 3-mark point, but nothing is added to fill the 7-mark tariff.',
      ],
      keyLevelId: 'fair',
      keyNote:
        'Fair — knowledge is there but the development the 7 marks pay for is not. The tariff told the candidate how much to write: a @7 point wants statement → mechanism → consequence, a short paragraph. A sentence that would max a @3 point cannot reach the top band of a @7 one. Let the mark value set your length.',
      embodies: {
        behaviour: 'Writes a low-tariff-sized answer for a high-tariff point, under-developing to the mark value.',
        cite: MS('p.2'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ec12',
    rule: 'The mark value tells you how much to write.',
    detail:
      'The scheme sets the detail required by the marks assigned: a @3 point wants a sentence, a @7 point wants a developed paragraph. Read the tariff before you answer, and develop each point to the size of its marks — statement, mechanism, consequence.',
    cite: MS('p.2'),
  },
};

// ─────────────── EC13 · Contradiction lands at Poor, not Fair ───────────────

const EC13: ScaleSession = {
  mode: 'scale',
  id: 'ec-poor-band',
  subject: 'economics',
  level: 'higher',
  title: 'Confused knowledge caps at Poor',
  cue: 'Explain (5-mark point)',
  question: 'A 5-mark point is graded on the scheme’s longer band: “4 Excellent · 3 Good · 2 Fair · 1 Poor · 0 Weak.” The 5-mark table adds a rung the 4-mark table doesn’t have — Poor (1) is reserved for “confusing or contradictory knowledge.” A candidate shows real knowledge but the explanation contradicts itself half-way through. Above the “no knowledge” floor, but where exactly?',
  questionNote:
    'Scenario authored for this exercise. The 5-mark descriptor band is real: it inserts a “Poor (1)” rung for confusing/contradictory knowledge, sitting above Weak (0 = no knowledge / repetition) and below Fair.',
  scale: {
    name: 'Developed point · band /4 (5-mark part)',
    levels: [
      { id: 'weak', label: 'Weak (0) — no knowledge / repetition', annotation: '0', marks: 0 },
      { id: 'poor', label: 'Poor (1) — confusing / contradictory', annotation: '1', marks: 1 },
      { id: 'fair', label: 'Fair (2) — vague knowledge', annotation: '2', marks: 2 },
      { id: 'good', label: 'Good (3) — some knowledge, limited development', annotation: '3', marks: 3 },
      { id: 'excellent', label: 'Excellent (4) — in-depth, relates, concise, logical', annotation: '4', marks: 4 },
    ],
    notes: [
      'Only 5-mark parts use this longer band — the extra rung is “Poor (1): confusing or contradictory knowledge.”',
      'Weak (0) is “no knowledge / repetition of statement”; Poor sits just above it.',
      'A self-contradiction pulls an otherwise knowledgeable answer down to Poor — real content, but undermined.',
    ],
    cite: MS('p.2 (5-mark band: 4/3/2/1/0; Poor = confusing or contradictory knowledge)'),
  },
  scripts: [
    {
      id: 'ec13-a',
      label: 'The answer',
      persona: 'Knows it, then contradicts it',
      work: [
        'Opens with a genuinely correct explanation of the point.',
        'Half-way through, states the opposite mechanism, leaving the answer internally contradictory.',
      ],
      keyLevelId: 'poor',
      keyNote:
        'Poor (1) — not zero, because there is real knowledge, but not Fair, because the contradiction confuses it. The 5-mark band exists precisely to place this: “confusing or contradictory knowledge” is its own rung above “no knowledge.” One consistent line of reasoning, without the self-contradiction, would climb to Fair or Good. Say one thing and hold it.',
      embodies: {
        behaviour: 'Presents knowledge undermined by a self-contradiction — the scheme’s named “Poor” descriptor.',
        cite: MS('p.2'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ec13',
    rule: 'Contradicting yourself caps you at Poor.',
    detail:
      'The 5-mark band adds a “Poor (1)” rung for confusing or contradictory knowledge — above “no knowledge” but below vague-but-consistent. Real content that argues against itself lands there. Pick one line of reasoning and stay consistent.',
    cite: MS('p.2'),
  },
};

// ─────────────── EC14 · Either/or — commit to one option ───────────────

const EC14: GridSession = {
  mode: 'grid',
  id: 'ec-either-or',
  subject: 'economics',
  level: 'higher',
  title: 'Choose one, and commit',
  cue: 'Answer either (b) or (c)',
  question: 'A question offers an internal choice — “Answer either (b) or (c)” — and only one option is marked. The chosen option is worth two developed points at 6 each. A candidate hedges: unsure which they know better, they half-answer both (b) and (c), splitting their time. Another candidate picks (b) and commits fully. How do they compare?',
  questionNote:
    'Scenario authored for this exercise. “Answer either (b) or (c)” is real HL structure — only one option is marked, so effort spent on the second option is wasted and the chosen one is what carries the marks.',
  grid: {
    perPoint: [
      { id: 'p1', label: '1st point of chosen option (developed)', marks: 6 },
      { id: 'p2', label: '2nd point of chosen option (developed)', marks: 6 },
    ],
    shorthand: 'either (b) or (c) · one option marked · 2 @ 6',
    ruleNote:
      'Only one option counts, so writing both does not double your chances — it halves your time on the one that will be marked. The hedger’s chosen option ends up thin; the committer’s is fully developed. Pick the option you know best and pour everything into it.',
    cite: MS('p.6 (Answer either (b) or (c) — internal choice, one option marked)'),
  },
  scripts: [
    {
      id: 'ec14-a',
      label: 'Script A',
      persona: 'Hedges both options',
      attempts: [
        {
          id: 'ec14-a-1',
          text: '(b) — first point, only half-developed, because time was split with (c).',
          key: { p1: 0, p2: 0 },
          keyNote: 'The first point of the marked option is under-developed — it doesn’t reach its band. Splitting time starved the answer that counts.',
        },
        {
          id: 'ec14-a-2',
          text: '(b) — second point, also thin.',
          key: { p1: 0, p2: 0 },
          keyNote: 'The second point is thin for the same reason. Both of (b)’s points fall short.',
        },
        {
          id: 'ec14-a-3',
          text: '(c) — also written out in full, hoping the better one is taken.',
          key: { p1: 0, p2: 0 },
          keyNote: 'The rubric marks only one option; the second is not credited at all. Every minute on (c) was a minute stolen from the (b) that was actually being marked.',
        },
      ],
      embodies: {
        behaviour: 'Answers both sides of an either/or choice, splitting effort so the marked option is under-developed.',
        cite: MS('p.6'),
      },
    },
    {
      id: 'ec14-b',
      label: 'Script B',
      persona: 'Commits to one',
      attempts: [
        {
          id: 'ec14-b-1',
          text: '(b) — first point, fully developed with mechanism and consequence.',
          key: { p1: 6, p2: 0 },
          keyNote: 'The full time on one option lets the first point reach its band. Banks 6.',
        },
        {
          id: 'ec14-b-2',
          text: '(b) — second point, fully developed.',
          key: { p1: 0, p2: 6 },
          keyNote: 'The second point, also developed. 12/12 — one committed option beats two hedged halves every time.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-ec14',
    rule: 'On an either/or, pick one and pour everything in.',
    detail:
      'Internal-choice parts mark only one option, so answering both just splits your time and thins the answer that counts. Choose the option you know best and develop it fully — the unchosen one earns nothing.',
    cite: MS('p.6'),
  },
};

// ─────────────── EC15 · Rounding is tolerated — a worked answer stands ───────────────

const EC15: ScaleSession = {
  mode: 'scale',
  id: 'ec-rounding',
  subject: 'economics',
  level: 'higher',
  title: 'A rounded answer still scores',
  cue: 'Calculate',
  question: 'A percentage calculation works out to 31.48%. The scheme prints the accepted answer as a range — “31.48 % / 32%” — so a correctly worked figure rounded to 32% is not penalised. A candidate, worried their rounding is “wrong”, crosses out a fully worked “32%” and leaves the box blank rather than commit. What did that cost?',
  questionNote:
    'Scenario authored for this exercise. Rounding tolerance is real: the scheme lists a range of acceptable answers (e.g. “31.48 % / 32%”), so a correctly worked, sensibly rounded figure keeps its answer mark.',
  scale: {
    name: 'Calculation · rounding tolerance',
    levels: [
      { id: 'm0', label: '0 (erased — nothing to mark)', annotation: '0', marks: 0 },
      { id: 'm2', label: '2 (workings only, no final figure)', annotation: '2', marks: 2 },
      { id: 'm6', label: '6 (worked + rounded answer accepted)', annotation: '6', marks: 6 },
    ],
    notes: [
      'The scheme accepts a range — “31.48 % / 32%” — so a sensibly rounded figure is not wrong.',
      'A blank box scores nothing; even the workings can’t be credited if the line is erased.',
      'A worked, rounded answer within the accepted range keeps full marks.',
    ],
    cite: MS('p.38 (accepted answer range “31.48 % / 32%”)'),
  },
  scripts: [
    {
      id: 'ec15-a',
      label: 'The answer',
      persona: 'Erased a correct answer',
      work: [
        'Worked the calculation correctly and reached “32%”.',
        'Second-guessed the rounding, crossed the whole thing out, and left the box blank.',
      ],
      keyLevelId: 'm0',
      keyNote:
        '0 — there is nothing left to mark. The rounding was never the problem: the scheme accepts “31.48 % / 32%”, so the crossed-out “32%” was a full-mark answer. Erasing it forfeited the workings too. A correctly worked, sensibly rounded figure stands — never delete a right answer for fear of the decimals.',
      embodies: {
        behaviour: 'Erases a correctly worked, in-range rounded answer, mistaking accepted rounding for an error.',
        cite: MS('p.38'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ec15',
    rule: 'A sensibly rounded answer is accepted — leave it in.',
    detail:
      'Calculation parts accept a range (e.g. “31.48 % / 32%”), so a correctly worked figure rounded reasonably keeps its marks. Don’t erase a right answer over the decimals — a blank box scores nothing, workings included.',
    cite: MS('p.38'),
  },
};

export const ECONOMICS_CHAIR: ChairSubject = {
  id: 'economics',
  label: 'Economics',
  tagline: 'Develop your points, label your diagrams, show your workings.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [EC1, EC2, EC3, EC4, EC5, EC6, EC7, EC8, EC9, EC10, EC11, EC12, EC13, EC14, EC15],
  sources: [
    { label: 'SEC LC Economics HL marking scheme 2025 (examiner-reports/economics/2025-marking-scheme)' },
    { label: 'SEC LC Economics OL marking scheme 2025 (examiner-reports/economics/2025-ol-marking-scheme)' },
  ],
  coverageNote:
    'The Higher-Level sessions cover the developed-point band and its depth-by-tariff and Poor-band rungs, the diagram-label and write-in-full rules, the show-your-workings, table-cell and rounding-tolerance calculation rules, the count-the-points (Surplus), for-and-against balance and either/or choice rules, the key-phrase gate, and the SRP length and data-deduction rules. The Ordinary session captures an OL-specific difference: two-point questions are front-loaded (1st @ 8 / 2nd @ 4), so the first point banks the most marks. Verified against the 2025 (and 2023) HL and OL schemes.',
};
