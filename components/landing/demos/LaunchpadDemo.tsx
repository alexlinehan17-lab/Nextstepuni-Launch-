/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Launchpad playground demo. Two modes:
 *  - reflex — a mini Command-Word Reflex. Same tokenising and cue matching as
 *    components/CommandWordReflex/index.tsx (split on whitespace, sliding
 *    window over the command word so multi-word cues match), re-cut in the
 *    landing register: ink text, one orange underline, hairline panels.
 *    Autoplays with a ScriptedCursor until the first real pointer or key.
 *  - points — a CAO points calculator on six subjects. The points table and
 *    the Maths bonus rule are copied from components/subjectData.ts, which is
 *    what components/CAOPointsSimulator.tsx computes with.
 */

import React, { useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { AnimatePresence, MotionDiv, MotionSpan, useReducedMotion } from '../../Motion';
import { ScriptedCursor, type CursorStep } from '../motion';
import { COPY } from '../copy';
import { COMMAND_WORDS } from '../demoData';
import { Button, Rule } from '../primitives';
import { FONT, L } from '../theme';
import type { DemoProps } from '../sections/Playground';

export const LAUNCHPAD_SUBTABS: { id: string; label: string }[] = [
  { id: 'reflex', label: 'Command-Word Reflex' },
  { id: 'points', label: 'CAO points' },
];

const T = COPY.playground.launchpad;
const EASE = [0.2, 0.8, 0.2, 1] as const;

/** The typographic meta line: mono, uppercase, tracked, faint. */
const META: React.CSSProperties = {
  fontFamily: FONT.mono, fontSize: 11, letterSpacing: '0.14em', textTransform: 'uppercase', color: L.faint, lineHeight: 1.5, margin: 0,
};
const SMALL: React.CSSProperties = { fontFamily: FONT.sans, fontSize: 13, lineHeight: 1.5, color: L.muted, margin: 0 };

// ─── Reflex: tokenising and matching, verbatim from CommandWordReflex ───────

const norm = (s: string) => s.replace(/[^a-zA-Z]/g, '').toLowerCase();
const isSpace = (t: string) => /^\s+$/.test(t);

/**
 * Token indices that make up the command word. Slides a window of the cue's
 * words over the non-whitespace token positions, so "Distinguish between"
 * would match as a run and single-word cues match unchanged.
 */
const cueIndices = (tokens: string[], commandWord: string): Set<number> => {
  const set = new Set<number>();
  const cmdWords = commandWord.toLowerCase().split(/\s+/).map(w => w.replace(/[^a-z]/g, '')).filter(Boolean);
  if (cmdWords.length === 0) return set;
  const wordPos = tokens.map((t, i) => (isSpace(t) ? -1 : i)).filter(i => i >= 0);
  for (let p = 0; p + cmdWords.length <= wordPos.length; p++) {
    let ok = true;
    for (let k = 0; k < cmdWords.length; k++) {
      if (norm(tokens[wordPos[p + k]]) !== cmdWords[k]) { ok = false; break; }
    }
    if (ok) for (let k = 0; k < cmdWords.length; k++) set.add(wordPos[p + k]);
  }
  return set;
};

const SHAKE = { x: [0, -4, 4, -2, 0] };
/** The cursor rests beside the stem first, as a reader would, before it goes for the command word. */
const HOLD_REST = 1800;
const HOLD_CUE = 2600;
const HOLD_NEXT = 700;
/** Gap between the stem's edge and the resting cursor, in px. */
const REST_GAP = 28;
/** Re-measure once the reveal panels (0.16s delay + 0.3s rise) have landed and the Next button is where it will stay. */
const MEASURE_AFTER_REVEAL = 650;
/** Re-measure once the question fade (0.2s out, 0.2s in, mode="wait") has put the new stem on stage. */
const MEASURE_AFTER_NEXT = 550;
/** Bring the Next button on stage a beat before the cursor sets off for it. */
const SHOW_NEXT_BEFORE = 400;
/** Move keyboard focus to the new stem once it has mounted. */
const FOCUS_AFTER_NEXT = 450;
/** Ignore sub-pixel jitter when deciding whether a re-measure changed anything. */
const POS_EPS = 0.2;

const ReflexMode: React.FC<{ reduce: boolean; playing: boolean; rootRef: React.RefObject<HTMLDivElement | null> }> = ({ reduce, playing, rootRef }) => {
  const [qIndex, setQIndex] = useState(0);
  const [phase, setPhase] = useState<'spot' | 'reveal'>('spot');
  const [wrong, setWrong] = useState<Set<number>>(() => new Set());
  const [usedReveal, setUsedReveal] = useState(false);
  /** First-try results for the last five questions answered. */
  const [results, setResults] = useState<boolean[]>([]);
  // The scripted cursor's taps are a demo, not the visitor's record: the tally
  // is hidden while autoplay runs and starts fresh the moment it stops.
  useEffect(() => { if (!playing) setResults([]); }, [playing]);
  /** Bumped when a re-measure moved a cursor target, so the cursor re-renders with the new numbers. */
  const [, setTick] = useState(0);

  const q = COMMAND_WORDS[qIndex];
  const tokens = useMemo(() => q.stem.split(/(\s+)/), [q]);
  const cue = useMemo(() => cueIndices(tokens, q.commandWord), [tokens, q]);
  const wordPos = useMemo(() => tokens.map((t, i) => (isSpace(t) ? -1 : i)).filter(i => i >= 0), [tokens]);
  const cueIdx = wordPos.find(i => cue.has(i)) ?? wordPos[0];

  // The phase is mirrored into a ref so scripted taps stay idempotent even if a
  // step fires twice.
  const phaseRef = useRef(phase);
  phaseRef.current = phase;
  /** True when the last state change came from a real tap or key, so focus follows it. */
  const byHand = useRef(false);
  const tokenRefs = useRef(new Map<number, HTMLElement>());
  const stemRef = useRef<HTMLParagraphElement>(null);
  const nextRef = useRef<HTMLSpanElement>(null);
  const timers = useRef<number[]>([]);
  const later = (ms: number, fn: () => void) => {
    const id = window.setTimeout(() => { timers.current = timers.current.filter(t => t !== id); fn(); }, ms);
    timers.current.push(id);
  };
  const clearTimers = () => { timers.current.forEach(id => window.clearTimeout(id)); timers.current = []; };

  const setTokenRef = (i: number) => (el: HTMLElement | null) => {
    if (el) tokenRefs.current.set(i, el);
    else tokenRefs.current.delete(i);
  };

  const solve = (firstTry: boolean) => {
    if (phaseRef.current === 'reveal') return;
    phaseRef.current = 'reveal';
    setPhase('reveal');
    setResults(r => [...r, firstTry].slice(-5));
  };
  const tapToken = (i: number) => {
    if (phaseRef.current === 'reveal') return;
    if (cue.has(i)) solve(wrong.size === 0 && !usedReveal);
    else setWrong(prev => (prev.has(i) ? prev : new Set(prev).add(i)));
  };
  const reveal = () => { setUsedReveal(true); solve(false); };
  const next = () => {
    if (phaseRef.current !== 'reveal') return;
    phaseRef.current = 'spot';
    setQIndex(i => (i + 1) % COMMAND_WORDS.length);
    setPhase('spot');
    setWrong(new Set());
    setUsedReveal(false);
    rootRef.current?.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
  };
  const handTap = (i: number) => { byHand.current = true; tapToken(i); };
  const handReveal = () => { byHand.current = true; reveal(); };
  const handNext = () => { byHand.current = true; next(); };

  // Keyboard users lose their place when the tapped token becomes a span or
  // the Next button unmounts: follow a by-hand change with focus.
  useEffect(() => {
    if (!byHand.current) return;
    byHand.current = false;
    if (phase === 'reveal') nextRef.current?.querySelector('button')?.focus({ preventScroll: true });
    else later(FOCUS_AFTER_NEXT, () => tokenRefs.current.get(wordPos[0])?.focus({ preventScroll: true }));
  }, [phase]);

  // ── Autoplay. ScriptedCursor restarts its timers whenever the `steps`
  // array changes identity, so the array is built once and the measured
  // positions are written into it in place; a tick re-renders the cursor with
  // the new numbers without re-firing the step it is on. Positions are in the
  // root's content coordinates (scroll-independent) as a percentage of its
  // client box, which is how the absolutely positioned cursor resolves its
  // left/top inside the scrolling root.
  const handlers = useRef({ cue: () => {}, next: () => {} });
  // Rest beside the stem (no tap) → tap the command word → Next question → loop.
  // The cursor never taps a wrong word: the strike and its message are for the
  // visitor's own misses.
  const stepsRef = useRef<CursorStep[]>([
    { x: 50, y: 50, hold: HOLD_REST },
    { x: 50, y: 50, click: true, hold: HOLD_CUE, onArrive: () => handlers.current.cue() },
    { x: 50, y: 50, click: true, hold: HOLD_NEXT, onArrive: () => handlers.current.next() },
  ]);

  const measure = () => {
    const root = rootRef.current;
    if (!root) return;
    const rr = root.getBoundingClientRect();
    const w = root.clientWidth, h = root.clientHeight;
    if (!w || !h) return;
    /** A viewport point as content coordinates inside the root, in percent of its client box. */
    const toPct = (px: number, py: number) => ({ x: ((px - rr.left) / w) * 100, y: ((py - rr.top + root.scrollTop) / h) * 100 });
    const centre = (el: Element | null | undefined) => {
      if (!el) return null;
      const r = el.getBoundingClientRect();
      return toPct(r.left + r.width / 2, r.top + r.height / 2);
    };
    /** Beside the stem: just off its right edge at mid-height, or under its right end when the stem fills the stage. */
    const rest = () => {
      const el = stemRef.current;
      if (!el) return null;
      const r = el.getBoundingClientRect();
      const fits = r.right + REST_GAP + 22 <= rr.left + w;
      return fits ? toPct(r.right + REST_GAP, r.top + r.height / 2) : toPct(r.right - REST_GAP, r.bottom + REST_GAP);
    };
    const targets = [
      rest(),
      centre(tokenRefs.current.get(cueIdx)),
      // The Next button is only on stage in the reveal; until then its step keeps the last value.
      centre(nextRef.current?.querySelector('button')),
    ];
    let changed = false;
    targets.forEach((p, k) => {
      if (!p) return;
      const s = stepsRef.current[k];
      if (Math.abs(s.x - p.x) > POS_EPS || Math.abs(s.y - p.y) > POS_EPS) { s.x = p.x; s.y = p.y; changed = true; }
    });
    if (changed) setTick(t => t + 1);
  };
  const measureRef = useRef(measure);
  measureRef.current = measure;

  /** Scroll the stage (only the stage) so the Next button is in view before the cursor heads for it. */
  const showNext = () => {
    const root = rootRef.current, el = nextRef.current;
    if (!root || !el) return;
    const bottom = el.getBoundingClientRect().bottom - root.getBoundingClientRect().top + root.scrollTop;
    if (bottom > root.scrollTop + root.clientHeight) root.scrollTo({ top: bottom - root.clientHeight + 16, behavior: 'smooth' });
  };

  handlers.current = {
    cue: () => {
      tapToken(cueIdx);
      later(MEASURE_AFTER_REVEAL, () => measureRef.current());
      later(HOLD_CUE - SHOW_NEXT_BEFORE, showNext);
    },
    next: () => { next(); later(MEASURE_AFTER_NEXT, () => measureRef.current()); },
  };

  // Measure before the cursor's first paint, then track the stage's size.
  useLayoutEffect(() => { if (playing) measureRef.current(); }, [playing]);
  useEffect(() => {
    if (!playing) return;
    const root = rootRef.current;
    const onResize = () => measureRef.current();
    const ro = typeof ResizeObserver !== 'undefined' ? new ResizeObserver(onResize) : null;
    if (root) ro?.observe(root);
    window.addEventListener('resize', onResize);
    return () => { ro?.disconnect(); window.removeEventListener('resize', onResize); };
  }, [playing, rootRef]);
  useEffect(() => clearTimers, []);

  const firstTry = wrong.size === 0 && !usedReveal;
  const stemStyle: React.CSSProperties = {
    fontFamily: FONT.serif, fontWeight: 600, fontSize: 'clamp(19px, 2.4vw, 26px)', lineHeight: 1.4, letterSpacing: '-0.01em', color: L.ink, margin: 0, maxWidth: '28em',
  };
  const tokenStyle: React.CSSProperties = {
    font: 'inherit', lineHeight: 'inherit', letterSpacing: 'inherit', color: 'inherit', background: 'none', border: 0, padding: '0 1px', margin: '0 -1px', borderRadius: 3, cursor: 'pointer',
  };

  return (
    <div className="flex flex-col min-h-full">
      <AnimatePresence mode="wait" initial={false}>
        <MotionDiv
          key={q.id}
          initial={reduce ? false : { opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          exit={reduce ? undefined : { opacity: 0, y: -6 }}
          transition={{ duration: 0.2, ease: 'easeOut' }}
        >
          <p style={META}>{q.subjectLabel} · {q.questionRef} · {q.marks} marks</p>
          <p style={{ ...SMALL, marginTop: 6 }}>{T.prompt}</p>

          <p ref={stemRef} style={{ ...stemStyle, marginTop: 18 }}>
            {tokens.map((tok, i) => {
              if (isSpace(tok)) return <span key={i}>{tok}</span>;
              const isCue = cue.has(i);
              const isWrong = wrong.has(i);
              if (phase === 'reveal' && isCue) {
                return <span key={i} ref={setTokenRef(i)} style={{ borderBottom: `3px solid ${L.orange}`, paddingBottom: 1 }}>{tok}</span>;
              }
              const button = (
                <button
                  key={i}
                  type="button"
                  ref={setTokenRef(i)}
                  onClick={() => handTap(i)}
                  disabled={phase === 'reveal'}
                  className={phase === 'spot' && !isWrong ? 'landing-hover-card' : undefined}
                  style={isWrong
                    ? { ...tokenStyle, textDecoration: 'line-through', color: L.faint, cursor: 'default' }
                    : { ...tokenStyle, cursor: phase === 'reveal' ? 'default' : 'pointer' }}
                >{tok}</button>
              );
              if (!isWrong) return button;
              return (
                <MotionSpan key={i} style={{ display: 'inline-block' }} initial={{ x: 0 }} animate={reduce ? undefined : SHAKE} transition={{ duration: 0.18, ease: 'easeOut' }}>
                  {button}
                </MotionSpan>
              );
            })}
          </p>

          {phase === 'spot' && wrong.size > 0 && (
            <MotionDiv
              className="mt-4 flex flex-wrap items-center justify-between gap-x-6 gap-y-2"
              initial={reduce ? false : { opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.18 }}
            >
              <p role="status" style={SMALL}>{T.wrong}</p>
              <Button variant="ghost" onClick={handReveal}>{T.reveal}</Button>
            </MotionDiv>
          )}

          <AnimatePresence initial={false}>
            {phase === 'reveal' && (
              <MotionDiv key="reveal" initial={reduce ? false : { opacity: 0 }} animate={{ opacity: 1 }} exit={reduce ? undefined : { opacity: 0 }} transition={{ duration: 0.15 }}>
                {firstTry && <p role="status" style={{ ...SMALL, color: L.ink, fontWeight: 600, marginTop: 10 }}>{T.right}</p>}
                <div className="mt-5 grid gap-5 sm:grid-cols-2 sm:gap-7" style={{ maxWidth: 880 }}>
                  {[{ heading: T.demand, text: q.demand }, { heading: T.trap, text: q.trap }].map((panel, k) => (
                    <MotionDiv
                      key={panel.heading}
                      initial={reduce ? false : { opacity: 0, y: 12 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.32, delay: k * 0.08, ease: EASE }}
                      style={{ borderTop: `1px solid ${L.hairline}`, paddingTop: 12 }}
                    >
                      <p style={META}>{panel.heading}</p>
                      <p style={{ fontFamily: FONT.sans, fontSize: 14, lineHeight: 1.55, color: L.ink, margin: '8px 0 0' }}>{panel.text}</p>
                    </MotionDiv>
                  ))}
                </div>
                <MotionDiv
                  className="mt-5 flex flex-wrap items-center justify-between gap-x-6 gap-y-3"
                  style={{ maxWidth: 880 }}
                  initial={reduce ? false : { opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: 0.16, ease: EASE }}
                >
                  <p style={{ fontFamily: FONT.mono, fontSize: 11, lineHeight: 1.5, color: L.faint, margin: 0 }}>{q.source}</p>
                  <span ref={nextRef} className="inline-block"><Button variant="ink" onClick={handNext}>{T.next}</Button></span>
                </MotionDiv>
              </MotionDiv>
            )}
          </AnimatePresence>
        </MotionDiv>
      </AnimatePresence>

      {results.length > 0 && !playing && (
        <p style={{ ...META, marginTop: 'auto', paddingTop: 24 }}>
          {results.filter(Boolean).length} {T.of} {results.length} {T.firstTime}
        </p>
      )}

      {playing && <ScriptedCursor steps={stepsRef.current} playing={playing} />}
    </div>
  );
};

// ─── Points: table and bonus rule copied from components/subjectData.ts ──────
// (HIGHER_POINTS, ORDINARY_POINTS and getPointsForGrade — the values that
// components/CAOPointsSimulator.tsx totals). Not imported: that module drags
// app state along with it.

const HIGHER_POINTS: Record<string, number> = {
  H1: 100, H2: 88, H3: 77, H4: 66, H5: 56, H6: 46, H7: 37, H8: 0,
};
const ORDINARY_POINTS: Record<string, number> = {
  O1: 56, O2: 46, O3: 37, O4: 28, O5: 20, O6: 12, O7: 0, O8: 0,
};
const MATHS_BONUS = 25;

/** CAO points for a grade, including the +25 Maths bonus for Higher Level H6 and above (H1–H6). */
const pointsForGrade = (grade: string, isMaths: boolean): number => {
  let points = grade.startsWith('H') ? (HIGHER_POINTS[grade] ?? 0) : (ORDINARY_POINTS[grade] ?? 0);
  if (isMaths && grade.startsWith('H') && HIGHER_POINTS[grade] >= 46) points += MATHS_BONUS;
  return points;
};

type Level = 'higher' | 'ordinary';
interface PointsRow { subject: string; level: Level; band: number }
const START_ROWS: PointsRow[] = [
  { subject: 'Mathematics', level: 'higher', band: 3 },
  { subject: 'English', level: 'higher', band: 3 },
  { subject: 'Irish', level: 'higher', band: 4 },
  { subject: 'Biology', level: 'higher', band: 3 },
  { subject: 'Business', level: 'higher', band: 3 },
  { subject: 'Geography', level: 'higher', band: 3 },
];
const gradeOf = (r: PointsRow) => `${r.level === 'higher' ? 'H' : 'O'}${r.band}`;
const isMaths = (r: PointsRow) => r.subject === 'Mathematics';

const PointsMode: React.FC<{ reduce: boolean }> = ({ reduce }) => {
  const [rows, setRows] = useState<PointsRow[]>(START_ROWS);
  // Six subjects, so the best six is all of them.
  const total = rows.reduce((sum, r) => sum + pointsForGrade(gradeOf(r), isMaths(r)), 0);
  const bonusApplies = rows.some(r => isMaths(r) && r.level === 'higher' && r.band <= 6);
  const update = (i: number, patch: Partial<PointsRow>) => setRows(rs => rs.map((r, k) => (k === i ? { ...r, ...patch } : r)));

  const stepStyle = (enabled: boolean): React.CSSProperties => ({
    width: 32, height: 32, display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
    background: L.paper, border: `1px solid ${L.hairline}`, borderRadius: 4,
    fontFamily: FONT.sans, fontSize: 16, lineHeight: 1, color: L.ink, padding: 0,
    cursor: enabled ? 'pointer' : 'default', opacity: enabled ? 1 : 0.4,
  });

  return (
    <div className="flex flex-col min-h-full">
      <p style={META}>{T.pointsEyebrow}</p>
      <div className="mt-4 flex flex-col md:flex-row md:items-stretch md:gap-7">
        <ul className="m-0 p-0 list-none flex-1 min-w-0">
          {rows.map((r, i) => {
            const enabledDown = r.band < 8;
            const enabledUp = r.band > 1;
            return (
              <li
                key={r.subject}
                className="grid items-center gap-x-2 sm:gap-x-4"
                style={{ gridTemplateColumns: '1fr auto auto', padding: '8px 0', borderTop: i === 0 ? `1.5px solid ${L.ink}` : `1px solid ${L.hairline}` }}
              >
                <span className="truncate" style={{ fontFamily: FONT.sans, fontWeight: 600, fontSize: 14, color: L.ink }}>{r.subject}</span>
                <span role="group" aria-label={`${r.subject} ${T.level}`} className="flex gap-2 sm:gap-3">
                  {(['higher', 'ordinary'] as Level[]).map(l => {
                    const on = r.level === l;
                    return (
                      <button
                        key={l}
                        type="button"
                        aria-pressed={on}
                        onClick={() => update(i, { level: l })}
                        className="landing-tab"
                        // The button is the 32px hit target; the underline stays tight to the word on the inner span.
                        style={{
                          fontFamily: FONT.sans, fontSize: 12, fontWeight: on ? 700 : 500, color: on ? L.ink : L.muted,
                          background: 'none', border: 0, padding: '5px 0', minHeight: 32, display: 'inline-flex', alignItems: 'center', cursor: 'pointer', lineHeight: 1.2,
                        }}
                      >
                        <span style={{ color: 'inherit', borderBottom: `1.5px solid ${on ? L.ink : 'transparent'}`, paddingBottom: 3 }}>
                          {l === 'higher' ? T.higher : T.ordinary}
                        </span>
                      </button>
                    );
                  })}
                </span>
                <span className="flex items-center gap-1 sm:gap-1.5">
                  <button
                    type="button"
                    aria-label={`${T.lower}, ${r.subject}`}
                    disabled={!enabledDown}
                    onClick={() => update(i, { band: r.band + 1 })}
                    className={enabledDown ? 'landing-hover-card' : undefined}
                    style={stepStyle(enabledDown)}
                  >−</button>
                  <span aria-live="polite" style={{ fontFamily: FONT.serif, fontWeight: 600, fontSize: 17, color: L.ink, minWidth: 30, textAlign: 'center', fontVariantNumeric: 'tabular-nums' }}>{gradeOf(r)}</span>
                  <button
                    type="button"
                    aria-label={`${T.raise}, ${r.subject}`}
                    disabled={!enabledUp}
                    onClick={() => update(i, { band: r.band - 1 })}
                    className={enabledUp ? 'landing-hover-card' : undefined}
                    style={stepStyle(enabledUp)}
                  >+</button>
                  <span className="hidden sm:inline-block" style={{ fontFamily: FONT.mono, fontSize: 12, color: L.faint, minWidth: 34, textAlign: 'right', fontVariantNumeric: 'tabular-nums' }}>
                    {pointsForGrade(gradeOf(r), isMaths(r))}
                  </span>
                </span>
              </li>
            );
          })}
        </ul>

        <Rule className="md:hidden mt-5" />
        <div aria-hidden="true" className="hidden md:block self-stretch shrink-0" style={{ width: 1, background: L.hairline }} />

        <div className="mt-5 md:mt-0 md:w-[240px] shrink-0 flex flex-col justify-end">
          <p aria-live="polite" style={{ fontFamily: FONT.serif, fontWeight: 600, fontSize: 'clamp(56px, 8vw, 96px)', lineHeight: 1, letterSpacing: '-0.03em', color: L.ink, margin: 0, fontVariantNumeric: 'tabular-nums' }}>
            <MotionSpan
              key={total}
              style={{ display: 'inline-block' }}
              initial={reduce ? false : { opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.28, ease: EASE }}
            >
              {total}
            </MotionSpan>
          </p>
          <p style={{ ...META, marginTop: 8 }}>{T.points}</p>
          {bonusApplies && <p style={{ ...SMALL, marginTop: 12 }}>{T.bonusApplied}</p>}
        </div>
      </div>
    </div>
  );
};

// ─── Root ────────────────────────────────────────────────────────────────────

const LaunchpadDemo: React.FC<DemoProps> = ({ sub, active }) => {
  const reduce = !!useReducedMotion();
  const rootRef = useRef<HTMLDivElement>(null);
  const [interacted, setInteracted] = useState(false);
  const stop = () => { if (!interacted) setInteracted(true); };
  const mode = sub === 'points' ? 'points' : 'reflex';
  const playing = mode === 'reflex' && active && !interacted && !reduce;

  return (
    <div
      ref={rootRef}
      className="h-full w-full p-4 sm:p-6 md:p-7"
      style={{ position: 'relative', overflowY: 'auto', overflowX: 'hidden', background: L.paper }}
      onPointerDownCapture={stop}
      onKeyDownCapture={stop}
    >
      {mode === 'points'
        ? <PointsMode reduce={reduce} />
        : <ReflexMode reduce={reduce} playing={playing} rootRef={rootRef} />}
    </div>
  );
};

export default LaunchpadDemo;
