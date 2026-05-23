/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type NorthStarCategory, type NorthStarVisionCard } from './types';
import { type CurriculumLevel } from './utils/authUtils';

export interface NorthStarCategoryOption {
  id: NorthStarCategory;
  label: string;
  description: string;
  icon: string;
  /** Phase 5: which curriculum level(s) this theme is shown to during NS
   *  onboarding. Lookups by ID (e.g., in NorthStarCallout) still find any
   *  category regardless of curriculum — the field only gates the picker. */
  curriculum: 'junior' | 'senior' | 'both';
}

export const NORTH_STAR_CATEGORIES: NorthStarCategoryOption[] = [
  // ─── Senior cycle (6) ────────────────────────────────────────────────
  { id: 'independence', label: 'My Own Path', description: 'Earn my own money, build my own life', icon: 'Wallet', curriculum: 'senior' },
  { id: 'family-community', label: 'For My People', description: 'Make my family proud, give back', icon: 'Heart', curriculum: 'senior' },
  { id: 'career-craft', label: 'A Career I Love', description: 'Get into a job or trade I\'m passionate about', icon: 'Wrench', curriculum: 'senior' },
  { id: 'college-learning', label: 'Keep Learning', description: 'Get into college, PLC, or apprenticeship', icon: 'GraduationCap', curriculum: 'senior' },
  { id: 'prove-myself', label: 'Prove Them Wrong', description: 'Show people what I\'m capable of', icon: 'Flame', curriculum: 'senior' },
  { id: 'options-freedom', label: 'Keep My Options Open', description: 'Get enough points so I have choices', icon: 'DoorOpen', curriculum: 'senior' },

  // ─── Junior cycle (4) — Phase 5 ──────────────────────────────────────
  // Tone: peer-from-6th-year, ages 12–15 reading level, no LC framing.
  { id: 'family-people', label: 'For my people', description: 'I want to make my family proud. I want to show the people who believe in me that they were right to.', icon: 'Heart', curriculum: 'junior' },
  { id: 'prove-myself-jc', label: 'Show what I can do', description: 'Maybe a teacher wrote me off. Maybe someone in class thinks they\'re smarter. I want to show what I\'m actually capable of.', icon: 'Flame', curriculum: 'junior' },
  { id: 'curiosity-craft', label: 'Get good at something', description: 'There\'s a subject or a thing I love, and I want to get really good at it. Not because I have to — because I want to.', icon: 'Sparkles', curriculum: 'junior' },
  { id: 'future-doors', label: 'Keep my future open', description: 'I don\'t know what I want to do yet, and that\'s fine. I want to keep my options open by doing well now.', icon: 'Compass', curriculum: 'junior' },
];

