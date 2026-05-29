/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * useCollegeCompass — owns the `collegeCompass` field on the shared
 * progress/{uid} Firestore doc. Modelled on useMockResults.
 *
 * Writes are additive merge writes scoped to the `collegeCompass` namespace —
 * they never touch pointsData/gamification, so they can't violate the strict
 * progress-doc invariants in firestore.rules, and need NO rules change.
 * Checklist toggles are debounced; a pending write is flushed on unmount so
 * the last toggle isn't lost when the student navigates back out of the tool.
 */
import { useState, useEffect, useCallback, useRef } from 'react';
import { doc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { useProgress } from '../contexts/ProgressContext';
import { type CollegeCompassState } from '../types';

const EMPTY: CollegeCompassState = { checklist: {}, updatedAt: '' };
const DEBOUNCE_MS = 1500;

/** Firestore rejects `undefined` values — drop any undefined keys before write. */
function stripUndefined<T extends Record<string, unknown>>(obj: T): T {
  const out: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(obj)) {
    if (v !== undefined) out[k] = v;
  }
  return out as T;
}

export function useCollegeCompass(uid: string | undefined) {
  const { rawProgressDoc, progressLoaded } = useProgress();
  const [state, setState] = useState<CollegeCompassState>(EMPTY);
  const [isLoaded, setIsLoaded] = useState(false);

  const seededRef = useRef(false);
  const writeTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const pendingWrite = useRef<(() => void) | null>(null);

  // Re-seed when the user changes.
  useEffect(() => {
    seededRef.current = false;
    setIsLoaded(false);
  }, [uid]);

  // Seed local state from the raw progress doc, once, after progress loads.
  useEffect(() => {
    if (!progressLoaded || seededRef.current) return;
    const saved = rawProgressDoc?.collegeCompass as CollegeCompassState | undefined;
    if (saved) setState({ ...EMPTY, ...saved, checklist: { ...(saved.checklist ?? {}) } });
    seededRef.current = true;
    setIsLoaded(true);
  }, [progressLoaded, rawProgressDoc]);

  // Flush any pending debounced write on unmount (navigating back out).
  useEffect(() => () => {
    if (writeTimer.current) clearTimeout(writeTimer.current);
    if (pendingWrite.current) pendingWrite.current();
  }, []);

  const persist = useCallback((next: CollegeCompassState, debounce: boolean) => {
    if (!uid) return;
    const payload = stripUndefined({ ...next, updatedAt: new Date().toISOString() });
    const write = () => {
      pendingWrite.current = null;
      writeTimer.current = null;
      setDoc(doc(db, 'progress', uid), { collegeCompass: payload }, { merge: true }).catch(() => {});
    };
    if (writeTimer.current) clearTimeout(writeTimer.current);
    if (debounce) {
      pendingWrite.current = write;
      writeTimer.current = setTimeout(write, DEBOUNCE_MS);
    } else {
      pendingWrite.current = null;
      write();
    }
  }, [uid]);

  /** Toggle a checklist item. `key` should be namespaced "<stopId>:<itemId>". */
  const toggleChecklistItem = useCallback((key: string) => {
    setState(prev => {
      const checklist = { ...prev.checklist };
      if (checklist[key]) delete checklist[key];
      else checklist[key] = true;
      const next = { ...prev, checklist };
      persist(next, true);
      return next;
    });
  }, [persist]);

  const setHearIndicators = useCallback((ids: string[]) => {
    setState(prev => {
      const next = { ...prev, hearIndicators: ids };
      persist(next, true);
      return next;
    });
  }, [persist]);

  const setDareCategory = useCallback((id: string | undefined) => {
    setState(prev => {
      const next = { ...prev, dareCategoryId: id };
      persist(next, false);
      return next;
    });
  }, [persist]);

  const setTargetInstitutions = useCallback((codes: string[]) => {
    setState(prev => {
      const next = { ...prev, targetInstitutionCodes: codes };
      persist(next, false);
      return next;
    });
  }, [persist]);

  /** Hide / restore a stop (e.g. DARE when not applicable). */
  const toggleDismissStop = useCallback((stopId: string) => {
    setState(prev => {
      const set = new Set(prev.dismissedStops ?? []);
      if (set.has(stopId)) set.delete(stopId);
      else set.add(stopId);
      const next = { ...prev, dismissedStops: Array.from(set) };
      persist(next, false);
      return next;
    });
  }, [persist]);

  return {
    state,
    isLoaded,
    toggleChecklistItem,
    setHearIndicators,
    setDareCategory,
    setTargetInstitutions,
    toggleDismissStop,
  };
}
