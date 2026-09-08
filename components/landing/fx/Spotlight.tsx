/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The marking scheme under the question. Chapter I's frame is a real exam
 * page — 2025 Biology Higher, Section A, Question 6 (a)–(d), lifted from the
 * Mark Bank deck (question text from the paper, marking points from the
 * scheme, never typed here). Two identical sheets are stacked: the plain
 * question, and the same sheet with the examiner's ticks, answers and marks
 * in orange. The marked sheet is masked to a soft circle that follows the
 * pointer (springs on --x/--y, written in one rAF), so only under the lens
 * do you see what the examiner saw. A real "Show marking" toggle reveals
 * the whole sheet for touch, keyboard and reduced motion; the scheme is also
 * exposed to assistive tech through a hidden list the toggle controls.
 */

import React, { useEffect, useRef, useState } from 'react';
import { useMotionValue, useSpring } from 'framer-motion';
import { useReducedMotion } from '../../Motion';
import { COPY } from '../copy';
import { FONT, L } from '../theme';
import { isStatic } from './env';

/** The parts of Question 6 the frame shows, in paper order. */
const IDS = ['bio-2025-hl-q6-a', 'bio-2025-hl-q6-b', 'bio-2025-hl-q6-c', 'bio-2025-hl-q6-d'];

interface Row { verbatim: string; marks: number }
interface CardLike {
  id: string; year: number; level: string; section: string; questionRef: string;
  stem?: string; questionText: string; totalMarks: number; rows?: Row[];
  figure?: { src: string; alt: string; attribution?: string }; schemeCitation?: string;
}
interface Sheet {
  head: string; stem: string; parts: { letter: string; text: string; rows: Row[] }[];
  figure?: { src: string; alt: string; attribution?: string }; total: number; citation: string;
}

const LEVEL: Record<string, string> = { higher: 'Higher Level', ordinary: 'Ordinary Level' };

const assemble = (cards: CardLike[]): Sheet | null => {
  const picked = IDS.map(id => cards.find(c => c.id === id)).filter((c): c is CardLike => Boolean(c));
  if (picked.length !== IDS.length) return null;
  const first = picked[0];
  const q = /Q(\d+)/.exec(first.questionRef)?.[1] ?? '';
  const letters = picked.map(c => /\(([a-z])\)/.exec(c.questionRef)?.[1] ?? '');
  return {
    head: `${first.year} · ${LEVEL[first.level] ?? first.level} · Section ${first.section} · Question ${q} (${letters[0]})–(${letters[letters.length - 1]})`,
    stem: first.stem ?? '',
    parts: picked.map((c, i) => ({ letter: letters[i], text: c.questionText, rows: c.rows ?? [] })),
    figure: first.figure,
    total: picked.reduce((n, c) => n + c.totalMarks, 0),
    citation: first.schemeCitation ?? '',
  };
};

/** One sheet of the question. `marked` adds the examiner's layer; the layout is identical either way. */
const Paper: React.FC<{ sheet: Sheet; marked: boolean }> = ({ sheet, marked }) => (
  <div className="fx-sheet">
    <div style={{ fontFamily: FONT.mono, fontSize: 10, letterSpacing: '0.14em', textTransform: 'uppercase', color: L.faint, lineHeight: '28px' }}>{sheet.head}</div>
    <div className="fx-sheet-grid">
      {sheet.figure && (
        <div className="fx-sheet-fig">
          <img src={sheet.figure.src} alt={marked ? '' : sheet.figure.alt} loading="lazy" draggable={false} />
        </div>
      )}
      <div>
        {sheet.stem && <p style={{ fontFamily: FONT.serif, fontSize: 15, lineHeight: '28px', margin: 0, color: L.ink }}>{sheet.stem}</p>}
        <ol style={{ listStyle: 'none', margin: 0, padding: 0 }}>
          {sheet.parts.map(p => (
            <li key={p.letter} style={{ marginTop: 8 }}>
              <p style={{ fontFamily: FONT.serif, fontSize: 15, lineHeight: '28px', margin: 0, color: L.ink }}>
                <span style={{ display: 'inline-block', width: 26 }}>({p.letter})</span>{p.text}
              </p>
              {p.rows.map(r => (
                <div key={r.verbatim} className={`fx-sheet-line${r.verbatim.length > 34 ? ' fx-sheet-line--tall' : ''}`} style={{ marginLeft: 26 }}>
                  {marked && <span className="fx-sheet-ans"><span className="fx-sheet-tick" aria-hidden="true">✓</span>{r.verbatim}</span>}
                  <span className="fx-sheet-marks">{marked ? r.marks : ''}</span>
                </div>
              ))}
            </li>
          ))}
        </ol>
      </div>
    </div>
    <div className="fx-sheet-foot">
      <span>{sheet.figure?.attribution}</span>
      <span style={{ color: marked ? L.orangeText : L.faint, fontWeight: marked ? 700 : 400 }}>{marked ? `${sheet.total} / ${sheet.total}` : `${sheet.total} marks`}</span>
    </div>
  </div>
);

