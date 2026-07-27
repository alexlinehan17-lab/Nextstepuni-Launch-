/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type CourseData } from '../Library';
import { type CategoryType } from '../KnowledgeTree';
import { type UserProgress } from '../../types';
import { getPointsForGrade, LC_SUBJECTS, JC_BANDS, type JCBand } from '../subjectData';
import { type TimetableCompletions } from '../subjectData';
import { type GCStudentFullData, type SubjectGapData } from './gcTypes';
import { getStudentStatus } from '../../utils/studentStatus';
import { filterCoursesForStudent } from '../../utils/courseVisibility';
import { startOfWeek, parseDateKey, lastActiveDateFrom, activeDayCount } from '../../utils/weekDates';

// ─── Visible-course denominator ─────────────────────────────────────────────

/**
 * The modules THIS student can actually open. The GC must score a student
 * against the same list the student's own progress counter uses — dividing by
 * the full 83-module catalogue made a fully-completed 7-subject senior read as
 * ~73%, and a JC student read as ~20%.
 */
export function getVisibleCourses(student: GCStudentFullData, allCourses: CourseData[]): CourseData[] {
  return filterCoursesForStudent(allCourses, student.curriculumLevel, student.subjectProfile);
}

// ─── Grade availability ─────────────────────────────────────────────────────

/**
 * Does this student have LC-style grades at all?
 *
 * `subjectProfile != null` was used as the proxy, but a Junior Cycle profile
 * carries currentBand/targetBand and an LCA profile carries level only — both
 * are complete, valid profiles with no H/O grade anywhere. Treating them as
 * "has grades" ran them through the CAO path and printed a confident `0`.
 */
export function hasCAOGrades(student: GCStudentFullData): boolean {
  return !!student.subjectProfile?.subjects.some(s => !!s.currentGrade || !!s.targetGrade);
}

// ─── Progress Helpers ───────────────────────────────────────────────────────

export function getOverallProgress(progress: UserProgress, allCourses: CourseData[]): number {
  if (allCourses.length === 0) return 0;
  const totalProgressSum = allCourses.reduce((sum, course) => {
    const p = progress[course.id];
    if (p && typeof p.unlockedSection === 'number' && course.sectionsCount > 0) {
      return sum + Math.min(100, (p.unlockedSection / course.sectionsCount) * 100);
    }
    return sum;
  }, 0);
  return totalProgressSum / allCourses.length;
}

export function getCategoryProgress(progress: UserProgress, allCourses: CourseData[], category: CategoryType): number {
  const categoryCourses = allCourses.filter(c => c.category === category);
  if (categoryCourses.length === 0) return 0;
  const totalProgress = categoryCourses.reduce((sum, course) => {
    const p = progress[course.id];
    if (p && typeof p.unlockedSection === 'number' && course.sectionsCount > 0) {
      return sum + Math.min(100, (p.unlockedSection / course.sectionsCount) * 100);
    }
    return sum;
  }, 0);
  return totalProgress / categoryCourses.length;
}

export function getCategoryModuleStats(progress: UserProgress, allCourses: CourseData[], category: CategoryType): { completed: number; total: number } {
  const categoryCourses = allCourses.filter(c => c.category === category);
  const completed = categoryCourses.filter(course => {
    const p = progress[course.id];
    return p && typeof p.unlockedSection === 'number' && course.sectionsCount > 0
      && p.unlockedSection >= course.sectionsCount;
  }).length;
  return { completed, total: categoryCourses.length };
}

// ─── CAO Calculation (Best 6) ───────────────────────────────────────────────

export function calculateCAOPoints(subjects: { subjectName: string; grade: string; level: string }[]): number {
  const points = subjects.map(s => {
    const isMaths = LC_SUBJECTS.find(lc => lc.name === s.subjectName)?.isMaths ?? false;
    return getPointsForGrade(s.grade as any, isMaths);
  });
  // Best 6
  points.sort((a, b) => b - a);
  return points.slice(0, 6).reduce((sum, p) => sum + p, 0);
}

export function getStudentCurrentCAO(student: GCStudentFullData): number {
  if (!student.subjectProfile) return 0;
  return calculateCAOPoints(
    student.subjectProfile.subjects.map(s => ({
      subjectName: s.subjectName,
      grade: s.currentGrade,
      level: s.level,
    }))
  );
}

