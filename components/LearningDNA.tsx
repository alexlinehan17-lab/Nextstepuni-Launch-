/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  Brain, TrendingUp, Target, BookOpen, RotateCcw, Lightbulb,
  Sparkles, BarChart3, CheckCircle, AlertTriangle, ArrowUp, ArrowDown,
} from 'lucide-react';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { type DebriefEntry, STRATEGY_OPTIONS } from './StudyDebrief';

const MotionDiv = motion.div as any;

// ─── Types ───────────────────────────────────────────────────────────────────

interface LearningDNAProps {
  uid: string;
}

interface SubjectInsight {
  subject: string;
  totalSessions: number;
  totalMinutes: number;
  avgConfidenceBefore: number;
  avgConfidenceAfter: number;
  confidenceGain: number;
  topStrategy: string;
  topStrategyCount: number;
  bestStrategy: string | null;       // strategy with highest avg confidence gain
  bestStrategyAvgGain: number;
  hardestTopics: string[];
}

interface StrategyInsight {
  strategy: string;
  label: string;
  count: number;
  avgConfidenceGain: number;
}

// ─── Subject Colors ──────────────────────────────────────────────────────────

const SUBJECT_DOT: Record<string, string> = {
  'English': 'bg-blue-500', 'Irish': 'bg-emerald-500', 'Mathematics': 'bg-indigo-500',
  'French': 'bg-sky-500', 'German': 'bg-yellow-500', 'Spanish': 'bg-orange-500',
  'Physics': 'bg-cyan-500', 'Chemistry': 'bg-teal-500', 'Biology': 'bg-lime-500',
  'Applied Maths': 'bg-violet-500', 'Computer Science': 'bg-fuchsia-500', 'Ag Science': 'bg-green-500',
  'Accounting': 'bg-amber-500', 'Business': 'bg-amber-600', 'Economics': 'bg-yellow-600',
  'History': 'bg-purple-500', 'Geography': 'bg-emerald-600', 'Home Economics': 'bg-orange-400',
  'Art': 'bg-rose-400', 'Music': 'bg-pink-400',
};

function getDot(name: string) { return SUBJECT_DOT[name] || 'bg-zinc-500'; }

function getStrategyLabel(id: string): string {
  return STRATEGY_OPTIONS.find(o => o.id === id)?.label ?? id;
}

// ─── Component ───────────────────────────────────────────────────────────────

