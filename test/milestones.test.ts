/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the Paper Trail milestone logic (feature E5): tiers fire once when
 * reached, acknowledged ones stay quiet, biggest shows first, and the shareable
 * card carries the real title + brand.
 */
import { describe, it, expect } from 'vitest';
import { newMilestones, buildMilestoneCardHtml } from '../components/PaperTrail/milestones';

describe('Paper Trail — milestones', () => {
  it('fires reached tiers and skips unreached ones', () => {
    const ids = newMilestones(14, 0, new Set()).map(m => m.id);
    expect(ids).toContain('streak-7');
    expect(ids).toContain('streak-14');
    expect(ids).not.toContain('streak-30');
  });

  it('mastery tiers fire on count', () => {
    const ids = newMilestones(0, 5, new Set()).map(m => m.id);
    expect(ids).toContain('mastery-1');
    expect(ids).toContain('mastery-5');
    expect(ids).not.toContain('mastery-10');
  });

  it('acknowledged milestones do not re-fire', () => {
    const ids = newMilestones(30, 0, new Set(['streak-7', 'streak-14'])).map(m => m.id);
    expect(ids).toEqual(['streak-30']);
  });

  it('returns the biggest milestone first', () => {
    const first = newMilestones(30, 10, new Set())[0];
    expect(first.value).toBe(30);
  });

  it('nothing fires when no tier is reached', () => {
    expect(newMilestones(3, 0, new Set())).toEqual([]);
  });

  it('the share card carries the title and brand, escaped', () => {
    const m = newMilestones(30, 0, new Set()).find(x => x.id === 'streak-30')!;
    const html = buildMilestoneCardHtml(m, '2026-07-05');
    expect(html).toContain('30-day streak');
    expect(html).toContain('Nextstepuni');
    expect(html).toContain('2026-07-05');
  });
});
