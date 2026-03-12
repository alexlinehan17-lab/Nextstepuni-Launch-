/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Zap, Quote } from 'lucide-react';
import { ModuleTheme } from '../types';

interface HighlightProps {
  children?: React.ReactNode;
  description: string;
  theme: ModuleTheme;
}

export const Highlight = ({ children, description, theme }: HighlightProps) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <span className="relative inline-block mx-0.5">
      <button
        onClick={(e) => {
          e.stopPropagation();
          setIsOpen(!isOpen);
        }}
        className={`relative inline-flex items-center px-2 py-0.5 font-bold ${theme.highlightBg} dark:bg-white/10 ${theme.highlightText} dark:text-white rounded-md cursor-help ${theme.highlightHover} transition-all duration-300 ${theme.highlightDecor} underline decoration-2 underline-offset-4`}
      >
        <span className="not-italic">{children}</span>
      </button>
      <AnimatePresence>
        {isOpen && (
          <>
            <div className="fixed inset-0 z-[60]" onClick={() => setIsOpen(false)} />
            <motion.div
              initial={{ opacity: 0, scale: 0.9, y: 10, x: "-50%" }}
              animate={{ opacity: 1, scale: 1, y: 0, x: "-50%" }}
              exit={{ opacity: 0, scale: 0.9, y: 10, x: "-50%" }}
              className="absolute z-[70] bottom-full left-1/2 mb-6 w-72 max-w-[calc(100vw-2rem)] p-6 bg-zinc-900/95 text-white text-xs rounded-2xl shadow-2xl pointer-events-auto leading-relaxed border border-white/10 backdrop-blur-xl whitespace-normal text-left"
              style={{ transformOrigin: 'bottom center' }}
            >
              <div className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-full w-0 h-0 border-l-[10px] border-l-transparent border-r-[10px] border-r-transparent border-t-[10px] border-t-zinc-900/95"></div>
              <p className={`font-sans font-bold ${theme.tooltipAccent} mb-2 uppercase tracking-wider text-[9px]`} style={{ color: 'var(--accent-hex)' }}>Key Insight</p>
              <p className="text-zinc-200 font-medium">{description}</p>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </span>
  );
};

interface ReadingSectionProps {
  title: string;
  eyebrow: string;
  icon: any;
  children?: React.ReactNode;
  theme: ModuleTheme;
}

export const ReadingSection = ({ title, eyebrow, icon: Icon, children, theme }: ReadingSectionProps) => (
  <article className="animate-fade-in">
    <header className="mb-12 text-left relative">
      <div className="absolute -left-16 top-0 hidden xl:block">
        <div className={`w-12 h-12 rounded-2xl bg-zinc-900 flex items-center justify-center ${theme.readingIconColor} shadow-xl border border-white/10`} style={{ color: 'var(--accent-hex)' }}>
          <Icon size={24} />
        </div>
      </div>
      <span className={`inline-flex items-center gap-2 px-3 py-1 ${theme.readingEyebrowBg} ${theme.readingEyebrowText} text-[10px] font-semibold tracking-wider uppercase rounded-full mb-4`} style={{ backgroundColor: 'rgba(var(--accent),0.08)', color: 'var(--accent-hex)' }}>
        {eyebrow}
      </span>
      <h2 className="font-serif text-3xl md:text-5xl leading-tight tracking-tight text-zinc-900 dark:text-white font-semibold">
        {title}
      </h2>
    </header>
    <div className="prose prose-stone dark:prose-invert prose-lg max-w-none space-y-8 text-zinc-600 dark:text-zinc-300 leading-relaxed font-serif overflow-visible">
      {children}
    </div>
  </article>
);

interface MicroCommitmentProps {
  children?: React.ReactNode;
  theme: ModuleTheme;
  northStarNudge?: string;
}

export const MicroCommitment = ({ children, theme, northStarNudge }: MicroCommitmentProps) => (
  <div className={`my-12 border-l-[3px] ${theme.microBorder} bg-white dark:bg-zinc-900 rounded-r-xl p-8`} style={{ borderLeftColor: 'var(--accent-hex)' }}>
    <div className="flex items-start gap-4">
      <div className={`w-9 h-9 rounded-lg ${theme.microIconBg} text-white flex items-center justify-center shrink-0`} style={{ backgroundColor: 'var(--accent-hex)' }}>
        <Zap size={16} />
      </div>
      <div>
        <p className={`text-[10px] font-semibold uppercase tracking-[0.15em] ${theme.microTitle} dark:text-zinc-300 mb-2`} style={{ color: 'var(--accent-hex)' }}>Quick Challenge</p>
        <div className="text-zinc-600 dark:text-zinc-400 text-sm leading-relaxed">
          {children}
        </div>
        {northStarNudge && (
          <p className="text-xs italic text-zinc-400 dark:text-zinc-500 mt-3">
            <Zap size={10} className="inline -mt-0.5 mr-1 text-[var(--accent-hex)]" />
            Remember: {northStarNudge}
          </p>
        )}
      </div>
    </div>
  </div>
);

