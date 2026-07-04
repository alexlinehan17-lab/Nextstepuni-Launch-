/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — spaced-recall deck (feature A2). A student saves real past-paper
 * questions to a review deck; each card is scheduled with a light SM-2 spacing
 * algorithm off their own recall rating. There is no fabricated answer text —
 * the card is a pointer to a genuine SEC question, and its marking scheme is one
 * tap away to check against. The rating is the student's honest self-assessment
 * of recall, which is exactly what SM-2 consumes.
 *
 * Persisted in localStorage, one blob per uid, keyed by the question's identity.
 * `now` is always passed in by the caller (browser `Date.now()`) so the SM-2
 * maths stays pure and unit-testable.
 */

import { type PaperLang, type PaperLevel } from '../../types/paperTrail';

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
  /** SM-2 ease factor (min 1.3). */
  ease: number;
  /** Current inter-repetition interval, in days. */
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
const MIN_EASE = 1.3;

// ─── pure SM-2 scheduler ────────────────────────────────────

/** SM-2 quality (0–5) for each of the four buttons. */
const GRADE_Q: Record<ReviewGrade, number> = { again: 2, hard: 3, good: 4, easy: 5 };

export interface Sm2State {
  ease: number;
  intervalDays: number;
  reps: number;
  lapses: number;
}

/** Apply one review to an SM-2 state. Pure — no clock, no storage. A failed
 *  card (`again`) resets its streak and comes back in a day; a passed card grows
 *  its interval by the (grade-adjusted) ease factor. */
export function schedule(prev: Sm2State, grade: ReviewGrade): Sm2State {
  const q = GRADE_Q[grade];
  // Ease update (standard SM-2), clamped so it never collapses below 1.3.
  const ease = Math.max(MIN_EASE, prev.ease + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)));

  if (grade === 'again') {
    return { ease, intervalDays: 1, reps: 0, lapses: prev.lapses + 1 };
  }
  const reps = prev.reps + 1;
  let intervalDays: number;
  if (reps === 1) intervalDays = grade === 'easy' ? 2 : 1;
  else if (reps === 2) intervalDays = grade === 'easy' ? 6 : 4;
  else intervalDays = Math.round(prev.intervalDays * ease * (grade === 'hard' ? 0.7 : 1));
  // Never let a passed card stall on the same day.
  intervalDays = Math.max(1, intervalDays);
  return { ease, intervalDays, reps, lapses: prev.lapses };
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
      ease: 2.5,
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
  const next = schedule({ ease: card.ease, intervalDays: card.intervalDays, reps: card.reps, lapses: card.lapses }, grade);
  deck[k] = {
    ...card,
    ...next,
    dueTs: now + next.intervalDays * DAY,
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
