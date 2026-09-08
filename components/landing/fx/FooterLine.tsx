/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The footer's drawn line and the caption that travels it. A hand-drawn
 * hairline path (1 px ink, non-scaling) runs the width of the footer along
 * the statement's baseline — the line the character lands on. As the page
 * lifts off the footer the line draws from the left, and a short DM Sans
 * caps caption rides it (SVG textPath; startOffset is an attribute, so it is
 * written from the reveal's MotionValue, never through React state). The
 * words are also in the DOM as visually hidden text. Reduced motion and
 * static renders freeze the caption at its resting offset.
 */

import React, { useEffect, useImperativeHandle, useMemo, useRef, useState } from 'react';
import type { MotionValue } from 'framer-motion';
import { useReducedMotion } from '../../Motion';
import { isStatic } from './env';

const HEIGHT = 64;
/** Where the caption comes to rest, as a percentage of the path — earlier on a line too short to carry it from there. */
const REST = 44;
const REST_MIN = 4;

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
const easeOut = (t: number) => 1 - Math.pow(1 - t, 3);

export const FooterLine = React.forwardRef<SVGSVGElement, { progress: MotionValue<number>; caption: string }>(({ progress, caption }, forwarded) => {
  const ref = useRef<SVGSVGElement>(null);
  useImperativeHandle(forwarded, () => ref.current as SVGSVGElement);
  const pathRef = useRef<SVGPathElement>(null);
  const textRef = useRef<SVGTextPathElement>(null);
  const reduce = useReducedMotion();
  const [w, setW] = useState(1136);
  // The caption is measured to find its resting offset; measure again once DM Sans is in.
  const [fontsReady, setFontsReady] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el || typeof ResizeObserver === 'undefined') return;
    const ro = new ResizeObserver(entries => setW(Math.max(240, Math.round(entries[0].contentRect.width))));
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  useEffect(() => {
    let on = true;
    (document.fonts?.ready ?? Promise.resolve()).then(() => { if (on) setFontsReady(true); }, () => undefined);
    return () => { on = false; };
  }, []);

  const d = useMemo(() => handLine(w), [w]);

  useEffect(() => {
    // Rest where the whole caption still fits on the line: 44% on a wide footer, earlier on a phone.
    let rest = REST;
    try {
      const len = textRef.current?.getComputedTextLength() ?? 0;
      if (len > 0) rest = Math.max(REST_MIN, Math.min(REST, 100 - (len / w) * 100 - 2));
    } catch { /* not laid out yet: keep the default */ }
    const apply = (p: number) => {
      // The line draws over the first half of the reveal; the caption arrives from the right over the rest.
      if (pathRef.current) pathRef.current.style.strokeDashoffset = String(1 - clamp01(p / 0.55));
      if (textRef.current) textRef.current.setAttribute('startOffset', `${(100 - (100 - rest) * easeOut(clamp01((p - 0.15) / 0.85))).toFixed(2)}%`);
    };
    if (reduce || isStatic()) { apply(1); return; }
    apply(progress.get());
    return progress.on('change', apply);
  }, [progress, reduce, d, w, fontsReady]);

  return (
    <>
      <svg ref={ref} className="fx-line" viewBox={`0 0 ${w} ${HEIGHT}`} width="100%" height={HEIGHT} aria-hidden="true" focusable="false">
        <path id="fx-floor-path" ref={pathRef} className="fx-line-path" d={d} pathLength={1} style={{ strokeDasharray: 1 }} />
        <text className="fx-line-caption" dy="17"><textPath ref={textRef} href="#fx-floor-path" startOffset="100%">{caption}</textPath></text>
      </svg>
      <p className="fx-sr">{caption}</p>
    </>
  );
});
FooterLine.displayName = 'FooterLine';

export default FooterLine;
