/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the Paper Trail handwriting-speed calibrator core (feature F4): the
 * localStorage round-trip is per-uid and tolerant of junk, the WPM calculation
 * rejects implausible timings, and the personalisation scale clamps to the
 * 0.75×–1.5× band.
 */
import { describe, it, expect, beforeEach } from 'vitest';
import {
  CALIBRATION_PASSAGE,
  CALIBRATION_WORD_COUNT,
  MIN_DRILL_SECONDS,
  STANDARD_WPM,
  clearCalibration,
  computeWpm,
  loadCalibration,
  paceScale,
  saveCalibration,
  type WpmCalibration,
} from '../components/PaperTrail/wpmStore';

const cal = (wpm: number): WpmCalibration => ({ wpm, words: 40, seconds: Math.round((40 / wpm) * 60), ts: 1_750_000_000_000 });

describe('Paper Trail — handwriting-speed store', () => {
  beforeEach(() => localStorage.clear());

  it('the drill passage is the promised ~40 words', () => {
    expect(CALIBRATION_WORD_COUNT).toBe(40);
    expect(CALIBRATION_PASSAGE.trim().split(/\s+/)).toHaveLength(CALIBRATION_WORD_COUNT);
  });

  it('round-trips a calibration per uid under pt:wpm:<uid>', () => {
    saveCalibration('u1', cal(14));
    expect(localStorage.getItem('pt:wpm:u1')).toBeTruthy();
    expect(loadCalibration('u1')?.wpm).toBe(14);
    // Other students on the same device are untouched.
    expect(loadCalibration('u2')).toBeNull();
    // No uid falls back to the shared anon slot.
    saveCalibration(undefined, cal(22));
    expect(localStorage.getItem('pt:wpm:anon')).toBeTruthy();
    expect(loadCalibration(undefined)?.wpm).toBe(22);
    expect(loadCalibration('u1')?.wpm).toBe(14);
  });

  it('reads a pre-seeded record and survives junk', () => {
    localStorage.setItem('pt:wpm:u1', JSON.stringify({ wpm: 17, words: 40, seconds: 141, ts: 1 }));
    expect(loadCalibration('u1')?.wpm).toBe(17);
    localStorage.setItem('pt:wpm:u2', 'not json');
    expect(loadCalibration('u2')).toBeNull();
    localStorage.setItem('pt:wpm:u3', JSON.stringify({ wpm: -5 }));
    expect(loadCalibration('u3')).toBeNull();
  });

  it('clearCalibration removes only that uid', () => {
    saveCalibration('u1', cal(14));
    saveCalibration('u2', cal(25));
    clearCalibration('u1');
    expect(loadCalibration('u1')).toBeNull();
    expect(loadCalibration('u2')?.wpm).toBe(25);
  });
});

describe('Paper Trail — WPM calculation', () => {
  it('computes words per minute from a timed copy', () => {
    expect(computeWpm(40, 120)).toBe(20); // 40 words in 2 min
    expect(computeWpm(40, 160)).toBe(15);
  });

  it('rejects implausible timings', () => {
    expect(computeWpm(40, MIN_DRILL_SECONDS - 1)).toBeNull(); // accidental double-tap
    expect(computeWpm(40, 0)).toBeNull();
    expect(computeWpm(0, 120)).toBeNull();
    expect(computeWpm(40, Number.NaN)).toBeNull();
  });
});

describe('Paper Trail — personalisation scale clamp', () => {
  it('is 1 with no calibration', () => {
    expect(paceScale(null)).toBe(1);
    expect(paceScale(undefined)).toBe(1);
    expect(paceScale({ ...cal(10), wpm: 0 })).toBe(1); // corrupt record
  });

  it('scales standard ÷ student inside the band', () => {
    expect(paceScale(cal(STANDARD_WPM))).toBe(1);
    expect(paceScale(cal(16))).toBeCloseTo(1.25); // slower writer → more time
    expect(paceScale(cal(25))).toBeCloseTo(0.8); // faster writer → less time
  });

  it('clamps to 0.75×–1.5× at the extremes', () => {
    expect(paceScale(cal(5))).toBe(1.5); // very slow → capped, budgets stay sane
    expect(paceScale(cal(100))).toBe(0.75); // very fast → floored
  });
});
