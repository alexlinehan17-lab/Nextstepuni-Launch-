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

import '../launchpad/launchpad.css';
import React, { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence, useReducedMotion } from 'framer-motion';
import {
  BookOpen,
  ChevronLeft,
  ChevronRight,
  Clock3,
  Pause,
  Play,
  Minus,
  Plus,
  RotateCcw,
  SlidersHorizontal,
  X,
} from 'lucide-react';
import { MotionDiv } from '../Motion';
import { Button as UiButton, IconButton, TextButton } from '../ui/Button';
import { TopBar } from '../ui/Bars';
import { ChoiceTile, SelectionBar, Switch } from '../ui/Choice';
import { Sheet } from '../ui/Sheet';
import { List, Row } from '../ui/List';
import { MenuAction, MenuLabel, MenuPanel, MenuSwitch } from '../ui/Menu';
import KobraScope, {
  Alert,
  AlertDescription,
  Spinner,
  Toasts,
  toast,
} from '../approved-ui-runtime';
import { prettyBytes } from './storage';
import { fetchPdfCached } from './pdfCache';
import { clearLoopPlace, loadLoopPlace, saveLoopPlace } from './loopResume';
import { composeReceipt, downloadReceipt, type LoopReceiptStats } from './receipt';
import { scanDocument, type CommandToken, type DocTokens, type MarkToken } from './textOverlay';
import { frequencyFor, questionLabel, siblingsFor, topicLabel, type TopicSibling } from './topics';
import { loadAttempt, setMark, setTriage, type GapKind, type SelfMark, type TriageRating } from './attemptStore';
import { markerLicence, type MarkerLicence } from './trust';
import { loadCalibration, paceScale } from './wpmStore';
import WpmCalibrator from './WpmCalibrator';
import { recordActivity } from './streakStore';
import type { ExaminerInsightSet } from '../../data/paperTrail/examinerInsights';
import type { FormulaeHandle, FormulaePageIndex } from '../../data/paperTrailFormulae';
import type { SubjectMarkingGrammar, SubjectTiming } from '../../types/knowledge';
import type { PaperTopicTags } from '../../types/paperTrailTopics';
import type { PaperAnswerMap, PaperAnswerQuestion } from '../../types/paperTrail';
import type { PDFDocumentProxy, PDFPageProxy } from 'pdfjs-dist';
// pdf.js lazy singleton + region renderer — shared with the Topic Vault.
import { loadPdfjs, openPdfDocument, type PdfjsModule } from './pdfjsLoader';
import CropView from './CropView';
import { captureZoomAnchor, restoreZoomAnchor, type ZoomAnchor } from './zoomAnchor';
import MobileQuestionTools from './MobileQuestionTools';
import { printedQuestionAnchors, questionsInDisplayOrder, schemeRegionFor } from './paperRegion';
import { isAnswerMap, mergePaperAnchorMetadata } from './vaultResolve';
import { audioForPaper } from './paperRecording';
import FrenchPaperAudio from './FrenchPaperAudio';
// The chrome (top bar, Tools menu, page bar, status toasts) is Kobra; see the file.
import './viewer-chrome.css';
import AnswerDesk from './AnswerDesk';
import AnswerInk, {type AnswerInkProps,type InkTool} from './AnswerInk';
import {useAnswerBook} from './useAnswerBook';
import {loadDeskQuestion,saveDeskQuestion,keepFirstAttempt,hasResponse,type InkStroke,type AnswerRecord} from './answerDeskStore';
import { COLORS } from '../../design/tokens';