export const VISION_CARDS: NorthStarVisionCard[] = [
  // ─── Senior cycle (18) ───────────────────────────────────────────────
  // Independence
  { id: 'first-paycheck', label: 'My First Real Paycheck', icon: 'Banknote', category: 'independence', curriculum: 'senior' },
  { id: 'own-car', label: 'My Own Car', icon: 'Car', category: 'independence', curriculum: 'senior' },
  { id: 'own-place', label: 'My Own Place', icon: 'Home', category: 'independence', curriculum: 'senior' },
  // Family
  { id: 'family-proud', label: 'Making My Family Proud', icon: 'Heart', category: 'family-community', curriculum: 'senior' },
  { id: 'role-model', label: 'Being a Role Model', icon: 'Users', category: 'family-community', curriculum: 'senior' },
  { id: 'giving-back', label: 'Giving Back to My Area', icon: 'HandHeart', category: 'family-community', curriculum: 'senior' },
  // Career
  { id: 'dream-job', label: 'Landing My Dream Job', icon: 'Briefcase', category: 'career-craft', curriculum: 'senior' },
  { id: 'own-thing', label: 'Starting My Own Thing', icon: 'Rocket', category: 'career-craft', curriculum: 'senior' },
  { id: 'skilled-trade', label: 'Mastering a Skilled Trade', icon: 'Wrench', category: 'career-craft', curriculum: 'senior' },
  // College
  { id: 'campus', label: 'Walking Onto Campus', icon: 'GraduationCap', category: 'college-learning', curriculum: 'senior' },
  { id: 'scholarship', label: 'Earning a Scholarship', icon: 'Award', category: 'college-learning', curriculum: 'senior' },
  { id: 'new-people', label: 'Meeting New People', icon: 'UserPlus', category: 'college-learning', curriculum: 'senior' },
  // Prove Myself
  { id: 'results-day', label: 'Results Day Feeling', icon: 'PartyPopper', category: 'prove-myself', curriculum: 'senior' },
  { id: 'beating-odds', label: 'Beating the Odds', icon: 'TrendingUp', category: 'prove-myself', curriculum: 'senior' },
  { id: 'silence-doubters', label: 'Silencing the Doubters', icon: 'MicOff', category: 'prove-myself', curriculum: 'senior' },
  // Options
  { id: 'real-choices', label: 'Having Real Choices', icon: 'Signpost', category: 'options-freedom', curriculum: 'senior' },
  { id: 'see-world', label: 'Seeing the World', icon: 'Plane', category: 'options-freedom', curriculum: 'senior' },
  { id: 'freedom-no', label: 'Freedom to Say No', icon: 'DoorOpen', category: 'options-freedom', curriculum: 'senior' },

  // ─── Junior cycle (12) — Phase 5 ─────────────────────────────────────
  // family-people
  { id: 'jc-family-proud', label: 'Making my family proud', icon: 'Heart', category: 'family-people', curriculum: 'junior' },
  { id: 'jc-role-model', label: 'Being a role model', icon: 'Users', category: 'family-people', curriculum: 'junior' },
  { id: 'jc-giving-back', label: 'Giving back to my area', icon: 'HandHeart', category: 'family-people', curriculum: 'junior' },
  // prove-myself-jc
  { id: 'jc-beating-odds', label: 'Beating the odds', icon: 'TrendingUp', category: 'prove-myself-jc', curriculum: 'junior' },
  { id: 'jc-silence-doubters', label: 'Silencing the doubters', icon: 'MicOff', category: 'prove-myself-jc', curriculum: 'junior' },
  { id: 'jc-results-day', label: 'Results day feeling', icon: 'PartyPopper', category: 'prove-myself-jc', curriculum: 'junior' },
  // curiosity-craft
  { id: 'jc-really-good', label: 'Getting really good at one thing', icon: 'Star', category: 'curiosity-craft', curriculum: 'junior' },
  { id: 'jc-solve-hard', label: 'Solving something hard', icon: 'Puzzle', category: 'curiosity-craft', curriculum: 'junior' },
  { id: 'jc-mastering-skill', label: 'Mastering a skill', icon: 'Award', category: 'curiosity-craft', curriculum: 'junior' },
  // future-doors
  { id: 'jc-subject-choice', label: 'Choosing subjects that suit me', icon: 'BookOpen', category: 'future-doors', curriculum: 'junior' },
  { id: 'jc-real-choices', label: 'Having real choices', icon: 'Signpost', category: 'future-doors', curriculum: 'junior' },
  { id: 'jc-try-new', label: 'Trying new things', icon: 'Compass', category: 'future-doors', curriculum: 'junior' },
];

export const CATEGORY_COLORS: Record<NorthStarCategory, { bg: string; border: string; text: string; selectedBg: string; selectedBorder: string; iconBg: string }> = {
  'independence': { bg: 'bg-stone-50 dark:bg-stone-900/20', border: 'border-stone-200 dark:border-stone-800/40', text: 'text-stone-700 dark:text-stone-300', selectedBg: 'bg-stone-100 dark:bg-stone-900/40', selectedBorder: 'border-stone-400 dark:border-stone-500', iconBg: 'bg-stone-100 dark:bg-stone-900/30' },
  'family-community': { bg: 'bg-rose-50 dark:bg-rose-900/20', border: 'border-rose-200 dark:border-rose-800/40', text: 'text-rose-700 dark:text-rose-300', selectedBg: 'bg-rose-100 dark:bg-rose-900/40', selectedBorder: 'border-rose-400 dark:border-rose-500', iconBg: 'bg-rose-100 dark:bg-rose-900/30' },
  'career-craft': { bg: 'bg-amber-50 dark:bg-amber-900/20', border: 'border-amber-200 dark:border-amber-800/40', text: 'text-amber-700 dark:text-amber-300', selectedBg: 'bg-amber-100 dark:bg-amber-900/40', selectedBorder: 'border-amber-400 dark:border-amber-500', iconBg: 'bg-amber-100 dark:bg-amber-900/30' },
  'college-learning': { bg: 'bg-blue-50 dark:bg-blue-900/20', border: 'border-blue-200 dark:border-blue-800/40', text: 'text-blue-700 dark:text-blue-300', selectedBg: 'bg-blue-100 dark:bg-blue-900/40', selectedBorder: 'border-blue-400 dark:border-blue-500', iconBg: 'bg-blue-100 dark:bg-blue-900/30' },
  'prove-myself': { bg: 'bg-orange-50 dark:bg-orange-900/20', border: 'border-orange-200 dark:border-orange-800/40', text: 'text-orange-700 dark:text-orange-300', selectedBg: 'bg-orange-100 dark:bg-orange-900/40', selectedBorder: 'border-orange-400 dark:border-orange-500', iconBg: 'bg-orange-100 dark:bg-orange-900/30' },
  'options-freedom': { bg: 'bg-teal-50 dark:bg-teal-900/20', border: 'border-teal-200 dark:border-teal-800/40', text: 'text-teal-700 dark:text-teal-300', selectedBg: 'bg-teal-100 dark:bg-teal-900/40', selectedBorder: 'border-teal-400 dark:border-teal-500', iconBg: 'bg-teal-100 dark:bg-teal-900/30' },

  // ─── Junior cycle (4) — Phase 5 ──────────────────────────────────────
  // Reuse-by-concept for the two overlapping themes (rose for family,
  // orange for prove-myself). Fresh hues for the two JC-bespoke themes:
  // violet for curiosity-craft, emerald for future-doors.
  'family-people': { bg: 'bg-rose-50 dark:bg-rose-900/20', border: 'border-rose-200 dark:border-rose-800/40', text: 'text-rose-700 dark:text-rose-300', selectedBg: 'bg-rose-100 dark:bg-rose-900/40', selectedBorder: 'border-rose-400 dark:border-rose-500', iconBg: 'bg-rose-100 dark:bg-rose-900/30' },
  'prove-myself-jc': { bg: 'bg-orange-50 dark:bg-orange-900/20', border: 'border-orange-200 dark:border-orange-800/40', text: 'text-orange-700 dark:text-orange-300', selectedBg: 'bg-orange-100 dark:bg-orange-900/40', selectedBorder: 'border-orange-400 dark:border-orange-500', iconBg: 'bg-orange-100 dark:bg-orange-900/30' },
  'curiosity-craft': { bg: 'bg-violet-50 dark:bg-violet-900/20', border: 'border-violet-200 dark:border-violet-800/40', text: 'text-violet-700 dark:text-violet-300', selectedBg: 'bg-violet-100 dark:bg-violet-900/40', selectedBorder: 'border-violet-400 dark:border-violet-500', iconBg: 'bg-violet-100 dark:bg-violet-900/30' },
  'future-doors': { bg: 'bg-emerald-50 dark:bg-emerald-900/20', border: 'border-emerald-200 dark:border-emerald-800/40', text: 'text-emerald-700 dark:text-emerald-300', selectedBg: 'bg-emerald-100 dark:bg-emerald-900/40', selectedBorder: 'border-emerald-400 dark:border-emerald-500', iconBg: 'bg-emerald-100 dark:bg-emerald-900/30' },
};

