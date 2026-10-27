import type { FrenchAllocation, FrenchAnswerRow, SecRubricCard } from '../../types/markBank';

export type FrenchScoreId = `french:${string}`;
export type FrenchScores = Partial<Record<FrenchScoreId, number>>;
export const frenchScoreId = (id: string): FrenchScoreId => `french:${id}`;
export const frenchRowScoreId = (rowId: string): FrenchScoreId => `french:row:${rowId}`;
export const FRENCH_ATTEMPT_ID: FrenchScoreId = 'french:communicative-task-attempted';

/** A claimed plain row is stored as 1; a stepped row stores the step it sits on. */
export const frenchRowValue = (row: FrenchAnswerRow, scores: FrenchScores): number => {
  const stored = scores[frenchRowScoreId(row.id)] ?? 0;
  if (stored <= 0) return 0;
  if (row.steps) return row.steps.includes(stored) ? stored : 0;
  return row.marks;
};

export const frenchRowClaimed = (row: FrenchAnswerRow, scores: FrenchScores): boolean =>
  (scores[frenchRowScoreId(row.id)] ?? 0) > 0;

/**
 * Marks for a card whose scheme is cut into rows. Up to `count` positive rows
 * score (the highest-valued ones, should more be claimed); a ladder prices the
 * number ticked; the aural higher-segment rule doubles the better detail; a
 * claimed deduction comes off; never below 0 or above the printed total.
 */
export function frenchAllocationMarks(total: number, allocation: FrenchAllocation, scores: FrenchScores): number {
  const claimed = allocation.rows.filter(row => frenchRowClaimed(row, scores));
  const deductions = claimed.filter(row => row.marks < 0).reduce((sum, row) => sum - row.marks, 0);
  let earned: number;
  if (allocation.ladder) {
    const ticked = Math.min(claimed.filter(row => row.marks >= 0).length, allocation.count);
    earned = ticked > 0 ? allocation.ladder[ticked - 1] : 0;
  } else {
    const values = claimed.filter(row => row.marks >= 0).map(row => frenchRowValue(row, scores)).sort((a, b) => b - a);
    earned = allocation.scoring === 'higher-segment-both'
      ? 2 * (values[0] ?? 0)
      : values.slice(0, allocation.count).reduce((sum, value) => sum + value, 0);
  }
  return Math.max(0, Math.min(total, earned - deductions));
}

/** An attempted but unclear task can earn zero communication marks. The SEC's
 * no-attempt rule must therefore use an explicit check, not a positive score. */
export function frenchMarks(card: SecRubricCard, scores: FrenchScores): number {
  if (card.rubric.system !== 'french') return 0;
  if (card.rubric.allocation) return frenchAllocationMarks(card.totalMarks, card.rubric.allocation, scores);
  return card.rubric.criteria.reduce((total, criterion) => {
    if (criterion.requiresAttempt && scores[FRENCH_ATTEMPT_ID] !== 1) return total;
    const selected = scores[frenchScoreId(criterion.id)] ?? 0;
    return total + (criterion.permittedMarks.includes(selected) ? selected : 0);
  }, 0);
}
