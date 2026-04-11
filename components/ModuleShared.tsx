/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useRef, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { Zap, Quote, Sparkles } from 'lucide-react';
import { ModuleTheme } from '../types';

/* ═══════════════════════════════════════════════════════
   Highlight — inline discovery tooltip
   ═══════════════════════════════════════════════════════ */

interface HighlightProps {
  children?: React.ReactNode;
  description: string;
  theme: ModuleTheme;
}

export const Highlight = ({ children, description, _theme }: HighlightProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const tooltipRef = useRef<HTMLDivElement>(null);
  const [tooltipStyle, setTooltipStyle] = useState<React.CSSProperties>({});

  const repositionTooltip = useCallback(() => {
    if (!buttonRef.current || !tooltipRef.current) return;
    const buttonRect = buttonRef.current.getBoundingClientRect();
    const tooltipRect = tooltipRef.current.getBoundingClientRect();
    const viewportWidth = window.innerWidth;
    const pad = 12;
    let leftOffset = (buttonRect.width / 2) - (tooltipRect.width / 2);
    const tooltipRight = buttonRect.left + leftOffset + tooltipRect.width;
    if (tooltipRight > viewportWidth - pad) leftOffset -= (tooltipRight - viewportWidth + pad);
    const tooltipLeft = buttonRect.left + leftOffset;
    if (tooltipLeft < pad) leftOffset += (pad - tooltipLeft);
    setTooltipStyle({ left: leftOffset });
  }, []);

  useEffect(() => {
    if (isOpen) requestAnimationFrame(repositionTooltip);
  }, [isOpen, repositionTooltip]);

  return (
    <span className="relative inline-block mx-0.5">
      <button
        ref={buttonRef}
        onClick={(e) => { e.stopPropagation(); setIsOpen(!isOpen); }}
        className="relative inline-flex items-center font-semibold cursor-help transition-all duration-200"
        style={{
          color: 'var(--accent-hex)',
          backgroundImage: 'linear-gradient(to right, rgba(var(--accent),0.2), rgba(var(--accent),0.2))',
          backgroundPosition: '0 100%',
          backgroundSize: '100% 3px',
          backgroundRepeat: 'no-repeat',
          paddingBottom: 2,
        }}
      >
        <span className="not-italic">{children}</span>
      </button>
      <AnimatePresence>
        {isOpen && (
          <>
            <div className="fixed inset-0 z-[60]" onClick={() => setIsOpen(false)} />
            <motion.div
              ref={tooltipRef}
              initial={{ opacity: 0, scale: 0.92, y: 8 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.92, y: 8 }}
              transition={{ duration: 0.2, ease: [0.25, 1, 0.5, 1] }}
              className="absolute z-[70] bottom-full mb-3 w-72 max-w-[calc(100vw-1.5rem)] p-5 bg-zinc-900 dark:bg-zinc-800 text-white rounded-2xl pointer-events-auto leading-relaxed whitespace-normal text-left"
              style={{ ...tooltipStyle, transformOrigin: 'bottom center', boxShadow: '0 4px 20px rgba(0,0,0,0.25)' }}
            >
              <div className="absolute -bottom-1.5 left-1/2 -translate-x-1/2 w-3 h-3 rotate-45 bg-zinc-900 dark:bg-zinc-800" />
              <div className="relative">
                <p className="font-sans font-bold uppercase tracking-wider text-[9px] mb-2 text-zinc-400">
                  <Sparkles size={10} className="inline -mt-0.5 mr-1" />
                  Key Insight
                </p>
                <p className="text-[13px] font-medium leading-relaxed text-zinc-100">{description}</p>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </span>
  );
};

/* ═══════════════════════════════════════════════════════
   ReadingSection — Headspace-inspired lesson page
   ═══════════════════════════════════════════════════════ */

interface ReadingSectionProps {
  title: string;
  eyebrow: string;
  icon: any;
  children?: React.ReactNode;
  theme: ModuleTheme;
}

export const ReadingSection = ({ title, eyebrow, icon: Icon, children, _theme }: ReadingSectionProps) => (
  <article className="relative">
    <header className="mb-14 relative">
      <MotionDiv
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.05, ease: [0.25, 1, 0.5, 1] }}
      >
        <span
          className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-[10px] font-bold tracking-wider uppercase mb-5"
          style={{ backgroundColor: 'rgba(var(--accent),0.08)', color: 'var(--accent-hex)' }}
        >
          <Icon size={12} />
          {eyebrow}
        </span>
      </MotionDiv>

      <MotionDiv
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.12, ease: [0.25, 1, 0.5, 1] }}
      >
        <h2
          className="font-serif font-bold leading-tight tracking-tight text-zinc-900 dark:text-white"
          style={{ fontSize: 'clamp(30px, 7vw, 48px)', letterSpacing: '-0.025em' }}
        >
          {title}
        </h2>
      </MotionDiv>

      <MotionDiv
        initial={{ scaleX: 0 }}
        animate={{ scaleX: 1 }}
        transition={{ duration: 0.8, delay: 0.3, ease: [0.25, 1, 0.5, 1] }}
        className="mt-6 h-0.5 rounded-full origin-left"
        style={{ backgroundColor: 'rgba(var(--accent),0.15)', maxWidth: 80 }}
      />
    </header>

    <MotionDiv
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5, delay: 0.25 }}
    >
      <div className="prose prose-stone dark:prose-invert prose-lg max-w-none text-zinc-600 dark:text-zinc-300 leading-[1.85] font-serif overflow-visible space-y-7">
        {children}
      </div>
    </MotionDiv>
  </article>
);

