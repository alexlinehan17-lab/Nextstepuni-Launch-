/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Mathematics marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * scale system (scale names, mark ladders, credit-level descriptors, the Full
 * Credit −1 rule, work-of-merit rules and margin annotations) is the real SEC
 * system, cited to:
 *  - SEC LC Mathematics marking scheme 2023, Ordinary Level (Paper 2 portion) —
 *    examiner-reports/maths/2023-marking-scheme-ol-p2.*
 *  - Chief Examiner's Report, Mathematics 2015 — examiner-reports/maths/2015-*
 * Claim-by-claim record: compliance/evidence/examinersChair.md.
 */

import { type ChairSubject, type ScaleSession, type ScaleLevel } from './types';

const MS23 = (p: string) => ({ label: `SEC Mathematics OL marking scheme 2023, ${p}` });
const CER15 = (p: string) => ({ label: `Chief Examiner's Report, Mathematics 2015, ${p}` });
const MSFL = (p: string) => ({ label: `SEC Mathematics Foundation marking scheme 2025, ${p}` });

// Verified scale ladders (marking scheme, p.[28]).
const SCALE_10C: ScaleLevel[] = [
  { id: 'none', label: 'No credit', annotation: '✗', marks: 0 },
  { id: 'low', label: 'Low partial credit', annotation: 'L', marks: 4 },
  { id: 'high', label: 'High partial credit', annotation: 'H', marks: 6 },
  { id: 'full', label: 'Full credit', annotation: '✓', marks: 10 },
];
const SCALE_10C_STAR: ScaleLevel[] = [
  SCALE_10C[0],
  SCALE_10C[1],
  SCALE_10C[2],
  { id: 'fullminus', label: 'Full credit −1', annotation: 'F✱', marks: 9 },
  SCALE_10C[3],
];
const SCALE_15D: ScaleLevel[] = [
  { id: 'none', label: 'No credit', annotation: '✗', marks: 0 },
  { id: 'low', label: 'Low partial credit', annotation: 'L', marks: 5 },
  { id: 'mid', label: 'Mid partial credit', annotation: 'M', marks: 8 },
  { id: 'high', label: 'High partial credit', annotation: 'H', marks: 12 },
  { id: 'full', label: 'Full credit', annotation: '✓', marks: 15 },
];

// ─────────────────────────── M1 · The ladder ───────────────────────────

