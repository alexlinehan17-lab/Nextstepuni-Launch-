/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { motion } from 'framer-motion';

const MotionPath = motion.path as any;
const MotionEllipse = motion.ellipse as any;
const MotionCircle = motion.circle as any;

// Leaf shape helper — returns a pointed-oval SVG path at a given position/angle/size
const leafPath = (cx: number, cy: number, size: number, angle: number): string => {
  const rad = (angle * Math.PI) / 180;
  const cos = Math.cos(rad);
  const sin = Math.sin(rad);
  const tip = size;
  const width = size * 0.4;

  const tx = (x: number, y: number) => `${cx + x * cos - y * sin},${cy + x * sin + y * cos}`;

  return `M ${tx(0, 0)} C ${tx(tip * 0.3, -width)}, ${tx(tip * 0.7, -width)}, ${tx(tip, 0)} C ${tx(tip * 0.7, width)}, ${tx(tip * 0.3, width)}, ${tx(0, 0)} Z`;
};

// How much of a vine's path to draw based on progress and the vine's start/end thresholds
const getVineLength = (progress: number, start: number, end: number): number => {
  if (progress <= start) return 0;
  if (progress >= end) return 1;
  return (progress - start) / (end - start);
};

// Vine definitions — each has a progress range where it grows from 0→1 pathLength
const VINES = [
  { d: 'M 10,490 C 15,400 5,350 12,280 C 18,220 8,180 15,120', delay: 0, start: 5, end: 40 },
  { d: 'M 390,495 C 385,420 395,370 388,300 C 382,260 392,230 386,200', delay: 0.2, start: 15, end: 55 },
  { d: 'M 5,495 C 60,488 120,492 180,486 C 240,480 300,488 340,484', delay: 0.4, start: 30, end: 70 },
  { d: 'M 395,10 C 388,40 392,70 385,100 C 380,120 386,140 382,160', delay: 0.6, start: 50, end: 85 },
];

// Leaves — each has a progress threshold at which it appears (aligned to its parent vine's growth)
const LEAVES = [
  // Left vine leaves
  { cx: 12, cy: 380, size: 18, angle: -40, delay: 0.5, threshold: 12 },
  { cx: 8, cy: 320, size: 15, angle: 35, delay: 0.58, threshold: 18 },
  { cx: 15, cy: 260, size: 16, angle: -50, delay: 0.66, threshold: 24 },
  { cx: 10, cy: 200, size: 13, angle: 40, delay: 0.74, threshold: 30 },
  { cx: 14, cy: 150, size: 11, angle: -35, delay: 0.82, threshold: 36 },
  // Right vine leaves
  { cx: 390, cy: 400, size: 17, angle: 210, delay: 0.6, threshold: 22 },
  { cx: 386, cy: 340, size: 14, angle: -210, delay: 0.68, threshold: 32 },
  { cx: 392, cy: 270, size: 12, angle: 220, delay: 0.76, threshold: 42 },
  { cx: 388, cy: 220, size: 10, angle: -215, delay: 0.84, threshold: 52 },
  // Bottom vine leaves
  { cx: 80, cy: 490, size: 14, angle: -80, delay: 0.7, threshold: 38 },
  { cx: 160, cy: 488, size: 16, angle: -90, delay: 0.78, threshold: 48 },
  { cx: 260, cy: 484, size: 13, angle: -85, delay: 0.86, threshold: 58 },
  // Top-right vine leaves
  { cx: 388, cy: 60, size: 12, angle: 210, delay: 0.9, threshold: 60 },
  { cx: 384, cy: 130, size: 10, angle: -200, delay: 0.98, threshold: 70 },
];

// Flowers — only bloom at high progress
const FLOWERS = [
  { cx: 15, cy: 120, size: 8, delay: 1.2, threshold: 65 },
  { cx: 386, cy: 200, size: 7, delay: 1.35, threshold: 80 },
  { cx: 340, cy: 484, size: 6, delay: 1.5, threshold: 90 },
  { cx: 382, cy: 160, size: 5, delay: 1.65, threshold: 100 },
];

interface VineSvgProps {
  progress: number;
  vineStroke: string;
  leafFill: string;
  petalFill: string;
  centerFill: string;
}

const VineSvg: React.FC<VineSvgProps> = ({ progress, vineStroke, leafFill, petalFill, centerFill }) => (
  <>
    {/* Vine stems — grow proportionally */}
    {VINES.map((vine, i) => {
      const target = getVineLength(progress, vine.start, vine.end);
      if (target <= 0) return null;
      return (
        <MotionPath
          key={`vine-${i}`}
          d={vine.d}
          stroke={vineStroke}
          strokeWidth={2.5}
          strokeLinecap="round"
          fill="none"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: target }}
          transition={{ duration: 1.2, delay: vine.delay, ease: 'easeOut' }}
        />
      );
    })}

    {/* Leaves — appear when progress crosses their threshold */}
    {LEAVES.map((leaf, i) => {
      if (progress < leaf.threshold) return null;
      return (
        <MotionPath
          key={`leaf-${i}`}
          d={leafPath(leaf.cx, leaf.cy, leaf.size, leaf.angle)}
          fill={leafFill}
          stroke="none"
          initial={{ pathLength: 0, fillOpacity: 0 }}
          animate={{ pathLength: 1, fillOpacity: 1 }}
          transition={{ duration: 0.5, delay: leaf.delay, ease: 'easeOut' }}
        />
      );
    })}

    {/* Flowers — bloom at high progress */}
    {FLOWERS.map((flower, i) => {
      if (progress < flower.threshold) return null;
      return (
        <motion.g
          key={`flower-${i}`}
          initial={{ scale: 0, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5, delay: flower.delay, ease: 'backOut' }}
          style={{ transformOrigin: `${flower.cx}px ${flower.cy}px` }}
        >
          {[0, 72, 144, 216, 288].map((rot) => (
            <MotionEllipse
              key={rot}
              cx={flower.cx}
              cy={flower.cy - flower.size * 0.8}
              rx={flower.size * 0.35}
              ry={flower.size * 0.7}
              fill={petalFill}
              transform={`rotate(${rot} ${flower.cx} ${flower.cy})`}
            />
          ))}
          <MotionCircle
            cx={flower.cx}
            cy={flower.cy}
            r={flower.size * 0.3}
            fill={centerFill}
          />
        </motion.g>
      );
    })}
  </>
);

interface CompletionVinesProps {
  progress: number; // 0–100
}

export const CompletionVines: React.FC<CompletionVinesProps> = ({ progress }) => {
  if (progress <= 0) return null;

  return (
    <div className="absolute inset-0 z-[5] pointer-events-none">
      {/* Light mode */}
      <svg
        className="block dark:hidden w-full h-full"
        viewBox="0 0 400 500"
        preserveAspectRatio="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <VineSvg
          progress={progress}
          vineStroke="rgba(107,143,113,0.35)"
          leafFill="rgba(123,168,130,0.25)"
          petalFill="rgba(204,120,92,0.30)"
          centerFill="rgba(181,101,74,0.40)"
        />
      </svg>

      {/* Dark mode */}
      <svg
        className="hidden dark:block w-full h-full"
        viewBox="0 0 400 500"
        preserveAspectRatio="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <VineSvg
          progress={progress}
          vineStroke="rgba(143,185,150,0.20)"
          leafFill="rgba(163,209,171,0.15)"
          petalFill="rgba(212,147,111,0.25)"
          centerFill="rgba(204,120,92,0.30)"
        />
      </svg>
    </div>
  );
};
