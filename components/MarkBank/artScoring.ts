/** @license SPDX-License-Identifier: Apache-2.0 */
import type { ArtAllocationRow, ArtCriterion, SecRubricCard } from '../../types/markBank';

export type ArtScoreId = `art:${string}`;
export type ArtScores = Partial<Record<ArtScoreId, number>>;

/** A whole criterion's placed mark: 2023+ descriptor bands, or a component without rows. */
export const artScoreId = (criterionId: string): ArtScoreId => `art:${criterionId}`;
/** A row of a component cut into rows (cards/art/answers.ts), or one of the parts its note splits it into. */
export const artRowScoreId = (criterionId: string, rowId: string, partId?: string): ArtScoreId =>
  partId ? `art:${criterionId}:row:${rowId}:part:${partId}` : `art:${criterionId}:row:${rowId}`;

/** A stored mark as the row takes it: a whole number from 0 up to the row's marks. */
export const artPlaced = (value: number | undefined, max: number) =>
  Number.isInteger(value) && (value as number) > 0 ? Math.min(max, value as number) : 0;
const placed = artPlaced;

/** What the student has placed on a row: its parts added, or its own mark. */
export const artRowMarks = (criterionId: string, row: ArtAllocationRow, scores: ArtScores): number => {
  if (row.parts) {
    return Math.min(row.marks, row.parts.reduce((total, part) => total + placed(scores[artRowScoreId(criterionId, row.id, part.id)], part.marks), 0));
  }
  return placed(scores[artRowScoreId(criterionId, row.id)], row.marks);
};

/** A criterion's marks: its rows added where it has rows, otherwise the mark placed on it, never above its maximum. */
export function artCriterionMarks(criterion: ArtCriterion, scores: ArtScores): number {
  if (criterion.allocation) {
    return Math.min(criterion.maxMarks, criterion.allocation.rows.reduce((total, row) => total + artRowMarks(criterion.id, row, scores), 0));
  }
  return placed(scores[artScoreId(criterion.id)], criterion.maxMarks);
}

/** Art components and descriptor criteria are independently awarded and added. */
export function artMarks(card: SecRubricCard, scores: ArtScores): number {
  if (card.rubric.system !== 'art') return 0;
  const total = card.rubric.criteria.reduce((total, criterion) => total + artCriterionMarks(criterion, scores), 0);
  return Math.max(0, Math.min(card.totalMarks, total));
}
