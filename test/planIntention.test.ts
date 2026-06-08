/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the planner's Intention Engine content: a usable trigger bank, a
 * sourced "why", and a subject-aware default line.
 */
import { describe, it, expect } from 'vitest';
import { PLAN_TRIGGERS, PLAN_WHY, defaultThen } from '../planIntentionData';

describe('Plan Intention data', () => {
  it('ships a usable trigger bank, all non-empty', () => {
    expect(PLAN_TRIGGERS.length).toBeGreaterThan(3);
    for (const t of PLAN_TRIGGERS) expect(t.trim().length).toBeGreaterThan(0);
  });

  it('the why-card cites the implementation-intentions evidence', () => {
    expect(PLAN_WHY.text.trim().length).toBeGreaterThan(0);
    expect(PLAN_WHY.source).toMatch(/Gollwitzer/);
  });

  it('defaultThen names the subject', () => {
    expect(defaultThen('Maths')).toContain('Maths');
  });
});
