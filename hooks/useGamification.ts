/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import { doc, getDoc, setDoc, updateDoc, increment } from 'firebase/firestore';
import { db } from '../firebase';
import { type UserProgress, type NorthStar, type IslandState, type StudyReflection } from '../types';
import { type StreakData } from './useStreak';
import { type PointsData } from './usePoints';
import {
  type GamificationState,
  type GamificationFirestoreData,
  type PersonalBests,
  type AchievementDefinition,
  DEFAULT_GAMIFICATION_DATA,
  DEFAULT_PERSONAL_BESTS,
  getRankForPoints,
  getNextRank,
  getRankProgress,
  getWeekStartDate,
  BONUS_FLASH_CHANCE,
} from '../gamificationConfig';
import { ACHIEVEMENTS } from '../achievementData';
import { ALL_COURSES } from '../courseData';
import { type TimetableCompletions } from '../components/subjectData';

interface UseGamificationOptions {
  uid?: string;
  userProgress: UserProgress;
  pointsData: PointsData & { reload: () => void };
  streak: StreakData;
  northStar: NorthStar | null;
}

interface UseGamificationReturn {
  state: GamificationState;
  isLoaded: boolean;
  checkAndUnlockAchievements: () => Promise<AchievementDefinition[]>;
  updateWeeklyGoalProgress: (metric: 'sections' | 'sessions' | 'reflections', incrementBy?: number) => Promise<void>;
  recordPersonalBest: (type: keyof PersonalBests, value: number) => Promise<void>;
  rollBonusFlash: () => boolean;
  reload: () => void;
}

