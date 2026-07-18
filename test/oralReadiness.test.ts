/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the Oral Exam Trainer readiness-delta helpers (feature F8): the light
 * 1/3/8/21-day re-record schedule and the take-metadata history. Privacy
 * invariant pinned in code review: these helpers store timestamps and blobs
 * on-device only — nothing here touches the network or Firestore.
 */
import { describe, it, expect } from 'vitest';
import {
  DAY_MS,
  MAX_TAKES_PER_PART,
  RERECORD_INTERVALS,
  appendTake,
  daysAgoLabel,
  daysBetween,
  intervalDaysFor,
  isDueForRerecord,
} from '../components/oralReadiness';

const NOW = 1_750_000_000_000;

describe('Oral trainer — spaced re-record schedule', () => {
  it('mirrors the light interval ladder 1/3/8/21', () => {
    expect(RERECORD_INTERVALS).toEqual([1, 3, 8, 21]);
    expect(intervalDaysFor(1)).toBe(1);
    expect(intervalDaysFor(2)).toBe(3);
    expect(intervalDaysFor(3)).toBe(8);
    expect(intervalDaysFor(4)).toBe(21);
  });

  it('caps at the top rung for long practice histories', () => {
    expect(intervalDaysFor(5)).toBe(21);
    expect(intervalDaysFor(50)).toBe(21);
  });

  it('a never-recorded part is not "due" — there is nothing to re-record', () => {
    expect(isDueForRerecord(undefined, 0, NOW)).toBe(false);
  });

  it('a part recorded just now is not due', () => {
    expect(isDueForRerecord(NOW, 1, NOW)).toBe(false);
    expect(isDueForRerecord(NOW - DAY_MS / 2, 1, NOW)).toBe(false);
  });

  it('becomes due once the last recording is older than its interval', () => {
    // 1 take → 1-day interval
    expect(isDueForRerecord(NOW - 1.5 * DAY_MS, 1, NOW)).toBe(true);
    // 2 takes → 3-day interval
    expect(isDueForRerecord(NOW - 2 * DAY_MS, 2, NOW)).toBe(false);
    expect(isDueForRerecord(NOW - 4 * DAY_MS, 2, NOW)).toBe(true);
    // 4+ takes → 21-day interval
    expect(isDueForRerecord(NOW - 20 * DAY_MS, 4, NOW)).toBe(false);
    expect(isDueForRerecord(NOW - 22 * DAY_MS, 6, NOW)).toBe(true);
  });

  it('daysBetween rounds to whole days and never goes negative', () => {
    expect(daysBetween(NOW, NOW)).toBe(0);
    expect(daysBetween(NOW - 3 * DAY_MS, NOW)).toBe(3);
    expect(daysBetween(NOW - 2.6 * DAY_MS, NOW)).toBe(3);
    expect(daysBetween(NOW + DAY_MS, NOW)).toBe(0);
  });

  it('daysAgoLabel reads calmly: today / yesterday / N days ago', () => {
    expect(daysAgoLabel(NOW, NOW)).toBe('today');
    expect(daysAgoLabel(NOW - DAY_MS, NOW)).toBe('yesterday');
    expect(daysAgoLabel(NOW - 8 * DAY_MS, NOW)).toBe('8 days ago');
  });
});

describe('Oral trainer — take history', () => {
  it('keeps the FULL take history so the 1/3/8/21 ladder can be walked', () => {
    // Only audio blobs are capped at 2; the lightweight metadata history is not,
    // otherwise intervalDaysFor never sees takeCount >= 3 and the 8/21-day rungs
    // are unreachable.
    expect(MAX_TAKES_PER_PART).toBe(2);
    let meta: Record<string, { at: number; durationMs: number }[]> = {};
    meta = appendTake(meta, 'comhra', { at: 1, durationMs: 10_000 });
    meta = appendTake(meta, 'comhra', { at: 2, durationMs: 11_000 });
    meta = appendTake(meta, 'comhra', { at: 3, durationMs: 12_000 });
    meta = appendTake(meta, 'comhra', { at: 4, durationMs: 13_000 });
    expect(meta.comhra.map(t => t.at)).toEqual([1, 2, 3, 4]);
    // Take count now reaches the top rungs of the ladder.
    expect(intervalDaysFor(meta.comhra.length)).toBe(21);
  });

  it('is pure and keeps other parts untouched', () => {
    const before = { comhra: [{ at: 1, durationMs: 5_000 }] };
    const after = appendTake(before, 'failtiu', { at: 9, durationMs: 4_000 });
    expect(before).toEqual({ comhra: [{ at: 1, durationMs: 5_000 }] });
    expect(after.comhra).toEqual(before.comhra);
    expect(after.failtiu.map(t => t.at)).toEqual([9]);
  });
});