const M1: ScaleSession = {
  mode: 'scale',
  id: 'maths-ladder',
  subject: 'maths',
  level: 'common',
  title: 'The ladder: 0 → 4 → 6 → 10',
  cue: 'Find',
  question: 'Find the distance between the points A(2, 1) and B(8, 9).',
  questionNote:
    'Question authored for this exercise; the scale and marking notes mirror the SEC 2023 OL coordinate-geometry questions (Q1(a)), which used Scale 10C with these exact descriptors.',
  scale: {
    name: '10C',
    levels: SCALE_10C,
    notes: [
      'Low partial credit: work of merit — e.g. the relevant formula written down.',
      'High partial credit: correct formula fully substituted; or error(s) in substitution but finishes correctly.',
      'Full credit: correct answer — on this question type, even without supporting work.',
      'General rule: a correct relevant formula written is regarded as work of merit and earns the lowest non-zero credit.',
    ],
    cite: MS23('p.[28]–[31] (scale table, descriptors and Q1(a) notes)'),
  },
  scripts: [
    {
      id: 'm1-a',
      label: 'Script A',
      persona: 'Wrote the formula, then froze',
      work: ['Distance = √((x₂ − x₁)² + (y₂ − y₁)²)', '…'],
      keyLevelId: 'low',
      keyNote:
        'The relevant formula, correctly written, is “work of merit” — the scheme’s own words — and earns the lowest non-zero credit: 4/10. Blank would have been 0. That formula is the cheapest 4 marks in the subject.',
      embodies: {
        behaviour: 'Shows only the relevant formula — which the scheme explicitly counts as work of merit.',
        cite: MS23('p.[29]'),
      },
    },
    {
      id: 'm1-b',
      label: 'Script B',
      persona: 'One slip, but keeps going',
      work: [
        'Distance = √((8 − 2)² + (9 − 1)²)',
        '= √(36 + 46)',
        '= √82',
        '≈ 9.06',
      ],
      keyLevelId: 'high',
      keyNote:
        'The substitution is fully set up, one square is miscalculated (8² written as 46), and the work is finished consistently from the error. “Error(s) in substitution but finishes correctly” is the scheme’s definition of high partial credit: 6/10. Abandoning after the slip would have cost more than the slip did.',
      embodies: {
        behaviour: 'Perseveres to a consistent finish after an error — the behaviour the Chief Examiner contrasts with abandoning work at the first difficulty.',
        cite: CER15('p.20'),
      },
    },
    {
      id: 'm1-c',
      label: 'Script C',
      persona: 'Just the answer',
      work: ['10'],
      keyLevelId: 'full',
      keyNote:
        'On this question the marking note says a correct answer earns full credit even without supporting work — 10/10. But be careful: that is question-specific generosity. The scheme’s DEFAULT is the opposite: an answer without sufficient supporting work is generally awarded the lowest non-zero credit. Never bet an exam on the generous case.',
    },
    {
      id: 'm1-d',
      label: 'Script D',
      persona: 'Confident — and off the syllabus',
      work: ['Distance = (8 + 9) − (2 + 1)', '= 14'],
      keyLevelId: 'none',
      keyNote:
        'Adding coordinates and subtracting is not a distance method — there is no relevant formula, no relevant procedure, nothing the scheme can call merit. “Response of no substantial merit”: 0/10.',
    },
  ],
  takeaway: {
    id: 'codex-m1',
    rule: 'The relevant formula is never worth zero.',
    detail:
      'Maths scales start paying at “work of merit”, and a correct relevant formula is work of merit by rule. Write the formula before you panic — it is the difference between 0 and 4 on a 10C scale.',
    cite: MS23('p.[29]'),
  },
};

// ─────────────────────────── M2 · Count the steps ───────────────────────────

