/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useMemo } from 'react';
import { type StreakData } from './useStreak';
import { useProgress } from '../contexts/ProgressContext';
import { type StrategyMasteryMap } from '../types';
import { type StudySessionRecord, STRATEGY_REGISTRY } from '../studySessionData';
import { type DebriefEntry } from '../components/StudyDebrief';

// ── Types ──────────────────────────────────────────────────

export interface Insight {
  id: string;
  icon: string;
  iconColor: string;
  title: string;
  description: string;
  category: 'momentum' | 'pattern' | 'strategy' | 'streak';
}

// ── Helpers ────────────────────────────────────────────────

function getMonthKey(date: Date): string {
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
}

function getTimeOfDay(hour: number): string {
  if (hour < 12) return 'morning';
  if (hour < 17) return 'afternoon';
  return 'evening';
}

function getDayLabel(day: number): string {
  return ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][day];
}

function isWeekday(day: number): boolean {
  return day >= 1 && day <= 5;
}

function strategyName(moduleId: string): string {
  const entry = STRATEGY_REGISTRY.find(s => s.moduleId === moduleId);
  return entry?.strategyName ?? moduleId;
}

// ── Insight Generators ─────────────────────────────────────

function monthlyVolumeChange(sessions: StudySessionRecord[]): Insight | null {
  const now = new Date();
  const thisMonth = getMonthKey(now);
  const lastMonth = getMonthKey(new Date(now.getFullYear(), now.getMonth() - 1, 1));

  let thisMinutes = 0;
  let lastMinutes = 0;

  for (const s of sessions) {
    const key = s.date.slice(0, 7);
    const mins = s.actualSeconds / 60;
    if (key === thisMonth) thisMinutes += mins;
    else if (key === lastMonth) lastMinutes += mins;
  }

  if (lastMinutes < 5 || thisMinutes < 5) return null;

  const pct = Math.round(((thisMinutes - lastMinutes) / lastMinutes) * 100);
  if (pct === 0) return null;

  const direction = pct > 0 ? 'more' : 'less';
  const absPct = Math.abs(pct);

  return {
    id: 'monthly-volume',
    icon: 'TrendingUp',
    iconColor: pct > 0 ? 'text-emerald-500' : 'text-amber-500',
    title: `${absPct}% ${direction} study time`,
    description: `You've studied ${Math.round(thisMinutes / 60 * 10) / 10}h this month vs ${Math.round(lastMinutes / 60 * 10) / 10}h last month.`,
    category: 'momentum',
  };
}

function bestStudyTime(sessions: StudySessionRecord[]): Insight | null {
  if (sessions.length < 5) return null;

  const counts: Record<string, number> = {};

  for (const s of sessions) {
    const d = new Date(s.startedAt);
    const dayType = isWeekday(d.getDay()) ? 'weekday' : 'weekend';
    const tod = getTimeOfDay(d.getHours());
    const key = `${dayType}-${tod}`;
    counts[key] = (counts[key] || 0) + 1;
  }

  let bestKey = '';
  let bestCount = 0;
  for (const [key, count] of Object.entries(counts)) {
    if (count > bestCount) {
      bestKey = key;
      bestCount = count;
    }
  }

  if (!bestKey || bestCount < 3) return null;

  const [dayType, tod] = bestKey.split('-');
  return {
    id: 'best-time',
    icon: 'Clock',
    iconColor: 'text-blue-500',
    title: `Best sessions: ${dayType} ${tod}s`,
    description: `Your most productive sessions happen on ${dayType} ${tod}s (${bestCount} sessions).`,
    category: 'pattern',
  };
}

function dormantStrategyNudge(
  sessions: StudySessionRecord[],
  mastery: StrategyMasteryMap,
): Insight | null {
  const now = Date.now();
  const twoWeeksMs = 14 * 24 * 60 * 60 * 1000;

  const practicedStrategies = Object.entries(mastery).filter(
    ([, rec]) => rec.tier !== 'none' && rec.tier !== 'learned'
  );

  if (practicedStrategies.length === 0) return null;

  for (const [moduleId] of practicedStrategies) {
    const lastUsed = sessions
      .filter(s => s.strategiesShown?.includes(moduleId))
      .reduce((latest, s) => Math.max(latest, s.startedAt), 0);

    if (lastUsed > 0 && now - lastUsed > twoWeeksMs) {
      const name = strategyName(moduleId);
      const daysSince = Math.floor((now - lastUsed) / (24 * 60 * 60 * 1000));
      return {
        id: `dormant-${moduleId}`,
        icon: 'RefreshCw',
        iconColor: 'text-violet-500',
        title: `${name} is gathering dust`,
        description: `You haven't used ${name} in ${daysSince} days — bring it back into your sessions.`,
        category: 'strategy',
      };
    }
  }

  return null;
}

