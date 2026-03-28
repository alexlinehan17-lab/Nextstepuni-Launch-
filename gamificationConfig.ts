/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type NorthStarCategory } from './types';

// ─── Athlete Ranks ──────────────────────────────────────────────────────────

export interface AthleteRank {
  id: string;
  title: string;
  minPoints: number;
  icon: string;       // Lucide icon name
  color: string;      // Tailwind color token
  colorHex: string;   // For inline styles
}

export const ATHLETE_RANKS: AthleteRank[] = [
  { id: 'newcomer',   title: 'Newcomer',   minPoints: 0,    icon: 'Footprints', color: 'teal-500',   colorHex: '#2A7D6F' },
  { id: 'beginner',   title: 'Beginner',   minPoints: 100,  icon: 'Flame',      color: 'blue-500',   colorHex: '#4361EE' },
  { id: 'consistent', title: 'Consistent', minPoints: 300,  icon: 'TrendingUp', color: 'emerald-500', colorHex: '#10b981' },
  { id: 'dedicated',  title: 'Dedicated',  minPoints: 600,  icon: 'Target',     color: 'teal-500',   colorHex: '#14b8a6' },
  { id: 'driven',     title: 'Driven',     minPoints: 1000, icon: 'Zap',        color: 'amber-500',  colorHex: '#f59e0b' },
  { id: 'elite',      title: 'Elite',      minPoints: 1800, icon: 'Award',      color: 'purple-500', colorHex: '#7209B7' },
  { id: 'master',     title: 'Master',     minPoints: 3000, icon: 'Crown',      color: 'orange-500', colorHex: '#f97316' },
  { id: 'legend',     title: 'Legend',     minPoints: 5000, icon: 'Mountain',   color: 'rose-500',   colorHex: '#E94560' },
];

export function getRankForPoints(totalPoints: number): AthleteRank {
  let rank = ATHLETE_RANKS[0];
  for (const r of ATHLETE_RANKS) {
    if (totalPoints >= r.minPoints) rank = r;
  }
  return rank;
}

export function getNextRank(currentRank: AthleteRank): AthleteRank | null {
  const idx = ATHLETE_RANKS.findIndex(r => r.id === currentRank.id);
  return idx < ATHLETE_RANKS.length - 1 ? ATHLETE_RANKS[idx + 1] : null;
}

export function getRankProgress(totalPoints: number, currentRank: AthleteRank, nextRank: AthleteRank | null): number {
  if (!nextRank) return 100;
  const range = nextRank.minPoints - currentRank.minPoints;
  if (range <= 0) return 100;
  return Math.min(100, Math.round(((totalPoints - currentRank.minPoints) / range) * 100));
}

// ─── Achievement Types ──────────────────────────────────────────────────────

export type AchievementCategory = 'modules' | 'timetable' | 'streaks' | 'reflection' | 'north-star' | 'mastery' | 'journey';

export interface AchievementDefinition {
  id: string;
  title: string;
  description: string;
  category: AchievementCategory;
  icon: string;          // Lucide icon name
  condition: (state: GamificationState) => boolean;
  bonusPoints: number;
  isHidden: boolean;
}

// ─── Weekly Goals ───────────────────────────────────────────────────────────

export interface WeeklyGoal {
  id: string;
  label: string;
  target: number;
  metric: 'sections' | 'sessions' | 'reflections' | 'streak-days';
  icon: string;
}

// Goal targets scale by rank
const GOAL_TARGETS_BY_RANK: Record<string, { sections: number; sessions: number; reflections: number }> = {
  newcomer:   { sections: 3,  sessions: 2,  reflections: 1 },
  beginner:   { sections: 4,  sessions: 3,  reflections: 2 },
  consistent: { sections: 6,  sessions: 5,  reflections: 3 },
  dedicated:  { sections: 8,  sessions: 6,  reflections: 3 },
  driven:     { sections: 10, sessions: 8,  reflections: 5 },
  elite:      { sections: 15, sessions: 12, reflections: 5 },
  master:     { sections: 18, sessions: 14, reflections: 6 },
  legend:     { sections: 20, sessions: 16, reflections: 7 },
};

// Goal variations to keep things fresh — deterministic via weekNumber seed
const GOAL_VARIATIONS: { label: string; metric: WeeklyGoal['metric']; icon: string; targetKey: 'sections' | 'sessions' | 'reflections' }[][] = [
  [
    { label: 'Complete sections', metric: 'sections', icon: 'BookOpen', targetKey: 'sections' },
    { label: 'Log study sessions', metric: 'sessions', icon: 'Clock', targetKey: 'sessions' },
    { label: 'Write reflections', metric: 'reflections', icon: 'PenLine', targetKey: 'reflections' },
  ],
  [
    { label: 'Unlock new content', metric: 'sections', icon: 'Layers', targetKey: 'sections' },
    { label: 'Study session hours', metric: 'sessions', icon: 'Timer', targetKey: 'sessions' },
    { label: 'Reflect on learning', metric: 'reflections', icon: 'MessageSquare', targetKey: 'reflections' },
  ],
  [
    { label: 'Progress through modules', metric: 'sections', icon: 'ChevronRight', targetKey: 'sections' },
    { label: 'Timetable sessions', metric: 'sessions', icon: 'CalendarCheck', targetKey: 'sessions' },
    { label: 'Journal entries', metric: 'reflections', icon: 'NotebookPen', targetKey: 'reflections' },
  ],
];

