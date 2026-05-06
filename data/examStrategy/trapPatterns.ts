/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Cross-subject trap pattern library.
 * Each pattern names a recurring marking-scheme trap that spans subjects
 * and years. Examples link back to real questions in the bank so students
 * can see the same trap shape applied in different domains.
 */

import { type TrapPattern } from '../../types/examStrategiser';

export const TRAP_PATTERNS: TrapPattern[] = [
  {
    id: 'geographic-constraint',
    name: 'Geographic constraint',
    description:
      'Some questions tie you to a specific region (Ireland-only) or explicitly forbid one (NOT in Europe / NOT Irish). Get the constraint wrong and the entire answer scores 0 regardless of quality. The single most catastrophic Geography trap.',
    diagnostic:
      'Look for phrases like "the Irish landscape", "Continental/Sub-Continental region (not in Europe)", "an Irish region you have studied". Pick your region BEFORE you start writing.',
    subjects: ['geography'],
    examples: [
      { questionId: 'geo-2025-hl-q1c', snippet: '"how isostasy has shaped the Irish landscape" — Ireland-tied. Foreign examples score 0.' },
      { questionId: 'geo-2025-hl-q4b', snippet: '"a Continental/Sub-Continental region (not in Europe)" — answers about France or Ireland score 0.' },
    ],
  },
  {
    id: 'genre-mismatch',
    name: 'Genre mismatch',
    description:
      'Most punitive English trap on long compositions. Discursive ≠ argumentative. Speech ≠ essay. Proposal ≠ letter. Genre is part of Purpose, and P caps Coherence and Language — so genre confusion ceilings the entire answer.',
    diagnostic:
      'Read the prescribed genre TWICE before writing a word. "Discursive" wants weighing of multiple views; "for or against" wants one side defended; "speech" wants oral register; "proposal" wants formal civic register with named audience.',
    subjects: ['english'],
    examples: [
      { questionId: 'english-2024-p1-composing-5', snippet: '"Write a discursive essay" — argumentative essays in this slot cap Purpose, ceiling C and L.' },
      { questionId: 'english-2025-p1-composing-2', snippet: '"Write a speech for or against" — must pick ONE side; hedging penalised.' },
      { questionId: 'english-2024-p1-text2-qb', snippet: '"Write a proposal to your local Tidy Towns Committee" — proposal not letter, formal not casual.' },
    ],
  },
  {
    id: 'missing-sub-task',
    name: 'Missing sub-task',
    description:
      'Multi-part questions list 2-3 explicit sub-tasks. Skipping one — almost always the third — caps Purpose, which under P-caps-C-L caps everything. Most common silent killer in 50-mark Question B compositions.',
    diagnostic:
      'Count the sub-tasks before you start. Look for bulleted lists or "outline X, propose Y, suggest Z" structures. Allocate roughly equal space to each.',
    subjects: ['english'],
    examples: [
      { questionId: 'english-2024-p1-text2-qb', snippet: 'THREE sub-tasks: outline concerns, propose project, suggest community engagement. Most students skip the third.' },
      { questionId: 'english-2025-p1-text2-qb', snippet: 'THREE sub-tasks: outline history, challenge criticisms, encourage return with events.' },
    ],
  },
  {
    id: 'rounding-direction',
    name: 'Quantification — rounding direction matters',
    description:
      'When the answer must be a natural number AND the constraint is "needs at least X", "below Y", or "maximum that…", round in the direction that satisfies the inequality. Marking scheme applies a star (Full Credit −1) for getting the rounding direction wrong even when the underlying calculation is correct.',
    diagnostic:
      'Look for "at least", "below", "maximum" combined with a domain restriction (n ∈ ℕ, integer participants, etc.). 11.6 participants who each "need at least 60cm" floors to 11, not 12. n = 24.06 with "must fall below €2" rounds UP to 25.',
    subjects: ['maths'],
    examples: [
      { questionId: 'maths-2025-ord-p1-q7', snippet: 'Solving 9·22 − 0·3n < 2 gives n = 24·06… With "must fall BELOW €2" and n ∈ ℕ → 25, not 24.' },
      { questionId: 'maths-2025-ord-p2-q9', snippet: '698·13 / 60 = 11·6 participants. With "needs at least 60cm" → floor to 11, not 12.' },
    ],
  },
  {
    id: 'inverted-operation',
    name: 'Inverted operation (× vs ÷)',
    description:
      'Percentage error and ratio questions invite the wrong operation when students rush. Pattern: "error / true value × 100 = percentage error" — to find true value, you DIVIDE error by the percentage, not multiply. Easy to flip.',
    diagnostic:
      'Write the relationship out fully before substituting. "error / true value = percentage" → true value = error / percentage. Always check the result is in the right ballpark.',
    subjects: ['maths'],
    examples: [
      { questionId: 'maths-2025-ord-p1-q7', snippet: '"error €1·50 = 16·3% of true value" → true value = 1·50 ÷ 0·163 ≈ €9·20. Multiplying gives €0·24, which makes no sense as a share price.' },
    ],
  },
  {
    id: 'wrong-formula-choice',
    name: 'Wrong formula / wrong tool',
    description:
      'Substituting into the wrong function (f(x) instead of f′(x) for a tangent slope), scaling by k instead of k² for an area, using sine rule when ½ ab sin C is intended. Marking scheme is explicit: "zero credit for substituting 2 into f" — wrong tool, wrong answer, no partial credit.',
    diagnostic:
      'Match the technique to what\'s being asked. Tangent slope → derivative. Areas under enlargement → k², not k. Two sides + included angle for AREA → ½ ab sin C; for the OPPOSITE SIDE → cosine rule.',
    subjects: ['maths'],
    examples: [
      { questionId: 'maths-2025-ord-p1-q4', snippet: 'Slope of tangent at (2, −4) = f′(2), NOT f(2). Marking scheme: zero credit for substituting into f.' },
      { questionId: 'maths-2025-ord-p2-q9', snippet: 'Areas scale by k², not k. 724 / 1·25 (one factor of k) = 579·2 — wrong. Use 1·25² = 1·5625.' },
    ],
  },
  {
    id: 'show-that',
    name: '"Show that" — demonstrate, don\'t state',
    description:
      'When the answer is given in the question ("Show that x = 1·25", "Show that ME = 3·5%"), your job is to DEMONSTRATE the working that produces it. Just stating the given answer scores 0. The working IS the marks.',
    diagnostic:
      'If the question contains "Show that…" followed by a specific value, do not write that value as your answer — write the calculation that produces it.',
    subjects: ['maths'],
    examples: [
      { questionId: 'maths-2025-ord-p2-q8', snippet: '"Show that the margin of error is 3·5%" — must derive ME = 1/√815 = 0·035... = 3·5%, not just state 3·5%.' },
      { questionId: 'maths-2025-ord-p2-q9', snippet: '"Show that k = 1·25" — must compute k = 45/36 = 1·25.' },
    ],
  },
  {
    id: 'method-specified',
    name: 'Method specified — alternatives don\'t count',
    description:
      'When the question names a method ("Use the cosine rule", "Use calculations to support your answer"), reaching the right answer by a different method earns no credit. The method is part of what\'s being assessed.',
    diagnostic:
      'Watch for "Use X" or "By Y" in the prompt. If a method is named, that\'s the only one that scores. Pythagoras instead of cosine rule: 0. Ticking the box without working when "Use calculations" is specified: Low Partial Credit only.',
    subjects: ['maths'],
    examples: [
      { questionId: 'maths-2025-ord-p2-q10', snippet: '"Use the cosine rule to work out the distance from A to C" — Pythagoras or sine rule earn 0 even with the right answer.' },
      { questionId: 'maths-2025-ord-p1-q3', snippet: '"Use calculations to support your answer" — ticking Offer A without per-bar comparison only earns Low Partial Credit.' },
    ],
  },
  {
    id: 'diagram-no-labels',
    name: 'Diagram without labels = 0 marks',
    description:
      'A universal Geography rule. Every 30-mark question that gives a diagram bonus enforces it: an unlabelled diagram earns nothing. The labels are where the SRPs hide — arrows, named features, layers, time markers all need to be labelled explicitly.',
    diagnostic:
      'If you draw it, label every component: ice/crust/mantle, sediment direction, named processes, time/depth markers, arrows. Additional labelled detail earns +2 SRPs beyond the base diagram credit.',
    subjects: ['geography'],
    examples: [
      { questionId: 'geo-2025-hl-q1c', snippet: 'Diagram of isostatic rebound — labelled crust/mantle/ice + arrows = +1 SRP. Unlabelled = 0.' },
      { questionId: 'geo-2025-hl-q2bi', snippet: 'Cross-section of the deposition feature — labelled sediment movement + deposition zones = +1 SRP. Unlabelled = 0.' },
      { questionId: 'geo-2025-hl-q2c', snippet: 'Process diagrams for physical AND chemical weathering — both need labels separately.' },
    ],
  },
  {
    id: 'and-not-or',
    name: 'AND not OR — both halves required',
    description:
      'When a question says "explain X and Y" or "consider whether possible and desirable", both halves are required. Doing only one caps you at roughly half marks regardless of how well you answer. "And" is enforced; "or" gives you a choice.',
    diagnostic:
      'Underline the conjunctions. Two-part prompts joined by AND mean both halves must appear. Two-part prompts joined by OR let you pick.',
    subjects: ['geography', 'english'],
    examples: [
      { questionId: 'geo-2025-hl-q2c', snippet: '"Explain one process of physical weathering AND one process of chemical weathering" — only one explained = max 7 SRPs (14 of 30).' },
      { questionId: 'english-2024-p1-composing-5', snippet: '"whether or not it is possible, OR EVEN desirable" — both halves; engaging with only one caps Purpose.' },
    ],
  },
  {
    id: 'personal-vs-textual',
    name: 'Personal vs textual evidence',
    description:
      'English Question A has two distinct task shapes. A(i) "what does the writer reveal" requires textual anchor — every point quoted or paraphrased from the text. A(ii) "why do you think… develop three points" accepts personal views drawn from text and/or experience. Confusing them costs marks both ways.',
    diagnostic:
      'Read the verb: "reveal" / "show" / "convey" → A(i) shape; anchor in text. "Why do you think" / "develop three points" → A(ii) shape; your views, optionally with textual reference.',
    subjects: ['english'],
    examples: [
      { questionId: 'english-2024-p1-text1-qa-i', snippet: '"What does the writer reveal about family relationships" — three points, each anchored in the article.' },
      { questionId: 'english-2024-p1-text1-qa-ii', snippet: '"Why do you think parents don\'t like tattoos" — your developed views, drawn from text and/or experience.' },
    ],
  },
];

export function getTrapPattern(id: string): TrapPattern | undefined {
  return TRAP_PATTERNS.find(p => p.id === id);
}
