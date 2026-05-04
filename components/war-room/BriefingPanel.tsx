/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import {
  Activity, ChevronDown, AlertTriangle, BookOpen,
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
  PAPER, PAPER_SOFT, INK, INK_SOFT, INK_MUTE, INK_FAINT, ACCENT,
  STATUS_SOLID, STATUS_SOLID_DEEP, STATUS_SOLID_TINT,
  STATUS_SHAKY, STATUS_SHAKY_DEEP, STATUS_SHAKY_TINT,
  STATUS_GAP, STATUS_GAP_DEEP, STATUS_GAP_TINT,
} from './warRoomShared';
import {
  Overline, SectionHeader, EditorialCard, Pill,
  SketchedStar, SketchedFlag, SketchedLeaf, SunburstRule, PaperRule,
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

const BriefingPanel: React.FC<BriefingPanelProps> = ({
  subjects, topicMap, mockResults, allocations, weeksUntilExam, daysUntilExam, timetableCompletions,
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

      if (concerns.length === 0 && topics.length === 0 && results.length === 0) {
        concerns.push('no coverage data or test results logged yet');
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
          action = `${sessionsPerWeek} session${sessionsPerWeek > 1 ? 's' : ''} allocated this week.`;
        }
      }

      if (concerns.length > 0) {
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

  const hasData = (topicMap && Object.values(topicMap).some(t => t.length > 0)) || mockResults.length > 0;
  const [expandedGuidance, setExpandedGuidance] = useState<string | null>(null);

  const topRec = recommendations[0];
  const supportingRecs = recommendations.slice(1, 3);
  const otherRecs = recommendations.slice(3, 5);

  const subjectIdx = (name: string) => subjects.findIndex(s => s.subjectName === name);
  const subjectHex = (name: string, fallback = 0) => mutedSubjectHex(getDistinctSubjectHex(name, subjectIdx(name) >= 0 ? subjectIdx(name) : fallback), 0.22);

  return (
    <div className="space-y-7">
      {/* ── Today's Brief masthead ── */}
      <div className="relative">
        <div className="flex items-end justify-between gap-4">
          <div>
            <Overline color={ACCENT}>Today’s brief</Overline>
            <h2 className="font-serif font-bold mt-1.5 leading-[1.05]"
                style={{ color: INK, fontSize: 'clamp(28px, 4.5vw, 36px)' }}>
              The strategic read
            </h2>
            <div className="mt-2 flex items-center gap-2">
              <img
                src="/assets/war-room-rule.png"
                alt=""
                aria-hidden
                style={{ width: 72, height: 'auto', objectFit: 'contain', flexShrink: 0 }}
              />
              <p className="font-sans text-[12px]" style={{ color: INK_MUTE }}>
                {daysUntilExam} days · {weeksUntilExam} weeks of study left
              </p>
            </div>
          </div>
          <div className="hidden sm:block">
            <SketchedStar size={36} color={ACCENT} />
          </div>
        </div>
        <PaperRule className="mt-5" />
      </div>

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
              style={{ borderTop: `1px solid ${INK}10` }}
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
                                  style={{ width: 18, height: 18, background: bgColor, border: `1px solid ${INK}10` }}
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
                    <div className="flex h-3 rounded-full overflow-hidden" style={{ border: `1px solid ${INK}1A` }}>
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
                                  style={{ background: hex, border: `1px solid ${INK}33` }} />
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
          {/* ── Top priority hero ── */}
          {topRec && (() => {
            const hex = subjectHex(topRec.subject);
            return (
              <section>
                <SectionHeader overline="Top priority" title="Where to focus first" rule />
                <div className="mt-3">
                  <EditorialCard tone="paper">
                    <div className="flex items-start gap-4">
                      {/* Sketched motif as marker */}
                      <div className="shrink-0 mt-1">
                        <SketchedFlag size={34} />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="w-3 h-3 rounded-full shrink-0"
                                style={{ background: hex, border: `1px solid ${INK}33` }} />
                          <h3 className="font-serif text-[22px] font-bold leading-tight" style={{ color: INK }}>
                            {topRec.subject}
                          </h3>
                          <Pill bg={INK} fg={PAPER}>Highest impact</Pill>
                        </div>
                        <p className="font-sans text-[13px] mt-2.5 leading-relaxed" style={{ color: INK_SOFT }}>
                          {topRec.concerns.join(' · ')}
                        </p>
                        {topRec.action && (
                          <p className="font-serif text-[15px] mt-2 leading-relaxed" style={{ color: ACCENT, fontWeight: 600 }}>
                            {topRec.action}
                          </p>
                        )}
                        <ExaminerInsightsBlock
                          rec={topRec}
                          isOpen={expandedGuidance === topRec.subject}
                          onToggle={() => setExpandedGuidance(expandedGuidance === topRec.subject ? null : topRec.subject)}
                          accent={hex}
                        />
                      </div>
                    </div>
                  </EditorialCard>
                </div>
              </section>
            );
          })()}

          {/* ── Supporting priorities ── */}
          {supportingRecs.length > 0 && (
            <section>
              <SectionHeader overline="Supporting priorities" title="Worth defending" rule ruleColor={INK_MUTE} />
              <div className="mt-3 grid sm:grid-cols-2 gap-3">
                {supportingRecs.map(rec => {
                  const hex = subjectHex(rec.subject);
                  return (
                    <EditorialCard key={rec.subject} tone="soft">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="w-2.5 h-2.5 rounded-full shrink-0"
                              style={{ background: hex, border: `1px solid ${INK}33` }} />
                        <h4 className="font-serif text-[16px] font-bold" style={{ color: INK }}>{rec.subject}</h4>
                      </div>
                      <p className="font-sans text-[12px] mt-2" style={{ color: INK_MUTE }}>
                        {rec.concerns.join(' · ')}
                      </p>
                      {rec.action && (
                        <p className="font-sans text-[13px] mt-1.5" style={{ color: INK_SOFT }}>
                          {rec.action}
                        </p>
                      )}
                      <ExaminerInsightsBlock
                        rec={rec}
                        isOpen={expandedGuidance === rec.subject}
                        onToggle={() => setExpandedGuidance(expandedGuidance === rec.subject ? null : rec.subject)}
                        accent={hex}
                        compact
                      />
                    </EditorialCard>
                  );
                })}
              </div>
            </section>
          )}

          {/* ── Other priorities ── */}
          {otherRecs.length > 0 && (
            <section>
              <SectionHeader overline="On the radar" title="Other subjects to watch" rule ruleColor={INK_MUTE} />
              <div className="mt-3 space-y-2">
                {otherRecs.map(rec => {
                  const hex = subjectHex(rec.subject);
                  return (
                    <div
                      key={rec.subject}
                      className="px-4 py-3"
                      style={{
                        background: '#FFFFFF',
                        border: `1px solid ${INK}14`,
                        borderRadius: 12,
                        boxShadow: '0 1px 0 rgba(31,27,23,0.03)',
                      }}
                    >
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="w-2.5 h-2.5 rounded-full shrink-0"
                              style={{ background: hex, border: `1px solid ${INK}33` }} />
                        <span className="font-serif text-[14px] font-semibold" style={{ color: INK }}>{rec.subject}</span>
                        <span className="font-sans text-[11px]" style={{ color: INK_MUTE }}>{rec.concerns.join(' · ')}</span>
                      </div>
                      {rec.action && (
                        <p className="font-sans text-[12px] mt-1.5 ml-4" style={{ color: INK_SOFT }}>{rec.action}</p>
                      )}
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
              <p>Add topics in the <strong>Coverage</strong> tab to track what you've studied.</p>
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
          : { background: 'transparent', color: INK_SOFT, border: `1px solid ${INK}22` }}
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
            <div className="mt-3 pt-3 space-y-3" style={{ borderTop: `1px dashed ${INK}22` }}>
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