function streakMilestone(streak: StreakData): Insight | null {
  if (streak.currentStreak <= 0) return null;

  const milestones = [3, 7, 14, 21, 30, 50, 100];
  const next = milestones.find(m => m > streak.currentStreak);

  if (!next) return null;

  const remaining = next - streak.currentStreak;
  if (remaining > 3) return null;

  if (remaining === 1) {
    return {
      id: 'streak-milestone',
      icon: 'Flame',
      iconColor: 'text-orange-500',
      title: `${next}-day streak incoming`,
      description: `One more session today and you hit a ${next}-day streak!`,
      category: 'streak',
    };
  }

  return {
    id: 'streak-milestone',
    icon: 'Flame',
    iconColor: 'text-orange-500',
    title: `${remaining} days to ${next}-day streak`,
    description: `You're on a ${streak.currentStreak}-day streak — keep it going!`,
    category: 'streak',
  };
}

function subjectBalance(sessions: StudySessionRecord[]): Insight | null {
  if (sessions.length < 5) return null;

  const counts: Record<string, number> = {};
  for (const s of sessions) {
    counts[s.subject] = (counts[s.subject] || 0) + 1;
  }

  const total = sessions.length;
  const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]);
  if (sorted.length < 2) return null;

  const [topSubject, topCount] = sorted[0];
  const pct = Math.round((topCount / total) * 100);

  if (pct < 60) return null;

  const second = sorted[1][0];
  return {
    id: 'subject-balance',
    icon: 'BarChart3',
    iconColor: 'text-amber-500',
    title: `${pct}% of sessions are ${topSubject}`,
    description: `Consider mixing in ${second} to balance your study.`,
    category: 'pattern',
  };
}

function consistencyTrend(sessions: StudySessionRecord[]): Insight | null {
  if (sessions.length < 5) return null;

  const now = new Date();
  const dayMs = 24 * 60 * 60 * 1000;
  const startOfWeek = new Date(now);
  startOfWeek.setDate(now.getDate() - now.getDay());
  startOfWeek.setHours(0, 0, 0, 0);
  const startOfWeekMs = startOfWeek.getTime();

  let thisWeek = 0;
  const weeklyBuckets: Record<number, number> = {};

  for (const s of sessions) {
    const ts = new Date(s.date + 'T00:00:00').getTime();
    if (ts >= startOfWeekMs) {
      thisWeek++;
    } else {
      const weeksAgo = Math.ceil((startOfWeekMs - ts) / (7 * dayMs));
      if (weeksAgo >= 1 && weeksAgo <= 4) {
        weeklyBuckets[weeksAgo] = (weeklyBuckets[weeksAgo] || 0) + 1;
      }
    }
  }

  const pastWeeks = Object.values(weeklyBuckets);
  if (pastWeeks.length === 0) return null;

  const avgPast = pastWeeks.reduce((a, b) => a + b, 0) / pastWeeks.length;
  if (avgPast === 0) return null;

  const pct = Math.round(((thisWeek - avgPast) / avgPast) * 100);
  if (pct <= 10) return null;

  return {
    id: 'consistency',
    icon: 'TrendingUp',
    iconColor: 'text-emerald-500',
    title: 'More consistent this week',
    description: `You have ${thisWeek} sessions this week vs an average of ${Math.round(avgPast * 10) / 10} over the last 4 weeks.`,
    category: 'momentum',
  };
}

// ── New Deep Insight Generators ────────────────────────────

