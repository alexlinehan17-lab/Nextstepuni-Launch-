/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { Plus, X, TrendingUp, AlertTriangle } from 'lucide-react';
import {
  type StudentSubjectProfile, type Grade,
  getPointsForGrade, getGradesForLevel,
  HIGHER_GRADES, LC_SUBJECTS,
} from '../subjectData';
import { getSubjectColor, getDistinctSubjectHex } from '../../studySessionData';
import { useMockResults } from '../../hooks/useMockResults';
import { type MockResult, CARD_STYLE, CARD_CLASS, gradeToPoints } from './warRoomShared';

// ── Constants ───────────────────────────────────────────────

const MOCK_PRESETS = ['Christmas Mocks', 'February Mocks', 'Pre-LC Mocks', 'Practice Exam'];

// ── Types ───────────────────────────────────────────────────

interface MockFeedback {
  improved: { subject: string; from: string; to: string; ptsDiff: number }[];
  declined: { subject: string; from: string; to: string; ptsDiff: number }[];
  unchanged: string[];
  totalPtsDiff: number;
}

interface TrajectoryPanelProps {
  subjects: StudentSubjectProfile['subjects'];
  mockResults: MockResult[];
  mockResultsHook: ReturnType<typeof useMockResults>;
  daysUntilExam: number;
}

// ── SVG Trajectory Chart ────────────────────────────────────

// Maximally distinct chart colours -- spread across the colour spectrum
const CHART_COLORS: Record<string, string> = {
  'Politics & Society': '#E84393', 'Religious Education': '#D63384',
  'Business': '#0984E3', 'Economics': '#E5A41E',
  'Applied Maths': '#6C5CE7', 'Applied Mathematics': '#6C5CE7',
  'Mathematics': '#2D3436', 'English': '#00B894',
  'Irish': '#10B981', 'French': '#0ea5e9', 'German': '#eab308',
  'Spanish': '#f97316', 'Physics': '#06b6d4', 'Chemistry': '#14b8a6',
  'Biology': '#84cc16', 'History': '#a855f7', 'Geography': '#059669',
  'Accounting': '#f59e0b', 'Home Economics': '#fb923c',
  'Music': '#f472b6', 'Art': '#fb7185',
};

