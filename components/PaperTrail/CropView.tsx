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
import { rotatedCropRect, trimRegion, type TrimRun } from './trimRegion';

// Same clamp the Viewer uses for full pages — keeps low-memory devices safe.
const MAX_CANVAS_PIXELS = 14_000_000;
/** Largest on-screen scale for a trimmed crop at 100%: 12pt type at about 21px. */
const MAX_TRIM_SCALE = 1.75;

export { rotatedCropRect } from './trimRegion';

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
    const run: TrimRun = { cancelled: false, task: null };
    const pieces = async () =>
      trim ? trimRegion(pdf, region, rotation, run) : region.map(seg => ({ seg, rect: rotatedCropRect(seg.r ?? [0, 0, 1, 1], seg.rotate) }));

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
          // A trimmed crop with a narrow printed area would otherwise fill the
          // panel at an outsized scale; past 1.75x print it stops growing.
          let scale = Math.min(cssWidth / clipW, trim ? MAX_TRIM_SCALE * zoom : Infinity) * dpr;
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
          // As wide as the widest canvas, so a capped crop leaves no empty scroll.
          host.style.width = zoom > 1 ? `${Math.max(...out.map(c => parseFloat(c.style.maxWidth) || 0), 0)}px` : '';
          host.replaceChildren(...out);
        }
      } catch (e) {
        // a cancelled render rejects routinely — only surface real failures
        if (!cancelled && e instanceof Error && e.name !== 'RenderingCancelledException') setFailed(true);
      }
    })();
    return () => {
      cancelled = true;
      run.cancelled = true;
      task?.cancel();
      run.task?.cancel();
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
