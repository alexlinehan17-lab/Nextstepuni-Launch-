/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type AchievementDefinition, type GamificationState } from './gamificationConfig';
import { getAllNorthStarAchievements } from './northStarProgressionData';
import { type CurriculumLevel } from './utils/authUtils';

// ─── Achievement Definitions ────────────────────────────────────────────────
// Achievements are recognition first and currency second. Bonuses stay small
// so a badge feels meaningful without allowing milestone cascades to dominate
// the Journey Points economy.

export const ACHIEVEMENTS: AchievementDefinition[] = [
  // ── Modules ───────────────────────────────────────────────────────────────
  {
    id: 'first-step',
    title: 'First Step',
    description: 'Complete your first section',
    category: 'modules',
    icon: 'Footprints',
    condition: (s: GamificationState) => s.sectionsCompleted >= 1,
    bonusPoints: 2,
    isHidden: false,
  },
  {
    id: 'getting-started',
    title: 'Getting Started',
    description: 'Complete 10 sections',
    category: 'modules',
    icon: 'PlayCircle',
    condition: (s: GamificationState) => s.sectionsCompleted >= 10,
    bonusPoints: 3,
    isHidden: false,
  },
  {
    id: 'first-module',
    title: 'Module Master',
    description: 'Complete your first full module',
    category: 'modules',
    icon: 'BookCheck',
    condition: (s: GamificationState) => s.modulesCompleted >= 1,
    bonusPoints: 5,
    isHidden: false,
  },
  {
    id: 'getting-serious',
    title: 'Getting Serious',
    description: 'Complete 5 modules',
    category: 'modules',
    icon: 'BookOpen',
    condition: (s: GamificationState) => s.modulesCompleted >= 5,
    bonusPoints: 10,
    isHidden: false,
  },
  {
    id: 'double-digits',
    title: 'Double Digits',
    description: 'Complete 10 modules',
    category: 'modules',
    icon: 'Hash',
    condition: (s: GamificationState) => s.modulesCompleted >= 10,
    bonusPoints: 15,
    isHidden: false,
  },
  {
    id: 'halfway-there',
    title: 'Halfway There',
    description: 'Complete 20 modules',
    category: 'modules',
    icon: 'Milestone',
    condition: (s: GamificationState) => s.modulesCompleted >= 20,
    bonusPoints: 20,
    isHidden: false,
  },
  {
    id: 'completionist',
    title: 'Completionist',
    description: 'Complete 40 modules',
    category: 'modules',
    icon: 'Trophy',
    condition: (s: GamificationState) => s.modulesCompleted >= 40,
    bonusPoints: 40,
    isHidden: false,
  },
  {
    id: 'section-grinder',
    title: 'Section Grinder',
    description: 'Complete 50 sections',
    category: 'modules',
    icon: 'Layers',
    condition: (s: GamificationState) => s.sectionsCompleted >= 50,
    bonusPoints: 10,
    isHidden: false,
  },
  {
    id: 'section-centurion',
    title: 'Centurion',
    description: 'Complete 100 sections',
    category: 'modules',
    icon: 'Shield',
    condition: (s: GamificationState) => s.sectionsCompleted >= 100,
    bonusPoints: 20,
    isHidden: false,
  },
  {
    id: 'category-cleared',
    title: 'Category Cleared',
    description: 'Complete all modules in a category',
    category: 'modules',
    icon: 'FolderCheck',
    condition: (s: GamificationState) => s.categoriesCompleted >= 1,
    bonusPoints: 15,
    isHidden: false,
  },
  {
    id: 'multi-category',
    title: 'Well Rounded',
    description: 'Complete modules in 3 different categories',
    category: 'modules',
    icon: 'CircleDot',
    condition: (s: GamificationState) => s.categoriesCompleted >= 3,
    bonusPoints: 20,
    isHidden: false,
  },

  // ── Timetable / Sessions ──────────────────────────────────────────────────
  {
    id: 'session-one',
    title: 'Session One',
    description: 'Log your first study session',
    category: 'timetable',
    icon: 'Clock',
    condition: (s: GamificationState) => s.totalTimetableSessions >= 1,
    bonusPoints: 2,
    isHidden: false,
  },
  {
    id: 'five-sessions',
    title: 'Building Rhythm',
    description: 'Log 5 study sessions',
    category: 'timetable',
    icon: 'Timer',
    condition: (s: GamificationState) => s.totalTimetableSessions >= 5,
    bonusPoints: 4,
    isHidden: false,
  },
  {
    id: 'ten-sessions',
    title: 'Double Digits',
    description: 'Log 10 study sessions',
    category: 'timetable',
    icon: 'CalendarCheck',
    condition: (s: GamificationState) => s.totalTimetableSessions >= 10,
    bonusPoints: 6,
    isHidden: false,
  },
  {
    id: 'twenty-five-sessions',
    title: 'Quarter Century',
    description: 'Log 25 study sessions',
    category: 'timetable',
    icon: 'Calendar',
    condition: (s: GamificationState) => s.totalTimetableSessions >= 25,
    bonusPoints: 10,
    isHidden: false,
  },
  {
    id: 'fifty-sessions',
    title: 'Study Machine',
    description: 'Log 50 study sessions',
    category: 'timetable',
    icon: 'Zap',
    condition: (s: GamificationState) => s.totalTimetableSessions >= 50,
    bonusPoints: 15,
    isHidden: false,
  },
  {
    id: 'hundred-sessions',
    title: 'Centurion Sessions',
    description: 'Log 100 study sessions',
    category: 'timetable',
    icon: 'Award',
    condition: (s: GamificationState) => s.totalTimetableSessions >= 100,
    bonusPoints: 30,
    isHidden: false,
  },

  // ── Streaks ───────────────────────────────────────────────────────────────
  {
    id: 'streak-3',
    title: '3-Day Streak',
    description: 'Study for 3 days in a row',
    category: 'streaks',
    icon: 'Flame',
    condition: (s: GamificationState) => s.currentStreak >= 3 || s.longestStreak >= 3,
    bonusPoints: 3,
    isHidden: false,
  },
  {
    id: 'streak-7',
    title: 'Full Week',
    description: 'Study for 7 days in a row',
    category: 'streaks',
    icon: 'Flame',
    condition: (s: GamificationState) => s.currentStreak >= 7 || s.longestStreak >= 7,
    bonusPoints: 6,
    isHidden: false,
  },
  {
    id: 'streak-14',
    title: 'Two Week Warrior',
    description: 'Study for 14 days in a row',
    category: 'streaks',
    icon: 'Flame',
    condition: (s: GamificationState) => s.currentStreak >= 14 || s.longestStreak >= 14,
    bonusPoints: 10,
    isHidden: false,
  },
  {
    id: 'streak-21',
    title: 'Three Week Champion',
    description: '21 days in a row — habit territory',
    category: 'streaks',
    icon: 'Flame',
    condition: (s: GamificationState) => s.currentStreak >= 21 || s.longestStreak >= 21,
    bonusPoints: 15,
    isHidden: false,
  },
  {
    id: 'streak-30',
    title: 'Monthly Machine',
    description: '30 consecutive days of study',
    category: 'streaks',
    icon: 'Flame',
    condition: (s: GamificationState) => s.currentStreak >= 30 || s.longestStreak >= 30,
    bonusPoints: 30,
    isHidden: true,
  },
  {
    id: 'streak-60',
    title: 'Unstoppable Force',
    description: '60 consecutive days of study',
    category: 'streaks',
    icon: 'Flame',
    condition: (s: GamificationState) => s.currentStreak >= 60 || s.longestStreak >= 60,
    bonusPoints: 60,
    isHidden: true,
  },

  // ── Reflections ───────────────────────────────────────────────────────────
  {
    id: 'thinking-out-loud',
    title: 'Thinking Out Loud',
    description: 'Write your first reflection',
    category: 'reflection',
    icon: 'PenLine',
    condition: (s: GamificationState) => s.totalReflections >= 1,
    bonusPoints: 2,
    isHidden: false,
  },
  {
    id: 'five-reflections',
    title: 'Reflective Mind',
    description: 'Write 5 reflections',
    category: 'reflection',
    icon: 'MessageSquare',
    condition: (s: GamificationState) => s.totalReflections >= 5,
    bonusPoints: 4,
    isHidden: false,
  },
  {
    id: 'ten-reflections',
    title: 'Deep Thinker',
    description: 'Write 10 reflections',
    category: 'reflection',
    icon: 'Brain',
    condition: (s: GamificationState) => s.totalReflections >= 10,
    bonusPoints: 7,
    isHidden: false,
  },
  {
    id: 'twenty-five-reflections',
    title: 'Philosopher',
    description: 'Write 25 reflections',
    category: 'reflection',
    icon: 'Lightbulb',
    condition: (s: GamificationState) => s.totalReflections >= 25,
    bonusPoints: 15,
    isHidden: false,
  },
  {
    id: 'fifty-reflections',
    title: 'Journaling Pro',
    description: 'Write 50 reflections',
    category: 'reflection',
    icon: 'NotebookPen',
    condition: (s: GamificationState) => s.totalReflections >= 50,
    bonusPoints: 30,
    isHidden: false,
  },

  // ── North Star ────────────────────────────────────────────────────────────
  {
    id: 'north-star-set',
    title: 'Direction Set',
    description: 'Set your North Star motivation',
    category: 'north-star',
    icon: 'Star',
    condition: (s: GamificationState) => s.northStarCategory !== null,
    bonusPoints: 4,
    isHidden: false,
  },
  {
    id: 'north-star-first-week',
    title: 'Star Gazer',
    description: 'Complete 15 sections after setting your North Star',
    category: 'north-star',
    icon: 'Sparkles',
    condition: (s: GamificationState) => s.northStarCategory !== null && s.sectionsCompleted >= 15,
    bonusPoints: 5,
    isHidden: false,
  },
  {
    id: 'north-star-dedicated',
    title: 'Star Driven',
    description: 'Reach Dedicated rank with a North Star set',
    category: 'north-star',
    icon: 'Compass',
    condition: (s: GamificationState) => s.northStarCategory !== null && s.totalPointsEarned >= 2400,
    bonusPoints: 10,
    isHidden: false,
  },
  {
    id: 'north-star-elite',
    title: 'Star Power',
    description: 'Reach Elite rank with a North Star set',
    category: 'north-star',
    icon: 'Crown',
    condition: (s: GamificationState) => s.northStarCategory !== null && s.totalPointsEarned >= 7200,
    bonusPoints: 20,
    isHidden: false,
  },

  // ── Journey ───────────────────────────────────────────────────────────────
  {
    id: 'first-vision',
    title: 'First Vision Unlocked',
    description: 'Unlock your first journey milestone',
    category: 'journey',
    icon: 'Eye',
    condition: (s: GamificationState) => s.journeyMilestones >= 1,
    bonusPoints: 4,
    isHidden: false,
  },
  {
    id: 'journey-halfway',
    title: 'Half Way There',
    description: 'Unlock 6 journey milestones',
    category: 'journey',
    icon: 'Mountain',
    condition: (s: GamificationState) => s.journeyMilestones >= 6,
    bonusPoints: 10,
    isHidden: false,
  },
  {
    id: 'journey-complete',
    title: 'Vision Complete',
    description: 'Unlock all 12 journey milestones',
    category: 'journey',
    icon: 'Sunrise',
    condition: (s: GamificationState) => s.journeyMilestones >= 12,
    bonusPoints: 40,
    isHidden: false,
  },

  // ── Mastery ───────────────────────────────────────────────────────────────
  {
    id: 'first-hundred',
    title: 'First Hundred',
    description: 'Earn 100 total points',
    category: 'mastery',
    icon: 'TrendingUp',
    condition: (s: GamificationState) => s.totalPointsEarned >= 100,
    bonusPoints: 2,
    isHidden: false,
  },
  {
    id: 'five-hundred',
    title: 'Rising Star',
    description: 'Earn 500 total points',
    category: 'mastery',
    icon: 'Star',
    condition: (s: GamificationState) => s.totalPointsEarned >= 500,
    bonusPoints: 5,
    isHidden: false,
  },
  {
    id: 'one-thousand',
    title: 'Grand',
    description: 'Earn 1,000 total points',
    category: 'mastery',
    icon: 'Sparkles',
    condition: (s: GamificationState) => s.totalPointsEarned >= 1000,
    bonusPoints: 10,
    isHidden: false,
  },
  {
    id: 'three-thousand',
    title: 'Triple Threat',
    description: 'Earn 3,000 total points',
    category: 'mastery',
    icon: 'Gem',
    condition: (s: GamificationState) => s.totalPointsEarned >= 3000,
    bonusPoints: 20,
    isHidden: false,
  },
  {
    id: 'five-thousand',
    title: 'Legendary',
    description: 'Earn 5,000 total points',
    category: 'mastery',
    icon: 'Crown',
    condition: (s: GamificationState) => s.totalPointsEarned >= 5000,
    bonusPoints: 40,
    isHidden: true,
  },
  {
    id: 'all-rounder',
    title: 'All-Rounder',
    description: 'Complete a module, log a session, and write a reflection',
    category: 'mastery',
    icon: 'Target',
    condition: (s: GamificationState) => s.modulesCompleted >= 1 && s.totalTimetableSessions >= 1 && s.totalReflections >= 1,
    bonusPoints: 6,
    isHidden: false,
  },
  {
    id: 'streak-shield-earned',
    title: 'Shielded',
    description: 'Earn your first streak shield',
    category: 'streaks',
    icon: 'ShieldCheck',
    condition: (s: GamificationState) => s.streakShields >= 1,
    bonusPoints: 3,
    isHidden: false,
  },
  {
    id: 'personal-best-day',
    title: 'Best Day Ever',
    description: 'Score 100+ points in a single day',
    category: 'mastery',
    icon: 'ArrowUp',
    condition: (s: GamificationState) => s.personalBests.bestDayPoints >= 100,
    bonusPoints: 5,
    isHidden: false,
  },
  {
    id: 'personal-best-week',
    title: 'Power Week',
    description: 'Log 20+ sessions in a single week',
    category: 'mastery',
    icon: 'BarChart3',
    condition: (s: GamificationState) => s.personalBests.bestWeekSessions >= 20,
    bonusPoints: 10,
    isHidden: true,
  },
];

