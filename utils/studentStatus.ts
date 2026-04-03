/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type GCStudentFullData, type StudentStatus } from '../components/gc/gcTypes';
import { type TimetableCompletions } from '../components/subjectData';
import { type CourseData } from '../components/Library';
import { type UserProgress } from '../types';

// ─── Helpers ───────────────────────────────────────────────────────────────

const DAY_MS = 1000 * 60 * 60 * 24;

function fmtDate(d: Date): string {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

/** Days since the most recent study session (timetable block). Infinity if never. */
function daysSinceLastSession(tc: TimetableCompletions | null): number {
  if (!tc) return Infinity;
  const now = new Date();
  let latest = '';
  for (const [date, blocks] of Object.entries(tc)) {
    if (Array.isArray(blocks) && blocks.length > 0 && date > latest) {
      latest = date;
    }
  }
  if (!latest) return Infinity;
  return Math.floor((now.getTime() - new Date(latest + 'T00:00:00').getTime()) / DAY_MS);
}

/**
 * Count consecutive COMPLETED weeks (Mon-Sun) with zero activity,
 * going backwards from the most recently completed week.
 * Skips the current partial week.
 */
function consecutiveZeroWeeks(tc: TimetableCompletions | null): number {
  if (!tc) return 0;

  const activeDates = new Set<string>();
  for (const [date, blocks] of Object.entries(tc)) {
    if (Array.isArray(blocks) && blocks.length > 0) activeDates.add(date);
  }
  if (activeDates.size === 0) return 0;

  const now = new Date();
  const dow = now.getDay();
  const mondayOffset = dow === 0 ? 6 : dow - 1;
  const thisMonday = new Date(now);
  thisMonday.setDate(now.getDate() - mondayOffset);
  thisMonday.setHours(0, 0, 0, 0);

  let count = 0;
  for (let w = 1; w <= 8; w++) {
    const weekMon = new Date(thisMonday);
    weekMon.setDate(thisMonday.getDate() - w * 7);
    let active = false;
    for (let d = 0; d < 7; d++) {
      const day = new Date(weekMon);
      day.setDate(weekMon.getDate() + d);
      if (activeDates.has(fmtDate(day))) { active = true; break; }
    }
    if (!active) count++;
    else break;
  }
  return count;
}

/**
 * Count consecutive weeks WITH activity, including the current partial week.
 */
function consecutiveActiveWeeks(tc: TimetableCompletions | null): number {
  if (!tc) return 0;

  const activeDates = new Set<string>();
  for (const [date, blocks] of Object.entries(tc)) {
    if (Array.isArray(blocks) && blocks.length > 0) activeDates.add(date);
  }
  if (activeDates.size === 0) return 0;

  const now = new Date();
  const dow = now.getDay();
  const mondayOffset = dow === 0 ? 6 : dow - 1;
  const thisMonday = new Date(now);
  thisMonday.setDate(now.getDate() - mondayOffset);
  thisMonday.setHours(0, 0, 0, 0);

  let count = 0;
  for (let w = 0; w <= 8; w++) {
    const weekMon = new Date(thisMonday);
    weekMon.setDate(thisMonday.getDate() - w * 7);
    const daysToCheck = w === 0 ? (dow === 0 ? 7 : dow) : 7;
    let active = false;
    for (let d = 0; d < daysToCheck; d++) {
      const day = new Date(weekMon);
      day.setDate(weekMon.getDate() + d);
      if (activeDates.has(fmtDate(day))) { active = true; break; }
    }
    if (active) count++;
    else break;
  }
  return count;
}

function completedModules(progress: UserProgress, allCourses: CourseData[]): number {
  return allCourses.filter(c => {
    const p = progress[c.id];
    return p && typeof p.unlockedSection === 'number' && c.sectionsCount > 0 && p.unlockedSection >= c.sectionsCount;
  }).length;
}

// ─── Main Classification ────────────────────────────────────────────────────

export function getStudentStatus(student: GCStudentFullData, allCourses: CourseData[]): StudentStatus {
  const now = new Date();

  // ── 1. NEW — account created within last 7 days ──
  const createdAt = student.subjectProfile?.createdAt;
  if (!createdAt) return 'new';
  const daysSinceSignup = Math.floor((now.getTime() - new Date(createdAt).getTime()) / DAY_MS);
  if (daysSinceSignup <= 7) return 'new';

  // ── Compute signals ──
  const daysSinceLast = daysSinceLastSession(student.timetableCompletions);
  const hasEverLogged = daysSinceLast !== Infinity;
  const curStreak = student.streak?.currentStreak ?? 0;
  const longStreak = student.streak?.longestStreak ?? 0;
  const lastActive = student.streak?.lastActiveDate;
  const daysSinceActive = lastActive
    ? Math.floor((now.getTime() - new Date(lastActive + 'T00:00:00').getTime()) / DAY_MS)
    : Infinity;
  const zeroWeeks = consecutiveZeroWeeks(student.timetableCompletions);

  // ── 2. INACTIVE — past 7 days but never logged a session ──
  if (!hasEverLogged) return 'inactive';

  // ── 3. AT RISK ──
  if (
    daysSinceLast >= 15 ||
    (longStreak >= 7 && curStreak === 0 && daysSinceActive >= 10) ||
    zeroWeeks >= 3
  ) return 'at-risk';

  // ── 4. DRIFTING ──
  if (
    (daysSinceLast >= 8 && daysSinceLast <= 14) ||
    (longStreak >= 5 && curStreak === 0 && daysSinceActive <= 14) ||
    zeroWeeks === 2
  ) return 'drifting';

  // ── 5. THRIVING ──
  if (daysSinceLast <= 7) {
    if (
      curStreak >= 5 ||
      completedModules(student.progress, allCourses) >= 3 ||
      consecutiveActiveWeeks(student.timetableCompletions) >= 3
    ) return 'thriving';
  }

  // ── 6. ACTIVE — default with recent session ──
  if (daysSinceLast <= 7) return 'active';

  // Fallback
  return 'active';
}

/** Human-readable reasons for at-risk or drifting status. */
export function getStatusReasons(student: GCStudentFullData, allCourses: CourseData[]): string[] {
  const status = getStudentStatus(student, allCourses);
  const reasons: string[] = [];
  if (status !== 'at-risk' && status !== 'drifting') return reasons;

  const now = new Date();
  const daysSinceLast = daysSinceLastSession(student.timetableCompletions);
  const curStreak = student.streak?.currentStreak ?? 0;
  const longStreak = student.streak?.longestStreak ?? 0;
  const lastActive = student.streak?.lastActiveDate;
  const daysSinceActive = lastActive
    ? Math.floor((now.getTime() - new Date(lastActive + 'T00:00:00').getTime()) / DAY_MS)
    : Infinity;
  const zeroWeeks = consecutiveZeroWeeks(student.timetableCompletions);

  if (status === 'at-risk') {
    if (daysSinceLast >= 15) reasons.push(`No study sessions in ${daysSinceLast} days`);
    if (longStreak >= 7 && curStreak === 0 && daysSinceActive >= 10)
      reasons.push(`${longStreak}-day streak broke ${daysSinceActive} days ago with no recovery`);
    if (zeroWeeks >= 3) reasons.push(`Zero activity for ${zeroWeeks} consecutive weeks`);
  }

  if (status === 'drifting') {
    if (daysSinceLast >= 8 && daysSinceLast <= 14) reasons.push(`No study sessions in ${daysSinceLast} days`);
    if (longStreak >= 5 && curStreak === 0 && daysSinceActive <= 14)
      reasons.push(`${longStreak}-day streak broke ${daysSinceActive} days ago`);
    if (zeroWeeks === 2) reasons.push('Zero activity for 2 consecutive weeks');
  }

  return reasons;
}

/** Badge config for each status — colours, label. */
export const STATUS_CONFIG: Record<StudentStatus, {
  label: string;
  bg: string;
  text: string;
  darkBgClass: string;
  darkTextClass: string;
}> = {
  'new':      { label: 'New',      bg: '#E5E7EB', text: '#4B5563', darkBgClass: 'dark:!bg-zinc-700/40',     darkTextClass: 'dark:!text-zinc-300' },
  'at-risk':  { label: 'At Risk',  bg: '#FEF3C7', text: '#92400E', darkBgClass: 'dark:!bg-amber-900/20',    darkTextClass: 'dark:!text-amber-400' },
  'drifting':  { label: 'Drifting',  bg: '#FFF7ED', text: '#9A3412', darkBgClass: 'dark:!bg-orange-900/20',   darkTextClass: 'dark:!text-orange-400' },
  'thriving':  { label: 'Thriving',  bg: '#ECFDF5', text: '#065F46', darkBgClass: 'dark:!bg-emerald-900/20',  darkTextClass: 'dark:!text-emerald-400' },
  'active':   { label: 'Active',   bg: '#F0FDFA', text: '#134E4A', darkBgClass: 'dark:!bg-teal-900/20',     darkTextClass: 'dark:!text-teal-400' },
  'inactive': { label: 'Inactive', bg: '#F3F4F6', text: '#6B7280', darkBgClass: 'dark:!bg-zinc-800/40',     darkTextClass: 'dark:!text-zinc-400' },
};
