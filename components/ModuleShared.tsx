/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { MotionDiv } from './Motion';
import { Quote, ArrowRight, Heart } from 'lucide-react';
import { type ModuleTheme } from '../types';
import { useNavigation } from '../contexts/NavigationContext';
import { useAuth } from '../contexts/AuthContext';
import { COLORS } from '../design/tokens';
import { Artwork, Eyebrow } from './learning/shared';
import { BrandBook } from './learning/BrandBook';
import { Popover, PopoverTrigger, PopoverContent } from './approved-ui-runtime';

/* ═══════════════════════════════════════════════════════
   Highlight — inline discovery tooltip
   ═══════════════════════════════════════════════════════ */

interface HighlightProps {
  children?: React.ReactNode;
  description: string;
  theme: ModuleTheme;
}

export const Highlight = ({ children, description }: HighlightProps) => (
  <Popover><PopoverTrigger className="mr-term">{children}</PopoverTrigger><PopoverContent className="mr-definition"><p>{description}</p></PopoverContent></Popover>
);

/* ═══════════════════════════════════════════════════════
   ReadingSection — approved learning notebook
   ═══════════════════════════════════════════════════════ */

interface ReadingSectionProps {
  title: string;
  eyebrow: string;
  icon: any;
  children?: React.ReactNode;
  theme: ModuleTheme;
}

export const ReadingSection = ({ title, eyebrow, children }: ReadingSectionProps) => (
  <section className="mr-lesson">
    <header className="mr-lesson-heading"><div><Eyebrow>{eyebrow}</Eyebrow><h1 tabIndex={-1}>{title}</h1></div><Artwork src="/assets/star-crew/companions/thinker.png" size={124} /></header>
    <div className="mr-prose" style={{ fontSize: 'calc(17px * var(--reading-scale, 1))', lineHeight: 'var(--reading-lh, 1.85)' }}>{children}</div>
  </section>
);

/* ═══════════════════════════════════════════════════════
   MicroCommitment — a small beginning in the learning notebook
   ═══════════════════════════════════════════════════════ */

interface MicroCommitmentProps {
  children?: React.ReactNode;
  theme: ModuleTheme;
  northStarNudge?: string;
}

export const MicroCommitment = ({ children, northStarNudge }: MicroCommitmentProps) => (
  <section className="mr-small-beginning"><header><BrandBook size={30} /><h3>A small beginning.</h3></header><div>{children}</div>{northStarNudge && <p className="mr-note-status">Remember: {northStarNudge}</p>}</section>
);

/* ═══════════════════════════════════════════════════════
   ToolJumpCard — link from a module to the relevant tool
   ═══════════════════════════════════════════════════════ */

interface ToolJumpCardProps {
  /** Tool ID — must match an Innovation Zone tool key
   *  ('planner', 'war-room', 'cao-simulator', 'future-finder',
   *   'war-room', 'comeback', 'journey', 'points-passport'). */
  toolId: string;
  /** Headline shown to the student, e.g. "Try this in the Spaced Repetition Timetable" */
  title: string;
  /** Short supporting line under the title. */
  description: string;
  /** Optional CTA label. Defaults to "Open tool". */
  ctaLabel?: string;
}

