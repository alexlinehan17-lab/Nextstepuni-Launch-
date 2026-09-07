/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Weighted paper. A mouse wheel notches a page 100px at a time; paper should
 * slide. Lenis (8 KB) eases the real scroll position — no transforms, no
 * scroll-jacking — so the chapter fold, the rail walker and the rules that
 * draw themselves run off a frame-smooth position instead of stepwise ticks.
 * Touch is left native (syncTouch: false). Anchors travel instead of jumping
 * and land exactly on each target's own scroll-margin-top. Off under
 * prefers-reduced-motion, under ?static=1, and under ?smooth=0 for comparing.
 */

import Lenis from 'lenis';
import { SMOOTH_SCROLL } from './theme';

let lenis: Lenis | null = null;

/** The live instance, for callers that need to pause it (a full-screen takeover). */
export const getLenis = (): Lenis | null => lenis;

/** Travel to an element by id, honouring its scroll-margin-top; falls back to native smooth scroll. */
export function scrollToId(id: string): void {
  const el = document.getElementById(id);
  if (!el) return;
  const margin = parseFloat(getComputedStyle(el).scrollMarginTop || '0');
  if (lenis) lenis.scrollTo(Math.max(0, el.getBoundingClientRect().top + window.scrollY - margin), { duration: 1.1 });
  else el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

export function setupSmoothScroll(): () => void {
  if (typeof window === 'undefined' || !SMOOTH_SCROLL) return () => undefined;
  const params = new URLSearchParams(window.location.search);
  if (params.get('static') || params.get('smooth') === '0') return () => undefined;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return () => undefined;

  lenis = new Lenis({
    lerp: 0.12,
    wheelMultiplier: 1,
    syncTouch: false,
    // The looking glasses own their scroll; a wheel over them never moves the page.
    prevent: node => !!node.closest('.landing-glass-host'),
  });
  let raf = 0;
  const loop = (time: number) => { lenis?.raf(time); raf = requestAnimationFrame(loop); };
  raf = requestAnimationFrame(loop);

  // A page opened at #section must open there: Lenis starts from 0 and would
  // otherwise pull the browser's own hash jump straight back to the top.
  const jumpToHash = () => {
    const target = window.location.hash ? document.getElementById(window.location.hash.slice(1)) : null;
    if (!target || !lenis) return;
    const margin = parseFloat(getComputedStyle(target).scrollMarginTop || '0');
    lenis.scrollTo(Math.max(0, target.getBoundingClientRect().top + window.scrollY - margin), { immediate: true });
  };
  jumpToHash();
  // …and once more when the webfonts land, since the serif reflows everything above.
  document.fonts?.ready.then(jumpToHash).catch(() => undefined);

  const onClick = (e: MouseEvent) => {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey) return;
    const a = e.target instanceof Element ? e.target.closest<HTMLAnchorElement>('a[href^="#"]') : null;
    if (!a) return;
    const id = (a.getAttribute('href') ?? '').slice(1);
    if (!id || !document.getElementById(id)) return;
    e.preventDefault();
    scrollToId(id);
    window.history.replaceState(null, '', `#${id}`);
  };
  document.addEventListener('click', onClick);

  return () => {
    document.removeEventListener('click', onClick);
    cancelAnimationFrame(raf);
    lenis?.destroy();
    lenis = null;
  };
}
