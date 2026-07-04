/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — Chief Examiner insight cards (Tier 2, feature 6). Each insight
 * is a real, citable pattern the SEC Chief Examiner's Report flags, paraphrased
 * to student-facing "here's where marks are lost / here's the fix" with the
 * source page. Verbatim quotes are kept short per the content rules; the full
 * traceable source lives in /examiner-reports/<subject>/.
 *
 * Gated by report coverage — currently Business + Mathematics (the two subjects
 * whose Chief Examiner reports are in-repo). Grows as more reports land.
 */

export interface ExaminerInsight {
  /** The common mistake, in the student's terms. */
  pitfall: string;
  /** The specific fix / what higher answers did instead. */
  fix: string;
  /** Citable source, e.g. "Chief Examiner's Report 2015, p.15". */
  cite: string;
}

export interface ExaminerInsightSet {
  subjectId: string;
  subjectLabel: string;
  /** One-line provenance shown under the card title. */
  source: string;
  insights: ExaminerInsight[];
}

const SETS: ExaminerInsightSet[] = [
  {
    subjectId: 'business',
    subjectLabel: 'Business',
    source: "SEC Chief Examiner's Report 2015 (Higher Level)",
    insights: [
      {
        pitfall: 'In the ABQ, writing business theory with no reference to the case — or rewriting chunks of the case with no theory. Either scores little or nothing.',
        fix: 'Every ABQ point = the theory PLUS a direct relevant quote from the case as the link. "No link awarded without relevant theory."',
        cite: "Chief Examiner's Report 2015, p.15",
      },
      {
        pitfall: 'Defining a term well but being unable to apply it — span of control, exchange rate, net profit %. Recall did not match application.',
        fix: 'Always carry the concept into the business context the question asks for. The application marks are separate from the definition marks.',
        cite: "Chief Examiner's Report 2015, p.14",
      },
      {
        pitfall: 'Missing the cue: writing paragraphs when the cue is "List", or defining a term without the example an "Illustrate" cue demands.',
        fix: 'Match the cue exactly — "List" = name only (no paragraphs); "Illustrate" = include an example; "Evaluate" = judgement + justification.',
        cite: "Chief Examiner's Report 2015, p.17",
      },
      {
        pitfall: 'Evaluation that is superficial or absent — the higher-order judgement skill is consistently the weakest.',
        fix: 'An evaluation states a reasoned opinion and justifies it. Description of the point is not evaluation and caps the marks.',
        cite: "Chief Examiner's Report 2015, p.17",
      },
      {
        pitfall: 'Omitting units of measurement (%, €) in calculations — "necessary to give meaning to the answers".',
        fix: 'Attach the unit to every numerical answer. Units are mark-bearing.',
        cite: "Chief Examiner's Report 2015, p.14",
      },
      {
        pitfall: 'Charts drawn without a title, axis labels, or accurate plotting (bar chart, product life cycle).',
        fix: 'Title the chart, label both axes, plot accurately — and use graph paper. Candidates who did performed better.',
        cite: "Chief Examiner's Report 2015, p.18",
      },
    ],
  },
  {
    subjectId: 'mathematics',
    subjectLabel: 'Mathematics',
    source: "SEC Chief Examiner's Report 2015 (Higher & Ordinary Level)",
    insights: [
      {
        pitfall: 'After squaring both sides of an equation, assuming both roots are valid — squaring can introduce extraneous roots.',
        fix: 'Test each solution back in the ORIGINAL equation and discard any that do not satisfy it.',
        cite: "Chief Examiner's Report 2015, p.21 (HL P1 Q5a)",
      },
      {
        pitfall: 'To find a turning point, solving f″(x) = 0 instead of f′(x) = 0 — a misread of what the derivative gives you.',
        fix: 'Solve f′(x) = 0 for the x-coordinates of the turning points. That is the relationship being tested.',
        cite: "Chief Examiner's Report 2015, p.21 (HL P1 Q5c)",
      },
      {
        pitfall: 'Reflexively differentiating because a question mentions "speed" — linking speed to calculus without reading the context.',
        fix: 'Read what the question actually asks. Not every rate/speed question is a differentiation question.',
        cite: "Chief Examiner's Report 2015, p.24 (HL P1 Q9c)",
      },
      {
        pitfall: 'Latching onto keywords like "angle between lines" and grabbing a formula, without thinking about the actual question.',
        fix: 'Sketch a diagram first. It often reveals a simpler approach than the formula the keyword suggests.',
        cite: "Chief Examiner's Report 2015, p.25 (HL P2 Q3c)",
      },
      {
        pitfall: 'Misreading subscript notation — treating p₍ₙ₊₁₎ as pₙ + 1, which corrupts the whole solution.',
        fix: 'Read notation precisely; a subscript indexes a term, it is not added to it.',
        cite: "Chief Examiner's Report 2015, p.26 (HL P2 Q8)",
      },
      {
        pitfall: 'Doing the calculation but never writing the conclusion, and giving up when the numbers get messy.',
        fix: 'State the conclusion the question asks for, with units. Top candidates persevered "even when the numerical values were not user-friendly".',
        cite: "Chief Examiner's Report 2015, p.20, p.22",
      },
    ],
  },
];

const byId = new Map(SETS.map(s => [s.subjectId, s]));

export const examinerInsightsFor = (subjectId: string): ExaminerInsightSet | null =>
  byId.get(subjectId) ?? null;