/* ═══════════════════════════════════════════════════════
   MicroCommitment — Chunky action card with hard shadow
   ═══════════════════════════════════════════════════════ */

interface MicroCommitmentProps {
  children?: React.ReactNode;
  theme: ModuleTheme;
  northStarNudge?: string;
}

export const MicroCommitment = ({ children, _theme, northStarNudge }: MicroCommitmentProps) => (
  <MotionDiv
    initial={{ opacity: 0, y: 12 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true, margin: '-40px' }}
    transition={{ duration: 0.5, ease: [0.25, 1, 0.5, 1] }}
    className="my-14"
  >
    <motion.div
      className="rounded-2xl relative px-7 py-6 md:px-8 md:py-7"
      style={{
        backgroundColor: '#FFFFFF',
        border: '2.5px solid #2A7D6F',
        boxShadow: '4px 4px 0px 0px #1F5F54',
        borderRadius: 18,
      }}
      whileHover={{ x: -2, y: -2, boxShadow: '6px 6px 0px 0px #1F5F54' }}
      whileTap={{ x: 2, y: 2, boxShadow: '1px 1px 0px 0px #1F5F54' }}
      transition={{ type: 'spring', stiffness: 400, damping: 25 }}
    >
      <div className="flex items-start gap-4">
        <div className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0 mt-0.5" style={{ backgroundColor: '#2A7D6F' }}>
          <Zap size={18} style={{ color: '#fff' }} />
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-[10px] font-bold uppercase tracking-[0.15em] mb-2" style={{ color: '#2A7D6F' }}>
            Quick Challenge
          </p>
          <div className="text-[15px] leading-relaxed font-sans text-zinc-700 dark:text-zinc-300">
            {children}
          </div>
          {northStarNudge && (
            <p className="text-xs mt-4 pt-3 text-zinc-400 dark:text-zinc-500" style={{ borderTop: '1px solid #E8E4DE' }}>
              <Zap size={10} className="inline -mt-0.5 mr-1 text-[#2A7D6F]" />
              Remember: {northStarNudge}
            </p>
          )}
        </div>
      </div>
    </motion.div>
  </MotionDiv>
);

/* ═══════════════════════════════════════════════════════
   PersonalStory — intimate, warm founder quote
   ═══════════════════════════════════════════════════════ */

interface PersonalStoryProps {
  children: React.ReactNode;
  name: string;
  role?: string;
}

