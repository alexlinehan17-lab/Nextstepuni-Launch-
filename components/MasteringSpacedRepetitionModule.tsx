import { BrandedForgettingView } from './learning/WideFeatures';

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { motion } from 'framer-motion';
import {
BarChart2,
Brain,
CalendarDays,
Clock,
RadioTower,Wrench
} from 'lucide-react';
import React,{ useEffect,useRef,useState } from 'react';
import { SPACED_REPETITION_REFERENCE_LIST } from '../data/references/spacedRepetition';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { skyTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { Highlight,MicroCommitment,ReadingSection,ToolJumpCard } from './ModuleShared';
import { MotionDiv } from './Motion';

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
      if (breakpoints[breakpoints.length - 1] !== totalDays) {
        addSegment(lastResetDay, totalDays, stability, retentionAtReset);
      }

      return points;
    };

    const baselinePoints = buildCurvePoints(0);
    const activePoints = buildCurvePoints(reviewCount);

    const finalRetention = Math.round(activePoints[activePoints.length - 1][1]);
    const baselineRetention = Math.round(baselinePoints[baselinePoints.length - 1][1]);

    return <BrandedForgettingView {...{baselinePoints,activePoints,reviewCount,setReviewCount,reviewSchedule,finalRetention,baselineRetention}} />;
};