// ─── Junior Cycle universal achievements ───────────────────────────────────
// Mirrors the senior universal set 1:1 — same categories, same counts, same
// mechanics (s.modulesCompleted / s.totalTimetableSessions / etc. count the
// same way regardless of curriculum), JC peer voice. Tagged
// curriculum: 'junior' so the gallery and unlock logic can filter cleanly.
// North-star achievements gate on JC NorthStarCategory ids.

const JC_ACHIEVEMENTS: AchievementDefinition[] = [
  // ── Modules (11) ──────────────────────────────────────────────────────────
  { id: 'jc-first-step', title: 'First Step', description: 'Finish your first section', category: 'modules', icon: 'Footprints', condition: (s) => s.sectionsCompleted >= 1, bonusPoints: 2, isHidden: false, curriculum: 'junior' },
  { id: 'jc-getting-started', title: 'Off the Mark', description: 'Finish 10 sections', category: 'modules', icon: 'PlayCircle', condition: (s) => s.sectionsCompleted >= 10, bonusPoints: 3, isHidden: false, curriculum: 'junior' },
  { id: 'jc-first-module', title: 'First Module Done', description: 'Finish a whole module from start to end', category: 'modules', icon: 'BookCheck', condition: (s) => s.modulesCompleted >= 1, bonusPoints: 5, isHidden: false, curriculum: 'junior' },
  { id: 'jc-getting-serious', title: 'Picking Up Speed', description: 'Finish 5 modules', category: 'modules', icon: 'BookOpen', condition: (s) => s.modulesCompleted >= 5, bonusPoints: 10, isHidden: false, curriculum: 'junior' },
  { id: 'jc-double-digits', title: 'Double Digits', description: 'Finish 10 modules', category: 'modules', icon: 'Hash', condition: (s) => s.modulesCompleted >= 10, bonusPoints: 15, isHidden: false, curriculum: 'junior' },
  { id: 'jc-halfway-there', title: 'Halfway There', description: 'Finish 20 modules', category: 'modules', icon: 'Milestone', condition: (s) => s.modulesCompleted >= 20, bonusPoints: 20, isHidden: false, curriculum: 'junior' },
  { id: 'jc-completionist', title: 'Completionist', description: 'Finish 40 modules', category: 'modules', icon: 'Trophy', condition: (s) => s.modulesCompleted >= 40, bonusPoints: 40, isHidden: false, curriculum: 'junior' },
  { id: 'jc-section-grinder', title: 'Section Grinder', description: 'Finish 50 sections', category: 'modules', icon: 'Layers', condition: (s) => s.sectionsCompleted >= 50, bonusPoints: 10, isHidden: false, curriculum: 'junior' },
  { id: 'jc-section-centurion', title: 'Hundred Up', description: 'Finish 100 sections', category: 'modules', icon: 'Shield', condition: (s) => s.sectionsCompleted >= 100, bonusPoints: 20, isHidden: false, curriculum: 'junior' },
  { id: 'jc-category-cleared', title: 'Category Cleared', description: 'Finish every module in a category', category: 'modules', icon: 'FolderCheck', condition: (s) => s.categoriesCompleted >= 1, bonusPoints: 15, isHidden: false, curriculum: 'junior' },
  { id: 'jc-multi-category', title: 'All-Round Player', description: 'Finish modules in 3 different categories', category: 'modules', icon: 'CircleDot', condition: (s) => s.categoriesCompleted >= 3, bonusPoints: 20, isHidden: false, curriculum: 'junior' },

  // ── Timetable / Sessions (6) ──────────────────────────────────────────────
  { id: 'jc-session-one', title: 'First Session', description: 'Log your first study session', category: 'timetable', icon: 'Clock', condition: (s) => s.totalTimetableSessions >= 1, bonusPoints: 2, isHidden: false, curriculum: 'junior' },
  { id: 'jc-five-sessions', title: 'Finding the Rhythm', description: 'Log 5 study sessions', category: 'timetable', icon: 'Timer', condition: (s) => s.totalTimetableSessions >= 5, bonusPoints: 4, isHidden: false, curriculum: 'junior' },
  { id: 'jc-ten-sessions', title: 'Ten in the Bag', description: 'Log 10 study sessions', category: 'timetable', icon: 'CalendarCheck', condition: (s) => s.totalTimetableSessions >= 10, bonusPoints: 6, isHidden: false, curriculum: 'junior' },
  { id: 'jc-twenty-five-sessions', title: 'Quarter Century', description: 'Log 25 study sessions', category: 'timetable', icon: 'Calendar', condition: (s) => s.totalTimetableSessions >= 25, bonusPoints: 10, isHidden: false, curriculum: 'junior' },
  { id: 'jc-fifty-sessions', title: 'Half a Hundred', description: 'Log 50 study sessions', category: 'timetable', icon: 'Zap', condition: (s) => s.totalTimetableSessions >= 50, bonusPoints: 15, isHidden: false, curriculum: 'junior' },
  { id: 'jc-hundred-sessions', title: 'Hundred Sessions', description: 'Log 100 study sessions', category: 'timetable', icon: 'Award', condition: (s) => s.totalTimetableSessions >= 100, bonusPoints: 30, isHidden: false, curriculum: 'junior' },

  // ── Streaks (7 — incl. shield) ────────────────────────────────────────────
  { id: 'jc-streak-3', title: '3-Day Streak', description: 'Study three days in a row', category: 'streaks', icon: 'Flame', condition: (s) => s.currentStreak >= 3 || s.longestStreak >= 3, bonusPoints: 3, isHidden: false, curriculum: 'junior' },
  { id: 'jc-streak-7', title: 'Full Week', description: 'Study seven days in a row', category: 'streaks', icon: 'Flame', condition: (s) => s.currentStreak >= 7 || s.longestStreak >= 7, bonusPoints: 6, isHidden: false, curriculum: 'junior' },
  { id: 'jc-streak-14', title: 'Two Solid Weeks', description: 'Study 14 days in a row', category: 'streaks', icon: 'Flame', condition: (s) => s.currentStreak >= 14 || s.longestStreak >= 14, bonusPoints: 10, isHidden: false, curriculum: 'junior' },
  { id: 'jc-streak-21', title: 'Habit Forming', description: '21 days in a row — that\'s the habit zone', category: 'streaks', icon: 'Flame', condition: (s) => s.currentStreak >= 21 || s.longestStreak >= 21, bonusPoints: 15, isHidden: false, curriculum: 'junior' },
  { id: 'jc-streak-30', title: 'Month Strong', description: '30 days in a row', category: 'streaks', icon: 'Flame', condition: (s) => s.currentStreak >= 30 || s.longestStreak >= 30, bonusPoints: 30, isHidden: true, curriculum: 'junior' },
  { id: 'jc-streak-60', title: 'Two Months Unbroken', description: '60 days in a row', category: 'streaks', icon: 'Flame', condition: (s) => s.currentStreak >= 60 || s.longestStreak >= 60, bonusPoints: 60, isHidden: true, curriculum: 'junior' },
  { id: 'jc-streak-shield-earned', title: 'Shielded', description: 'Earn your first streak shield', category: 'streaks', icon: 'ShieldCheck', condition: (s) => s.streakShields >= 1, bonusPoints: 3, isHidden: false, curriculum: 'junior' },

  // ── Reflections (5) ───────────────────────────────────────────────────────
  { id: 'jc-thinking-out-loud', title: 'Thinking Out Loud', description: 'Write your first reflection', category: 'reflection', icon: 'PenLine', condition: (s) => s.totalReflections >= 1, bonusPoints: 2, isHidden: false, curriculum: 'junior' },
  { id: 'jc-five-reflections', title: 'Reflective Mind', description: 'Write 5 reflections', category: 'reflection', icon: 'MessageSquare', condition: (s) => s.totalReflections >= 5, bonusPoints: 4, isHidden: false, curriculum: 'junior' },
  { id: 'jc-ten-reflections', title: 'Deep Thinker', description: 'Write 10 reflections', category: 'reflection', icon: 'Brain', condition: (s) => s.totalReflections >= 10, bonusPoints: 7, isHidden: false, curriculum: 'junior' },
  { id: 'jc-twenty-five-reflections', title: 'Real Self-Awareness', description: 'Write 25 reflections', category: 'reflection', icon: 'Lightbulb', condition: (s) => s.totalReflections >= 25, bonusPoints: 15, isHidden: false, curriculum: 'junior' },
  { id: 'jc-fifty-reflections', title: 'Journal Habit', description: 'Write 50 reflections', category: 'reflection', icon: 'NotebookPen', condition: (s) => s.totalReflections >= 50, bonusPoints: 30, isHidden: false, curriculum: 'junior' },

  // ── North Star (4 — gates on JC NS categories) ────────────────────────────
  { id: 'jc-north-star-set', title: 'Direction Set', description: 'Pick a North Star', category: 'north-star', icon: 'Star', condition: (s) => s.northStarCategory === 'family-people' || s.northStarCategory === 'prove-myself-jc' || s.northStarCategory === 'curiosity-craft' || s.northStarCategory === 'future-doors', bonusPoints: 4, isHidden: false, curriculum: 'junior' },
  { id: 'jc-north-star-first-week', title: 'Star Gazer', description: 'Finish 15 sections after picking your North Star', category: 'north-star', icon: 'Sparkles', condition: (s) => (s.northStarCategory === 'family-people' || s.northStarCategory === 'prove-myself-jc' || s.northStarCategory === 'curiosity-craft' || s.northStarCategory === 'future-doors') && s.sectionsCompleted >= 15, bonusPoints: 5, isHidden: false, curriculum: 'junior' },
  { id: 'jc-north-star-dedicated', title: 'Locked In', description: 'Reach Dedicated rank with a North Star picked', category: 'north-star', icon: 'Compass', condition: (s) => (s.northStarCategory === 'family-people' || s.northStarCategory === 'prove-myself-jc' || s.northStarCategory === 'curiosity-craft' || s.northStarCategory === 'future-doors') && s.totalPointsEarned >= 2400, bonusPoints: 10, isHidden: false, curriculum: 'junior' },
  { id: 'jc-north-star-elite', title: 'Star Power', description: 'Reach Elite rank with a North Star picked', category: 'north-star', icon: 'Crown', condition: (s) => (s.northStarCategory === 'family-people' || s.northStarCategory === 'prove-myself-jc' || s.northStarCategory === 'curiosity-craft' || s.northStarCategory === 'future-doors') && s.totalPointsEarned >= 7200, bonusPoints: 20, isHidden: false, curriculum: 'junior' },

  // ── Journey (3) ───────────────────────────────────────────────────────────
  { id: 'jc-first-vision', title: 'First Vision Unlocked', description: 'Unlock your first journey milestone', category: 'journey', icon: 'Eye', condition: (s) => s.journeyMilestones >= 1, bonusPoints: 4, isHidden: false, curriculum: 'junior' },
  { id: 'jc-journey-halfway', title: 'Halfway Up', description: 'Unlock 6 journey milestones', category: 'journey', icon: 'Mountain', condition: (s) => s.journeyMilestones >= 6, bonusPoints: 10, isHidden: false, curriculum: 'junior' },
  { id: 'jc-journey-complete', title: 'Full Picture', description: 'Unlock all 12 journey milestones', category: 'journey', icon: 'Sunrise', condition: (s) => s.journeyMilestones >= 12, bonusPoints: 40, isHidden: false, curriculum: 'junior' },

  // ── Mastery (8) ───────────────────────────────────────────────────────────
  { id: 'jc-first-hundred', title: 'First Hundred', description: 'Earn 100 points', category: 'mastery', icon: 'TrendingUp', condition: (s) => s.totalPointsEarned >= 100, bonusPoints: 2, isHidden: false, curriculum: 'junior' },
  { id: 'jc-five-hundred', title: 'On the Rise', description: 'Earn 500 points', category: 'mastery', icon: 'Star', condition: (s) => s.totalPointsEarned >= 500, bonusPoints: 5, isHidden: false, curriculum: 'junior' },
  { id: 'jc-one-thousand', title: 'A Grand', description: 'Earn 1,000 points', category: 'mastery', icon: 'Sparkles', condition: (s) => s.totalPointsEarned >= 1000, bonusPoints: 10, isHidden: false, curriculum: 'junior' },
  { id: 'jc-three-thousand', title: 'Triple Threat', description: 'Earn 3,000 points', category: 'mastery', icon: 'Gem', condition: (s) => s.totalPointsEarned >= 3000, bonusPoints: 20, isHidden: false, curriculum: 'junior' },
  { id: 'jc-five-thousand', title: 'Legend', description: 'Earn 5,000 points', category: 'mastery', icon: 'Crown', condition: (s) => s.totalPointsEarned >= 5000, bonusPoints: 40, isHidden: true, curriculum: 'junior' },
  { id: 'jc-all-rounder', title: 'All-Rounder', description: 'Finish a module, log a session, and write a reflection', category: 'mastery', icon: 'Target', condition: (s) => s.modulesCompleted >= 1 && s.totalTimetableSessions >= 1 && s.totalReflections >= 1, bonusPoints: 6, isHidden: false, curriculum: 'junior' },
  { id: 'jc-personal-best-day', title: 'Best Day Yet', description: 'Score 100+ points in a single day', category: 'mastery', icon: 'ArrowUp', condition: (s) => s.personalBests.bestDayPoints >= 100, bonusPoints: 5, isHidden: false, curriculum: 'junior' },
  { id: 'jc-personal-best-week', title: 'Big Week', description: 'Log 20+ sessions in a single week', category: 'mastery', icon: 'BarChart3', condition: (s) => s.personalBests.bestWeekSessions >= 20, bonusPoints: 10, isHidden: true, curriculum: 'junior' },
];

