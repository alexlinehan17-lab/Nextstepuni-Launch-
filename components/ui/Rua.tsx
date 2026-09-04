/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Rua the Robin — the app's guide and companion. One hand-drawn SVG,
 * ten poses, crisp from 20px to 200px. Ireland's boldest garden bird:
 * the one that lands beside you while you work. Her breast carries the
 * brand apricot as plumage, never as paint.
 *
 * Keyframes (rua-*) live in index.css; every animation respects
 * prefers-reduced-motion via the shared hook. Poses:
 *   perch  — idle with a slow blink (default)
 *   wave   — wing raised in greeting
 *   fly    — mid-flight, for "next step" moments
 *   cheer  — celebration hop
 *   rest   — asleep, for rest days
 *   think  — eyes up, considering
 *   read   — head down over a little book
 *   point  — wing extended toward what matters
 *   peek   — just the top half over an edge (give the container overflow-hidden)
 *   nod    — gentle encouraging rock
 */

import React from 'react';
import { useReducedMotion } from '../Motion';

export type RuaPose =
  | 'perch' | 'wave' | 'fly' | 'cheer' | 'rest'
  | 'think' | 'read' | 'point' | 'peek' | 'nod';

const INK = '#1A1A1A';
const CAP = '#CDC2B4';
const BELLY = '#EFE9E1';
const BREAST = '#F29A5B';
const BEAK = '#E8B04B';

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

  const anim = (name: string, dur: string, origin: string): React.CSSProperties =>
    live ? { animation: `${name} ${dur} ease-in-out infinite`, transformOrigin: origin } : { transformOrigin: origin };

  const wingStyle: React.CSSProperties =
    pose === 'wave' || pose === 'point'
      ? anim('rua-wave', '1.6s', '38px 62px')
      : pose === 'fly'
        ? anim('rua-flap', '0.5s', '38px 62px')
        : pose === 'nod'
          ? anim('rua-bob', '1.8s', '38px 62px')
          : { transformOrigin: '38px 62px' };

  const bodyStyle: React.CSSProperties =
    pose === 'cheer'
      ? anim('rua-hop', '0.9s', '50px 78px')
      : pose === 'fly'
        ? anim('rua-drift', '2.4s', '50px 60px')
        : pose === 'nod'
          ? anim('rua-rock', '2.2s', '50px 78px')
          : {};

  const eyesClosed = pose === 'rest' || pose === 'read';
  const pupilShift = pose === 'think' ? -2.4 : pose === 'read' ? 0 : 0;
  const bodyTilt = pose === 'point' ? 'rotate(4 50 60)' : pose === 'read' ? 'rotate(6 50 60)' : undefined;
  const peekShift = pose === 'peek' ? 'translate(0, 34)' : undefined;

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      className={className}
      role={label ? 'img' : undefined}
      aria-label={label}
      aria-hidden={label ? undefined : true}
    >
      <g transform={peekShift}>
        <g style={bodyStyle}>
          <g transform={bodyTilt}>
            {/* tail */}
            <path
              d="M 24 56 L 10 46 M 24 60 L 9 54"
              stroke={INK} strokeWidth="2.6" strokeLinecap="round" fill="none"
              transform={pose === 'fly' ? 'rotate(14 24 58)' : undefined}
            />
            {/* body */}
            <path d="M 30 62 Q 28 34 52 31 Q 74 29 78 52 Q 81 74 60 80 Q 36 85 30 62 Z" fill={BELLY} stroke={INK} strokeWidth="2.6" strokeLinejoin="round" />
            {/* head + back cap */}
            <path d="M 30 62 Q 28 34 52 31 Q 68 30 75 42 Q 62 40 52 46 Q 38 52 36 68 Q 31 66 30 62 Z" fill={CAP} stroke="none" />
            {/* apricot breast */}
            <path d="M 44 50 Q 58 42 70 48 Q 78 60 70 72 Q 58 81 46 76 Q 38 64 44 50 Z" fill={BREAST} stroke="none" opacity="0.92" />
            {/* wing */}
            <g style={wingStyle} transform={pose === 'point' ? 'rotate(-52 38 62)' : undefined}>
              <path d="M 36 58 Q 52 52 60 62 Q 54 74 42 73 Q 33 68 36 58 Z" fill={CAP} stroke={INK} strokeWidth="2.4" strokeLinejoin="round" />
              <path d="M 44 62 Q 50 61 54 65" stroke={INK} strokeWidth="1.6" strokeLinecap="round" fill="none" />
            </g>
            {/* beak */}
            <path d="M 76 46 L 86 49 L 76 52 Z" fill={BEAK} stroke={INK} strokeWidth="2" strokeLinejoin="round" />
            {/* eye */}
            {eyesClosed ? (
              <path d="M 63 44 Q 66 46 69 44" stroke={INK} strokeWidth="2.2" strokeLinecap="round" fill="none" />
            ) : (
              <g style={live ? { animation: 'rua-blink 4.2s infinite', transformOrigin: '66px 44px' } : undefined}>
                <circle cx={66 + pupilShift * 0.4} cy={44 + (pose === 'think' ? -1.6 : 0)} r="3.1" fill={INK} />
                <circle cx={67 + pupilShift * 0.4} cy={43 + (pose === 'think' ? -1.6 : 0)} r="0.9" fill="#fff" />
              </g>
            )}
            {/* legs */}
            {pose !== 'fly' && pose !== 'peek' && (
              <g stroke={INK} strokeWidth="2.4" strokeLinecap="round">
                <path d="M 46 82 L 45 91 M 45 91 L 41 93 M 45 91 L 49 93" fill="none" />
                <path d="M 58 80 L 59 90 M 59 90 L 55 92 M 59 90 L 63 92" fill="none" />
              </g>
            )}
            {/* pose furniture */}
            {pose === 'rest' && (
              <g fill={INK} opacity="0.55">
                <text x="80" y="30" fontSize="9" fontFamily="Georgia, serif">z</text>
                <text x="86" y="22" fontSize="7" fontFamily="Georgia, serif">z</text>
              </g>
            )}
            {pose === 'think' && (
              <g fill={INK} opacity="0.45">
                <circle cx="80" cy="28" r="1.6" />
                <circle cx="86" cy="21" r="2.1" />
                <circle cx="93" cy="13" r="2.6" />
              </g>
            )}
            {pose === 'read' && (
              <g>
                <path d="M 62 84 Q 72 79 82 84 L 82 94 Q 72 89 62 94 Z" fill="#fff" stroke={INK} strokeWidth="2" strokeLinejoin="round" />
                <path d="M 72 81.5 L 72 91.5" stroke={INK} strokeWidth="1.6" />
                <path d="M 66 86 Q 69 85 70 86 M 74 86 Q 77 85 78 86" stroke={INK} strokeWidth="1.1" strokeLinecap="round" fill="none" opacity="0.6" />
              </g>
            )}
            {pose === 'cheer' && (
              <g stroke={INK} strokeWidth="1.8" strokeLinecap="round" opacity="0.5">
                <path d="M 22 26 L 26 30 M 34 16 L 36 21 M 84 24 L 80 28" fill="none" />
              </g>
            )}
          </g>
        </g>
      </g>
    </svg>
  );
};

export default Rua;
