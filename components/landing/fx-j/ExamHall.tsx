/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The exam hall: the takeover a "Sit this paper" press opens. A full-window
 * dialog portalled to <body> (the page's <main> paints in a containment,
 * so a fixed layer inside it would be clipped). While it is open the page
 * behind is inert, scroll is locked (Lenis paused, html overflow hidden),
 * focus stays inside, and Escape leaves.
 *
 * Opening (OPEN_MS, CSS animations in fx-j.css keyed on data-phase): the
 * lights go grey and the page recedes, the desk edge draws in from the
 * left, the paper lands face-down and turns face-up — the real first page —
 * then the clock, the paper's own instructions and "You may begin." Then
 * silence: nothing moves but the clock, which counts the sitting's printed
 * length down from that moment. Ending (CLOSE_MS): "Pens down.", the paper
 * is collected up the desk, the clock stops, the lights come back and the
 * layer is gone. The clock running out runs the same ending on its own.
 * Reduced motion (read once as the hall opens) and ?static=1 carry
 * data-instant: every state at once.
 */

import React, { useCallback, useEffect, useId, useLayoutEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { Button } from '../primitives';
import { getLenis } from '../scroll';
import { isStatic } from '../fx/env';
import { STACK_PAGE, type StackPaper } from '../fx-c/papers';
import { type HallCover } from './covers';
import { clockFace, durationWords } from './time';
import './fx-j.css';

/** Lights 0–600, desk edge 300–1000, the paper lands 700–1220 and turns 1400–2100, the line rises 2100–2700. */
export const OPEN_MS = 2200;
/** "Pens down." at 0, the paper collected 300–1000, the lights back from 900. */
const LIGHTS_MS = 900;
export const CLOSE_MS = 1700;

type Phase = 'opening' | 'open' | 'closing';

export const TEXT = {
  begin: 'You may begin.',
  down: 'Pens down.',
  leave: 'Leave the hall',
  hall: 'Exam hall',
  cover: 'From the cover',
  page: (n: number) => `From page ${n}`,
  running: (words: string) => `The clock is running: ${words}.`,
} as const;

export const attribution = (p: StackPaper): string => `SEC Leaving Certificate ${p.subject} ${p.year} ${p.level} — © State Examinations Commission`;

const FOCUSABLE = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';

/** Read once, as the hall opens: Framer's useReducedMotion is null on a first render, which would run the opening twice. */
const prefersReducedMotion = (): boolean => typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

interface Props {
  paper: StackPaper;
  cover: HallCover;
  /** The layer has finished its ending (or was instant) and can be unmounted. */
  onClosed: () => void;
}

const ExamHall: React.FC<Props> = ({ paper, cover, onClosed }) => {
  const [instant] = useState(() => prefersReducedMotion() || isStatic());
  const layerRef = useRef<HTMLDivElement>(null);
  const titleId = useId();
  const [phase, setPhase] = useState<Phase>('opening');
  const [face, setFace] = useState(() => clockFace(cover.minutes * 60_000));
  const [status, setStatus] = useState('');
  const deadline = useRef<number | null>(null);

  const leave = useCallback(() => setPhase(p => (p === 'closing' ? p : 'closing')), []);

  // The document while the hall is open: the page recedes, nothing behind it scrolls or takes focus.
  useLayoutEffect(() => {
    const html = document.documentElement;
    const layer = layerRef.current;
    const prevOverflow = html.style.overflow;
    html.style.setProperty('--hall-oy', `${Math.round(window.scrollY + window.innerHeight / 2)}px`);
    html.classList.add('landing-hall-open');
    if (instant) html.classList.add('landing-hall-instant');
    void html.offsetHeight; // flush, so the recede is a transition rather than a jump
    html.classList.add('landing-hall-receded');
    html.style.overflow = 'hidden';
    getLenis()?.stop();
    const made: Element[] = [];
    for (const el of Array.from(document.body.children)) {
      if (el === layer || el.hasAttribute('inert')) continue;
      el.setAttribute('inert', '');
      made.push(el);
    }
    layer?.focus({ preventScroll: true });
    return () => {
      // Full size first, under the hall's own transition rule (none when instant), then the rest.
      html.classList.remove('landing-hall-receded');
      void html.offsetHeight;
      html.classList.remove('landing-hall-open', 'landing-hall-instant');
      html.style.removeProperty('--hall-oy');
      html.style.overflow = prevOverflow;
      getLenis()?.start();
      for (const el of made) el.removeAttribute('inert');
    };
  }, [instant]);

  // Opening → open, once the paper has turned.
  useEffect(() => {
    if (instant) { setPhase(p => (p === 'opening' ? 'open' : p)); return; }
    const t = window.setTimeout(() => setPhase(p => (p === 'opening' ? 'open' : p)), OPEN_MS);
    return () => window.clearTimeout(t);
  }, [instant]);

  // The clock: counts down from the moment you begin; running out runs the ending.
  useEffect(() => {
    if (phase !== 'open') return;
    deadline.current = Date.now() + cover.minutes * 60_000;
    setStatus(TEXT.running(durationWords(cover.minutes)));
    const id = window.setInterval(() => {
      const left = (deadline.current ?? 0) - Date.now();
      setFace(clockFace(left));
      if (left <= 0) { window.clearInterval(id); leave(); }
    }, 200);
    return () => window.clearInterval(id);
  }, [phase, cover.minutes, leave]);

  // The ending: the lights come back part-way, then the layer is done.
  useEffect(() => {
    if (phase !== 'closing') return;
    setStatus(TEXT.down);
    if (instant) { onClosed(); return; }
    const a = window.setTimeout(() => document.documentElement.classList.remove('landing-hall-receded'), LIGHTS_MS);
    const b = window.setTimeout(onClosed, CLOSE_MS);
    return () => { window.clearTimeout(a); window.clearTimeout(b); };
  }, [phase, instant, onClosed]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') { e.preventDefault(); leave(); } };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [leave]);

  // Tab stays in the hall.
  const onKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key !== 'Tab') return;
    const root = layerRef.current;
    if (!root) return;
    const nodes = Array.from(root.querySelectorAll<HTMLElement>(FOCUSABLE)).filter(n => !n.hasAttribute('disabled'));
    if (!nodes.length) { e.preventDefault(); return; }
    const first = nodes[0];
    const last = nodes[nodes.length - 1];
    const active = document.activeElement;
    if (e.shiftKey && (active === first || active === root)) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && (active === last || active === root)) { e.preventDefault(); first.focus(); }
  };

  const ga = cover.id === 'irish' ? 'ga' : undefined;
  const closing = phase === 'closing';

  return createPortal(
    <div
      ref={layerRef}
      className="hall"
      data-phase={phase}
      data-instant={instant || undefined}
      role="dialog"
      aria-modal="true"
      aria-labelledby={titleId}
      tabIndex={-1}
      onKeyDown={onKeyDown}
    >
      <div className="hall__lights" aria-hidden="true" />
      <div className="hall__room">
        <h2 id={titleId} className="sr-only">{TEXT.hall}: {paper.subject}, {paper.level}, {paper.year}{paper.part ? `, ${paper.part}` : ''}</h2>
        <header className="hall__wall">
          <p className="hall__clock" role="timer" aria-live="off" aria-label={`Time left ${face}`}>{face}</p>
          <p className="hall__sitting" lang={ga}>{cover.sitting}{cover.marks ? ` · ${cover.marks}` : ''}</p>
        </header>
        <span className="hall__edge" aria-hidden="true" />
        <div className="hall__desk">
          <div className="hall__paper">
            <div className="hall__sheet">
              <img
                className="hall__face hall__face--front"
                src={paper.src}
                alt={`${paper.subject}, ${paper.level}, ${paper.year}: the first page of the paper`}
                width={STACK_PAGE.width}
                height={STACK_PAGE.height}
                decoding="async"
                draggable={false}
              />
              <div className="hall__face hall__face--back" aria-hidden="true" />
            </div>
          </div>
          <div className="hall__notes">
            <p key={closing ? 'down' : 'begin'} className="hall__begin">{closing ? TEXT.down : TEXT.begin}</p>
            <ul className="hall__instructions" lang={ga} aria-label="The paper’s instructions">
              {cover.instructions.map((line, i) => <li key={i}>{line}</li>)}
            </ul>
            <p className="hall__source">{cover.instructionsPage === 1 ? TEXT.cover : TEXT.page(cover.instructionsPage)} · {attribution(paper)}</p>
          </div>
        </div>
        <div className="hall__leave">
          <Button variant="secondary" size="sm" onClick={leave}>{TEXT.leave}</Button>
        </div>
      </div>
      <p className="sr-only" role="status" aria-live="polite">{status}</p>
    </div>,
    document.body,
  );
};

export default ExamHall;
