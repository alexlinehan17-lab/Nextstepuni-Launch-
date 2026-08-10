/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect, useMemo, useRef, useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { Plus, X } from 'lucide-react';
import {
  type StudentSubjectProfile, type Grade,
  getPointsForGrade, getGradesForLevel,
  LC_SUBJECTS,
} from '../subjectData';
import { getSubjectColor, getDistinctSubjectHex } from '../../studySessionData';
import { type useMockResults } from '../../hooks/useMockResults';
import { parseDateKey, toDateKey } from '../../utils/weekDates';
import {
  type MockResult,
  PAPER, INK, INK_SOFT, INK_MUTE, ACCENT,
  mutedSubjectHex,
} from './warRoomShared';
import { fieldClass, fieldStyle } from './warRoomPrimitives';

// ── Constants ───────────────────────────────────────────────

const MOCK_PRESETS = ['Christmas Mocks', 'February Mocks', 'Pre-LC Mocks', 'Practice Exam'];

interface MockFeedback {
  improved: { subject: string; from: string; to: string; ptsDiff: number }[];
  declined: { subject: string; from: string; to: string; ptsDiff: number }[];
  unchanged: string[];
  totalPtsDiff: number;
  previousLabel: string;
  previousTotal: number;
  currentTotal: number;
}

interface TrajectoryPanelProps {
  subjects: StudentSubjectProfile['subjects'];
  mockResults: MockResult[];
  mockResultsHook: ReturnType<typeof useMockResults>;
  daysUntilExam: number;
}

// ── Refined chart palette ───────────────────────────────────
// Existing distinct hex per subject, but blended toward paper for restraint.

function getChartColor(name: string, fallbackIdx: number): string {
  return mutedSubjectHex(getDistinctSubjectHex(name, fallbackIdx), 0.18);
}

function isMathsSubject(subjectName: string): boolean {
  return LC_SUBJECTS.find(subject => subject.name === subjectName)?.isMaths ?? false;
}

function pointsForSubject(subjectName: string, grade: string | undefined | null): number {
  return getPointsForGrade(grade as Grade | undefined, isMathsSubject(subjectName));
}

function bestSixTotal(entries: ReadonlyArray<{ subjectName: string; grade?: string | null }>): number {
  return entries
    .map(entry => pointsForSubject(entry.subjectName, entry.grade))
    .sort((a, b) => b - a)
    .slice(0, 6)
    .reduce((sum, points) => sum + points, 0);
}

function formatResultDate(dateKey: string): string {
  const date = parseDateKey(dateKey);
  return Number.isNaN(date.getTime())
    ? dateKey
    : date.toLocaleDateString('en-IE', { day: 'numeric', month: 'short', year: 'numeric' });
}

interface TrajectoryChartProps {
  subjects: StudentSubjectProfile['subjects'];
  resultsBySubject: Record<string, MockResult[]>;
}

