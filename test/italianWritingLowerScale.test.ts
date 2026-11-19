/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Italian writing cards carry the scheme's printed language cap as a lower
 * scale (FrenchCriterion.lowerScale): Higher "In C1 and C2 where the marks
 * awarded for content and communication are 7 or less, language will be marked
 * out of 5" (C3: 12 or less, out of 7), Ordinary "Where marks for content and
 * communication are 7 or less, award no marks for language". The scheme prints
 * no bands for the lower scale, so it carries none.
 */

import { describe, expect, it } from 'vitest';
import { frenchMarks, frenchScoreId, lowerScaleActive, type FrenchScores } from '../components/MarkBank/frenchRubric';
import { CARDS as ITALIAN_HIGHER } from '../components/MarkBank/cards/italian/higher';
import { CARDS as ITALIAN_ORDINARY } from '../components/MarkBank/cards/italian/ordinary';
import type { FrenchRubric, SecCard, SecRubricCard } from '../types/markBank';

const card = (cards: readonly SecCard[], id: string): SecRubricCard => {
  const found = cards.find(c => c.id === id);
  if (!found || found.kind !== 'rubric') throw new Error(`${id} is not a rubric card`);
  return found as SecRubricCard;
};
const criteria = (c: SecRubricCard) => (c.rubric as FrenchRubric).criteria;
const place = (entries: Record<string, number>): FrenchScores =>
  Object.fromEntries(Object.entries(entries).map(([id, mark]) => [frenchScoreId(id), mark]));

describe('Italian writing: the scheme\'s printed language cap', () => {
  it('Higher C2 places language out of 5 while content is 7 or less', () => {
    const c = card(ITALIAN_HIGHER, 'it-2026-hl-c-2');
    const language = criteria(c).find(k => k.id === 'language')!;
    expect(language.lowerScale?.maxMarks).toBe(5);
    expect(language.lowerScale?.rule).toMatch(/7 or less, language\s+will be marked out of 5/);
    expect(lowerScaleActive(criteria(c), language, place({ content: 7, language: 5 }))).toBe(true);
    expect(frenchMarks(c, place({ content: 7, language: 5 }))).toBe(12);
    expect(frenchMarks(c, place({ content: 8, language: 10 }))).toBe(18);
  });

  it('Higher C3 places language out of 7 while content is 12 or less', () => {
    const c = card(ITALIAN_HIGHER, 'it-2026-hl-c-3-a');
    const language = criteria(c).find(k => k.id === 'language')!;
    expect(language.lowerScale?.maxMarks).toBe(7);
    expect(frenchMarks(c, place({ format: 10, content: 12, language: 7 }))).toBe(29);
    expect(frenchMarks(c, place({ format: 10, content: 13, language: 15 }))).toBe(38);
  });

  it('Ordinary C1 awards no language marks while content is 7 or less', () => {
    const c = card(ITALIAN_ORDINARY, 'it-2026-ol-c-1-a');
    const language = criteria(c).find(k => k.id === 'language')!;
    expect(language.lowerScale?.maxMarks).toBe(0);
    expect(frenchMarks(c, place({ format: 7, content: 7, language: 0 }))).toBe(14);
    expect(frenchMarks(c, place({ format: 7, content: 8, language: 7 }))).toBe(22);
  });
});
