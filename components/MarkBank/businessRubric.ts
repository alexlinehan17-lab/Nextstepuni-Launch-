/** @license SPDX-License-Identifier: Apache-2.0 */
import type { BusinessExpectedItem, BusinessRubric, SecRubricCard } from '../../types/markBank';

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

export const businessExpectedId = (item: string): BusinessScoreId => `business:expected:${item}`;
/** The row for an answer the scheme's sample does not print; the SEC says the list is never exhaustive. */
export const BUSINESS_OTHER_RESPONSE = 'other';

export type BusinessExpectedLayout =
  /** Every response names one printed item ("Gross pay", "PAYE"): the item sits under its response. */
  | { kind: 'per-response'; items: Map<string, BusinessExpectedItem> }
  /** One printed pool the responses draw from ("Benefit 1", "Benefit 2" over five bullets). */
  | { kind: 'pool'; items: BusinessExpectedItem[] };

const compact = (value: string) => value.toLowerCase().replace(/[^a-z0-9]+/g, '');

/** How the scheme's printed responses map onto the card's responses. */
export function businessExpectedLayout(rubric: BusinessRubric): BusinessExpectedLayout | null {
  const expected = rubric.expected;
  if (!expected?.items.length) return null;
  const perResponse = new Map<string, BusinessExpectedItem>();
  const taken = new Set<string>();
  for (const response of rubric.responses) {
    const label = compact(response.label);
    if (label.length < 4) break;
    const hits = expected.items.filter(item => {
      const text = compact(item.text);
      return text.startsWith(label.slice(0, 12)) || text.slice(0, 80).includes(label);
    });
    if (hits.length !== 1 || taken.has(hits[0].id)) break;
    taken.add(hits[0].id);
    perResponse.set(response.id, hits[0]);
  }
  if (perResponse.size === rubric.responses.length) return { kind: 'per-response', items: perResponse };
  return { kind: 'pool', items: expected.items };
}

/** The marks one claimed response is worth: one chip when every response prices the same, else the printed sequence. */
export function businessResponseMarks(rubric: BusinessRubric): { marks?: number; tag?: string } {
  const totals = rubric.responses.map(response => response.allocations.reduce((sum, allocation) => sum + allocation.maxMarks, 0));
  if (totals.length === 0) return {};
  if (totals.every(total => total === totals[0])) return { marks: totals[0] };
  return { tag: totals.map(total => `${total}m`).join(' then ') };
}

/** The score writes that claim or clear a response's full allocation. */
export function businessResponseFill(rubric: BusinessRubric, responseId: string, claim: boolean): Array<[BusinessScoreId, number]> {
  const response = rubric.responses.find(item => item.id === responseId);
  if (!response) return [];
  return response.allocations.map(allocation => [businessScoreId(response.id, allocation.id), claim ? allocation.maxMarks : 0]);
}

/** In a pool, a claim fills the first response with nothing placed; a clear empties the last one still at full marks. */
export function businessPoolTarget(rubric: BusinessRubric, scores: BusinessScores, claim: boolean): string | undefined {
  const placed = (response: BusinessRubric['responses'][number]) =>
    response.allocations.reduce((sum, allocation) => sum + (scores[businessScoreId(response.id, allocation.id)] ?? 0), 0);
  const full = (response: BusinessRubric['responses'][number]) =>
    response.allocations.every(allocation => (scores[businessScoreId(response.id, allocation.id)] ?? 0) === allocation.maxMarks);
  if (claim) return rubric.responses.find(response => placed(response) === 0)?.id;
  return [...rubric.responses].reverse().find(full)?.id;
}
