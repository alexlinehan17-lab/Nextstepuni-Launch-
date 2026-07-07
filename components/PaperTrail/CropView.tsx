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

// Same clamp the Viewer uses for full pages — keeps low-memory devices safe.
const MAX_CANVAS_PIXELS = 14_000_000;

const CropView: React.FC<{
  pdf: PDFDocumentProxy;
  region: PaperAnswerSeg[];
  /** Accessible label per rendered page. Defaults to the scheme wording the
   *  answer reveal has always used. */
  ariaLabel?: (page: number) => string;
  /** Shown when rendering fails. */
  failText?: string;
}> = ({ pdf, region, ariaLabel, failText }) => {
  const hostRef = useRef<HTMLDivElement | null>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    let cancelled = false;
    let task: { promise: Promise<void>; cancel: () => void } | null = null;
    const host = hostRef.current;
    if (!host) return;
    host.replaceChildren();
    setFailed(false);
    (async () => {
      try {
        const cssWidth = Math.min(host.clientWidth || 320, 900);
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        for (const seg of region) {
          if (cancelled) return;
          const page = await pdf.getPage(seg.p);
          if (cancelled) {
            page.cleanup();
            return;
          }
          const base = page.getViewport({ scale: 1 });
          const r = seg.r ?? [0, 0, 1, 1];
          const clipW = (r[2] - r[0]) * base.width;
          const clipH = (r[3] - r[1]) * base.height;
          if (clipW <= 0 || clipH <= 0) {
            page.cleanup();
            continue;
          }
          let scale = (cssWidth / clipW) * dpr;
          const pixels = clipW * scale * (clipH * scale);
          if (pixels > MAX_CANVAS_PIXELS) scale *= Math.sqrt(MAX_CANVAS_PIXELS / pixels);
          const vp = page.getViewport({ scale });
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
          canvas.className = 'block w-full h-auto rounded-md shadow-sm mb-2 bg-white';
          canvas.style.maxWidth = `${Math.floor((clipW * scale) / dpr)}px`;
          canvas.setAttribute('role', 'img');
          canvas.setAttribute(
            'aria-label',
            ariaLabel
              ? ariaLabel(seg.p)
              : `Marking scheme page ${seg.p}, shown as an image — © State Examinations Commission`,
          );
          host.appendChild(canvas);
          page.cleanup();
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
  }, [pdf, region, ariaLabel]);

  return (
    <div>
      <div ref={hostRef} className="mx-auto max-w-[900px]" />
      {failed && (
        <p className="text-[12px] text-zinc-500 text-center py-4">
          {failText ?? 'Couldn’t render this region — open the full scheme.'}
        </p>
      )}
    </div>
  );
};

export default CropView;