export function useGamification({
  uid,
  userProgress,
  pointsData,
  streak,
  northStar,
}: UseGamificationOptions): UseGamificationReturn {
  const [gamificationData, setGamificationData] = useState<GamificationFirestoreData>({ ...DEFAULT_GAMIFICATION_DATA });
  const [isLoaded, setIsLoaded] = useState(false);
  const [version, setVersion] = useState(0);

  // Separate state for async-loaded counts (fixes state mutation bug)
  const [asyncCounts, setAsyncCounts] = useState({ totalTimetableSessions: 0, totalReflections: 0, journeyMilestones: 0 });

  // Ref to track if achievement check is already in-flight (prevents duplicate checks)
  const checkInFlightRef = useRef(false);

  // Session-level cache of all achievements ever unlocked this session (prevents duplicates from stale Firestore reads)
  const sessionUnlockedRef = useRef<Set<string>>(new Set());

  // Load gamification data from Firestore
  useEffect(() => {
    if (!uid) {
      setGamificationData({ ...DEFAULT_GAMIFICATION_DATA });
      setAsyncCounts({ totalTimetableSessions: 0, totalReflections: 0, journeyMilestones: 0 });
      setIsLoaded(true);
      return;
    }

    let cancelled = false;

    const load = async () => {
      try {
        const progressDoc = await getDoc(doc(db, 'progress', uid));
        if (cancelled) return;
        if (progressDoc.exists()) {
          const data = progressDoc.data();

          // Load gamification sub-document
          const gd = data.gamification as Partial<GamificationFirestoreData> | undefined;
          if (gd) {
            // Seed session cache with already-unlocked achievements
            const loadedIds = gd.unlockedAchievements ?? [];
            for (const id of loadedIds) {
              sessionUnlockedRef.current.add(id);
            }
            setGamificationData({
              unlockedAchievements: loadedIds,
              achievementTimestamps: gd.achievementTimestamps ?? {},
              weeklyGoalProgress: gd.weeklyGoalProgress ?? {},
              weekStartDate: gd.weekStartDate ?? '',
              lastSurpriseDate: gd.lastSurpriseDate ?? '',
              personalBests: { ...DEFAULT_PERSONAL_BESTS, ...(gd.personalBests ?? {}) },
              streakShields: gd.streakShields ?? 0,
              streakShieldUsedDates: gd.streakShieldUsedDates ?? [],
              lastStreakBreakDate: gd.lastStreakBreakDate ?? '',
              recoveryWindowEnd: gd.recoveryWindowEnd ?? '',
            });
          } else {
            setGamificationData({ ...DEFAULT_GAMIFICATION_DATA });
          }

          // Load timetable sessions, reflections, journey milestones
          const completions: TimetableCompletions = data.timetableCompletions ?? {};
          const reflections: StudyReflection[] = data.timetableReflections ?? [];
          const island: IslandState | undefined = data.islandState;

          let totalSessions = 0;
          for (const dayBlocks of Object.values(completions)) {
            if (Array.isArray(dayBlocks)) {
              totalSessions += dayBlocks.length;
            }
          }

          setAsyncCounts({
            totalTimetableSessions: totalSessions,
            totalReflections: reflections.length,
            journeyMilestones: island?.placements?.length ?? 0,
          });
        } else {
          setGamificationData({ ...DEFAULT_GAMIFICATION_DATA });
          setAsyncCounts({ totalTimetableSessions: 0, totalReflections: 0, journeyMilestones: 0 });
        }
      } catch (err) {
        console.error('Failed to load gamification data:', err);
      }
      if (!cancelled) setIsLoaded(true);
    };

    load();
    return () => { cancelled = true; };
  }, [uid, version]);

  // Derive module/section/category counts from existing userProgress
  const { modulesCompleted, sectionsCompleted, categoriesCompleted } = useMemo(() => {
    let modules = 0;
    let sections = 0;
    let categories = 0;

    const categoriesMap: Record<string, { total: number; completed: number }> = {};

    for (const course of ALL_COURSES) {
      const p = userProgress[course.id];
      if (p) {
        sections += p.unlockedSection;
        if (p.unlockedSection >= course.sectionsCount) {
          modules++;
        }
      }
      if (!categoriesMap[course.category]) {
        categoriesMap[course.category] = { total: 0, completed: 0 };
      }
      categoriesMap[course.category].total++;
      if (p && p.unlockedSection >= course.sectionsCount) {
        categoriesMap[course.category].completed++;
      }
    }

    for (const cat of Object.values(categoriesMap)) {
      if (cat.total > 0 && cat.completed >= cat.total) {
        categories++;
      }
    }

    return { modulesCompleted: modules, sectionsCompleted: sections, categoriesCompleted: categories };
  }, [userProgress]);

  // Reset weekly goals if week has changed
  const currentWeekStart = getWeekStartDate();
  const weeklyGoalProgress = useMemo(() => {
    if (gamificationData.weekStartDate !== currentWeekStart) {
      return {}; // New week, reset progress
    }
    return gamificationData.weeklyGoalProgress;
  }, [gamificationData.weeklyGoalProgress, gamificationData.weekStartDate, currentWeekStart]);

  // Build the full GamificationState (immutable, never mutated)
  const state: GamificationState = useMemo(() => {
    const totalPointsEarned = pointsData.totalEarned;
    const currentRank = getRankForPoints(totalPointsEarned);
    const nextRank = getNextRank(currentRank);
    const rankProgress = getRankProgress(totalPointsEarned, currentRank, nextRank);

    // Compute streak shields: earn 1 at 7-day streak, another at 14-day (max 2)
    let streakShields = gamificationData.streakShields;
    if (streak.longestStreak >= 14 && streakShields < 2) {
      streakShields = 2;
    } else if (streak.longestStreak >= 7 && streakShields < 1) {
      streakShields = 1;
    }

    return {
      totalPointsEarned,
      currentStreak: streak.currentStreak,
      longestStreak: streak.longestStreak,
      modulesCompleted,
      sectionsCompleted,
      categoriesCompleted,
      totalReflections: asyncCounts.totalReflections,
      totalTimetableSessions: asyncCounts.totalTimetableSessions,
      northStarCategory: northStar?.category ?? null,
      currentRank,
      nextRank,
      rankProgress,
      unlockedAchievements: gamificationData.unlockedAchievements,
      achievementTimestamps: gamificationData.achievementTimestamps,
      weeklyGoalProgress,
      weekStartDate: currentWeekStart,
      personalBests: gamificationData.personalBests,
      journeyMilestones: asyncCounts.journeyMilestones,
      streakShields,
    };
  }, [
    pointsData.totalEarned,
    streak,
    modulesCompleted,
    sectionsCompleted,
    categoriesCompleted,
    asyncCounts,
    northStar,
    gamificationData,
    weeklyGoalProgress,
    currentWeekStart,
  ]);

  // Save gamification data to Firestore
  const saveGamificationData = useCallback(async (data: Partial<GamificationFirestoreData>) => {
    if (!uid) return;
    try {
      const merged = { ...gamificationData, ...data };
      await setDoc(doc(db, 'progress', uid), { gamification: merged }, { merge: true });
      setGamificationData(merged);
    } catch (err) {
      console.error('Failed to save gamification data:', err);
    }
  }, [uid, gamificationData]);

  // Check and unlock achievements (with in-flight guard to prevent duplicates)
  const checkAndUnlockAchievements = useCallback(async (): Promise<AchievementDefinition[]> => {
    if (checkInFlightRef.current) return [];
    checkInFlightRef.current = true;

    try {
      // Re-read current unlocked list from Firestore to avoid stale state
      let currentUnlockedIds: string[] = gamificationData.unlockedAchievements;
      let currentTimestamps: Record<string, number> = { ...gamificationData.achievementTimestamps };

      if (uid) {
        try {
          const freshDoc = await getDoc(doc(db, 'progress', uid));
          if (freshDoc.exists()) {
            const freshData = freshDoc.data();
            const freshGd = freshData.gamification as Partial<GamificationFirestoreData> | undefined;
            if (freshGd?.unlockedAchievements) {
              currentUnlockedIds = freshGd.unlockedAchievements;
              currentTimestamps = freshGd.achievementTimestamps ?? {};
            }
          }
        } catch {
          // Fall back to local state
        }
      }

      // Merge Firestore data with session cache to handle stale reads
      const currentUnlocked = new Set([...currentUnlockedIds, ...sessionUnlockedRef.current]);
      const newlyUnlocked: AchievementDefinition[] = [];

      for (const achievement of ACHIEVEMENTS) {
        if (currentUnlocked.has(achievement.id)) continue;
        try {
          if (achievement.condition(state)) {
            newlyUnlocked.push(achievement);
            currentUnlocked.add(achievement.id);
            sessionUnlockedRef.current.add(achievement.id);
          }
        } catch {
          // Skip achievements that fail to evaluate
        }
      }

      if (newlyUnlocked.length > 0) {
        const timestamps = { ...currentTimestamps };
        for (const a of newlyUnlocked) {
          timestamps[a.id] = Date.now();
        }

        const updatedList = Array.from(currentUnlocked);

        // Save achievements to Firestore
        await saveGamificationData({
          unlockedAchievements: updatedList,
          achievementTimestamps: timestamps,
        });

        // Award bonus points for new achievements
        const totalBonus = newlyUnlocked.reduce((sum, a) => sum + a.bonusPoints, 0);
        if (totalBonus > 0 && uid) {
          try {
            await updateDoc(doc(db, 'progress', uid), {
              'pointsData.totalEarned': increment(totalBonus),
            });
            pointsData.reload();
          } catch (err) {
            console.error('Failed to award achievement bonus:', err);
          }
        }
      }

      return newlyUnlocked;
    } finally {
      checkInFlightRef.current = false;
    }
  }, [state, gamificationData, saveGamificationData, uid, pointsData]);

  // Update weekly goal progress
  const updateWeeklyGoalProgress = useCallback(async (metric: 'sections' | 'sessions' | 'reflections', incrementBy = 1) => {
    const currentWeek = getWeekStartDate();
    const isNewWeek = gamificationData.weekStartDate !== currentWeek;

    const progress = isNewWeek ? {} : { ...gamificationData.weeklyGoalProgress };
    progress[metric] = (progress[metric] ?? 0) + incrementBy;

    await saveGamificationData({
      weeklyGoalProgress: progress,
      weekStartDate: currentWeek,
    });
  }, [gamificationData, saveGamificationData]);

  // Record personal best
  const recordPersonalBest = useCallback(async (type: keyof PersonalBests, value: number) => {
    const current = gamificationData.personalBests[type] ?? 0;
    if (value > current) {
      await saveGamificationData({
        personalBests: { ...gamificationData.personalBests, [type]: value },
      });
    }
  }, [gamificationData, saveGamificationData]);

  // Roll for bonus flash (15% chance)
  const rollBonusFlash = useCallback((): boolean => {
    return Math.random() < BONUS_FLASH_CHANCE;
  }, []);

  const reload = useCallback(() => {
    setVersion(v => v + 1);
  }, []);

  return {
    state,
    isLoaded,
    checkAndUnlockAchievements,
    updateWeeklyGoalProgress,
    recordPersonalBest,
    rollBonusFlash,
    reload,
  };
}
