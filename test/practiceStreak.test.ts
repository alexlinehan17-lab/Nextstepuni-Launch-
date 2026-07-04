/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the Paper Trail practice-streak maths (feature B3): consecutive-day
 * runs, the "grace" anchor (a streak stays alive the morning after, before you
 * practise again), and gap handling.
 */
import { describe, it, expect } from 'vitest';
import { computeStreak, dayIndex, dayKey } from '../components/PaperTrail/streakStore';

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
});
