/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * MountainLandscape — five-peak progress visualisation for the My Progress
 * page. Each peak corresponds to one of the five worlds (Mind, Growth,
 * Learn, Decode, Exam). Each peak fills from the base up in the world's
 * snow colour, proportional to that world's modules-completed ratio.
 *
 * Atmospheric layers (drawn back-to-front):
 *   1. Warm sky gradient
 *   2. Three distant ridge silhouettes (low opacity, recede in fog)
 *   3. Faint ground line
 *   4. Sun glyph upper right
 *   5. Per mountain: wobbly silhouette → diagonal pencil shade on right
 *      half → progress fill → water-line dash → snow cap → outline stroke
 *      on top → flagpole → flag → world name
 *   6. Wobbly ground baseline drawn after the mountains
 *   7. Below-mountain labels
 *
 * Hand-drawn quality is achieved via a seeded perpendicular Bézier wobble
 * on each edge — deterministic per mountain (so renders are stable) and
 * cheap (no rough.js dependency, no DOM-imperative coupling). The wobbly
 * silhouette is reused as the clipPath, so progress fills, water lines,
 * and snow caps hug the wobbly edge exactly rather than the math triangle.
 */
import React from 'react';
import type { WorldId } from './WorldIconBlob';

export interface WorldProgress {
  completed: number;
  total: number;
}

interface MountainLandscapeProps {
  progress: Record<WorldId, WorldProgress>;
  className?: string;
}

interface PeakConfig {
  id: WorldId;
  label: string;
  baseLeft: number;
  baseRight: number;
  summitX: number;
  summitY: number;
  /** Soft snow-cap colour used as the progress fill. */
  snowColor: string;
  /** Saturated flag colour — used for the snow cap, flag, and pole tip. */
  flagColor: string;
  silhouetteStroke?: number;
  /** Seed feeding the wobble RNG so each mountain has a stable, unique shape. */
  seed: number;
}

const BASE_Y = 380;
const VIEWBOX_W = 1100;
const VIEWBOX_H = 480;

const PEAKS: PeakConfig[] = [
  { id: 'mind',   label: 'Mind',   baseLeft:  60, baseRight:  300, summitX: 180, summitY: 140, snowColor: '#B8C9E5', flagColor: '#5B7DB0', seed: 17,  silhouetteStroke: 1.9 },
  { id: 'growth', label: 'Growth', baseLeft: 250, baseRight:  470, summitX: 360, summitY: 200, snowColor: '#F5C9A8', flagColor: '#D89060', seed: 41,  silhouetteStroke: 1.9 },
  { id: 'learn',  label: 'Learn',  baseLeft: 430, baseRight:  690, summitX: 560, summitY:  90, snowColor: '#B8DDC8', flagColor: '#2A7D6F', seed: 73,  silhouetteStroke: 2.0 },
  { id: 'decode', label: 'Decode', baseLeft: 650, baseRight:  890, summitX: 770, summitY: 180, snowColor: '#F0BFCE', flagColor: '#C76489', seed: 109, silhouetteStroke: 1.9 },
  { id: 'exam',   label: 'Exam',   baseLeft: 850, baseRight: 1080, summitX: 970, summitY: 160, snowColor: '#F5BFB0', flagColor: '#D85F47', seed: 197, silhouetteStroke: 1.9 },
];

const SERIF: React.CSSProperties = { fontFamily: "'Source Serif 4', serif" };
const SANS: React.CSSProperties = { fontFamily: "'DM Sans', system-ui, sans-serif" };

/** Seeded pseudo-random in [0, 1). Same seed → same value, every render. */
function seededRand(seed: number, k: number): number {
  const v = Math.sin(seed * 12.9898 + k * 78.233) * 43758.5453;
  return v - Math.floor(v);
}

/** Build an SVG sub-path drawing a hand-drawn-looking edge from (x1,y1) to
 *  (x2,y2) using `segments` Q-curves with control points offset perpendicular
 *  to the edge by up to ±amplitude. The end of the final segment lands
 *  exactly on (x2,y2) so consecutive edges chain cleanly. */
