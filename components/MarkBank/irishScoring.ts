/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Scoring for an Irish criterion whose exact guidance is cut into parts and
 * rows (cards/irish/answers.ts). A row's claim is stored as 1 under an id
 * that nests under the criterion's id, so the listening sheet, which
 * namespaces each extract's criteria, carries the rows with it.
 */
import type { IrishAllocation, IrishAnswerPart, IrishCriterion } from '../../types/markBank';

export type IrishScores = Partial<Record<string, number>>;

export const irishRowScoreId = (criterionId: string, partId: string, rowId: string) =>
  `irish:${criterionId}:${partId}:${rowId}`;

export const irishRowClaimed = (criterionId: string, part: IrishAnswerPart, rowId: string, scores: IrishScores) =>
  (scores[irishRowScoreId(criterionId, part.id, rowId)] ?? 0) > 0;

/** How many answers a sub-question asks for: its tariff over its full answer, or its ladder's length. */
export const irishPartCount = (part: IrishAnswerPart): number => {
  if (part.ladder) return part.ladder.length;
  const max = Math.max(0, ...part.rows.map(row => row.marks));
  return max > 0 ? Math.max(1, Math.floor(part.tariff / max)) : 1;
};

/** Marks for one sub-question: the ladder by rows ticked, or the highest
 * `count` claimed rows added, never above the sub-question's tariff. */
export const irishPartMarks = (criterionId: string, part: IrishAnswerPart, scores: IrishScores): number => {
  const claimed = part.rows.filter(row => irishRowClaimed(criterionId, part, row.id, scores));
  if (part.ladder) {
    const ticked = Math.min(claimed.length, part.ladder.length);
    return ticked > 0 ? part.ladder[ticked - 1] : 0;
  }
  const values = claimed.map(row => row.marks).sort((a, b) => b - a).slice(0, irishPartCount(part));
  return Math.min(part.tariff, values.reduce((sum, value) => sum + value, 0));
};

export const irishAllocationMarks = (criterionId: string, allocation: IrishAllocation, scores: IrishScores): number =>
  allocation.parts.reduce((sum, part) => sum + irishPartMarks(criterionId, part, scores), 0);

/** The criterion's value: its rows where it has them, its placed mark otherwise. */
export const irishCriterionMarks = (criterion: IrishCriterion, scores: IrishScores): number =>
  criterion.allocation
    ? Math.min(criterion.maxMarks, irishAllocationMarks(criterion.id, criterion.allocation, scores))
    : scores[`irish:${criterion.id}`] ?? 0;
