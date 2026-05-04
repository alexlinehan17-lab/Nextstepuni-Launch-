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
import { type useMockResults } from '../../hooks/useMockResults';
import {
  type MockResult, gradeToPoints,
  PAPER, PAPER_SOFT, INK, INK_SOFT, INK_MUTE, INK_FAINT, ACCENT,
  STATUS_SOLID, STATUS_SOLID_DEEP, STATUS_SOLID_TINT,
  STATUS_GAP, STATUS_GAP_DEEP, STATUS_GAP_TINT,
  mutedSubjectHex,
} from './warRoomShared';
import {
  Overline, SectionHeader, EditorialCard, Pill,
  fieldClass, fieldStyle,
} from './warRoomPrimitives';

// ── Constants ───────────────────────────────────────────────

const MOCK_PRESETS = ['Christmas Mocks', 'February Mocks', 'Pre-LC Mocks', 'Practice Exam'];

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

// ── Refined chart palette ───────────────────────────────────
// Existing distinct hex per subject, but blended toward paper for restraint.

function getChartColor(name: string, fallbackIdx: number): string {
  return mutedSubjectHex(getDistinctSubjectHex(name, fallbackIdx), 0.18);
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

  const targetPts = subjectsWithResults.length > 0 ? getPointsForGrade(subjectsWithResults[0].targetGrade, false) : 0;
  const uniqueDates = [...new Set(allResults.map(r => r.date))].sort();

  return (
    <div className="space-y-3">
      <svg
        viewBox={`0 0 ${W} ${H}`}
        className="w-full"
        style={{ maxHeight: 340 }}
        onMouseLeave={() => { setHoveredSubject(null); setHoveredDot(null); }}
      >
        {/* Horizontal grid lines on cream */}
        {yLabels.map(pts => (
          <g key={pts}>
            <line x1={PAD.left} y1={scaleY(pts)} x2={W - PAD.right} y2={scaleY(pts)}
                  stroke={INK} strokeOpacity={0.08} strokeWidth="0.5" />
            <text x={PAD.left - 6} y={scaleY(pts) + 3} textAnchor="end"
                  fill={INK_MUTE} fontSize="9">{pts}</text>
          </g>
        ))}

        {/* X-axis date labels */}
        {uniqueDates.map(d => (
          <text key={d} x={scaleX(d)} y={H - 8} textAnchor="middle"
                fill={INK_MUTE} fontSize="9">
            {new Date(d).toLocaleDateString('en-IE', { day: 'numeric', month: 'short' })}
          </text>
        ))}

        {/* Target dashed line — accent orange */}
        {targetPts > 0 && (
          <g>
            <line x1={PAD.left} y1={scaleY(targetPts)} x2={W - PAD.right} y2={scaleY(targetPts)}
                  stroke={ACCENT} strokeWidth="1" strokeDasharray="4 3" opacity="0.55" />
            <text x={W - PAD.right + 4} y={scaleY(targetPts) + 3} fill={ACCENT} fontSize="9" fontWeight="600">Target</text>
          </g>
        )}

        {/* Subject lines */}
        {subjectsWithResults.map(s => {
          const results = resultsBySubject[s.subjectName];
          if (!results || results.length < 1) return null;
          const hexColor = getChartColor(s.subjectName, subjectIndexMap[s.subjectName] ?? 0);
          const isHovered = hoveredSubject === s.subjectName;
          const isFaded = hoveredSubject !== null && !isHovered;

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
            <g key={s.subjectName} style={{ opacity: isFaded ? 0.12 : 1, transition: 'opacity 0.2s' }}>
              {pts.length > 1 && (
                <>
                  <polyline points={polyPoints} fill="none" stroke="transparent" strokeWidth="14"
                            strokeLinecap="round" onMouseEnter={() => setHoveredSubject(s.subjectName)}
                            style={{ cursor: 'pointer' }} />
                  <polyline points={polyPoints} fill="none" stroke={hexColor}
                            strokeWidth={isHovered ? 2.6 : 1.8}
                            strokeLinecap="round" strokeLinejoin="round"
                            style={{ pointerEvents: 'none' }} />
                </>
              )}
              {pts.map(p => {
                const formatted = new Date(p.date).toLocaleDateString('en-IE', { day: 'numeric', month: 'short' });
                const label = `${s.subjectName}: ${p.grade} (${p.points}pts) — ${formatted}`;
                const isDotHovered = hoveredDot?.id === p.id;
                return (
                  <circle
                    key={p.id}
                    cx={p.x} cy={p.y} r={isDotHovered ? 5.5 : 3.5}
                    fill={hexColor}
                    stroke={PAPER}
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

        {/* Hover tooltip — charcoal pill */}
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
                      style={{ background: hexColor, border: `1px solid ${INK}33` }} />
                <span className="font-sans text-[11px] font-semibold" style={{ color: INK_SOFT }}>{s.subjectName}</span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

// ── TrajectoryPanel ─────────────────────────────────────────

const TrajectoryPanel: React.FC<TrajectoryPanelProps> = ({ subjects, mockResults, mockResultsHook }) => {
  const [showAddForm, setShowAddForm] = useState<false | 'single' | 'full'>(false);
  const [formSubject, setFormSubject] = useState(subjects[0]?.subjectName ?? '');
  const [formGrade, setFormGrade] = useState('');
  const [formDate, setFormDate] = useState(new Date().toISOString().split('T')[0]);
  const [formLabel, setFormLabel] = useState('');
  const [fullMockGrades, setFullMockGrades] = useState<Record<string, string>>({});
  const [fullMockLabel, setFullMockLabel] = useState('');
  const [fullMockDate, setFullMockDate] = useState(new Date().toISOString().split('T')[0]);
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

    const entries = subjects.map(s => ({
      subjectName: s.subjectName,
      grade: fullMockGrades[s.subjectName] || s.currentGrade,
      level: s.level,
    }));

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

    const scored = entries.map(e => {
      const isMaths = LC_SUBJECTS.find(lc => lc.name === e.subjectName)?.isMaths ?? false;
      return getPointsForGrade(e.grade as Grade, isMaths);
    }).sort((a, b) => b - a);
    const totalPoints = scored.slice(0, 6).reduce((sum, p) => sum + p, 0);

    mockResultsHook.addMockResult({ label, date: fullMockDate, entries, totalPoints });
    setShowAddForm(false);
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
    background: INK, color: PAPER,
    boxShadow: '0 2px 0 rgba(31,27,23,0.18)',
    borderRadius: 999,
  };
  const ghostBtnStyle: React.CSSProperties = {
    background: 'transparent', color: INK_SOFT,
    border: `1px solid ${INK}22`, borderRadius: 999,
  };

  return (
    <div className="space-y-6">
      <SectionHeader
        overline="The arc"
        title="Mock & test results"
        rule
        trailing={
          <div className="flex gap-2">
            {showAddForm ? (
              <button onClick={() => setShowAddForm(false)}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 text-[12px] font-semibold transition-colors"
                      style={ghostBtnStyle}>
                <X size={12} /> Cancel
              </button>
            ) : (
              <>
                <button onClick={initFullMockForm}
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 text-[12px] font-semibold transition-all"
                        style={primaryBtnStyle}>
                  <Plus size={12} /> Full Mock
                </button>
                <button onClick={() => setShowAddForm('single')}
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 text-[12px] font-semibold transition-colors"
                        style={ghostBtnStyle}>
                  <Plus size={12} /> Single
                </button>
              </>
            )}
          </div>
        }
      />

      {/* Add-result forms — same fields, refined surfaces */}
      <AnimatePresence>
        {showAddForm === 'full' && (
          <MotionDiv initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }}
                     exit={{ height: 0, opacity: 0 }} className="overflow-hidden">
            <EditorialCard tone="soft">
              <Overline>Log full mock — all subjects at once</Overline>
              <div className="grid grid-cols-2 gap-3 mt-3">
                <div>
                  <label className="font-sans text-[10px] font-bold uppercase tracking-[0.18em]"
                         style={{ color: INK_MUTE }}>Label</label>
                  <div className="flex flex-wrap gap-1.5 mt-1 mb-1.5">
                    {MOCK_PRESETS.map(p => {
                      const active = fullMockLabel === p;
                      return (
                        <button key={p} onClick={() => setFullMockLabel(p)}
                                className="px-2 py-1 rounded-md text-[10px] font-semibold transition-colors"
                                style={active
                                  ? { background: INK, color: PAPER }
                                  : { background: PAPER, color: INK_SOFT, border: `1px solid ${INK}1A` }}>
                          {p}
                        </button>
                      );
                    })}
                  </div>
                  <input type="text" value={fullMockLabel} onChange={(e) => setFullMockLabel(e.target.value)}
                         placeholder="Or type your own…" maxLength={30}
                         className={fieldClass} style={fieldStyle} />
                </div>
                <div>
                  <label className="font-sans text-[10px] font-bold uppercase tracking-[0.18em]"
                         style={{ color: INK_MUTE }}>Date</label>
                  <input type="date" value={fullMockDate} onChange={(e) => setFullMockDate(e.target.value)}
                         className={fieldClass} style={{ ...fieldStyle, marginTop: 4 }} />
                </div>
              </div>
              <div className="space-y-2 mt-4">
                {subjects.map(s => {
                  const grades = getGradesForLevel(s.level);
                  const color = getSubjectColor(s.subjectName);
                  return (
                    <div key={s.subjectName} className="flex items-center gap-3">
                      <div className={`w-2 h-2 rounded-full ${color.dot} shrink-0`} />
                      <span className="font-serif text-[13px] font-semibold w-28 truncate" style={{ color: INK }}>
                        {s.subjectName}
                      </span>
                      <select
                        value={fullMockGrades[s.subjectName] || s.currentGrade}
                        onChange={(e) => setFullMockGrades(prev => ({ ...prev, [s.subjectName]: e.target.value }))}
                        className={fieldClass} style={{ ...fieldStyle, flex: 1 }}
                      >
                        {grades.map(g => <option key={g} value={g}>{g}</option>)}
                      </select>
                    </div>
                  );
                })}
              </div>
              <button onClick={addFullMock}
                      className="w-full py-2.5 mt-4 text-[13px] font-bold transition-all"
                      style={primaryBtnStyle}>
                Save Full Mock
              </button>
            </EditorialCard>
          </MotionDiv>
        )}
        {showAddForm === 'single' && (
          <MotionDiv initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }}
                     exit={{ height: 0, opacity: 0 }} className="overflow-hidden">
            <EditorialCard tone="soft">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-sans text-[10px] font-bold uppercase tracking-[0.18em]"
                         style={{ color: INK_MUTE }}>Subject</label>
                  <select value={formSubject}
                          onChange={(e) => { setFormSubject(e.target.value); setFormGrade(''); }}
                          className={fieldClass} style={{ ...fieldStyle, marginTop: 4 }}>
                    {subjects.map(s => <option key={s.subjectName} value={s.subjectName}>{s.subjectName}</option>)}
                  </select>
                </div>
                <div>
                  <label className="font-sans text-[10px] font-bold uppercase tracking-[0.18em]"
                         style={{ color: INK_MUTE }}>Grade</label>
                  <select value={formGrade} onChange={(e) => setFormGrade(e.target.value)}
                          className={fieldClass} style={{ ...fieldStyle, marginTop: 4 }}>
                    <option value="">Select…</option>
                    {gradeOptions.map(g => <option key={g} value={g}>{g} ({gradeToPoints(g)} pts)</option>)}
                  </select>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3 mt-3">
                <div>
                  <label className="font-sans text-[10px] font-bold uppercase tracking-[0.18em]"
                         style={{ color: INK_MUTE }}>Date</label>
                  <input type="date" value={formDate} onChange={(e) => setFormDate(e.target.value)}
                         className={fieldClass} style={{ ...fieldStyle, marginTop: 4 }} />
                </div>
                <div>
                  <label className="font-sans text-[10px] font-bold uppercase tracking-[0.18em]"
                         style={{ color: INK_MUTE }}>Label (optional)</label>
                  <input type="text" value={formLabel} onChange={(e) => setFormLabel(e.target.value)}
                         placeholder="e.g. Mock 1" maxLength={30}
                         className={fieldClass} style={{ ...fieldStyle, marginTop: 4 }} />
                </div>
              </div>
              <button onClick={addResult} disabled={!formGrade}
                      className="w-full py-2.5 mt-4 text-[13px] font-bold disabled:opacity-40 transition-all"
                      style={primaryBtnStyle}>
                Save Result
              </button>
            </EditorialCard>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Mock feedback card — calmer */}
      <AnimatePresence>
        {mockFeedback && (
          <MotionDiv initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }}
                     exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.3 }} className="overflow-hidden">
            <EditorialCard tone="soft" style={
              mockFeedback.totalPtsDiff > 0
                ? { background: STATUS_SOLID_TINT }
                : mockFeedback.totalPtsDiff < 0
                  ? { background: STATUS_GAP_TINT }
                  : undefined
            }>
              <div className="flex items-center justify-between mb-3">
                <p className="font-serif text-[14px] font-bold" style={{ color: INK }}>
                  {mockFeedback.totalPtsDiff > 0 ? 'Progress since last mock'
                    : mockFeedback.totalPtsDiff < 0 ? 'Changes since last mock'
                      : 'Compared to last mock'}
                </p>
                <button onClick={() => setMockFeedback(null)} style={{ color: INK_MUTE }}>
                  <X size={14} />
                </button>
              </div>
              {mockFeedback.improved.length > 0 && (
                <div className="mb-2">
                  <Overline color={STATUS_SOLID_DEEP}>Improved</Overline>
                  <div className="space-y-1 mt-1">
                    {mockFeedback.improved.map(s => (
                      <p key={s.subject} className="font-sans text-[12px] flex items-center gap-1.5"
                         style={{ color: INK_SOFT }}>
                        <TrendingUp size={11} style={{ color: STATUS_SOLID_DEEP }} />
                        {s.subject}: {s.from} → {s.to} <span className="font-bold" style={{ color: STATUS_SOLID_DEEP }}>(+{s.ptsDiff}pts)</span>
                      </p>
                    ))}
                  </div>
                </div>
              )}
              {mockFeedback.declined.length > 0 && (
                <div className="mb-2">
                  <Overline color={STATUS_GAP_DEEP}>Needs attention</Overline>
                  <div className="space-y-1 mt-1">
                    {mockFeedback.declined.map(s => (
                      <p key={s.subject} className="font-sans text-[12px] flex items-center gap-1.5"
                         style={{ color: INK_SOFT }}>
                        <AlertTriangle size={11} style={{ color: STATUS_GAP_DEEP }} />
                        {s.subject}: {s.from} → {s.to} <span className="font-bold" style={{ color: STATUS_GAP_DEEP }}>({s.ptsDiff}pts)</span>
                      </p>
                    ))}
                  </div>
                </div>
              )}
              {mockFeedback.unchanged.length > 0 && (
                <p className="font-mono text-[10px] mt-1" style={{ color: INK_MUTE }}>
                  Unchanged: {mockFeedback.unchanged.join(', ')}
                </p>
              )}
              {mockFeedback.totalPtsDiff !== 0 && (
                <div className="mt-3 pt-3" style={{ borderTop: `1px solid ${INK}1A` }}>
                  <p className="font-serif text-[13px] font-bold"
                     style={{ color: mockFeedback.totalPtsDiff > 0 ? STATUS_SOLID_DEEP : STATUS_GAP_DEEP }}>
                    Net change: {mockFeedback.totalPtsDiff > 0 ? '+' : ''}{mockFeedback.totalPtsDiff} CAO points
                  </p>
                </div>
              )}
            </EditorialCard>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* SVG Chart card */}
      {chartSubjects.length > 0 && (
        <EditorialCard tone="soft">
          <Overline className="mb-3">Mock trajectory</Overline>
          <TrajectoryChart subjects={subjects} resultsBySubject={resultsBySubject} />
        </EditorialCard>
      )}

      {/* Subject status table — refined paper rows */}
      <section>
        <SectionHeader overline="The standings" title="Subject status" rule />
        <div className="mt-3">
          <EditorialCard tone="soft" padded={false}>
            {[...subjects].map((s, sIdx) => {
              const results = resultsBySubject[s.subjectName] || [];
              const latest = results[results.length - 1];
              const targetPts = getPointsForGrade(s.targetGrade, false);
              const currentPts = latest ? gradeToPoints(latest.grade) : null;
              const rawHex = getDistinctSubjectHex(s.subjectName, sIdx);
              const hexColor = mutedSubjectHex(rawHex, 0.22);
              const gap = currentPts !== null ? targetPts - currentPts : null;
              return { s, latest, currentPts, hexColor, gap, targetPts };
            }).sort((a, b) => {
              const gA = a.gap ?? 999;
              const gB = b.gap ?? 999;
              if (gA <= 0 && gB > 0) return 1;
              if (gA > 0 && gB <= 0) return -1;
              return gB - gA;
            }).map((item, idx, arr) => {
              const { s, latest, currentPts, hexColor, gap } = item;
              const isLast = idx === arr.length - 1;
              const ptsColor = gap !== null && gap <= 0 ? STATUS_SOLID_DEEP : gap !== null && gap > 0 ? STATUS_GAP_DEEP : INK;
              return (
                <div
                  key={s.subjectName}
                  className="flex items-center gap-3 px-5 py-3"
                  style={isLast ? undefined : { borderBottom: `1px solid ${INK}10` }}
                >
                  <span className="shrink-0"
                        style={{ width: 12, height: 12, borderRadius: '50%', background: hexColor, border: `1px solid ${INK}33` }} />
                  <span className="font-serif text-[14px] font-semibold flex-1 min-w-0 truncate" style={{ color: INK }}>
                    {s.subjectName}
                  </span>
                  {latest ? (
                    <>
                      <span className="font-mono text-[11px]" style={{ color: INK_MUTE }}>{latest.grade}</span>
                      <span className="font-mono text-[12px] font-bold tabular-nums" style={{ color: ptsColor }}>{currentPts}pts</span>
                    </>
                  ) : (
                    <span className="font-mono text-[11px]" style={{ color: INK_FAINT }}>—</span>
                  )}
                  {gap !== null ? (
                    gap <= 0
                      ? <Pill bg={STATUS_SOLID_TINT} fg={STATUS_SOLID_DEEP}>On target</Pill>
                      : <Pill bg={STATUS_GAP_TINT} fg={STATUS_GAP_DEEP}>{gap}pt gap</Pill>
                  ) : (
                    <span className="font-mono text-[11px]" style={{ color: INK_MUTE }}>{s.targetGrade}</span>
                  )}
                </div>
              );
            })}
          </EditorialCard>
        </div>
      </section>

      {mockResults.length === 0 && (
        <div className="text-center py-12 space-y-4">
          <div className="w-14 h-14 mx-auto rounded-2xl flex items-center justify-center"
               style={{ background: '#FFFFFF', border: `1px solid ${INK}14` }}>
            <TrendingUp size={26} style={{ color: ACCENT }} />
          </div>
          <h3 className="font-serif text-[18px] font-bold" style={{ color: INK }}>
            Track your mock exam trajectory
          </h3>
          <p className="font-sans text-[13px] max-w-xs mx-auto leading-relaxed" style={{ color: INK_MUTE }}>
            Log mock results to see your points climb over time and identify the subjects worth targeting.
          </p>
        </div>
      )}
    </div>
  );
};

export default TrajectoryPanel;