function wobblyEdge(
  x1: number, y1: number,
  x2: number, y2: number,
  seed: number,
  segments = 5,
  amplitude = 2.2,
): string {
  const dx = x2 - x1;
  const dy = y2 - y1;
  const len = Math.sqrt(dx * dx + dy * dy);
  if (len < 0.001) return '';
  const nx = -dy / len;
  const ny = dx / len;

  let out = '';
  for (let i = 1; i <= segments; i++) {
    const t = i / segments;
    const px = x1 + dx * t;
    const py = y1 + dy * t;
    const endOff = i === segments ? 0 : (seededRand(seed, i * 2) - 0.5) * 2 * amplitude;
    const ex = px + nx * endOff;
    const ey = py + ny * endOff;

    const midT = (t + (i - 1) / segments) / 2;
    const midPx = x1 + dx * midT;
    const midPy = y1 + dy * midT;
    const ctrlOff = (seededRand(seed, i * 2 + 1) - 0.5) * 2 * amplitude;
    const cx = midPx + nx * ctrlOff;
    const cy = midPy + ny * ctrlOff;

    out += ` Q ${cx.toFixed(2)} ${cy.toFixed(2)} ${ex.toFixed(2)} ${ey.toFixed(2)}`;
  }
  return out;
}

/** Wobbly horizontal line — used for the ground baseline. */
function wobblyHorizontal(x1: number, y: number, x2: number, seed: number, segments = 30, amplitude = 0.8): string {
  let out = `M ${x1} ${y}`;
  out += wobblyEdge(x1, y, x2, y, seed, segments, amplitude);
  return out;
}

/** Build the closed wobbly silhouette for a mountain — used both as the
 *  visible outline AND the clipPath. */
function buildMountainPath(p: PeakConfig): string {
  return (
    `M ${p.baseLeft} ${BASE_Y}` +
    wobblyEdge(p.baseLeft, BASE_Y, p.summitX, p.summitY, p.seed, 6, 2.2) +
    wobblyEdge(p.summitX, p.summitY, p.baseRight, BASE_Y, p.seed + 1000, 6, 2.2) +
    ' Z'
  );
}

/** Right-half shade region — quadrilateral covering the lower-right of the
 *  triangle. Diagonal upper edge runs from base midpoint up to a point
 *  25% down the central axis (per the spec). */
function buildShadePath(p: PeakConfig): string {
  const midX = (p.baseLeft + p.baseRight) / 2;
  const innerY = p.summitY + 0.25 * (BASE_Y - p.summitY);
  return `M ${p.summitX} ${p.summitY} L ${p.baseRight} ${BASE_Y} L ${midX} ${BASE_Y} L ${p.summitX} ${innerY} Z`;
}

/** Coloured peak fill — the top 14% of the mountain in the world's flag
 *  colour. A simple triangle from the summit down to a wobbly horizontal
 *  line at cap_bottom_y. Both bottom corners overshoot the mountain edge
 *  so the mountain's clipPath cleanly trims the cap to the wobbly
 *  silhouette — gives the impression of snow following the rocky peak. */
function buildCapPath(p: PeakConfig): string {
  const sx = p.summitX, sy = p.summitY;
  const mountainHeight = BASE_Y - sy;
  const capH = 0.14 * mountainHeight;
  const capBottomY = sy + capH;

  const leftSlope = (BASE_Y - sy) / (sx - p.baseLeft);
  const rightSlope = (BASE_Y - sy) / (p.baseRight - sx);
  const overshoot = 5;
  const leftX = sx - capH / leftSlope - overshoot;
  const rightX = sx + capH / rightSlope + overshoot;

  return (
    `M ${sx.toFixed(2)} ${(sy - 3).toFixed(2)}` +
    ` L ${leftX.toFixed(2)} ${capBottomY.toFixed(2)}` +
    wobblyEdge(leftX, capBottomY, rightX, capBottomY, p.seed + 5000, 5, 0.8) +
    ' Z'
  );
}

