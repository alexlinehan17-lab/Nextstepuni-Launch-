/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Subject strategy preamble for Business (Higher Level).
 */

import { type SubjectStrategy } from '../../types/examStrategiser';

export const businessStrategy: SubjectStrategy = {
  subject: 'business',
  headline: 'How Business Higher Level is marked',
  intro:
    "Business HL has a unique scoring shape: most marks come from short-response recall + a long case-based question (the ABQ) where you have to combine business theory with direct quotes from the case. Misreading the question cue or skipping a sub-part is where most marks leak.",
  rules: [
    {
      id: 'abq-link-rule',
      title: 'The ABQ link-to-text rule — the killer',
      body: 'Section 2 (the Applied Business Question, 80 marks / 20% of the paper) is compulsory and uniquely punishing. Two failure modes both score 0: (1) writing business theory with no reference to the case, (2) treating it as a comprehension piece and rewriting chunks of the case material. The correct shape is theory + a direct relevant quote/phrase/sentence from the case as the LINK. Per the 2015 Chief Examiner Report, this approach has "serious impact" on Business HL grades.',
      pinned: true,
    },
    {
      id: 'question-cues',
      title: 'Question cues drive mark allocation',
      body: 'Cues are not interchangeable. "List / name / state" reward brevity — give the items, no extras. "Outline / explain / discuss / describe / evaluate" require developed points (typically 2-3 sentences each). "Illustrate" requires an example. "Define" rewards precise terminology. The 2015 Chief Examiner Report notes "marks continue to be lost when very brief or one-word answers are given in response to questions requiring developed points of information."',
    },
    {
      id: 'definitions-vs-answering',
      title: 'Definitions ≠ answering the question',
      body: 'Recurring HL pattern: students give a strong definition of a term and then provide an inadequate answer to the actual question that uses it. The 2015 Chief Examiner Report calls this out specifically: "the requirement to build on the definitions to answer the actual questions set at the Higher level was not always evident." Define quickly, then answer.',
    },
    {
      id: 'diagrams',
      title: 'Diagrams need labels, titles, scale, and accurate plots',
      body: 'Bar charts (Q4 / Q6 type), product life cycle (Q5 type), breakeven charts (Q8 type) — all enforce the same rules. Marks are lost for missing axis labels, missing chart title, incorrect scale, or imprecisely plotted points. Use graph paper if it\'s available — the 2015 report observed students who did "in general performed better".',
    },
    {
      id: 'distinct-points',
      title: 'Discussion questions reward distinct points',
      body: 'When the question asks for two or three points (especially "discuss" / "explain", or any 20-mark sub-part), each point must be genuinely distinct. Repeating one core point in different words — the classic "reduce, reuse, and recycle" trap from 2015 Q2(C) — caps you below the band. Plan distinct angles before writing.',
    },
  ],
  marksToMinutes: {
    summary: 'HL paper: 400 marks across 180 minutes — roughly 0.45 minutes per mark.',
    examples: [
      '10-mark Section 1 question → ~4-5 mins each',
      '20-mark Section 3 sub-part → ~9 mins',
      '60-mark Section 3 question (3 × 20m) → ~27 mins',
      '80-mark ABQ (Section 2) → ~36 mins',
    ],
  },
};
