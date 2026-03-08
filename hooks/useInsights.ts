/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useMemo } from 'react';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { type StreakData } from './useStreak';
import { type MoodEntry } from './useMood';
import { type StrategyMasteryMap } from '../types';
import { type StudySessionRecord, STRATEGY_REGISTRY } from '../studySessionData';

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

function moodProductivity(
  sessions: StudySessionRecord[],
  moodEntries: MoodEntry[],
): Insight | null {
  if (sessions.length < 5 || moodEntries.length < 5) return null;

  const moodByDate: Record<string, string> = {};
  for (const e of moodEntries) {
    moodByDate[e.date] = e.mood;
  }

  const moodMinutes: Record<string, number[]> = {};
  for (const s of sessions) {
    const mood = moodByDate[s.date];
    if (!mood) continue;
    if (!moodMinutes[mood]) moodMinutes[mood] = [];
    moodMinutes[mood].push(s.actualSeconds / 60);
  }

  const moods = Object.keys(moodMinutes);
  if (moods.length < 2) return null;

  let bestMood = '';
  let bestAvg = 0;

  for (const mood of moods) {
    const arr = moodMinutes[mood];
    if (arr.length < 2) continue;
    const avg = arr.reduce((a, b) => a + b, 0) / arr.length;
    if (avg > bestAvg) {
      bestAvg = avg;
      bestMood = mood;
    }
  }

  if (!bestMood) return null;

  return {
    id: 'mood-productivity',
    icon: 'Sparkles',
    iconColor: 'text-pink-500',
    title: `Best focus when ${bestMood}`,
    description: `You study longest when you feel ${bestMood} (avg ${Math.round(bestAvg)} min per session).`,
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
  moodEntries: MoodEntry[],
  strategyMastery: StrategyMasteryMap,
): { insights: Insight[]; isLoaded: boolean } {
  const [sessions, setSessions] = useState<StudySessionRecord[]>([]);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    if (!uid) {
      setIsLoaded(true);
      return;
    }

    const load = async () => {
      try {
        const progressDoc = await getDoc(doc(db, 'progress', uid));
        if (progressDoc.exists()) {
          const data = progressDoc.data();
          setSessions(data.studySessions ?? []);
        }
      } catch (err) {
        console.error('Failed to load study sessions for insights:', err);
      }
      setIsLoaded(true);
    };

    load();
  }, [uid]);

  const insights = useMemo(() => {
    const results: Insight[] = [
      monthlyVolumeChange(sessions),
      bestStudyTime(sessions),
      dormantStrategyNudge(sessions, strategyMastery),
      streakMilestone(streak),
      subjectBalance(sessions),
      moodProductivity(sessions, moodEntries),
      consistencyTrend(sessions),
    ].filter((i): i is Insight => i !== null);

    results.sort((a, b) => CATEGORY_PRIORITY[a.category] - CATEGORY_PRIORITY[b.category]);

    return results.slice(0, 5);
  }, [sessions, streak, moodEntries, strategyMastery]);

  return { insights, isLoaded };
}
