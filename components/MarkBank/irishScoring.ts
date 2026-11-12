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

/** A row's point: rows sharing a group are one point's printed alternatives; every other row is its own point. */
export const irishRowPoint = (row: IrishAnswerPart['rows'][number]) => row.group ?? row.id;

/** One entry per point, at its best row's marks (a group counts once). */
const irishPoints = (part: IrishAnswerPart): number[] => {
  const best = new Map<string, number>();
  for (const row of part.rows) best.set(irishRowPoint(row), Math.max(best.get(irishRowPoint(row)) ?? 0, row.marks));
  return [...best.values()];
};

/** How many answers a sub-question asks for: its tariff over its full answer, or its ladder's length. */
export const irishPartCount = (part: IrishAnswerPart): number => {
  if (part.ladder) return part.ladder.length;
  // Rows priced as a tariff ("Tréith 1 = 13 mharc", "Dhá phointe eolais = 4 + 4") are all claimable at once,
  // and so are rows that are the tariff's components ("Tréith 1 a lua = 2 mharc", "sampla … = 4 mharc" of 6):
  // an answer list prices alternatives, which never add up to the sub-question exactly when their marks differ.
  // A group of one point's alternatives counts as that one point.
  const points = irishPoints(part);
  if (part.rows.some(row => row.steps)) return points.length;
  if (points.length > 1 && points.reduce((sum, marks) => sum + marks, 0) === part.tariff) return points.length;
  const max = Math.max(0, ...part.rows.map(row => row.marks));
  return max > 0 ? Math.max(1, Math.floor(part.tariff / max)) : 1;
};

/** What a claimed row is worth: its placed step where it has steps, else its marks. */
export const irishRowValue = (criterionId: string, part: IrishAnswerPart, row: IrishAnswerPart['rows'][number], scores: IrishScores): number => {
  const stored = scores[irishRowScoreId(criterionId, part.id, row.id)] ?? 0;
  if (row.steps) return row.steps.includes(stored) ? stored : 0;
  return stored > 0 ? row.marks : 0;
};

/** Marks for one sub-question: the ladder by rows ticked, or the highest
 * `count` claimed rows added, never above the sub-question's tariff. */
export const irishPartMarks = (criterionId: string, part: IrishAnswerPart, scores: IrishScores): number => {
  const claimed = part.rows.filter(row => irishRowClaimed(criterionId, part, row.id, scores));
  if (part.ladder) {
    const ticked = Math.min(new Set(claimed.map(irishRowPoint)).size, part.ladder.length);
    return ticked > 0 ? part.ladder[ticked - 1] : 0;
  }
  // A point counts once, at its best claimed row.
  const best = new Map<string, number>();
  for (const row of claimed) best.set(irishRowPoint(row), Math.max(best.get(irishRowPoint(row)) ?? 0, irishRowValue(criterionId, part, row, scores)));
  const values = [...best.values()].sort((a, b) => b - a).slice(0, irishPartCount(part));
  return Math.min(part.tariff, values.reduce((sum, value) => sum + value, 0));
};

export const irishAllocationMarks = (criterionId: string, allocation: IrishAllocation, scores: IrishScores): number =>
  allocation.parts.reduce((sum, part) => sum + irishPartMarks(criterionId, part, scores), 0);

/** The criterion's value: its rows where it has them, its placed mark otherwise. */
export const irishCriterionMarks = (criterion: IrishCriterion, scores: IrishScores): number =>
  criterion.allocation
    ? Math.min(criterion.maxMarks, irishAllocationMarks(criterion.id, criterion.allocation, scores))
    : scores[`irish:${criterion.id}`] ?? 0;