function strategyEffectiveness(sessions: StudySessionRecord[]): Insight | null {
  // Compare avg session duration when a strategy was marked "Done" vs overall avg
  if (sessions.length < 8) return null;

  const overallAvg = sessions.reduce((sum, s) => sum + s.actualSeconds, 0) / sessions.length;
  if (overallAvg < 60) return null;

  let bestStrategy = '';
  let bestDiff = 0;
  let bestAvg = 0;

  // Group sessions by which strategies were completed
  const strategySessionDurations: Record<string, number[]> = {};
  for (const s of sessions) {
    if (!s.strategiesShown || s.strategiesShown.length === 0) continue;
    for (const moduleId of s.strategiesShown) {
      if (!strategySessionDurations[moduleId]) strategySessionDurations[moduleId] = [];
      strategySessionDurations[moduleId].push(s.actualSeconds);
    }
  }

  for (const [moduleId, durations] of Object.entries(strategySessionDurations)) {
    if (durations.length < 3) continue;
    const avg = durations.reduce((a, b) => a + b, 0) / durations.length;
    const diff = avg - overallAvg;
    if (diff > bestDiff) {
      bestDiff = diff;
      bestStrategy = moduleId;
      bestAvg = avg;
    }
  }

  if (!bestStrategy || bestDiff < 60) return null; // need at least 1 min difference

  const pct = Math.round((bestDiff / overallAvg) * 100);
  const name = strategyName(bestStrategy);

  return {
    id: 'strategy-effectiveness',
    icon: 'Zap',
    iconColor: 'text-purple-500',
    title: `${pct}% longer sessions with ${name}`,
    description: `You study ${Math.round(bestAvg / 60)} min on average when using ${name} vs ${Math.round(overallAvg / 60)} min overall.`,
    category: 'strategy',
  };
}

function sessionLengthTrend(sessions: StudySessionRecord[]): Insight | null {
  // Compare average session length: last 2 weeks vs previous 2 weeks
  if (sessions.length < 6) return null;

  const now = Date.now();
  const twoWeeksMs = 14 * 24 * 60 * 60 * 1000;

  const recent: number[] = [];
  const older: number[] = [];

  for (const s of sessions) {
    const age = now - s.startedAt;
    if (age <= twoWeeksMs) {
      recent.push(s.actualSeconds);
    } else if (age <= twoWeeksMs * 2) {
      older.push(s.actualSeconds);
    }
  }

  if (recent.length < 3 || older.length < 3) return null;

  const recentAvg = recent.reduce((a, b) => a + b, 0) / recent.length;
  const olderAvg = older.reduce((a, b) => a + b, 0) / older.length;

  if (olderAvg < 60) return null;

  const pct = Math.round(((recentAvg - olderAvg) / olderAvg) * 100);
  if (Math.abs(pct) < 10) return null;

  if (pct > 0) {
    return {
      id: 'session-length-trend',
      icon: 'TrendingUp',
      iconColor: 'text-emerald-500',
      title: `Sessions are ${pct}% longer`,
      description: `Your recent sessions average ${Math.round(recentAvg / 60)} min vs ${Math.round(olderAvg / 60)} min two weeks ago. Your stamina is building.`,
      category: 'momentum',
    };
  }

  return {
    id: 'session-length-trend',
    icon: 'TrendingUp',
    iconColor: 'text-amber-500',
    title: `Sessions are ${Math.abs(pct)}% shorter`,
    description: `Your recent sessions average ${Math.round(recentAvg / 60)} min vs ${Math.round(olderAvg / 60)} min two weeks ago. Try pushing for a few more minutes.`,
    category: 'momentum',
  };
}

function reflectionImpact(sessions: StudySessionRecord[]): Insight | null {
  // Compare points earned in sessions with reflections vs without
  const withReflection = sessions.filter(s => s.hadReflection);
  const withoutReflection = sessions.filter(s => !s.hadReflection);

  if (withReflection.length < 3 || withoutReflection.length < 3) return null;

  const avgWith = withReflection.reduce((sum, s) => sum + s.pointsEarned, 0) / withReflection.length;
  const avgWithout = withoutReflection.reduce((sum, s) => sum + s.pointsEarned, 0) / withoutReflection.length;

  if (avgWithout < 1) return null;

  const pct = Math.round(((avgWith - avgWithout) / avgWithout) * 100);
  if (pct < 15) return null;

  return {
    id: 'reflection-impact',
    icon: 'Sparkles',
    iconColor: 'text-teal-500',
    title: `Reflections boost points by ${pct}%`,
    description: `Sessions with reflections earn ${Math.round(avgWith)} pts vs ${Math.round(avgWithout)} pts without. The few extra minutes of reflection pay off.`,
    category: 'pattern',
  };
}

