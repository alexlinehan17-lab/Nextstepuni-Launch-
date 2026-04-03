/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import jsPDF from 'jspdf';
import 'jspdf-autotable';

import { GCStudentFullData } from '../components/gc/gcTypes';
import { CourseData } from '../components/Library';
import { getRankForPoints } from '../gamificationConfig';

// ─── Helpers ────────────────────────────────────────────────────────────────

function getModulesCompleted(student: GCStudentFullData, allCourses: CourseData[]): number {
  return allCourses.filter(course => {
    const p = student.progress[course.id];
    return p && p.unlockedSection >= course.sectionsCount;
  }).length;
}

function getCompletionPercent(student: GCStudentFullData, allCourses: CourseData[]): number {
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

function getSessionCount(completions: Record<string, string[]> | null): number {
  if (!completions) return 0;
  return Object.keys(completions).length;
}

function getTotalMinutes(completions: Record<string, string[]> | null): number {
  if (!completions) return 0;
  const totalBlocks = Object.values(completions).reduce((sum, blocks) => sum + blocks.length, 0);
  return totalBlocks * 45;
}

function getSessionsInWeek(completions: Record<string, string[]> | null, weeksAgo: number): number {
  if (!completions) return 0;
  const now = new Date();
  const startOfCurrentWeek = new Date(now);
  startOfCurrentWeek.setDate(now.getDate() - now.getDay() + 1 - weeksAgo * 7);
  startOfCurrentWeek.setHours(0, 0, 0, 0);
  const endOfWeek = new Date(startOfCurrentWeek);
  endOfWeek.setDate(startOfCurrentWeek.getDate() + 7);

  return Object.keys(completions).filter(dateKey => {
    const d = new Date(dateKey + 'T00:00:00');
    return d >= startOfCurrentWeek && d < endOfWeek;
  }).length;
}

// ─── Shared table styles ────────────────────────────────────────────────────

const HEAD_STYLES = {
  fillColor: [42, 125, 111] as [number, number, number],
  textColor: [255, 255, 255] as [number, number, number],
  fontSize: 11,
  fontStyle: 'bold' as const,
};

const BODY_STYLES = {
  fontSize: 9,
};

const ALTERNATE_ROW_STYLES = {
  fillColor: [253, 248, 240] as [number, number, number],
};

// ─── Main export ────────────────────────────────────────────────────────────

export function generateReport(options: {
  school: string;
  students: GCStudentFullData[];
  allCourses: CourseData[];
  includeProgress: boolean;
  includeAttendance: boolean;
  includeSubjectHealth: boolean;
  individualStudent?: GCStudentFullData;
}): void {
  const { school, students, allCourses, includeProgress, includeAttendance, includeSubjectHealth, individualStudent } = options;
  const doc = new jsPDF('p', 'mm', 'a4');
  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();
  const today = new Date().toLocaleDateString('en-IE', { year: 'numeric', month: 'long', day: 'numeric' });

  // ── Title page ──
  doc.setFontSize(28);
  doc.setTextColor(42, 125, 111);
  doc.text('NextStepUni Report', pageWidth / 2, 80, { align: 'center' });

  doc.setFontSize(14);
  doc.setTextColor(80, 80, 80);
  doc.text(school, pageWidth / 2, 95, { align: 'center' });

  doc.setFontSize(11);
  doc.setTextColor(140, 140, 140);
  doc.text(today, pageWidth / 2, 106, { align: 'center' });

  doc.setFontSize(10);
  doc.setTextColor(140, 140, 140);
  doc.text(`${students.length} student${students.length !== 1 ? 's' : ''}`, pageWidth / 2, 116, { align: 'center' });

  // ── Student Progress ──
  if (includeProgress) {
    doc.addPage();
    doc.setFontSize(16);
    doc.setTextColor(42, 125, 111);
    doc.text('Student Progress Summary', 14, 20);

    const progressBody = students.map(s => {
      const totalPoints = s.points?.totalEarned ?? 0;
      const rank = getRankForPoints(totalPoints);
      return [
        s.user.name,
        String(getModulesCompleted(s, allCourses)),
        getCompletionPercent(s, allCourses).toFixed(1) + '%',
        rank.title,
        String(totalPoints),
        String(s.streak?.currentStreak ?? 0),
        String(s.streak?.longestStreak ?? 0),
      ];
    });

    (doc as any).autoTable({
      startY: 28,
      head: [['Name', 'Modules', 'Completion %', 'Rank', 'Points', 'Streak', 'Best Streak']],
      body: progressBody,
      headStyles: HEAD_STYLES,
      bodyStyles: BODY_STYLES,
      alternateRowStyles: ALTERNATE_ROW_STYLES,
      styles: { cellPadding: 3 },
    });
  }

  // ── Attendance Patterns ──
  if (includeAttendance) {
    doc.addPage();
    doc.setFontSize(16);
    doc.setTextColor(42, 125, 111);
    doc.text('Attendance Patterns', 14, 20);

    const attendanceBody = students.map(s => {
      const completions = s.timetableCompletions;
      return [
        s.user.name,
        String(getSessionCount(completions)),
        String(getTotalMinutes(completions)),
        String(getSessionsInWeek(completions, 0)),
        String(getSessionsInWeek(completions, 1)),
      ];
    });

    (doc as any).autoTable({
      startY: 28,
      head: [['Name', 'Total Sessions', 'Total Minutes', 'This Week', 'Last Week']],
      body: attendanceBody,
      headStyles: HEAD_STYLES,
      bodyStyles: BODY_STYLES,
      alternateRowStyles: ALTERNATE_ROW_STYLES,
      styles: { cellPadding: 3 },
    });
  }

  // ── Subject Health ──
  if (includeSubjectHealth) {
    doc.addPage();
    doc.setFontSize(16);
    doc.setTextColor(42, 125, 111);
    doc.text('Subject Health Overview', 14, 20);

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

        if (totalDays > 0) {
          const daysWithSubject = Object.values(completions).filter(
            blocks => blocks.some(b => b.startsWith(sub.subjectName + '|'))
          ).length;
          subjectMap[sub.subjectName].totalCoverage += (daysWithSubject / totalDays) * 100;
        }
      });
    });

    const subjectBody = Object.entries(subjectMap)
      .sort((a, b) => b[1].count - a[1].count)
      .map(([name, data]) => {
        const avgCoverage = data.count > 0 ? (data.totalCoverage / data.count) : 0;
        return [name, String(data.count), avgCoverage.toFixed(1) + '%'];
      });

    (doc as any).autoTable({
      startY: 28,
      head: [['Subject', 'Students Taking', 'Avg Coverage %']],
      body: subjectBody,
      headStyles: HEAD_STYLES,
      bodyStyles: BODY_STYLES,
      alternateRowStyles: ALTERNATE_ROW_STYLES,
      styles: { cellPadding: 3 },
    });
  }

  // ── Individual Student ──
  if (individualStudent) {
    doc.addPage();
    doc.setFontSize(16);
    doc.setTextColor(42, 125, 111);
    doc.text(`Student Detail: ${individualStudent.user.name}`, 14, 20);

    const totalPoints = individualStudent.points?.totalEarned ?? 0;
    const rank = getRankForPoints(totalPoints);
    const modulesCompleted = getModulesCompleted(individualStudent, allCourses);
    const completionPct = getCompletionPercent(individualStudent, allCourses);

    // Summary paragraph
    doc.setFontSize(10);
    doc.setTextColor(60, 60, 60);
    const summaryText = `${individualStudent.user.name} is currently ranked ${rank.title} with ${totalPoints} points. ` +
      `They have completed ${modulesCompleted} modules (${completionPct.toFixed(1)}% overall progress). ` +
      `Current streak: ${individualStudent.streak?.currentStreak ?? 0} days. ` +
      `Longest streak: ${individualStudent.streak?.longestStreak ?? 0} days.`;
    const splitSummary = doc.splitTextToSize(summaryText, pageWidth - 28);
    doc.text(splitSummary, 14, 30);

    let nextY = 30 + splitSummary.length * 5 + 8;

    // Subjects table
    if (individualStudent.subjectProfile?.subjects && individualStudent.subjectProfile.subjects.length > 0) {
      doc.setFontSize(12);
      doc.setTextColor(42, 125, 111);
      doc.text('Subjects', 14, nextY);

      (doc as any).autoTable({
        startY: nextY + 4,
        head: [['Subject', 'Level', 'Current Grade', 'Target Grade']],
        body: individualStudent.subjectProfile.subjects.map(sub => [
          sub.subjectName,
          sub.level === 'higher' ? 'Higher' : 'Ordinary',
          sub.currentGrade,
          sub.targetGrade,
        ]),
        headStyles: HEAD_STYLES,
        bodyStyles: BODY_STYLES,
        alternateRowStyles: ALTERNATE_ROW_STYLES,
        styles: { cellPadding: 3 },
      });

      nextY = (doc as any).lastAutoTable.finalY + 10;
    }

    // Mock results table
    if (individualStudent.mockResults && individualStudent.mockResults.length > 0) {
      if (nextY > pageHeight - 50) {
        doc.addPage();
        nextY = 20;
      }

      doc.setFontSize(12);
      doc.setTextColor(42, 125, 111);
      doc.text('Mock Results', 14, nextY);

      (doc as any).autoTable({
        startY: nextY + 4,
        head: [['Subject', 'Grade', 'Date']],
        body: individualStudent.mockResults.map(m => [m.subject, m.grade, m.date]),
        headStyles: HEAD_STYLES,
        bodyStyles: BODY_STYLES,
        alternateRowStyles: ALTERNATE_ROW_STYLES,
        styles: { cellPadding: 3 },
      });
    }
  }

  // ── Page numbers ──
  const totalPages = (doc as any).internal.getNumberOfPages();
  for (let i = 1; i <= totalPages; i++) {
    doc.setPage(i);
    doc.setFontSize(8);
    doc.setTextColor(160, 160, 160);
    doc.text(`Page ${i} of ${totalPages}`, pageWidth / 2, pageHeight - 8, { align: 'center' });
  }

  // ── Save ──
  const dateStr = new Date().toISOString().split('T')[0];
  const filename = individualStudent
    ? `nextstepuni-${individualStudent.user.name.replace(/\s+/g, '-').toLowerCase()}-${dateStr}.pdf`
    : `nextstepuni-report-${dateStr}.pdf`;
  doc.save(filename);
}
