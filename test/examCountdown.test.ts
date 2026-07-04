/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the Paper Trail exam-date store (feature A3): round-tripping a date,
 * rejecting malformed input, and the pure days-to-go maths (today = 0, past is
 * negative), which drives the countdown and weekly-pace planner.
 */
import { describe, it, expect, beforeEach } from 'vitest';
import { getExamDate, setExamDate, clearExamDate, daysUntil } from '../components/PaperTrail/examDateStore';
import { dayKey } from '../components/PaperTrail/streakStore';

const NOON = (y: number, m: number, d: number) => Date.UTC(y, m - 1, d, 12);

describe('Paper Trail — exam countdown', () => {
  beforeEach(() => localStorage.clear());

  it('round-trips a valid ISO date per uid and clears it', () => {
    setExamDate('u1', '2026-06-05');
    expect(getExamDate('u1')).toBe('2026-06-05');
    expect(getExamDate('u2')).toBeNull();
    clearExamDate('u1');
    expect(getExamDate('u1')).toBeNull();
  });

  it('rejects malformed dates', () => {
    setExamDate('u1', 'not-a-date');
    expect(getExamDate('u1')).toBeNull();
  });

  it('counts whole days: today is 0, future positive, past negative', () => {
    const today = dayKey(NOON(2026, 6, 1));
    expect(daysUntil(today, NOON(2026, 6, 1))).toBe(0);
    expect(daysUntil('2026-06-05', NOON(2026, 6, 1))).toBe(4);
    expect(daysUntil('2026-05-30', NOON(2026, 6, 1))).toBe(-2);
  });
});
