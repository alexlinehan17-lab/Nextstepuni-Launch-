/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { NorthStarCategory, NorthStarVisionCard } from './types';

export interface NorthStarCategoryOption {
  id: NorthStarCategory;
  label: string;
  description: string;
  icon: string;
}

export const NORTH_STAR_CATEGORIES: NorthStarCategoryOption[] = [
  { id: 'independence', label: 'My Own Path', description: 'Earn my own money, build my own life', icon: 'Wallet' },
  { id: 'family-community', label: 'For My People', description: 'Make my family proud, give back', icon: 'Heart' },
  { id: 'career-craft', label: 'A Career I Love', description: 'Get into a job or trade I\'m passionate about', icon: 'Wrench' },
  { id: 'college-learning', label: 'Keep Learning', description: 'Get into college, PLC, or apprenticeship', icon: 'GraduationCap' },
  { id: 'prove-myself', label: 'Prove Them Wrong', description: 'Show people what I\'m capable of', icon: 'Flame' },
  { id: 'options-freedom', label: 'Keep My Options Open', description: 'Get enough points so I have choices', icon: 'DoorOpen' },
];

export const VISION_CARDS: NorthStarVisionCard[] = [
  // Independence
  { id: 'first-paycheck', label: 'My First Real Paycheck', icon: 'Banknote', category: 'independence' },
  { id: 'own-car', label: 'My Own Car', icon: 'Car', category: 'independence' },
  { id: 'own-place', label: 'My Own Place', icon: 'Home', category: 'independence' },
  // Family
  { id: 'family-proud', label: 'Making My Family Proud', icon: 'Heart', category: 'family-community' },
  { id: 'role-model', label: 'Being a Role Model', icon: 'Users', category: 'family-community' },
  { id: 'giving-back', label: 'Giving Back to My Area', icon: 'HandHeart', category: 'family-community' },
  // Career
  { id: 'dream-job', label: 'Landing My Dream Job', icon: 'Briefcase', category: 'career-craft' },
  { id: 'own-thing', label: 'Starting My Own Thing', icon: 'Rocket', category: 'career-craft' },
  { id: 'skilled-trade', label: 'Mastering a Skilled Trade', icon: 'Wrench', category: 'career-craft' },
  // College
  { id: 'campus', label: 'Walking Onto Campus', icon: 'GraduationCap', category: 'college-learning' },
  { id: 'scholarship', label: 'Earning a Scholarship', icon: 'Award', category: 'college-learning' },
  { id: 'new-people', label: 'Meeting New People', icon: 'UserPlus', category: 'college-learning' },
  // Prove Myself
  { id: 'results-day', label: 'Results Day Feeling', icon: 'PartyPopper', category: 'prove-myself' },
  { id: 'beating-odds', label: 'Beating the Odds', icon: 'TrendingUp', category: 'prove-myself' },
  { id: 'silence-doubters', label: 'Silencing the Doubters', icon: 'MicOff', category: 'prove-myself' },
  // Options
  { id: 'real-choices', label: 'Having Real Choices', icon: 'Signpost', category: 'options-freedom' },
  { id: 'see-world', label: 'Seeing the World', icon: 'Plane', category: 'options-freedom' },
  { id: 'freedom-no', label: 'Freedom to Say No', icon: 'DoorOpen', category: 'options-freedom' },
];

export const CATEGORY_COLORS: Record<NorthStarCategory, { bg: string; border: string; text: string; selectedBg: string; selectedBorder: string; iconBg: string }> = {
  'independence': { bg: 'bg-stone-50 dark:bg-stone-900/20', border: 'border-stone-200 dark:border-stone-800/40', text: 'text-stone-700 dark:text-stone-300', selectedBg: 'bg-stone-100 dark:bg-stone-900/40', selectedBorder: 'border-stone-400 dark:border-stone-500', iconBg: 'bg-stone-100 dark:bg-stone-900/30' },
  'family-community': { bg: 'bg-rose-50 dark:bg-rose-900/20', border: 'border-rose-200 dark:border-rose-800/40', text: 'text-rose-700 dark:text-rose-300', selectedBg: 'bg-rose-100 dark:bg-rose-900/40', selectedBorder: 'border-rose-400 dark:border-rose-500', iconBg: 'bg-rose-100 dark:bg-rose-900/30' },
  'career-craft': { bg: 'bg-amber-50 dark:bg-amber-900/20', border: 'border-amber-200 dark:border-amber-800/40', text: 'text-amber-700 dark:text-amber-300', selectedBg: 'bg-amber-100 dark:bg-amber-900/40', selectedBorder: 'border-amber-400 dark:border-amber-500', iconBg: 'bg-amber-100 dark:bg-amber-900/30' },
  'college-learning': { bg: 'bg-blue-50 dark:bg-blue-900/20', border: 'border-blue-200 dark:border-blue-800/40', text: 'text-blue-700 dark:text-blue-300', selectedBg: 'bg-blue-100 dark:bg-blue-900/40', selectedBorder: 'border-blue-400 dark:border-blue-500', iconBg: 'bg-blue-100 dark:bg-blue-900/30' },
  'prove-myself': { bg: 'bg-orange-50 dark:bg-orange-900/20', border: 'border-orange-200 dark:border-orange-800/40', text: 'text-orange-700 dark:text-orange-300', selectedBg: 'bg-orange-100 dark:bg-orange-900/40', selectedBorder: 'border-orange-400 dark:border-orange-500', iconBg: 'bg-orange-100 dark:bg-orange-900/30' },
  'options-freedom': { bg: 'bg-teal-50 dark:bg-teal-900/20', border: 'border-teal-200 dark:border-teal-800/40', text: 'text-teal-700 dark:text-teal-300', selectedBg: 'bg-teal-100 dark:bg-teal-900/40', selectedBorder: 'border-teal-400 dark:border-teal-500', iconBg: 'bg-teal-100 dark:bg-teal-900/30' },
};

export const CATEGORY_PROMPTS: Record<NorthStarCategory, string> = {
  'independence': 'When you picture building your own independent life, what does that look like?',
  'family-community': 'When you picture making your family proud, what does that look like?',
  'career-craft': 'When you imagine doing work you love every day, what does that look like?',
  'college-learning': 'When you picture yourself continuing to learn and grow, what does that look like?',
  'prove-myself': 'When you imagine proving everyone wrong, what does that moment feel like?',
  'options-freedom': 'When you picture having real choices in life, what does that freedom look like?',
};

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
