/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — the review scheduler.
 *
 * FSRS-6 via `ts-fsrs`, wrapped to give Mark Bank three behaviours the raw
 * library cannot provide on its own:
 *
 *  1. **Due is derived, never stored.** We persist only the memory state
 *     (stability, difficulty, last review, reps, lapses, learning state) and
 *     compute the due date at read time from the *current* target retention.
 *     Paper Trail's deck stores `dueTs` instead, which means raising target
 *     retention as an exam approaches changes nothing until each card is next
 *     reviewed — a card sitting on a 40-day interval sails straight through the
 *     ramp. Deriving at read time makes the ramp take effect immediately.
 *
 *  2. **Fuzz keyed on the card id.** Interval fuzz stops a batch of cards graded
 *     in one sitting from all landing on the same future day. The library's own
 *     fuzz is applied at review time and seeded from card *state*, so (measured)
 *     40 cards with identical stability all land on the same day, and any fuzz it
 *     did apply would have to be stored to survive re-derivation — which
 *     contradicts (1). Hashing the card id instead is stable across
 *     re-derivation and varies between cards, which is exactly what is needed.
 *
 *  3. **An exam-date retention ramp**, automatic and invisible to the student.
 *
 * Pure and clock-free: every entry point takes `now` (ms epoch), so the whole
 * module is deterministic and unit-testable. Grades are the student's three
 * buttons, never the library's four.
 */

import {
  FSRSAlgorithm,
  Rating,
  State,
  createEmptyCard,
  forgetting_curve,
  generatorParameters,
  FSRS,
  type Card as FsrsCard,
  type FSRSParameters,
} from 'ts-fsrs';

const DAY = 86_400_000;

/** The three buttons the student actually sees. `Easy` is deliberately never emitted. */
export type MarkBankGrade = 'missed' | 'shaky' | 'got';

const RATING: Record<MarkBankGrade, Rating.Again | Rating.Hard | Rating.Good> = {
  missed: Rating.Again,
  shaky: Rating.Hard,
  got: Rating.Good,
};

/**
 * Everything persisted for one card. Deliberately short keys — this is stored as
 * a map of ~800 of these per student, and the field names are the bulk of it.
 * There is no `due` field, by design (see 1 above).
 */
export interface CardMemory {
  /** Stability, in days. */
  s: number;
  /** Difficulty, 1–10. */
  d: number;
  /** Last review, ms epoch. 0 means never reviewed. */
  last: number;
  reps: number;
  lapses: number;
  /** ts-fsrs State: 0 New, 1 Learning, 2 Review, 3 Relearning. */
  state: 0 | 1 | 2 | 3;
  /**
   * Sub-day due time, ms epoch, for a card inside a learning or relearning step.
   * This is the one due value we do store, because minute-scale steps are not
   * derivable from stability — and it is what makes "it'll come back before you
   * finish today" true rather than marketing.
   */
  stepDue?: number;
}

export const RETENTION_BASE = 0.9;
export const RETENTION_PEAK = 0.95;
export const RETENTION_CEILING = 0.97;
/** How far out from the exam the ramp starts. Six weeks. */
export const RAMP_DAYS = 42;

/**
 * Target retention for a moment in time. Flat at 0.90 year-round, then ramping
 * to 0.95 across the final six weeks so cards come back more often when it
 * matters. Capped well below 1.0 — past about 0.97 the daily load becomes
 * punishing and the tool starts working against the student.
 *
 * Honest caveat: densifying review toward a deadline follows from spacing theory
 * (optimal gaps scale with the retention interval), but no peer-reviewed
 * evaluation of deadline-aware scheduling exists. This is reasoned, not proven.
 */
export function retentionFor(now: number, examTs?: number): number {
  if (!examTs || now >= examTs) return RETENTION_BASE;
  const daysOut = (examTs - now) / DAY;
  if (daysOut >= RAMP_DAYS) return RETENTION_BASE;
  const progress = 1 - daysOut / RAMP_DAYS;
  const r = RETENTION_BASE + (RETENTION_PEAK - RETENTION_BASE) * progress;
  return Math.min(RETENTION_CEILING, r);
}

