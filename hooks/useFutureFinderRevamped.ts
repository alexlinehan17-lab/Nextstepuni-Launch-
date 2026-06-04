/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * useFutureFinderRevamped — state for the RIASEC-based "Future Finder Revamped"
 * tool. Owns progress/{uid}.futureFinderRevamped (its OWN namespace — separate
 * from the original tool's `futureFinder` field, so both coexist with no clash).
 *
 * Loads FRESH from Firestore on every mount (getDoc), the way the original
 * Future Finder does — NOT from the shared progress context. The context's
 * snapshot is taken once at app start and isn't refreshed after this tool writes
 * results, so seeding from it made the tool "restart" (lose its results) whenever
 * the student left and came back in the same session. A direct read guarantees
 * the latest saved results are always restored.
 */
import { useState, useEffect, useCallback } from 'react';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { reportSaveError, logError } from '../utils/logError';

export interface FutureFinderRevampedState {
  length: 'full' | 'quick';
  /** RIASEC item id -> 1..5 (dislike→like). */
  responses: Record<string, number>;
  /** work-value item id -> 1..5 (not important→very important). */
  valueResponses: Record<string, number>;
  /** Saved-pick course codes (the shared results UI's "Save to Picks"). */
  picks?: string[];
  /** Course codes selected for the compare view. */
  compareCodes?: string[];
  completedAt: string;
  updatedAt: string;
}

export function useFutureFinderRevamped(uid?: string) {
  const [saved, setSaved] = useState<FutureFinderRevampedState | null>(null);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    let cancelled = false;
    setIsLoaded(false);
    if (!uid) { setSaved(null); setIsLoaded(true); return; }
    getDoc(doc(db, 'progress', uid))
      .then((snap) => {
        if (cancelled) return;
        setSaved((snap.data()?.futureFinderRevamped as FutureFinderRevampedState) ?? null);
        setIsLoaded(true);
      })
      .catch((e) => { logError('useFutureFinderRevamped.load', e); if (!cancelled) { setSaved(null); setIsLoaded(true); } });
    return () => { cancelled = true; };
  }, [uid]);

  const persist = useCallback((next: FutureFinderRevampedState) => {
    setSaved(next);
    if (uid) setDoc(doc(db, 'progress', uid), { futureFinderRevamped: next }, { merge: true }).catch((e) => reportSaveError('useFutureFinderRevamped.save', e));
  }, [uid]);

  const reset = useCallback(() => {
    setSaved(null);
    if (uid) setDoc(doc(db, 'progress', uid), { futureFinderRevamped: null }, { merge: true }).catch((e) => reportSaveError('useFutureFinderRevamped.save', e));
  }, [uid]);

  return { saved, isLoaded, persist, reset };
}
