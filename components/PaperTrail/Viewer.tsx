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
import { AnimatePresence, useReducedMotion } from 'framer-motion';
import {
  ArrowLeft,
  BookOpen,
  Clock3,
  Download,
  Highlighter,
  Pause,
  Play,
  ListChecks,
  PenLine,
  RotateCcw,
  ScrollText,
  SlidersHorizontal,
  Sparkles,
  TrendingUp,
  X,
  ZoomIn,
  ZoomOut,
} from 'lucide-react';
import { MotionDiv } from '../Motion';
import { prettyBytes } from './storage';
import { scanDocument, type CommandToken, type DocTokens, type MarkToken } from './textOverlay';
import { frequencyFor, siblingsFor, topicLabel, type TopicSibling } from './topics';
import { loadAttempt, setMark, setTriage, type GapKind, type SelfMark, type TriageRating } from './attemptStore';
import { markerLicence, type MarkerLicence } from './trust';
import { recordActivity } from './streakStore';
import type { ExaminerInsightSet } from '../../data/paperTrail/examinerInsights';
import type { FormulaeHandle, FormulaePageIndex } from '../../data/paperTrailFormulae';
import type { SubjectMarkingGrammar, SubjectTiming } from '../../types/knowledge';
import type { PaperTopicTags } from '../../types/paperTrailTopics';
import type { PaperAnswerMap, PaperAnswerQuestion } from '../../types/paperTrail';
import type { PDFDocumentProxy, PDFPageProxy } from 'pdfjs-dist';