for (const a of JC_ACHIEVEMENTS) {
  if (!ACHIEVEMENTS.find(existing => existing.id === a.id)) {
    ACHIEVEMENTS.push(a);
  }
}

// Add North Star track achievements
const NS_ACHIEVEMENTS = getAllNorthStarAchievements();
for (const a of NS_ACHIEVEMENTS) {
  if (!ACHIEVEMENTS.find(existing => existing.id === a.id)) {
    ACHIEVEMENTS.push(a);
  }
}

// Lookup helpers
export function isAchievementForCurriculum(
  achievement: AchievementDefinition,
  curriculumLevel: CurriculumLevel = 'senior',
): boolean {
  const scope = achievement.curriculum ?? 'senior';
  return scope === 'both' || scope === curriculumLevel;
}

export function getAchievementsForCurriculum(
  curriculumLevel: CurriculumLevel = 'senior',
): AchievementDefinition[] {
  return ACHIEVEMENTS.filter(achievement => isAchievementForCurriculum(achievement, curriculumLevel));
}

export function getAchievementById(id: string): AchievementDefinition | undefined {
  return ACHIEVEMENTS.find(a => a.id === id);
}

export function getAchievementsByCategory(category: AchievementDefinition['category']): AchievementDefinition[] {
  return ACHIEVEMENTS.filter(a => a.category === category);
}
