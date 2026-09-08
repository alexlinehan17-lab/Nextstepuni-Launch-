/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Examiner's marks. A sketchy ink underline, circle or bracket draws itself
 * over ~600 ms when its phrase scrolls into view, the way a pen marks a
 * script (rough-notation). Rationed to THREE on the whole page: an underline
 * in the hero headline, an orange circle on one figure in a chapter, a
 * bracket beside the join code in Schools. Never the highlight type — the
 * headline's pointer highlighter already owns that.
 *
 * Draws once, after the webfonts are in (so the geometry is final); re-shown
 * without animation on resize so a circle never drifts off its target.
 * Static under reduced motion and ?static=1. Purely decorative: aria-hidden
 * SVG, meaning never lives only in the mark.
 */

import React, { useEffect, useRef } from 'react';
import { annotate } from 'rough-notation';
import { useInView } from 'framer-motion';
import { useReducedMotion } from '../../Motion';
import { L } from '../theme';
import { isStatic } from './env';

type Annotation = ReturnType<typeof annotate>;
type Config = Parameters<typeof annotate>[1];

export const Mark: React.FC<{
  type: 'underline' | 'circle' | 'bracket';
  color?: string;
  brackets?: Config['brackets'];
  padding?: Config['padding'];
  strokeWidth?: number;
  /** Wait this long after the phrase is seen — e.g. until a headline has finished rising. */
  delay?: number;
  className?: string;
  style?: React.CSSProperties;
  children: React.ReactNode;
}> = ({ type, color = L.ink, brackets, padding, strokeWidth = 1.25, delay = 0, className, style, children }) => {
  const ref = useRef<HTMLSpanElement>(null);
  const reduce = useReducedMotion();
  const seen = useInView(ref, { once: true, margin: '-10% 0px' as never });

  useEffect(() => {
    if (!seen) return;
    let a: Annotation | null = null;
    let on = true;
    let timer = 0;
    let resizeTimer = 0;
    const draw = () => {
      if (!on || !ref.current) return;
      a = annotate(ref.current, { type, color, strokeWidth, iterations: 1, animationDuration: 600, animate: !(reduce || isStatic()), brackets, padding });
      a.show();
    };
    // Redraw in place, without the animation, once the text has reflowed.
    const reshow = () => { if (!a || !on) return; a.animate = false; a.hide(); a.show(); };
    const onResize = () => { window.clearTimeout(resizeTimer); resizeTimer = window.setTimeout(reshow, 160); };
    timer = window.setTimeout(() => {
      const ready = document.fonts?.ready ?? Promise.resolve();
      ready.then(draw, draw);
    }, delay);
    window.addEventListener('resize', onResize);
    return () => {
      on = false;
      window.clearTimeout(timer); window.clearTimeout(resizeTimer);
      window.removeEventListener('resize', onResize);
      a?.remove();
    };
  }, [seen, type, color, strokeWidth, brackets, padding, delay, reduce]);

  return <span ref={ref} className={className} style={style}>{children}</span>;
};

/** Wrap the first occurrence of `phrase` in `text` with `wrap`, leaving the copy itself untouched. */
export const markPhrase = (text: string, phrase: string, wrap: (node: string) => React.ReactNode): React.ReactNode => {
  const i = text.indexOf(phrase);
  if (i < 0) return text;
  return (
    <>
      {text.slice(0, i)}
      {wrap(phrase)}
      {text.slice(i + phrase.length)}
    </>
  );
};
