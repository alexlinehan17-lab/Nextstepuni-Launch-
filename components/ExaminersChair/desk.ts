/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "Your desk, earned" — cosmetic desk unlocks tied to the Daily Mark
 * calibration streak. Pure logic over ChairState (read-only) plus a tiny
 * localStorage preference for the chosen examiner-pen ink, per uid — same
 * persistence shape as ./store. Rendering lives in index.tsx (home view).
 */

import { type ChairState } from './store';

// ── unlock thresholds ──

export const PLANT_STREAK = 3;
export const GREEN_INK_STREAK = 7;
export const LAMP_STREAK = 14;
export const NAMEPLATE_SESSIONS = 25;

/** Deep green examiner ink — an alternative marking-pen colour unlocked at a
 * 7-day streak. Examiner-plausible; deliberately NOT the app success token. */
export const GREEN_INK_HEX = '#2F6B4F';

export interface DeskUnlocks {
  /** 3-day streak — a small desk plant beside the Daily Mark card. */
  plant: boolean;
  /** 7-day streak — the deep-green pen ink becomes selectable. */
  greenInk: boolean;
  /** 14-day streak — a brass desk lamp on the home header. */
  lamp: boolean;
  /** 25 completed sessions — the "Senior Marker" nameplate. */
  nameplate: boolean;
}

/** What the student's desk has earned. Streak unlocks are judged against the
 * best streak ever reached, so a broken streak never takes the plant away. */
export function deskUnlocks(state: ChairState): DeskUnlocks {
  const streak = Math.max(state.daily.streak, state.daily.best);
  const sessions = Object.keys(state.results).length;
  return {
    plant: streak >= PLANT_STREAK,
    greenInk: streak >= GREEN_INK_STREAK,
    lamp: streak >= LAMP_STREAK,
    nameplate: sessions >= NAMEPLATE_SESSIONS,
  };
}

// ── ink preference (local-only, per uid) ──

export type ChairInk = 'red' | 'green';

const inkKey = (uid?: string) => `chair-ink:${uid || 'anon'}`;

/** The chosen pen ink — defaults to the examiner's red on anything unknown. */
export function loadInk(uid?: string): ChairInk {
  try {
    return localStorage.getItem(inkKey(uid)) === 'green' ? 'green' : 'red';
  } catch {
    return 'red';
  }
}

export function saveInk(uid: string | undefined, ink: ChairInk): void {
  try {
    localStorage.setItem(inkKey(uid), ink);
  } catch {
    /* quota / private mode — degrade silently */
  }
}