const M2: ScaleSession = {
  mode: 'scale',
  id: 'maths-steps',
  subject: 'maths',
  level: 'common',
  title: 'Count the steps',
  cue: 'Find',
  question: 'Find the coordinates of the points where the line y = x + 1 meets the circle x² + y² = 25.',
  questionNote:
    'Question authored for this exercise; the SEC 2023 OL scheme marked its line-meets-circle question (Q2(b)) on Scale 15D by enumerating the four solution steps and mapping them onto the ladder, exactly as below.',
  scale: {
    name: '15D',
    levels: SCALE_15D,
    notes: [
      'Four steps: ① substitute the line into the circle; ② simplify to a quadratic; ③ solve for the first variable; ④ find the second variable.',
      'Low partial credit: some work of merit — e.g. work in isolating/substituting one variable.',
      'Mid partial credit: two steps correct.',
      'High partial credit: three steps correct.',
      'Full credit: all four steps — both points found.',
    ],
    cite: MS23('p.[35] (Q2(b) notes; scale table p.[28])'),
  },
  scripts: [
    {
      id: 'm2-a',
      label: 'Script A',
      persona: 'One step in',
      work: ['x² + (x + 1)² = 25'],
      keyLevelId: 'low',
      keyNote:
        'Step ① done: the line is substituted into the circle. One step on a four-step ladder is “some work of merit” — low partial credit, 5/15. Five marks for one line.',
    },
    {
      id: 'm2-b',
      label: 'Script B',
      persona: 'Reaches the quadratic, stalls',
      work: [
        'x² + (x + 1)² = 25',
        'x² + x² + 2x + 1 = 25',
        '2x² + 2x − 24 = 0',
        'x² + x − 12 = 0',
      ],
      keyLevelId: 'mid',
      keyNote:
        'Steps ① and ② correct — substituted and simplified to the right quadratic, then stopped at the factorising wall. Two steps = mid partial credit, 8/15. More than half marks without solving anything.',
    },
    {
      id: 'm2-c',
      label: 'Script C',
      persona: 'Forgot the second half of the question',
      work: [
        'x² + (x + 1)² = 25',
        '2x² + 2x − 24 = 0  →  x² + x − 12 = 0',
        '(x + 4)(x − 3) = 0',
        'x = 3 and x = −4',
      ],
      keyLevelId: 'high',
      keyNote:
        'Steps ①–③ correct, but the question asked for POINTS — the y-values were never found. Three steps = high partial credit, 12/15. Three marks lost to reading, not to maths.',
      embodies: {
        behaviour: 'Completes the calculation but does not answer the question actually asked — a recurring examiner theme.',
        cite: CER15('p.22'),
      },
    },
    {
      id: 'm2-d',
      label: 'Script D',
      persona: 'All four steps',
      work: [
        'x² + (x + 1)² = 25',
        '2x² + 2x − 24 = 0  →  x² + x − 12 = 0',
        '(x + 4)(x − 3) = 0  →  x = 3 and x = −4',
        'y = x + 1  →  y = 4 and y = −3.  Points: (3, 4) and (−4, −3)',
      ],
      keyLevelId: 'full',
      keyNote: 'All four steps, both points. 15/15.',
    },
  ],
  takeaway: {
    id: 'codex-m2',
    rule: 'Long questions are marked in steps.',
    detail:
      'The examiner maps your progress onto the ladder step by step — every step you write is credit banked. Never abandon a multi-step question at the first wall: the next rung may be one line away.',
    cite: MS23('p.[35]'),
  },
};

// ─────────────────────── M3 · Say the conclusion ───────────────────────

const M3: ScaleSession = {
  mode: 'scale',
  id: 'maths-conclusion',
  subject: 'maths',
  level: 'common',
  title: 'Say the conclusion',
  cue: 'Verify',
  question: 'Verify that the point (−3, 4) lies on the circle x² + y² = 25.',
  questionNote:
    'Question authored for this exercise; the SEC 2023 OL scheme’s point-on-circle verification (Q2(a)(ii)) carried the marking note “Full Credit (−1): No conclusion” — the rule this session trains.',
  scale: {
    name: '10C (with Full credit −1)',
    levels: SCALE_10C_STAR,
    notes: [
      'Low partial credit: work of merit — e.g. some substitution into the circle equation.',
      'High partial credit: fully substituted with an error, finished consistently.',
      'Full credit −1: correct verification with NO conclusion stated.',
      'Full credit: correct verification with the conclusion stated.',
    ],
    cite: MS23('p.[34] (Q2(a)(ii) note; Full Credit −1 rule p.[29])'),
  },
  scripts: [
    {
      id: 'm3-a',
      label: 'Script A',
      persona: 'The silent calculation',
      work: ['(−3)² + (4)² = 9 + 16', '= 25'],
      keyLevelId: 'fullminus',
      keyNote:
        'The verification is complete and correct — but the script never SAYS what it shows. “Verify” questions require the conclusion: 25 = r², so the point lies on the circle. The scheme’s note for exactly this omission: Full Credit −1. 9/10 — one mark for one missing sentence.',
      embodies: {
        behaviour: 'Correct working with no conclusion drawn — examiners note candidates who calculate and then forget to conclude.',
        cite: MS23('p.[34]'),
      },
    },
    {
      id: 'm3-b',
      label: 'Script B',
      persona: 'Calculates something — the wrong something',
      work: ['Centre = (0, 0), radius = 5', 'Point (−3, 4) plotted on a sketch'],
      keyLevelId: 'low',
      keyNote:
        'Reading the centre and radius from the equation and engaging with the point is work of merit — but nothing verifies anything yet. Low partial credit, 4/10.',
    },
    {
      id: 'm3-c',
      label: 'Script C',
      persona: 'Slip, finished consistently',
      work: ['(−3)² + (4)² = −9 + 16', '= 7', '7 ≠ 25, so the point is not on the circle'],
      keyLevelId: 'high',
      keyNote:
        'One sign error — (−3)² taken as −9 — then finished correctly and consistently from that error, conclusion included. High partial credit, 6/10. Note the conclusion is stated; the error is in the squaring, not the logic.',
    },
    {
      id: 'm3-d',
      label: 'Script D',
      persona: 'Shows it and says it',
      work: ['(−3)² + (4)² = 9 + 16 = 25', '25 = 5² = r²', '⟹ the point (−3, 4) lies on the circle'],
      keyLevelId: 'full',
      keyNote: 'Correct working AND the conclusion in words. 10/10.',
    },
  ],
  takeaway: {
    id: 'codex-m3',
    rule: '“Show that” isn’t finished until you say the conclusion.',
    detail:
      'On verify/show-that questions, a perfect calculation with no stated conclusion is Full Credit −1 by rule. End with the sentence: “… ⟹ the point lies on the circle.”',
    cite: MS23('p.[34]'),
  },
};

