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

/** Counts a formatted number up from zero once it scrolls into view. "10,495" → 0 … 10,495. */
export const CountUp: React.FC<{ value: string; duration?: number; className?: string; style?: React.CSSProperties }> = ({ value, duration = 1400, className = '', style }) => {
  const reduce = useReducedMotion();
  const ref = useRef<HTMLSpanElement>(null);
  const seen = useInView(ref, { once: true, margin: '-10% 0px' as never });
  const target = Number(value.replace(/[^\d.]/g, ''));
  const suffix = value.replace(/^[\d.,]+/, '');
  const [shown, setShown] = useState(reduce ? target : 0);
  useEffect(() => {
    if (reduce || !seen || !Number.isFinite(target)) { setShown(target); return; }
    let raf = 0; const t0 = performance.now();
    const tick = (now: number) => {
      const p = Math.min(1, (now - t0) / duration);
      const eased = 1 - Math.pow(1 - p, 3);
      setShown(Math.round(target * eased));
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [seen, reduce, target, duration]);
  return <span ref={ref} className={className} style={style}>{shown.toLocaleString('en-IE')}{suffix}</span>;
};

interface Star { id: number; x: number; y: number; size: number; rot: number }

/**
 * Tiny orange stars fall away from the pointer as it crosses the hero — the
 * Shopify Design ASCII trail, in starguy's own material. Pointer only; nothing
 * on touch or under reduced motion.
 */
export const StarTrail: React.FC<{ hostRef: React.RefObject<HTMLElement | null> }> = ({ hostRef }) => {
  const reduce = useReducedMotion();
  const [stars, setStars] = useState<Star[]>([]);
  const last = useRef(0); const seq = useRef(0);
  useEffect(() => {
    const host = hostRef.current;
    if (!host || reduce) return;
    const onMove = (e: PointerEvent) => {
      if (e.pointerType !== 'mouse') return;
      const now = performance.now();
      if (now - last.current < 45) return;
      last.current = now;
      const r = host.getBoundingClientRect();
      const star: Star = { id: seq.current++, x: e.clientX - r.left, y: e.clientY - r.top, size: 8 + Math.random() * 8, rot: Math.random() * 60 - 30 };
      setStars(s => [...s.slice(-28), star]);
      window.setTimeout(() => setStars(s => s.filter(k => k.id !== star.id)), 900);
    };
    host.addEventListener('pointermove', onMove);
    return () => host.removeEventListener('pointermove', onMove);
  }, [hostRef, reduce]);
  if (reduce) return null;
  return (
    <div aria-hidden="true" style={{ position: 'absolute', inset: 0, pointerEvents: 'none', overflow: 'hidden', zIndex: 2 }}>
      {stars.map(s => (
        <MotionSpan
          key={s.id}
          initial={{ opacity: 0.95, scale: 1, x: s.x, y: s.y, rotate: s.rot }}
          animate={{ opacity: 0, scale: 0.4, y: s.y + 22, rotate: s.rot + 40 }}
          transition={{ duration: 0.85, ease: 'easeOut' }}
          style={{ position: 'absolute', left: 0, top: 0, width: s.size, height: s.size, display: 'block' }}
        >
          <svg viewBox="0 0 24 24" width={s.size} height={s.size} aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4 6.1 20.5l1.2-6.5L2.5 9.4l6.6-.9z" fill={L.orange} stroke={L.ink} strokeWidth="1.4" strokeLinejoin="round" /></svg>
        </MotionSpan>
      ))}
    </div>
  );
};

/** A word that builds letter by letter the first time it scrolls into view, then stays. */
export const LetterBuild: React.FC<{ text: string; stagger?: number; className?: string }> = ({ text, stagger = 0.035, className = '' }) => {
  const reduce = useReducedMotion();
  const ref = useRef<HTMLSpanElement>(null);
  const seen = useInView(ref, { once: true, margin: '-8% 0px' as never });
  if (reduce) return <span className={className}>{text}</span>;
  return (
    <span ref={ref} className={className} aria-label={text} style={{ display: 'inline-block', whiteSpace: 'pre' }}>
      {Array.from(text).map((ch, i) => (
        <MotionSpan
          key={i}
          aria-hidden="true"
          style={{ display: 'inline-block' }}
          initial={{ opacity: 0, y: '0.28em', rotate: -3 }}
          animate={seen ? { opacity: 1, y: 0, rotate: 0 } : undefined}
          transition={{ delay: i * stagger, duration: 0.42, ease: [0.2, 0.8, 0.2, 1] }}
        >
          {ch === ' ' ? ' ' : ch}
        </MotionSpan>
      ))}
    </span>
  );
};


/* ── LineRise ────────────────────────────────────────────────────────────────
   The headline arrives one line at a time: each line is masked and rises out of
   its own baseline over ~0.8s with an expo ease, lines 90ms apart. No markers,
   no per-word popping. Every word is a Highlight: pass the pointer over it and
   a pale orange highlighter sweeps under it, then fades once you have moved on. */

const Highlight: React.FC<{ word: string; color?: string }> = ({ word, color }) => {
  const [state, setState] = useState<'off' | 'on' | 'out'>('off');
  const timer = useRef<number | null>(null);
  const clear = () => { if (timer.current) { window.clearTimeout(timer.current); timer.current = null; } };
  useEffect(() => clear, []);
  return (
    <span
      className={`landing-hl${state === 'on' ? ' landing-hl--on' : state === 'out' ? ' landing-hl--out' : ''}`}
      style={{ color }}
      onPointerEnter={() => { clear(); setState('on'); }}
      onPointerLeave={() => {
        clear();
        timer.current = window.setTimeout(() => {
          setState('out');
          timer.current = window.setTimeout(() => setState('off'), 520);
        }, 500);
      }}
    >
      {word}
    </span>
  );
};

export const LineRise: React.FC<{
  text: string;
  accentWord?: string;
  className?: string;
  style?: React.CSSProperties;
  as?: 'h1' | 'h2' | 'p';
  /** Rendered inside the LAST word's box, absolutely positioned — for a character hanging off the headline. */
  tail?: React.ReactNode;
  delay?: number;
}> = ({ text, accentWord, className = '', style, as = 'h1', tail, delay = 0.1 }) => {
  const reduce = useReducedMotion();
  const lines = useMemo(() => text.split('\n').map(l => l.split(' ').filter(Boolean)), [text]);
  const Tag = as;
  const lastLine = lines.length - 1;
  return (
    <Tag className={className} style={style} aria-label={text.replace(/\n/g, ' ')}>
      {lines.map((words, li) => (
        <span key={li} aria-hidden="true" className="landing-line" style={{ display: 'block', overflow: 'hidden', paddingBottom: '0.28em', marginBottom: '-0.28em', paddingTop: '0.08em', marginTop: '-0.08em' }}>
          <MotionSpan
            style={{ display: 'block', willChange: 'transform' }}
            initial={reduce ? false : { y: '120%', opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: delay + li * 0.09, duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
          >
            {words.map((w, wi) => {
              const isAccent = accentWord && w.replace(/[^\w']/g, '') === accentWord;
              const last = li === lastLine && wi === words.length - 1;
              return (
                <React.Fragment key={wi}>
                  {last ? (
                    <span style={{ position: 'relative', display: 'inline-block' }}>
                      <Highlight word={w} color={isAccent ? L.orangeText : undefined} />
                      {tail}
                    </span>
                  ) : <Highlight word={w} color={isAccent ? L.orangeText : undefined} />}
                  {wi < words.length - 1 ? ' ' : null}
                </React.Fragment>
              );
            })}
          </MotionSpan>
        </span>
      ))}
    </Tag>
  );
};
