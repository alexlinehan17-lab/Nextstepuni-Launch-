/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useMemo } from 'react';
import { motion } from 'framer-motion';

import { type StudentSubjectProfile } from '../subjectData';
import { getDistinctSubjectHex } from '../../studySessionData';
import {
  type MockResult, gradeToPoints,
  PAPER, PAPER_SOFT, INK, INK_SOFT, INK_MUTE, INK_FAINT, ACCENT,
  STATUS_SOLID, STATUS_GAP, STATUS_GAP_DEEP, STATUS_GAP_TINT, STATUS_SOLID_DEEP, STATUS_SOLID_TINT,
  mutedSubjectHex,
} from './warRoomShared';
import {
  Overline, SectionHeader, EditorialCard, MutedProgress, Pill,
} from './warRoomPrimitives';
import { type CAOCourse } from '../futureFinderData';

// ── Panel 0: Countdown & Time Budget ───────────────────────

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
  daysUntilExam, subjects, allocations, weeksUntilExam, hoursStudiedMap, blockDuration,
  mockResults, targetCourse, currentPoints,
}) => {
  const latestGradeMap = useMemo(() => {
    const map: Record<string, string> = {};
    const sorted = [...mockResults].filter(r => r.grade && r.date)
      .sort((a, b) => (a.date ?? '').localeCompare(b.date ?? ''));
    for (const r of sorted) map[r.subject] = r.grade;
    return map;
  }, [mockResults]);

  const subjectBudgets = useMemo(() => {
    return subjects.map(s => {
      const alloc = allocations.find(a => a.subjectName === s.subjectName);
      const sessionsPerWeek = alloc?.sessions ?? 1;
      const hoursRemaining = (sessionsPerWeek * weeksUntilExam * blockDuration) / 60;
      const hoursStudied = hoursStudiedMap[s.subjectName] || 0;
      const totalHours = hoursStudied + hoursRemaining;
      const pct = totalHours > 0 ? Math.min(100, Math.round((hoursStudied / totalHours) * 100)) : 0;
      const latestGrade = latestGradeMap[s.subjectName];
      const targetPts = gradeToPoints(s.targetGrade);
      const currentPts = latestGrade ? gradeToPoints(latestGrade) : gradeToPoints(s.currentGrade);
      const gap = targetPts - currentPts;
      return {
        subjectName: s.subjectName, hoursStudied, hoursRemaining, totalHours, pct,
        latestGrade: latestGrade || s.currentGrade, targetGrade: s.targetGrade, gap, sessionsPerWeek,
      };
    });
  }, [subjects, allocations, weeksUntilExam, hoursStudiedMap, blockDuration, latestGradeMap]);

  const totalStudied = subjectBudgets.reduce((sum, s) => sum + s.hoursStudied, 0);
  const totalRemaining = subjectBudgets.reduce((sum, s) => sum + s.hoursRemaining, 0);

  return (
    <div className="space-y-6">
      {/* ── Editorial countdown hero ── */}
      <EditorialCard tone="paper" padded={false}>
        <div className="grid md:grid-cols-[1fr,1.1fr] gap-0">
          {/* Left: large number + meta lines */}
          <div className="px-6 sm:px-8 py-7 sm:py-8 flex flex-col justify-center">
            <Overline color={ACCENT}>The countdown</Overline>
            <motion.p
              className="font-serif font-bold tabular-nums mt-2"
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
              style={{
                color: INK,
                fontSize: 'clamp(80px, 14vw, 132px)',
                letterSpacing: '-0.04em',
                lineHeight: 0.95,
              }}
            >
              {daysUntilExam}
            </motion.p>
            <p className="font-serif text-[18px] mt-1" style={{ color: INK_SOFT }}>
              days until exams
            </p>

            {/* Refined meta line */}
            <div className="mt-5 flex flex-wrap items-center gap-x-4 gap-y-1">
              <span className="font-mono text-[12px]" style={{ color: INK_MUTE }}>
                {weeksUntilExam} weeks of study
              </span>
              <span className="font-mono text-[12px]" style={{ color: INK_FAINT }}>·</span>
              <span className="font-mono text-[12px]" style={{ color: INK_MUTE }}>
                ~{Math.round(totalRemaining)}h remaining
              </span>
              <span className="font-mono text-[12px]" style={{ color: INK_FAINT }}>·</span>
              <span className="font-mono text-[12px]" style={{ color: INK_MUTE }}>
                {Math.round(totalStudied)}h studied
              </span>
            </div>
          </div>

          {/* Right: hand-drawn calendar → checklist illustration */}
          <div className="hidden md:flex items-center justify-end pr-4 sm:pr-6">
            <img
              src="/assets/war-room-countdown.png"
              alt=""
              aria-hidden
              style={{
                width: '100%',
                height: '100%',
                maxHeight: 280,
                objectFit: 'contain',
                objectPosition: 'right center',
              }}
            />
          </div>
        </div>
      </EditorialCard>

      {/* ── Target Course banner ── */}
      {targetCourse && currentPoints !== undefined && (() => {
        const onTarget = currentPoints >= targetCourse.typicalPoints;
        return (
          <EditorialCard tone="soft">
            <div className="flex items-center justify-between gap-4">
              <div className="min-w-0">
                <Overline>Target course</Overline>
                <p className="font-serif text-[17px] font-bold mt-1 truncate" style={{ color: INK }}>
                  {targetCourse.title}
                </p>
                <p className="font-sans text-[12px] mt-0.5" style={{ color: INK_MUTE }}>
                  {targetCourse.institution} · {targetCourse.typicalPoints} pts required
                </p>
              </div>
              <div className="text-right shrink-0">
                {onTarget ? (
                  <Pill bg={STATUS_SOLID_TINT} fg={STATUS_SOLID_DEEP}>On target</Pill>
                ) : (
                  <Pill bg={STATUS_GAP_TINT} fg={STATUS_GAP_DEEP}>{targetCourse.typicalPoints - currentPoints}pt gap</Pill>
                )}
              </div>
            </div>
          </EditorialCard>
        );
      })()}

      {/* ── Subject status table ── */}
      <section>
        <SectionHeader overline="The slate" title="Subject status" rule />
        <div className="mt-3">
          <EditorialCard tone="soft" padded={false}>
            {[...subjectBudgets].sort((a, b) => b.gap - a.gap).map((s, sIdx) => {
              const idx = subjects.findIndex(sub => sub.subjectName === s.subjectName);
              const rawHex = getDistinctSubjectHex(s.subjectName, idx >= 0 ? idx : sIdx);
              const hex = mutedSubjectHex(rawHex, 0.22);
              const isLast = sIdx === subjectBudgets.length - 1;
              const onTarget = s.gap <= 0;
              return (
                <div
                  key={s.subjectName}
                  className="px-5 py-2"
                  style={{
                    borderBottom: isLast ? 'none' : `1px solid ${INK}10`,
                  }}
                >
                  <div className="flex items-center gap-3">
                    {/* refined subject marker — outlined dot */}
                    <span
                      className="shrink-0"
                      style={{
                        width: 12, height: 12, borderRadius: '50%',
                        background: hex,
                        border: `1px solid ${INK}33`,
                      }}
                    />
                    <span className="font-serif text-[15px] font-semibold flex-1 min-w-0 truncate"
                          style={{ color: INK }}>
                      {s.subjectName}
                    </span>
                    <span className="font-mono text-[11px] tabular-nums hidden sm:inline" style={{ color: INK_MUTE }}>
                      {s.latestGrade} → {s.targetGrade}
                    </span>
                    {onTarget
                      ? <Pill bg={STATUS_SOLID_TINT} fg={STATUS_SOLID_DEEP}>On target</Pill>
                      : <Pill bg={STATUS_GAP_TINT} fg={STATUS_GAP_DEEP}>{s.gap}pt gap</Pill>}
                  </div>

                  <div className="flex items-center gap-3 mt-1 ml-[24px]">
                    <div className="flex-1">
                      <MutedProgress value={s.pct} color={hex} height={4} />
                    </div>
                    <span className="font-mono text-[10px] tabular-nums shrink-0" style={{ color: INK_FAINT }}>
                      {Math.round(s.hoursStudied)}h / {Math.round(s.totalHours)}h
                    </span>
                  </div>
                </div>
              );
            })}
          </EditorialCard>
        </div>
      </section>
    </div>
  );
};

export default CountdownPanel;
