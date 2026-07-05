/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the Paper Trail practice-streak maths (feature B3): consecutive-day
 * runs, the "grace" anchor (a streak stays alive the morning after, before you
 * practise again), and gap handling.
 */
import { describe, it, expect } from 'vitest';
import { computeStreak, dayIndex, dayKey, indexToKey, frozenBridge } from '../components/PaperTrail/streakStore';

const T = dayIndex('2026-07-04'); // an arbitrary "today"

describe('Paper Trail — practice streak', () => {
  it('counts a consecutive run ending today', () => {
    expect(computeStreak([T - 2, T - 1, T], T)).toEqual({ current: 3, longest: 3 });
  });

  it('keeps the streak alive the day after (anchor falls back to yesterday)', () => {
    // Practised through yesterday but not yet today → still a live 2-day streak.
    expect(computeStreak([T - 2, T - 1], T).current).toBe(2);
  });

  it('breaks the current streak after a full missed day', () => {
    // Last practised two days ago → current streak is 0, but longest is retained.
    const s = computeStreak([T - 5, T - 4, T - 3, T - 2], T);
    expect(s.current).toBe(0);
    expect(s.longest).toBe(4);
  });

  it('reports the longest run even when it is not the current one', () => {
    const s = computeStreak([T - 10, T - 9, T - 8, T - 7, T - 1, T], T);
    expect(s.longest).toBe(4);
    expect(s.current).toBe(2);
  });

  it('is robust to unsorted and duplicate day indices', () => {
    expect(computeStreak([T, T - 1, T, T - 2, T - 1], T)).toEqual({ current: 3, longest: 3 });
  });

  it('dayKey/dayIndex round-trip consecutive local days to adjacent integers', () => {
    const a = dayIndex(dayKey(Date.UTC(2026, 6, 4, 12)));
    const b = dayIndex(dayKey(Date.UTC(2026, 6, 5, 12)));
    expect(b - a).toBe(1);
  });

  it('indexToKey inverts dayIndex', () => {
    for (const key of ['2026-06-05', '2026-01-01', '2025-12-31']) {
      expect(indexToKey(dayIndex(key))).toBe(key);
    }
  });
});

describe('Paper Trail — streak freezes', () => {
  it('freezes a single missed day when a freeze is available', () => {
    // Practised up to T-2, missed T-1, one freeze available → freeze T-1.
    expect(frozenBridge([T - 3, T - 2], [], 1, T)).toEqual([T - 1]);
  });

  it('does nothing when already active today or yesterday (grace)', () => {
    expect(frozenBridge([T - 1, T], [], 2, T)).toEqual([]); // active today
    expect(frozenBridge([T - 1], [], 2, T)).toEqual([]); // yesterday = grace
  });

  it('will not partially bridge — preserves freezes if the gap is too big', () => {
    // Missed T-2 and T-1 (gap of 2) but only 1 freeze → break, keep the freeze.
    expect(frozenBridge([T - 3], [], 1, T)).toEqual([]);
    // With 2 freezes it bridges both.
    expect(frozenBridge([T - 3], [], 2, T)).toEqual([T - 2, T - 1]);
  });

  it('a frozen streak stays continuous under computeStreak', () => {
    // Active T-3, frozen T-2 and T-1, active T → one 4-day run.
    expect(computeStreak([T - 3, T - 2, T - 1, T], T).current).toBe(4);
  });
});
