/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Reusable per-category decorative motifs. Each category has a signature
 * visual (rings, branch, dots, layered papers, line-to-target) that appears
 * across the IA — at home, on the Modules page, and inside ModuleShowcase —
 * so the same world reads as the same world wherever it lives.
 *
 * The full progress-encoding versions (water rising, branch extending, etc.)
 * are inlined in ModulesView.tsx because they're tightly coupled to the
 * layout there. These shared components are decorative only.
 */

import React from 'react';
import { motion } from 'framer-motion';

export type MotifCategoryId =
  | 'architecture-mindset'
  | 'science-growth'
  | 'learning-cheat-codes'
  | 'subject-specific-science'
  | 'exam-zone';

interface MotifProps {
  color: string;
  size?: number;
  /** Background opacity floor (0–1). Defaults to 0.18. */
  baseOpacity?: number;
  /** Animation amplitude (0–1). Defaults to 0.25. */
  peakOpacity?: number;
  className?: string;
}

// ── 01 Mind — concentric rings, breathing ──

export const MindMotif: React.FC<MotifProps> = ({
  color,
  size = 80,
  baseOpacity = 0.18,
  peakOpacity = 0.36,
  className = '',
}) => (
  <svg
    className={`pointer-events-none ${className}`}
    width={size}
    height={size}
    viewBox="-40 -40 80 80"
    aria-hidden="true"
  >
    {[34, 24, 15, 7].map((r, i) => (
      <motion.circle
        key={r}
        cx="0"
        cy="0"
        r={r}
        fill="none"
        stroke={color}
        strokeWidth="1.25"
        animate={{ opacity: [baseOpacity, peakOpacity, baseOpacity] }}
        transition={{ duration: 4 + i * 0.4, repeat: Infinity, ease: 'easeInOut', delay: i * 0.3 }}
      />
    ))}
  </svg>
);

// ── 02 Growth — concentric arcs fanning from a focal point (emergence) ──

export const GrowthMotif: React.FC<MotifProps> = ({
  color,
  size = 80,
  baseOpacity = 0.10,
  peakOpacity = 0.34,
  className = '',
}) => (
  <svg
    className={`pointer-events-none ${className}`}
    width={size}
    height={size * 0.85}
    viewBox="0 0 80 68"
    aria-hidden="true"
  >
    {[18, 30, 42, 54, 66].map((r, i) => (
      <motion.circle
        key={r}
        cx="70"
        cy="64"
        r={r}
        fill="none"
        stroke={color}
        strokeWidth="1.1"
        animate={{ opacity: [baseOpacity, peakOpacity, baseOpacity] }}
        transition={{ duration: 5.5, repeat: Infinity, ease: 'easeInOut', delay: i * 0.35 }}
      />
    ))}
  </svg>
);

// ── 03 Learn — three stacked sine waves drifting horizontally (rhythm) ──

export const LearnMotif: React.FC<MotifProps> = ({
  color,
  size = 80,
  baseOpacity = 0.32,
  className = '',
}) => {
  const wavePath = (yBase: number) =>
    `M -10 ${yBase} Q 5 ${yBase - 7} 20 ${yBase} T 50 ${yBase} T 80 ${yBase} T 110 ${yBase}`;
  return (
    <svg
      className={`pointer-events-none ${className}`}
      width={size}
      height={size * 0.7}
      viewBox="0 0 80 56"
      aria-hidden="true"
    >
      <motion.path
        d={wavePath(14)}
        stroke={color}
        strokeWidth="1.5"
        fill="none"
        opacity={Math.min(1, baseOpacity + 0.15)}
        strokeLinecap="round"
        animate={{ x: [0, -10, 0] }}
        transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
      />
      <motion.path
        d={wavePath(28)}
        stroke={color}
        strokeWidth="1.5"
        fill="none"
        opacity={baseOpacity}
        strokeLinecap="round"
        animate={{ x: [0, 8, 0] }}
        transition={{ duration: 6, repeat: Infinity, ease: 'easeInOut', delay: 0.4 }}
      />
      <motion.path
        d={wavePath(42)}
        stroke={color}
        strokeWidth="1.5"
        fill="none"
        opacity={Math.max(0.05, baseOpacity - 0.12)}
        strokeLinecap="round"
        animate={{ x: [0, -6, 0] }}
        transition={{ duration: 10, repeat: Infinity, ease: 'easeInOut', delay: 0.8 }}
      />
    </svg>
  );
};

// ── 04 Decode — three layered translucent rectangles ──

export const DecodeMotif: React.FC<MotifProps> = ({
  color,
  size = 80,
  className = '',
}) => {
  const w = size * 0.52;
  const h = size * 0.66;
  return (
    <svg
      className={`pointer-events-none ${className}`}
      width={size}
      height={size * 0.85}
      viewBox={`0 0 ${size} ${size * 0.85}`}
      aria-hidden="true"
    >
      <rect x={size * 0.32} y={size * 0.15} width={w} height={h} rx="5" fill={color} opacity="0.10" />
      <rect x={size * 0.26} y={size * 0.10} width={w} height={h} rx="5" fill={color} opacity="0.18" />
      <rect x={size * 0.20} y={size * 0.05} width={w} height={h} rx="5" fill={color} opacity="0.32" />
    </svg>
  );
};

// ── 05 Exam — diagonal line + target ──

export const ExamMotif: React.FC<MotifProps> = ({
  color,
  size = 80,
  className = '',
}) => (
  <svg
    className={`pointer-events-none ${className}`}
    width={size}
    height={size * 0.85}
    viewBox="0 0 80 68"
    aria-hidden="true"
  >
    <line x1="14" y1="56" x2="64" y2="14" stroke={color} strokeWidth="1" opacity="0.20" strokeDasharray="2 4" />
    <motion.line
      x1="14"
      y1="56"
      x2="64"
      y2="14"
      stroke={color}
      strokeWidth="1.75"
      strokeLinecap="round"
      strokeDasharray="68 68"
      initial={{ strokeDashoffset: 68 }}
      animate={{ strokeDashoffset: [68, 0, 0, 68] }}
      transition={{ duration: 8, times: [0, 0.4, 0.7, 1], repeat: Infinity, ease: 'easeInOut' }}
      opacity="0.55"
    />
    <circle cx="14" cy="56" r="3" fill={color} opacity="0.6" />
    <circle cx="64" cy="14" r="6" fill="none" stroke={color} strokeWidth="1.25" opacity="0.5" />
    <circle cx="64" cy="14" r="2" fill={color} opacity="0.7" />
  </svg>
);

// ── Dispatcher ──

export const CategoryMotif: React.FC<MotifProps & { categoryId: MotifCategoryId }> = ({ categoryId, ...rest }) => {
  switch (categoryId) {
    case 'architecture-mindset': return <MindMotif {...rest} />;
    case 'science-growth':       return <GrowthMotif {...rest} />;
    case 'learning-cheat-codes': return <LearnMotif {...rest} />;
    case 'subject-specific-science': return <DecodeMotif {...rest} />;
    case 'exam-zone':            return <ExamMotif {...rest} />;
    default: return null;
  }
};
