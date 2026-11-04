/** @license SPDX-License-Identifier: Apache-2.0 */
import type { PhysicalEducationAllocation, PhysicalEducationRubric, SecRubricCard } from '../../types/markBank';

export type PhysicalEducationScoreId = `pe:${string}`;
export type PhysicalEducationScores = Partial<Record<PhysicalEducationScoreId, number>>;
export const physicalEducationScoreId = (criterionId: string): PhysicalEducationScoreId => `pe:${criterionId}`;
/** A claimed row of a criterion cut into rows (cards/physical-education/answers.ts): 1, or the step it sits on. */
export const physicalEducationRowScoreId = (criterionId: string, rowId: string): PhysicalEducationScoreId => `pe:${criterionId}:row:${rowId}`;

type Criterion = PhysicalEducationRubric['criteria'][number];

export const physicalEducationRowValue = (criterion: Criterion, row: NonNullable<PhysicalEducationAllocation['rows']>[number], scores: PhysicalEducationScores): number => {
  const stored = scores[physicalEducationRowScoreId(criterion.id, row.id)] ?? 0;
  if (stored <= 0) return 0;
  if (row.steps) return row.steps.includes(stored) ? stored : 0;
  return row.marks;
};

/** A criterion's marks: the band mark placed on it plus its claimed rows, never above its maximum. */
export function physicalEducationCriterionMarks(criterion: Criterion, scores: PhysicalEducationScores): number {
  const placed = scores[physicalEducationScoreId(criterion.id)] ?? 0;
  const allocation = criterion.allocation;
  if (!allocation) return criterion.permittedMarks.includes(placed) ? placed : 0;
  const band = allocation.bands?.some(item => item.marks.includes(placed)) ? placed : 0;
  const rows = (allocation.rows ?? []).reduce((sum, row) => sum + physicalEducationRowValue(criterion, row, scores), 0);
  return Math.min(criterion.maxMarks, band + rows);
}

/** Only a mark actually permitted by this allocation contributes to the score. */
export function physicalEducationMarks(card: SecRubricCard, scores: PhysicalEducationScores): number {
  if (card.rubric.system !== 'physical-education') return 0;
  return card.rubric.criteria.reduce((sum, criterion) => sum + physicalEducationCriterionMarks(criterion, scores), 0);
}
