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
 * When no slot is on screen, he floats in the empty left margin, larger and
 * balancing on his star through the Rive rig. On a narrow desktop he rests
 * in the nav's normal mascot position to keep clear of the content.
 * And a claim: any character effect can ask him
 * to stand somewhere for a while (fx-char/control.ts) — beside a focused
 * textarea, at the foot of a toppled headline, at the end of a paper floor —
 * and that beats every slot until it is released.
 *
 * He also answers the page. `window.dispatchEvent(new CustomEvent('starguy',
 * { detail }))` with detail.kind of watch / unwatch / nod / tilt / cheer is
 * the whole contract; see fx-char/control.ts. Nothing happens when he is not
 * live.
 *
 * Lives only from 1024px up and never under reduced motion; below that the
 * static copies show exactly as before.
 */

import React, { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { animate, useMotionValue, useSpring, useTransform } from 'framer-motion';
import { MotionDiv, useReducedMotion } from '../../Motion';
import { StarguyFigure } from './StarguyFigure';
import { installLeave } from '../leave';
import { CANVAS, STAR, fireGrab, installControl, type Claim, type StarguyControl, type StarguyEvent } from '../fx-char/control';
import CharacterEffects from '../fx-char/CharacterEffects';
import { floatingHome, floatingMotion } from './floating';

export type SlotId = 'hero' | `word-${string}` | 'rail' | 'footer' | 'nav';

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
    <span ref={ref} data-starguy-slot={id} className={className} style={{ display: 'block', visibility: live ? 'hidden' : 'visible', ...style }}>
      {children}
    </span>
  );
};

export const useTravellerLive = (): boolean => useContext(TravellerContext).live;

const NAV = 68;
const clamp = (v: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, v));
/** How long the headline takes to arrive; the in-mask copy carries him until then. */
const SETTLE_MS = 1400;
/** How close the springs must be to a target before he counts as standing on it. */
const ARRIVED = 5;
/** The drawing's height for a given width. */
const RATIO = CANVAS.height / CANVAS.width;

interface Target { id: string; left: number; top: number; width: number; look?: { x: number; y: number } | null; squash?: number; lean?: number; hop?: boolean }

