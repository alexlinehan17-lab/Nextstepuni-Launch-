/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — exam-date store (feature A3). The student sets their own exam
 * (or first-paper) date; we never hardcode an SEC timetable we can't verify.
 * One ISO date per uid in localStorage, plus a pure days-to-go helper.
 */

import { dayIndex, dayKey } from './streakStore';

const PREFIX = 'pt:examdate:';
const blobKey = (uid?: string) => PREFIX + (uid || 'anon');
const ISO = /^\d{4}-\d{2}-\d{2}$/;

export function getExamDate(uid?: string): string | null {
  try {
    const v = localStorage.getItem(blobKey(uid));
    return v && ISO.test(v) ? v : null;
  } catch {
    return null;
  }
}

export function setExamDate(uid: string | undefined, iso: string): void {
  try {
    if (ISO.test(iso)) localStorage.setItem(blobKey(uid), iso);
  } catch {
    /* quota / private mode — degrade silently */
  }
}

export function clearExamDate(uid?: string): void {
  try {
    localStorage.removeItem(blobKey(uid));
  } catch {
    /* ignore */
  }
}

/** Whole days from `now` (local) to an ISO exam date. 0 = today, negative =
 *  already passed. Pure. */
export function daysUntil(iso: string, now: number): number {
  if (!ISO.test(iso)) return NaN;
  return dayIndex(iso) - dayIndex(dayKey(now));
}
