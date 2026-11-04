/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The rolling odometer for the Numbers section (NumberFlow). A figure sits
 * at 0 until 60% of it is on screen, then rolls once to its real value —
 * digits that change spin, the rest stay put, and the number never reflows
 * (tabular figures, Intl thousands separators). Where the browser cannot
 * animate (no CSS mod(), reduced motion, ?static=1) the final number is
 * rendered outright, so screen readers and screenshots always get the value.
 */

import React, { useEffect, useRef, useState } from 'react';
import NumberFlow, { useCanAnimate } from '@number-flow/react';
import { useInView } from 'framer-motion';
import { useReducedMotion } from '../../Motion';

/** NumberFlow's own ease-out, stretched to the pace of the section's arrival. */
const SPIN: EffectTiming = { duration: 1500, easing: 'cubic-bezier(0.16, 1, 0.3, 1)' };

const Odometer: React.FC<{ value: string; delay?: number; style?: React.CSSProperties }> = ({ value, delay = 0, style }) => {
  const reduce = useReducedMotion();
  const canAnimate = useCanAnimate();
  const ref = useRef<HTMLSpanElement>(null);
  const seen = useInView(ref, { once: true, amount: 0.6 });
  const target = Number(value.replace(/[^\d.]/g, ''));
  const suffix = value.replace(/^[\d.,]+/, '');
  const [live, setLive] = useState(false);
  useEffect(() => {
    setLive(canAnimate && !reduce && !document.documentElement.classList.contains('landing-static'));
  }, [canAnimate, reduce]);
  // Stagger the four figures the way the rows reveal, so they do not all start on the same frame.
  const [go, setGo] = useState(false);
  useEffect(() => {
    if (!seen) return;
    const id = window.setTimeout(() => setGo(true), delay * 1000);
    return () => window.clearTimeout(id);
  }, [seen, delay]);
  const shown = live && !go ? 0 : target;
  return (
    <span ref={ref} style={{ display: 'inline-block', fontVariantNumeric: 'tabular-nums', ...style }}>
      <NumberFlow
        value={Number.isFinite(shown) ? shown : 0}
        locales="en-IE"
        trend={1}
        animated={live}
        willChange
        spinTiming={SPIN}
        transformTiming={SPIN}
        style={{ fontVariantNumeric: 'tabular-nums' }}
      />
      {suffix}
    </span>
  );
};

export default Odometer;
