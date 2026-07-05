/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the Paper Trail FSRS scheduler (feature E1). We pin the qualitative
 * behaviour the student relies on rather than exact weights: recall grows the
 * interval, a lapse collapses it, Easy ≥ Good ≥ Hard, difficulty stays in range,
 * retrievability decays with time, and a lower target retention spaces further.
 */
import { describe, it, expect } from 'vitest';
import {
  fsrsInit,
  fsrsNext,
  intervalFor,
  retrievability,
  DEFAULT_RETENTION,
  type FsrsGrade,
} from '../components/PaperTrail/fsrs';

describe('Paper Trail — FSRS scheduler', () => {
  it('init: Easy ≥ Good ≥ Hard first intervals, all ≥ 1 day', () => {
    const hard = fsrsInit(2).intervalDays;
    const good = fsrsInit(3).intervalDays;
    const easy = fsrsInit(4).intervalDays;
    expect(easy).toBeGreaterThanOrEqual(good);
    expect(good).toBeGreaterThanOrEqual(hard);
    expect(hard).toBeGreaterThanOrEqual(1);
  });

  it('recall grows stability and interval across spaced reviews', () => {
    let s = fsrsInit(3); // Good
    const first = s.intervalDays;
    // Review each time right at the scheduled interval, always "Good".
    s = fsrsNext(s, 3, first, DEFAULT_RETENTION);
    const second = s.intervalDays;
    s = fsrsNext(s, 3, second, DEFAULT_RETENTION);
    const third = s.intervalDays;
    expect(second).toBeGreaterThan(first);
    expect(third).toBeGreaterThan(second);
  });

  it('a lapse (Again) collapses the interval and drops stability', () => {
    let s = fsrsInit(3);
    s = fsrsNext(s, 3, s.intervalDays, DEFAULT_RETENTION);
    const matureStability = s.stability;
    const lapsed = fsrsNext(s, 1, s.intervalDays, DEFAULT_RETENTION);
    expect(lapsed.stability).toBeLessThan(matureStability);
    expect(lapsed.intervalDays).toBeLessThanOrEqual(s.intervalDays);
  });

  it('on a mature card, Easy ≥ Good ≥ Hard intervals', () => {
    let s = fsrsInit(3);
    s = fsrsNext(s, 3, s.intervalDays, DEFAULT_RETENTION);
    const t = s.intervalDays;
    const hard = fsrsNext(s, 2, t, DEFAULT_RETENTION).intervalDays;
    const good = fsrsNext(s, 3, t, DEFAULT_RETENTION).intervalDays;
    const easy = fsrsNext(s, 4, t, DEFAULT_RETENTION).intervalDays;
    expect(easy).toBeGreaterThanOrEqual(good);
    expect(good).toBeGreaterThanOrEqual(hard);
  });

  it('difficulty stays within [1,10] under repeated Again and repeated Easy', () => {
    let hardest = fsrsInit(1);
    for (let i = 0; i < 15; i++) hardest = fsrsNext(hardest, 1, 1, DEFAULT_RETENTION);
    expect(hardest.difficulty).toBeGreaterThanOrEqual(1);
    expect(hardest.difficulty).toBeLessThanOrEqual(10);
    let easiest = fsrsInit(4);
    for (let i = 0; i < 15; i++) easiest = fsrsNext(easiest, 4, easiest.intervalDays, DEFAULT_RETENTION);
    expect(easiest.difficulty).toBeGreaterThanOrEqual(1);
    expect(easiest.difficulty).toBeLessThanOrEqual(10);
  });

  it('retrievability decays: R(0)=1 and R(stability)≈0.9', () => {
    expect(retrievability(0, 10)).toBeCloseTo(1, 5);
    expect(retrievability(10, 10)).toBeCloseTo(0.9, 2);
    expect(retrievability(40, 10)).toBeLessThan(retrievability(10, 10));
  });

  it('a lower target retention schedules further out', () => {
    const s = 20;
    expect(intervalFor(s, 0.85)).toBeGreaterThan(intervalFor(s, 0.95));
  });

  it('every grade yields at least a 1-day interval', () => {
    for (const g of [1, 2, 3, 4] as FsrsGrade[]) {
      expect(fsrsInit(g).intervalDays).toBeGreaterThanOrEqual(1);
    }
  });
});
