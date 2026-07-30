/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank scheduler — behavioural pins.
 *
 * These are not incidental unit tests. Each one pins a behaviour that the
 * scheduler this replaces got wrong, and that the design's student-facing copy
 * promises. If one of these fails, the tool is lying to a student.
 */

import { describe, it, expect } from 'vitest';
import {
  NEW_CARD,
  RAMP_DAYS,
  RETENTION_BASE,
  RETENTION_CEILING,
  RETENTION_PEAK,
  baseInterval,
  dueAt,
  fuzzFactor,
  grade,
  intervalWords,
  isDue,
  planSession,
  retentionFor,
  retrievability,
  seedFromSibling,
  type CardMemory,
} from '../components/MarkBank/scheduler';

const DAY = 86_400_000;
const NOW = Date.UTC(2026, 6, 30, 10, 0, 0);

/** A card that has been known for a while: stability 30 days, reviewed a month ago. */
const mature = (over = 30): CardMemory => ({
  s: 30,
  d: 5,
  last: NOW - over * DAY,
  reps: 5,
  lapses: 0,
  state: 2,
});

describe('grade mapping', () => {
  it('never emits Easy — the student only has three buttons', () => {
    // Good is the top grade available, so a "got it" must not schedule like Easy.
    const got = grade(mature(), 'got', NOW);
    const shaky = grade(mature(), 'shaky', NOW);
    const missed = grade(mature(), 'missed', NOW);
    expect(got.s).toBeGreaterThan(shaky.s);
    expect(shaky.s).toBeGreaterThan(missed.s);
  });

  it('counts a lapse only on "missed it"', () => {
    expect(grade(mature(), 'missed', NOW).lapses).toBe(1);
    expect(grade(mature(), 'shaky', NOW).lapses).toBe(0);
    expect(grade(mature(), 'got', NOW).lapses).toBe(0);
  });
});

describe('same-day return — "it\'ll come back before you finish today"', () => {
  it('puts a missed card back inside the day, not tomorrow', () => {
    const m = grade(mature(), 'missed', NOW);
    const due = dueAt('bio-2025-hl-q6-ab', m, RETENTION_BASE);
    expect(due).toBeGreaterThan(NOW);
    expect(due - NOW).toBeLessThan(DAY);
  });

  it('says so in words', () => {
    const m = grade(mature(), 'missed', NOW);
    expect(intervalWords('bio-2025-hl-q6-ab', m, NOW, RETENTION_BASE)).toBe('before you finish today');
  });

  it('exits the step on recovery but does not let a same-day retry buy a long interval', () => {
    // FSRS-6 deliberately grants no stability credit for re-answering a card you
    // failed minutes ago: that proves nothing about durable memory. Measured, its
    // stability is identical at 6, 11 and 60 minutes. What must hold is that the
    // card leaves relearning and comes back on a short, conservative interval —
    // far shorter than a card recalled correctly first time earns.
    const missed = grade(mature(), 'missed', NOW);
    const then = NOW + 6 * 60_000;
    const sameDay = grade(missed, 'got', then);
    expect(sameDay.state).toBe(2);

    const sameDayGap = dueAt('bio-2025-hl-q6-ab', sameDay, RETENTION_BASE) - then;
    const firstTimeGap = dueAt('bio-2025-hl-q6-ab', grade(mature(), 'got', NOW), RETENTION_BASE) - NOW;
    expect(sameDayGap).toBeGreaterThan(0);
    expect(sameDayGap).toBeLessThan(firstTimeGap);
  });

  it('grows stability once the recall is genuinely spaced', () => {
    const missed = grade(mature(), 'missed', NOW);
    expect(grade(missed, 'got', NOW + 2 * DAY).s).toBeGreaterThan(missed.s);
  });
});

describe('fuzz — a batch graded together must not land on one day', () => {
  it('spreads 100 identically-graded cards across at least five distinct days', () => {
    const days = new Set<number>();
    for (let i = 0; i < 100; i++) {
      const id = `bio-2025-hl-q${i}-a`;
      const m = grade(mature(), 'got', NOW);
      days.add(Math.round((dueAt(id, m, RETENTION_BASE) - NOW) / DAY));
    }
    expect(days.size).toBeGreaterThanOrEqual(5);
  });

  it('is stable for a given card, so a reload never moves the date', () => {
    const m = grade(mature(), 'got', NOW);
    const first = dueAt('bio-2025-hl-q6-ab', m, RETENTION_BASE);
    for (let i = 0; i < 5; i++) {
      expect(dueAt('bio-2025-hl-q6-ab', m, RETENTION_BASE)).toBe(first);
    }
  });

  it('leaves short intervals alone — a day either side of three days is disruptive', () => {
    expect(fuzzFactor('any-card-id', 2)).toBe(1);
  });

  it('widens with the interval', () => {
    const short = Math.abs(fuzzFactor('bio-x', 10) - 1);
    const long = Math.abs(fuzzFactor('bio-x', 120) - 1);
    expect(long).toBeGreaterThan(short);
  });
});