const TrajectoryChart: React.FC<TrajectoryChartProps> = ({ subjects, resultsBySubject }) => {
  const [hoveredSubject, setHoveredSubject] = useState<string | null>(null);
  const [hoveredDot, setHoveredDot] = useState<{ id: string; cx: number; cy: number; label: string } | null>(null);

  const W = 520;
  const H = 320;
  const PAD = { top: 20, right: 50, bottom: 35, left: 40 };
  const plotW = W - PAD.left - PAD.right;
  const plotH = H - PAD.top - PAD.bottom;

  const subjectsWithResults = subjects.filter(subject => resultsBySubject[subject.subjectName]?.length);
  const allResults = subjectsWithResults.flatMap(subject => resultsBySubject[subject.subjectName] ?? []);
  if (allResults.length === 0) return null;

  const dates = allResults.map(result => parseDateKey(result.date).getTime()).filter(time => !Number.isNaN(time));
  if (dates.length === 0) return null;
  const minDate = Math.min(...dates);
  const maxDate = Math.max(...dates);
  const dateRange = maxDate - minDate || 86400000;

  const maxPts = subjectsWithResults.some(subject => isMathsSubject(subject.subjectName)) ? 125 : 100;
  const yLabels = maxPts === 125 ? [0, 25, 50, 75, 100, 125] : [0, 25, 50, 75, 100];

  const scaleX = (date: string) => {
    const t = parseDateKey(date).getTime();
    return PAD.left + ((t - minDate) / dateRange) * plotW;
  };
  const scaleY = (pts: number) => PAD.top + plotH - (pts / maxPts) * plotH;

  const subjectIndexMap: Record<string, number> = {};
  subjects.forEach((s, i) => { subjectIndexMap[s.subjectName] = i; });

  const uniqueDates = [...new Set(allResults.map(r => r.date))].sort();
  const chronologicalResults = subjectsWithResults
    .flatMap(subject => (resultsBySubject[subject.subjectName] ?? []).map(result => ({
      ...result,
      points: pointsForSubject(subject.subjectName, result.grade),
    })))
    .sort((a, b) => a.date.localeCompare(b.date) || a.subject.localeCompare(b.subject));

  return (
    <div className="space-y-3">
      <div
        className="overflow-x-auto pb-1 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--outline-strong)]"
        role="region"
        aria-label="Scrollable mock results chart"
        tabIndex={0}
      >
        <svg
          viewBox={`0 0 ${W} ${H}`}
          className="min-w-[520px] w-full"
          style={{ maxHeight: 340 }}
          role="img"
          aria-label="Mock results over time by subject. A chronological data table follows."
          onMouseLeave={() => { setHoveredSubject(null); setHoveredDot(null); }}
        >
          <title>Mock results over time by subject</title>
          {yLabels.map(pts => (
            <g key={pts}>
              <line x1={PAD.left} y1={scaleY(pts)} x2={W - PAD.right} y2={scaleY(pts)}
                    stroke={INK} strokeOpacity={0.08} strokeWidth="0.5" />
              <text x={PAD.left - 6} y={scaleY(pts) + 3} textAnchor="end"
                    fill={INK_MUTE} fontSize="9">{pts}</text>
            </g>
          ))}

          {uniqueDates.map(date => (
            <text key={date} x={scaleX(date)} y={H - 8} textAnchor="middle"
                  fill={INK_MUTE} fontSize="9">
              {parseDateKey(date).toLocaleDateString('en-IE', { day: 'numeric', month: 'short' })}
            </text>
          ))}

          {subjectsWithResults.map(subject => {
            const results = resultsBySubject[subject.subjectName];
            if (!results || results.length < 1) return null;
            const hexColor = getChartColor(subject.subjectName, subjectIndexMap[subject.subjectName] ?? 0);
            const isHovered = hoveredSubject === subject.subjectName;
            const isFaded = hoveredSubject !== null && !isHovered;

            const points = results.map(result => ({
              x: scaleX(result.date),
              y: scaleY(pointsForSubject(subject.subjectName, result.grade)),
              grade: result.grade,
              date: result.date,
              id: result.id,
              points: pointsForSubject(subject.subjectName, result.grade),
            }));
            const polyPoints = points.map(point => `${point.x},${point.y}`).join(' ');

            return (
              <g key={subject.subjectName} style={{ opacity: isFaded ? 0.12 : 1, transition: 'opacity 0.2s' }}>
                {points.length > 1 && (
                  <>
                    <polyline points={polyPoints} fill="none" stroke="transparent" strokeWidth="14"
                              strokeLinecap="round" onMouseEnter={() => setHoveredSubject(subject.subjectName)}
                              style={{ cursor: 'pointer' }} />
                    <polyline points={polyPoints} fill="none" stroke={hexColor}
                              strokeWidth={isHovered ? 2.6 : 1.8}
                              strokeLinecap="round" strokeLinejoin="round"
                              style={{ pointerEvents: 'none' }} />
                  </>
                )}
                {points.map(point => {
                  const label = `${subject.subjectName}: ${point.grade} (${point.points} pts) — ${formatResultDate(point.date)}`;
                  const isDotHovered = hoveredDot?.id === point.id;
                  return (
                    <circle
                      key={point.id}
                      cx={point.x} cy={point.y} r={isDotHovered ? 5.5 : 3.5}
                      fill={hexColor}
                      stroke={PAPER}
                      strokeWidth="2"
                      style={{ cursor: 'pointer', transition: 'r 0.15s' }}
                      onMouseEnter={() => setHoveredDot({ id: point.id, cx: point.x, cy: point.y, label })}
                      onMouseLeave={() => setHoveredDot(null)}
                    />
                  );
                })}
              </g>
            );
          })}

          {hoveredDot && (() => {
            const tooltipW = Math.max(hoveredDot.label.length * 5 + 16, 80);
            const tx = Math.min(Math.max(5, hoveredDot.cx - tooltipW / 2), W - tooltipW - 5);
            const ty = hoveredDot.cy > 40 ? hoveredDot.cy - 24 : hoveredDot.cy + 12;
            return (
              <g style={{ pointerEvents: 'none' }}>
                <rect x={tx} y={ty} width={tooltipW} height={18} rx="4" fill={INK} />
                <text x={tx + tooltipW / 2} y={ty + 13} fontSize="8" fill={PAPER} fontWeight="600" textAnchor="middle">{hoveredDot.label}</text>
              </g>
            );
          })()}
        </svg>
      </div>

      {/* Legend */}
      {subjectsWithResults.length > 0 && (
        <div className="flex flex-wrap gap-x-4 gap-y-1.5 px-1">
          {subjectsWithResults.map(s => {
            const hexColor = getChartColor(s.subjectName, subjectIndexMap[s.subjectName] ?? 0);
            const isHovered = hoveredSubject === s.subjectName;
            return (
              <div
                key={s.subjectName}
                className="flex items-center gap-1.5 cursor-pointer transition-opacity"
                style={{ opacity: hoveredSubject && !isHovered ? 0.3 : 1 }}
                onMouseEnter={() => setHoveredSubject(s.subjectName)}
                onMouseLeave={() => setHoveredSubject(null)}
              >
                <span className="w-2.5 h-2.5 rounded-full shrink-0"
                      style={{ background: hexColor, border: `1px solid color-mix(in srgb, var(--ink-primary) 20%, transparent)` }} />
                <span className="font-sans text-[11px] font-semibold" style={{ color: INK_SOFT }}>{s.subjectName}</span>
              </div>
            );
          })}
        </div>
      )}

      <table className="sr-only">
        <caption>Chronological mock results</caption>
        <thead>
          <tr><th scope="col">Date</th><th scope="col">Subject</th><th scope="col">Grade</th><th scope="col">CAO points</th></tr>
        </thead>
        <tbody>
          {chronologicalResults.map(result => (
            <tr key={result.id}>
              <td>{formatResultDate(result.date)}</td>
              <th scope="row">{result.subject}</th>
              <td>{result.grade}</td>
              <td>{result.points}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

// ── TrajectoryPanel ─────────────────────────────────────────

const TrajectoryPanel: React.FC<TrajectoryPanelProps> = ({ subjects, mockResults, mockResultsHook }) => {
  const gradeSubjects = useMemo(
    () => subjects.filter(subject => subject.level === 'higher' || subject.level === 'ordinary'),
    [subjects],
  );
  const [showAddForm, setShowAddForm] = useState<false | 'single' | 'full'>(false);
  const [formSubject, setFormSubject] = useState(
    () => subjects.find(subject => subject.level === 'higher' || subject.level === 'ordinary')?.subjectName ?? '',
  );
  const [formGrade, setFormGrade] = useState('');
  const [formDate, setFormDate] = useState(() => toDateKey(new Date()));
  const [formLabel, setFormLabel] = useState('');
  const [fullMockGrades, setFullMockGrades] = useState<Record<string, string>>({});
  const [fullMockLabel, setFullMockLabel] = useState('');
  const [fullMockDate, setFullMockDate] = useState(() => toDateKey(new Date()));
  const [mockFeedback, setMockFeedback] = useState<MockFeedback | null>(null);
  const fullMockTriggerRef = useRef<HTMLButtonElement>(null);
  const singleResultTriggerRef = useRef<HTMLButtonElement>(null);
  const fullMockFirstFieldRef = useRef<HTMLInputElement>(null);
  const singleResultFirstFieldRef = useRef<HTMLSelectElement>(null);
  const lastFormTriggerRef = useRef<'full' | 'single'>('single');
  const restoreFormTriggerRef = useRef(false);

  const formSubjectData = gradeSubjects.find(subject => subject.subjectName === formSubject);
  const gradeOptions = formSubjectData ? getGradesForLevel(formSubjectData.level) : [];
  const canSaveSingleResult = Boolean(
    formSubjectData && formDate && formGrade && gradeOptions.includes(formGrade as Grade),
  );

  const gradeForFullMockSubject = (subject: StudentSubjectProfile['subjects'][number]): string => {
    const candidate = fullMockGrades[subject.subjectName] || subject.currentGrade || '';
    return getGradesForLevel(subject.level).includes(candidate as Grade) ? candidate : '';
  };
  const canSaveFullMock = Boolean(
    fullMockDate
      && gradeSubjects.length > 0
      && gradeSubjects.every(subject => Boolean(gradeForFullMockSubject(subject))),
  );

  useEffect(() => {
    const selectedSubject = gradeSubjects.find(subject => subject.subjectName === formSubject);
    if (!selectedSubject) {
      setFormSubject(gradeSubjects[0]?.subjectName ?? '');
      setFormGrade('');
      return;
    }
    if (formGrade && !getGradesForLevel(selectedSubject.level).includes(formGrade as Grade)) {
      setFormGrade('');
    }
  }, [formGrade, formSubject, gradeSubjects]);

  useEffect(() => {
    if (showAddForm === 'full') {
      fullMockFirstFieldRef.current?.focus();
      return;
    }
    if (showAddForm === 'single') {
      singleResultFirstFieldRef.current?.focus();
      return;
    }
    if (!restoreFormTriggerRef.current) return;
    restoreFormTriggerRef.current = false;
    const trigger = lastFormTriggerRef.current === 'full'
      ? fullMockTriggerRef.current
      : singleResultTriggerRef.current;
    trigger?.focus();
  }, [showAddForm]);

  const closeAddForm = () => {
    restoreFormTriggerRef.current = true;
    setShowAddForm(false);
  };

  const initFullMockForm = () => {
    const grades: Record<string, string> = {};
    gradeSubjects.forEach(subject => {
      const currentGrade = subject.currentGrade ?? '';
      grades[subject.subjectName] = getGradesForLevel(subject.level).includes(currentGrade as Grade)
        ? currentGrade
        : '';
    });
    setFullMockGrades(grades);
    setFullMockLabel('');
    setFullMockDate(toDateKey(new Date()));
    lastFormTriggerRef.current = 'full';
    setShowAddForm('full');
  };

  const initSingleResultForm = () => {
    const nextSubject = gradeSubjects.some(subject => subject.subjectName === formSubject)
      ? formSubject
      : gradeSubjects[0]?.subjectName ?? '';
    if (nextSubject !== formSubject) {
      setFormSubject(nextSubject);
      setFormGrade('');
    }
    setFormDate(toDateKey(new Date()));
    lastFormTriggerRef.current = 'single';
    setShowAddForm('single');
  };

  const addResult = () => {
    if (!canSaveSingleResult || !formSubjectData) return;
    mockResultsHook.addMockResult({
      label: formLabel.trim() || 'Single Result',
      date: formDate,
      entries: [{ subjectName: formSubject, grade: formGrade, level: formSubjectData.level }],
      totalPoints: pointsForSubject(formSubject, formGrade),
    });
    setFormGrade('');
    setFormLabel('');
    closeAddForm();
  };

  const addFullMock = () => {
    if (!canSaveFullMock) return;
    const label = fullMockLabel.trim() || 'Mock Exam';

    const entries = gradeSubjects.map(subject => ({
      subjectName: subject.subjectName,
      grade: gradeForFullMockSubject(subject),
      level: subject.level,
    }));
    const totalPoints = bestSixTotal(entries);

    const improved: MockFeedback['improved'] = [];
    const declined: MockFeedback['declined'] = [];
    const unchanged: string[] = [];
    const previousCandidates = [...mockResultsHook.mocks]
      .filter(mock => mock.date <= fullMockDate && mock.entries.length > 1)
      .sort((a, b) => a.date.localeCompare(b.date) || a.timestamp - b.timestamp);
    const previousMock = previousCandidates[previousCandidates.length - 1];

    if (previousMock) {
      const previousEntries = new Map(previousMock.entries.map(entry => [entry.subjectName, entry]));
      for (const entry of entries) {
        const previousEntry = previousEntries.get(entry.subjectName);
        if (!previousEntry?.grade) continue;
        const previousPoints = pointsForSubject(entry.subjectName, previousEntry.grade);
        const currentPoints = pointsForSubject(entry.subjectName, entry.grade);
        const difference = currentPoints - previousPoints;
        if (difference > 0) improved.push({ subject: entry.subjectName, from: previousEntry.grade, to: entry.grade, ptsDiff: difference });
        else if (difference < 0) declined.push({ subject: entry.subjectName, from: previousEntry.grade, to: entry.grade, ptsDiff: difference });
        else unchanged.push(entry.subjectName);
      }
      const currentSubjectNames = new Set(gradeSubjects.map(subject => subject.subjectName));
      const previousTotal = bestSixTotal(
        previousMock.entries.filter(entry => currentSubjectNames.has(entry.subjectName)),
      );
      setMockFeedback({
        improved,
        declined,
        unchanged,
        totalPtsDiff: totalPoints - previousTotal,
        previousLabel: previousMock.label.trim() || formatResultDate(previousMock.date),
        previousTotal,
        currentTotal: totalPoints,
      });
    } else {
      setMockFeedback(null);
    }

    mockResultsHook.addMockResult({ label, date: fullMockDate, entries, totalPoints });
    closeAddForm();
  };

  const _removeResult = (derivedId: string) => {
    for (const mock of mockResultsHook.mocks) {
      if (derivedId.startsWith(mock.id + '-')) {
        mockResultsHook.removeMockResult(mock.id);
        return;
      }
    }
  };

  const resultsBySubject = useMemo(() => {
    const map: Record<string, MockResult[]> = {};
    for (const r of mockResults) {
      if (!r.subject || !r.grade || !r.date) continue;
      if (!map[r.subject]) map[r.subject] = [];
      map[r.subject].push(r);
    }
    for (const key of Object.keys(map)) {
      map[key].sort((a, b) => (a.date ?? '').localeCompare(b.date ?? ''));
    }
    return map;
  }, [mockResults]);

  const chartSubjects = subjects.filter(s => resultsBySubject[s.subjectName]?.length);

  // Buttons
  const primaryBtnStyle: React.CSSProperties = {
    background: ACCENT,
    color: 'var(--ink-on-accent)',
    border: '1px solid var(--outline-strong)',
    borderRadius: 9,
  };
  const ghostBtnStyle: React.CSSProperties = {
    background: PAPER,
    color: INK,
    border: '1px solid var(--outline-strong)',
    borderRadius: 9,
  };
  const buttonClass = 'inline-flex min-h-10 items-center justify-center gap-1.5 px-3 py-2 font-sans text-[12px] font-semibold transition-[background-color,color,opacity] disabled:cursor-not-allowed disabled:opacity-40';

  return (
    <div className="trajectory-panel space-y-6">
      <style>{`
        .trajectory-panel button:focus-visible,
        .trajectory-panel [role='region'][tabindex='0']:focus-visible,
        .trajectory-panel .product-field:focus-visible {
          outline: 2px solid var(--outline-strong) !important;
          outline-offset: 2px !important;
          box-shadow: 0 0 0 2px var(--surface-paper) !important;
        }
      `}</style>
      <header className="flex flex-col gap-4 border-b border-[var(--outline-soft)] pb-4 sm:flex-row sm:items-end sm:justify-between">
        <div className="min-w-0">
          <h3 className="font-sans text-[18px] font-semibold leading-tight" style={{ color: INK }}>
            Mock trajectory
          </h3>
          <p className="mt-1 max-w-xl font-sans text-[12px] leading-relaxed" style={{ color: INK_MUTE }}>
            Log results and compare your latest grades with your targets.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          {showAddForm ? (
            <button
              type="button"
              onClick={closeAddForm}
              className={buttonClass}
              style={ghostBtnStyle}
            >
              <X size={12} aria-hidden="true" /> Cancel
            </button>
          ) : (
            <>
              <button
                ref={fullMockTriggerRef}
                type="button"
                onClick={initFullMockForm}
                className={buttonClass}
                style={primaryBtnStyle}
                aria-controls="trajectory-entry-form"
                aria-expanded="false"
                disabled={gradeSubjects.length === 0}
              >
                <Plus size={12} aria-hidden="true" /> Full mock
              </button>
              <button
                ref={singleResultTriggerRef}
                type="button"
                onClick={initSingleResultForm}
                className={buttonClass}
                style={ghostBtnStyle}
                aria-controls="trajectory-entry-form"
                aria-expanded="false"
                disabled={gradeSubjects.length === 0}
              >
                <Plus size={12} aria-hidden="true" /> Single result
              </button>
            </>
          )}
        </div>
      </header>

      {/* Add-result forms */}
      <AnimatePresence>
        {showAddForm === 'full' && (
          <MotionDiv initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }}
                     exit={{ height: 0, opacity: 0 }} className="overflow-hidden">
            <section
              id="trajectory-entry-form"
              aria-labelledby="full-mock-form-title"
              className="rounded-[12px] border border-[var(--outline-strong)] bg-[var(--surface-paper)] p-4 sm:p-5"
            >
              <h3 id="full-mock-form-title" className="font-sans text-[14px] font-semibold" style={{ color: INK }}>
                Log a full mock
              </h3>
              <p className="mt-1 font-sans text-[12px]" style={{ color: INK_MUTE }}>
                Add one grade for each subject.
              </p>
              <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2">
                <div>
                  <label htmlFor="full-mock-label" className="font-sans text-[10px] font-bold uppercase tracking-[0.16em]"
                         style={{ color: INK_MUTE }}>Label</label>
                  <input ref={fullMockFirstFieldRef} id="full-mock-label" type="text" value={fullMockLabel} onChange={(e) => setFullMockLabel(e.target.value)}
                         placeholder="Or type your own…" maxLength={30}
                         className={fieldClass} style={{ ...fieldStyle, marginTop: 4 }} />
                  <div className="mt-2 flex flex-wrap gap-1.5" role="group" aria-label="Mock label presets">
                    {MOCK_PRESETS.map(p => {
                      const active = fullMockLabel === p;
                      return (
                        <button
                          key={p}
                          type="button"
                          onClick={() => setFullMockLabel(p)}
                          aria-pressed={active}
                          className="rounded-[7px] px-2 py-1 font-sans text-[10px] font-semibold transition-colors"
                          style={active
                            ? { background: INK, color: PAPER, border: `1px solid ${INK}` }
                            : { background: PAPER, color: INK_SOFT, border: '1px solid var(--outline-soft)' }}
                        >
                          {p}
                        </button>
                      );
                    })}
                  </div>
                </div>
                <div>
                  <label htmlFor="full-mock-date" className="font-sans text-[10px] font-bold uppercase tracking-[0.16em]"
                         style={{ color: INK_MUTE }}>Date</label>
                  <input id="full-mock-date" type="date" value={fullMockDate} onChange={(e) => setFullMockDate(e.target.value)}
                         className={fieldClass} style={{ ...fieldStyle, marginTop: 4 }} />
                </div>
              </div>
              <div className="mt-4 divide-y divide-[var(--outline-soft)] border-y border-[var(--outline-soft)]">
                {gradeSubjects.map((s, subjectIndex) => {
                  const grades = getGradesForLevel(s.level);
                  const color = getSubjectColor(s.subjectName);
                  const selectId = `full-mock-grade-${subjectIndex}`;
                  return (
                    <div key={s.subjectName} className="grid grid-cols-[auto_minmax(0,1fr)_96px] items-center gap-2 py-2 sm:grid-cols-[auto_minmax(0,1fr)_112px] sm:gap-3">
                      <span className={`h-2 w-2 shrink-0 rounded-full ${color.dot}`} aria-hidden="true" />
                      <label htmlFor={selectId} className="truncate font-sans text-[12px] font-medium" style={{ color: INK }}>
                        {s.subjectName}
                      </label>
                      <select
                        id={selectId}
                        value={gradeForFullMockSubject(s)}
                        onChange={(e) => setFullMockGrades(prev => ({ ...prev, [s.subjectName]: e.target.value }))}
                        className={fieldClass} style={fieldStyle}
                      >
                        <option value="">Select…</option>
                        {grades.map(g => <option key={g} value={g}>{g}</option>)}
                      </select>
                    </div>
                  );
                })}
              </div>
              <div className="mt-4 flex justify-end">
                <button type="button" onClick={addFullMock} disabled={!canSaveFullMock} className={buttonClass} style={primaryBtnStyle}>
                  Save full mock
                </button>
              </div>
            </section>
          </MotionDiv>
        )}
        {showAddForm === 'single' && (
          <MotionDiv initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }}
                     exit={{ height: 0, opacity: 0 }} className="overflow-hidden">
            <section
              id="trajectory-entry-form"
              aria-labelledby="single-result-form-title"
              className="rounded-[12px] border border-[var(--outline-strong)] bg-[var(--surface-paper)] p-4 sm:p-5"
            >
              <h3 id="single-result-form-title" className="font-sans text-[14px] font-semibold" style={{ color: INK }}>
                Log a single result
              </h3>
              <p className="mt-1 font-sans text-[12px]" style={{ color: INK_MUTE }}>
                Add a result from a test or practice paper.
              </p>
              <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2">
                <div>
                  <label htmlFor="single-result-subject" className="font-sans text-[10px] font-bold uppercase tracking-[0.16em]"
                         style={{ color: INK_MUTE }}>Subject</label>
                  <select ref={singleResultFirstFieldRef} id="single-result-subject" value={formSubject}
                          onChange={(e) => { setFormSubject(e.target.value); setFormGrade(''); }}
                          className={fieldClass} style={{ ...fieldStyle, marginTop: 4 }}>
                    {gradeSubjects.map(s => <option key={s.subjectName} value={s.subjectName}>{s.subjectName}</option>)}
                  </select>
                </div>
                <div>
                  <label htmlFor="single-result-grade" className="font-sans text-[10px] font-bold uppercase tracking-[0.16em]"
                         style={{ color: INK_MUTE }}>Grade</label>
                  <select id="single-result-grade" value={formGrade} onChange={(e) => setFormGrade(e.target.value)}
                          className={fieldClass} style={{ ...fieldStyle, marginTop: 4 }}>
                    <option value="">Select…</option>
                    {gradeOptions.map(g => <option key={g} value={g}>{g} ({pointsForSubject(formSubject, g)} pts)</option>)}
                  </select>
                </div>
              </div>
              <div className="mt-3 grid grid-cols-1 gap-3 sm:grid-cols-2">
                <div>
                  <label htmlFor="single-result-date" className="font-sans text-[10px] font-bold uppercase tracking-[0.16em]"
                         style={{ color: INK_MUTE }}>Date</label>
                  <input id="single-result-date" type="date" value={formDate} onChange={(e) => setFormDate(e.target.value)}
                         className={fieldClass} style={{ ...fieldStyle, marginTop: 4 }} />
                </div>
                <div>
                  <label htmlFor="single-result-label" className="font-sans text-[10px] font-bold uppercase tracking-[0.16em]"
                         style={{ color: INK_MUTE }}>Label (optional)</label>
                  <input id="single-result-label" type="text" value={formLabel} onChange={(e) => setFormLabel(e.target.value)}
                         placeholder="e.g. Mock 1" maxLength={30}
                         className={fieldClass} style={{ ...fieldStyle, marginTop: 4 }} />
                </div>
              </div>
              <div className="mt-4 flex justify-end">
                <button type="button" onClick={addResult} disabled={!canSaveSingleResult}
                        className={buttonClass}
                        style={primaryBtnStyle}>
                  Save result
                </button>
              </div>
            </section>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Mock feedback */}
      <AnimatePresence>
        {mockFeedback && (
          <MotionDiv initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }}
                     exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.3 }} className="overflow-hidden">
            <section
              aria-live="polite"
              aria-labelledby="mock-feedback-title"
              className="border-y border-[var(--outline-soft)] py-4"
            >
              <div className="mb-3 flex items-center justify-between gap-3">
                <h3 id="mock-feedback-title" className="font-sans text-[13px] font-semibold" style={{ color: INK }}>
                  Compared with {mockFeedback.previousLabel}
                </h3>
                <button
                  type="button"
                  onClick={() => setMockFeedback(null)}
                  aria-label="Dismiss mock comparison"
                  className="inline-flex h-8 w-8 items-center justify-center rounded-[7px] border border-[var(--outline-strong)]"
                  style={{ color: INK, background: PAPER }}
                >
                  <X size={13} aria-hidden="true" />
                </button>
              </div>
              <div className="grid gap-4 sm:grid-cols-2">
                {mockFeedback.improved.length > 0 && (
                  <div>
                    <p className="font-sans text-[10px] font-bold uppercase tracking-[0.14em]" style={{ color: INK_MUTE }}>
                      Improved
                    </p>
                    <ul className="mt-1.5 space-y-1">
                      {mockFeedback.improved.map(s => (
                        <li key={s.subject} className="flex items-baseline justify-between gap-3 font-sans text-[12px]" style={{ color: INK_SOFT }}>
                          <span>{s.subject}: {s.from} → {s.to}</span>
                          <span className="shrink-0 font-sans font-semibold tabular-nums" style={{ color: INK }}>+{s.ptsDiff} pts</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {mockFeedback.declined.length > 0 && (
                  <div>
                    <p className="font-sans text-[10px] font-bold uppercase tracking-[0.14em]" style={{ color: INK_MUTE }}>
                      Needs attention
                    </p>
                    <ul className="mt-1.5 space-y-1">
                      {mockFeedback.declined.map(s => (
                        <li key={s.subject} className="flex items-baseline justify-between gap-3 font-sans text-[12px]" style={{ color: INK_SOFT }}>
                          <span>{s.subject}: {s.from} → {s.to}</span>
                          <span className="shrink-0 font-sans font-semibold tabular-nums" style={{ color: INK }}>{s.ptsDiff} pts</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
              {mockFeedback.unchanged.length > 0 && (
                <p className="mt-3 font-sans text-[11px]" style={{ color: INK_MUTE }}>
                  Unchanged: {mockFeedback.unchanged.join(', ')}
                </p>
              )}
              <div className="mt-3 border-t border-[var(--outline-soft)] pt-3">
                <p className="font-sans text-[12px] font-semibold" style={{ color: INK }}>
                  Best-six total: {mockFeedback.previousTotal} → {mockFeedback.currentTotal}
                  <span className="ml-2 font-sans tabular-nums" style={{ color: INK_SOFT }}>
                    ({mockFeedback.totalPtsDiff > 0 ? '+' : ''}{mockFeedback.totalPtsDiff} points)
                  </span>
                </p>
              </div>
            </section>
          </MotionDiv>
        )}
      </AnimatePresence>

      {chartSubjects.length === 0 && (
        <section className="flex flex-col gap-3 border-y border-[var(--outline-soft)] py-5 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h3 className="font-sans text-[13px] font-semibold" style={{ color: INK }}>
              No mock results yet
            </h3>
            <p className="mt-1 max-w-lg font-sans text-[12px] leading-relaxed" style={{ color: INK_MUTE }}>
              Add a single result or a full mock to start tracking your progress.
            </p>
          </div>
          {!showAddForm && (
            <button
              type="button"
              onClick={initSingleResultForm}
              className={`${buttonClass} shrink-0 self-start sm:self-auto`}
              style={ghostBtnStyle}
              aria-controls="trajectory-entry-form"
              aria-expanded="false"
            >
              Add first result
            </button>
          )}
        </section>
      )}

      {/* SVG chart */}
      {chartSubjects.length > 0 && (
        <section aria-labelledby="trajectory-chart-title" className="border-t border-[var(--outline-soft)] pt-5">
          <div className="mb-3">
            <h3 id="trajectory-chart-title" className="font-sans text-[13px] font-semibold" style={{ color: INK }}>
              Performance over time
            </h3>
            <p className="mt-1 font-sans text-[11px]" style={{ color: INK_MUTE }}>
              CAO points by subject and result date.
            </p>
          </div>
          <TrajectoryChart subjects={subjects} resultsBySubject={resultsBySubject} />
        </section>
      )}

      {/* Subject status table */}
      <section aria-labelledby="subject-position-title" className="border-t border-[var(--outline-soft)] pt-5">
        <div>
          <h3 id="subject-position-title" className="font-sans text-[13px] font-semibold" style={{ color: INK }}>
            Subject position
          </h3>
          <p className="mt-1 font-sans text-[11px]" style={{ color: INK_MUTE }}>
            Your latest recorded grade and target, where one is set.
          </p>
        </div>
        <div className="mt-3 divide-y divide-[var(--outline-soft)] border-y border-[var(--outline-soft)]">
            {[...gradeSubjects].map((s, sIdx) => {
              const results = resultsBySubject[s.subjectName] || [];
              const latest = results[results.length - 1];
              const targetPts = s.targetGrade ? pointsForSubject(s.subjectName, s.targetGrade) : null;
              const currentPts = latest ? pointsForSubject(s.subjectName, latest.grade) : null;
              const rawHex = getDistinctSubjectHex(s.subjectName, sIdx);
              const hexColor = mutedSubjectHex(rawHex, 0.22);
              const gap = currentPts !== null && targetPts !== null ? targetPts - currentPts : null;
              return { s, latest, currentPts, hexColor, gap };
            }).sort((a, b) => {
              if (a.gap === null && b.gap !== null) return 1;
              if (a.gap !== null && b.gap === null) return -1;
              const gA = a.gap ?? 0;
              const gB = b.gap ?? 0;
              if (gA <= 0 && gB > 0) return 1;
              if (gA > 0 && gB <= 0) return -1;
              return gB - gA;
            }).map((item) => {
              const { s, latest, currentPts, hexColor, gap } = item;
              return (
                <div
                  key={s.subjectName}
                  className="flex items-center gap-2.5 py-3 sm:gap-3"
                >
                  <span className="h-2 w-2 shrink-0 rounded-full"
                        style={{ background: hexColor, border: '1px solid var(--outline-soft)' }} aria-hidden="true" />
                  <span className="min-w-0 flex-1 truncate font-sans text-[12px] font-medium" style={{ color: INK }}>
                    {s.subjectName}
                  </span>
                  {latest ? (
                    <div className="shrink-0 text-right">
                      <p className="font-sans text-[11px] font-semibold tabular-nums" style={{ color: INK }}>
                        {latest.grade} · {currentPts} pts
                      </p>
                      <p className="mt-0.5 font-sans text-[10px]" style={{ color: INK_SOFT }}>
                        {!s.targetGrade
                          ? 'No target set'
                          : gap !== null && gap <= 0
                          ? 'On target'
                          : gap !== null
                            ? `${gap} pts to ${s.targetGrade}`
                            : `Target ${s.targetGrade}`}
                      </p>
                    </div>
                  ) : (
                    <div className="shrink-0 text-right">
                      <p className="font-sans text-[11px] font-medium" style={{ color: INK_SOFT }}>
                        {s.targetGrade ? `Target ${s.targetGrade}` : 'No target set'}
                      </p>
                      <p className="mt-0.5 font-sans text-[10px]" style={{ color: INK_MUTE }}>No result yet</p>
                    </div>
                  )}
                </div>
              );
            })}
        </div>
      </section>
    </div>
  );
};

export default TrajectoryPanel;
