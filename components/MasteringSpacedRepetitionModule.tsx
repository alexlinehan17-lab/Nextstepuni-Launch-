
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Clock, BarChart2, CalendarDays, RadioTower, Wrench, Brain, RefreshCcw, TrendingDown
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { skyTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = skyTheme;

// --- INTERACTIVE COMPONENTS ---
const ForgettingCurveVisualizer = () => {
    const [reviewCount, setReviewCount] = useState(0);

    // Review schedule: day 1, 3, 7, 14 — with increasing stability
    const reviewSchedule = [
      { day: 1, stability: 2.5, label: 'Review 1 (Day 1)' },
      { day: 3, stability: 6, label: 'Review 2 (Day 3)' },
      { day: 7, stability: 14, label: 'Review 3 (Day 7)' },
      { day: 14, stability: 35, label: 'Review 4 (Day 14)' },
    ];

    const totalDays = 30;

    // Chart dimensions — extra padding for labels
    const W = 400, H = 200;
    const padL = 40, padR = 16, padT = 20, padB = 36;
    const chartW = W - padL - padR;
    const chartH = H - padT - padB;
    const toX = (day: number) => padL + (day / totalDays) * chartW;
    const toY = (pct: number) => padT + chartH - (pct / 100) * chartH;

    // Build retention data as segments between review points
    const buildCurvePoints = (numReviews: number): [number, number][] => {
      const activeReviews = reviewSchedule.slice(0, numReviews);
      const reviewDays = activeReviews.map(r => r.day);
      const points: [number, number][] = [];

      let stability = 1.2;
      let retentionAtReset = 100;
      let lastResetDay = 0;

      // Generate smooth sample points between resets
      const addSegment = (fromDay: number, toDay: number, stab: number, startR: number) => {
        const steps = Math.max(8, Math.round((toDay - fromDay) * 2));
        for (let i = 0; i <= steps; i++) {
          const day = fromDay + (i / steps) * (toDay - fromDay);
          const elapsed = day - fromDay;
          const retention = startR * Math.exp(-elapsed / stab);
          points.push([day, Math.max(3, Math.min(100, retention))]);
        }
      };

      // Build segments between reviews
      const breakpoints = [...reviewDays.filter(d => d > 0), totalDays];
      for (const bp of breakpoints) {
        addSegment(lastResetDay, bp, stability, retentionAtReset);

        const review = activeReviews.find(r => r.day === bp);
        if (review) {
          const elapsed = bp - lastResetDay;
          const retentionAtReview = retentionAtReset * Math.exp(-elapsed / stability);
          const boosted = Math.min(98, retentionAtReview + (100 - retentionAtReview) * 0.9);
          points.push([bp, boosted]); // vertical jump
          lastResetDay = bp;
          stability = review.stability;
          retentionAtReset = boosted;
        }
      }

      // If no reviews reach totalDays, add the base decay
      if (breakpoints[breakpoints.length - 1] !== totalDays || breakpoints.length === 1) {
        addSegment(lastResetDay, totalDays, stability, retentionAtReset);
      }

      return points;
    };

    const baselinePoints = buildCurvePoints(0);
    const activePoints = buildCurvePoints(reviewCount);

    // Smooth cubic bezier path builder
    const buildPath = (points: [number, number][]) => {
      if (points.length < 2) return '';
      const coords = points.map(([d, r]) => [toX(d), toY(r)]);
      let path = `M ${coords[0][0]} ${coords[0][1]}`;

      for (let i = 1; i < coords.length; i++) {
        const [x, y] = coords[i];
        const [px, py] = coords[i - 1];
        // Detect vertical jump (review reset) — use straight line
        if (Math.abs(x - px) < 1) {
          path += ` L ${x} ${y}`;
        } else {
          // Smooth cubic bezier
          const cpx1 = px + (x - px) * 0.4;
          const cpx2 = px + (x - px) * 0.6;
          path += ` C ${cpx1} ${py}, ${cpx2} ${y}, ${x} ${y}`;
        }
      }
      return path;
    };

    const baselinePath = buildPath(baselinePoints);
    const activePath = buildPath(activePoints);

    const finalRetention = Math.round(activePoints[activePoints.length - 1][1]);
    const baselineRetention = Math.round(baselinePoints[baselinePoints.length - 1][1]);

    const dayMarkers = [0, 5, 10, 15, 20, 25, 30];
    const retentionMarkers = [0, 25, 50, 75, 100];

    // Segment colors for cascading effect
    const segmentColors = ['#0ea5e9', '#06b6d4', '#14b8a6', '#10b981'];

    return (
      <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Forgetting Curve</h4>
        <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-2">Each review doesn't just refresh the memory — it makes the decay slower.</p>
        <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 mb-6">Add reviews one at a time and watch the curve flatten.</p>

        {/* Chart */}
        <div className="bg-zinc-50 dark:bg-zinc-900/30 rounded-xl border border-zinc-200 dark:border-zinc-700 p-2 mb-4">
          <svg viewBox={`0 0 ${W} ${H}`} className="w-full h-auto">
            <defs>
              <linearGradient id="srActiveGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#0ea5e9" stopOpacity="0.15" />
                <stop offset="100%" stopColor="#0ea5e9" stopOpacity="0" />
              </linearGradient>
            </defs>

            {/* Gridlines */}
            {retentionMarkers.map(pct => (
              <g key={pct}>
                <line x1={padL} y1={toY(pct)} x2={W - padR} y2={toY(pct)} stroke="currentColor" className="text-zinc-200 dark:text-zinc-700" strokeWidth="0.5" />
                <text x={padL - 5} y={toY(pct) + 3} textAnchor="end" className="text-[7px]" fill="#a1a1aa">{pct}%</text>
              </g>
            ))}
            {dayMarkers.map(d => (
              <g key={d}>
                <line x1={toX(d)} y1={padT} x2={toX(d)} y2={H - padB} stroke="currentColor" className="text-zinc-200 dark:text-zinc-700" strokeWidth="0.5" />
                <text x={toX(d)} y={H - padB + 14} textAnchor="middle" className="text-[7px]" fill="#a1a1aa">{d === 0 ? 'Learn' : `${d}d`}</text>
              </g>
            ))}

            {/* Axis labels */}
            <text x={padL + 2} y={padT - 6} textAnchor="start" className="text-[7px] font-bold" fill="#a1a1aa">Retention</text>
            <text x={W - padR} y={H - 4} textAnchor="end" className="text-[7px] font-bold" fill="#a1a1aa">Days</text>

            {/* Baseline curve (no reviews) */}
            <path d={baselinePath} fill="none" stroke="#d4d4d8" strokeWidth="1.5" strokeDasharray="5 3" className="dark:opacity-40" />

            {/* Shaded area under active curve */}
            {reviewCount > 0 && (
              <motion.path
                key={`fill-${reviewCount}`}
                d={`${activePath} L ${toX(totalDays)} ${toY(0)} L ${toX(0)} ${toY(0)} Z`}
                fill="url(#srActiveGrad)"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5 }}
              />
            )}

            {/* Active curve */}
            <motion.path
              key={`curve-${reviewCount}`}
              d={activePath}
              fill="none"
              stroke={segmentColors[Math.max(0, reviewCount - 1)] || '#0ea5e9'}
              strokeWidth="2.5"
              strokeLinecap="round"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 1.2, ease: 'easeOut' }}
            />

            {/* Review point markers */}
            {reviewSchedule.slice(0, reviewCount).map((r, i) => (
              <g key={i}>
                <motion.circle
                  cx={toX(r.day)} cy={toY(98)}
                  r="4"
                  fill={segmentColors[i]}
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.3, type: 'spring' }}
                />
                <motion.line
                  x1={toX(r.day)} y1={padT} x2={toX(r.day)} y2={H - padB}
                  stroke={segmentColors[i]}
                  strokeWidth="0.8"
                  strokeDasharray="2 2"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 0.3 }}
                  transition={{ delay: 0.2 }}
                />
              </g>
            ))}

            {/* Endpoint dots */}
            <circle cx={toX(totalDays)} cy={toY(baselineRetention)} r="3" fill="#d4d4d8" />
            <motion.circle
              key={`end-${reviewCount}`}
              cx={toX(totalDays)} cy={toY(finalRetention)}
              r="4"
              fill={segmentColors[Math.max(0, reviewCount - 1)] || '#0ea5e9'}
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.8 }}
            />
          </svg>
        </div>

        {/* Review buttons */}
        <div className="flex justify-center gap-2 mb-5">
          {reviewSchedule.map((r, i) => (
            <button
              key={i}
              onClick={() => setReviewCount(i + 1)}
              disabled={i + 1 <= reviewCount}
              className={`px-3 py-2 text-[10px] font-bold rounded-lg border transition-all ${
                i < reviewCount
                  ? 'text-white border-transparent'
                  : i === reviewCount
                    ? 'bg-sky-50 dark:bg-sky-950/20 text-sky-700 dark:text-sky-300 border-sky-200 dark:border-sky-800/40 hover:border-sky-400 cursor-pointer'
                    : 'bg-zinc-50 dark:bg-zinc-900/30 text-zinc-400 dark:text-zinc-500 border-zinc-200 dark:border-zinc-700 opacity-50 cursor-not-allowed'
              }`}
              style={i < reviewCount ? { backgroundColor: segmentColors[i] } : undefined}
            >
              {r.label}
            </button>
          ))}
          {reviewCount > 0 && (
            <button
              onClick={() => setReviewCount(0)}
              className="px-3 py-2 text-[10px] font-bold rounded-lg text-zinc-500 dark:text-zinc-400 border border-zinc-200 dark:border-zinc-700 hover:border-zinc-400"
            >
              Reset
            </button>
          )}
        </div>

        {/* Retention comparison */}
        <div className="grid grid-cols-2 gap-3">
          <div className="p-3 bg-zinc-50 dark:bg-zinc-900/30 rounded-xl border border-zinc-200 dark:border-zinc-700 text-center">
            <p className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 mb-1">No Review (Day 30)</p>
            <p className="text-2xl font-bold text-zinc-400">{baselineRetention}%</p>
          </div>
          <div className={`p-3 rounded-xl border text-center ${
            reviewCount > 0
              ? 'bg-sky-50 dark:bg-sky-950/20 border-sky-200 dark:border-sky-800/40'
              : 'bg-zinc-50 dark:bg-zinc-900/30 border-zinc-200 dark:border-zinc-700'
          }`}>
            <p className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 mb-1">
              {reviewCount > 0 ? `${reviewCount} Review${reviewCount > 1 ? 's' : ''} (Day 30)` : 'Add Reviews'}
            </p>
            <p className={`text-2xl font-bold ${reviewCount > 0 ? 'text-sky-500' : 'text-zinc-400'}`}>{finalRetention}%</p>
          </div>
        </div>

        {/* Stability insight */}
        {reviewCount > 0 && (
          <motion.p
            key={reviewCount}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center text-xs text-zinc-500 dark:text-zinc-400 mt-4"
          >
            {reviewCount === 1 && 'After 1 review, the memory is slightly more stable — but still fragile.'}
            {reviewCount === 2 && 'After 2 reviews, the decay is noticeably slower. The curve is flattening.'}
            {reviewCount === 3 && 'After 3 reviews, the memory is becoming durable. Notice how much flatter the curve is.'}
            {reviewCount === 4 && 'After 4 spaced reviews, retention at day 30 is dramatically higher. Each review made the memory progressively harder to forget.'}
          </motion.p>
        )}
      </div>
    );
};


