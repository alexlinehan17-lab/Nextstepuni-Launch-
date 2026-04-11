/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useMemo } from 'react';
import { motion } from 'framer-motion';

import { type StudentSubjectProfile } from '../subjectData';
import { getDistinctSubjectHex } from '../../studySessionData';
import { type MockResult, gradeToPoints } from './warRoomShared';
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
  tabRow?: React.ReactNode;
  phaseColor?: string;
}

const CountdownPanel: React.FC<CountdownPanelProps> = ({ daysUntilExam, subjects, allocations, weeksUntilExam, hoursStudiedMap, blockDuration, mockResults, targetCourse, currentPoints, tabRow, phaseColor: phaseColorProp }) => {
  // Derive effective current grade from latest mock results (falls back to profile)
  const latestGradeMap = useMemo(() => {
    const map: Record<string, string> = {};
    const sorted = [...mockResults].filter(r => r.grade && r.date).sort((a, b) => (a.date ?? '').localeCompare(b.date ?? ''));
    for (const r of sorted) {
      map[r.subject] = r.grade; // last one wins (sorted ascending)
    }
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

  const phaseColor = phaseColorProp || (daysUntilExam > 180 ? '#2A7D6F' : daysUntilExam > 90 ? '#D4891C' : daysUntilExam > 30 ? '#D4564E' : '#C5981A');

  return (
    <div>
      {/* ── Full-bleed hero with integrated tabs ── */}
      <div
        className="relative overflow-hidden mb-5"
        style={{
          backgroundColor: phaseColor,
          position: 'relative',
          left: '50%',
          right: '50%',
          marginLeft: '-50vw',
          marginRight: '-50vw',
          width: '100vw',
        }}
      >
        {/* Decorative blobs */}
        <div className="absolute pointer-events-none" style={{ top: -50, right: -40, width: 240, height: 240, borderRadius: '50%', background: 'rgba(255,255,255,0.07)' }} />
        <div className="absolute pointer-events-none" style={{ bottom: -30, left: -50, width: 180, height: 180, borderRadius: '50%', background: 'rgba(0,0,0,0.05)' }} />
        <div className="absolute pointer-events-none" style={{ top: 30, right: 80, width: 60, height: 60, borderRadius: '50%', background: 'rgba(255,255,255,0.05)' }} />

        <div className="relative z-10">
          {/* Tab row — inside the colour field, padded below fixed nav */}
          <div className="pt-16 md:pt-20 pb-2">
            {tabRow}
          </div>

          {/* Countdown hero */}
          <div className="text-center py-6 px-6">
            <motion.p
              className="font-apercu font-black tabular-nums"
              style={{ fontSize: 'clamp(96px, 20vw, 140px)', color: '#fff', lineHeight: 1, letterSpacing: '-0.03em' }}
              initial={{ scale: 0.85, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
            >
              {daysUntilExam}
            </motion.p>
            <p className="text-base font-medium mt-1" style={{ color: 'rgba(255,255,255,0.7)' }}>days until exams</p>
            <div className="flex items-center justify-center gap-4 mt-2 text-xs" style={{ color: 'rgba(255,255,255,0.45)' }}>
              <span>{Math.round(totalStudied)}h studied</span>
              <span className="w-1 h-1 rounded-full" style={{ backgroundColor: 'rgba(255,255,255,0.3)' }} />
              <span>~{Math.round(totalRemaining)}h remaining</span>
            </div>
          </div>
        </div>

        {/* Wavy bottom edge */}
        <div className="absolute bottom-0 left-0 right-0" style={{ transform: 'translateY(1px)' }}>
          <svg viewBox="0 0 1440 40" preserveAspectRatio="none" className="block w-full" style={{ height: 36 }}>
            <path d="M0,20 C360,40 720,8 1080,28 C1260,38 1360,18 1440,24 L1440,40 L0,40 Z" className="fill-[#FDF8F0] dark:fill-zinc-950" />
          </svg>
        </div>
      </div>

      {/* ── Target Course banner ── */}
      {targetCourse && currentPoints !== undefined && (
        <div className="px-4 py-3 mb-4 rounded-2xl bg-[#FEFDFB] dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800" style={{ boxShadow: '0 1px 3px rgba(28,25,23,0.04)' }}>
          <div className="flex items-center justify-between">
            <div className="min-w-0">
              <p className="text-[10px] font-bold uppercase tracking-widest mb-0.5 text-[#A8A29E] dark:text-zinc-500">Target Course</p>
              <p className="text-sm font-semibold truncate text-[#1C1917] dark:text-white">{targetCourse.title}</p>
              <p className="text-[10px] text-[#A8A29E] dark:text-zinc-500">{targetCourse.institution} · {targetCourse.typicalPoints} pts required</p>
            </div>
            <div className="text-right shrink-0 ml-3">
              {currentPoints >= targetCourse.typicalPoints ? (
                <span className="text-[10px] font-bold px-2.5 py-1 rounded-full" style={{ backgroundColor: '#DEF7EC', color: '#276749' }}>On target</span>
              ) : (
                <span className="text-[10px] font-bold px-2.5 py-1 rounded-full" style={{ backgroundColor: '#FDE8E8', color: '#C53030' }}>
                  {targetCourse.typicalPoints - currentPoints}pt gap
                </span>
              )}
            </div>
          </div>
        </div>
      )}

      {/* ── Subject status — tight Mercury rows ── */}
      <div>
        <p className="text-[10px] font-bold uppercase tracking-widest mb-2 text-[#A8A29E] dark:text-zinc-500">Subject Status</p>
        <div className="rounded-2xl overflow-hidden bg-[#FEFDFB] dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800" style={{ boxShadow: '0 1px 3px rgba(28,25,23,0.04)' }}>
          {[...subjectBudgets].sort((a, b) => b.gap - a.gap).map((s, sIdx) => {
            const hex = getDistinctSubjectHex(s.subjectName, subjects.findIndex(sub => sub.subjectName === s.subjectName) ?? sIdx);
            const isLast = sIdx === subjectBudgets.length - 1;
            return (
              <div
                key={s.subjectName}
                className={`px-4 py-2 ${isLast ? '' : 'border-b border-[#F0EFED] dark:border-zinc-800'}`}
              >
                <div className="flex items-center gap-2.5">
                  <div className="w-3 h-3 rounded-full shrink-0" style={{ backgroundColor: hex }} />
                  <span className="text-[13px] font-semibold flex-1 min-w-0 truncate text-[#1C1917] dark:text-white">{s.subjectName}</span>
                  <span className="text-[10px] tabular-nums text-[#A8A29E] dark:text-zinc-500">{s.latestGrade} → {s.targetGrade}</span>
                  {s.gap <= 0 ? (
                    <span className="text-[9px] font-bold px-2 py-0.5 rounded-full" style={{ backgroundColor: '#DEF7EC', color: '#276749' }}>On target</span>
                  ) : (
                    <span className="text-[9px] font-bold px-2 py-0.5 rounded-full" style={{ backgroundColor: '#FDE8E8', color: '#C53030' }}>{s.gap}pt gap</span>
                  )}
                </div>
                <div className="flex items-center gap-2.5 mt-1 ml-[22px]">
                  <div className="flex-1 h-[6px] rounded-full overflow-hidden bg-[#EDEBE8] dark:bg-zinc-700">
                    <motion.div
                      className="h-full rounded-full"
                      style={{ backgroundColor: hex }}
                      initial={{ width: 0 }}
                      animate={{ width: `${s.pct}%` }}
                      transition={{ duration: 0.6, delay: sIdx * 0.04, ease: [0.16, 1, 0.3, 1] }}
                    />
                  </div>
                  <span className="text-[9px] tabular-nums shrink-0" style={{ color: '#C4C0BC' }}>
                    {Math.round(s.hoursStudied)}h / {Math.round(s.totalHours)}h
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default CountdownPanel;
