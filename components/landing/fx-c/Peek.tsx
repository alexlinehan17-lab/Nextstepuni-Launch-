/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The editorial hover peek: hover a subject name and a small hairline plate
 * appears beside the pointer with the real paper — the first page of that
 * subject's SEC exam — drifting with the pointer on a spring, then folding
 * away on leave. One shared plate is portalled to <body> for every PeekLink
 * on the page. Pointer only: touch taps just follow the link; keyboard focus
 * gets the same plate anchored beside the link. The image is preloaded on
 * hover intent and hidden until it has arrived. Reduced motion: a fade.
 */

import React, { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { useMotionValue, useSpring } from 'framer-motion';
import { AnimatePresence, MotionDiv, useReducedMotion } from '../../Motion';
import { PEEK_PAGE } from './papers';

/** Plate size: an A4 page at 176px wide. */
const PLATE_W = 176;
const PLATE_H = Math.round(PLATE_W * (PEEK_PAGE.height / PEEK_PAGE.width));
const GAP = 16;
const EDGE = 8;

interface Peek { src: string; alt: string }
interface PeekApi {
  /** Open (or swap) the plate beside a pointer position. */
  show: (peek: Peek, x: number, y: number) => void;
  /** Follow the pointer. */
  move: (x: number, y: number) => void;
  /** Open the plate beside a focused element. */
  anchor: (peek: Peek, rect: DOMRect) => void;
  hide: () => void;
}

const PeekContext = createContext<PeekApi | null>(null);

const preloaded = new Set<string>();
export const preload = (src: string): void => {
  if (preloaded.has(src) || typeof Image === 'undefined') return;
  preloaded.add(src);
  const img = new Image();
  img.src = src;
};

/** Where the plate goes for a pointer at (x, y): below-right, flipping to keep clear of the viewport edges. */
const beside = (x: number, y: number): { x: number; y: number } => {
  const vw = window.innerWidth; const vh = window.innerHeight;
  let px = x + GAP;
  if (px + PLATE_W > vw - EDGE) px = x - GAP - PLATE_W;
  let py = y + GAP;
  if (py + PLATE_H > vh - EDGE) py = Math.max(EDGE, y - GAP - PLATE_H);
  return { x: Math.max(EDGE, px), y: py };
};

/** Where the plate goes for a focused link: to its right, vertically centred, else to its left. */
const alongside = (r: DOMRect): { x: number; y: number } => {
  const vw = window.innerWidth; const vh = window.innerHeight;
  let px = r.right + 12;
  if (px + PLATE_W > vw - EDGE) px = r.left - 12 - PLATE_W;
  const py = Math.min(vh - EDGE - PLATE_H, Math.max(EDGE, r.top + r.height / 2 - PLATE_H / 2));
  return { x: Math.max(EDGE, px), y: py };
};

export const PeekProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const reduce = useReducedMotion();
  const [peek, setPeek] = useState<Peek | null>(null);
  const [loaded, setLoaded] = useState<string | null>(null);
  const x = useMotionValue(0);
  const y = useMotionValue(0);
  const spring = { stiffness: 420, damping: 38, mass: 0.7 };
  const sx = useSpring(x, spring);
  const sy = useSpring(y, spring);

  const api = useMemo<PeekApi>(() => {
    const jump = (p: { x: number; y: number }) => { x.jump(p.x); y.jump(p.y); sx.jump(p.x); sy.jump(p.y); };
    return {
      show: (next, px, py) => { preload(next.src); jump(beside(px, py)); setPeek(next); },
      move: (px, py) => { const p = beside(px, py); x.set(p.x); y.set(p.y); },
      anchor: (next, rect) => { preload(next.src); jump(alongside(rect)); setPeek(next); },
      hide: () => setPeek(null),
    };
  }, [x, y, sx, sy]);

  const plate = typeof document === 'undefined' ? null : createPortal(
    <AnimatePresence>
      {peek && (
        <MotionDiv
          key="peek"
          aria-hidden="true"
          className="fxc-peek"
          style={{ x: sx, y: sy, width: PLATE_W, height: PLATE_H }}
          initial={reduce ? { opacity: 0 } : { clipPath: 'inset(0 0 100% 0)', rotate: -2, opacity: 1 }}
          animate={reduce ? { opacity: 1 } : { clipPath: 'inset(0 0 0% 0)', rotate: 0, opacity: 1 }}
          exit={reduce ? { opacity: 0, transition: { duration: 0.12 } } : { clipPath: 'inset(0 0 100% 0)', rotate: -2, transition: { duration: 0.22, ease: [0.4, 0, 0.6, 1] } }}
          transition={reduce ? { duration: 0.15 } : { clipPath: { type: 'spring', bounce: 0, duration: 0.5 }, rotate: { type: 'spring', bounce: 0.25, duration: 0.6 } }}
        >
          <img
            src={peek.src}
            alt=""
            width={PEEK_PAGE.width}
            height={PEEK_PAGE.height}
            decoding="async"
            draggable={false}
            onLoad={() => setLoaded(peek.src)}
            style={{ opacity: loaded === peek.src ? 1 : 0 }}
          />
        </MotionDiv>
      )}
    </AnimatePresence>,
    document.body,
  );

  return (
    <PeekContext.Provider value={api}>
      {children}
      {plate}
    </PeekContext.Provider>
  );
};

/**
 * A link that peeks. With no `peek` it is a plain link — never a placeholder.
 * Mouse: the plate follows the pointer. Keyboard: the plate sits beside the
 * link while it has visible focus. Touch and pen: nothing, the tap navigates.
 */
export const PeekLink: React.FC<{
  href: string;
  peek: Peek | null;
  children: React.ReactNode;
  className?: string;
  style?: React.CSSProperties;
}> = ({ href, peek, children, className, style }) => {
  const api = useContext(PeekContext);
  const ref = useRef<HTMLAnchorElement>(null);
  const live = api && peek;
  // Hide on unmount so a plate never outlives the row it came from (tab changes remount the list).
  useEffect(() => () => { if (live) api.hide(); }, [api, live]);
  const onPointerEnter = useCallback((e: React.PointerEvent) => {
    if (!live || e.pointerType !== 'mouse') return;
    api.show(peek, e.clientX, e.clientY);
  }, [api, live, peek]);
  const onPointerMove = useCallback((e: React.PointerEvent) => {
    if (!live || e.pointerType !== 'mouse') return;
    api.move(e.clientX, e.clientY);
  }, [api, live]);
  const onPointerLeave = useCallback((e: React.PointerEvent) => {
    if (!live || e.pointerType !== 'mouse') return;
    api.hide();
  }, [api, live]);
  const onFocus = useCallback(() => {
    const el = ref.current;
    if (!live || !el || !el.matches(':focus-visible')) return;
    api.anchor(peek, el.getBoundingClientRect());
  }, [api, live, peek]);
  const onBlur = useCallback(() => { if (live) api.hide(); }, [api, live]);
  return (
    <a
      ref={ref}
      href={href}
      className={className}
      style={style}
      onPointerEnter={onPointerEnter}
      onPointerMove={onPointerMove}
      onPointerLeave={onPointerLeave}
      onFocus={onFocus}
      onBlur={onBlur}
    >
      {children}
    </a>
  );
};