const RetentionCurveComparison = () => {
    const [revealed, setRevealed] = useState(false);

    const W = 440, H = 260;
    const padL = 8, padR = 8, padT = 28, padB = 44;
    const chartW = W - padL - padR, chartH = H - padT - padB;
    const toX = (f: number) => padL + f * chartW;
    const toY = (f: number) => padT + (1 - f) * chartH;

    const days = ['Day 1', 'Day 3', 'Day 7', 'Day 14', 'Day 21', 'Day 30'];
    // The Crammer: single massive session, Ebbinghaus forgetting curve
    const cramRetention = [0.95, 0.60, 0.35, 0.20, 0.12, 0.08];
    // The Spacer: spaced reviews with increasing intervals
    const spacerRetention = [0.55, 0.42, 0.60, 0.50, 0.65, 0.58];
    // Stress lines
    const cramStress = [0.10, 0.15, 0.30, 0.55, 0.80, 0.95];
    const spacerStress = [0.20, 0.18, 0.15, 0.12, 0.10, 0.08];

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

    const cramPhases = [
        { label: 'Feels great', x1: 0, x2: 0.33, color: '#fca5a5' },
        { label: 'Fading fast', x1: 0.33, x2: 0.66, color: '#f87171' },
        { label: 'Gone', x1: 0.66, x2: 1, color: '#ef4444' },
    ];
    const spacerPhases = [
        { label: 'Learn + review', x1: 0, x2: 0.33, color: '#6ee7b7' },
        { label: 'Spaces widen', x1: 0.33, x2: 0.66, color: '#34d399' },
        { label: 'Locked in', x1: 0.66, x2: 1, color: '#10b981' },
    ];

    const Chart = ({ effort, stress, phases, areaColor, areaId, stressColor, label }: {
        effort: number[]; stress: number[]; phases: { label: string; x1: number; x2: number; color: string }[];
        areaColor: string; areaId: string; stressColor: string; label: string;
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
            {/* Retention area */}
            <motion.path
                d={buildArea(effort)}
                fill={`url(#${areaId})`}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.8 }}
            />
            {/* Retention line */}
            <motion.path
                d={buildLine(effort)}
                fill="none" stroke={areaColor} strokeWidth="2.5" strokeLinecap="round"
                initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                transition={{ duration: 1.2, ease: 'easeOut' }}
            />
            {/* Stress line (dashed) */}
            <motion.path
                d={buildLine(stress)}
                fill="none" stroke={stressColor} strokeWidth="1.5" strokeDasharray="5 3" strokeLinecap="round"
                initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                transition={{ duration: 1.2, ease: 'easeOut', delay: 0.3 }}
            />
            {/* Retention dots */}
            {effort.map((v, i) => (
                <motion.circle key={i} cx={toX(i / (effort.length - 1))} cy={toY(v)} r="3.5" fill={areaColor}
                    initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2 * i + 0.3 }}
                />
            ))}
            {/* Y-axis labels */}
            <text x={padL + 2} y={toY(1.0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">High</text>
            <text x={padL + 2} y={toY(0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">Low</text>
            {/* Day labels */}
            {days.map((m, i) => (
                <text key={m} x={toX(i / (days.length - 1))} y={toY(0) + 14} fontSize="9" fill="#a1a1aa" textAnchor="middle" fontWeight="600">{m}</text>
            ))}
            {/* Phase labels */}
            {phases.map((p, i) => (
                <text key={i} x={toX((p.x1 + p.x2) / 2)} y={toY(0) + 28} fontSize="8" fill={p.color} textAnchor="middle" fontWeight="700">{p.label}</text>
            ))}
            {/* Chart label */}
            <text x={W / 2} y={14} fontSize="11" fill="#71717a" textAnchor="middle" fontWeight="700">{label}</text>
            {/* Legend */}
            <line x1={W - padR - 100} x2={W - padR - 84} y1={14} y2={14} stroke={areaColor} strokeWidth="2" />
            <text x={W - padR - 80} y={17} fontSize="8" fill="#a1a1aa">Retention</text>
            <line x1={W - padR - 44} x2={W - padR - 28} y1={14} y2={14} stroke={stressColor} strokeWidth="1.5" strokeDasharray="4 2" />
            <text x={W - padR - 24} y={17} fontSize="8" fill="#a1a1aa">Stress</text>
        </svg>
    );

    return (
        <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Retention Crossover</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Same material. Same student. Two different strategies.</p>

            {!revealed ? (
                <div className="text-center">
                    <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">Most students cram before exams. What does their retention actually look like over 30 days?</p>
                    <button onClick={() => setRevealed(true)} className="px-5 py-2.5 text-sm font-bold rounded-lg bg-sky-500 text-white hover:bg-sky-600 transition-colors">
                        Reveal the Crossover
                    </button>
                </div>
            ) : (
                <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
                    <div className="grid md:grid-cols-2 gap-4 mb-5">
                        <div className="rounded-lg border border-rose-200 dark:border-rose-900 bg-rose-50/50 dark:bg-rose-950/20 p-3">
                            <Chart effort={cramRetention} stress={cramStress} phases={cramPhases}
                                areaColor="#ef4444" areaId="cram-grad" stressColor="#f59e0b" label="The Crammer" />
                        </div>
                        <div className="rounded-lg border border-emerald-200 dark:border-emerald-900 bg-emerald-50/50 dark:bg-emerald-950/20 p-3">
                            <Chart effort={spacerRetention} stress={spacerStress} phases={spacerPhases}
                                areaColor="#10b981" areaId="spacer-grad" stressColor="#f59e0b" label="The Spacer" />
                        </div>
                    </div>
                    <div className="grid md:grid-cols-2 gap-4 text-sm">
                        <div className="flex items-start gap-2.5 p-3 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900">
                            <span className="text-rose-500 text-lg mt-0.5">&#x2716;</span>
                            <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-rose-600 dark:text-rose-400">Cramming</strong> gives an illusion of mastery. Retention peaks immediately then collapses. By exam day, you're relearning from scratch.</p>
                        </div>
                        <div className="flex items-start gap-2.5 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900">
                            <span className="text-emerald-500 text-lg mt-0.5">&#x2714;</span>
                            <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-emerald-600 dark:text-emerald-400">Spacing</strong> feels slower, but each review strengthens the memory trace. By exam day, the material is deeply encoded.</p>
                        </div>
                    </div>
                </motion.div>
            )}
        </div>
    );
};

const MotionDiv = motion.div as any;

const CrammingVsSpacingShowdown = () => {
  type Phase = 'idle' | 'day1' | 'day7' | 'day30' | 'done';
  const [phase, setPhase] = useState<Phase>('idle');
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const clearTimers = () => {
    if (timerRef.current) clearTimeout(timerRef.current);
  };

  useEffect(() => {
    return () => clearTimers();
  }, []);

  const runExperiment = () => {
    clearTimers();
    setPhase('day1');
    timerRef.current = setTimeout(() => {
      setPhase('day7');
      timerRef.current = setTimeout(() => {
        setPhase('day30');
        timerRef.current = setTimeout(() => {
          setPhase('done');
        }, 3000);
      }, 3000);
    }, 3000);
  };

  const reset = () => {
    clearTimers();
    setPhase('idle');
  };

  const scores: Record<string, { crammer: number; spacer: number }> = {
    day1: { crammer: 85, spacer: 72 },
    day7: { crammer: 35, spacer: 68 },
    day30: { crammer: 12, spacer: 55 },
  };

  const currentPhaseKey = phase === 'done' ? 'day30' : phase;
  const crammerScore = phase === 'idle' ? 0 : scores[currentPhaseKey as keyof typeof scores]?.crammer ?? 0;
  const spacerScore = phase === 'idle' ? 0 : scores[currentPhaseKey as keyof typeof scores]?.spacer ?? 0;

  const phaseLabel = (() => {
    switch (phase) {
      case 'day1': return 'Day 1: Cramming wins!';
      case 'day7': return 'Day 7: Spacing wins by nearly 2x';
      case 'day30':
      case 'done': return 'Day 30: Crammer forgot almost everything';
      default: return '';
    }
  })();

  const transitionText = (() => {
    switch (phase) {
      case 'day7': return '7 days pass...';
      case 'day30':
      case 'done': return '30 days pass...';
      default: return '';
    }
  })();

  const barMaxH = 200;

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">
        Cramming vs. Spacing Showdown
      </h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-2">
        Two students study the same 6 hours total. Who remembers more?
      </p>
      <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 mb-8">
        Run the experiment and watch what happens over time.
      </p>

      {/* Two lanes */}
      <div className="grid grid-cols-2 gap-4 md:gap-6 mb-6">
        {/* Crammer lane */}
        <div className="p-4 md:p-6 bg-rose-50 dark:bg-rose-950/20 rounded-xl border border-rose-200 dark:border-rose-800/40 text-center">
          <p className="font-bold text-rose-700 dark:text-rose-300 text-lg mb-1">Crammer</p>
          <p className="text-xs text-rose-500 dark:text-rose-400 mb-6">6 hours the night before</p>
          <div className="flex justify-center items-end mb-3" style={{ height: barMaxH }}>
            <MotionDiv
              className="w-16 md:w-20 rounded-t-lg bg-rose-400 dark:bg-rose-500 relative"
              initial={{ height: 0 }}
              animate={{ height: (crammerScore / 100) * barMaxH }}
              transition={{ duration: 1, ease: 'easeOut' }}
            >
              {phase !== 'idle' && (
                <MotionDiv
                  className="absolute -top-7 left-0 right-0 text-center font-bold text-sm text-rose-700 dark:text-rose-300"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.8 }}
                >
                  {crammerScore}%
                </MotionDiv>
              )}
            </MotionDiv>
          </div>
          <div className="h-1 bg-rose-200 dark:bg-rose-800/40 rounded-full" />
        </div>

        {/* Spacer lane */}
        <div className="p-4 md:p-6 bg-emerald-50 dark:bg-emerald-950/20 rounded-xl border border-emerald-200 dark:border-emerald-800/40 text-center">
          <p className="font-bold text-emerald-700 dark:text-emerald-300 text-lg mb-1">Spacer</p>
          <p className="text-xs text-emerald-500 dark:text-emerald-400 mb-6">1 hour across 6 different days</p>
          <div className="flex justify-center items-end mb-3" style={{ height: barMaxH }}>
            <MotionDiv
              className="w-16 md:w-20 rounded-t-lg bg-emerald-400 dark:bg-emerald-500 relative"
              initial={{ height: 0 }}
              animate={{ height: (spacerScore / 100) * barMaxH }}
              transition={{ duration: 1, ease: 'easeOut' }}
            >
              {phase !== 'idle' && (
                <MotionDiv
                  className="absolute -top-7 left-0 right-0 text-center font-bold text-sm text-emerald-700 dark:text-emerald-300"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.8 }}
                >
                  {spacerScore}%
                </MotionDiv>
              )}
            </MotionDiv>
          </div>
          <div className="h-1 bg-emerald-200 dark:bg-emerald-800/40 rounded-full" />
        </div>
      </div>

      {/* Transition text */}
      {transitionText && (
        <MotionDiv
          key={transitionText}
          className="text-center text-lg font-serif font-semibold text-zinc-600 dark:text-zinc-300 mb-3"
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          {transitionText}
        </MotionDiv>
      )}

      {/* Phase label */}
      {phaseLabel && (
        <MotionDiv
          key={phaseLabel}
          className={`text-center text-sm font-bold mb-6 ${
            phase === 'day1'
              ? 'text-rose-600 dark:text-rose-400'
              : 'text-emerald-600 dark:text-emerald-400'
          }`}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          {phaseLabel}
        </MotionDiv>
      )}

      {/* Final insight panel */}
      {phase === 'done' && (
        <MotionDiv
          className="p-6 bg-sky-50 dark:bg-sky-950/20 rounded-xl border border-sky-200 dark:border-sky-800/40 text-center mb-6"
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <p className="text-sm text-sky-800 dark:text-sky-200 font-medium leading-relaxed">
            Same total study time. Radically different long-term results. Spacing works because each retrieval strengthens storage strength.
          </p>
        </MotionDiv>
      )}

      {/* Buttons */}
      <div className="flex justify-center">
        {phase === 'idle' && (
          <button
            onClick={runExperiment}
            className="px-6 py-3 bg-sky-500 hover:bg-sky-600 text-white font-bold text-sm rounded-xl transition-colors"
          >
            Run Experiment
          </button>
        )}
        {(phase === 'done') && (
          <button
            onClick={reset}
            className="px-5 py-2.5 text-sm font-bold rounded-xl text-zinc-500 dark:text-zinc-400 border border-zinc-200 dark:border-zinc-700 hover:border-zinc-400 transition-colors"
          >
            Reset
          </button>
        )}
      </div>
    </div>
  );
};