// ─────────────────────── M4 · The one-mark star ───────────────────────

const M4: ScaleSession = {
  mode: 'scale',
  id: 'maths-star',
  subject: 'maths',
  level: 'common',
  title: 'The one-mark star (F✱)',
  cue: 'Calculate',
  question: 'A circular pond has radius 3.7 m. Calculate its area in m², correct to two decimal places.',
  questionNote:
    'Question authored for this exercise; the Full Credit −1 rule and rounding penalty are quoted from the SEC 2023 OL scheme’s general instructions, which apply across LC Mathematics.',
  scale: {
    name: '10C (with Full credit −1)',
    levels: SCALE_10C_STAR,
    notes: [
      'Low partial credit: work of merit — e.g. the relevant formula (A = πr²) written.',
      'High partial credit: correct formula fully substituted; or error in substitution, finished consistently.',
      'Full credit −1 (✱): incorrect rounding, omitted units where required, a misreading or arithmetic slip that does not oversimplify the work.',
      'A rounding penalty is applied each time it occurs. No penalty for omitted units when the question specifies the unit (as here: “in m²”).',
    ],
    cite: MS23('p.[29] (Full Credit −1 and rounding rules)'),
  },
  scripts: [
    {
      id: 'm4-a',
      label: 'Script A',
      persona: 'Right method, lazy rounding',
      work: ['A = πr² = π(3.7)²', '= π × 13.69', '= 43.0084…', '= 43.00 m²'],
      keyLevelId: 'fullminus',
      keyNote:
        'Method and arithmetic are perfect; 43.0084… truncated to 43.00 instead of rounded to 43.01. Incorrect rounding is the textbook Full Credit −1 case: 9/10. The star costs one mark every time it happens — across a paper, that adds up.',
      embodies: {
        behaviour: 'Loses the accuracy mark to rounding — a skill the Chief Examiner says is “not conceptually challenging” and should be routine.',
        cite: CER15('p.30'),
      },
    },
    {
      id: 'm4-b',
      label: 'Script B',
      persona: 'Formula only',
      work: ['A = πr²'],
      keyLevelId: 'low',
      keyNote: 'The relevant formula is work of merit: low partial credit, 4/10.',
    },
    {
      id: 'm4-c',
      label: 'Script C',
      persona: 'Clean to the last digit',
      work: ['A = πr² = π(3.7)² = π × 13.69', '= 43.0084…', '= 43.01 m²'],
      keyLevelId: 'full',
      keyNote:
        'Correct method, correct rounding to two decimal places, unit included. 10/10. (Had the unit been omitted, no penalty here — the question specified m², and the scheme waives the unit penalty in that case.)',
    },
  ],
  takeaway: {
    id: 'codex-m4',
    rule: 'Method gets you to 10 — presentation keeps you there.',
    detail:
      'Rounding, required formats and misread-but-not-oversimplified slips each cost exactly one mark (Full Credit −1), and the rounding penalty repeats every time. Check the required accuracy before you write the final line.',
    cite: MS23('p.[29]'),
  },
};

