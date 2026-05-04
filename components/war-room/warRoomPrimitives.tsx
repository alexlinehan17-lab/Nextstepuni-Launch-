/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// Editorial UI primitives shared across the War Room redesign.
// Hand-drawn SVG motifs + small reusable components to keep the four panels visually consistent.

import React from 'react';
import {
  PAPER, PAPER_SOFT, INK, INK_SOFT, INK_MUTE, INK_FAINT, ACCENT,
} from './warRoomShared';

// ── Hand-drawn SVG motifs ──────────────────────────────────

export const SunburstRule: React.FC<{ width?: number; color?: string }> = ({ width = 70, color = ACCENT }) => (
  <svg width={width} height="10" viewBox="0 0 70 10" fill="none" aria-hidden>
    <path d="M2 5 Q 18 3, 36 5 T 68 5" stroke={color} strokeWidth={1.2} strokeLinecap="round" />
    <path d="M30 2 L 32 0" stroke={color} strokeWidth={0.9} strokeLinecap="round" />
    <path d="M34 1 L 35 -1" stroke={color} strokeWidth={0.9} strokeLinecap="round" />
    <path d="M38 2 L 40 0" stroke={color} strokeWidth={0.9} strokeLinecap="round" />
  </svg>
);

export const SketchedFlag: React.FC<{ size?: number; color?: string }> = ({ size = 24, color = INK }) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" aria-hidden>
    <path d="M8 28 L 8 4" stroke={color} strokeWidth={1.3} strokeLinecap="round" />
    <path d="M8 4 Q 18 6, 24 4 Q 22 10, 24 14 Q 16 12, 8 14 Z" fill={ACCENT} stroke={color} strokeWidth={1.1} strokeLinejoin="round" />
  </svg>
);

export const SketchedStar: React.FC<{ size?: number; color?: string }> = ({ size = 22, color = ACCENT }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" aria-hidden>
    <path d="M12 3 L 14.3 9.4 L 21 9.7 L 15.7 13.8 L 17.6 20.3 L 12 16.6 L 6.4 20.3 L 8.3 13.8 L 3 9.7 L 9.7 9.4 Z"
          stroke={color} strokeWidth={1.3} strokeLinejoin="round" strokeLinecap="round" />
  </svg>
);

export const SketchedLeaf: React.FC<{ size?: number; color?: string }> = ({ size = 28, color = INK }) => (
  <svg width={size} height={size} viewBox="0 0 64 64" fill="none" aria-hidden>
    <path d="M16 48 Q 18 18, 48 16 Q 46 46, 16 48 Z" stroke={color} strokeWidth={1.3} fill="rgba(94,139,126,0.16)" strokeLinejoin="round" />
    <path d="M18 46 L 46 18" stroke={color} strokeWidth={0.9} strokeLinecap="round" />
  </svg>
);

export const SketchedHorizon: React.FC<{ width?: number; height?: number; color?: string }> = ({ width = 280, height = 60, color = INK }) => (
  <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} fill="none" aria-hidden>
    {/* gentle horizon line with a tiny flag at the end */}
    <path d={`M2 ${height - 12} Q ${width * 0.3} ${height - 22}, ${width * 0.55} ${height - 18} T ${width - 18} ${height - 14}`}
          stroke={color} strokeWidth={1.1} strokeLinecap="round" />
    <path d={`M${width - 16} ${height - 14} L ${width - 16} ${height - 32}`} stroke={color} strokeWidth={1} strokeLinecap="round" />
    <path d={`M${width - 16} ${height - 32} Q ${width - 8} ${height - 30}, ${width - 4} ${height - 32} Q ${width - 6} ${height - 28}, ${width - 4} ${height - 24} Q ${width - 12} ${height - 26}, ${width - 16} ${height - 24} Z`}
          fill={ACCENT} stroke={color} strokeWidth={0.9} strokeLinejoin="round" />
    {/* small dashes suggesting path */}
    <path d={`M${width * 0.18} ${height - 18} l 4 0`} stroke={color} strokeWidth={0.8} strokeLinecap="round" strokeOpacity={0.5} />
    <path d={`M${width * 0.4} ${height - 19} l 5 0`} stroke={color} strokeWidth={0.8} strokeLinecap="round" strokeOpacity={0.5} />
    <path d={`M${width * 0.7} ${height - 17} l 4 0`} stroke={color} strokeWidth={0.8} strokeLinecap="round" strokeOpacity={0.5} />
  </svg>
);

// Decorative dashed paper-rule used for section dividers.
export const PaperRule: React.FC<{ className?: string }> = ({ className = '' }) => (
  <div className={`w-full h-px ${className}`} aria-hidden style={{
    backgroundImage: `radial-gradient(circle, ${INK_MUTE} 0.9px, transparent 1px)`,
    backgroundSize: '6px 1px',
    backgroundRepeat: 'repeat-x',
    backgroundPosition: 'center',
    opacity: 0.55,
  }} />
);

// ── Editorial primitives ───────────────────────────────────

