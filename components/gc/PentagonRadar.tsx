/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';

interface PentagonRadarProps {
  values: number[]; // 5 values, 0-100
  labels: string[];
  colors?: { fill: string; stroke: string };
  size?: number;
}

const GRID_LEVELS = [20, 40, 60, 80, 100];

function getVertex(index: number, radius: number, cx: number, cy: number): [number, number] {
  const angle = (index * 2 * Math.PI) / 5 - Math.PI / 2;
  return [cx + radius * Math.cos(angle), cy + radius * Math.sin(angle)];
}

function polygonPoints(values: number[], maxRadius: number, cx: number, cy: number): string {
  return values
    .map((v, i) => {
      const r = (v / 100) * maxRadius;
      const [x, y] = getVertex(i, r, cx, cy);
      return `${x},${y}`;
    })
    .join(' ');
}

function gridPolygon(level: number, maxRadius: number, cx: number, cy: number): string {
  const r = (level / 100) * maxRadius;
  return Array.from({ length: 5 })
    .map((_, i) => {
      const [x, y] = getVertex(i, r, cx, cy);
      return `${x},${y}`;
    })
    .join(' ');
}

export const PentagonRadar: React.FC<PentagonRadarProps> = ({
  values,
  labels,
  colors = { fill: 'rgba(204, 120, 92, 0.25)', stroke: 'rgba(204, 120, 92, 0.8)' },
  size = 200,
}) => {
  // Use a larger internal viewBox with padding so labels don't clip
  const pad = 80;
  const vbSize = size + pad * 2;
  const cx = vbSize / 2;
  const cy = vbSize / 2;
  const maxRadius = size * 0.44;
  const labelRadius = maxRadius + 30;

  const gradientId = `radar-gradient-${size}`;
  const glowId = `radar-glow-${size}`;

  return (
    <svg width={size} height={size} viewBox={`0 0 ${vbSize} ${vbSize}`} className="mx-auto">
      <defs>
        {/* Radial gradient fill for data polygon */}
        <radialGradient id={gradientId} cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="rgba(204, 120, 92, 0.35)" />
          <stop offset="100%" stopColor="rgba(204, 120, 92, 0.08)" />
        </radialGradient>
        {/* Drop-shadow glow */}
        <filter id={glowId} x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur" />
          <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0.8  0 0 0 0 0.47  0 0 0 0 0.36  0 0 0 0.4 0" result="glow" />
          <feMerge>
            <feMergeNode in="glow" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      {/* Grid pentagons — inner dashed, outer solid */}
      {GRID_LEVELS.map(level => (
        <polygon
          key={level}
          points={gridPolygon(level, maxRadius, cx, cy)}
          fill="none"
          stroke="currentColor"
          className="text-zinc-200 dark:text-zinc-700"
          strokeWidth={level === 100 ? 1.5 : 0.75}
          strokeDasharray={level < 100 ? '4 3' : 'none'}
        />
      ))}

      {/* Axis lines */}
      {Array.from({ length: 5 }).map((_, i) => {
        const [x, y] = getVertex(i, maxRadius, cx, cy);
        return (
          <line
            key={i}
            x1={cx}
            y1={cy}
            x2={x}
            y2={y}
            stroke="currentColor"
            className="text-zinc-200 dark:text-zinc-700"
            strokeWidth={0.75}
          />
        );
      })}

      {/* Data polygon with radial gradient + glow */}
      <polygon
        points={polygonPoints(values, maxRadius, cx, cy)}
        fill={`url(#${gradientId})`}
        stroke={colors.stroke}
        strokeWidth={2}
        filter={`url(#${glowId})`}
      />

      {/* Data points with glow */}
      {values.map((v, i) => {
        const r = (v / 100) * maxRadius;
        const [x, y] = getVertex(i, r, cx, cy);
        return (
          <circle
            key={i}
            cx={x}
            cy={y}
            r={4}
            fill={colors.stroke}
            filter={`url(#${glowId})`}
          />
        );
      })}

      {/* Labels */}
      {labels.map((label, i) => {
        const [x, y] = getVertex(i, labelRadius, cx, cy);
        return (
          <text
            key={i}
            x={x}
            y={y}
            textAnchor="middle"
            dominantBaseline="middle"
            className="fill-zinc-600 dark:fill-zinc-300 text-[16px] font-semibold"
          >
            {label}
          </text>
        );
      })}
    </svg>
  );
};
