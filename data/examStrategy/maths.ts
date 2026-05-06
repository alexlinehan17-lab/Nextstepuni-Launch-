/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Subject strategy preamble for Maths (Ordinary / Higher Level).
 */

import { type SubjectStrategy } from '../../types/examStrategiser';

export const mathsStrategy: SubjectStrategy = {
  subject: 'maths',
  headline: 'How Maths is marked',
  intro:
    'Maths is marked on a partial-credit ladder: Low / Mid / High Partial Credit / Full Credit. Working is most of the marks. Stating the right answer without working typically caps you at Low Partial Credit — even when the answer is correct.',
  rules: [
    {
      id: 'ladder',
      title: 'The Partial Credit ladder',
      body: 'Each part of each question has its own ladder. For a 5-mark sub-part: Blank/wrong direction = 0. Some valid working but no answer = Low Partial Credit (LPC). Substantial working with minor errors = Mid/High Partial Credit (MPC/HPC). Correct method + correct answer = Full Credit. Even when you can\'t finish: WRITE WHAT YOU HAVE. LPC is real points.',
      pinned: true,
    },
    {
      id: 'show-vs-find',
      title: '"Show that" vs "Find" — different tasks',
      body: '"Show that x = 3" — the answer is given. Your job is to DEMONSTRATE the working that produces 3. Just stating the answer scores 0 — the marks are for the derivation. "Find x" — you produce the answer. Both need working, but "Show that" makes the working the entire point.',
    },
    {
      id: 'apply-star',
      title: '"Apply a *" — the most common penalty',
      body: 'The marking scheme\'s favourite penalty: full credit minus 1, applied for missing one specific step (missing units, missing rounding to specified d.p., missing justification, wrong rounding direction for a "max" with "needs at least" floor, etc.). Easy to lose, easy to keep. Read the rounding/units instruction TWICE before submitting.',
    },
    {
      id: 'method-specified',
      title: 'Method specified = method enforced',
      body: '"Use the cosine rule" forbids Pythagoras and sine rule. "Use calculations to support your answer" forbids ticking the box. When the question names the method, alternatives don\'t earn credit even if they reach the right answer. The method is part of what\'s being assessed.',
    },
    {
      id: 'working-is-marks',
      title: 'Working IS the marks',
      body: 'In Section B contextual questions, the working is graded line by line. Showing each step (with the rule used — "by Vieta\'s formulas", "since lengths scale by k, areas scale by k²") earns more than a flashy single line that gets the right answer. Justify each step.',
    },
    {
      id: 'natural-numbers',
      title: 'Domain matters — n ∈ ℕ forces floor for "below" thresholds',
      body: 'When the answer must be a natural number AND the constraint is "needs at least X", "below Y", or "maximum that…", round in the direction that satisfies the inequality. n = 24.06 with "must fall below €2" rounds UP to 25 — at n = 24 the value still equals 2 and hasn\'t fallen below. Marking scheme applies a star for getting the rounding direction wrong.',
    },
  ],
  marksToMinutes: {
    summary: 'OL: 300 marks across 150 minutes — exactly 0.5 minutes per mark.',
    examples: [
      '5-mark sub-part → ~2.5 mins',
      '20-mark Section A question → ~10 mins',
      '30-mark question → ~15 mins',
      '50-mark Section B context question → ~25 mins',
    ],
  },
};
