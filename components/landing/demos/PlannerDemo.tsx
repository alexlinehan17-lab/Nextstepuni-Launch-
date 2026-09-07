/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Planner playground demo. Two modes. "Today" is the app's stepped rail: a
 * hairline spine with one node per thing due, the current one ringed in
 * orange, and a Mark done button that walks the ring down the list while a
 * 3px bar under the header fills. "This week" is the ruled seven-column
 * week, which folds to a stacked list of collapsible days on small screens.
 * Echoes the app's own planner idioms — stepped rails for sequences, numbers
 * as identity, resume-first — and Brilliant's scripted cursor autoplays the
 * rail until the first real pointer, key or focus inside the demo.
 */

import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { AnimatePresence, MotionDiv, MotionSpan, useReducedMotion } from '../../Motion';
import { COPY } from '../copy';
import { PLANNER_WEEK, type PlanDay, type PlanItem } from '../demoData';
import { ScriptedCursor, type CursorStep } from '../motion';
import { Button } from '../primitives';
import type { DemoProps } from '../sections/Playground';
import { FONT, L } from '../theme';

export const PLANNER_SUBTABS: { id: string; label: string }[] = [
  { id: 'today', label: 'Today' },
  { id: 'week', label: 'This week' },
];

const T = COPY.playground.planner;
const EASE: [number, number, number, number] = [0.2, 0.8, 0.2, 1];
const TODAY_IDX = Math.max(0, PLANNER_WEEK.findIndex(d => d.today));

/** The typographic meta line: mono, uppercase, tracked, faint. */
const META: React.CSSProperties = { fontFamily: FONT.mono, fontSize: 11, letterSpacing: '0.14em', textTransform: 'uppercase', color: L.faint, lineHeight: 1.5 };
/** Minutes at the right of a row: mono, tabular, never uppercased. */
const MINS: React.CSSProperties = { fontFamily: FONT.mono, fontSize: 12, color: L.muted, fontVariantNumeric: 'tabular-nums', whiteSpace: 'nowrap', lineHeight: 1.5 };

type DoneSet = Set<string>;
const key = (di: number, ii: number) => `${di}:${ii}`;
const initialDone = (): DoneSet => {
  const s = new Set<string>();
  PLANNER_WEEK.forEach((d, di) => d.items.forEach((it, ii) => { if (it.done) s.add(key(di, ii)); }));
  return s;
};

const isDue = (it: PlanItem) => it.kind !== 'rest';
const isRestDay = (day: PlanDay) => day.items.every(it => it.kind === 'rest');
const sumMinutes = (items: PlanItem[]) => items.reduce((a, it) => a + it.minutes, 0);
const thingsLabel = (n: number) => `${n} ${n === 1 ? T.thing : T.things}`;
const minsLabel = (n: number) => `${n} ${T.minutes}`;

/** "2 things · 27 min" for a day; "2 done · 27 min" once everything on it is ticked. */
const daySummary = (day: PlanDay, di: number, done: DoneSet) => {
  const due = day.items.map((it, ii) => ({ it, ii })).filter(x => isDue(x.it));
  const open = due.filter(x => !done.has(key(di, x.ii)));
  const head = due.length > 0 && open.length === 0 ? `${due.length} ${T.done}` : thingsLabel(due.length);
  return `${head} · ${minsLabel(sumMinutes(due.map(x => x.it)))}`;
};

// ---------------------------------------------------------------------------
// Today — the stepped rail
// ---------------------------------------------------------------------------

type NodeState = 'done' | 'current' | 'upcoming';

