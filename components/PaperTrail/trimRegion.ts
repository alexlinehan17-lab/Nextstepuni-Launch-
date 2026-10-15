/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Trims a region's segments to their printed ink by scanning a low-resolution
 * render (see cropTrim.ts for the band rules). Shared by CropView and the
 * cross-subject audit harness, so the audit measures what students see.
 */

import type { PDFDocumentProxy } from 'pdfjs-dist';
import { type PaperAnswerSeg } from '../../types/paperTrail';
import { inkBox, inkClusters, inkRows, isRunningText, TRIM_MARGIN_PT, type PlacedWord } from './cropTrim';

export type Rect = [number, number, number, number];

/** Cancellation shared with the caller's render effect. */
export interface TrimRun {
  cancelled: boolean;
  task: { cancel: () => void } | null;
}

/** Keep the same source rectangle when turning a sideways table upright. */
export function rotatedCropRect(r: [number, number, number, number], rotate: PaperAnswerSeg['rotate']): [number, number, number, number] {
  const [x0, y0, x1, y1] = r;
  switch (rotate) {
    case 90: return [1 - y1, x0, 1 - y0, x1];
    case 180: return [1 - x1, 1 - y1, 1 - x0, 1 - y0];
    case 270: return [y0, 1 - x1, y1, 1 - x0];
    default: return r;
  }
}

/** Trimmed rects per document, keyed by segment, so a zoom step or a panel
 *  resize never re-scans the page. null marks a blank segment. */
const trimCache = new WeakMap<PDFDocumentProxy, Map<string, Rect | null>>();
/** Width of the low-resolution render the ink scan reads. */
const PROBE_WIDTH = 600;
/** Ink shorter than this is checked for words before it is shown. */
const SLIVER_PT = 20;

const clamp = (v: number, lo: number, hi: number) => Math.min(Math.max(v, lo), hi);

/** Each page's words at their baselines, per document and rotation. */
const wordCache = new WeakMap<PDFDocumentProxy, Map<string, Promise<PlacedWord[] | null>>>();

function pageWords(pdf: PDFDocumentProxy, p: number, rotation: number): Promise<PlacedWord[] | null> {
  let cache = wordCache.get(pdf);
  if (!cache) wordCache.set(pdf, (cache = new Map()));
  const key = `${p}|${rotation}`;
  let found = cache.get(key);
  if (!found) {
    found = (async () => {
      const page = await pdf.getPage(p);
      const vp = page.getViewport({ scale: 1, rotation: ((page.rotate ?? 0) + rotation) % 360 });
      const text = await page.getTextContent();
      return text.items.flatMap(item => {
        if (!('str' in item) || !item.str.trim()) return [];
        const [x, y] = vp.convertToViewportPoint(item.transform[4], item.transform[5]);
        return [{ s: item.str, fx: x / vp.width, fy: y / vp.height }];
      });
    })().catch(() => null);
    cache.set(key, found);
  }
  return found;
}

