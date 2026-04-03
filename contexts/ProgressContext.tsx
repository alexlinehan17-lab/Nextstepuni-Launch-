/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { createContext, useContext, useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { db } from '../firebase';
import { doc, setDoc, updateDoc, increment } from 'firebase/firestore';
import { type ModuleProgress, type UserProgress, type NorthStar } from '../types';
import { type StudentSubjectProfile } from '../components/subjectData';
import { useStreak, type StreakData } from '../hooks/useStreak';
import { usePoints } from '../hooks/usePoints';
import { useAuth } from './AuthContext';

// ─── Types ──────────────────────────────────────────────────

interface ProgressContextValue {
  // Core progress
  userProgress: UserProgress;
  setUserProgress: React.Dispatch<React.SetStateAction<UserProgress>>;

  // Student profile
  studentProfile: StudentSubjectProfile | null;
  setStudentProfile: (profile: StudentSubjectProfile | null) => void;

  // North Star
  northStar: NorthStar | null;
  setNorthStar: (ns: NorthStar | null) => void;

  // Timetable
  timetableCompletions: Record<string, string[]>;
  setTimetableCompletions: React.Dispatch<React.SetStateAction<Record<string, string[]>>>;

  // Points & streak
  pointsData: ReturnType<typeof usePoints>;
  streak: StreakData;

  // Cosmetic unlocks
  unlockedAvatarSeeds: string[];
  setUnlockedAvatarSeeds: (seeds: string[]) => void;
  unlockedThemes: string[];
  setUnlockedThemes: (themes: string[]) => void;
  unlockedCardStyles: string[];
  setUnlockedCardStyles: (styles: string[]) => void;

  // Dismissed guides
  dismissedGuides: Record<string, string>;
  setDismissedGuides: React.Dispatch<React.SetStateAction<Record<string, string>>>;
}

// ─── Context ────────────────────────────────────────────────

const ProgressContext = createContext<ProgressContextValue | null>(null);

export const useProgress = (): ProgressContextValue => {
  const ctx = useContext(ProgressContext);
  if (!ctx) throw new Error('useProgress must be used within ProgressProvider');
  return ctx;
};

// ─── Provider ───────────────────────────────────────────────

export const ProgressProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, isLoadingAuth, loadedData } = useAuth();

  // Core state
  const [userProgress, setUserProgress] = useState<UserProgress>({});
  const [studentProfile, setStudentProfile] = useState<StudentSubjectProfile | null>(null);
  const [northStar, setNorthStar] = useState<NorthStar | null>(null);
  const [timetableCompletions, setTimetableCompletions] = useState<Record<string, string[]>>({});
  const [unlockedAvatarSeeds, setUnlockedAvatarSeeds] = useState<string[]>([]);
  const [unlockedThemes, setUnlockedThemes] = useState<string[]>([]);
  const [unlockedCardStyles, setUnlockedCardStyles] = useState<string[]>([]);
  const [dismissedGuides, setDismissedGuides] = useState<Record<string, string>>({});

  // Hooks that depend on uid
  const { streak } = useStreak(user?.uid);
  const pointsData = usePoints(user?.uid);

  // Sync from auth loaded data
  const syncedRef = useRef(false);
  useEffect(() => {
    if (isLoadingAuth || syncedRef.current) return;
    if (!user) {
      syncedRef.current = false;
      setUserProgress({});
      setStudentProfile(null);
      setNorthStar(null);
      setTimetableCompletions({});
      setUnlockedAvatarSeeds([]);
      setUnlockedThemes([]);
      setUnlockedCardStyles([]);
      setDismissedGuides({});
      return;
    }
    setUserProgress(loadedData.userProgress);
    setStudentProfile(loadedData.studentProfile);
    setNorthStar(loadedData.northStar);
    setTimetableCompletions(loadedData.timetableCompletions);
    setUnlockedAvatarSeeds(loadedData.unlockedAvatarSeeds);
    setUnlockedThemes(loadedData.unlockedThemes);
    setUnlockedCardStyles(loadedData.unlockedCardStyles);
    setDismissedGuides(loadedData.dismissedGuides);
    syncedRef.current = true;
  }, [isLoadingAuth, user, loadedData]);

  // Reset sync flag on user change
  useEffect(() => {
    syncedRef.current = false;
  }, [user?.uid]);

  const value: ProgressContextValue = {
    userProgress,
    setUserProgress,
    studentProfile,
    setStudentProfile,
    northStar,
    setNorthStar,
    timetableCompletions,
    setTimetableCompletions,
    pointsData,
    streak,
    unlockedAvatarSeeds,
    setUnlockedAvatarSeeds,
    unlockedThemes,
    setUnlockedThemes,
    unlockedCardStyles,
    setUnlockedCardStyles,
    dismissedGuides,
    setDismissedGuides,
  };

  return <ProgressContext.Provider value={value}>{children}</ProgressContext.Provider>;
};

export default ProgressContext;