// ─────────────── M5 · Foundation — right answer, wrong detail ───────────────

const M5: ScaleSession = {
  mode: 'scale',
  id: 'maths-fl-detail',
  subject: 'maths',
  level: 'foundation',
  title: 'Right answer, wrong detail',
  cue: 'Find',
  question: 'A Foundation-level question asks for the coordinates of a point. The candidate’s working is perfect and finds the right numbers — but writes the point as (7, 4) when it should be (4, 7). The part is worth 10 marks. What does it score?',
  questionNote:
    'Question authored for this exercise; the Foundation scheme applies Full Credit −1 for a correct result presented with the wrong detail — coordinate order, a wrong label, a missing unit or bad rounding.',
  scale: {
    name: '10-mark item · Full credit −1',
    levels: [
      { id: 'm5', label: 'High partial (5)', annotation: 'H', marks: 5 },
      { id: 'm9', label: 'Full credit −1 (9)', annotation: 'F✱', marks: 9 },
      { id: 'm10', label: 'Full credit (10)', annotation: '✓', marks: 10 },
    ],
    notes: [
      'The working is correct and finds the right numbers.',
      'Writing the coordinates in the wrong order, (7, 4) for (4, 7), is a presentation slip.',
      'Full Credit −1 applies: the same one-mark deduction as a wrong label, missing unit or bad rounding.',
    ],
    cite: MSFL('p.14 (coordinate order, Full Credit −1)'),
  },
  scripts: [
    {
      id: 'm5-a',
      label: 'The answer',
      persona: 'Right point, wrong order',
      work: ['Correct working throughout.', 'Answer written as (7, 4) — it should be (4, 7).'],
      keyLevelId: 'm9',
      keyNote:
        '9 of 10 — Full Credit −1. The maths is right; only the order is wrong, and that’s a one-mark presentation slip, the same family as a missing unit or bad rounding. These “right answer, wrong detail” marks are the easiest to protect: write x first then y, label the right figure to the right thing, and always include the unit.',
      embodies: {
        behaviour: 'Gets the right result but writes it with the wrong detail (coordinate order) — Full Credit −1.',
        cite: MSFL('p.14'),
      },
    },
  ],
  takeaway: {
    id: 'codex-m5',
    rule: 'Protect the presentation marks — order, label, unit, rounding.',
    detail:
      'At Foundation Level, a correct answer written with the wrong detail — coordinates out of order, a figure on the wrong label, a missing unit, bad rounding — is Full Credit −1. The maths is done; don’t give a mark back on the last line.',
    cite: MSFL('p.14'),
  },
};

export const MATHS_CHAIR: ChairSubject = {
  id: 'maths',
  label: 'Mathematics',
  tagline: 'Scales, steps and stars — how maths scripts are really graded.',
  offeredLevels: ['higher', 'ordinary', 'foundation'],
  sessions: [M1, M2, M3, M4, M5],
  sources: [
    { label: 'SEC LC Mathematics OL marking scheme 2023, Paper 2 portion (examiner-reports/maths/2023-marking-scheme-ol-p2)' },
    { label: 'Chief Examiner’s Report, Mathematics 2015 (examiner-reports/maths/2015-chief-examiner)' },
  ],
  coverageNote:
    'Maths is marked on the same scale system — A–D scales, the partial-credit ladders, work-of-merit and Full Credit −1 — at Higher, Ordinary and Foundation level, so these sessions teach the system that applies at every level. The example questions are pitched around Ordinary Level; harder HL-specific worked examples are being added.',
};
