/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * useHowTheyDidIt — state for the "How They Did It" card deck.
 * Owns progress/{uid}.howTheyDidIt (additive-merge namespace, same pattern as
 * the other Innovation tools — no Firestore rules change).
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { doc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { reportSaveError } from '../utils/logError';
import { useFreshProgress } from './useFreshProgress';
import { type HowTheyDidItState } from '../types/howTheyDidIt';

const EMPTY: HowTheyDidItState = { seenIds: [], savedIds: [], updatedAt: '' };
const add = (arr: string[], v: string) => (arr.includes(v) ? arr : [...arr, v]);

export function useHowTheyDidIt(uid?: string) {
  const { doc: rawProgressDoc, loaded: progressLoaded } = useFreshProgress(uid);
  const [state, setState] = useState<HowTheyDidItState>(EMPTY);
  const [isLoaded, setIsLoaded] = useState(false);
  const seededRef = useRef(false);

  useEffect(() => { seededRef.current = false; }, [uid]);

  useEffect(() => {
    if (!progressLoaded || seededRef.current) return;
    const saved = rawProgressDoc?.howTheyDidIt as HowTheyDidItState | undefined;
    setState(saved ? { ...EMPTY, ...saved } : EMPTY);
    setIsLoaded(true);
    seededRef.current = true;
  }, [progressLoaded, rawProgressDoc, uid]);

  const persist = useCallback((next: HowTheyDidItState) => {
    if (uid) setDoc(doc(db, 'progress', uid), { howTheyDidIt: next }, { merge: true }).catch((e) => reportSaveError('useHowTheyDidIt.save', e));
  }, [uid]);

  const markSeen = useCallback((id: string) => {
    setState(prev => {
      if (prev.seenIds.includes(id)) return prev;
      const next = { ...prev, seenIds: add(prev.seenIds, id), updatedAt: new Date().toISOString() };
      persist(next);
      return next;
    });
  }, [persist]);

  const toggleSaved = useCallback((id: string) => {
    setState(prev => {
      const savedIds = prev.savedIds.includes(id) ? prev.savedIds.filter(x => x !== id) : [...prev.savedIds, id];
      const next = { ...prev, savedIds, updatedAt: new Date().toISOString() };
      persist(next);
      return next;
    });
  }, [persist]);

  return { state, isLoaded, markSeen, toggleSaved };
}
