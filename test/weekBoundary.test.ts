/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Week boundaries and date-key parsing.
 *
 * Two bug classes are locked here:
 *  1. `now.getDate() - now.getDay() + 1` resolves to NEXT Monday on a Sunday,
 *     so every attendance export run on a Sunday read 0 sessions this week for
 *     the whole school.
 *  2. `new Date('YYYY-MM-DD')` parses as UTC midnight while every writer builds
 *     keys from LOCAL date parts — an off-by-one for the whole Irish summer.
 */
import { describe, it, expect } from 'vitest';
import { startOfWeek, parseDateKey, toDateKey, lastActiveDateFrom, activeDayCount } from '../utils/weekDates';
import { getSessionsInWeek, getTotalMinutes, getSessionCount } from '../components/gc/gcUtils';

describe('startOfWeek', () => {
  it('returns the Monday that has just passed when run on a Sunday', () => {
    // 2026-07-26 is a Sunday. Its week started Monday 2026-07-20 — NOT the
    // 27th, which is tomorrow.
    expect(toDateKey(startOfWeek(new Date('2026-07-26T12:00:00')))).toBe('2026-07-20');
  });

  it('returns the same day when run on a Monday', () => {
    expect(toDateKey(startOfWeek(new Date('2026-07-27T12:00:00')))).toBe('2026-07-27');
  });

  it('agrees with the old formula for Monday through Saturday', () => {
    // The fix must be a no-op for six days out of seven.
    for (let day = 20; day <= 25; day++) {
      const d = new Date(`2026-07-${day}T12:00:00`);
      const old = new Date(d);
      old.setDate(d.getDate() - d.getDay() + 1);
      expect(toDateKey(startOfWeek(d))).toBe(toDateKey(old));
    }
  });

  it('steps back whole weeks', () => {
    expect(toDateKey(startOfWeek(new Date('2026-07-26T12:00:00'), 1))).toBe('2026-07-13');
  });
});

describe('parseDateKey', () => {
  it('parses as local midnight, not UTC', () => {
    const d = parseDateKey('2026-07-15');
    expect(d.getFullYear()).toBe(2026);
    expect(d.getMonth()).toBe(6);
    expect(d.getDate()).toBe(15);   // bare `new Date('2026-07-15')` shifts this
    expect(d.getHours()).toBe(0);
  });

  it('round-trips with toDateKey', () => {
    expect(toDateKey(parseDateKey('2026-02-29'.replace('29', '28')))).toBe('2026-02-28');
  });
});

describe('lastActiveDateFrom / activeDayCount', () => {
  it('picks the most recent day with real activity', () => {
    expect(lastActiveDateFrom({ '2026-07-01': ['b1'], '2026-07-09': ['b2'], '2026-07-05': ['b3'] })).toBe('2026-07-09');
  });

  it('ignores days left behind with an empty array', () => {
    // The un-tick bug stranded empty day-keys; an empty day is not a study day.
    expect(lastActiveDateFrom({ '2026-07-01': ['b1'], '2026-07-09': [] })).toBe('2026-07-01');
    expect(activeDayCount({ '2026-07-01': ['b1'], '2026-07-09': [] })).toBe(1);
  });

  it('returns null rather than today for a student who never studied', () => {
    expect(lastActiveDateFrom({})).toBeNull();
    expect(lastActiveDateFrom(null)).toBeNull();
  });
});

describe('attendance export helpers', () => {
  const mondayOfThisWeek = toDateKey(startOfWeek(new Date()));
  const lastWeek = toDateKey(startOfWeek(new Date(), 1));

  it('counts this week even when today is a Sunday', () => {
    const completions = { [mondayOfThisWeek]: ['b1', 'b2'] };
    expect(getSessionsInWeek(completions, 0)).toBe(1);
    expect(getSessionsInWeek(completions, 1)).toBe(0);
  });

  it('separates last week from this week', () => {
    expect(getSessionsInWeek({ [lastWeek]: ['b1'] }, 1)).toBe(1);
    expect(getSessionsInWeek({ [lastWeek]: ['b1'] }, 0)).toBe(0);
  });

  it('uses the student\'s own block length, not a hardcoded 45', () => {
    const completions = { '2026-07-01': ['b1', 'b2'], '2026-07-02': ['b3'] };
    expect(getTotalMinutes(completions, 60)).toBe(180);
    expect(getTotalMinutes(completions)).toBe(135);   // default stays 45
  });

  it('does not count emptied days as sessions', () => {
    expect(getSessionCount({ '2026-07-01': ['b1'], '2026-07-02': [] })).toBe(1);
  });
});
