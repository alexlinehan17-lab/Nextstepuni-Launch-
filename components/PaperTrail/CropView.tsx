/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — generic PDF region renderer, extracted from the Viewer so the
 * Topic Vault can render PAPER crops with the same machinery the answer
 * reveal uses for SCHEME crops.
 *
 * Renders each region segment (a fractional rect of a page) as its own
 * canvas, stacked vertically — the student sees a continuous crop of the real
 * document. Page-render → offscreen → blit pattern with a canvas-pixel clamp.
 */

import React, { useEffect, useRef, useState } from 'react';
import type { PDFDocumentProxy } from 'pdfjs-dist';
import { type PaperAnswerSeg } from '../../types/paperTrail';
import { inkBounds, inkRows, TRIM_MARGIN_PT } from './cropTrim';

// Same clamp the Viewer uses for full pages — keeps low-memory devices safe.
const MAX_CANVAS_PIXELS = 14_000_000;

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

type Rect = [number, number, number, number];

/** Trimmed rects per document, keyed by segment, so a zoom step or a panel
 *  resize never re-scans the page. null marks a blank segment. */
const trimCache = new WeakMap<PDFDocumentProxy, Map<string, Rect | null>>();
/** Width of the low-resolution render the ink scan reads. */
const PROBE_WIDTH = 600;
/** Ink shorter than this is checked for words before it is shown. */
const SLIVER_PT = 20;

const clamp = (v: number, lo: number, hi: number) => Math.min(Math.max(v, lo), hi);