export function generateWeeklyGoals(rankId: string, weekNumber: number): WeeklyGoal[] {
  const targets = GOAL_TARGETS_BY_RANK[rankId] || GOAL_TARGETS_BY_RANK.newcomer;
  const variationSet = GOAL_VARIATIONS[weekNumber % GOAL_VARIATIONS.length];

  return variationSet.map((v, i) => ({
    id: `week-${weekNumber}-goal-${i}`,
    label: v.label,
    target: targets[v.targetKey],
    metric: v.metric,
    icon: v.icon,
  }));
}

// Weekly goal bonus points: 50 for 1 goal, 100 for 2, 200 for 3
export const WEEKLY_GOAL_BONUS = [0, 50, 100, 200] as const;

export function getWeekNumber(date: Date = new Date()): number {
  const start = new Date(date.getFullYear(), 0, 1);
  const diff = date.getTime() - start.getTime();
  return Math.floor(diff / (7 * 24 * 60 * 60 * 1000));
}

export function getWeekStartDate(date: Date = new Date()): string {
  const d = new Date(date);
  const day = d.getDay();
  const diff = d.getDate() - day + (day === 0 ? -6 : 1); // Monday
  d.setDate(diff);
  d.setHours(0, 0, 0, 0);
  return d.toISOString().slice(0, 10);
}

// ─── Personal Bests ─────────────────────────────────────────────────────────

export interface PersonalBests {
  bestDayPoints: number;
  bestDaySections: number;
  bestDayReflections: number;
  bestWeekPoints: number;
  bestWeekSessions: number;
}

export const DEFAULT_PERSONAL_BESTS: PersonalBests = {
  bestDayPoints: 0,
  bestDaySections: 0,
  bestDayReflections: 0,
  bestWeekPoints: 0,
  bestWeekSessions: 0,
};

// ─── Habit Strength ─────────────────────────────────────────────────────────

export interface HabitStrength {
  behavior: 'modules' | 'sessions' | 'reflections';
  totalCount: number;
  last30DayCount: number;
  consistencyScore: number;  // 0-1
  isEstablished: boolean;    // last30DayCount >= 20 AND consistencyScore >= 0.6
}

// ─── Gamification State ─────────────────────────────────────────────────────

export interface GamificationState {
  totalPointsEarned: number;
  currentStreak: number;
  longestStreak: number;
  modulesCompleted: number;
  sectionsCompleted: number;
  categoriesCompleted: number;
  totalReflections: number;
  totalTimetableSessions: number;
  northStarCategory: NorthStarCategory | null;
  currentRank: AthleteRank;
  nextRank: AthleteRank | null;
  rankProgress: number;
  unlockedAchievements: string[];
  achievementTimestamps: Record<string, number>;
  weeklyGoalProgress: Record<string, number>;
  weekStartDate: string;
  personalBests: PersonalBests;
  journeyMilestones: number;
  streakShields: number;
}

// ─── Gamification Firestore Schema ──────────────────────────────────────────

export interface GamificationFirestoreData {
  unlockedAchievements: string[];
  achievementTimestamps: Record<string, number>;
  weeklyGoalProgress: Record<string, number>;
  weekStartDate: string;
  lastSurpriseDate: string;
  personalBests: PersonalBests;
  streakShields: number;
  streakShieldUsedDates: string[];
  lastStreakBreakDate: string;
  recoveryWindowEnd: string;
}

export const DEFAULT_GAMIFICATION_DATA: GamificationFirestoreData = {
  unlockedAchievements: [],
  achievementTimestamps: {},
  weeklyGoalProgress: {},
  weekStartDate: '',
  lastSurpriseDate: '',
  personalBests: { ...DEFAULT_PERSONAL_BESTS },
  streakShields: 0,
  streakShieldUsedDates: [],
  lastStreakBreakDate: '',
  recoveryWindowEnd: '',
};

// ─── Streak Tier Visuals ────────────────────────────────────────────────────

export type StreakTier = 'none' | 'small' | 'medium' | 'large' | 'monthly';

export function getStreakTier(currentStreak: number): StreakTier {
  if (currentStreak >= 30) return 'monthly';
  if (currentStreak >= 14) return 'large';
  if (currentStreak >= 7) return 'medium';
  if (currentStreak >= 3) return 'small';
  return 'none';
}

// ─── Milestone Surprise Thresholds ──────────────────────────────────────────

export const MILESTONE_THRESHOLDS = [250, 750, 1500, 2500, 4000] as const;

export interface MilestoneSurprise {
  threshold: number;
  label: string;
  bonusPoints: number;
}

export const MILESTONE_SURPRISES: MilestoneSurprise[] = [
  { threshold: 250,  label: 'First Milestone!',  bonusPoints: 25 },
  { threshold: 750,  label: 'Rising Star',        bonusPoints: 50 },
  { threshold: 1500, label: 'Halfway Hero',        bonusPoints: 75 },
  { threshold: 2500, label: 'Unstoppable',         bonusPoints: 100 },
  { threshold: 4000, label: 'Legend in the Making', bonusPoints: 150 },
];

// ─── Variable Reward (Bonus Flash) ──────────────────────────────────────────

export const BONUS_FLASH_CHANCE = 0.08; // 8% chance of 2x multiplier
