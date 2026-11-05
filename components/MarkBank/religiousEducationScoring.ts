/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Scoring for a Religious Education card: each answer holds the one mark the
 * student placed on the scheme's band grid, and a ticked ceiling caps every
 * answer at its printed maximum.
 */
import type { ReligiousEducationRubric } from '../../types/markBank';

export type ReligiousEducationScoreId = `re:${string}`;
export type ReligiousEducationScores = Partial<Record<string, number>>;

/** Answer `index` (0-based): the mark placed on its grid. */
export const reAnswerScoreId = (index: number): ReligiousEducationScoreId => `re:answer:${index + 1}`;
/** The ceiling ticked, as its 1-based position in the rubric's ceilings; 0 for none. */
export const reCeilingScoreId: ReligiousEducationScoreId = 're:ceiling';

/** The ceiling the student ticked, or null. */
export function reCeiling(rubric: ReligiousEducationRubric, scores: ReligiousEducationScores): number | null {
  const ticked = scores[reCeilingScoreId] ?? 0;
  const ceiling = rubric.ceilings?.[ticked - 1];
  return ceiling ? ceiling.max : null;
}

/** The mark placed on one answer's grid: 0 unless it is a mark one of the bands permits. */
export function reAnswerValue(rubric: ReligiousEducationRubric, scores: ReligiousEducationScores, index: number): number {
  const value = scores[reAnswerScoreId(index)] ?? 0;
  return rubric.bands.some(band => band.marks.includes(value)) ? value : 0;
}

/** What one answer scores: its placed mark, held under a ticked ceiling. */
export function reAnswerMarks(rubric: ReligiousEducationRubric, scores: ReligiousEducationScores, index: number): number {
  const value = reAnswerValue(rubric, scores, index);
  const ceiling = reCeiling(rubric, scores);
  return ceiling === null ? value : Math.min(value, ceiling);
}

export function religiousEducationRubricMarks(rubric: ReligiousEducationRubric, scores: ReligiousEducationScores, totalMarks: number): number {
  let total = 0;
  for (let index = 0; index < rubric.answers; index += 1) total += reAnswerMarks(rubric, scores, index);
  return Math.max(0, Math.min(totalMarks, total));
}
