/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useMemo } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown, Minus, Users } from 'lucide-react';
import { GCStudentFullData } from './gcTypes';

const MotionDiv = motion.div as any;
const CUSTOM_EASE = [0.16, 1, 0.3, 1] as const;

// ─── Grade conversion (Irish system only) ──────────────────────────────────

const GRADE_POINTS: Record<string, number> = {
  'H1': 100, 'H2': 88, 'H3': 77, 'H4': 66, 'H5': 56, 'H6': 46, 'H7': 37, 'H8': 0,
  'O1': 56, 'O2': 46, 'O3': 37, 'O4': 28, 'O5': 20, 'O6': 12, 'O7': 0, 'O8': 0,
};

function gradeToNumeric(grade: string): number | null {
  return GRADE_POINTS[grade] ?? null;
}

function numericToGrade(points: number, isHigher: boolean): string {
  const prefix = isHigher ? 'H' : 'O';
  const grades = isHigher
    ? [['H1',100],['H2',88],['H3',77],['H4',66],['H5',56],['H6',46],['H7',37],['H8',0]] as const
    : [['O1',56],['O2',46],['O3',37],['O4',28],['O5',20],['O6',12],['O7',0],['O8',0]] as const;
  for (const [grade, pts] of grades) {
    if (points >= pts) return grade;
  }
  return `${prefix}8`;
}

// ─── Trend calculation ─────────────────────────────────────────────────────

type Trend = 'improving' | 'stable' | 'declining';

function computeTrend(current: number, previous: number, threshold: number = 5): Trend {
  const diff = current - previous;
  if (diff >= threshold) return 'improving';
  if (diff <= -threshold) return 'declining';
  return 'stable';
}

// ─── Component ──────────────────────────────────────────────────────────────

interface SubjectHealthPanelProps {
  studentData: GCStudentFullData[];
}

interface SubjectHealth {
  subject: string;
  studentCount: number;
  avgGradePoints: number;
  avgGradeLabel: string;
  gradeTrend: Trend;
  avgConfidence: number | null;
  confidenceTrend: Trend | null;
  isHigherLevel: boolean;
}