export function getStudentTargetCAO(student: GCStudentFullData): number {
  if (!student.subjectProfile) return 0;
  return calculateCAOPoints(
    student.subjectProfile.subjects.map(s => ({
      subjectName: s.subjectName,
      grade: s.targetGrade,
      level: s.level,
    }))
  );
}

// ─── JC Metrics (Phase 6 — replace CAO columns for JC students) ─────────────
//
// JC students have currentBand / targetBand instead of currentGrade /
// targetGrade. The senior helpers above silently return 0 for them
// (HIGHER_POINTS[undefined] ?? 0). These JC-flavoured equivalents
// surface what's actually meaningful for a JC student's GC view.

const MERIT_INDEX = JC_BANDS.indexOf('Merit'); // 2 — bands ≤ this index are Merit-or-above

/** Count of subjects the JC student has set up. Same shape as senior — just
 *  reads from the array length. Returns 0 if no profile / no subjects. */
export function getStudentSubjectsCovered(student: GCStudentFullData): number {
  return student.subjectProfile?.subjects.length ?? 0;
}

/** Subjects with a current band of Merit or above (Distinction / Higher
 *  Merit / Merit). Read as "subjects on track" for the JC dashboard.
 *  Returns 0 if the student is senior (no currentBand on their subjects)
 *  or has no profile. */
export function getStudentTopBandsCount(student: GCStudentFullData): number {
  if (!student.subjectProfile) return 0;
  return student.subjectProfile.subjects.filter(s => {
    if (!s.currentBand) return false;
    const idx = JC_BANDS.indexOf(s.currentBand as JCBand);
    return idx >= 0 && idx <= MERIT_INDEX;
  }).length;
}

/** Target-side equivalent — subjects the student is *aiming* for Merit
 *  or above. Useful as a "target ambition" indicator on the GC view. */
export function getStudentTargetTopBandsCount(student: GCStudentFullData): number {
  if (!student.subjectProfile) return 0;
  return student.subjectProfile.subjects.filter(s => {
    if (!s.targetBand) return false;
    const idx = JC_BANDS.indexOf(s.targetBand as JCBand);
    return idx >= 0 && idx <= MERIT_INDEX;
  }).length;
}

// ─── Student Status (delegated to utils/studentStatus.ts) ────────────────────

export { getStudentStatus, getStatusReasons, getStatusReasons as getSupportReasons } from '../../utils/studentStatus';

// ─── Days Until LC ──────────────────────────────────────────────────────────

