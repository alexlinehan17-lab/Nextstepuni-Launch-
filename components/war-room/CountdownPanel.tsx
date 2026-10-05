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
import CrewIllustration from '../CrewIllustration';
import { type CAOCourse } from '../futureFinderData';
import type { MockResult } from './warRoomShared';
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
    <div className="wr-time-plan">
      <section className="wr-time-summary" aria-labelledby="war-room-time-summary">
        <h3 id="war-room-time-summary">A manageable week, repeated</h3>
        <div className="wr-time-rhythm">
          <div className="wr-time-week">
            <p><strong>{weeklyHoursText}</strong> <span>hour{weeklyHours === 1 ? '' : 's'} a week.</span></p>
            <p>{weeklySessions} session{weeklySessions === 1 ? '' : 's'} · {blockDuration} minute{blockDuration === 1 ? '' : 's'} each</p>
          </div>
          <div className="wr-time-horizon">
            <p>About <strong>{roundedRemainingHours}</strong> focused hour{roundedRemainingHours === 1 ? '' : 's'} ahead.</p>
            <p>{weeksUntilExam} study week{weeksUntilExam === 1 ? '' : 's'} between now and exams.</p>
            <p className="wr-time-date">{daysUntilExam} day{daysUntilExam === 1 ? '' : 's'} to go.</p>
          </div>
        </div>
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

      <section className="wr-time-allocation" aria-labelledby="war-room-time-allocation">
        <header><p className="wr-eyebrow">Weekly allocation</p><h3 id="war-room-time-allocation">Where the time goes</h3></header>
        <ul className="wr-time-subjects">
          {subjectBudgets.map(subject => (
            <li key={subject.subjectName} className="wr-time-subject">
              <div className="wr-time-subject-top">
                <div className="wr-time-identity">
                  <CrewIllustration subject={subject.subjectName} className="wr-time-art" />
                  <div><h4>{subject.subjectName}</h4><p><span className="sr-only">{subject.gradeAriaLabel}</span><span aria-hidden="true">{subject.gradeLabel}</span></p></div>
                </div>
                <p className="wr-time-sessions"><strong>{subject.sessionsPerWeek}</strong> <span>session{subject.sessionsPerWeek === 1 ? '' : 's'} / week</span></p>
              </div>
              <div className="wr-time-runway">
                <div>
                  <span>{Math.round(subject.hoursStudied)}h recorded</span>
                  <span>{Math.round(subject.hoursRemaining)}h ahead</span>
                </div>
                <MutedProgress value={subject.progress} color="var(--wr-orange)" height={3} />
              </div>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
};

export default CountdownPanel;
