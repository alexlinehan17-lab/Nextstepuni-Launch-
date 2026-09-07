/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Landing-page motion. Four moves, each lifted from a reference and re-cut in
 * our register:
 *  - WordPop      — Shopify Design's hero: an ink square lands, the word appears.
 *  - CollapseWord — Leonardo's giant section word that folds away on scroll.
 *  - Reveal       — plain in-view rise for rows and frames.
 *  - Cursor       — Brilliant's scripted demo cursor.
 * All of it respects prefers-reduced-motion via the shared hook: static
 * render, no timers.
 */

import React, { useEffect, useMemo, useRef, useState } from 'react';
import { useInView, useScroll, useTransform } from 'framer-motion';
import { MotionDiv, MotionSpan, useReducedMotion } from '../Motion';
import { L } from './theme';

/** Split a headline into words, keeping the author's line breaks ("\n"). */
const tokenize = (text: string): { word: string; br: boolean }[] =>
  text.split('\n').flatMap((line, li) =>
    line.split(/\s+/).filter(Boolean).map((word, wi) => ({ word, br: li > 0 && wi === 0 })),
  );

/**
 * Word-by-word headline build. Each word gets a small ink square that lands
 * a beat before the word rises in beside it; the square blinks out once the
 * word has landed. Pass `accent` to paint one word in orange.
 */