const OptimalScheduleCalculator = () => {
    const [ri, setRi] = useState<string>('1_week');

    const schedules = {
        '1_week': { gap: '1-2 Days', ratio: '20-40%', example: 'Study Mon, Review Weds, Test next Mon.' },
        '1_month': { gap: '1 Week', ratio: '~20%', example: 'Study Week 1, Review Week 2, Test Week 5.' },
        '3_months': { gap: '2 Weeks', ratio: '~15%', example: 'Mid-term review should be 2 weeks after intro.' },
        '6_months': { gap: '3 Weeks', ratio: '~10-12%', example: 'Long-term prep requires substantial spacing.' },
    };

    return(
         <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Optimal Schedule Calculator</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Based on the landmark Cepeda et al. (2008) research.</p>
             <div className="flex items-center justify-center gap-4">
                 <label className="font-bold">My test is in:</label>
                 <select value={ri} onChange={e => setRi(e.target.value)} className="p-2 bg-zinc-100 dark:bg-zinc-800 rounded-lg">
                    <option value="1_week">1 Week</option>
                    <option value="1_month">1 Month</option>
                    <option value="3_months">3 Months</option>
                    <option value="6_months">6 Months</option>
                 </select>
             </div>
             <div className="mt-6 p-6 bg-sky-50/50 border border-sky-200 rounded-xl text-center">
                <p className="text-sm text-sky-800">Optimal Review Gap (ISI):</p>
                <p className="font-bold text-2xl text-sky-600">{schedules[ri as keyof typeof schedules].gap}</p>
                <p className="text-xs text-sky-500 mt-4"><strong>Actionable Advice:</strong> {schedules[ri as keyof typeof schedules].example}</p>
             </div>
        </div>
    );
};


