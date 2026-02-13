/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback } from 'react';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';

export interface MoodEntry {
  date: string;     // YYYY-MM-DD
  mood: string;     // 'calm' | 'balanced' | 'energized' | 'stressed'
  timestamp: number;
}

interface MoodData {
  entries: MoodEntry[];
}

const STORAGE_KEY = 'nextstep-moods';
const MAX_ENTRIES = 90;

function getToday(): string {
  return new Date().toISOString().slice(0, 10);
}

function readLocalMoods(): MoodData {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch {}
  return { entries: [] };
}

function writeLocalMoods(data: MoodData) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

export function useMood(uid?: string) {
  const [moodData, setMoodData] = useState<MoodData>(readLocalMoods);
  const [isLoaded, setIsLoaded] = useState(false);

  // Load from Firestore on mount
  useEffect(() => {
    if (!uid) {
      setIsLoaded(true);
      return;
    }

    const load = async () => {
      try {
        const moodDoc = await getDoc(doc(db, 'moods', uid));
        if (moodDoc.exists()) {
          const remote = moodDoc.data() as MoodData;
          if (remote.entries && remote.entries.length > 0) {
            setMoodData(remote);
            writeLocalMoods(remote);
          }
        }
      } catch (err) {
        console.error('Failed to load moods:', err);
      }
      setIsLoaded(true);
    };

    load();
  }, [uid]);

  const today = getToday();
  const todayEntry = moodData.entries.find(e => e.date === today);
  const todayMood = todayEntry?.mood || null;

  const setMood = useCallback((mood: string) => {
    setMoodData(prev => {
      // Remove existing entry for today if any
      const filtered = prev.entries.filter(e => e.date !== today);
      const newEntry: MoodEntry = { date: today, mood, timestamp: Date.now() };
      const entries = [...filtered, newEntry].slice(-MAX_ENTRIES);
      const next = { entries };

      writeLocalMoods(next);

      if (uid) {
        setDoc(doc(db, 'moods', uid), next, { merge: true }).catch(err =>
          console.error('Failed to save mood:', err)
        );
      }

      return next;
    });
  }, [uid, today]);

  return { todayMood, setMood, isLoaded, entries: moodData.entries };
}
