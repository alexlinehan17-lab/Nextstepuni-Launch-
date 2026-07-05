/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — student flashcards (feature E6). The honest way to practise
 * *beyond* past papers: the student authors their own question/answer cards, so
 * the content is theirs (no fabrication on our part), and they're scheduled with
 * the very same FSRS engine and recall-strength setting as the past-paper review
 * deck. Persisted per uid in localStorage; `now` injected by the caller.
 */

import { fsrsInit, fsrsNext, MIN_STABILITY, type FsrsGrade } from './fsrs';
import { getTargetRetention, type ReviewGrade } from './reviewStore';

const DAY = 86_400_000;
const GRADE_NUM: Record<ReviewGrade, FsrsGrade> = { again: 1, hard: 2, good: 3, easy: 4 };

export interface Flashcard {
  id: string;
  front: string;
  back: string;
  /** Optional subject tag for grouping. */
  subjectId?: string;
  stability?: number;
  difficulty?: number;
  intervalDays: number;
  dueTs: number;
  reps: number;
  lapses: number;
  addedTs: number;
  lastTs: number;
}

const PREFIX = 'pt:cards:';
const blobKey = (uid?: string) => PREFIX + (uid || 'anon');

type Store = Record<string, Flashcard>;

const read = (uid?: string): Store => {
  try {
    const raw = localStorage.getItem(blobKey(uid));
    return raw ? (JSON.parse(raw) as Store) : {};
  } catch {
    return {};
  }
};
const write = (uid: string | undefined, s: Store) => {
  try {
    localStorage.setItem(blobKey(uid), JSON.stringify(s));
  } catch {
    /* quota / private mode — degrade silently */
  }
};

/** All cards, newest-added first. */
export function loadCards(uid?: string): Flashcard[] {
  return Object.values(read(uid)).sort((a, b) => b.addedTs - a.addedTs);
}

export function createCard(
  uid: string | undefined,
  front: string,
  back: string,
  subjectId: string | undefined,
  now: number,
): Flashcard[] {
  const f = front.trim();
  const b = back.trim();
  if (!f || !b) return loadCards(uid);
  const s = read(uid);
  const id = `${now.toString(36)}-${Object.keys(s).length}-${Math.floor(Math.random() * 1e6).toString(36)}`;
  s[id] = { id, front: f, back: b, subjectId, intervalDays: 0, dueTs: now, reps: 0, lapses: 0, addedTs: now, lastTs: 0 };
  write(uid, s);
  return loadCards(uid);
}

export function updateCard(uid: string | undefined, id: string, front: string, back: string): Flashcard[] {
  const s = read(uid);
  if (s[id]) {
    s[id] = { ...s[id], front: front.trim() || s[id].front, back: back.trim() || s[id].back };
    write(uid, s);
  }
  return loadCards(uid);
}

export function deleteCard(uid: string | undefined, id: string): Flashcard[] {
  const s = read(uid);
  delete s[id];
  write(uid, s);
  return loadCards(uid);
}

/** Record a review and reschedule with FSRS (same engine as the review deck). */
export function gradeCard(uid: string | undefined, id: string, grade: ReviewGrade, now: number): Flashcard[] {
  const s = read(uid);
  const card = s[id];
  if (!card) return loadCards(uid);
  const g = GRADE_NUM[grade];
  const retention = getTargetRetention(uid);
  const elapsed = card.lastTs ? (now - card.lastTs) / DAY : 0;
  const review = card.stability != null
    ? fsrsNext({ stability: card.stability, difficulty: card.difficulty ?? 5 }, g, elapsed, retention)
    : card.intervalDays > 0
      ? fsrsNext({ stability: Math.max(MIN_STABILITY, card.intervalDays), difficulty: 5 }, g, elapsed, retention)
      : fsrsInit(g, retention);
  s[id] = {
    ...card,
    stability: review.stability,
    difficulty: review.difficulty,
    intervalDays: review.intervalDays,
    dueTs: now + review.intervalDays * DAY,
    reps: grade === 'again' ? 0 : card.reps + 1,
    lapses: card.lapses + (grade === 'again' ? 1 : 0),
    lastTs: now,
  };
  write(uid, s);
  return loadCards(uid);
}

/** The interval (days) a grade would set, for the rating-button previews. */
export function projectCardInterval(card: Flashcard, grade: ReviewGrade, now: number, uid?: string): number {
  const g = GRADE_NUM[grade];
  const retention = getTargetRetention(uid);
  const elapsed = card.lastTs ? (now - card.lastTs) / DAY : 0;
  if (card.stability != null) return fsrsNext({ stability: card.stability, difficulty: card.difficulty ?? 5 }, g, elapsed, retention).intervalDays;
  if (card.intervalDays > 0) return fsrsNext({ stability: Math.max(MIN_STABILITY, card.intervalDays), difficulty: 5 }, g, elapsed, retention).intervalDays;
  return fsrsInit(g, retention).intervalDays;
}

export function dueCards(uid: string | undefined, now: number): Flashcard[] {
  return loadCards(uid).filter(c => c.dueTs <= now).sort((a, b) => a.addedTs - b.addedTs);
}

export function cardStats(uid: string | undefined, now: number): { total: number; due: number } {
  const all = loadCards(uid);
  return { total: all.length, due: all.filter(c => c.dueTs <= now).length };
}
