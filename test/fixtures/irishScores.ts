/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Full marks on an Irish card, placed the way a student places them: every row of a criterion the scheme
 * is cut into (cards/irish/answers.ts, tariffs.ts) claimed at its top step, the mark itself on any other
 * award, and `deduct` on a language deduction.
 */
import { irishScoreId } from '../../components/MarkBank/SessionScreen';
import { irishRowScoreId } from '../../components/MarkBank/irishScoring';
import type { SecRubricCard } from '../../types/markBank';

export const irishFullScores = (card: SecRubricCard, deduct = 0): Record<string, number> => {
  if (card.rubric.system !== 'irish') throw new Error(`${card.id} is not an Irish card`);
  return Object.fromEntries(card.rubric.criteria.flatMap(criterion => criterion.allocation
    ? criterion.allocation.parts.flatMap(part => part.rows.map(row =>
      [irishRowScoreId(criterion.id, part.id, row.id), row.steps ? row.steps[row.steps.length - 1] : 1] as const))
    : [[irishScoreId(criterion.id), criterion.kind === 'deduction' ? deduct : criterion.maxMarks] as const]));
};
