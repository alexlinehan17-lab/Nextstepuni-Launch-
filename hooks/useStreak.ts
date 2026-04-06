/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect } from 'react';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { type TimetableCompletions } from '../components/subjectData';
import { computeStreak } from '../components/timetableAlgorithm';

export interface StreakData {
  currentStreak: number;
  lastActiveDate: string; // YYYY-MM-DD
  longestStreak: number;
}

const DEFAULT_STREAK: StreakData = {
  currentStreak: 0,
  lastActiveDate: '',
  longestStreak: 0,
};

export function useStreak(uid?: string) {
  const [streak, setStreak] = useState<StreakData>(DEFAULT_STREAK);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    if (!uid) {
      setStreak(DEFAULT_STREAK);
      setIsLoaded(true);
      return;
    }

    let cancelled = false;

    const load = async () => {
      try {
        const progressDoc = await getDoc(doc(db, 'progress', uid));
        if (cancelled) return;
        if (progressDoc.exists()) {
          const data = progressDoc.data();
          const completions: TimetableCompletions = data.timetableCompletions ?? {};
          const restDays: string[] = data.subjectProfile?.restDays ?? [];
          const savedStreak = data.timetableStreak as StreakData | undefined;

          const { currentStreak, lastActiveDate } = computeStreak(completions, restDays);
          const longestStreak = Math.max(savedStreak?.longestStreak ?? 0, currentStreak);

          setStreak({ currentStreak, lastActiveDate, longestStreak });
        } else {
          setStreak(DEFAULT_STREAK);
        }
      } catch (err) {
        console.error('Failed to load streak:');
      }
      if (!cancelled) setIsLoaded(true);
    };

    load();
    return () => { cancelled = true; };
  }, [uid]);

  return { streak, isLoaded };
}
