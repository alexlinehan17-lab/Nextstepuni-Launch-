/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The page turn. When chapter VII rewrites itself around a course, the
 * chapter as it WAS is copied (a DOM clone, inert and hidden from AT), laid
 * over the rewritten chapter, and wiped away along a fold that travels from
 * the bottom-right corner to the top-left — the leaf turning; "back" turns
 * it the other way. The article's height eases from old to new at the same
 * time so the page below slides rather than jumps. Under reduced motion or
 * ?static=1 nothing is copied and the swap is instant.
 *
 * Also here: the fitted title. A course title takes the chapter word's place
 * and shrinks until its longest word fits the column and it sets in two
 * lines (three on a phone).
 */

import { useCallback, useEffect, useLayoutEffect, useRef, type RefObject } from 'react';
import { animate } from 'framer-motion';

const DURATION = 0.85;
const EASE: [number, number, number, number] = [0.7, 0, 0.2, 1];

type Pt = [number, number];

/** The part of the old leaf still showing at progress t, as points on the unit square. Forward: x + y ≤ s with s falling 2 → 0. Back: x + y ≥ s with s rising 0 → 2. */
const visible = (t: number, back: boolean): Pt[] => {
  if (back) {
    const s = 2 * t;
    return s <= 1 ? [[s, 0], [1, 0], [1, 1], [0, 1], [0, s]] : [[1, s - 1], [1, 1], [s - 1, 1]];
  }
  const s = 2 * (1 - t);
  return s >= 1 ? [[0, 0], [1, 0], [1, s - 1], [s - 1, 1], [0, 1]] : [[0, 0], [s, 0], [0, s]];
};

/** The fold: the segment where x + y = s crosses the box, from its left end. */
const fold = (t: number, back: boolean, w: number, h: number): { x: number; y: number; len: number; angle: number } => {
  const s = back ? 2 * t : 2 * (1 - t);
  const a: Pt = s <= 1 ? [0, s] : [s - 1, 1];
  const b: Pt = s <= 1 ? [s, 0] : [1, s - 1];
  const x1 = a[0] * w, y1 = a[1] * h, x2 = b[0] * w, y2 = b[1] * h;
  return { x: x1, y: y1, len: Math.hypot(x2 - x1, y2 - y1), angle: Math.atan2(y2 - y1, x2 - x1) };
};

const polygon = (pts: Pt[]): string => `polygon(${pts.map(([x, y]) => `${(x * 100).toFixed(2)}% ${(y * 100).toFixed(2)}%`).join(', ')})`;

interface Pending { clone: HTMLElement; height: number; back: boolean }

/**
 * Drive the turn on `leaf`. Call `snapshot(back)` in the event handler, BEFORE
 * the state change that rewrites the chapter (React commits after the
 * handler returns, so the copy is of the page as it stands); the turn runs
 * once the change has rendered and `token` differs.
 */