const RetentionCurveComparison = () => {
    const [revealed, setRevealed] = useState(false);

    const W = 440, H = 260;
    const padL = 8, padR = 8, padT = 28, padB = 44;
    const chartW = W - padL - padR, chartH = H - padT - padB;
    const toX = (f: number) => padL + f * chartW;
    const toY = (f: number) => padT + (1 - f) * chartH;

    const days = ['Day 1', 'Day 3', 'Day 7', 'Day 14', 'Day 21', 'Day 30'];
    // The Crammer: single massive session, classic forgetting curve
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
        { label: 'Feels great', x1: 0, x2: 0.33, color: "var(--module-ink)" },
        { label: 'Fading fast', x1: 0.33, x2: 0.66, color: "var(--module-danger-text)" },
        { label: 'Gone', x1: 0.66, x2: 1, color: "var(--module-danger-text)" },
    ];
    const spacerPhases = [
        { label: 'Learn + review', x1: 0, x2: 0.33, color: "var(--module-success-text)" },
        { label: 'Spaces widen', x1: 0.33, x2: 0.66, color: "var(--module-success-text)" },
        { label: 'Locked in', x1: 0.66, x2: 1, color: "var(--module-success-text)" },
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
                <line key={v} x1={padL} x2={W - padR} y1={toY(v)} y2={toY(v)} stroke="var(--module-muted)" strokeOpacity="0.15" strokeDasharray="3 3" />
            ))}
            {/* Baseline */}
            <line x1={padL} x2={W - padR} y1={toY(0)} y2={toY(0)} stroke="var(--module-muted)" strokeOpacity="0.3" />
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
            <text x={padL + 2} y={toY(1.0) - 4} fontSize="9" fill="var(--module-surface)" fontWeight="600">High</text>
            <text x={padL + 2} y={toY(0) - 4} fontSize="9" fill="var(--module-surface)" fontWeight="600">Low</text>
            {/* Day labels */}
            {days.map((m, i) => (
                <text key={m} x={toX(i / (days.length - 1))} y={toY(0) + 14} fontSize="9" fill="var(--module-surface)" textAnchor="middle" fontWeight="600">{m}</text>
            ))}
            {/* Phase labels */}
            {phases.map((p, i) => (
                <text key={i} x={toX((p.x1 + p.x2) / 2)} y={toY(0) + 28} fontSize="8" fill={p.color} textAnchor="middle" fontWeight="700">{p.label}</text>
            ))}
            {/* Chart label */}
            <text x={W / 2} y={14} fontSize="11" fill="var(--module-muted)" textAnchor="middle" fontWeight="700">{label}</text>
            {/* Legend */}
            <line x1={W - padR - 100} x2={W - padR - 84} y1={14} y2={14} stroke={areaColor} strokeWidth="2" />
            <text x={W - padR - 80} y={17} fontSize="8" fill="var(--module-surface)">Retention</text>
            <line x1={W - padR - 44} x2={W - padR - 28} y1={14} y2={14} stroke={stressColor} strokeWidth="1.5" strokeDasharray="4 2" />
            <text x={W - padR - 24} y={17} fontSize="8" fill="var(--module-surface)">Stress</text>
        </svg>
    );

    return (
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">The Retention Crossover</h4>
            <p className="text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-6">Same material. Same student. Two different strategies.</p>

            {!revealed ? (
                <div className="text-center">
                    <p className="text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-4">Most students cram before exams. What does their retention actually look like over 30 days?</p>
                    <button onClick={() => setRevealed(true)} className="px-5 py-2.5 text-sm font-bold rounded-lg bg-[var(--module-surface)] text-[var(--module-ink)] hover:bg-[var(--module-surface)] transition-colors" data-wide-button="true">
                        Reveal the Crossover
                    </button>
                </div>
            ) : (
                <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
                    <div className="grid md:grid-cols-2 gap-4 mb-5">
                        <div className="rounded-lg border border-[var(--module-line)] dark:border-[var(--module-line)] bg-[var(--module-danger-soft)] dark:bg-[var(--module-danger-soft)] p-3">
                            <Chart effort={cramRetention} stress={cramStress} phases={cramPhases}
                                areaColor="var(--module-danger-text)" areaId="cram-grad" stressColor="var(--module-ink)" label="The Crammer" />
                        </div>
                        <div className="rounded-lg border border-[var(--module-line)] dark:border-[var(--module-line)] bg-[var(--module-success-soft)] dark:bg-[var(--module-success-soft)] p-3">
                            <Chart effort={spacerRetention} stress={spacerStress} phases={spacerPhases}
                                areaColor="var(--module-success-text)" areaId="spacer-grad" stressColor="var(--module-ink)" label="The Spacer" />
                        </div>
                    </div>
                    <div className="grid md:grid-cols-2 gap-4 text-sm">
                        <div className="flex items-start gap-2.5 p-3 rounded-lg bg-[var(--module-danger-soft)] dark:bg-[var(--module-danger-soft)] border border-[var(--module-line)] dark:border-[var(--module-line)]">
                            <span className="text-[var(--module-danger-text)] text-lg mt-0.5"></span>
                            <p className="text-[var(--module-ink)] dark:text-[var(--module-muted)]"><strong className="text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)]">Cramming</strong> gives an illusion of mastery. Retention peaks immediately then collapses. By exam day, you're relearning from scratch.</p>
                        </div>
                        <div className="flex items-start gap-2.5 p-3 rounded-lg bg-[var(--module-success-soft)] dark:bg-[var(--module-success-soft)] border border-[var(--module-line)] dark:border-[var(--module-line)]">
                            <span className="text-[var(--module-success-text)] text-lg mt-0.5"></span>
                            <p className="text-[var(--module-ink)] dark:text-[var(--module-muted)]"><strong className="text-[var(--module-success-text)] dark:text-[var(--module-success-text)]">Spacing</strong> feels slower, but each review makes the memory stronger. By exam day, you actually know the material properly.</p>
                        </div>
                    </div>
                </motion.div>
            )}
        </div>
    );
};

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

  return <div className="wr-skin" data-wide="CrammingVsSpacingShowdown"><div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">
        Cramming vs. Spacing Showdown
      </h4>
      <p className="text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-2">
        Two students study the same 6 hours total. Who remembers more?
      </p>
      <p className="text-center text-xs text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-8">
        Run the experiment and watch what happens over time.
      </p>

      {/* Two lanes */}
      <div className="grid grid-cols-2 gap-4 md:gap-6 mb-6">
        {/* Crammer lane */}
        <div className="p-4 md:p-6 bg-[var(--module-danger-soft)] dark:bg-[var(--module-danger-soft)] rounded-xl border border-[var(--module-line)] dark:border-[var(--module-line)] text-center">
          <p className="font-bold text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)] text-lg mb-1">Crammer</p>
          <p className="text-xs text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)] mb-6">6 hours the night before</p>
          <div className="flex justify-center items-end mb-3" style={{ height: barMaxH }}>
            <MotionDiv
              className="w-16 md:w-20 rounded-t-lg bg-[var(--module-danger)] dark:bg-[var(--module-danger)] relative"
              initial={{ height: 0 }}
              animate={{ height: (crammerScore / 100) * barMaxH }}
              transition={{ duration: 1, ease: 'easeOut' }}
            >
              {phase !== 'idle' && (
                <MotionDiv
                  className="absolute -top-7 left-0 right-0 text-center font-bold text-sm text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)]"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.8 }}
                >
                  {crammerScore}%
                </MotionDiv>
              )}
            </MotionDiv>
          </div>
          <div className="h-1 bg-[var(--module-danger-soft)] dark:bg-[var(--module-danger-soft)] rounded-full" />
        </div>

        {/* Spacer lane */}
        <div className="p-4 md:p-6 bg-[var(--module-success-soft)] dark:bg-[var(--module-success-soft)] rounded-xl border border-[var(--module-line)] dark:border-[var(--module-line)] text-center">
          <p className="font-bold text-[var(--module-success-text)] dark:text-[var(--module-success-text)] text-lg mb-1">Spacer</p>
          <p className="text-xs text-[var(--module-success-text)] dark:text-[var(--module-success-text)] mb-6">1 hour across 6 different days</p>
          <div className="flex justify-center items-end mb-3" style={{ height: barMaxH }}>
            <MotionDiv
              className="w-16 md:w-20 rounded-t-lg bg-[var(--module-success)] dark:bg-[var(--module-success)] relative"
              initial={{ height: 0 }}
              animate={{ height: (spacerScore / 100) * barMaxH }}
              transition={{ duration: 1, ease: 'easeOut' }}
            >
              {phase !== 'idle' && (
                <MotionDiv
                  className="absolute -top-7 left-0 right-0 text-center font-bold text-sm text-[var(--module-success-text)] dark:text-[var(--module-success-text)]"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.8 }}
                >
                  {spacerScore}%
                </MotionDiv>
              )}
            </MotionDiv>
          </div>
          <div className="h-1 bg-[var(--module-success-soft)] dark:bg-[var(--module-success-soft)] rounded-full" />
        </div>
      </div>

      {/* Transition text */}
      {transitionText && (
        <MotionDiv
          key={transitionText}
          className="text-center text-lg font-serif font-semibold text-[var(--module-ink)] dark:text-[var(--module-muted)] mb-3"
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
              ? "text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)]"
              : "text-[var(--module-success-text)] dark:text-[var(--module-success-text)]"
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
          className="p-6 bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-xl border border-[var(--module-line)] dark:border-[var(--module-line)] text-center mb-6"
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <p className="text-sm text-[var(--module-ink)] dark:text-[var(--module-ink)] font-medium leading-relaxed">
            Same total study time. Completely different long-term results. Spacing works because every time you make your brain dig up a memory, it gets easier to find next time.
          </p>
        </MotionDiv>
      )}

      {/* Buttons */}
      <div className="flex justify-center">
        {phase === 'idle' && (
          <button
            onClick={runExperiment}
            className="px-6 py-3 bg-[var(--module-surface)] hover:bg-[var(--module-surface)] text-[var(--module-ink)] font-bold text-sm rounded-xl transition-colors" data-wide-button="true"
          >
            Run Experiment
          </button>
        )}
        {(phase === 'done') && (
          <button
            onClick={reset}
            className="px-5 py-2.5 text-sm font-bold rounded-xl text-[var(--module-muted)] dark:text-[var(--module-muted)] border border-[var(--module-line)] dark:border-[var(--module-line)] hover:border-[var(--module-line)] transition-colors" data-wide-button="true"
          >
            Reset
          </button>
        )}
      </div>
    </div></div>;
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
         <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
             <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">Optimal Schedule Calculator</h4>
             <p className="text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-6">Pick when your test is, and we'll tell you the best time to review.</p>
             <div className="flex items-center justify-center gap-4">
                 <label className="font-bold">My test is in:</label>
                 <select value={ri} onChange={e => setRi(e.target.value)} className="p-2 bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-lg">
                    <option value="1_week">1 Week</option>
                    <option value="1_month">1 Month</option>
                    <option value="3_months">3 Months</option>
                    <option value="6_months">6 Months</option>
                 </select>
             </div>
             <div className="mt-6 p-6 rounded-xl text-center" style={{ backgroundColor: "var(--module-success-soft)", border: "2.5px solid var(--module-line)", boxShadow: 'none' }}>
                <p className="text-sm font-semibold" style={{ color: "var(--module-success-text)" }}>Best gap between study sessions:</p>
                <p className="font-bold text-2xl mt-1" style={{ color: "var(--module-success-text)" }}>{schedules[ri as keyof typeof schedules].gap}</p>
                <p className="text-xs mt-4" style={{ color: "var(--module-success-text)" }}><strong>Actionable Advice:</strong> {schedules[ri as keyof typeof schedules].example}</p>
             </div>
        </div>
    );
};

