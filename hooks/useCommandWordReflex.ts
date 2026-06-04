/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * useCommandWordReflex — state for the Command-Word Reflex tool.
 * Owns progress/{uid}.commandWordReflex (additive-merge namespace, same pattern
 * as useExamReps / useCatchUpLane — no Firestore rules change).
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { doc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { useFreshProgress } from './useFreshProgress';
import { type CommandWordState } from '../types/commandWord';

const EMPTY: CommandWordState = {
  seenIds: [],
  firstTryIds: [],
  wordsMet: [],
  attempts: 0,
  updatedAt: '',
};

const uniqPush = (arr: string[], v: string) => (arr.includes(v) ? arr : [...arr, v]);

export function useCommandWordReflex(uid?: string) {
  const { doc: rawProgressDoc, loaded: progressLoaded } = useFreshProgress(uid);
  const [state, setState] = useState<CommandWordState>(EMPTY);
  const [isLoaded, setIsLoaded] = useState(false);
  const seededRef = useRef(false);

  useEffect(() => { seededRef.current = false; }, [uid]);

  useEffect(() => {
    if (!progressLoaded || seededRef.current) return;
    const saved = rawProgressDoc?.commandWordReflex as CommandWordState | undefined;
    setState(saved ? { ...EMPTY, ...saved } : EMPTY);
    setIsLoaded(true);
    seededRef.current = true;
  }, [progressLoaded, rawProgressDoc, uid]);

  const persist = useCallback((next: CommandWordState) => {
    if (uid) {
      setDoc(doc(db, 'progress', uid), { commandWordReflex: next }, { merge: true }).catch(() => {});
    }
  }, [uid]);

  /** Record a completed question: whether it was spotted on the first tap, and the cue word met. */
  const recordResult = useCallback((questionId: string, commandWord: string, firstTry: boolean) => {
    setState(prev => {
      const next: CommandWordState = {
        ...prev,
        seenIds: uniqPush(prev.seenIds, questionId),
        firstTryIds: firstTry ? uniqPush(prev.firstTryIds, questionId) : prev.firstTryIds.filter(id => id !== questionId),
        wordsMet: uniqPush(prev.wordsMet, commandWord.toLowerCase()),
        attempts: prev.attempts + 1,
        updatedAt: new Date().toISOString(),
      };
      persist(next);
      return next;
    });
  }, [persist]);

  return { state, isLoaded, recordResult };
}
