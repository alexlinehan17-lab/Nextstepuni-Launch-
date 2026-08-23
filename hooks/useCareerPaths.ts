/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * useCareerPaths — state for the "Career Paths" card deck.
 * Owns progress/{uid}.careerPaths (additive-merge namespace, same pattern as
 * the other Innovation tools — no Firestore rules change).
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { doc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { useFreshProgress } from './useFreshProgress';
import { type CareerPathsState } from '../types/careerPaths';
import { reportSaveError } from '../utils/logError';
import { useProgress } from '../contexts/ProgressContext';
import { DEMO_STUDENT_UID } from '../data/devStudent';

const EMPTY: CareerPathsState = { seenIds: [], savedIds: [], shiftRatings: {}, updatedAt: '' };
const add = (arr: string[], v: string) => (arr.includes(v) ? arr : [...arr, v]);

export function useCareerPaths(uid?: string) {
  const { updateDemoProgress } = useProgress();
  const isDemo = uid === DEMO_STUDENT_UID;
  const { doc: rawProgressDoc, loaded: progressLoaded } = useFreshProgress(uid);
  const [state, setState] = useState<CareerPathsState>(EMPTY);
  const [isLoaded, setIsLoaded] = useState(false);
  const seededRef = useRef(false);

  useEffect(() => { seededRef.current = false; }, [uid]);

  useEffect(() => {
    if (!progressLoaded || seededRef.current) return;
    const saved = rawProgressDoc?.careerPaths as CareerPathsState | undefined;
    setState(saved ? { ...EMPTY, ...saved } : EMPTY);
    setIsLoaded(true);
    seededRef.current = true;
  }, [progressLoaded, rawProgressDoc, uid]);

  const persist = useCallback((next: CareerPathsState) => {
    if (!uid) return;
    if (isDemo) updateDemoProgress(current => ({ ...current, careerPaths: next }));
    else setDoc(doc(db, 'progress', uid), { careerPaths: next }, { merge: true }).catch((e) => reportSaveError('useCareerPaths.save', e));
  }, [uid, isDemo, updateDemoProgress]);

  const markSeen = useCallback((id: string) => {
    setState((prev) => {
      if (prev.seenIds.includes(id)) return prev;
      const next = { ...prev, seenIds: add(prev.seenIds, id), updatedAt: new Date().toISOString() };
      persist(next);
      return next;
    });
  }, [persist]);

  const toggleSaved = useCallback((id: string) => {
    setState((prev) => {
      const savedIds = prev.savedIds.includes(id) ? prev.savedIds.filter((x) => x !== id) : [...prev.savedIds, id];
      const next = { ...prev, savedIds, updatedAt: new Date().toISOString() };
      persist(next);
      return next;
    });
  }, [persist]);

  /** "Could I see myself doing this?" 1–5 self-rating from the Day-in-the-Life sim. */
  const setShiftRating = useCallback((id: string, rating: number) => {
    setState((prev) => {
      const next = { ...prev, shiftRatings: { ...(prev.shiftRatings ?? {}), [id]: rating }, updatedAt: new Date().toISOString() };
      persist(next);
      return next;
    });
  }, [persist]);

  return { state, isLoaded, markSeen, toggleSaved, setShiftRating };
}
