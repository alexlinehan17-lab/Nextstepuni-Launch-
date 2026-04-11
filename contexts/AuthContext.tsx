/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { createContext, useContext, useState, useEffect, useCallback, useRef } from 'react';
import { auth, db } from '../firebase';
import { onAuthStateChanged, signOut, type User as FirebaseUser } from 'firebase/auth';
import { doc, getDoc } from 'firebase/firestore';
import { type SessionUser } from '../components/Auth';
import { type UserProgress, type NorthStar } from '../types';
import { type StudentSubjectProfile } from '../components/subjectData';
import { generateAutoNotifications } from '../components/gc/gcNotifications';

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
          const [userDoc, progressDoc] = await Promise.all([
            getDoc(doc(db, 'users', firebaseUser.uid)),
            getDoc(doc(db, 'progress', firebaseUser.uid)),
          ]);

          if (userDoc.exists()) {
            const userData = userDoc.data();
            setUser({
              uid: firebaseUser.uid,
              name: userData.name,
              avatar: userData.avatar || 'Charlie',
              isAdmin: false,
              role: userData.role,
              school: userData.school,
              yearGroup: userData.yearGroup,
            });

            if (progressDoc.exists()) {
              const pd = progressDoc.data();
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
              // Fire-and-forget auto-notifications
              if (userData.role !== 'gc') {
                generateAutoNotifications(firebaseUser.uid, pd).catch(() => {});
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
            setUser({ uid: firebaseUser.uid, name: fallbackName, avatar: 'Charlie', isAdmin: false });
            if (progressDoc.exists()) {
              const pd = progressDoc.data();
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
        } catch {
          console.error('Error fetching user data:');
          const fallbackName = firebaseUser.displayName || firebaseUser.email?.split('@')[0] || 'Student';
          setUser({ uid: firebaseUser.uid, name: fallbackName, avatar: 'Charlie', isAdmin: false });
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

  const value: AuthContextValue = {
    user,
    isLoadingAuth,
    authResolved,
    userResolved,
    needsOnboarding: loadedData.needsOnboarding,
    loadedData,
    handleLoginSuccess,
    handleLogout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext;
