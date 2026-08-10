/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useMemo } from 'react';
import {
  type Grade,
  type StudentSubjectProfile,
  getPointsForGrade,
  LC_SUBJECTS,
} from '../subjectData';
import { getDistinctSubjectHex } from '../../studySessionData';
import { type CAOCourse } from '../futureFinderData';
import {
  type MockResult,
  mutedSubjectHex,
} from './warRoomShared';
import { MutedProgress } from './warRoomPrimitives';

interface CountdownPanelProps {
  daysUntilExam: number;
  subjects: StudentSubjectProfile['subjects'];
  allocations: { subjectName: string; sessions: number }[];
  weeksUntilExam: number;
  hoursStudiedMap: Record<string, number>;
  blockDuration: number;
  mockResults: MockResult[];
  targetCourse?: CAOCourse | null;
  currentPoints?: number;
}

const CountdownPanel: React.FC<CountdownPanelProps> = ({
  daysUntilExam,
  subjects,
  allocations,
  weeksUntilExam,
  hoursStudiedMap,
  blockDuration,
  mockResults,
  targetCourse,
  currentPoints,
}) => {
  const latestGradeMap = useMemo(() => {
    const map: Record<string, string> = {};
    const sorted = [...mockResults]
      .filter(result => result.grade && result.date)
      .sort((a, b) => a.date.localeCompare(b.date));
    for (const result of sorted) map[result.subject] = result.grade;
    return map;
  }, [mockResults]);

  const subjectBudgets = useMemo(() => subjects.map((subject, index) => {
    const sessionsPerWeek = allocations.find(item => item.subjectName === subject.subjectName)?.sessions ?? 1;
    const hoursRemaining = (sessionsPerWeek * weeksUntilExam * blockDuration) / 60;
    const hoursStudied = hoursStudiedMap[subject.subjectName] || 0;
    const plannedHours = hoursStudied + hoursRemaining;
    const progress = plannedHours > 0 ? Math.min(100, Math.round((hoursStudied / plannedHours) * 100)) : 0;
    const latestGrade = (latestGradeMap[subject.subjectName] as Grade | undefined) ?? subject.currentGrade;
    const targetGrade = subject.targetGrade;
    const isMaths = LC_SUBJECTS.find(item => item.name === subject.subjectName)?.isMaths ?? false;
    const gap = latestGrade && targetGrade
      ? getPointsForGrade(targetGrade, isMaths) - getPointsForGrade(latestGrade, isMaths)
      : null;
    const gradeLabel = latestGrade && targetGrade
      ? `${latestGrade} → ${targetGrade}`
      : latestGrade
        ? `${latestGrade} · target not set`
        : targetGrade
          ? `Target ${targetGrade}`
          : 'Grades not set';
    const gradeAriaLabel = latestGrade && targetGrade
      ? `Current grade ${latestGrade}. Target grade ${targetGrade}.`
      : latestGrade
        ? `Current grade ${latestGrade}. Target grade not set.`
        : targetGrade
          ? `Current grade not set. Target grade ${targetGrade}.`
          : 'Current and target grades not set.';
    return {
      ...subject,
      subjectIndex: index,
      sessionsPerWeek,
      hoursRemaining,
      hoursStudied,
      plannedHours,
      progress,
      latestGrade,
      gap,
      gradeLabel,
      gradeAriaLabel,
      color: mutedSubjectHex(getDistinctSubjectHex(subject.subjectName, index), 0.14),
    };
  }).sort((a, b) => {
    if (a.gap !== null && b.gap !== null && a.gap !== b.gap) return b.gap - a.gap;
    if (a.gap !== null) return -1;
    if (b.gap !== null) return 1;
    if (a.sessionsPerWeek !== b.sessionsPerWeek) return b.sessionsPerWeek - a.sessionsPerWeek;
    return a.subjectIndex - b.subjectIndex;
  }), [allocations, blockDuration, hoursStudiedMap, latestGradeMap, subjects, weeksUntilExam]);

  const weeklySessions = subjectBudgets.reduce((total, subject) => total + subject.sessionsPerWeek, 0);
  const weeklyHours = weeklySessions * blockDuration / 60;
  const totalRemaining = subjectBudgets.reduce((total, subject) => total + subject.hoursRemaining, 0);
  const weeklyHoursText = weeklyHours.toFixed(Number.isInteger(weeklyHours) ? 0 : 1);
  const roundedRemainingHours = Math.round(totalRemaining);

  return (
    <div className="space-y-9">
      <section aria-labelledby="war-room-time-summary">
        <div className="max-w-2xl">
          <h3 id="war-room-time-summary" className="text-xl font-semibold tracking-[-0.02em] text-[var(--ink-primary)]">
            A manageable week, repeated
          </h3>
        </div>

        <dl className="mt-5 grid border-y border-[var(--outline-soft)] sm:grid-cols-4 sm:divide-x sm:divide-[var(--outline-soft)]">
          <div className="flex items-baseline justify-between gap-4 border-b border-[var(--outline-soft)] py-3 sm:block sm:border-b-0 sm:px-4 sm:first:pl-0">
            <dt className="text-xs text-[var(--ink-muted)]">Until exams</dt>
            <dd className="text-sm font-semibold text-[var(--ink-primary)] tabular-nums sm:mt-1">{daysUntilExam} day{daysUntilExam === 1 ? '' : 's'}</dd>
          </div>
          <div className="flex items-baseline justify-between gap-4 border-b border-[var(--outline-soft)] py-3 sm:block sm:border-b-0 sm:px-4">
            <dt className="text-xs text-[var(--ink-muted)]">Each week</dt>
            <dd className="text-sm font-semibold text-[var(--ink-primary)] tabular-nums sm:mt-1">{weeklySessions} session{weeklySessions === 1 ? '' : 's'}</dd>
          </div>
          <div className="flex items-baseline justify-between gap-4 border-b border-[var(--outline-soft)] py-3 sm:block sm:border-b-0 sm:px-4">
            <dt className="text-xs text-[var(--ink-muted)]">Weekly time</dt>
            <dd className="text-sm font-semibold text-[var(--ink-primary)] tabular-nums sm:mt-1">{weeklyHoursText} hour{weeklyHours === 1 ? '' : 's'}</dd>
          </div>
          <div className="flex items-baseline justify-between gap-4 py-3 sm:block sm:px-4 sm:last:pr-0">
            <dt className="text-xs text-[var(--ink-muted)]">Focused time ahead</dt>
            <dd className="text-sm font-semibold text-[var(--ink-primary)] tabular-nums sm:mt-1">About {roundedRemainingHours} hour{roundedRemainingHours === 1 ? '' : 's'}</dd>
          </div>
        </dl>
        <p className="mt-3 text-xs text-[var(--ink-muted)]">
          {weeksUntilExam} study week{weeksUntilExam === 1 ? '' : 's'} · {blockDuration} minute{blockDuration === 1 ? '' : 's'} per session
        </p>
      </section>

      {targetCourse && currentPoints !== undefined && (
        <section aria-labelledby="war-room-course-target">
          <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-[var(--ink-muted)]">Course target</p>
          <div className="mt-3 flex flex-col gap-3 border-y border-[var(--outline-soft)] py-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h3 id="war-room-course-target" className="text-sm font-semibold text-[var(--ink-primary)]">{targetCourse.title}</h3>
              <p className="mt-1 text-xs text-[var(--ink-muted)]">
                {targetCourse.institution} · {targetCourse.typicalPoints} points typically required
              </p>
            </div>
            <p className="shrink-0 text-xs font-semibold text-[var(--ink-secondary)] tabular-nums">
              {currentPoints >= targetCourse.typicalPoints
                ? 'On target'
                : `${targetCourse.typicalPoints - currentPoints} points to target`}
            </p>
          </div>
        </section>
      )}

      <section aria-labelledby="war-room-time-allocation">
        <div>
          <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-[var(--ink-muted)]">Weekly allocation</p>
          <h3 id="war-room-time-allocation" className="mt-2 text-lg font-semibold tracking-[-0.01em] text-[var(--ink-primary)]">Where the time goes</h3>
        </div>
        <div className="mt-4 border-y border-[var(--outline-soft)]">
          <div className="hidden grid-cols-[minmax(150px,1fr)_90px_90px_minmax(160px,1fr)] gap-4 border-b border-[var(--outline-soft)] py-3 text-[10px] font-bold uppercase tracking-[.14em] text-[var(--ink-muted)] sm:grid" aria-hidden="true">
            <span>Subject</span><span>Grade path</span><span>Per week</span><span>Planned runway</span>
          </div>
          <ul>
            {subjectBudgets.map(subject => (
              <li
                key={subject.subjectName}
                className="grid gap-3 border-b border-[var(--outline-soft)] py-4 last:border-b-0 sm:grid-cols-[minmax(150px,1fr)_90px_90px_minmax(160px,1fr)] sm:items-center sm:gap-4"
              >
                <div className="flex min-w-0 items-center gap-3">
                  <span className="h-2 w-2 shrink-0 rounded-full" style={{ background: subject.color }} aria-hidden="true" />
                  <span className="truncate text-sm font-semibold text-[var(--ink-primary)]">{subject.subjectName}</span>
                </div>
                <span className="text-xs text-[var(--ink-secondary)] tabular-nums">
                  <span className="sr-only">{subject.gradeAriaLabel}</span>
                  <span aria-hidden="true">{subject.gradeLabel}</span>
                </span>
                <span className="text-xs font-semibold text-[var(--ink-primary)]">
                  <span className="sr-only">Per week: </span>{subject.sessionsPerWeek} session{subject.sessionsPerWeek === 1 ? '' : 's'}
                </span>
                <div>
                  <div className="mb-1.5 flex items-center justify-between gap-3 text-[10px] text-[var(--ink-muted)] tabular-nums">
                    <span>{Math.round(subject.hoursStudied)}h done</span>
                    <span>{Math.round(subject.hoursRemaining)}h ahead</span>
                  </div>
                  <MutedProgress value={subject.progress} color={subject.color} height={3} />
                </div>
              </li>
            ))}
          </ul>
        </div>
      </section>
    </div>
  );
};

export default CountdownPanel;
