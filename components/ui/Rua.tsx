/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Rua the Robin — the app's guide and companion. A soft 3D character
 * modelled and rendered in Blender (Cycles, vinyl-toy language: molded
 * color parts, soft studio light, baked ground shadow). Her breast wears
 * the brand apricot as plumage, never as paint.
 *
 * Renders live in public/assets/rua/<pose>.webp (transparent, 768px).
 * The Blender build script that generates them is kept in the design
 * scratchpad (rua3d.py) — poses are parameterised, so new ones are a
 * dict entry away.
 *
 * Poses: perch (idle), wave, fly, cheer, rest, think, read, point,
 * peek (perch cropped by an overflow-hidden container), nod (perch +
 * a gentle CSS rock). Idle motion is CSS-only and respects
 * prefers-reduced-motion via the shared hook.
 */

import React from 'react';
import { useReducedMotion } from '../Motion';

export type RuaPose =
  | 'perch' | 'wave' | 'fly' | 'cheer' | 'rest'
  | 'think' | 'read' | 'point' | 'peek' | 'nod';

/** Poses that reuse another pose's render. */
const RENDER_ALIAS: Partial<Record<RuaPose, string>> = { nod: 'perch', peek: 'perch' };

/** Gentle idle motion per pose — meaning, not decoration. */
const MOTION: Partial<Record<RuaPose, string>> = {
  perch: 'rua-bob 3.2s ease-in-out infinite',
  wave: 'rua-rock 1.8s ease-in-out infinite',
  cheer: 'rua-hop 0.9s ease-in-out infinite',
  fly: 'rua-drift 2.6s ease-in-out infinite',
  nod: 'rua-rock 2.2s ease-in-out infinite',
  rest: 'rua-bob 5.2s ease-in-out infinite',
};

interface RuaProps {
  pose?: RuaPose;
  size?: number;
  /** Set false to freeze all motion regardless of OS setting. */
  animate?: boolean;
  className?: string;
  /** Decorative by default; pass a label to expose her to screen readers. */
  label?: string;
}

const Rua: React.FC<RuaProps> = ({ pose = 'perch', size = 96, animate = true, className, label }) => {
  const reduceMotion = useReducedMotion();
  const live = animate && !reduceMotion;
  const src = `/assets/rua/${RENDER_ALIAS[pose] ?? pose}.webp`;

  return (
    <img
      src={src}
      width={size}
      height={size}
      className={className}
      alt={label ?? ''}
      aria-hidden={label ? undefined : true}
      draggable={false}
      loading="lazy"
      style={{
        display: 'block',
        userSelect: 'none',
        animation: live ? MOTION[pose] : undefined,
        transformOrigin: '50% 90%',
      }}
    />
  );
};

export default Rua;
