/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — spaced-recall deck (feature A2, scheduler upgraded in E1). A
 * student saves real past-paper questions to a review deck; each card is
 * scheduled with the FSRS algorithm off their own recall rating, so it returns
 * right as recall is predicted to fall to the target retention. There is no
 * fabricated answer text — the card is a pointer to a genuine SEC question, and
 * its marking scheme is one tap away to check against.
 *
 * Persisted in localStorage, one blob per uid, keyed by the question's identity.
 * `now` is always passed in by the caller (browser `Date.now()`); the FSRS maths
 * itself lives in fsrs.ts, pure and unit-tested.
 */

import { type PaperLang, type PaperLevel } from '../../types/paperTrail';
import {
  DEFAULT_RETENTION,
  MIN_STABILITY,
  fsrsInit,
  fsrsNext,
  type FsrsGrade,
  type FsrsReview,
} from './fsrs';

export type ReviewGrade = 'again' | 'hard' | 'good' | 'easy';

/** The identity of the past-paper question a card points at. */
export interface ReviewCardId {
  subjectId: string;
  year: number;
  level: PaperLevel;
  lang: PaperLang;
  fileid: string;
  n: string;
}

export interface ReviewCard extends ReviewCardId {
  /** Primary curriculum topic, when the question is tagged (for grouping). */
  topicId?: string;
  /** FSRS memory stability in days; undefined until the first review. */
  stability?: number;
  /** FSRS difficulty 1–10; undefined until the first review. */
  difficulty?: number;
  /** Interval (whole days) set at the last review. */
  intervalDays: number;
  /** Next-due epoch ms. */
  dueTs: number;
  /** Successful repetitions in a row (resets to 0 on a lapse). */
  reps: number;
  /** Times the card has been failed (`again`). */
  lapses: number;
  addedTs: number;
  lastTs: number;
}

const DAY = 86_400_000;

// ─── FSRS scheduling (maths in fsrs.ts) ─────────────────────

const GRADE_NUM: Record<ReviewGrade, FsrsGrade> = { again: 1, hard: 2, good: 3, easy: 4 };

/** Compute the next review for a card + grade without persisting. Handles the
 *  three cases: an FSRS card (has stability), a legacy SM-2 card (seed stability
 *  from its old interval), and a brand-new card (FSRS init). */
function computeReview(card: ReviewCard, grade: ReviewGrade, now: number, retention: number): FsrsReview {
  const g = GRADE_NUM[grade];
  const elapsed = card.lastTs ? (now - card.lastTs) / DAY : 0;
  if (card.stability != null) {
    return fsrsNext({ stability: card.stability, difficulty: card.difficulty ?? 5 }, g, elapsed, retention);
  }
  if (card.intervalDays > 0) {
    return fsrsNext({ stability: Math.max(MIN_STABILITY, card.intervalDays), difficulty: 5 }, g, elapsed, retention);
  }
  return fsrsInit(g, retention);
}

/** The interval (days) a grade would set, for the rating-button previews. */
export function projectInterval(card: ReviewCard, grade: ReviewGrade, now: number, uid?: string): number {
  return computeReview(card, grade, now, getTargetRetention(uid)).intervalDays;
}

// ─── target-retention setting (per uid) ─────────────────────

const CFG_PREFIX = 'pt:reviewcfg:';

/** The student's desired recall probability at review time (0.80–0.97). Higher
 *  = more frequent reviews, stronger recall; lower = fewer reviews. */
export function getTargetRetention(uid?: string): number {
  try {
    const v = Number(localStorage.getItem(CFG_PREFIX + (uid || 'anon')));
    return v >= 0.8 && v <= 0.97 ? v : DEFAULT_RETENTION;
  } catch {
    return DEFAULT_RETENTION;
  }
}

export function setTargetRetention(uid: string | undefined, retention: number): void {
  try {
    localStorage.setItem(CFG_PREFIX + (uid || 'anon'), String(Math.min(0.97, Math.max(0.8, retention))));
  } catch {
    /* private mode — degrade silently */
  }
}

// ─── persistence ────────────────────────────────────────────

const PREFIX = 'pt:review:';
const blobKey = (uid?: string) => PREFIX + (uid || 'anon');

export const reviewKey = (c: ReviewCardId) =>
  `${c.subjectId}|${c.year}|${c.level}|${c.lang}|${c.fileid}|${c.n}`;

type Deck = Record<string, ReviewCard>;

const readDeck = (uid?: string): Deck => {
  try {
    const raw = localStorage.getItem(blobKey(uid));
    return raw ? (JSON.parse(raw) as Deck) : {};
  } catch {
    return {};
  }
};
const writeDeck = (uid: string | undefined, deck: Deck) => {
  try {
    localStorage.setItem(blobKey(uid), JSON.stringify(deck));
  } catch {
    /* quota / private mode — degrade silently */
  }
};

/** The whole deck, newest-added first. */
export function loadDeck(uid?: string): ReviewCard[] {
  return Object.values(readDeck(uid)).sort((a, b) => b.addedTs - a.addedTs);
}

export function hasCard(uid: string | undefined, id: ReviewCardId): boolean {
  return reviewKey(id) in readDeck(uid);
}

/** Add a question to the deck (no-op if already there). Starts due immediately. */
export function addCard(
  uid: string | undefined,
  id: ReviewCardId,
  topicId: string | undefined,
  now: number,
): ReviewCard[] {
  const deck = readDeck(uid);
  const k = reviewKey(id);
  if (!deck[k]) {
    deck[k] = {
      ...id,
      topicId,
      intervalDays: 0,
      dueTs: now,
      reps: 0,
      lapses: 0,
      addedTs: now,
      lastTs: 0,
    };
    writeDeck(uid, deck);
  }
  return loadDeck(uid);
}

export function removeCard(uid: string | undefined, id: ReviewCardId): ReviewCard[] {
  const deck = readDeck(uid);
  delete deck[reviewKey(id)];
  writeDeck(uid, deck);
  return loadDeck(uid);
}

/** Record a review and reschedule the card. */
export function gradeCard(
  uid: string | undefined,
  id: ReviewCardId,
  grade: ReviewGrade,
  now: number,
): ReviewCard[] {
  const deck = readDeck(uid);
  const k = reviewKey(id);
  const card = deck[k];
  if (!card) return loadDeck(uid);
  const review = computeReview(card, grade, now, getTargetRetention(uid));
  deck[k] = {
    ...card,
    stability: review.stability,
    difficulty: review.difficulty,
    intervalDays: review.intervalDays,
    dueTs: now + review.intervalDays * DAY,
    reps: grade === 'again' ? 0 : card.reps + 1,
    lapses: card.lapses + (grade === 'again' ? 1 : 0),
    lastTs: now,
  };
  writeDeck(uid, deck);
  return loadDeck(uid);
}

/** Cards due now (dueTs ≤ now), soonest-added first among the due set. */
export function dueCards(uid: string | undefined, now: number): ReviewCard[] {
  return loadDeck(uid)
    .filter(c => c.dueTs <= now)
    .sort((a, b) => a.addedTs - b.addedTs);
}

export interface DeckStats {
  total: number;
  due: number;
  /** Cards never reviewed yet. */
  fresh: number;
}

export function deckStats(uid: string | undefined, now: number): DeckStats {
  const deck = loadDeck(uid);
  return {
    total: deck.length,
    due: deck.filter(c => c.dueTs <= now).length,
    fresh: deck.filter(c => c.lastTs === 0).length,
  };
}