export const SubjectHealthPanel: React.FC<SubjectHealthPanelProps> = ({ studentData }) => {
  const subjectHealthData = useMemo(() => {
    const now = new Date();
    const thisMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
    const lastMonthDate = new Date(now.getFullYear(), now.getMonth() - 1, 1);
    const lastMonth = `${lastMonthDate.getFullYear()}-${String(lastMonthDate.getMonth() + 1).padStart(2, '0')}`;

    // Aggregate mock results per subject
    const subjectMocks: Record<string, { thisMonth: number[]; lastMonth: number[]; isHigher: boolean; studentUids: Set<string> }> = {};
    // Aggregate debrief confidence per subject
    const subjectConfidence: Record<string, { thisMonth: number[]; lastMonth: number[] }> = {};

    for (const student of studentData) {
      // Mock results
      const mocks = student.mockResults || [];
      for (const mock of mocks) {
        const pts = gradeToNumeric(mock.grade);
        if (pts === null) continue;
        const mockMonth = mock.date?.slice(0, 7);
        if (!mockMonth) continue;

        if (!subjectMocks[mock.subject]) {
          subjectMocks[mock.subject] = { thisMonth: [], lastMonth: [], isHigher: mock.grade.startsWith('H'), studentUids: new Set() };
        }
        subjectMocks[mock.subject].studentUids.add(student.user.uid);
        if (mockMonth === thisMonth) subjectMocks[mock.subject].thisMonth.push(pts);
        else if (mockMonth === lastMonth) subjectMocks[mock.subject].lastMonth.push(pts);
      }

      // Debrief confidence
      const debriefs = student.recentDebriefs || [];
      for (const debrief of debriefs) {
        if (!debrief.date) continue;
        const debriefMonth = debrief.date.slice(0, 7); // "YYYY-MM"
        const confidence = (debrief as any).confidenceAfter;
        if (typeof confidence !== 'number') continue;

        if (!subjectConfidence[debrief.subject]) {
          subjectConfidence[debrief.subject] = { thisMonth: [], lastMonth: [] };
        }
        if (debriefMonth === thisMonth) subjectConfidence[debrief.subject].thisMonth.push(confidence);
        else if (debriefMonth === lastMonth) subjectConfidence[debrief.subject].lastMonth.push(confidence);
      }
    }

    // Build health data per subject (only subjects with 3+ students)
    const results: SubjectHealth[] = [];
    for (const [subject, data] of Object.entries(subjectMocks)) {
      if (data.studentUids.size < 3) continue;

      const allMocks = [...data.thisMonth, ...data.lastMonth];
      if (allMocks.length === 0) continue;

      const avg = (arr: number[]) => arr.length > 0 ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
      const currentAvg = data.thisMonth.length > 0 ? avg(data.thisMonth) : avg(allMocks);
      const prevAvg = data.lastMonth.length > 0 ? avg(data.lastMonth) : currentAvg;
      const gradeTrend = data.thisMonth.length > 0 && data.lastMonth.length > 0
        ? computeTrend(currentAvg, prevAvg)
        : 'stable';

      // Confidence
      const conf = subjectConfidence[subject];
      let avgConfidence: number | null = null;
      let confidenceTrend: Trend | null = null;
      if (conf) {
        const allConf = [...conf.thisMonth, ...conf.lastMonth];
        if (allConf.length > 0) {
          avgConfidence = conf.thisMonth.length > 0 ? avg(conf.thisMonth) : avg(allConf);
          if (conf.thisMonth.length > 0 && conf.lastMonth.length > 0) {
            confidenceTrend = computeTrend(avg(conf.thisMonth), avg(conf.lastMonth), 0.5);
          }
        }
      }

      results.push({
        subject,
        studentCount: data.studentUids.size,
        avgGradePoints: currentAvg,
        avgGradeLabel: numericToGrade(currentAvg, data.isHigher),
        gradeTrend,
        avgConfidence,
        confidenceTrend,
        isHigherLevel: data.isHigher,
      });
    }

    return results.sort((a, b) => a.subject.localeCompare(b.subject));
  }, [studentData]);

  if (subjectHealthData.length === 0) return null;

  const TrendIcon: React.FC<{ trend: Trend | null }> = ({ trend }) => {
    if (trend === 'improving') return <TrendingUp size={14} className="text-emerald-500" />;
    if (trend === 'declining') return <TrendingDown size={14} className="text-rose-500" />;
    return <Minus size={14} className="text-zinc-400" />;
  };

  return (
    <MotionDiv
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: CUSTOM_EASE }}
      className="rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-zinc-800/60 shadow-[0_1px_3px_rgba(0,0,0,0.04)] hover:shadow-[0_4px_12px_rgba(0,0,0,0.06)] transition-shadow overflow-hidden"
    >
      {/* Header */}
      <div className="flex items-center justify-between px-5 py-3.5 border-b border-zinc-100 dark:border-zinc-800/60">
        <div className="flex items-center gap-2.5">
          <TrendingUp size={16} className="text-[var(--accent-hex)]" />
          <span className="text-sm font-semibold text-zinc-800 dark:text-white">Subject Health</span>
        </div>
        <span className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">
          {subjectHealthData.length} subjects
        </span>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-px bg-zinc-100 dark:bg-zinc-800/40">
        {subjectHealthData.map((item) => (
          <div
            key={item.subject}
            className="bg-white dark:bg-zinc-900 p-4"
          >
            {/* Subject name + student count */}
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-sm font-semibold text-zinc-800 dark:text-white truncate">{item.subject}</h4>
              <span className="flex items-center gap-1 text-[10px] font-medium text-zinc-400 dark:text-zinc-500 shrink-0 ml-2">
                <Users size={10} />
                {item.studentCount}
              </span>
            </div>

            {/* Mock grade trend */}
            <div className="flex items-center justify-between mb-2">
              <span className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">Mock Avg</span>
              <div className="flex items-center gap-1.5">
                <span className="text-sm font-bold text-zinc-700 dark:text-zinc-200">{item.avgGradeLabel}</span>
                <TrendIcon trend={item.gradeTrend} />
              </div>
            </div>

            {/* Confidence trend */}
            {item.avgConfidence !== null && (
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">Confidence</span>
                <div className="flex items-center gap-1.5">
                  <span className="text-sm font-bold text-zinc-700 dark:text-zinc-200">{item.avgConfidence.toFixed(1)}/5</span>
                  <TrendIcon trend={item.confidenceTrend} />
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </MotionDiv>
  );
};
