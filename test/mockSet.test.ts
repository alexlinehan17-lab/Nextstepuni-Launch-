/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the Paper Trail mock-set builder core (feature B1): seeded selection is
 * deterministic, respects the requested length, never exceeds the pool, and
 * returns distinct questions.
 */
import { describe, it, expect } from 'vitest';
import { buildSet } from '../components/PaperTrail/mockSetStore';
import { type TopicSibling } from '../components/PaperTrail/topics';

const pool: TopicSibling[] = Array.from({ length: 20 }, (_, i) => ({
  subjectId: 'business', level: 'higher', lang: 'ev', year: 2000 + i, fileid: `f${i}`, paperKey: 'p1', n: String(i + 1),
}));
const key = (q: TopicSibling) => `${q.year}-${q.n}`;

describe('Paper Trail — mock-set selection', () => {
  it('is deterministic for a given seed', () => {
    const a = buildSet(pool, 10, 42).map(key);
    const b = buildSet(pool, 10, 42).map(key);
    expect(a).toEqual(b);
  });

  it('different seeds generally give different selections', () => {
    const a = buildSet(pool, 10, 1).map(key).join();
    const b = buildSet(pool, 10, 999).map(key).join();
    expect(a).not.toBe(b);
  });

  it('respects the requested length and returns distinct questions', () => {
    const set = buildSet(pool, 8, 7);
    expect(set).toHaveLength(8);
    expect(new Set(set.map(key)).size).toBe(8);
  });

  it('clamps to the pool size when asked for more than exists', () => {
    expect(buildSet(pool, 100, 3)).toHaveLength(20);
  });

  it('handles an empty pool', () => {
    expect(buildSet([], 5, 1)).toEqual([]);
  });
});