function subjectGap(sessions: StudySessionRecord[]): Insight | null {
  // Find subjects that haven't been studied in 7+ days
  if (sessions.length < 5) return null;

  const now = Date.now();
  const subjectLastStudied: Record<string, number> = {};

  for (const s of sessions) {
    if (!subjectLastStudied[s.subject] || s.startedAt > subjectLastStudied[s.subject]) {
      subjectLastStudied[s.subject] = s.startedAt;
    }
  }

  // Only consider subjects with 3+ sessions (not one-offs)
  const subjectCounts: Record<string, number> = {};
  for (const s of sessions) {
    subjectCounts[s.subject] = (subjectCounts[s.subject] || 0) + 1;
  }

  let longestGapSubject = '';
  let longestGapDays = 0;

  for (const [subject, lastTs] of Object.entries(subjectLastStudied)) {
    if ((subjectCounts[subject] || 0) < 3) continue;
    const daysSince = Math.floor((now - lastTs) / (24 * 60 * 60 * 1000));
    if (daysSince >= 7 && daysSince > longestGapDays) {
      longestGapDays = daysSince;
      longestGapSubject = subject;
    }
  }

  if (!longestGapSubject) return null;

  return {
    id: `subject-gap-${longestGapSubject}`,
    icon: 'BookOpen',
    iconColor: 'text-rose-500',
    title: `${longestGapDays} days since ${longestGapSubject}`,
    description: `You used to study ${longestGapSubject} regularly. A quick session this week would keep it fresh.`,
    category: 'pattern',
  };
}

function peakProductivityDay(sessions: StudySessionRecord[]): Insight | null {
  // Find the day of the week with highest avg session duration
  if (sessions.length < 10) return null;

  const dayMinutes: Record<number, number[]> = {};
  for (const s of sessions) {
    const day = new Date(s.startedAt).getDay();
    if (!dayMinutes[day]) dayMinutes[day] = [];
    dayMinutes[day].push(s.actualSeconds / 60);
  }

  let bestDay = -1;
  let bestAvg = 0;

  for (const [day, mins] of Object.entries(dayMinutes)) {
    if (mins.length < 2) continue;
    const avg = mins.reduce((a, b) => a + b, 0) / mins.length;
    if (avg > bestAvg) {
      bestAvg = avg;
      bestDay = Number(day);
    }
  }

  if (bestDay < 0 || bestAvg < 5) return null;

  return {
    id: 'peak-day',
    icon: 'Calendar',
    iconColor: 'text-indigo-500',
    title: `${getDayLabel(bestDay)}s are your power day`,
    description: `You average ${Math.round(bestAvg)} min per session on ${getDayLabel(bestDay)}s — your most productive day of the week.`,
    category: 'pattern',
  };
}

function completionRate(sessions: StudySessionRecord[]): Insight | null {
  // What % of planned session time do they actually complete?
  if (sessions.length < 5) return null;

  let totalPlanned = 0;
  let totalActual = 0;

  for (const s of sessions) {
    totalPlanned += s.plannedMinutes * 60;
    totalActual += s.actualSeconds;
  }

  if (totalPlanned === 0) return null;

  const rate = Math.round((totalActual / totalPlanned) * 100);

  if (rate >= 90) {
    return {
      id: 'completion-rate',
      icon: 'Target',
      iconColor: 'text-emerald-500',
      title: `${rate}% session completion rate`,
      description: `You complete almost all of your planned study time. That consistency is rare — keep it up.`,
      category: 'momentum',
    };
  }

  if (rate < 60) {
    return {
      id: 'completion-rate',
      icon: 'Target',
      iconColor: 'text-amber-500',
      title: `${rate}% of planned time completed`,
      description: `You tend to end sessions early. Try starting with shorter planned times — finishing feels good and builds momentum.`,
      category: 'momentum',
    };
  }

  return null;
}

// ── Debrief Insight Generators ─────────────────────────────

