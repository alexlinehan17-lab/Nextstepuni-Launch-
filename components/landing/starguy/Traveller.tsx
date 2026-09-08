/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * One starguy. The page used to carry five separate pictures of him that
 * teleported; now one figure travels. Each place he belongs — the end of the
 * headline, the rail row of the chapter being read, the ends of the words
 * "Mark Bank" and "Planner & Study", the footer line — is a Slot: it keeps
 * rendering its own static copy (hidden while he is live, so nothing
 * reflows) and reports where it is. A fixed layer springs him from slot to
 * slot: he stands on whichever slot is on screen, stays attached to the last
 * one as it scrolls away, and springs down the page to the next as it
 * arrives — always standing on his star at a slot when the page is still.
 *
 * Lives only from 1024px up and never under reduced motion; below that the
 * five static copies show exactly as before.
 */

import React, { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { animate, useMotionValue, useSpring } from 'framer-motion';
import { MotionDiv, useReducedMotion } from '../../Motion';
import { StarguyFigure } from './StarguyFigure';

export type SlotId = 'hero' | 'word-markbank' | 'word-planner' | 'rail' | 'footer';

interface TravellerContextValue {
  register: (id: SlotId, el: HTMLElement | null) => void;
  live: boolean;
}

const TravellerContext = createContext<TravellerContextValue>({ register: () => undefined, live: false });

/** A place starguy belongs. Wrap the static Starguy in it; the traveller takes the wrapper's box. */
export const StarguySlot: React.FC<{ id: SlotId; children: React.ReactNode; className?: string; style?: React.CSSProperties }> = ({ id, children, className = '', style }) => {
  const { register, live } = useContext(TravellerContext);
  const ref = useCallback((el: HTMLElement | null) => register(id, el), [id, register]);
  return (
    <span ref={ref} className={className} style={{ display: 'block', visibility: live ? 'hidden' : 'visible', ...style }}>
      {children}
    </span>
  );
};

export const useTravellerLive = (): boolean => useContext(TravellerContext).live;

const NAV = 68;
const clamp = (v: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, v));
/** How long the headline takes to arrive; the in-mask copy carries him until then. */
const SETTLE_MS = 1400;

