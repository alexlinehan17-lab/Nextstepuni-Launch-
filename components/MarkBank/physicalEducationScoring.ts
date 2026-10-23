/** @license SPDX-License-Identifier: Apache-2.0 */
import type { SecRubricCard } from '../../types/markBank';

export type PhysicalEducationScoreId = `pe:${string}`;
export const physicalEducationScoreId = (criterionId: string): PhysicalEducationScoreId => `pe:${criterionId}`;

/** Only a mark actually permitted by this allocation contributes to the score. */
export function physicalEducationMarks(
  card: SecRubricCard,
  scores: Partial<Record<PhysicalEducationScoreId, number>>,
): number {
  if (card.rubric.system !== 'physical-education') return 0;
  return card.rubric.criteria.reduce((sum, criterion) => {
    const mark = scores[physicalEducationScoreId(criterion.id)] ?? 0;
    return sum + (criterion.permittedMarks.includes(mark) ? mark : 0);
  }, 0);
}