function debriefConfidenceGain(debriefs: DebriefEntry[]): Insight | null {
  if (debriefs.length < 3) return null;

  // Find subject with highest avg confidence gain
  const gainsBySubject: Record<string, number[]> = {};
  for (const d of debriefs) {
    const gain = d.confidenceAfter - d.confidenceBefore;
    if (!gainsBySubject[d.subject]) gainsBySubject[d.subject] = [];
    gainsBySubject[d.subject].push(gain);
  }

  let bestSubject = '';
  let bestAvg = 0;
  for (const [subject, gains] of Object.entries(gainsBySubject)) {
    if (gains.length < 2) continue;
    const avg = gains.reduce((a, b) => a + b, 0) / gains.length;
    if (avg > bestAvg) { bestAvg = avg; bestSubject = subject; }
  }

  if (!bestSubject || bestAvg <= 0) return null;

  return {
    id: 'debrief-confidence',
    icon: 'TrendingUp',
    iconColor: 'text-teal-500',
    title: `Biggest confidence gains: ${bestSubject}`,
    description: `Your debriefs show an average +${(bestAvg).toFixed(1)} confidence gain per session in ${bestSubject}.`,
    category: 'momentum',
  };
}

function debriefStrategyEffectiveness(debriefs: DebriefEntry[]): Insight | null {
  if (debriefs.length < 5) return null;

  const gainsByStrategy: Record<string, number[]> = {};
  for (const d of debriefs) {
    if (!d.strategy) continue;
    if (!gainsByStrategy[d.strategy]) gainsByStrategy[d.strategy] = [];
    gainsByStrategy[d.strategy].push(d.confidenceAfter - d.confidenceBefore);
  }

  let bestStrat = '';
  let bestAvg = 0;
  for (const [strat, gains] of Object.entries(gainsByStrategy)) {
    if (gains.length < 2) continue;
    const avg = gains.reduce((a, b) => a + b, 0) / gains.length;
    if (avg > bestAvg) { bestAvg = avg; bestStrat = strat; }
  }

  if (!bestStrat || bestAvg <= 0) return null;

  // Map strategy ID to human label
  const STRATEGY_LABELS: Record<string, string> = {
    'past-papers': 'Past papers',
    'active-recall': 'Active recall',
    're-reading': 'Re-reading',
    'summarising': 'Summarising',
    'teaching': 'Teaching',
    'videos': 'Videos',
    'flashcards': 'Flashcards',
  };
  const label = STRATEGY_LABELS[bestStrat] || bestStrat;

  return {
    id: 'debrief-strategy',
    icon: 'Zap',
    iconColor: 'text-purple-500',
    title: `${label} gives you the biggest boost`,
    description: `Your debriefs show +${(bestAvg).toFixed(1)} avg confidence gain when using ${label.toLowerCase()}.`,
    category: 'strategy',
  };
}

// ── Priority Sort ──────────────────────────────────────────

const CATEGORY_PRIORITY: Record<Insight['category'], number> = {
  streak: 0,
  strategy: 1,
  pattern: 2,
  momentum: 3,
};

// ── Hook ───────────────────────────────────────────────────

export function useInsights(
  uid: string | undefined,
  streak: StreakData,
  strategyMastery: StrategyMasteryMap,
): { insights: Insight[]; isLoaded: boolean } {
  const { studySessions: sessions, studyDebriefs: debriefs, progressLoaded } = useProgress();
  const isLoaded = progressLoaded;

  const insights = useMemo(() => {
    const results: Insight[] = [
      // Core insights
      monthlyVolumeChange(sessions),
      bestStudyTime(sessions),
      dormantStrategyNudge(sessions, strategyMastery),
      streakMilestone(streak),
      subjectBalance(sessions),
      consistencyTrend(sessions),
      // Deep insights
      strategyEffectiveness(sessions),
      sessionLengthTrend(sessions),
      reflectionImpact(sessions),
      subjectGap(sessions),
      peakProductivityDay(sessions),
      completionRate(sessions),
      // Debrief insights
      debriefConfidenceGain(debriefs),
      debriefStrategyEffectiveness(debriefs),
    ].filter((i): i is Insight => i !== null);

    results.sort((a, b) => CATEGORY_PRIORITY[a.category] - CATEGORY_PRIORITY[b.category]);

    return results.slice(0, 8);
  }, [sessions, debriefs, streak, strategyMastery]);

  return { insights, isLoaded };
}
