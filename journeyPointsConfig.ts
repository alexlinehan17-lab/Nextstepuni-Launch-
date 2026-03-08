/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { ALL_COURSES } from './courseData';
import { UserProgress } from './types';

// Points earned for completing content
export const POINTS = {
  SECTION_COMPLETE: 15,
  MODULE_COMPLETE_BONUS: 50,
  CATEGORY_COMPLETE_BONUS: 200,
  DAILY_STREAK: 10,
  // Reflection tiers (Phase 4)
  REFLECTION_BASIC: 10,
  REFLECTION_THOUGHTFUL: 15,
  REFLECTION_DEEP: 20,
  // Weekly goal bonuses (Phase 2)
  WEEKLY_GOAL_1: 50,
  WEEKLY_GOAL_2: 100,
  WEEKLY_GOAL_3: 200,
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
