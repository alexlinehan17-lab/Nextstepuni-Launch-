/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — handwriting-speed calibration store (feature F4). A one-time
 * self-timed drill: the student copies a fixed ~40-word passage BY HAND on
 * paper while the app times them, yielding a words-per-minute figure. That
 * figure personalises the time-budget guidance elsewhere in Paper Trail by
 * scaling the displayed writing-time targets (standard WPM ÷ student WPM),
 * clamped to a sane band so one odd calibration can't produce absurd budgets.
 *
 * Local-only: persisted per uid in localStorage (`pt:wpm:<uid>`), no network.
 */

/** The copy-this passage for the drill. Exactly 40 words — the word count is
 *  derived from the string so the two can never drift apart. */
export const CALIBRATION_PASSAGE =
  'Strong exam answers are built long before exam day. When you practise under real conditions, ' +
  'you learn how long each mark truly takes, where your timing slips, and how to leave enough ' +
  'space at the end for checking your work.';

export const CALIBRATION_WORD_COUNT = CALIBRATION_PASSAGE.trim().split(/\s+/).length;

/** Baseline handwriting speed the un-personalised budgets assume. A student
 *  writing at exactly this speed sees the standard (unscaled) guidance. */
export const STANDARD_WPM = 20;

/** Personalisation clamp — how far the guidance may stretch/shrink. */
export const MIN_SCALE = 0.75;
export const MAX_SCALE = 1.5;

/** A stop press shorter than this can't be a real handwriting pass of the
 *  passage — treat it as an accidental tap and don't record it. */
export const MIN_DRILL_SECONDS = 15;

export interface WpmCalibration {
  /** Measured handwriting speed, words per minute (rounded, ≥ 1). */
  wpm: number;
  /** Words in the drill passage at calibration time. */
  words: number;
  /** How long the drill took, seconds. */
  seconds: number;
  /** When the calibration was taken (ms epoch). */
  ts: number;
}

const key = (uid?: string) => `pt:wpm:${uid || 'anon'}`;

// ─── pure calculations ──────────────────────────────────────

/** Words-per-minute from a timed copy. Null when the timing is implausible
 *  (too short to be a real pass, or a non-positive duration). */
export function computeWpm(words: number, seconds: number): number | null {
  if (!Number.isFinite(words) || !Number.isFinite(seconds)) return null;
  if (words <= 0 || seconds < MIN_DRILL_SECONDS) return null;
  return Math.max(1, Math.round((words / seconds) * 60));
}

/** Scale factor for displayed writing-time guidance: standard ÷ student,
 *  clamped to [MIN_SCALE, MAX_SCALE]. A slower writer (< standard WPM) gets a
 *  factor > 1 — each question genuinely costs them more writing time. Returns
 *  1 (no personalisation) for missing/invalid input. */
export function paceScale(cal: WpmCalibration | null | undefined): number {
  if (!cal || !Number.isFinite(cal.wpm) || cal.wpm <= 0) return 1;
  return Math.min(MAX_SCALE, Math.max(MIN_SCALE, STANDARD_WPM / cal.wpm));
}

// ─── persistence (one calibration per uid) ──────────────────

export function loadCalibration(uid?: string): WpmCalibration | null {
  try {
    const raw = localStorage.getItem(key(uid));
    if (!raw) return null;
    const v = JSON.parse(raw) as WpmCalibration;
    if (typeof v?.wpm !== 'number' || !Number.isFinite(v.wpm) || v.wpm <= 0) return null;
    return v;
  } catch {
    return null;
  }
}

export function saveCalibration(uid: string | undefined, cal: WpmCalibration): void {
  try {
    localStorage.setItem(key(uid), JSON.stringify(cal));
  } catch {
    /* quota / private mode — degrade silently */
  }
}

export function clearCalibration(uid?: string): void {
  try {
    localStorage.removeItem(key(uid));
  } catch {
    /* ignore */
  }
}
