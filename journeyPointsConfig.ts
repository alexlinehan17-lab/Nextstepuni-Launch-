/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type UserProgress } from './types';

// Content is deliberately a light-touch source of Journey Points. Reading
// through a module should support the learning loop, not out-earn a genuine
// timed study session or make the island economy trivial to complete.
export const POINTS = {
  SECTION_COMPLETE: 2,
  MODULE_COMPLETE_BONUS: 6,
  CATEGORY_COMPLETE_BONUS: 20,
  DAILY_STREAK: 10,
  // Reflection tiers (Phase 4)
  REFLECTION_BASIC: 15,
  REFLECTION_THOUGHTFUL: 20,
  REFLECTION_DEEP: 30,
  // Weekly goal bonuses (Phase 2)
  WEEKLY_GOAL_1: 75,
  WEEKLY_GOAL_2: 125,
  WEEKLY_GOAL_3: 250,
} as const;

/**
 * Check if a module is fully completed given the new section unlock.
 */
export function isModuleJustCompleted(newUnlockedSection: number, totalSections: number): boolean {
  return newUnlockedSection >= totalSections;
}

/**
 * Check if all modules in a category are now complete after an update.
 */
export function isCategoryJustCompleted(
  moduleId: string,
  updatedProgress: UserProgress,
  allCourses: { id: string; category: string; sectionsCount: number }[]
): boolean {
  const course = allCourses.find(c => c.id === moduleId);
  if (!course) return false;

  const categoryCourses = allCourses.filter(c => c.category === course.category);
  return categoryCourses.every(c => {
    const p = updatedProgress[c.id];
    return p && p.unlockedSection >= c.sectionsCount;
  });
}
