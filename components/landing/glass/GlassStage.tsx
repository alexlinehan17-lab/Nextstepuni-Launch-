/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The looking glass. A real app surface is laid out at the app's own width,
 * scaled to fit the page, and given its own scroll so the page never moves
 * under it. Two things the app does not expect when embedded are handled here:
 * headings that call focus() on drill-down (which would yank the page) get
 * their scroll restored, and an optional scripted cursor can walk to a real
 * button by its label and press it, so the demo plays itself until the
 * visitor touches it.
 */

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { MotionDiv, useReducedMotion } from '../../Motion';
import { L } from '../theme';
import { useLogicalWidth } from './useLogicalWidth';
import { getLenis } from '../scroll';
import { SubjectAccessContext } from '../../launchpad/SubjectAccess';

export interface AutoStep {
  /** Button label to look for (substring match on textContent). */
  text: string;
  /** Wait after pressing, ms. */
  hold: number;
  /** Wait before travelling to it, ms (gives the surface time to load). */
  before?: number;
  /** After the press, bring the glass back to the top (for presses that open a new screen). */
  then?: 'top';
}

/** Props every looking-glass surface accepts, so the chapters can mount the same glass at a different size. */
export interface GlassProps {
  /** Mode chosen along the bottom of the playground (subject, topic…); '' when the surface has none. */
  sub: string;
  active: boolean;
  height?: number;
  logicalWidth?: number;
}

/**
 * Controls the visitor may look at but not use. Matched by name — the
 * control's aria-label up to its first comma, else its text — against
 * `names`, or by `test`. Locked controls get a padlock and shake when
 * pressed; the press never reaches the app.
 */
export interface GlassLocks {
  names?: readonly string[];
  test?: (name: string, el: HTMLElement) => boolean;
  /** Custom reader for a control's name; return undefined to fall back to the default. */
  nameOf?: (el: HTMLElement) => string | undefined;
}

const CONTROL = 'button, a, [role="button"], [role="tab"]';
const norm = (s: string) => s.replace(/\s+/g, ' ').trim();
const defaultName = (el: HTMLElement) => norm((el.getAttribute('aria-label') ?? el.textContent ?? '').split(',')[0]);
const shake = (el: HTMLElement) => {
  el.classList.remove('landing-shake');
  void el.offsetWidth; // restart the animation
  el.classList.add('landing-shake');
  window.setTimeout(() => el.classList.remove('landing-shake'), 480);
};

const findButton = (root: HTMLElement, text: string): HTMLElement | null => {
  const all = Array.from(root.querySelectorAll<HTMLElement>('button, a[role="button"]'));
  return all.find(el => (el.textContent ?? '').trim().toLowerCase().includes(text.toLowerCase())) ?? null;
};

