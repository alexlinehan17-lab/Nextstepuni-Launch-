/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Geography scoring. A criterion is placed either as one number (the prose
 * fallback's mark control) or, when the scheme has been cut into rows
 * (cards/geography/allocation.ts), row by row: each claimed answer carries its
 * own marks, each SRP part its count. Where the scheme prices a criterion one
 * of several ways (two routes, a band table, one printed answer or another) the
 * student picks one option and only that option scores. The criterion's total
 * is capped at the printed maximum, so a student can never place above the paper.
 */

import type { GeographyAllocation, GeographyAnswerRow, GeographyCriterion, SecRubricCard } from '../../types/markBank';

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

/** A choice's claim: the 1-based option the student picked (a route, a band
 *  or one of two printed answers); 0 or absent is none. A choice that
 *  `follows` another criterion's is scored under that criterion's id. */
export const geographyChoiceScoreId = (criterionId: string): GeographyScoreId =>
  `geography:${criterionId}:choice`;

/** The criterion id an option's own rows are scored under, so a route's rows
 *  never share a score with the other route's. */
export const geographyOptionCriterionId = (criterionId: string, optionId: string) =>
  `${criterionId}:${optionId}`;

/** What a row can be claimed at in one unit of a repeated group: its own
 *  price there where the scheme prices the units unalike (`unitMarks`, "7/6
 *  marks graded" over 27 + 27 + 26), and only the steps up to that price. */
export function geographyRowInUnit(row: GeographyAnswerRow, unit?: number): { marks: number; steps?: number[] } {
  const own = unit !== undefined ? row.unitMarks?.[unit - 1] : undefined;
  if (own === undefined || own === row.marks) return { marks: row.marks, steps: row.steps };
  const steps = row.steps?.filter(step => step <= own);
  return { marks: own, steps: steps && steps.length > 1 ? steps : undefined };
}

/** The values a row can be claimed at in one unit: its steps, or its price. */
export const geographyRowClaims = (row: GeographyAnswerRow, unit?: number): number[] => {
  const { marks, steps } = geographyRowInUnit(row, unit);
  return steps ?? [marks];
};

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
  if (allocation.choice) {
    // A choice that follows another criterion's (one printed route table split
    // over several criteria) reads that criterion's pick.
    const picked = allocation.choice.options[(scores[geographyChoiceScoreId(allocation.choice.follows ?? criterion.id)] ?? 0) - 1];
    if (!picked) return 0;
    const value = picked.allocation
      ? geographyAllocationMarks({
        ...criterion,
        id: geographyOptionCriterionId(criterion.id, picked.id),
        allocation: picked.allocation,
      }, scores)
      : picked.marks ?? 0;
    return Math.max(0, Math.min(criterion.maxMarks, value));
  }
  let total = 0;
  for (const group of allocation.groups) {
    for (const unit of units(group.repeat?.count)) {
      for (const row of group.rows) {
        const claimed = scores[geographyRowScoreId(criterion.id, row.id, unit)] ?? 0;
        total += geographyRowClaims(row, unit).includes(claimed) ? claimed : 0;
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
