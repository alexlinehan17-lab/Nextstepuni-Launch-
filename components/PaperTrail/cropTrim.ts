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

/**
 * The inked box worth showing, in probe pixels, or null when the band is
 * blank. Drops a page footer (short, in the bottom tenth, set apart by a wide
 * gap), a page header (the same at the top), and a lone rule at either end
 * (the next question's table border).
 */
export function inkBounds(rows: InkRow[], g: InkGeometry): { x0: number; y0: number; x1: number; y1: number } | null {
  const pt = (px: number) => px / g.pxPerPt;
  const clusters = runs(rows, 0, rows.length - 1, BAND_GAP_PT * g.pxPerPt).filter(([a, b]) => {
    const top = g.topPt + pt(a);
    const bottom = g.topPt + pt(b);
    const height = pt(b - a);
    const footer = top > g.pageHeightPt * 0.9 && height < g.pageHeightPt * 0.07;
    const header = bottom < g.pageHeightPt * 0.06 && height < g.pageHeightPt * 0.05;
    return !footer && !header;
  });
  if (!clusters.length) return null;
  const lines = runs(rows, clusters[0][0], clusters[clusters.length - 1][1], 2);
  const thin = (r: Run) => pt(r[1] - r[0]) < THIN_RULE_PT;
  while (lines.length > 1 && thin(lines[lines.length - 1]) && pt(lines[lines.length - 1][0] - lines[lines.length - 2][1]) > RULE_GAP_PT) lines.pop();
  while (lines.length > 1 && thin(lines[0]) && pt(lines[1][0] - lines[0][1]) > RULE_GAP_PT) lines.shift();
  const y0 = lines[0][0];
  const y1 = lines[lines.length - 1][1];
  let x0 = Infinity;
  let x1 = -Infinity;
  for (let y = y0; y <= y1; y++) {
    const row = rows[y];
    if (!row) continue;
    if (row[0] < x0) x0 = row[0];
    if (row[1] > x1) x1 = row[1];
  }
  return { x0, y0, x1, y1 };
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