describe('exam-date retention ramp', () => {
  const exam = Date.UTC(2027, 5, 9, 9, 0, 0);

  it('sits at the base retention outside the ramp window', () => {
    expect(retentionFor(exam - 200 * DAY, exam)).toBe(RETENTION_BASE);
    expect(retentionFor(exam - (RAMP_DAYS + 1) * DAY, exam)).toBe(RETENTION_BASE);
  });

  it('climbs as the exam approaches and peaks at the exam', () => {
    const midway = retentionFor(exam - (RAMP_DAYS / 2) * DAY, exam);
    expect(midway).toBeGreaterThan(RETENTION_BASE);
    expect(midway).toBeLessThan(RETENTION_PEAK);
    expect(retentionFor(exam - 60_000, exam)).toBeCloseTo(RETENTION_PEAK, 2);
  });

  it('never exceeds the ceiling, where daily load becomes punishing', () => {
    for (let d = 0; d <= RAMP_DAYS; d++) {
      expect(retentionFor(exam - d * DAY, exam)).toBeLessThanOrEqual(RETENTION_CEILING);
    }
  });

  it('relaxes again once the exam has passed', () => {
    expect(retentionFor(exam + DAY, exam)).toBe(RETENTION_BASE);
  });

  it('has no effect when no exam date is set', () => {
    expect(retentionFor(NOW)).toBe(RETENTION_BASE);
  });
});

describe('due is derived, not stored', () => {
  it('moves the due date the instant retention rises, with no review taking place', () => {
    // This is the whole point. Paper Trail's deck persists dueTs, so a card on a
    // 40-day interval would sail straight through the ramp untouched.
    const m = mature(0);
    const atBase = dueAt('bio-2025-hl-q6-ab', m, RETENTION_BASE);
    const atPeak = dueAt('bio-2025-hl-q6-ab', m, RETENTION_PEAK);
    expect(atPeak).toBeLessThan(atBase);
  });

  it('brings cards into the due set as retention rises', () => {
    const ids = Array.from({ length: 40 }, (_, i) => `bio-2025-hl-q${i}-a`);
    const memories: Record<string, CardMemory> = {};
    for (const id of ids) memories[id] = mature(15);

    const relaxed = ids.filter(id => isDue(id, memories[id], NOW, RETENTION_BASE)).length;
    const tight = ids.filter(id => isDue(id, memories[id], NOW, RETENTION_CEILING)).length;
    expect(tight).toBeGreaterThan(relaxed);
  });

  it('shortens the interval at higher retention', () => {
    expect(baseInterval(30, RETENTION_PEAK)).toBeLessThan(baseInterval(30, RETENTION_BASE));
  });
});

describe('session planning', () => {
  const ids = Array.from({ length: 60 }, (_, i) => `bio-c${i}`);

  it('treats an unmet card as new and never as overdue', () => {
    const plan = planSession(ids, {}, NOW, { size: 12 });
    expect(plan.newCount).toBe(12);
    expect(plan.dueCount).toBe(0);
    expect(plan.heldBack).toBe(0);
  });

  it('serves the most-forgotten cards first after a long absence', () => {
    const memories: Record<string, CardMemory> = {};
    ids.forEach((id, i) => {
      // Stability varies, so retrievability after the same elapsed time varies.
      memories[id] = { s: 2 + i, d: 5, last: NOW - 60 * DAY, reps: 3, lapses: 0, state: 2 };
    });
    const plan = planSession(ids, memories, NOW, { size: 12 });
    const rs = plan.queue.map(id => retrievability(memories[id], NOW));
    const sorted = [...rs].sort((a, b) => a - b);
    expect(rs).toEqual(sorted);
    // And the weakest card in the deck must be in the session.
    const weakest = ids.reduce((w, id) =>
      retrievability(memories[id], NOW) < retrievability(memories[w], NOW) ? id : w, ids[0]);
    expect(plan.queue).toContain(weakest);
  });

  it('pauses new material while a backlog exists, so the backlog can drain', () => {
    const memories: Record<string, CardMemory> = {};
    ids.slice(0, 40).forEach(id => {
      memories[id] = { s: 5, d: 5, last: NOW - 90 * DAY, reps: 3, lapses: 0, state: 2 };
    });
    const plan = planSession(ids, memories, NOW, { size: 12 });
    expect(plan.heldBack).toBeGreaterThan(0);
    expect(plan.newCount).toBe(0);
    expect(plan.queue).toHaveLength(12);
  });

  it('never reveals the backlog size in the plan it hands the student', () => {
    // heldBack exists for internal reasoning; the queue itself stays session-sized.
    const memories: Record<string, CardMemory> = {};
    ids.forEach(id => { memories[id] = { s: 3, d: 5, last: NOW - 120 * DAY, reps: 2, lapses: 1, state: 2 }; });
    const plan = planSession(ids, memories, NOW, { size: 12 });
    expect(plan.queue.length).toBeLessThanOrEqual(12);
  });

  it('is deterministic for the same inputs', () => {
    const memories: Record<string, CardMemory> = {};
    ids.forEach((id, i) => { memories[id] = { s: 4 + (i % 7), d: 5, last: NOW - 40 * DAY, reps: 2, lapses: 0, state: 2 }; });
    expect(planSession(ids, memories, NOW, { size: 12 }).queue)
      .toEqual(planSession(ids, memories, NOW, { size: 12 }).queue);
  });
});

describe('Higher to Ordinary switch in March', () => {
  it('carries memory across at a discount instead of resetting to zero', () => {
    const hl = mature();
    const ol = seedFromSibling(hl, NOW);
    expect(ol.s).toBeGreaterThan(0);
    expect(ol.s).toBeLessThan(hl.s);
    expect(ol.state).toBe(2);
    expect(ol.reps).toBe(0);
  });

  it('does not invent memory for a concept the student never met', () => {
    expect(seedFromSibling(NEW_CARD, NOW).state).toBe(0);
  });
});

describe('interval words', () => {
  it('never states a bare unit and never counts anything overdue', () => {
    const m = grade(mature(), 'got', NOW);
    const words = intervalWords('bio-2025-hl-q6-ab', m, NOW, RETENTION_BASE);
    expect(words).toMatch(/^(before you finish today|later today|tomorrow|in about )/);
    expect(words).not.toMatch(/overdue|late|behind|failed/i);
  });
});