export const PersonalStory = ({ children, name, role }: PersonalStoryProps) => (
  <MotionDiv
    initial={{ opacity: 0, y: 8 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true, margin: '-40px' }}
    transition={{ duration: 0.5, ease: [0.25, 1, 0.5, 1] }}
    className="my-14"
  >
    <div className="relative rounded-2xl bg-[#FAF7F4] dark:bg-zinc-800/60 px-8 py-7 md:px-10 md:py-9">
      <div className="absolute top-4 right-6 pointer-events-none" style={{ fontSize: 72, lineHeight: 1, fontFamily: 'Georgia, serif', color: 'rgba(0,0,0,0.04)' }}>
        &rdquo;
      </div>
      <div className="relative">
        <div className="flex items-center gap-3 mb-5">
          <div className="w-9 h-9 rounded-full flex items-center justify-center shrink-0" style={{ backgroundColor: 'rgba(var(--accent),0.1)' }}>
            <Quote size={14} style={{ color: 'var(--accent-hex)' }} />
          </div>
          <div>
            <span className="text-sm font-bold text-zinc-800 dark:text-zinc-200">{name}</span>
            {role && (
              <span className="text-[10px] font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 ml-2">{role}</span>
            )}
          </div>
        </div>
        <div className="text-[15px] leading-[1.8] text-zinc-600 dark:text-zinc-400 italic font-serif">
          {children}
        </div>
      </div>
    </div>
  </MotionDiv>
);

/* ═══════════════════════════════════════════════════════
   DualChartComparison
   ═══════════════════════════════════════════════════════ */

interface ChartSeriesData { data: number[]; color: string; legendLabel: string; }
interface ChartPhase { label: string; x1: number; x2: number; color: string; }
interface ChartPanelConfig { label: string; primary: ChartSeriesData; secondary: ChartSeriesData; phases?: ChartPhase[]; areaSource?: 'primary' | 'secondary'; borderColor: 'rose' | 'emerald'; }
interface DualChartComparisonProps { heading: string; subheading: string; xLabels: string[]; leftPanel: ChartPanelConfig; rightPanel: ChartPanelConfig; revealButtonText: string; revealButtonColor: string; revealButtonHover: string; teaserText: string; leftDescription: React.ReactNode; rightDescription: React.ReactNode; idPrefix: string; }

const BORDER_COLORS = { rose: { border: 'border-rose-200 dark:border-rose-900', bg: 'bg-rose-50/50 dark:bg-rose-950/20', descBorder: 'border-rose-200 dark:border-rose-900', descBg: 'bg-rose-50 dark:bg-rose-950/30' }, emerald: { border: 'border-emerald-200 dark:border-emerald-900', bg: 'bg-emerald-50/50 dark:bg-emerald-950/20', descBorder: 'border-emerald-200 dark:border-emerald-900', descBg: 'bg-emerald-50 dark:bg-emerald-950/30' } } as const;

const SVG_W = 440, SVG_H = 260, PAD_L = 8, PAD_R = 8, PAD_T = 28, PAD_B = 44;
const CHART_W = SVG_W - PAD_L - PAD_R, CHART_H = SVG_H - PAD_T - PAD_B;
const chartToX = (f: number) => PAD_L + f * CHART_W;
const chartToY = (f: number) => PAD_T + (1 - f) * CHART_H;

