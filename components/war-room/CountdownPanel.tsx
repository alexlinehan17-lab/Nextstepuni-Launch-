/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useMemo } from 'react';
import { CalendarDays, Clock3 } from 'lucide-react';
import { type StudentSubjectProfile } from '../subjectData';
import { getDistinctSubjectHex } from '../../studySessionData';
import { type CAOCourse } from '../futureFinderData';
import {
  type MockResult,
  gradeToPoints,
  mutedSubjectHex,
} from './warRoomShared';
import { EditorialCard, MutedProgress, Overline, Pill, SectionHeader } from './warRoomPrimitives';

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
    const latestGrade = latestGradeMap[subject.subjectName] || subject.currentGrade;
    const gap = gradeToPoints(subject.targetGrade) - gradeToPoints(latestGrade);
    return {
      ...subject,
      sessionsPerWeek,
      hoursRemaining,
      hoursStudied,
      plannedHours,
      progress,
      latestGrade,
      gap,
      color: mutedSubjectHex(getDistinctSubjectHex(subject.subjectName, index), 0.14),
    };
  }).sort((a, b) => b.gap - a.gap), [allocations, blockDuration, hoursStudiedMap, latestGradeMap, subjects, weeksUntilExam]);

  const weeklySessions = subjectBudgets.reduce((total, subject) => total + subject.sessionsPerWeek, 0);
  const weeklyHours = weeklySessions * blockDuration / 60;
  const totalRemaining = subjectBudgets.reduce((total, subject) => total + subject.hoursRemaining, 0);

  return (
    <div className="space-y-8">
      <section className="grid gap-4 md:grid-cols-[1.15fr_.85fr]">
        <EditorialCard className="flex min-h-[190px] flex-col justify-between" style={{ border: '1.5px solid var(--outline-strong)' }}>
          <div className="flex items-start justify-between gap-5">
            <div>
              <Overline>Exam runway</Overline>
              <p className="mt-3 font-serif text-[52px] font-semibold leading-none tracking-[-.04em] text-[var(--ink-primary)] tabular-nums sm:text-[64px]">
                {daysUntilExam}
              </p>
              <p className="mt-2 text-sm text-[var(--ink-secondary)]">days until your first exam</p>
            </div>
            <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-[#FDEEDF] text-[#A43F08]" aria-hidden="true">
              <CalendarDays size={23} />
            </span>
          </div>
          <p className="mt-6 border-t border-[var(--outline-soft)] pt-4 text-xs leading-relaxed text-[var(--ink-muted)]">
            {weeksUntilExam} study weeks remain. At the current allocation, that creates about {Math.round(totalRemaining)} focused hours.
          </p>
        </EditorialCard>

        <EditorialCard className="flex min-h-[190px] flex-col justify-between">
          <div>
            <div className="flex items-center justify-between gap-4">
              <Overline>Weekly capacity</Overline>
              <Clock3 size={18} className="text-[var(--ink-muted)]" aria-hidden="true" />
            </div>
            <p className="mt-4 font-serif text-[34px] font-semibold leading-none text-[var(--ink-primary)]">
              {weeklySessions} sessions
            </p>
            <p className="mt-2 text-sm text-[var(--ink-secondary)]">
              approximately {weeklyHours.toFixed(weeklyHours < 10 ? 1 : 0)} hours each week
            </p>
          </div>
          <div className="mt-6 grid grid-cols-2 gap-3 border-t border-[var(--outline-soft)] pt-4 text-xs">
            <div><span className="block font-semibold text-[var(--ink-primary)]">{blockDuration} min</span><span className="text-[var(--ink-muted)]">per session</span></div>
            <div><span className="block font-semibold text-[var(--ink-primary)]">{subjects.length}</span><span className="text-[var(--ink-muted)]">subjects covered</span></div>
          </div>
        </EditorialCard>
      </section>

      {targetCourse && currentPoints !== undefined && (
        <section>
          <SectionHeader overline="Course target" title={targetCourse.title} rule={false} />
          <div className="mt-3 flex flex-col gap-3 border-y border-[var(--outline-soft)] py-4 sm:flex-row sm:items-center sm:justify-between">
            <p className="text-sm text-[var(--ink-secondary)]">
              {targetCourse.institution} · {targetCourse.typicalPoints} points typically required
            </p>
            {currentPoints >= targetCourse.typicalPoints
              ? <Pill bg="#E8F2EC" fg="#1F5F3E">On target</Pill>
              : <Pill bg="#FDEEDF" fg="#A43F08">{targetCourse.typicalPoints - currentPoints} point gap</Pill>}
          </div>
        </section>
      )}

      <section>
        <SectionHeader
          overline="Weekly allocation"
          title="Where the time goes"
          rule={false}
          trailing={<span className="text-xs text-[var(--ink-muted)]">Highest grade gap first</span>}
        />
        <EditorialCard padded={false} className="mt-4 overflow-hidden">
          <div className="hidden grid-cols-[minmax(150px,1fr)_90px_90px_minmax(160px,1fr)] gap-4 border-b border-[var(--outline-soft)] px-5 py-3 text-[10px] font-bold uppercase tracking-[.14em] text-[var(--ink-muted)] sm:grid">
            <span>Subject</span><span>Grade</span><span>Per week</span><span>Planned runway</span>
          </div>
          {subjectBudgets.map((subject, index) => (
            <div
              key={subject.subjectName}
              className="grid gap-3 px-5 py-4 sm:grid-cols-[minmax(150px,1fr)_90px_90px_minmax(160px,1fr)] sm:items-center sm:gap-4"
              style={{ borderTop: index ? '1px solid var(--outline-soft)' : undefined }}
            >
              <div className="flex min-w-0 items-center gap-3">
                <span className="h-2.5 w-2.5 shrink-0 rounded-full" style={{ background: subject.color }} aria-hidden="true" />
                <span className="truncate font-serif text-[15px] font-semibold text-[var(--ink-primary)]">{subject.subjectName}</span>
              </div>
              <span className="font-mono text-xs text-[var(--ink-secondary)]">{subject.latestGrade} → {subject.targetGrade}</span>
              <span className="text-xs font-semibold text-[var(--ink-primary)]">{subject.sessionsPerWeek} session{subject.sessionsPerWeek === 1 ? '' : 's'}</span>
              <div>
                <div className="mb-1.5 flex items-center justify-between gap-3 font-mono text-[10px] text-[var(--ink-muted)]">
                  <span>{Math.round(subject.hoursStudied)}h done</span>
                  <span>{Math.round(subject.hoursRemaining)}h ahead</span>
                </div>
                <MutedProgress value={subject.progress} color={subject.color} height={5} />
              </div>
            </div>
          ))}
        </EditorialCard>
      </section>
    </div>
  );
};

export default CountdownPanel;
