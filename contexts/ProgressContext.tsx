/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { createContext, useContext, useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { db } from '../firebase';
import { doc, getDoc } from 'firebase/firestore';
import { type UserProgress, type NorthStar } from '../types';
import { type StudentSubjectProfile } from '../components/subjectData';
import { computeStreak } from '../components/timetableAlgorithm';
import { useAuth } from './AuthContext';

// ─── Types ──────────────────────────────────────────────────

export interface PointsData {
  totalEarned: number;
  totalSpent: number;
  balance: number;
  reload: () => void;
}

export interface StreakData {
  currentStreak: number;
  longestStreak: number;
  lastActiveDate: string;
}

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

  // Points & streak (derived from rawProgressDoc)
  pointsData: PointsData;
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

  // True after progress data has been synced at least once from auth
  progressLoaded: boolean;

  /** The full raw progress/{uid} doc. Hooks derive their fields from this
   *  instead of making independent getDoc calls. */
  rawProgressDoc: Record<string, any>;

  /** Re-fetches the progress doc from Firestore and updates all derived state.
   *  Replaces the old per-hook reload() pattern. */
  reloadProgress: () => void;
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
  const [progressLoaded, setProgressLoaded] = useState(false);
  const [rawProgressDoc, setRawProgressDoc] = useState<Record<string, any>>({});
  const [reloadVersion, setReloadVersion] = useState(0);

  // Derive points from raw doc
  const pointsData: PointsData = useMemo(() => {
    const earned = rawProgressDoc.pointsData?.totalEarned ?? 0;
    const spent = rawProgressDoc.pointsData?.totalSpent ?? 0;
    return {
      totalEarned: earned,
      totalSpent: spent,
      balance: earned - spent,
      reload: () => setReloadVersion(v => v + 1),
    };
  }, [rawProgressDoc.pointsData?.totalEarned, rawProgressDoc.pointsData?.totalSpent]);

  // Derive streak from raw doc
  const streak: StreakData = useMemo(() => {
    const completions = rawProgressDoc.timetableCompletions || timetableCompletions || {};
    const restDays = rawProgressDoc.subjectProfile?.restDays || studentProfile?.restDays || [];
    const saved = rawProgressDoc.timetableStreak;
    const computed = computeStreak(completions, restDays);
    return {
      currentStreak: computed.currentStreak,
      longestStreak: Math.max(computed.longestStreak ?? 0, saved?.longestStreak ?? 0),
      lastActiveDate: computed.lastActiveDate || saved?.lastActiveDate || '',
    };
  }, [rawProgressDoc, timetableCompletions, studentProfile?.restDays]);

  const reloadProgress = useCallback(() => {
    setReloadVersion(v => v + 1);
  }, []);

  // Sync from auth loaded data (initial load)
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
      setRawProgressDoc({});
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
    setRawProgressDoc(loadedData.rawProgressDoc);
    syncedRef.current = true;
    setProgressLoaded(true);
  }, [isLoadingAuth, user, loadedData]);

  // Reset sync flag on user change
  useEffect(() => {
    syncedRef.current = false;
  }, [user?.uid]);

  // Reload: re-fetch progress doc from Firestore when reloadVersion bumps
  useEffect(() => {
    if (reloadVersion === 0 || !user?.uid) return;
    let cancelled = false;
    getDoc(doc(db, 'progress', user.uid)).then(snap => {
      if (cancelled) return;
      if (snap.exists()) {
        const pd = snap.data();
        setRawProgressDoc(pd);
        // Also refresh the cherry-picked fields for backwards compat
        setTimetableCompletions(pd.timetableCompletions || {});
      }
    }).catch(() => {});
    return () => { cancelled = true; };
  }, [reloadVersion, user?.uid]);

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
    progressLoaded,
    rawProgressDoc,
    reloadProgress,
  };

  return <ProgressContext.Provider value={value}>{children}</ProgressContext.Provider>;
};

export default ProgressContext;
