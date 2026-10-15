/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Scheme crops are page-wide bands: a 360px panel set Biology 2024 Q1's
 * answers at about 7px, and Q7's crop was two-thirds blank page and footer
 * (Oct 2026). The trim keeps only the printed answer.
 */

import { describe, expect, test } from 'vitest';
import { inkBounds, inkRows, type InkRow } from '@/components/PaperTrail/cropTrim';

// One probe pixel per point keeps the geometry readable: an A4 page is 842pt.
const PAGE = { pxPerPt: 1, topPt: 0, pageHeightPt: 842 };

function band(height: number, ink: [from: number, to: number, x0: number, x1: number][]): InkRow[] {
  const rows: InkRow[] = new Array(height).fill(null);
  for (const [from, to, x0, x1] of ink) for (let y = from; y <= to; y++) rows[y] = [x0, x1];
  return rows;
}

describe('trimming a scheme crop to its printed answer', () => {
  test('a crop that runs to the page bottom loses the blank page and the running footer', () => {
    // Q7 2024: the answer table at the top, then blank page, then the footer.
    const rows = band(780, [[0, 250, 60, 550], [770, 779, 50, 200]]);
    const g = { ...PAGE, topPt: 60 };
    expect(inkBounds(rows, g)).toEqual({ x0: 60, y0: 0, x1: 550, y1: 250 });
  });

  test('the next question\'s table border, set apart below the answer, is not kept', () => {
    const rows = band(340, [[0, 300, 60, 550], [312, 313, 55, 555]]);
    expect(inkBounds(rows, { ...PAGE, topPt: 90 })).toEqual({ x0: 60, y0: 0, x1: 550, y1: 300 });
  });

  test('a rule that closes the table it belongs to stays', () => {
    const rows = band(340, [[0, 300, 60, 550], [303, 304, 55, 555]]);
    expect(inkBounds(rows, { ...PAGE, topPt: 90 })).toEqual({ x0: 55, y0: 0, x1: 555, y1: 304 });
  });

  test('a page header above a continued answer is dropped', () => {
    const rows = band(400, [[10, 25, 200, 400], [80, 380, 60, 550]]);
    expect(inkBounds(rows, PAGE)).toEqual({ x0: 60, y0: 80, x1: 550, y1: 380 });
  });

  test('answer text low on the page is kept when it is part of the answer', () => {
    // No wide gap separates it, so it is not a footer.
    const rows = band(842, [[100, 790, 60, 550]]);
    expect(inkBounds(rows, PAGE)).toEqual({ x0: 60, y0: 100, x1: 550, y1: 790 });
  });

  test('a blank segment has nothing to show', () => {
    expect(inkBounds(band(200, []), PAGE)).toBeNull();
    expect(inkBounds(band(60, [[50, 58, 50, 200]]), { ...PAGE, topPt: 782 })).toBeNull();
  });

  test('ink is read from pixels by darkness, so the grey question bands are not ink', () => {
    const w = 4;
    const px = (v: number) => [v, v, v, 255];
    const data = new Uint8ClampedArray([
      ...px(255), ...px(255), ...px(255), ...px(255),
      ...px(217), ...px(217), ...px(30), ...px(217),
      ...px(255), ...px(0), ...px(255), ...px(0),
    ]);
    expect(inkRows(data, w, 3)).toEqual([null, [2, 2], [1, 3]]);
  });
});
