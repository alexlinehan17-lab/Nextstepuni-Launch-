/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail viewer — in-app PDF reading with the paper ↔ marking-scheme
 * toggle that keeps your place in each document independently.
 *
 * Engineering notes (device floor is hand-me-down phones; several behaviours
 * here exist because adversarial review proved the naive versions broke):
 *  - pdfjs-dist LEGACY build, lazily loaded; worker failures reject with a
 *    timeout so the student always reaches the retry / open-in-browser UI.
 *  - ONE shared IntersectionObserver rooted on the inner scroller (an
 *    unrooted observer never fires for elements clipped by overflow:auto).
 *  - Page placeholders correct their aspect ratio from the real page once
 *    measured; canvases double-buffer on zoom (old bitmap stays until the new
 *    render lands) and are torn down + page.cleanup()'d when far away.
 *  - Per-page render errors surface a tap-to-retry chip, not silent white.
 *  - Rendered through a portal: Innovation-Zone ancestors carry framer-motion
 *    transforms which would re-anchor position:fixed.
 */

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { ArrowLeft, Download, RotateCcw, ZoomIn, ZoomOut } from 'lucide-react';
import { prettyBytes } from './storage';
import type { PDFDocumentProxy, PDFPageProxy } from 'pdfjs-dist';

// ─── pdf.js lazy singleton ──────────────────────────────────

// eslint-disable-next-line @typescript-eslint/consistent-type-imports -- typing a dynamic module namespace requires typeof import()
type PdfjsModule = typeof import('pdfjs-dist/legacy/build/pdf.mjs');
let pdfjsPromise: Promise<PdfjsModule> | null = null;

function loadPdfjs(): Promise<PdfjsModule> {
  if (!pdfjsPromise) {
    pdfjsPromise = import('pdfjs-dist/legacy/build/pdf.mjs').then(mod => {
      const worker = new Worker(
        new URL('pdfjs-dist/legacy/build/pdf.worker.mjs', import.meta.url),
        { type: 'module' },
      );
      // A worker whose script fails to fetch dies silently — reset the
      // singleton so the next attempt can retry with a fresh worker.
      worker.onerror = () => {
        pdfjsPromise = null;
      };
      mod.GlobalWorkerOptions.workerPort = worker;
      return mod;
    });
    pdfjsPromise.catch(() => {
      pdfjsPromise = null; // allow retry after a transient failure
    });
  }
  return pdfjsPromise;
}

const withTimeout = <T,>(p: Promise<T>, ms: number): Promise<T> =>
  new Promise((resolve, reject) => {
    const t = setTimeout(() => reject(new Error('timeout')), ms);
    p.then(
      v => {
        clearTimeout(t);
        resolve(v);
      },
      e => {
        clearTimeout(t);
        reject(e);
      },
    );
  });

// ─── types ──────────────────────────────────────────────────

export interface ViewerDoc {
  url: string;
  label: string;
  bytes: number;
}

interface ViewerProps {
  title: string;
  subtitle?: string;
  paper: ViewerDoc;
  scheme?: ViewerDoc;
  initialSide?: 'paper' | 'scheme';
  /** 1-based starting page per side (from recents). */
  initialPaperPage?: number;
  initialSchemePage?: number;
  onClose: () => void;
  /** Reports reading position for recents persistence (debounced upstream). */
  onPosition?: (side: 'paper' | 'scheme', page: number) => void;
}

type Side = 'paper' | 'scheme';
type LoadState = 'loading' | 'ready' | 'error' | 'unsupported';

interface DocSession {
  pdf: PDFDocumentProxy | null;
  /** The loading task owns teardown in pdf.js — destroy() lives here. */
  task: { destroy: () => Promise<void> } | null;
  state: LoadState;
  numPages: number;
  scrollTop: number;
  page: number;
}

const freshSession = (page: number): DocSession => ({
  pdf: null,
  task: null,
  state: 'loading',
  numPages: 0,
  scrollTop: 0,
  page,
});

// iOS Safari hard limit is ~16.7M pixels per canvas; stay safely under it.
const MAX_CANVAS_PIXELS = 14_000_000;
const ZOOM_STEPS = [0.75, 1, 1.25, 1.5, 2, 2.5];
const LOAD_TIMEOUT_MS = 30_000;

// ─── component ──────────────────────────────────────────────

