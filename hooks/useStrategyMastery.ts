/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback } from 'react';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { type UserProgress, type StrategyMasteryMap, type StrategyMasteryRecord, type MasteryTier } from '../types';
import { type CourseData } from '../components/Library';
import { STRATEGY_REGISTRY, type StudySessionRecord } from '../utils/strategyRegistry';

export function useStrategyMastery(
  uid: string | undefined,
  userProgress: UserProgress,
  allCourses: CourseData[],
): { masteryMap: StrategyMasteryMap; isLoaded: boolean; recompute: () => Promise<void> } {
  const [masteryMap, setMasteryMap] = useState<StrategyMasteryMap>({});
  const [isLoaded, setIsLoaded] = useState(false);

  const compute = useCallback(async () => {
    if (!uid) {
      setMasteryMap({});
      setIsLoaded(true);
      return;
    }

    try {
      const progressDoc = await getDoc(doc(db, 'progress', uid));
      const data = progressDoc.exists() ? progressDoc.data() : {};
      const sessions: StudySessionRecord[] = data.studySessions || [];

      const map: StrategyMasteryMap = {};

      for (const strategy of STRATEGY_REGISTRY) {
        const { moduleId } = strategy;

        // Check if module is completed
        const course = allCourses.find(c => c.id === moduleId);
        const progress = userProgress[moduleId];
        const isCompleted = course && progress && progress.unlockedSection >= course.sectionsCount;

        if (!isCompleted) {
          map[moduleId] = { tier: 'none', sessionCount: 0, subjectsSeen: [] };
          continue;
        }

        // Filter sessions where this strategy's prompt was shown
        const relevantSessions = sessions.filter(
          s => s.strategiesShown && s.strategiesShown.includes(moduleId)
        );

        const sessionCount = relevantSessions.length;
        const subjectsSeen = [...new Set(relevantSessions.map(s => s.subject))];

        // Determine tier
        let tier: MasteryTier = 'learned';
        let appliedAt: string | undefined;
        let habitualAt: string | undefined;

        if (sessionCount >= 3) {
          tier = 'practiced';
        }

        if (subjectsSeen.length >= 2) {
          tier = 'applied';
          // Find when second subject first appeared
          const subjectOrder: string[] = [];
          for (const s of relevantSessions) {
            if (!subjectOrder.includes(s.subject)) {
              subjectOrder.push(s.subject);
              if (subjectOrder.length === 2) {
                appliedAt = s.date;
                break;
              }
            }
          }
        }

        // Habitual: 3+ sessions/week for 2 consecutive weeks (only if Applied)
        if (tier === 'applied') {
          const habitualDate = checkHabitual(relevantSessions);
          if (habitualDate) {
            tier = 'habitual';
            habitualAt = habitualDate;
          }
        }

        map[moduleId] = {
          tier,
          learnedAt: relevantSessions.length > 0 ? relevantSessions[0].date : undefined,
          appliedAt,
          habitualAt,
          sessionCount,
          subjectsSeen,
        };
      }

      setMasteryMap(map);
      setIsLoaded(true);

      // Persist to Firestore
      await setDoc(doc(db, 'progress', uid), { strategyMastery: map }, { merge: true });
    } catch (err) {
      console.error('Failed to compute strategy mastery:');
      setIsLoaded(true);
    }
  }, [uid, userProgress, allCourses]);

  useEffect(() => {
    compute();
  }, [compute]);

  return { masteryMap, isLoaded, recompute: compute };
}

/**
 * Check if there are 2 consecutive weeks with 3+ sessions each.
 * Returns the date string of when habitual was achieved, or null.
 */
function checkHabitual(sessions: StudySessionRecord[]): string | null {
  if (sessions.length < 6) return null;

  // Group sessions by ISO week (Mon-Sun)
  const weekMap: Record<string, string[]> = {};
  for (const s of sessions) {
    const d = new Date(s.date);
    const weekKey = getISOWeekKey(d);
    if (!weekMap[weekKey]) weekMap[weekKey] = [];
    weekMap[weekKey].push(s.date);
  }

  // Sort week keys chronologically
  const weekKeys = Object.keys(weekMap).sort();

  for (let i = 1; i < weekKeys.length; i++) {
    const prevWeek = weekKeys[i - 1];
    const currWeek = weekKeys[i];

    // Check consecutive weeks
    if (!areConsecutiveWeeks(prevWeek, currWeek)) continue;

    if (weekMap[prevWeek].length >= 3 && weekMap[currWeek].length >= 3) {
      // Return the last date of the second qualifying week
      const dates = weekMap[currWeek].sort();
      return dates[dates.length - 1];
    }
  }

  return null;
}

function getISOWeekKey(date: Date): string {
  // Get the Thursday of the week to determine ISO week number
  const d = new Date(date.getTime());
  d.setDate(d.getDate() + 3 - ((d.getDay() + 6) % 7));
  const yearStart = new Date(d.getFullYear(), 0, 1);
  const weekNum = Math.ceil((((d.getTime() - yearStart.getTime()) / 86400000) + 1) / 7);
  return `${d.getFullYear()}-W${String(weekNum).padStart(2, '0')}`;
}

function areConsecutiveWeeks(a: string, b: string): boolean {
  const [yearA, weekA] = a.split('-W').map(Number);
  const [yearB, weekB] = b.split('-W').map(Number);
  if (yearA === yearB) return weekB === weekA + 1;
  // Handle year boundary (week 52/53 → week 1)
  if (yearB === yearA + 1 && weekB === 1 && weekA >= 52) return true;
  return false;
}
