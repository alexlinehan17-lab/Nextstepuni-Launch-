/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback } from 'react';
import {
  collection, query, where, orderBy, limit, getDocs, doc,
  getDoc, setDoc, updateDoc, writeBatch, Timestamp,
  serverTimestamp, increment,
} from 'firebase/firestore';
import { db } from '../firebase';
import { useProgress } from '../contexts/ProgressContext';
import { containsProfanity } from '../components/flares/profanityFilter';

// ── Types ──────────────────────────────────────────────────

export interface FlareDoc {
  id: string;
  school: string;
  subject: string;
  question: string;
  senderUid: string;
  status: 'active' | 'resolved' | 'expired';
  createdAt: Date;
  expiresAt: Date;
  responseCount: number;
}

export interface FlareResponse {
  id: string;
  text: string;
  responderUid: string;
  helpful: boolean;
  createdAt: Date;
}

export interface FlareCounts {
  daily: number;
  dailyDate: string;
  weekly: number;
  weeklyStart: string;
  dailyRemaining: number;
  dailyLimit: number;
  weeklyRemaining: number;
  weeklyLimit: number;
}

// ── Constants ──────────────────────────────────────────────

const MAX_DAILY = 3;
const MAX_WEEKLY = 10;
const FLARE_TTL_MS = 24 * 60 * 60 * 1000; // 24 hours

// ── Helpers ────────────────────────────────────────────────

function getDateKey(): string {
  return new Date().toISOString().slice(0, 10); // YYYY-MM-DD
}

function getWeekStart(): string {
  const now = new Date();
  const day = now.getDay();
  const diff = now.getDate() - day + (day === 0 ? -6 : 1); // Monday start
  const monday = new Date(now);
  monday.setDate(diff);
  return monday.toISOString().slice(0, 10);
}

function _isExpired(expiresAt: Date): boolean {
  return expiresAt.getTime() <= Date.now();
}

// ── Hook ───────────────────────────────────────────────────