export const WordPop: React.FC<{
  text: string;
  accentWord?: string;
  stagger?: number;
  delay?: number;
  className?: string;
  style?: React.CSSProperties;
  as?: 'h1' | 'h2' | 'p';
  /** Rendered inside the LAST word's box, absolutely positioned — for a character hanging off the headline. */
  tail?: React.ReactNode;
}> = ({ text, accentWord, stagger = 0.13, delay = 0.2, className = '', style, as = 'h1', tail }) => {
  const reduce = useReducedMotion();
  const tokens = useMemo(() => tokenize(text), [text]);
  const Tag = as;
  return (
    <Tag className={className} style={style} aria-label={text.replace(/\n/g, ' ')}>
      {tokens.map((t, i) => {
        const isAccent = accentWord && t.word.replace(/[^\w']/g, '') === accentWord;
        const color = isAccent ? L.orangeText : undefined;
        const last = i === tokens.length - 1;
        if (reduce) {
          return (
            <React.Fragment key={i}>
              {t.br && <br className="landing-br" />}
              <span aria-hidden="true" style={{ color, position: last ? 'relative' : undefined, display: last ? 'inline-block' : undefined }}>{t.word}{last && tail}</span>{' '}
            </React.Fragment>
          );
        }
        const at = delay + i * stagger;
        return (
          <React.Fragment key={i}>
            {t.br && <br className="landing-br" />}
            <span aria-hidden="true" style={{ display: 'inline-block', whiteSpace: 'nowrap', position: 'relative', color }}>
              <MotionSpan
                aria-hidden="true"
                initial={{ opacity: 0, scale: 0.6 }}
                animate={{ opacity: [0, 1, 1, 0], scale: [0.6, 1, 1, 1] }}
                transition={{ delay: at - 0.08, duration: 0.42, times: [0, 0.2, 0.7, 1], ease: 'easeOut' }}
                style={{ position: 'absolute', left: '-0.42em', bottom: '0.14em', width: '0.22em', height: '0.22em', background: L.ink, display: 'block' }}
              />
              <MotionSpan
                style={{ display: 'inline-block' }}
                initial={{ opacity: 0, y: '0.35em' }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: at, duration: 0.38, ease: [0.2, 0.8, 0.2, 1] }}
              >
                {t.word}
              </MotionSpan>
              {last && tail}
            </span>{' '}
          </React.Fragment>
        );
      })}
    </Tag>
  );
};

/**
 * A giant word that folds away as it leaves the top of the viewport: it
 * compresses vertically and fades over the last stretch of its own exit, so
 * the next chapter's word reads as the page turning (Leonardo's move). It is
 * fully legible whenever its body copy is on screen. Static below 1024px —
 * a 64px word has no room to fold on a phone — and under reduced motion.
 */
export const CollapseWord: React.FC<{ children: React.ReactNode; className?: string; style?: React.CSSProperties }> = ({ children, className = '', style }) => {
  const reduce = useReducedMotion();
  const [wide, setWide] = useState(false);
  useEffect(() => {
    const mq = window.matchMedia('(min-width: 1024px)');
    const sync = () => setWide(mq.matches);
    sync();
    mq.addEventListener('change', sync);
    return () => mq.removeEventListener('change', sync);
  }, []);
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start 92%', 'end 6%'] });
  const scaleY = useTransform(scrollYProgress, [0, 0.7, 1], [1, 1, 0.1]);
  const opacity = useTransform(scrollYProgress, [0, 0.7, 1], [1, 1, 0]);
  const y = useTransform(scrollYProgress, [0, 0.7, 1], ['0em', '0em', '-0.2em']);
  if (reduce || !wide) return <div ref={ref} className={className} style={style}>{children}</div>;
  return (
    <div ref={ref} className={className} style={style}>
      <MotionDiv style={{ scaleY, opacity, y, transformOrigin: '50% 100%', willChange: 'transform, opacity' }}>{children}</MotionDiv>
    </div>
  );
};

/** In-view rise, once. */
export const Reveal: React.FC<{ children: React.ReactNode; delay?: number; className?: string; style?: React.CSSProperties; y?: number }> = ({ children, delay = 0, className = '', style, y = 18 }) => {
  const reduce = useReducedMotion();
  if (reduce) return <div className={className} style={style}>{children}</div>;
  return (
    <MotionDiv
      className={className}
      style={style}
      initial={{ opacity: 0, y }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-10% 0px -10% 0px' }}
      transition={{ delay, duration: 0.55, ease: [0.2, 0.8, 0.2, 1] }}
    >
      {children}
    </MotionDiv>
  );
};

/** Report whether an element has been on screen at least once. */
export const useSeen = (ref: React.RefObject<Element | null>, margin = '-15% 0px'): boolean => {
  const inView = useInView(ref, { once: true, margin: margin as never });
  return inView;
};

export interface CursorStep {
  /** Percent position inside the demo frame. */
  x: number;
  y: number;
  /** Hold here (ms) before the next step. */
  hold?: number;
  /** Fires when the cursor arrives — set state here to fake the click. */
  onArrive?: () => void;
  click?: boolean;
}

/**
 * A scripted cursor for auto-playing demos. Give it steps; it glides between
 * them, pulses on "click" steps, and calls onArrive so the host component can
 * flip its own state. Stops when `playing` is false or motion is reduced.
 */
export const ScriptedCursor: React.FC<{ steps: CursorStep[]; playing: boolean; loop?: boolean; onLoop?: () => void; travel?: number }> = ({ steps, playing, loop = true, onLoop, travel = 650 }) => {
  const reduce = useReducedMotion();
  const [i, setI] = useState(0);
  const [pulse, setPulse] = useState(false);
  const timer = useRef<number | null>(null);

  useEffect(() => {
    if (reduce || !playing || steps.length === 0) return;
    const step = steps[i];
    const arrive = window.setTimeout(() => {
      if (step.click) { setPulse(true); window.setTimeout(() => setPulse(false), 220); }
      step.onArrive?.();
      timer.current = window.setTimeout(() => {
        if (i + 1 < steps.length) setI(i + 1);
        else if (loop) { onLoop?.(); setI(0); }
      }, step.hold ?? 900);
    }, travel);
    return () => { window.clearTimeout(arrive); if (timer.current) window.clearTimeout(timer.current); };
  }, [i, playing, reduce, steps, loop, onLoop, travel]);

  useEffect(() => { if (!playing) setI(0); }, [playing]);

  if (reduce || !playing || steps.length === 0) return null;
  const s = steps[i];
  return (
    <MotionDiv
      aria-hidden="true"
      initial={false}
      animate={{ left: `${s.x}%`, top: `${s.y}%`, scale: pulse ? 0.82 : 1 }}
      transition={{ left: { duration: travel / 1000, ease: [0.3, 0.7, 0.2, 1] }, top: { duration: travel / 1000, ease: [0.3, 0.7, 0.2, 1] }, scale: { duration: 0.16 } }}
      style={{ position: 'absolute', zIndex: 5, pointerEvents: 'none', width: 22, height: 26, marginLeft: -2, marginTop: -2, filter: 'drop-shadow(0 1px 1px rgba(0,0,0,0.25))' }}
    >
      <svg viewBox="0 0 22 26" width="22" height="26" aria-hidden="true">
        <path d="M2 1 L2 20 L7 15.5 L10.5 24 L14 22.5 L10.5 14 L17 14 Z" fill="#fff" stroke={L.ink} strokeWidth="1.6" strokeLinejoin="round" />
      </svg>
      {pulse && <span style={{ position: 'absolute', left: -8, top: -8, width: 22, height: 22, borderRadius: 999, border: `2px solid ${L.orange}`, display: 'block' }} />}
    </MotionDiv>
  );
};
