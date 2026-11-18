import type { FrenchAllocation, FrenchAnswerRow, FrenchCriterion, SecRubricCard } from '../../types/markBank';

/** The language a card on the French marking grid is examined in. Spanish
 *  writing is marked on the same grid shape (Communication/Language bands), so
 *  the panel names the scheme by the card's own subject. */
const RUBRIC_LANGUAGE: Record<string, string> = { french: 'French', spanish: 'Spanish', german: 'German' };
export const rubricLanguage = (subjectId: string): string => RUBRIC_LANGUAGE[subjectId] ?? 'French';

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

/** The student's "my answer is under N words" toggle for a lower scale. */
export const frenchShortId = (criterionId: string): FrenchScoreId => `french:${criterionId}:short`;

/** Whether a criterion's printed lower scale applies: the content it names
 *  adds up to its threshold or less, or the student says the answer is short.
 *  False for every criterion without one. */
export function lowerScaleActive(criteria: readonly FrenchCriterion[], criterion: FrenchCriterion, scores: FrenchScores): boolean {
  const lower = criterion.lowerScale;
  if (!lower) return false;
  if (lower.wordsUnder && scores[frenchShortId(criterion.id)] === 1) return true;
  const content = lower.contentCriteria.reduce((sum, id) => {
    const named = criteria.find(other => other.id === id);
    return sum + (named && !named.lowerScale ? frenchCriterionMark(criteria, named, scores) : 0);
  }, 0);
  return content <= lower.contentAtMost;
}

/** The marks one criterion earns as placed. Unchanged for every criterion
 *  without a lower scale; one with it is read against the scale that applies. */
export function frenchCriterionMark(criteria: readonly FrenchCriterion[], criterion: FrenchCriterion, scores: FrenchScores): number {
  if (criterion.requiresAttempt && scores[FRENCH_ATTEMPT_ID] !== 1) return 0;
  if (criterion.zeroWhenZero && (scores[frenchScoreId(criterion.zeroWhenZero)] ?? 0) === 0) return 0;
  const selected = scores[frenchScoreId(criterion.id)] ?? 0;
  const permitted = criterion.lowerScale && lowerScaleActive(criteria, criterion, scores)
    ? criterion.lowerScale.permittedMarks : criterion.permittedMarks;
  return permitted.includes(selected) ? selected : 0;
}

/** An attempted but unclear task can earn zero communication marks. The SEC's
 * no-attempt rule must therefore use an explicit check, not a positive score. */
export function frenchMarks(card: SecRubricCard, scores: FrenchScores): number {
  if (card.rubric.system !== 'french') return 0;
  if (card.rubric.allocation) return frenchAllocationMarks(card.totalMarks, card.rubric.allocation, scores);
  const { criteria } = card.rubric;
  return criteria.reduce((total, criterion) => total + frenchCriterionMark(criteria, criterion, scores), 0);
}
