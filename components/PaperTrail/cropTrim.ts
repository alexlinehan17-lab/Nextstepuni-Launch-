/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Trims a scheme crop to the printed answer. Answer-map regions are page-wide
 * bands, so a crop carries the page margins, the blank rest of the page and
 * the running footer; drawn in a side panel that shrank the answer text to
 * about 7px (Oct 2026). Pure, so the band logic is testable without a canvas.
 */

/** Per probe-canvas row: the first and last dark pixel, or null when blank. */
export type InkRow = readonly [number, number] | null;

export interface InkGeometry {
  /** Probe pixels per PDF point. */
  pxPerPt: number;
  /** Where the probe's first row sits on its page, in points from the top. */
  topPt: number;
  /** The page's height in points. */
  pageHeightPt: number;
}

/** A run of inked rows set apart from its neighbours by a wide blank gap. */
export interface InkCluster {
  y0: number;
  y1: number;
  /** Shaped like a running header or footer: short, at the page edge, set
   *  apart. Only words decide whether it is one — see isRunningText. */
  edge: 'header' | 'footer' | null;
}

/** A blank gap this tall separates the answer from a running header/footer. */
const BAND_GAP_PT = 30;
/** Rules thinner than this, set apart at either end, belong to a neighbour's table. */
const THIN_RULE_PT = 4;
const RULE_GAP_PT = 5;
/** White space kept around the trimmed ink. */
export const TRIM_MARGIN_PT = 5;

type Run = [number, number];

function runs(rows: InkRow[], from: number, to: number, gap: number): Run[] {
  const out: Run[] = [];
  let cur: Run | null = null;
  for (let y = from; y <= to; y++) {
    if (!rows[y]) continue;
    if (cur && y - cur[1] > gap) {
      out.push(cur);
      cur = null;
    }
    cur = cur ? [cur[0], y] : [y, y];
  }
  if (cur) out.push(cur);
  return out;
}

/** The inked clusters of a band, with the ones shaped like a page header or
 *  footer marked. */
export function inkClusters(rows: InkRow[], g: InkGeometry): InkCluster[] {
  const pt = (px: number) => px / g.pxPerPt;
  return runs(rows, 0, rows.length - 1, BAND_GAP_PT * g.pxPerPt).map(([y0, y1]) => {
    const top = g.topPt + pt(y0);
    const bottom = g.topPt + pt(y1);
    const height = pt(y1 - y0);
    const edge = top > g.pageHeightPt * 0.9 && height < g.pageHeightPt * 0.07
      ? 'footer'
      : bottom < g.pageHeightPt * 0.06 && height < g.pageHeightPt * 0.05
        ? 'header'
        : null;
    return { y0, y1, edge };
  });
}

/**
 * The inked box spanning the kept clusters, in probe pixels, or null when
 * nothing is kept. A lone rule at either end (the next question's table
 * border) is peeled off.
 */
export function inkBox(rows: InkRow[], g: InkGeometry, kept: InkCluster[]): { x0: number; y0: number; x1: number; y1: number } | null {
  if (!kept.length) return null;
  const pt = (px: number) => px / g.pxPerPt;
  const lines = runs(rows, kept[0].y0, kept[kept.length - 1].y1, 2)
    .filter(([a, b]) => kept.some(c => a >= c.y0 && b <= c.y1));
  if (!lines.length) return null;
  const thin = (r: Run) => pt(r[1] - r[0]) < THIN_RULE_PT;
  while (lines.length > 1 && thin(lines[lines.length - 1]) && pt(lines[lines.length - 1][0] - lines[lines.length - 2][1]) > RULE_GAP_PT) lines.pop();
  while (lines.length > 1 && thin(lines[0]) && pt(lines[1][0] - lines[0][1]) > RULE_GAP_PT) lines.shift();
  const y0 = lines[0][0];
  const y1 = lines[lines.length - 1][1];
  let x0 = Infinity;
  let x1 = -Infinity;
  for (const [a, b] of lines) {
    for (let y = a; y <= b; y++) {
      const row = rows[y];
      if (!row) continue;
      if (row[0] < x0) x0 = row[0];
      if (row[1] > x1) x1 = row[1];
    }
  }
  return { x0, y0, x1, y1 };
}

/** A word on a page, at its baseline's position as page fractions. */
export interface PlacedWord {
  s: string;
  fx: number;
  fy: number;
}

// Page numbers change from page to page, in digits or in words ("page three
// of twenty one" in the LCA schemes), so both read as '#'.
const NUMBER_WORDS = /\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty)\b/g;
const normalise = (s: string) =>
  s.toLowerCase().replace(/\d+/g, '#').replace(NUMBER_WORDS, '#').replace(/#(?:[\s-]*#)+/g, '#').replace(/\s+/g, ' ').trim();

/**
 * True when every word in a page-edge cluster also appears at about the same
 * height on another page: a running header or footer. A question line that
 * happens to sit low on its page (English 2010 OL Q12) is not repeated, so it
 * stays. A cluster with no words (a rule) counts as running.
 */
export function isRunningText(words: PlacedWord[], otherPages: PlacedWord[][]): boolean {
  if (!otherPages.length) return false;
  return words.every(w => {
    const key = normalise(w.s);
    if (!key) return true;
    return otherPages.some(page => page.some(o => Math.abs(o.fy - w.fy) < 0.03 && normalise(o.s) === key));
  });
}

/** Row extents from RGBA pixels: a pixel is ink when its mean channel is dark. */
export function inkRows(data: Uint8ClampedArray, width: number, height: number): InkRow[] {
  const rows: InkRow[] = new Array(height);
  for (let y = 0; y < height; y++) {
    let first = -1;
    let last = -1;
    const base = y * width * 4;
    for (let x = 0; x < width; x++) {
      const i = base + x * 4;
      if (data[i] + data[i + 1] + data[i + 2] < 600) {
        if (first < 0) first = x;
        last = x;
      }
    }
    rows[y] = first < 0 ? null : [first, last];
  }
  return rows;
}