// Sleek glide shared with the GC dashboard student-view tray.
const GLIDE = { duration: 0.32, ease: [0.16, 1, 0.3, 1] as const };

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
  /** The bar's name and the small line over it ("Physics" over "2025 · Higher ·
   *  Exam Paper"); default the title and subtitle. */
  barName?: string;
  barOver?: string;
  /** The paper is in Saved papers; Tools can save it or take it out ("Save this paper"). */
  saved?: boolean;
  onSave?: () => void;
  paper: ViewerDoc;
  scheme?: ViewerDoc;
  initialSide?: 'paper' | 'scheme';
  /** 1-based starting page per side (from recents). */
  initialPaperPage?: number;
  /** Open a guided preview with the verified answer ribbons already visible. */
  initialAnswersOn?: boolean;
  initialSchemePage?: number;
  /** Storage URL of this paper's PaperAnswerMap sidecar — present only when a
   *  verified answer map shipped. Drives the "Answers" toggle + question chips. */
  answersUrl?: string;
  /** Hosted paper-only sidecar used to land a Topic Atlas jump. Its audited
   * paper coordinates override a matching Storage map's paper jump while the
   * Storage map remains authoritative for verified marking-scheme crops. */
  focusAnchorsUrl?: string;
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
  /** Set when the server ANSWERED with an error (4xx/5xx) — the connection is
   *  fine, so the failure copy must not blame it (e.g. 402 = billing lapsed). */
  httpStatus?: number;
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
  barName,
  barOver,
  saved = false,
  onSave,
  paper,
  scheme,
  initialSide = 'paper',
  initialPaperPage = 1,
  initialAnswersOn = false,
  initialSchemePage = 1,
  answersUrl,
  focusAnchorsUrl,
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
  const audioSource = useMemo(() => topics ? audioForPaper(topics) : null, [topics]);
  const deskNs = storageNs ?? `anon|${paper.url}`;
  const book = useAnswerBook(deskNs);
  // Opening a paper never opts the student into the answer desk. Saved work
  // remains available when they explicitly enable it for this visit.
  const [attemptFirst,setAttemptFirst] = useState(false);
  const [deskId,setDeskId] = useState(() => focusQuestion ?? loadDeskQuestion(deskNs) ?? `page:${initialPaperPage}`);
  const [deskCollapsed,setDeskCollapsed] = useState(false);
  const [deskWidth,setDeskWidth] = useState(43);
  const [deskHeight,setDeskHeight] = useState(49);
  const [deskResizing,setDeskResizing] = useState(false);
  const workspaceRef = useRef<HTMLDivElement | null>(null);
  const deskResizeAnchor = useRef<ZoomAnchor | null>(null);
  const deskDrag = useRef<{pointer:number;end:number;extent:number;wide:boolean} | null>(null);
  const [inkTool,setInkTool] = useState<InkTool>('move');
  const [inkView,setInkView] = useState<'first'|'retry'>('retry');
  const inkHistory = useRef<Record<string,InkStroke[][]>>({});
  const deskRecord = book.get(deskId);
  const [side, setSide] = useState<Side>(initialSide === 'scheme' && scheme ? 'scheme' : 'paper');
  const [zoom, setZoom] = useState(1);
  const activeSideRef = useRef(side);
  activeSideRef.current = side;
  const readingPoint = useRef<{side: Side; anchor: ZoomAnchor} | null>(null);
  const [epoch, setEpoch] = useState(0); // bumped on resize/rotation → canvases re-render
  const [, forceRender] = useState(0);
  const bump = useCallback(() => forceRender(n => n + 1), []);

  // ── answers (per-question marking-scheme crops) ──
  const [answersOn, setAnswersOn] = useState(initialAnswersOn);
  const [answerMap, setAnswerMap] = useState<PaperAnswerMap | null>(null);
  const [answerState, setAnswerState] = useState<'idle' | 'loading' | 'error'>('idle');
  const [focusAnchorMap, setFocusAnchorMap] = useState<PaperAnswerMap | null>(null);
  const [focusAnchorSettled, setFocusAnchorSettled] = useState(false);
  const focusAnchorStartedRef = useRef(false);
  const [reveal, setReveal] = useState<PaperAnswerQuestion | null>(null);
  const schemePrefetched = useRef(false);

  // ── on-paper study tools (live text-layer overlays) ──
  const [toolsOpen, setToolsOpen] = useState(false); // Tools menu (a controlled Kobra DropdownMenu)
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
  // Handwriting-speed calibration (F4) — scales the minute budgets to the
  // student's measured pace. attemptNs leads with the uid, so derive it from
  // the storage namespace (this component deliberately has no uid prop).
  const wpmUid = storageNs ? storageNs.split('|')[0] : undefined;
  const [wpmCal, setWpmCal] = useState(() => loadCalibration(wpmUid));
  const [calibratorOpen, setCalibratorOpen] = useState(false);
  const minsPerMark = timing ? (timing.totalMinutes / timing.totalMarks) * paceScale(wpmCal) : null;

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
  // A scheme opened beside the paper needs room for both. From 1100px the
  // workspace widens to about half the screen; narrower tablets open the
  // scheme over the paper instead.
  const [isRoomy, setIsRoomy] = useState(
    () => typeof window !== 'undefined' && window.matchMedia('(min-width: 1100px)').matches,
  );
  useEffect(() => {
    const mq = window.matchMedia('(min-width: 1100px)');
    const on = () => setIsRoomy(mq.matches);
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

  const onCommand = useCallback((c: CommandToken) => setCommandReveal(c), []);

  // page → its question anchors, memoised so Page's React.memo holds across
  // scroll/zoom re-renders (a fresh filter() each render would defeat it).
  const anchorsByPage = useMemo(() => {
    const m = new Map<number, PaperAnswerQuestion[]>();
    if (answerMap) for (const q of printedQuestionAnchors(answerMap.q)) {
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
    onCloseRef.current = () => {
      if (book.hasProblems() && !window.confirm('This browser has not saved your latest work. Download a copy from the answer desk before leaving. Leave anyway?')) return;
      onClose();
    };
    onPositionRef.current = onPosition;
  });

  const activeDoc = side === 'paper' ? paper : scheme!;
  const session = sessions.current[side];

  useEffect(() => {
    const protect = (event: BeforeUnloadEvent) => { if (book.hasProblems()) {event.preventDefault();event.returnValue='';} };
    window.addEventListener('beforeunload',protect);
    return () => window.removeEventListener('beforeunload',protect);
  // The book methods read stable refs for this mounted paper.
  }, []);

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
      s.httpStatus = undefined;
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
        // Cache-first bytes (CacheStorage, LRU-capped) — instant on repeat
        // opens and works offline. null → fall back to pdf.js's own URL
        // loader, which surfaces the existing retry / open-in-browser UI.
        const bytes = await withTimeout(fetchPdfCached(target.url), LOAD_TIMEOUT_MS).catch(
          () => null,
        );
        if (!mountedRef.current) return;
        const task = bytes
          ? openPdfDocument(pdfjs, { data: new Uint8Array(bytes) })
          : openPdfDocument(pdfjs, { url: target.url });
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
      } catch (e) {
        if (mountedRef.current) {
          s.state = 'error';
          // pdf.js's URL loader throws UnexpectedResponseException with the
          // HTTP status when the server answered but refused (402/403/5xx),
          // and MissingPDFException on 404. A status here means the network
          // is fine — the failure copy must say so instead of blaming it.
          const status = (e as { status?: unknown }).status;
          s.httpStatus =
            typeof status === 'number' && status >= 400
              ? status
              : (e as { name?: string }).name === 'MissingPDFException'
                ? 404
                : undefined;
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
          setAnswerMap({ ...m, q: questionsInDisplayOrder(m.q) });
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

  const initialAnswersStarted = useRef(false);
  useEffect(() => {
    if (attemptFirst || !initialAnswersOn || initialAnswersStarted.current) return;
    initialAnswersStarted.current = true;
    ensureAnswerMap();
    if (scheme && !sessions.current.scheme.pdf && !sessions.current.scheme.task) load('scheme');
  }, [initialAnswersOn, attemptFirst, ensureAnswerMap, scheme, load]);

  useEffect(() => { if (attemptFirst) ensureAnswerMap(); }, [attemptFirst, ensureAnswerMap]);

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
    setAttemptFirst(false); // Explicitly entering the existing marking workflow.
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

  // ── The Full Loop (PT-2): question → attempt → reveal → self-mark → next ──
  // One guided pass through every mapped question of the paper, reusing the
  // existing reveal + self-mark machinery; the loop only sequences them.
  const [loop, setLoop] = useState<{ idx: number; qStartTs: number } | null>(null);
  const [loopDone, setLoopDone] = useState(false);
  const [loopTick, setLoopTick] = useState(0);
  // ── save-and-exit: the loop place persists per uid+paper (loopResume.ts) ──
  const [resumePlace, setResumePlace] = useState(() =>
    storageNs ? loadLoopPlace(storageNs, Date.now()) : null,
  );
  // Quiet "your place is saved" line, shown briefly on the exit path.
  const [placeSavedNote, setPlaceSavedNote] = useState(false);
  const [receiptSaved, setReceiptSaved] = useState(false);
  // Whole-loop wall clock: set on start (or back-dated on resume); the finish
  // path snapshots it for the receipt.
  const loopStartedAtRef = useRef(0);
  const loopTotalSecRef = useRef(0);
  // Ref mirrors so unmount/pagehide handlers see live state without re-binding.
  const loopStateRef = useRef(loop);
  loopStateRef.current = loop;
  const answerMapRef = useRef<PaperAnswerMap | null>(null);
  answerMapRef.current = answerMap;
  // The Full Loop walks the printed questions. Reviewed practice tasks stay in
  // the map so a focused jump can still find them, but a student looping the
  // paper answers each printed question once rather than its parts again.
  const loopQuestions = useMemo(() => (answerMap ? printedQuestionAnchors(answerMap.q) : []), [answerMap]);
  const loopQuestionsRef = useRef(loopQuestions);
  loopQuestionsRef.current = loopQuestions;
  const attemptMarkedRef = useRef(0);
  attemptMarkedRef.current = Object.keys(attempt.marks ?? {}).length;

  const persistLoopPlace = useCallback(() => {
    const l = loopStateRef.current;
    if (!l || !storageNs) return;
    const total = loopQuestionsRef.current.length;
    if (total < 1) return;
    saveLoopPlace(
      storageNs,
      {
        idx: Math.min(l.idx, total - 1),
        total,
        elapsedSec: loopStartedAtRef.current
          ? Math.max(0, Math.round((Date.now() - loopStartedAtRef.current) / 1000))
          : 0,
        marked: attemptMarkedRef.current,
      },
      Date.now(),
    );
  }, [storageNs]);
  const persistLoopPlaceRef = useRef(persistLoopPlace);
  persistLoopPlaceRef.current = persistLoopPlace;

  const scrollToQuestion = useCallback((q: PaperAnswerQuestion) => {
    requestAnimationFrame(() => {
      const el = scrollerRef.current;
      if (!el) return;
      const target = el.querySelector<HTMLElement>(`[data-page="${q.pP}"]`);
      if (target) el.scrollTo({ top: target.offsetTop - 8 + target.clientHeight * Math.max(0, q.pY[0] - 0.02), behavior: 'smooth' });
    });
  }, []);

  const startLoop = useCallback(() => {
    setAttemptFirst(false); // Keep the student's default preference for next time.
    ensureAnswerMap();
    setSelfMarkOn(true);
    setAnswersOn(true);
    if (scheme && !sessions.current.scheme.pdf && !sessions.current.scheme.task) load('scheme');
    setSide('paper');
    setLoopDone(false);
    setReceiptSaved(false);
    loopStartedAtRef.current = Date.now();
    if (storageNs) clearLoopPlace(storageNs);
    setResumePlace(null);
    setPlaceSavedNote(false);
    setLoop({ idx: 0, qStartTs: Date.now() });
    setToolsOpen(false);
  }, [ensureAnswerMap, scheme, load, storageNs]);

  /** Resume a saved loop place — same warm-up as startLoop, but the index and
   *  the wall clock pick up where the student left off. */
  const resumeLoop = useCallback(() => {
    setAttemptFirst(false);
    const place = resumePlace;
    if (!place) return;
    ensureAnswerMap();
    setSelfMarkOn(true);
    setAnswersOn(true);
    if (scheme && !sessions.current.scheme.pdf && !sessions.current.scheme.task) load('scheme');
    setSide('paper');
    setLoopDone(false);
    setReceiptSaved(false);
    loopStartedAtRef.current = Date.now() - place.elapsedSec * 1000;
    if (storageNs) clearLoopPlace(storageNs);
    setPlaceSavedNote(false);
    // If the map is already in, clamp against its live length (the saved
    // total guards most drift; a re-generated shorter map is the edge case —
    // the clamp effect below covers a map that arrives after this tap).
    const liveTotal = loopQuestionsRef.current.length || undefined;
    const idx = liveTotal ? Math.min(place.idx, liveTotal - 1) : place.idx;
    setLoop({ idx, qStartTs: Date.now() });
    setResumePlace(null);
  }, [resumePlace, ensureAnswerMap, scheme, load, storageNs]);

  /** The mid-loop exit path (the ✕ on the loop bar): save the place quietly. */
  const exitLoopSavingPlace = useCallback(() => {
    persistLoopPlace();
    setLoop(null);
    if (storageNs) {
      setResumePlace(loadLoopPlace(storageNs, Date.now()));
      setPlaceSavedNote(true);
    }
  }, [persistLoopPlace, storageNs]);

  // The saved-place note is a brief, quiet line — it fades out on its own.
  useEffect(() => {
    if (!placeSavedNote) return;
    const id = setTimeout(() => setPlaceSavedNote(false), 4000);
    return () => clearTimeout(id);
  }, [placeSavedNote]);

  // A resumed index can outrun a re-generated (shorter) answer map that arrives
  // after the resume tap — clamp once the map is in.
  useEffect(() => {
    if (loop && loopQuestions.length > 0 && loop.idx >= loopQuestions.length) {
      setLoop({ idx: loopQuestions.length - 1, qStartTs: Date.now() });
    }
  }, [loop, loopQuestions]);

  // Mid-loop persistence: save on every loop step, and on tab close / bfcache
  // eviction while a loop is live. Unmount is covered separately below.
  useEffect(() => {
    if (!loop) return;
    persistLoopPlace();
    const save = () => persistLoopPlaceRef.current();
    window.addEventListener('pagehide', save);
    window.addEventListener('beforeunload', save);
    return () => {
      window.removeEventListener('pagehide', save);
      window.removeEventListener('beforeunload', save);
    };
  }, [loop, persistLoopPlace]);

  // Component unmount mid-loop (back out of the paper) saves the place too.
  useEffect(
    () => () => {
      persistLoopPlaceRef.current();
    },
    [],
  );

  // Jump to the current loop question once the map is in.
  useEffect(() => {
    if (!loop || !answerMap) return;
    const q = loopQuestions[loop.idx];
    if (q) scrollToQuestion(q);
  }, [loop, answerMap, loopQuestions, scrollToQuestion]);

  // Per-question elapsed readout, 1s cadence while the loop bar is showing.
  useEffect(() => {
    if (!loop) return;
    const id = setInterval(() => setLoopTick(t => t + 1), 1000);
    return () => clearInterval(id);
  }, [loop]);

  const loopNext = useCallback(() => {
    setReveal(null);
    setLoop(l => {
      if (!l || !answerMap) return l;
      if (l.idx + 1 >= loopQuestions.length) {
        // Finished: snapshot the wall clock for the receipt and retire the
        // saved place — a completed loop has nothing to resume.
        loopTotalSecRef.current = loopStartedAtRef.current
          ? Math.max(0, Math.round((Date.now() - loopStartedAtRef.current) / 1000))
          : 0;
        if (storageNs) clearLoopPlace(storageNs);
        setReceiptSaved(false);
        setLoopDone(true);
        return null;
      }
      return { idx: l.idx + 1, qStartTs: Date.now() };
    });
  }, [answerMap, loopQuestions, storageNs]);

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
        // Mark done only on success, so a failed warm (offline) retries next
        // tap. Routed through the CacheStorage layer so the full scheme lands
        // in BOTH the app cache and the SW cache for offline reveals.
        fetchPdfCached(scheme.url)
          .then(bytes => {
            if (bytes) schemePrefetched.current = true;
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
        const focusables = Array.from(rootRef.current.querySelectorAll<HTMLElement>(
          'button:not([disabled]), a[href], input:not([disabled]), select, textarea, [tabindex]:not([tabindex="-1"])',
        )).filter(el=>!el.closest('[hidden]') && el.getClientRects().length>0);
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
    let beforeResize: {side: Side; anchor: ZoomAnchor} | null = null;
    const onResize = () => {
      if (!resizeTimer) beforeResize = readingPoint.current;
      if (resizeTimer) clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        resizeTimer = null;
        const place = beforeResize;
        setEpoch(n => n + 1);
        requestAnimationFrame(() => {
          if (place && place.side === activeSideRef.current && scrollerRef.current) {
            restoreZoomAnchor(scrollerRef.current, place.anchor);
          }
        });
      }, 250);
    };
    window.addEventListener('resize', onResize);
    return () => {
      window.removeEventListener('keydown', onKey);
      window.removeEventListener('resize', onResize);
      if (resizeTimer) clearTimeout(resizeTimer);
    };
  }, []);

  // ── scroll → current page + persistence ──
  // The point being read on the paper, kept current so a change in the
  // paper column's width (the scheme panel opening) can hold it in place.
  const layoutAnchor = useRef<ZoomAnchor | null>(null);
  const onScroll = useCallback(() => {
    const el = scrollerRef.current;
    const s = sessions.current[side];
    if (!el || s.state !== 'ready') return;
    s.scrollTop = el.scrollTop;
    const anchor = captureZoomAnchor(el);
    if (anchor) readingPoint.current = {side, anchor};
    if (side === 'paper') layoutAnchor.current = anchor;
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

  // Topic Atlas navigation always checks the hosted paper-only sidecar. It may
  // carry a card absent from the richer Storage answer map, or corrected paper
  // coordinates for a card the Storage map already contains. In the latter
  // case merge only the audited paper extent; the Storage scheme crop remains
  // authoritative.
  useEffect(() => {
    if (!focusQuestion || !focusAnchorsUrl || focusAnchorStartedRef.current) return;
    if (answersUrl && answerState !== 'error' && !answerMap) return;
    let cancelled = false;
    focusAnchorStartedRef.current = true;
    fetch(focusAnchorsUrl)
      .then(response => (response.ok ? response.json() : Promise.reject(new Error('anchor fetch'))))
      .then((value: unknown) => {
        if (cancelled) return;
        if (isAnswerMap(value)) {
          const ordered = { ...value, q: questionsInDisplayOrder(value.q) };
          setFocusAnchorMap(ordered);
          setAnswerMap(current => current?.q.some(question => question.n === focusQuestion)
            ? mergePaperAnchorMetadata(current, ordered, focusQuestion)
            : current);
        }
        setFocusAnchorSettled(true);
      })
      .catch(() => { if (!cancelled) setFocusAnchorSettled(true); });
    return () => { cancelled = true; };
  }, [
    answerMap,
    answerState,
    answersUrl,
    focusAnchorMap,
    focusAnchorsUrl,
    focusQuestion,
  ]);

  // Once the paper + anchor map are ready, scroll to the focused question.
  const focusedRef = useRef(false);
  useEffect(() => {
    if (!focusQuestion || focusedRef.current || session.state !== 'ready') return;
    if (focusAnchorsUrl && !focusAnchorSettled) return;
    const q = answerMap?.q.find(x => x.n === focusQuestion)
      ?? focusAnchorMap?.q.find(x => x.n === focusQuestion);
    if (!q) return;
    focusedRef.current = true;
    requestAnimationFrame(() => {
      const el = scrollerRef.current;
      if (!el) return;
      const target = el.querySelector<HTMLElement>(`[data-page="${q.pP}"]`);
      if (target) el.scrollTo({ top: target.offsetTop - 8 + target.clientHeight * Math.max(0, q.pY[0] - 0.02) });
    });
  }, [focusQuestion, answerMap, focusAnchorMap, focusAnchorSettled, focusAnchorsUrl, session.state]);

  // Zoom resizes every page, so note the point being read before it and
  // scroll back to it once the new widths are laid out, before paint.
  const zoomAnchor = useRef<ZoomAnchor | null>(null);
  const zoomBy = (dir: 1 | -1) => {
    const i = ZOOM_STEPS.indexOf(zoom);
    const next = ZOOM_STEPS[Math.min(ZOOM_STEPS.length - 1, Math.max(0, i + dir))];
    if (next === zoom) return;
    zoomAnchor.current = scrollerRef.current ? captureZoomAnchor(scrollerRef.current) : null;
    setZoom(next);
  };
  useLayoutEffect(() => {
    const anchor = zoomAnchor.current;
    zoomAnchor.current = null;
    const el = scrollerRef.current;
    if (!anchor || !el) return;
    restoreZoomAnchor(el, anchor);
    onScroll();
  }, [zoom, onScroll]);

  const deskQuestions = useMemo(() => {
    const list = answerMap ? printedQuestionAnchors(answerMap.q) : [];
    const focused = focusQuestion && answerMap?.q.find(q => q.n === focusQuestion);
    if(!focused || list.some(q=>q.n===focused.n))return list;
    // A focused sub-question belongs in its physical place, so Next never
    // sends a student back to the first question of the paper.
    const after=list.findIndex(q=>q.pP>focused.pP || (q.pP===focused.pP && q.pY[0]>focused.pY[0]));
    const at=after<0 ? list.length : after;
    return [...list.slice(0,at),focused,...list.slice(at)];
  },[answerMap,focusQuestion]);
  const deskQuestion = deskQuestions.find(q => q.n === deskId);
  const pickDeskQuestion = (id:string) => {
    setDeskId(id);saveDeskQuestion(deskNs,id);setReveal(null);
    const q = deskQuestions.find(q => q.n === id);
    if(q)scrollToQuestion(q);
    else if(id.startsWith('page:'))jumpToPage(Number(id.slice(5)));
    requestAnimationFrame(()=>{
      const drawer=workspaceRef.current?.querySelector<HTMLElement>('.ad-pane');
      drawer?.scrollTo({top:0});
      drawer?.querySelector<HTMLSelectElement>('#answer-desk-question')?.focus({preventScroll:true});
    });
  };
  const deskInitialised = useRef(false);
  useEffect(() => {
    if(!attemptFirst || deskInitialised.current || session.state!=='ready' || !deskQuestions.length)return;
    deskInitialised.current=true;
    // Never move an attempt begun while the question map was loading.
    if(deskId.startsWith('page:') && hasResponse(deskRecord.draft))return;
    const selected=deskQuestions.find(q=>q.n===deskId)
      ?? deskQuestions.find(q=>q.pP===session.page)
      ?? [...deskQuestions].reverse().find(q=>q.pP<session.page) ?? deskQuestions[0];
    setDeskId(selected.n);saveDeskQuestion(deskNs,selected.n);
    if(session.page<selected.pP || (focusQuestion && selected.n===focusQuestion))scrollToQuestion(selected);
  },[attemptFirst,deskQuestions,deskId,deskNs,deskRecord.draft,session.state,session.page,focusQuestion,scrollToQuestion]);
  const toggleAttemptFirst = (on:boolean) => {
    if(scrollerRef.current)layoutAnchor.current=captureZoomAnchor(scrollerRef.current);
    if(loop)persistLoopPlace();
    setLoop(null);setLoopDone(false);setReveal(null);setAnswersOn(false);setToolsOpen(false);
    if(on)setSelfMarkOn(false);
    setAttemptFirst(on);
  };
  // Keep the same point on the paper while changing the drawer's footprint.
  const captureDeskPlace = () => {
    deskResizeAnchor.current=scrollerRef.current ? captureZoomAnchor(scrollerRef.current) : null;
  };
  const deskExtent = () => {
    const rect=workspaceRef.current?.getBoundingClientRect();
    return (isWide ? rect?.width : rect?.height) || (isWide ? window.innerWidth : window.innerHeight);
  };
  const deskBounds = (extent:number,wide:boolean) => ({
    min: Math.min(wide ? 320 : 160,extent*.45)/extent*100,
    max: Math.max(50,Math.min(wide ? 70 : 75,(extent-(wide ? 290 : 150))/extent*100)),
  });
  const resizeDesk = (percent:number,extent=deskExtent(),wide=isWide) => {
    const {min,max}=deskBounds(extent,wide);
    (wide ? setDeskWidth : setDeskHeight)(Math.max(min,Math.min(max,percent)));
  };
  const startDeskResize = (e:React.PointerEvent<HTMLDivElement>) => {
    if(e.button!==0)return;
    e.preventDefault();captureDeskPlace();
    const rect=workspaceRef.current?.getBoundingClientRect();
    if(!rect)return;
    deskDrag.current={pointer:e.pointerId,end:isWide ? rect.right : rect.bottom,extent:isWide ? rect.width : rect.height,wide:isWide};
    e.currentTarget.setPointerCapture(e.pointerId);setDeskResizing(true);
  };
  const moveDeskResize = (e:React.PointerEvent<HTMLDivElement>) => {
    const drag=deskDrag.current;
    if(!drag || drag.pointer!==e.pointerId || !drag.extent)return;
    resizeDesk((drag.end-(drag.wide ? e.clientX : e.clientY))/drag.extent*100,drag.extent,drag.wide);
  };
  const endDeskResize = () => {deskDrag.current=null;setDeskResizing(false);};
  const keyDeskResize = (e:React.KeyboardEvent<HTMLDivElement>) => {
    const grow=isWide ? 'ArrowLeft' : 'ArrowUp';
    const shrink=isWide ? 'ArrowRight' : 'ArrowDown';
    if(![grow,shrink,'Home','End','Enter'].includes(e.key))return;
    e.preventDefault();captureDeskPlace();
    if(e.key==='Enter'){setDeskCollapsed(true);requestAnimationFrame(()=>workspaceRef.current?.querySelector<HTMLButtonElement>('.ad-collapse')?.focus());return;}
    const extent=deskExtent(),bounds=deskBounds(extent,isWide);
    const value=deskSizePercent;
    resizeDesk(e.key==='Home' ? bounds.min : e.key==='End' ? bounds.max : value+(e.key===grow ? 1 : -1)*(e.shiftKey ? 50 : 20)/extent*100);
  };
  useLayoutEffect(() => {
    const el=scrollerRef.current;
    const anchor=deskResizeAnchor.current??layoutAnchor.current;
    if(el && anchor)restoreZoomAnchor(el,anchor);
    if(!deskResizing){deskResizeAnchor.current=null;setEpoch(n=>n+1);}
  },[attemptFirst,deskCollapsed,deskWidth,deskHeight,deskResizing]);
  const revealDesk = () => {
    book.change(deskId,keepFirstAttempt);
    if(deskQuestion)onReveal(deskQuestion);
    else if(scheme)setSide('scheme');
  };
  const deskSide = (next:Side) => {
    if(next==='scheme' && attemptFirst)book.change(deskId,keepFirstAttempt);
    setSide(next);
  };
  const editableInk = (r:AnswerRecord) => r.phase==='compare'?r.correctionInk:r.phase==='retry'||r.phase==='done'?r.retry.ink:r.draft.ink;
  const replaceInk = (r:AnswerRecord,page:number,strokes:InkStroke[]):AnswerRecord => r.phase==='compare'
    ? {...r,correctionInk:{...r.correctionInk,[page]:strokes}}
    : {...r,[r.phase==='retry'?'retry':'draft']:{...(r.phase==='retry'?r.retry:r.draft),ink:{...editableInk(r),[page]:strokes}}};
  const inkHistoryKey = (page:number) => `${deskId}|${deskRecord.phase}|${page}`;
  const pageInk = (page:number):AnswerInkProps => ({
    strokes:(deskRecord.phase==='done'&&inkView==='first'?deskRecord.first?.ink[page]:editableInk(deskRecord)[page])??[],
    base:deskRecord.phase==='compare'?deskRecord.first?.ink[page]:undefined,
    tool:inkTool, enabled:deskRecord.mode==='ink'&&deskRecord.phase!=='done',correction:deskRecord.phase==='compare',
    onChange:strokes=>{
      const key=inkHistoryKey(page);
      inkHistory.current[key]=[...(inkHistory.current[key]??[]).slice(-29),editableInk(deskRecord)[page]??[]];
      book.change(deskId,r=>replaceInk(r,page,strokes));
    },
  });
  const undoInk = () => {
    const previous=inkHistory.current[inkHistoryKey(session.page)]?.pop();
    if(previous)book.change(deskId,r=>replaceInk(r,session.page,previous));
  };

  const deskSizeBounds=deskBounds(deskExtent(),isWide);
  const deskSizePercent=Math.max(deskSizeBounds.min,Math.min(deskSizeBounds.max,isWide ? deskWidth : deskHeight));
  const inlineScheme = !attemptFirst && isWide && side === 'paper' && Boolean(answersOn || topicsOn || (reveal && isRoomy));
  // The scheme reads at panel width, so beside the paper it gets half the
  // screen (Oct 2026: a 360px panel set the answers at about 7px).
  const schemeBeside = inlineScheme && isRoomy && Boolean(reveal);
  const besideRef = useRef(schemeBeside);
  useLayoutEffect(() => {
    if (besideRef.current === schemeBeside) return;
    besideRef.current = schemeBeside;
    const el = scrollerRef.current;
    if (el && layoutAnchor.current) restoreZoomAnchor(el, layoutAnchor.current);
    setEpoch(n => n + 1); // pages re-render at the column's new width
  }, [schemeBeside]);

  // Step the open scheme through the paper's questions, bringing each
  // question into view beside it.
  const revealIndex = reveal ? loopQuestions.findIndex(x => x.n === reveal.n) : -1;
  const stepReveal = useCallback((dir: 1 | -1) => {
    const cur = revealRef.current;
    const list = loopQuestionsRef.current;
    const i = cur ? list.findIndex(x => x.n === cur.n) : -1;
    const next = i < 0 ? undefined : list[i + dir];
    if (!next) return;
    onReveal(next);
    scrollToQuestion(next);
  }, [onReveal, scrollToQuestion]);

  // The last question shown, so the phone sheet keeps its words while it leaves.
  const lastRevealRef = useRef<PaperAnswerQuestion | null>(null);
  if (reveal) lastRevealRef.current = reveal;
  const revealPanel = (q: PaperAnswerQuestion, open = true) => (
              <RevealContent
                q={q}
                wide={isWide}
                open={open}
                reduced={!!reducedMotion}
                schemePdf={sessions.current.scheme.pdf}
                schemeUrl={scheme?.url}
                schemeErrored={sessions.current.scheme.state === 'error' || sessions.current.scheme.state === 'unsupported'}
                copyright={answerMap?.copyright}
                selfMark={selfMarkOn}
                existingMark={attempt.marks?.[q.n]}
                licence={storageNs ? markerLicence(storageNs.split('|')[0]) : null}
                siblings={(() => {
                  if (!topics) return undefined;
                  const tag = topics.q.find(t => t.n === q.n);
                  if (!tag) return undefined;
                  return siblingsFor(topics.subjectId, tag.primary)
                    .filter(s => !(s.year === topics.year && s.level === topics.level && s.lang === topics.lang && s.fileid === topics.fileid))
                    .slice(0, 3);
                })()}
                onJumpSibling={s => { setReveal(null); onCrossYear?.(s); }}
                onRecordMark={m => recordMark(q.n, m)}
                onClose={() => setReveal(null)}
                onFullScheme={jumpSchemeToPage}
                onStep={!loop && revealIndex >= 0 ? stepReveal : undefined}
                canPrev={revealIndex > 0}
                canNext={revealIndex >= 0 && revealIndex < loopQuestions.length - 1}
              />
  );
  const schemeContent = reveal ? revealPanel(reveal) : null;

  // Answers map fetch status (chips appear once ready), as a runtime toast.
  useStatusToast(
    'pt-viewer-question-tools',
    (answersOn || topicsOn) && side === 'paper' && answerState !== 'idle'
      ? answerState === 'loading'
        ? { message: 'Loading question tools…', state: 'pending' }
        : { message: 'Couldn’t load question tools — try again later.', state: 'error' }
      : null,
  );
  // Text-scan status while the overlay tools read the paper.
  useStatusToast(
    'pt-viewer-text-scan',
    side === 'paper' && (paceOn || decodeOn) && scanState === 'loading' && !docTokens
      ? { message: 'Reading the paper…', state: 'pending' }
      : null,
  );

  // ── The bar's parts and Tools (boards c-papers-bar, r5-paper-viewer) ──
  // Answers is a black and white switch beside Paper or Scheme. On the scheme it
  // steps aside, as today; on a laptop it keeps its place so zoom and Tools stay put.
  const showAnswers = !attemptFirst && side === 'paper' && Boolean(answersUrl);
  const documentBar = scheme ? (
    <SelectionBar label="Paper or marking scheme" size="md" className="pv-document" value={side}
      onChange={next => deskSide(next)} options={[{ value: 'paper', label: 'Paper' }, { value: 'scheme', label: 'Scheme' }]} />
  ) : null;
  const answersSwitch = answersUrl ? (
    <label className="ui-switch-row pv-answers" hidden={(!isWide && !showAnswers) || undefined} data-ghost={isWide && !showAnswers ? '' : undefined}>
      <span>Answers</span>
      <Switch checked={answersOn} onChange={() => toggleAnswers()} label="Show the marking scheme beside each question"
        tabIndex={showAnswers ? undefined : -1} />
    </label>
  ) : null;
  const zoomControl = (
    <span className="pv-zoom" role="group" aria-label="Zoom">
      <IconButton label="Zoom out" aria-disabled={session.state !== 'ready' || zoom === ZOOM_STEPS[0] || undefined}
        onClick={() => { if (session.state === 'ready') zoomBy(-1); }}
        icon={<Minus className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" />} />
      <span className="ui-readout pv-zoom-value">{Math.round(zoom * 100)}%</span>
      <IconButton label="Zoom in" aria-disabled={session.state !== 'ready' || zoom === ZOOM_STEPS[ZOOM_STEPS.length - 1] || undefined}
        onClick={() => { if (session.state === 'ready') zoomBy(1); }}
        icon={<Plus className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" />} />
    </span>
  );
  // Go to page: today's page field, kept in Tools (the agreed bar shows the page
  // count as a readout only).
  const pageJump = (inMenu = false) => (
    <form className="pv-page-jump" aria-label="Page navigation" onSubmit={e => { e.preventDefault(); if (scrubbing != null) jumpToPage(Math.max(1, Math.min(session.numPages, scrubbing))); setScrubbing(null); }}>
      <input type="number" inputMode="numeric" min={1} max={session.numPages || 1} disabled={session.state !== 'ready'} value={scrubbing ?? session.page} aria-label="Go to page"
        // In the laptop menu the field is out of the tab order, so the menu opens
        // with its own focus, as drawn; it still takes a click and typing.
        tabIndex={inMenu ? -1 : undefined}
        onKeyDown={e => e.stopPropagation()}
        onChange={e => setScrubbing(e.target.value ? Number(e.target.value) : 1)}
        onBlur={() => { if (scrubbing != null) jumpToPage(Math.max(1, Math.min(session.numPages, scrubbing))); setScrubbing(null); }} />
      <span aria-hidden="true">/ {session.numPages || '—'}</span>
    </form>
  );
  type ToolEntry =
    | { kind: 'switch'; key: string; title: string; meta: string; on: boolean; toggle: () => void; close?: boolean }
    | { kind: 'open'; key: string; title: string; meta: string; onPress: () => void }
    | { kind: 'link'; key: string; title: string; meta: string; href: string };
  const fileWord = side === 'paper' ? 'paper' : 'scheme';
  const keep: ToolEntry[] = [
    ...(onSave ? [{ kind: 'switch' as const, key: 'save', title: 'Save this paper', meta: 'Keeps it in Saved papers', on: saved, toggle: onSave }] : []),
    { kind: 'link', key: 'download', title: `Download the ${fileWord}`, meta: `Opens in your browser · PDF${activeDoc.bytes ? ` · ${prettyBytes(activeDoc.bytes)}` : ''}`, href: activeDoc.url },
  ];
  const switchOn: ToolEntry[] = [
    { kind: 'switch', key: 'attempt', title: 'Attempt first', meta: 'Write your answer before the scheme shows', on: attemptFirst, toggle: () => toggleAttemptFirst(!attemptFirst), close: true },
    ...(side === 'paper' ? [
      ...(answersUrl && scheme && storageNs ? [{ kind: 'switch' as const, key: 'self', title: 'Self-mark', meta: 'Score yourself against the scheme', on: selfMarkOn, toggle: toggleSelfMark, close: true }] : []),
      { kind: 'switch' as const, key: 'decode', title: 'Command words', meta: 'Decode what each question demands', on: decodeOn, toggle: () => toggleTool('decode') },
      ...(topics ? [{ kind: 'switch' as const, key: 'topics', title: 'Topics & frequency', meta: 'How often each topic comes up', on: topicsOn, toggle: toggleTopics }] : []),
      ...(timing ? [{ kind: 'switch' as const, key: 'exam', title: 'Exam mode', meta: `Clock set to ${timing.totalMinutes} min`, on: examOn, close: true, toggle: () => {
        setExamOn(v => {
          const next = !v;
          setRunning(next);
          if (next) setElapsed(0);
          return next;
        });
        setToolsOpen(false);
      } }] : []),
    ] : []),
  ];
  const start: ToolEntry[] = side === 'paper' ? [
    ...(answersUrl && storageNs ? [{ kind: 'open' as const, key: 'triage', title: 'Triage', meta: 'Rate each question before you start', onPress: openTriage }] : []),
    ...(answersUrl && scheme && storageNs ? [{ kind: 'open' as const, key: 'loop', title: 'The Full Loop', meta: resumePlace ? `Resume at question ${resumePlace.idx + 1}` : 'Question by question: attempt, reveal, mark', onPress: resumePlace ? resumeLoop : startLoop }] : []),
    ...(formulae ? [{ kind: 'open' as const, key: 'formulae', title: 'Formulae & Tables', meta: 'Jump to the booklet section', onPress: openFormulae }] : []),
  ] : [];
  const onCount = switchOn.filter(entry => entry.kind === 'switch' && entry.on).length;
  const scanNote = scanState === 'error' && side === 'paper'
    ? <p className="pv-tools-note">Couldn’t read this paper’s text layer — overlays unavailable.</p> : null;
  // On a phone: rows in a sheet. A switch turns a thing on; a row with a chevron opens it.
  const sheetRow = (entry: ToolEntry) => entry.kind === 'switch'
    ? <li key={entry.key} className="ui-row-item">
        <label className="ui-part ui-row pv-switch-row">
          <span className="ui-row-body"><span className="ui-row-title">{entry.title}</span><span className="ui-row-meta">{entry.meta}</span></span>
          <Switch checked={entry.on} onChange={() => entry.toggle()} label={entry.title} />
        </label>
      </li>
    : entry.kind === 'link'
      ? <Row key={entry.key} external href={entry.href} title={entry.title} meta={entry.meta} />
      : <Row key={entry.key} title={entry.title} meta={entry.meta} onPress={entry.onPress} />;
  const toolsList = (
    <div className="pv-tools">
      <List label="This paper">
        <Row title="Zoom" trailing={zoomControl} />
        <Row title="Go to page" trailing={pageJump()} />
        {keep.map(sheetRow)}
      </List>
      <p className="t-label pv-tools-label">Switch on</p>
      <List label="Switch on">{switchOn.map(sheetRow)}</List>
      {start.length > 0 && <><p className="t-label pv-tools-label">Start</p><List label="Start">{start.map(sheetRow)}</List></>}
      {scanNote}
    </div>
  );
  // On a laptop: the same list as a menu under its button; zoom stays in the bar.
  const menuRow = (entry: ToolEntry) => entry.kind === 'switch'
    ? <MenuSwitch key={entry.key} title={entry.title} meta={entry.meta} checked={entry.on} onChange={() => entry.toggle()} closeOnClick={entry.close} />
    : entry.kind === 'link'
      ? <MenuAction key={entry.key} title={entry.title} meta={entry.meta} href={entry.href} />
      : <MenuAction key={entry.key} title={entry.title} meta={entry.meta} onPress={entry.onPress} />;
  const toolsMenu = (
    <MenuPanel label="Tools" buttonLabel="Study tools for this paper" className="pv-tools-btn" open={toolsOpen} onOpenChange={setToolsOpen}
      face={<><SlidersHorizontal className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" />Tools</>}
      head="Tools" status={onCount > 0 ? `${onCount} on` : undefined}>
      {keep.map(menuRow)}
      <div className="pv-page-row"><span className="ui-menu-item-title">Go to page</span>{pageJump(true)}</div>
      <MenuLabel>Switch on</MenuLabel>
      {switchOn.map(menuRow)}
      {start.length > 0 && <><MenuLabel>Start</MenuLabel>{start.map(menuRow)}</>}
      {scanNote}
    </MenuPanel>
  );
  const toolsButton = (
    <IconButton label="Study tools for this paper" onClick={() => setToolsOpen(true)}
      icon={<SlidersHorizontal className="ui-icon" width={24} height={24} strokeWidth={1.75} aria-hidden="true" focusable="false" />} />
  );

  // ── render ──
  return createPortal(
    <div
      ref={rootRef}
      data-lenis-prevent
      className="pv-root fixed inset-0 z-[100] flex flex-col"
      role="dialog"
      aria-modal="true"
      aria-label={`${title} — document viewer`}
    >
      {/* The bar (c-papers-bar, r5-paper-viewer): on a phone two rows, Close, the
          paper's name and Tools, then Paper or Scheme beside the Answers switch;
          on a laptop one line, Close and the name, Paper or Scheme in the
          middle, then Answers, zoom and Tools. The viewer comes up over Paper
          Trail: its one way out is Close, top left, back to exactly where you were. */}
      <div ref={headerRef} tabIndex={-1} className="pv-top">
        <TopBar ruled className="pv-bar"
          leave={{ kind: 'close', onPress: () => onCloseRef.current(), label: 'Close viewer' }}
          over={barOver ?? subtitle} title={barName ?? title}
          center={isWide && documentBar ? documentBar : undefined}
          action={isWide ? <div className="pv-actions">{answersSwitch ?? <span />}{zoomControl}{toolsMenu}</div> : toolsButton}
          below={!isWide && (documentBar || answersSwitch) ? <>{documentBar}{answersSwitch}</> : undefined} />
      </div>

      {audioSource && <div className="shrink-0 bg-[var(--surface-canvas)] border-b border-[var(--hairline)]">
        <div className="max-w-3xl mx-auto"><FrenchPaperAudio source={audioSource} /></div>
      </div>}
      <div ref={workspaceRef} className="pt-reader-workspace" style={{'--ad-size':`${deskSizePercent}%`} as React.CSSProperties} data-resizing={deskResizing||undefined} data-attempt={attemptFirst && side==='paper' || undefined} data-split={inlineScheme || undefined}>
      {/* Body */}
      <div className="pv-doc">
      {session.state === 'ready' && session.pdf ? (
        <div
          ref={attachScroller}
          onScroll={onScroll}
          className="pv-scroller relative flex-1 overflow-auto overscroll-contain"
          aria-label={`${activeDoc.label}, page ${session.page} of ${session.numPages}`}
        >
          <p className="sr-only">
            This document is shown as page images. For a screen-reader-friendly copy, use
            “Download the {side === 'paper' ? 'paper' : 'scheme'}” in Tools.
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
                anchors={isWide && (answersOn || topicsOn) && side === 'paper' ? anchorsByPage.get(i + 1) : undefined}
                showAnswerChip={!attemptFirst && answersOn}
                answerInk={attemptFirst && side==='paper' ? pageInk(i+1) : undefined}
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
          <p className="pv-copyright">© State Examinations Commission</p>
        </div>
      ) : session.state === 'loading' ? (
        <div className="pv-state">
          <Spinner />
          <p className="t-meta">
            Opening {side === 'paper' ? 'the paper' : 'the marking scheme'}…
            {activeDoc.bytes ? ` ${prettyBytes(activeDoc.bytes)}` : ''}
          </p>
          <a href={activeDoc.url} target="_blank" rel="noopener noreferrer" className="ui-part ui-link ui-link--quiet">
            <span>Taking too long? Open in browser</span>
          </a>
        </div>
      ) : (
        <div className="pv-state">
          <p className="pv-state-title">
            {session.state === 'unsupported'
              ? 'This phone can’t show PDFs inside the app.'
              : session.httpStatus != null
                ? 'The paper archive is temporarily unavailable.'
                : 'That didn’t load.'}
          </p>
          <p className="t-sub max-w-sm">
            {session.state === 'unsupported'
              ? 'No problem — the document will open in your browser instead.'
              : session.httpStatus != null
                ? 'The problem is on our side — not your connection or your phone. Please try again in a little while.'
                : 'It might be the connection. Try again, or open it in your browser.'}
          </p>
          <div className="pv-state-actions">
            {session.state === 'error' && (
              <UiButton kind="main" onClick={() => load(side)}>Try again</UiButton>
            )}
            {/* When the server itself refused (402/403/…), the same URL is just
                as dead in a browser tab — offering it would be a dead link. */}
            {session.httpStatus == null && (
              <a href={activeDoc.url} target="_blank" rel="noopener noreferrer" className="ui-part ui-btn">
                <span>Open in browser</span>
              </a>
            )}
          </div>
        </div>
      )}
      {session.state === 'ready' && session.numPages > 0 && !(loop && answerMap) && !(resumePlace && !loop && !loopDone && side === 'paper') && (
        <div className="pv-pos ui-readout" aria-hidden="true">{String(session.page).padStart(2, '0')} / {String(session.numPages).padStart(2, '0')}</div>
      )}
      <span className="sr-only" role="status">Page {session.page} of {session.numPages}</span>
      {/* Exam-mode clock: over the paper, above the page count, clear of the panels below it. */}
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
      </div>

      {(!attemptFirst || topicsOn) && !isWide && side === 'paper' && session.state === 'ready' && answerMap && (answersOn || topicsOn) && (
        <MobileQuestionTools
          page={session.page}
          initialQuestion={focusQuestion}
          questions={anchorsByPage.get(session.page) ?? []}
          topicInfo={topicsOn ? topicInfoByN : undefined}
          showAnswers={answersOn}
          onAnswer={onReveal}
          onTopic={onTopic}
        />
      )}

      {attemptFirst && side==='paper' && !deskCollapsed && <div
        className="ad-resize" role="separator" tabIndex={0} aria-label="Resize answer desk"
        aria-orientation={isWide ? 'vertical' : 'horizontal'} aria-controls="paper-answer-drawer"
        aria-valuenow={Math.round(deskSizePercent)}
        aria-valuemin={Math.round(deskSizeBounds.min)} aria-valuemax={Math.round(deskSizeBounds.max)}
        aria-valuetext={`${Math.round(deskSizePercent)} percent of the workspace`}
        title="Drag to resize. Use arrow keys for smaller adjustments, or double-click to reset."
        onPointerDown={startDeskResize} onPointerMove={moveDeskResize} onPointerUp={endDeskResize} onPointerCancel={endDeskResize}
        onKeyDown={keyDeskResize} onDoubleClick={()=>{captureDeskPlace();resizeDesk(isWide ? 43 : 49);}}
      ><span/></div>}
      {attemptFirst && side==='paper' && <AnswerDesk title={title} id={deskId} questions={deskQuestions} page={session.page} record={deskRecord} problem={book.problem(deskId)} onChange={update=>book.change(deskId,update)} onQuestion={pickDeskQuestion} onReveal={revealDesk} onHide={()=>setReveal(null)} schemeVisible={reveal?.n===deskId} hasScheme={!!scheme} schemePdf={sessions.current.scheme.pdf} schemeErrored={sessions.current.scheme.state==='error'||sessions.current.scheme.state==='unsupported'} onRetryScheme={()=>load('scheme')} onFullScheme={()=>jumpSchemeToPage(deskQuestion?schemeRegionFor(deskQuestion)[0]?.p??1:1)} inkView={inkView} onInkView={setInkView} tool={inkTool} onTool={setInkTool} onUndo={undoInk} canUndo={!!inkHistory.current[inkHistoryKey(session.page)]?.length} wide={isWide} collapsed={deskCollapsed} onCollapse={()=>{captureDeskPlace();setDeskCollapsed(v=>!v);}} />}

      {inlineScheme && <aside className="pt-reader-sidebar" data-scheme-open={schemeBeside || undefined} aria-label="Question workspace">
        {/* Hidden, not unmounted, while a scheme is open, so the question
            picker keeps its place for when the scheme closes. */}
        <div hidden={schemeBeside}>
          <div className="pt-reader-sidebar-heading"><h2>Question workspace</h2><p>Keep the question in view while you explore its scheme.</p></div>
          {answerMap && session.state === 'ready' && <MobileQuestionTools page={session.page} initialQuestion={focusQuestion} questions={anchorsByPage.get(session.page) ?? []} topicInfo={topicsOn ? topicInfoByN : undefined} showAnswers={answersOn} onAnswer={onReveal} onTopic={onTopic} />}
        </div>
        {schemeBeside && schemeContent}
      </aside>}
      </div>
      {/* Status toasts and notices, where the floating status pills sat. */}
      <KobraScope className="nsu-paper-viewer">
        <div className="pvc-toasts">
          <Toasts position="bottom-center" />
        </div>
        {/* Scanned paper (no text layer) — explain why overlays are absent. Too
            long for a one-line toast, so it is the house hairline notice. */}
        {side === 'paper' && (paceOn || decodeOn) && scanState === 'idle' && docTokens && !hasAnyTokens && (
          <Alert variant="info" role="status" aria-live="polite" className="pvc-notice">
            <AlertDescription>
              This paper is a scanned image — its text can’t be read for on-paper tools.
            </AlertDescription>
          </Alert>
        )}
      </KobraScope>

      {/* Tools on a phone: a sheet from the bottom (c-papers-bar, "Agreed · Tools"). */}
      <Sheet open={toolsOpen && !isWide} onClose={() => setToolsOpen(false)} title="Tools" titleAlign="start"
        status={onCount > 0 ? <span className="pv-on-count">{onCount} on</span> : undefined} className="pv-tools-sheet">
        {toolsList}
      </Sheet>

      {/* Cross-year topic sheet — every sibling question for this subtopic. */}
      <Sheet open={Boolean(topicReveal && topics)} onClose={() => setTopicReveal(null)} titleAlign="start"
        title={topicReveal ? topicLabel(topicReveal.subtopicId) : ''}>
        {topicReveal && topics && (
          <TopicContent
            subtopicId={topicReveal.subtopicId}
            subjectId={topics.subjectId}
            current={{ year: topics.year, level: topics.level, lang: topics.lang, fileid: topics.fileid, n: topicReveal.n }}
            onJump={s => {
              setTopicReveal(null);
              onCrossYear?.(s);
            }}
          />
        )}
      </Sheet>

      {/* Per-question marking-scheme reveal: on a phone the shared Sheet; from 768px a tray
          at the right over the paper; from 1100px it sits beside the paper (above). */}
      {!isWide && !attemptFirst && lastRevealRef.current && revealPanel(lastRevealRef.current, Boolean(reveal))}
      <AnimatePresence>
        {isWide && !attemptFirst && reveal && !schemeBeside && (
          <>
            <MotionDiv
              key="reveal-backdrop"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              onClick={() => setReveal(null)}
              className="pv-reveal-scrim fixed inset-0 z-[110]"
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
              className="pv-reveal-tray frame-page fixed top-0 right-0 z-[111] h-full w-[min(720px,calc(100vw-48px))] flex flex-col"
            >
              {schemeContent}
            </MotionDiv>
          </>
        )}
      </AnimatePresence>

      {/* The Full Loop bar (PT-2) — sequences attempt → reveal → mark → next. On a phone it is
          pinned at the foot, under the question panel; on a laptop it floats over the paper. */}
      {loop && answerMap && !reveal && (() => {
        const q = loopQuestions[loop.idx];
        if (!q) return null;
        void loopTick; // 1s cadence re-render for the elapsed readout
        const marked = attempt.marks?.[q.n] !== undefined;
        const secs = Math.max(0, Math.floor((Date.now() - loop.qStartTs) / 1000));
        const mm = Math.floor(secs / 60);
        const ss = String(secs % 60).padStart(2, '0');
        return (
          <div className="pv-loop" data-place="bar">
            <div className="pv-loop-copy">
              <p className="t-label pv-loop-label">
                The full loop · <span className="ui-readout">{loop.idx + 1} of {loopQuestions.length}</span>
              </p>
              <p className="pv-loop-name">
                {q.label ?? `Question ${q.n}`}
              </p>
            </div>
            <span className="ui-readout pv-loop-time">{mm}:{ss}</span>
            {/* Ending the loop is said in words, not an X: the viewer's Close is the screen's one leave
                control (navigation.md; area 9). The words are the start of its name. */}
            <TextButton tone="quiet" className="pv-loop-end" aria-label="End the loop — your place is saved" onClick={exitLoopSavingPlace}>
              End the loop
            </TextButton>
            {marked ? (
              <UiButton kind="main" size="lg" block arrow={loop.idx + 1 >= loopQuestions.length ? undefined : 'forward'} onClick={loopNext}>
                {loop.idx + 1 >= loopQuestions.length ? 'Finish' : 'Next'}
              </UiButton>
            ) : (
              <UiButton kind="main" size="lg" block onClick={() => onReveal(q)}>
                Reveal & mark
              </UiButton>
            )}
          </div>
        );
      })()}

      {/* Full Loop resume card — a saved place from a previous mid-loop exit. */}
      {!attemptFirst && resumePlace && !loop && !loopDone && !reveal && side === 'paper' && answersUrl && scheme && storageNs && (
        <div className="pv-loop pv-loop--resume" data-place="resume">
          <div className="pv-loop-head">
            <div className="pv-loop-copy">
              <p className="t-label pv-loop-label">The full loop</p>
              <p className="pv-loop-say">
                You were on question {resumePlace.idx + 1} of {resumePlace.total} — pick up where you left off.
              </p>
              {placeSavedNote && (
                <p className="pv-loop-saved">
                  Your place is saved.
                </p>
              )}
            </div>
            <TextButton tone="quiet" className="pv-loop-end" aria-label="Dismiss — keep the place saved for next time" onClick={() => setResumePlace(null)}>
              Dismiss
            </TextButton>
          </div>
          <div className="ui-pair">
            <UiButton kind="main" size="lg" onClick={resumeLoop}>
              Resume
            </UiButton>
            <UiButton size="lg" onClick={startLoop}>
              Start over
            </UiButton>
          </div>
        </div>
      )}

      {/* Full Loop summary — the session in the student's own marks, on the shared Sheet. Its
          own choices are its way out: Save image and Done. */}
      {(() => {
        if (!answerMap) return null;
        const qs = loopQuestions;
        const marks = qs.map(q => attempt.marks?.[q.n]).filter((m): m is SelfMark => !!m);
        const avg = marks.length ? Math.round(marks.reduce((a, m) => a + (m.max ? (m.score / m.max) * 100 : m.score), 0) / marks.length) : 0;
        const gapCounts = new Map<GapKind, number>();
        for (const m of marks) if (m.gap) gapCounts.set(m.gap, (gapCounts.get(m.gap) ?? 0) + 1);
        const topGap = [...gapCounts.entries()].sort((a, b) => b[1] - a[1])[0];
        const gapLabel: Record<GapKind, string> = { content: 'not knowing it', process: 'the wrong method', careless: 'careless slips', timing: 'the clock' };
        // The receipt — anonymous by construction (no name, no uid).
        const receiptStats: LoopReceiptStats = {
          dateIso: new Date().toISOString().slice(0, 10),
          paperTitle: title,
          ...(subtitle ? { paperDetail: subtitle } : {}),
          questionsWorked: marks.length,
          questionsTotal: qs.length,
          totalSec: loopTotalSecRef.current,
          avgPct: marks.length ? avg : null,
          gaps: Object.fromEntries(gapCounts) as Partial<Record<GapKind, number>>,
        };
        const receipt = composeReceipt(receiptStats);
        return (
          <Sheet open={loopDone} plain title="The full loop · done" onClose={() => setLoopDone(false)} className="pv-summary"
            footer={
              <div className="ui-pair">
                <UiButton size="lg" onClick={() => { if (downloadReceipt(receiptStats)) setReceiptSaved(true); }}>
                  {receiptSaved ? 'Saved' : 'Save image'}
                </UiButton>
                <UiButton kind="main" size="lg" onClick={() => setLoopDone(false)}>
                  Done
                </UiButton>
              </div>
            }>
            <p className="pv-summary-score">
              {marks.length ? <><span>{avg}</span><span className="pv-summary-unit">%</span></> : '—'}
            </p>
            <p className="t-sub">
              {marks.length} of {qs.length} questions self-marked against the real scheme.
            </p>
            {topGap && (
              <p className="pv-summary-note">
                Most marks died to {gapLabel[topGap[0]]} ({topGap[1]}×) — your dashboard's autopsy has the fix.
              </p>
            )}
            {/* The receipt — the session's numbers, saveable as an image. */}
            <div className="pv-receipt">
              <div className="pv-receipt-head">
                <span className="t-label">Receipt</span>
                <span className="ui-readout">{receipt.date}</span>
              </div>
              {receipt.rows.map(r => (
                <div key={r.label} className="pv-receipt-row">
                  <span>{r.label}</span>
                  <span>{r.value}</span>
                </div>
              ))}
            </div>
          </Sheet>
        );
      })()}

      {/* Handwriting-speed calibrator (F4) — opened from the tools menu or the
          pace footer line; result feeds straight back into the minute budgets. */}
      {calibratorOpen && (
        <WpmCalibrator uid={wpmUid} onSaved={setWpmCal} onClose={() => setCalibratorOpen(false)} />
      )}

      {/* Command-word decoder, on the shared Sheet. */}
      <Sheet open={Boolean(commandReveal)} onClose={() => setCommandReveal(null)} titleAlign="start"
        title={commandReveal ? `“${commandReveal.entry.word}”` : ''}>
        {commandReveal && <CommandContent token={commandReveal} />}
      </Sheet>

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
                  ? 'frame-page fixed top-0 right-0 z-[111] h-full w-full max-w-md flex flex-col bg-white dark:bg-surface-paper shadow-2xl border-l border-zinc-200 dark:border-hairline'
                  : 'fixed bottom-0 inset-x-0 z-[111] max-h-[85vh] flex flex-col bg-white dark:bg-surface-paper rounded-t-2xl shadow-2xl'
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
                  ? 'frame-page fixed top-0 right-0 z-[111] h-full w-full max-w-md flex flex-col bg-white dark:bg-surface-paper shadow-2xl border-l border-zinc-200 dark:border-hairline'
                  : 'fixed bottom-0 inset-x-0 z-[111] max-h-[85vh] flex flex-col bg-white dark:bg-surface-paper rounded-t-2xl shadow-2xl'
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

      {/* Triage — plan-your-attack ratings over the question list, on the shared Sheet. */}
      <Sheet open={triageOpen} onClose={() => setTriageOpen(false)} title="Triage — plan your attack" titleAlign="start">
        <TriageContent
          questions={answerMap?.q ?? null}
          loading={answerState === 'loading'}
          ratings={attempt.triage ?? {}}
          minsPerMark={minsPerMark}
          onRate={rateTriage}
          onJump={n => {
            const q = answerMap?.q.find(x => x.n === n);
            setTriageOpen(false);
            if (attemptFirst && q) {setDeskId(n);saveDeskQuestion(deskNs,n);setReveal(null);}
            if (q) requestAnimationFrame(() => {
              const el = scrollerRef.current;
              const target = el?.querySelector<HTMLElement>(`[data-page="${q.pP}"]`);
              if (el && target) el.scrollTo({ top: target.offsetTop - 8 + target.clientHeight * Math.max(0, q.pY[0] - 0.02) });
            });
          }}
        />
      </Sheet>

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
              className={isWide ? 'frame-page fixed top-0 right-0 z-[111] h-full w-full max-w-md flex flex-col bg-white dark:bg-surface-paper shadow-2xl border-l border-zinc-200 dark:border-hairline' : 'fixed bottom-0 inset-x-0 z-[111] max-h-[85vh] flex flex-col bg-white dark:bg-surface-paper rounded-t-2xl shadow-2xl'}
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
      <div className="shrink-0 flex items-center gap-2 px-4 py-3 border-b border-zinc-200 dark:border-hairline">
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
            className="flex items-center justify-between gap-2 rounded-xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-surface-paper px-3 py-3 text-left transition-transform active:translate-y-0.5"
          >
            <span className="text-[13px] font-semibold leading-tight" style={{ color: '#1a1a1a' }}>{s.label}</span>
            <BookOpen size={14} style={{ color: COLORS.accent }} className="shrink-0" />
          </a>
        ))}
      </div>
      <p className="shrink-0 px-4 py-2 text-[10px] text-zinc-400 border-t border-zinc-200 dark:border-hairline">
        Formulae and Tables © State Examinations Commission.
      </p>
    </>
  );
};

// ─── triage (plan your attack) ──────────────────────────────

const TRIAGE_OPTS: { r: TriageRating; label: string }[] = [
  { r: 'g', label: 'Confident' },
  { r: 'a', label: 'Unsure' },
  { r: 'r', label: 'Hard' },
];

/** Triage on the shared Sheet: each question, then Confident / Unsure / Hard as a
 *  selection bar (choosing the chosen one again clears it, as before). */
const TriageContent: React.FC<{
  questions: PaperAnswerQuestion[] | null;
  loading: boolean;
  ratings: Record<string, TriageRating>;
  minsPerMark: number | null;
  onRate: (n: string, rating: TriageRating | null) => void;
  onJump: (n: string) => void;
}> = ({ questions, loading, ratings, minsPerMark, onRate, onJump }) => {
  const counts = { g: 0, a: 0, r: 0 };
  for (const q of questions ?? []) {
    const rt = ratings[q.n];
    if (rt) counts[rt]++;
  }
  const rated = counts.g + counts.a + counts.r;
  return (
    <>
      <p className="pv-sheet-sub">Rate each question before you start. Do your confident ones first.</p>
      {rated > 0 && (
        <p className="pv-tally"><span>{counts.g} confident</span><span>{counts.a} unsure</span><span>{counts.r} hard</span></p>
      )}
      {!questions && loading && (
        <div role="status" className="pv-state" style={{ padding: '40px 0' }}>
          <Spinner />
          <span className="t-meta">Loading the question list…</span>
        </div>
      )}
      {questions?.map(q => {
        const rt = ratings[q.n];
        const name = q.label ?? `Question ${q.n}`;
        return (
          <div key={q.n} className="pv-triage-q">
            <TextButton onClick={() => onJump(q.n)}>{name}</TextButton>
            <SelectionBar label={`How sure are you of ${name}?`} value={rt ?? ''}
              onChange={next => onRate(q.n, next === rt ? null : next)}
              options={TRIAGE_OPTS.map(opt => ({ value: opt.r, label: opt.label }))} />
          </div>
        );
      })}
      {rated > 0 && (
        <p className="pv-sheet-foot">
          Plan: bank the <b>{counts.g} confident</b>{minsPerMark ? '' : ''} first, then the {counts.a} unsure, and leave the {counts.r} hard for last.
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
      <div className="shrink-0 flex items-center gap-2 px-4 py-3 border-b border-zinc-200 dark:border-hairline">
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
          <div key={i} className="rounded-xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-surface-paper px-3.5 py-3">
            <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-1" style={{ color: '#9e9186' }}>Where marks are lost</p>
            <p className="text-[13px] leading-relaxed mb-2.5" style={{ color: '#3a3530' }}>{ins.pitfall}</p>
            <div className="rounded-lg px-3 py-2 mb-1.5" style={{ backgroundColor: '#E8F2EC', borderLeft: '3px solid #3A8D5F' }}>
              <p className="text-[12.5px] leading-relaxed" style={{ color: '#1F5F3E' }}>{ins.fix}</p>
            </div>
            <p className="text-[10.5px] italic" style={{ color: '#9e9186' }}>{ins.cite}</p>
          </div>
        ))}
      </div>
      <p className="shrink-0 px-4 py-2 text-[10px] text-zinc-400 border-t border-zinc-200 dark:border-hairline">
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
  // Floating over the paper: Close at its left, the time in the pixel mono, a thin track, pause and reset.
  return (
    <div className="pv-clock" role="timer" aria-live="off" data-over={over || undefined}>
      <div className="pv-clock-read">
        <span className="ui-readout pv-clock-time">
          {over ? `+${fmtClock(-remaining)}` : fmtClock(remaining)}
        </span>
        <span className="pv-clock-label">
          {over ? 'over time' : 'remaining'}
        </span>
      </div>
      <span className="pv-clock-track" aria-hidden><i style={{ width: `${frac * 100}%` }} /></span>
      <IconButton label={running ? 'Pause timer' : 'Start timer'} onClick={onToggle}
        icon={running ? <Pause className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" />
          : <Play className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" />} />
      <IconButton label="Reset timer" onClick={onReset}
        icon={<RotateCcw className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" />} />
      {/* Said in words at the end, not an X at the start: the viewer's Close is the screen's one leave
          control (navigation.md; area 9, as the Full Loop's bar). The name is unchanged. */}
      <TextButton tone="quiet" className="pv-clock-close" aria-label="Close exam mode" onClick={onClose}>Close</TextButton>
    </div>
  );
};

// ─── status toasts ──────────────────────────────────────────

type StatusToast = { message: string; state: 'pending' | 'error' | 'info' };
/** setTimeout's ceiling: a settled status stays until it clears. */
const UNTIL_CLEARED = 2 ** 31 - 1;

/** Reports a viewer status through the runtime toast, where the floating
 *  status pill used to be: shown while the status holds, then let go once it
 *  clears, as the pill went with its condition. */
function useStatusToast(id: string, status: StatusToast | null) {
  const shown = useRef<string | null>(null);
  const message = status?.message;
  const state = status?.state;
  useEffect(() => {
    if (message && state) {
      shown.current = message;
      toast(state === 'pending' ? { id, message, state } : { id, message, state, lifetime: UNTIL_CLEARED });
    } else if (shown.current) {
      // Same toast, no state: it drops its mark and leaves.
      toast({ id, message: shown.current, lifetime: 200 });
      shown.current = null;
    }
  }, [id, message, state]);
}

// ─── command-word decoder content (on the shared Sheet) ─────

const CommandContent: React.FC<{ token: CommandToken }> = ({ token }) => {
  const { entry, matched } = token;
  const alias = matched.toLowerCase() !== entry.word.toLowerCase();
  return (
    <>
      <p className="pv-sheet-sub">{alias ? `seen as “${matched}” · ` : ''}Command word · {entry.typicalMarkRange}</p>
      <div className="pv-sheet-section">
        <p className="t-label">What it asks</p>
        <p className="pv-sheet-text">{entry.requiredAction}</p>
      </div>
      <div className="pv-sheet-section">
        <p className="t-label">How to structure it</p>
        <p className="pv-sheet-text">{entry.structuralTemplate}</p>
      </div>
      <div className="pv-sheet-section">
        <p className="t-label">Where students lose marks</p>
        <p className="pv-sheet-text">{entry.commonError}</p>
      </div>
    </>
  );
};

// ─── cross-year topic content (on the shared Sheet) ─────────

const LVL_ABBR: Record<string, string> = { higher: 'HL', ordinary: 'OL', foundation: 'FL', common: 'CL' };
const paperAbbr = (k: string) => (k === 'p1' ? 'P1' : k === 'p2' ? 'P2' : '');

const TopicContent: React.FC<{
  subtopicId: string;
  subjectId: string;
  current: { year: number; level: string; lang: string; fileid: string; n: string };
  onJump: (s: TopicSibling) => void;
}> = ({ subtopicId, subjectId, current, onJump }) => {
  const siblings = useMemo(() => siblingsFor(subjectId, subtopicId), [subjectId, subtopicId]);
  const years = new Set(siblings.map(s => s.year));
  const isCurrent = (s: TopicSibling) =>
    s.year === current.year && s.level === current.level && s.lang === current.lang && s.fileid === current.fileid && s.n === current.n;
  return (
    <>
      <p className="pv-sheet-sub">
        {siblings.length} question{siblings.length === 1 ? '' : 's'} across {years.size} tagged year{years.size === 1 ? '' : 's'} — tap to drill it
      </p>
      <List label={`${topicLabel(subtopicId)} across the years`}>
        {siblings.map(s => {
          const here = isCurrent(s);
          const detail = `${LVL_ABBR[s.level] ?? s.level}${paperAbbr(s.paperKey) ? ` · ${paperAbbr(s.paperKey)}` : ''}${s.lang === 'iv' ? ' · Gaeilge' : ''} · Question ${s.n}`;
          return (
            <Row
              key={`${s.year}-${s.level}-${s.lang}-${s.fileid}-${s.n}`}
              title={String(s.year)}
              meta={detail}
              trailing={here ? <span className="pv-here">you’re here</span> : undefined}
              onPress={here ? undefined : () => onJump(s)}
            />
          );
        })}
      </List>
      <p className="pv-sheet-foot">Frequency reflects the years tagged so far — coverage grows as more papers are added.</p>
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
      <div className="shrink-0 flex items-center gap-2 px-4 py-3 border-b border-zinc-200 dark:border-hairline">
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
            <div key={i} className="rounded-xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-surface-paper px-3.5 py-3">
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
  /** Same-topic questions in other papers — threaded as next reps on a low
   *  self-mark (PT-3). */
  siblings?: TopicSibling[];
  onJumpSibling?: (s: TopicSibling) => void;
  onRecordMark?: (mark: SelfMark | null) => void;
  onClose: () => void;
  onFullScheme: (page: number) => void;
  /** Previous/next question's scheme; absent during the Full Loop, which
   *  sequences questions itself. */
  onStep?: (dir: 1 | -1) => void;
  canPrev?: boolean;
  canNext?: boolean;
  /** On a phone the scheme is the shared Sheet; `open` lets it rise and leave. */
  open?: boolean;
}> = ({ q, wide, reduced, schemePdf, schemeUrl, schemeErrored, copyright, selfMark, existingMark, licence, siblings, onJumpSibling, onRecordMark, onClose, onFullScheme, onStep, canPrev, canNext, open = true }) => {
  const schemeRegion = schemeRegionFor(q);
  // Text size for the crop; it carries across questions while the panel is open.
  const [zoom, setZoom] = useState(1);
  // The phone sheet stays mounted to leave; it opens again at the crop's own size.
  useEffect(() => { if (open) setZoom(1); }, [open]);
  const zoomStep = (dir: 1 | -1) => setZoom(z => Math.min(2, Math.max(1, Math.round((z + dir * 0.25) * 100) / 100)));
  const showsCrop = q.mode !== 'pagejump' && !schemeErrored;
  const firstPage = schemeRegion[0]?.p;
  const closeRef = useRef<HTMLButtonElement | null>(null);
  useEffect(() => {
    closeRef.current?.focus();
  }, []);
  const scored = existingMark?.score;
  const setScore = (v: number) =>
    onRecordMark?.({ score: v, max: 100, gap: v >= 100 ? undefined : existingMark?.gap, ts: Date.now() });
  const setGap = (k: GapKind) =>
    onRecordMark?.({ score: existingMark?.score ?? 0, max: 100, gap: existingMark?.gap === k ? undefined : k, ts: Date.now() });
  const title = `${q.label ?? `Question ${q.n}`} · marking scheme`;
  // Previous and next question: bar glyphs at the right of the head (Close stays at the left).
  const steps = onStep ? (
    <span className="pv-reveal-steps">
      <IconButton label="Previous question’s marking scheme" aria-disabled={!canPrev || undefined} onClick={() => { if (canPrev) onStep(-1); }}
        icon={<ChevronLeft className="ui-icon" width={24} height={24} strokeWidth={1.75} aria-hidden="true" focusable="false" />} />
      <IconButton label="Next question’s marking scheme" aria-disabled={!canNext || undefined} onClick={() => { if (canNext) onStep(1); }}
        icon={<ChevronRight className="ui-icon" width={24} height={24} strokeWidth={1.75} aria-hidden="true" focusable="false" />} />
    </span>
  ) : null;
  const body = (
    <>
      <p className="pv-sheet-sub pv-reveal-sub">How examiners award the marks — not a model answer.</p>
      {showsCrop && (
        <div className="pv-reveal-size">
          <span className="t-meta">Text size</span>
          <span className="pv-zoom" role="group" aria-label="Text size">
            <IconButton label="Smaller marking scheme text" aria-disabled={zoom <= 1 || undefined} onClick={() => { if (zoom > 1) zoomStep(-1); }}
              icon={<Minus className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" />} />
            <output aria-live="polite" className="ui-readout pv-zoom-value">{Math.round(zoom * 100)}%</output>
            <IconButton label="Bigger marking scheme text" aria-disabled={zoom >= 2 || undefined} onClick={() => { if (zoom < 2) zoomStep(1); }}
              icon={<Plus className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" />} />
          </span>
          <UiButton size="sm" onClick={() => setZoom(1)}>Fit</UiButton>
        </div>
      )}
      {/* Content settles a beat after the panel lands (premium stagger). */}
      <MotionDiv
        initial={reduced ? false : { opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: reduced ? 0 : 0.08, duration: 0.28, ease: [0.16, 1, 0.3, 1] }}
        className="pv-reveal-crop"
      >
        {q.schemeNote && (
          <p className="pv-reveal-note">
            {q.schemeNote}
          </p>
        )}
        {q.mode === 'pagejump' ? (
          <p className="pv-reveal-say">
            This question’s answer spans several scheme pages. Open the marking scheme to read it in full.
          </p>
        ) : schemeErrored ? (
          <p className="pv-reveal-say">
            Couldn’t load the marking scheme. Open it in the Scheme tab instead.
          </p>
        ) : schemePdf ? (
          <CropView pdf={schemePdf} region={schemeRegion} trim zoom={zoom} responsive maxWidth={1200} />
        ) : (
          <div role="status" aria-live="polite" className="pv-state pv-reveal-loading">
            <Spinner />
            <span className="t-meta">Loading the marking scheme…</span>
            {schemeUrl && (
              <a href={schemeUrl} target="_blank" rel="noopener noreferrer" className="ui-part ui-link ui-link--quiet">
                <span>Taking too long? Open it in your browser</span>
              </a>
            )}
          </div>
        )}
      </MotionDiv>
    </>
  );
  const foot = (
    <>
      {selfMark && (
        <div className="pv-selfmark">
          <div className="pv-selfmark-head">
            <p className="t-label">How did you do against the scheme?</p>
            {licence && (
              <span className="pv-selfmark-licence">
                {licence.pct}%-calibrated eye · {licence.sessions} chair sessions
              </span>
            )}
          </div>
          <div className="pv-bands" role="group" aria-label="How did you do against the scheme?">
            {SCORE_BANDS.map(b => (
              <ChoiceTile key={b.v} compact kind="toggle" chosen={scored === b.v} label={b.label} onClick={() => setScore(b.v)} />
            ))}
          </div>
          {scored !== undefined && scored < 100 && (
            <>
              <p className="pv-selfmark-ask">What went wrong? (helps your weakness map)</p>
              <div className="pv-gaps" role="group" aria-label="What went wrong?">
                {GAP_OPTS.map(g => (
                  <ChoiceTile key={g.k} compact kind="toggle" chosen={existingMark?.gap === g.k} label={g.label} onClick={() => setGap(g.k)} />
                ))}
              </div>
            </>
          )}
          {/* PT-3: a low mark turns into immediate next reps — the same topic,
              other years. Failure becomes actionable in one tap. */}
          {scored !== undefined && scored <= 50 && !!siblings?.length && onJumpSibling && (
            <>
              <p className="pv-selfmark-ask">Next reps — the same topic came up in other years:</p>
              <div className="pv-reps">
                {siblings.map(s => (
                  <TextButton key={s.paperKey + s.n} arrow="forward" onClick={() => onJumpSibling(s)}>
                    {s.year} · {questionLabel(s, { short: true })}
                  </TextButton>
                ))}
              </div>
            </>
          )}
        </div>
      )}
      <div className="pv-reveal-end">
        <span className="pv-reveal-copy">{copyright ?? '© State Examinations Commission'}</span>
        <TextButton arrow="forward" aria-disabled={!firstPage || undefined} onClick={() => { if (firstPage) onFullScheme(firstPage); }}>
          View full scheme
        </TextButton>
      </div>
    </>
  );
  // On a phone: the shared Sheet, Close at the top left, the self-mark pinned at its foot.
  if (!wide) {
    return (
      <Sheet open={open} onClose={onClose} title={title} titleAlign="start" titleSize="small" actions={steps ?? undefined}
        footer={foot} className="pv-reveal-sheet">
        {body}
      </Sheet>
    );
  }
  // On a tablet (the tray) and a laptop (beside the paper): the same head as a sheet's.
  return (
    <>
      <div className="ui-sheet-head ui-sheet-head--start pv-reveal-head">
        <IconButton ref={closeRef} label="Close" onClick={onClose}
          icon={<X className="ui-icon" width={24} height={24} strokeWidth={1.75} aria-hidden="true" focusable="false" />} />
        <h2 className="ui-sheet-title">{title}</h2>
        {steps ?? <span aria-hidden="true" />}
      </div>
      <div className="pv-reveal-body">{body}</div>
      <div className="pv-reveal-foot">{foot}</div>
    </>
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
  answerInk?: AnswerInkProps;
  onReveal?: (q: PaperAnswerQuestion) => void;
  topicInfo?: Map<string, { subtopicId: string; label: string; yearsWith: number; totalYears: number }> | null;
  onTopic?: (n: string) => void;
  marks?: MarkToken[];
  paceInfo?: { minsPerMark: number | null; totalMarks: number };
  commands?: CommandToken[];
  onCommand?: (c: CommandToken) => void;
}> = React.memo(({ pdf, pageNumber, zoom, epoch, observe, anchors, showAnswerChip, answerInk, onReveal, topicInfo, onTopic, marks, paceInfo, commands, onCommand }) => {
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
      className="relative bg-white dark:bg-surface-paper rounded-md shadow-sm mb-2.5 overflow-hidden"
      style={{ paddingBottom: `${(aspect ?? 1.414) * 100}%` }}
      aria-label={`Page ${pageNumber}`}
    >
      <canvas ref={canvasRef} className="absolute inset-0 w-full h-full" />
      {answerInk && <AnswerInk {...answerInk} aspect={aspect??1.414} />}
      {/* Per-question rails — fractional top rides zoom + virtualisation. The
          marking-scheme action rides the right edge; topic context the left. */}
      {anchors?.map(q => {
        const top = `${Math.min(0.97, Math.max(0, q.pY[0])) * 100}%`;
        const info = topicInfo?.get(q.n);
        return (
          <React.Fragment key={`${q.pP}-${q.n}`}>
            {info && (
              // The topic and how often it comes up, at the question's left: a box you press.
              <UiButton
                size="sm"
                onClick={() => onTopic?.(q.n)}
                className="pv-chip pv-chip--topic"
                style={{
                  top,
                  // Float just above the question's first line so the label
                  // doesn't sit on top of the question text (unless it's at the
                  // very top of the page, where there's no room above).
                  transform: q.pY[0] > 0.05 ? 'translateY(-100%)' : 'none',
                }}
                aria-label={`${info.label} — appeared in ${info.yearsWith} of ${info.totalYears} tagged years. Drill it across years.`}
              >
                <span className="pv-chip-label">Topic</span>
                <span className="pv-chip-name">{info.label}</span>
                {info.totalYears > 0 && (
                  <span className="ui-readout pv-chip-count">
                    {info.yearsWith} / {info.totalYears}
                  </span>
                )}
              </UiButton>
            )}
            {showAnswerChip && (
              <UiButton
                size="sm"
                arrow="forward"
                onClick={() => onReveal?.(q)}
                className="pv-chip pv-chip--scheme"
                style={{ top }}
                aria-label={`Open the marking scheme for ${q.label ?? `Question ${q.n}`}`}
              >
                Mark scheme
              </UiButton>
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
            backgroundColor: 'rgba(var(--nsu-orange-rgb), 0.16)',
            borderBottom: '2px solid var(--nsu-orange)',
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
              color: COLORS.accentDarkText,
              border: '1px solid rgba(var(--nsu-orange-rgb), 0.35)',
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

// A changed paper/account is a new document session, with isolated authored work.
const PaperViewer:React.FC<ViewerProps> = props => <Viewer key={`${props.storageNs??props.paper.url}|${props.scheme?.url??''}`} {...props}/>;
export default PaperViewer;
