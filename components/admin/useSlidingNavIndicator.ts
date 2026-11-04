import { useLayoutEffect, type RefObject } from 'react';

/** Keep one underline aligned with the active button, including wrapped rows. */
export function useSlidingNavIndicator(navRef: RefObject<HTMLElement | null>, activeView: string): void {
  useLayoutEffect(() => {
    const nav = navRef.current;
    if (!nav) return;

    let frame = 0;
    let disposed = false;
    const measure = () => {
      const active = nav.querySelector<HTMLButtonElement>('button[aria-current="page"]');
      if (!active) return;
      const navBox = nav.getBoundingClientRect();
      const buttonBox = active.getBoundingClientRect();
      if (buttonBox.width === 0) return;

      nav.style.setProperty('--admin-nav-line-left', `${buttonBox.left - navBox.left + nav.scrollLeft + 8}px`);
      nav.style.setProperty('--admin-nav-line-top', `${buttonBox.bottom - navBox.top + nav.scrollTop - 2}px`);
      nav.style.setProperty('--admin-nav-line-width', `${Math.max(0, buttonBox.width - 16)}px`);
      nav.dataset.indicatorReady = 'true';
    };
    const scheduleMeasure = () => {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(measure);
    };

    // Measure before paint on selection changes. Keep the same pseudo-element
    // mounted so CSS can animate from its previous position to the new one.
    measure();
    const resized = typeof ResizeObserver === 'undefined' ? null : new ResizeObserver(scheduleMeasure);
    resized?.observe(nav);
    nav.querySelectorAll('button').forEach(button => resized?.observe(button));
    window.addEventListener('resize', scheduleMeasure);
    void document.fonts?.ready.then(() => {
      if (!disposed) scheduleMeasure();
    });

    return () => {
      disposed = true;
      cancelAnimationFrame(frame);
      resized?.disconnect();
      window.removeEventListener('resize', scheduleMeasure);
    };
  }, [navRef, activeView]);
}
