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
 *  - SEC LC Mathematics marking scheme 2024, Higher Level (Papers 1 & 2) —
 *    examiner-reports/maths/2024-hl-marking-scheme.*
 *  - Chief Examiner's Report, Mathematics 2015 — examiner-reports/maths/2015-*
 * Claim-by-claim record: compliance/evidence/examinersChair.md.
 */

import { type ChairSubject, type ScaleSession, type ScaleLevel } from './types';

const MS23 = (p: string) => ({ label: `SEC Mathematics OL marking scheme 2023, ${p}` });
const MS24 = (p: string) => ({ label: `SEC Mathematics HL marking scheme 2024, ${p}` });
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
// 10-mark D scale (five categories), verified from the 2024 HL scale table
// (marking scheme p.[4]): "10 mark scales … 0, 3, 5, 7, 10".
const SCALE_10D: ScaleLevel[] = [
  { id: 'none', label: 'No credit', annotation: '✗', marks: 0 },
  { id: 'low', label: 'Low partial credit', annotation: 'L', marks: 3 },
  { id: 'mid', label: 'Mid partial credit', annotation: 'M', marks: 5 },
  { id: 'high', label: 'High partial credit', annotation: 'H', marks: 7 },
  { id: 'full', label: 'Full credit', annotation: '✓', marks: 10 },
];
// HL 10D with Full credit −1 = 9 (10-mark D scale + F✱), verified from the 2024
// HL scale table (p.[4], "10 mark scales D: 0, 3, 5, 7, 10") and the Full
// Credit −1 rule (p.[5]).
const SCALE_10D_STAR: ScaleLevel[] = [
  SCALE_10D[0],
  SCALE_10D[1],
  SCALE_10D[2],
  SCALE_10D[3],
  { id: 'fullminus', label: 'Full credit −1', annotation: 'F✱', marks: 9 },
  SCALE_10D[4],
];
// HL 5C scale (four categories) + Full credit −1 = 4, verified from the 2024 HL
// scale table (p.[4], "5 mark scales C: 0, 2, 3, 5").
const SCALE_5C_STAR: ScaleLevel[] = [
  { id: 'none', label: 'No credit', annotation: '✗', marks: 0 },
  { id: 'low', label: 'Low partial credit', annotation: 'L', marks: 2 },
  { id: 'high', label: 'High partial credit', annotation: 'H', marks: 3 },
  { id: 'fullminus', label: 'Full credit −1', annotation: 'F✱', marks: 4 },
  { id: 'full', label: 'Full credit', annotation: '✓', marks: 5 },
];
// HL 15D scale (five categories), verified from the 2024 HL scale table
// (p.[4], "15 mark scale D: 0, 4, 6, 8, 15"). Distinct from the OL 15D above.
const SCALE_15D_HL: ScaleLevel[] = [
  { id: 'none', label: 'No credit', annotation: '✗', marks: 0 },
  { id: 'low', label: 'Low partial credit', annotation: 'L', marks: 4 },
  { id: 'mid', label: 'Mid partial credit', annotation: 'M', marks: 6 },
  { id: 'high', label: 'High partial credit', annotation: 'H', marks: 8 },
  { id: 'full', label: 'Full credit', annotation: '✓', marks: 15 },
];
// 2025 Foundation Level scales, verified from the Foundation scale table
// (2025 Foundation marking scheme p.[4]): 10C "0, 4, 6, 10" and 10D
// "0, 4, 5, 7, 10". Full Credit −1 = 9 on a 10-mark scale (p.[5]).
const SCALE_F10C: ScaleLevel[] = [
  { id: 'none', label: 'No credit', annotation: '✗', marks: 0 },
  { id: 'low', label: 'Low partial credit', annotation: 'L', marks: 4 },
  { id: 'high', label: 'High partial credit', annotation: 'H', marks: 6 },
  { id: 'full', label: 'Full credit', annotation: '✓', marks: 10 },
];
const SCALE_F10C_STAR: ScaleLevel[] = [
  SCALE_F10C[0],
  SCALE_F10C[1],
  SCALE_F10C[2],
  { id: 'fullminus', label: 'Full credit −1', annotation: 'F✱', marks: 9 },
  SCALE_F10C[3],
];
const SCALE_F10D: ScaleLevel[] = [
  { id: 'none', label: 'No credit', annotation: '✗', marks: 0 },
  { id: 'low', label: 'Low partial credit', annotation: 'L', marks: 4 },
  { id: 'mid', label: 'Mid partial credit', annotation: 'M', marks: 5 },
  { id: 'high', label: 'High partial credit', annotation: 'H', marks: 7 },
  { id: 'full', label: 'Full credit', annotation: '✓', marks: 10 },
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
    {
      id: 'm4-d',
      label: 'Script D',
      persona: 'Right formula, one square slips',
      work: ['A = πr² = π(3.7)²', '= π × 12.69', '= 39.8672…', '= 39.87 m²'],
      keyLevelId: 'high',
      keyNote:
        'The formula is fully substituted and the work is finished consistently — but 3.7² is taken as 12.69 instead of 13.69, so the answer is wrong. That is “error in substitution, finished consistently”: high partial credit, 6/10. Note the difference from Script A — this slip changes the answer, so it lands two rungs lower than the rounding star, not on Full Credit −1. The rounding here is correct; it is the arithmetic that costs the marks.',
      embodies: {
        behaviour: 'Substitutes correctly, makes an arithmetic slip, and carries it through to a consistent finish — the scheme’s definition of high partial credit.',
        cite: MS23('p.[29]'),
      },
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

// ───────────── M6 · Higher — the oversimplify ceiling ─────────────

const M6: ScaleSession = {
  mode: 'scale',
  id: 'maths-oversimplify',
  subject: 'maths',
  level: 'higher',
  title: 'The oversimplify ceiling',
  cue: 'Solve',
  question: 'Find the values of x for which x² − 5x + 6 ≤ 0.',
  questionNote:
    'Question authored for this exercise; the ladder and the “oversimplify → low partial credit at most” cap mirror the SEC 2024 HL scheme’s quadratic-inequality question (Q10(b)), which used Scale 10D with the note “For a linear inequality, award low partial credit at most”.',
  scale: {
    name: '10D',
    levels: SCALE_10D,
    notes: [
      'Correct answer: (x − 2)(x − 3) ≤ 0, so the quadratic is below zero between the roots — 2 ≤ x ≤ 3.',
      'Low partial credit: work of merit — the inequality rearranged to standard form, or one value trialled.',
      'Mid partial credit: the quadratic factorised (or the quadratic formula fully substituted).',
      'High partial credit: the roots found — x = 2 and x = 3.',
      'Full credit: the correct solution set, 2 ≤ x ≤ 3.',
      'Oversimplify cap: if the squared term is dropped and a LINEAR inequality solved, award low partial credit at most — however cleanly it finishes.',
    ],
    cite: MS24('p.[26] (Q10(b) inequality ladder and the “linear inequality → low partial credit at most” cap); “Oversimplify” annotation p.[5]; scale table p.[4]'),
  },
  scripts: [
    {
      id: 'm6-a',
      label: 'Script A',
      persona: 'Drops the square',
      work: ['x² − 5x + 6 ≤ 0', '−5x + 6 ≤ 0', '−5x ≤ −6', 'x ≥ 6/5'],
      keyLevelId: 'low',
      keyNote:
        'The squared term is simply dropped and a linear inequality solved — cleanly, even. But turning a quadratic inequality into a linear one is oversimplifying, and the scheme caps oversimplified work at low partial credit however tidy the finish: 3/10. The clean algebra after the shortcut earns nothing extra — the ceiling was set the moment the x² went missing.',
      embodies: {
        behaviour: 'Oversimplifies — solves a linear inequality in place of the quadratic — which the scheme caps at low partial credit at most.',
        cite: MS24('p.[26]'),
      },
    },
    {
      id: 'm6-b',
      label: 'Script B',
      persona: 'Factorises, then stops',
      work: ['x² − 5x + 6 ≤ 0', '(x − 2)(x − 3) ≤ 0'],
      keyLevelId: 'mid',
      keyNote:
        'The quadratic is kept whole and factorised correctly — genuine progress on the real problem, not a shortcut around it. Factorising is mid partial credit: 5/10. Two rungs above Script A for doing strictly less arithmetic, because it engaged the quadratic instead of dodging it.',
    },
    {
      id: 'm6-c',
      label: 'Script C',
      persona: 'Right roots, wrong direction',
      work: ['(x − 2)(x − 3) ≤ 0', 'x = 2, x = 3', 'x ≤ 2 or x ≥ 3'],
      keyLevelId: 'high',
      keyNote:
        'Both roots found — high partial credit, 7/10 — but the solution set points the wrong way. For ≤ 0 the quadratic sits below the axis BETWEEN the roots, so it is 2 ≤ x ≤ 3, not outside them. “Roots of quadratic found” is the high rung; the final direction is the last mark.',
    },
    {
      id: 'm6-d',
      label: 'Script D',
      persona: 'All the way',
      work: ['x² − 5x + 6 ≤ 0', '(x − 2)(x − 3) ≤ 0', 'x = 2, x = 3', '2 ≤ x ≤ 3'],
      keyLevelId: 'full',
      keyNote: 'Kept the quadratic, factorised, found the roots, and read the correct interval between them. 10/10.',
    },
  ],
  takeaway: {
    id: 'codex-m6',
    rule: 'Oversimplifying caps your marks — no clean finish can lift it.',
    detail:
      'When you drop a term or downgrade a quadratic to a linear problem, the scheme sets a ceiling — low partial credit at most — before you write another line. Solve the problem you were actually given, even if it is harder: a messy attempt at the real question outscores a tidy solution to an easier one.',
    cite: MS24('p.[26]'),
  },
};

// ─────────── M7 · Higher — when the question names the method ───────────

const M7: ScaleSession = {
  mode: 'scale',
  id: 'maths-first-principles',
  subject: 'maths',
  level: 'higher',
  title: 'When the question names the method',
  cue: 'Differentiate from first principles',
  question: 'Differentiate f(x) = x² − 7x − 10 from first principles.',
  questionNote:
    'Question adapted from the SEC 2024 HL scheme’s first-principles item (Q4(a), f(x) = x² − 7x − 10); the Scale 10D ladder and the note “No credit if first principles is not used” are the real ones.',
  scale: {
    name: '10D',
    levels: SCALE_10D,
    notes: [
      'No credit if first principles is not used — a correct derivative reached by the power rule scores zero here.',
      'Low partial credit: work of merit — e.g. f(x + h) written down.',
      'Mid partial credit: f(x + h) expanded correctly, or f(x + h) − f(x) left unsimplified.',
      'High partial credit: f(x + h) − f(x) = 2hx + h² − 7h, or the complete difference quotient without the limit line.',
      'Full credit: the full first-principles derivation, ending f′(x) = 2x − 7.',
    ],
    cite: MS24('p.[13] (Q4(a) first-principles notes and the “No credit if first principles is not used” gate); scale table p.[4]'),
  },
  scripts: [
    {
      id: 'm7-a',
      label: 'Script A',
      persona: 'Right answer, forbidden method',
      work: ['f(x) = x² − 7x − 10', 'f′(x) = 2x − 7'],
      keyLevelId: 'none',
      keyNote:
        'The derivative is exactly right — but it was written straight down by the power rule, and the question said “from first principles”. The scheme’s note is blunt: No credit if first principles is not used. 0/10 for a correct answer, because the method was the thing being tested. When a question names a method, that method IS the marks.',
      embodies: {
        behaviour: 'Reaches the correct derivative by the power rule rather than the prescribed first-principles method, which the scheme gates to zero.',
        cite: MS24('p.[13]'),
      },
    },
    {
      id: 'm7-b',
      label: 'Script B',
      persona: 'Starts it properly',
      work: ['f(x + h) = (x + h)² − 7(x + h) − 10'],
      keyLevelId: 'low',
      keyNote:
        'One correct first-principles line — f(x + h) written out — is work of merit and clears the zero-gate because it uses the prescribed method: low partial credit, 3/10. Script A did far more algebra and scored nothing; this did one honest line the right way and banks 3.',
    },
    {
      id: 'm7-c',
      label: 'Script C',
      persona: 'Halfway down',
      work: [
        'f(x + h) = (x + h)² − 7(x + h) − 10',
        '= x² + 2hx + h² − 7x − 7h − 10',
        'f(x + h) − f(x) = (x² + 2hx + h² − 7x − 7h − 10) − (x² − 7x − 10)',
      ],
      keyLevelId: 'mid',
      keyNote:
        'f(x + h) is expanded correctly and the difference f(x + h) − f(x) is set up but not yet simplified. The scheme lists “f(x + h) expanded correctly” and “f(x + h) − f(x) unsimplified” as mid partial credit: 5/10. Halfway down the derivation, half the marks.',
    },
    {
      id: 'm7-d',
      label: 'Script D',
      persona: 'Full derivation',
      work: [
        'f(x + h) − f(x) = 2hx + h² − 7h',
        '[f(x + h) − f(x)] / h = 2x + h − 7',
        'lim (h→0) (2x + h − 7) = 2x − 7',
        'f′(x) = 2x − 7',
      ],
      keyLevelId: 'full',
      keyNote:
        'The full first-principles chain — form the difference, divide by h, take the limit as h → 0 — ending at 2x − 7. 10/10. The same answer as Script A, but earned the way the question demanded.',
    },
  ],
  takeaway: {
    id: 'codex-m7',
    rule: 'When the question names the method, the method is the marks.',
    detail:
      '“From first principles”, “using de Moivre’s theorem”, “by integration” are not suggestions — the scheme gates these questions to zero if you reach the answer another way. Read the instruction word before you start, and use the tool it names even if a faster one exists.',
    cite: MS24('p.[13]'),
  },
};

// ─────────────── M8 · Own work carries forward ───────────────

const M8: ScaleSession = {
  mode: 'scale',
  id: 'maths-own-work',
  subject: 'maths',
  level: 'common',
  title: 'Own work carries forward',
  cue: 'Hence',
  question:
    'Part (i) asked for the radius of a circle; the candidate answered r = 6·2 cm (the correct value was 6·0 cm). Part (ii): “Hence find the area of the circle, correct to one decimal place.” How is part (ii) marked?',
  questionNote:
    'Question authored for this exercise; the rule that a candidate’s earlier work is accepted in later parts (unless it oversimplifies) is the real SEC 2023 OL general instruction, reinforced by the Q8(c)(iii) “Use of Ans” note.',
  scale: {
    name: '10C (own-work carry-forward)',
    levels: SCALE_10C,
    notes: [
      'General rule: accept the candidate’s work from one part of a question for use in later parts — unless using it oversimplifies the work.',
      'Low partial credit: work of merit — the area formula A = πr² written.',
      'High partial credit: the formula fully substituted with the candidate’s own radius.',
      'Full credit: the area found correctly from the candidate’s OWN radius — the earlier error is penalised in part (i), not again here.',
      'Exception: if the carried value makes THIS part trivial (oversimplifies it), the carry-forward is not accepted.',
    ],
    cite: MS23('p.[29] (accept earlier work in later parts); Q8(c)(iii) “Use of Ans” note p.[49]'),
  },
  scripts: [
    {
      id: 'm8-a',
      label: 'Script A',
      persona: 'Wrong radius, carried correctly',
      work: ['A = πr² = π(6·2)²', '= π × 38·44', '= 120·76…', '= 120·8 cm²'],
      keyLevelId: 'full',
      keyNote:
        'The radius is wrong — but it is the candidate’s OWN answer from part (i), and part (ii) uses it correctly and finishes. The scheme accepts own work in later parts, so part (ii) earns full credit: 10/10. The error is charged once, in part (i); it is not charged a second time here.',
      embodies: {
        behaviour: 'Carries an incorrect earlier answer correctly into a later part — accepted as own work by the scheme.',
        cite: MS23('p.[29]'),
      },
    },
    {
      id: 'm8-b',
      label: 'Script B',
      persona: 'Formula only',
      work: ['A = πr²'],
      keyLevelId: 'low',
      keyNote: 'The relevant formula is work of merit: low partial credit, 4/10.',
    },
    {
      id: 'm8-c',
      label: 'Script C',
      persona: 'Own radius, one slip',
      work: ['A = πr² = π(6·2)²', '= π × 36·44', '= 114·48…', '= 114·5 cm²'],
      keyLevelId: 'high',
      keyNote:
        'Uses the own radius and finishes consistently, but squares 6·2 as 36·44 instead of 38·44 — an error in substitution, carried through cleanly. High partial credit, 6/10.',
    },
  ],
  takeaway: {
    id: 'codex-m8',
    rule: 'Your earlier answer becomes your material — use it, and you are not charged twice.',
    detail:
      'The scheme accepts your own work from an earlier part when you use it in a later one, so a slip in part (i) costs you only in part (i). Carry your own number forward confidently — the exception is only when doing so makes the later part trivially easy.',
    cite: MS23('p.[29]'),
  },
};

// ─────────────── M9 · Don’t drop the ± ───────────────

const M9: ScaleSession = {
  mode: 'scale',
  id: 'maths-both-values',
  subject: 'maths',
  level: 'higher',
  title: 'Don’t drop the ±',
  cue: 'Find',
  question: 'Solving for the common ratio of a geometric sequence gives 6r⁴ = 3/8. Find r.',
  questionNote:
    'Question adapted from the SEC 2024 HL scheme’s geometric-sequence item (Q5(b), 6r⁴ = 3/8); the Scale 5C ladder and the note “Apply a * if only 1 value of r is given” are the real ones.',
  scale: {
    name: '5C (with Full credit −1)',
    levels: SCALE_5C_STAR,
    notes: [
      'Low partial credit: work of merit in forming an equation in r.',
      'High partial credit: r⁴ = 1/16 reached correctly.',
      'Full credit −1: only ONE value of r given — the ± is dropped.',
      'Full credit: both values, r = ±1/2.',
    ],
    cite: MS24('p.[16] (Q5(b) note “Apply a * if only 1 value of r is given”); scale table p.[4]'),
  },
  scripts: [
    {
      id: 'm9-a',
      label: 'Script A',
      persona: 'Half the answer',
      work: ['6r⁴ = 3/8', 'r⁴ = 1/16', 'r = 1/2'],
      keyLevelId: 'fullminus',
      keyNote:
        'r⁴ = 1/16 has two real roots, +1/2 and −1/2, and the work only reports one. Dropping the negative root is exactly the scheme’s Full Credit −1 case: “Apply a * if only 1 value of r is given” — 4/5. One missing sign, one mark.',
      embodies: {
        behaviour: 'Gives only one value where an even power admits ±, dropping a valid solution — Full Credit −1.',
        cite: MS24('p.[16]'),
      },
    },
    {
      id: 'm9-b',
      label: 'Script B',
      persona: 'Both roots',
      work: ['6r⁴ = 3/8', 'r⁴ = 1/16', 'r = ±1/2'],
      keyLevelId: 'full',
      keyNote: 'Both values reported. 5/5.',
    },
    {
      id: 'm9-c',
      label: 'Script C',
      persona: 'One line short',
      work: ['6r⁴ = 3/8', 'r⁴ = 3/48 = 1/16'],
      keyLevelId: 'high',
      keyNote: 'Reaches r⁴ = 1/16 but stops before taking the fourth root. That is the high-partial line: 3/5.',
    },
    {
      id: 'm9-d',
      label: 'Script D',
      persona: 'Just starting',
      work: ['6r⁴ = 3/8', 'r⁴ = (3/8) ÷ 6'],
      keyLevelId: 'low',
      keyNote: 'Work of merit in forming an equation in r: low partial credit, 2/5.',
    },
  ],
  takeaway: {
    id: 'codex-m9',
    rule: 'An even power hides a second root — report the ±.',
    detail:
      'Square roots and fourth roots have a positive AND a negative solution; giving only one is Full Credit −1 by rule. Whenever you undo an even power, write ± first and then decide, from the context, which values survive.',
    cite: MS24('p.[16]'),
  },
};

// ─────────────── M10 · The MPC ceiling ───────────────

const M10: ScaleSession = {
  mode: 'scale',
  id: 'maths-mpc-cap',
  subject: 'maths',
  level: 'higher',
  title: 'The MPC ceiling',
  cue: 'Differentiate',
  question: 'Differentiate g(x) = (6x + 1)/(x⁴ + 3) and find g′(−2).',
  questionNote:
    'Question adapted from the SEC 2024 HL scheme’s quotient item (Q4(b)); the Scale 10D four-step ladder and the note “Award MPC at most if quotient/product rule is not used” are the real ones.',
  scale: {
    name: '10D',
    levels: SCALE_10D,
    notes: [
      'Four steps: ① find du/dx; ② find dv/dx; ③ correct substitution into the quotient (or product) rule; ④ evaluate g′(−2).',
      'Low partial credit: work of merit in one step.',
      'Mid partial credit: two steps correct.',
      'High partial credit: three steps correct.',
      'Full credit: g′(−2) = −238/361.',
      'Method cap: if the quotient/product rule is NOT used, award mid partial credit at most — however far the work is carried.',
    ],
    cite: MS24('p.[13] (Q4(b) ladder and the “Award MPC at most if quotient/product rule is not used” cap); scale table p.[4]'),
  },
  scripts: [
    {
      id: 'm10-a',
      label: 'Script A',
      persona: 'Skips the rule, gets a number',
      work: ['g′(x) = 6 / (4x³)   ← derivative of top over derivative of bottom', 'g′(−2) = 6 / (4(−2)³) = 6/−32 = −3/16'],
      keyLevelId: 'mid',
      keyNote:
        'A clean final number — but it was reached by differentiating the numerator over the denominator separately, which is NOT the quotient rule. The scheme caps that at mid partial credit however tidily it finishes: 5/10. The ceiling is set by the method chosen, not by how far it is carried.',
      embodies: {
        behaviour: 'Reaches an answer without the quotient/product rule, which the scheme caps at mid partial credit.',
        cite: MS24('p.[13]'),
      },
    },
    {
      id: 'm10-b',
      label: 'Script B',
      persona: 'Rule set up, not evaluated',
      work: ['u = 6x + 1,  v = x⁴ + 3', 'du/dx = 6,  dv/dx = 4x³', 'g′(x) = [(x⁴ + 3)(6) − (6x + 1)(4x³)] / (x⁴ + 3)²'],
      keyLevelId: 'high',
      keyNote:
        'Three of the four steps done — both derivatives found and correctly substituted into the quotient rule — but g′(−2) not evaluated. Three steps = high partial credit, 7/10. Two rungs above Script A while doing the harder, correct thing.',
    },
    {
      id: 'm10-c',
      label: 'Script C',
      persona: 'One step in',
      work: ['u = 6x + 1,  v = x⁴ + 3', 'du/dx = 6'],
      keyLevelId: 'low',
      keyNote: 'Work of merit in one step: low partial credit, 3/10.',
    },
    {
      id: 'm10-d',
      label: 'Script D',
      persona: 'All the way',
      work: ['g′(x) = [(x⁴ + 3)(6) − (6x + 1)(4x³)] / (x⁴ + 3)²', 'g′(−2) = −238/361'],
      keyLevelId: 'full',
      keyNote: 'Quotient rule used, fully substituted and evaluated. 10/10.',
    },
  ],
  takeaway: {
    id: 'codex-m10',
    rule: 'The wrong tool caps your marks even when the answer comes out.',
    detail:
      'Some questions cap credit at mid partial if you avoid the named rule (quotient, product, de Moivre, complex form) — softer than a zero gate, but still a ceiling set the moment you choose the shortcut. Reach for the rule the topic is testing, even when a back-of-envelope route seems to land.',
    cite: MS24('p.[13]'),
  },
};

// ─────────────── M11 · Eliminate the impostor root ───────────────

const M11: ScaleSession = {
  mode: 'scale',
  id: 'maths-eliminate-root',
  subject: 'maths',
  level: 'higher',
  title: 'Eliminate the impostor root',
  cue: 'Solve',
  question: 'Solve (n − 3)² = 3n + 1 for n, and state the valid solution.',
  questionNote:
    'Question adapted from the SEC 2024 HL scheme’s surd-equation item (Q1(a), where n = 1 gives −2 = √4 and must be rejected); the Scale 10D ladder and the note “Apply a * for incorrect solution(s) not eliminated” are the real ones.',
  scale: {
    name: '10D (with Full credit −1)',
    levels: SCALE_10D_STAR,
    notes: [
      'Low partial credit: work of merit — an indication of squaring, or values trialled.',
      'Mid partial credit: the fully correct quadratic, n² − 9n + 8 = 0.',
      'High partial credit: the quadratic factorised, (n − 8)(n − 1) = 0.',
      'Full credit −1: both roots given, but the invalid root (n = 1) not eliminated.',
      'Full credit: n = 8, with n = 1 rejected because it gives −2 = √4.',
    ],
    cite: MS24('p.[6] (Q1(a) ladder and “Apply a * for incorrect solution(s) not eliminated”); scale table p.[4]'),
  },
  scripts: [
    {
      id: 'm11-a',
      label: 'Script A',
      persona: 'Keeps both roots',
      work: ['(n − 3)² = 3n + 1', 'n² − 6n + 9 = 3n + 1', 'n² − 9n + 8 = 0', '(n − 8)(n − 1) = 0', 'n = 8,  n = 1'],
      keyLevelId: 'fullminus',
      keyNote:
        'The algebra is flawless and both roots are found — but n = 1 does not satisfy the original equation (it gives −2 = √4), and it is left standing. The scheme’s note is exact: “Apply a * for incorrect solution(s) not eliminated.” Full Credit −1, 9/10. The last mark is the sentence that throws the impostor out.',
      embodies: {
        behaviour: 'Finds every root but fails to reject the one that does not satisfy the original equation — Full Credit −1.',
        cite: MS24('p.[6]'),
      },
    },
    {
      id: 'm11-b',
      label: 'Script B',
      persona: 'Right quadratic, stops',
      work: ['(n − 3)² = 3n + 1', 'n² − 6n + 9 = 3n + 1', 'n² − 9n + 8 = 0'],
      keyLevelId: 'mid',
      keyNote: 'The fully correct quadratic, then a stop before factorising. Mid partial credit, 5/10.',
    },
    {
      id: 'm11-c',
      label: 'Script C',
      persona: 'Shows it and rejects it',
      work: ['n² − 9n + 8 = 0', '(n − 8)(n − 1) = 0', 'n = 8 or n = 1', 'n = 1 ⟹ −2 = √4  ✗, reject.  So n = 8'],
      keyLevelId: 'full',
      keyNote: 'Both roots found AND the invalid one tested and rejected against the original. 10/10.',
    },
    {
      id: 'm11-d',
      label: 'Script D',
      persona: 'Just squaring',
      work: ['(n − 3)² = 3n + 1', 'n² − 6n + 9 = 3n + 1'],
      keyLevelId: 'low',
      keyNote: 'An indication of squaring is work of merit: low partial credit, 3/10.',
    },
  ],
  takeaway: {
    id: 'codex-m11',
    rule: 'Squaring can breed a false root — test every solution in the original.',
    detail:
      'Squaring both sides, or solving a quadratic thrown up by a word problem, can produce a value that does not actually satisfy the original equation or its context. Leaving it in is Full Credit −1. Always substitute each root back and say which ones you are keeping and why.',
    cite: MS24('p.[6]'),
  },
};

// ─────────────── M12 · The graph is marked in parts ───────────────

const M12: ScaleSession = {
  mode: 'scale',
  id: 'maths-graph-parts',
  subject: 'maths',
  level: 'higher',
  title: 'The graph is marked in parts',
  cue: 'Complete and plot',
  question:
    'Complete the table of five values for T(x), plot the seven points, and join them with a smooth curve.',
  questionNote:
    'Question adapted from the SEC 2024 HL scheme’s table-and-graph item (Q8(a)); the “13 parts” count, the Scale 10D ladder and the Full Credit −1 for a graph with no table entries are the real ones. The “No labels (once only)” rule is the SEC 2023 OL Q9(a)(iv) note.',
  scale: {
    name: '10D (13-part graph)',
    levels: SCALE_10D_STAR,
    notes: [
      'The solution is 13 parts: 5 table values + 7 points plotted + points joined appropriately (a smooth curve, not line segments).',
      'Low partial credit: 1 part correct.',
      'Mid partial credit: 7 parts correct.',
      'High partial credit: 10 parts correct.',
      'Full credit −1: 12 parts correct — or a correct graph with no table entries; and missing labels cost Full Credit −1 (once only).',
      'Full credit: all 13 parts.',
    ],
    cite: MS24('p.[21] (Q8(a) “13 parts” count and Full Credit −1 rules); “No labels (once only)” SEC 2023 OL p.[51]; scale table p.[4]'),
  },
  scripts: [
    {
      id: 'm12-a',
      label: 'Script A',
      persona: 'Twelve of thirteen',
      work: ['Table: 5/5 values correct', 'Points plotted: 6/7 correct (one point off)', 'Curve joined smoothly', '→ 12 of 13 parts'],
      keyLevelId: 'fullminus',
      keyNote:
        'Twelve of the thirteen parts are right — one point is misplotted. On a part-counted graph the scheme reads that as Full Credit −1: 9/10. A single stray point is one mark, no more; the rest of the graph still banks.',
      embodies: {
        behaviour: 'Loses one of many discrete graph parts (a single misplotted point) — Full Credit −1 on a part-counted item.',
        cite: MS24('p.[21]'),
      },
    },
    {
      id: 'm12-b',
      label: 'Script B',
      persona: 'Half the parts',
      work: ['Table: 5/5 values correct', 'Points plotted: 2/7', 'Curve not yet joined', '→ 7 of 13 parts'],
      keyLevelId: 'mid',
      keyNote: 'Seven parts correct — the five table values and two points — is the mid rung: 5/10. Every value and every point is its own mark.',
    },
    {
      id: 'm12-c',
      label: 'Script C',
      persona: 'Ten parts',
      work: ['Table: 5/5 values correct', 'Points plotted: 5/7', 'Curve joined smoothly', '→ 10 of 13 parts'],
      keyLevelId: 'high',
      keyNote: 'Ten parts = high partial credit, 7/10.',
    },
    {
      id: 'm12-d',
      label: 'Script D',
      persona: 'One value',
      work: ['Table: 1/5 values correct', 'No points plotted', '→ 1 of 13 parts'],
      keyLevelId: 'low',
      keyNote: 'A single correct table value is one part — low partial credit, 3/10.',
    },
  ],
  takeaway: {
    id: 'codex-m12',
    rule: 'A graph is not one mark — it is a pile of small ones.',
    detail:
      'Table values, plotted points and the join are each counted separately, so a graph question rewards finishing every point and punishes leaving it half-drawn. Fill in every table cell, plot every point, join with a smooth curve, and label the axes — the labels themselves are a Full-Credit −1 line.',
    cite: MS24('p.[21]'),
  },
};

// ─────────────── M13 · Which penalties repeat ───────────────

const M13: ScaleSession = {
  mode: 'scale',
  id: 'maths-penalty-scope',
  subject: 'maths',
  level: 'ordinary',
  title: 'Which penalties repeat',
  cue: 'Find',
  question: 'Find the angle A, where tan A = 9/100, correct to the nearest degree.',
  questionNote:
    'Question adapted from the SEC 2023 OL scheme’s trigonometry item (Q7(a)(iv)); the Full Credit −1 star and the note “Incorrect Calculator Mode (Apply once in paper)” are the real ones.',
  scale: {
    name: '10C (with Full credit −1)',
    levels: SCALE_10C_STAR,
    notes: [
      'Low partial credit: work of merit — the relevant trig ratio written.',
      'High partial credit: A = tan⁻¹(9/100) reached.',
      'Full credit −1: correct method with the calculator in the wrong mode (radians/grad instead of degrees).',
      'Scope: the calculator-mode penalty is applied ONCE in the paper; a rounding penalty is applied EACH time it occurs.',
    ],
    cite: MS23('p.[45] (Q7(a)(iv) “Incorrect Calculator Mode — Apply once in paper”); rounding “each time” general rule p.[29]'),
  },
  scripts: [
    {
      id: 'm13-a',
      label: 'Script A',
      persona: 'Right method, wrong mode',
      work: ['tan A = 9/100', 'A = tan⁻¹(0·09)', 'A = 0·0898…   (calculator left in radian mode)'],
      keyLevelId: 'fullminus',
      keyNote:
        'The method is perfect; only the calculator mode is wrong, so the answer is 0·0898 (radians) instead of 5°. That is Full Credit −1 — but note the scope: the scheme applies the calculator-mode penalty ONCE across the whole paper. Get the mode right after this and you lose nothing further; a rounding error, by contrast, is charged every single time.',
      embodies: {
        behaviour: 'Correct method with the calculator in the wrong mode — Full Credit −1, applied once per paper.',
        cite: MS23('p.[45]'),
      },
    },
    {
      id: 'm13-b',
      label: 'Script B',
      persona: 'Mode right',
      work: ['tan A = 9/100', 'A = tan⁻¹(0·09) = 5·14°', 'A = 5°'],
      keyLevelId: 'full',
      keyNote: 'Correct ratio, calculator in degrees, rounded to the nearest degree. 10/10.',
    },
    {
      id: 'm13-c',
      label: 'Script C',
      persona: 'Ratio only',
      work: ['tan A = 9/100'],
      keyLevelId: 'low',
      keyNote: 'The relevant trig ratio is work of merit: low partial credit, 4/10.',
    },
  ],
  takeaway: {
    id: 'codex-m13',
    rule: 'Know which mistakes repeat — the calculator mode is charged once, rounding every time.',
    detail:
      'The scheme charges some penalties once per paper (calculator mode) and others on every occurrence (rounding). Set your calculator to degrees before you start so the once-off never triggers, and check the required accuracy on every answer, because that one keeps billing.',
    cite: MS23('p.[45]'),
  },
};

// ─────────────── M14 · An impossible answer scores zero ───────────────

const M14: ScaleSession = {
  mode: 'scale',
  id: 'maths-impossible-zero',
  subject: 'maths',
  level: 'ordinary',
  title: 'An impossible answer scores zero',
  cue: 'Find',
  question:
    'A player takes three independent shots, each with probability 0·7 of scoring. Find the probability that the player scores with all three shots.',
  questionNote:
    'Question adapted from the SEC 2023 OL scheme’s probability item (Q4(a)); the note “Zero Credit: Probability greater than 1” is the real one.',
  scale: {
    name: '10C (with a zero-credit gate)',
    levels: SCALE_10C,
    notes: [
      'Low partial credit: work of merit — e.g. 0·7 written, or three trials indicated.',
      'High partial credit: correct layout with full substitution, (0·7)(0·7)(0·7).',
      'Full credit: 0·343.',
      'Zero-credit gate: any answer giving a probability greater than 1 is awarded zero — no matter how much working is shown.',
    ],
    cite: MS23('p.[38] (Q4(a) “Zero Credit: Probability greater than 1”)'),
  },
  scripts: [
    {
      id: 'm14-a',
      label: 'Script A',
      persona: 'Adds instead of multiplying',
      work: ['P = 0·7 + 0·7 + 0·7', '= 2·1'],
      keyLevelId: 'none',
      keyNote:
        'There is working here — normally worth some merit — but the result, 2·1, is a probability greater than 1, which is impossible. The scheme’s note zeroes it: 0/10. A result that breaks a basic law of the topic forfeits the credit the working would otherwise have earned. The first sanity check on any probability is 0 ≤ P ≤ 1.',
      embodies: {
        behaviour: 'Reaches a probability above 1, which the scheme caps at zero regardless of working.',
        cite: MS23('p.[38]'),
      },
    },
    {
      id: 'm14-b',
      label: 'Script B',
      persona: 'Multiplies correctly',
      work: ['P = (0·7)(0·7)(0·7)', '= 0·343'],
      keyLevelId: 'full',
      keyNote: 'Independent events multiplied, correct layout and answer. 10/10.',
    },
    {
      id: 'm14-c',
      label: 'Script C',
      persona: 'Right layout, not evaluated',
      work: ['P = (0·7)(0·7)(0·7)'],
      keyLevelId: 'high',
      keyNote: 'Correct layout with full substitution, not yet evaluated. High partial credit, 6/10.',
    },
  ],
  takeaway: {
    id: 'codex-m14',
    rule: 'A result that breaks the rules of the topic scores zero — check it is possible.',
    detail:
      'A probability above 1, a negative length, a sine greater than 1: these are gated to zero however much work you show. Before you write a final answer, ask whether it can even exist — an impossible number is worse than an unfinished one.',
    cite: MS23('p.[38]'),
  },
};

// ─────────────── M15 · One slip, not two, in a step ───────────────

const M15: ScaleSession = {
  mode: 'scale',
  id: 'maths-step-block',
  subject: 'maths',
  level: 'higher',
  title: 'One slip, not two, in a step',
  cue: 'Calculate',
  question:
    'A loan is repaid by 300 equal monthly repayments. Using the amortisation formula, calculate the sum borrowed. (Marked as three steps: ① present values of the first repayments; ② fully correct substitution into the formula; ③ find the sum borrowed.)',
  questionNote:
    'Question adapted from the SEC 2024 HL scheme’s loan item (Q7(b)); the Scale 15D three-step ladder and the note “Step 3 is not given if there is more than one error in substitution in Step 2” are the real ones.',
  scale: {
    name: '15D (three steps)',
    levels: SCALE_15D_HL,
    notes: [
      'Low partial credit: work of merit — e.g. the monthly rate written as a decimal.',
      'Mid partial credit: one step correct.',
      'High partial credit: two steps correct.',
      'Full credit: all three steps — the sum borrowed found.',
      'Step gate: Step 3 is NOT credited if Step 2 contains more than one substitution error. One slip is tolerated and carried; a second slip closes the next step.',
    ],
    cite: MS24('p.[18] (Q7(b) three-step ladder and “Step 3 is not given if there is more than one error in substitution in Step 2”); scale table p.[4]'),
  },
  scripts: [
    {
      id: 'm15-a',
      label: 'Script A',
      persona: 'Two slips, then a finish',
      work: ['Step ①: present values written — correct', 'Step ②: substitution into the amortisation formula with TWO errors', 'Step ③: arithmetic carried to a final euro figure'],
      keyLevelId: 'mid',
      keyNote:
        'Step ① is right, but Step ② carries two substitution errors — and the scheme is explicit: “Step 3 is not given if there is more than one error in substitution in Step 2.” So even though a final figure is produced, Step ③ earns nothing: one step correct, mid partial credit, 6/15. A single error would have been tolerated and carried; the second one shut the door on the last step.',
      embodies: {
        behaviour: 'Makes more than one substitution error in a step, which blocks credit for the following step.',
        cite: MS24('p.[18]'),
      },
    },
    {
      id: 'm15-b',
      label: 'Script B',
      persona: 'One slip, carried',
      work: ['Step ①: present values — correct', 'Step ②: substitution into the formula with ONE slip, otherwise correct', 'Step ③: sum borrowed found consistently'],
      keyLevelId: 'high',
      keyNote:
        'One substitution slip in Step ②, finished consistently — a single error is tolerated, so Steps ① and ② both count: two steps correct, high partial credit, 8/15. The same script with a second slip in Step ② would have dropped to Script A’s mid.',
    },
    {
      id: 'm15-c',
      label: 'Script C',
      persona: 'All three steps',
      work: ['Step ①: present values — correct', 'Step ②: fully correct substitution', 'Step ③: sum borrowed = €334 563'],
      keyLevelId: 'full',
      keyNote: 'Three clean steps to the sum borrowed. 15/15.',
    },
    {
      id: 'm15-d',
      label: 'Script D',
      persona: 'A first decimal',
      work: ['Monthly rate = 0·279% = 0·00279'],
      keyLevelId: 'low',
      keyNote: 'Writing the monthly rate as a decimal is work of merit: low partial credit, 4/15.',
    },
  ],
  takeaway: {
    id: 'codex-m15',
    rule: 'One slip in a step is survivable — a second can cost you the next step too.',
    detail:
      'The scheme carries you through a single substitution error, but more than one error in a step can block credit for the step that depends on it. On long substitutions, slow down and check each value once: the second slip does not just cost its own mark, it can forfeit the finish.',
    cite: MS24('p.[18]'),
  },
};

// ─────────────── M16 · Foundation — right figures, wrong person ───────────────

const M16: ScaleSession = {
  mode: 'scale',
  id: 'maths-fl-wrong-person',
  subject: 'maths',
  level: 'foundation',
  title: 'Right figures, wrong person',
  cue: 'Find',
  question:
    'Three friends — Tom, Jack and Michael — share the cost of a meal, spending €200 in total. Jack spent €3 more than Tom, and Michael spent €8 more than Tom. How much did each person spend? (10 marks.)',
  questionNote:
    'Question authored for this exercise; the 10C ladder (0, 4, 6, 10) and the Full Credit −1 “correct figures assigned to the incorrect person” note are the real 2025 Foundation scheme rules for the shared-spending question Q2(c).',
  scale: {
    name: '10C · Full credit −1',
    levels: SCALE_F10C_STAR,
    notes: [
      'Model: Jack and Michael together spent €11 more than Tom, so €200 − €11 = €189 is shared equally: €189 ÷ 3 = €63. Then Tom €63, Jack €66, Michael €71.',
      'Low partial credit: work of merit — indicates the €11, or adds the 3 or the 8.',
      'High partial credit: finds €189, or finds €63.',
      'Full Credit −1: the correct figures, but assigned to the wrong people.',
      'Full credit: €63, €66 and €71 assigned to Tom, Jack and Michael respectively.',
    ],
    cite: MSFL('p.[8] (Q2(c) 10C ladder and the “correct figures, incorrect person” Full Credit −1)'),
  },
  scripts: [
    {
      id: 'm16-a',
      label: 'Script A',
      persona: 'The €11 and no more',
      work: ['Jack is €3 more, Michael is €8 more.', '3 + 8 = 11'],
      keyLevelId: 'low',
      keyNote:
        'Spotting that Jack and Michael together account for €11 above Tom is the work-of-merit step — low partial credit, 4/10. It is the right first move, but nothing is shared out yet, so it cannot climb higher.',
    },
    {
      id: 'm16-b',
      label: 'Script B',
      persona: 'Shares it out, stops at €63',
      work: ['200 − 11 = 189', '189 ÷ 3 = 63'],
      keyLevelId: 'high',
      keyNote:
        'Reaching €63 — the equal amount before the extras are added back — is the “finds €63” step, high partial credit, 6/10. The three individual amounts are never written, so the last four marks stay on the table.',
    },
    {
      id: 'm16-border',
      label: 'Script C',
      persona: 'Right numbers, wrong labels',
      work: ['200 − 11 = 189', '189 ÷ 3 = 63', 'Tom = €71, Jack = €66, Michael = €63'],
      keyLevelId: 'fullminus',
      keyNote:
        '9 of 10 — Full Credit −1, and the hardest call on this question. Every figure is correct — €63, €66, €71 — and the arithmetic is complete; only the names are swapped, with €71 put on Tom instead of Michael. The scheme treats “correct figures assigned to the incorrect person” as a one-mark slip, not a wrong answer, so it sits one rung below full, not down at high partial. Don’t mark it full (the labels are wrong) and don’t drop it to 6 (the maths is entirely right).',
    },
    {
      id: 'm16-d',
      label: 'Script D',
      persona: 'All the way home',
      work: ['200 − 11 = 189', '189 ÷ 3 = 63', 'Tom = €63', 'Jack = 63 + 3 = €66', 'Michael = 63 + 8 = €71'],
      keyLevelId: 'full',
      keyNote:
        'Full marks, 10/10. The €63 base is found and the €3 and €8 are added back to the right people, so every amount is correct and correctly labelled.',
    },
  ],
  takeaway: {
    id: 'codex-m16',
    rule: 'Right figures on the wrong name is Full Credit −1, not a wrong answer.',
    detail:
      'At Foundation Level, when the arithmetic is complete and every value is correct but the values are matched to the wrong people, the scheme awards Full Credit −1 (9 on a 10-mark item) — a one-mark labelling slip, not a drop to high partial. Label the last line to the right person and protect that mark.',
    cite: MSFL('p.[8]'),
  },
};

// ─────────────── M17 · Foundation — one part right on a two-part item ───────────────

const M17: ScaleSession = {
  mode: 'scale',
  id: 'maths-fl-counting',
  subject: 'maths',
  level: 'foundation',
  title: 'One part right on a two-part item',
  cue: 'Find',
  question:
    'A café menu has 2 starters, 4 main courses and 3 desserts. (ii) How many different meals of one starter, one main and one dessert are possible? (iii) On the set-lunch deal the starter is fixed (1 choice), there are 4 mains and 2 desserts — how many set-lunch meals are possible? (10 marks.)',
  questionNote:
    'Question authored for this exercise; the two-part 10D ladder (0, 4, 5, 7, 10) and its “one part correct = mid, one part correct + work of merit in the other = high” rule are the real 2025 Foundation scheme rules for the counting question Q3(a).',
  scale: {
    name: '10D (two-part)',
    levels: SCALE_F10D,
    notes: [
      'Model: (ii) 2 × 4 × 3 = 24.  (iii) 1 × 4 × 2 = 8.',
      'Low partial credit: work of merit in either part — some relevant multiplication.',
      'Mid partial credit: one part fully correct (or work of merit in both parts).',
      'High partial credit: one part fully correct AND work of merit in the other part.',
      'Full credit: both parts correct — 24 and 8.',
    ],
    cite: MSFL('p.[9] (Q3(a) two-part 10D ladder: 0, 4, 5, 7, 10)'),
  },
  scripts: [
    {
      id: 'm17-a',
      label: 'Script A',
      persona: 'Multiplies something',
      work: ['(ii) 2 × 4 = 8', '(iii) 4 + 2 = 6'],
      keyLevelId: 'low',
      keyNote:
        'A relevant multiplication is started in (ii) but neither part is finished correctly — the dessert factor is dropped in (ii), and (iii) is added rather than multiplied. Work of merit only: low partial credit, 4/10.',
    },
    {
      id: 'm17-border',
      label: 'Script B',
      persona: 'One part nailed, one left blank',
      work: ['(ii) 2 × 4 × 3 = 24', '(iii) —'],
      keyLevelId: 'mid',
      keyNote:
        '5 of 10 — mid partial credit, and the classic two-part judgement call. Part (ii) is fully correct at 24, but part (iii) is blank, so there is no work of merit in the second part. “One part correct” is the mid rung; it only lifts to high (7) if the other part also shows some relevant working. One complete part and one blank is exactly mid — don’t round it up for the strong (ii), and don’t drop it for the empty (iii).',
    },
    {
      id: 'm17-c',
      label: 'Script C',
      persona: 'One right, one attempted',
      work: ['(ii) 2 × 4 × 3 = 24', '(iii) 1 × 4 = 4'],
      keyLevelId: 'high',
      keyNote:
        'Part (ii) is fully correct and part (iii) shows a relevant multiplication (the fixed starter times the mains) even though the dessert factor is missed. One part correct plus work of merit in the other is the high rung: 7/10.',
    },
    {
      id: 'm17-d',
      label: 'Script D',
      persona: 'Both parts home',
      work: ['(ii) 2 × 4 × 3 = 24', '(iii) 1 × 4 × 2 = 8'],
      keyLevelId: 'full',
      keyNote:
        'Both parts correct — 24 and 8 — full credit, 10/10.',
    },
  ],
  takeaway: {
    id: 'codex-m17',
    rule: 'On a two-part item, one complete part is mid; add working in the other to reach high.',
    detail:
      'Foundation two-part questions use a D-scale (0, 4, 5, 7, 10). One part fully correct is mid partial credit; to climb to high you also need work of merit in the second part. A blank second part caps you at mid however strong the first — always put down a relevant line for the other part.',
    cite: MSFL('p.[9]'),
  },
};

export const MATHS_CHAIR: ChairSubject = {
  id: 'maths',
  label: 'Mathematics',
  tagline: 'Scales, steps and stars — how maths scripts are really graded.',
  offeredLevels: ['higher', 'ordinary', 'foundation'],
  sessions: [M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11, M12, M13, M14, M15, M16, M17],
  sources: [
    { label: 'SEC LC Mathematics OL marking scheme 2023, Paper 2 portion (examiner-reports/maths/2023-marking-scheme-ol-p2)' },
    { label: 'SEC LC Mathematics HL marking scheme 2024, Papers 1 & 2 (examiner-reports/maths/2024-hl-marking-scheme)' },
    { label: 'SEC LC Mathematics Foundation marking scheme 2025 (examiner-reports/maths/2025-foundation-marking-scheme)' },
    { label: 'Chief Examiner’s Report, Mathematics 2015 (examiner-reports/maths/2015-chief-examiner)' },
  ],
  coverageNote:
    'Maths is marked on the same scale system — A–D scales, the partial-credit ladders, work-of-merit and Full Credit −1 — at Higher, Ordinary and Foundation level, so these sessions teach the system that applies at every level. Five shared-convention sessions (the ladder, counting steps, saying the conclusion, the one-mark star and own-work carry-forward) are pitched around Ordinary Level; the Higher Level sessions (the oversimplify ceiling, the named-method gate, the MPC ceiling, the ± rule, the impostor-root rule, the part-counted graph and the two-slip step gate) are drawn from the 2024 HL scheme; two Ordinary Level sessions (penalty scope and the impossible-answer gate) from the 2023 OL scheme; and three Foundation Level sessions (right answer / wrong detail, right figures / wrong person, and the two-part D-scale) from the 2025 Foundation scheme.',
};
