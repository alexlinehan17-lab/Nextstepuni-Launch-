/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The footer reveal, measured. main is an opaque sheet above a footer pinned
 * to the bottom of the window (fx.css, .fx-floor); as the sheet scrolls away
 * the footer shows beneath it. This hook turns that into numbers the footer's
 * effects run on: `progress` 0…1 as the sheet lifts clear of the footer, and
 * `cleared` — the sheet's edge has passed the line the character lands on,
 * which is when his footer slot may claim him. Lenis scrolls the real
 * document, so plain scroll events are enough; writes are coalesced per
 * frame and land in a MotionValue, not React state.
 */

import { useEffect, useState, type RefObject } from 'react';
import { useMotionValue, type MotionValue } from 'framer-motion';

export interface FloorReveal {
  progress: MotionValue<number>;
  cleared: boolean;
  revealed: boolean;
}

export const useFloorReveal = (footerRef: RefObject<HTMLElement | null>, lineRef: RefObject<Element | null>): FloorReveal => {
  const progress = useMotionValue(0);
  const [cleared, setCleared] = useState(false);
  const [revealed, setRevealed] = useState(false);

  useEffect(() => {
    const main = document.querySelector<HTMLElement>('.landing-page > main');
    const footer = footerRef.current;
    if (!main || !footer) return;
    let raf = 0;
    const measure = () => {
      raf = 0;
      const vh = window.innerHeight;
      const sheetEdge = main.getBoundingClientRect().bottom;
      const height = footer.offsetHeight || 1;
      const p = Math.min(1, Math.max(0, (vh - sheetEdge) / height));
      progress.set(p);
      setRevealed(p > 0.12);
      const line = lineRef.current?.getBoundingClientRect();
      setCleared(Boolean(line) && sheetEdge <= (line as DOMRect).top + 2);
    };
    const request = () => { if (!raf) raf = requestAnimationFrame(measure); };
    measure();
    window.addEventListener('scroll', request, { passive: true });
    window.addEventListener('resize', request);
    return () => {
      window.removeEventListener('scroll', request);
      window.removeEventListener('resize', request);
      if (raf) cancelAnimationFrame(raf);
    };
  }, [footerRef, lineRef, progress]);

  return { progress, cleared, revealed };
};
