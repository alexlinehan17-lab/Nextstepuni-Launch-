/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the Paper Trail spaced-recall scheduler (feature A2). The SM-2 core is
 * pure, so we can pin its behaviour: failing resets the streak and brings the
 * card back within a day; passing grows the interval; ease never collapses.
 */
import { describe, it, expect } from 'vitest';
import { schedule, type Sm2State } from '../components/PaperTrail/reviewStore';

const START: Sm2State = { ease: 2.5, intervalDays: 0, reps: 0, lapses: 0 };

describe('Paper Trail — SM-2 spaced-recall scheduler', () => {
  it('a fresh card graded "good" comes back in a day, then grows', () => {
    const a = schedule(START, 'good');
    expect(a.reps).toBe(1);
    expect(a.intervalDays).toBe(1);
    const b = schedule(a, 'good');
    expect(b.reps).toBe(2);
    expect(b.intervalDays).toBe(4);
    const c = schedule(b, 'good');
    expect(c.reps).toBe(3);
    expect(c.intervalDays).toBeGreaterThan(b.intervalDays); // interval * ease
  });

  it('"again" resets the streak, schedules a same-day retry, and counts a lapse', () => {
    const grown = schedule(schedule(schedule(START, 'good'), 'good'), 'good');
    const lapsed = schedule(grown, 'again');
    expect(lapsed.reps).toBe(0);
    expect(lapsed.intervalDays).toBe(1);
    expect(lapsed.lapses).toBe(grown.lapses + 1);
  });

  it('ease is clamped and never falls below 1.3, even after repeated failures', () => {
    let s = START;
    for (let i = 0; i < 12; i++) s = schedule(s, 'again');
    expect(s.ease).toBeGreaterThanOrEqual(1.3);
  });

  it('"easy" advances faster than "good", and "hard" slower, on a mature card', () => {
    const mature = schedule(schedule(schedule(START, 'good'), 'good'), 'good');
    const easy = schedule(mature, 'easy');
    const good = schedule(mature, 'good');
    const hard = schedule(mature, 'hard');
    expect(easy.intervalDays).toBeGreaterThanOrEqual(good.intervalDays);
    expect(hard.intervalDays).toBeLessThan(good.intervalDays);
  });

  it('every passed card advances by at least a day (never stalls same-day)', () => {
    for (const g of ['hard', 'good', 'easy'] as const) {
      expect(schedule(START, g).intervalDays).toBeGreaterThanOrEqual(1);
    }
  });
});
