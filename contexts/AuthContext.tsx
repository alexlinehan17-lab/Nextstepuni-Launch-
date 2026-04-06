/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { auth, db } from '../firebase';
import { onAuthStateChanged, signOut, User as FirebaseUser } from 'firebase/auth';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { SessionUser } from '../components/Auth';
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
}

interface AuthContextValue {
  user: SessionUser | null;
  isLoadingAuth: boolean;
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
};

// ─── Context ────────────────────────────────────────────────

const AuthContext = createContext<AuthContextValue>({
  user: null,
  isLoadingAuth: true,
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
  const [loadedData, setLoadedData] = useState<AuthLoadedData>(defaultLoadedData);

  // Auth listener
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser: FirebaseUser | null) => {
      if (firebaseUser) {
        // Admin user
        if (firebaseUser.email === 'admin@nextstep.app') {
          setUser({ uid: firebaseUser.uid, name: 'Admin', avatar: 'Charlie', isAdmin: true });
          setLoadedData({ ...defaultLoadedData });
          setIsLoadingAuth(false);
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
              });
              // Fire-and-forget auto-notifications
              if (userData.role !== 'gc') {
                generateAutoNotifications(firebaseUser.uid, pd).catch(() => {});
              }
            } else {
              setLoadedData({ ...defaultLoadedData, needsOnboarding: true });
            }
          } else {
            // No user doc — this account may have been deleted by a GC/admin.
            // Sign them out rather than auto-recovering.
            console.warn('[Auth] No user doc found for authenticated user — signing out.');
            await signOut(auth);
            setUser(null);
            setLoadedData({ ...defaultLoadedData });
          }
        } catch (error) {
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
    });

    return () => unsubscribe();
  }, []);

  const handleLoginSuccess = useCallback((loggedInUser: SessionUser) => {
    setUser(loggedInUser);
  }, []);

  const handleLogout = useCallback(async () => {
    await signOut(auth);
  }, []);

  const value: AuthContextValue = {
    user,
    isLoadingAuth,
    needsOnboarding: loadedData.needsOnboarding,
    loadedData,
    handleLoginSuccess,
    handleLogout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext;