interface PersonalStoryProps {
  children: React.ReactNode;
  name: string;
  role?: string;
}

export const PersonalStory = ({ children, name, role }: PersonalStoryProps) => (
  <div className="my-10 rounded-2xl bg-stone-50 dark:bg-stone-900/40 border border-stone-200/60 dark:border-stone-800/60 border-l-[3px] border-l-stone-400 dark:border-l-stone-600 p-8">
    <div className="flex items-center gap-3 mb-4">
      <div className="w-8 h-8 rounded-lg bg-stone-200 dark:bg-stone-800 flex items-center justify-center text-stone-500 dark:text-stone-400 shrink-0">
        <Quote size={14} />
      </div>
      <div className="flex items-center gap-2">
        <span className="text-sm font-bold text-stone-700 dark:text-stone-300">{name}</span>
        {role && (
          <span className="text-[10px] font-semibold uppercase tracking-wider text-stone-400 dark:text-stone-500">{role}</span>
        )}
      </div>
    </div>
    <div className="text-stone-600 dark:text-stone-400 text-sm leading-relaxed italic font-serif">
      {children}
    </div>
  </div>
);

/* ---- Dual Chart Comparison ---- */

interface ChartSeriesData {
  data: number[];
  color: string;
  legendLabel: string;
  /** If true this series gets the area fill and dots; if false it is drawn as the dashed secondary line. Default: first series is primary. */
}

interface ChartPhase {
  label: string;
  x1: number;
  x2: number;
  color: string;
}

interface ChartPanelConfig {
  /** Label rendered at the top of the SVG chart */
  label: string;
  /** Primary series (solid line, area fill, dots) */
  primary: ChartSeriesData;
  /** Secondary series (dashed line) */
  secondary: ChartSeriesData;
  /** Optional phase annotations rendered below x-axis */
  phases?: ChartPhase[];
  /** Which series provides the area fill: 'primary' (default) or 'secondary' */
  areaSource?: 'primary' | 'secondary';
  /** Border / background color scheme for the card wrapping the chart */
  borderColor: 'rose' | 'emerald';
}

interface DualChartComparisonProps {
  /** Heading above both charts */
  heading: string;
  /** Subheading / tagline */
  subheading: string;
  /** X-axis tick labels (e.g. day names, time labels) */
  xLabels: string[];
  /** Left chart panel configuration */
  leftPanel: ChartPanelConfig;
  /** Right chart panel configuration */
  rightPanel: ChartPanelConfig;
  /** Text shown on the reveal button */
  revealButtonText: string;
  /** Tailwind bg color class for the reveal button, e.g. "bg-orange-500" */
  revealButtonColor: string;
  /** Tailwind hover bg class for the reveal button, e.g. "hover:bg-orange-600" */
  revealButtonHover: string;
  /** Teaser paragraph shown before reveal */
  teaserText: string;
  /** Description shown below the left chart after reveal */
  leftDescription: React.ReactNode;
  /** Description shown below the right chart after reveal */
  rightDescription: React.ReactNode;
  /** Unique prefix for SVG gradient ids to avoid collisions when multiple instances are on-page */
  idPrefix: string;
}

const BORDER_COLORS = {
  rose: {
    border: 'border-rose-200 dark:border-rose-900',
    bg: 'bg-rose-50/50 dark:bg-rose-950/20',
    descBorder: 'border-rose-200 dark:border-rose-900',
    descBg: 'bg-rose-50 dark:bg-rose-950/30',
  },
  emerald: {
    border: 'border-emerald-200 dark:border-emerald-900',
    bg: 'bg-emerald-50/50 dark:bg-emerald-950/20',
    descBorder: 'border-emerald-200 dark:border-emerald-900',
    descBg: 'bg-emerald-50 dark:bg-emerald-950/30',
  },
} as const;

const SVG_W = 440, SVG_H = 260;
const PAD_L = 8, PAD_R = 8, PAD_T = 28, PAD_B = 44;
const CHART_W = SVG_W - PAD_L - PAD_R;
const CHART_H = SVG_H - PAD_T - PAD_B;
const chartToX = (f: number) => PAD_L + f * CHART_W;
const chartToY = (f: number) => PAD_T + (1 - f) * CHART_H;

