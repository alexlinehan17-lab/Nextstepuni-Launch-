/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * useCatchUpLane — state for the Catch-Up Lane absence-recovery tool.
 *
 * Owns the `catchUpLane` field on progress/{uid} (additive-merge namespace,
 * same pattern as useExamReps / useTopicMastery — no Firestore rules change).
 * Seeds once from the ProgressContext raw doc, then is the local source of
 * truth for the session.
 */

import { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import { doc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { useFreshProgress } from './useFreshProgress';
import { type CatchUpLaneState, type ComebackPlan } from '../types/catchUpLane';
import { RECOVERY_CARDS } from '../catchUpLaneData';

const EMPTY: CatchUpLaneState = {
  recoveredTopicIds: [],
  shakyTopicIds: [],
  attempts: 0,
  absences: [],
  updatedAt: '',
};

export function useCatchUpLane(uid?: string) {
  const { doc: rawProgressDoc, loaded: progressLoaded } = useFreshProgress(uid);
  const [state, setState] = useState<CatchUpLaneState>(EMPTY);
  const [isLoaded, setIsLoaded] = useState(false);
  const seededRef = useRef(false);

  // Re-seed when the user changes.
  useEffect(() => { seededRef.current = false; }, [uid]);

  // Seed once from the persisted doc. We don't re-seed on later rawProgressDoc
  // changes because local state is authoritative after a write (the doc only
  // refreshes on an explicit reloadProgress()).
  useEffect(() => {
    if (!progressLoaded || seededRef.current) return;
    const saved = rawProgressDoc?.catchUpLane as CatchUpLaneState | undefined;
    setState(saved ? { ...EMPTY, ...saved } : EMPTY);
    setIsLoaded(true);
    seededRef.current = true;
  }, [progressLoaded, rawProgressDoc, uid]);

  const persist = useCallback((next: CatchUpLaneState) => {
    if (uid) {
      setDoc(doc(db, 'progress', uid), { catchUpLane: next }, { merge: true }).catch(() => {});
    }
  }, [uid]);

  const markRecovered = useCallback((topicId: string) => {
    setState(prev => {
      const next: CatchUpLaneState = {
        ...prev,
        recoveredTopicIds: prev.recoveredTopicIds.includes(topicId)
          ? prev.recoveredTopicIds
          : [...prev.recoveredTopicIds, topicId],
        shakyTopicIds: prev.shakyTopicIds.filter(t => t !== topicId),
        attempts: prev.attempts + 1,
        updatedAt: new Date().toISOString(),
      };
      persist(next);
      return next;
    });
  }, [persist]);

  const markShaky = useCallback((topicId: string) => {
    setState(prev => {
      const next: CatchUpLaneState = {
        ...prev,
        shakyTopicIds: prev.shakyTopicIds.includes(topicId)
          ? prev.shakyTopicIds
          : [...prev.shakyTopicIds, topicId],
        // a "still shaky" topic is no longer counted as recovered
        recoveredTopicIds: prev.recoveredTopicIds.filter(t => t !== topicId),
        attempts: prev.attempts + 1,
        updatedAt: new Date().toISOString(),
      };
      persist(next);
      return next;
    });
  }, [persist]);

  const logAbsence = useCallback((dateKey: string, subjectIds: string[]) => {
    setState(prev => {
      const next: CatchUpLaneState = {
        ...prev,
        absences: [...prev.absences, { dateKey, subjectIds }],
        updatedAt: new Date().toISOString(),
      };
      persist(next);
      return next;
    });
  }, [persist]);

  // Arm 2: save the student's re-entry plan (stamps savedAt).
  const saveComeback = useCallback((plan: Omit<ComebackPlan, 'savedAt'>) => {
    setState(prev => {
      const next: CatchUpLaneState = {
        ...prev,
        comeback: { ...plan, savedAt: new Date().toISOString() },
        updatedAt: new Date().toISOString(),
      };
      persist(next);
      return next;
    });
  }, [persist]);

  // Total marks "protected" so far — conservative sum of recovered topics' weights.
  const marksProtected = useMemo(() => {
    const recovered = new Set(state.recoveredTopicIds);
    return RECOVERY_CARDS.reduce((sum, c) => sum + (recovered.has(c.topicId) ? c.marksWeight : 0), 0);
  }, [state.recoveredTopicIds]);

  return { state, isLoaded, markRecovered, markShaky, logAbsence, saveComeback, marksProtected };
}
