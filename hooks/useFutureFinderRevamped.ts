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
  /** The algorithm's top-10 ranked course codes, captured when the quiz
   *  completes. Distinct from `picks`, which are the student's explicit
   *  bookmarks — most students never bookmark anything, so without this the
   *  results the student actually read were never persisted and every
   *  downstream consumer (Your Possible Life, War Room, the GC dashboard) saw
   *  an empty list. */
  topMatches?: string[];
  /** Course codes selected for the compare view. */
  compareCodes?: string[];
  completedAt: string;
  updatedAt: string;
}

const cacheKey = (uid: string) => `nextstepuni:future-finder:v1:${uid}`;

function readCached(uid?: string): FutureFinderRevampedState | null {
  if (!uid) return null;
  try {
    const value = JSON.parse(localStorage.getItem(cacheKey(uid)) ?? 'null') as FutureFinderRevampedState | null;
    return value?.completedAt ? value : null;
  } catch {
    return null;
  }
}

function writeCached(uid: string | undefined, value: FutureFinderRevampedState | null): void {
  if (!uid) return;
  try {
    if (value) localStorage.setItem(cacheKey(uid), JSON.stringify(value));
    else localStorage.removeItem(cacheKey(uid));
  } catch { /* storage may be unavailable */ }
}

export function useFutureFinderRevamped(uid?: string) {
  // The device cache is the hot path. This prevents an immediate exit/re-entry
  // from racing Firestore's async snapshot inside a native WebView.
  const [saved, setSaved] = useState<FutureFinderRevampedState | null>(() => readCached(uid));
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    let cancelled = false;
    setIsLoaded(false);
    if (!uid) { setSaved(null); setIsLoaded(true); return; }
    getDoc(doc(db, 'progress', uid))
      .then((snap) => {
        if (cancelled) return;
        const remote = (snap.data()?.futureFinderRevamped as FutureFinderRevampedState) ?? null;
        if (remote?.completedAt) {
          setSaved(remote);
          writeCached(uid, remote);
        }
        setIsLoaded(true);
      })
      .catch((e) => { logError('useFutureFinderRevamped.load', e); if (!cancelled) setIsLoaded(true); });
    return () => { cancelled = true; };
  }, [uid]);

  const persist = useCallback((next: FutureFinderRevampedState) => {
    setSaved(next);
    writeCached(uid, next);
    if (uid) setDoc(doc(db, 'progress', uid), { futureFinderRevamped: next }, { merge: true }).catch((e) => reportSaveError('useFutureFinderRevamped.save', e));
  }, [uid]);

  const reset = useCallback(() => {
    setSaved(null);
    writeCached(uid, null);
    if (uid) setDoc(doc(db, 'progress', uid), { futureFinderRevamped: null }, { merge: true }).catch((e) => reportSaveError('useFutureFinderRevamped.save', e));
  }, [uid]);

  return { saved, isLoaded, persist, reset };
}