export const GlassStage: React.FC<{
  children: React.ReactNode;
  /** Logical height of the window into the app. */
  height?: number;
  /** Autoplay script; stops for good on the first real pointer/keyboard event inside. */
  auto?: AutoStep[];
  /** False while the tab is hidden or off screen. */
  active: boolean;
  className?: string;
  /** Override the width the surface is laid out at (default: the app's own breakpoint logic). */
  logicalWidth?: number;
  /** Controls to show locked. */
  locks?: GlassLocks;
  canSelectSubject?: (subject: string) => boolean;
}> = ({ children, height = 680, auto, active, className = '', logicalWidth, locks, canSelectSubject }) => {
  const reduce = useReducedMotion();
  const hostRef = useRef<HTMLDivElement>(null);
  const innerRef = useRef<HTMLDivElement>(null);
  const [hostWidth, setHostWidth] = useState(0);
  const autoLogical = useLogicalWidth(hostWidth);
  const logical = logicalWidth ?? autoLogical;
  const scale = hostWidth > 0 ? Math.min(1, hostWidth / logical) : 1;

  useEffect(() => {
    const host = hostRef.current;
    if (!host) return;
    const sync = () => setHostWidth(host.clientWidth);
    sync();
    const ro = new ResizeObserver(sync);
    ro.observe(host);
    return () => ro.disconnect();
  }, []);

  // The app focuses headings on drill-down; keep the page where the reader left it.
  const lastY = useRef(0);
  useEffect(() => {
    const onScroll = () => { lastY.current = window.scrollY; };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);
  // Scripted cursor over the real UI.
  const [interacted, setInteracted] = useState(false);
  const interactedRef = useRef(false);
  const onFocusCapture = useCallback((e: React.FocusEvent) => {
    const t = e.target as HTMLElement;
    // Until the visitor touches the glass, focus moves are the app's own (autofocus on
    // mount, heading focus on drill-down): keep both the page and the glass where they were.
    if (!interactedRef.current || (t && t.getAttribute('tabindex') === '-1')) {
      window.scrollTo(0, lastY.current);
      if (!interactedRef.current && innerRef.current) innerRef.current.scrollTop = 0;
    }
  }, []);
  const [cursor, setCursor] = useState<{ x: number; y: number; press: boolean } | null>(null);
  const stop = useCallback(() => { interactedRef.current = true; setInteracted(true); }, []);

  // The wheel stays in the glass: at the top or bottom of the surface a further
  // wheel tick would otherwise hand the scroll to the page and carry the visitor
  // out of the tool mid-paper. (Touch keeps native behaviour — a phone must be
  // able to scroll past a full-width frame.)
  useEffect(() => {
    const root = innerRef.current;
    if (!root) return;
    const onWheel = (e: WheelEvent) => {
      // A nested app pane may still have room even when this outer frame does not.
      let node = e.target instanceof Element ? e.target : null;
      while (node && node !== root) {
        if (node instanceof HTMLElement && /auto|scroll/.test(getComputedStyle(node).overflowY)) {
          const canScroll = e.deltaY < 0 ? node.scrollTop > 0 : node.scrollTop + node.clientHeight < node.scrollHeight - 1;
          if (canScroll) return;
        }
        node = node.parentElement;
      }
      const atTop = root.scrollTop <= 0;
      const atBottom = root.scrollTop + root.clientHeight >= root.scrollHeight - 1;
      if ((e.deltaY < 0 && atTop) || (e.deltaY > 0 && atBottom)) e.preventDefault();
    };
    root.addEventListener('wheel', onWheel, { passive: false });
    return () => root.removeEventListener('wheel', onWheel);
  }, []);

  // While a surface takes the whole screen (Paper Trail's viewer, a Mark Bank
  // session — both portal a fixed layer onto <body>), the page underneath
  // must not scroll, or closing the takeover lands the visitor somewhere else.
  useEffect(() => {
    if (!active) return;
    const isTakeover = (n: Node) => n instanceof HTMLElement && n.classList.contains('fixed') && n.classList.contains('inset-0');
    let locked = false;
    const update = () => {
      const open = Array.from(document.body.children).some(isTakeover);
      if (open === locked) return;
      locked = open;
      document.documentElement.style.overflow = open ? 'hidden' : '';
      if (open) getLenis()?.stop(); else getLenis()?.start();
    };
    const mo = new MutationObserver(update);
    mo.observe(document.body, { childList: true });
    update();
    return () => { mo.disconnect(); if (locked) { document.documentElement.style.overflow = ''; getLenis()?.start(); } };
  }, [active]);

  // Locks: decorate matching controls as the app renders them, and swallow their presses.
  useEffect(() => {
    const root = innerRef.current;
    if (!root || !locks) return;
    const names = new Set(locks.names ?? []);
    const nameOf = (el: HTMLElement) => locks.nameOf?.(el) ?? defaultName(el);
    const isLocked = (el: HTMLElement) => { const n = nameOf(el); return names.has(n) || !!locks.test?.(n, el); };
    let raf = 0;
    const apply = () => {
      raf = 0;
      root.querySelectorAll<HTMLElement>(CONTROL).forEach(el => {
        const on = isLocked(el);
        if (on !== el.classList.contains('landing-locked')) el.classList.toggle('landing-locked', on);
        if (on) { if (!el.hasAttribute('data-landing-locked')) el.setAttribute('data-landing-locked', ''); }
        else if (el.hasAttribute('data-landing-locked')) el.removeAttribute('data-landing-locked');
      });
    };
    const schedule = () => { if (!raf) raf = requestAnimationFrame(apply); };
    schedule();
    const mo = new MutationObserver(schedule);
    mo.observe(root, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ['class', 'aria-pressed', 'aria-selected', 'aria-label'] });
    const onClick = (e: MouseEvent) => {
      const target = e.target instanceof Element ? e.target.closest<HTMLElement>(CONTROL) : null;
      if (!target || !root.contains(target) || !target.hasAttribute('data-landing-locked')) return;
      e.preventDefault();
      e.stopPropagation();
      shake(target);
    };
    root.addEventListener('click', onClick, true);
    return () => { mo.disconnect(); if (raf) cancelAnimationFrame(raf); root.removeEventListener('click', onClick, true); };
  }, [locks, active]);
  useEffect(() => {
    if (!auto || !active || interacted || reduce) { setCursor(null); return; }
    let cancelled = false;
    const timers: number[] = [];
    const later = (fn: () => void, ms: number) => { const id = window.setTimeout(() => { if (!cancelled) fn(); }, ms); timers.push(id); };
    const run = (i: number) => {
      const step = auto[i % auto.length];
      later(() => {
        const root = innerRef.current;
        const btn = root ? findButton(root, step.text) : null;
        if (!root || !btn) { later(() => run(i + 1), 1200); return; }
        const rr = root.getBoundingClientRect(); const br = btn.getBoundingClientRect();
        // Positions in logical (unscaled) pixels inside the inner surface.
        const x = (br.left - rr.left) / scale + br.width / (2 * scale) + root.scrollLeft;
        const y = (br.top - rr.top) / scale + br.height / (2 * scale) + root.scrollTop;
        // Scroll the glass, never the page: scrollIntoView would drag every scrollable ancestor along.
        root.scrollTo({ top: Math.max(0, y - height / 2), behavior: 'smooth' });
        setCursor({ x, y, press: false });
        later(() => {
          setCursor({ x, y, press: true }); btn.click();
          later(() => {
            setCursor(c => c && { ...c, press: false });
            if (step.then === 'top') later(() => { root.scrollTo({ top: 0, behavior: 'smooth' }); setCursor(null); }, 500);
            later(() => run(i + 1), step.hold);
          }, 180);
        }, 900);
      }, step.before ?? 600);
    };
    run(0);
    return () => { cancelled = true; timers.forEach(clearTimeout); };
  }, [auto, active, interacted, reduce, scale, height]);

  return (
    <div
      ref={hostRef}
      className={`landing-glass-host ${className}`}
      style={{ position: 'relative', width: '100%', height: Math.round(height * scale), overflow: 'hidden', background: L.paper }}
      onPointerDownCapture={stop}
      onKeyDownCapture={stop}
      onWheelCapture={stop}
      onFocusCapture={onFocusCapture}
    >
      <div
        ref={innerRef}
        className="landing-glass"
        style={{ position: 'absolute', top: 0, left: 0, width: logical, height, overflowY: 'auto', overflowX: 'hidden', transform: `scale(${scale})`, transformOrigin: '0 0', overscrollBehavior: 'contain' }}
      >
        <SubjectAccessContext.Provider value={canSelectSubject}>{children}</SubjectAccessContext.Provider>
        {cursor && (
          <MotionDiv
            aria-hidden="true"
            initial={false}
            animate={{ left: cursor.x, top: cursor.y, scale: cursor.press ? 0.82 : 1 }}
            transition={{ left: { duration: 0.7, ease: [0.3, 0.7, 0.2, 1] }, top: { duration: 0.7, ease: [0.3, 0.7, 0.2, 1] }, scale: { duration: 0.16 } }}
            style={{ position: 'absolute', zIndex: 50, pointerEvents: 'none', width: 24, height: 28, marginLeft: -3, marginTop: -3, filter: 'drop-shadow(0 1px 1px rgba(0,0,0,0.25))' }}
          >
            <svg viewBox="0 0 22 26" width="24" height="28" aria-hidden="true">
              <path d="M2 1 L2 20 L7 15.5 L10.5 24 L14 22.5 L10.5 14 L17 14 Z" fill="#fff" stroke={L.ink} strokeWidth="1.6" strokeLinejoin="round" />
            </svg>
          </MotionDiv>
        )}
      </div>
    </div>
  );
};

export default GlassStage;
