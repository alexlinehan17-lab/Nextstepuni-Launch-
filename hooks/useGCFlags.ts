/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback } from 'react';
import { db } from '../firebase';
import { saveInBackground } from '../utils/firestoreWrite';
import { collection, getDocs, doc, setDoc, deleteDoc, Timestamp } from 'firebase/firestore';

// ─── Types ──────────────────────────────────────────────────────────────────

export type FlagPriority = 'normal' | 'high';

export interface FlagData {
  studentUid: string;
  flaggedAt: number; // millis
  priority: FlagPriority;
}

// ─── Hook ───────────────────────────────────────────────────────────────────

export function useGCFlags(gcUid: string | undefined) {
  const [flags, setFlags] = useState<Record<string, FlagData>>({});
  const [isLoaded, setIsLoaded] = useState(false);

  // Load all flags on mount
  useEffect(() => {
    if (!gcUid) return;
    let cancelled = false;

    const load = async () => {
      try {
        const snap = await getDocs(collection(db, 'gcFlags', gcUid, 'flaggedStudents'));
        if (cancelled) return;
        const loaded: Record<string, FlagData> = {};
        snap.docs.forEach(d => {
          const data = d.data();
          loaded[d.id] = {
            studentUid: d.id,
            flaggedAt: data.flaggedAt?.toMillis?.() ?? data.flaggedAt ?? Date.now(),
            priority: data.priority === 'high' ? 'high' : 'normal',
          };
        });
        setFlags(loaded);
      } catch (err) {
        console.error('[useGCFlags] Failed to load flags:', err);
      }
      if (!cancelled) setIsLoaded(true);
    };
    load();

    return () => { cancelled = true; };
  }, [gcUid]);

  const flagStudent = useCallback(async (studentUid: string, priority?: FlagPriority) => {
    if (!gcUid) return;
    const data: FlagData = {
      studentUid,
      flaggedAt: Date.now(),
      priority: priority ?? 'normal',
    };
    // The optimistic update was already here, but the awaited write had no
    // rollback — so a rules rejection left the flag showing as saved when it
    // wasn't. (Offline the await never settles at all, so the catch was dead.)
    const previous = flags[studentUid];
    setFlags(prev => ({ ...prev, [studentUid]: data }));
    saveInBackground(
      setDoc(doc(db, 'gcFlags', gcUid, 'flaggedStudents', studentUid), {
        studentUid,
        flaggedAt: Timestamp.now(),
        priority: data.priority,
      }),
      'useGCFlags.flagStudent',
      () => setFlags(prev => {
        const next = { ...prev };
        if (previous) next[studentUid] = previous; else delete next[studentUid];
        return next;
      }),
    );
  }, [gcUid, flags]);

  const unflagStudent = useCallback(async (studentUid: string) => {
    if (!gcUid) return;
    const previous = flags[studentUid];
    setFlags(prev => {
      const next = { ...prev };
      delete next[studentUid];
      return next;
    });
    saveInBackground(
      deleteDoc(doc(db, 'gcFlags', gcUid, 'flaggedStudents', studentUid)),
      'useGCFlags.unflagStudent',
      () => { if (previous) setFlags(prev => ({ ...prev, [studentUid]: previous })); },
    );
  }, [gcUid, flags]);

  const updateFlagPriority = useCallback(async (studentUid: string, priority: FlagPriority) => {
    if (!gcUid) return;
    const previousPriority = flags[studentUid]?.priority;
    setFlags(prev => {
      const existing = prev[studentUid];
      if (!existing) return prev;
      return { ...prev, [studentUid]: { ...existing, priority } };
    });
    saveInBackground(
      setDoc(doc(db, 'gcFlags', gcUid, 'flaggedStudents', studentUid), { priority }, { merge: true }),
      'useGCFlags.updateFlagPriority',
      () => setFlags(prev => {
        const existing = prev[studentUid];
        if (!existing || !previousPriority) return prev;
        return { ...prev, [studentUid]: { ...existing, priority: previousPriority } };
      }),
    );
  }, [gcUid, flags]);

  const isFlagged = useCallback((studentUid: string) => studentUid in flags, [flags]);

  const getFlagData = useCallback((studentUid: string): FlagData | null => flags[studentUid] ?? null, [flags]);

  const flaggedStudentUids = Object.keys(flags);

  return {
    flags,
    isLoaded,
    flagStudent,
    unflagStudent,
    updateFlagPriority,
    isFlagged,
    getFlagData,
    flaggedStudentUids,
  };
}
