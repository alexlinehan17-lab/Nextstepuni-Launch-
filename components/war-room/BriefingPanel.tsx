/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import {
  Activity, ArrowRight, ChevronDown, AlertTriangle, BookOpen,
  Shield, CheckCircle, Target,
} from 'lucide-react';
import {
  type StudentSubjectProfile, type TimetableCompletions,
  getPointsForGrade,
} from '../subjectData';
import { getDistinctSubjectHex } from '../../studySessionData';
import { getSubjectGuidance, type SubjectGuidance } from '../subjectGuidance';
import {
  type TopicMap, type MockResult,
  gradeToPoints, mutedSubjectHex,
  INK, INK_SOFT, INK_MUTE, INK_FAINT, ACCENT,
  STATUS_SOLID, STATUS_SOLID_DEEP, STATUS_SOLID_TINT,
  STATUS_SHAKY, STATUS_SHAKY_DEEP, STATUS_SHAKY_TINT,
} from './warRoomShared';
import {
  Overline, SectionHeader, EditorialCard,
  SketchedLeaf, accentButtonClass, accentButtonStyle,
} from './warRoomPrimitives';

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

interface Recommendation {
  subject: string;
  priority: number;
  evidence: boolean;
  concerns: string[];
  action: string;
  guidance?: SubjectGuidance;
  latestGrade?: string;
  targetGrade: string;
  sessionsPerWeek: number;
  topicsTotal: number;
  notStarted: number;
  shaky: number;
  solid: number;
  coveragePct: number | null;
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
  onReviewSubjects?: () => void;
}

