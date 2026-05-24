/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type NorthStarCategory } from './types';
import { type AchievementDefinition, type GamificationState } from './gamificationConfig';

// ─── North Star Progression Tracks ──────────────────────────────────────────

export interface NorthStarTrack {
  category: NorthStarCategory;
  trackTitle: string;
  trackDescription: string;
  milestoneNames: string[];         // 5 named milestones
  achievements: AchievementDefinition[];  // Category-specific achievements
  weeklyChallengeFlavors: string[];       // Rotating motivational text
  progressMetric: 'modules' | 'sessions' | 'reflections';
}

export const NORTH_STAR_TRACKS: Record<NorthStarCategory, NorthStarTrack> = {
  independence: {
    category: 'independence',
    trackTitle: 'The Independence Track',
    trackDescription: 'Building the discipline and skills to forge your own path.',
    milestoneNames: ['Foundation', 'Self-Starter', 'Building Momentum', 'Self-Reliant', 'Independent'],
    progressMetric: 'sessions',
    weeklyChallengeFlavors: [
      'Every session builds your independence.',
      'Discipline is freedom in disguise.',
      'Your future self is counting on you.',
      'Each study block is a brick in your foundation.',
    ],
    achievements: [
      {
        id: 'ns-independence-start',
        title: 'Path Chosen',
        description: 'Begin the Independence Track',
        category: 'north-star',
        icon: 'Footprints',
        condition: (s: GamificationState) => s.northStarCategory === 'independence' && s.totalTimetableSessions >= 1,
        bonusPoints: 15,
        isHidden: false,
      },
      {
        id: 'ns-independence-5',
        title: 'Self-Starter',
        description: 'Log 10 sessions on the Independence Track',
        category: 'north-star',
        icon: 'TrendingUp',
        condition: (s: GamificationState) => s.northStarCategory === 'independence' && s.totalTimetableSessions >= 10,
        bonusPoints: 30,
        isHidden: false,
      },
      {
        id: 'ns-independence-25',
        title: 'Self-Reliant',
        description: 'Log 25 sessions on the Independence Track',
        category: 'north-star',
        icon: 'Shield',
        condition: (s: GamificationState) => s.northStarCategory === 'independence' && s.totalTimetableSessions >= 25,
        bonusPoints: 50,
        isHidden: false,
      },
    ],
  },

  'family-community': {
    category: 'family-community',
    trackTitle: 'The Legacy Track',
    trackDescription: 'Making your family proud through dedication and heart.',
    milestoneNames: ['Roots', 'Growing Strong', 'Giving Back', 'Role Model', 'Legacy Builder'],
    progressMetric: 'reflections',
    weeklyChallengeFlavors: [
      'Your family sees your effort, even when you don\'t.',
      'Every reflection shows growth they\'d be proud of.',
      'Think about who you\'re doing this for.',
      'Your commitment inspires the people around you.',
    ],
    achievements: [
      {
        id: 'ns-family-start',
        title: 'For My People',
        description: 'Write your first reflection on the Legacy Track',
        category: 'north-star',
        icon: 'Heart',
        condition: (s: GamificationState) => s.northStarCategory === 'family-community' && s.totalReflections >= 1,
        bonusPoints: 15,
        isHidden: false,
      },
      {
        id: 'ns-family-10',
        title: 'Growing Strong',
        description: 'Write 10 reflections on the Legacy Track',
        category: 'north-star',
        icon: 'Users',
        condition: (s: GamificationState) => s.northStarCategory === 'family-community' && s.totalReflections >= 10,
        bonusPoints: 30,
        isHidden: false,
      },
      {
        id: 'ns-family-25',
        title: 'Role Model',
        description: 'Write 25 reflections on the Legacy Track',
        category: 'north-star',
        icon: 'Award',
        condition: (s: GamificationState) => s.northStarCategory === 'family-community' && s.totalReflections >= 25,
        bonusPoints: 50,
        isHidden: false,
      },
    ],
  },

  'career-craft': {
    category: 'career-craft',
    trackTitle: 'The Craft Track',
    trackDescription: 'Mastering the skills that lead to work you love.',
    milestoneNames: ['Apprentice', 'Practitioner', 'Skilled', 'Expert', 'Craftsman'],
    progressMetric: 'modules',
    weeklyChallengeFlavors: [
      'Every module is a step towards mastery.',
      'The best careers are built on deep knowledge.',
      'Passion + skill = unstoppable.',
      'Your craft is taking shape.',
    ],
    achievements: [
      {
        id: 'ns-career-start',
        title: 'Apprentice',
        description: 'Complete your first module on the Craft Track',
        category: 'north-star',
        icon: 'Wrench',
        condition: (s: GamificationState) => s.northStarCategory === 'career-craft' && s.modulesCompleted >= 1,
        bonusPoints: 15,
        isHidden: false,
      },
      {
        id: 'ns-career-5',
        title: 'Skilled',
        description: 'Complete 5 modules on the Craft Track',
        category: 'north-star',
        icon: 'Target',
        condition: (s: GamificationState) => s.northStarCategory === 'career-craft' && s.modulesCompleted >= 5,
        bonusPoints: 30,
        isHidden: false,
      },
      {
        id: 'ns-career-15',
        title: 'Craftsman',
        description: 'Complete 15 modules on the Craft Track',
        category: 'north-star',
        icon: 'Crown',
        condition: (s: GamificationState) => s.northStarCategory === 'career-craft' && s.modulesCompleted >= 15,
        bonusPoints: 50,
        isHidden: false,
      },
    ],
  },

  'college-learning': {
    category: 'college-learning',
    trackTitle: 'The Scholar Track',
    trackDescription: 'Building the academic foundation for your next chapter.',
    milestoneNames: ['Curious', 'Studious', 'Scholar', 'Academic', 'Graduate'],
    progressMetric: 'modules',
    weeklyChallengeFlavors: [
      'College-ready starts right here.',
      'Every concept mastered is a door opened.',
      'You\'re building the foundation for your degree.',
      'Keep learning — your future self will thank you.',
    ],
    achievements: [
      {
        id: 'ns-college-start',
        title: 'Curious Mind',
        description: 'Complete your first module on the Scholar Track',
        category: 'north-star',
        icon: 'GraduationCap',
        condition: (s: GamificationState) => s.northStarCategory === 'college-learning' && s.modulesCompleted >= 1,
        bonusPoints: 15,
        isHidden: false,
      },
      {
        id: 'ns-college-5',
        title: 'Studious',
        description: 'Complete 5 modules on the Scholar Track',
        category: 'north-star',
        icon: 'BookOpen',
        condition: (s: GamificationState) => s.northStarCategory === 'college-learning' && s.modulesCompleted >= 5,
        bonusPoints: 30,
        isHidden: false,
      },
      {
        id: 'ns-college-15',
        title: 'Graduate Ready',
        description: 'Complete 15 modules on the Scholar Track',
        category: 'north-star',
        icon: 'Award',
        condition: (s: GamificationState) => s.northStarCategory === 'college-learning' && s.modulesCompleted >= 15,
        bonusPoints: 50,
        isHidden: false,
      },
    ],
  },

  'prove-myself': {
    category: 'prove-myself',
    trackTitle: 'The Proof Track',
    trackDescription: 'Silencing the doubters through undeniable results.',
    milestoneNames: ['Underdog', 'Contender', 'Competitor', 'Contender', 'Proven'],
    progressMetric: 'modules',
    weeklyChallengeFlavors: [
      'Results don\'t lie. Keep stacking them.',
      'Every module completed is proof.',
      'They\'ll see. You\'ll make sure of it.',
      'The best revenge is massive success.',
    ],
    achievements: [
      {
        id: 'ns-prove-start',
        title: 'Underdog',
        description: 'Complete your first module on the Proof Track',
        category: 'north-star',
        icon: 'Flame',
        condition: (s: GamificationState) => s.northStarCategory === 'prove-myself' && s.modulesCompleted >= 1,
        bonusPoints: 15,
        isHidden: false,
      },
      {
        id: 'ns-prove-5',
        title: 'Contender',
        description: 'Complete 5 modules on the Proof Track',
        category: 'north-star',
        icon: 'TrendingUp',
        condition: (s: GamificationState) => s.northStarCategory === 'prove-myself' && s.modulesCompleted >= 5,
        bonusPoints: 30,
        isHidden: false,
      },
      {
        id: 'ns-prove-15',
        title: 'Proven',
        description: 'Complete 15 modules on the Proof Track',
        category: 'north-star',
        icon: 'Trophy',
        condition: (s: GamificationState) => s.northStarCategory === 'prove-myself' && s.modulesCompleted >= 15,
        bonusPoints: 50,
        isHidden: false,
      },
    ],
  },

  'options-freedom': {
    category: 'options-freedom',
    trackTitle: 'The Freedom Track',
    trackDescription: 'Maximizing your options so you always have choices.',
    milestoneNames: ['Explorer', 'Opportunist', 'Strategist', 'Free Agent', 'Unlimited'],
    progressMetric: 'sessions',
    weeklyChallengeFlavors: [
      'More study = more options. Simple.',
      'Every session opens another door.',
      'Freedom comes from preparation.',
      'The more you know, the more choices you have.',
    ],
    achievements: [
      {
        id: 'ns-freedom-start',
        title: 'Explorer',
        description: 'Log your first session on the Freedom Track',
        category: 'north-star',
        icon: 'Compass',
        condition: (s: GamificationState) => s.northStarCategory === 'options-freedom' && s.totalTimetableSessions >= 1,
        bonusPoints: 15,
        isHidden: false,
      },
      {
        id: 'ns-freedom-10',
        title: 'Strategist',
        description: 'Log 10 sessions on the Freedom Track',
        category: 'north-star',
        icon: 'Target',
        condition: (s: GamificationState) => s.northStarCategory === 'options-freedom' && s.totalTimetableSessions >= 10,
        bonusPoints: 30,
        isHidden: false,
      },
      {
        id: 'ns-freedom-25',
        title: 'Unlimited',
        description: 'Log 25 sessions on the Freedom Track',
        category: 'north-star',
        icon: 'Sparkles',
        condition: (s: GamificationState) => s.northStarCategory === 'options-freedom' && s.totalTimetableSessions >= 25,
        bonusPoints: 50,
        isHidden: false,
      },
    ],
  },

  // ─── Junior Cycle tracks (4) — Phase 5 (extended to 5 milestones) ──────────
  // Mirrors the senior structure 1:1 — 5 milestone names + 5 milestone
  // achievements per track, unlocking at the same metric thresholds the
  // senior tracks use (1, 5/10, 15, 30, 50 depending on metric).
  // Copy tuned to JC tone (peer-from-6th-year voice, no LC framing).

  'family-people': {
    category: 'family-people',
    trackTitle: 'For My People',
    trackDescription: 'Show the people who believe in you that they were right to.',
    milestoneNames: ['First Step', 'Building Up', 'Making Them Proud', 'Role Model', 'Family Legacy'],
    progressMetric: 'reflections',
    weeklyChallengeFlavors: [
      'They see your effort, even when you don\'t feel it.',
      'You\'re building something they can be proud of.',
      'Every reflection shows growth.',
      'Think about who you\'re doing this for.',
    ],
    achievements: [
      {
        id: 'ns-family-people-start',
        title: 'For My People',
        description: 'Write your first reflection on the For My People track',
        category: 'north-star',
        icon: 'Heart',
        condition: (s: GamificationState) => s.northStarCategory === 'family-people' && s.totalReflections >= 1,
        bonusPoints: 15,
        isHidden: false,
        curriculum: 'junior' as const,
      },
      {
        id: 'ns-family-people-10',
        title: 'Building Up',
        description: 'Write 10 reflections on the For My People track',
        category: 'north-star',
        icon: 'Users',
        condition: (s: GamificationState) => s.northStarCategory === 'family-people' && s.totalReflections >= 10,
        bonusPoints: 30,
        isHidden: false,
        curriculum: 'junior' as const,
      },
      {
        id: 'ns-family-people-25',
        title: 'Making Them Proud',
        description: 'Write 25 reflections on the For My People track',
        category: 'north-star',
        icon: 'HandHeart',
        condition: (s: GamificationState) => s.northStarCategory === 'family-people' && s.totalReflections >= 25,
        bonusPoints: 50,
        isHidden: false,
        curriculum: 'junior' as const,
      },
      {
        id: 'ns-family-people-40',
        title: 'Role Model',
        description: 'Write 40 reflections on the For My People track',
        category: 'north-star',
        icon: 'Award',
        condition: (s: GamificationState) => s.northStarCategory === 'family-people' && s.totalReflections >= 40,
        bonusPoints: 75,
        isHidden: false,
        curriculum: 'junior' as const,
      },
      {
        id: 'ns-family-people-60',
        title: 'Family Legacy',
        description: 'Write 60 reflections on the For My People track',
        category: 'north-star',
        icon: 'Crown',
        condition: (s: GamificationState) => s.northStarCategory === 'family-people' && s.totalReflections >= 60,
        bonusPoints: 125,
        isHidden: false,
        curriculum: 'junior' as const,
      },
    ],
  },

  'prove-myself-jc': {
    category: 'prove-myself-jc',
    trackTitle: 'Show What I Can Do',
    trackDescription: 'Prove what you\'re actually capable of — to yourself first.',
    milestoneNames: ['First Spark', 'Stacking Wins', 'Beyond Doubt', 'Quietly Lethal', 'Undeniable'],
    progressMetric: 'sessions',
    weeklyChallengeFlavors: [
      'Quiet wins build loud results.',
      'Every session is evidence.',
      'You don\'t have to prove it today — just keep showing up.',
      'Doubters fade. The work stays.',
    ],
    achievements: [
      {
        id: 'ns-prove-jc-start',
        title: 'First Spark',
        description: 'Begin the Show What I Can Do track',
        category: 'north-star',
        icon: 'Flame',
        condition: (s: GamificationState) => s.northStarCategory === 'prove-myself-jc' && s.totalTimetableSessions >= 1,
        bonusPoints: 15,
        isHidden: false,
      curriculum: 'junior' as const,
      },
      {
        id: 'ns-prove-jc-10',
        title: 'Stacking Wins',
        description: 'Log 10 sessions on the Show What I Can Do track',
        category: 'north-star',
        icon: 'TrendingUp',
        condition: (s: GamificationState) => s.northStarCategory === 'prove-myself-jc' && s.totalTimetableSessions >= 10,
        bonusPoints: 30,
        isHidden: false,
      curriculum: 'junior' as const,
      },
      {
        id: 'ns-prove-jc-25',
        title: 'Beyond Doubt',
        description: 'Log 25 sessions on the Show What I Can Do track',
        category: 'north-star',
        icon: 'MicOff',
        condition: (s: GamificationState) => s.northStarCategory === 'prove-myself-jc' && s.totalTimetableSessions >= 25,
        bonusPoints: 50,
        isHidden: false,
      curriculum: 'junior' as const,
      },
      {
        id: 'ns-prove-jc-40',
        title: 'Quietly Lethal',
        description: 'Log 40 sessions on the Show What I Can Do track',
        category: 'north-star',
        icon: 'Target',
        condition: (s: GamificationState) => s.northStarCategory === 'prove-myself-jc' && s.totalTimetableSessions >= 40,
        bonusPoints: 75,
        isHidden: false,
      curriculum: 'junior' as const,
      },
      {
        id: 'ns-prove-jc-60',
        title: 'Undeniable',
        description: 'Log 60 sessions on the Show What I Can Do track',
        category: 'north-star',
        icon: 'Trophy',
        condition: (s: GamificationState) => s.northStarCategory === 'prove-myself-jc' && s.totalTimetableSessions >= 60,
        bonusPoints: 125,
        isHidden: false,
      curriculum: 'junior' as const,
      },
    ],
  },

  'curiosity-craft': {
    category: 'curiosity-craft',
    trackTitle: 'Get Good at Something',
    trackDescription: 'Find the thing you love and go deep on it.',
    milestoneNames: ['Hooked', 'Sharper', 'Mastering It', 'In the Zone', 'Craft Locked In'],
    progressMetric: 'sessions',
    weeklyChallengeFlavors: [
      'Pick the thing you can\'t stop thinking about — go deeper.',
      'Every session adds a tiny bit of mastery.',
      'You\'re building a skill, not just doing homework.',
      'The best part is when it starts to click.',
    ],
    achievements: [
      {
        id: 'ns-curiosity-start',
        title: 'Hooked',
        description: 'Begin the Get Good at Something track',
        category: 'north-star',
        icon: 'Sparkles',
        condition: (s: GamificationState) => s.northStarCategory === 'curiosity-craft' && s.totalTimetableSessions >= 1,
        bonusPoints: 15,
        isHidden: false,
      curriculum: 'junior' as const,
      },
      {
        id: 'ns-curiosity-10',
        title: 'Sharper',
        description: 'Log 10 sessions on the Get Good at Something track',
        category: 'north-star',
        icon: 'Star',
        condition: (s: GamificationState) => s.northStarCategory === 'curiosity-craft' && s.totalTimetableSessions >= 10,
        bonusPoints: 30,
        isHidden: false,
      curriculum: 'junior' as const,
      },
      {
        id: 'ns-curiosity-25',
        title: 'Mastering It',
        description: 'Log 25 sessions on the Get Good at Something track',
        category: 'north-star',
        icon: 'Award',
        condition: (s: GamificationState) => s.northStarCategory === 'curiosity-craft' && s.totalTimetableSessions >= 25,
        bonusPoints: 50,
        isHidden: false,
      curriculum: 'junior' as const,
      },
      {
        id: 'ns-curiosity-40',
        title: 'In the Zone',
        description: 'Log 40 sessions on the Get Good at Something track',
        category: 'north-star',
        icon: 'Zap',
        condition: (s: GamificationState) => s.northStarCategory === 'curiosity-craft' && s.totalTimetableSessions >= 40,
        bonusPoints: 75,
        isHidden: false,
      curriculum: 'junior' as const,
      },
      {
        id: 'ns-curiosity-60',
        title: 'Craft Locked In',
        description: 'Log 60 sessions on the Get Good at Something track',
        category: 'north-star',
        icon: 'Crown',
        condition: (s: GamificationState) => s.northStarCategory === 'curiosity-craft' && s.totalTimetableSessions >= 60,
        bonusPoints: 125,
        isHidden: false,
      curriculum: 'junior' as const,
      },
    ],
  },

  'future-doors': {
    category: 'future-doors',
    trackTitle: 'Keep My Future Open',
    trackDescription: 'Do well now so you have real choices later.',
    milestoneNames: ['First Door', 'More Options', 'Open Future', 'Wide Horizon', 'Wherever You Want'],
    progressMetric: 'modules',
    weeklyChallengeFlavors: [
      'Every module you finish opens another door.',
      'You don\'t need to know the destination yet — just keep moving.',
      'Future-you is paying attention.',
      'Options compound. Keep going.',
    ],
    achievements: [
      {
        id: 'ns-future-start',
        title: 'First Door',
        description: 'Complete your first module on the Keep My Future Open track',
        category: 'north-star',
        icon: 'Compass',
        condition: (s: GamificationState) => s.northStarCategory === 'future-doors' && s.modulesCompleted >= 1,
        bonusPoints: 15,
        isHidden: false,
      curriculum: 'junior' as const,
      },
      {
        id: 'ns-future-5',
        title: 'More Options',
        description: 'Complete 5 modules on the Keep My Future Open track',
        category: 'north-star',
        icon: 'Signpost',
        condition: (s: GamificationState) => s.northStarCategory === 'future-doors' && s.modulesCompleted >= 5,
        bonusPoints: 30,
        isHidden: false,
      curriculum: 'junior' as const,
      },
      {
        id: 'ns-future-15',
        title: 'Open Future',
        description: 'Complete 15 modules on the Keep My Future Open track',
        category: 'north-star',
        icon: 'DoorOpen',
        condition: (s: GamificationState) => s.northStarCategory === 'future-doors' && s.modulesCompleted >= 15,
        bonusPoints: 50,
        isHidden: false,
      curriculum: 'junior' as const,
      },
      {
        id: 'ns-future-30',
        title: 'Wide Horizon',
        description: 'Complete 30 modules on the Keep My Future Open track',
        category: 'north-star',
        icon: 'Mountain',
        condition: (s: GamificationState) => s.northStarCategory === 'future-doors' && s.modulesCompleted >= 30,
        bonusPoints: 75,
        isHidden: false,
      curriculum: 'junior' as const,
      },
      {
        id: 'ns-future-50',
        title: 'Wherever You Want',
        description: 'Complete 50 modules on the Keep My Future Open track',
        category: 'north-star',
        icon: 'Sparkles',
        condition: (s: GamificationState) => s.northStarCategory === 'future-doors' && s.modulesCompleted >= 50,
        bonusPoints: 125,
        isHidden: false,
      curriculum: 'junior' as const,
      },
    ],
  },
};

// Get all North Star achievements (to be added to the main achievements list)
export function getAllNorthStarAchievements(): AchievementDefinition[] {
  const all: AchievementDefinition[] = [];
  for (const track of Object.values(NORTH_STAR_TRACKS)) {
    all.push(...track.achievements);
  }
  return all;
}

// Get current milestone index for a track based on progress
export function getTrackMilestoneIndex(
  track: NorthStarTrack,
  state: GamificationState
): number {
  const value = track.progressMetric === 'modules' ? state.modulesCompleted
    : track.progressMetric === 'sessions' ? state.totalTimetableSessions
    : state.totalReflections;

  // 5 milestones at thresholds: 1, 5, 15, 30, 50
  const thresholds = [1, 5, 15, 30, 50];
  let index = 0;
  for (const t of thresholds) {
    if (value >= t) index++;
  }
  return Math.min(index, 5);
}

// Get rotating weekly challenge text
export function getWeeklyChallengeFlavor(track: NorthStarTrack, weekNumber: number): string {
  return track.weeklyChallengeFlavors[weekNumber % track.weeklyChallengeFlavors.length];
}