// --- MODULE COMPONENT ---
const MasteringSpacedRepetitionModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'forgetting-curve', title: 'The Forgetting Curve', eyebrow: '01 // The Default Setting', icon: Clock },
    { id: 'cramming-paradox', title: 'The Cramming Paradox', eyebrow: '02 // The Illusion of Speed', icon: BarChart2 },
    { id: 'desirable-difficulty', title: 'Desirable Difficulty', eyebrow: '03 // The Brain\'s Trigger', icon: Brain },
    { id: 'optimal-schedule', title: 'The Optimal Schedule', eyebrow: '04 // The Ridgeline Rule', icon: CalendarDays },
    { id: 'algorithmic-tools', title: 'Algorithmic Tools', eyebrow: '05 // The Autopilot', icon: RadioTower },
    { id: 'spacing-blueprint', title: 'Your Spacing Blueprint', eyebrow: '06 // The Action Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout moduleNumber="02" moduleTitle="Spaced Repetition" moduleSubtitle="The Forgetting Curve Protocol" moduleDescription={`Learn to defeat the "forgetting curve" by understanding the science of when and how often to review material for maximum long-term retention.`} theme={theme} sections={sections} onBack={onBack} progress={progress} onProgressUpdate={onProgressUpdate}>
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Forgetting Curve." eyebrow="Step 1" icon={Clock} theme={theme}>
              <p>Your brain is designed to forget. This isn't a flaw; it's a feature. To survive, your brain has to constantly discard useless information. The problem is, it defaults to forgetting almost everything. This process was first mapped in 1885 by Hermann Ebbinghaus, who discovered the <Highlight description="The mathematical certainty that, without active reinforcement, your memory for new information will decay exponentially over time." theme={theme}>Forgetting Curve</Highlight>.</p>
              <p>The curve is brutal. Without reviewing, you can lose over 50% of new information within an hour, and up to 80% within a day. This is why "cramming" is a catastrophic waste of time. To build lasting knowledge, you can't just put information *in* to your brain; you have to interrupt the process of it leaking *out*.</p>
              <ForgettingCurveVisualizer />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Cramming Paradox." eyebrow="Step 2" icon={BarChart2} theme={theme}>
                <p>If cramming is so bad, why does everyone do it? Because of a metacognitive trap called the <Highlight description="The common student experience where massed practice (cramming) leads to high immediate test performance but catastrophic long-term forgetting, reinforcing an ineffective study habit." theme={theme}>Cramming Paradox</Highlight>. For tests that happen immediately after studying (minutes or hours), cramming works. It keeps information active in your temporary working memory, creating a powerful "Illusion of Competence."</p>
                <RetentionCurveComparison />
                <p>This gives you a false sense of security. You score well on the immediate test, which "rewards" the cramming behaviour. But the information never gets consolidated into long-term memory. As the research shows, for the same amount of study time, <Highlight description="Also called Distributed Practice. The method of spreading study sessions out over time, which is proven to be vastly superior to cramming for long-term retention." theme={theme}>Spaced Practice</Highlight> can triple the durability of your memory.</p>
                <CrammingVsSpacingShowdown />
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="Desirable Difficulty." eyebrow="Step 3" icon={Brain} theme={theme}>
              <p>Why is spacing so much more powerful? Because it leverages the "struggle" of forgetting. This is the principle of <Highlight description="A learning task that requires a considerable but desirable amount of effort, thereby improving long-term performance. Spacing creates this by allowing some forgetting to occur between sessions." theme={theme}>Desirable Difficulty</Highlight>. When you space out your study, you allow your memory to fade slightly. When you come back to review it, your brain has to work harder to retrieve it.</p>
              <p>This effortful retrieval is a powerful biological signal. It tells your brain, "This information is important! I had to work hard to find it, so I should strengthen the pathway to make it easier next time." Cramming eliminates this difficulty; the information is always right there, so your brain sees no reason to invest the resources in building a strong, long-term memory trace.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Optimal Schedule." eyebrow="Step 4" icon={CalendarDays} theme={theme}>
              <p>So, what is the perfect gap between study sessions? There's no single magic number. Landmark research by Cepeda and Pashler found that the <Highlight description="The Inter-Study Interval (ISI) is the time gap between your study sessions." theme={theme}>Optimal Gap</Highlight> depends entirely on when you need to remember the information—the <Highlight description="The Retention Interval (RI) is the time between your last study session and the final test." theme={theme}>Retention Interval</Highlight>.</p>
              <p>Their "Ridgeline Rule" gives us a practical ratio: to maximize recall, your review gap should be roughly <strong>5-20%</strong> of the time until the test. For a test in a week, you need a short gap (1-2 days). For a test in 6 months, you need a much longer gap (e.g., 3 weeks). This is because a longer gap allows for more forgetting, creating a more "desirable difficulty" and triggering a stronger memory consolidation process for the long haul.</p>
              <OptimalScheduleCalculator />
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Algorithmic Tools." eyebrow="Step 5" icon={RadioTower} theme={theme}>
              <p>Managing the optimal schedule for thousands of facts across dozens of subjects is humanly impossible. This is where <Highlight description="Software (like Anki or SuperMemo) that uses algorithms based on the Forgetting Curve and Spacing Effect to automatically schedule reviews for individual pieces of information (like flashcards)." theme={theme}>Spaced Repetition Software (SRS)</Highlight> comes in. These tools are like a personal tutor for your memory.</p>
              <p>Using an app like Anki, you create digital flashcards. Each time you review a card, you tell the algorithm how difficult it was ("Again," "Hard," "Good," "Easy"). The algorithm then uses this feedback to predict when you'll be on the verge of forgetting that specific card and schedules it for review at that precise moment. It automates the entire process of optimal scheduling, ensuring you review the right thing at the right time.</p>
              <MicroCommitment theme={theme}>
                <p>Download Anki on your phone or computer. Don't worry about making cards yet. Just get the tool. This is the first step to building an automated, long-term memory system.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Your Spacing Blueprint." eyebrow="Step 6" icon={Wrench} theme={theme}>
              <p>You now have the science to defeat the Forgetting Curve. The timing of your study is as important as the content. This section provides a simple, actionable heuristic to put this into practice immediately, even without software.</p>
              <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
                <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Actionable Advice: The Heuristic Planner</h4>
                <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">For any test or exam, follow this simple rule-of-thumb schedule.</p>
                <div className="grid grid-cols-3 gap-4 text-center">
                    <div className="p-4 bg-zinc-50 dark:bg-zinc-800/50 rounded-xl">
                        <p className="font-bold">Day 1: Learn</p>
                        <p className="text-xs mt-1">First exposure to the material in class.</p>
                    </div>
                     <div className="p-4 bg-zinc-50 dark:bg-zinc-800/50 rounded-xl">
                        <p className="font-bold">Day 2-3: First Review</p>
                        <p className="text-xs mt-1">Review the material using Active Recall. This is the most critical review.</p>
                    </div>
                     <div className="p-4 bg-zinc-50 dark:bg-zinc-800/50 rounded-xl">
                        <p className="font-bold">Day 7 (or before test): Final Review</p>
                        <p className="text-xs mt-1">A final active recall session to consolidate the memory.</p>
                    </div>
                </div>
              </div>
              <MicroCommitment theme={theme}>
                <p>Pick one subject you have a test for in the next two weeks. Open your calendar and schedule two short review sessions for it between now and then, following the "Ridgeline Rule".</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default MasteringSpacedRepetitionModule;
