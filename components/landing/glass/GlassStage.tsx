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

export interface AutoStep {
  /** Button label to look for (substring match on textContent). */
  text: string;
  /** Wait after pressing, ms. */
  hold: number;
  /** Wait before travelling to it, ms (gives the surface time to load). */
  before?: number;
}

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
}> = ({ children, height = 680, auto, active, className = '', logicalWidth }) => {
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
        btn.scrollIntoView({ block: 'center', behavior: 'smooth' });
        setCursor({ x, y, press: false });
        later(() => { setCursor({ x, y, press: true }); btn.click(); later(() => { setCursor(c => c && { ...c, press: false }); later(() => run(i + 1), step.hold); }, 180); }, 900);
      }, step.before ?? 600);
    };
    run(0);
    return () => { cancelled = true; timers.forEach(clearTimeout); };
  }, [auto, active, interacted, reduce, scale]);

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
        {children}
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
