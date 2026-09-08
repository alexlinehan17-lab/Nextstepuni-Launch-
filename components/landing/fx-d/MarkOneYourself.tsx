/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark one yourself. The marking scheme's points, as chips carrying their
 * marks, and the scheme's own possible response to a different question,
 * one line per point in a fixed shuffled order. Drag a chip onto the line
 * that earns it: a right drop ticks the line in orange and tallies the
 * marks; a wrong one shakes the line and the chip returns. Keyboard: select
 * a chip (Enter or Space), then a line. When every point is placed, the
 * total and the attribution. Drag is pointer events with capture, so it is
 * the same on a mouse, a trackpad and a thumb; the chip moves by transform
 * so the tray never reflows.
 */

import React, { useRef, useState } from 'react';
import { useReducedMotion } from '../../Motion';
import { Button, Frame } from '../primitives';
import { L } from '../theme';
import { isStatic } from '../fx/env';
import { PLACE } from './examinerData';

const TEXT = {
  frame: 'Mark one yourself',
  tray: 'The scheme’s points',
  hint: 'Drag a point onto the line that earns it — or select it, then the line.',
  lines: 'The scheme’s own answer',
  placedOn: 'placed',
  marks: 'marks',
  wrong: 'Not that line',
  full: 'Full marks',
  again: 'Start again',
  total: 'total',
} as const;

/** A fixed shuffle of the scheme's lines — presentation only; the words and their points are the scheme's. */
const ORDER = [2, 0, 3, 1];
const SHAKE_MS = 340;
const DRAG_THRESHOLD = 4;
/** Auto-scroll band at the bottom of the viewport, and under the 68px nav at the top, in px; and the most one move scrolls. */
const EDGE = 72;
const NAV_EDGE = 68 + 48;
const EDGE_STEP = 14;

interface Drag { id: string; dx: number; dy: number; moved: boolean }

