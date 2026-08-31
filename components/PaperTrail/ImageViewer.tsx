/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — image-supplement lightbox.
 *
 * The SEC ships a small family of exam documents as images rather than PDFs
 * (the Geography aerial photograph and Ordnance Survey map sheets, and their
 * JC / LCA cousins). Forcing them through the pdf.js viewer would fail, so
 * they get a dedicated lightbox: the sheet is mounted like a photographic
 * print on the viewer's zinc ground, fit to width at rest, with the same zoom
 * ladder as the document viewer and free two-axis panning via natural scroll.
 */

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { ArrowLeft, ExternalLink, ZoomIn, ZoomOut } from 'lucide-react';

const ZOOM_STEPS = [0.75, 1, 1.25, 1.5, 2, 2.5];

const ImageViewer: React.FC<{
  title: string;
  subtitle?: string;
  url: string;
  onClose: () => void;
}> = ({ title, subtitle, url, onClose }) => {
  const [zoom, setZoom] = useState(1);
  const [state, setState] = useState<'loading' | 'ready' | 'error'>('loading');
  const [retryTick, setRetryTick] = useState(0);
  const headerRef = useRef<HTMLDivElement | null>(null);
  const scrollRef = useRef<HTMLDivElement | null>(null);
  const onCloseRef = useRef(onClose);
  onCloseRef.current = onClose;

  useEffect(() => {
    headerRef.current?.focus();
  }, []);

  const zoomBy = useCallback((dir: number) => {
    setZoom(z => {
      const i = ZOOM_STEPS.indexOf(z);
      return ZOOM_STEPS[Math.min(ZOOM_STEPS.length - 1, Math.max(0, i + dir))];
    });
  }, []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onCloseRef.current();
      else if (e.key === '+' || e.key === '=') zoomBy(1);
      else if (e.key === '-') zoomBy(-1);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [zoomBy]);

  // Double-tap / double-click: jump between rest and a close look, centred on
  // nothing fancier than the scroll position the reader already chose.
  const onDoubleClick = () => setZoom(z => (z === 1 ? 2 : 1));

  return createPortal(
    <div
      className="fixed inset-0 z-[100] flex flex-col bg-zinc-100 dark:bg-zinc-950"
      role="dialog"
      aria-modal="true"
      aria-label={`${title} — image viewer`}
    >
      {/* Header — same chrome as the document viewer */}
      <div
        ref={headerRef}
        tabIndex={-1}
        className="shrink-0 bg-white dark:bg-zinc-900 border-b border-zinc-200 dark:border-zinc-800 outline-none"
        style={{
          paddingTop: 'calc(8px + var(--sat, 0px))',
          paddingBottom: 8,
          paddingLeft: 'calc(12px + var(--sal, 0px))',
          paddingRight: 'calc(12px + var(--sar, 0px))',
        }}
      >
        <div className="flex items-center gap-2 max-w-3xl mx-auto">
          <button
            onClick={() => onCloseRef.current()}
            aria-label="Close viewer"
            className="p-2 -ml-1 rounded-lg text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100"
          >
            <ArrowLeft size={19} />
          </button>
          <div className="flex-1 min-w-0">
            <p className="text-[14px] font-semibold truncate text-zinc-900 dark:text-white">{title}</p>
            {subtitle && <p className="text-[11px] truncate text-zinc-500">{subtitle}</p>}
          </div>
          <button
            onClick={() => zoomBy(-1)}
            disabled={zoom === ZOOM_STEPS[0]}
            aria-label="Zoom out"
            className="p-1.5 rounded-lg text-zinc-500 disabled:opacity-30"
          >
            <ZoomOut size={17} />
          </button>
          <button
            onClick={() => zoomBy(1)}
            disabled={zoom === ZOOM_STEPS[ZOOM_STEPS.length - 1]}
            aria-label="Zoom in"
            className="p-1.5 rounded-lg text-zinc-500 disabled:opacity-30"
          >
            <ZoomIn size={17} />
          </button>
          <a
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Open the original in your browser"
            className="p-1.5 rounded-lg text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100"
          >
            <ExternalLink size={17} />
          </a>
        </div>
      </div>

      {/* Sheet */}
      <div ref={scrollRef} className="flex-1 overflow-auto overscroll-contain">
        <div className="min-h-full flex items-start justify-center p-4 sm:p-6">
          {state === 'error' ? (
            <div className="self-center text-center max-w-sm px-6 py-10">
              <p className="text-[14px] font-semibold text-zinc-900 dark:text-white">
                The image didn’t load
              </p>
              <p className="mt-1 text-[12px] text-zinc-500">
                Check your connection, then try again — or open the original in
                your browser.
              </p>
              <div className="mt-4 flex items-center justify-center gap-2">
                <button
                  onClick={() => {
                    setState('loading');
                    setRetryTick(t => t + 1);
                  }}
                  className="px-4 py-2 rounded-full text-[13px] font-semibold text-white bg-zinc-900 dark:bg-white dark:text-zinc-900"
                >
                  Try again
                </button>
                <a
                  href={url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-4 py-2 rounded-full text-[13px] font-semibold text-zinc-700 dark:text-zinc-200 border border-zinc-300 dark:border-zinc-700"
                >
                  Open in browser
                </a>
              </div>
            </div>
          ) : (
            <div
              className="transition-[width] duration-150 ease-out"
              style={{ width: `${zoom * 100}%`, maxWidth: zoom === 1 ? 900 : undefined }}
            >
              {state === 'loading' && (
                <div
                  aria-hidden
                  className="w-full aspect-[4/3] rounded-xl bg-zinc-200 dark:bg-zinc-800/70 animate-pulse"
                />
              )}
              <img
                key={retryTick}
                src={url}
                alt={subtitle ? `${title} — ${subtitle}` : title}
                onLoad={() => setState('ready')}
                onError={() => setState('error')}
                onDoubleClick={onDoubleClick}
                draggable={false}
                className={`w-full h-auto rounded-xl shadow-lg ring-1 ring-black/10 dark:ring-white/10 bg-white select-none ${
                  state === 'ready' ? '' : 'hidden'
                }`}
              />
            </div>
          )}
        </div>
        <p className="pb-4 text-center text-[10px] text-zinc-400 dark:text-zinc-600">
          Examination material © State Examinations Commission
        </p>
      </div>
    </div>,
    document.body,
  );
};

export default ImageViewer;