export const Overline: React.FC<{ children: React.ReactNode; color?: string; className?: string }> = ({ children, color = INK_MUTE, className = '' }) => (
  <p className={`font-sans text-[10px] font-semibold uppercase tracking-[0.22em] ${className}`} style={{ color }}>{children}</p>
);

// SectionHeader — paired overline + serif title, optional sunburst flourish.
export const SectionHeader: React.FC<{
  overline?: string;
  title: string;
  rule?: boolean;
  ruleColor?: string;
  trailing?: React.ReactNode;
  className?: string;
}> = ({ overline, title, rule = true, ruleColor = ACCENT, trailing, className = '' }) => (
  <div className={`flex items-end justify-between gap-3 ${className}`}>
    <div>
      {overline && <Overline className="mb-1.5">{overline}</Overline>}
      <div className="flex items-center gap-3">
        <h3 className="font-serif text-[20px] sm:text-[22px] font-bold leading-tight" style={{ color: INK }}>{title}</h3>
        {rule && (
          <img
            src="/assets/war-room-rule.png"
            alt=""
            aria-hidden
            style={{ width: 96, height: 'auto', objectFit: 'contain', flexShrink: 0 }}
          />
        )}
      </div>
    </div>
    {trailing && <div className="shrink-0">{trailing}</div>}
  </div>
);

// EditorialCard — white surface with thin charcoal border and faint shadow.
// Default is white across the War Room. The `tone` prop is kept for API compatibility
// but all variants resolve to white; pass an explicit `style.background` to override.
export const EditorialCard: React.FC<{
  children: React.ReactNode;
  className?: string;
  padded?: boolean;
  tone?: 'paper' | 'soft' | 'deep';
  style?: React.CSSProperties;
}> = ({ children, className = '', padded = true, style }) => {
  return (
    <div
      className={`${padded ? 'p-5 sm:p-6' : ''} ${className}`}
      style={{
        background: '#FFFFFF',
        border: `1px solid ${INK}14`,
        borderRadius: 14,
        boxShadow: '0 1px 0 rgba(31,27,23,0.03), 0 6px 20px rgba(31,27,23,0.04)',
        ...style,
      }}
    >
      {children}
    </div>
  );
};

// MutedProgress — soft progress rail used in tables, briefings, coverage.
export const MutedProgress: React.FC<{ value: number; color?: string; height?: number }> = ({ value, color = ACCENT, height = 6 }) => (
  <div className="w-full overflow-hidden" style={{ height, borderRadius: 999, background: `${INK}10` }}>
    <div
      className="h-full transition-all"
      style={{
        width: `${Math.max(0, Math.min(100, value))}%`,
        background: color,
        borderRadius: 999,
      }}
    />
  </div>
);

// Pill — compact label chip used for grades, status badges, etc.
export const Pill: React.FC<{
  children: React.ReactNode;
  bg?: string;
  fg?: string;
  border?: string;
  className?: string;
}> = ({ children, bg = `${INK}10`, fg = INK_SOFT, border, className = '' }) => (
  <span
    className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold ${className}`}
    style={{
      background: bg,
      color: fg,
      border: border ? `1px solid ${border}` : undefined,
      letterSpacing: '0.04em',
    }}
  >
    {children}
  </span>
);

// ConfidenceDot — small filled circle used to mark topic status.
export const ConfidenceDot: React.FC<{ confidence: 'solid' | 'shaky' | 'not-started'; size?: number }> = ({ confidence, size = 10 }) => {
  const fill = confidence === 'solid' ? '#5E8B7E' : confidence === 'shaky' ? '#B8843D' : '#C4BEB3';
  return <span className="inline-block shrink-0" style={{ width: size, height: size, borderRadius: '50%', background: fill, border: `1px solid ${INK}33` }} />;
};

// TextField / Select — muted paper inputs.
export const fieldClass =
  `w-full px-3 py-2 rounded-lg outline-none focus:ring-2 focus:ring-[rgba(204,120,92,0.25)] text-[13px]`;

export const fieldStyle: React.CSSProperties = {
  background: '#FFFFFF',
  border: `1px solid ${INK}1A`,
  color: INK,
};

// Subtle accent button — refined CTA used across panels.
export const accentButtonClass =
  `inline-flex items-center justify-center gap-1.5 px-4 py-2 rounded-full font-semibold text-[13px] transition-all`;

export const accentButtonStyle: React.CSSProperties = {
  background: INK,
  color: PAPER,
  letterSpacing: '0.02em',
  boxShadow: '0 2px 0 rgba(31,27,23,0.18)',
};

export const ghostButtonClass =
  `inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-[12px] font-semibold transition-colors`;

export const ghostButtonStyle: React.CSSProperties = {
  background: 'transparent',
  color: INK_SOFT,
  border: `1px solid ${INK}22`,
};

// Re-export tokens for one-stop import.
export { PAPER, PAPER_SOFT, INK, INK_SOFT, INK_MUTE, INK_FAINT, ACCENT };