// The printed ink inside one segment, as a rect in the same (rotated)
// page fractions the renderer clips by.
async function probe(pdf: PDFDocumentProxy, seg: PaperAnswerSeg, rotation: number, run: TrimRun): Promise<Rect | null | undefined> {
  const r = rotatedCropRect(seg.r ?? [0, 0, 1, 1], seg.rotate);
  const key = `${seg.p}|${r.join(',')}|${seg.rotate ?? 0}|${rotation}`;
  let cache = trimCache.get(pdf);
  if (!cache) trimCache.set(pdf, (cache = new Map()));
  if (cache.has(key)) return cache.get(key);
  const page = await pdf.getPage(seg.p);
  if (run.cancelled) {
    page.cleanup();
    return undefined;
  }
  const pageRotation = ((page.rotate ?? 0) + rotation + (seg.rotate ?? 0)) % 360;
  const base = page.getViewport({ scale: 1, rotation: pageRotation });
  const clipW = (r[2] - r[0]) * base.width;
  const clipH = (r[3] - r[1]) * base.height;
  if (clipW <= 0 || clipH <= 0) {
    page.cleanup();
    return null;
  }
  const scale = PROBE_WIDTH / clipW;
  const canvas = document.createElement('canvas');
  const W = PROBE_WIDTH;
  const H = Math.max(1, Math.round(clipH * scale));
  canvas.width = W;
  canvas.height = H;
  const ctx = canvas.getContext('2d', { willReadFrequently: true });
  if (!ctx) {
    page.cleanup();
    return r; // no pixels to read: show the segment untrimmed
  }
  ctx.fillStyle = '#fff';
  ctx.fillRect(0, 0, W, H);
  const vp = page.getViewport({ scale, rotation: pageRotation });
  const task = page.render({ canvas, viewport: vp, transform: [1, 0, 0, 1, -r[0] * base.width * scale, -r[1] * base.height * scale] });
  run.task = task;
  await task.promise;
  run.task = null;
  if (run.cancelled) {
    page.cleanup();
    return undefined;
  }
  const rows = inkRows(ctx.getImageData(0, 0, W, H).data, W, H);
  const geometry = { pxPerPt: scale, topPt: r[1] * base.height, pageHeightPt: base.height };
  const clusters = inkClusters(rows, geometry);
  const extra = ((seg.rotate ?? 0) + rotation) % 360;
  // A cluster at the page edge is dropped only when its words repeat at the
  // same height on a neighbouring page: a running header or footer. A
  // question line that happens to sit there stays.
  let kept = clusters.filter(c => !c.edge);
  if (kept.length < clusters.length) {
    const words = await pageWords(pdf, seg.p, extra);
    const others = (await Promise.all([seg.p - 1, seg.p + 1]
      .filter(n => n >= 1 && n <= pdf.numPages)
      .map(n => pageWords(pdf, n, extra)))).filter((w): w is PlacedWord[] => !!w?.length);
    if (run.cancelled) {
      page.cleanup();
      return undefined;
    }
    const toFy = (px: number) => (r[1] * base.height + px / scale) / base.height;
    kept = clusters.filter(c => {
      if (!c.edge) return true;
      if (!words?.length) return true; // scanned: no words to judge by, so keep it
      const inside = words.filter(w => w.fx >= r[0] && w.fx <= r[2] && w.fy >= toFy(c.y0) - 0.002 && w.fy <= toFy(c.y1) + 0.004);
      return !isRunningText(inside, others);
    });
  }
  const box = inkBox(rows, geometry, kept);
  canvas.width = 0;
  canvas.height = 0;
  const m = TRIM_MARGIN_PT * scale;
  const fx = (px: number) => r[0] + (clamp(px, 0, W) / W) * (r[2] - r[0]);
  const fy = (px: number) => r[1] + (clamp(px, 0, H) / H) * (r[3] - r[1]);
  let out: Rect | null = box ? [fx(box.x0 - m), fy(box.y0 - m), fx(box.x1 + 1 + m), fy(box.y1 + 1 + m)] : null;
  // A short strip with no words in it is the edge of a neighbouring table
  // where the region crosses a page, not part of the answer.
  if (out && box && (box.y1 - box.y0) / scale < SLIVER_PT) {
    const words = await pageWords(pdf, seg.p, extra);
    if (run.cancelled) {
      page.cleanup();
      return undefined;
    }
    const [a, b, c, d] = out;
    // A word counts only when its baseline sits inside the shown strip;
    // the next question's heading starts just below the region.
    const bottom = Math.min(d, r[3]) + 2 / base.height;
    const inside = words?.some(w => w.fx >= a && w.fx <= c && w.fy >= b && w.fy <= bottom);
    // A scanned page has no text layer, so absence of words proves nothing there.
    if (words?.length && !inside) out = null;
  }
  page.cleanup();
  cache.set(key, out);
  return out;
}

/**
 * Each segment cut to its ink, sharing one horizontal extent so they stack at
 * one scale. Blank segments drop out; if every segment is blank the region is
 * returned untrimmed. null when cancelled.
 */
export async function trimRegion(
  pdf: PDFDocumentProxy,
  region: PaperAnswerSeg[],
  rotation: number,
  run: TrimRun,
): Promise<{ seg: PaperAnswerSeg; rect: Rect }[] | null> {
  const plain = region.map(seg => ({ seg, rect: rotatedCropRect(seg.r ?? [0, 0, 1, 1], seg.rotate) }));
  const found: { seg: PaperAnswerSeg; rect: Rect; ink: Rect }[] = [];
  for (const { seg, rect } of plain) {
    const ink = await probe(pdf, seg, rotation, run);
    if (ink === undefined) return null; // cancelled
    if (ink) found.push({ seg, rect, ink });
  }
  if (!found.length) return plain;
  const x0 = Math.min(...found.map(f => f.ink[0]));
  const x1 = Math.max(...found.map(f => f.ink[2]));
  return found.map(({ seg, rect, ink }) => ({ seg, rect: [Math.max(x0, rect[0]), ink[1], Math.min(x1, rect[2]), ink[3]] }));
}