const BriefingPanel: React.FC<BriefingPanelProps> = ({
  subjects, topicMap, mockResults, allocations, weeksUntilExam: _weeksUntilExam, daysUntilExam, timetableCompletions, onReviewSubjects,
}) => {
  const [showStudyPatterns, setShowStudyPatterns] = useState(false);

  // ── Study pattern data ──
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

  // ── Recommendations ──
  const recommendations = useMemo((): Recommendation[] => {
    const recs: Recommendation[] = [];

    for (const s of subjects) {
      const concerns: string[] = [];
      let priority = 0;

      const topics = topicMap[s.subjectName] || [];
      const notStarted = topics.filter(t => t.confidence === 'not-started').length;
      const shaky = topics.filter(t => t.confidence === 'shaky').length;
      const solid = topics.filter(t => t.confidence === 'solid').length;
      const coveragePct = topics.length > 0
        ? Math.round(((solid + shaky * 0.5) / topics.length) * 100)
        : null;
      if (topics.length > 0) {
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
        if (results.length >= 2) {
          const prev = results[results.length - 2];
          const prevPts = gradeToPoints(prev.grade);
          if (latestPts < prevPts) {
            concerns.push('grade declining');
            priority += 15;
          }
        }
      }

      const alloc = allocations.find(a => a.subjectName === s.subjectName);
      const sessionsPerWeek = alloc?.sessions ?? 1;
      const hasEvidence = topics.length > 0 || results.length > 0;

      if (concerns.length === 0 && topics.length === 0 && results.length === 0) {
        concerns.push('No coverage data or test results logged yet');
        priority += 5;
      }

      let action = '';
      if (concerns.length > 0) {
        const weakTopics = topics.filter(t => t.confidence === 'not-started').slice(0, 2).map(t => t.name);
        if (weakTopics.length > 0) {
          action = `Prioritise: ${weakTopics.join(', ')}. You have ${sessionsPerWeek} session${sessionsPerWeek > 1 ? 's' : ''} allocated this week.`;
        } else if (topics.filter(t => t.confidence === 'shaky').length > 0) {
          const shakyNames = topics.filter(t => t.confidence === 'shaky').slice(0, 2).map(t => t.name);
          action = `Strengthen: ${shakyNames.join(', ')}.`;
        } else {
          action = `Map the first topics, then protect ${sessionsPerWeek} session${sessionsPerWeek > 1 ? 's' : ''} for this subject this week.`;
        }
      }

      if (concerns.length > 0) {
        const latestGrade = results.length > 0
          ? results[results.length - 1].grade
          : (s.currentGrade as string | undefined);
        const guidance = latestGrade ? getSubjectGuidance(s.subjectName, latestGrade) : undefined;
        recs.push({
          subject: s.subjectName,
          priority,
          evidence: hasEvidence,
          concerns,
          action,
          guidance,
          latestGrade,
          targetGrade: s.targetGrade,
          sessionsPerWeek,
          topicsTotal: topics.length,
          notStarted,
          shaky,
          solid,
          coveragePct,
        });
      }
    }

    recs.sort((a, b) => b.priority - a.priority);
    return recs;
  }, [subjects, topicMap, mockResults, allocations]);

  const subjectsWithResults = subjects.filter(s =>
    mockResults.some(r => r.subject === s.subjectName)
  );

  const bestSubject = useMemo(() => {
    let best: { name: string; surplus: number } | null = null;
    for (const s of subjectsWithResults) {
      const results = mockResults.filter(r => r.subject === s.subjectName && r.grade && r.date)
        .sort((a, b) => (a.date ?? '').localeCompare(b.date ?? ''));
      const latest = results[results.length - 1];
      if (!latest) continue;
      const surplus = gradeToPoints(latest.grade) - getPointsForGrade(s.targetGrade, false);
      if (!best || surplus > best.surplus) best = { name: s.subjectName, surplus };
    }
    return best;
  }, [subjectsWithResults, mockResults]);

  // A configured subject profile is already enough to produce a useful first
  // briefing. Missing coverage or mock evidence becomes the recommendation,
  // rather than turning the whole workspace into an empty state.
  const hasData = subjects.length > 0;
  const [expandedGuidance, setExpandedGuidance] = useState<string | null>(null);

  const topRec = recommendations[0];
  const rankedRecs = recommendations.slice(1);

  const subjectIdx = (name: string) => subjects.findIndex(s => s.subjectName === name);
  const subjectHex = (name: string, fallback = 0) => mutedSubjectHex(getDistinctSubjectHex(name, subjectIdx(name) >= 0 ? subjectIdx(name) : fallback), 0.22);

  return (
    <div className="space-y-7">
      <header className="border-b border-[var(--outline-soft)] pb-5">
        <Overline color={ACCENT}>Today’s briefing</Overline>
        <h2 className="mt-2 font-serif text-[26px] font-semibold leading-tight text-[var(--ink-primary)] sm:text-[30px]">
          What needs attention now
        </h2>
        <p className="mt-2 max-w-2xl text-sm leading-relaxed text-[var(--ink-secondary)]">
          Your highest-impact move, based on coverage, recent results and the {daysUntilExam} days remaining.
        </p>
      </header>

      {/* ── Study Patterns — refined collapsible ── */}
      <EditorialCard tone="soft" padded={false}>
        <button
          onClick={() => setShowStudyPatterns(!showStudyPatterns)}
          className="w-full flex items-center justify-between px-5 py-3.5 text-left"
        >
          <div className="flex items-center gap-2">
            <Activity size={14} style={{ color: ACCENT }} />
            <span className="font-serif text-[13px] font-semibold" style={{ color: INK }}>Study patterns</span>
            {currentWeekTotal > 0 && (
              <span className="font-mono text-[11px]" style={{ color: INK_MUTE }}>
                {currentWeekTotal} sessions this week
              </span>
            )}
          </div>
          <ChevronDown size={14} style={{ color: INK_MUTE }}
                       className={`transition-transform ${showStudyPatterns ? 'rotate-180' : ''}`} />
        </button>
        <AnimatePresence>
          {showStudyPatterns && (
            <MotionDiv
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.25 }}
              className="overflow-hidden"
              style={{ borderTop: `1px solid color-mix(in srgb, var(--ink-primary) 6%, transparent)` }}
            >
              <div className="px-5 py-5 space-y-6">
                {/* Weekly volume */}
                <div>
                  <Overline className="mb-2">Weekly volume</Overline>
                  <svg viewBox={`0 0 ${SPW} ${SPH}`} className="w-full" style={{ maxHeight: 140 }}>
                    {[0, 0.5, 1].map(frac => {
                      const y = SPAD.top + spPlotH * (1 - frac);
                      const val = Math.round(maxWeekBlocks * frac);
                      return (
                        <g key={frac}>
                          <line x1={SPAD.left} y1={y} x2={SPW - SPAD.right} y2={y}
                                stroke={INK} strokeOpacity={0.08} strokeWidth="0.5" />
                          {frac > 0 && <text x={SPAD.left - 4} y={y + 3} textAnchor="end"
                                             fill={INK_MUTE} fontSize="7">{val}</text>}
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
                          <rect x={x} y={SPAD.top + spPlotH - barH} width={barW} height={Math.max(0, barH)}
                                rx="3" fill={isCurrentWeek ? ACCENT : INK_FAINT} opacity={isCurrentWeek ? 1 : 0.6} />
                          <text x={x + barW / 2} y={SPH - 4} textAnchor="middle"
                                fill={INK_MUTE} fontSize="7">{w.label}</text>
                          {w.totalBlocks > 0 && <text x={x + barW / 2} y={SPAD.top + spPlotH - barH - 3} textAnchor="middle"
                                                     fill={INK_SOFT} fontSize="7" fontWeight="600">{w.totalBlocks}</text>}
                        </g>
                      );
                    })}
                  </svg>
                </div>

                {/* Daily heatmap */}
                <div>
                  <Overline className="mb-2">Daily consistency (28 days)</Overline>
                  <div className="flex flex-wrap gap-1 justify-center">
                    {heatmapData.map(d => {
                      const intensity = d.blocks / maxDayBlocks;
                      const bgColor = d.blocks === 0
                        ? '#EFEAE0'
                        : intensity > 0.66 ? STATUS_SOLID
                          : intensity > 0.33 ? '#9DBFAF'
                            : '#C9DCD2';
                      return <div key={d.date} className="rounded-sm"
                                  style={{ width: 18, height: 18, background: bgColor, border: `1px solid color-mix(in srgb, var(--ink-primary) 6%, transparent)` }}
                                  title={`${d.date}: ${d.blocks} session${d.blocks !== 1 ? 's' : ''}`} />;
                    })}
                  </div>
                  <div className="flex items-center justify-center gap-2 mt-2 font-mono text-[10px]" style={{ color: INK_MUTE }}>
                    <span>Less</span>
                    <div className="rounded-sm" style={{ width: 12, height: 12, background: '#EFEAE0' }} />
                    <div className="rounded-sm" style={{ width: 12, height: 12, background: '#C9DCD2' }} />
                    <div className="rounded-sm" style={{ width: 12, height: 12, background: '#9DBFAF' }} />
                    <div className="rounded-sm" style={{ width: 12, height: 12, background: STATUS_SOLID }} />
                    <span>More</span>
                  </div>
                </div>

                {/* Subject balance */}
                {currentWeekTotal > 0 && (
                  <div>
                    <Overline className="mb-2">Subject balance — this week</Overline>
                    <div className="flex h-3 rounded-full overflow-hidden" style={{ border: `1px solid color-mix(in srgb, var(--ink-primary) 10%, transparent)` }}>
                      {subjects.map((s, i) => {
                        const count = currentWeekSubjects[s.subjectName] || 0;
                        if (count === 0) return null;
                        const pct = (count / currentWeekTotal) * 100;
                        const hex = subjectHex(s.subjectName, i);
                        return <div key={s.subjectName} style={{ width: `${pct}%`, background: hex }} className="h-full" title={`${s.subjectName}: ${count} sessions`} />;
                      })}
                    </div>
                    <div className="flex flex-wrap gap-x-3 gap-y-1.5 mt-2.5">
                      {subjects.map((s, i) => {
                        const count = currentWeekSubjects[s.subjectName] || 0;
                        if (count === 0) return null;
                        const hex = subjectHex(s.subjectName, i);
                        return (
                          <div key={s.subjectName} className="flex items-center gap-1.5">
                            <span className="w-2 h-2 rounded-full shrink-0"
                                  style={{ background: hex, border: `1px solid color-mix(in srgb, var(--ink-primary) 20%, transparent)` }} />
                            <span className="font-sans text-[11px]" style={{ color: INK_SOFT }}>{s.subjectName}</span>
                            <span className="font-mono text-[11px] font-bold" style={{ color: INK }}>{count}</span>
                          </div>
                        );
                      })}
                    </div>
                    {subjects.filter(s => !currentWeekSubjects[s.subjectName]).length > 0 && (
                      <div className="mt-3 flex items-start gap-2 px-3 py-2 rounded-lg"
                           style={{ background: STATUS_SHAKY_TINT, border: `1px solid ${STATUS_SHAKY}33` }}>
                        <AlertTriangle size={12} style={{ color: STATUS_SHAKY_DEEP }} className="mt-0.5 shrink-0" />
                        <p className="font-sans text-[11px]" style={{ color: STATUS_SHAKY_DEEP }}>
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
      </EditorialCard>

      {hasData ? (
        <>
          {/* ── Top priority: recommendation + evidence ── */}
          {topRec && (() => {
            const hex = subjectHex(topRec.subject);
            return (
              <section>
                <SectionHeader overline="Top priority" title="Where to focus first" rule />
                <div
                  className="mt-3 overflow-hidden rounded-[14px] border border-[var(--outline-soft)] bg-[var(--surface-paper)]"
                >
                  <div className="grid lg:grid-cols-[1.35fr_0.65fr]">
                    <div className="p-5 sm:p-6 lg:p-7">
                      <div className="flex items-center gap-2.5">
                        <span className="h-3 w-3 shrink-0 rounded-full"
                              style={{ background: hex, border: `1px solid color-mix(in srgb, var(--ink-primary) 20%, transparent)` }} />
                        <span className="text-[10px] font-bold uppercase tracking-[0.18em] text-[var(--ink-muted)]">
                          {topRec.evidence ? 'Highest impact' : 'Start here'}
                        </span>
                      </div>
                      <h3 className="mt-4 font-serif text-[29px] font-semibold leading-tight text-[var(--ink-primary)] sm:text-[34px]">
                        {topRec.subject}
                      </h3>
                      <p className="mt-2 text-sm leading-relaxed text-[var(--ink-secondary)]">
                        {topRec.concerns.join(' · ')}
                      </p>

                      <div className="mt-7 border-t border-[var(--outline-soft)] pt-5">
                        <Overline color={ACCENT}>Recommended next move</Overline>
                        <p className="mt-2 max-w-2xl text-[15px] font-medium leading-relaxed text-[var(--ink-primary)]">
                          {topRec.action}
                        </p>
                      </div>

                      <div className="mt-6 flex flex-wrap items-center gap-3">
                        {onReviewSubjects && (
                          <button
                            type="button"
                            onClick={onReviewSubjects}
                            className={accentButtonClass}
                            style={accentButtonStyle}
                          >
                            Review {topRec.subject} coverage
                            <ArrowRight size={14} />
                          </button>
                        )}
                        <ExaminerInsightsBlock
                          rec={topRec}
                          isOpen={expandedGuidance === topRec.subject}
                          onToggle={() => setExpandedGuidance(expandedGuidance === topRec.subject ? null : topRec.subject)}
                          accent={hex}
                        />
                      </div>
                    </div>

                    <aside className="border-t border-[var(--outline-soft)] bg-[var(--surface-soft)] p-5 sm:p-6 lg:border-l lg:border-t-0 lg:p-7" aria-label={`${topRec.subject} priority evidence`}>
                      <Overline>Priority evidence</Overline>
                      <div className="mt-6">
                        <div className="flex items-end justify-between gap-4">
                          <div>
                            <p className="font-mono text-[30px] font-semibold leading-none text-[var(--ink-primary)]">
                              {topRec.coveragePct === null ? '—' : `${topRec.coveragePct}%`}
                            </p>
                            <p className="mt-1.5 text-xs text-[var(--ink-secondary)]">
                              {topRec.coveragePct === null ? 'Coverage not mapped' : 'Weighted coverage'}
                            </p>
                          </div>
                          {topRec.topicsTotal > 0 && (
                            <p className="font-mono text-[11px] text-[var(--ink-muted)]">{topRec.topicsTotal} topics</p>
                          )}
                        </div>
                        <div className="mt-3 h-2 overflow-hidden bg-[var(--outline-soft)]">
                          <div
                            className="h-full bg-[var(--ink-primary)] transition-[width] duration-500"
                            style={{ width: `${topRec.coveragePct ?? 0}%` }}
                          />
                        </div>
                      </div>

                      <dl className="mt-7 divide-y divide-[var(--outline-soft)] border-y border-[var(--outline-soft)]">
                        <div className="flex items-center justify-between gap-4 py-3">
                          <dt className="text-xs text-[var(--ink-secondary)]">Grade path</dt>
                          <dd className="font-mono text-sm font-semibold text-[var(--ink-primary)]">
                            {topRec.latestGrade ?? '—'} <span className="text-[var(--ink-muted)]">→</span> {topRec.targetGrade}
                          </dd>
                        </div>
                        <div className="flex items-center justify-between gap-4 py-3">
                          <dt className="text-xs text-[var(--ink-secondary)]">Weekly plan</dt>
                          <dd className="font-mono text-sm font-semibold text-[var(--ink-primary)]">{topRec.sessionsPerWeek} session{topRec.sessionsPerWeek === 1 ? '' : 's'}</dd>
                        </div>
                      </dl>

                      {topRec.topicsTotal > 0 && (
                        <div className="mt-5 grid grid-cols-3 gap-2 text-center">
                          {[
                            ['Solid', topRec.solid],
                            ['Shaky', topRec.shaky],
                            ['Not started', topRec.notStarted],
                          ].map(([label, value]) => (
                            <div key={String(label)}>
                              <p className="font-mono text-sm font-semibold text-[var(--ink-primary)]">{value}</p>
                              <p className="mt-1 text-[9px] font-semibold uppercase tracking-[0.1em] text-[var(--ink-muted)]">{label}</p>
                            </div>
                          ))}
                        </div>
                      )}
                    </aside>
                  </div>
                </div>
              </section>
            );
          })()}

          {/* ── One ranked subject register instead of repeated cards ── */}
          {rankedRecs.length > 0 && (
            <section>
              <SectionHeader overline="Across your subjects" title="Ranked next priorities" rule ruleColor={INK_MUTE} />
              <EditorialCard padded={false} className="mt-3 overflow-hidden">
                <div className="hidden grid-cols-[minmax(150px,0.85fr)_130px_110px_100px_minmax(240px,1.35fr)] gap-4 border-b border-[var(--outline-soft)] bg-[var(--surface-soft)] px-5 py-3 md:grid">
                  {['Subject', 'Coverage', 'Grade path', 'Weekly plan', 'Next move'].map(label => (
                    <span key={label} className="text-[9px] font-bold uppercase tracking-[0.16em] text-[var(--ink-muted)]">{label}</span>
                  ))}
                </div>
                <div className="divide-y divide-[var(--outline-soft)]">
                  {rankedRecs.map((rec, index) => {
                  const hex = subjectHex(rec.subject);
                  return (
                    <div key={rec.subject} className="px-4 py-4 sm:px-5">
                      <div className="grid gap-4 md:grid-cols-[minmax(150px,0.85fr)_130px_110px_100px_minmax(240px,1.35fr)] md:items-center">
                        <div className="min-w-0">
                          <div className="flex items-center gap-2">
                            <span className="font-mono text-[10px] text-[var(--ink-muted)]">{String(index + 2).padStart(2, '0')}</span>
                            <span className="h-2.5 w-2.5 shrink-0 rounded-full"
                              style={{ background: hex, border: `1px solid color-mix(in srgb, var(--ink-primary) 20%, transparent)` }} />
                            <h4 className="truncate font-serif text-[15px] font-semibold text-[var(--ink-primary)]">{rec.subject}</h4>
                          </div>
                          <p className="mt-1.5 line-clamp-2 text-[11px] leading-relaxed text-[var(--ink-muted)] md:hidden">{rec.concerns.join(' · ')}</p>
                        </div>

                        <div>
                          <div className="flex items-center justify-between gap-2">
                            <span className="text-[10px] font-semibold uppercase tracking-[0.12em] text-[var(--ink-muted)] md:hidden">Coverage</span>
                            <span className="font-mono text-xs font-semibold text-[var(--ink-primary)]">{rec.coveragePct === null ? 'Not mapped' : `${rec.coveragePct}%`}</span>
                          </div>
                          <div className="mt-2 h-1.5 overflow-hidden bg-[var(--outline-soft)]">
                            <div className="h-full bg-[var(--ink-primary)]" style={{ width: `${rec.coveragePct ?? 0}%` }} />
                          </div>
                        </div>

                        <div className="flex items-center justify-between gap-3 md:block">
                          <span className="text-[10px] font-semibold uppercase tracking-[0.12em] text-[var(--ink-muted)] md:hidden">Grade path</span>
                          <span className="font-mono text-xs font-semibold text-[var(--ink-primary)]">{rec.latestGrade ?? '—'} → {rec.targetGrade}</span>
                        </div>

                        <div className="flex items-center justify-between gap-3 md:block">
                          <span className="text-[10px] font-semibold uppercase tracking-[0.12em] text-[var(--ink-muted)] md:hidden">Weekly plan</span>
                          <span className="font-mono text-xs font-semibold text-[var(--ink-primary)]">{rec.sessionsPerWeek} session{rec.sessionsPerWeek === 1 ? '' : 's'}</span>
                        </div>

                        <div>
                          <p className="text-xs leading-relaxed text-[var(--ink-secondary)]">
                            {rec.action}
                          </p>
                        </div>
                      </div>
                      <ExaminerInsightsBlock
                        rec={rec}
                        isOpen={expandedGuidance === rec.subject}
                        onToggle={() => setExpandedGuidance(expandedGuidance === rec.subject ? null : rec.subject)}
                        accent={hex}
                        compact
                      />
                    </div>
                  );
                  })}
                </div>
              </EditorialCard>
            </section>
          )}

          {/* ── Momentum / closest-to-target ── */}
          {bestSubject && (
            <section>
              <SectionHeader overline="Momentum" title="Hold the line" rule ruleColor={STATUS_SOLID} />
              <div className="mt-3">
                <EditorialCard tone="soft" style={{ background: STATUS_SOLID_TINT }}>
                  <div className="flex items-center gap-3">
                    <SketchedLeaf size={28} color={STATUS_SOLID_DEEP} />
                    <div className="flex-1">
                      <p className="font-serif text-[15px] font-bold" style={{ color: STATUS_SOLID_DEEP }}>
                        {bestSubject.surplus >= 0
                          ? `Strongest: ${bestSubject.name} — above target`
                          : `Closest to target: ${bestSubject.name}`}
                      </p>
                      <p className="font-sans text-[12px] mt-0.5" style={{ color: INK_SOFT }}>
                        {bestSubject.surplus >= 0
                          ? 'Protect this lead — keep doing what’s working.'
                          : 'A small push here will tip you over your target.'}
                      </p>
                    </div>
                    <CheckCircle size={18} style={{ color: STATUS_SOLID_DEEP }} />
                  </div>
                </EditorialCard>
              </div>
            </section>
          )}
        </>
      ) : (
        <EditorialCard tone="soft">
          <div className="text-center py-8 space-y-3">
            <Target size={36} style={{ color: ACCENT, opacity: 0.7 }} className="mx-auto" />
            <p className="font-serif text-[16px] font-bold" style={{ color: INK }}>No strategic data yet</p>
            <div className="font-sans text-[12px] space-y-1" style={{ color: INK_MUTE }}>
              <p>Add topics in the <strong>Subjects</strong> tab to track what you've studied.</p>
              <p>Log test results in the <strong>Trajectory</strong> tab to track your grades.</p>
            </div>
          </div>
        </EditorialCard>
      )}
    </div>
  );
};

// ── Examiner Insights — quieter accordion block ────────────

const ExaminerInsightsBlock: React.FC<{
  rec: Recommendation;
  isOpen: boolean;
  onToggle: () => void;
  accent: string;
  compact?: boolean;
}> = ({ rec, isOpen, onToggle, accent, compact }) => {
  if (!rec.guidance) return null;
  return (
    <div className={compact ? 'mt-2.5' : 'mt-3.5'}>
      <button
        onClick={onToggle}
        className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-full text-[11px] font-semibold transition-colors"
        style={isOpen
          ? { background: accent + '22', color: INK }
          : { background: 'transparent', color: INK_SOFT, border: `1px solid color-mix(in srgb, var(--ink-primary) 13%, transparent)` }}
      >
        <BookOpen size={12} />
        Examiner insights
        <ChevronDown size={11} className={`transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>
      <AnimatePresence>
        {isOpen && (
          <MotionDiv
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25 }}
            className="overflow-hidden"
          >
            <div className="mt-3 pt-3 space-y-3" style={{ borderTop: `1px dashed color-mix(in srgb, var(--ink-primary) 13%, transparent)` }}>
              <div>
                <Overline color={STATUS_SHAKY_DEEP}>Why students struggle here</Overline>
                <ul className="space-y-1.5 mt-1.5">
                  {rec.guidance.commonStruggles.map((s, si) => (
                    <li key={si} className="flex items-start gap-2.5 font-sans text-[13px]" style={{ color: INK_SOFT }}>
                      <span className="mt-1.5 w-1.5 h-1.5 rounded-full shrink-0" style={{ background: STATUS_SHAKY_DEEP }} />
                      {s}
                    </li>
                  ))}
                </ul>
              </div>
              <div>
                <Overline color={STATUS_SOLID_DEEP}>What to do</Overline>
                <ul className="space-y-1.5 mt-1.5">
                  {rec.guidance.actions.map((a, ai) => (
                    <li key={ai} className="flex items-start gap-2.5 font-sans text-[13px]" style={{ color: INK_SOFT }}>
                      <span className="mt-1.5 w-1.5 h-1.5 rounded-full shrink-0" style={{ background: STATUS_SOLID_DEEP }} />
                      {a}
                    </li>
                  ))}
                </ul>
              </div>
              <div className="flex items-start gap-2.5 p-3 rounded-lg"
                   style={{ background: STATUS_SHAKY_TINT, border: `1px solid ${STATUS_SHAKY}33` }}>
                <AlertTriangle size={13} style={{ color: STATUS_SHAKY_DEEP }} className="shrink-0 mt-0.5" />
                <div>
                  <p className="font-sans text-[11px] font-bold uppercase tracking-[0.18em]" style={{ color: STATUS_SHAKY_DEEP }}>Exam trap</p>
                  <p className="font-sans text-[13px] mt-0.5" style={{ color: INK_SOFT }}>{rec.guidance.examTrap}</p>
                </div>
              </div>
              <div className="flex items-start gap-2.5 p-3 rounded-lg"
                   style={{ background: STATUS_SOLID_TINT, border: `1px solid ${STATUS_SOLID}33` }}>
                <Shield size={13} style={{ color: STATUS_SOLID_DEEP }} className="shrink-0 mt-0.5" />
                <div>
                  <p className="font-sans text-[11px] font-bold uppercase tracking-[0.18em]" style={{ color: STATUS_SOLID_DEEP }}>Mindset shift</p>
                  <p className="font-sans text-[13px] mt-0.5" style={{ color: INK_SOFT }}>{rec.guidance.mindsetShift}</p>
                </div>
              </div>
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
  );
};

export default BriefingPanel;
