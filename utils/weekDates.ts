/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * One place for "what week is it" and "when was this student last active".
 *
 * Five call sites used to answer these independently — two of them with
 * `now.getDate() - now.getDay() + 1`, which lands on NEXT Monday when run on a
 * Sunday, so the weekly export read 0 sessions for the whole school every
 * Sunday. A sixth parsed date keys with `new Date('YYYY-MM-DD')`, which is
 * UTC midnight, while every writer builds keys from LOCAL date parts.
 *
 * Rules for this codebase:
 *  - Date keys are 'YYYY-MM-DD' built from LOCAL getFullYear/getMonth/getDate
 *    (see subjectData.toDateKey). Parse them with `parseDateKey`, never with
 *    the bare Date constructor.
 *  - Weeks run Monday → Sunday.
 */

/** Local-midnight Date for a 'YYYY-MM-DD' key. The bare `new Date(key)`
 *  constructor parses ISO date-only strings as UTC, which shifts the day for
 *  every timezone east of Greenwich (Ireland, all summer). */
export function parseDateKey(key: string): Date {
  return new Date(`${key}T00:00:00`);
}

/** 'YYYY-MM-DD' for a Date, using local parts — matches every writer. */
export function toDateKey(d: Date): string {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
}

/**
 * Local midnight on the Monday of `date`'s week, optionally `weeksAgo` weeks
 * back. Sunday belongs to the week that just ended, not the one about to start.
 */
export function startOfWeek(date: Date, weeksAgo: number = 0): Date {
  const dow = date.getDay();                    // 0 = Sunday
  const mondayOffset = dow === 0 ? 6 : dow - 1;
  const monday = new Date(date);
  monday.setDate(date.getDate() - mondayOffset - weeksAgo * 7);
  monday.setHours(0, 0, 0, 0);
  return monday;
}

/**
 * The most recent date key with at least one completed block, or null.
 *
 * Deliberately derived from the completions map rather than from
 * `computeStreak(...).lastActiveDate` — that function returns TODAY whenever
 * the streak is 0 (timetableAlgorithm.ts: `lastActiveDate || todayKey`), which
 * would make every dormant student read "last active: today" and permanently
 * disable the at-risk and streak-broken alerts.
 *
 * Days whose array is empty are ignored: un-ticking the last block of a day
 * historically left the key behind, so an empty array is not a study day.
 */
export function lastActiveDateFrom(
  completions: Record<string, unknown> | null | undefined,
): string | null {
  if (!completions) return null;
  let latest: string | null = null;
  for (const [key, blocks] of Object.entries(completions)) {
    if (!Array.isArray(blocks) || blocks.length === 0) continue;
    if (latest === null || key > latest) latest = key;
  }
  return latest;
}

/** Count of distinct days with at least one completed block. */
export function activeDayCount(completions: Record<string, unknown> | null | undefined): number {
  if (!completions) return 0;
  return Object.values(completions).filter(b => Array.isArray(b) && b.length > 0).length;
}