export function useFlares(uid?: string, school?: string, subjects?: string[]) {
  const { rawProgressDoc, progressLoaded } = useProgress();
  const [activeFlares, setActiveFlares] = useState<FlareDoc[]>([]);
  const [myFlares, setMyFlares] = useState<FlareDoc[]>([]);
  const [myFlareResponses, setMyFlareResponses] = useState<Record<string, FlareResponse[]>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [flareCounts, setFlareCounts] = useState<FlareCounts>({
    daily: 0, dailyDate: '', weekly: 0, weeklyStart: '',
    dailyRemaining: MAX_DAILY, dailyLimit: MAX_DAILY,
    weeklyRemaining: MAX_WEEKLY, weeklyLimit: MAX_WEEKLY,
  });

  // ── Load active flares from same school ────────────────

  const loadActiveFlares = useCallback(async () => {
    if (!uid || !school || !subjects?.length) return;

    try {
      const q = query(
        collection(db, 'flares'),
        where('school', '==', school),
        where('status', '==', 'active'),
        orderBy('createdAt', 'desc'),
        limit(50),
      );
      const snap = await getDocs(q);

      const now = Date.now();
      const flares: FlareDoc[] = snap.docs
        .map(d => {
          const data = d.data();
          return {
            id: d.id,
            school: data.school,
            subject: data.subject,
            question: data.question,
            senderUid: data.senderUid,
            status: data.status as FlareDoc['status'],
            createdAt: (data.createdAt as Timestamp)?.toDate?.() ?? new Date(),
            expiresAt: (data.expiresAt as Timestamp)?.toDate?.() ?? new Date(),
            responseCount: data.responseCount || 0,
          };
        })
        // Filter: matching subjects, not own, not expired
        .filter(f =>
          f.senderUid !== uid &&
          subjects.includes(f.subject) &&
          f.expiresAt.getTime() > now,
        );

      setActiveFlares(flares);
    } catch (err) {
      console.error('[useFlares] Failed to load active flares:', err);
    }
  }, [uid, school, subjects]);

  // ── Load my own flares + their responses ───────────────

  const loadMyFlares = useCallback(async () => {
    if (!uid) return;

    try {
      const q = query(
        collection(db, 'flares'),
        where('senderUid', '==', uid),
        orderBy('createdAt', 'desc'),
        limit(20),
      );
      const snap = await getDocs(q);

      const flares: FlareDoc[] = snap.docs.map(d => {
        const data = d.data();
        return {
          id: d.id,
          school: data.school,
          subject: data.subject,
          question: data.question,
          senderUid: data.senderUid,
          status: data.status as FlareDoc['status'],
          createdAt: (data.createdAt as Timestamp)?.toDate?.() ?? new Date(),
          expiresAt: (data.expiresAt as Timestamp)?.toDate?.() ?? new Date(),
          responseCount: data.responseCount || 0,
        };
      });

      setMyFlares(flares);

      // Fetch responses for each flare
      const responsesMap: Record<string, FlareResponse[]> = {};
      await Promise.all(
        flares.map(async (flare) => {
          try {
            const rq = query(
              collection(db, 'flares', flare.id, 'responses'),
              orderBy('createdAt', 'desc'),
              limit(20),
            );
            const rsnap = await getDocs(rq);
            responsesMap[flare.id] = rsnap.docs.map(rd => {
              const rdata = rd.data();
              return {
                id: rd.id,
                text: rdata.text,
                responderUid: rdata.responderUid,
                helpful: rdata.helpful || false,
                createdAt: (rdata.createdAt as Timestamp)?.toDate?.() ?? new Date(),
              };
            });
          } catch (err) {
            console.error(`[useFlares] Failed to load responses for ${flare.id}`, err);
            responsesMap[flare.id] = [];
          }
        }),
      );

      setMyFlareResponses(responsesMap);
    } catch (err) {
      console.error('[useFlares] Failed to load my flares:', err);
    }
  }, [uid]);

  // ── Initial load ───────────────────────────────────────

  useEffect(() => {
    if (!uid) return;
    let cancelled = false;

    (async () => {
      setIsLoading(true);
      try {
        await Promise.all([loadActiveFlares(), loadMyFlares()]);
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    })();

    return () => { cancelled = true; };
  }, [uid, loadActiveFlares, loadMyFlares]);

  // ── Load user progress (rescue count, lighthouse, flare counts) from context ──

  useEffect(() => {
    if (!progressLoaded || !uid) return;

    const data = rawProgressDoc;
    const rawCounts = data.flareCounts || { daily: 0, dailyDate: '', weekly: 0, weeklyStart: '' };
    const today = getDateKey();
    const weekStart = getWeekStart();
    const dailyUsed = rawCounts.dailyDate === today ? rawCounts.daily : 0;
    const weeklyUsed = rawCounts.weeklyStart === weekStart ? rawCounts.weekly : 0;

    setFlareCounts({
      daily: dailyUsed,
      dailyDate: rawCounts.dailyDate,
      weekly: weeklyUsed,
      weeklyStart: rawCounts.weeklyStart,
      dailyRemaining: MAX_DAILY - dailyUsed,
      dailyLimit: MAX_DAILY,
      weeklyRemaining: MAX_WEEKLY - weeklyUsed,
      weeklyLimit: MAX_WEEKLY,
    });
  }, [progressLoaded, rawProgressDoc, uid]);

  // ── Get responses for a specific flare ──────────────

  const getResponses = useCallback(async (flareId: string): Promise<FlareResponse[]> => {
    try {
      const rq = query(
        collection(db, 'flares', flareId, 'responses'),
        orderBy('createdAt', 'desc'),
        limit(20),
      );
      const rsnap = await getDocs(rq);
      return rsnap.docs.map(rd => {
        const rdata = rd.data();
        return {
          id: rd.id,
          text: rdata.text,
          responderUid: rdata.responderUid,
          helpful: rdata.helpful || false,
          createdAt: (rdata.createdAt as Timestamp)?.toDate?.() ?? new Date(),
        };
      });
    } catch (err) {
      console.error(`[useFlares] Failed to get responses for ${flareId}`, err);
      return [];
    }
  }, []);

  // ── Send a flare ──────────────────────────────────────

  const sendFlare = useCallback(async (subject: string, question: string): Promise<{ ok: boolean; error?: string }> => {
    if (!uid || !school) return { ok: false, error: 'Not signed in.' };

    const trimmed = question.trim();
    if (!trimmed) return { ok: false, error: 'Question cannot be empty.' };
    if (trimmed.length > 500) return { ok: false, error: 'Question too long (max 500 chars).' };

    // Profanity check
    if (containsProfanity(trimmed)) {
      return { ok: false, error: 'Please rephrase — inappropriate language detected.' };
    }

    try {
      // Check rate limits from progress doc
      const progressRef = doc(db, 'progress', uid);
      const progressSnap = await getDoc(progressRef);
      const progressData = progressSnap.exists() ? progressSnap.data() : {};

      const counts: FlareCounts = progressData.flareCounts || {
        daily: 0,
        dailyDate: '',
        weekly: 0,
        weeklyStart: '',
      };

      const today = getDateKey();
      const weekStart = getWeekStart();

      // Reset counters if date/week changed
      const dailyCount = counts.dailyDate === today ? counts.daily : 0;
      const weeklyCount = counts.weeklyStart === weekStart ? counts.weekly : 0;

      if (dailyCount >= MAX_DAILY) {
        return { ok: false, error: `Daily limit reached (${MAX_DAILY} flares/day).` };
      }
      if (weeklyCount >= MAX_WEEKLY) {
        return { ok: false, error: `Weekly limit reached (${MAX_WEEKLY} flares/week).` };
      }

      // Create flare + update counts atomically
      const batch = writeBatch(db);

      const flareRef = doc(collection(db, 'flares'));
      const now = new Date();
      const expiresAt = new Date(now.getTime() + FLARE_TTL_MS);

      batch.set(flareRef, {
        school,
        subject,
        question: trimmed,
        senderUid: uid,
        status: 'active',
        createdAt: serverTimestamp(),
        expiresAt: Timestamp.fromDate(expiresAt),
        responseCount: 0,
      });

      batch.set(progressRef, {
        flareCounts: {
          daily: dailyCount + 1,
          dailyDate: today,
          weekly: weeklyCount + 1,
          weeklyStart: weekStart,
        },
      }, { merge: true });

      await batch.commit();

      // Update local flareCounts
      setFlareCounts({
        daily: dailyCount + 1,
        dailyDate: today,
        weekly: weeklyCount + 1,
        weeklyStart: weekStart,
        dailyRemaining: MAX_DAILY - (dailyCount + 1),
        dailyLimit: MAX_DAILY,
        weeklyRemaining: MAX_WEEKLY - (weeklyCount + 1),
        weeklyLimit: MAX_WEEKLY,
      });

      // Add new flare to local myFlares so "My Flares" tab shows it immediately
      const newFlare: FlareDoc = {
        id: flareRef.id,
        school,
        subject,
        question: trimmed,
        senderUid: uid,
        status: 'active',
        createdAt: now,
        expiresAt,
        responseCount: 0,
      };
      setMyFlares(prev => [newFlare, ...prev]);

      return { ok: true };
    } catch (err) {
      console.error('[useFlares] Failed to send flare:', err);
      return { ok: false, error: 'Failed to send. Try again.' };
    }
  }, [uid, school]);

  // ── Respond to a flare ────────────────────────────────

  const respondToFlare = useCallback(async (flareId: string, text: string): Promise<{ ok: boolean; error?: string }> => {
    if (!uid) return { ok: false, error: 'Not signed in.' };

    const trimmed = text.trim();
    if (!trimmed) return { ok: false, error: 'Response cannot be empty.' };
    if (trimmed.length > 1000) return { ok: false, error: 'Response too long (max 1000 chars).' };

    // Profanity check
    if (containsProfanity(trimmed)) {
      return { ok: false, error: 'Please rephrase — inappropriate language detected.' };
    }

    try {
      const batch = writeBatch(db);

      const responseRef = doc(collection(db, 'flares', flareId, 'responses'));
      batch.set(responseRef, {
        text: trimmed,
        responderUid: uid,
        helpful: false,
        createdAt: serverTimestamp(),
      });

      // Increment response count on the flare doc
      const flareRef = doc(db, 'flares', flareId);
      batch.update(flareRef, {
        responseCount: increment(1),
      });

      await batch.commit();
      return { ok: true };
    } catch (err) {
      console.error('[useFlares] Failed to respond to flare:', err);
      return { ok: false, error: 'Failed to send response. Try again.' };
    }
  }, [uid]);

  // ── Mark a response as helpful ────────────────────────

  const markHelpful = useCallback(async (flareId: string, responseId: string): Promise<void> => {
    if (!uid) return;

    try {
      // Mark response as helpful (this write is allowed by rules)
      const responseRef = doc(db, 'flares', flareId, 'responses', responseId);
      await updateDoc(responseRef, { helpful: true });

      // Update local state immediately
      setMyFlareResponses(prev => {
        const responses = prev[flareId];
        if (!responses) return prev;
        return {
          ...prev,
          [flareId]: responses.map(r =>
            r.id === responseId ? { ...r, helpful: true } : r,
          ),
        };
      });

    } catch (err) {
      console.error('[useFlares] Failed to mark helpful:', err);
    }
  }, [uid]);

  // ── Resolve a flare ───────────────────────────────────

  const resolveFlare = useCallback(async (flareId: string): Promise<void> => {
    if (!uid) return;

    try {
      await updateDoc(doc(db, 'flares', flareId), {
        status: 'resolved',
      });

      // Update local state
      setMyFlares(prev => prev.map(f =>
        f.id === flareId ? { ...f, status: 'resolved' as const } : f,
      ));
      setActiveFlares(prev => prev.filter(f => f.id !== flareId));
    } catch (err) {
      console.error('[useFlares] Failed to resolve flare:', err);
    }
  }, [uid]);

  // ── Reload everything ─────────────────────────────────

  const reload = useCallback(async () => {
    setIsLoading(true);
    try {
      await Promise.all([loadActiveFlares(), loadMyFlares()]);
    } finally {
      setIsLoading(false);
    }
  }, [loadActiveFlares, loadMyFlares]);

  return {
    activeFlares,
    myFlares,
    myFlareResponses,
    isLoading,
    flareCounts,
    sendFlare,
    respondToFlare,
    getResponses,
    markHelpful,
    resolveFlare,
    reload,
  };
}
