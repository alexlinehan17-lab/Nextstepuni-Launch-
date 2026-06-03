/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * CountUp — animates a number from `from` to `to` on mount (cubic ease-out).
 * Used for the salary reveal on Career Paths cards. rAF-driven, cleans up.
 */

import React, { useEffect, useRef, useState } from 'react';

interface CountUpProps {
  to: number;
  from?: number;
  durationMs?: number;
  /** Format the current value into display text (e.g. euro). */
  format?: (n: number) => string;
  className?: string;
  style?: React.CSSProperties;
}

export const CountUp: React.FC<CountUpProps> = ({ to, from = 0, durationMs = 900, format, className, style }) => {
  const [val, setVal] = useState(from);
  const raf = useRef<number | undefined>(undefined);

  useEffect(() => {
    const start = performance.now();
    const step = (now: number) => {
      const t = Math.min(1, (now - start) / durationMs);
      const eased = 1 - Math.pow(1 - t, 3);
      setVal(Math.round(from + (to - from) * eased));
      if (t < 1) raf.current = requestAnimationFrame(step);
    };
    raf.current = requestAnimationFrame(step);
    return () => { if (raf.current) cancelAnimationFrame(raf.current); };
  }, [to, from, durationMs]);

  return <span className={className} style={style}>{format ? format(val) : val.toLocaleString()}</span>;
};