function chartBuildArea(data: number[]): string { const pts = data.map((v, i) => ({ x: chartToX(i / (data.length - 1)), y: chartToY(v) })); let d = `M ${pts[0].x} ${chartToY(0)} L ${pts[0].x} ${pts[0].y}`; for (let i = 1; i < pts.length; i++) { const cx1 = pts[i-1].x + (pts[i].x - pts[i-1].x) * 0.4; const cx2 = pts[i-1].x + (pts[i].x - pts[i-1].x) * 0.6; d += ` C ${cx1} ${pts[i-1].y}, ${cx2} ${pts[i].y}, ${pts[i].x} ${pts[i].y}`; } d += ` L ${pts[pts.length-1].x} ${chartToY(0)} Z`; return d; }
function chartBuildLine(data: number[]): string { const pts = data.map((v, i) => ({ x: chartToX(i / (data.length - 1)), y: chartToY(v) })); let d = `M ${pts[0].x} ${pts[0].y}`; for (let i = 1; i < pts.length; i++) { const cx1 = pts[i-1].x + (pts[i].x - pts[i-1].x) * 0.4; const cx2 = pts[i-1].x + (pts[i].x - pts[i-1].x) * 0.6; d += ` C ${cx1} ${pts[i-1].y}, ${cx2} ${pts[i].y}, ${pts[i].x} ${pts[i].y}`; } return d; }

const DualChartSvg = ({ panel, xLabels, gradientId }: { panel: ChartPanelConfig; xLabels: string[]; gradientId: string }) => { const areaData = panel.areaSource === 'secondary' ? panel.secondary.data : panel.primary.data; const areaColor = panel.primary.color; const pLW = panel.primary.legendLabel.length * 5 + 20; const sLW = panel.secondary.legendLabel.length * 5 + 20; const legendStartX = SVG_W - PAD_R - pLW - sLW - 8; return (<svg viewBox={`0 0 ${SVG_W} ${SVG_H}`} className="w-full"><defs><linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={areaColor} stopOpacity="0.5" /><stop offset="100%" stopColor={areaColor} stopOpacity="0.05" /></linearGradient></defs>{[0.25,0.5,0.75,1.0].map(v => <line key={v} x1={PAD_L} x2={SVG_W-PAD_R} y1={chartToY(v)} y2={chartToY(v)} stroke="#a1a1aa" strokeOpacity="0.15" strokeDasharray="3 3" />)}<line x1={PAD_L} x2={SVG_W-PAD_R} y1={chartToY(0)} y2={chartToY(0)} stroke="#a1a1aa" strokeOpacity="0.3" /><motion.path d={chartBuildArea(areaData)} fill={`url(#${gradientId})`} initial={{opacity:0}} animate={{opacity:1}} transition={{duration:0.8}} /><motion.path d={chartBuildLine(panel.primary.data)} fill="none" stroke={areaColor} strokeWidth="2.5" strokeLinecap="round" initial={{pathLength:0}} animate={{pathLength:1}} transition={{duration:1.2,ease:'easeOut'}} /><motion.path d={chartBuildLine(panel.secondary.data)} fill="none" stroke={panel.secondary.color} strokeWidth="1.5" strokeDasharray="5 3" strokeLinecap="round" initial={{pathLength:0}} animate={{pathLength:1}} transition={{duration:1.2,ease:'easeOut',delay:0.3}} />{panel.primary.data.map((v,i) => <motion.circle key={i} cx={chartToX(i/(panel.primary.data.length-1))} cy={chartToY(v)} r="3.5" fill={areaColor} initial={{scale:0}} animate={{scale:1}} transition={{delay:0.2*i+0.3}} />)}<text x={PAD_L+2} y={chartToY(1.0)-4} fontSize="9" fill="#a1a1aa" fontWeight="600">High</text><text x={PAD_L+2} y={chartToY(0)-4} fontSize="9" fill="#a1a1aa" fontWeight="600">Low</text>{xLabels.map((m,i) => <text key={m} x={chartToX(i/(xLabels.length-1))} y={chartToY(0)+14} fontSize="9" fill="#a1a1aa" textAnchor="middle" fontWeight="600">{m}</text>)}{panel.phases?.map((p,i) => <text key={i} x={chartToX((p.x1+p.x2)/2)} y={chartToY(0)+28} fontSize="8" fill={p.color} textAnchor="middle" fontWeight="700">{p.label}</text>)}<text x={SVG_W/2} y={14} fontSize="11" fill="#71717a" textAnchor="middle" fontWeight="700">{panel.label}</text><line x1={legendStartX} x2={legendStartX+16} y1={14} y2={14} stroke={areaColor} strokeWidth="2" /><text x={legendStartX+20} y={17} fontSize="8" fill="#a1a1aa">{panel.primary.legendLabel}</text><line x1={legendStartX+pLW+4} x2={legendStartX+pLW+20} y1={14} y2={14} stroke={panel.secondary.color} strokeWidth="1.5" strokeDasharray="4 2" /><text x={legendStartX+pLW+24} y={17} fontSize="8" fill="#a1a1aa">{panel.secondary.legendLabel}</text></svg>); };

