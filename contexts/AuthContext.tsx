/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { createContext, useContext, useState, useEffect, useCallback, useRef } from 'react';
import { auth } from '../firebase';
import { onAuthStateChanged, signOut, type User as FirebaseUser } from 'firebase/auth';
import { type SessionUser, yearGroupToCurriculumLevel, type CurriculumLevel, isSchoolStaff } from '../utils/authUtils';
import { type UserProgress, type NorthStar } from '../types';
import { type StudentSubjectProfile } from '../components/subjectData';
import { generateAutoNotifications } from '../components/gc/gcNotifications';
import { logError } from '../utils/logError';
import { getProgressDocument, progressNeedsOnboarding } from '../services/progressRepository';
import { mergeUserDocument, waitForUserDocument } from '../services/userRepository';
import {
  DEMO_STUDENT_UID,
  clearDemoSession,
  createDemoStudentSession,
  hasActiveDemoSession,
  loadDemoStudentLoadedData,
  markDemoSessionActive,
} from '../data/devStudent';
import { isVerifiedAdminSession } from '../utils/adminIdentity';
import { clearLocalSessionData } from '../utils/sessionPrivacy';

// ─── Types ──────────────────────────────────────────────────

interface AuthLoadedData {
  userProgress: UserProgress;
  northStar: NorthStar | null;
  studentProfile: StudentSubjectProfile | null;
  needsOnboarding: boolean;
  unlockedAvatarSeeds: string[];
  unlockedThemes: string[];
  unlockedCardStyles: string[];
  dismissedGuides: Record<string, string>;
  timetableCompletions: Record<string, string[]>;
  /** The full raw progress doc from Firestore — hooks derive their fields from this */
  rawProgressDoc: Record<string, any>;
}

export interface LoginSuccessOptions {
  /** Preserve the new-account route while AuthContext finishes its own reads. */
  requiresOnboarding?: boolean;
}

interface AuthContextValue {
  user: SessionUser | null;
  isLoadingAuth: boolean;
  authResolved: boolean;
  /** True once Firebase's persistence layer has been read and we have a definitive
   *  auth state. Driven by auth.authStateReady() on initial load, then set immediately
   *  on subsequent auth changes (login, logout). Gate LoginPage on this. */
  userResolved: boolean;
  needsOnboarding: boolean;
  loadedData: AuthLoadedData;
  /** UID whose Firestore progress is represented by `loadedData`. This stays
   *  null during the eager LoginPage session hand-off, until the auth listener
   *  has finished loading that account's data. */
  loadedDataUid: string | null;
  /** Whether the owning user's initial profile/progress read completed. Failed
   *  fallback data is intentionally not authoritative for rank baselines. */
  loadedDataStatus: 'pending' | 'loaded' | 'failed';
  handleLoginSuccess: (user: SessionUser, options?: LoginSuccessOptions) => void;
  handleLogout: () => Promise<void>;
  /** Called by App.tsx after the onboarding flow saves a subject profile, so
   *  the redirect at App.tsx:252 doesn't fire again on the next render. */
  markOnboardingComplete: () => void;
  /** Re-raise the onboarding gate. Needed because the onboarding save is now
   *  fired rather than awaited: if it is genuinely rejected we must be able to
   *  put the student back into onboarding, or they sit in the app with no
   *  profile — the exact state that hid a rules bug for weeks in May 2026. */
  markOnboardingNeeded: () => void;
  /** Patch in-memory user fields after a Firestore write to users/{uid} so
   *  callers don't have to wait for the next sign-in to see the change.
   *  Used after onboarding writes yearGroup, and after year-progression
   *  writes update yearGroup/curriculumLevel. */
  patchUser: (patch: Partial<SessionUser>) => void;
}

const defaultLoadedData: AuthLoadedData = {
  userProgress: {},
  northStar: null,
  studentProfile: null,
  needsOnboarding: false,
  unlockedAvatarSeeds: [],
  unlockedThemes: [],
  unlockedCardStyles: [],
  dismissedGuides: {},
  timetableCompletions: {},
  rawProgressDoc: {},
};

// ─── Context ────────────────────────────────────────────────

const AuthContext = createContext<AuthContextValue>({
  user: null,
  isLoadingAuth: true,
  authResolved: false,
  userResolved: false,
  needsOnboarding: false,
  loadedData: defaultLoadedData,
  loadedDataUid: null,
  loadedDataStatus: 'pending',
  handleLoginSuccess: () => {},
  handleLogout: async () => {},
  markOnboardingComplete: () => {},
  markOnboardingNeeded: () => {},
  patchUser: () => {},
});

export const useAuth = () => useContext(AuthContext);