function getChartColor(name: string, fallbackIdx: number): string {
  return CHART_COLORS[name] || getDistinctSubjectHex(name, fallbackIdx);
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

  const allResults = Object.values(resultsBySubject).flat();
  if (allResults.length === 0) return null;

  const dates = allResults.map(r => new Date(r.date).getTime()).filter(t => !isNaN(t));
  if (dates.length === 0) return null;
  const minDate = Math.min(...dates);
  const maxDate = Math.max(...dates);
  const dateRange = maxDate - minDate || 86400000;

  const maxPts = 100;
  const yLabels = [0, 25, 50, 75, 100];

  const scaleX = (date: string) => {
    const t = new Date(date).getTime();
    return PAD.left + ((t - minDate) / dateRange) * plotW;
  };
  const scaleY = (pts: number) => PAD.top + plotH - (pts / maxPts) * plotH;

  const subjectsWithResults = subjects.filter(s => resultsBySubject[s.subjectName]?.length);
  const subjectIndexMap: Record<string, number> = {};
  subjects.forEach((s, i) => { subjectIndexMap[s.subjectName] = i; });

  // Target line (use first subject's target as representative)
  const targetPts = subjectsWithResults.length > 0 ? getPointsForGrade(subjectsWithResults[0].targetGrade, false) : 0;

  // Unique dates for x-axis labels
  const uniqueDates = [...new Set(allResults.map(r => r.date))].sort();

  return (
    <div className="space-y-3">
      <svg
        viewBox={`0 0 ${W} ${H}`}
        className="w-full"
        style={{ maxHeight: 340 }}
        onMouseLeave={() => { setHoveredSubject(null); setHoveredDot(null); }}
      >
        {/* Horizontal grid lines */}
        {yLabels.map(pts => (
          <g key={pts}>
            <line x1={PAD.left} y1={scaleY(pts)} x2={W - PAD.right} y2={scaleY(pts)} className="stroke-[#F0EDE8] dark:stroke-zinc-700" strokeWidth="0.5" />
            <text x={PAD.left - 6} y={scaleY(pts) + 3} textAnchor="end" className="fill-[#A8A29E] dark:fill-zinc-500" fontSize="9">{pts}</text>
          </g>
        ))}

        {/* X-axis date labels */}
        {uniqueDates.map(d => (
          <text key={d} x={scaleX(d)} y={H - 8} textAnchor="middle" className="fill-[#A8A29E] dark:fill-zinc-500" fontSize="9">
            {new Date(d).toLocaleDateString('en-IE', { day: 'numeric', month: 'short' })}
          </text>
        ))}

        {/* Target dashed line */}
        {targetPts > 0 && (
          <g>
            <line x1={PAD.left} y1={scaleY(targetPts)} x2={W - PAD.right} y2={scaleY(targetPts)} stroke="#B8B0A6" strokeWidth="1" strokeDasharray="4 3" opacity="0.4" />
            <text x={W - PAD.right + 4} y={scaleY(targetPts) + 3} fill="#B8B0A6" fontSize="9">Target</text>
          </g>
        )}

        {/* Subject lines */}
        {subjectsWithResults.map(s => {
          const results = resultsBySubject[s.subjectName];
          if (!results || results.length < 1) return null;
          const hexColor = getChartColor(s.subjectName, subjectIndexMap[s.subjectName] ?? 0);
          const isHovered = hoveredSubject === s.subjectName;
          const isFaded = hoveredSubject !== null && !isHovered;

          // Build polyline points
          const pts = results.map(r => ({
            x: scaleX(r.date),
            y: scaleY(gradeToPoints(r.grade)),
            grade: r.grade,
            date: r.date,
            id: r.id,
            points: gradeToPoints(r.grade),
          }));
          const polyPoints = pts.map(p => `${p.x},${p.y}`).join(' ');

          return (
            <g key={s.subjectName} style={{ opacity: isFaded ? 0.1 : 1, transition: 'opacity 0.2s' }}>
              {/* Polyline -- only if 2+ results */}
              {pts.length > 1 && (
                <>
                  <polyline points={polyPoints} fill="none" stroke="transparent" strokeWidth="14" strokeLinecap="round" onMouseEnter={() => setHoveredSubject(s.subjectName)} style={{ cursor: 'pointer' }} />
                  <polyline points={polyPoints} fill="none" stroke={hexColor} strokeWidth={isHovered ? 3 : 2} strokeLinecap="round" strokeLinejoin="round" style={{ pointerEvents: 'none' }} />
                </>
              )}
              {/* Data points */}
              {pts.map(p => {
                const formatted = new Date(p.date).toLocaleDateString('en-IE', { day: 'numeric', month: 'short' });
                const label = `${s.subjectName}: ${p.grade} (${p.points}pts) — ${formatted}`;
                const isDotHovered = hoveredDot?.id === p.id;
                return (
                  <circle
                    key={p.id}
                    cx={p.x} cy={p.y} r={isDotHovered ? 6 : 4}
                    fill={hexColor}
                    className="stroke-[#FEFDFB] dark:stroke-zinc-900"
                    strokeWidth="2"
                    style={{ cursor: 'pointer', transition: 'r 0.15s' }}
                    onMouseEnter={() => setHoveredDot({ id: p.id, cx: p.x, cy: p.y, label })}
                    onMouseLeave={() => setHoveredDot(null)}
                  />
                );
              })}
            </g>
          );
        })}

        {/* Hover tooltip */}
        {hoveredDot && (() => {
          const tooltipW = Math.max(hoveredDot.label.length * 5 + 16, 80);
          const tx = Math.min(Math.max(5, hoveredDot.cx - tooltipW / 2), W - tooltipW - 5);
          const ty = hoveredDot.cy > 40 ? hoveredDot.cy - 24 : hoveredDot.cy + 12;
          return (
            <g style={{ pointerEvents: 'none' }}>
              <rect x={tx} y={ty} width={tooltipW} height={18} rx="4" fill="rgba(0,0,0,0.85)" />
              <text x={tx + tooltipW / 2} y={ty + 13} fontSize="8" fill="white" fontWeight="600" textAnchor="middle">{hoveredDot.label}</text>
            </g>
          );
        })()}
      </svg>

      {/* Legend */}
      {subjectsWithResults.length > 0 && (
        <div className="flex flex-wrap gap-x-5 gap-y-2 px-1">
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
                <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: hexColor }} />
                <span className="text-[11px] font-semibold text-[#57534E] dark:text-zinc-400">{s.subjectName}</span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

// ── TrajectoryPanel ─────────────────────────────────────────

const TrajectoryPanel: React.FC<TrajectoryPanelProps> = ({ subjects, mockResults, mockResultsHook, _daysUntilExam }) => {
  const [showAddForm, setShowAddForm] = useState<false | 'single' | 'full'>(false);
  const [formSubject, setFormSubject] = useState(subjects[0]?.subjectName ?? '');
  const [formGrade, setFormGrade] = useState('');
  const [formDate, setFormDate] = useState(new Date().toISOString().split('T')[0]);
  const [formLabel, setFormLabel] = useState('');
  // Full mock form
  const [fullMockGrades, setFullMockGrades] = useState<Record<string, string>>({});
  const [fullMockLabel, setFullMockLabel] = useState('');
  const [fullMockDate, setFullMockDate] = useState(new Date().toISOString().split('T')[0]);
  // Mock feedback after saving
  const [mockFeedback, setMockFeedback] = useState<MockFeedback | null>(null);

  const formSubjectData = subjects.find(s => s.subjectName === formSubject);
  const gradeOptions = formSubjectData ? getGradesForLevel(formSubjectData.level) : HIGHER_GRADES;

  const initFullMockForm = () => {
    const grades: Record<string, string> = {};
    subjects.forEach(s => { grades[s.subjectName] = s.currentGrade; });
    setFullMockGrades(grades);
    setFullMockLabel('');
    setFullMockDate(new Date().toISOString().split('T')[0]);
    setShowAddForm('full');
  };

  const addResult = () => {
    if (!formSubject || !formGrade || !formDate) return;
    const subjectData = subjects.find(s => s.subjectName === formSubject);
    mockResultsHook.addMockResult({
      label: formLabel.trim() || 'Single Result',
      date: formDate,
      entries: [{ subjectName: formSubject, grade: formGrade, level: subjectData?.level || 'Higher' }],
      totalPoints: gradeToPoints(formGrade),
    });
    setShowAddForm(false);
    setFormGrade('');
    setFormLabel('');
  };

  const addFullMock = () => {
    if (!fullMockDate) return;
    const label = fullMockLabel.trim() || 'Mock Exam';

    // Build entries for unified mock
    const entries = subjects.map(s => ({
      subjectName: s.subjectName,
      grade: fullMockGrades[s.subjectName] || s.currentGrade,
      level: s.level,
    }));

    // Compute feedback vs previous results (using derived mockResults for comparison)
    const improved: MockFeedback['improved'] = [];
    const declined: MockFeedback['declined'] = [];
    const unchanged: string[] = [];
    for (const entry of entries) {
      const prev = mockResults
        .filter(r => r.subject === entry.subjectName && r.grade && r.date)
        .sort((a, b) => (a.date ?? '').localeCompare(b.date ?? ''));
      const prevResult = prev[prev.length - 1];
      if (!prevResult) continue;
      const prevPts = gradeToPoints(prevResult.grade);
      const newPts = gradeToPoints(entry.grade);
      const diff = newPts - prevPts;
      if (diff > 0) improved.push({ subject: entry.subjectName, from: prevResult.grade, to: entry.grade, ptsDiff: diff });
      else if (diff < 0) declined.push({ subject: entry.subjectName, from: prevResult.grade, to: entry.grade, ptsDiff: diff });
      else unchanged.push(entry.subjectName);
    }
    const totalPtsDiff = improved.reduce((s, x) => s + x.ptsDiff, 0) + declined.reduce((s, x) => s + x.ptsDiff, 0);
    if (improved.length > 0 || declined.length > 0 || unchanged.length > 0) {
      setMockFeedback({ improved, declined, unchanged, totalPtsDiff });
    }

    // Compute total points (best 6)
    const scored = entries.map(e => {
      const isMaths = LC_SUBJECTS.find(lc => lc.name === e.subjectName)?.isMaths ?? false;
      return getPointsForGrade(e.grade as Grade, isMaths);
    }).sort((a, b) => b - a);
    const totalPoints = scored.slice(0, 6).reduce((sum, p) => sum + p, 0);

    mockResultsHook.addMockResult({ label, date: fullMockDate, entries, totalPoints });
    setShowAddForm(false);
  };

  const _removeResult = (derivedId: string) => {
    // Derived IDs are formatted as `${mock.id}-${subjectName}`.
    // Find the parent unified mock by checking if derivedId starts with mock.id.
    for (const mock of mockResultsHook.mocks) {
      if (derivedId.startsWith(mock.id + '-')) {
        mockResultsHook.removeMockResult(mock.id);
        return;
      }
    }
  };

  // Group results by subject
  const resultsBySubject = useMemo(() => {
    const map: Record<string, MockResult[]> = {};
    for (const r of mockResults) {
      if (!r.subject || !r.grade || !r.date) continue; // skip corrupted entries
      if (!map[r.subject]) map[r.subject] = [];
      map[r.subject].push(r);
    }
    // Sort each group by date
    for (const key of Object.keys(map)) {
      map[key].sort((a, b) => (a.date ?? '').localeCompare(b.date ?? ''));
    }
    return map;
  }, [mockResults]);

  // SVG chart data
  const chartSubjects = subjects.filter(s => resultsBySubject[s.subjectName]?.length);

  return (
    <div className="space-y-5">
      {/* Add result buttons */}
      <div className="flex items-center justify-between">
        <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Mock & Test Results</p>
        <div className="flex gap-2">
          {showAddForm ? (
            <button onClick={() => setShowAddForm(false)} className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-zinc-100 dark:bg-zinc-800 text-zinc-500 text-xs font-bold hover:bg-zinc-200 dark:hover:bg-zinc-700 transition-colors">
              <X size={12} /> Cancel
            </button>
          ) : (
            <>
              <button onClick={initFullMockForm} className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-white text-xs font-bold hover:shadow-md transition-colors" style={{ backgroundColor: '#2A7D6F' }}>
                <Plus size={12} /> Full Mock
              </button>
              <button onClick={() => setShowAddForm('single')} className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-zinc-600 dark:text-zinc-400 text-xs font-bold hover:bg-zinc-100 dark:hover:bg-zinc-700 transition-colors" style={{ border: '0.5px solid rgba(0,0,0,0.07)' }}>
                <Plus size={12} /> Single
              </button>
            </>
          )}
        </div>
      </div>

      {/* Add result form */}
      <AnimatePresence>
        {showAddForm === 'full' && (
          <MotionDiv
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            <div className={`p-4 space-y-3 ${CARD_CLASS}`} style={CARD_STYLE}>
              <p className="text-xs font-bold text-zinc-600 dark:text-zinc-300">Log Full Mock — all subjects at once</p>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider">Label</label>
                  <div className="flex flex-wrap gap-1.5 mt-1 mb-1">
                    {MOCK_PRESETS.map(p => (
                      <button key={p} onClick={() => setFullMockLabel(p)} className={`px-2 py-1 rounded-md text-[10px] font-semibold transition-colors ${fullMockLabel === p ? 'text-white' : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-500 hover:bg-zinc-200 dark:hover:bg-zinc-700'}`} style={fullMockLabel === p ? { backgroundColor: '#2A7D6F' } : undefined}>
                        {p}
                      </button>
                    ))}
                  </div>
                  <input type="text" value={fullMockLabel} onChange={(e) => setFullMockLabel(e.target.value)} placeholder="Or type your own..." maxLength={30} className="w-full px-3 py-2 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-sm text-zinc-800 dark:text-white placeholder-zinc-400 outline-none" />
                </div>
                <div>
                  <label className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider">Date</label>
                  <input type="date" value={fullMockDate} onChange={(e) => setFullMockDate(e.target.value)} className="w-full mt-1 px-3 py-2 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-sm text-zinc-800 dark:text-white outline-none" />
                </div>
              </div>
              <div className="space-y-2">
                {subjects.map(s => {
                  const grades = getGradesForLevel(s.level);
                  const color = getSubjectColor(s.subjectName);
                  return (
                    <div key={s.subjectName} className="flex items-center gap-3">
                      <div className={`w-2 h-2 rounded-full ${color.dot} shrink-0`} />
                      <span className="text-xs font-semibold text-zinc-600 dark:text-zinc-400 w-28 truncate">{s.subjectName}</span>
                      <select
                        value={fullMockGrades[s.subjectName] || s.currentGrade}
                        onChange={(e) => setFullMockGrades(prev => ({ ...prev, [s.subjectName]: e.target.value }))}
                        className="flex-1 px-2 py-1.5 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-xs text-zinc-800 dark:text-white outline-none"
                      >
                        {grades.map(g => <option key={g} value={g}>{g}</option>)}
                      </select>
                    </div>
                  );
                })}
              </div>
              <button onClick={addFullMock} className="w-full py-2.5 text-sm font-bold text-white hover:shadow-md active:scale-[0.98] transition-all" style={{ backgroundColor: '#2A7D6F', borderRadius: 12 }}>
                Save Full Mock
              </button>
            </div>
          </MotionDiv>
        )}
        {showAddForm === 'single' && (
          <MotionDiv
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            <div className={`p-4 space-y-3 ${CARD_CLASS}`} style={CARD_STYLE}>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider">Subject</label>
                  <select
                    value={formSubject}
                    onChange={(e) => { setFormSubject(e.target.value); setFormGrade(''); }}
                    className="w-full mt-1 px-3 py-2 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-sm text-zinc-800 dark:text-white outline-none"
                  >
                    {subjects.map(s => (
                      <option key={s.subjectName} value={s.subjectName}>{s.subjectName}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider">Grade</label>
                  <select
                    value={formGrade}
                    onChange={(e) => setFormGrade(e.target.value)}
                    className="w-full mt-1 px-3 py-2 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-sm text-zinc-800 dark:text-white outline-none"
                  >
                    <option value="">Select...</option>
                    {gradeOptions.map(g => (
                      <option key={g} value={g}>{g} ({gradeToPoints(g)} pts)</option>
                    ))}
                  </select>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider">Date</label>
                  <input
                    type="date"
                    value={formDate}
                    onChange={(e) => setFormDate(e.target.value)}
                    className="w-full mt-1 px-3 py-2 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-sm text-zinc-800 dark:text-white outline-none"
                  />
                </div>
                <div>
                  <label className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider">Label (optional)</label>
                  <input
                    type="text"
                    value={formLabel}
                    onChange={(e) => setFormLabel(e.target.value)}
                    placeholder="e.g. Mock 1"
                    maxLength={30}
                    className="w-full mt-1 px-3 py-2 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-sm text-zinc-800 dark:text-white placeholder-zinc-400 outline-none"
                  />
                </div>
              </div>
              <button
                onClick={addResult}
                disabled={!formGrade}
                className="w-full py-2.5 text-sm font-bold text-white disabled:opacity-40 hover:shadow-md active:scale-[0.98] transition-all"
                style={{ backgroundColor: '#2A7D6F', borderRadius: 12 }}
              >
                Save Result
              </button>
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Mock feedback card */}
      <AnimatePresence>
        {mockFeedback && (
          <MotionDiv
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="overflow-hidden"
          >
            <div
              className={`p-4 ${CARD_CLASS}`}
              style={{
                ...CARD_STYLE,
                ...(mockFeedback.totalPtsDiff > 0
                  ? { backgroundColor: 'rgba(107,143,113,0.08)' }
                  : mockFeedback.totalPtsDiff < 0
                    ? { backgroundColor: 'rgba(42,125,111,0.06)' }
                    : {}),
              }}
            >
              <div className="flex items-center justify-between mb-3">
                <p className="text-xs font-bold text-zinc-700 dark:text-zinc-300">
                  {mockFeedback.totalPtsDiff > 0 ? 'Progress since last mock' : mockFeedback.totalPtsDiff < 0 ? 'Changes since last mock' : 'Compared to last mock'}
                </p>
                <button onClick={() => setMockFeedback(null)} className="text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300">
                  <X size={14} />
                </button>
              </div>
              {mockFeedback.improved.length > 0 && (
                <div className="mb-2">
                  <p className="text-[10px] font-bold mb-1" style={{ color: '#6B8F71' }}>Improved</p>
                  {mockFeedback.improved.map(s => (
                    <p key={s.subject} className="text-xs text-zinc-600 dark:text-zinc-400 flex items-center gap-1.5">
                      <TrendingUp size={10} style={{ color: '#6B8F71' }} />
                      {s.subject}: {s.from} → {s.to} <span className="font-bold" style={{ color: '#6B8F71' }}>(+{s.ptsDiff}pts)</span>
                    </p>
                  ))}
                </div>
              )}
              {mockFeedback.declined.length > 0 && (
                <div className="mb-2">
                  <p className="text-[10px] font-bold mb-1" style={{ color: '#B85C4A' }}>Needs attention</p>
                  {mockFeedback.declined.map(s => (
                    <p key={s.subject} className="text-xs text-zinc-600 dark:text-zinc-400 flex items-center gap-1.5">
                      <AlertTriangle size={10} style={{ color: '#B85C4A' }} />
                      {s.subject}: {s.from} → {s.to} <span className="font-bold" style={{ color: '#B85C4A' }}>({s.ptsDiff}pts)</span>
                    </p>
                  ))}
                </div>
              )}
              {mockFeedback.unchanged.length > 0 && (
                <p className="text-[10px] text-zinc-400 dark:text-zinc-500">
                  Unchanged: {mockFeedback.unchanged.join(', ')}
                </p>
              )}
              {mockFeedback.totalPtsDiff !== 0 && (
                <div className="mt-2 pt-2 border-t border-zinc-200/50 dark:border-white/[0.06]">
                  <p className="text-xs font-bold" style={{ color: mockFeedback.totalPtsDiff > 0 ? '#6B8F71' : '#B85C4A' }}>
                    Net change: {mockFeedback.totalPtsDiff > 0 ? '+' : ''}{mockFeedback.totalPtsDiff} CAO points
                  </p>
                </div>
              )}
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* SVG Chart */}
      {chartSubjects.length > 0 && (
        <div className={`p-4 ${CARD_CLASS}`} style={CARD_STYLE}>
          <TrajectoryChart
            subjects={subjects}
            resultsBySubject={resultsBySubject}
          />
        </div>
      )}

      {/* Subject status -- compact rows in one card, NO left borders */}
      <div>
        <p className="text-[10px] font-bold uppercase tracking-widest mb-2 text-[#A8A29E] dark:text-zinc-500">Subject Status</p>
        <div className="rounded-2xl overflow-hidden bg-[#FEFDFB] dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800" style={{ boxShadow: '0 1px 3px rgba(28,25,23,0.04)' }}>
          {[...subjects].map((s, sIdx) => {
            const results = resultsBySubject[s.subjectName] || [];
            const latest = results[results.length - 1];
            const targetPts = getPointsForGrade(s.targetGrade, false);
            const currentPts = latest ? gradeToPoints(latest.grade) : null;
            const hexColor = getDistinctSubjectHex(s.subjectName, sIdx);
            const gap = currentPts !== null ? targetPts - currentPts : null;
            return { s, latest, currentPts, hexColor, gap, targetPts };
          }).sort((a, b) => {
            // Gaps first (largest gap at top), then on-target, then no data
            const gA = a.gap ?? 999;
            const gB = b.gap ?? 999;
            if (gA <= 0 && gB > 0) return 1;
            if (gA > 0 && gB <= 0) return -1;
            return gB - gA;
          }).map((item, idx, arr) => {
            const { s, latest, currentPts, hexColor, gap } = item;
            const isLast = idx === arr.length - 1;
            const ptsColorClass = gap !== null && gap <= 0 ? 'text-[#2A7D6F]' : gap !== null && gap > 0 ? 'text-[#C53030]' : 'text-[#1C1917] dark:text-white';

            return (
              <div
                key={s.subjectName}
                className={`flex items-center gap-2.5 px-4 py-1.5 ${isLast ? '' : 'border-b border-[#F0EFED] dark:border-zinc-800'}`}
              >
                <div className="w-3 h-3 rounded-full shrink-0" style={{ backgroundColor: hexColor }} />
                <span className="text-[13px] font-semibold flex-1 min-w-0 truncate text-[#1C1917] dark:text-white">{s.subjectName}</span>
                {latest ? (
                  <>
                    <span className="text-[10px]" style={{ color: '#C4C0BC' }}>{latest.grade}</span>
                    <span className={`text-[11px] font-bold tabular-nums ${ptsColorClass}`}>{currentPts}pts</span>
                  </>
                ) : (
                  <span className="text-[10px]" style={{ color: '#C4C0BC' }}>—</span>
                )}
                {gap !== null ? (
                  gap <= 0 ? (
                    <span className="text-[9px] font-bold px-2 py-0.5 rounded-full" style={{ backgroundColor: '#DEF7EC', color: '#276749' }}>On target</span>
                  ) : (
                    <span className="text-[9px] font-bold px-2 py-0.5 rounded-full" style={{ backgroundColor: '#FDE8E8', color: '#C53030' }}>{gap}pt gap</span>
                  )
                ) : (
                  <span className="text-[10px] text-[#A8A29E] dark:text-zinc-500">{s.targetGrade}</span>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {mockResults.length === 0 && (
        <div className="text-center py-12 space-y-4">
          <div className="w-14 h-14 mx-auto rounded-2xl flex items-center justify-center" style={{ backgroundColor: 'rgba(42,125,111,0.1)' }}>
            <TrendingUp size={28} style={{ color: '#2A7D6F' }} />
          </div>
          <h3 className="text-base font-bold text-zinc-800 dark:text-white">Track your mock exam trajectory</h3>
          <p className="text-xs text-zinc-500 dark:text-zinc-400 max-w-xs mx-auto leading-relaxed">
            Log mock results to see your points climb over time and identify the subjects worth targeting.
          </p>
        </div>
      )}
    </div>
  );
};

export default TrajectoryPanel;
