/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * useFutureFinderRevamped — state for the RIASEC-based "Future Finder Revamped"
 * tool. Owns progress/{uid}.futureFinderRevamped (its OWN namespace — separate
 * from the original tool's `futureFinder` field, so both coexist with no clash).
 */
import { useState, useEffect, useCallback, useRef } from 'react';
import { doc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { useProgress } from '../contexts/ProgressContext';

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
  const { rawProgressDoc, progressLoaded } = useProgress();
  const [saved, setSaved] = useState<FutureFinderRevampedState | null>(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const seededRef = useRef(false);

  useEffect(() => { seededRef.current = false; setIsLoaded(false); }, [uid]);

  useEffect(() => {
    if (!progressLoaded || seededRef.current) return;
    setSaved((rawProgressDoc?.futureFinderRevamped as FutureFinderRevampedState) ?? null);
    seededRef.current = true;
    setIsLoaded(true);
  }, [progressLoaded, rawProgressDoc]);

  const persist = useCallback((next: FutureFinderRevampedState) => {
    setSaved(next);
    if (uid) setDoc(doc(db, 'progress', uid), { futureFinderRevamped: next }, { merge: true }).catch(() => {});
  }, [uid]);

  const reset = useCallback(() => {
    setSaved(null);
    if (uid) setDoc(doc(db, 'progress', uid), { futureFinderRevamped: null }, { merge: true }).catch(() => {});
  }, [uid]);

  return { saved, isLoaded, persist, reset };
}
