/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useMemo } from 'react';
import { UserProgress } from '../types';
import { CategoryType } from '../components/KnowledgeTree';

interface CourseInfo {
  id: string;
  title: string;
  category: CategoryType;
  sectionsCount: number;
}

export interface FocusRecommendation {
  moduleId: string;
  title: string;
  category: CategoryType;
  reason: 'in-progress' | 'not-started' | 'all-complete';
}

export function useTodaysFocus(
  userProgress: UserProgress,
  allCourses: CourseInfo[]
): { recommendation: FocusRecommendation | null } {
  const recommendation = useMemo(() => {
    // 1. Find in-progress modules (started but not complete)
    const inProgress = allCourses.filter(course => {
      const progress = userProgress[course.id];
      if (!progress) return false;
      return progress.unlockedSection > 0 && progress.unlockedSection < course.sectionsCount;
    });

    if (inProgress.length > 0) {
      // Pick the one with least progress (most benefit from returning)
      const sorted = [...inProgress].sort((a, b) => {
        const pa = userProgress[a.id]?.unlockedSection || 0;
        const pb = userProgress[b.id]?.unlockedSection || 0;
        return pa - pb;
      });
      const pick = sorted[0];
      return {
        moduleId: pick.id,
        title: pick.title,
        category: pick.category,
        reason: 'in-progress' as const,
      };
    }

    // 2. First not-yet-started module
    const notStarted = allCourses.find(course => {
      const progress = userProgress[course.id];
      return !progress || progress.unlockedSection === 0;
    });

    if (notStarted) {
      return {
        moduleId: notStarted.id,
        title: notStarted.title,
        category: notStarted.category,
        reason: 'not-started' as const,
      };
    }

    // 3. All complete
    return {
      moduleId: '',
      title: '',
      category: 'architecture-mindset' as CategoryType,
      reason: 'all-complete' as const,
    };
  }, [userProgress, allCourses]);

  return { recommendation };
}