const Viewer: React.FC<ViewerProps> = ({
  title,
  subtitle,
  paper,
  scheme,
  initialSide = 'paper',
  initialPaperPage = 1,
  initialSchemePage = 1,
  onClose,
  onPosition,
}) => {
  const [side, setSide] = useState<Side>(initialSide === 'scheme' && scheme ? 'scheme' : 'paper');
  const [zoom, setZoom] = useState(1);
  const [epoch, setEpoch] = useState(0); // bumped on resize/rotation → canvases re-render
  const [, forceRender] = useState(0);
  const bump = useCallback(() => forceRender(n => n + 1), []);

  const sessions = useRef<Record<Side, DocSession>>({
    paper: freshSession(initialPaperPage),
    scheme: freshSession(initialSchemePage),
  });
  const scrollerRef = useRef<HTMLDivElement | null>(null);
  const rootRef = useRef<HTMLDivElement | null>(null);
  const headerRef = useRef<HTMLDivElement | null>(null);
  const restoredRef = useRef<Record<Side, boolean>>({ paper: false, scheme: false });
  const mountedRef = useRef(true);
  const [scrubbing, setScrubbing] = useState<number | null>(null);

  // Stable refs for parent callbacks so effects never re-fire on parent renders.
  const onCloseRef = useRef(onClose);
  const onPositionRef = useRef(onPosition);
  useEffect(() => {
    onCloseRef.current = onClose;
    onPositionRef.current = onPosition;
  });

  const activeDoc = side === 'paper' ? paper : scheme!;
  const session = sessions.current[side];

  // ── shared IntersectionObserver (rooted on the scroller) ──
  const ioRef = useRef<IntersectionObserver | null>(null);
  const ioCallbacks = useRef(new Map<Element, (near: boolean) => void>());
  const observe = useCallback((el: Element, cb: (near: boolean) => void) => {
    ioCallbacks.current.set(el, cb);
    ioRef.current?.observe(el);
    return () => {
      ioCallbacks.current.delete(el);
      ioRef.current?.unobserve(el);
    };
  }, []);
  const attachScroller = useCallback((el: HTMLDivElement | null) => {
    scrollerRef.current = el;
    ioRef.current?.disconnect();
    ioRef.current = null;
    if (el) {
      ioRef.current = new IntersectionObserver(
        entries => entries.forEach(e => ioCallbacks.current.get(e.target)?.(e.isIntersecting)),
        { root: el, rootMargin: '125% 0px' },
      );
      ioCallbacks.current.forEach((_cb, target) => ioRef.current!.observe(target));
    }
  }, []);

  // ── document loading ──
  const load = useCallback(
    async (which: Side) => {
      const target = which === 'paper' ? paper : scheme;
      if (!target) return;
      const s = sessions.current[which];
      s.state = 'loading';
      bump();
      let pdfjs: PdfjsModule;
      try {
        pdfjs = await withTimeout(loadPdfjs(), LOAD_TIMEOUT_MS);
      } catch {
        if (mountedRef.current) {
          s.state = 'unsupported';
          bump();
        }
        return;
      }
      if (!mountedRef.current) return;
      try {
        const task = pdfjs.getDocument({ url: target.url });
        s.task = task;
        const pdf = await withTimeout(task.promise, LOAD_TIMEOUT_MS);
        if (!mountedRef.current) {
          task.destroy().catch(() => {});
          return;
        }
        s.pdf = pdf;
        s.numPages = pdf.numPages;
        s.state = 'ready';
        bump();
      } catch {
        if (mountedRef.current) {
          s.state = 'error';
          bump();
        }
      }
    },
    [paper, scheme, bump],
  );

  useEffect(() => {
    mountedRef.current = true;
    load('paper');
    if (initialSide === 'scheme' && scheme) load('scheme');
    return () => {
      mountedRef.current = false;
      (['paper', 'scheme'] as const).forEach(w => {
        sessions.current[w].task?.destroy().catch(() => {});
      });
      ioRef.current?.disconnect();
    };
  }, []);

  // Side switch: lazy-load the scheme, restore that side's scroll position.
  const prevSide = useRef(side);
  useEffect(() => {
    const s = sessions.current[side];
    if (side === 'scheme' && !s.pdf && s.state === 'loading' && !s.task) load('scheme');
    if (prevSide.current !== side) {
      prevSide.current = side;
      requestAnimationFrame(() => {
        if (scrollerRef.current && s.state === 'ready') {
          scrollerRef.current.scrollTop = s.scrollTop;
        }
      });
    }
  }, [side, load]);

  // Dialog behaviour: focus, Escape, Tab trap; resize/rotation re-render.
  useEffect(() => {
    headerRef.current?.focus();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onCloseRef.current();
      if (e.key === 'Tab' && rootRef.current) {
        const focusables = rootRef.current.querySelectorAll<HTMLElement>(
          'button:not([disabled]), a[href], input, [tabindex]:not([tabindex="-1"])',
        );
        if (focusables.length === 0) return;
        const first = focusables[0];
        const last = focusables[focusables.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    };
    window.addEventListener('keydown', onKey);
    let resizeTimer: ReturnType<typeof setTimeout> | null = null;
    const onResize = () => {
      if (resizeTimer) clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => setEpoch(n => n + 1), 250);
    };
    window.addEventListener('resize', onResize);
    return () => {
      window.removeEventListener('keydown', onKey);
      window.removeEventListener('resize', onResize);
      if (resizeTimer) clearTimeout(resizeTimer);
    };
  }, []);

  // ── scroll → current page + persistence ──
  const onScroll = useCallback(() => {
    const el = scrollerRef.current;
    const s = sessions.current[side];
    if (!el || s.state !== 'ready') return;
    s.scrollTop = el.scrollTop;
    const kids = el.querySelectorAll<HTMLElement>('[data-page]');
    const mid = el.scrollTop + el.clientHeight / 2;
    let current = 1;
    for (let i = 0; i < kids.length; i++) {
      if (kids[i].offsetTop <= mid) current = Number(kids[i].dataset.page);
      else break;
    }
    if (current !== s.page) {
      s.page = current;
      bump();
      onPositionRef.current?.(side, current);
    }
  }, [side, bump]);

  const jumpToPage = useCallback((p: number) => {
    const el = scrollerRef.current;
    if (!el) return;
    const target = el.querySelector<HTMLElement>(`[data-page="${p}"]`);
    if (target) el.scrollTo({ top: target.offsetTop - 8 });
  }, []);

  // Restore the initial page once a side is first ready.
  useEffect(() => {
    if (session.state === 'ready' && !restoredRef.current[side]) {
      restoredRef.current[side] = true;
      if (session.page > 1) requestAnimationFrame(() => jumpToPage(session.page));
    }
  }, [session.state, side, session.page, jumpToPage]);

  const zoomBy = (dir: 1 | -1) => {
    const i = ZOOM_STEPS.indexOf(zoom);
    setZoom(ZOOM_STEPS[Math.min(ZOOM_STEPS.length - 1, Math.max(0, i + dir))]);
  };

  // ── render ──
  const segBtn = (active: boolean) =>
    `px-4 py-1.5 rounded-lg text-[13px] transition-all ${
      active
        ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white font-semibold shadow-sm'
        : 'text-zinc-500 dark:text-zinc-400'
    }`;

  return createPortal(
    <div
      ref={rootRef}
      className="fixed inset-0 z-[100] flex flex-col bg-zinc-100 dark:bg-zinc-950"
      role="dialog"
      aria-modal="true"
      aria-label={`${title} — document viewer`}
    >
      {/* Header */}
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
          {scheme && (
            <div className="flex items-center gap-1 p-1 rounded-xl bg-zinc-100 dark:bg-zinc-800/50" role="group" aria-label="Paper or marking scheme">
              <button aria-pressed={side === 'paper'} onClick={() => setSide('paper')} className={segBtn(side === 'paper')}>
                Paper
              </button>
              <button aria-pressed={side === 'scheme'} onClick={() => setSide('scheme')} className={segBtn(side === 'scheme')}>
                Scheme
              </button>
            </div>
          )}
          <a
            href={activeDoc.url}
            target="_blank"
            rel="noopener noreferrer"
            aria-label={`Open the ${side} in your browser or download it${activeDoc.bytes ? ` (${prettyBytes(activeDoc.bytes)})` : ''}`}
            className="p-2 rounded-lg text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100"
          >
            <Download size={17} />
          </a>
        </div>
      </div>

      {/* Body */}
      {session.state === 'ready' && session.pdf ? (
        <div
          ref={attachScroller}
          onScroll={onScroll}
          className="relative flex-1 overflow-auto overscroll-contain"
          aria-label={`${activeDoc.label}, page ${session.page} of ${session.numPages}`}
        >
          <p className="sr-only">
            This document is shown as page images. For a screen-reader-friendly copy, use the
            “Open in your browser” button in the header.
          </p>
          <div className="mx-auto py-3 px-2" style={{ width: `${Math.round(zoom * 100)}%`, maxWidth: zoom === 1 ? 820 : undefined }}>
            {Array.from({ length: session.numPages }, (_, i) => (
              <Page
                key={`${side}-${i + 1}`}
                pdf={session.pdf!}
                pageNumber={i + 1}
                zoom={zoom}
                epoch={epoch}
                observe={observe}
              />
            ))}
          </div>
          <p className="text-center text-[10px] text-zinc-400 pb-3">© State Examinations Commission</p>
        </div>
      ) : session.state === 'loading' ? (
        <div className="flex-1 flex flex-col items-center justify-center gap-3 text-zinc-400">
          <div className="w-7 h-7 rounded-full border-2 border-zinc-300 border-t-zinc-500 animate-spin" aria-hidden />
          <p className="text-[13px]">
            Opening {side === 'paper' ? 'the paper' : 'the marking scheme'}…
            {activeDoc.bytes ? ` ${prettyBytes(activeDoc.bytes)}` : ''}
          </p>
          <a href={activeDoc.url} target="_blank" rel="noopener noreferrer" className="text-[12px] underline underline-offset-2 text-zinc-400">
            Taking too long? Open in browser
          </a>
        </div>
      ) : (
        <div className="flex-1 flex flex-col items-center justify-center gap-4 px-8 text-center">
          <p className="text-[15px] font-semibold text-zinc-800 dark:text-zinc-100">
            {session.state === 'unsupported' ? 'This phone can’t show PDFs inside the app.' : 'That didn’t load.'}
          </p>
          <p className="text-[13px] text-zinc-500 max-w-sm">
            {session.state === 'unsupported'
              ? 'No problem — the document will open in your browser instead.'
              : 'It might be the connection. Try again, or open it in your browser.'}
          </p>
          <div className="flex items-center gap-2.5">
            {session.state === 'error' && (
              <button
                onClick={() => load(side)}
                className="flex items-center gap-1.5 px-4 py-2 rounded-full text-[13px] font-semibold text-white"
                style={{ backgroundColor: '#F26B1F', boxShadow: '0 3px 0 #B54D14' }}
              >
                <RotateCcw size={14} /> Try again
              </button>
            )}
            <a
              href={activeDoc.url}
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2 rounded-full text-[13px] font-semibold border-2 border-zinc-300 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300"
            >
              Open in browser
            </a>
          </div>
        </div>
      )}

      {/* Footer: zoom + page scrubber */}
      {session.state === 'ready' && (
        <div
          className="shrink-0 bg-white dark:bg-zinc-900 border-t border-zinc-200 dark:border-zinc-800"
          style={{
            paddingTop: 8,
            paddingBottom: 'calc(8px + var(--sab, 0px))',
            paddingLeft: 'calc(16px + var(--sal, 0px))',
            paddingRight: 'calc(16px + var(--sar, 0px))',
          }}
        >
          <div className="flex items-center gap-3 max-w-3xl mx-auto">
            <button onClick={() => zoomBy(-1)} disabled={zoom === ZOOM_STEPS[0]} aria-label="Zoom out" className="p-1.5 rounded-lg text-zinc-500 disabled:opacity-30">
              <ZoomOut size={17} />
            </button>
            <button onClick={() => zoomBy(1)} disabled={zoom === ZOOM_STEPS[ZOOM_STEPS.length - 1]} aria-label="Zoom in" className="p-1.5 rounded-lg text-zinc-500 disabled:opacity-30">
              <ZoomIn size={17} />
            </button>
            {session.numPages > 3 ? (
              <>
                <input
                  type="range"
                  min={1}
                  max={session.numPages}
                  value={scrubbing ?? session.page}
                  onChange={e => setScrubbing(Number(e.target.value))}
                  onPointerUp={() => {
                    if (scrubbing != null) jumpToPage(scrubbing);
                    setScrubbing(null);
                  }}
                  onKeyUp={() => {
                    if (scrubbing != null) jumpToPage(scrubbing);
                    setScrubbing(null);
                  }}
                  aria-label={`Go to page, currently page ${session.page} of ${session.numPages}`}
                  className="flex-1 accent-[#F26B1F]"
                />
                <span className="text-[12px] tabular-nums text-zinc-500 whitespace-nowrap">
                  {scrubbing ?? session.page} / {session.numPages}
                </span>
              </>
            ) : (
              <span className="flex-1 text-right text-[12px] tabular-nums text-zinc-500">
                {session.page} / {session.numPages}
              </span>
            )}
          </div>
        </div>
      )}
    </div>,
    document.body,
  );
};

