/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useMemo } from 'react';
import { useProgress } from '../contexts/ProgressContext';
import { type UserProgress, type TopicMasteryMap } from '../types';
import { type StreakData } from './useStreak';
import { type StudentSubjectProfile, toDateKey } from '../components/subjectData';
import { type CourseData } from '../components/Library';
import { type StudySessionRecord } from '../utils/strategyRegistry';
import { type DebriefEntry } from '../components/StudyDebrief';

// ── Types ──────────────────────────────────────────────────

export interface SmartRecommendation {
  id: string;
  title: string;
  description: string;
  category: 'mastery' | 'strategy' | 'progress' | 'consistency';
}

// ── Recommendation Generators ──────────────────────────────

function streakAtRisk(
  streak: StreakData,
  timetableCompletions: Record<string, string[]> | undefined,
): SmartRecommendation | null {
  if (streak.currentStreak < 2) return null;
  const todayKey = toDateKey(new Date());
  const todayDone = timetableCompletions?.[todayKey] ?? [];
  if (todayDone.length > 0) return null;
  return {
    id: 'streak-at-risk',
    title: `Protect your ${streak.currentStreak}-day streak`,
    description: 'Complete at least one study block today to keep it alive.',
    category: 'consistency',
  };
}

function neglectedSubject(
  sessions: StudySessionRecord[],
  studentProfile: StudentSubjectProfile | null,
): SmartRecommendation | null {
  if (!studentProfile || studentProfile.subjects.length === 0) return null;
  if (sessions.length < 3) return null;

  const now = Date.now();
  const subjectLastStudied: Record<string, number> = {};
  for (const s of sessions) {
    if (!subjectLastStudied[s.subject] || s.startedAt > subjectLastStudied[s.subject]) {
      subjectLastStudied[s.subject] = s.startedAt;
    }
  }

  const profileSubjects = studentProfile.subjects.map(s => s.subjectName);
  let worstSubject = '';
  let worstDays = 0;

  for (const name of profileSubjects) {
    const last = subjectLastStudied[name];
    if (!last) {
      // Never studied — highest priority
      worstSubject = name;
      worstDays = 999;
      break;
    }
    const daysSince = Math.floor((now - last) / 86400000);
    if (daysSince >= 5 && daysSince > worstDays) {
      worstDays = daysSince;
      worstSubject = name;
    }
  }

  if (!worstSubject) return null;

  return {
    id: `neglected-${worstSubject}`,
    title: `${worstSubject} needs attention`,
    description: worstDays >= 999
      ? `You haven't studied ${worstSubject} yet. Start a session today.`
      : `It's been ${worstDays} days since your last ${worstSubject} session.`,
    category: 'mastery',
  };
}

function shakyTopicFocus(
  topicMastery: TopicMasteryMap | undefined,
  studentProfile: StudentSubjectProfile | null,
): SmartRecommendation | null {
  if (!topicMastery || !studentProfile) return null;

  let worstSubject = '';
  let worstCount = 0;

  for (const [subject, topics] of Object.entries(topicMastery)) {
    const shakyCount = Object.values(topics).filter(t => t.confidence === 'shaky').length;
    if (shakyCount > worstCount) {
      worstCount = shakyCount;
      worstSubject = subject;
    }
  }

  if (!worstSubject || worstCount === 0) return null;

  return {
    id: `shaky-${worstSubject}`,
    title: `${worstCount} shaky topic${worstCount !== 1 ? 's' : ''} in ${worstSubject}`,
    description: 'Focus your next session on these weak areas to turn them solid.',
    category: 'mastery',
  };
}

function strategyEffectiveness(
  sessions: StudySessionRecord[],
): SmartRecommendation | null {
  if (sessions.length < 8) return null;

  const overallAvg = sessions.reduce((sum, s) => sum + s.actualSeconds, 0) / sessions.length;
  if (overallAvg < 60) return null;

  const stratDurations: Record<string, number[]> = {};
  for (const s of sessions) {
    if (!s.strategiesShown || s.strategiesShown.length === 0) continue;
    for (const moduleId of s.strategiesShown) {
      if (!stratDurations[moduleId]) stratDurations[moduleId] = [];
      stratDurations[moduleId].push(s.actualSeconds);
    }
  }

  let bestStrategy = '';
  let bestAvg = 0;

  for (const [moduleId, durations] of Object.entries(stratDurations)) {
    if (durations.length < 3) continue;
    const avg = durations.reduce((a, b) => a + b, 0) / durations.length;
    if (avg > bestAvg) {
      bestAvg = avg;
      bestStrategy = moduleId;
    }
  }

  if (!bestStrategy || bestAvg - overallAvg < 60) return null;

  const pct = Math.round(((bestAvg - overallAvg) / overallAvg) * 100);
  // Use a simplified name — just the module id for now
  return {
    id: 'strategy-recommend',
    title: `Use your best strategy`,
    description: `Your sessions are ${pct}% longer with your top strategy. Apply it today.`,
    category: 'strategy',
  };
}

