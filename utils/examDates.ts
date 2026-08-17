/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The default exam start date offered during onboarding.
 *
 * State exams begin on the first Wednesday of June. This was duplicated in
 * Onboarding.tsx and SubjectOnboarding.tsx, and both copies carried the same
 * two bugs (2026-08-17):
 *
 *   1. They pinned the CURRENT calendar year, so from the moment that June
 *      passed the default was a date in the past — and onboarding step 7
 *      gates "next" on `getDaysUntil(examDate) > 0`, so a student who left it
 *      untouched simply could not continue.
 *   2. They formatted via `toISOString()`, which converts to UTC first. Ireland
 *      is UTC+1 in June, so local midnight became 23:00 the previous day and
 *      the string came back one day early.
 */

/** The first Wednesday of June in `year`, as a local-midnight Date. */
function firstWednesdayOfJune(year: number): Date {
  const june1 = new Date(year, 5, 1);
  return new Date(year, 5, 1 + ((3 - june1.getDay() + 7) % 7));
}

/** `YYYY-MM-DD` from a Date's LOCAL fields — never via UTC. */
function toLocalISODate(date: Date): string {
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${date.getFullYear()}-${month}-${day}`;
}

/**
 * The next state-exam start date: the first Wednesday of June, rolling to the
 * following year once this year's sitting has started or passed.
 */
export function getDefaultExamDate(today: Date = new Date()): string {
  const midnight = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  let examStart = firstWednesdayOfJune(midnight.getFullYear());
  if (examStart <= midnight) examStart = firstWednesdayOfJune(midnight.getFullYear() + 1);
  return toLocalISODate(examStart);
}