const CropView: React.FC<{
  pdf: PDFDocumentProxy;
  region: PaperAnswerSeg[];
  /** Accessible label per rendered page. Defaults to the scheme wording the
   *  answer reveal has always used. */
  ariaLabel?: (page: number) => string;
  /** Shown when rendering fails. */
  failText?: string;
  /** Additional clockwise rotation for complete source pages. */
  rotation?: 0 | 90 | 180 | 270;
  /** Raised by readers with explicit zoom controls; the pixel safety cap still applies. */
  maxWidth?: number;
  /** Cut each segment down to its printed ink: no page margins, blank page,
   *  running header/footer or stray neighbouring rule. Segments share one
   *  horizontal extent so they stack at one scale. */
  trim?: boolean;
  /** Multiple of the fitted width; past 1 the crop overflows its host, which
   *  scrolls. */
  zoom?: number;
  /** Re-render when the host's width changes (a panel that resizes). */
  responsive?: boolean;
}> = ({ pdf, region, ariaLabel, failText, rotation = 0, maxWidth = 900, trim = false, zoom = 1, responsive = false }) => {
  const outerRef = useRef<HTMLDivElement | null>(null);
  const hostRef = useRef<HTMLDivElement | null>(null);
  const [failed, setFailed] = useState(false);
  const [width, setWidth] = useState(0);
  const renderedWidth = useRef(0);

  useEffect(() => {
    const el = outerRef.current;
    if (!responsive || !el || typeof ResizeObserver === 'undefined') return;
    let timer: ReturnType<typeof setTimeout> | null = null;
    const ro = new ResizeObserver(() => {
      if (timer) clearTimeout(timer);
      timer = setTimeout(() => {
        if (Math.abs(el.clientWidth - renderedWidth.current) > 2) setWidth(el.clientWidth);
      }, 120);
    });
    ro.observe(el);
    return () => {
      ro.disconnect();
      if (timer) clearTimeout(timer);
    };
  }, [responsive]);

  useEffect(() => {
    let cancelled = false;
    let task: { promise: Promise<void>; cancel: () => void } | null = null;
    const outer = outerRef.current;
    const host = hostRef.current;
    if (!outer || !host) return;
    // Trimmed, zoomed and resizing crops swap in whole, so a re-render never
    // flashes an empty panel; plain crops keep appending as they arrive.
    const buffered = trim || zoom !== 1 || responsive;
    if (!buffered) host.replaceChildren();
    setFailed(false);

    const pageRotationOf = (page: { rotate?: number }, seg: PaperAnswerSeg) =>
      ((page.rotate ?? 0) + rotation + (seg.rotate ?? 0)) % 360;

    // The printed ink inside one segment, as a rect in the same (rotated)
    // page fractions the renderer clips by.
    const probe = async (seg: PaperAnswerSeg): Promise<Rect | null | undefined> => {
      const r = rotatedCropRect(seg.r ?? [0, 0, 1, 1], seg.rotate);
      const key = `${seg.p}|${r.join(',')}|${seg.rotate ?? 0}|${rotation}`;
      let cache = trimCache.get(pdf);
      if (!cache) trimCache.set(pdf, (cache = new Map()));
      if (cache.has(key)) return cache.get(key);
      const page = await pdf.getPage(seg.p);
      if (cancelled) {
        page.cleanup();
        return undefined;
      }
      const pageRotation = pageRotationOf(page, seg);
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
      task = page.render({ canvas, viewport: vp, transform: [1, 0, 0, 1, -r[0] * base.width * scale, -r[1] * base.height * scale] });
      await task.promise;
      task = null;
      if (cancelled) {
        page.cleanup();
        return undefined;
      }
      const box = inkBounds(inkRows(ctx.getImageData(0, 0, W, H).data, W, H), {
        pxPerPt: scale,
        topPt: r[1] * base.height,
        pageHeightPt: base.height,
      });
      canvas.width = 0;
      canvas.height = 0;
      const m = TRIM_MARGIN_PT * scale;
      const fx = (px: number) => r[0] + (clamp(px, 0, W) / W) * (r[2] - r[0]);
      const fy = (px: number) => r[1] + (clamp(px, 0, H) / H) * (r[3] - r[1]);
      let out: Rect | null = box ? [fx(box.x0 - m), fy(box.y0 - m), fx(box.x1 + 1 + m), fy(box.y1 + 1 + m)] : null;
      // A short strip with no words in it is the edge of a neighbouring table
      // where the region crosses a page, not part of the answer.
      if (out && box && (box.y1 - box.y0) / scale < SLIVER_PT) {
        const words = await page.getTextContent().catch(() => null);
        if (cancelled) {
          page.cleanup();
          return undefined;
        }
        const [a, b, c, d] = out;
        // A word counts only when its baseline sits inside the shown strip;
        // the next question's heading starts just below the region.
        const bottom = Math.min(d, r[3]) + 2 / base.height;
        const inside = words?.items.some(item => {
          if (!('str' in item) || !item.str.trim()) return false;
          const [vx, vy] = base.convertToViewportPoint(item.transform[4], item.transform[5]);
          const fxv = vx / base.width;
          const fyv = vy / base.height;
          return fxv >= a && fxv <= c && fyv >= b && fyv <= bottom;
        });
        if (words && !inside) out = null;
      }
      page.cleanup();
      cache.set(key, out);
      return out;
    };

    const pieces = async (): Promise<{ seg: PaperAnswerSeg; rect: Rect }[] | null> => {
      const plain = region.map(seg => ({ seg, rect: rotatedCropRect(seg.r ?? [0, 0, 1, 1], seg.rotate) }));
      if (!trim) return plain;
      const found: { seg: PaperAnswerSeg; rect: Rect; ink: Rect }[] = [];
      for (const { seg, rect } of plain) {
        const ink = await probe(seg);
        if (ink === undefined) return null; // cancelled
        if (ink) found.push({ seg, rect, ink });
      }
      if (!found.length) return plain;
      const x0 = Math.min(...found.map(f => f.ink[0]));
      const x1 = Math.max(...found.map(f => f.ink[2]));
      return found.map(({ seg, rect, ink }) => ({ seg, rect: [Math.max(x0, rect[0]), ink[1], Math.min(x1, rect[2]), ink[3]] }));
    };

    (async () => {
      try {
        renderedWidth.current = outer.clientWidth;
        const cssWidth = Math.min(outer.clientWidth || 320, maxWidth) * zoom;
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        const list = await pieces();
        if (!list || cancelled) return;
        const out: HTMLCanvasElement[] = [];
        for (const { seg, rect: r } of list) {
          if (cancelled) return;
          const page = await pdf.getPage(seg.p);
          if (cancelled) {
            page.cleanup();
            return;
          }
          const pageRotation = pageRotationOf(page, seg);
          const base = page.getViewport({ scale: 1, rotation: pageRotation });
          const clipW = (r[2] - r[0]) * base.width;
          const clipH = (r[3] - r[1]) * base.height;
          if (clipW <= 0 || clipH <= 0) {
            page.cleanup();
            continue;
          }
          let scale = (cssWidth / clipW) * dpr;
          const pixels = clipW * scale * (clipH * scale);
          if (pixels > MAX_CANVAS_PIXELS) scale *= Math.sqrt(MAX_CANVAS_PIXELS / pixels);
          const vp = page.getViewport({ scale, rotation: pageRotation });
          const canvas = document.createElement('canvas');
          canvas.width = Math.floor(clipW * scale);
          canvas.height = Math.floor(clipH * scale);
          // Shift the page so the clip rect's top-left lands at canvas (0,0).
          const transform = [1, 0, 0, 1, -r[0] * base.width * scale, -r[1] * base.height * scale];
          task = page.render({ canvas, viewport: vp, transform });
          await task.promise;
          task = null;
          if (cancelled) {
            page.cleanup();
            return;
          }
          canvas.className = trim
            ? 'block w-full h-auto bg-white rounded-[3px] ring-1 ring-zinc-200 dark:ring-zinc-700 mb-2 last:mb-0'
            : 'block w-full h-auto rounded-md shadow-sm mb-2 bg-white';
          canvas.style.maxWidth = `${Math.floor((clipW * scale) / dpr)}px`;
          canvas.setAttribute('role', 'img');
          canvas.setAttribute(
            'aria-label',
            ariaLabel
              ? ariaLabel(seg.p)
              : `Marking scheme page ${seg.p}, shown as an image — © State Examinations Commission`,
          );
          if (buffered) out.push(canvas);
          else host.appendChild(canvas);
          page.cleanup();
        }
        if (buffered && !cancelled) {
          host.style.maxWidth = zoom > 1 ? 'none' : `${maxWidth}px`;
          host.style.width = zoom > 1 ? `${cssWidth}px` : '';
          host.replaceChildren(...out);
        }
      } catch (e) {
        // a cancelled render rejects routinely — only surface real failures
        if (!cancelled && e instanceof Error && e.name !== 'RenderingCancelledException') setFailed(true);
      }
    })();
    return () => {
      cancelled = true;
      task?.cancel();
    };
  }, [pdf, region, ariaLabel, rotation, maxWidth, trim, zoom, responsive, width]);

  return (
    <div ref={outerRef}>
      <div ref={hostRef} className="mx-auto" style={{ maxWidth }} />
      {failed && (
        <p className="text-[12px] text-zinc-500 text-center py-4">
          {failText ?? 'Couldn’t render this region — open the full scheme.'}
        </p>
      )}
    </div>
  );
};

export default CropView;
