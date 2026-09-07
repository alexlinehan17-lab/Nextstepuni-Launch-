/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank playground demo — the "use the product right here" moment for
 * the Mark Bank (echoes Brilliant's auto-playing hero demo). One real card
 * from demoData.ts: the question, then the marking scheme rows quoted from
 * the SEC scheme, then a self-score, then the next card. A scripted cursor
 * walks that loop — resting beside the question first, so the reader gets the
 * "answer it in your head" beat — until the visitor touches the demo, at
 * which point it stops for good and the card is theirs.
 */

import React, { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import { AnimatePresence, MotionDiv, useReducedMotion } from '../../Motion';
import { COPY } from '../copy';
import { DEMO_CARD_SUBJECTS, DEMO_CARDS, type DemoCard, type RowKind } from '../demoData';
import { type CursorStep, ScriptedCursor } from '../motion';
import { Button } from '../primitives';
import type { DemoProps } from '../sections/Playground';
import { FONT, L } from '../theme';

export const MARKBANK_SUBTABS: { id: string; label: string }[] = DEMO_CARD_SUBJECTS.map(s => ({ id: s.id, label: s.label }));

type Phase = 'question' | 'scheme' | 'scored';
type Choice = 'got' | 'shaky' | 'missed';
interface View { index: number; phase: Phase; choice: Choice | null }

const MB = COPY.playground.markbank;
const EASE: [number, number, number, number] = [0.2, 0.8, 0.2, 1];
const RESET: View = { index: 0, phase: 'question', choice: null };

/** Mono meta style shared by the top line, the qualifiers and the progress line. */
const META: React.CSSProperties = { fontFamily: FONT.mono, fontSize: 11, letterSpacing: '0.14em', textTransform: 'uppercase', color: L.faint, lineHeight: 1.4 };

const QUALIFIER: Record<RowKind, string | null> = { point: null, allOf: MB.allOf, alt: MB.or, anyN: MB.anyOf };
const NOTE: Record<Choice, string> = { got: MB.backLater, shaky: MB.backShaky, missed: MB.backSoon };

/** "2025 HL Q1(b)" → "Q1(b)": the question part after the year and level tokens. */
const questionPart = (ref: string): string => ref.replace(/^\d{4}\s+\S+\s+/, '');

/** How close (in % of the stage) a re-measured button has to move before the cursor script is told. */
const POS_EPS = 0.25;
/** Gap between the question's right edge and the resting cursor, and the cursor's own width, in px. */
const REST_GAP = 10;
const CURSOR_W = 24;
/** The card block's width, shared by the meta line, the question, the scheme and the progress line. */
const CARD_MAX = 760;

const clamp = (n: number, lo: number, hi: number): number => Math.min(Math.max(n, lo), hi);

/**
 * Scroll the demo's own scroller (never the page) so `el` is in view, keeping
 * its top visible when it is taller than the stage. A long Home Economics
 * card overflows a 440px stage on a phone; without this the cursor would be
 * "clicking" a button below the fold.
 */
const reveal = (scroller: HTMLElement | null, el: HTMLElement | null | undefined): void => {
  if (!scroller || !el) return;
  const s = scroller.getBoundingClientRect();
  const b = el.getBoundingClientRect();
  const pad = 16;
  if (b.top < s.top + pad) scroller.scrollTop -= s.top + pad - b.top;
  else if (b.bottom > s.bottom - pad) scroller.scrollTop += Math.min(b.bottom - (s.bottom - pad), b.top - (s.top + pad));
};

const MarkBankDemo: React.FC<DemoProps> = ({ sub, active }) => {
  const reduce = useReducedMotion();
  const cards = DEMO_CARDS.filter(c => c.subject === sub);
  const subjectLabel = MARKBANK_SUBTABS.find(s => s.id === sub)?.label ?? sub;

  const [view, setView] = useState<View>(RESET);
  const [interacted, setInteracted] = useState(false);
  const [, setTick] = useState(0);

  const rootRef = useRef<HTMLDivElement>(null);
  const scrollerRef = useRef<HTMLDivElement>(null);
  const schemeRef = useRef<HTMLDivElement>(null);
  const questionRef = useRef<HTMLParagraphElement>(null);
  const flipRef = useRef<HTMLSpanElement>(null);
  const gotRef = useRef<HTMLSpanElement>(null);
  const nextRef = useRef<HTMLSpanElement>(null);
  const countRef = useRef(cards.length);
  countRef.current = cards.length;
  /** Set when a transition came from the visitor's own click, so focus follows it. The cursor never sets it. */
  const byHandRef = useRef(false);

  // New subject: back to its first card, question side up.
  useLayoutEffect(() => { setView(RESET); }, [sub]);

  const index = cards.length ? Math.min(view.index, cards.length - 1) : 0;
  const card: DemoCard | undefined = cards[index];
  const hasCard = card !== undefined;

  // --- transitions (guarded, so a repeated scripted arrival is a no-op) ---
  const flip = useCallback(() => setView(v => (v.phase === 'question' ? { ...v, phase: 'scheme' } : v)), []);
  const unflip = useCallback(() => setView(v => (v.phase === 'scheme' ? { ...v, phase: 'question', choice: null } : v)), []);
  const score = useCallback((choice: Choice) => setView(v => (v.phase === 'scheme' ? { ...v, phase: 'scored', choice } : v)), []);
  const next = useCallback(() => setView(v => {
    if (v.phase !== 'scored') return v;
    const count = Math.max(countRef.current, 1);
    return { index: (v.index + 1) % count, phase: 'question', choice: null };
  }), []);
  const byHand = (fn: () => void) => () => { byHandRef.current = true; fn(); };

  // A hand-driven transition unmounts the button that had focus; put focus
  // where the visitor is now (the revealed scheme, "Next card", or the next
  // question's button) so keyboard users are not dropped back to the top of
  // the page. Only the demo's own scroller moves, never the window.
  useEffect(() => {
    if (!byHandRef.current) return;
    byHandRef.current = false;
    const target: HTMLElement | null | undefined = view.phase === 'question'
      ? flipRef.current?.querySelector('button')
      : view.phase === 'scheme' ? schemeRef.current : nextRef.current?.querySelector('button');
    target?.focus({ preventScroll: true });
    reveal(scrollerRef.current, target);
  }, [view.phase, index]);

  // --- the scripted cursor ---
  // ScriptedCursor restarts its timers whenever the `steps` array changes
  // identity, so the array is built once and the measured positions are
  // written into it in place; a tick re-renders the cursor with the new
  // numbers without restarting its script. Step 0 is the "answer it in your
  // head" beat: the cursor rests beside the question, no click, before it
  // goes for the reveal.
  const stepsRef = useRef<CursorStep[]>([
    { x: 50, y: 50, click: false, hold: 2600 },
    { x: 50, y: 50, click: true, hold: 2400, onArrive: flip },
    { x: 50, y: 50, click: true, hold: 1400, onArrive: () => score('got') },
    { x: 50, y: 50, click: true, hold: 900, onArrive: next },
  ]);

  const measure = useCallback(() => {
    const root = rootRef.current;
    if (!root) return;
    const r = root.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    let changed = false;
    const put = (k: number, px: number, py: number) => {
      const x = clamp(((px - r.left) / r.width) * 100, 0, 100);
      const y = clamp(((py - r.top) / r.height) * 100, 0, 100);
      const s = stepsRef.current[k];
      if (Math.abs(s.x - x) > POS_EPS || Math.abs(s.y - y) > POS_EPS) { s.x = x; s.y = y; changed = true; }
    };
    // The rest: just past the question's right edge, kept inside the root so
    // the cursor never sits in the clipped margin on a narrow phone.
    const q = questionRef.current;
    if (q) {
      const b = q.getBoundingClientRect();
      put(0, clamp(b.right + REST_GAP, r.left, r.right - CURSOR_W), b.top + b.height * 0.5);
    }
    [flipRef, gotRef, nextRef].forEach((target, k) => {
      const el = target.current;
      if (!el) return;
      const b = el.getBoundingClientRect();
      put(k + 1, b.left + b.width * 0.42, b.top + b.height * 0.45);
    });
    if (changed) setTick(t => t + 1);
  }, []);

  const stop = useCallback(() => { if (!interacted) setInteracted(true); }, [interacted]);
  const playing = active && !interacted && !reduce && cards.length > 0;
  const playingRef = useRef(playing);
  playingRef.current = playing;

  // Before the cursor sets off: a new question starts at the top of the
  // card; while the script is running, the button it is about to press is
  // brought on-stage. Then measure so the step positions are right. Read
  // through a ref so the tap that stops the script does not re-run this.
  useLayoutEffect(() => {
    const scroller = scrollerRef.current;
    if (scroller) {
      if (view.phase === 'question') scroller.scrollTop = 0;
      else if (playingRef.current) reveal(scroller, (view.phase === 'scheme' ? gotRef : nextRef).current);
    }
    measure();
  }, [measure, view.phase, index, sub]);

  useEffect(() => {
    const root = rootRef.current;
    const scroller = scrollerRef.current;
    if (!root || !scroller) return;
    const ro = typeof ResizeObserver !== 'undefined' ? new ResizeObserver(() => measure()) : null;
    ro?.observe(root);
    scroller.addEventListener('scroll', measure, { passive: true });
    window.addEventListener('resize', measure);
    return () => { ro?.disconnect(); scroller.removeEventListener('scroll', measure); window.removeEventListener('resize', measure); };
  }, [measure, hasCard]);

  if (!card) {
    return <div ref={rootRef} className="h-full w-full flex flex-col justify-center" />;
  }

  const rise = (delay = 0) => (reduce
    ? { initial: false as const }
    : { initial: { opacity: 0, y: 8 }, animate: { opacity: 1, y: 0 }, transition: { duration: 0.32, delay, ease: EASE } });
  const showScheme = view.phase !== 'question';

  return (
    <div
      ref={rootRef}
      className="h-full w-full flex flex-col justify-center"
      style={{ position: 'relative', overflow: 'hidden' }}
      onPointerDownCapture={stop}
      onKeyDownCapture={stop}
    >
      {/* The stage grows with the card; when a parent does fix its height, this scroller clips and scrolls instead of the page. */}
      <div ref={scrollerRef} className="landing-strip flex-1 min-h-0 w-full" style={{ overflowY: 'auto', overflowX: 'hidden' }}>
        <div className="min-h-full flex flex-col items-center px-4 py-5 sm:px-8 sm:py-8">
          <div className="w-full flex-1 flex flex-col justify-center" style={{ maxWidth: CARD_MAX }}>
            {/* Meta line */}
            <div className="flex items-baseline justify-between gap-3 flex-wrap">
              <span style={META}>
                <span style={{ textTransform: 'none' }}>{card.year}</span> · {card.level} · <span style={{ textTransform: 'none' }}>{questionPart(card.ref)}</span> · {card.marks} {MB.marks}
              </span>
              <span style={META}>{card.subjectLabel}</span>
            </div>

            {/* Question */}
            <MotionDiv key={card.id} {...rise()} style={{ marginTop: 14 }}>
              <p
                ref={questionRef}
                className="m-0"
                style={{ fontFamily: FONT.serif, fontWeight: 600, fontSize: 'clamp(22px, 2.8vw, 32px)', lineHeight: 1.2, letterSpacing: '-0.01em', color: L.ink, overflowWrap: 'anywhere' }}
              >
                {card.question}
              </p>
            </MotionDiv>

            {/* Question side */}
            {view.phase === 'question' && (
              <MotionDiv {...rise()} className="flex flex-col items-start gap-3" style={{ marginTop: 22 }}>
                <span ref={flipRef} className="inline-flex">
                  <Button variant="secondary" onClick={byHand(flip)}>{MB.flip}</Button>
                </span>
                <p className="m-0" style={{ fontFamily: FONT.sans, fontSize: 13, color: L.faint, lineHeight: 1.4 }}>{MB.hint}</p>
              </MotionDiv>
            )}

            {/* Scheme side: rows, citation, then the self-score or the result.
                The live region stays mounted so the reveal is announced. */}
            <div aria-live="polite">
            {showScheme && (
              <div ref={schemeRef} tabIndex={-1} style={{ marginTop: 18, outline: 'none' }}>
                <div role="list" style={{ borderBottom: `1px solid ${L.hairline}` }}>
                  <AnimatePresence initial={!reduce}>
                    {card.rows.map((row, i) => {
                      const q = QUALIFIER[row.kind];
                      return (
                        <MotionDiv
                          key={`${card.id}-${i}`}
                          role="listitem"
                          {...rise(i * 0.06)}
                          className="flex items-baseline gap-3"
                          style={{ borderTop: `1px solid ${L.hairline}`, padding: '10px 0' }}
                        >
                          <span className="flex items-baseline gap-3 flex-1 min-w-0">
                            {q && <span style={{ ...META, whiteSpace: 'nowrap', flexShrink: 0 }}>{q}</span>}
                            <span style={{ fontFamily: FONT.sans, fontSize: 15, lineHeight: 1.5, color: L.ink, overflowWrap: 'anywhere' }}>{row.text}</span>
                          </span>
                          <span style={{ fontFamily: FONT.mono, fontSize: 12, color: L.ink, whiteSpace: 'nowrap', fontVariantNumeric: 'tabular-nums', flexShrink: 0 }}>
                            {row.marks} {MB.markShort}
                          </span>
                        </MotionDiv>
                      );
                    })}
                  </AnimatePresence>
                </div>
                <MotionDiv {...rise(card.rows.length * 0.06)}>
                  <p className="m-0" style={{ fontFamily: FONT.sans, fontSize: 11, lineHeight: 1.45, color: L.faint, marginTop: 10 }}>{card.citation}</p>
                </MotionDiv>

                {view.phase === 'scheme' && (
                  <MotionDiv {...rise(card.rows.length * 0.06 + 0.06)} style={{ marginTop: 20 }}>
                    <p className="m-0" style={{ fontFamily: FONT.sans, fontSize: 15, color: L.ink, fontWeight: 600, lineHeight: 1.4 }}>{MB.scoreSelf}</p>
                    <div className="flex flex-wrap items-center gap-x-3 gap-y-3" style={{ marginTop: 12 }}>
                      <span ref={gotRef} className="inline-flex">
                        <Button variant="secondary" onClick={byHand(() => score('got'))}>{MB.got}</Button>
                      </span>
                      <Button variant="secondary" onClick={byHand(() => score('shaky'))}>{MB.shaky}</Button>
                      <Button variant="secondary" onClick={byHand(() => score('missed'))}>{MB.missed}</Button>
                      <Button variant="ghost" onClick={byHand(unflip)}>{MB.back}</Button>
                    </div>
                  </MotionDiv>
                )}

                {view.phase === 'scored' && view.choice && (
                  <MotionDiv {...rise()} className="flex flex-wrap items-center justify-between gap-x-6 gap-y-3" style={{ marginTop: 20 }}>
                    <p className="m-0" style={{ fontFamily: FONT.serif, fontStyle: 'italic', fontSize: 17, lineHeight: 1.4, color: L.ink }}>{NOTE[view.choice]}</p>
                    <span ref={nextRef} className="inline-flex">
                      <Button variant="ink" onClick={byHand(next)}>{MB.next}</Button>
                    </span>
                  </MotionDiv>
                )}
              </div>
            )}
            </div>
          </div>

          {/* Progress line */}
          <p className="m-0 w-full" style={{ ...META, maxWidth: CARD_MAX, paddingTop: 20, fontVariantNumeric: 'tabular-nums' }}>
            {MB.card} {index + 1} {MB.of} {cards.length} · {subjectLabel}
          </p>
        </div>
      </div>

      {playing && <ScriptedCursor key={sub} steps={stepsRef.current} playing={playing} travel={650} />}
    </div>
  );
};

export default MarkBankDemo;
