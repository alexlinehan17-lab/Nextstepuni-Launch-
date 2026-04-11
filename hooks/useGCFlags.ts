/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback } from 'react';
import { db } from '../firebase';
import { collection, getDocs, doc, setDoc, deleteDoc, Timestamp } from 'firebase/firestore';

// ─── Types ──────────────────────────────────────────────────────────────────

export type FlagPriority = 'normal' | 'high';

export interface FlagData {
  studentUid: string;
  flaggedAt: number; // millis
  note: string;
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
            note: data.note ?? '',
            priority: data.priority === 'high' ? 'high' : 'normal',
          };
        });
        setFlags(loaded);
      } catch {
        // Permission error or collection doesn't exist yet
      }
      if (!cancelled) setIsLoaded(true);
    };
    load();

    return () => { cancelled = true; };
  }, [gcUid]);

  const flagStudent = useCallback(async (studentUid: string, note?: string, priority?: FlagPriority) => {
    if (!gcUid) return;
    const data: FlagData = {
      studentUid,
      flaggedAt: Date.now(),
      note: note ?? '',
      priority: priority ?? 'normal',
    };
    setFlags(prev => ({ ...prev, [studentUid]: data }));
    try {
      await setDoc(doc(db, 'gcFlags', gcUid, 'flaggedStudents', studentUid), {
        studentUid,
        flaggedAt: Timestamp.now(),
        note: data.note,
        priority: data.priority,
      });
    } catch {
      console.error('[useGCFlags] Failed to flag student:');
    }
  }, [gcUid]);

  const unflagStudent = useCallback(async (studentUid: string) => {
    if (!gcUid) return;
    setFlags(prev => {
      const next = { ...prev };
      delete next[studentUid];
      return next;
    });
    try {
      await deleteDoc(doc(db, 'gcFlags', gcUid, 'flaggedStudents', studentUid));
    } catch {
      console.error('[useGCFlags] Failed to unflag student:');
    }
  }, [gcUid]);

  const updateFlagNote = useCallback(async (studentUid: string, note: string) => {
    if (!gcUid) return;
    setFlags(prev => {
      const existing = prev[studentUid];
      if (!existing) return prev;
      return { ...prev, [studentUid]: { ...existing, note } };
    });
    try {
      await setDoc(doc(db, 'gcFlags', gcUid, 'flaggedStudents', studentUid), { note }, { merge: true });
    } catch {
      console.error('[useGCFlags] Failed to update flag note:');
    }
  }, [gcUid]);

  const updateFlagPriority = useCallback(async (studentUid: string, priority: FlagPriority) => {
    if (!gcUid) return;
    setFlags(prev => {
      const existing = prev[studentUid];
      if (!existing) return prev;
      return { ...prev, [studentUid]: { ...existing, priority } };
    });
    try {
      await setDoc(doc(db, 'gcFlags', gcUid, 'flaggedStudents', studentUid), { priority }, { merge: true });
    } catch {
      console.error('[useGCFlags] Failed to update flag priority:');
    }
  }, [gcUid]);

  const isFlagged = useCallback((studentUid: string) => studentUid in flags, [flags]);

  const getFlagData = useCallback((studentUid: string): FlagData | null => flags[studentUid] ?? null, [flags]);

  const flaggedStudentUids = Object.keys(flags);

  return {
    flags,
    isLoaded,
    flagStudent,
    unflagStudent,
    updateFlagNote,
    updateFlagPriority,
    isFlagged,
    getFlagData,
    flaggedStudentUids,
  };
}
