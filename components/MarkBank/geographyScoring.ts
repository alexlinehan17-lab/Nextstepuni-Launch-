/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Geography scoring. A criterion is placed either as one number (the prose
 * fallback's mark control) or, when the scheme has been cut into rows
 * (cards/geography/allocation.ts), row by row: each claimed answer carries its
 * own marks, each SRP part its count. The criterion's total is the sum, capped
 * at the printed maximum, so a student can never place above the paper.
 */

import type { GeographyAllocation, GeographyCriterion, SecRubricCard } from '../../types/markBank';

export type GeographyScoreId = `geography:${string}`;
export type GeographyScores = Partial<Record<GeographyScoreId, number>>;

export const geographyScoreId = (criterionId: string): GeographyScoreId =>
  `geography:${criterionId}`;

/** A row's claim: 0, or one of the values the scheme prints for it. `unit` is
 *  the 1-based unit of a repeated group ("4 features @ 4 marks each"). */
export const geographyRowScoreId = (criterionId: string, rowId: string, unit?: number): GeographyScoreId =>
  `geography:${criterionId}:row:${rowId}${unit ? `:u${unit}` : ''}`;

/** An SRP part's claim: how many SRPs the student counted. */
export const geographySrpScoreId = (criterionId: string, srpId: string, unit?: number): GeographyScoreId =>
  `geography:${criterionId}:srp:${srpId}${unit ? `:u${unit}` : ''}`;

const units = (count: number | undefined) =>
  count ? Array.from({ length: count }, (_, index) => index + 1) : [undefined];

/** SRPs counted across the parts that share a pool, capped at the pool. */
export function geographyPooledSrps(criterion: GeographyCriterion, allocation: GeographyAllocation, scores: GeographyScores): number {
  let counted = 0;
  for (const group of allocation.groups) {
    for (const unit of units(group.repeat?.count)) {
      for (const srp of group.srp) {
        if (srp.min === undefined) continue;
        counted += Math.min(srp.count, scores[geographySrpScoreId(criterion.id, srp.id, unit)] ?? 0);
      }
    }
  }
  return allocation.srpPool ? Math.min(allocation.srpPool.count, counted) : counted;
}

export function geographyAllocationMarks(criterion: GeographyCriterion, scores: GeographyScores): number {
  const allocation = criterion.allocation;
  if (!allocation) return Math.max(0, Math.min(criterion.maxMarks, scores[geographyScoreId(criterion.id)] ?? 0));
  let total = 0;
  for (const group of allocation.groups) {
    for (const unit of units(group.repeat?.count)) {
      for (const row of group.rows) {
        const claimed = scores[geographyRowScoreId(criterion.id, row.id, unit)] ?? 0;
        const permitted = row.steps ?? [row.marks];
        total += permitted.includes(claimed) ? claimed : 0;
      }
      for (const srp of group.srp) {
        if (srp.min !== undefined) continue;
        const count = Math.min(srp.count, Math.max(0, scores[geographySrpScoreId(criterion.id, srp.id, unit)] ?? 0));
        total += count * srp.marks;
      }
    }
  }
  if (allocation.srpPool) total += geographyPooledSrps(criterion, allocation, scores) * allocation.srpPool.marks;
  return Math.max(0, Math.min(criterion.maxMarks, total));
}

/** The marks a Geography card is placed at, across all its criteria. */
export function geographyMarks(card: SecRubricCard, scores: GeographyScores): number {
  if (card.rubric.system !== 'geography') return 0;
  const total = card.rubric.criteria.reduce(
    (sum, criterion) => sum + geographyAllocationMarks(criterion, scores), 0,
  );
  return Math.max(0, Math.min(card.totalMarks, total));
}
