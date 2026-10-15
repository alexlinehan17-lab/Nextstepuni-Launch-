/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Scheme crops are page-wide bands: a 360px panel set Biology 2024 Q1's
 * answers at about 7px, and Q7's crop was two-thirds blank page and footer
 * (Oct 2026). The trim keeps only the printed answer, and never a question
 * line that merely sits at the page edge.
 */

import { describe, expect, test } from 'vitest';
import { inkBox, inkClusters, inkRows, isRunningText, type InkRow } from '@/components/PaperTrail/cropTrim';

// One probe pixel per point keeps the geometry readable: an A4 page is 842pt.
const PAGE = { pxPerPt: 1, topPt: 0, pageHeightPt: 842 };

function band(height: number, ink: [from: number, to: number, x0: number, x1: number][]): InkRow[] {
  const rows: InkRow[] = new Array(height).fill(null);
  for (const [from, to, x0, x1] of ink) for (let y = from; y <= to; y++) rows[y] = [x0, x1];
  return rows;
}

const withoutEdges = (rows: InkRow[], g = PAGE) => inkBox(rows, g, inkClusters(rows, g).filter(c => !c.edge));

describe('finding the printed answer in a scheme crop', () => {
  test('a crop that runs to the page bottom marks the running footer as a page edge', () => {
    // Q7 2024: the answer table at the top, then blank page, then the footer.
    const rows = band(780, [[0, 250, 60, 550], [770, 779, 50, 200]]);
    const g = { ...PAGE, topPt: 60 };
    expect(inkClusters(rows, g).map(c => c.edge)).toEqual([null, 'footer']);
    expect(withoutEdges(rows, g)).toEqual({ x0: 60, y0: 0, x1: 550, y1: 250 });
  });

  test('a line at the very top of the page is marked as a possible header', () => {
    const rows = band(400, [[10, 25, 200, 400], [80, 380, 60, 550]]);
    expect(inkClusters(rows, PAGE).map(c => c.edge)).toEqual(['header', null]);
  });

  test('answer text low on the page is not a page edge when no wide gap separates it', () => {
    const rows = band(842, [[100, 790, 60, 550]]);
    expect(inkClusters(rows, PAGE)).toEqual([{ y0: 100, y1: 790, edge: null }]);
  });

  test('a kept edge cluster stays in the box', () => {
    const rows = band(842, [[600, 700, 60, 550], [800, 812, 90, 500]]);
    expect(inkBox(rows, PAGE, inkClusters(rows, PAGE))).toEqual({ x0: 60, y0: 600, x1: 550, y1: 812 });
  });

  test('the next question\'s table border, set apart below the answer, is not kept', () => {
    const rows = band(340, [[0, 300, 60, 550], [312, 313, 55, 555]]);
    expect(withoutEdges(rows, { ...PAGE, topPt: 90 })).toEqual({ x0: 60, y0: 0, x1: 550, y1: 300 });
  });

  test('a rule that closes the table it belongs to stays', () => {
    const rows = band(340, [[0, 300, 60, 550], [303, 304, 55, 555]]);
    expect(withoutEdges(rows, { ...PAGE, topPt: 90 })).toEqual({ x0: 55, y0: 0, x1: 555, y1: 304 });
  });

  test('a blank band has nothing to show', () => {
    expect(withoutEdges(band(200, []))).toBeNull();
  });

  test('ink is read from pixels by darkness, so the grey question bands are not ink', () => {
    const px = (v: number) => [v, v, v, 255];
    const data = new Uint8ClampedArray([
      ...px(255), ...px(255), ...px(255), ...px(255),
      ...px(217), ...px(217), ...px(30), ...px(217),
      ...px(255), ...px(0), ...px(255), ...px(0),
    ]);
    expect(inkRows(data, 4, 3)).toEqual([null, [2, 2], [1, 3]]);
  });
});

describe('telling a running header or footer from a question line', () => {
  const footer = (n: number, page: string) => [
    { s: 'Leaving Certificate 2024', fx: 0.1, fy: 0.93 },
    { s: String(n), fx: 0.5, fy: 0.93 },
    { s: page, fx: 0.1, fy: 0.95 },
  ];

  test('a footer repeated on the next page is running, page number and all', () => {
    expect(isRunningText(footer(11, 'Marking Scheme'), [footer(12, 'Marking Scheme')])).toBe(true);
  });

  test('page numbers written as words still match (LCA schemes)', () => {
    const here = [{ s: 'page three of twenty one', fx: 0.4, fy: 0.968 }];
    const next = [{ s: 'page four of twenty one', fx: 0.4, fy: 0.97 }];
    expect(isRunningText(here, [next])).toBe(true);
  });

  test('a question line low on its page is not running (English 2010 OL Q12)', () => {
    const here = [{ s: 'Which is your favourite stanza in this poem? Explain why you like it.', fx: 0.19, fy: 0.916 }];
    expect(isRunningText(here, [footer(35, 'Marking Scheme')])).toBe(false);
  });

  test('a question stem at the top of its page is not running (LCA Active Leisure 2011 Q7)', () => {
    const here = [{ s: 'health benefits people get from regular swimming.', fx: 0.2, fy: 0.043 }];
    const next = [{ s: 'A swimmer is in difficulty off a pier. Explain', fx: 0.2, fy: 0.042 }];
    expect(isRunningText(here, [next])).toBe(false);
  });

  test('with no other page to compare, nothing is called running', () => {
    expect(isRunningText(footer(1, 'Marking Scheme'), [])).toBe(false);
  });

  test('a wordless rule at the page edge counts as running', () => {
    expect(isRunningText([], [footer(2, 'Marking Scheme')])).toBe(true);
  });
});
