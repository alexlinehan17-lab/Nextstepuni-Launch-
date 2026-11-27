/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useMemo, useState } from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { type GCStudentFullData } from './gcTypes';
import SubjectAvatar from '../SubjectAvatar';
import { TextButton } from '../ui/Button';
import { List, Row } from '../ui/List';
import { Sheet } from '../ui/Sheet';
import './gc-8a.css';

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
  /** The laptop layout (four to a row); a phone shows the first three as rows, with All. */
  wide?: boolean;
}

interface SubjectHealth {
  subject: string;
  /** The subject alone, for its character and its row (the display; `subject` keys the list). */
  subjectName: string;
  studentCount: number;
  avgGradePoints: number;
  avgGradeLabel: string;
  gradeTrend: Trend;
  avgConfidence: number | null;
  confidenceTrend: Trend | null;
  isHigherLevel: boolean;
}

export const SubjectHealthPanel: React.FC<SubjectHealthPanelProps> = ({ studentData, wide = true }) => {
  const [allOpen, setAllOpen] = useState(false);
  const subjectHealthData = useMemo(() => {
    const now = new Date();
    const thisMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
    const lastMonthDate = new Date(now.getFullYear(), now.getMonth() - 1, 1);
    const lastMonth = `${lastMonthDate.getFullYear()}-${String(lastMonthDate.getMonth() + 1).padStart(2, '0')}`;

    // Aggregate mock results per subject
    // Keyed `${subject}|H` / `${subject}|O` — see the level split below.
    const subjectMocks: Record<string, { subject: string; thisMonth: number[]; lastMonth: number[]; isHigher: boolean; studentUids: Set<string> }> = {};
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

        // Key by subject AND level. `isHigher` used to latch from the first
        // mock seen for a subject, so Higher and Ordinary results were averaged
        // into one number and labelled with whichever level happened to arrive
        // first — an H1 and an O1 are not the same grade. This never surfaced
        // because no mock data reached this panel at all (the GC was reading a
        // dead field); it goes live the moment that is fixed, so split it now.
        const isHigher = mock.grade.startsWith('H');
        const key = `${mock.subject}|${isHigher ? 'H' : 'O'}`;
        if (!subjectMocks[key]) {
          subjectMocks[key] = { subject: mock.subject, thisMonth: [], lastMonth: [], isHigher, studentUids: new Set() };
        }
        subjectMocks[key].studentUids.add(student.user.uid);
        if (mockMonth === thisMonth) subjectMocks[key].thisMonth.push(pts);
        else if (mockMonth === lastMonth) subjectMocks[key].lastMonth.push(pts);
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
    for (const data of Object.values(subjectMocks)) {
      if (data.studentUids.size < 3) continue;
      const subject = data.subject;

      const allMocks = [...data.thisMonth, ...data.lastMonth];
      if (allMocks.length === 0) continue;

      const avg = (arr: number[]) => arr.length > 0 ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
      const currentAvg = data.thisMonth.length > 0 ? avg(data.thisMonth) : avg(allMocks);
      const prevAvg = data.lastMonth.length > 0 ? avg(data.lastMonth) : currentAvg;
      const gradeTrend = data.thisMonth.length > 0 && data.lastMonth.length > 0
        ? computeTrend(currentAvg, prevAvg)
        : 'stable';

      // Confidence
      // Confidence is not level-split (debriefs carry no level), so both the
      // HL and OL card for a subject show the same subject-wide confidence.
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
        subject: `${subject} · ${data.isHigher ? 'HL' : 'OL'}`,
        subjectName: subject,
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

  // Each trend drawn and said: up in green, down in ink, level as a dash.
  const TrendIcon: React.FC<{ trend: Trend | null }> = ({ trend }) => {
    if (trend === 'improving') return <TrendingUp className="ui-icon gc8-up" width={16} height={16} strokeWidth={2} aria-label="Up on last month" />;
    if (trend === 'declining') return <TrendingDown className="ui-icon gc8-down" width={16} height={16} strokeWidth={2} aria-label="Down on last month" />;
    return <Minus className="ui-icon gc8-dim" width={16} height={16} strokeWidth={2} aria-label="Level with last month" />;
  };
  const level = (item: SubjectHealth) => (item.isHigherLevel ? 'Higher' : 'Ordinary');
  const students = (n: number) => `${n} ${n === 1 ? 'student' : 'students'}`;
  const phoneRow = (item: SubjectHealth) => (
    <Row
      key={item.subject}
      art={<SubjectAvatar bare subject={item.subjectName} className="gc8-art" />}
      title={`${item.subjectName} · ${level(item)}`}
      meta={`${students(item.studentCount)} · ${item.avgConfidence !== null
        ? `confidence ${item.avgConfidence.toFixed(1)} of 5`
        : item.gradeTrend === 'declining' ? 'down on last month' : item.gradeTrend === 'improving' ? 'up on last month' : 'mock average'}`}
      trailing={<span className="gc8-g">{item.avgGradeLabel}<TrendIcon trend={item.gradeTrend} /></span>}
    />
  );

  return (
    <section className="gc8-sec" aria-labelledby="gc8-health">
      <div className="gc8-sechead">
        <h2 id="gc8-health" className="gc8-h">Subject health</h2>
        <span className="gc8-meta">{wide
          ? `${subjectHealthData.length} subjects · average mock grade, confidence out of 5 where given, and the change on last month`
          : `${subjectHealthData.length} subjects`}</span>
      </div>
      {wide ? (
        <div className="gc8-health">
          {subjectHealthData.map(item => (
            <div key={item.subject} className="gc8-hc">
              <SubjectAvatar bare subject={item.subjectName} className="gc8-art gc8-art--32" />
              <span className="gc8-hc-copy">
                <span className="gc8-person">{item.subjectName}</span>
                <span className="gc8-meta">{level(item)} · {students(item.studentCount)}</span>
              </span>
              <span className="gc8-gcol">
                <span className="gc8-g">{item.avgGradeLabel}<TrendIcon trend={item.gradeTrend} /></span>
                {item.avgConfidence !== null && (
                  <span className="gc8-meta gc8-trend">{item.avgConfidence.toFixed(1)} of 5{item.confidenceTrend ? <TrendIcon trend={item.confidenceTrend} /> : null}</span>
                )}
              </span>
            </div>
          ))}
        </div>
      ) : (
        <>
          <List className="gc8-list">{subjectHealthData.slice(0, 3).map(phoneRow)}</List>
          {subjectHealthData.length > 3 && (
            <TextButton className="gc8-more" arrow="forward" onClick={() => setAllOpen(true)}>{`All ${subjectHealthData.length} subjects`}</TextButton>
          )}
          <Sheet open={allOpen} title="Subject health" onClose={() => setAllOpen(false)}>
            <List className="gc8-list">{subjectHealthData.map(phoneRow)}</List>
          </Sheet>
        </>
      )}
    </section>
  );
};
