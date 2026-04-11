/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { CourseData } from '../Library';
import { CategoryType } from '../KnowledgeTree';
import { UserProgress } from '../../types';
import { getPointsForGrade, LC_SUBJECTS } from '../subjectData';
import { TimetableCompletions } from '../subjectData';
import { GCStudentFullData, SubjectGapData } from './gcTypes';

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

export function isActiveThisWeek(student: GCStudentFullData): boolean {
  if (!student.timetableCompletions) return false;
  const now = new Date();
  const sevenDaysAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);

  return Object.keys(student.timetableCompletions).some(dateKey => {
    const d = new Date(dateKey);
    return d >= sevenDaysAgo && d <= now;
  });
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
  const headers = ['Name', 'Progress %', 'CAO Current', 'CAO Target', 'Gap', 'Streak', 'Status'];
  const rows = students.map(s => {
    const progress = getOverallProgress(s.progress, allCourses);
    const currentCAO = getStudentCurrentCAO(s);
    const targetCAO = getStudentTargetCAO(s);
    const gap = targetCAO - currentCAO;
    const streak = s.streak?.currentStreak ?? 0;
    const status = getStudentStatus(s, allCourses);

    return [
      escapeCSV(s.user.name),
      progress.toFixed(1),
      String(currentCAO),
      String(targetCAO),
      String(gap),
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
    const p = getOverallProgress(s.progress, allCourses);
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
      const dateKeys = Object.keys(s.timetableCompletions);
      if (dateKeys.length === 0) return null;

      // Find the most recent date key
      dateKeys.sort((a, b) => b.localeCompare(a));
      const lastActiveDate = dateKeys[0];

      // Count blocks completed today
      const todayBlocks = s.timetableCompletions[todayKey];
      const blocksCompletedToday = Array.isArray(todayBlocks) ? todayBlocks.length : 0;

      // Compute timeAgo
      const lastDate = new Date(lastActiveDate);
      const diffMs = now.getTime() - lastDate.getTime();
      const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
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

