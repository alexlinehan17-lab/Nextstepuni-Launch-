/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Scoring for a Religious Education card: each answer holds the one mark the
 * student placed on the scheme's band grid, and a ticked ceiling caps every
 * answer at its printed maximum. Where the grid prints two marks rows (one
 * answer out of 40, or two answers out of 20), the student picks the way they
 * wrote and only that way's placements score.
 */
import type { ReligiousEducationBand, ReligiousEducationRubric } from '../../types/markBank';

export type ReligiousEducationScoreId = `re:${string}`;
export type ReligiousEducationScores = Partial<Record<string, number>>;

/** The way chosen: 0 for the card's own (first-named) marks row, 1 for its
 *  other one. Absent means 0. */
export const reWayScoreId: ReligiousEducationScoreId = 're:way';

/** One way of marking the card: how many answers, each out of what, on which ranges. */
export interface ReligiousEducationActiveWay {
  way: 0 | 1;
  gridHead: string;
  answers: number;
  answerMax: number;
  bands: ReligiousEducationBand[];
}

/** The card's ways, its own first: one, or two where the grid prints two marks rows. */
export function reWays(rubric: ReligiousEducationRubric): ReligiousEducationActiveWay[] {
  const own: ReligiousEducationActiveWay = {
    way: 0, gridHead: rubric.gridHead, answers: rubric.answers, answerMax: rubric.answerMax, bands: rubric.bands,
  };
  const other = rubric.otherWay;
  if (!other) return [own];
  return [own, {
    way: 1, gridHead: other.gridHead, answers: other.answers, answerMax: other.answerMax,
    bands: rubric.bands.map((band, index) => ({ ...band, printed: other.bands[index].printed, marks: other.bands[index].marks })),
  }];
}

/** The way the student has chosen, or the card's own by default. */
export function reWay(rubric: ReligiousEducationRubric, scores: ReligiousEducationScores): ReligiousEducationActiveWay {
  const ways = reWays(rubric);
  return ways[scores[reWayScoreId] === 1 ? ways.length - 1 : 0];
}

/** Answer `index` (0-based) on a way: the mark placed on its grid. Each way
 *  keeps its own placements, so marks placed on the way not chosen never score. */
export const reAnswerScoreId = (index: number, way: 0 | 1 = 0): ReligiousEducationScoreId =>
  way === 1 ? `re:other:answer:${index + 1}` : `re:answer:${index + 1}`;
/** The band an answer was placed in, by its position on the ladder. Kept only
 *  where the placed mark is printed in more than one band (2019 Higher
 *  I(b)(i) prints 3-4 and 2-3; 2018 Higher B(a)(i) prints one "1 ↑ 0" cell
 *  beside three bands): the mark scores either way, and the band the
 *  student chose is the one that shows it. */
export const reAnswerBandId = (index: number, way: 0 | 1 = 0): ReligiousEducationScoreId =>
  `${reAnswerScoreId(index, way)}:band`;
/** The ceiling ticked, as its 1-based position in the rubric's ceilings; 0 for none. */
export const reCeilingScoreId: ReligiousEducationScoreId = 're:ceiling';

/** The ceiling the student ticked, or null. */
export function reCeiling(rubric: ReligiousEducationRubric, scores: ReligiousEducationScores): number | null {
  const ticked = scores[reCeilingScoreId] ?? 0;
  const ceiling = rubric.ceilings?.[ticked - 1];
  return ceiling ? ceiling.max : null;
}

/** The mark placed on one answer's grid, on the chosen way: 0 unless it is a
 *  mark one of the bands permits. */
export function reAnswerValue(rubric: ReligiousEducationRubric, scores: ReligiousEducationScores, index: number): number {
  const way = reWay(rubric, scores);
  const value = scores[reAnswerScoreId(index, way.way)] ?? 0;
  return way.bands.some(band => band.marks.includes(value)) ? value : 0;
}

/** Whether the student has placed this answer at all, on the chosen way. 0
 *  is a mark the bottom band permits, so "placed at 0" and "not placed" are
 *  told apart: an unplaced answer is stored as -1 (or never stored). */
export const reAnswerPlaced = (rubric: ReligiousEducationRubric, scores: ReligiousEducationScores, index: number): boolean => {
  const way = reWay(rubric, scores);
  const value = scores[reAnswerScoreId(index, way.way)];
  return value !== undefined && way.bands.some(band => band.marks.includes(value));
};
export const RE_UNPLACED = -1;

/** Where an answer's placed mark shows: the band it was placed in when that
 *  band prints the mark, else the first band that prints it; -1 when the
 *  answer is not placed. On a grid whose bands do not overlap this is simply
 *  the one band holding the mark. */
export function reAnswerBand(rubric: ReligiousEducationRubric, scores: ReligiousEducationScores, index: number): number {
  if (!reAnswerPlaced(rubric, scores, index)) return -1;
  const way = reWay(rubric, scores);
  const value = reAnswerValue(rubric, scores, index);
  const chosen = scores[reAnswerBandId(index, way.way)];
  if (chosen !== undefined && way.bands[chosen]?.marks.includes(value)) return chosen;
  return way.bands.findIndex(band => band.marks.includes(value));
}

/** What one answer scores: its placed mark, held under a ticked ceiling. */
export function reAnswerMarks(rubric: ReligiousEducationRubric, scores: ReligiousEducationScores, index: number): number {
  const value = reAnswerValue(rubric, scores, index);
  const ceiling = reCeiling(rubric, scores);
  return ceiling === null ? value : Math.min(value, ceiling);
}

export function religiousEducationRubricMarks(rubric: ReligiousEducationRubric, scores: ReligiousEducationScores, totalMarks: number): number {
  let total = 0;
  const { answers } = reWay(rubric, scores);
  for (let index = 0; index < answers; index += 1) total += reAnswerMarks(rubric, scores, index);
  return Math.max(0, Math.min(totalMarks, total));
}
