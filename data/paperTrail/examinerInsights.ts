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
 * Gated by report coverage — a subject gets a set only once its Chief
 * Examiner's report is in-repo and the set is verified against it (currently
 * Business, Mathematics, English). Grows as more reports are verified.
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
    subjectId: 'english',
    subjectLabel: 'English',
    source: "SEC Chief Examiner's Report 2013 (Higher & Ordinary Level)",
    insights: [
      {
        pitfall: 'Comparative answers built from a pre-learned formula — the report found "a significant minority of candidates were hampered by a rigid and formulaic approach", and the Comparative was the weakest-scoring section at both levels.',
        fix: 'Engage with the terms of the actual question in every paragraph. The quality of the evidence you cite was "a significant discriminator used by examiners".',
        cite: "Chief Examiner's Report 2013, pp.8, 18–20",
      },
      {
        pitfall: 'Skipping the Unseen Poem — "a number of candidates did not answer on this compulsory section", losing up to twenty marks outright, and it was the lowest-scoring element on Paper 2.',
        fix: 'Always attempt it. Examiners are told there is no single "correct" reading — a well-argued personal response to the poem\'s language and imagery is exactly what is rewarded.',
        cite: "Chief Examiner's Report 2013, pp.7–9",
      },
      {
        pitfall: 'Careless quotation in Single Text answers — "the careless use of quotation, observed in a significant number of responses, served to undermine answers".',
        fix: 'Short, apt, accurate quotes woven into your point beat long misremembered ones. Check each quote actually supports the sentence it sits in.',
        cite: "Chief Examiner's Report 2013, p.8",
      },
      {
        pitfall: 'Reproducing prepared "banks of knowledge" — material delivered regardless of what was asked. Knowledge alone did not score; unmanaged, it read as not answering the question.',
        fix: 'Shape everything to the specific question asked. Under-achievement was traced to "a loss of focus in terms of the requirements of the task".',
        cite: "Chief Examiner's Report 2013, pp.11, 18, 20",
      },
      {
        pitfall: 'Compositions that are "extremely brief and lacked development" — it is difficult to reach the top marks "if the answer is brief in the extreme".',
        fix: 'Sustain and develop the piece, and honour your chosen genre: a short story needs narrative shape, characterisation, setting and atmosphere, not just good sentences.',
        cite: "Chief Examiner's Report 2013, pp.15–16",
      },
      {
        pitfall: 'Treating the question with too much reverence — assuming you must agree with its premise, which "can affect candidates\' ability to demonstrate skills in critical literacy".',
        fix: 'You may challenge or disagree with part or all of a question\'s premise — the marking schemes explicitly cater for disputation. A defended independent view scores.',
        cite: "Chief Examiner's Report 2013, p.17",
      },
    ],
  },
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
