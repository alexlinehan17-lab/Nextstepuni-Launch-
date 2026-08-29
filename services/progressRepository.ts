/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Typed read boundary for progress/{uid}. This deliberately starts with the
 * boot-critical fields; feature owners can add typed namespaces here as they
 * migrate away from direct Firestore access.
 */

import { arrayUnion, collection, doc, getDoc, getDocs, increment, setDoc, updateDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { type StudentSubjectProfile } from '../components/subjectData';
import { type DebriefEntry } from '../components/StudyDebrief';
import { type StudySessionRecord } from '../utils/strategyRegistry';
import { type GamificationFirestoreData } from '../gamificationConfig';
import {
  type IslandState,
  type NorthStar,
  type StudyReflection,
  type TopicMasteryMap,
  type TopicMasteryV2,
  type UnifiedMockResult,
  type UserProgress,
} from '../types';

export interface ProgressDocument {
  northStar?: NorthStar;
  subjectProfile?: StudentSubjectProfile;
  /** A student may deliberately enter the app before creating a subject
   * profile. Persist that choice so refreshes do not restart onboarding. */
  onboardingSkippedAt?: string | null;
  cosmeticUnlocks?: {
    avatarSeeds?: string[];
    themeColors?: string[];
    cardStyles?: string[];
  };
  dismissedGuides?: Record<string, string>;
  timetableCompletions?: Record<string, string[]>;
  timetableStreak?: { currentStreak: number; longestStreak: number; lastActiveDate: string };
  pointsData?: { totalEarned?: number; totalSpent?: number };
  earnedRest?: { restDayPasses?: string[] };
  /** Localhost Demo Account only. Real sessions live in the sessions subcollection. */
  studySessions?: StudySessionRecord[];
  studyDebriefs?: DebriefEntry[];
  reflections?: StudyReflection[];
  topicMastery?: TopicMasteryMap;
  topicMasteryV2?: TopicMasteryV2;
  unifiedMockResults?: UnifiedMockResult[];
  mockResults?: UnifiedMockResult[];
  pointsPassport?: { mockResults?: LegacyMockResult[] };
  warRoom?: {
    mockResults?: LegacyMockResult[];
    topicMap?: Record<string, Array<{ name: string; confidence: string; updatedAt?: number }>>;
  };
  syllabusXRayMastery?: Record<string, Record<string, string>>;
  questRewards?: Record<string, string>;
  weeklyChallengeRewards?: Record<string, string>;
  islandState?: IslandState;
  gamification?: Partial<GamificationFirestoreData>;
  [field: string]: unknown;
}

/** The single source of truth for the account-setup gate. */
export function progressNeedsOnboarding(progress: ProgressDocument | null): boolean {
  return !progress?.subjectProfile && !progress?.onboardingSkippedAt;
}

interface LegacyMockResult {
  id?: string;
  label?: string;
  date?: string;
  grades?: UnifiedMockResult['entries'];
  subject?: string;
  grade?: string;
  level?: string;
  totalPoints?: number;
  timestamp?: number;
}

export async function getProgressDocument(uid: string): Promise<ProgressDocument | null> {
  const snapshot = await getDoc(doc(db, 'progress', uid));
  return snapshot.exists() ? snapshot.data() as ProgressDocument : null;
}

export async function getStudySessions(uid: string): Promise<StudySessionRecord[]> {
  const snapshot = await getDocs(collection(db, 'progress', uid, 'sessions'));
  return snapshot.docs.map(item => item.data() as StudySessionRecord);
}

/** Atomically merge a module checkpoint and its earned-points delta. */
export function saveModuleProgress(
  uid: string,
  moduleId: string,
  progress: { unlockedSection: number },
  pointsToAward: number,
): Promise<void> {
  const patch: Record<string, unknown> = { [moduleId]: progress };
  if (pointsToAward > 0) {
    patch.pointsData = { totalEarned: increment(pointsToAward) };
  }
  return setDoc(doc(db, 'progress', uid), patch, { merge: true });
}

/** Merge only the supplied gamification leaves, never a stale full snapshot. */
export function saveGamificationFields(
  uid: string,
  fields: Partial<GamificationFirestoreData>,
): Promise<void> {
  const patch: Record<string, unknown> = {};
  for (const [field, value] of Object.entries(fields)) {
    patch[`gamification.${field}`] = value;
  }
  return updateDoc(doc(db, 'progress', uid), patch);
}

/** Append achievement ids and timestamp each id atomically with its bonus. */
export function unlockAchievements(
  uid: string,
  achievements: ReadonlyArray<{ id: string; timestamp: number }>,
  bonusPoints: number,
): Promise<void> {
  const ids = achievements.map(item => item.id);
  const patch: Record<string, unknown> = {
    'gamification.unlockedAchievements': arrayUnion(...ids),
  };
  for (const item of achievements) {
    if (item.id.includes('.')) throw new Error(`Invalid achievement id: ${item.id}`);
    patch[`gamification.achievementTimestamps.${item.id}`] = item.timestamp;
  }
  if (bonusPoints > 0) patch['pointsData.totalEarned'] = increment(bonusPoints);
  return updateDoc(doc(db, 'progress', uid), patch);
}

export function extractModuleProgress(data: ProgressDocument): UserProgress {
  const result: UserProgress = {};
  for (const [key, value] of Object.entries(data)) {
    if (
      value !== null
      && typeof value === 'object'
      && 'unlockedSection' in value
      && typeof value.unlockedSection === 'number'
    ) {
      result[key] = { unlockedSection: value.unlockedSection };
    }
  }
  return result;
}
