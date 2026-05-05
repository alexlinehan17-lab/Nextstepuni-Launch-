/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { createContext, useContext, useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { db } from '../firebase';
import { collection, doc, getDoc, getDocs } from 'firebase/firestore';
import { type UserProgress, type NorthStar, type TopicMasteryMap, type UnifiedMockResult } from '../types';
import { type StudentSubjectProfile } from '../components/subjectData';
import { computeStreak } from '../components/timetableAlgorithm';
import { useAuth } from './AuthContext';
import { type StudySessionRecord } from '../utils/strategyRegistry';
import { type DebriefEntry } from '../components/StudyDebrief';

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

  // Typed accessors over the raw progress/{uid} doc. Hooks that read these
  // shared fields should use these rather than the underlying doc shape so the
  // schema can evolve without breaking every consumer.
  studySessions: StudySessionRecord[];
  studyDebriefs: DebriefEntry[];
  topicMastery: TopicMasteryMap | undefined;
  unifiedMockResults: UnifiedMockResult[];
  questRewards: Record<string, string>;
  teachBacksSeen: string[];

  /** Escape hatch — only for hooks that own their own field on the progress
   *  doc (useGamification, useIslandShop, useFlares, useWeeklyChallenge,
   *  useTopicMastery, useMockResults). New code should use the typed
   *  accessors above. */
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
  // Study sessions live in /progress/{uid}/sessions/{sessionId} subcollection
  // (migrated from the old rawProgressDoc.studySessions array — see Schema
  // notes). Loaded once on user-change and on reloadProgress().
  const [sessionsFromSubcollection, setSessionsFromSubcollection] = useState<StudySessionRecord[]>([]);

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
      longestStreak: Math.max(computed.currentStreak, saved?.longestStreak ?? 0),
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

  // Load study sessions from the /progress/{uid}/sessions subcollection.
  // Re-runs on user change and on reloadProgress() bumps.
  useEffect(() => {
    if (!user?.uid) {
      setSessionsFromSubcollection([]);
      return;
    }
    let cancelled = false;
    getDocs(collection(db, 'progress', user.uid, 'sessions'))
      .then(snap => {
        if (cancelled) return;
        const records = snap.docs.map(d => d.data() as StudySessionRecord);
        setSessionsFromSubcollection(records);
      })
      .catch(err => {
        console.error('Failed to load study sessions:', err);
      });
    return () => { cancelled = true; };
  }, [user?.uid, reloadVersion]);

  // Typed accessors derived from the raw doc — see the interface comment.
  // studySessions is sourced from the /progress/{uid}/sessions subcollection
  // (loaded by the effect above). The legacy rawProgressDoc.studySessions
  // array is no longer written to and is ignored here.
  const studySessions = sessionsFromSubcollection;
  const studyDebriefs: DebriefEntry[] = rawProgressDoc.studyDebriefs ?? [];
  const topicMastery: TopicMasteryMap | undefined = rawProgressDoc.topicMastery ?? undefined;
  const unifiedMockResults: UnifiedMockResult[] = rawProgressDoc.unifiedMockResults ?? [];
  const questRewards: Record<string, string> = rawProgressDoc.questRewards ?? {};
  const teachBacksSeen: string[] = rawProgressDoc.teachBacksSeen ?? [];

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
    studySessions,
    studyDebriefs,
    topicMastery,
    unifiedMockResults,
    questRewards,
    teachBacksSeen,
    rawProgressDoc,
    reloadProgress,
  };

  return <ProgressContext.Provider value={value}>{children}</ProgressContext.Provider>;
};

export default ProgressContext;
