/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect } from 'react';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';

export interface StreakData {
  currentStreak: number;
  lastActiveDate: string; // YYYY-MM-DD
  longestStreak: number;
}

const STORAGE_KEY = 'nextstep-streak';

const DEFAULT_STREAK: StreakData = {
  currentStreak: 0,
  lastActiveDate: '',
  longestStreak: 0,
};

function getToday(): string {
  return new Date().toISOString().slice(0, 10);
}

function getYesterday(): string {
  const d = new Date();
  d.setDate(d.getDate() - 1);
  return d.toISOString().slice(0, 10);
}

function computeStreak(existing: StreakData): StreakData {
  const today = getToday();

  if (existing.lastActiveDate === today) {
    return existing; // Already counted today
  }

  if (existing.lastActiveDate === getYesterday()) {
    const newStreak = existing.currentStreak + 1;
    return {
      currentStreak: newStreak,
      lastActiveDate: today,
      longestStreak: Math.max(existing.longestStreak, newStreak),
    };
  }

  // Streak broken — reset to 1
  return {
    currentStreak: 1,
    lastActiveDate: today,
    longestStreak: Math.max(existing.longestStreak, 1),
  };
}

function readLocalStreak(): StreakData {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch {}
  return DEFAULT_STREAK;
}

function writeLocalStreak(data: StreakData) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

export function useStreak(uid?: string) {
  const [streak, setStreak] = useState<StreakData>(() => {
    const local = readLocalStreak();
    return computeStreak(local);
  });
  const [isLoaded, setIsLoaded] = useState(false);

  // Write computed streak to localStorage immediately
  useEffect(() => {
    writeLocalStreak(streak);
  }, [streak]);

  // Load from Firestore, compute, and persist
  useEffect(() => {
    if (!uid) {
      setIsLoaded(true);
      return;
    }

    const load = async () => {
      try {
        const streakDoc = await getDoc(doc(db, 'streaks', uid));
        let base = readLocalStreak();

        if (streakDoc.exists()) {
          const remote = streakDoc.data() as StreakData;
          // Firestore wins if it has a more recent or higher streak
          if (remote.lastActiveDate >= base.lastActiveDate) {
            base = remote;
          }
        }

        const updated = computeStreak(base);
        setStreak(updated);
        writeLocalStreak(updated);

        // Persist back to Firestore
        await setDoc(doc(db, 'streaks', uid), updated, { merge: true });
      } catch (err) {
        console.error('Failed to load/save streak:', err);
      }
      setIsLoaded(true);
    };

    load();
  }, [uid]);

  return { streak, isLoaded };
}