export const CATEGORY_PROMPTS: Record<NorthStarCategory, string> = {
  'independence': 'When you picture building your own independent life, what does that look like?',
  'family-community': 'When you picture making your family proud, what does that look like?',
  'career-craft': 'When you imagine doing work you love every day, what does that look like?',
  'college-learning': 'When you picture yourself continuing to learn and grow, what does that look like?',
  'prove-myself': 'When you imagine proving everyone wrong, what does that moment feel like?',
  'options-freedom': 'When you picture having real choices in life, what does that freedom look like?',

  // Junior cycle — Phase 5 (lighter, more concrete prompts for ages 12–15)
  'family-people': 'When you imagine making your family proud of you, what does that look like?',
  'prove-myself-jc': 'When you imagine showing what you\'re actually capable of, what does that feel like?',
  'curiosity-craft': 'When you imagine being really good at something you love, what does that look like?',
  'future-doors': 'When you picture having real options open to you later, what does that look like?',
};

// ─── Curriculum-aware helpers (Phase 5) ────────────────────────────────────

/** Themes to show in the NS picker for the given curriculum level. */
export function getActiveCategories(level: CurriculumLevel): NorthStarCategoryOption[] {
  return NORTH_STAR_CATEGORIES.filter(c => c.curriculum === level || c.curriculum === 'both');
}

/** Vision cards available for the given curriculum level. */
export function getVisionCardsForLevel(level: CurriculumLevel): NorthStarVisionCard[] {
  return VISION_CARDS.filter(c => c.curriculum === level || c.curriculum === 'both');
}

export interface NorthStarCalloutPlacement {
  moduleId: string;
  section: number;
  message: string;
}

export const COMPACT_CALLOUT_PLACEMENTS: NorthStarCalloutPlacement[] = [
  { moduleId: 'agency-protocol', section: 3, message: "You chose to be a driver. Here's your reason why." },
  { moduleId: 'best-possible-self-protocol', section: 1, message: "Your North Star is the 'W' in WOOP — the Wish." },
  { moduleId: 'linking-study-future-goals-protocol', section: 0, message: "You've already started connecting study to your future." },
  { moduleId: 'hope-protocol', section: 3, message: "Hope isn't wishful thinking. You've already defined yours." },
  { moduleId: 'implementation-protocol', section: 2, message: "The best plans connect to something you care about." },
  { moduleId: 'procrastination-protocol', section: 4, message: "When work feels pointless, remember what it's building." },
  { moduleId: 'leaving-cert-strategy-protocol', section: 0, message: "Every point is a step closer to your North Star." },
  { moduleId: 'game-day-protocol', section: 5, message: "In that exam hall, this is what you're doing it for." },
  { moduleId: 'strategic-advantage-protocol', section: 2, message: "Your story, your goals, your advantage." },
  { moduleId: 'self-efficacy-protocol', section: 3, message: "Believing in yourself starts with knowing what you believe in." },
];
