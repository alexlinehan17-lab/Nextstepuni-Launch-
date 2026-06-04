/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * useEffortLifeSim — state for the "Your Possible Life" tool. Owns
 * progress/{uid}.effortLifeSim (its OWN additive-merge namespace, the same
 * pattern as careerPaths / futureFinderRevamped — no Firestore rules change,
 * coexists cleanly with every other tool's field).
 */
import { useState, useEffect, useCallback, useRef } from 'react';
import { doc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { useFreshProgress } from './useFreshProgress';
import { type LifeRegion } from '../components/effortLifeModel';
import { reportSaveError } from '../utils/logError';

export interface EffortLifeSimState {
  /** The career id the student is exploring (from CAREERS). */
  careerId?: string;
  /** Region lens for the lifestyle picture. */
  region?: LifeRegion;
  /** Horizon shown: starting out vs a few years in. */
  horizon?: 'start' | 'experienced';
  /** The self-transcendent "why" reflection (optional, student-authored). */
  why?: string;
  updatedAt: string;
}

export function useEffortLifeSim(uid?: string) {
  const { doc: rawProgressDoc, loaded: progressLoaded } = useFreshProgress(uid);
  const [saved, setSaved] = useState<EffortLifeSimState | null>(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const seededRef = useRef(false);

  useEffect(() => { seededRef.current = false; setIsLoaded(false); }, [uid]);

  useEffect(() => {
    if (!progressLoaded || seededRef.current) return;
    setSaved((rawProgressDoc?.effortLifeSim as EffortLifeSimState) ?? null);
    seededRef.current = true;
    setIsLoaded(true);
  }, [progressLoaded, rawProgressDoc]);

  const save = useCallback((patch: Partial<EffortLifeSimState>) => {
    setSaved((prev) => {
      const next: EffortLifeSimState = { ...(prev ?? {}), ...patch, updatedAt: new Date().toISOString() };
      if (uid) setDoc(doc(db, 'progress', uid), { effortLifeSim: next }, { merge: true }).catch((e) => reportSaveError('useEffortLifeSim.save', e));
      return next;
    });
  }, [uid]);

  const reset = useCallback(() => {
    setSaved(null);
    if (uid) setDoc(doc(db, 'progress', uid), { effortLifeSim: null }, { merge: true }).catch((e) => reportSaveError('useEffortLifeSim.save', e));
  }, [uid]);

  return { saved, isLoaded, save, reset };
}