export const ToolJumpCard: React.FC<ToolJumpCardProps> = ({ toolId, title, description, ctaLabel }) => {
  const nav = useNavigation();
  return (
    <MotionDiv
      initial={{ opacity: 0, y: 12 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-40px' }}
      transition={{ duration: 0.5, ease: [0.25, 1, 0.5, 1] }}
      className="my-14"
    >
      <button
        type="button"
        onClick={() => nav.navigateToInnovationZone(toolId)}
        className="module-tool-jump w-full bg-[var(--surface-paper)] text-left text-[var(--ink-primary)]"
        style={{
          border: '2px solid var(--outline-strong)',
          borderRadius: 16,
          padding: '20px 22px',
          boxShadow: '4px 4px 0px 0px var(--outline-strong)',
          transition: 'transform 120ms ease, box-shadow 120ms ease',
        }}
        onMouseEnter={(e) => {
          (e.currentTarget as HTMLButtonElement).style.transform = 'translate(-2px, -2px)';
          (e.currentTarget as HTMLButtonElement).style.boxShadow = '6px 6px 0px 0px var(--outline-strong)';
        }}
        onMouseLeave={(e) => {
          (e.currentTarget as HTMLButtonElement).style.transform = 'translate(0, 0)';
          (e.currentTarget as HTMLButtonElement).style.boxShadow = '4px 4px 0px 0px var(--outline-strong)';
        }}
      >
        <div className="flex items-center gap-4">
          <div className="flex-1 min-w-0">
            <p className="text-[10px] font-bold uppercase tracking-[0.15em] mb-1.5" style={{ color: COLORS.accent }}>
              Apply this · Tool
            </p>
            <h4 className="font-serif text-lg sm:text-xl font-semibold text-zinc-900 dark:text-white mb-1">
              {title}
            </h4>
            <p className="text-[13px] sm:text-sm text-zinc-600 dark:text-zinc-400 leading-snug">
              {description}
            </p>
          </div>
          <div
            className="shrink-0 w-11 h-11 rounded-full flex items-center justify-center"
            style={{ backgroundColor: COLORS.accent }}
          >
            <ArrowRight size={18} style={{ color: '#fff' }} />
          </div>
        </div>
        {ctaLabel && (
          <div className="mt-3 inline-flex items-center gap-1 text-xs font-bold tracking-wide" style={{ color: COLORS.accent }}>
            {ctaLabel}
            <ArrowRight size={12} />
          </div>
        )}
      </button>
    </MotionDiv>
  );
};

/* ═══════════════════════════════════════════════════════
   PersonalStory — intimate, warm founder quote
   ═══════════════════════════════════════════════════════ */

interface PersonalStoryProps {
  children: React.ReactNode;
  name: string;
  role?: string;
  /** Junior Cycle variant. When the reader is a JC student (1st–3rd year) and
   *  this is supplied, it replaces name/role/children so 12–15 year-olds aren't
   *  shown senior-only framing (mocks, CAO points, 5th/6th year, college).
   *  Content complexity audit 2026-07 — see compliance/JC_READABILITY_AUDIT.md. */
  junior?: { name?: string; role?: string; children: React.ReactNode };
}

export const PersonalStory = ({ children, name, role, junior }: PersonalStoryProps) => {
  const { user } = useAuth();
  const useJunior = user?.curriculumLevel === 'junior' && !!junior;
  const shownName = useJunior ? (junior!.name ?? name) : name;
  const shownRole = useJunior ? junior!.role : role;
  const shownChildren = useJunior ? junior!.children : children;
  const isFounderStory = /founder/i.test(shownRole ?? '');
  return (
  <MotionDiv
    initial={{ opacity: 0, y: 8 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true, margin: '-40px' }}
    transition={{ duration: 0.5, ease: [0.25, 1, 0.5, 1] }}
    className="my-14"
  >
    <div className="relative rounded-2xl bg-white dark:bg-zinc-800/60 border border-zinc-200 dark:border-zinc-700 px-8 py-7 md:px-10 md:py-9">
      <div aria-hidden="true" className="absolute top-4 right-6 pointer-events-none" style={{ fontSize: 72, lineHeight: 1, fontFamily: 'Georgia, serif', color: 'rgba(0,0,0,0.04)' }}>
        &rdquo;
      </div>
      <div className="relative">
        <div className="flex items-center gap-3 mb-5">
          <div className="w-9 h-9 rounded-full flex items-center justify-center shrink-0" style={{ backgroundColor: 'rgba(var(--accent),0.1)' }}>
            <Quote size={14} style={{ color: 'var(--accent-hex)' }} />
          </div>
          <div className="min-w-0">
            <span className="text-sm font-bold text-zinc-800 dark:text-zinc-200">{shownName}</span>
            {shownRole && (
              <span className="text-[10px] font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 ml-2">{shownRole}</span>
            )}
          </div>
          {/* Honesty label: student voices are illustrative composites drawn from
              common student experiences, not quotes from identifiable named
              students. Rendered app-wide so no PersonalStory implies a real,
              traceable individual. See docs/module-content-audit-2026-07-21.md. */}
          <span
            className="ml-auto shrink-0 text-[9px] font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 border border-zinc-200 dark:border-zinc-700 rounded-full px-2 py-0.5"
            title={isFounderStory ? 'A first-person note from the NextStepUni founder.' : 'An illustrative example based on common student experiences — not a quote from a specific named student.'}
          >
            {isFounderStory ? 'Founder’s note' : 'Illustrative'}
          </span>
        </div>
        <div className="text-[15px] leading-[1.8] text-zinc-600 dark:text-zinc-400 italic font-serif">
          {shownChildren}
        </div>
      </div>
    </div>
  </MotionDiv>
  );
};

/* ═══════════════════════════════════════════════════════
   SupportSignpost — wellbeing safety net
   Rendered in modules that touch exam stress, anxiety or crisis
   (Catastrophic Thinking, Exam Crisis Management, Emotional
   Intelligence…). These modules coach students through distressing
   feelings, so they must always point to real human support for
   anything bigger than exam nerves. Shown in BOTH essentials and
   full render paths. See docs/module-content-audit-2026-07-21.md.
   ═══════════════════════════════════════════════════════ */

export const SupportSignpost = ({ children }: { children?: React.ReactNode }) => (
  <div
    className="my-8 rounded-2xl px-5 py-4 flex gap-3.5 items-start"
    style={{ backgroundColor: 'var(--success-tint)', border: '1px solid var(--outline-soft)' }}
  >
    <div className="w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-0.5" style={{ backgroundColor: 'rgba(58,141,95,0.15)' }}>
      <Heart size={15} style={{ color: '#3A8D5F' }} />
    </div>
    <div className="text-[13.5px] leading-relaxed" style={{ color: 'var(--success-tint-ink)' }}>
      {children ?? (
        <>
          <span className="font-semibold">These tools are for exam nerves.</span>{' '}
          If your worries feel bigger than exams, or they don&rsquo;t ease off, please talk to
          someone you trust — a parent, a teacher, or your school&rsquo;s guidance counsellor.
          You can also reach <span className="font-semibold">Jigsaw</span> (jigsaw.ie) or free-text{' '}
          <span className="font-semibold">50808</span> any time, or call{' '}
          <span className="font-semibold">Childline on 1800 66 66 66</span>. Reaching out is a strong move,
          not a weak one.
        </>
      )}
    </div>
  </div>
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

const DualChartSvg = ({ panel, xLabels, gradientId }: { panel: ChartPanelConfig; xLabels: string[]; gradientId: string }) => { const areaData = panel.areaSource === 'secondary' ? panel.secondary.data : panel.primary.data; const areaColor = panel.primary.color; const pLW = panel.primary.legendLabel.length * 5 + 20; const sLW = panel.secondary.legendLabel.length * 5 + 20; const legendStartX = SVG_W - PAD_R - pLW - sLW - 8; return (<svg viewBox={`0 0 ${SVG_W} ${SVG_H}`} className="w-full"><defs><linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={areaColor} stopOpacity="0.5" /><stop offset="100%" stopColor={areaColor} stopOpacity="0.05" /></linearGradient></defs>{[0.25,0.5,0.75,1.0].map(v => <line key={v} x1={PAD_L} x2={SVG_W-PAD_R} y1={chartToY(v)} y2={chartToY(v)} stroke="#a1a1aa" strokeOpacity="0.15" strokeDasharray="3 3" />)}<line x1={PAD_L} x2={SVG_W-PAD_R} y1={chartToY(0)} y2={chartToY(0)} stroke="#a1a1aa" strokeOpacity="0.3" /><motion.path d={chartBuildArea(areaData)} fill={`url(#${gradientId})`} initial={{opacity:0}} animate={{opacity:1}} transition={{duration:0.8}} /><motion.path d={chartBuildLine(panel.primary.data)} fill="none" stroke={areaColor} strokeWidth="2.5" strokeLinecap="round" initial={{pathLength:0}} animate={{pathLength:1}} transition={{duration:1.2,ease:'easeOut'}} /><motion.path d={chartBuildLine(panel.secondary.data)} fill="none" stroke={panel.secondary.color} strokeWidth="1.5" strokeDasharray="5 3" strokeLinecap="round" initial={{pathLength:0}} animate={{pathLength:1}} transition={{duration:1.2,ease:'easeOut',delay:0.3}} />{panel.primary.data.map((v,i) => <motion.circle key={i} cx={chartToX(i/(panel.primary.data.length-1))} cy={chartToY(v)} r="3.5" fill={areaColor} initial={{scale:0}} animate={{scale:1}} transition={{delay:0.2*i+0.3}} />)}<text x={PAD_L+2} y={chartToY(1.0)-4} fontSize="9" fill="#a1a1aa" fontWeight="600">High</text><text x={PAD_L+2} y={chartToY(0)-4} fontSize="9" fill="#a1a1aa" fontWeight="600">Low</text>{xLabels.map((m,i) => <text key={m} x={chartToX(i/(xLabels.length-1))} y={chartToY(0)+14} fontSize="9" fill="#a1a1aa" textAnchor="middle" fontWeight="600">{m}</text>)}{panel.phases?.map((p,i) => <text key={i} x={chartToX((p.x1+p.x2)/2)} y={chartToY(0)+28} fontSize="8" fill={p.color} textAnchor="middle" fontWeight="700">{p.label}</text>)}<text x={SVG_W/2} y={14} fontSize="11" fill="var(--ink-muted)" textAnchor="middle" fontWeight="700">{panel.label}</text><line x1={legendStartX} x2={legendStartX+16} y1={14} y2={14} stroke={areaColor} strokeWidth="2" /><text x={legendStartX+20} y={17} fontSize="8" fill="#a1a1aa">{panel.primary.legendLabel}</text><line x1={legendStartX+pLW+4} x2={legendStartX+pLW+20} y1={14} y2={14} stroke={panel.secondary.color} strokeWidth="1.5" strokeDasharray="4 2" /><text x={legendStartX+pLW+24} y={17} fontSize="8" fill="#a1a1aa">{panel.secondary.legendLabel}</text></svg>); };

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
            backgroundColor: card.highlight ? 'var(--accent-tint)' : 'var(--surface-paper)',
            border: card.highlight ? `2px solid ${COLORS.accent}` : '1.5px solid var(--outline-soft)',
            borderRadius: 14,
            padding: '18px 20px',
          }}
        >
          {card.highlight && (
            <span className="absolute top-3 right-3 text-[10px] font-bold uppercase tracking-wider" style={{ backgroundColor: 'var(--accent-tint)', color: 'var(--accent-tint-ink)', borderRadius: 20, padding: '3px 8px' }}>
              Key Lever
            </span>
          )}
          <div className="w-9 h-9 rounded-full flex items-center justify-center mb-3" style={{ backgroundColor: COLORS.accent }}>
            <span className="font-serif font-bold text-base text-white">{card.number}</span>
          </div>
          <p className="font-serif font-bold text-base mb-1" style={{ color: 'var(--ink-primary)' }}>{card.term}</p>
          <p className="text-[13px] leading-relaxed" style={{ color: 'var(--ink-secondary)' }}>{card.description}</p>
        </div>
      ))}
    </div>
    {accentNote && (
      <div className="mt-3" style={{ borderLeft: `3px solid ${COLORS.accent}`, backgroundColor: COLORS.accentTint, padding: '12px 16px', borderRadius: '0 10px 10px 0' }}>
        <p className="text-[13px] italic" style={{ color: COLORS.accentDarkText }}>{accentNote}</p>
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
        background: item.highlight ? 'var(--accent-tint)' : 'var(--surface-paper)',
        border: item.highlight ? `2px solid ${COLORS.accent}` : '1.5px solid var(--outline-soft)',
        borderRadius: 14,
        padding: '16px 20px',
        display: 'flex',
        alignItems: 'flex-start',
        gap: 16,
      }}>
        <div style={{
          background: item.highlight ? COLORS.accent : 'var(--surface-soft)',
          border: item.highlight ? 'none' : '1px solid var(--outline-soft)',
          borderRadius: 10,
          padding: '6px 12px',
          flexShrink: 0,
          fontFamily: "'Source Serif 4', serif",
          fontSize: 15,
          fontWeight: 700,
          color: item.highlight ? 'var(--ink-on-accent)' : 'var(--ink-primary)',
          whiteSpace: 'nowrap' as const,
        }}>
          &ldquo;{item.term}&rdquo;
        </div>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 13, fontWeight: 700, color: item.highlight ? 'var(--accent-tint-ink)' : 'var(--accent-text)', marginBottom: 4 }}>
            = {item.definition}
          </div>
          <div style={{ fontSize: 14, color: 'var(--ink-secondary)', lineHeight: 1.5 }}>
            {item.explanation}
          </div>
        </div>
      </div>
    ))}
  </div>
);
