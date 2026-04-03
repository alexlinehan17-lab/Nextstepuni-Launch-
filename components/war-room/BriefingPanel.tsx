/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import {
  Clock, Activity, ChevronDown, AlertTriangle, BookOpen,
  Shield, CheckCircle, Target,
} from 'lucide-react';
import {
  type StudentSubjectProfile, type TimetableCompletions,
  type Grade, getPointsForGrade,
} from '../subjectData';
import { getDistinctSubjectHex } from '../../studySessionData';
import { getSubjectGuidance, type SubjectGuidance } from '../subjectGuidance';
import {
  type TopicMap, type MockResult,
  CARD_STYLE, CARD_CLASS, gradeToPoints,
} from './warRoomShared';

// ── Helpers for study pattern charts ───────────────────────

function getMonday(d: Date): Date {
  const day = d.getDay();
  const diff = d.getDate() - day + (day === 0 ? -6 : 1);
  const m = new Date(d);
  m.setDate(diff);
  m.setHours(0, 0, 0, 0);
  return m;
}

function toISODateKey(d: Date): string {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

// ── Types ──────────────────────────────────────────────────

interface Recommendation {
  subject: string;
  priority: number; // 0-100
  concerns: string[];
  action: string;
  guidance?: SubjectGuidance;
  latestGrade?: string;
}

interface BriefingPanelProps {
  subjects: StudentSubjectProfile['subjects'];
  topicMap: TopicMap;
  mockResults: MockResult[];
  allocations: { subjectName: string; sessions: number }[];
  hoursStudiedMap: Record<string, number>;
  weeksUntilExam: number;
  blockDuration: number;
  daysUntilExam: number;
  timetableCompletions: TimetableCompletions;
}

// ── Component ──────────────────────────────────────────────

const BriefingPanel: React.FC<BriefingPanelProps> = ({
  subjects, topicMap, mockResults, allocations, hoursStudiedMap, weeksUntilExam, blockDuration, daysUntilExam, timetableCompletions,
}) => {
  const [showStudyPatterns, setShowStudyPatterns] = useState(false);

  // ── Study pattern data (merged from Insights) ──
  const weeklyData = useMemo(() => {
    const weeks: { label: string; startDate: Date; totalBlocks: number; subjectBlocks: Record<string, number> }[] = [];
    const today = new Date();
    for (let w = 7; w >= 0; w--) {
      const weekStart = getMonday(new Date(today.getTime() - w * 7 * 86400000));
      const subjectBlocks: Record<string, number> = {};
      let total = 0;
      for (let d = 0; d < 7; d++) {
        const dayDate = new Date(weekStart);
        dayDate.setDate(weekStart.getDate() + d);
        const key = toISODateKey(dayDate);
        const blocks = timetableCompletions[key] || [];
        total += blocks.length;
        for (const blockId of blocks) {
          const subName = blockId.split('|')[0];
          if (subName) subjectBlocks[subName] = (subjectBlocks[subName] || 0) + 1;
        }
      }
      const label = `${weekStart.getDate()}/${weekStart.getMonth() + 1}`;
      weeks.push({ label, startDate: weekStart, totalBlocks: total, subjectBlocks });
    }
    return weeks;
  }, [timetableCompletions]);

  const heatmapData = useMemo(() => {
    const days: { date: string; blocks: number }[] = [];
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    for (let i = 27; i >= 0; i--) {
      const d = new Date(today.getTime() - i * 86400000);
      const key = toISODateKey(d);
      const blocks = (timetableCompletions[key] || []).length;
      days.push({ date: key, blocks });
    }
    return days;
  }, [timetableCompletions]);

  const maxDayBlocks = Math.max(1, ...heatmapData.map(d => d.blocks));
  const maxWeekBlocks = Math.max(1, ...weeklyData.map(w => w.totalBlocks));
  const currentWeekSubjects = weeklyData[weeklyData.length - 1]?.subjectBlocks ?? {};
  const currentWeekTotal = Object.values(currentWeekSubjects).reduce((a, b) => a + b, 0);
  const SPW = 360; const SPH = 120;
  const SPAD = { top: 10, right: 10, bottom: 20, left: 30 };
  const spPlotW = SPW - SPAD.left - SPAD.right;
  const spPlotH = SPH - SPAD.top - SPAD.bottom;

  const recommendations = useMemo((): Recommendation[] => {
    const recs: Recommendation[] = [];

    for (const s of subjects) {
      const concerns: string[] = [];
      let priority = 0;

      // Coverage analysis
      const topics = topicMap[s.subjectName] || [];
      if (topics.length > 0) {
        const notStarted = topics.filter(t => t.confidence === 'not-started').length;
        const shaky = topics.filter(t => t.confidence === 'shaky').length;
        const weakPct = (notStarted + shaky * 0.5) / topics.length;
        if (notStarted > 0) {
          concerns.push(`${notStarted} topic${notStarted > 1 ? 's' : ''} not started`);
          priority += weakPct * 40;
        }
        if (shaky > 0 && notStarted === 0) {
          concerns.push(`${shaky} shaky topic${shaky > 1 ? 's' : ''}`);
          priority += weakPct * 25;
        }
      }

      // Trajectory analysis
      const results = mockResults
        .filter(r => r.subject === s.subjectName && r.grade && r.date)
        .sort((a, b) => (a.date ?? '').localeCompare(b.date ?? ''));
      if (results.length > 0) {
        const latest = results[results.length - 1];
        const latestPts = gradeToPoints(latest.grade);
        const targetPts = getPointsForGrade(s.targetGrade, false);
        const gap = targetPts - latestPts;
        if (gap > 0) {
          concerns.push(`${gap} point gap to target (${latest.grade} → ${s.targetGrade})`);
          priority += Math.min(40, (gap / targetPts) * 60);
        }
        // Declining trend
        if (results.length >= 2) {
          const prev = results[results.length - 2];
          const prevPts = gradeToPoints(prev.grade);
          if (latestPts < prevPts) {
            concerns.push('grade declining');
            priority += 15;
          }
        }
      }

      // Time allocation relative to need
      const alloc = allocations.find(a => a.subjectName === s.subjectName);
      const sessionsPerWeek = alloc?.sessions ?? 1;

      if (concerns.length === 0 && topics.length === 0 && results.length === 0) {
        // No data — gentle nudge
        concerns.push('no coverage data or test results logged yet');
        priority += 5;
      }

      // Generate action text
      let action = '';
      if (concerns.length > 0) {
        const weakTopics = topics.filter(t => t.confidence === 'not-started').slice(0, 2).map(t => t.name);
        if (weakTopics.length > 0) {
          action = `Prioritise: ${weakTopics.join(', ')}. You have ${sessionsPerWeek} session${sessionsPerWeek > 1 ? 's' : ''} allocated this week.`;
        } else if (topics.filter(t => t.confidence === 'shaky').length > 0) {
          const shakyNames = topics.filter(t => t.confidence === 'shaky').slice(0, 2).map(t => t.name);
          action = `Strengthen: ${shakyNames.join(', ')}.`;
        } else {
          action = `${sessionsPerWeek} session${sessionsPerWeek > 1 ? 's' : ''} allocated this week.`;
        }
      }

      if (concerns.length > 0) {
        // Derive latest grade for subject guidance
        const latestGrade = results.length > 0
          ? results[results.length - 1].grade
          : (s.currentGrade as string | undefined);
        const guidance = latestGrade ? getSubjectGuidance(s.subjectName, latestGrade) : undefined;
        recs.push({ subject: s.subjectName, priority, concerns, action, guidance, latestGrade });
      }
    }

    recs.sort((a, b) => b.priority - a.priority);
    return recs;
  }, [subjects, topicMap, mockResults, allocations]);

  // Best and worst subjects
  const subjectsWithResults = subjects.filter(s =>
    mockResults.some(r => r.subject === s.subjectName)
  );

  const bestSubject = useMemo(() => {
    let best: { name: string; surplus: number } | null = null;
    for (const s of subjectsWithResults) {
      const results = mockResults.filter(r => r.subject === s.subjectName && r.grade && r.date).sort((a, b) => (a.date ?? '').localeCompare(b.date ?? ''));
      const latest = results[results.length - 1];
      if (!latest) continue;
      const surplus = gradeToPoints(latest.grade) - getPointsForGrade(s.targetGrade, false);
      if (!best || surplus > best.surplus) {
        best = { name: s.subjectName, surplus };
      }
    }
    return best;
  }, [subjectsWithResults, mockResults]);

  const hasData = topicMap && Object.values(topicMap).some(t => t.length > 0) || mockResults.length > 0;

  const [expandedGuidance, setExpandedGuidance] = useState<string | null>(null);

  return (
    <div className="space-y-5">
      {/* Countdown reminder — bold warm banner */}
      <div className="flex items-center gap-3 px-5 py-4 rounded-2xl" style={{ backgroundColor: '#F5D08A', boxShadow: '0 2px 8px rgba(212,137,28,0.12)' }}>
        <Clock size={20} style={{ color: '#8B5E2A' }} className="shrink-0" />
        <p style={{ color: '#5C3D14' }}>
          <span className="text-2xl font-black text-[#1A1A1A] dark:text-white">{daysUntilExam}</span>{' '}
          <span className="text-sm font-bold">days remaining</span>
          <span className="text-sm"> — {weeksUntilExam} weeks of study</span>
        </p>
      </div>

      {/* Study Patterns — collapsible */}
      <div className={`overflow-hidden ${CARD_CLASS}`} style={CARD_STYLE}>
        <button
          onClick={() => setShowStudyPatterns(!showStudyPatterns)}
          className="w-full flex items-center justify-between px-4 py-3 text-left"
        >
          <div className="flex items-center gap-2">
            <Activity size={14} style={{ color: '#2A7D6F' }} />
            <span className="text-xs font-bold text-zinc-700 dark:text-zinc-300">Study Patterns</span>
            {currentWeekTotal > 0 && (
              <span className="text-[10px] text-zinc-400 dark:text-zinc-500">{currentWeekTotal} sessions this week</span>
            )}
          </div>
          <ChevronDown size={14} className={`text-zinc-400 transition-transform ${showStudyPatterns ? 'rotate-180' : ''}`} />
        </button>
        <AnimatePresence>
          {showStudyPatterns && (
            <MotionDiv
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.25 }}
              className="overflow-hidden"
            >
              <div className="px-4 pb-4 space-y-5">
                {/* Weekly volume bar chart */}
                <div>
                  <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">Weekly Volume</p>
                  <svg viewBox={`0 0 ${SPW} ${SPH}`} className="w-full" style={{ maxHeight: 140 }}>
                    {[0, 0.5, 1].map(frac => {
                      const y = SPAD.top + spPlotH * (1 - frac);
                      const val = Math.round(maxWeekBlocks * frac);
                      return (
                        <g key={frac}>
                          <line x1={SPAD.left} y1={y} x2={SPW - SPAD.right} y2={y} stroke="currentColor" className="text-zinc-200 dark:text-zinc-700" strokeWidth="0.5" />
                          {frac > 0 && <text x={SPAD.left - 4} y={y + 3} textAnchor="end" className="text-zinc-400 dark:text-zinc-500 fill-current" fontSize="7">{val}</text>}
                        </g>
                      );
                    })}
                    {weeklyData.map((w, i) => {
                      const barW = Math.max(8, spPlotW / weeklyData.length - 4);
                      const x = SPAD.left + (i / weeklyData.length) * spPlotW + 2;
                      const barH = maxWeekBlocks > 0 ? (w.totalBlocks / maxWeekBlocks) * spPlotH : 0;
                      const isCurrentWeek = i === weeklyData.length - 1;
                      return (
                        <g key={i}>
                          <rect x={x} y={SPAD.top + spPlotH - barH} width={barW} height={Math.max(0, barH)} rx="3" fill={isCurrentWeek ? '#2A7D6F' : undefined} className={isCurrentWeek ? '' : 'fill-zinc-300 dark:fill-zinc-600'} opacity={isCurrentWeek ? 1 : 0.7} />
                          <text x={x + barW / 2} y={SPH - 4} textAnchor="middle" className="fill-current text-zinc-400 dark:text-zinc-500" fontSize="7">{w.label}</text>
                          {w.totalBlocks > 0 && <text x={x + barW / 2} y={SPAD.top + spPlotH - barH - 3} textAnchor="middle" className="fill-current text-zinc-500 dark:text-zinc-400" fontSize="7" fontWeight="600">{w.totalBlocks}</text>}
                        </g>
                      );
                    })}
                  </svg>
                </div>

                {/* Daily consistency heatmap */}
                <div>
                  <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">Daily Consistency (28 days)</p>
                  <div className="flex flex-wrap gap-1 justify-center">
                    {heatmapData.map(d => {
                      const intensity = d.blocks / maxDayBlocks;
                      const bgColor = d.blocks === 0
                        ? '#EDEAE6'
                        : intensity > 0.66
                          ? '#2A7D6F'
                          : intensity > 0.33
                            ? '#6BB5A8'
                            : '#B8DDD5';
                      return <div key={d.date} className="w-5 h-5 rounded-sm" style={{ backgroundColor: bgColor }} title={`${d.date}: ${d.blocks} session${d.blocks !== 1 ? 's' : ''}`} />;
                    })}
                  </div>
                  <div className="flex items-center justify-center gap-2 mt-2 text-[10px] text-zinc-400 dark:text-zinc-500">
                    <span>Less</span>
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: '#EDEAE6' }} />
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: '#B8DDD5' }} />
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: '#6BB5A8' }} />
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: '#2A7D6F' }} />
                    <span>More</span>
                  </div>
                </div>

                {/* Subject balance — this week */}
                {currentWeekTotal > 0 && (
                  <div>
                    <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">Subject Balance — This Week</p>
                    <div className="flex h-3.5 rounded-full overflow-hidden">
                      {subjects.map((s, i) => {
                        const count = currentWeekSubjects[s.subjectName] || 0;
                        if (count === 0) return null;
                        const pct = (count / currentWeekTotal) * 100;
                        const hexColor = getDistinctSubjectHex(s.subjectName, i);
                        return <div key={s.subjectName} style={{ width: `${pct}%`, backgroundColor: hexColor }} className="h-full" title={`${s.subjectName}: ${count} sessions`} />;
                      })}
                    </div>
                    <div className="flex flex-wrap gap-x-3 gap-y-1 mt-2">
                      {subjects.map((s, i) => {
                        const count = currentWeekSubjects[s.subjectName] || 0;
                        if (count === 0) return null;
                        const hexColor = getDistinctSubjectHex(s.subjectName, i);
                        return (
                          <div key={s.subjectName} className="flex items-center gap-1.5">
                            <span className="w-2 h-2 rounded-full shrink-0" style={{ backgroundColor: hexColor }} />
                            <span className="text-[10px] text-zinc-500 dark:text-zinc-400">{s.subjectName}</span>
                            <span className="text-[10px] font-bold text-zinc-600 dark:text-zinc-300">{count}</span>
                          </div>
                        );
                      })}
                    </div>
                    {subjects.filter(s => !currentWeekSubjects[s.subjectName]).length > 0 && (
                      <div className="mt-2 flex items-start gap-2 px-3 py-2 rounded-lg bg-amber-50 dark:bg-amber-900/15 border border-amber-200 dark:border-amber-800/30">
                        <AlertTriangle size={12} className="text-amber-500 mt-0.5 shrink-0" />
                        <p className="text-[10px] text-amber-700 dark:text-amber-300">
                          <strong>Not studied this week:</strong>{' '}
                          {subjects.filter(s => !currentWeekSubjects[s.subjectName]).map(s => s.subjectName).join(', ')}
                        </p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </MotionDiv>
          )}
        </AnimatePresence>
      </div>

      {hasData ? (
        <>
          {/* Priority Actions — all in one card, Linear-style rows */}
          <div>
            <p className="text-[10px] font-bold uppercase tracking-widest mb-2 text-[#A8A29E] dark:text-zinc-500">Priority Actions</p>
            <div className="space-y-2">
              {recommendations.slice(0, 5).map((rec, i) => {
                const subjectIdx = subjects.findIndex(s => s.subjectName === rec.subject);
                // Maximally distinct colours
                const BRIEFING_COLORS: Record<string, string> = {
                  'Applied Maths': '#6C5CE7', 'Applied Mathematics': '#6C5CE7',
                  'Economics': '#E67E22', 'Religious Education': '#E84393',
                  'Business': '#0984E3', 'Politics & Society': '#00B894',
                  'Mathematics': '#2D3436', 'English': '#E74C3C',
                };
                const hex = BRIEFING_COLORS[rec.subject] || getDistinctSubjectHex(rec.subject, subjectIdx >= 0 ? subjectIdx : i);
                const isUrgent = rec.priority >= 30;
                const isTop = i === 0;
                return (
                  <div
                    key={rec.subject}
                    className="rounded-2xl px-5 py-4 transition-all"
                    style={{
                      backgroundColor: isTop ? `${hex}14` : `${hex}08`,
                      border: `1px solid ${hex}12`,
                    }}
                  >
                    {/* L1: Subject name — 18px bold, subject colour */}
                    <div className="flex items-center gap-2.5 mb-1 flex-wrap">
                      <div className="w-3.5 h-3.5 rounded-full shrink-0" style={{ backgroundColor: hex }} />
                      <span className="text-lg font-bold" style={{ color: hex }}>{rec.subject}</span>
                      {isTop && <span className="text-[8px] font-bold uppercase tracking-wider px-2 py-0.5 rounded" style={{ backgroundColor: '#2D2D2D', color: '#fff' }}>Top priority</span>}
                    </div>

                    {/* L2: Stats — 13px regular, warm grey */}
                    <p className="text-[13px] ml-6 mb-2 text-[#78716C] dark:text-zinc-400" style={{ fontWeight: 400 }}>
                      {rec.concerns.join(' · ')}
                    </p>

                    {/* L3: Action text — 15px medium, teal */}
                    {rec.action && (
                      <p className="text-[15px] ml-6 mb-3" style={{ color: '#2A7D6F', fontWeight: 500 }}>{rec.action}</p>
                    )}

                    {/* Examiner Insights — pill button */}
                    {rec.guidance && (
                      <div className="ml-6">
                        <button
                          onClick={() => setExpandedGuidance(expandedGuidance === rec.subject ? null : rec.subject)}
                          className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[12px] font-semibold transition-all ${
                            expandedGuidance === rec.subject ? '' : 'bg-[#F0EDE8] dark:bg-zinc-700 text-[#78716C] dark:text-zinc-400'
                          }`}
                          style={expandedGuidance === rec.subject ? {
                            backgroundColor: `${hex}15`,
                            color: hex,
                          } : undefined}
                        >
                          <BookOpen size={13} />
                          Examiner Insights
                          <ChevronDown size={12} className={`transition-transform ${expandedGuidance === rec.subject ? 'rotate-180' : ''}`} />
                        </button>
                        <AnimatePresence>
                          {expandedGuidance === rec.subject && (
                            <MotionDiv
                              initial={{ height: 0, opacity: 0 }}
                              animate={{ height: 'auto', opacity: 1 }}
                              exit={{ height: 0, opacity: 0 }}
                              transition={{ duration: 0.25 }}
                              className="overflow-hidden"
                            >
                              <div className="mt-3 pt-3 space-y-3 border-t border-[#EDEBE8] dark:border-zinc-800">
                                {/* L4: Section headers — 14px semibold */}
                                <div>
                                  <p className="text-[14px] mb-1.5" style={{ color: '#2D2D2D', fontWeight: 600 }}>Why students struggle here</p>
                                  <ul className="space-y-1.5">
                                    {rec.guidance.commonStruggles.map((s, si) => (
                                      <li key={si} className="flex items-start gap-2.5 text-[14px]" style={{ color: '#4A4A4A', fontWeight: 400 }}>
                                        <span className="mt-2 w-1.5 h-1.5 rounded-full shrink-0" style={{ backgroundColor: '#D4891C' }} />
                                        {s}
                                      </li>
                                    ))}
                                  </ul>
                                </div>
                                <div>
                                  <p className="text-[14px] mb-1.5" style={{ color: '#2D2D2D', fontWeight: 600 }}>What to do</p>
                                  <ul className="space-y-1.5">
                                    {rec.guidance.actions.map((a, ai) => (
                                      <li key={ai} className="flex items-start gap-2.5 text-[14px]" style={{ color: '#4A4A4A', fontWeight: 400 }}>
                                        <span className="mt-2 w-1.5 h-1.5 rounded-full shrink-0" style={{ backgroundColor: '#2A7D6F' }} />
                                        {a}
                                      </li>
                                    ))}
                                  </ul>
                                </div>
                                {/* Exam trap callout */}
                                <div className="flex items-start gap-2.5 p-3.5 rounded-xl" style={{ backgroundColor: '#FDEBD0' }}>
                                  <AlertTriangle size={14} style={{ color: '#D4891C' }} className="shrink-0 mt-0.5" />
                                  <div>
                                    <p className="text-[14px] mb-0.5" style={{ color: '#D4891C', fontWeight: 700 }}>Exam trap</p>
                                    <p className="text-[14px]" style={{ color: '#4A4A4A', fontWeight: 400 }}>{rec.guidance.examTrap}</p>
                                  </div>
                                </div>
                                {/* Mindset shift callout */}
                                <div className="flex items-start gap-2.5 p-3.5 rounded-xl" style={{ backgroundColor: '#E8F8F5' }}>
                                  <Shield size={14} style={{ color: '#2A7D6F' }} className="shrink-0 mt-0.5" />
                                  <div>
                                    <p className="text-[14px] mb-0.5" style={{ color: '#2A7D6F', fontWeight: 700 }}>Mindset shift</p>
                                    <p className="text-[14px]" style={{ color: '#4A4A4A', fontWeight: 400 }}>{rec.guidance.mindsetShift}</p>
                                  </div>
                                </div>
                              </div>
                            </MotionDiv>
                          )}
                        </AnimatePresence>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Overall summary */}
          {bestSubject && (
            <div className="px-5 py-4 rounded-2xl" style={{ backgroundColor: '#C6F0D9', border: '1px solid #8DD7AE' }}>
              <div className="flex items-center gap-2.5">
                <CheckCircle size={18} style={{ color: '#1B5E3B' }} />
                <p className="text-sm font-bold" style={{ color: '#1B5E3B' }}>
                  {bestSubject.surplus >= 0
                    ? `Strongest: ${bestSubject.name} — above target`
                    : `Closest to target: ${bestSubject.name}`
                  }
                </p>
              </div>
            </div>
          )}
        </>
      ) : (
        <div className="text-center py-12 text-zinc-400 dark:text-zinc-500 space-y-3">
          <Target size={36} className="mx-auto opacity-40" />
          <p className="text-sm font-medium">No strategic data yet</p>
          <div className="text-xs space-y-1">
            <p>Add topics in the <strong>Coverage</strong> tab to track what you've studied</p>
            <p>Log test results in the <strong>Trajectory</strong> tab to track your grades</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default BriefingPanel;