// Sleek glide shared with the GC dashboard student-view tray.
const GLIDE = { duration: 0.32, ease: [0.16, 1, 0.3, 1] as const };

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
  /** Official timing for this exact paper (from SUBJECT_TIMING), if the subject
   *  has one — drives minute targets + the exam-mode clock. Null → generic
   *  proportional-to-marks pace derived live from the paper's own mark tokens. */
  timing?: SubjectTiming | null;
  /** Marking-scheme grammar card for this subject, if one applies. */
  grammar?: SubjectMarkingGrammar | null;
  /** Formulae & Tables quick-jump — present only when the booklet is live for
   *  a booklet subject (gated upstream). */
  formulae?: FormulaeHandle;
  /** This paper's verified topic tags (Tier 2) — present only when tagged.
   *  Drives the frequency chips + cross-year jump. */
  topics?: PaperTopicTags;
  /** Open another paper focused on a question (cross-year jump target). */
  onCrossYear?: (target: TopicSibling) => void;
  /** On open, scroll to this question number once anchors are ready (the
   *  landing target of a cross-year jump). */
  focusQuestion?: string;
  /** Per-paper localStorage namespace for the triage + self-mark tools
   *  (`uid|subjectId|year|level|lang|fileid`). Absent → those tools stay hidden. */
  storageNs?: string;
  /** Chief-Examiner insight card for this subject, if a report is in-repo. */
  examinerInsights?: ExaminerInsightSet;
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
  timing = null,
  grammar = null,
  formulae,
  topics,
  onCrossYear,
  focusQuestion,
  storageNs,
  examinerInsights,
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

  // ── on-paper study tools (live text-layer overlays) ──
  const [toolsOpen, setToolsOpen] = useState(false); // tools menu popover
  const [paceOn, setPaceOn] = useState(false); // time-budget chips
  const [decodeOn, setDecodeOn] = useState(false); // command-word highlighting
  const [markingOpen, setMarkingOpen] = useState(false); // "how it's marked" card
  const [formulaeOpen, setFormulaeOpen] = useState(false); // formulae & tables sheet
  const [formulaeIndex, setFormulaeIndex] = useState<FormulaePageIndex | null>(null);
  const [commandReveal, setCommandReveal] = useState<CommandToken | null>(null);
  // ── topic tags (frequency chips + cross-year jump) ──
  const [topicsOn, setTopicsOn] = useState(false);
  const [topicReveal, setTopicReveal] = useState<{ n: string; subtopicId: string } | null>(null);
  // ── triage (Tier 2) + self-mark (Tier 3) ──
  const [triageOpen, setTriageOpen] = useState(false);
  const [examinerOpen, setExaminerOpen] = useState(false);
  const [selfMarkOn, setSelfMarkOn] = useState(false);
  // attempt state (triage ratings + self-mark scores) for this paper, persisted.
  const [attempt, setAttempt] = useState(() => (storageNs ? loadAttempt(storageNs) : {}));
  // The whole-paper text scan (marks + command words) — run once, lazily, the
  // first time any text-overlay tool is switched on.
  const [docTokens, setDocTokens] = useState<DocTokens | null>(null);
  const [scanState, setScanState] = useState<'idle' | 'loading' | 'error'>('idle');
  // Exam-mode clock.
  const [examOn, setExamOn] = useState(false);
  const [running, setRunning] = useState(false);
  const [elapsed, setElapsed] = useState(0); // seconds
  const minsPerMark = timing ? timing.totalMinutes / timing.totalMarks : null;

  // Reveal panel comes up from the bottom on phones, in from the right on
  // tablet/desktop (≥768px) — same glide as the GC dashboard student view.
  const reducedMotion = useReducedMotion();
  const [isWide, setIsWide] = useState(
    () => typeof window !== 'undefined' && window.matchMedia('(min-width: 768px)').matches,
  );
  useEffect(() => {
    const mq = window.matchMedia('(min-width: 768px)');
    const on = () => setIsWide(mq.matches);
    mq.addEventListener('change', on);
    return () => mq.removeEventListener('change', on);
  }, []);
  const panelHidden = reducedMotion ? { opacity: 0 } : isWide ? { x: '100%' } : { y: '100%' };
  const panelShown = reducedMotion ? { opacity: 1 } : { x: 0, y: 0 };
  // Ref mirror so the once-mounted Escape handler sees the live reveal state.
  const revealRef = useRef<PaperAnswerQuestion | null>(null);
  revealRef.current = reveal;
  // Same mirroring for the paper-side tool overlays, so Escape dismisses the
  // open panel/menu instead of closing the whole viewer underneath it.
  const commandRevealRef = useRef<CommandToken | null>(null);
  commandRevealRef.current = commandReveal;
  const topicRevealRef = useRef<{ n: string; subtopicId: string } | null>(null);
  topicRevealRef.current = topicReveal;
  const markingOpenRef = useRef(false);
  markingOpenRef.current = markingOpen;
  const formulaeOpenRef = useRef(false);
  formulaeOpenRef.current = formulaeOpen;
  const triageOpenRef = useRef(false);
  triageOpenRef.current = triageOpen;
  const examinerOpenRef = useRef(false);
  examinerOpenRef.current = examinerOpen;
  const toolsOpenRef = useRef(false);
  toolsOpenRef.current = toolsOpen;
  // "View full scheme" jump target, consumed by the side-switch / restore effects.
  const pendingSchemeJump = useRef<number | null>(null);

  // Stable pace descriptor so Page's React.memo isn't defeated each render.
  const paceInfo = useMemo(
    () => ({ minsPerMark, totalMarks: docTokens?.totalMarks ?? 0 }),
    [minsPerMark, docTokens],
  );

  // Marks-per-page for the heat-strip — where the marks live across the paper.
  const marksByPage = useMemo(() => {
    if (!docTokens) return null;
    const map = new Map<number, number>();
    let max = 1;
    for (const [pg, tok] of docTokens.byPage) {
      const sum = tok.marks.reduce((a, m) => a + m.value, 0);
      map.set(pg, sum);
      if (sum > max) max = sum;
    }
    return { map, max };
  }, [docTokens]);

  const onCommand = useCallback((c: CommandToken) => setCommandReveal(c), []);

  const activeToolCount = [answersOn, paceOn, decodeOn, examOn, topicsOn, selfMarkOn].filter(Boolean).length;

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

  // Any text-overlay tool needs the whole-paper token scan. Presence of the two
  // per-page maps below is what actually renders overlays (memoised so Page's
  // React.memo holds across scroll/zoom).
  const paceEnabled = paceOn && !!docTokens;
  const decodeEnabled = decodeOn && !!docTokens;

  // question n → its topic tag + cross-year frequency (for the chip). Stable
  // across renders so Page's React.memo holds.
  const topicInfoByN = useMemo(() => {
    if (!topics) return null;
    const m = new Map<string, { subtopicId: string; label: string; yearsWith: number; totalYears: number }>();
    for (const t of topics.q) {
      const freq = frequencyFor(topics.subjectId, topics.level, topics.paperKey, t.primary);
      m.set(t.n, {
        subtopicId: t.primary,
        label: topicLabel(t.primary),
        yearsWith: freq.yearsWith.length,
        totalYears: freq.totalYears,
      });
    }
    return m;
  }, [topics]);

  const onTopic = useCallback(
    (n: string) => {
      const info = topicInfoByN?.get(n);
      if (info) setTopicReveal({ n, subtopicId: info.subtopicId });
    },
    [topicInfoByN],
  );

  // Some older papers are image scans with no text layer — the extractor finds
  // nothing. Detect the truly-empty case so a text tool explains itself instead
  // of silently doing nothing.
  const hasAnyTokens = useMemo(() => {
    if (!docTokens) return true; // not scanned yet — assume fine
    for (const p of docTokens.byPage.values()) if (p.marks.length || p.commands.length) return true;
    return false;
  }, [docTokens]);

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

  // Fetch the answer map once — shared by the Answers overlay (scheme crops) and
  // the Topics overlay (which needs the same per-question anchor positions).
  const ensureAnswerMap = useCallback(() => {
    if (answerMap || answerState === 'loading' || !answersUrl) return;
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
  }, [answerMap, answerState, answersUrl]);

  // Turn the answers overlay on/off; lazily fetch the map and warm the scheme
  // PDF the first time it's enabled (the crop renders from the scheme doc).
  const toggleAnswers = useCallback(() => {
    setReveal(null);
    setAnswersOn(on => {
      const next = !on;
      if (next) {
        ensureAnswerMap();
        if (scheme && !sessions.current.scheme.pdf && !sessions.current.scheme.task) load('scheme');
      }
      return next;
    });
  }, [ensureAnswerMap, scheme, load]);

  // Topics overlay: reuses the answer-map anchors for positions; tags themselves
  // are committed in-bundle, so no extra fetch beyond the anchor map.
  const toggleTopics = useCallback(() => {
    setTopicReveal(null);
    setTopicsOn(on => {
      const next = !on;
      if (next) ensureAnswerMap();
      return next;
    });
  }, [ensureAnswerMap]);

  // Triage (Tier 2): plan-your-attack ratings over the paper's question list.
  const openTriage = useCallback(() => {
    ensureAnswerMap();
    setToolsOpen(false);
    setTriageOpen(true);
  }, [ensureAnswerMap]);

  const rateTriage = useCallback(
    (n: string, rating: TriageRating | null) => {
      if (!storageNs) return;
      setAttempt(setTriage(storageNs, n, rating));
    },
    [storageNs],
  );

  // Self-mark (Tier 3): scoring control appears inside the answer reveal. Turning
  // it on ensures the answer chips are available to open a reveal from.
  const toggleSelfMark = useCallback(() => {
    setSelfMarkOn(on => {
      const next = !on;
      if (next) {
        ensureAnswerMap();
        setAnswersOn(true);
        if (scheme && !sessions.current.scheme.pdf && !sessions.current.scheme.task) load('scheme');
      }
      return next;
    });
    setToolsOpen(false);
  }, [ensureAnswerMap, scheme, load]);

  const recordMark = useCallback(
    (n: string, mark: SelfMark | null) => {
      if (!storageNs) return;
      setAttempt(setMark(storageNs, n, mark));
      // uid is the first segment of storageNs; self-marking counts toward the streak.
      if (mark) recordActivity(storageNs.split('|')[0], Date.now(), 1);
    },
    [storageNs],
  );

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

  // Whole-paper text scan for the overlay tools. Runs once, lazily, when the
  // first text tool is switched on and the paper PDF is ready. A ref (not
  // scanState) guards the single-start, so setting scanState='loading' can't
  // re-fire this effect and cancel its own in-flight scan.
  const wantScan = paceOn || decodeOn;
  const scanStartedRef = useRef(false);
  useEffect(() => {
    if (!wantScan || scanStartedRef.current) return;
    const pdf = sessions.current.paper.pdf;
    if (!pdf) return; // paper not ready yet; effect re-runs when it loads (bump)
    scanStartedRef.current = true;
    setScanState('loading');
    scanDocument(pdf)
      .then(tokens => {
        if (mountedRef.current) {
          setDocTokens(tokens);
          setScanState('idle');
        }
      })
      .catch(() => {
        if (mountedRef.current) setScanState('error');
      });
  }, [wantScan, sessions.current.paper.state]);

  // Exam-mode clock — one interval while running. Elapsed persists across
  // pause/resume; reset zeroes it.
  useEffect(() => {
    if (!examOn || !running) return;
    const id = setInterval(() => setElapsed(s => s + 1), 1000);
    return () => clearInterval(id);
  }, [examOn, running]);

  const toggleTool = useCallback((tool: 'pace' | 'decode') => {
    setCommandReveal(null);
    if (tool === 'pace') setPaceOn(v => !v);
    else setDecodeOn(v => !v);
  }, []);

  // Open the Formulae & Tables sheet; fetch its page-index sidecar once. A
  // missing/failed index just means sections open the booklet at the front.
  const openFormulae = useCallback(() => {
    setToolsOpen(false);
    setFormulaeOpen(true);
    if (formulae && !formulaeIndex) {
      fetch(formulae.indexUrl)
        .then(r => (r.ok ? r.json() : Promise.reject(new Error('index'))))
        .then((idx: FormulaePageIndex) => mountedRef.current && setFormulaeIndex(idx))
        .catch(() => {});
    }
  }, [formulae, formulaeIndex]);

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
  // paper side and to the question that was tapped) plus the paper-side tools UI.
  useEffect(() => {
    setReveal(null);
    setToolsOpen(false);
    setCommandReveal(null);
    setMarkingOpen(false);
    setFormulaeOpen(false);
    setTopicReveal(null);
    setTriageOpen(false);
    setExaminerOpen(false);
  }, [side]);

  // Close the tools menu on outside tap.
  useEffect(() => {
    if (!toolsOpen) return;
    const onDown = (e: PointerEvent) => {
      const t = e.target as HTMLElement;
      if (!t.closest('[data-tools-anchor]')) setToolsOpen(false);
    };
    window.addEventListener('pointerdown', onDown);
    return () => window.removeEventListener('pointerdown', onDown);
  }, [toolsOpen]);

  // Dialog behaviour: focus, Escape, Tab trap; resize/rotation re-render.
  useEffect(() => {
    headerRef.current?.focus();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        // Any open overlay/menu swallows Escape first; only then does it close
        // the viewer.
        if (revealRef.current) {
          setReveal(null);
          return;
        }
        if (commandRevealRef.current) {
          setCommandReveal(null);
          return;
        }
        if (topicRevealRef.current) {
          setTopicReveal(null);
          return;
        }
        if (markingOpenRef.current) {
          setMarkingOpen(false);
          return;
        }
        if (formulaeOpenRef.current) {
          setFormulaeOpen(false);
          return;
        }
        if (triageOpenRef.current) {
          setTriageOpen(false);
          return;
        }
        if (examinerOpenRef.current) {
          setExaminerOpen(false);
          return;
        }
        if (toolsOpenRef.current) {
          setToolsOpen(false);
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

  // Landing from a cross-year jump: turn Topics on and pull the anchor map so
  // the target question's chip is visible. Mount-only (focusQuestion is fixed
  // per viewer open); ensureAnswerMap is a no-op once the map is loaded.
  const focusInitRef = useRef(false);
  useEffect(() => {
    if (focusQuestion && !focusInitRef.current) {
      focusInitRef.current = true;
      setTopicsOn(true);
      ensureAnswerMap();
    }
  }, [focusQuestion, ensureAnswerMap]);

  // Once the paper + anchor map are ready, scroll to the focused question.
  const focusedRef = useRef(false);
  useEffect(() => {
    if (!focusQuestion || focusedRef.current || !answerMap || session.state !== 'ready') return;
    const q = answerMap.q.find(x => x.n === focusQuestion);
    focusedRef.current = true;
    if (!q) return;
    requestAnimationFrame(() => {
      const el = scrollerRef.current;
      if (!el) return;
      const target = el.querySelector<HTMLElement>(`[data-page="${q.pP}"]`);
      if (target) el.scrollTo({ top: target.offsetTop - 8 + target.clientHeight * Math.max(0, q.pY[0] - 0.02) });
    });
  }, [focusQuestion, answerMap, session.state]);

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
          {side === 'paper' && (
            <div className="relative" data-tools-anchor>
              <button
                onClick={() => setToolsOpen(o => !o)}
                aria-expanded={toolsOpen}
                aria-label="Study tools for this paper"
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-[13px] font-semibold transition-all ${
                  activeToolCount > 0 ? 'text-white' : 'text-[#F26B1F] bg-[#FDEEDF]'
                }`}
                style={activeToolCount > 0 ? { backgroundColor: '#F26B1F', boxShadow: '0 2px 0 #B54D14' } : undefined}
              >
                <SlidersHorizontal size={14} /> Tools
                {activeToolCount > 0 && (
                  <span className="ml-0.5 min-w-[16px] h-4 px-1 inline-flex items-center justify-center rounded-full bg-white/25 text-[10px] tabular-nums">
                    {activeToolCount}
                  </span>
                )}
              </button>
              <AnimatePresence>
                {toolsOpen && (
                  <MotionDiv
                    key="tools-menu"
                    initial={reducedMotion ? { opacity: 0 } : { opacity: 0, y: -6, scale: 0.98 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={reducedMotion ? { opacity: 0 } : { opacity: 0, y: -6, scale: 0.98 }}
                    transition={{ duration: 0.16, ease: [0.16, 1, 0.3, 1] }}
                    role="menu"
                    className="absolute right-0 mt-2 w-64 z-[70] rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 shadow-2xl overflow-hidden"
                    style={{ transformOrigin: 'top right' }}
                  >
                    <p className="px-3.5 pt-3 pb-1.5 text-[10px] font-bold uppercase tracking-[0.12em] text-zinc-400">
                      Study tools
                    </p>
                    {answersUrl && (
                      <ToolRow
                        icon={<Sparkles size={15} />}
                        title="Answers"
                        sub="Marking scheme beside each question"
                        on={answersOn}
                        onClick={() => {
                          toggleAnswers();
                          setToolsOpen(false);
                        }}
                      />
                    )}
                    {answersUrl && storageNs && (
                      <ToolRow
                        icon={<ListChecks size={15} />}
                        title="Triage"
                        sub="Rate each question before you start"
                        busy={answerState === 'loading'}
                        onClick={openTriage}
                      />
                    )}
                    {answersUrl && scheme && storageNs && (
                      <ToolRow
                        icon={<PenLine size={15} />}
                        title="Self-mark"
                        sub="Score yourself against the scheme"
                        on={selfMarkOn}
                        busy={selfMarkOn && answerState === 'loading'}
                        onClick={toggleSelfMark}
                      />
                    )}
                    <ToolRow
                      icon={<Clock3 size={15} />}
                      title="Time budget"
                      sub={timing ? 'Minutes to spend per question' : 'Each question’s share of the paper'}
                      on={paceOn}
                      busy={paceOn && scanState === 'loading'}
                      onClick={() => toggleTool('pace')}
                    />
                    <ToolRow
                      icon={<Highlighter size={15} />}
                      title="Command words"
                      sub="Decode what each question demands"
                      on={decodeOn}
                      busy={decodeOn && scanState === 'loading'}
                      onClick={() => toggleTool('decode')}
                    />
                    {timing && (
                      <ToolRow
                        icon={<Play size={15} />}
                        title="Exam mode"
                        sub={`Clock set to ${timing.totalMinutes} min`}
                        on={examOn}
                        onClick={() => {
                          setExamOn(v => {
                            const next = !v;
                            setRunning(next);
                            if (next) setElapsed(0);
                            return next;
                          });
                          setToolsOpen(false);
                        }}
                      />
                    )}
                    {topics && (
                      <ToolRow
                        icon={<TrendingUp size={15} />}
                        title="Topics & frequency"
                        sub="How often each topic comes up + drill it across years"
                        on={topicsOn}
                        busy={topicsOn && answerState === 'loading'}
                        onClick={toggleTopics}
                      />
                    )}
                    {grammar && (
                      <ToolRow
                        icon={<ScrollText size={15} />}
                        title="How it’s marked"
                        sub={grammar.subjectLabel}
                        onClick={() => {
                          setMarkingOpen(true);
                          setToolsOpen(false);
                        }}
                      />
                    )}
                    {examinerInsights && (
                      <ToolRow
                        icon={<ScrollText size={15} />}
                        title="Examiner insights"
                        sub="Where the Chief Examiner says marks are lost"
                        onClick={() => {
                          setExaminerOpen(true);
                          setToolsOpen(false);
                        }}
                      />
                    )}
                    {formulae && (
                      <ToolRow
                        icon={<BookOpen size={15} />}
                        title="Formulae & Tables"
                        sub="Jump to the booklet section"
                        onClick={openFormulae}
                      />
                    )}
                    {scanState === 'error' && (
                      <p className="px-3.5 py-2 text-[11px] text-zinc-500">
                        Couldn’t read this paper’s text layer — overlays unavailable.
                      </p>
                    )}
                  </MotionDiv>
                )}
              </AnimatePresence>
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
                anchors={(answersOn || topicsOn) && side === 'paper' ? anchorsByPage.get(i + 1) : undefined}
                showAnswerChip={answersOn}
                onReveal={onReveal}
                topicInfo={topicsOn && side === 'paper' ? topicInfoByN : undefined}
                onTopic={onTopic}
                marks={paceEnabled && side === 'paper' ? docTokens!.byPage.get(i + 1)?.marks : undefined}
                paceInfo={paceInfo}
                commands={decodeEnabled && side === 'paper' ? docTokens!.byPage.get(i + 1)?.commands : undefined}
                onCommand={onCommand}
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
          {/* Marks heat-strip — where the marks live across the paper (pace tool). */}
          {paceOn && side === 'paper' && marksByPage && hasAnyTokens && session.numPages > 1 && (
            <div className="max-w-3xl mx-auto mb-2">
              <div className="flex items-center justify-between mb-1">
                <span className="text-[9px] font-bold uppercase tracking-[0.12em] text-zinc-400">Where the marks are</span>
                <span className="text-[9px] text-zinc-400">tap a page</span>
              </div>
              <div className="flex gap-px h-2.5 rounded overflow-hidden bg-[#ece9e4] dark:bg-zinc-800">
                {Array.from({ length: session.numPages }, (_, i) => {
                  const v = marksByPage.map.get(i + 1) ?? 0;
                  const intensity = v / marksByPage.max;
                  return (
                    <button
                      key={i}
                      onClick={() => jumpToPage(i + 1)}
                      aria-label={`Page ${i + 1}: ${v} marks — go there`}
                      className="flex-1 min-w-[2px] transition-opacity hover:opacity-80"
                      style={{ backgroundColor: v ? `rgba(242,107,31,${0.22 + 0.78 * intensity})` : 'transparent' }}
                    />
                  );
                })}
              </div>
            </div>
          )}
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

      {/* Cross-year topic sheet — every sibling question for this subtopic. */}
      <AnimatePresence>
        {topicReveal && topics && (
          <>
            <MotionDiv
              key="topic-backdrop"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              onClick={() => setTopicReveal(null)}
              className="fixed inset-0 z-[110] bg-black/40"
            />
            <MotionDiv
              key="topic-panel"
              initial={panelHidden}
              animate={panelShown}
              exit={panelHidden}
              transition={GLIDE}
              role="dialog"
              aria-modal="true"
              aria-label={`${topicLabel(topicReveal.subtopicId)} across the years`}
              style={{ paddingBottom: 'var(--sab, 0px)' }}
              className={
                isWide
                  ? 'fixed top-0 right-0 z-[111] h-full w-full max-w-md flex flex-col bg-white dark:bg-zinc-900 shadow-2xl border-l border-zinc-200 dark:border-zinc-800'
                  : 'fixed bottom-0 inset-x-0 z-[111] max-h-[85vh] flex flex-col bg-white dark:bg-zinc-900 rounded-t-2xl shadow-2xl'
              }
            >
              <TopicContent
                wide={isWide}
                subtopicId={topicReveal.subtopicId}
                subjectId={topics.subjectId}
                current={{ year: topics.year, level: topics.level, lang: topics.lang, fileid: topics.fileid, n: topicReveal.n }}
                onJump={s => {
                  setTopicReveal(null);
                  onCrossYear?.(s);
                }}
                onClose={() => setTopicReveal(null)}
              />
            </MotionDiv>
          </>
        )}
      </AnimatePresence>

      {/* Per-question marking-scheme reveal — bottom sheet on phones, right tray
          on tablet+; same sleek glide as the GC dashboard student view. */}
      <AnimatePresence>
        {reveal && (
          <>
            <MotionDiv
              key="reveal-backdrop"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              onClick={() => setReveal(null)}
              className="fixed inset-0 z-[110] bg-black/40"
            />
            <MotionDiv
              key="reveal-panel"
              initial={panelHidden}
              animate={panelShown}
              exit={panelHidden}
              transition={GLIDE}
              role="dialog"
              aria-modal="true"
              aria-label={`Marking scheme for ${reveal.label ?? `Question ${reveal.n}`}`}
              style={{ paddingBottom: 'var(--sab, 0px)' }}
              className={
                isWide
                  ? 'fixed top-0 right-0 z-[111] h-full w-full max-w-md flex flex-col bg-white dark:bg-zinc-900 shadow-2xl border-l border-zinc-200 dark:border-zinc-800'
                  : 'fixed bottom-0 inset-x-0 z-[111] max-h-[85vh] flex flex-col bg-white dark:bg-zinc-900 rounded-t-2xl shadow-2xl'
              }
            >
              <RevealContent
                q={reveal}
                wide={isWide}
                reduced={!!reducedMotion}
                schemePdf={sessions.current.scheme.pdf}
                schemeUrl={scheme?.url}
                schemeErrored={sessions.current.scheme.state === 'error' || sessions.current.scheme.state === 'unsupported'}
                copyright={answerMap?.copyright}
                selfMark={selfMarkOn}
                existingMark={attempt.marks?.[reveal.n]}
                licence={storageNs ? markerLicence(storageNs.split('|')[0]) : null}
                onRecordMark={m => recordMark(reveal.n, m)}
                onClose={() => setReveal(null)}
                onFullScheme={jumpSchemeToPage}
              />
            </MotionDiv>
          </>
        )}
      </AnimatePresence>

      {/* Text-scan status while the overlay tools read the paper. */}
      {side === 'paper' && (paceOn || decodeOn) && scanState === 'loading' && !docTokens && (
        <div
          role="status"
          aria-live="polite"
          className="absolute left-1/2 -translate-x-1/2 bottom-24 z-[60] flex items-center gap-2 px-3 py-1.5 rounded-full text-[12px] font-medium bg-zinc-900/90 text-white shadow-lg"
        >
          <span className="w-3 h-3 rounded-full border-2 border-white/40 border-t-white animate-spin" aria-hidden />
          Reading the paper…
        </div>
      )}
      {/* Scanned paper (no text layer) — explain why overlays are absent. */}
      {side === 'paper' && (paceOn || decodeOn) && scanState === 'idle' && docTokens && !hasAnyTokens && (
        <div
          role="status"
          aria-live="polite"
          className="absolute left-1/2 -translate-x-1/2 bottom-24 z-[60] max-w-[86%] px-3.5 py-2 rounded-full text-[12px] font-medium text-center bg-zinc-900/90 text-white shadow-lg"
        >
          This paper is a scanned image — its text can’t be read for on-paper tools.
        </div>
      )}

      {/* Exam-mode clock — floating pill above the footer. */}
      {examOn && timing && side === 'paper' && (
        <ExamClock
          totalMinutes={timing.totalMinutes}
          elapsed={elapsed}
          running={running}
          onToggle={() => setRunning(r => !r)}
          onReset={() => setElapsed(0)}
          onClose={() => {
            setExamOn(false);
            setRunning(false);
          }}
        />
      )}

      {/* Command-word decoder — same glide as the answer reveal. */}
      <AnimatePresence>
        {commandReveal && (
          <>
            <MotionDiv
              key="cmd-backdrop"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              onClick={() => setCommandReveal(null)}
              className="fixed inset-0 z-[110] bg-black/40"
            />
            <MotionDiv
              key="cmd-panel"
              initial={panelHidden}
              animate={panelShown}
              exit={panelHidden}
              transition={GLIDE}
              role="dialog"
              aria-modal="true"
              aria-label={`What “${commandReveal.matched}” asks you to do`}
              style={{ paddingBottom: 'var(--sab, 0px)' }}
              className={
                isWide
                  ? 'fixed top-0 right-0 z-[111] h-full w-full max-w-md flex flex-col bg-white dark:bg-zinc-900 shadow-2xl border-l border-zinc-200 dark:border-zinc-800'
                  : 'fixed bottom-0 inset-x-0 z-[111] max-h-[85vh] flex flex-col bg-white dark:bg-zinc-900 rounded-t-2xl shadow-2xl'
              }
            >
              <CommandContent wide={isWide} token={commandReveal} onClose={() => setCommandReveal(null)} />
            </MotionDiv>
          </>
        )}
      </AnimatePresence>

      {/* "How this subject is marked" card. */}
      <AnimatePresence>
        {markingOpen && grammar && (
          <>
            <MotionDiv
              key="mark-backdrop"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              onClick={() => setMarkingOpen(false)}
              className="fixed inset-0 z-[110] bg-black/40"
            />
            <MotionDiv
              key="mark-panel"
              initial={panelHidden}
              animate={panelShown}
              exit={panelHidden}
              transition={GLIDE}
              role="dialog"
              aria-modal="true"
              aria-label={`How ${grammar.subjectLabel} is marked`}
              style={{ paddingBottom: 'var(--sab, 0px)' }}
              className={
                isWide
                  ? 'fixed top-0 right-0 z-[111] h-full w-full max-w-md flex flex-col bg-white dark:bg-zinc-900 shadow-2xl border-l border-zinc-200 dark:border-zinc-800'
                  : 'fixed bottom-0 inset-x-0 z-[111] max-h-[85vh] flex flex-col bg-white dark:bg-zinc-900 rounded-t-2xl shadow-2xl'
              }
            >
              <MarkingContent wide={isWide} grammar={grammar} onClose={() => setMarkingOpen(false)} />
            </MotionDiv>
          </>
        )}
      </AnimatePresence>

      {/* Formulae & Tables quick-jump sheet. */}
      <AnimatePresence>
        {formulaeOpen && formulae && (
          <>
            <MotionDiv
              key="formulae-backdrop"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              onClick={() => setFormulaeOpen(false)}
              className="fixed inset-0 z-[110] bg-black/40"
            />
            <MotionDiv
              key="formulae-panel"
              initial={panelHidden}
              animate={panelShown}
              exit={panelHidden}
              transition={GLIDE}
              role="dialog"
              aria-modal="true"
              aria-label="Formulae and Tables — jump to a section"
              style={{ paddingBottom: 'var(--sab, 0px)' }}
              className={
                isWide
                  ? 'fixed top-0 right-0 z-[111] h-full w-full max-w-md flex flex-col bg-white dark:bg-zinc-900 shadow-2xl border-l border-zinc-200 dark:border-zinc-800'
                  : 'fixed bottom-0 inset-x-0 z-[111] max-h-[85vh] flex flex-col bg-white dark:bg-zinc-900 rounded-t-2xl shadow-2xl'
              }
            >
              <FormulaeContent
                wide={isWide}
                handle={formulae}
                index={formulaeIndex}
                onClose={() => setFormulaeOpen(false)}
              />
            </MotionDiv>
          </>
        )}
      </AnimatePresence>

      {/* Triage — plan-your-attack ratings over the question list. */}
      <AnimatePresence>
        {triageOpen && (
          <>
            <MotionDiv key="triage-bd" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.2 }} onClick={() => setTriageOpen(false)} className="fixed inset-0 z-[110] bg-black/40" />
            <MotionDiv
              key="triage-panel"
              initial={panelHidden}
              animate={panelShown}
              exit={panelHidden}
              transition={GLIDE}
              role="dialog"
              aria-modal="true"
              aria-label="Triage — plan your attack"
              style={{ paddingBottom: 'var(--sab, 0px)' }}
              className={isWide ? 'fixed top-0 right-0 z-[111] h-full w-full max-w-md flex flex-col bg-white dark:bg-zinc-900 shadow-2xl border-l border-zinc-200 dark:border-zinc-800' : 'fixed bottom-0 inset-x-0 z-[111] max-h-[85vh] flex flex-col bg-white dark:bg-zinc-900 rounded-t-2xl shadow-2xl'}
            >
              <TriageContent
                wide={isWide}
                questions={answerMap?.q ?? null}
                loading={answerState === 'loading'}
                ratings={attempt.triage ?? {}}
                minsPerMark={minsPerMark}
                onRate={rateTriage}
                onJump={n => {
                  const q = answerMap?.q.find(x => x.n === n);
                  setTriageOpen(false);
                  if (q) requestAnimationFrame(() => {
                    const el = scrollerRef.current;
                    const target = el?.querySelector<HTMLElement>(`[data-page="${q.pP}"]`);
                    if (el && target) el.scrollTo({ top: target.offsetTop - 8 + target.clientHeight * Math.max(0, q.pY[0] - 0.02) });
                  });
                }}
                onClose={() => setTriageOpen(false)}
              />
            </MotionDiv>
          </>
        )}
      </AnimatePresence>

      {/* Examiner insights — Chief Examiner "where marks are lost" card. */}
      <AnimatePresence>
        {examinerOpen && examinerInsights && (
          <>
            <MotionDiv key="exam-bd" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.2 }} onClick={() => setExaminerOpen(false)} className="fixed inset-0 z-[110] bg-black/40" />
            <MotionDiv
              key="examiner-panel"
              initial={panelHidden}
              animate={panelShown}
              exit={panelHidden}
              transition={GLIDE}
              role="dialog"
              aria-modal="true"
              aria-label={`Examiner insights for ${examinerInsights.subjectLabel}`}
              style={{ paddingBottom: 'var(--sab, 0px)' }}
              className={isWide ? 'fixed top-0 right-0 z-[111] h-full w-full max-w-md flex flex-col bg-white dark:bg-zinc-900 shadow-2xl border-l border-zinc-200 dark:border-zinc-800' : 'fixed bottom-0 inset-x-0 z-[111] max-h-[85vh] flex flex-col bg-white dark:bg-zinc-900 rounded-t-2xl shadow-2xl'}
            >
              <ExaminerContent wide={isWide} data={examinerInsights} onClose={() => setExaminerOpen(false)} />
            </MotionDiv>
          </>
        )}
      </AnimatePresence>
    </div>,
    document.body,
  );
};

// ─── formulae & tables quick-jump content ───────────────────

const FormulaeContent: React.FC<{
  wide: boolean;
  handle: FormulaeHandle;
  index: FormulaePageIndex | null;
  onClose: () => void;
}> = ({ wide, handle, index, onClose }) => {
  const closeRef = useRef<HTMLButtonElement | null>(null);
  useEffect(() => {
    closeRef.current?.focus();
  }, []);
  // Browsers honour the #page=N fragment on a PDF URL — the booklet opens at
  // the section. Without an index entry it opens at the front.
  const hrefFor = (id: string) => {
    const page = index?.[id];
    return page ? `${handle.bookletUrl}#page=${page}` : handle.bookletUrl;
  };
  return (
    <>
      {!wide && (
        <div className="shrink-0 flex justify-center pt-2 pb-0.5" aria-hidden>
          <div className="h-1 w-9 rounded-full bg-zinc-300 dark:bg-zinc-700" />
        </div>
      )}
      <div className="shrink-0 flex items-center gap-2 px-4 py-3 border-b border-zinc-200 dark:border-zinc-800">
        <div className="flex-1 min-w-0">
          <p className="text-[15px] font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Formulae &amp; Tables</p>
          <p className="text-[11px] text-zinc-500">The SEC booklet — opens at the section you pick.</p>
        </div>
        <button ref={closeRef} onClick={onClose} aria-label="Close" className="p-2 -mr-1 rounded-lg text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100">
          <X size={18} />
        </button>
      </div>
      <div className="flex-1 overflow-auto overscroll-contain px-3 py-3 grid grid-cols-2 gap-2">
        {handle.sections.map(s => (
          <a
            key={s.id}
            href={hrefFor(s.id)}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-between gap-2 rounded-xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 px-3 py-3 text-left transition-transform active:translate-y-0.5"
          >
            <span className="text-[13px] font-semibold leading-tight" style={{ color: '#1a1a1a' }}>{s.label}</span>
            <BookOpen size={14} style={{ color: '#F26B1F' }} className="shrink-0" />
          </a>
        ))}
      </div>
      <p className="shrink-0 px-4 py-2 text-[10px] text-zinc-400 border-t border-zinc-200 dark:border-zinc-800">
        Formulae and Tables © State Examinations Commission.
      </p>
    </>
  );
};

// ─── triage (plan your attack) ──────────────────────────────

const TRIAGE_OPTS: { r: TriageRating; label: string; bg: string }[] = [
  { r: 'g', label: 'Confident', bg: '#3A8D5F' },
  { r: 'a', label: 'Unsure', bg: '#F26B1F' },
  { r: 'r', label: 'Hard', bg: '#1a1a1a' },
];

const TriageContent: React.FC<{
  wide: boolean;
  questions: PaperAnswerQuestion[] | null;
  loading: boolean;
  ratings: Record<string, TriageRating>;
  minsPerMark: number | null;
  onRate: (n: string, rating: TriageRating | null) => void;
  onJump: (n: string) => void;
  onClose: () => void;
}> = ({ wide, questions, loading, ratings, minsPerMark, onRate, onJump, onClose }) => {
  const closeRef = useRef<HTMLButtonElement | null>(null);
  useEffect(() => {
    closeRef.current?.focus();
  }, []);
  const counts = { g: 0, a: 0, r: 0 };
  for (const q of questions ?? []) {
    const rt = ratings[q.n];
    if (rt) counts[rt]++;
  }
  const rated = counts.g + counts.a + counts.r;
  return (
    <>
      {!wide && (
        <div className="shrink-0 flex justify-center pt-2 pb-0.5" aria-hidden>
          <div className="h-1 w-9 rounded-full bg-zinc-300 dark:bg-zinc-700" />
        </div>
      )}
      <div className="shrink-0 flex items-center gap-2 px-4 py-3 border-b border-zinc-200 dark:border-zinc-800">
        <div className="flex-1 min-w-0">
          <p className="text-[15px] font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Triage — plan your attack</p>
          <p className="text-[11px] text-zinc-500">Rate each question before you start. Do your confident ones first.</p>
        </div>
        <button ref={closeRef} onClick={onClose} aria-label="Close" className="p-2 -mr-1 rounded-lg text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100">
          <X size={18} />
        </button>
      </div>
      {rated > 0 && (
        <div className="shrink-0 flex items-center gap-3 px-4 py-2 text-[11px] font-semibold border-b border-zinc-100 dark:border-zinc-800">
          <span style={{ color: '#3A8D5F' }}>{counts.g} confident</span>
          <span style={{ color: '#F26B1F' }}>{counts.a} unsure</span>
          <span style={{ color: '#1a1a1a' }}>{counts.r} hard</span>
        </div>
      )}
      <div className="flex-1 overflow-auto overscroll-contain px-3 py-3 space-y-1.5">
        {!questions && loading && (
          <div className="flex flex-col items-center gap-2 py-10 text-zinc-400">
            <div className="w-5 h-5 rounded-full border-2 border-zinc-300 border-t-zinc-500 animate-spin" aria-hidden />
            <span className="text-[12px]">Loading the question list…</span>
          </div>
        )}
        {questions?.map(q => {
          const rt = ratings[q.n];
          return (
            <div key={q.n} className="rounded-xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 px-3 py-2.5">
              <div className="flex items-center justify-between gap-2 mb-1.5">
                <button onClick={() => onJump(q.n)} className="text-[13px] font-semibold text-left" style={{ color: '#1a1a1a' }}>
                  {q.label ?? `Question ${q.n}`}
                </button>
              </div>
              <div className="flex items-center gap-1.5">
                {TRIAGE_OPTS.map(opt => {
                  const active = rt === opt.r;
                  return (
                    <button
                      key={opt.r}
                      onClick={() => onRate(q.n, active ? null : opt.r)}
                      aria-pressed={active}
                      className="flex-1 py-1.5 rounded-lg text-[12px] font-semibold transition-all border-2"
                      style={
                        active
                          ? { backgroundColor: opt.bg, borderColor: opt.bg, color: '#fff' }
                          : { backgroundColor: '#fff', borderColor: '#d0cdc8', color: '#7a7068' }
                      }
                    >
                      {opt.label}
                    </button>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
      {counts.g + counts.a + counts.r > 0 && (
        <p className="shrink-0 px-4 py-2.5 text-[12px] border-t border-zinc-200 dark:border-zinc-800" style={{ color: '#5a5550' }}>
          Plan: bank the <b style={{ color: '#3A8D5F' }}>{counts.g} confident</b>{minsPerMark ? '' : ''} first, then the {counts.a} unsure, and leave the {counts.r} hard for last.
        </p>
      )}
    </>
  );
};

// ─── examiner insights card ─────────────────────────────────

const ExaminerContent: React.FC<{ wide: boolean; data: ExaminerInsightSet; onClose: () => void }> = ({ wide, data, onClose }) => {
  const closeRef = useRef<HTMLButtonElement | null>(null);
  useEffect(() => {
    closeRef.current?.focus();
  }, []);
  return (
    <>
      {!wide && (
        <div className="shrink-0 flex justify-center pt-2 pb-0.5" aria-hidden>
          <div className="h-1 w-9 rounded-full bg-zinc-300 dark:bg-zinc-700" />
        </div>
      )}
      <div className="shrink-0 flex items-center gap-2 px-4 py-3 border-b border-zinc-200 dark:border-zinc-800">
        <div className="flex-1 min-w-0">
          <p className="text-[15px] font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Examiner insights</p>
          <p className="text-[11px] text-zinc-500 truncate">{data.source}</p>
        </div>
        <button ref={closeRef} onClick={onClose} aria-label="Close" className="p-2 -mr-1 rounded-lg text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100">
          <X size={18} />
        </button>
      </div>
      <div className="flex-1 overflow-auto overscroll-contain px-4 py-4 space-y-3">
        {data.insights.map((ins, i) => (
          <div key={i} className="rounded-xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 px-3.5 py-3">
            <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-1" style={{ color: '#9e9186' }}>Where marks are lost</p>
            <p className="text-[13px] leading-relaxed mb-2.5" style={{ color: '#3a3530' }}>{ins.pitfall}</p>
            <div className="rounded-lg px-3 py-2 mb-1.5" style={{ backgroundColor: '#E8F2EC', borderLeft: '3px solid #3A8D5F' }}>
              <p className="text-[12.5px] leading-relaxed" style={{ color: '#1F5F3E' }}>{ins.fix}</p>
            </div>
            <p className="text-[10.5px] italic" style={{ color: '#9e9186' }}>{ins.cite}</p>
          </div>
        ))}
      </div>
      <p className="shrink-0 px-4 py-2 text-[10px] text-zinc-400 border-t border-zinc-200 dark:border-zinc-800">
        Source: State Examinations Commission. Full report in the school’s evidence dossier.
      </p>
    </>
  );
};

// ─── exam-mode clock ────────────────────────────────────────

const fmtClock = (sec: number) => {
  const s = Math.max(0, Math.floor(sec));
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const r = s % 60;
  const pad = (n: number) => String(n).padStart(2, '0');
  return h > 0 ? `${h}:${pad(m)}:${pad(r)}` : `${m}:${pad(r)}`;
};

const ExamClock: React.FC<{
  totalMinutes: number;
  elapsed: number;
  running: boolean;
  onToggle: () => void;
  onReset: () => void;
  onClose: () => void;
}> = ({ totalMinutes, elapsed, running, onToggle, onReset, onClose }) => {
  const totalSec = totalMinutes * 60;
  const remaining = totalSec - elapsed;
  const over = remaining < 0;
  const frac = Math.min(1, Math.max(0, elapsed / totalSec));
  return (
    <div
      className="absolute left-1/2 -translate-x-1/2 bottom-[76px] z-[65] flex items-center gap-2.5 pl-3 pr-2 py-2 rounded-2xl bg-white dark:bg-zinc-900 border-2 border-[#1A1A1A] dark:border-zinc-700 shadow-[3px_3px_0_0_#1A1A1A] dark:shadow-[3px_3px_0_0_#3f3f46]"
      role="timer"
      aria-live="off"
    >
      <div className="flex flex-col">
        <span
          className="text-[16px] font-bold tabular-nums leading-none"
          style={{ fontFamily: "'Source Serif 4', serif", color: over ? '#F26B1F' : '#1a1a1a' }}
        >
          {over ? `+${fmtClock(-remaining)}` : fmtClock(remaining)}
        </span>
        <span className="text-[9px] font-bold uppercase tracking-wide mt-0.5" style={{ color: over ? '#F26B1F' : '#9e9186' }}>
          {over ? 'over time' : 'remaining'}
        </span>
      </div>
      <div className="w-16 h-1.5 rounded-full overflow-hidden bg-[#e0dbd4]" aria-hidden>
        <div className="h-full rounded-full" style={{ width: `${frac * 100}%`, backgroundColor: over ? '#F26B1F' : '#3A8D5F' }} />
      </div>
      <button onClick={onToggle} aria-label={running ? 'Pause timer' : 'Start timer'} className="p-1.5 rounded-lg text-zinc-600 hover:text-zinc-900 dark:text-zinc-300">
        {running ? <Pause size={16} /> : <Play size={16} />}
      </button>
      <button onClick={onReset} aria-label="Reset timer" className="p-1.5 rounded-lg text-zinc-500 hover:text-zinc-800 dark:text-zinc-400">
        <RotateCcw size={15} />
      </button>
      <button onClick={onClose} aria-label="Close exam mode" className="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-700 dark:text-zinc-500">
        <X size={15} />
      </button>
    </div>
  );
};

// ─── tools-menu row ─────────────────────────────────────────

const ToolRow: React.FC<{
  icon: React.ReactNode;
  title: string;
  sub: string;
  on?: boolean;
  busy?: boolean;
  onClick: () => void;
}> = ({ icon, title, sub, on, busy, onClick }) => (
  <button
    role="menuitemcheckbox"
    aria-checked={!!on}
    onClick={onClick}
    className="w-full flex items-center gap-3 px-3.5 py-2.5 text-left hover:bg-zinc-50 dark:hover:bg-zinc-800/60 transition-colors"
  >
    <span
      className="shrink-0 w-8 h-8 rounded-lg flex items-center justify-center"
      style={{ backgroundColor: on ? '#F26B1F' : '#FDEEDF', color: on ? '#fff' : '#F26B1F' }}
    >
      {busy ? <span className="w-3.5 h-3.5 rounded-full border-2 border-current/40 border-t-current animate-spin" /> : icon}
    </span>
    <span className="flex-1 min-w-0">
      <span className="block text-[13px] font-semibold text-zinc-900 dark:text-zinc-100">{title}</span>
      <span className="block text-[11px] text-zinc-500 truncate">{sub}</span>
    </span>
    {on !== undefined && (
      <span
        className="shrink-0 w-9 h-5 rounded-full p-0.5 transition-colors"
        style={{ backgroundColor: on ? '#F26B1F' : '#d0cdc8' }}
        aria-hidden
      >
        <span className="block w-4 h-4 rounded-full bg-white transition-transform" style={{ transform: on ? 'translateX(16px)' : 'none' }} />
      </span>
    )}
  </button>
);

// ─── command-word decoder content ───────────────────────────

const CommandContent: React.FC<{ wide: boolean; token: CommandToken; onClose: () => void }> = ({ wide, token, onClose }) => {
  const closeRef = useRef<HTMLButtonElement | null>(null);
  useEffect(() => {
    closeRef.current?.focus();
  }, []);
  const { entry, matched } = token;
  const alias = matched.toLowerCase() !== entry.word.toLowerCase();
  return (
    <>
      {!wide && (
        <div className="shrink-0 flex justify-center pt-2 pb-0.5" aria-hidden>
          <div className="h-1 w-9 rounded-full bg-zinc-300 dark:bg-zinc-700" />
        </div>
      )}
      <div className="shrink-0 flex items-center gap-2 px-4 py-3 border-b border-zinc-200 dark:border-zinc-800">
        <div className="flex-1 min-w-0">
          <p className="text-[15px] font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>
            “{entry.word}”
            {alias && <span className="ml-1.5 text-[12px] font-sans font-normal text-zinc-500">seen as “{matched}”</span>}
          </p>
          <p className="text-[11px] text-zinc-500">Command word · {entry.typicalMarkRange}</p>
        </div>
        <button ref={closeRef} onClick={onClose} aria-label="Close" className="p-2 -mr-1 rounded-lg text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100">
          <X size={18} />
        </button>
      </div>
      <div className="flex-1 overflow-auto overscroll-contain px-4 py-4 space-y-3.5">
        <div>
          <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-1" style={{ color: '#9e9186' }}>What it asks</p>
          <p className="text-[13.5px] leading-relaxed" style={{ color: '#3a3530' }}>{entry.requiredAction}</p>
        </div>
        <div className="rounded-xl px-3.5 py-3" style={{ backgroundColor: '#FDEEDF', borderLeft: '3px solid #F26B1F' }}>
          <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-1" style={{ color: '#8C3A0E' }}>How to structure it</p>
          <p className="text-[13px] leading-relaxed" style={{ color: '#8C3A0E' }}>{entry.structuralTemplate}</p>
        </div>
        <div>
          <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-1" style={{ color: '#9e9186' }}>Where students lose marks</p>
          <p className="text-[13px] leading-relaxed" style={{ color: '#5a5550' }}>{entry.commonError}</p>
        </div>
      </div>
    </>
  );
};

// ─── cross-year topic content ───────────────────────────────

const LVL_ABBR: Record<string, string> = { higher: 'HL', ordinary: 'OL', foundation: 'FL', common: 'CL' };
const paperAbbr = (k: string) => (k === 'p1' ? 'P1' : k === 'p2' ? 'P2' : '');

const TopicContent: React.FC<{
  wide: boolean;
  subtopicId: string;
  subjectId: string;
  current: { year: number; level: string; lang: string; fileid: string; n: string };
  onJump: (s: TopicSibling) => void;
  onClose: () => void;
}> = ({ wide, subtopicId, subjectId, current, onJump, onClose }) => {
  const closeRef = useRef<HTMLButtonElement | null>(null);
  useEffect(() => {
    closeRef.current?.focus();
  }, []);
  const siblings = useMemo(() => siblingsFor(subjectId, subtopicId), [subjectId, subtopicId]);
  const years = new Set(siblings.map(s => s.year));
  const isCurrent = (s: TopicSibling) =>
    s.year === current.year && s.level === current.level && s.lang === current.lang && s.fileid === current.fileid && s.n === current.n;
  return (
    <>
      {!wide && (
        <div className="shrink-0 flex justify-center pt-2 pb-0.5" aria-hidden>
          <div className="h-1 w-9 rounded-full bg-zinc-300 dark:bg-zinc-700" />
        </div>
      )}
      <div className="shrink-0 flex items-center gap-2 px-4 py-3 border-b border-zinc-200 dark:border-zinc-800">
        <div className="flex-1 min-w-0">
          <p className="text-[15px] font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>{topicLabel(subtopicId)}</p>
          <p className="text-[11px] text-zinc-500">
            {siblings.length} question{siblings.length === 1 ? '' : 's'} across {years.size} tagged year{years.size === 1 ? '' : 's'} — tap to drill it
          </p>
        </div>
        <button ref={closeRef} onClick={onClose} aria-label="Close" className="p-2 -mr-1 rounded-lg text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100">
          <X size={18} />
        </button>
      </div>
      <div className="flex-1 overflow-auto overscroll-contain px-3 py-3 space-y-1.5">
        {siblings.map(s => {
          const here = isCurrent(s);
          return (
            <button
              key={`${s.year}-${s.level}-${s.lang}-${s.fileid}-${s.n}`}
              onClick={() => !here && onJump(s)}
              disabled={here}
              className={`w-full flex items-center gap-3 rounded-xl border-2 px-3.5 py-2.5 text-left transition-transform ${
                here ? 'border-[#F26B1F] bg-[#FDEEDF]' : 'border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 active:translate-y-0.5'
              }`}
            >
              <span className="shrink-0 w-11 text-[13px] font-bold tabular-nums" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>{s.year}</span>
              <span className="flex-1 text-[12.5px]" style={{ color: '#5a5550' }}>
                {LVL_ABBR[s.level] ?? s.level}
                {paperAbbr(s.paperKey) ? ` · ${paperAbbr(s.paperKey)}` : ''}
                {s.lang === 'iv' ? ' · Gaeilge' : ''} · Question {s.n}
              </span>
              {here ? (
                <span className="shrink-0 text-[10px] font-bold uppercase tracking-wide" style={{ color: '#8C3A0E' }}>you’re here</span>
              ) : (
                <ArrowLeft size={14} className="shrink-0 rotate-180" style={{ color: '#F26B1F' }} />
              )}
            </button>
          );
        })}
      </div>
      <p className="shrink-0 px-4 py-2 text-[10px] text-zinc-400 border-t border-zinc-200 dark:border-zinc-800">
        Frequency reflects the years tagged so far — coverage grows as more papers are added.
      </p>
    </>
  );
};

// ─── marking-grammar card content ───────────────────────────

const MarkingContent: React.FC<{ wide: boolean; grammar: SubjectMarkingGrammar; onClose: () => void }> = ({ wide, grammar, onClose }) => {
  const closeRef = useRef<HTMLButtonElement | null>(null);
  useEffect(() => {
    closeRef.current?.focus();
  }, []);
  return (
    <>
      {!wide && (
        <div className="shrink-0 flex justify-center pt-2 pb-0.5" aria-hidden>
          <div className="h-1 w-9 rounded-full bg-zinc-300 dark:bg-zinc-700" />
        </div>
      )}
      <div className="shrink-0 flex items-center gap-2 px-4 py-3 border-b border-zinc-200 dark:border-zinc-800">
        <div className="flex-1 min-w-0">
          <p className="text-[15px] font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>How it’s marked</p>
          <p className="text-[11px] text-zinc-500 truncate">{grammar.subjectLabel}</p>
        </div>
        <button ref={closeRef} onClick={onClose} aria-label="Close" className="p-2 -mr-1 rounded-lg text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100">
          <X size={18} />
        </button>
      </div>
      <div className="flex-1 overflow-auto overscroll-contain px-4 py-4 space-y-4">
        <p className="text-[13.5px] leading-relaxed" style={{ color: '#3a3530' }}>{grammar.architecture}</p>
        <div className="space-y-2.5">
          {grammar.rules.map((r, i) => (
            <div key={i} className="rounded-xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 px-3.5 py-3">
              <p className="text-[13px] font-semibold mb-0.5" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>{r.title}</p>
              <p className="text-[12.5px] leading-relaxed" style={{ color: '#5a5550' }}>{r.body}</p>
            </div>
          ))}
        </div>
        {grammar.workedExample && (
          <div className="rounded-xl px-3.5 py-3" style={{ backgroundColor: '#E8F2EC', borderLeft: '3px solid #3A8D5F' }}>
            <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-1" style={{ color: '#1F5F3E' }}>Worked example</p>
            <p className="text-[12.5px] leading-relaxed mb-1.5" style={{ color: '#1F5F3E' }}>{grammar.workedExample.setup}</p>
            <p className="text-[12.5px] leading-relaxed font-semibold" style={{ color: '#1F5F3E' }}>{grammar.workedExample.outcome}</p>
          </div>
        )}
      </div>
    </>
  );
};

// ─── per-question marking-scheme reveal content (inside the glide panel) ─────

const SCORE_BANDS: { v: number; label: string }[] = [
  { v: 0, label: 'Blank' },
  { v: 25, label: 'Some' },
  { v: 50, label: 'Half' },
  { v: 75, label: 'Most' },
  { v: 100, label: 'Full' },
];
const GAP_OPTS: { k: GapKind; label: string }[] = [
  { k: 'content', label: 'Didn’t know it' },
  { k: 'process', label: 'Wrong method' },
  { k: 'careless', label: 'Careless slip' },
  { k: 'timing', label: 'Ran out of time' },
];

const RevealContent: React.FC<{
  q: PaperAnswerQuestion;
  wide: boolean;
  reduced: boolean;
  schemePdf: PDFDocumentProxy | null;
  schemeUrl?: string;
  schemeErrored: boolean;
  copyright?: string;
  selfMark?: boolean;
  existingMark?: SelfMark;
  /** Marker's Licence — calibration earned in The Examiner's Chair (F3). */
  licence?: MarkerLicence | null;
  onRecordMark?: (mark: SelfMark | null) => void;
  onClose: () => void;
  onFullScheme: (page: number) => void;
}> = ({ q, wide, reduced, schemePdf, schemeUrl, schemeErrored, copyright, selfMark, existingMark, licence, onRecordMark, onClose, onFullScheme }) => {
  const firstPage = q.region[0]?.p;
  const closeRef = useRef<HTMLButtonElement | null>(null);
  useEffect(() => {
    closeRef.current?.focus();
  }, []);
  const scored = existingMark?.score;
  const setScore = (v: number) =>
    onRecordMark?.({ score: v, max: 100, gap: v >= 100 ? undefined : existingMark?.gap, ts: Date.now() });
  const setGap = (k: GapKind) =>
    onRecordMark?.({ score: existingMark?.score ?? 0, max: 100, gap: existingMark?.gap === k ? undefined : k, ts: Date.now() });
  return (
    <>
      {!wide && (
        <div className="shrink-0 flex justify-center pt-2 pb-0.5" aria-hidden>
          <div className="h-1 w-9 rounded-full bg-zinc-300 dark:bg-zinc-700" />
        </div>
      )}
      <div className="shrink-0 flex items-center gap-2 px-4 py-3 border-b border-zinc-200 dark:border-zinc-800">
        <div className="flex-1 min-w-0">
          <p className="text-[14px] font-semibold text-zinc-900 dark:text-white">{q.label ?? `Question ${q.n}`} · marking scheme</p>
          <p className="text-[11px] text-zinc-500">How examiners award the marks — not a model answer.</p>
        </div>
        <button ref={closeRef} onClick={onClose} aria-label="Close" className="p-2 -mr-1 rounded-lg text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100">
          <X size={18} />
        </button>
      </div>
      {/* Content settles a beat after the panel lands (premium stagger). */}
      <MotionDiv
        initial={reduced ? false : { opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: reduced ? 0 : 0.08, duration: 0.28, ease: [0.16, 1, 0.3, 1] }}
        className="flex-1 overflow-auto overscroll-contain px-3 py-3 bg-zinc-100 dark:bg-zinc-950"
      >
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
      </MotionDiv>
      {selfMark && (
        <div className="shrink-0 px-4 py-3 border-t border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900">
          <div className="flex items-baseline justify-between gap-2 mb-2">
            <p className="text-[11px] font-bold uppercase tracking-[0.1em]" style={{ color: '#9e9186' }}>
              How did you do against the scheme?
            </p>
            {licence && (
              <span className="shrink-0 text-[10.5px] font-semibold rounded-full px-2 py-0.5" style={{ backgroundColor: '#E8F2EC', color: '#1F5F3E' }}>
                {licence.pct}%-calibrated eye · {licence.sessions} chair sessions
              </span>
            )}
          </div>
          <div className="flex items-center gap-1.5 mb-2">
            {SCORE_BANDS.map(b => {
              const active = scored === b.v;
              return (
                <button
                  key={b.v}
                  onClick={() => setScore(b.v)}
                  aria-pressed={active}
                  className="flex-1 py-1.5 rounded-lg text-[11.5px] font-semibold border-2 transition-all"
                  style={active ? { backgroundColor: '#3A8D5F', borderColor: '#3A8D5F', color: '#fff' } : { backgroundColor: '#fff', borderColor: '#d0cdc8', color: '#7a7068' }}
                >
                  {b.label}
                </button>
              );
            })}
          </div>
          {scored !== undefined && scored < 100 && (
            <>
              <p className="text-[11px] mb-1.5" style={{ color: '#7a7068' }}>What went wrong? (helps your weakness map)</p>
              <div className="flex flex-wrap gap-1.5">
                {GAP_OPTS.map(g => {
                  const active = existingMark?.gap === g.k;
                  return (
                    <button
                      key={g.k}
                      onClick={() => setGap(g.k)}
                      aria-pressed={active}
                      className="px-2.5 py-1 rounded-full text-[11.5px] font-medium border-2 transition-all"
                      style={active ? { backgroundColor: '#FDEEDF', borderColor: '#F26B1F', color: '#8C3A0E' } : { backgroundColor: '#fff', borderColor: '#d0cdc8', color: '#7a7068' }}
                    >
                      {g.label}
                    </button>
                  );
                })}
              </div>
            </>
          )}
        </div>
      )}
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
    </>
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
  showAnswerChip?: boolean;
  onReveal?: (q: PaperAnswerQuestion) => void;
  topicInfo?: Map<string, { subtopicId: string; label: string; yearsWith: number; totalYears: number }> | null;
  onTopic?: (n: string) => void;
  marks?: MarkToken[];
  paceInfo?: { minsPerMark: number | null; totalMarks: number };
  commands?: CommandToken[];
  onCommand?: (c: CommandToken) => void;
}> = React.memo(({ pdf, pageNumber, zoom, epoch, observe, anchors, showAnswerChip, onReveal, topicInfo, onTopic, marks, paceInfo, commands, onCommand }) => {
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
      {/* Per-question chips — fractional top rides zoom + virtualisation. The
          "Answer" chip rides the right edge; the topic/frequency chip the left. */}
      {anchors?.map(q => {
        const top = `${Math.min(0.97, Math.max(0, q.pY[0])) * 100}%`;
        const info = topicInfo?.get(q.n);
        return (
          <React.Fragment key={`${q.pP}-${q.n}`}>
            {info && (
              <button
                onClick={() => onTopic?.(q.n)}
                className="absolute left-0 z-10 flex items-center gap-1 pr-2 pl-1.5 py-1 rounded-r-full text-[11px] font-bold"
                style={{
                  top,
                  // Float just above the question's first line so the label
                  // doesn't sit on top of the question text (unless it's at the
                  // very top of the page, where there's no room above).
                  transform: q.pY[0] > 0.05 ? 'translateY(-100%)' : 'none',
                  backgroundColor: '#FDEEDF',
                  color: '#8C3A0E',
                  border: '1px solid rgba(242,107,31,0.4)',
                  boxShadow: '0 1px 5px rgba(0,0,0,.15)',
                }}
                aria-label={`${info.label} — appeared in ${info.yearsWith} of ${info.totalYears} tagged years. Drill it across years.`}
              >
                <TrendingUp size={11} /> {info.label}
                {info.totalYears > 0 && (
                  <span className="tabular-nums opacity-80">· {info.yearsWith}/{info.totalYears}</span>
                )}
              </button>
            )}
            {showAnswerChip && (
              <button
                onClick={() => onReveal?.(q)}
                className="absolute right-0 z-10 flex items-center gap-1 pl-2 pr-2.5 py-1 rounded-l-full text-[11px] font-bold text-white"
                style={{ top, backgroundColor: '#F26B1F', boxShadow: '0 1px 5px rgba(0,0,0,.28)' }}
                aria-label={`See the marking scheme answer for ${q.label ?? `Question ${q.n}`}`}
              >
                <Sparkles size={11} /> Answer
              </button>
            )}
          </React.Fragment>
        );
      })}
      {/* Command-word highlights — underline the leading command + tap for what
          it demands. Subtle accent so the page still reads as the real paper. */}
      {commands?.map((c, i) => (
        <button
          key={`cmd-${i}-${c.matched}`}
          onClick={() => onCommand?.(c)}
          className="absolute z-10 rounded-sm"
          style={{
            left: `${c.pX * 100}%`,
            top: `${c.pY * 100}%`,
            width: `${c.pW * 100}%`,
            height: `${c.pH * 100}%`,
            backgroundColor: 'rgba(242,107,31,0.16)',
            borderBottom: '2px solid #F26B1F',
          }}
          aria-label={`What “${c.matched}” asks you to do — command word guide`}
        />
      ))}
      {/* Time-budget chips — one per marks token, anchored just before it. The
          cover page (1) carries the grand total, not a question — skip it. */}
      {pageNumber > 1 && marks?.map((mk, i) => {
        const label =
          paceInfo?.minsPerMark != null
            ? `≈${Math.max(1, Math.round(mk.value * paceInfo.minsPerMark))} min`
            : paceInfo && paceInfo.totalMarks > 0
              ? `${Math.max(1, Math.round((mk.value / paceInfo.totalMarks) * 100))}%`
              : `${mk.value}`;
        return (
          <span
            key={`mk-${i}-${mk.value}`}
            className="absolute z-10 flex items-center gap-0.5 px-1.5 py-0.5 rounded-full text-[10px] font-bold whitespace-nowrap pointer-events-none"
            style={{
              left: `${mk.pX * 100}%`,
              top: `${(mk.pY + mk.pH / 2) * 100}%`,
              transform: 'translate(-104%, -50%)',
              backgroundColor: '#FDEEDF',
              color: '#8C3A0E',
              border: '1px solid rgba(242,107,31,0.35)',
            }}
          >
            <Clock3 size={9} /> {label}
          </span>
        );
      })}
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
