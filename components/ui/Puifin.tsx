/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Puifín the Puffin — the app's guide and companion. A vibrant flat-toon
 * character modelled and rendered in Blender (emission-flat colors, ink
 * hull outlines, cartoon eyes). Brand orange lives in the beak and feet.
 *
 * Renders live in public/assets/puifin/<pose>.webp (transparent, 768px).
 * The Blender build script that generates them is docs/design/puifin_poses.py
 * — poses are parameterised, so new ones are a dict entry away.
 *
 * Poses: perch (idle), wave, fly, cheer, rest, think, read, point,
 * peek (perch cropped by an overflow-hidden container), nod (perch +
 * a gentle CSS rock). Idle motion is CSS-only and respects
 * prefers-reduced-motion via the shared hook.
 */

import React from 'react';
import { useReducedMotion } from '../Motion';

export type PuifinPose =
  | 'perch' | 'wave' | 'fly' | 'cheer' | 'rest'
  | 'think' | 'read' | 'point' | 'peek' | 'nod';

/** Poses that reuse another pose's render. */
const RENDER_ALIAS: Partial<Record<PuifinPose, string>> = { nod: 'perch', peek: 'perch' };

/**
 * Rendered sprite-strip animations (horizontal filmstrips from the same
 * Blender build). Played with stepped CSS transforms — no video codecs,
 * works everywhere a WebP does. Poses without a strip fall back to the
 * static render + gentle CSS motion.
 */
const STRIPS: Partial<Record<PuifinPose, { file: string; frames: number; anim: string }>> = {
  perch: { file: 'anim-blink', frames: 4, anim: 'puifin-strip-blink 4.6s step-end infinite' },
  wave: { file: 'anim-wave', frames: 12, anim: 'puifin-strip-wave 1.5s steps(11) 2 forwards' },
  fly: { file: 'anim-flap', frames: 8, anim: 'puifin-strip-flap 0.66s steps(8) infinite' },
};

/** Gentle idle motion per pose — meaning, not decoration. */
const MOTION: Partial<Record<PuifinPose, string>> = {
  perch: 'puifin-bob 3.2s ease-in-out infinite',
  cheer: 'puifin-hop 0.9s ease-in-out infinite',
  fly: 'puifin-drift 2.6s ease-in-out infinite',
  nod: 'puifin-rock 2.2s ease-in-out infinite',
  rest: 'puifin-bob 5.2s ease-in-out infinite',
};

interface PuifinProps {
  pose?: PuifinPose;
  size?: number;
  /** Set false to freeze all motion regardless of OS setting. */
  animate?: boolean;
  className?: string;
  /** Decorative by default; pass a label to expose her to screen readers. */
  label?: string;
}

const Puifin: React.FC<PuifinProps> = ({ pose = 'perch', size = 96, animate = true, className, label }) => {
  const reduceMotion = useReducedMotion();
  const live = animate && !reduceMotion;
  const strip = live ? STRIPS[pose] : undefined;
  const src = `/assets/puifin/${strip ? strip.file : RENDER_ALIAS[pose] ?? pose}.webp`;

  if (strip) {
    return (
      <span
        className={className}
        role={label ? 'img' : undefined}
        aria-label={label}
        aria-hidden={label ? undefined : true}
        style={{
          display: 'block',
          width: size,
          height: size,
          overflow: 'hidden',
          userSelect: 'none',
          animation: MOTION[pose],
          transformOrigin: '50% 90%',
        }}
      >
        <img
          src={src}
          width={size * strip.frames}
          height={size}
          alt=""
          aria-hidden="true"
          draggable={false}
          style={{ display: 'block', maxWidth: 'none', animation: strip.anim }}
        />
      </span>
    );
  }

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

export default Puifin;