export const usePageTurn = (leaf: RefObject<HTMLElement | null>, token: string, instant: boolean): { snapshot: (back: boolean) => void } => {
  const pending = useRef<Pending | null>(null);
  const running = useRef<(() => void) | null>(null);

  const finish = useCallback(() => { running.current?.(); running.current = null; }, []);

  const snapshot = useCallback((back: boolean) => {
    const el = leaf.current;
    if (!el || instant) return;
    finish();
    const clone = el.cloneNode(true) as HTMLElement;
    // The copy is a picture: no ids, no timelines, no slots, no ornament of its own, nothing focusable.
    clone.removeAttribute('id');
    clone.removeAttribute('aria-labelledby');
    clone.className = '';
    clone.removeAttribute('style');
    clone.querySelectorAll('[id]').forEach(n => n.removeAttribute('id'));
    clone.querySelectorAll('[data-starguy-slot]').forEach(n => n.removeAttribute('data-starguy-slot'));
    clone.querySelectorAll('.fx-field, .fxf-turn, [aria-live]').forEach(n => n.remove());
    clone.setAttribute('inert', '');
    clone.setAttribute('aria-hidden', 'true');
    pending.current = { clone, height: el.offsetHeight, back };
  }, [leaf, instant, finish]);

  useLayoutEffect(() => {
    const p = pending.current;
    const el = leaf.current;
    if (!p || !el) return;
    pending.current = null;

    const overlay = document.createElement('div');
    overlay.className = 'fxf-turn';
    overlay.appendChild(p.clone);
    const line = document.createElement('span');
    line.className = 'fxf-fold';
    line.setAttribute('aria-hidden', 'true');
    overlay.appendChild(line);
    el.appendChild(overlay);

    const from = p.height;
    const to = el.offsetHeight;
    const w = el.clientWidth;
    el.style.height = `${from}px`;
    el.style.overflow = 'hidden';
    overlay.style.clipPath = polygon(visible(0, p.back));

    const controls = animate(0, 1, {
      duration: DURATION,
      ease: EASE,
      onUpdate: t => {
        const h = from + (to - from) * t;
        el.style.height = `${h}px`;
        overlay.style.clipPath = polygon(visible(t, p.back));
        const f = fold(t, p.back, w, Math.max(from, to));
        line.style.width = `${f.len}px`;
        line.style.transform = `translate(${f.x}px, ${f.y}px) rotate(${f.angle}rad)`;
        line.style.opacity = t > 0.01 && t < 0.99 ? '1' : '0';
      },
    });
    const cleanup = () => {
      controls.stop();
      overlay.remove();
      el.style.height = '';
      el.style.overflow = '';
    };
    running.current = cleanup;
    controls.then(() => { if (running.current === cleanup) { cleanup(); running.current = null; } });
  }, [leaf, token]);

  // Unmount: nothing left over the page.
  useEffect(() => finish, [finish]);

  return { snapshot };
};

const MIN_PX = 36;

/**
 * Fit the chapter word. `host` is the article; the word is the heading with
 * `id` inside it (its first child is the inline-block span that carries the
 * text). Fitting is on while `fit` is true; otherwise the heading is put
 * back to `base`, the inline size React gave it — React never re-applies an
 * unchanged style prop, so the hook must restore it rather than clear it.
 */
export const useFitTitle = (host: RefObject<HTMLElement | null>, id: string, text: string, fit: boolean, base: string): void => {
  useLayoutEffect(() => {
    const el = host.current?.querySelector<HTMLElement>(`#${CSS.escape(id)}`);
    if (!el) return;
    if (!fit) { el.style.fontSize = base; return; }
    const run = () => {
      el.style.fontSize = base;
      const basePx = parseFloat(getComputedStyle(el).fontSize);
      const avail = el.clientWidth;
      if (!avail || !basePx) return;
      // The longest word must fit the column on its own line.
      const probe = document.createElement('span');
      probe.style.cssText = 'position:absolute;left:0;top:0;visibility:hidden;white-space:nowrap;pointer-events:none;';
      el.appendChild(probe);
      let longest = 0;
      for (const word of text.split(/\s+/)) { probe.textContent = word; longest = Math.max(longest, probe.getBoundingClientRect().width); }
      probe.remove();
      let size = longest > 0 ? Math.min(basePx, basePx * (avail * 0.96) / longest) : basePx;
      // Then the whole title sets in two lines (three on a phone).
      const maxLines = avail < 640 ? 3 : 2;
      const inner = el.firstElementChild as HTMLElement | null;
      const lines = () => (inner ? Math.round(inner.getBoundingClientRect().height / (size * 0.9)) : 1);
      el.style.fontSize = `${size}px`;
      let guard = 0;
      while (size > MIN_PX && lines() > maxLines && guard++ < 14) { size = Math.max(MIN_PX, size * 0.93); el.style.fontSize = `${size}px`; }
    };
    run();
    window.addEventListener('resize', run);
    return () => { window.removeEventListener('resize', run); el.style.fontSize = base; };
  }, [host, id, text, fit, base]);
};
