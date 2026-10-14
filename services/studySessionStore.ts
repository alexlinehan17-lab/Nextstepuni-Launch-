/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Keeps study time safe across reloads. A student reported "my study time
 * keeps getting deleted after i log it" and asked for the timer not to stop
 * while they used notes on their iPad (12 Oct 2026). iPad Safari reloads a
 * backgrounded tab when it needs memory, and two things lived only in memory:
 *
 *   1. the running session (timer, subject, plan), and
 *   2. a finished session whose Firestore write had not been acknowledged —
 *      the app uses a memory-only Firestore cache, so a pending write dies
 *      with the page.
 *
 * Both now sit in this tab's storage until they are safe. Web sign-in is
 * already tab-scoped (browserSessionPersistence), so sessionStorage matches it
 * and clearLocalSessionData() wipes both on sign-out. The native shells keep
 * their sign-in across launches, so they use localStorage.
 */

import { doc, getDoc, increment, writeBatch } from 'firebase/firestore';
import { Capacitor } from '@capacitor/core';
import { db } from '../firebase';
import { logError } from '../utils/logError';
import type { StudySessionRecord } from '../studySessionData';
import type { StudyTopicSelection } from '../types/studyTopics';

export interface ActiveStudySession {
  subject: string;
  sessionType: 'new-learning' | 'practice' | 'revision';
  plannedMinutes: number;
  topicSelection?: StudyTopicSelection;
  /** Wall-clock start, shifted forward by any paused time (as the timer keeps it). */
  startedAt: number;
  phase: 'active' | 'paused' | 'complete';
  /** Elapsed seconds when paused or completed; derived from startedAt while active. */
  elapsedSeconds: number;
  completedPrompts: string[];
}

export interface PendingStudySession {
  record: StudySessionRecord;
  points: number;
}

const activeKey = (uid: string) => `nextstepuni:study-active:v1:${uid}`;
const outboxKey = (uid: string) => `nextstepuni:study-outbox:v1:${uid}`;

function storage(): Storage | null {
  try {
    return Capacitor.isNativePlatform() ? window.localStorage : window.sessionStorage;
  } catch {
    return null;
  }
}

function read<T>(key: string): T | null {
  try {
    const raw = storage()?.getItem(key);
    return raw ? JSON.parse(raw) as T : null;
  } catch {
    return null;
  }
}

function write(key: string, value: unknown | null): void {
  try {
    const store = storage();
    if (!store) return;
    if (value === null) store.removeItem(key);
    else store.setItem(key, JSON.stringify(value));
  } catch { /* Storage can be full or blocked; the session still runs in memory. */ }
}

export const readActiveStudySession = (uid: string) => read<ActiveStudySession>(activeKey(uid));
export const writeActiveStudySession = (uid: string, session: ActiveStudySession | null) => write(activeKey(uid), session);

export const readPendingStudySessions = (uid: string): PendingStudySession[] =>
  (read<PendingStudySession[]>(outboxKey(uid)) ?? []).filter(item => item?.record?.id);

function setPending(uid: string, items: PendingStudySession[]): void {
  write(outboxKey(uid), items.length ? items : null);
}

/** Records and points go in one batch, so a retry can never award points twice. */
async function commit(uid: string, item: PendingStudySession): Promise<void> {
  const batch = writeBatch(db);
  batch.set(doc(db, 'progress', uid, 'sessions', item.record.id), item.record);
  if (item.points > 0) {
    batch.set(doc(db, 'progress', uid), { pointsData: { totalEarned: increment(item.points) } }, { merge: true });
  }
  await batch.commit();
}

/**
 * Queue a finished session, then write it. It stays queued until Firestore
 * acknowledges it, so a reload in between only delays it.
 */
export function recordStudySession(uid: string, item: PendingStudySession): Promise<boolean> {
  setPending(uid, [...readPendingStudySessions(uid).filter(p => p.record.id !== item.record.id), item]);
  return commit(uid, item)
    .then(() => {
      setPending(uid, readPendingStudySessions(uid).filter(p => p.record.id !== item.record.id));
      return true;
    })
    .catch(error => {
      logError('studySessionStore.record', error);
      return false;
    });
}

/**
 * Retry anything a previous page queued but never saw acknowledged. A session
 * that already exists was committed (with its points) before the page went
 * away, so it is only dequeued, never written twice.
 */
export async function flushPendingStudySessions(uid: string): Promise<number> {
  let saved = 0;
  for (const item of readPendingStudySessions(uid)) {
    try {
      const existing = await getDoc(doc(db, 'progress', uid, 'sessions', item.record.id));
      if (!existing.exists()) {
        await commit(uid, item);
        saved += 1;
      }
      setPending(uid, readPendingStudySessions(uid).filter(p => p.record.id !== item.record.id));
    } catch (error) {
      logError('studySessionStore.flush', error);
    }
  }
  return saved;
}

/** Saved sessions plus queued ones, so a reload never hides a queued session. */
export function withPendingStudySessions(uid: string, saved: StudySessionRecord[]): StudySessionRecord[] {
  const ids = new Set(saved.map(record => record.id));
  return [...saved, ...readPendingStudySessions(uid).map(p => p.record).filter(record => !ids.has(record.id))];
}
