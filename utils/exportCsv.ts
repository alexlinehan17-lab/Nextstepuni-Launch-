/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type GCStudentFullData } from '../components/gc/gcTypes';
import { type CourseData } from '../components/Library';
import { getRankForPoints } from '../gamificationConfig';
import { getSessionCount, getTotalMinutes, getSessionsInWeek, getBlockMinutes, getVisibleCourses } from '../components/gc/gcUtils';

// ─── Helpers ────────────────────────────────────────────────────────────────

function escapeCSV(value: string): string {
  let v = value;
  // Neutralise spreadsheet formula/macro injection: a cell beginning with
  // = + - @ (or a leading tab / carriage return) is executed as a formula by
  // Excel / Google Sheets. Student-controlled fields (name, subject, mock
  // subject) flow into GC-exported CSVs, so prefix any such value with an
  // apostrophe to force text. (Security review 2026-07-16, MEDIUM.)
  if (/^[=+\-@\t\r]/.test(v)) v = `'${v}`;
  if (v.includes(',') || v.includes('"') || v.includes('\n') || v.includes('\r')) {
    return `"${v.replace(/"/g, '""')}"`;
  }
  return v;
}

// Both of these scope to the modules the student can actually open — the whole
// catalogue as a denominator understated every student's completion (a
// finished 7-subject senior exported as ~73%).
function getModulesCompleted(student: GCStudentFullData, allCourses: CourseData[]): number {
  return getVisibleCourses(student, allCourses).filter(course => {
    const p = student.progress[course.id];
    return p && p.unlockedSection >= course.sectionsCount;
  }).length;
}

function getCompletionPercent(student: GCStudentFullData, catalogue: CourseData[]): number {
  const allCourses = getVisibleCourses(student, catalogue);
  if (allCourses.length === 0) return 0;
  const totalProgressSum = allCourses.reduce((sum, course) => {
    const p = student.progress[course.id];
    if (p && typeof p.unlockedSection === 'number' && course.sectionsCount > 0) {
      return sum + Math.min(100, (p.unlockedSection / course.sectionsCount) * 100);
    }
    return sum;
  }, 0);
  return totalProgressSum / allCourses.length;
}


// ─── CSV Generators ─────────────────────────────────────────────────────────

export function generateStudentProgressCSV(students: GCStudentFullData[], allCourses: CourseData[]): string {
  const headers = ['Name', 'Modules Completed', 'Completion %', 'Rank', 'Total Points', 'Current Streak', 'Longest Streak'];
  const rows = students.map(s => {
    const modulesCompleted = getModulesCompleted(s, allCourses);
    const completionPct = getCompletionPercent(s, allCourses);
    const totalPoints = s.points?.totalEarned ?? 0;
    const rank = getRankForPoints(totalPoints);
    const currentStreak = s.streak?.currentStreak ?? 0;
    const longestStreak = s.streak?.longestStreak ?? 0;

    return [
      escapeCSV(s.user.name),
      String(modulesCompleted),
      completionPct.toFixed(1),
      rank.title,
      String(totalPoints),
      String(currentStreak),
      String(longestStreak),
    ].join(',');
  });

  return [headers.join(','), ...rows].join('\n');
}

export function generateAttendanceCSV(students: GCStudentFullData[]): string {
  const headers = ['Name', 'Total Sessions', 'Total Minutes', 'This Week Sessions', 'Last Week Sessions'];
  const rows = students.map(s => {
    const completions = s.timetableCompletions;
    return [
      escapeCSV(s.user.name),
      String(getSessionCount(completions)),
      // Real block length, not a hardcoded 45 — a student on 60-minute blocks
      // was under-reported by a third.
      String(getTotalMinutes(completions, getBlockMinutes(s))),
      String(getSessionsInWeek(completions, 0)),
      String(getSessionsInWeek(completions, 1)),
    ].join(',');
  });

  return [headers.join(','), ...rows].join('\n');
}

export function generateSubjectHealthCSV(students: GCStudentFullData[]): string {
  const headers = ['Subject', 'Students Taking', 'Avg Coverage %'];

  // Aggregate subjects across all students
  const subjectMap: Record<string, { count: number; totalCoverage: number }> = {};
  students.forEach(s => {
    if (!s.subjectProfile?.subjects) return;
    const completions = s.timetableCompletions ?? {};
    const totalDays = Object.keys(completions).length;

    s.subjectProfile.subjects.forEach(sub => {
      if (!subjectMap[sub.subjectName]) {
        subjectMap[sub.subjectName] = { count: 0, totalCoverage: 0 };
      }
      subjectMap[sub.subjectName].count++;

      // Coverage: what % of study days included this subject
      if (totalDays > 0) {
        const daysWithSubject = Object.values(completions).filter(
          blocks => blocks.some(b => b.startsWith(sub.subjectName + '|'))
        ).length;
        subjectMap[sub.subjectName].totalCoverage += (daysWithSubject / totalDays) * 100;
      }
    });
  });

  const rows = Object.entries(subjectMap)
    .sort((a, b) => b[1].count - a[1].count)
    .map(([name, data]) => {
      const avgCoverage = data.count > 0 ? (data.totalCoverage / data.count) : 0;
      return [
        escapeCSV(name),
        String(data.count),
        avgCoverage.toFixed(1),
      ].join(',');
    });

  return [headers.join(','), ...rows].join('\n');
}

export function generateStudentDetailCSV(student: GCStudentFullData, allCourses: CourseData[]): string {
  const lines: string[] = [];
  const totalPoints = student.points?.totalEarned ?? 0;
  const rank = getRankForPoints(totalPoints);

  // General info
  lines.push('Field,Value');
  lines.push(`Name,${escapeCSV(student.user.name)}`);
  lines.push(`Rank,${rank.title}`);
  lines.push(`Total Points,${totalPoints}`);
  lines.push(`Current Streak,${student.streak?.currentStreak ?? 0}`);
  lines.push(`Longest Streak,${student.streak?.longestStreak ?? 0}`);
  lines.push(`Modules Completed,${getModulesCompleted(student, allCourses)}`);
  lines.push(`Completion %,${getCompletionPercent(student, allCourses).toFixed(1)}`);
  lines.push('');

  // Subjects
  if (student.subjectProfile?.subjects && student.subjectProfile.subjects.length > 0) {
    lines.push('Subject,Level,Current Grade,Target Grade');
    student.subjectProfile.subjects.forEach(sub => {
      lines.push([
        escapeCSV(sub.subjectName),
        sub.level,
        sub.currentGrade,
        sub.targetGrade,
      ].join(','));
    });
    lines.push('');
  }

  // Mock results
  if (student.mockResults && student.mockResults.length > 0) {
    lines.push('Mock Subject,Grade,Date');
    student.mockResults.forEach(m => {
      lines.push([
        escapeCSV(m.subject),
        m.grade,
        m.date,
      ].join(','));
    });
  }

  return lines.join('\n');
}

// ─── Download helper ────────────────────────────────────────────────────────

export function downloadCSV(content: string, filename: string): void {
  const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.style.display = 'none';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
