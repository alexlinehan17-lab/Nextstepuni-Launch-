/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The footer’s hand-drawn baseline. It draws with the reveal and remains
 * the landing surface for Star Guy. The caption is normal brand typography
 * in Footer.tsx, where it can wrap cleanly on a small screen.
 */

import React, { useEffect, useImperativeHandle, useMemo, useRef, useState } from 'react';
import type { MotionValue } from 'framer-motion';
import { useReducedMotion } from '../../Motion';
import { isStatic } from './env';

const HEIGHT = 28;
/** A hairline across `w` px with a pen's slight waver, drawn at y = 1. */
const handLine = (w: number): string => {
  const segs = Math.max(3, Math.round(w / 220));
  const step = w / segs;
  let d = 'M0 1';
  for (let i = 0; i < segs; i++) {
    const x0 = i * step, x1 = (i + 1) * step;
    // Deterministic waver: alternating, shrinking towards the ends.
    const amp = 1.3 * (i % 2 === 0 ? 1 : -1);
    d += ` C${(x0 + step * 0.35).toFixed(1)} ${(1 + amp).toFixed(2)} ${(x1 - step * 0.35).toFixed(1)} ${(1 - amp * 0.6).toFixed(2)} ${x1.toFixed(1)} 1`;
  }
  return d;
};

const clamp01 = (v: number) => Math.min(1, Math.max(0, v));

export const FooterLine = React.forwardRef<SVGSVGElement, { progress: MotionValue<number> }>(({ progress }, forwarded) => {
  const ref = useRef<SVGSVGElement>(null);
  useImperativeHandle(forwarded, () => ref.current as SVGSVGElement);
  const pathRef = useRef<SVGPathElement>(null);
  const reduce = useReducedMotion();
  const [w, setW] = useState(1136);

  useEffect(() => {
    const el = ref.current;
    if (!el || typeof ResizeObserver === 'undefined') return;
    const ro = new ResizeObserver(entries => setW(Math.max(240, Math.round(entries[0].contentRect.width))));
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  const d = useMemo(() => handLine(w), [w]);

  useEffect(() => {
    const apply = (p: number) => {
      // Keep the character’s baseline drawing with the footer reveal.
      if (pathRef.current) pathRef.current.style.strokeDashoffset = String(1 - clamp01(p / 0.55));
    };
    if (reduce || isStatic()) { apply(1); return; }
    apply(progress.get());
    return progress.on('change', apply);
  }, [progress, reduce, d, w]);

  return (
    <>
      <svg ref={ref} className="fx-line" viewBox={`0 0 ${w} ${HEIGHT}`} width="100%" height={HEIGHT} aria-hidden="true" focusable="false">
        <path id="fx-floor-path" ref={pathRef} className="fx-line-path" d={d} pathLength={1} style={{ strokeDasharray: 1 }} />
      </svg>
    </>
  );
});
FooterLine.displayName = 'FooterLine';

export default FooterLine;