/** Hand-drawn flag — triangle attached to the right of the flagpole top. */
function buildFlagPath(sx: number, sy: number, seed: number): string {
  const tip = [sx, sy] as const;
  const right = [sx + 18, sy + 4] as const;
  const bottom = [sx, sy + 10] as const;
  return (
    `M ${tip[0]} ${tip[1]}` +
    wobblyEdge(tip[0], tip[1], right[0], right[1], seed + 11, 2, 0.45) +
    wobblyEdge(right[0], right[1], bottom[0], bottom[1], seed + 22, 2, 0.45) +
    wobblyEdge(bottom[0], bottom[1], tip[0], tip[1], seed + 33, 2, 0.45) +
    ' Z'
  );
}

export const MountainLandscape: React.FC<MountainLandscapeProps> = ({ progress, className }) => {
  // Pre-compute per-mountain paths so the same wobble feeds both the
  // visible silhouette and the clip path — fills hug the wobbly edge.
  const mountainPaths = PEAKS.map(p => buildMountainPath(p));
  const shadePaths = PEAKS.map(p => buildShadePath(p));

  return (
    <svg
      viewBox={`0 0 ${VIEWBOX_W} ${VIEWBOX_H}`}
      width="100%"
      height="auto"
      className={className}
      role="img"
      aria-label="Mountain landscape showing progress in each of the five worlds"
    >
      <defs>
        {/* Diagonal pencil-stroke pattern for shading */}
        <pattern id="ml-shade-pattern" patternUnits="userSpaceOnUse" width="6" height="6" patternTransform="rotate(45)">
          <line x1="0" y1="0" x2="0" y2="6" stroke="#1a1a1a" strokeWidth="0.4" opacity="0.18" />
        </pattern>

        {/* Per-mountain wobbly clipPath (silhouette = clip) */}
        {PEAKS.map((p, i) => (
          <clipPath key={`mc-${p.id}`} id={`ml-clip-${p.id}`}>
            <path d={mountainPaths[i]} />
          </clipPath>
        ))}
        {/* Per-mountain right-half shade clipPath */}
        {PEAKS.map((p, i) => (
          <clipPath key={`ms-${p.id}`} id={`ml-shade-clip-${p.id}`}>
            <path d={shadePaths[i]} />
          </clipPath>
        ))}
      </defs>

      {/* SVG background is transparent — the cream tile beneath shows
          through, so the landscape blends with the card rather than
          reading as a separate coloured block. */}

      {/* Sun upper-right (atmospheric, decorative) */}
      <g opacity="0.4">
        <circle cx="1030" cy="58" r="14" fill="none" stroke="#1a1a1a" strokeWidth="1.1" />
        <line x1="1030" y1="32" x2="1030" y2="38" stroke="#1a1a1a" strokeWidth="1.1" strokeLinecap="round" />
        <line x1="1054" y1="58" x2="1060" y2="58" stroke="#1a1a1a" strokeWidth="1.1" strokeLinecap="round" />
        <line x1="1006" y1="36" x2="1011" y2="42" stroke="#1a1a1a" strokeWidth="1.1" strokeLinecap="round" />
      </g>

      {/* Per-mountain stack — left to right; later peaks paint over
            earlier peaks in their overlap zones, producing a continuous
            ridge silhouette. */}
      {PEAKS.map((p, i) => {
        const wp = progress[p.id] ?? { completed: 0, total: 0 };
        const ratio = wp.total > 0 ? Math.max(0, Math.min(1, wp.completed / wp.total)) : 0;
        const heightPx = BASE_Y - p.summitY;
        const fillHeight = heightPx * ratio;
        const fillTopY = BASE_Y - fillHeight;
        const stroke = p.silhouetteStroke ?? 1.9;
        const path = mountainPaths[i];
        const clipUrl = `url(#ml-clip-${p.id})`;
        const shadeClipUrl = `url(#ml-shade-clip-${p.id})`;

        // Flagpole roots at the summit — the apex of the snow cap.
        const poleBaseX = p.summitX;
        const poleBaseY = p.summitY;
        const poleTopY = poleBaseY - 30;

        return (
          <g key={p.id}>
            {/* 1. White triangle silhouette fill */}
            <path d={path} fill="white" stroke="none" />

            {/* 2. Pencil shading on the right half */}
            <rect
              x={p.baseLeft}
              y={p.summitY}
              width={p.baseRight - p.baseLeft}
              height={BASE_Y - p.summitY}
              fill="url(#ml-shade-pattern)"
              clipPath={shadeClipUrl}
            />

            {/* 3. Progress fill — clipped to the wobbly silhouette */}
            {ratio > 0 && (
              <rect
                x={p.baseLeft}
                y={fillTopY}
                width={p.baseRight - p.baseLeft}
                height={fillHeight}
                fill={p.snowColor}
                opacity="0.88"
                clipPath={clipUrl}
              />
            )}

            {/* 4. Water-level dashed line */}
            {ratio > 0 && (
              <line
                x1={p.baseLeft}
                y1={fillTopY}
                x2={p.baseRight}
                y2={fillTopY}
                stroke="#1a1a1a"
                strokeWidth="1"
                strokeDasharray="3 3"
                opacity="0.5"
                clipPath={clipUrl}
              />
            )}

            {/* 5. Coloured peak — the top portion of the mountain in the
                  world's flag colour, clipped to the wobbly silhouette so
                  the colour follows the same edges as the dark outline. */}
            <path
              d={buildCapPath(p)}
              fill={p.flagColor}
              stroke="none"
              clipPath={clipUrl}
            />

            {/* Mountain outline — drawn on top so the dark silhouette
                stays crisp regardless of the fills underneath. */}
            <path d={path} fill="none" stroke="#1a1a1a" strokeWidth={stroke} strokeLinejoin="round" strokeLinecap="round" />

            {/* 6. Flagpole — straight from the summit up */}
            <path
              d={`M ${poleBaseX} ${poleBaseY}` + wobblyEdge(poleBaseX, poleBaseY, poleBaseX, poleTopY, p.seed + 2000, 4, 0.5)}
              fill="none"
              stroke="#1a1a1a"
              strokeWidth="1.4"
              strokeLinecap="round"
            />

            {/* 7. Triangular flag — attached to the top of the pole */}
            <path
              d={buildFlagPath(poleBaseX, poleTopY, p.seed + 3000)}
              fill={p.flagColor}
              stroke="#1a1a1a"
              strokeWidth="1.3"
              strokeLinejoin="round"
              strokeLinecap="round"
            />

            {/* 8. World name label — clear of the flag */}
            <text
              x={p.summitX}
              y={poleTopY - 10}
              textAnchor="middle"
              fontSize="13"
              fontWeight="500"
              fill="#1a1a1a"
              style={SERIF}
            >
              {p.label}
            </text>
          </g>
        );
      })}

      {/* 6. Hand-drawn ground baseline — drawn after mountains so the
            wobble reads as a continuous ground stroke across the scene */}
      <path
        d={wobblyHorizontal(20, BASE_Y, 1080, 991, 40, 0.9)}
        fill="none"
        stroke="#1a1a1a"
        strokeWidth="1.4"
        opacity="0.55"
        strokeLinecap="round"
      />

      {/* 7. Below-mountain labels — percentage + module count */}
      {PEAKS.map(p => {
        const wp = progress[p.id] ?? { completed: 0, total: 0 };
        const ratio = wp.total > 0 ? Math.max(0, Math.min(1, wp.completed / wp.total)) : 0;
        const pct = wp.total > 0 ? Math.round(ratio * 100) : 0;
        return (
          <g key={`label-${p.id}`}>
            <text
              x={p.summitX}
              y={412}
              textAnchor="middle"
              fontSize="22"
              fontWeight="500"
              fill="#1a1a1a"
              style={SERIF}
            >
              {pct}%
            </text>
            <text
              x={p.summitX}
              y={432}
              textAnchor="middle"
              fontSize="10"
              fill="rgba(0,0,0,0.55)"
              letterSpacing="1"
              style={SANS}
            >
              {wp.completed} / {wp.total}
            </text>
          </g>
        );
      })}
    </svg>
  );
};

export default MountainLandscape;
