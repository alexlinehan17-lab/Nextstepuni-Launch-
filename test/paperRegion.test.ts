/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Topic Vault — paper-side region synthesis. A wrong crop shown to a student
 * is the worst failure, so the null (refuse) paths matter as much as the
 * happy paths.
 */

import { describe, it, expect } from 'vitest';
import { paperRegionFor } from '../components/PaperTrail/paperRegion';
import { type PaperAnswerQuestion } from '../types/paperTrail';

const q = (n: string, pP: number, y0: number, y1: number): PaperAnswerQuestion => ({
  n,
  pP,
  pY: [y0, y1],
  region: [{ p: 1 }],
  mode: 'crop',
  conf: 1,
});

describe('paperRegionFor', () => {
  it('crops from the anchor to the next anchor on the same page', () => {
    const qs = [q('1', 3, 0.1, 0.4), q('2', 3, 0.45, 0.8)];
    const r = paperRegionFor(qs, '1')!;
    expect(r).toHaveLength(1);
    expect(r[0].p).toBe(3);
    expect(r[0].r![1]).toBeCloseTo(0.092, 3); // 0.1 - pad
    expect(r[0].r![3]).toBeCloseTo(0.45, 5);  // next anchor's start
  });

  it('spans pages up to the next anchor, dropping a negligible tail', () => {
    const qs = [q('1', 2, 0.5, 1), q('2', 4, 0.02, 0.6)];
    const r = paperRegionFor(qs, '1')!;
    // page 2 from anchor, page 3 whole; page-4 tail (0.02) is below MIN_TAIL
    expect(r.map(s => s.p)).toEqual([2, 3]);
    expect(r[0].r![3]).toBe(1);
    expect(r[1].r).toEqual([0, 0, 1, 1]);
  });

  it('keeps a meaningful tail on the next question’s page', () => {
    const qs = [q('1', 2, 0.5, 1), q('2', 3, 0.4, 0.9)];
    const r = paperRegionFor(qs, '1')!;
    expect(r.map(s => s.p)).toEqual([2, 3]);
    expect(r[1].r![3]).toBeCloseTo(0.4, 5);
  });

  it('uses the question’s own band when it is the last anchor', () => {
    const qs = [q('1', 1, 0.1, 0.3), q('2', 2, 0.2, 0.7)];
    const r = paperRegionFor(qs, '2')!;
    expect(r).toEqual([{ p: 2, r: [0, expect.closeTo(0.192, 3), 1, 0.7] }]);
  });

  it('runs to the page bottom when the last anchor’s band is degenerate', () => {
    const qs = [q('1', 1, 0.6, 0.6)];
    const r = paperRegionFor(qs, '1')!;
    expect(r[0].r![3]).toBe(1);
  });

  it('refuses unknown questions, huge spans and non-monotonic anchors', () => {
    const qs = [q('1', 1, 0.1, 0.5), q('2', 6, 0.1, 0.5)];
    expect(paperRegionFor(qs, '9')).toBeNull();
    expect(paperRegionFor(qs, '1')).toBeNull(); // 5-page span > MAX_PAGES
    const bad = [q('1', 3, 0.5, 0.9), q('2', 3, 0.5, 0.9)]; // same spot
    expect(paperRegionFor(bad, '1')).toBeNull();
    expect(paperRegionFor([], '1')).toBeNull();
  });

  it('sorts anchors into printed order before deriving', () => {
    const qs = [q('2', 3, 0.45, 0.8), q('1', 3, 0.1, 0.4)]; // reversed input
    const r = paperRegionFor(qs, '1')!;
    expect(r[0].r![3]).toBeCloseTo(0.45, 5);
  });
});