export const DualChartComparison = ({ heading, subheading, xLabels, leftPanel, rightPanel, revealButtonText, revealButtonColor, revealButtonHover, teaserText, leftDescription, rightDescription, idPrefix }: DualChartComparisonProps) => { const [revealed, setRevealed] = useState(false); const lc = BORDER_COLORS[leftPanel.borderColor]; const rc = BORDER_COLORS[rightPanel.borderColor]; return (<div className="my-14 p-6 md:p-10 bg-white dark:bg-zinc-800/50 rounded-2xl border border-zinc-200 dark:border-zinc-700" style={{boxShadow:'0 1px 3px rgba(28,25,23,0.06), 0 4px 16px rgba(28,25,23,0.04)'}}><h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">{heading}</h4><p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">{subheading}</p>{!revealed ? (<div className="text-center"><p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">{teaserText}</p><button onClick={() => setRevealed(true)} className={`px-5 py-2.5 text-sm font-bold rounded-xl ${revealButtonColor} text-white ${revealButtonHover} transition-colors`}>{revealButtonText}</button></div>) : (<MotionDiv initial={{opacity:0,y:12}} animate={{opacity:1,y:0}} transition={{duration:0.4}}><div className="grid md:grid-cols-2 gap-4 mb-5"><div className={`rounded-xl border ${lc.border} ${lc.bg} p-3`}><DualChartSvg panel={leftPanel} xLabels={xLabels} gradientId={`${idPrefix}-left-grad`} /></div><div className={`rounded-xl border ${rc.border} ${rc.bg} p-3`}><DualChartSvg panel={rightPanel} xLabels={xLabels} gradientId={`${idPrefix}-right-grad`} /></div></div><div className="grid md:grid-cols-2 gap-4 text-sm"><div className={`flex items-start gap-2.5 p-3 rounded-xl ${lc.descBg} border ${lc.descBorder}`}>{leftDescription}</div><div className={`flex items-start gap-2.5 p-3 rounded-xl ${rc.descBg} border ${rc.descBorder}`}>{rightDescription}</div></div></MotionDiv>)}</div>); };

/* ═══════════════════════════════════════════════════════
   ActivityRing
   ═══════════════════════════════════════════════════════ */

interface ActivityRingProps { progress: number; color?: string; size?: number; strokeWidth?: number; }

export const ActivityRing = ({ progress, color = "#f59e0b", size, strokeWidth }: ActivityRingProps) => { const sw = strokeWidth ?? 10; const r = size ? (size/2)-(sw/2) : 35; const vb = size ?? 96; const cx = vb/2; const circumference = 2*Math.PI*r; const offset = circumference-(progress/100)*circumference; const px = size ? `${size}px` : '96px'; return (<div className={`relative flex items-center justify-center ${size ? '' : 'w-24 h-24'} mx-auto mb-4`} style={size ? {width:px,height:px} : undefined}><svg className="w-full h-full -rotate-90 overflow-visible" viewBox={`0 0 ${vb} ${vb}`}><circle cx={cx} cy={cx} r={r} stroke={color} strokeWidth={sw} fill="transparent" className="opacity-10" /><motion.circle cx={cx} cy={cx} r={r} stroke={color} strokeWidth={sw} fill="transparent" strokeDasharray={circumference} initial={{strokeDashoffset:circumference}} animate={{strokeDashoffset:offset}} transition={{duration:1.5,ease:"easeOut"}} strokeLinecap="round" style={{filter:`drop-shadow(0 0 8px ${color}55)`}} /></svg></div>); };

/* ═══════════════════════════════════════════════════════
   ConceptCardGrid — named concepts as visual cards
   ═══════════════════════════════════════════════════════ */

interface ConceptCard {
  number: number;
  term: string;
  description: string;
  highlight?: boolean;
}

interface ConceptCardGridProps {
  cards: ConceptCard[];
  columns?: 2 | 4;
  accentNote?: string;
}

export const ConceptCardGrid = ({ cards, columns = 2, accentNote }: ConceptCardGridProps) => (
  <div className="my-8 not-prose">
    <div className={`grid gap-3 ${columns === 4 ? 'grid-cols-2 md:grid-cols-4' : 'grid-cols-1 md:grid-cols-2'}`}>
      {cards.map((card) => (
        <div
          key={card.number}
          className="relative"
          style={{
            backgroundColor: card.highlight ? '#e8f5f2' : '#FFFFFF',
            border: card.highlight ? '2px solid #2A7D6F' : '2px solid #1a1a1a',
            borderRadius: 14,
            padding: '18px 20px',
          }}
        >
          {card.highlight && (
            <span className="absolute top-3 right-3 text-[10px] font-bold uppercase tracking-wider" style={{ backgroundColor: '#c8e8e0', color: '#1a6358', borderRadius: 20, padding: '3px 8px' }}>
              Key Lever
            </span>
          )}
          <div className="w-9 h-9 rounded-full flex items-center justify-center mb-3" style={{ backgroundColor: '#2A7D6F' }}>
            <span className="font-serif font-bold text-base text-white">{card.number}</span>
          </div>
          <p className="font-serif font-bold text-base mb-1" style={{ color: '#1a1a1a' }}>{card.term}</p>
          <p className="text-[13px] leading-relaxed" style={{ color: '#5a5550' }}>{card.description}</p>
        </div>
      ))}
    </div>
    {accentNote && (
      <div className="mt-3" style={{ borderLeft: '3px solid #2A7D6F', backgroundColor: '#f0faf7', padding: '12px 16px', borderRadius: '0 10px 10px 0' }}>
        <p className="text-[13px] italic" style={{ color: '#1a6358' }}>{accentNote}</p>
      </div>
    )}
  </div>
);

/* ═══════════════════════════════════════════════════════
   GlossaryGrid — quoted term definitions
   ═══════════════════════════════════════════════════════ */

interface GlossaryItem {
  term: string;
  definition: string;
  explanation: string;
  highlight?: boolean;
}

interface GlossaryGridProps {
  items: GlossaryItem[];
}

export const GlossaryGrid: React.FC<GlossaryGridProps> = ({ items }) => (
  <div className="my-8 not-prose" style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
    {items.map((item, i) => (
      <div key={i} style={{
        background: item.highlight ? '#e8f5f2' : 'white',
        border: item.highlight ? '2px solid #2A7D6F' : '2px solid #1a1a1a',
        borderRadius: 14,
        padding: '16px 20px',
        display: 'flex',
        alignItems: 'flex-start',
        gap: 16,
      }}>
        <div style={{
          background: item.highlight ? '#2A7D6F' : '#f0ece6',
          border: item.highlight ? 'none' : '1.5px solid #d0cdc8',
          borderRadius: 10,
          padding: '6px 12px',
          flexShrink: 0,
          fontFamily: "'Source Serif 4', serif",
          fontSize: 15,
          fontWeight: 700,
          color: item.highlight ? 'white' : '#1a1a1a',
          whiteSpace: 'nowrap' as const,
        }}>
          &ldquo;{item.term}&rdquo;
        </div>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 13, fontWeight: 700, color: item.highlight ? '#1a6358' : '#2A7D6F', marginBottom: 4 }}>
            = {item.definition}
          </div>
          <div style={{ fontSize: 14, color: '#5a5550', lineHeight: 1.5 }}>
            {item.explanation}
          </div>
        </div>
      </div>
    ))}
  </div>
);
