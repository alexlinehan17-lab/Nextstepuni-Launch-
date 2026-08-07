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
import { getProgressDocument } from '../services/progressRepository';
import { getUserDocument, mergeUserDocument } from '../services/userRepository';

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
  handleLoginSuccess: (user: SessionUser) => void;
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

  // Auth listener — handles initial state + ongoing changes (login, logout).
  // userResolved is set at the END of each callback, after all async Firestore
  // work completes. This avoids the race where authStateReady() resolves before
  // the Firestore user/progress docs are fetched, which would flash LoginPage
  // because user is still null mid-fetch.
  // Firebase guarantees onAuthStateChanged waits for the persistence layer
  // (IndexedDB) before its first fire, so the first callback is always definitive.
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser: FirebaseUser | null) => {
      if (firebaseUser) {
        // Admin user
        if (firebaseUser.email === 'admin@nextstep.app') {
          setUser({ uid: firebaseUser.uid, name: 'Admin', avatar: 'Charlie', isAdmin: true });
          setLoadedData({ ...defaultLoadedData });
          setIsLoadingAuth(false);
          if (!authResolvedRef.current) {
            authResolvedRef.current = true;
            setAuthResolved(true);
          }
          setUserResolved(true);
          return;
        }

        // Regular user — fetch profile + progress
        try {
          const [userData, progressData] = await Promise.all([
            getUserDocument(firebaseUser.uid),
            getProgressDocument(firebaseUser.uid),
          ]);
          const token = await firebaseUser.getIdTokenResult();
          const claimedRole = token.claims.role;
          const claimedSchool = token.claims.school;
          const roleFromClaims = claimedRole === 'gc' || claimedRole === 'staff' || claimedRole === 'admin'
            ? claimedRole
            : undefined;
          const schoolFromClaims = typeof claimedSchool === 'string' ? claimedSchool : undefined;

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
              role: userData.role ?? roleFromClaims,
              school: userData.school ?? schoolFromClaims,
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
                needsOnboarding: !pd.subjectProfile,
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
            const fallbackName = firebaseUser.displayName || firebaseUser.email?.split('@')[0] || 'Student';
            setUser({
              uid: firebaseUser.uid,
              name: fallbackName,
              avatar: 'Charlie',
              isAdmin: false,
              role: roleFromClaims,
              school: schoolFromClaims,
            });
            if (progressData) {
              const pd = progressData;
              setLoadedData({
                userProgress: pd as UserProgress,
                northStar: pd.northStar ? (pd.northStar as NorthStar) : null,
                studentProfile: pd.subjectProfile ? (pd.subjectProfile as StudentSubjectProfile) : null,
                needsOnboarding: !pd.subjectProfile,
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
          console.error('Error fetching user data:', err);
          const fallbackName = firebaseUser.displayName || firebaseUser.email?.split('@')[0] || 'Student';
          setUser({
            uid: firebaseUser.uid,
            name: fallbackName,
            avatar: 'Charlie',
            isAdmin: false,
          });
          setLoadedData({ ...defaultLoadedData, needsOnboarding: true });
        }
      } else {
        setUser(null);
        setLoadedData({ ...defaultLoadedData });
      }

      setIsLoadingAuth(false);
      if (!authResolvedRef.current) {
        authResolvedRef.current = true;
        setAuthResolved(true);
      }
      setUserResolved(true);
    });

    return () => unsubscribe();
  }, []);

  const handleLoginSuccess = useCallback((loggedInUser: SessionUser) => {
    setUser(loggedInUser);
    setUserResolved(true);
  }, []);

  const handleLogout = useCallback(async () => {
    await signOut(auth);
  }, []);

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
    handleLoginSuccess,
    handleLogout,
    markOnboardingComplete,
    markOnboardingNeeded,
    patchUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext;
