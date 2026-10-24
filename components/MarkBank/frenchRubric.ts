import type { SecRubricCard } from '../../types/markBank';

export type FrenchScoreId = `french:${string}`;
export type FrenchScores = Partial<Record<FrenchScoreId, number>>;
export const frenchScoreId = (id: string): FrenchScoreId => `french:${id}`;
export const FRENCH_ATTEMPT_ID: FrenchScoreId = 'french:communicative-task-attempted';

/** An attempted but unclear task can earn zero communication marks. The SEC's
 * no-attempt rule must therefore use an explicit check, not a positive score. */
export function frenchMarks(card: SecRubricCard, scores: FrenchScores): number {
  if (card.rubric.system !== 'french') return 0;
  return card.rubric.criteria.reduce((total, criterion) => {
    if (criterion.requiresAttempt && scores[FRENCH_ATTEMPT_ID] !== 1) return total;
    const selected = scores[frenchScoreId(criterion.id)] ?? 0;
    return total + (criterion.permittedMarks.includes(selected) ? selected : 0);
  }, 0);
}
