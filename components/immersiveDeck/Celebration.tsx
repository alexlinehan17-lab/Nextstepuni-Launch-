/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Celebration — a lightweight radial particle burst for "you saved a move" /
 * "deck complete" moments. Deterministic (no Math.random) so it never flickers
 * on re-render. Renders inside a relatively-positioned parent (absolute inset-0).
 */

import React, { useMemo } from 'react';
import { MotionDiv } from '../Motion';

interface CelebrationProps {
  /** Particle colours, cycled. */
  colors?: string[];
  count?: number;
}

export const Celebration: React.FC<CelebrationProps> = ({ colors = ['#FFFFFF'], count = 26 }) => {
  const bits = useMemo(
    () =>
      Array.from({ length: count }, (_, i) => {
        const angle = (i / count) * Math.PI * 2;
        const dist = 70 + (i % 5) * 28;
        return {
          x: Math.cos(angle) * dist,
          y: Math.sin(angle) * dist,
          c: colors[i % colors.length],
          s: 5 + (i % 3) * 4,
          delay: (i % 6) * 0.025,
        };
      }),
    [count, colors],
  );

  return (
    <div className="pointer-events-none absolute inset-0 flex items-center justify-center overflow-hidden z-40">
      {bits.map((b, i) => (
        <MotionDiv
          key={i}
          className="absolute"
          style={{ width: b.s, height: b.s, backgroundColor: b.c, borderRadius: 2 }}
          initial={{ x: 0, y: 0, opacity: 1, scale: 1 }}
          animate={{ x: b.x, y: b.y, opacity: 0, scale: 0.3, rotate: 160 }}
          transition={{ duration: 0.9, delay: b.delay, ease: 'easeOut' }}
        />
      ))}
    </div>
  );
};