export const Spotlight: React.FC = () => {
  const [sheet, setSheet] = useState<Sheet | null>(null);
  const [on, setOn] = useState(false);
  const reduce = useReducedMotion();
  const marked = useRef<HTMLDivElement>(null);
  const x = useMotionValue(0);
  const y = useMotionValue(0);
  const sx = useSpring(x, { stiffness: 380, damping: 34, mass: 0.5 });
  const sy = useSpring(y, { stiffness: 380, damping: 34, mass: 0.5 });
  const lens = !reduce && !isStatic();

  // The deck is lazy, like the Mark Bank's own loader; only the four parts are kept.
  useEffect(() => {
    let live = true;
    import('../../MarkBank/cards/biology/higher')
      .then(m => { if (live) setSheet(assemble(m.CARDS as unknown as CardLike[])); })
      .catch(() => undefined);
    return () => { live = false; };
  }, []);

  // Both spring outputs land in one style write per frame.
  useEffect(() => {
    const el = marked.current;
    if (!el || !lens) return;
    let raf = 0;
    const flush = () => {
      raf = 0;
      el.style.setProperty('--fx-x', `${sx.get().toFixed(1)}px`);
      el.style.setProperty('--fx-y', `${sy.get().toFixed(1)}px`);
    };
    const req = () => { if (!raf) raf = requestAnimationFrame(flush); };
    const offX = sx.on('change', req);
    const offY = sy.on('change', req);
    return () => { offX(); offY(); if (raf) cancelAnimationFrame(raf); };
  }, [sx, sy, lens, sheet]);

  const at = (e: React.PointerEvent<HTMLDivElement>) => {
    const r = e.currentTarget.getBoundingClientRect();
    return [e.clientX - r.left, e.clientY - r.top] as const;
  };
  const enter = (e: React.PointerEvent<HTMLDivElement>) => {
    if (!lens || e.pointerType !== 'mouse') return;
    const [px, py] = at(e);
    x.jump(px); y.jump(py);
    marked.current?.style.setProperty('--fx-r', '140px');
  };
  const move = (e: React.PointerEvent<HTMLDivElement>) => {
    if (!lens || e.pointerType !== 'mouse') return;
    const [px, py] = at(e);
    x.set(px); y.set(py);
  };
  const leave = () => marked.current?.style.setProperty('--fx-r', '0px');

  const t = COPY.chapters.spotlight;
  if (!sheet) return <div className="fx-sheet" style={{ minHeight: 520 }} aria-busy="true" />;
  return (
    <>
      <div className={`fx-spot${on ? ' fx-spot--on' : ''}${lens ? '' : ' fx-spot--nolens'}`} onPointerEnter={enter} onPointerMove={move} onPointerLeave={leave}>
        <Paper sheet={sheet} marked={false} />
        <div ref={marked} className="fx-spot-marked" aria-hidden="true"><Paper sheet={sheet} marked /></div>
      </div>
      <div className="fx-spot-bar">
        <button type="button" className="fx-spot-toggle" aria-pressed={on} aria-controls="fx-spot-scheme" onClick={() => setOn(v => !v)}>{on ? t.hide : t.show}</button>
        <span className="fx-spot-hint" hidden={on || !lens}>{t.hint}</span>
      </div>
      <div id="fx-spot-scheme" className="fx-sr" hidden={!on}>
        <p>{t.scheme}</p>
        <ul>
          {sheet.parts.map(p => p.rows.map(r => <li key={`${p.letter}-${r.verbatim}`}>({p.letter}) {r.verbatim} — {r.marks} {r.marks === 1 ? 'mark' : 'marks'}</li>))}
        </ul>
        <p>{sheet.citation}</p>
      </div>
    </>
  );
};

export default Spotlight;