const LearningDNA: React.FC<LearningDNAProps> = ({ uid }) => {
  const [debriefs, setDebriefs] = useState<DebriefEntry[]>([]);
  const [loaded, setLoaded] = useState(false);

  // Load debriefs from Firestore
  useEffect(() => {
    (async () => {
      try {
        const snap = await getDoc(doc(db, 'progress', uid));
        const data = snap.data()?.studyDebriefs as DebriefEntry[] | undefined;
        if (data) setDebriefs(data);
      } catch (e) {
        console.error('Failed to load debriefs:', e);
      }
      setLoaded(true);
    })();
  }, [uid]);

  // Compute per-subject insights
  const subjectInsights = useMemo((): SubjectInsight[] => {
    const bySubject = new Map<string, DebriefEntry[]>();
    debriefs.forEach(d => {
      const arr = bySubject.get(d.subject) || [];
      arr.push(d);
      bySubject.set(d.subject, arr);
    });

    return Array.from(bySubject.entries()).map(([subject, entries]) => {
      const totalMinutes = entries.reduce((s, e) => s + e.durationMinutes, 0);
      const avgBefore = entries.reduce((s, e) => s + e.confidenceBefore, 0) / entries.length;
      const avgAfter = entries.reduce((s, e) => s + e.confidenceAfter, 0) / entries.length;

      // Strategy frequency
      const strategyCounts = new Map<string, number>();
      entries.forEach(e => {
        strategyCounts.set(e.strategy, (strategyCounts.get(e.strategy) || 0) + 1);
      });
      const topStrategy = [...strategyCounts.entries()].sort((a, b) => b[1] - a[1])[0];

      // Best strategy by confidence gain
      const strategyGains = new Map<string, number[]>();
      entries.forEach(e => {
        const arr = strategyGains.get(e.strategy) || [];
        arr.push(e.confidenceAfter - e.confidenceBefore);
        strategyGains.set(e.strategy, arr);
      });
      let bestStrategy: string | null = null;
      let bestStrategyAvgGain = 0;
      strategyGains.forEach((gains, strat) => {
        if (gains.length >= 2) {
          const avg = gains.reduce((s, g) => s + g, 0) / gains.length;
          if (avg > bestStrategyAvgGain) {
            bestStrategyAvgGain = avg;
            bestStrategy = strat;
          }
        }
      });

      // Hardest topics
      const topicCounts = new Map<string, number>();
      entries.forEach(e => {
        if (e.hardestTopic && e.hardestTopic !== 'Not specified') {
          topicCounts.set(e.hardestTopic, (topicCounts.get(e.hardestTopic) || 0) + 1);
        }
      });
      const hardestTopics = [...topicCounts.entries()]
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3)
        .map(([t]) => t);

      return {
        subject,
        totalSessions: entries.length,
        totalMinutes,
        avgConfidenceBefore: Math.round(avgBefore * 10) / 10,
        avgConfidenceAfter: Math.round(avgAfter * 10) / 10,
        confidenceGain: Math.round((avgAfter - avgBefore) * 10) / 10,
        topStrategy: topStrategy?.[0] ?? 'other',
        topStrategyCount: topStrategy?.[1] ?? 0,
        bestStrategy,
        bestStrategyAvgGain: Math.round(bestStrategyAvgGain * 10) / 10,
        hardestTopics,
      };
    }).sort((a, b) => b.totalSessions - a.totalSessions);
  }, [debriefs]);

  // Global strategy insights
  const strategyInsights = useMemo((): StrategyInsight[] => {
    const strategyData = new Map<string, { count: number; gains: number[] }>();
    debriefs.forEach(d => {
      const data = strategyData.get(d.strategy) || { count: 0, gains: [] };
      data.count++;
      data.gains.push(d.confidenceAfter - d.confidenceBefore);
      strategyData.set(d.strategy, data);
    });

    return [...strategyData.entries()]
      .map(([strategy, data]) => ({
        strategy,
        label: getStrategyLabel(strategy),
        count: data.count,
        avgConfidenceGain: Math.round((data.gains.reduce((s, g) => s + g, 0) / data.gains.length) * 10) / 10,
      }))
      .sort((a, b) => b.avgConfidenceGain - a.avgConfidenceGain);
  }, [debriefs]);

  // Top insight message
  const topInsight = useMemo((): string | null => {
    if (debriefs.length < 3) return null;

    // Find strategy with highest avg gain across all subjects
    const best = strategyInsights.find(s => s.count >= 2 && s.avgConfidenceGain > 0);
    const worst = [...strategyInsights].sort((a, b) => a.avgConfidenceGain - b.avgConfidenceGain).find(s => s.count >= 2);

    if (best && worst && best.strategy !== worst.strategy && worst.avgConfidenceGain < best.avgConfidenceGain) {
      return `Your data shows ${best.label.toLowerCase()} works ${Math.round((best.avgConfidenceGain / Math.max(0.1, worst.avgConfidenceGain)) * 10) / 10}x better for your confidence than ${worst.label.toLowerCase()}. Consider swapping next session.`;
    }

    if (best) {
      return `${best.label} gives you the biggest confidence boost (avg +${best.avgConfidenceGain} per session). Keep using it.`;
    }

    return null;
  }, [debriefs, strategyInsights]);

  if (!loaded) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-6 h-6 border-2 border-teal-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white">Learning DNA</h2>
        <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1">
          Patterns from your study debriefs. The more sessions you log, the sharper these insights become.
        </p>
      </div>

      {debriefs.length === 0 ? (
        <div className="text-center py-12">
          <Brain size={40} className="text-zinc-300 dark:text-zinc-600 mx-auto mb-4" />
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-1">No debriefs yet</p>
          <p className="text-xs text-zinc-400 dark:text-zinc-500 max-w-xs mx-auto">
            Complete a study session and fill out the quick debrief to start building your learning profile.
          </p>
        </div>
      ) : (
        <>
          {/* Summary stats */}
          <div className="grid grid-cols-3 gap-3">
            <div className="rounded-xl p-4 border bg-teal-50 dark:bg-teal-900/15 border-teal-200 dark:border-teal-800/40">
              <p className="text-[10px] font-bold uppercase tracking-widest text-teal-500 dark:text-teal-400 mb-1">Sessions</p>
              <span className="font-serif text-2xl font-bold text-teal-700 dark:text-teal-300">{debriefs.length}</span>
            </div>
            <div className="rounded-xl p-4 border bg-zinc-50 dark:bg-zinc-800/40 border-zinc-200 dark:border-zinc-700/40">
              <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-1">Subjects</p>
              <span className="font-serif text-2xl font-bold text-zinc-700 dark:text-zinc-300">{subjectInsights.length}</span>
            </div>
            <div className="rounded-xl p-4 border bg-emerald-50 dark:bg-emerald-900/15 border-emerald-200 dark:border-emerald-800/40">
              <p className="text-[10px] font-bold uppercase tracking-widest text-emerald-500 dark:text-emerald-400 mb-1">Avg Gain</p>
              <span className="font-serif text-2xl font-bold text-emerald-700 dark:text-emerald-300">
                {debriefs.length > 0 ? (
                  '+' + (Math.round((debriefs.reduce((s, d) => s + d.confidenceAfter - d.confidenceBefore, 0) / debriefs.length) * 10) / 10)
                ) : '—'}
              </span>
            </div>
          </div>

          {/* Top insight */}
          {topInsight && (
            <div className="bg-teal-50 dark:bg-teal-900/15 border border-teal-200 dark:border-teal-800/30 rounded-xl p-4">
              <div className="flex items-start gap-3">
                <Lightbulb size={16} className="text-teal-500 shrink-0 mt-0.5" />
                <div>
                  <p className="text-[10px] font-bold uppercase tracking-widest text-teal-500 mb-1">Your Data Says</p>
                  <p className="text-xs text-teal-700 dark:text-teal-300 leading-relaxed">{topInsight}</p>
                </div>
              </div>
            </div>
          )}

          {/* Strategy effectiveness */}
          {strategyInsights.length > 0 && (
            <div>
              <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
                Strategy Effectiveness
              </p>
              <div className="space-y-2">
                {strategyInsights.map((si, idx) => (
                  <MotionDiv
                    key={si.strategy}
                    initial={{ opacity: 0, x: -8 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.05 }}
                    className="flex items-center gap-3 p-3 rounded-xl bg-white/60 dark:bg-white/5 border border-zinc-200/60 dark:border-white/10"
                  >
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-semibold text-zinc-800 dark:text-zinc-200 truncate">{si.label}</p>
                      <p className="text-[11px] text-zinc-400 dark:text-zinc-500">{si.count} session{si.count !== 1 ? 's' : ''}</p>
                    </div>
                    <div className="flex items-center gap-1.5">
                      {si.avgConfidenceGain > 0 ? (
                        <ArrowUp size={12} className="text-emerald-500" />
                      ) : si.avgConfidenceGain < 0 ? (
                        <ArrowDown size={12} className="text-rose-500" />
                      ) : null}
                      <span className={`text-sm font-bold px-2 py-0.5 rounded-full ${
                        si.avgConfidenceGain > 0
                          ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400'
                          : si.avgConfidenceGain < 0
                            ? 'bg-rose-100 dark:bg-rose-900/30 text-rose-600 dark:text-rose-400'
                            : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-500'
                      }`}>
                        {si.avgConfidenceGain > 0 ? '+' : ''}{si.avgConfidenceGain}
                      </span>
                    </div>
                  </MotionDiv>
                ))}
              </div>
            </div>
          )}

          {/* Per-subject breakdown */}
          {subjectInsights.length > 0 && (
            <div>
              <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
                Subject Breakdown
              </p>
              <div className="space-y-3">
                {subjectInsights.map((si, idx) => (
                  <MotionDiv
                    key={si.subject}
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: idx * 0.05 }}
                    className="p-4 rounded-xl bg-white/60 dark:bg-white/5 border border-zinc-200/60 dark:border-white/10 space-y-3"
                  >
                    <div className="flex items-center gap-3">
                      <span className={`w-3 h-3 rounded-full ${getDot(si.subject)}`} />
                      <span className="text-sm font-bold text-zinc-800 dark:text-zinc-200 flex-1">{si.subject}</span>
                      <span className="text-xs text-zinc-400">{si.totalSessions} sessions &middot; {si.totalMinutes} min</span>
                    </div>

                    {/* Confidence trend */}
                    <div className="flex items-center gap-4">
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] text-zinc-400">Confidence:</span>
                        <span className="text-xs font-bold text-zinc-500">{si.avgConfidenceBefore}</span>
                        <ArrowRight size={10} className="text-zinc-400" />
                        <span className={`text-xs font-bold ${si.confidenceGain >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}`}>
                          {si.avgConfidenceAfter}
                        </span>
                        <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded-full ${
                          si.confidenceGain > 0
                            ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400'
                            : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-500'
                        }`}>
                          {si.confidenceGain > 0 ? '+' : ''}{si.confidenceGain}
                        </span>
                      </div>
                    </div>

                    {/* Best strategy for this subject */}
                    {si.bestStrategy && (
                      <div className="flex items-center gap-2">
                        <CheckCircle size={12} className="text-emerald-500" />
                        <span className="text-[11px] text-zinc-600 dark:text-zinc-400">
                          Best strategy: <span className="font-semibold">{getStrategyLabel(si.bestStrategy)}</span> (avg +{si.bestStrategyAvgGain})
                        </span>
                      </div>
                    )}

                    {/* Hardest topics */}
                    {si.hardestTopics.length > 0 && (
                      <div className="flex items-start gap-2">
                        <AlertTriangle size={12} className="text-amber-500 shrink-0 mt-0.5" />
                        <div className="flex flex-wrap gap-1.5">
                          {si.hardestTopics.map(topic => (
                            <span key={topic} className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-amber-100 dark:bg-amber-900/20 text-amber-700 dark:text-amber-400">
                              {topic}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </MotionDiv>
                ))}
              </div>
            </div>
          )}

          {/* Encouragement */}
          {debriefs.length < 5 && (
            <div className="bg-zinc-100 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl p-4">
              <p className="text-xs text-zinc-500 dark:text-zinc-400 text-center">
                {5 - debriefs.length} more debrief{5 - debriefs.length !== 1 ? 's' : ''} until your first personalised strategy recommendation.
              </p>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default LearningDNA;
