/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "Your desk, earned" — desk unlock thresholds + the pen-ink preference.
 */

import { beforeEach, describe, expect, it } from 'vitest';
import {
  GREEN_INK_HEX,
  GREEN_INK_STREAK,
  LAMP_STREAK,
  NAMEPLATE_SESSIONS,
  PLANT_STREAK,
  deskUnlocks,
  loadInk,
  saveInk,
} from '../components/ExaminersChair/desk';
import { type ChairState, type SessionResult } from '../components/ExaminersChair/store';

const baseState = (over?: Partial<ChairState>): ChairState => ({
  results: {},
  codex: [],
  codexOnCards: [],
  misses: {},
  codexReview: {},
  daily: { day: '', streak: 0, best: 0 },
  ...over,
});

const withStreak = (streak: number, best = streak): ChairState =>
  baseState({ daily: { day: '2026-7-7', streak, best } });

const withSessions = (n: number): ChairState => {
  const results: Record<string, SessionResult> = {};
  for (let i = 0; i < n; i++) {
    results[`s${i}`] = { sessionId: `s${i}`, agreement: 0.8, scripts: [], completedAt: i + 1, attempts: 1 };
  }
  return baseState({ results });
};

describe('deskUnlocks', () => {
  it('locks everything on a fresh state', () => {
    expect(deskUnlocks(baseState())).toEqual({ plant: false, greenInk: false, lamp: false, nameplate: false });
  });

  it('grows the plant at exactly a 3-day streak', () => {
    expect(deskUnlocks(withStreak(PLANT_STREAK - 1)).plant).toBe(false);
    expect(deskUnlocks(withStreak(PLANT_STREAK)).plant).toBe(true);
    // ...but nothing further yet
    const d = deskUnlocks(withStreak(PLANT_STREAK));
    expect(d.greenInk).toBe(false);
    expect(d.lamp).toBe(false);
  });

  it('unlocks the green ink at a 7-day streak and the lamp at 14', () => {
    expect(deskUnlocks(withStreak(GREEN_INK_STREAK - 1)).greenInk).toBe(false);
    const seven = deskUnlocks(withStreak(GREEN_INK_STREAK));
    expect(seven.greenInk).toBe(true);
    expect(seven.lamp).toBe(false);
    expect(deskUnlocks(withStreak(LAMP_STREAK - 1)).lamp).toBe(false);
    const fourteen = deskUnlocks(withStreak(LAMP_STREAK));
    expect(fourteen).toEqual({ plant: true, greenInk: true, lamp: true, nameplate: false });
  });

  it('never takes a streak unlock away — best streak counts after a break', () => {
    expect(deskUnlocks(withStreak(1, 14))).toEqual({ plant: true, greenInk: true, lamp: true, nameplate: false });
    expect(deskUnlocks(withStreak(2, 3)).plant).toBe(true);
  });

  it('awards the nameplate at 25 completed sessions, independent of streak', () => {
    expect(deskUnlocks(withSessions(NAMEPLATE_SESSIONS - 1)).nameplate).toBe(false);
    const d = deskUnlocks(withSessions(NAMEPLATE_SESSIONS));
    expect(d.nameplate).toBe(true);
    expect(d.plant).toBe(false); // sessions alone unlock nothing streak-gated
  });

  it('uses an examiner-plausible green that is NOT the app success token', () => {
    expect(GREEN_INK_HEX.toLowerCase()).toBe('#2f6b4f');
    expect(GREEN_INK_HEX.toLowerCase()).not.toBe('#3a8d5f');
  });
});

describe('ink preference (localStorage, per uid)', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('defaults to red when nothing is stored', () => {
    expect(loadInk(undefined)).toBe('red');
    expect(loadInk('u1')).toBe('red');
  });

  it('round-trips a saved choice per uid', () => {
    saveInk('u1', 'green');
    expect(loadInk('u1')).toBe('green');
    expect(loadInk('u2')).toBe('red'); // other uids untouched
    saveInk('u1', 'red');
    expect(loadInk('u1')).toBe('red');
  });

  it('keys anonymous users separately from signed-in ones', () => {
    saveInk(undefined, 'green');
    expect(loadInk(undefined)).toBe('green');
    expect(loadInk('u1')).toBe('red');
  });

  it('falls back to red on an unknown stored value', () => {
    localStorage.setItem('chair-ink:u1', 'sepia');
    expect(loadInk('u1')).toBe('red');
  });
});