/** One node on the spine. Done = ink disc with a paper tick; current = orange ring; upcoming = hairline hollow. */
const Node: React.FC<{ state: NodeState; reduce: boolean }> = ({ state, reduce }) => {
  const base: React.CSSProperties = {
    width: 22, height: 22, borderRadius: 999, boxSizing: 'border-box', flexShrink: 0,
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    transition: reduce ? undefined : 'background-color 220ms ease, border-color 220ms ease',
  };
  if (state === 'done') {
    return (
      <span aria-hidden="true" style={{ ...base, background: L.ink }}>
        <MotionSpan
          initial={reduce ? false : { scale: 0.4, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.22, ease: EASE }}
          style={{ display: 'block', color: L.paper, fontFamily: FONT.mono, fontSize: 12, lineHeight: 1 }}
        >
          ✓
        </MotionSpan>
      </span>
    );
  }
  if (state === 'current') return <span aria-hidden="true" style={{ ...base, background: L.paper, border: `2px solid ${L.orange}` }} />;
  return <span aria-hidden="true" style={{ ...base, background: L.paper, border: `1.5px solid ${L.hairline}` }} />;
};

const TodayRail: React.FC<{
  done: DoneSet;
  onMarkDone: () => void;
  reduce: boolean;
  btnRef: React.RefObject<HTMLDivElement | null>;
  doneLineRef: React.RefObject<HTMLDivElement | null>;
}> = ({ done, onMarkDone, reduce, btnRef, doneLineRef }) => {
  const today = PLANNER_WEEK[TODAY_IDX];
  const due = today.items.map((it, ii) => ({ it, ii })).filter(x => isDue(x.it));
  const remaining = due.filter(x => !done.has(key(TODAY_IDX, x.ii)));
  const currentIi = remaining.length > 0 ? remaining[0].ii : -1;
  const allDone = remaining.length === 0;
  const pct = due.length === 0 ? 100 : Math.round(((due.length - remaining.length) / due.length) * 100);
  const meta = [
    `${today.day} ${today.date}`,
    allDone ? `${due.length} ${T.done}` : `${thingsLabel(remaining.length)} ${T.due}`,
    minsLabel(sumMinutes((allDone ? due : remaining).map(x => x.it))),
  ].join(' · ');

  return (
    <div>
      <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
        <h3 className="m-0" style={{ fontFamily: FONT.serif, fontWeight: 600, fontSize: 'clamp(24px, 3vw, 30px)', lineHeight: 1.1, letterSpacing: '-0.015em', color: L.ink }}>{T.today}</h3>
        <p className="m-0" style={META}>{meta}</p>
      </div>

      {/* The one warm element: a 3px bar that fills as the day is worked through. */}
      <div
        role="progressbar"
        aria-label={T.today}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={pct}
        style={{ height: 3, background: L.hairline, marginTop: 14, overflow: 'hidden' }}
      >
        <MotionDiv
          initial={false}
          animate={{ width: `${pct}%` }}
          transition={{ duration: reduce ? 0 : 0.4, ease: EASE }}
          style={{ height: '100%', background: L.orange }}
        />
      </div>

      <ol className="m-0 p-0 list-none" style={{ marginTop: 26 }}>
        {today.items.map((it, ii) => {
          const isDone = done.has(key(TODAY_IDX, ii));
          const state: NodeState = isDone ? 'done' : ii === currentIi ? 'current' : 'upcoming';
          const last = ii === today.items.length - 1;
          const inkOrFaint = isDone ? L.faint : L.ink;
          return (
            <li key={ii} className="flex gap-4" aria-current={state === 'current' ? 'step' : undefined}>
              <div className="flex flex-col items-center" style={{ width: 22, flexShrink: 0 }}>
                <Node state={state} reduce={reduce} />
                {!last && <span aria-hidden="true" style={{ flex: 1, width: 1, minHeight: 16, background: L.hairline }} />}
              </div>
              <div className="min-w-0 flex-1" style={{ paddingBottom: last ? 0 : 24 }}>
                {it.kind === 'rest' ? (
                  <p className="m-0" style={{ fontFamily: FONT.serif, fontStyle: 'italic', fontSize: 16, lineHeight: 1.4, color: L.ink }}>{T.rest}</p>
                ) : (
                  <>
                    <div className="flex items-baseline justify-between gap-3">
                      <span className="min-w-0" style={{ fontFamily: FONT.sans, fontWeight: 600, fontSize: 15, lineHeight: 1.45, color: inkOrFaint, overflowWrap: 'anywhere' }}>
                        {it.subject}
                        {isDone && <span className="sr-only"> · {T.done}</span>}
                      </span>
                      <span style={{ ...MINS, color: isDone ? L.faint : L.muted }}>{minsLabel(it.minutes)}</span>
                    </div>
                    <p className="m-0" style={{ fontFamily: FONT.sans, fontSize: 14, lineHeight: 1.45, marginTop: 2, color: isDone ? L.faint : L.muted, overflowWrap: 'anywhere' }}>
                      {it.kind === 'paper' && <span style={{ ...META, marginRight: 8 }}>{T.paper}</span>}
                      {it.label}
                    </p>
                    {state === 'current' && (
                      <div ref={btnRef} className="inline-block" style={{ marginTop: 12 }}>
                        <Button variant="ink" onClick={onMarkDone}>{T.markDone}</Button>
                      </div>
                    )}
                  </>
                )}
              </div>
            </li>
          );
        })}
      </ol>

      <AnimatePresence>
        {allDone && (
          <MotionDiv
            key="all-done"
            initial={reduce ? false : { opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, ease: EASE }}
            style={{ marginTop: 28 }}
          >
            <div ref={doneLineRef} className="inline-block">
              <p className="m-0" style={{ fontFamily: FONT.serif, fontWeight: 600, fontSize: 22, lineHeight: 1.2, letterSpacing: '-0.01em', color: L.ink }}>{T.allDone}</p>
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
  );
};

// ---------------------------------------------------------------------------
// This week — the ruled grid, and the stacked list under lg
// ---------------------------------------------------------------------------

/** A two-line entry in the week: subject, then label. Done entries go faint and struck through with a tick. */
const WeekEntry: React.FC<{ it: PlanItem; isDone: boolean; dense: boolean }> = ({ it, isDone, dense }) => {
  if (it.kind === 'rest') {
    return <li style={{ fontFamily: FONT.serif, fontStyle: 'italic', fontSize: dense ? 13 : 15, lineHeight: 1.4, color: L.ink }}>{T.rest}</li>;
  }
  const colour = isDone ? L.faint : undefined;
  /** The strike sits on the words only — the tick and the minutes stay clean. */
  const struck: React.CSSProperties = isDone ? { textDecoration: 'line-through', textDecorationColor: L.faint } : {};
  return (
    <li>
      <div className="flex flex-wrap items-baseline justify-between gap-x-2">
        <span className="min-w-0" style={{ fontFamily: FONT.sans, fontWeight: 600, fontSize: dense ? 13 : 15, lineHeight: 1.35, color: colour ?? L.ink, overflowWrap: 'anywhere' }}>
          {isDone && <span aria-hidden="true" style={{ fontFamily: FONT.mono, marginRight: 5 }}>✓</span>}
          <span style={struck}>{it.subject}</span>
          {isDone && <span className="sr-only"> · {T.done}</span>}
        </span>
        <span style={{ ...MINS, fontSize: dense ? 11 : 12, color: colour ?? L.muted }}>{minsLabel(it.minutes)}</span>
      </div>
      <div style={{ fontFamily: FONT.sans, fontSize: dense ? 12 : 13, lineHeight: 1.4, marginTop: 1, color: colour ?? L.muted, overflowWrap: 'anywhere' }}>
        {it.kind === 'paper' && <span style={{ ...META, marginRight: 6 }}>{T.paper}</span>}
        <span style={struck}>{it.label}</span>
      </div>
    </li>
  );
};

const WeekView: React.FC<{ done: DoneSet; reduce: boolean }> = ({ done, reduce }) => {
  const [open, setOpen] = useState<Set<number>>(() => new Set([TODAY_IDX]));
  const toggle = (di: number) => setOpen(prev => {
    const next = new Set(prev);
    if (next.has(di)) next.delete(di); else next.add(di);
    return next;
  });

  const allDue = PLANNER_WEEK.flatMap(d => d.items.filter(isDue));
  const first = PLANNER_WEEK[0];
  const last = PLANNER_WEEK[PLANNER_WEEK.length - 1];
  const meta = `${first.date} – ${last.date} · ${thingsLabel(allDue.length)} · ${minsLabel(sumMinutes(allDue))}`;

  return (
    <div>
      <p className="m-0" style={META}>{meta}</p>

      {/* lg and up: seven ruled columns. */}
      <div className="hidden lg:grid lg:grid-cols-7" style={{ marginTop: 16 }}>
        {PLANNER_WEEK.map((day, di) => (
          <section
            key={day.day}
            aria-label={`${day.day} ${day.date}`}
            aria-current={day.today ? 'date' : undefined}
            style={{
              borderLeft: `1px solid ${L.hairline}`,
              borderTop: day.today ? `1.5px solid ${L.ink}` : `1px solid ${L.hairline}`,
              padding: '12px 10px 18px',
              minWidth: 0,
            }}
          >
            <header style={{ marginBottom: 12 }}>
              <div style={{ fontFamily: FONT.sans, fontWeight: 600, fontSize: 14, lineHeight: 1.2, color: day.today ? L.orangeText : L.ink }}>{day.day}</div>
              <div style={{ ...META, marginTop: 3, color: day.today ? L.orangeText : L.faint }}>{day.date}</div>
            </header>
            <ul className="m-0 p-0 list-none flex flex-col" style={{ gap: 12 }}>
              {day.items.map((it, ii) => <WeekEntry key={ii} it={it} isDone={done.has(key(di, ii))} dense />)}
            </ul>
          </section>
        ))}
      </div>

      {/* Under lg: a stacked list of days, today open, the rest a summary line that opens on tap. */}
      <div className="lg:hidden" style={{ marginTop: 14 }}>
        {PLANNER_WEEK.map((day, di) => {
          const rest = isRestDay(day);
          const isOpen = open.has(di);
          const dayLabel = (
            <span style={{ fontFamily: FONT.sans, fontWeight: 600, fontSize: 15, lineHeight: 1.35, color: day.today ? L.orangeText : L.ink }}>
              {day.day} {day.date}
            </span>
          );
          return (
            <div key={day.day} style={{ borderTop: `1px solid ${L.hairline}` }}>
              {rest ? (
                <div className="flex flex-wrap items-baseline justify-between gap-x-3 gap-y-1" style={{ padding: '12px 0' }}>
                  {dayLabel}
                  <span style={{ fontFamily: FONT.serif, fontStyle: 'italic', fontSize: 14, lineHeight: 1.4, color: L.ink, textAlign: 'right' }}>{T.rest}</span>
                </div>
              ) : (
                <button
                  type="button"
                  aria-expanded={isOpen}
                  onClick={() => toggle(di)}
                  className="flex w-full flex-wrap items-baseline justify-between gap-x-3 gap-y-1 text-left"
                  style={{ background: 'none', border: 0, padding: '12px 0', cursor: 'pointer', color: L.ink, fontFamily: FONT.sans }}
                >
                  {dayLabel}
                  <span style={{ ...META, whiteSpace: 'nowrap' }}>{daySummary(day, di, done)}</span>
                </button>
              )}
              <AnimatePresence initial={false}>
                {isOpen && !rest && (
                  <MotionDiv
                    key="items"
                    initial={reduce ? false : { height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={reduce ? undefined : { height: 0, opacity: 0 }}
                    transition={{ duration: 0.25, ease: EASE }}
                    style={{ overflow: 'hidden' }}
                  >
                    <ul className="m-0 p-0 list-none flex flex-col" style={{ gap: 12, paddingBottom: 16 }}>
                      {day.items.map((it, ii) => <WeekEntry key={ii} it={it} isDone={done.has(key(di, ii))} dense={false} />)}
                    </ul>
                  </MotionDiv>
                )}
              </AnimatePresence>
            </div>
          );
        })}
      </div>
    </div>
  );
};

// ---------------------------------------------------------------------------
// The demo
// ---------------------------------------------------------------------------

interface CursorTarget { x: number; y: number; click: boolean }
const INTRO_SPOT: CursorTarget = { x: 74, y: 26, click: false };
const sameTarget = (a: CursorTarget | null, b: CursorTarget) => !!a && a.x === b.x && a.y === b.y && a.click === b.click;

const PlannerDemo: React.FC<DemoProps> = ({ sub, active }) => {
  const reduce = useReducedMotion() === true;
  const mode: 'today' | 'week' = sub === 'week' ? 'week' : 'today';
  const [done, setDone] = useState<DoneSet>(initialDone);
  const [interacted, setInteracted] = useState(false);
  const [target, setTarget] = useState<CursorTarget | null>(null);
  const rootRef = useRef<HTMLDivElement>(null);
  const btnRef = useRef<HTMLDivElement>(null);
  const doneLineRef = useRef<HTMLDivElement>(null);

  const wantsAutoplay = active && mode === 'today' && !interacted && !reduce;
  const stop = useCallback(() => setInteracted(true), []);

  /** Tick the first thing on today's list that is not done yet. */
  const markDone = useCallback(() => {
    setDone(prev => {
      const day = PLANNER_WEEK[TODAY_IDX];
      const ii = day.items.findIndex((it, i) => isDue(it) && !prev.has(key(TODAY_IDX, i)));
      if (ii < 0) return prev;
      const next = new Set(prev);
      next.add(key(TODAY_IDX, ii));
      return next;
    });
  }, []);

  /** Where the cursor goes next, as a percent of the root: the Mark done button, or a resting spot beside the done line. */
  const measure = useCallback((): CursorTarget | null => {
    const root = rootRef.current;
    if (!root) return null;
    const r = root.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return null;
    const pct = (el: Element, fx: number, fy: number, dx = 0): CursorTarget => {
      const b = el.getBoundingClientRect();
      return {
        x: Math.round(((b.left + b.width * fx + dx - r.left) / r.width) * 1000) / 10,
        y: Math.round(((b.top + b.height * fy - r.top + root.scrollTop) / r.height) * 1000) / 10,
        click: false,
      };
    };
    if (btnRef.current) return { ...pct(btnRef.current, 0.5, 0.55), click: true };
    if (doneLineRef.current) { const t = pct(doneLineRef.current, 1, 0.5, 28); return { ...t, x: Math.min(t.x, 90) }; }
    return null;
  }, []);

  // Arm the autoplay 1600ms after the rail is showing; disarm whenever it should not run.
  useEffect(() => {
    if (!wantsAutoplay) { setTarget(null); return; }
    const t = window.setTimeout(() => setTarget(INTRO_SPOT), 1600);
    return () => window.clearTimeout(t);
  }, [wantsAutoplay]);

  // After each hold, look again: the button has moved down a row, or gone.
  const onLoop = useCallback(() => {
    const next = measure();
    if (!next) return;
    setTarget(prev => (sameTarget(prev, next) ? prev : next));
  }, [measure]);

  const steps = useMemo<CursorStep[]>(
    () => (target ? [{ x: target.x, y: target.y, click: target.click, hold: target.click ? 1800 : 250, onArrive: target.click ? markDone : undefined }] : []),
    [target, markDone],
  );
  const playing = wantsAutoplay && target !== null;

  return (
    <div
      ref={rootRef}
      className="h-full w-full"
      style={{ position: 'relative', overflowY: 'auto', overflowX: 'hidden' }}
      onPointerDownCapture={stop}
      onKeyDownCapture={stop}
      onFocusCapture={stop}
    >
      <MotionDiv
        key={mode}
        className="mx-auto px-5 py-6 sm:px-8 sm:py-8"
        style={{ maxWidth: mode === 'today' ? 640 : 1120 }}
        initial={reduce ? false : { opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.22, ease: 'easeOut' }}
      >
        {mode === 'today'
          ? <TodayRail done={done} onMarkDone={markDone} reduce={reduce} btnRef={btnRef} doneLineRef={doneLineRef} />
          : <WeekView done={done} reduce={reduce} />}
      </MotionDiv>
      <ScriptedCursor steps={steps} playing={playing} onLoop={onLoop} />
    </div>
  );
};

export default PlannerDemo;
