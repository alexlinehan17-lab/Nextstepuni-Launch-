/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Scoring for an unseen-translation card (types/markBank.ts TranslationRubric),
 * as the scheme marks one: unit by unit.
 *
 *  - Each unit is marked on its own, out of the marks the scheme writes after
 *    it ("…ferunt;/4").
 *  - Full marks for a unit, none, or partial marks: the scheme names no
 *    partial value, so a partial unit is any whole mark above none and below
 *    full, and the student chooses it.
 *  - The card's mark is the sum of the units, never more than the question's
 *    total. A saved value the unit does not permit (a fraction, a negative, a
 *    mark above the unit's value) counts as not marked, never rounded.
 */
import type { SecRubricCard, TranslationRubric, TranslationUnit } from '../../types/markBank';

export type TranslationScoreId = `translation:${string}`;
export type TranslationScores = Partial<Record<string, number>>;

export const translationUnitId = (unit: Pick<TranslationUnit, 'id'>): TranslationScoreId => `translation:${unit.id}`;

/** The mark a unit is placed at, or null when it is not marked (or marked with a value it cannot take). */
export function translationUnitMark(unit: TranslationUnit, scores: TranslationScores): number | null {
  const value = scores[translationUnitId(unit)];
  return typeof value === 'number' && Number.isInteger(value) && value >= 0 && value <= unit.marks ? value : null;
}

/** Every whole mark strictly between none and full: the partial marks a unit can take. */
export const partialSteps = (unit: TranslationUnit): number[] =>
  Array.from({ length: Math.max(0, unit.marks - 1) }, (_, index) => index + 1);

export function translationTally(rubric: TranslationRubric, scores: TranslationScores) {
  const marks = rubric.units.map(unit => translationUnitMark(unit, scores));
  return {
    marked: marks.filter(mark => mark !== null).length,
    units: rubric.units.length,
    total: marks.reduce<number>((sum, mark) => sum + (mark ?? 0), 0),
  };
}

export function translationMarks(card: SecRubricCard, scores: TranslationScores): number {
  if (card.rubric.system !== 'translation') return 0;
  return Math.max(0, Math.min(card.totalMarks, translationTally(card.rubric, scores).total));
}

/** Every unit has been marked (full, partial or none), so a grade can be suggested from the total. */
export const translationPlacementComplete = (rubric: TranslationRubric, scores: TranslationScores): boolean =>
  rubric.units.every(unit => translationUnitMark(unit, scores) !== null);
