
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Battery, Brain, Moon, Coffee, HeartPulse, SlidersHorizontal
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { orangeTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = orangeTheme;

// --- INTERACTIVE COMPONENTS ---

const AllostaticLoadComparison = () => {
    const [revealed, setRevealed] = useState(false);

    const W = 440, H = 260;
    const padL = 8, padR = 8, padT = 28, padB = 44;
    const chartW = W - padL - padR, chartH = H - padT - padB;
    const toX = (f: number) => padL + f * chartW;
    const toY = (f: number) => padT + (1 - f) * chartH;

    const months = ['Sep', 'Nov', 'Jan', 'Mar', 'May', 'Jun'];
    // No Recovery: stress climbs monotonically, accelerating at end
    const noRecStress = [0.15, 0.30, 0.45, 0.62, 0.82, 0.98];
    // No Recovery: performance starts OK then drops as load accumulates
    const noRecPerf = [0.70, 0.65, 0.55, 0.42, 0.30, 0.18];
    // Strategic Recovery: stress rises but dips from recovery windows
    const recStress = [0.15, 0.28, 0.22, 0.38, 0.32, 0.40];
    // Strategic Recovery: performance stays high with slight improvement
    const recPerf = [0.70, 0.68, 0.72, 0.70, 0.75, 0.78];

    const buildArea = (data: number[]) => {
        const pts = data.map((v, i) => ({ x: toX(i / (data.length - 1)), y: toY(v) }));
        let d = `M ${pts[0].x} ${toY(0)} L ${pts[0].x} ${pts[0].y}`;
        for (let i = 1; i < pts.length; i++) {
            const cx1 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.4;
            const cx2 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.6;
            d += ` C ${cx1} ${pts[i - 1].y}, ${cx2} ${pts[i].y}, ${pts[i].x} ${pts[i].y}`;
        }
        d += ` L ${pts[pts.length - 1].x} ${toY(0)} Z`;
        return d;
    };

    const buildLine = (data: number[]) => {
        const pts = data.map((v, i) => ({ x: toX(i / (data.length - 1)), y: toY(v) }));
        let d = `M ${pts[0].x} ${pts[0].y}`;
        for (let i = 1; i < pts.length; i++) {
            const cx1 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.4;
            const cx2 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.6;
            d += ` C ${cx1} ${pts[i - 1].y}, ${cx2} ${pts[i].y}, ${pts[i].x} ${pts[i].y}`;
        }
        return d;
    };

    const noRecPhases = [
        { label: 'Manageable', x1: 0, x2: 0.33, color: '#fca5a5' },
        { label: 'Accumulating', x1: 0.33, x2: 0.66, color: '#f87171' },
        { label: 'Burnout', x1: 0.66, x2: 1, color: '#ef4444' },
    ];
    const recPhases = [
        { label: 'Build + recover', x1: 0, x2: 0.33, color: '#6ee7b7' },
        { label: 'Sustain', x1: 0.33, x2: 0.66, color: '#34d399' },
        { label: 'Peak form', x1: 0.66, x2: 1, color: '#10b981' },
    ];

    const Chart = ({ primary, secondary, phases, areaColor, areaId, areaData, label }: {
        primary: number[]; secondary: number[]; phases: { label: string; x1: number; x2: number; color: string }[];
        areaColor: string; areaId: string; areaData: number[]; label: string;
    }) => (
        <svg viewBox={`0 0 ${W} ${H}`} className="w-full">
            <defs>
                <linearGradient id={areaId} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={areaColor} stopOpacity="0.5" />
                    <stop offset="100%" stopColor={areaColor} stopOpacity="0.05" />
                </linearGradient>
            </defs>
            {/* Grid lines */}
            {[0.25, 0.5, 0.75, 1.0].map(v => (
                <line key={v} x1={padL} x2={W - padR} y1={toY(v)} y2={toY(v)} stroke="#a1a1aa" strokeOpacity="0.15" strokeDasharray="3 3" />
            ))}
            {/* Baseline */}
            <line x1={padL} x2={W - padR} y1={toY(0)} y2={toY(0)} stroke="#a1a1aa" strokeOpacity="0.3" />
            {/* Area fill */}
            <motion.path
                d={buildArea(areaData)}
                fill={`url(#${areaId})`}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.8 }}
            />
            {/* Primary line (solid — Stress Load) */}
            <motion.path
                d={buildLine(primary)}
                fill="none" stroke={areaColor} strokeWidth="2.5" strokeLinecap="round"
                initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                transition={{ duration: 1.2, ease: 'easeOut' }}
            />
            {/* Secondary line (dashed — Performance) */}
            <motion.path
                d={buildLine(secondary)}
                fill="none" stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="5 3" strokeLinecap="round"
                initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                transition={{ duration: 1.2, ease: 'easeOut', delay: 0.3 }}
            />
            {/* Primary dots */}
            {primary.map((v, i) => (
                <motion.circle key={i} cx={toX(i / (primary.length - 1))} cy={toY(v)} r="3.5" fill={areaColor}
                    initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2 * i + 0.3 }}
                />
            ))}
            {/* Y-axis labels */}
            <text x={padL + 2} y={toY(1.0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">High</text>
            <text x={padL + 2} y={toY(0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">Low</text>
            {/* Month labels */}
            {months.map((m, i) => (
                <text key={m} x={toX(i / (months.length - 1))} y={toY(0) + 14} fontSize="9" fill="#a1a1aa" textAnchor="middle" fontWeight="600">{m}</text>
            ))}
            {/* Phase labels */}
            {phases.map((p, i) => (
                <text key={i} x={toX((p.x1 + p.x2) / 2)} y={toY(0) + 28} fontSize="8" fill={p.color} textAnchor="middle" fontWeight="700">{p.label}</text>
            ))}
            {/* Chart label */}
            <text x={W / 2} y={14} fontSize="11" fill="#71717a" textAnchor="middle" fontWeight="700">{label}</text>
            {/* Legend */}
            <line x1={W - padR - 108} x2={W - padR - 92} y1={14} y2={14} stroke={areaColor} strokeWidth="2" />
            <text x={W - padR - 88} y={17} fontSize="8" fill="#a1a1aa">Stress Load</text>
            <line x1={W - padR - 44} x2={W - padR - 28} y1={14} y2={14} stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="4 2" />
            <text x={W - padR - 24} y={17} fontSize="8" fill="#a1a1aa">Performance</text>
        </svg>
    );

    return (
        <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Recovery Effect</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Same exams. Same syllabus. One student recovers strategically.</p>

            {!revealed ? (
                <div className="text-center">
                    <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">Two students face the same Leaving Cert year. What happens when one builds in strategic recovery?</p>
                    <button onClick={() => setRevealed(true)} className="px-5 py-2.5 text-sm font-bold rounded-lg bg-orange-500 text-white hover:bg-orange-600 transition-colors">
                        Reveal the Recovery Effect
                    </button>
                </div>
            ) : (
                <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
                    <div className="grid md:grid-cols-2 gap-4 mb-5">
                        <div className="rounded-lg border border-rose-200 dark:border-rose-900 bg-rose-50/50 dark:bg-rose-950/20 p-3">
                            <Chart primary={noRecStress} secondary={noRecPerf} phases={noRecPhases}
                                areaColor="#ef4444" areaId="norec-grad" areaData={noRecStress} label="No Recovery Protocol" />
                        </div>
                        <div className="rounded-lg border border-emerald-200 dark:border-emerald-900 bg-emerald-50/50 dark:bg-emerald-950/20 p-3">
                            <Chart primary={recStress} secondary={recPerf} phases={recPhases}
                                areaColor="#10b981" areaId="rec-grad" areaData={recPerf} label="Strategic Recovery" />
                        </div>
                    </div>
                    <div className="grid md:grid-cols-2 gap-4 text-sm">
                        <div className="flex items-start gap-2.5 p-3 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900">
                            <span className="text-rose-500 text-lg mt-0.5">&#x2716;</span>
                            <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-rose-600 dark:text-rose-400">Without recovery</strong>, stress piles up like debt with interest. By May, you're so worn out that studying becomes pointless — you're running on fumes.</p>
                        </div>
                        <div className="flex items-start gap-2.5 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900">
                            <span className="text-emerald-500 text-lg mt-0.5">&#x2714;</span>
                            <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-emerald-600 dark:text-emerald-400">Strategic recovery</strong> — proper sleep, exercise, guided relaxation — creates deliberate dips in the stress curve. You arrive at exams with energy left in the tank.</p>
                        </div>
                    </div>
                </motion.div>
            )}
        </div>
    );
};

const AllostaticLoadVisualizer = () => {
    const W = 400, H = 190;
    const padL = 8, padR = 8, padT = 20, padB = 42;
    const chartW = W - padL - padR;
    const chartH = H - padT - padB;
    const toX = (pct: number) => padL + pct * chartW;
    const toY = (pct: number) => padT + chartH - pct * chartH;

    // Timeline data: [x position %, stress level 0-1]
    const points: [number, number][] = [
        [0, 0.06], [0.05, 0.10], [0.12, 0.16],
        [0.18, 0.24], [0.22, 0.30], [0.26, 0.24],
        [0.34, 0.22], [0.40, 0.18],
        [0.44, 0.10], [0.48, 0.08],             // summer dip
        [0.52, 0.15], [0.58, 0.26], [0.64, 0.38],
        [0.68, 0.44], [0.72, 0.42], [0.76, 0.52],
        [0.80, 0.60], [0.84, 0.68], [0.87, 0.74],
        [0.89, 0.68],                            // brief calm
        [0.91, 0.86], [0.925, 0.76],             // exam spikes
        [0.94, 0.92], [0.955, 0.82],
        [0.97, 0.96], [0.985, 0.88], [1.0, 0.78],
    ];

    const coords = points.map(([px, py]) => [toX(px), toY(py)]);
    let curvePath = `M ${coords[0][0]} ${coords[0][1]}`;
    for (let i = 1; i < coords.length; i++) {
        const [x, y] = coords[i];
        const [px, py] = coords[i - 1];
        curvePath += ` C ${px + (x - px) * 0.4} ${py}, ${px + (x - px) * 0.6} ${y}, ${x} ${y}`;
    }
    const areaPath = curvePath + ` L ${toX(1)} ${toY(0)} L ${toX(0)} ${toY(0)} Z`;

    const phases = [
        { start: 0, end: 0.40, label: '5th Year' },
        { start: 0.40, end: 0.50, label: 'Summer' },
        { start: 0.50, end: 0.78, label: '6th Year' },
        { start: 0.78, end: 0.89, label: 'Pre-Exam' },
        { start: 0.89, end: 1.0, label: 'Exams' },
    ];

    const yLevels = [
        { pct: 0, label: 'Low' },
        { pct: 0.33, label: 'Moderate' },
        { pct: 0.66, label: 'High' },
        { pct: 1.0, label: 'Critical' },
    ];

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Your Stress Build-Up Over the Leaving Cert</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-2">Your brain's stress builds up over time and spikes during exam clusters.</p>
            <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 mb-6">This is why mental stamina matters — not just knowledge.</p>

            <div className="bg-zinc-50 dark:bg-zinc-900/30 rounded-xl border border-zinc-200 dark:border-zinc-700 p-2 mb-4">
                <svg viewBox={`0 0 ${W} ${H}`} className="w-full h-auto">
                    <defs>
                        <linearGradient id="alLoadFill" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stopColor="#ef4444" stopOpacity="0.18" />
                            <stop offset="50%" stopColor="#f97316" stopOpacity="0.08" />
                            <stop offset="100%" stopColor="#f97316" stopOpacity="0" />
                        </linearGradient>
                        <linearGradient id="alStroke" x1="0" y1="0" x2="1" y2="0">
                            <stop offset="0%" stopColor="#fb923c" />
                            <stop offset="65%" stopColor="#f97316" />
                            <stop offset="85%" stopColor="#ef4444" />
                            <stop offset="100%" stopColor="#dc2626" />
                        </linearGradient>
                    </defs>

                    {/* Danger zone band */}
                    <rect x={padL} y={padT} width={chartW} height={chartH * 0.28} fill="#ef4444" opacity="0.04" />
                    <line x1={padL} y1={toY(0.72)} x2={W - padR} y2={toY(0.72)}
                        stroke="#ef4444" strokeWidth="0.6" strokeDasharray="4 3" opacity="0.3" />
                    <text x={W - padR - 4} y={toY(0.72) - 4} textAnchor="end"
                        className="text-[5px] font-bold" fill="#ef4444" opacity="0.5">DANGER ZONE</text>

                    {/* Y-axis gridlines + labels */}
                    {yLevels.map(({ pct, label }) => (
                        <g key={label}>
                            <line x1={padL} y1={toY(pct)} x2={W - padR} y2={toY(pct)}
                                stroke="#d4d4d8" strokeWidth="0.4" opacity="0.6" />
                            <text x={padL + 4} y={toY(pct) - 4} textAnchor="start"
                                className="text-[5.5px]" fill="#a1a1aa">{label}</text>
                        </g>
                    ))}

                    {/* Phase dividers + labels */}
                    {phases.map(({ start, end, label }, i) => {
                        const isExam = label === 'Exams';
                        const isPreExam = label === 'Pre-Exam';
                        const isSummer = label === 'Summer';
                        return (
                            <g key={label}>
                                {i > 0 && (
                                    <line x1={toX(start)} y1={padT} x2={toX(start)} y2={H - padB}
                                        stroke="#d4d4d8" strokeWidth="0.5" strokeDasharray="3 3" opacity="0.4" />
                                )}
                                <text x={toX((start + end) / 2)} y={H - padB + 14}
                                    textAnchor="middle"
                                    className="text-[7px] font-bold"
                                    fill={isExam ? '#dc2626' : isPreExam ? '#ef4444' : isSummer ? '#10b981' : '#a1a1aa'}
                                >
                                    {label}
                                </text>
                            </g>
                        );
                    })}

                    {/* Shaded area under curve */}
                    <path d={areaPath} fill="url(#alLoadFill)" />

                    {/* Main curve */}
                    <motion.path
                        d={curvePath}
                        fill="none"
                        stroke="url(#alStroke)"
                        strokeWidth="2.5"
                        strokeLinecap="round"
                        initial={{ pathLength: 0 }}
                        animate={{ pathLength: 1 }}
                        transition={{ duration: 2, ease: 'easeOut' }}
                    />

                    {/* Summer recovery annotation */}
                    <circle cx={toX(0.48)} cy={toY(0.08)} r="3" fill="#10b981" />
                    <text x={toX(0.48)} y={toY(0.08) + 12} textAnchor="middle"
                        className="text-[5px] font-semibold" fill="#10b981">Recovery</text>

                    {/* Peak load annotation */}
                    <circle cx={toX(0.97)} cy={toY(0.96)} r="3" fill="#dc2626" />
                    <text x={toX(0.97)} y={toY(0.96) - 7} textAnchor="middle"
                        className="text-[5px] font-bold" fill="#dc2626">Peak Load</text>

                </svg>
            </div>

            <p className="text-center text-xs text-zinc-500 dark:text-zinc-400">
                The exam spikes aren't the real danger — it's the <span className="font-semibold text-orange-600 dark:text-orange-400">stress that's been building up underneath</span> that determines whether you crash or keep going.
            </p>
        </div>
    );
};

const SleepCycleArchitect = () => {
    const [sleepHours, setSleepHours] = useState(8);

    const W = 400, H = 170;
    const padL = 6, padR = 6, padT = 16, padB = 28;
    const chartW = W - padL - padR;
    const chartH = H - padT - padB;
    const maxH = 9;
    const toX = (h: number) => padL + (h / maxH) * chartW;
    const toY = (d: number) => padT + d * chartH; // 0=awake(top), 1=deep(bottom)

    /* Hypnogram waypoints: [hour, depth 0-1]
       Early cycles: deep NREM dominant. Late cycles: REM dominant. */
    const wave: [number, number][] = [
        [0, 0], [0.2, 0.3], [0.5, 0.75], [0.8, 0.95], [1.1, 0.85],
        [1.3, 0.5], [1.45, 0.12], [1.55, 0.12],    // Cycle 1 REM (short)
        [1.65, 0.05],
        [1.85, 0.35], [2.1, 0.8], [2.4, 0.9], [2.6, 0.6],
        [2.8, 0.12], [3.1, 0.12],                   // Cycle 2 REM
        [3.2, 0.05],
        [3.4, 0.3], [3.7, 0.55], [3.9, 0.45],
        [4.1, 0.12], [4.55, 0.12],                  // Cycle 3 REM (longer)
        [4.65, 0.05],
        [4.85, 0.25], [5.1, 0.35],
        [5.3, 0.12], [6.0, 0.12],                   // Cycle 4 REM (long)
        [6.1, 0.05],
        [6.3, 0.2],
        [6.5, 0.12], [7.5, 0.12],                   // Cycle 5 REM (very long)
        [7.7, 0.08], [8.0, 0.05], [8.5, 0],
    ];

    const coords = wave.map(([h, d]) => [toX(h), toY(d)]);
    let curvePath = `M ${coords[0][0]} ${coords[0][1]}`;
    for (let i = 1; i < coords.length; i++) {
        const [x, y] = coords[i];
        const [px, py] = coords[i - 1];
        curvePath += ` C ${px + (x - px) * 0.4} ${py}, ${px + (x - px) * 0.6} ${y}, ${x} ${y}`;
    }
    const areaPath = curvePath + ` L ${coords[coords.length - 1][0]} ${toY(0)} L ${toX(0)} ${toY(0)} Z`;

    /* REM regions for highlight + loss calculation */
    const remRegions = [
        { start: 1.45, end: 1.55 },
        { start: 2.8, end: 3.1 },
        { start: 4.1, end: 4.55 },
        { start: 5.3, end: 6.0 },
        { start: 6.5, end: 7.5 },
    ];
    const totalRemMin = remRegions.reduce((s, r) => s + (r.end - r.start) * 60, 0);
    const lostRemMin = remRegions.reduce((s, r) => {
        if (sleepHours >= r.end) return s;
        if (sleepHours <= r.start) return s + (r.end - r.start) * 60;
        return s + (r.end - sleepHours) * 60;
    }, 0);
    const remLostPct = Math.round((lostRemMin / totalRemMin) * 100);

    const stages = [
        { d: 0, label: 'Awake' },
        { d: 0.5, label: 'Light' },
        { d: 1.0, label: 'Deep' },
    ];
    const hourMarks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Sleep Cycle Architect</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-2">Drag the slider to cut your sleep short and see what gets sacrificed.</p>
            <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 mb-6">The REM-rich later cycles are the first to go.</p>

            <div className="bg-zinc-50 dark:bg-zinc-900/30 rounded-xl border border-zinc-200 dark:border-zinc-700 p-2 mb-4">
                <svg viewBox={`0 0 ${W} ${H}`} className="w-full h-auto">
                    <defs>
                        <linearGradient id="sleepFill" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stopColor="#818cf8" stopOpacity="0.03" />
                            <stop offset="100%" stopColor="#4f46e5" stopOpacity="0.2" />
                        </linearGradient>
                    </defs>

                    {/* Stage gridlines */}
                    {stages.map(({ d, label }) => (
                        <g key={label}>
                            <line x1={padL} y1={toY(d)} x2={W - padR} y2={toY(d)}
                                stroke="#d4d4d8" strokeWidth="0.4" opacity="0.5" />
                            <text x={padL + 4} y={toY(d) - 4} textAnchor="start"
                                className="text-[5.5px]" fill="#a1a1aa">{label}</text>
                        </g>
                    ))}

                    {/* Hour tick marks */}
                    {hourMarks.map(h => (
                        <g key={h}>
                            <line x1={toX(h)} y1={H - padB} x2={toX(h)} y2={H - padB + 4}
                                stroke="#d4d4d8" strokeWidth="0.5" />
                            <text x={toX(h)} y={H - padB + 13} textAnchor="middle"
                                className="text-[6px]" fill="#a1a1aa">{h}h</text>
                        </g>
                    ))}

                    {/* REM highlight bands */}
                    {remRegions.map((r, i) => (
                        <rect key={i} x={toX(r.start)} y={padT}
                            width={toX(r.end) - toX(r.start)} height={chartH * 0.18}
                            fill="#f59e0b" opacity="0.12" rx="1" />
                    ))}
                    {/* REM label on wider bands */}
                    {remRegions.slice(2).map((r, i) => (
                        <text key={i} x={toX((r.start + r.end) / 2)} y={padT + 9}
                            textAnchor="middle" className="text-[4.5px] font-bold" fill="#d97706" opacity="0.7">REM</text>
                    ))}

                    {/* Shaded area under curve */}
                    <path d={areaPath} fill="url(#sleepFill)" />

                    {/* Hypnogram wave */}
                    <path d={curvePath} fill="none" stroke="#6366f1" strokeWidth="2" strokeLinecap="round" />

                    {/* Cut-off overlay */}
                    <rect x={toX(sleepHours)} y={0} width={W - toX(sleepHours)} height={H}
                        fill="currentColor" className="text-zinc-100 dark:text-zinc-800" opacity="0.82" />

                    {/* Wake-up line */}
                    {sleepHours < 9 && (
                        <>
                            <line x1={toX(sleepHours)} y1={padT - 2} x2={toX(sleepHours)} y2={H - padB}
                                stroke="#ef4444" strokeWidth="1.5" strokeDasharray="4 3" />
                            <text x={toX(sleepHours)} y={padT - 5} textAnchor="middle"
                                className="text-[5.5px] font-bold" fill="#ef4444">WAKE UP</text>
                        </>
                    )}
                </svg>
            </div>

            {/* Slider */}
            <div className="px-2">
                <input type="range" min="4" max="9" step="0.5" value={sleepHours}
                    onChange={e => setSleepHours(parseFloat(e.target.value))}
                    className="w-full accent-orange-500" />
                <div className="flex justify-between items-center mt-1">
                    <span className="text-[10px] text-zinc-400 dark:text-zinc-500">4 hours</span>
                    <span className="text-sm font-bold text-zinc-700 dark:text-zinc-200">{sleepHours} hours of sleep</span>
                    <span className="text-[10px] text-zinc-400 dark:text-zinc-500">9 hours</span>
                </div>
            </div>

            {/* Legend */}
            <div className="flex justify-center gap-5 mt-4 mb-3">
                <div className="flex items-center gap-1.5">
                    <div className="w-3 h-2 rounded-sm bg-indigo-400" />
                    <span className="text-[10px] text-zinc-500 dark:text-zinc-400">NREM (Deep + Light)</span>
                </div>
                <div className="flex items-center gap-1.5">
                    <div className="w-3 h-2 rounded-sm bg-amber-400" />
                    <span className="text-[10px] text-zinc-500 dark:text-zinc-400">REM Sleep</span>
                </div>
            </div>

            {/* REM loss warning */}
            <AnimatePresence>
                {remLostPct > 0 && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                        className="mt-3 p-4 bg-rose-50 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-800/40 rounded-xl text-center text-sm text-zinc-700 dark:text-zinc-300"
                    >
                        You've lost approximately <span className="font-bold text-rose-600 dark:text-rose-400">{remLostPct}%</span> of your REM sleep — impairing problem-solving and emotional regulation.
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

// --- MODULE COMPONENT ---
const CognitiveEnduranceModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'marathon-mindset', title: 'The Marathon Mindset', eyebrow: '01 // The Big Picture', icon: Brain },
    { id: 'sleep-banking', title: 'The Sleep Banking Strategy', eyebrow: '02 // The Non-Negotiable', icon: Moon },
    { id: 'fueling-engine', title: 'Fueling the Engine', eyebrow: '03 // Food & Drink', icon: Coffee },
    { id: 'in-exam-tools', title: 'The In-Exam Toolkit', eyebrow: '04 // Staying Calm Under Pressure', icon: HeartPulse },
    { id: 'training-plan', title: 'The Training Plan', eyebrow: '05 // Building Up Gradually', icon: SlidersHorizontal },
    { id: 'recovery-protocol', title: 'The Recovery Protocol', eyebrow: '06 // Real Rest', icon: Battery },
  ];

  return (
    <ModuleLayout
      moduleNumber="06"
      moduleTitle="Cognitive Endurance"
      moduleSubtitle="The Marathon Method"
      moduleDescription="The Leaving Cert isn't a sprint. Learn how to keep your brain sharp across weeks of exams, even when you're tired and stressed."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Go the Distance"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Marathon Mindset." eyebrow="Step 1" icon={Brain} theme={theme}>
              <p>The Leaving Cert isn't a sprint; it's a marathon. Success isn't just about knowing the material. It's about being able to access that knowledge at 4 PM on a Friday after a brutal week of exams. This is <Highlight description="Your ability to stay focused and think clearly for long stretches, even when you're tired or stressed. Think of it like fitness for your brain." theme={theme}>Cognitive Endurance</Highlight>.</p>
              <p>It's a trainable skill, not a measure of willpower. Your brain is an organ that uses 20% of your body's energy. Under the constant stress of the Leaving Cert, your brain builds up "wear and tear" over time — we call this <Highlight description="The total stress build-up in your body and brain from weeks of pressure. When it gets too high, your thinking gets foggy and your emotions get harder to control." theme={theme}>Stress Load</Highlight>. Building cognitive endurance is about training your brain to handle this build-up.</p>
              <AllostaticLoadVisualizer />
              <AllostaticLoadComparison />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Sleep Banking Strategy." eyebrow="Step 2" icon={Moon} theme={theme}>
              <p>Sleep is the single most powerful tool for building endurance. It's not just rest; it's when your brain organises your memories and clears out the <Highlight description="A chemical that builds up in your brain the longer you're awake. It's basically what makes you feel foggy and tired — and sleep is the only thing that properly clears it out." theme={theme}>tiredness chemicals</Highlight> that pile up during the day.</p>
              <p>As a teenager, your brain is naturally wired to sleep late and wake up late. The exam schedule fights this. The really important thing is that the final hours of your sleep are packed with <Highlight description="A special stage of sleep where your brain practises problem-solving and processes your emotions. Most of it happens in the last few hours of sleep, so if you cut your night short, this is the first thing you lose." theme={theme}>REM Sleep</Highlight>, which is vital for problem-solving and keeping your emotions in check. Cutting sleep short is like skipping the most important part of your training.</p>
              <SleepCycleArchitect />
              <MicroCommitment theme={theme}><p>For the next 10 days, wake up at the same time every single day — even weekends. This is the fastest way to reset your body clock so you feel most alert during exam time.</p></MicroCommitment>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Fueling the Engine." eyebrow="Step 3" icon={Coffee} theme={theme}>
              <p>Your brain runs on sugar from your blood. An unstable fuel supply leads to unstable focus. High-sugar snacks cause a spike-and-crash cycle — a <Highlight description="That horrible brain fog and irritability you get about an hour after eating something really sugary. Your blood sugar spikes, then crashes, leaving you unable to concentrate — often right in the middle of an exam." theme={theme}>sugar crash</Highlight> — that can sabotage your performance mid-exam.</p>
              <p>Here's a neat trick from sports science: the <Highlight description="A simple hack where you swish a sports drink around your mouth for about 10 seconds (you don't even have to swallow it). It tricks your brain into feeling less tired by activating your brain's reward system." theme={theme}>Sports Drink Mouth Rinse</Highlight>. Swishing a sports drink around your mouth for 10 seconds tricks your brain into thinking fuel is on the way. This can give you a real mental boost in the final, gruelling hour of a long exam.</p>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The In-Exam Toolkit." eyebrow="Step 4" icon={HeartPulse} theme={theme}>
                <p>Anxiety is the enemy of endurance. It hijacks your brain, shutting down your <Highlight description="The front part of your brain that handles thinking, planning, and staying focused. When you're stressed or panicking, this part basically goes offline — which is why you can't think straight." theme={theme}>thinking brain</Highlight> and handing control to your <Highlight description="The part of your brain that triggers fear and panic. When it takes over, it can cause you to 'blank out' — even on stuff you definitely know." theme={theme}>panic centre</Highlight>. You need tools to manage this in real-time.</p>
                <p>The fastest way to calm yourself down is the <Highlight description="A breathing trick: two quick sniffs in through your nose, then one long breath out through your mouth. It works in under 10 seconds and physically calms your nervous system down." theme={theme}>Physiological Sigh</Highlight>. It takes less than 10 seconds. When you feel panic rising after a tough question, this is your emergency brake.</p>
                <p>For your eyes, use the <strong>20-20-20 Rule</strong>: every 20 minutes, look at something 20 feet away for 20 seconds. This relaxes your eye muscles and fights the visual fatigue that causes headaches and slows reading speed.</p>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="The Training Plan." eyebrow="Step 5" icon={SlidersHorizontal} theme={theme}>
              <p>You can't train for a marathon by only running sprints. Likewise, you can't prepare for a 3-hour exam by only studying in 20-minute bursts. You need to train your focus by <Highlight description="The simple idea behind all training: start easy and gradually make it harder. For studying, this means starting with short focus sessions and slowly making them longer over time." theme={theme}>building up gradually</Highlight>.</p>
              <p>This means structuring your study in phases. Start with short, focused bursts (like 25-minute Pomodoro sessions) to build your base. Then, gradually increase the length of your focus blocks, training your brain to push past the "boredom barrier." In the final weeks, you should be doing full practice runs — studying under exam conditions for 90-120 minutes straight. This is not about learning more content; it's about building mental muscle.</p>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="The Recovery Protocol." eyebrow="Step 6" icon={Battery} theme={theme}>
              <p>Recovery is not the absence of work; it's an active process. Lying on the couch scrolling through TikTok is not rest. It's <Highlight description="The kind of 'rest' that doesn't actually recharge you — like scrolling social media or bingeing videos. It feels relaxing but it keeps your brain busy and tired." theme={theme}>Junk Rest</Highlight>, and it can actually make your mental tiredness worse.</p>
              <p><Highlight description="Rest that actually recharges your brain — things like going for a walk, spending time outside, or doing a guided relaxation. It feels boring compared to your phone, but it works way better." theme={theme}>Real Rest</Highlight> strategies are far better. A 20-minute walk clears stress hormones. Even better is <Highlight description="Non-Sleep Deep Rest — basically a guided relaxation you do while lying down with your eyes closed. You stay awake, but your brain gets a proper reset. Think of it like a power nap without actually sleeping." theme={theme}>NSDR</Highlight>, a 10-20 minute guided relaxation that acts as a "reset button" for your brain. In the crucial break between two exams on the same day, a 20-minute NSDR session is the single most effective way to recharge for the afternoon paper.</p>
              <MicroCommitment theme={theme}><p>Find a 10-minute NSDR or Yoga Nidra script on YouTube. Try it once this week instead of scrolling on your phone during a study break.</p></MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default CognitiveEnduranceModule;