function chartBuildArea(data: number[]): string {
  const pts = data.map((v, i) => ({ x: chartToX(i / (data.length - 1)), y: chartToY(v) }));
  let d = `M ${pts[0].x} ${chartToY(0)} L ${pts[0].x} ${pts[0].y}`;
  for (let i = 1; i < pts.length; i++) {
    const cx1 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.4;
    const cx2 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.6;
    d += ` C ${cx1} ${pts[i - 1].y}, ${cx2} ${pts[i].y}, ${pts[i].x} ${pts[i].y}`;
  }
  d += ` L ${pts[pts.length - 1].x} ${chartToY(0)} Z`;
  return d;
}

function chartBuildLine(data: number[]): string {
  const pts = data.map((v, i) => ({ x: chartToX(i / (data.length - 1)), y: chartToY(v) }));
  let d = `M ${pts[0].x} ${pts[0].y}`;
  for (let i = 1; i < pts.length; i++) {
    const cx1 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.4;
    const cx2 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.6;
    d += ` C ${cx1} ${pts[i - 1].y}, ${cx2} ${pts[i].y}, ${pts[i].x} ${pts[i].y}`;
  }
  return d;
}

const MotionDivAny = motion.div as any;

const DualChartSvg = ({ panel, xLabels, gradientId }: { panel: ChartPanelConfig; xLabels: string[]; gradientId: string }) => {
  const areaData = panel.areaSource === 'secondary' ? panel.secondary.data : panel.primary.data;
  const areaColor = panel.primary.color;

  // Compute legend widths dynamically
  const primaryLabelLen = panel.primary.legendLabel.length;
  const secondaryLabelLen = panel.secondary.legendLabel.length;
  const secondaryLegendW = secondaryLabelLen * 5 + 20; // approx char width + line
  const primaryLegendW = primaryLabelLen * 5 + 20;
  const totalLegendW = primaryLegendW + secondaryLegendW + 8;
  const legendStartX = SVG_W - PAD_R - totalLegendW;

  return (
    <svg viewBox={`0 0 ${SVG_W} ${SVG_H}`} className="w-full">
      <defs>
        <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={areaColor} stopOpacity="0.5" />
          <stop offset="100%" stopColor={areaColor} stopOpacity="0.05" />
        </linearGradient>
      </defs>
      {/* Grid lines */}
      {[0.25, 0.5, 0.75, 1.0].map(v => (
        <line key={v} x1={PAD_L} x2={SVG_W - PAD_R} y1={chartToY(v)} y2={chartToY(v)} stroke="#a1a1aa" strokeOpacity="0.15" strokeDasharray="3 3" />
      ))}
      {/* Baseline */}
      <line x1={PAD_L} x2={SVG_W - PAD_R} y1={chartToY(0)} y2={chartToY(0)} stroke="#a1a1aa" strokeOpacity="0.3" />
      {/* Area fill */}
      <motion.path
        d={chartBuildArea(areaData)}
        fill={`url(#${gradientId})`}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
      />
      {/* Primary line (solid) */}
      <motion.path
        d={chartBuildLine(panel.primary.data)}
        fill="none" stroke={areaColor} strokeWidth="2.5" strokeLinecap="round"
        initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
        transition={{ duration: 1.2, ease: 'easeOut' }}
      />
      {/* Secondary line (dashed) */}
      <motion.path
        d={chartBuildLine(panel.secondary.data)}
        fill="none" stroke={panel.secondary.color} strokeWidth="1.5" strokeDasharray="5 3" strokeLinecap="round"
        initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
        transition={{ duration: 1.2, ease: 'easeOut', delay: 0.3 }}
      />
      {/* Primary dots */}
      {panel.primary.data.map((v, i) => (
        <motion.circle key={i} cx={chartToX(i / (panel.primary.data.length - 1))} cy={chartToY(v)} r="3.5" fill={areaColor}
          initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2 * i + 0.3 }}
        />
      ))}
      {/* Y-axis labels */}
      <text x={PAD_L + 2} y={chartToY(1.0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">High</text>
      <text x={PAD_L + 2} y={chartToY(0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">Low</text>
      {/* X-axis labels */}
      {xLabels.map((m, i) => (
        <text key={m} x={chartToX(i / (xLabels.length - 1))} y={chartToY(0) + 14} fontSize="9" fill="#a1a1aa" textAnchor="middle" fontWeight="600">{m}</text>
      ))}
      {/* Phase labels */}
      {panel.phases?.map((p, i) => (
        <text key={i} x={chartToX((p.x1 + p.x2) / 2)} y={chartToY(0) + 28} fontSize="8" fill={p.color} textAnchor="middle" fontWeight="700">{p.label}</text>
      ))}
      {/* Chart label */}
      <text x={SVG_W / 2} y={14} fontSize="11" fill="#71717a" textAnchor="middle" fontWeight="700">{panel.label}</text>
      {/* Legend */}
      <line x1={legendStartX} x2={legendStartX + 16} y1={14} y2={14} stroke={areaColor} strokeWidth="2" />
      <text x={legendStartX + 20} y={17} fontSize="8" fill="#a1a1aa">{panel.primary.legendLabel}</text>
      <line x1={legendStartX + primaryLegendW + 4} x2={legendStartX + primaryLegendW + 20} y1={14} y2={14} stroke={panel.secondary.color} strokeWidth="1.5" strokeDasharray="4 2" />
      <text x={legendStartX + primaryLegendW + 24} y={17} fontSize="8" fill="#a1a1aa">{panel.secondary.legendLabel}</text>
    </svg>
  );
};

export const DualChartComparison = ({
  heading, subheading, xLabels,
  leftPanel, rightPanel,
  revealButtonText, revealButtonColor, revealButtonHover,
  teaserText,
  leftDescription, rightDescription,
  idPrefix,
}: DualChartComparisonProps) => {
  const [revealed, setRevealed] = useState(false);

  const leftColors = BORDER_COLORS[leftPanel.borderColor];
  const rightColors = BORDER_COLORS[rightPanel.borderColor];

  return (
    <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">{heading}</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">{subheading}</p>

      {!revealed ? (
        <div className="text-center">
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">{teaserText}</p>
          <button onClick={() => setRevealed(true)} className={`px-5 py-2.5 text-sm font-bold rounded-lg ${revealButtonColor} text-white ${revealButtonHover} transition-colors`}>
            {revealButtonText}
          </button>
        </div>
      ) : (
        <MotionDivAny initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
          <div className="grid md:grid-cols-2 gap-4 mb-5">
            <div className={`rounded-lg border ${leftColors.border} ${leftColors.bg} p-3`}>
              <DualChartSvg panel={leftPanel} xLabels={xLabels} gradientId={`${idPrefix}-left-grad`} />
            </div>
            <div className={`rounded-lg border ${rightColors.border} ${rightColors.bg} p-3`}>
              <DualChartSvg panel={rightPanel} xLabels={xLabels} gradientId={`${idPrefix}-right-grad`} />
            </div>
          </div>
          <div className="grid md:grid-cols-2 gap-4 text-sm">
            <div className={`flex items-start gap-2.5 p-3 rounded-lg ${leftColors.descBg} border ${leftColors.descBorder}`}>
              {leftDescription}
            </div>
            <div className={`flex items-start gap-2.5 p-3 rounded-lg ${rightColors.descBg} border ${rightColors.descBorder}`}>
              {rightDescription}
            </div>
          </div>
        </MotionDivAny>
      )}
    </div>
  );
};

interface ActivityRingProps {
  progress: number;
  color?: string;
  size?: number;
  strokeWidth?: number;
}

export const ActivityRing = ({ progress, color = "#f59e0b", size, strokeWidth }: ActivityRingProps) => {
  const sw = strokeWidth ?? 10;
  const r = size ? (size / 2) - (sw / 2) : 35;
  const vb = size ?? 96;
  const cx = vb / 2;
  const circumference = 2 * Math.PI * r;
  const offset = circumference - (progress / 100) * circumference;
  const px = size ? `${size}px` : '96px';

  return (
    <div className={`relative flex items-center justify-center ${size ? '' : 'w-24 h-24'} mx-auto mb-4`} style={size ? { width: px, height: px } : undefined}>
      <svg className="w-full h-full -rotate-90 overflow-visible" viewBox={`0 0 ${vb} ${vb}`}>
        <circle cx={cx} cy={cx} r={r} stroke={color} strokeWidth={sw} fill="transparent" className="opacity-10" />
        <motion.circle cx={cx} cy={cx} r={r} stroke={color} strokeWidth={sw} fill="transparent" strokeDasharray={circumference} initial={{ strokeDashoffset: circumference }} animate={{ strokeDashoffset: offset }} transition={{ duration: 1.5, ease: "easeOut" }} strokeLinecap="round" style={{ filter: `drop-shadow(0 0 8px ${color}55)` }} />
      </svg>
    </div>
  );
};
