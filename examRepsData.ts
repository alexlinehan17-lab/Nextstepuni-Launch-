/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Exam Reps — the Rep Card bank.
 *
 * Cards are AGENT-FORGED from real State Examinations Commission sources
 * (examiner-reports/ + examinations.ie), faithfully reproducing the question
 * and rebuilding the real marking scheme as checkable "mark ribbons". Every
 * lesson cites its source. This file is seeded with one pilot-verified card;
 * the forge pipeline appends more (Business / Maths / more Geography).
 *
 * ⚠️ Content is cycle-dated reference material — re-verify against the current
 * marking schemes/reports each year. Chief Examiner report recency varies by
 * subject; lessons cite the year so the vintage is honest.
 */
import { type RepCard } from './types/examReps';

export const REP_CARDS: RepCard[] = [
  {
    id: 'geo-hl-2023-q6b',
    subject: 'geography',
    subjectLabel: 'Geography',
    level: 'higher',
    year: 2023,
    questionRef: '2023 HL · Q6B',
    questionText:
      'Account for the development of secondary economic activity in a European region (not in Ireland) that you have studied, with reference to any two of the following factors:\n• Labour\n• Transport\n• Raw materials\n• Markets.',
    marks: 30,
    minutes: 20,
    answerKind: 'written',
    taskType: 'regional-economic-account',
    commandWord: {
      word: 'Account for',
      reminder:
        '“Account for” means EXPLAIN the causes — every point must link the factor to WHY the activity developed there, not just describe it.',
    },
    ribbons: [
      { id: 'region-gate', label: 'Named a valid European region (not in Ireland)', marks: 0, kind: 'gate' },
      { id: 'factor1', label: 'Factor 1 examined — each point linked to WHY the activity developed (up to 8 points)', marks: 16, kind: 'srp' },
      { id: 'factor2', label: 'Factor 2 examined — each point linked to development (up to 7 points)', marks: 14, kind: 'srp' },
    ],
    lesson: {
      text:
        'You can write a flawless description of each factor and still be capped at just 4 marks per factor — the scheme rewards “merely describing the factor” at a maximum of 2 points. The marks live in the LINK: “Because [factor]…, [the activity] developed/located here…”. And name your European (non-Irish) region up front — an examination with no named or clearly-inferred region scores zero.',
      source: 'Chief Examiner 2012, p.27 · Marking scheme 2023, p.22',
    },
  },

  // ── Forged from the real SEC 2025 Business HL marking scheme; adversarially
  //    verified (marks, ribbons, question text, citations all confirmed). ──
  {
    id: 'business-hl-2025-q8c-breakeven-chart',
    subject: 'business',
    subjectLabel: 'Business',
    level: 'higher',
    year: 2025,
    questionRef: '2025 HL · Q8(C)',
    questionText:
      'Illustrate the following by means of a breakeven chart:\n(i) Breakeven point\n(ii) Margin of safety at the forecast output\n(iii) Profit at forecast output.',
    marks: 25,
    minutes: 11,
    answerKind: 'steps',
    taskType: 'breakeven-chart',
    commandWord: {
      word: 'Illustrate',
      reminder:
        '“Illustrate by means of a chart” means you must DRAW the chart — calculations alone, even perfect ones, cap at 12 of 25 marks. The chart’s lines, labels and title carry the other 13.',
    },
    ribbons: [
      { id: 'chart-gate', label: 'Chart actually drawn (not calculations alone) — required to access the full 25-mark grid', marks: 0, kind: 'gate' },
      { id: 'title-axes', label: 'Title the chart (2m) + label both axes (1m + 1m)', marks: 4, kind: 'method' },
      { id: 'three-lines', label: 'Plot the three lines: Fixed Costs (3m), Total Costs (3m), Total Revenue (3m)', marks: 9, kind: 'method' },
      { id: 'bep', label: 'Mark the Breakeven Point — 120,000 units / €1,200,000', marks: 4, kind: 'srp' },
      { id: 'profit', label: 'Mark Profit at forecast output — €400,000', marks: 4, kind: 'srp' },
      { id: 'mos', label: 'Mark the Margin of Safety — 80,000 units', marks: 4, kind: 'srp' },
    ],
    lesson: {
      text:
        'Doing the calculations only — even all three perfectly — caps you at 12 of 25 marks; the drawn chart carries the other 13. And the chart marking is granular: no title costs 2 marks and unlabelled axes cost 2 — the exact omissions examiners flag year after year.',
      source: 'Marking scheme 2025, p.11 & p.51 · Chief Examiner 2015, p.18',
    },
  },
  {
    id: 'business-hl-2025-abq-b-i-eval-control',
    subject: 'business',
    subjectLabel: 'Business',
    level: 'higher',
    year: 2025,
    questionRef: '2025 HL · ABQ (B)(i)',
    questionText:
      'Evaluate the effectiveness of the types of management control in place at Inis Bia. Refer to the text in your answer.',
    marks: 28,
    minutes: 13,
    answerKind: 'steps',
    taskType: 'abq-evaluate',
    commandWord: {
      word: 'Evaluate',
      reminder:
        '“Evaluate” means for each control you must JUDGE whether it was effective or not and justify it. Naming + explaining + a case quote earns only 4 of the 7 marks per point; the 3-mark judgement is the heaviest part and where most stop short.',
    },
    ribbons: [
      { id: 'name', label: 'Name a valid type of management control (Quality / Stock / Financial / Credit) — 1m × 4 points', marks: 4, kind: 'name' },
      { id: 'explain', label: 'Explain the theory of that control — 2m × 4 points', marks: 8, kind: 'explain' },
      { id: 'link', label: 'Link a relevant quote from the Inis Bia text for each — 1m × 4 points', marks: 4, kind: 'link' },
      { id: 'evaluation', label: 'Evaluate the effectiveness of each (judgement + justification) — 3m × 4 points', marks: 12, kind: 'evaluation' },
    ],
    lesson: {
      text:
        'Evaluation is the single most heavily-weighted component here (3 of 7 marks per point) yet the Chief Examiner calls it the weakest: “Some evaluations continue to be very superficial and some candidates do not evaluate at all.” Naming, explaining and quoting earns only 4 of 7 per point — you forfeit 12 of the 28 marks unless you finish each point with an effectiveness judgement.',
      source: 'Chief Examiner 2015, p.16 · Marking scheme 2025, p.6 & p.20',
    },
  },
];
