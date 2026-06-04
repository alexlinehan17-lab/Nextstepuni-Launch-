/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * useExamReps — owns the `examReps` field on the shared progress/{uid} doc.
 * Modelled on useMockResults. Tracks the all-time "marks banked" tally, the
 * cards seen (so the picker can interleave fresh questions), and the cards
 * where ribbons were missed (leaks, for future spaced resurfacing).
 *
 * Additive merge writes scoped to the `examReps` namespace — no firestore.rules
 * change, can't touch gamification invariants.
 */
import { useState, useEffect, useCallback, useRef } from 'react';
import { doc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { useFreshProgress } from './useFreshProgress';
import { type RepSelection } from '../types/examReps';

export interface ExamRepsState {
  /** All-time marks captured across every rep (the competence tally). */
  banked: number;
  attempts: number;
  seenCardIds: string[];
  /** Card ids where the student missed ≥1 ribbon — for later resurfacing. */
  leakCardIds: string[];
  /** The student's current Subject → Level → Topic selection. */
  selection?: RepSelection;
  updatedAt: string;
}

const EMPTY: ExamRepsState = { banked: 0, attempts: 0, seenCardIds: [], leakCardIds: [], updatedAt: '' };

export interface RepResult {
  cardId: string;
  capturedMarks: number;
  missedRibbons: number;
}

export function useExamReps(uid: string | undefined) {
  const { doc: rawProgressDoc, loaded: progressLoaded } = useFreshProgress(uid);
  const [state, setState] = useState<ExamRepsState>(EMPTY);
  const [isLoaded, setIsLoaded] = useState(false);
  const seededRef = useRef(false);

  useEffect(() => {
    seededRef.current = false;
    setIsLoaded(false);
  }, [uid]);

  useEffect(() => {
    if (!progressLoaded || seededRef.current) return;
    const saved = rawProgressDoc?.examReps as ExamRepsState | undefined;
    if (saved) {
      setState({
        ...EMPTY,
        ...saved,
        seenCardIds: [...(saved.seenCardIds ?? [])],
        leakCardIds: [...(saved.leakCardIds ?? [])],
      });
    }
    seededRef.current = true;
    setIsLoaded(true);
  }, [progressLoaded, rawProgressDoc]);

  /** Record one completed rep. Updates the all-time tally and persists. */
  const recordRep = useCallback((result: RepResult) => {
    setState(prev => {
      const seen = prev.seenCardIds.includes(result.cardId) ? prev.seenCardIds : [...prev.seenCardIds, result.cardId];
      const leaks = result.missedRibbons > 0 && !prev.leakCardIds.includes(result.cardId)
        ? [...prev.leakCardIds, result.cardId]
        : prev.leakCardIds.filter(id => result.missedRibbons > 0 || id !== result.cardId);
      const next: ExamRepsState = {
        ...prev, // preserve selection + any other fields
        banked: prev.banked + Math.max(0, result.capturedMarks),
        attempts: prev.attempts + 1,
        seenCardIds: seen,
        leakCardIds: leaks,
        updatedAt: new Date().toISOString(),
      };
      if (uid) {
        setDoc(doc(db, 'progress', uid), { examReps: next }, { merge: true }).catch(() => {});
      }
      return next;
    });
  }, [uid]);

  /** Persist the student's Subject → Level → Topic selection. */
  const setSelection = useCallback((selection: RepSelection) => {
    setState(prev => {
      const next = { ...prev, selection, updatedAt: new Date().toISOString() };
      if (uid) setDoc(doc(db, 'progress', uid), { examReps: next }, { merge: true }).catch(() => {});
      return next;
    });
  }, [uid]);

  return { state, isLoaded, recordRep, setSelection };
}
