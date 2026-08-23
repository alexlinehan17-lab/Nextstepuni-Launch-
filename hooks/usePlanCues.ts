/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * usePlanCues — per-block implementation-intention cues for the planner
 * ("The Intention Engine"). Owns the `planCues` field on progress/{uid}
 * (additive-merge namespace, getDoc-on-mount via useFreshProgress — same
 * seed-once-then-local-authoritative pattern as useCatchUpLane / useExamReps,
 * no Firestore rules change). Keyed by the block's stable getBlockId, so a cue
 * follows the recurring block ("when I get home, then I'll do my Maths block").
 */
import { useState, useEffect, useCallback, useRef } from 'react';
import { doc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { useFreshProgress } from './useFreshProgress';
import { reportSaveError } from '../utils/logError';
import { useProgress } from '../contexts/ProgressContext';
import { DEMO_STUDENT_UID } from '../data/devStudent';

export interface PlanCue {
  /** Fixed situational trigger, e.g. "When I get home and drop my bag". */
  trigger: string;
  /** The student's own "…then I will…" line. */
  then: string;
}
export type PlanCues = Record<string, PlanCue>;

export function usePlanCues(uid?: string) {
  const { doc: rawProgressDoc, loaded } = useFreshProgress(uid);
  const { updateDemoProgress } = useProgress();
  const isDemo = uid === DEMO_STUDENT_UID;
  const [cues, setCues] = useState<PlanCues>({});
  const [isLoaded, setIsLoaded] = useState(false);
  const seededRef = useRef(false);

  useEffect(() => { seededRef.current = false; }, [uid]);

  useEffect(() => {
    if (!loaded || seededRef.current) return;
    const saved = rawProgressDoc?.planCues as PlanCues | undefined;
    setCues(saved && typeof saved === 'object' ? saved : {});
    setIsLoaded(true);
    seededRef.current = true;
  }, [loaded, rawProgressDoc, uid]);

  /** Set (or clear, via empty strings) the cue for one block. Persists. */
  const setCue = useCallback((blockId: string, cue: PlanCue) => {
    setCues(prev => {
      const next: PlanCues = { ...prev, [blockId]: cue };
      if (isDemo) {
        updateDemoProgress(current => ({ ...current, planCues: next }));
      } else if (uid) {
        setDoc(doc(db, 'progress', uid), { planCues: next }, { merge: true }).catch((e) => reportSaveError('usePlanCues.save', e));
      }
      return next;
    });
  }, [uid, isDemo, updateDemoProgress]);

  return { cues, isLoaded, setCue };
}
