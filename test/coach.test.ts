/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Coach (F2) — composer unit tests. Seeds the underlying localStorage
 * stores directly and asserts the composed plan: ordering, capping, and the
 * quiet empty state.
 */
import { beforeEach, describe, expect, it } from 'vitest';
import { composeCoach } from '../components/PaperTrail/coach';
import { saveChair, loadChair, mergeMisses, type ChairState } from '../components/ExaminersChair/store';

const UID = 'coach-test';
const NOW = 1_750_000_000_000;

beforeEach(() => localStorage.clear());

describe('composeCoach', () => {
  it('returns an empty plan when there is no signal at all', () => {
    expect(composeCoach(UID, NOW)).toEqual([]);
  });

  it('leads with due reviews when the deck has them', () => {
    localStorage.setItem(
      `pt:review:${UID}`,
      JSON.stringify({ q1: { dueTs: NOW - 1000, addedTs: NOW - 86_400_000 } }),
    );
    const plan = composeCoach(UID, NOW);
    expect(plan.length).toBeGreaterThan(0);
    expect(plan[0].id).toBe('review-due');
    expect(plan[0].route).toBe('review');
  });

  it('surfaces the top calibration blind spot as a chair action', () => {
    const base: ChairState = loadChair(UID);
    const withMiss = mergeMisses(
      base,
      [{ key: 'business::Link', subject: 'business', label: 'Link', over: 3, under: 0, sessionId: 's1' }],
      NOW,
    );
    saveChair(UID, withMiss);
    const plan = composeCoach(UID, NOW);
    const blind = plan.find(i => i.id === 'blind-spot');
    expect(blind).toBeDefined();
    expect(blind!.route).toBe('chair');
    expect(blind!.title).toContain('Link');
  });

  it('caps the plan at three actions', () => {
    localStorage.setItem(
      `pt:review:${UID}`,
      JSON.stringify({ q1: { dueTs: NOW - 1000, addedTs: NOW - 86_400_000 } }),
    );
    const base: ChairState = loadChair(UID);
    saveChair(
      UID,
      mergeMisses(
        base,
        [{ key: 'a::x', subject: 'a', label: 'x', over: 2, under: 0, sessionId: 's' }],
        NOW,
      ),
    );
    expect(composeCoach(UID, NOW).length).toBeLessThanOrEqual(3);
  });
});
