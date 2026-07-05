/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — FSRS scheduler (feature E1). A faithful implementation of the
 * Free Spaced Repetition Scheduler (FSRS-4.5) with its default weights: each
 * card carries a Difficulty (1–10) and a Stability (days), the retrievability is
 * modelled from time elapsed since the last review, and the next interval is set
 * so the card comes back right as recall is predicted to fall to the student's
 * target retention. This replaces the older fixed-step SM-2 maths.
 *
 * Pure and clock-free: the caller passes elapsed days and target retention, so
 * the whole thing is deterministic and unit-tested. Grades map 1=Again, 2=Hard,
 * 3=Good, 4=Easy.
 */

/** FSRS-4.5 default weights (open-spaced-repetition). */
const W = [
  0.4072, 1.1829, 3.1262, 15.4722, 7.2102, 0.5316, 1.0651, 0.0234, 1.616, 0.1544,
  1.0824, 1.9813, 0.0953, 0.2975, 2.2042, 0.2407, 2.9466, 0.5034, 0.6567,
];
const DECAY = -0.5;
/** Constant such that R = (1 + FACTOR·t/S)^DECAY gives R=0.9 at t=S. */
const FACTOR = Math.pow(0.9, 1 / DECAY) - 1;

export const DEFAULT_RETENTION = 0.9;
export const MIN_STABILITY = 0.1;

export type FsrsGrade = 1 | 2 | 3 | 4;

export interface FsrsState {
  /** Memory stability, in days. */
  stability: number;
  /** Difficulty, 1 (easy) – 10 (hard). */
  difficulty: number;
}

export interface FsrsReview extends FsrsState {
  /** Whole-day interval until the next review. */
  intervalDays: number;
}

const clampD = (d: number) => Math.min(10, Math.max(1, d));
const initDifficulty = (g: FsrsGrade) => clampD(W[4] - Math.exp(W[5] * (g - 1)) + 1);
const initStability = (g: FsrsGrade) => Math.max(MIN_STABILITY, W[g - 1]);

/** Predicted recall probability after `elapsedDays` for a card of `stability`. */
export function retrievability(elapsedDays: number, stability: number): number {
  return Math.pow(1 + (FACTOR * Math.max(0, elapsedDays)) / Math.max(MIN_STABILITY, stability), DECAY);
}

/** Whole-day interval that lands recall at `retention` for a given stability. */
export function intervalFor(stability: number, retention: number): number {
  const days = (stability / FACTOR) * (Math.pow(retention, 1 / DECAY) - 1);
  return Math.max(1, Math.round(days));
}

// Difficulty mean-reverts toward a neutral ("Good") baseline so it can't drift.
const nextDifficulty = (d: number, g: FsrsGrade) => {
  const dp = d - W[6] * (g - 3);
  return clampD(W[7] * initDifficulty(3) + (1 - W[7]) * dp);
};

const stabilityOnRecall = (d: number, s: number, r: number, g: FsrsGrade) => {
  const hard = g === 2 ? W[15] : 1;
  const easy = g === 4 ? W[16] : 1;
  const inc = Math.exp(W[8]) * (11 - d) * Math.pow(s, -W[9]) * (Math.exp(W[10] * (1 - r)) - 1) * hard * easy;
  return s * (1 + inc);
};

const stabilityOnLapse = (d: number, s: number, r: number) =>
  W[11] * Math.pow(d, -W[12]) * (Math.pow(s + 1, W[13]) - 1) * Math.exp(W[14] * (1 - r));

/** First review of a brand-new card. */
export function fsrsInit(g: FsrsGrade, retention: number = DEFAULT_RETENTION): FsrsReview {
  const stability = initStability(g);
  const difficulty = initDifficulty(g);
  return { stability, difficulty, intervalDays: intervalFor(stability, retention) };
}

/** A subsequent review: update difficulty and stability, then the interval. */
export function fsrsNext(
  state: FsrsState,
  g: FsrsGrade,
  elapsedDays: number,
  retention: number = DEFAULT_RETENTION,
): FsrsReview {
  const r = retrievability(elapsedDays, state.stability);
  const difficulty = nextDifficulty(state.difficulty, g);
  const raw = g === 1 ? stabilityOnLapse(difficulty, state.stability, r) : stabilityOnRecall(difficulty, state.stability, r, g);
  const stability = Math.max(MIN_STABILITY, raw);
  return { stability, difficulty, intervalDays: intervalFor(stability, retention) };
}