const Layer: React.FC<{ slots: React.RefObject<Map<SlotId, HTMLElement>> }> = ({ slots }) => {
  const x = useMotionValue(0);
  const y = useMotionValue(-200);
  const w = useMotionValue(52);
  const sx = useSpring(x, { stiffness: 260, damping: 26 });
  const sy = useSpring(y, { stiffness: 260, damping: 26 });
  const sw = useSpring(w, { stiffness: 260, damping: 30 });
  const hop = useMotionValue(0);
  /** Stride input for the rig: 0 at rest, 100 at a fast flick — from his own speed over the page. */
  const speed = useMotionValue(0);
  /** Where he looks: the pointer, relative to his own centre, −1…1 each way. */
  const lookXTarget = useMotionValue(0);
  const lookYTarget = useMotionValue(0);
  const lookXSpring = useSpring(lookXTarget, { stiffness: 120, damping: 20 });
  const lookYSpring = useSpring(lookYTarget, { stiffness: 120, damping: 20 });
  /** Reactions ride on top of the look: a nod bobs Y, a tilt glances away in X. */
  const nod = useMotionValue(0);
  const glance = useMotionValue(0);
  const lookX = useTransform(() => clamp(lookXSpring.get() + glance.get(), -1, 1));
  const lookY = useTransform(() => clamp(lookYSpring.get() + nod.get(), -1, 1));
  /** Lean with sideways motion, degrees; stretch with vertical speed, squash on landing. */
  const leanTarget = useMotionValue(0);
  const lean = useSpring(leanTarget, { stiffness: 140, damping: 18 });
  const tilt = useMotionValue(0);
  const squash = useMotionValue(0);
  const pulse = useMotionValue(0);
  const current = useRef<string | null>(null);
  const primed = useRef(false);
  const pointer = useRef<{ x: number; y: number; at: number } | null>(null);
  const claims = useRef<Map<string, Claim>>(new Map());
  const watching = useRef<HTMLElement | null>(null);
  const [hidden, setHidden] = useState(false);
  const hiddenRef = useRef(false);
  const [activeSlot, setActiveSlot] = useState<string | null>(null);
  const onHero = activeSlot === 'hero';
  const target = useRef<Target | null>(null);

  useEffect(() => {
    const onMove = (e: PointerEvent) => { pointer.current = { x: e.clientX, y: e.clientY, at: performance.now() }; };
    window.addEventListener('pointermove', onMove, { passive: true });
    return () => window.removeEventListener('pointermove', onMove);
  }, []);

  // The reactions. Each is a short keyframe ride on one channel; they layer
  // over whatever the tick is doing and hand the channel back at zero.
  const react = useCallback((kind: 'nod' | 'tilt' | 'cheer' | 'squash') => {
    if (kind === 'nod') {
      animate(nod, [0, 0.9, -0.25, 0.55, 0], { duration: 0.7, times: [0, 0.25, 0.5, 0.75, 1], ease: 'easeInOut' });
      animate(pulse, [0, 0.35, 0], { duration: 0.45, ease: 'easeOut', delay: 0.08 });
    } else if (kind === 'tilt') {
      animate(tilt, [0, 6, 6, 0], { duration: 1.3, times: [0, 0.2, 0.7, 1], ease: 'easeInOut' });
      animate(glance, [0, -0.85, -0.85, 0], { duration: 1.3, times: [0, 0.25, 0.7, 1], ease: 'easeInOut' });
    } else if (kind === 'cheer') {
      animate(hop, [0, -26, 0, -12, 0], { duration: 0.9, times: [0, 0.3, 0.55, 0.75, 1], ease: 'easeOut' });
      animate(pulse, [0, -0.3, 0.7, -0.1, 0.4, 0], { duration: 1.0, times: [0, 0.2, 0.55, 0.7, 0.85, 1], ease: 'easeOut' });
    } else {
      animate(pulse, [0, 0.7, -0.15, 0], { duration: 0.5, times: [0, 0.3, 0.7, 1], ease: 'easeOut' });
    }
  }, [nod, pulse, tilt, glance, hop]);

  // The public bus and the control, installed for as long as he is live.
  useEffect(() => {
    const unwatch = () => { watching.current = null; claims.current.delete('watch'); };
    const onBus = (e: Event) => {
      const d = (e as CustomEvent<StarguyEvent>).detail;
      if (!d) return;
      if (d.kind === 'watch' && d.el instanceof HTMLElement) {
        watching.current = d.el;
        d.el.addEventListener('blur', unwatch, { once: true });
      } else if (d.kind === 'unwatch') unwatch();
      else if (d.kind === 'nod' || d.kind === 'tilt' || d.kind === 'cheer') react(d.kind);
    };
    window.addEventListener('starguy', onBus);
    const control: StarguyControl = {
      claim: (id, c) => claims.current.set(id, c),
      release: id => claims.current.delete(id),
      pulse: react,
      hide: () => { hiddenRef.current = true; setHidden(true); },
      show: () => { hiddenRef.current = false; setHidden(false); },
      box: () => ({ left: sx.get(), top: sy.get() + hop.get(), width: sw.get(), height: sw.get() * RATIO }),
      where: () => {
        const t = target.current;
        if (!t) return null;
        return { id: t.id, arrived: Math.hypot(sx.get() - t.left, sy.get() - t.top) < ARRIVED && Math.abs(sw.get() - t.width) < 2 };
      },
      look: () => ({ x: lookX.get(), y: lookY.get() }),
    };
    installControl(control);
    return () => { window.removeEventListener('starguy', onBus); installControl(null); };
  }, [react, sx, sy, sw, hop, lookX, lookY]);

  useEffect(() => {
    let raf = 0;
    // Scroll velocity, px/s, for the passenger lean below.
    let lastScrollY = window.scrollY, lastAt = performance.now(), scrollV = 0;
    const nav = document.querySelector<HTMLElement>('.landing-nav');
    const pick = (): Target | null => {
      const map = slots.current;
      if (!map) return null;
      const vh = window.innerHeight;
      const rectOf = (id: SlotId) => map.get(id)?.getBoundingClientRect();
      // A watched element is a claim he computes himself: he stands to its
      // left with his feet on its bottom edge, looking across at it.
      const el = watching.current;
      if (el) {
        if (!el.isConnected) { watching.current = null; claims.current.delete('watch'); }
        else {
          const r = el.getBoundingClientRect();
          const width = 48, height = width * RATIO;
          const fitsLeft = r.left - width - 14 > 8;
          const left = fitsLeft ? r.left - width - 14 : r.right + 14;
          claims.current.set('watch', { box: { left, top: r.bottom - height, width }, priority: 10, look: { x: fitsLeft ? 0.9 : -0.9, y: 0.25 } });
        }
      }
      let best: { id: string; c: Claim } | null = null;
      claims.current.forEach((c, id) => { if (!best || c.priority > best.c.priority) best = { id, c }; });
      if (best) {
        const { id, c } = best as { id: string; c: Claim };
        return { id, left: c.box.left, top: c.box.top, width: c.box.width, look: c.look, squash: c.squash, lean: c.lean, hop: c.hop };
      }
      const hero = rectOf('hero');
      if (hero && hero.width > 0 && hero.bottom > NAV + 8 && hero.top < vh) return { id: 'hero', left: hero.left, top: hero.top, width: hero.width };
      for (const id of Array.from(map.keys()).filter(k => k.startsWith('word-'))) {
        const r = rectOf(id);
        if (r && r.width > 0 && r.top > NAV + 40 && r.bottom < vh + 80) return { id, left: r.left, top: r.top, width: r.width };
      }
      const chapters = document.getElementById('chapters')?.getBoundingClientRect();
      const rail = rectOf('rail');
      if (rail && rail.width > 0 && chapters && chapters.top < vh * 0.55 && chapters.bottom > NAV + 160) return { id: 'rail', left: rail.left, top: rail.top, width: rail.width };
      const footer = rectOf('footer');
      if (footer && footer.width > 0 && footer.top < vh - 24) return { id: 'footer', left: footer.left, top: footer.top, width: footer.width };
      // Float in the outer margin when the page has no other place for him.
      // Use the nav mark itself when the margin cannot fit the larger figure.
      if (nav && nav.dataset.condensed === 'true') {
        const bar = nav.getBoundingClientRect();
        const home = nav.querySelector('a')?.getBoundingClientRect();
        const floating = floatingHome(home?.left ?? 0, bar.bottom, vh);
        if (floating) return { id: 'float', ...floating, hop: false };
        const mark = Array.from(nav.querySelectorAll<HTMLElement>('.landing-nav-guy'))
          .map(el => el.getBoundingClientRect()).find(r => r.width > 0);
        if (mark) return { id: 'nav', left: mark.left, top: mark.top, width: mark.width, hop: false };
      }
      const last = current.current ? rectOf(current.current as SlotId) : undefined;
      return last && current.current ? { id: current.current, left: last.left, top: last.top, width: last.width } : null;
    };
    const tick = () => {
      raf = requestAnimationFrame(tick);
      const now = performance.now();
      const dt = Math.max(1, now - lastAt);
      const sv = ((window.scrollY - lastScrollY) / dt) * 1000;
      scrollV += (sv - scrollV) * Math.min(1, dt / 80);
      lastScrollY = window.scrollY; lastAt = now;
      const home = pick();
      if (!home) return;
      const floating = home.id === 'float' ? floatingMotion(now, scrollV) : null;
      const next = floating ? { ...home, left: home.left + floating.x, top: home.top + floating.y } : home;
      target.current = next;
      const { id, left: tx, top: ty, width: tw } = next;
      if (!primed.current) {
        primed.current = true;
        // Home from the app (landing-dev.html's pagereveal): he stands on the
        // door; start him there so the springs walk him up to his first slot.
        const door = document.querySelector<HTMLElement>('#landing-mark[data-here]');
        const from = door ? door.getBoundingClientRect() : null;
        if (door) door.removeAttribute('data-here');
        const px = from ? from.left : tx, py = from ? from.top : ty, pw = from ? from.width : tw;
        x.jump(px); y.jump(py); w.jump(pw); sx.jump(px); sy.jump(py); sw.jump(pw);
      }
      if (id !== current.current) {
        const far = Math.abs(ty - sy.get()) > window.innerHeight * 1.2;
        if (far) { x.jump(tx); y.jump(ty); sx.jump(tx); sy.jump(ty); }
        current.current = id;
        setActiveSlot(id);
        if (next.hop !== false) {
          animate(hop, [0, -10, 0], { duration: 0.45, ease: 'easeOut' });
          // He lands as the hop ends: a squash, a small rebound, then rest.
          animate(pulse, [0, 0.7, -0.15, 0], { duration: 0.5, times: [0, 0.3, 0.7, 1], ease: 'easeOut', delay: 0.45 });
        }
      }
      x.set(tx); y.set(ty); w.set(tw);
      const vy = sy.getVelocity();
      const vx = sx.getVelocity();
      speed.set(floating ? floating.speed : Math.min(100, Math.hypot(vx, vy) / 18));
      // A passenger's lean: into his own sideways travel, and into the reader's
      // scroll — a fast scroll down tips him forward a few degrees, and the
      // spring settles him again as it slows. Stretch a little when moving
      // fast; on the way down to the footer line, crouch as he arrives —
      // reader-paced, so scrolling back stands him up again.
      const still = hiddenRef.current;
      leanTarget.set(still ? 0 : clamp(vx / 250, -6, 6) + (floating?.lean ?? clamp(scrollV / 300, -4, 4)) + (next.lean ?? 0) + tilt.get());
      const stretch = clamp(-Math.abs(vy) / 2500, -0.5, 0);
      const d = Math.abs(ty - sy.get());
      const bump = id === 'footer' && d < 120 ? 0.6 * Math.sin(Math.PI * (1 - d / 120)) : 0;
      squash.set(still ? 0 : clamp(pulse.get() + stretch + bump + (next.squash ?? 0) + (floating?.squash ?? 0), -1, 1));
      // Look at the pointer, from his own centre; drift back to neutral when it
      // rests. A claim may fix his gaze instead; while the ragdoll stands in for
      // him he looks straight ahead, so the rig comes back in the same pose.
      const p = pointer.current;
      const cx = sx.get() + sw.get() * 0.5, cy = sy.get() + sw.get() * 0.5;
      if (still) { lookXTarget.set(0); lookYTarget.set(0); }
      else if (next.look) { lookXTarget.set(next.look.x); lookYTarget.set(next.look.y); }
      else if (p && performance.now() - p.at < 1600) {
        lookXTarget.set(clamp((p.x - cx) / (window.innerWidth * 0.35), -1, 1));
        lookYTarget.set(clamp((p.y - cy) / (window.innerHeight * 0.35), -1, 1));
      } else { lookXTarget.set(0); lookYTarget.set(0); }
      // The nav's printed mascot steps aside while the live figure is nearby.
      if (nav) {
        const guest = id === 'nav' || id === 'float' ? 'true' : 'false';
        if (nav.dataset.guest !== guest) nav.dataset.guest = guest;
      }
    };
    raf = requestAnimationFrame(tick);
    return () => { cancelAnimationFrame(raf); if (nav) nav.dataset.guest = 'false'; };
  }, [slots, x, y, w, sx, sy, sw, hop, speed, lookXTarget, lookYTarget, leanTarget, squash, pulse, tilt]);

  return createPortal(
    <MotionDiv
      aria-hidden="true"
      className="landing-traveller"
      data-slot={activeSlot ?? undefined}
      style={{ position: 'fixed', left: 0, top: 0, x: sx, y: sy, width: sw, marginTop: hop, zIndex: activeSlot === 'nav' ? 51 : 45, pointerEvents: 'none', lineHeight: 0 }}
    >
      <StarguyFigure speed={speed} lookX={lookX} lookY={lookY} lean={lean} squash={squash} style={{ visibility: hidden ? 'hidden' : 'visible' }} />
      {/* His star is a physics object: grabbable in the hero, where there is room to fall. */}
      {onHero && !hidden && (
        <span
          className="fx-char-grab"
          style={{ left: `${(STAR.x / CANVAS.width) * 100}%`, top: `${(STAR.y / CANVAS.height) * 100}%` }}
          onPointerDown={e => { e.preventDefault(); fireGrab(e.nativeEvent); }}
        />
      )}
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
    installLeave();
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
      {live && <CharacterEffects />}
    </TravellerContext.Provider>
  );
};