// ─── virtualised page ───────────────────────────────────────

const Page: React.FC<{
  pdf: PDFDocumentProxy;
  pageNumber: number;
  zoom: number;
  epoch: number;
  observe: (el: Element, cb: (near: boolean) => void) => () => void;
}> = React.memo(({ pdf, pageNumber, zoom, epoch, observe }) => {
  const holderRef = useRef<HTMLDivElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const pageRef = useRef<PDFPageProxy | null>(null);
  const [near, setNear] = useState(pageNumber <= 2);
  const [aspect, setAspect] = useState<number | null>(null);
  const [failed, setFailed] = useState(false);
  const renderTask = useRef<{ cancel: () => void } | null>(null);
  const [retryTick, setRetryTick] = useState(0);

  useEffect(() => {
    const el = holderRef.current;
    if (!el) return;
    return observe(el, setNear);
  }, [observe]);

  useEffect(() => {
    if (!near) {
      // Tear down far-away canvases AND pdf.js's decoded-image caches — both
      // grow unboundedly on long scanned schemes otherwise.
      const c = canvasRef.current;
      if (c) {
        c.width = 0;
        c.height = 0;
      }
      pageRef.current?.cleanup();
      return;
    }
    let cancelled = false;
    (async () => {
      try {
        const page = pageRef.current ?? (await pdf.getPage(pageNumber));
        pageRef.current = page;
        if (cancelled) return;
        const holder = holderRef.current;
        const canvas = canvasRef.current;
        if (!holder || !canvas) return;
        const base = page.getViewport({ scale: 1 });
        const realAspect = base.height / base.width;
        setAspect(prev => (prev !== realAspect ? realAspect : prev));
        const cssWidth = holder.clientWidth || 1;
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        let scale = (cssWidth / base.width) * dpr;
        const pixels = base.width * scale * (base.height * scale);
        if (pixels > MAX_CANVAS_PIXELS) scale *= Math.sqrt(MAX_CANVAS_PIXELS / pixels);
        const vp = page.getViewport({ scale });
        // Double-buffer: render offscreen, then blit — the old bitmap stays
        // visible during zoom re-renders instead of flashing white.
        const off = document.createElement('canvas');
        off.width = Math.floor(vp.width);
        off.height = Math.floor(vp.height);
        renderTask.current?.cancel();
        const task = page.render({ canvas: off, viewport: vp });
        renderTask.current = task;
        await task.promise;
        if (cancelled) return;
        canvas.width = off.width;
        canvas.height = off.height;
        canvas.getContext('2d')?.drawImage(off, 0, 0);
        setFailed(false);
      } catch (e) {
        // RenderingCancelledException is routine; real failures get a retry chip.
        if (!cancelled && e instanceof Error && e.name !== 'RenderingCancelledException') {
          setFailed(true);
        }
      }
    })();
    return () => {
      cancelled = true;
      renderTask.current?.cancel();
    };
  }, [near, pdf, pageNumber, zoom, epoch, retryTick]);

  return (
    <div
      ref={holderRef}
      data-page={pageNumber}
      className="relative bg-white dark:bg-zinc-900 rounded-md shadow-sm mb-2.5 overflow-hidden"
      style={{ paddingBottom: `${(aspect ?? 1.414) * 100}%` }}
      aria-label={`Page ${pageNumber}`}
    >
      <canvas ref={canvasRef} className="absolute inset-0 w-full h-full" />
      {failed && (
        <button
          onClick={() => {
            setFailed(false);
            setRetryTick(n => n + 1);
          }}
          className="absolute inset-0 flex flex-col items-center justify-center gap-1.5 text-zinc-400"
        >
          <RotateCcw size={16} />
          <span className="text-[12px]">Page {pageNumber} didn’t load — tap to retry</span>
        </button>
      )}
    </div>
  );
});
Page.displayName = 'PaperTrailPage';

export default Viewer;