const Layer: React.FC<{ slots: React.RefObject<Map<SlotId, HTMLElement>> }> = ({ slots }) => {
  const x = useMotionValue(0);
  const y = useMotionValue(-200);
  const w = useMotionValue(52);
  const sx = useSpring(x, { stiffness: 260, damping: 26 });
  const sy = useSpring(y, { stiffness: 260, damping: 26 });
  const sw = useSpring(w, { stiffness: 260, damping: 30 });
  const hop = useMotionValue(0);
  /** Stride input for the rig: 0 at rest, 100 at a fast flick — from his own vertical speed. */
  const speed = useMotionValue(0);
  /** Where he looks: the pointer, relative to his own centre, −1…1 each way. */
  const lookXTarget = useMotionValue(0);
  const lookYTarget = useMotionValue(0);
  const lookX = useSpring(lookXTarget, { stiffness: 120, damping: 20 });
  const lookY = useSpring(lookYTarget, { stiffness: 120, damping: 20 });
  /** Lean with sideways motion, degrees; stretch with vertical speed, squash on landing. */
  const leanTarget = useMotionValue(0);
  const lean = useSpring(leanTarget, { stiffness: 140, damping: 18 });
  const squash = useMotionValue(0);
  const pulse = useMotionValue(0);
  const current = useRef<SlotId | null>(null);
  const primed = useRef(false);
  const pointer = useRef<{ x: number; y: number; at: number } | null>(null);

  useEffect(() => {
    const onMove = (e: PointerEvent) => { pointer.current = { x: e.clientX, y: e.clientY, at: performance.now() }; };
    window.addEventListener('pointermove', onMove, { passive: true });
    return () => window.removeEventListener('pointermove', onMove);
  }, []);

  useEffect(() => {
    let raf = 0;
    const pick = (): { id: SlotId; rect: DOMRect } | null => {
      const map = slots.current;
      if (!map) return null;
      const vh = window.innerHeight;
      const rectOf = (id: SlotId) => map.get(id)?.getBoundingClientRect();
      const hero = rectOf('hero');
      if (hero && hero.width > 0 && hero.bottom > NAV + 8 && hero.top < vh) return { id: 'hero', rect: hero };
      for (const id of ['word-markbank', 'word-planner'] as const) {
        const r = rectOf(id);
        if (r && r.width > 0 && r.top > NAV + 40 && r.bottom < vh + 80) return { id, rect: r };
      }
      const chapters = document.getElementById('chapters')?.getBoundingClientRect();
      const rail = rectOf('rail');
      if (rail && rail.width > 0 && chapters && chapters.top < vh * 0.55 && chapters.bottom > NAV + 160) return { id: 'rail', rect: rail };
      const footer = rectOf('footer');
      if (footer && footer.width > 0 && footer.top < vh - 24) return { id: 'footer', rect: footer };
      // Nothing on screen claims him: stay attached to the last slot as it scrolls.
      const last = current.current ? rectOf(current.current) : undefined;
      return last && current.current ? { id: current.current, rect: last } : null;
    };
    const tick = () => {
      raf = requestAnimationFrame(tick);
      const next = pick();
      if (!next) return;
      const { id, rect } = next;
      const tx = rect.left, ty = rect.top, tw = rect.width;
      if (!primed.current) { primed.current = true; x.jump(tx); y.jump(ty); w.jump(tw); sx.jump(tx); sy.jump(ty); sw.jump(tw); }
      if (id !== current.current) {
        const far = Math.abs(ty - sy.get()) > window.innerHeight * 1.2;
        if (far) { x.jump(tx); y.jump(ty); sx.jump(tx); sy.jump(ty); }
        current.current = id;
        animate(hop, [0, -10, 0], { duration: 0.45, ease: 'easeOut' });
        // He lands as the hop ends: a squash, a small rebound, then rest.
        animate(pulse, [0, 0.7, -0.15, 0], { duration: 0.5, times: [0, 0.3, 0.7, 1], ease: 'easeOut', delay: 0.45 });
      }
      x.set(tx); y.set(ty); w.set(tw);
      const vy = sy.getVelocity();
      const vx = sx.getVelocity();
      speed.set(Math.min(100, Math.abs(vy) / 18));
      // Lean into sideways travel; stretch a little when moving fast; and on the
      // way down to the footer line, crouch as he arrives — reader-paced, so
      // scrolling back stands him up again.
      leanTarget.set(clamp(vx / 250, -6, 6));
      const stretch = clamp(-Math.abs(vy) / 2500, -0.5, 0);
      const d = Math.abs(ty - sy.get());
      const bump = id === 'footer' && d < 120 ? 0.6 * Math.sin(Math.PI * (1 - d / 120)) : 0;
      squash.set(clamp(pulse.get() + stretch + bump, -1, 1));
      // Look at the pointer, from his own centre; drift back to neutral when it rests.
      const p = pointer.current;
      const cx = sx.get() + sw.get() * 0.5, cy = sy.get() + sw.get() * 0.5;
      if (p && performance.now() - p.at < 1600) {
        lookXTarget.set(clamp((p.x - cx) / (window.innerWidth * 0.35), -1, 1));
        lookYTarget.set(clamp((p.y - cy) / (window.innerHeight * 0.35), -1, 1));
      } else { lookXTarget.set(0); lookYTarget.set(0); }
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [slots, x, y, w, sx, sy, sw, hop, speed, lookXTarget, lookYTarget, leanTarget, squash, pulse]);

  return createPortal(
    <MotionDiv
      aria-hidden="true"
      className="landing-traveller"
      style={{ position: 'fixed', left: 0, top: 0, x: sx, y: sy, width: sw, marginTop: hop, zIndex: 45, pointerEvents: 'none', lineHeight: 0 }}
    >
      <StarguyFigure speed={speed} lookX={lookX} lookY={lookY} lean={lean} squash={squash} />
    </MotionDiv>,
    document.body,
  );
};

export const StarguyProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const reduce = useReducedMotion();
  const slots = useRef<Map<SlotId, HTMLElement>>(new Map());
  const [wide, setWide] = useState(false);
  const [settled, setSettled] = useState(false);
  const [staticMode] = useState(() => typeof window !== 'undefined' && new URLSearchParams(window.location.search).has('static'));
  useEffect(() => {
    const mq = window.matchMedia('(min-width: 1024px)');
    const sync = () => setWide(mq.matches);
    sync();
    mq.addEventListener('change', sync);
    const id = window.setTimeout(() => setSettled(true), SETTLE_MS);
    return () => { mq.removeEventListener('change', sync); window.clearTimeout(id); };
  }, []);
  const live = wide && settled && !reduce && !staticMode;
  const register = useCallback((id: SlotId, el: HTMLElement | null) => {
    if (el) slots.current.set(id, el); else slots.current.delete(id);
  }, []);
  const value = useMemo(() => ({ register, live }), [register, live]);
  return (
    <TravellerContext.Provider value={value}>
      {children}
      {live && <Layer slots={slots} />}
    </TravellerContext.Provider>
  );
};
