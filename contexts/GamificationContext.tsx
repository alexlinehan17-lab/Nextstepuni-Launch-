/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { createContext, useContext, useState, useEffect, useRef, useCallback } from 'react';
import { db } from '../firebase';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { useGamification } from '../hooks/useGamification';
import { type AthleteRank, type AchievementDefinition } from '../gamificationConfig';
import { type IslandState } from '../types';
import { findBestLandPlacement } from '../components/journey/hex/hexGeometry';
import { type StreakData } from '../hooks/useStreak';

// ─── Types ──────────────────────────────────────────────────

interface GamificationContextValue {
  gamification: ReturnType<typeof useGamification>;
  // Toast queue
  currentToast: AchievementDefinition | null;
  isBonusFlashToast: boolean;
  dismissToast: () => void;
  queueToast: (item: AchievementDefinition | 'bonus-flash') => void;
  queueToasts: (items: (AchievementDefinition | 'bonus-flash')[]) => void;
  // Rank-up modal
  rankUpModal: AthleteRank | null;
  setRankUpModal: (rank: AthleteRank | null) => void;
  // Streak celebration
  streakCelebration: number | null;
  dismissStreakCelebration: () => void;
}

// ─── Context ────────────────────────────────────────────────

const GamificationContext = createContext<GamificationContextValue | null>(null);

export const useGamificationContext = (): GamificationContextValue => {
  const ctx = useContext(GamificationContext);
  if (!ctx) throw new Error('useGamificationContext must be used within GamificationProvider');
  return ctx;
};

// ─── Provider ───────────────────────────────────────────────

interface GamificationProviderProps {
  children: React.ReactNode;
  uid?: string;
  gamification: ReturnType<typeof useGamification>;
  streak: StreakData;
}

export const GamificationProvider: React.FC<GamificationProviderProps> = ({
  children, uid, gamification, streak,
}) => {

  // Toast queue
  const [toastQueue, setToastQueue] = useState<(AchievementDefinition | 'bonus-flash')[]>([]);
  const [currentToast, setCurrentToast] = useState<AchievementDefinition | null>(null);
  const [isBonusFlashToast, setIsBonusFlashToast] = useState(false);

  // Rank-up modal
  const [rankUpModal, setRankUpModal] = useState<AthleteRank | null>(null);
  const prevRankRef = useRef<string | null>(null);

  // Streak celebration
  const [streakCelebration, setStreakCelebration] = useState<number | null>(null);
  const lastStreakRef = useRef(0);

  // Process toast queue
  useEffect(() => {
    if (currentToast || isBonusFlashToast) return;
    if (toastQueue.length === 0) return;
    const next = toastQueue[0];
    setToastQueue(q => q.slice(1));
    if (next === 'bonus-flash') {
      setIsBonusFlashToast(true);
    } else {
      setCurrentToast(next);
    }
  }, [toastQueue, currentToast, isBonusFlashToast]);

  // Grant 3 grass tiles on rank-up
  const grantRankUpTiles = async (userUid: string) => {
    try {
      const snap = await getDoc(doc(db, 'progress', userUid));
      const data = snap.data();
      const island: IslandState | undefined = data?.islandState;
      if (!island || !island.placements) return;

      const occupied = new Set<string>();
      for (const p of island.placements) {
        if (p.type === 'hex') occupied.add(`${p.q},${p.r}`);
      }

      const newPlacements = [...island.placements];
      const now = new Date().toISOString();
      for (let i = 0; i < 3; i++) {
        const pos = findBestLandPlacement(occupied);
        const key = `${pos.q},${pos.r}`;
        occupied.add(key);
        newPlacements.push({
          itemId: 'terrain-grass',
          model: 'grass.glb',
          type: 'hex',
          q: pos.q,
          r: pos.r,
          purchasedAt: now,
        });
      }

      const newState: IslandState = { ...island, placements: newPlacements, lastPurchaseTimestamp: now };
      await setDoc(doc(db, 'progress', userUid), { islandState: newState }, { merge: true });
    } catch {
      console.error('Failed to grant rank-up tiles:');
    }
  };

  // Detect rank changes
  useEffect(() => {
    if (!gamification.isLoaded) return;
    const currentRankId = gamification.state.currentRank.id;
    if (prevRankRef.current !== null && prevRankRef.current !== currentRankId) {
      setRankUpModal(gamification.state.currentRank);
      if (uid) grantRankUpTiles(uid);
    }
    prevRankRef.current = currentRankId;
  }, [gamification.state.currentRank.id, gamification.isLoaded, uid]);

  // Detect streak milestones
  useEffect(() => {
    const milestones = [3, 7, 14, 21, 30, 50, 100];
    const current = streak.currentStreak;
    const last = lastStreakRef.current;
    if (current > last && milestones.includes(current)) {
      setStreakCelebration(current);
    }
    lastStreakRef.current = current;
  }, [streak.currentStreak]);

  const dismissToast = useCallback(() => {
    setCurrentToast(null);
    setIsBonusFlashToast(false);
  }, []);

  const queueToast = useCallback((item: AchievementDefinition | 'bonus-flash') => {
    setToastQueue(q => [...q, item]);
  }, []);

  const queueToasts = useCallback((items: (AchievementDefinition | 'bonus-flash')[]) => {
    setToastQueue(q => [...q, ...items]);
  }, []);

  const dismissStreakCelebration = useCallback(() => {
    setStreakCelebration(null);
  }, []);

  const value: GamificationContextValue = {
    gamification,
    currentToast,
    isBonusFlashToast,
    dismissToast,
    queueToast,
    queueToasts,
    rankUpModal,
    setRankUpModal,
    streakCelebration,
    dismissStreakCelebration,
  };

  return <GamificationContext.Provider value={value}>{children}</GamificationContext.Provider>;
};

export default GamificationContext;
