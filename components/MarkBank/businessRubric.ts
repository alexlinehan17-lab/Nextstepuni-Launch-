/** @license SPDX-License-Identifier: Apache-2.0 */
import type { BusinessRubric, SecRubricCard } from '../../types/markBank';

export type BusinessScoreId = `business:${string}:${string}`;
export type BusinessScores = Partial<Record<BusinessScoreId, number>>;
export const businessScoreId = (response: string, allocation: string): BusinessScoreId =>
  `business:${response}:${allocation}`;

/** Enforce published allocations and link dependencies even for persisted data. */
export function effectiveBusinessScores(rubric: BusinessRubric, scores: BusinessScores): BusinessScores {
  const effective: BusinessScores = {};
  for (const response of rubric.responses) {
    const bounded = new Map(response.allocations.map(allocation => {
      const requested = scores[businessScoreId(response.id, allocation.id)] ?? 0;
      const marks = Number.isFinite(requested)
        ? Math.max(0, ...allocation.permittedMarks.filter(mark => mark <= requested)) : 0;
      return [allocation.id, marks];
    }));
    for (const allocation of response.allocations) {
      const permitted = !allocation.requiresAnyOf
        || allocation.requiresAnyOf.some(id => (bounded.get(id) ?? 0) > 0);
      effective[businessScoreId(response.id, allocation.id)] = permitted
        ? bounded.get(allocation.id) ?? 0 : 0;
    }
  }
  return effective;
}

export function businessMarks(card: SecRubricCard, scores: BusinessScores): number {
  if (card.rubric.system !== 'business') return 0;
  return Object.values(effectiveBusinessScores(card.rubric, scores))
    .reduce((sum, value) => sum + (value ?? 0), 0);
}
