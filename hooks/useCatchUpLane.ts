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
import { type CatchUpLaneState, type ComebackPlan, type FirstWeekDayProgress } from '../types/catchUpLane';
import { RECOVERY_CARDS } from '../catchUpLaneData';
import { reportSaveError } from '../utils/logError';
import { useProgress } from '../contexts/ProgressContext';
import { DEMO_STUDENT_UID } from '../data/devStudent';

const EMPTY: CatchUpLaneState = {
  recoveredTopicIds: [],
  shakyTopicIds: [],
  attempts: 0,
  absences: [],
  updatedAt: '',
};

export function useCatchUpLane(uid?: string) {
  const { doc: rawProgressDoc, loaded: progressLoaded } = useFreshProgress(uid);
  const { updateDemoProgress } = useProgress();
  const isDemo = uid === DEMO_STUDENT_UID;
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
    if (isDemo) {
      updateDemoProgress(current => ({ ...current, catchUpLane: next }));
    } else if (uid) {
      setDoc(doc(db, 'progress', uid), { catchUpLane: next }, { merge: true }).catch((e) => reportSaveError('useCatchUpLane.save', e));
    }
  }, [uid, isDemo, updateDemoProgress]);

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

  // Arm 2: save the student's re-entry plan (stamps savedAt). Preserve any
  // First-Week-Back timeline the student has already completed — the incoming
  // `plan` from Comeback.finish() carries no `firstWeek`, so without this a
  // "Redo my plan" would silently wipe their day-by-day progress.
  const saveComeback = useCallback((plan: Omit<ComebackPlan, 'savedAt'>) => {
    setState(prev => {
      const next: CatchUpLaneState = {
        ...prev,
        comeback: {
          ...plan,
          savedAt: new Date().toISOString(),
          ...(prev.comeback?.firstWeek ? { firstWeek: prev.comeback.firstWeek } : {}),
        },
        updatedAt: new Date().toISOString(),
      };
      persist(next);
      return next;
    });
  }, [persist]);

  // Arm 2 timeline: patch one day of the First-Week-Back walk. Lazily creates
  // the firstWeek object on the saved plan (no-op if no plan is saved yet).
  const setFirstWeekDay = useCallback((day: number, patch: Partial<FirstWeekDayProgress>) => {
    setState(prev => {
      if (!prev.comeback) return prev;
      const fw = prev.comeback.firstWeek ?? { startedAt: new Date().toISOString(), days: {} };
      const next: CatchUpLaneState = {
        ...prev,
        comeback: {
          ...prev.comeback,
          firstWeek: {
            ...fw,
            days: { ...fw.days, [day]: { ...fw.days[day], ...patch } },
          },
        },
        updatedAt: new Date().toISOString(),
      };
      persist(next);
      return next;
    });
  }, [persist]);

  // Total marks "protected" so far — conservative sum of recovered topics'
  // weights. Many topics have multiple recovery cards sharing one topicId, so we
  // count each recovered TOPIC once (not once per card) to avoid inflating the
  // figure many-fold.
  const marksProtected = useMemo(() => {
    const weightByTopic = new Map<string, number>();
    for (const c of RECOVERY_CARDS) {
      if (!weightByTopic.has(c.topicId)) weightByTopic.set(c.topicId, c.marksWeight);
    }
    return state.recoveredTopicIds.reduce((sum, id) => sum + (weightByTopic.get(id) ?? 0), 0);
  }, [state.recoveredTopicIds]);

  return { state, isLoaded, markRecovered, markShaky, logAbsence, saveComeback, setFirstWeekDay, marksProtected };
}