/** Cheap deterministic string hash, for id-keyed fuzz. */
function hash(id: string): number {
  let h = 2166136261;
  for (let i = 0; i < id.length; i++) {
    h ^= id.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return (h >>> 0) / 4294967296;
}

/**
 * Fuzz factor for a card, in [1 - spread, 1 + spread]. Stable for a given id, so
 * re-deriving a due date always gives the same answer, and the student never
 * sees "back Thursday" turn into "back Wednesday" on a reload.
 *
 * The spread widens with the interval — a day either side of a 3-day interval
 * would be disruptive, a day either side of 60 days is invisible.
 */
export function fuzzFactor(cardId: string, intervalDays: number): number {
  if (intervalDays < 3) return 1;
  const spread = intervalDays < 21 ? 0.05 : intervalDays < 90 ? 0.1 : 0.15;
  return 1 + (hash(cardId) * 2 - 1) * spread;
}

let cachedRetention = -1;
let cachedAlg: FSRSAlgorithm | null = null;

/** Algorithm instance for a target retention. Library fuzz off — we apply our own. */
function algFor(retention: number): FSRSAlgorithm {
  if (cachedAlg && cachedRetention === retention) return cachedAlg;
  cachedRetention = retention;
  cachedAlg = new FSRSAlgorithm(params(retention));
  return cachedAlg;
}

function params(retention: number): FSRSParameters {
  return generatorParameters({
    request_retention: retention,
    enable_fuzz: false,
    enable_short_term: true,
  });
}

/**
 * Whole-day interval at which recall is predicted to fall to `retention`.
 * Unfuzzed — `enable_fuzz` is off in `params`, because we apply our own id-keyed
 * fuzz at read time instead (see 2 in the module header).
 */
export function baseInterval(stability: number, retention: number): number {
  return algFor(retention).next_interval(stability, 0);
}

/**
 * When this card next comes back. Derived — never read from storage.
 *
 * A card in a learning step uses its stored minute-scale `stepDue`. A new card
 * is due immediately. Everything else is `last review + fuzzed interval`.
 */
export function dueAt(cardId: string, m: CardMemory, retention: number): number {
  if (m.state === State.New || !m.last) return 0;
  if ((m.state === State.Learning || m.state === State.Relearning) && m.stepDue) return m.stepDue;
  const base = baseInterval(m.s, retention);
  return m.last + Math.max(1, Math.round(base * fuzzFactor(cardId, base))) * DAY;
}

export function isDue(cardId: string, m: CardMemory, now: number, retention: number): boolean {
  return dueAt(cardId, m, retention) <= now;
}

/**
 * Predicted probability the student still has this card, 0–1. Used to rank a
 * backlog: the cards a student has genuinely forgotten should be the ones they
 * see, not the ones that happen to be oldest.
 */
export function retrievability(m: CardMemory, now: number): number {
  if (m.state === State.New || !m.last || m.s <= 0) return 0;
  const elapsed = Math.max(0, (now - m.last) / DAY);
  return forgetting_curve(params(RETENTION_BASE).w[20], elapsed, m.s);
}

export const NEW_CARD: CardMemory = { s: 0, d: 0, last: 0, reps: 0, lapses: 0, state: State.New };

function toFsrsCard(m: CardMemory, now: number): FsrsCard {
  const empty = createEmptyCard(new Date(now));
  if (m.state === State.New || !m.last) return empty;
  return {
    ...empty,
    stability: m.s,
    difficulty: m.d,
    reps: m.reps,
    lapses: m.lapses,
    state: m.state,
    last_review: new Date(m.last),
    due: new Date(dueAt('', m, RETENTION_BASE) || now),
  };
}

/**
 * Record one review. Returns the new memory state; the caller persists it and
 * derives the next due date from it.
 */
export function grade(
  m: CardMemory,
  g: MarkBankGrade,
  now: number,
  retention: number = RETENTION_BASE,
): CardMemory {
  const scheduler = new FSRS(params(retention));
  const out = scheduler.next(toFsrsCard(m, now), new Date(now), RATING[g]);
  const c = out.card;
  const state = c.state as 0 | 1 | 2 | 3;
  const next: CardMemory = {
    s: c.stability,
    d: c.difficulty,
    last: now,
    reps: c.reps,
    lapses: c.lapses,
    state,
  };
  // Keep the minute-scale step time only while the card is actually in a step.
  if (state === State.Learning || state === State.Relearning) {
    const stepDue = c.due.getTime();
    if (stepDue - now < DAY) next.stepDue = stepDue;
  }
  return next;
}

/**
 * Seed an Ordinary Level card from its Higher Level sibling on the same concept.
 *
 * Students drop from Higher to Ordinary in the spring, disproportionately in
 * DEIS schools. Without this, that student opens the tool in March to an empty
 * deck and every visible trace of a year's work is gone — the single most
 * demoralising thing this product could do to them. The discount is deliberate:
 * they have met the concept, but not this wording, so the card is treated as
 * known-but-rusty rather than mastered.
 */
export function seedFromSibling(hl: CardMemory, now: number, discount = 0.6): CardMemory {
  if (hl.state === State.New || !hl.last || hl.s <= 0) return { ...NEW_CARD };
  return {
    s: Math.max(0.5, hl.s * discount),
    d: hl.d || 5,
    last: now,
    reps: 0,
    lapses: 0,
    state: State.Review,
  };
}

export interface SessionOptions {
  /** Distinct cards in one sitting. Twelve is about fifteen minutes. */
  size?: number;
  examTs?: number;
  /** Cap on brand-new cards per session, so a new topic can't swamp the mix. */
  newLimit?: number;
}

export interface SessionPlan {
  /** Card ids in presentation order. */
  queue: string[];
  /** How many were due versus newly introduced. */
  dueCount: number;
  newCount: number;
  /** Due cards that did not fit this session. Never shown to the student. */
  heldBack: number;
  retention: number;
}

/**
 * Build one session.
 *
 * Due cards come first, ranked by retrievability ascending — the most-forgotten
 * first. This matters most after a long absence: with the whole deck due,
 * picking by age or at random pushes genuinely forgotten cards weeks out while
 * the student is sitting there wanting to study them.
 *
 * New cards fill any remaining room, and are suppressed entirely while a backlog
 * exists, or the backlog never drains.
 */
export function planSession(
  ids: string[],
  memories: Record<string, CardMemory | undefined>,
  now: number,
  opts: SessionOptions = {},
): SessionPlan {
  const size = opts.size ?? 12;
  const retention = retentionFor(now, opts.examTs);

  const due: { id: string; r: number }[] = [];
  const fresh: string[] = [];

  for (const id of ids) {
    const m = memories[id] ?? NEW_CARD;
    if (m.state === State.New || !m.last) {
      fresh.push(id);
    } else if (isDue(id, m, now, retention)) {
      due.push({ id, r: retrievability(m, now) });
    }
  }

  due.sort((a, b) => a.r - b.r || (a.id < b.id ? -1 : 1));
  const queue = due.slice(0, size).map(d => d.id);
  const heldBack = Math.max(0, due.length - queue.length);

  // Only introduce new material once the student is on top of what they've met.
  const room = size - queue.length;
  const newLimit = opts.newLimit ?? size;
  const newCount = heldBack > 0 ? 0 : Math.max(0, Math.min(room, newLimit, fresh.length));
  queue.push(...fresh.slice(0, newCount));

  return { queue, dueCount: Math.min(due.length, size), newCount, heldBack, retention };
}

/**
 * Words for the next return. Always approximate and always forward-looking:
 * never a bare unit, never a count of anything "overdue".
 */
export function intervalWords(cardId: string, m: CardMemory, now: number, retention: number): string {
  const ts = dueAt(cardId, m, retention);
  const mins = (ts - now) / 60_000;
  if (mins < 60) return 'before you finish today';
  const days = mins / 1440;
  if (days < 1) return 'later today';
  if (days < 1.5) return 'tomorrow';
  if (days < 21) return `in about ${Math.round(days)} days`;
  if (days < 60) return `in about ${Math.round(days / 7)} weeks`;
  return `in about ${Math.round(days / 30)} months`;
}
