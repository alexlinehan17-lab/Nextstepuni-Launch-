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

import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { ArrowLeft, Download, RotateCcw, Sparkles, X, ZoomIn, ZoomOut } from 'lucide-react';
import { prettyBytes } from './storage';
import type { PaperAnswerMap, PaperAnswerQuestion } from '../../types/paperTrail';
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
  /** Storage URL of this paper's PaperAnswerMap sidecar — present only when a
   *  verified answer map shipped. Drives the "Answers" toggle + question chips. */
  answersUrl?: string;
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
  answersUrl,
  onClose,
  onPosition,
}) => {
  const [side, setSide] = useState<Side>(initialSide === 'scheme' && scheme ? 'scheme' : 'paper');
  const [zoom, setZoom] = useState(1);
  const [epoch, setEpoch] = useState(0); // bumped on resize/rotation → canvases re-render
  const [, forceRender] = useState(0);
  const bump = useCallback(() => forceRender(n => n + 1), []);

  // ── answers (per-question marking-scheme crops) ──
  const [answersOn, setAnswersOn] = useState(false);
  const [answerMap, setAnswerMap] = useState<PaperAnswerMap | null>(null);
  const [answerState, setAnswerState] = useState<'idle' | 'loading' | 'error'>('idle');
  const [reveal, setReveal] = useState<PaperAnswerQuestion | null>(null);
  const schemePrefetched = useRef(false);
  // Ref mirror so the once-mounted Escape handler sees the live reveal state.
  const revealRef = useRef<PaperAnswerQuestion | null>(null);
  revealRef.current = reveal;
  // "View full scheme" jump target, consumed by the side-switch / restore effects.
  const pendingSchemeJump = useRef<number | null>(null);

  // page → its question anchors, memoised so Page's React.memo holds across
  // scroll/zoom re-renders (a fresh filter() each render would defeat it).
  const anchorsByPage = useMemo(() => {
    const m = new Map<number, PaperAnswerQuestion[]>();
    if (answerMap) for (const q of answerMap.q) {
      const list = m.get(q.pP);
      if (list) list.push(q);
      else m.set(q.pP, [q]);
    }
    return m;
  }, [answerMap]);

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

  // Turn the answers overlay on/off; lazily fetch the map and warm the scheme
  // PDF the first time it's enabled (the crop renders from the scheme doc).
  const toggleAnswers = useCallback(() => {
    setReveal(null);
    setAnswersOn(on => {
      const next = !on;
      if (next) {
        if (!answerMap && answerState !== 'loading' && answersUrl) {
          setAnswerState('loading');
          fetch(answersUrl)
            .then(r => (r.ok ? r.json() : Promise.reject(new Error('answers fetch'))))
            .then((m: PaperAnswerMap) => {
              if (mountedRef.current) {
                setAnswerMap(m);
                setAnswerState('idle');
              }
            })
            .catch(() => mountedRef.current && setAnswerState('error'));
        }
        if (scheme && !sessions.current.scheme.pdf && !sessions.current.scheme.task) load('scheme');
      }
      return next;
    });
  }, [answerMap, answerState, answersUrl, scheme, load]);

  // Reveal one question's scheme crop. On the FIRST reveal, full-GET the scheme
  // so the CacheFirst (200-only) rule stores a complete copy for offline reveals.
  const onReveal = useCallback(
    (q: PaperAnswerQuestion) => {
      if (scheme && !schemePrefetched.current) {
        // Mark done only on success, so a failed warm (offline) retries next tap.
        fetch(scheme.url)
          .then(() => {
            schemePrefetched.current = true;
          })
          .catch(() => {});
      }
      if (scheme && !sessions.current.scheme.pdf && !sessions.current.scheme.task) load('scheme');
      setReveal(q);
    },
    [scheme, load],
  );

  // Jump the Scheme side to a given page (the "View full scheme" escape hatch).
  // Records the target in a ref; the single scroll path (side-switch / restore
  // effects) honours it, so it never fights the saved-scrollTop restore.
  const jumpSchemeToPage = useCallback((page: number) => {
    pendingSchemeJump.current = page;
    setReveal(null);
    setSide('scheme');
  }, []);

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

  // Scroll the active scroller to a given 1-based page.
  const jumpToPage = useCallback((p: number) => {
    const el = scrollerRef.current;
    if (!el) return;
    const target = el.querySelector<HTMLElement>(`[data-page="${p}"]`);
    if (target) el.scrollTo({ top: target.offsetTop - 8 });
  }, []);

  // Side switch: lazy-load the scheme, restore that side's scroll position.
  const prevSide = useRef(side);
  useEffect(() => {
    const s = sessions.current[side];
    if (side === 'scheme' && !s.pdf && s.state === 'loading' && !s.task) load('scheme');
    if (prevSide.current !== side) {
      prevSide.current = side;
      requestAnimationFrame(() => {
        if (!scrollerRef.current || s.state !== 'ready') return;
        // A pending "View full scheme" jump wins over the saved scroll position.
        if (side === 'scheme' && pendingSchemeJump.current != null) {
          jumpToPage(pendingSchemeJump.current);
          pendingSchemeJump.current = null;
        } else {
          scrollerRef.current.scrollTop = s.scrollTop;
        }
      });
    }
  }, [side, load, jumpToPage]);

  // Closing/leaving a side dismisses any open answer reveal (it belongs to the
  // paper side and to the question that was tapped).
  useEffect(() => {
    setReveal(null);
  }, [side]);

  // Dialog behaviour: focus, Escape, Tab trap; resize/rotation re-render.
  useEffect(() => {
    headerRef.current?.focus();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        // An open answer reveal swallows Escape; only then does it close the viewer.
        if (revealRef.current) {
          setReveal(null);
          return;
        }
        onCloseRef.current();
      }
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

  // Restore the initial page once a side is first ready — or honour a pending
  // "View full scheme" jump that arrived before the scheme finished loading.
  useEffect(() => {
    if (session.state !== 'ready') return;
    if (side === 'scheme' && pendingSchemeJump.current != null) {
      const p = pendingSchemeJump.current;
      pendingSchemeJump.current = null;
      restoredRef.current.scheme = true;
      requestAnimationFrame(() => jumpToPage(p));
      return;
    }
    if (!restoredRef.current[side]) {
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
          {answersUrl && side === 'paper' && (
            <button
              onClick={toggleAnswers}
              aria-pressed={answersOn}
              aria-label="Show marking-scheme answers beside each question"
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-[13px] font-semibold transition-all ${
                answersOn ? 'text-white' : 'text-[#F26B1F] bg-[#FDEEDF]'
              }`}
              style={answersOn ? { backgroundColor: '#F26B1F', boxShadow: '0 2px 0 #B54D14' } : undefined}
            >
              <Sparkles size={14} /> Answers
            </button>
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
                anchors={answersOn && side === 'paper' ? anchorsByPage.get(i + 1) : undefined}
                onReveal={onReveal}
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

      {/* Answers map fetch status (chips appear once ready). */}
      {answersOn && side === 'paper' && answerState !== 'idle' && (
        <div
          role="status"
          aria-live="polite"
          className="absolute left-1/2 -translate-x-1/2 bottom-24 z-[60] px-3 py-1.5 rounded-full text-[12px] font-medium bg-zinc-900/90 text-white shadow-lg"
        >
          {answerState === 'loading' ? 'Loading answers…' : 'Couldn’t load answers — try again later.'}
        </div>
      )}

      {/* Per-question marking-scheme reveal. */}
      {reveal && (
        <RevealSheet
          q={reveal}
          schemePdf={sessions.current.scheme.pdf}
          schemeUrl={scheme?.url}
          schemeErrored={sessions.current.scheme.state === 'error' || sessions.current.scheme.state === 'unsupported'}
          copyright={answerMap?.copyright}
          onClose={() => setReveal(null)}
          onFullScheme={jumpSchemeToPage}
        />
      )}
    </div>,
    document.body,
  );
};

// ─── per-question marking-scheme reveal sheet ───────────────

const RevealSheet: React.FC<{
  q: PaperAnswerQuestion;
  schemePdf: PDFDocumentProxy | null;
  schemeUrl?: string;
  schemeErrored: boolean;
  copyright?: string;
  onClose: () => void;
  onFullScheme: (page: number) => void;
}> = ({ q, schemePdf, schemeUrl, schemeErrored, copyright, onClose, onFullScheme }) => {
  const firstPage = q.region[0]?.p;
  const closeRef = useRef<HTMLButtonElement | null>(null);
  useEffect(() => {
    closeRef.current?.focus();
  }, []);
  return (
    <div className="fixed inset-0 z-[110] flex flex-col justify-end" role="dialog" aria-modal="true" aria-label={`Marking scheme for Question ${q.n}`}>
      <button className="absolute inset-0 bg-black/40" aria-label="Close" tabIndex={-1} onClick={onClose} />
      <div
        className="relative bg-white dark:bg-zinc-900 rounded-t-2xl shadow-2xl flex flex-col max-h-[80vh]"
        style={{ paddingBottom: 'var(--sab, 0px)' }}
      >
        <div className="shrink-0 flex items-center gap-2 px-4 py-3 border-b border-zinc-200 dark:border-zinc-800">
          <div className="flex-1 min-w-0">
            <p className="text-[14px] font-semibold text-zinc-900 dark:text-white">Question {q.n} · marking scheme</p>
            <p className="text-[11px] text-zinc-500">How examiners award the marks — not a model answer.</p>
          </div>
          <button ref={closeRef} onClick={onClose} aria-label="Close" className="p-2 -mr-1 rounded-lg text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100">
            <X size={18} />
          </button>
        </div>
        <div className="overflow-auto overscroll-contain px-3 py-3 bg-zinc-100 dark:bg-zinc-950">
          {q.mode === 'pagejump' ? (
            <p className="text-[13px] text-zinc-600 dark:text-zinc-300 text-center py-8 px-4">
              This question’s answer spans several scheme pages. Open the marking scheme to read it in full.
            </p>
          ) : schemeErrored ? (
            <p className="text-[13px] text-zinc-600 dark:text-zinc-300 text-center py-8 px-4">
              Couldn’t load the marking scheme. Open it in the Scheme tab instead.
            </p>
          ) : schemePdf ? (
            <CropView pdf={schemePdf} region={q.region} />
          ) : (
            <div role="status" aria-live="polite" className="flex flex-col items-center justify-center gap-2 py-10 text-zinc-400">
              <div className="w-5 h-5 rounded-full border-2 border-zinc-300 border-t-zinc-500 animate-spin" aria-hidden />
              <span className="text-[12px]">Loading the marking scheme…</span>
              {schemeUrl && (
                <a href={schemeUrl} target="_blank" rel="noopener noreferrer" className="text-[12px] underline underline-offset-2">
                  Taking too long? Open it in your browser
                </a>
              )}
            </div>
          )}
        </div>
        <div className="shrink-0 flex items-center justify-between gap-2 px-4 py-2.5 border-t border-zinc-200 dark:border-zinc-800">
          <span className="text-[10px] text-zinc-400 truncate">{copyright ?? '© State Examinations Commission'}</span>
          <button
            onClick={() => firstPage && onFullScheme(firstPage)}
            disabled={!firstPage}
            className="shrink-0 px-3 py-1.5 rounded-full text-[12px] font-semibold text-[#F26B1F] bg-[#FDEEDF] disabled:opacity-40"
          >
            View full scheme →
          </button>
        </div>
      </div>
    </div>
  );
};

// ─── clipped scheme-region renderer ─────────────────────────
//
// Renders each region segment (a fractional rect of a scheme page) as its own
// canvas, stacked vertically — the student sees a continuous crop of the real
// scheme. Reuses the page-render → offscreen → blit pattern and the canvas-pixel
// clamp from the main viewer.

const CropView: React.FC<{ pdf: PDFDocumentProxy; region: PaperAnswerQuestion['region'] }> = ({ pdf, region }) => {
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
          canvas.setAttribute('aria-label', `Marking scheme page ${seg.p}, shown as an image — © State Examinations Commission`);
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
  }, [pdf, region]);

  return (
    <div>
      <div ref={hostRef} className="mx-auto max-w-[900px]" />
      {failed && <p className="text-[12px] text-zinc-500 text-center py-4">Couldn’t render this region — open the full scheme.</p>}
    </div>
  );
};

// ─── virtualised page ───────────────────────────────────────

const Page: React.FC<{
  pdf: PDFDocumentProxy;
  pageNumber: number;
  zoom: number;
  epoch: number;
  observe: (el: Element, cb: (near: boolean) => void) => () => void;
  anchors?: PaperAnswerQuestion[];
  onReveal?: (q: PaperAnswerQuestion) => void;
}> = React.memo(({ pdf, pageNumber, zoom, epoch, observe, anchors, onReveal }) => {
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
      {/* Per-question "See answer" chips — fractional top rides zoom + virtualisation. */}
      {anchors?.map(q => (
        <button
          key={`${q.pP}-${q.n}`}
          onClick={() => onReveal?.(q)}
          className="absolute right-0 z-10 flex items-center gap-1 pl-2 pr-2.5 py-1 rounded-l-full text-[11px] font-bold text-white"
          style={{
            top: `${Math.min(0.97, Math.max(0, q.pY[0])) * 100}%`,
            backgroundColor: '#F26B1F',
            boxShadow: '0 1px 5px rgba(0,0,0,.28)',
          }}
          aria-label={`See the marking scheme answer for Question ${q.n}`}
        >
          <Sparkles size={11} /> Answer
        </button>
      ))}
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