function timetableAdherence(
  timetableCompletions: Record<string, string[]> | undefined,
  studentProfile: StudentSubjectProfile | null,
): SmartRecommendation | null {
  if (!timetableCompletions || !studentProfile) return null;

  // Look at the last 7 days
  const now = new Date();
  let totalBlocks = 0;
  let completedBlocks = 0;

  for (let i = 0; i < 7; i++) {
    const d = new Date(now);
    d.setDate(d.getDate() - i);
    const key = toDateKey(d);
    const completions = timetableCompletions[key];
    if (completions) {
      completedBlocks += completions.length;
    }
    // Estimate ~3 blocks per active day
    const dayName = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][d.getDay()];
    const restDays = studentProfile.restDays || [];
    if (!restDays.includes(dayName)) {
      totalBlocks += 3;
    }
  }

  if (totalBlocks === 0) return null;
  const rate = completedBlocks / totalBlocks;
  if (rate >= 0.6) return null;

  const pct = Math.round(rate * 100);
  return {
    id: 'timetable-adherence',
    title: `${pct}% timetable completion this week`,
    description: 'Try to follow your timetable more closely. Start with today\'s first block.',
    category: 'consistency',
  };
}

function moduleMomentum(
  userProgress: UserProgress,
  courses: CourseData[],
): SmartRecommendation | null {
  let bestModule = '';
  let bestPct = 0;

  for (const course of courses) {
    const p = userProgress[course.id];
    if (!p) continue;
    const pct = p.unlockedSection / course.sectionsCount;
    if (pct > 0 && pct < 1 && pct > bestPct) {
      bestPct = pct;
      bestModule = course.title;
    }
  }

  if (!bestModule || bestPct < 0.3) return null;

  const pctStr = Math.round(bestPct * 100);
  return {
    id: 'module-momentum',
    title: `${pctStr}% through "${bestModule}"`,
    description: 'Keep the momentum going \u2014 finish the next section today.',
    category: 'progress',
  };
}

function unstudiedModule(
  userProgress: UserProgress,
  courses: CourseData[],
): SmartRecommendation | null {
  const unstudied = courses.filter(c => {
    if (c.category === 'subject-specific-science') return false;
    const p = userProgress[c.id];
    return !p || p.unlockedSection === 0;
  });

  if (unstudied.length === 0) return null;

  // Pick first unstudied
  const pick = unstudied[0];
  return {
    id: `unstudied-${pick.id}`,
    title: `Start "${pick.title}"`,
    description: 'You haven\'t opened this module yet. Take a look today.',
    category: 'progress',
  };
}

// ── Hook ───────────────────────────────────────────────────

export function useRecommendation(
  uid: string | undefined,
  userProgress: UserProgress,
  courses: CourseData[],
  streak: StreakData,
  studentProfile: StudentSubjectProfile | null,
  timetableCompletions: Record<string, string[]> | undefined,
): { recommendation: SmartRecommendation | null } {
  const { rawProgressDoc, progressLoaded } = useProgress();
  const sessions: StudySessionRecord[] = rawProgressDoc.studySessions ?? [];
  const topicMastery: TopicMasteryMap | undefined = rawProgressDoc.topicMastery ?? undefined;
  const isLoaded = progressLoaded;

  const recommendation = useMemo(() => {
    if (!isLoaded) return null;

    // Priority order — first non-null wins
    const generators: (SmartRecommendation | null)[] = [
      streakAtRisk(streak, timetableCompletions),
      neglectedSubject(sessions, studentProfile),
      shakyTopicFocus(topicMastery, studentProfile),
      strategyEffectiveness(sessions),
      timetableAdherence(timetableCompletions, studentProfile),
      moduleMomentum(userProgress, courses),
      unstudiedModule(userProgress, courses),
    ];

    return generators.find(r => r !== null) ?? null;
  }, [isLoaded, streak, timetableCompletions, sessions, studentProfile, topicMastery, userProgress, courses]);

  return { recommendation };
}
