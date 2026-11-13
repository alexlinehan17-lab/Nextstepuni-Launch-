/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * FrenchCriterion.lowerScale (German "Lower E"): the scale the scheme prints
 * beside a criterion's full one, switched on by the content placed or by the
 * student saying the answer is short. A card without one scores exactly as
 * before: every French and Spanish grid card is checked against the scoring
 * this change replaced, over many placements.
 */

import { describe, expect, it } from 'vitest';
import { FRENCH_ATTEMPT_ID, frenchMarks, frenchScoreId, frenchShortId, lowerScaleActive, type FrenchScores } from '../components/MarkBank/frenchRubric';
import { CARDS as SPANISH_HIGHER } from '../components/MarkBank/cards/spanish/higher';
import { CARDS as SPANISH_ORDINARY } from '../components/MarkBank/cards/spanish/ordinary';
import frenchWriting from '../components/MarkBank/cards/french/writing.json';
import type { FrenchCriterion, FrenchRubric, SecCard, SecRubricCard } from '../types/markBank';

/** frenchMarks as it was before lowerScale, for the criteria path. */
function previousMarks(card: SecRubricCard, scores: FrenchScores): number {
  if (card.rubric.system !== 'french' || card.rubric.allocation) return frenchMarks(card, scores);
  return card.rubric.criteria.reduce((total, criterion) => {
    if (criterion.requiresAttempt && scores[FRENCH_ATTEMPT_ID] !== 1) return total;
    if (criterion.zeroWhenZero && (scores[frenchScoreId(criterion.zeroWhenZero)] ?? 0) === 0) return total;
    const selected = scores[frenchScoreId(criterion.id)] ?? 0;
    return total + (criterion.permittedMarks.includes(selected) ? selected : 0);
  }, 0);
}

/** A small deterministic generator, so a failure names a reproducible case. */
function random(seed: number) {
  let s = seed;
  return () => { s = (s * 1103515245 + 12345) % 2147483648; return s / 2147483648; };
}

const grids = [...frenchWriting, ...SPANISH_HIGHER, ...SPANISH_ORDINARY]
  .filter((card): card is SecRubricCard => (card as SecCard).kind === 'rubric'
    && (card as SecRubricCard).rubric.system === 'french'
    && !((card as SecRubricCard).rubric as FrenchRubric).allocation);

describe('a grid card without a lower scale scores as before', () => {
  it('matches the previous scoring on every French and Spanish grid card', () => {
    expect(grids.length).toBeGreaterThan(50);
    const next = random(7);
    const mismatches: string[] = [];
    for (const card of grids) {
      if (card.rubric.system !== 'french') continue;
      for (let round = 0; round < 40; round += 1) {
        const scores: FrenchScores = {};
        if (next() < 0.7) scores[FRENCH_ATTEMPT_ID] = 1;
        for (const criterion of card.rubric.criteria) {
          scores[frenchScoreId(criterion.id)] = Math.floor(next() * (criterion.maxMarks + 3));
        }
        if (frenchMarks(card, scores) !== previousMarks(card, scores)) mismatches.push(`${card.id} round ${round}`);
      }
    }
    expect(mismatches).toEqual([]);
  });

  it('no French or Spanish card carries a lower scale', () => {
    expect(grids.filter(card => card.rubric.system === 'french'
      && card.rubric.criteria.some(criterion => criterion.lowerScale)).map(card => card.id)).toEqual([]);
  });
});

describe('a printed lower scale', () => {
  // The 2026 Higher Äußerung shape: content A 3, B 4, C 4, Dis. 2; Expression
  // 12, or 7 "if the content mark is 8 or less, or the answer is too short".
  const point = (id: string, max: number): FrenchCriterion => ({
    id, label: id.toUpperCase(), maxMarks: max, permittedMarks: Array.from({ length: max + 1 }, (_v, i) => i), guidance: [],
  });
  const expression: FrenchCriterion = {
    ...point('expression', 12),
    lowerScale: {
      label: 'Lower E', maxMarks: 7, permittedMarks: [0, 1, 2, 3, 4, 5, 6, 7], bands: [],
      contentCriteria: ['a', 'b', 'c', 'dis'], contentAtMost: 8, wordsUnder: 60,
      rule: 'If the content mark is 8 or less, or the answer is too short (less than 60 words), mark expression out of 7',
    },
  };
  const criteria = [point('a', 3), point('b', 4), point('c', 4), point('dis', 2), expression];
  const card = { kind: 'rubric', totalMarks: 25, rubric: { system: 'french', taskRequirements: [], criteria, markingGuideNote: '' } } as unknown as SecRubricCard;
  const place = (a: number, b: number, c: number, dis: number, e: number, short = false): FrenchScores => ({
    [frenchScoreId('a')]: a, [frenchScoreId('b')]: b, [frenchScoreId('c')]: c, [frenchScoreId('dis')]: dis,
    [frenchScoreId('expression')]: e, ...(short ? { [frenchShortId('expression')]: 1 } : {}),
  });

  it('applies when the content adds up to the printed threshold or less', () => {
    expect(lowerScaleActive(criteria, expression, place(3, 3, 2, 0, 0))).toBe(true);
    expect(lowerScaleActive(criteria, expression, place(3, 3, 3, 0, 0))).toBe(false);
  });

  it('pays expression on the lower scale only, and never above it', () => {
    expect(frenchMarks(card, place(2, 2, 2, 1, 5))).toBe(12);
    expect(frenchMarks(card, place(2, 2, 2, 1, 10))).toBe(7);
    expect(frenchMarks(card, place(3, 4, 4, 2, 10))).toBe(23);
  });

  it('applies when the student says the answer is short, whatever the content', () => {
    expect(frenchMarks(card, place(3, 4, 4, 2, 10, true))).toBe(13);
    expect(frenchMarks(card, place(3, 4, 4, 2, 6, true))).toBe(19);
  });
});