// ─── Provider ───────────────────────────────────────────────

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<SessionUser | null>(null);
  const [isLoadingAuth, setIsLoadingAuth] = useState(true);
  const [authResolved, setAuthResolved] = useState(false);
  const [userResolved, setUserResolved] = useState(false);
  const authResolvedRef = useRef(false);
  const [loadedData, setLoadedData] = useState<AuthLoadedData>(defaultLoadedData);
  const [loadedDataUid, setLoadedDataUid] = useState<string | null>(null);
  const [loadedDataStatus, setLoadedDataStatus] = useState<'pending' | 'loaded' | 'failed'>('pending');

  // Auth listener — handles initial state + ongoing changes (login, logout).
  // userResolved is set at the END of each callback, after all async Firestore
  // work completes. This avoids the race where authStateReady() resolves before
  // the Firestore user/progress docs are fetched, which would flash LoginPage
  // because user is still null mid-fetch.
  // Firebase guarantees onAuthStateChanged waits for the persistence layer
  // (IndexedDB) before its first fire, so the first callback is always definitive.
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser: FirebaseUser | null) => {
      setLoadedDataUid(null);
      setLoadedDataStatus('pending');

      if (firebaseUser) {
        // Token refresh can fail on a poor connection. Settle the auth listener
        // deterministically and fail closed for privileged routing: an
        // unavailable claim set must never become an admin or staff grant.
        const initialToken = await firebaseUser.getIdTokenResult().catch(err => {
          console.error('Could not verify the current ID token:', err);
          return null;
        });
        // Admin user
        if (initialToken && isVerifiedAdminSession(firebaseUser, initialToken.claims)) {
          setUser({ uid: firebaseUser.uid, name: 'Admin', avatar: 'Charlie', isAdmin: true });
          setLoadedData({ ...defaultLoadedData });
          setLoadedDataUid(firebaseUser.uid);
          setLoadedDataStatus('loaded');
          setIsLoadingAuth(false);
          if (!authResolvedRef.current) {
            authResolvedRef.current = true;
            setAuthResolved(true);
          }
          setUserResolved(true);
          return;
        }

        // Regular user — fetch profile + progress
        let loadFailed = false;
        try {
          const [userData, progressData] = await Promise.all([
            waitForUserDocument(firebaseUser.uid),
            getProgressDocument(firebaseUser.uid),
          ]);
          if (userData) {

            // ─── Junior Cycle Phase 1: backfill curriculumLevel ──────────
            // Existing users (created before Phase 1) lack the
            // `curriculumLevel` field. Compute it from `yearGroup` if
            // present, default to 'senior' otherwise (everyone pre-JC was
            // by definition senior). Write back to Firestore so the next
            // session reads it directly. Idempotent.
            let curriculumLevel: CurriculumLevel | undefined = userData.curriculumLevel;
            if (!curriculumLevel) {
              curriculumLevel = userData.yearGroup
                ? yearGroupToCurriculumLevel(userData.yearGroup)
                : 'senior';
              mergeUserDocument(firebaseUser.uid, { curriculumLevel })
                .catch(err => console.error('Failed to backfill curriculumLevel:', err));
            }

            setUser({
              uid: firebaseUser.uid,
              name: userData.name,
              avatar: userData.avatar || 'Charlie',
              isAdmin: false,
              // Current server-managed profile state is authoritative. Token
              // claims may remain cached after a demotion and are never used
              // as a fallback grant.
              role: userData.role,
              school: userData.school,
              yearGroup: userData.yearGroup,
              curriculumLevel,
              needsPasswordChange: userData.needsPasswordChange || false,
            });

            if (progressData) {
              const pd = progressData;
              setLoadedData({
                userProgress: pd as UserProgress,
                northStar: pd.northStar ? (pd.northStar as NorthStar) : null,
                studentProfile: pd.subjectProfile ? (pd.subjectProfile as StudentSubjectProfile) : null,
                needsOnboarding: progressNeedsOnboarding(pd),
                unlockedAvatarSeeds: pd.cosmeticUnlocks?.avatarSeeds || [],
                unlockedThemes: pd.cosmeticUnlocks?.themeColors || [],
                unlockedCardStyles: pd.cosmeticUnlocks?.cardStyles || [],
                dismissedGuides: pd.dismissedGuides || {},
                timetableCompletions: pd.timetableCompletions || {},
                rawProgressDoc: pd,
              });
              // Fire-and-forget auto-notifications (students only — not staff)
              if (!isSchoolStaff(userData.role)) {
                generateAutoNotifications(firebaseUser.uid, pd).catch((e) => logError('AuthContext.autoNotifications', e));
              }
            } else {
              setLoadedData({ ...defaultLoadedData, needsOnboarding: true });
            }
          } else {
            // No user doc in Firestore. Could be a race with registration
            // (doc write still pending/offline), or a deleted account. Either way,
            // don't sign out — that destroys the session. Use a fallback user,
            // but still check the progress doc for onboarding state.
            // Not the email local-part: it is wrong for every account that has a
            // real name on file, and it puts part of a school-issued address on
            // screen. A neutral placeholder is the honest thing to show while the
            // document is missing.
            const fallbackName = firebaseUser.displayName || 'Student';
            setUser({
              uid: firebaseUser.uid,
              name: fallbackName,
              avatar: 'Charlie',
              isAdmin: false,
            });
            if (progressData) {
              const pd = progressData;
              setLoadedData({
                userProgress: pd as UserProgress,
                northStar: pd.northStar ? (pd.northStar as NorthStar) : null,
                studentProfile: pd.subjectProfile ? (pd.subjectProfile as StudentSubjectProfile) : null,
                needsOnboarding: progressNeedsOnboarding(pd),
                unlockedAvatarSeeds: pd.cosmeticUnlocks?.avatarSeeds || [],
                unlockedThemes: pd.cosmeticUnlocks?.themeColors || [],
                unlockedCardStyles: pd.cosmeticUnlocks?.cardStyles || [],
                dismissedGuides: pd.dismissedGuides || {},
                timetableCompletions: pd.timetableCompletions || {},
                rawProgressDoc: pd,
              });
            } else {
              setLoadedData({ ...defaultLoadedData, needsOnboarding: true });
            }
          }
        } catch (err) {
          loadFailed = true;
          console.error('Error fetching user data:', err);
          // Not the email local-part: it is wrong for every account that has a
            // real name on file, and it puts part of a school-issued address on
            // screen. A neutral placeholder is the honest thing to show while the
            // document is missing.
            const fallbackName = firebaseUser.displayName || 'Student';
          setUser({
            uid: firebaseUser.uid,
            name: fallbackName,
            avatar: 'Charlie',
            isAdmin: false,
          });
          setLoadedData({ ...defaultLoadedData, needsOnboarding: true });
        }
        setLoadedDataStatus(loadFailed ? 'failed' : 'loaded');
      } else {
        if (hasActiveDemoSession()) {
          setUser(createDemoStudentSession());
          setLoadedData(loadDemoStudentLoadedData());
          setLoadedDataUid(DEMO_STUDENT_UID);
          setLoadedDataStatus('loaded');
        } else {
          // Browser auth uses session persistence, so closing a shared-school
          // browser ends Firebase sign-in but cannot run our logout handler.
          // Clear the previous account's device-only drafts on the next
          // unauthenticated boot before presenting the login screen.
          await clearLocalSessionData();
          setUser(null);
          setLoadedData({ ...defaultLoadedData });
        }
      }

      if (firebaseUser) setLoadedDataUid(firebaseUser.uid);
      setIsLoadingAuth(false);
      if (!authResolvedRef.current) {
        authResolvedRef.current = true;
        setAuthResolved(true);
      }
      setUserResolved(true);
    });

    return () => unsubscribe();
  }, []);

  const handleLoginSuccess = useCallback((loggedInUser: SessionUser, options?: LoginSuccessOptions) => {
    if (loggedInUser.uid === DEMO_STUDENT_UID) {
      markDemoSessionActive();
      setLoadedData(loadDemoStudentLoadedData());
      setLoadedDataUid(loggedInUser.uid);
      setLoadedDataStatus('loaded');
    } else if (options?.requiresOnboarding) {
      // LoginPage knows synchronously that this is a newly-created account.
      // Keep that intent while the auth listener and ProgressContext finish
      // mirroring Firestore; otherwise their default `false` value briefly
      // swaps the account-setup loader for "Loading your workspace".
      setLoadedData(previous => ({ ...previous, needsOnboarding: true }));
    }
    setUser(loggedInUser);
    setUserResolved(true);
  }, []);

  const handleLogout = useCallback(async () => {
    if (user?.uid === DEMO_STUDENT_UID) {
      clearDemoSession();
      setUser(null);
      setLoadedData({ ...defaultLoadedData });
      setLoadedDataUid(null);
      setLoadedDataStatus('pending');
      setUserResolved(true);
      return;
    }
    try {
      await signOut(auth);
    } finally {
      // A network/auth error must not leave the previous student's drafts,
      // marks or oral recordings behind on a shared school computer.
      await clearLocalSessionData();
    }
    setUser(null);
    setLoadedData({ ...defaultLoadedData });
    setLoadedDataUid(null);
    setLoadedDataStatus('pending');
    setUserResolved(true);
  }, [user?.uid]);

  const markOnboardingComplete = useCallback(() => {
    setLoadedData(prev => ({ ...prev, needsOnboarding: false }));
  }, []);

  const markOnboardingNeeded = useCallback(() => {
    setLoadedData(prev => ({ ...prev, needsOnboarding: true }));
  }, []);

  const patchUser = useCallback((patch: Partial<SessionUser>) => {
    setUser(prev => (prev ? { ...prev, ...patch } : prev));
  }, []);

  const value: AuthContextValue = {
    user,
    isLoadingAuth,
    authResolved,
    userResolved,
    needsOnboarding: loadedData.needsOnboarding,
    loadedData,
    loadedDataUid,
    loadedDataStatus,
    handleLoginSuccess,
    handleLogout,
    markOnboardingComplete,
    markOnboardingNeeded,
    patchUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext;