const MarkOneYourself: React.FC = () => {
  const q = PLACE;
  const lines = ORDER.map(i => q.lines[i]).filter(Boolean);
  const [placed, setPlaced] = useState<Record<string, string>>({});
  const [selected, setSelected] = useState<string | null>(null);
  const [drag, setDrag] = useState<Drag | null>(null);
  const [over, setOver] = useState<string | null>(null);
  const [shaking, setShaking] = useState<string | null>(null);
  const [returning, setReturning] = useState<string | null>(null);
  const [live, setLive] = useState('');
  const start = useRef<{ x: number; y: number; sy: number } | null>(null);
  const reduce = useReducedMotion();
  const instant = reduce || isStatic();

  const done = Object.keys(placed).length === q.points.length;
  const earned = q.points.filter(p => placed[p.id]).reduce((n, p) => n + p.marks, 0);
  const pointOf = (id: string) => q.points.find(p => p.id === id);

  const attempt = (pointId: string, lineId: string) => {
    const line = lines.find(l => l.id === lineId);
    const point = pointOf(pointId);
    if (!line || !point || placed[pointId]) return;
    if (Object.values(placed).includes(lineId)) return;
    if (line.pointId === pointId) {
      setPlaced(p => ({ ...p, [pointId]: lineId }));
      setSelected(null);
      setLive(`${point.label} ${TEXT.placedOn} — ${point.marks} ${TEXT.marks}`);
    } else {
      setShaking(lineId);
      window.setTimeout(() => setShaking(s => (s === lineId ? null : s)), SHAKE_MS);
      setLive(TEXT.wrong);
    }
  };

  const dropAt = (x: number, y: number): string | null => {
    const el = document.elementsFromPoint(x, y).find(e => (e as HTMLElement).dataset?.drop) as HTMLElement | undefined;
    return el?.dataset.drop ?? null;
  };

  const onPointerDown = (e: React.PointerEvent<HTMLButtonElement>, id: string) => {
    if (placed[id] || e.button !== 0) return;
    e.currentTarget.setPointerCapture(e.pointerId);
    start.current = { x: e.clientX, y: e.clientY, sy: window.scrollY };
    setReturning(null);
    setDrag({ id, dx: 0, dy: 0, moved: false });
  };
  const onPointerMove = (e: React.PointerEvent<HTMLButtonElement>) => {
    if (!drag || !start.current) return;
    // A thumb near the viewport's edge scrolls the page under the chip (the chip itself blocks native scrolling), so a lower line is reachable.
    const vh = window.innerHeight;
    if (e.clientY > vh - EDGE) window.scrollBy(0, Math.min(EDGE_STEP, e.clientY - (vh - EDGE)));
    else if (e.clientY < NAV_EDGE) window.scrollBy(0, -Math.min(EDGE_STEP, NAV_EDGE - e.clientY));
    // The chip follows the pointer in page space: pointer travel plus whatever the page has scrolled since the grab.
    const dx = e.clientX - start.current.x, dy = e.clientY - start.current.y + (window.scrollY - start.current.sy);
    const moved = drag.moved || Math.hypot(dx, dy) > DRAG_THRESHOLD;
    setDrag({ ...drag, dx, dy, moved });
    setOver(moved ? dropAt(e.clientX, e.clientY) : null);
  };
  const onPointerUp = (e: React.PointerEvent<HTMLButtonElement>) => {
    if (!drag) return;
    const target = drag.moved ? dropAt(e.clientX, e.clientY) : null;
    if (drag.moved) {
      if (target) attempt(drag.id, target);
      setReturning(drag.id);
      window.setTimeout(() => setReturning(r => (r === drag.id ? null : r)), 300);
    } else {
      setSelected(s => (s === drag.id ? null : drag.id));
    }
    setDrag(null);
    setOver(null);
    start.current = null;
  };

  const reset = () => { setPlaced({}); setSelected(null); setLive(''); };

  return (
    <Frame title={TEXT.frame} meta={`${q.subject} · ${q.ref}`}>
      <div style={{ padding: '18px 20px', borderBottom: `1px solid ${L.hairline}` }}>
        <p className="fxd-q">{q.question}</p>
      </div>

      {/* The chips: the scheme's points with their marks */}
      <div className="fxd-mono" style={{ padding: '12px 14px 0' }}>{TEXT.tray} · {q.notation}</div>
      <div className="fxd-tray" role="group" aria-label={TEXT.tray}>
        {q.points.map(p => {
          const isPlaced = !!placed[p.id];
          const dragging = drag?.id === p.id && drag.moved;
          return (
            <button
              key={p.id}
              type="button"
              className={`fxd-chip ${dragging ? 'fxd-chip--drag' : ''} ${isPlaced ? 'fxd-chip--placed' : ''} ${returning === p.id && !instant ? 'fxd-chip--return' : ''}`}
              style={dragging ? { transform: `translate(${drag.dx}px, ${drag.dy}px)` } : undefined}
              aria-pressed={selected === p.id}
              aria-disabled={isPlaced || undefined}
              tabIndex={isPlaced ? -1 : 0}
              onPointerDown={e => onPointerDown(e, p.id)}
              onPointerMove={onPointerMove}
              onPointerUp={onPointerUp}
              onPointerCancel={() => { setDrag(null); setOver(null); start.current = null; }}
              onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); if (!isPlaced) setSelected(s => (s === p.id ? null : p.id)); } }}
            >
              <span>{p.label}</span>
              <span className="fxd-chip__marks">{p.marks}</span>
            </button>
          );
        })}
        <span className="fxd-hint hidden md:inline">{TEXT.hint}</span>
      </div>
      <p className="fxd-hint md:hidden" style={{ margin: 0, padding: '8px 14px 0' }}>{TEXT.hint}</p>

      {/* The lines: the scheme's own answer, each the drop for one point */}
      <div className="fxd-mono" style={{ padding: '14px 14px 6px' }}>{TEXT.lines}</div>
      <ol className="fxd-drops">
        {lines.map(line => {
          const placedPoint = q.points.find(p => placed[p.id] === line.id);
          const lineDone = !!placedPoint;
          return (
            <li key={line.id}>
              <button
                type="button"
                className={`fxd-drop ${over === line.id && !lineDone ? 'fxd-drop--over' : ''} ${selected && !lineDone ? 'fxd-drop--ready' : ''} ${lineDone ? 'fxd-drop--done' : ''} ${shaking === line.id ? 'fxd-shake' : ''}`}
                data-drop={lineDone ? undefined : line.id}
                aria-disabled={lineDone || undefined}
                onClick={() => { if (selected && !lineDone) attempt(selected, line.id); }}
              >
                <span className={`fxd-sq fxd-drop__sq ${lineDone ? 'fxd-sq--on fxd-sq--pop' : ''}`} aria-hidden="true" />
                <span>{line.text}</span>
                {placedPoint
                  ? <span className="fxd-drop__label">{placedPoint.label} · {placedPoint.marks}</span>
                  : <span className="fxd-drop__slot" aria-hidden="true" />}
              </button>
            </li>
          );
        })}
      </ol>

      <div style={{ padding: '4px 20px 18px' }}>
        <div className="fxd-total" role="status">
          <span className="fxd-total__n">{earned}</span>
          <span className="fxd-total__of">/ {q.total}</span>
          <span className="fxd-total__word">{done ? TEXT.full : `${q.total} ${TEXT.total}`}</span>
        </div>
        {done && <div className="mt-4"><Button variant="ghost" onClick={reset}>{TEXT.again}</Button></div>}
      </div>
      <div className="fxd-live" aria-live="polite">{live}</div>
      <div className="fxd-attrib">{q.attribution}</div>
    </Frame>
  );
};

export default MarkOneYourself;
