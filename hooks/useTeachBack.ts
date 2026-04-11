/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import {
  collection, query, where, getDocs, addDoc,
  doc, updateDoc, increment, arrayUnion,
} from 'firebase/firestore';
import { db } from '../firebase';
import { useProgress } from '../contexts/ProgressContext';
import { containsProfanity } from '../components/flares/profanityFilter';

// ── Types ──────────────────────────────────────────────────

export interface TeachBackEntry {
  id: string;
  subject: string;
  explanation: string;
  helpfulCount: number;
  createdAt: number;
}

// ── Weighted random selection (helpful = shown more) ──────

function weightedPick(items: TeachBackEntry[]): TeachBackEntry {
  const totalWeight = items.reduce((sum, c) => sum + 1 + c.helpfulCount, 0);
  let rand = Math.random() * totalWeight;
  for (const item of items) {
    rand -= (1 + item.helpfulCount);
    if (rand <= 0) return item;
  }
  return items[items.length - 1];
}

// ── Hook ───────────────────────────────────────────────────

export function useTeachBack(uid?: string, school?: string) {
  const { rawProgressDoc, progressLoaded } = useProgress();
  const [teachBackToRead, setTeachBackToRead] = useState<TeachBackEntry | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const seenIdsRef = useRef<Set<string>>(new Set());
  const fetchedForSubjectRef = useRef('');
  const isMountedRef = useRef(true);
  useEffect(() => () => { isMountedRef.current = false; }, []);

  // Load seen IDs from context
  useEffect(() => {
    if (!progressLoaded) return;
    const seen: string[] = rawProgressDoc.teachBacksSeen || [];
    seenIdsRef.current = new Set(seen);
  }, [progressLoaded, rawProgressDoc]);

  // Fetch a teach-back for a given subject (weighted by helpfulness)
  const fetchTeachBack = useCallback(async (subject: string) => {
    if (!uid || !school || !subject) return;
    if (fetchedForSubjectRef.current === subject) return;
    fetchedForSubjectRef.current = subject;

    try {
      const q = query(
        collection(db, 'teachbacks'),
        where('school', '==', school),
        where('subject', '==', subject),
      );
      const snapshot = await getDocs(q);

      // Filter: not self, not already seen
      const candidates: TeachBackEntry[] = snapshot.docs
        .filter(d => d.data().authorUid !== uid && !seenIdsRef.current.has(d.id))
        .map(d => ({
          id: d.id,
          subject: d.data().subject,
          explanation: d.data().explanation,
          helpfulCount: d.data().helpfulCount || 0,
          createdAt: d.data().createdAt,
        }));

      if (candidates.length === 0) {
        setTeachBackToRead(null);
        return;
      }

      // Weighted selection — helpful ones appear more often
      setTeachBackToRead(weightedPick(candidates));
    } catch {
      console.error('[TeachBack] Failed to fetch:');
    }
  }, [uid, school]);

  // Submit a new teach-back
  const submitTeachBack = useCallback(async (subject: string, explanation: string): Promise<boolean> => {
    if (!uid || !school || !explanation.trim()) return false;
    if (containsProfanity(explanation)) return false;
    setIsSubmitting(true);
    try {
      await addDoc(collection(db, 'teachbacks'), {
        authorUid: uid,
        school,
        subject,
        explanation: explanation.trim(),
        createdAt: Date.now(),
        helpfulCount: 0,
      });
      if (isMountedRef.current) setIsSubmitting(false);
      return true;
    } catch (err) {
      console.error('[TeachBack] Failed to submit:', err);
      if (isMountedRef.current) setIsSubmitting(false);
      return false;
    }
  }, [uid, school]);

  // Mark a teach-back as helpful + mark seen
  const markHelpful = useCallback(async (teachBackId: string) => {
    if (!uid) return;
    try {
      await updateDoc(doc(db, 'teachbacks', teachBackId), {
        helpfulCount: increment(1),
      });
    } catch (err) {
      console.error('[TeachBack] Failed to mark helpful:', err);
    }
    // Also mark seen
    seenIdsRef.current.add(teachBackId);
    if (isMountedRef.current) setTeachBackToRead(null);
    try {
      await updateDoc(doc(db, 'progress', uid), {
        teachBacksSeen: arrayUnion(teachBackId),
      });
    } catch {
      console.error('[TeachBack] Failed to update seen list:');
    }
  }, [uid]);

  // Mark as seen without helpful
  const markSeen = useCallback(async (teachBackId: string) => {
    if (!uid) return;
    seenIdsRef.current.add(teachBackId);
    setTeachBackToRead(null);
    try {
      await updateDoc(doc(db, 'progress', uid), {
        teachBacksSeen: arrayUnion(teachBackId),
      });
    } catch {
      console.error('[TeachBack] Failed to update seen list:');
    }
  }, [uid]);

  // Reset for a new session
  const resetForSubject = useCallback(() => {
    fetchedForSubjectRef.current = '';
    setTeachBackToRead(null);
  }, []);

  return {
    teachBackToRead,
    fetchTeachBack,
    submitTeachBack,
    markHelpful,
    markSeen,
    resetForSubject,
    isSubmitting,
  };
}