// --- MODULE COMPONENT ---
const MasteringSpacedRepetitionModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'forgetting-curve', title: 'The Forgetting Curve', eyebrow: '01 // The Default Setting', icon: Clock },
    { id: 'cramming-paradox', title: 'The Cramming Paradox', eyebrow: '02 // The Illusion of Speed', icon: BarChart2 },
    { id: 'desirable-difficulty', title: 'The Struggle Sweet Spot', eyebrow: '03 // The Brain\'s Trigger', icon: Brain },
    { id: 'optimal-schedule', title: 'The Best Review Schedule', eyebrow: '04 // When to Review', icon: CalendarDays },
    { id: 'algorithmic-tools', title: 'Apps That Do It For You', eyebrow: '05 // The Autopilot', icon: RadioTower },
    { id: 'spacing-blueprint', title: 'Your Spacing Blueprint', eyebrow: '06 // The Action Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout moduleNumber="02" moduleTitle="Spaced Repetition" moduleSubtitle="The Forgetting Curve Method" moduleDescription={`Stop forgetting what you study. Learn when and how often to review so the stuff you learn actually sticks for your big exams and beyond.`} theme={theme} sections={sections} onBack={onBack} progress={progress} onProgressUpdate={onProgressUpdate} finishButtonText="Space It Out" references={SPACED_REPETITION_REFERENCE_LIST}>
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Forgetting Curve." eyebrow="Step 1" icon={Clock} theme={theme}>
              {essentials ? (
                <p>Your brain is designed to forget. Without reviewing, memory of new material fades fast — a large share of it can be gone within a day or two.<Cite n={1} /> This is the <Highlight description="The natural pattern where your memory of something new fades quickly over time unless you go back and review it." theme={theme}>Forgetting Curve</Highlight>. To build lasting knowledge, you need to stop it leaking out.</p>
              ) : (
                <>
                  <p>Your brain is designed to forget. This isn't a flaw -- it's actually a feature. To survive, your brain has to constantly clear out stuff it doesn't think you need. The problem is, it defaults to forgetting almost everything. This is called the <Highlight description="The natural pattern where your memory of something new fades quickly over time unless you go back and review it." theme={theme}>Forgetting Curve</Highlight>.</p>
                  <p>The curve is brutal. Without reviewing, a large share of new information slips away within the first day or two — classic studies of the forgetting curve, since replicated, show memory dropping sharply soon after learning.<Cite n={1} /> This is why cramming is such a waste of time. To build lasting knowledge, you can't just put information <em>in</em> to your brain; you have to stop it from leaking <em>out</em>.</p>
                </>
              )}
              <ForgettingCurveVisualizer />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Cramming Paradox." eyebrow="Step 2" icon={BarChart2} theme={theme}>
              {essentials ? (
                <>
                  <p>Cramming tricks you. It's the <Highlight description="The trap where cramming makes you feel like you've nailed it right after studying, but the knowledge falls apart within days -- so you keep cramming because it 'worked' last time." theme={theme}>Cramming Paradox</Highlight>. You feel great right after, but the knowledge vanishes within days.</p>
                  <RetentionCurveComparison />
                  <p>For the same total study time, <Highlight description="Spreading your study sessions out over time instead of doing it all in one go. It feels slower, but it makes your memory way stronger and longer-lasting." theme={theme}>Spaced Practice</Highlight> can dramatically increase how long you remember something.<Cite n={2} /></p>
                  <CrammingVsSpacingShowdown />
                </>
              ) : (
                <>
                  <p>If cramming is so bad, why does everyone do it? Because it tricks you. This is what we call the <Highlight description="The trap where cramming makes you feel like you've nailed it right after studying, but the knowledge falls apart within days -- so you keep cramming because it 'worked' last time." theme={theme}>Cramming Paradox</Highlight>. For tests that happen straight after studying (minutes or hours), cramming actually works. It keeps information floating in your short-term memory, making you feel like you know it all.</p>
                  <RetentionCurveComparison />
                  <p>This gives you a false sense of security. You score well on the immediate test, which "rewards" the cramming behaviour. But the information never actually makes it into your long-term memory. Here's the thing: for the same amount of study time, <Highlight description="Spreading your study sessions out over time instead of doing it all in one go. It feels slower, but it makes your memory way stronger and longer-lasting." theme={theme}>Spaced Practice</Highlight> can dramatically improve how long you actually remember something.<Cite n={2} /></p>
                  <CrammingVsSpacingShowdown />
                </>
              )}
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The Struggle Sweet Spot." eyebrow="Step 3" icon={Brain} theme={theme}>
              {essentials ? (
                <p>Spacing works because of <Highlight description="When studying feels a bit harder -- like when you've half-forgotten something and have to really think to recall it -- that extra effort actually makes the memory stick much better." theme={theme}>Desirable Difficulty</Highlight>.<Cite n={3} /> You let yourself half-forget. Then when you review, your brain works harder to dig it up. That effort tells your brain to make the memory stronger.</p>
              ) : (
                <>
                  <p>Why is spacing so much more powerful? Because it uses the "struggle" of forgetting to your advantage. This is the idea behind <Highlight description="When studying feels a bit harder -- like when you've half-forgotten something and have to really think to recall it -- that extra effort actually makes the memory stick much better." theme={theme}>Desirable Difficulty</Highlight>.<Cite n={3} /> When you space out your study, you let your memory fade a little on purpose. When you come back to review it, your brain has to work harder to dig it up.</p>
                  <p>That extra effort is a powerful signal. It tells your brain, "This information is important! I had to work hard to find it, so I should make the pathway stronger for next time." Cramming skips this difficulty entirely -- the information is always right there in front of you, so your brain sees no reason to lock it in for the long term.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Best Review Schedule." eyebrow="Step 4" icon={CalendarDays} theme={theme}>
              {essentials ? (
                <p>Your <Highlight description="The gap between your study sessions. The right gap depends on how far away your test is." theme={theme}>review gap</Highlight> should be a fraction of the time until your <Highlight description="The time between your last study session and the actual test or exam." theme={theme}>test date</Highlight> — a bigger share when the test is close, a smaller share when it is far off.<Cite n={4} /> Test in a week? Review every 1-2 days. Big exam in 6 months? Review every 3 weeks.</p>
              ) : (
                <>
                  <p>So, what's the perfect gap between study sessions? There's no single magic number. The <Highlight description="The gap between your study sessions. The right gap depends on how far away your test is." theme={theme}>best review gap</Highlight> depends entirely on when you need to remember the information -- basically, how far away your <Highlight description="The time between your last study session and the actual test or exam." theme={theme}>test date</Highlight> is.</p>
                  <p>Here's a handy rule of thumb: set your review gap as a fraction of the time until the test — around <strong>20-40%</strong> of the interval when the test is about a week away, shrinking to roughly <strong>5-10%</strong> when it's a year off.<Cite n={4} /> So for a test in a week, a short gap (1-2 days); for a big exam in 6 months, a much longer gap (around 3 weeks). The gap still grows in absolute terms as the test moves further away -- you just don't scale it up in direct proportion. A longer gap lets you forget a little more, which makes your brain work harder when you review -- and that extra effort is exactly what locks it in for the long term.</p>
                </>
              )}
              <OptimalScheduleCalculator />
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Apps That Do It For You." eyebrow="Step 5" icon={RadioTower} theme={theme}>
              {essentials ? (
                <p>Use <Highlight description="Apps like Anki (free on computer and Android; the iPhone app is paid — the AnkiWeb site is free in a browser) that automatically figure out when you're about to forget something and remind you to review it at the right time." theme={theme}>Spaced Repetition Apps</Highlight> like Anki. You make flashcards. The app tracks when you're about to forget each one. It shows you the right card at the right time. No guesswork.</p>
              ) : (
                <>
                  <p>Keeping track of the perfect review schedule for thousands of facts across all your subjects is basically impossible to do by hand. That's where <Highlight description="Apps like Anki (free on computer and Android; the iPhone app is paid — the AnkiWeb site is free in a browser) that automatically figure out when you're about to forget something and remind you to review it at the right time." theme={theme}>Spaced Repetition Apps</Highlight> come in. Think of them as a personal tutor for your memory.</p>
                  <p>Using an app like Anki, you create digital flashcards. Each time you review a card, you tell the app how hard it was ("Again," "Hard," "Good," "Easy"). The app then uses your answers to figure out when you're about to forget that card and puts it in front of you at just the right moment. It takes all the guesswork out of scheduling -- you just show up and review whatever the app tells you to.</p>
                </>
              )}
              <MicroCommitment theme={theme}>
                <p>Get Anki — it’s free on computer and Android; on iPhone the official app is paid, so use ankiweb.net free in your browser instead. Don't worry about making cards yet. Just get the tool. This is the first step to building an automated, long-term memory system.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Your Spacing Blueprint." eyebrow="Step 6" icon={Wrench} theme={theme}>
              {essentials ? (
                <p>When you study matters as much as what you study. Follow a simple plan: learn on Day 1, test yourself on Day 2-3, final review on Day 7.</p>
              ) : (
                <p>You now know how to beat the Forgetting Curve. When you study matters just as much as what you study. Here's a simple plan you can start using right now, even without any apps.</p>
              )}
              <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
                <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">Your Simple Review Plan</h4>
                <p className="text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-8">For any test or exam, follow this simple schedule.</p>
                <div className="grid grid-cols-3 gap-4 text-center">
                    <div className="p-4 rounded-xl" style={{ backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none' }}>
                        <p className="font-bold text-[var(--module-ink)]">Day 1: Learn</p>
                        <p className="text-xs mt-1 text-[var(--module-ink)]">First exposure to the material in class.</p>
                    </div>
                     <div className="p-4 rounded-xl" style={{ backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none' }}>
                        <p className="font-bold text-[var(--module-ink)]">Day 2-3: First Review</p>
                        <p className="text-xs mt-1 text-[var(--module-ink)]">Review by testing yourself (don't just re-read). This is the most important review.</p>
                    </div>
                     <div className="p-4 rounded-xl" style={{ backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none' }}>
                        <p className="font-bold text-[var(--module-ink)]">Day 7 (or before test): Final Review</p>
                        <p className="text-xs mt-1 text-[var(--module-ink)]">One last round of testing yourself to lock it in.</p>
                    </div>
                </div>
              </div>
              <MicroCommitment theme={theme}>
                <p>Pick one subject you have a test for in the next two weeks. Open your calendar and schedule two short review sessions for it between now and then, using the rule of thumb above.</p>
              </MicroCommitment>
              <ToolJumpCard
                toolId="planner"
                title="Build your spacing schedule in the Planner"
                description="Drop your subjects in and the Planner lays out the Day 1 / Day 2-3 / Day 7 reviews for you, on the dates that match your timetable."
                ctaLabel="Open the Planner"
              />
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default MasteringSpacedRepetitionModule;
