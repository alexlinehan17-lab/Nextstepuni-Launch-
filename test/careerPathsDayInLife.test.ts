/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the "A Day in the Life" decision-sim data: every moment must be
 * well-formed (≥2 options, a valid correct + tempting index that differ,
 * non-empty consequence/fix, and a source) — or the sim renders broken.
 */
import { describe, it, expect } from 'vitest';
import { CAREERS } from '../careerPathsData';

describe('Career Paths — A Day in the Life sim data', () => {
  const withSim = CAREERS.filter((c) => c.dayInLife);

  it('ships at least one authored decision sim', () => {
    expect(withSim.length).toBeGreaterThan(0);
  });

  it('every moment is well-formed', () => {
    for (const c of withSim) {
      expect(c.dayInLife!.moments.length, `${c.id}: no moments`).toBeGreaterThan(0);
      for (const m of c.dayInLife!.moments) {
        expect(m.options.length, `${c.id}: <2 options`).toBeGreaterThanOrEqual(2);
        expect(m.correctIndex, `${c.id}: correctIndex out of range`).toBeGreaterThanOrEqual(0);
        expect(m.correctIndex, `${c.id}: correctIndex out of range`).toBeLessThan(m.options.length);
        expect(m.temptingIndex, `${c.id}: temptingIndex out of range`).toBeGreaterThanOrEqual(0);
        expect(m.temptingIndex, `${c.id}: temptingIndex out of range`).toBeLessThan(m.options.length);
        expect(m.temptingIndex, `${c.id}: tempting === correct (no real wrong choice)`).not.toBe(m.correctIndex);
        expect(m.setup.trim().length, `${c.id}: empty setup`).toBeGreaterThan(0);
        expect(m.consequence.trim().length, `${c.id}: empty consequence`).toBeGreaterThan(0);
        expect(m.fix.trim().length, `${c.id}: empty fix`).toBeGreaterThan(0);
        expect(m.source.trim().length, `${c.id}: missing source`).toBeGreaterThan(0);
      }
    }
  });
});