export function getDaysUntilLC(): number {
  const now = new Date();
  const year = now.getFullYear();

  // LC starts first Wednesday of June
  const june1 = new Date(year, 5, 1); // June 1
  let firstWednesday = new Date(june1);
  const day = june1.getDay(); // 0=Sun
  const daysUntilWed = (3 - day + 7) % 7; // 3 = Wednesday
  firstWednesday.setDate(june1.getDate() + daysUntilWed);

  // If that date has passed, use next year
  if (firstWednesday.getTime() < now.getTime()) {
    const nextJune1 = new Date(year + 1, 5, 1);
    const nextDay = nextJune1.getDay();
    const nextDaysUntilWed = (3 - nextDay + 7) % 7;
    firstWednesday = new Date(nextJune1);
    firstWednesday.setDate(nextJune1.getDate() + nextDaysUntilWed);
  }

  return Math.ceil((firstWednesday.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
}

// ─── Active This Week ───────────────────────────────────────────────────────

/**
 * Monday-to-now, matching the exports and the student-status helpers. This
 * previously used a rolling 7-day window AND parsed date keys with the bare
 * Date constructor (UTC midnight vs. the writer's local-parts keys), so the
 * same dashboard answered "active this week" two different ways and shifted a
 * day every summer.
 */
export function isActiveThisWeek(student: GCStudentFullData): boolean {
  if (!student.timetableCompletions) return false;
  const monday = startOfWeek(new Date());

  return Object.entries(student.timetableCompletions).some(([dateKey, blocks]) =>
    Array.isArray(blocks) && blocks.length > 0 && parseDateKey(dateKey) >= monday,
  );
}

// ─── Engagement Timeline ────────────────────────────────────────────────────

export function getEngagementTimeline(
  timetableCompletions: TimetableCompletions | null,
  days: number = 30,
): { date: string; count: number }[] {
  const result: { date: string; count: number }[] = [];
  const now = new Date();
  for (let i = days - 1; i >= 0; i--) {
    const d = new Date(now);
    d.setDate(d.getDate() - i);
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    const key = `${y}-${m}-${day}`;
    const blocks = timetableCompletions?.[key];
    result.push({ date: key, count: Array.isArray(blocks) ? blocks.length : 0 });
  }
  return result;
}

// ─── Attendance helpers (shared by both exporters) ──────────────────────────
//
// These lived as byte-identical private copies in utils/exportCsv.ts and
// utils/exportPdf.ts, which is how they came to share the same two bugs: a
// Sunday off-by-one week and a hardcoded 45-minute block. One definition now,
// so the copies cannot drift again.

/** Days with at least one completed block. Empty day-keys left behind by the
 *  old un-tick bug are not study days. */
export function getSessionCount(completions: Record<string, string[]> | null | undefined): number {
  return activeDayCount(completions);
}

/** Total minutes studied. `blockMinutes` must come from the student's
 *  `subjectProfile.defaultBlockDuration` — hardcoding 45 put the export out by
 *  up to 50% for anyone who changed their block length in settings. */
export function getTotalMinutes(
  completions: Record<string, string[]> | null | undefined,
  blockMinutes: number = 45,
): number {
  if (!completions) return 0;
  const totalBlocks = Object.values(completions).reduce((sum, blocks) => sum + (Array.isArray(blocks) ? blocks.length : 0), 0);
  return totalBlocks * blockMinutes;
}

/** Study days in the Monday–Sunday week `weeksAgo` weeks back. */
export function getSessionsInWeek(
  completions: Record<string, string[]> | null | undefined,
  weeksAgo: number,
): number {
  if (!completions) return 0;
  // Was `now.getDate() - now.getDay() + 1`, which on a Sunday (getDay() === 0)
  // resolves to NEXT Monday — so every export run on a Sunday reported zero
  // sessions this week for the entire school.
  const weekStart = startOfWeek(new Date(), weeksAgo);
  const weekEnd = new Date(weekStart);
  weekEnd.setDate(weekStart.getDate() + 7);

  return Object.entries(completions).filter(([dateKey, blocks]) => {
    if (!Array.isArray(blocks) || blocks.length === 0) return false;
    const d = parseDateKey(dateKey);
    return d >= weekStart && d < weekEnd;
  }).length;
}

/** The student's configured study-block length, defaulting to the app's 45. */
export function getBlockMinutes(student: GCStudentFullData): number {
  return student.subjectProfile?.defaultBlockDuration ?? 45;
}

// ─── Subject-Level Gaps ─────────────────────────────────────────────────────

export function getSubjectGaps(students: GCStudentFullData[]): SubjectGapData[] {
  const subjectMap: Record<string, { totalGap: number; maxGap: number; count: number }> = {};

  students.forEach(s => {
    if (!s.subjectProfile) return;
    s.subjectProfile.subjects.forEach(sub => {
      const isMaths = LC_SUBJECTS.find(lc => lc.name === sub.subjectName)?.isMaths ?? false;
      const currentPts = getPointsForGrade(sub.currentGrade as any, isMaths);
      const targetPts = getPointsForGrade(sub.targetGrade as any, isMaths);
      const gap = targetPts - currentPts;
      if (gap <= 0) return;

      if (!subjectMap[sub.subjectName]) {
        subjectMap[sub.subjectName] = { totalGap: 0, maxGap: 0, count: 0 };
      }
      subjectMap[sub.subjectName].totalGap += gap;
      subjectMap[sub.subjectName].count++;
      if (gap > subjectMap[sub.subjectName].maxGap) {
        subjectMap[sub.subjectName].maxGap = gap;
      }
    });
  });

  return Object.entries(subjectMap)
    .map(([subjectName, data]) => ({
      subjectName,
      studentCount: data.count,
      avgGap: Math.round(data.totalGap / data.count),
      maxGap: data.maxGap,
    }))
    .sort((a, b) => b.avgGap - a.avgGap);
}

// ─── CSV Export ──────────────────────────────────────────────────────────────

function escapeCSV(val: string): string {
  if (val.includes(',') || val.includes('"') || val.includes('\n')) {
    return `"${val.replace(/"/g, '""')}"`;
  }
  return val;
}

export function generateStudentCSV(students: GCStudentFullData[], allCourses: CourseData[]): string {
  const headers = ['Name', 'Year', 'Progress %', 'CAO Current', 'CAO Target', 'Gap', 'Streak', 'Status'];
  const rows = students.map(s => {
    // Score each student against the modules they can actually open, and only
    // print CAO figures for students who have LC grades — a JC or LCA student
    // has no CAO total, so a blank cell is the truth and '0' is a fabrication.
    const visible = getVisibleCourses(s, allCourses);
    const progress = getOverallProgress(s.progress, visible);
    const hasGrades = hasCAOGrades(s);
    const currentCAO = getStudentCurrentCAO(s);
    const targetCAO = getStudentTargetCAO(s);
    const streak = s.streak?.currentStreak ?? 0;
    const status = getStudentStatus(s, visible);

    return [
      escapeCSV(s.user.name),
      escapeCSV(s.yearGroup ?? ''),
      progress.toFixed(1),
      hasGrades ? String(currentCAO) : '',
      hasGrades ? String(targetCAO) : '',
      hasGrades ? String(targetCAO - currentCAO) : '',
      String(streak),
      status,
    ].join(',');
  });

  return [headers.join(','), ...rows].join('\n');
}

// ─── Progress Distribution ──────────────────────────────────────────────────

export function getProgressDistribution(students: GCStudentFullData[], allCourses: CourseData[]): [number, number, number, number] {
  const buckets: [number, number, number, number] = [0, 0, 0, 0];
  students.forEach(s => {
    const p = getOverallProgress(s.progress, getVisibleCourses(s, allCourses));
    if (p < 25) buckets[0]++;
    else if (p < 50) buckets[1]++;
    else if (p < 75) buckets[2]++;
    else buckets[3]++;
  });
  return buckets;
}

// ─── Recently Active Students ────────────────────────────────────────────────

export interface RecentlyActiveStudent {
  uid: string;
  name: string;
  avatar: string;
  lastActiveDate: string;
  blocksCompletedToday: number;
  timeAgo: string;
}

export function getRecentlyActiveStudents(students: GCStudentFullData[], limit: number = 8): RecentlyActiveStudent[] {
  const now = new Date();
  const todayKey = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;

  const withActivity = students
    .map(s => {
      if (!s.timetableCompletions) return null;
      // Days left behind with an empty array (the un-tick bug) are not study
      // days — lastActiveDateFrom skips them.
      const lastActiveDate = lastActiveDateFrom(s.timetableCompletions);
      if (!lastActiveDate) return null;

      // Count blocks completed today
      const todayBlocks = s.timetableCompletions[todayKey];
      const blocksCompletedToday = Array.isArray(todayBlocks) ? todayBlocks.length : 0;

      // Compute timeAgo — parseDateKey keeps this in local time, so a key
      // written last night doesn't read as "1 day ago" all of today.
      const lastDate = parseDateKey(lastActiveDate);
      const todayMidnight = new Date(now);
      todayMidnight.setHours(0, 0, 0, 0);
      const diffDays = Math.round((todayMidnight.getTime() - lastDate.getTime()) / (1000 * 60 * 60 * 24));
      let timeAgo: string;
      if (lastActiveDate === todayKey) {
        timeAgo = 'Today';
      } else if (diffDays <= 1) {
        timeAgo = 'Yesterday';
      } else {
        timeAgo = `${diffDays} days ago`;
      }

      return {
        uid: s.user.uid,
        name: s.user.name,
        avatar: s.user.avatar,
        lastActiveDate,
        blocksCompletedToday,
        timeAgo,
      };
    })
    .filter((x): x is RecentlyActiveStudent => x !== null);

  // Sort by most recent date descending
  withActivity.sort((a, b) => b.lastActiveDate.localeCompare(a.lastActiveDate));
  return withActivity.slice(0, limit);
}

