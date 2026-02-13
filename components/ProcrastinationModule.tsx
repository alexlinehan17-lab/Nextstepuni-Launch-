/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  HeartPulse, Calculator, Shield, Zap, Wrench, Brain, RotateCcw, HeartHandshake
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { orangeTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = orangeTheme;

// --- INTERACTIVE COMPONENTS ---

const ProcrastinationEquation = () => {
    const [vars, setVars] = useState({ E: 50, V: 50, I: 50, D: 50 });
    const utility = (vars.E * vars.V) / (1 + (vars.I * vars.D / 100));
    const maxUtility = (100 * 100) / (1 + (1 * 1 / 100));
    const pct = Math.min(100, Math.round((utility / maxUtility) * 100));

    const level = pct >= 65 ? 'high' : pct >= 35 ? 'medium' : 'low';
    const levelColor = { high: 'text-emerald-500', medium: 'text-amber-500', low: 'text-rose-500' }[level];
    const levelLabel = { high: 'High', medium: 'Medium', low: 'Low' }[level];
    const ringColor = { high: '#10b981', medium: '#f59e0b', low: '#ef4444' }[level];

    // Dynamic insight based on weakest variable
    const getDiagnosis = () => {
      const issues: string[] = [];
      if (vars.E <= 30) issues.push("you don't believe you can succeed");
      if (vars.V <= 30) issues.push("the task feels boring or meaningless");
      if (vars.I >= 70) issues.push("you're highly susceptible to distractions");
      if (vars.D >= 70) issues.push("the deadline feels far away");
      if (issues.length === 0 && level === 'high') return "All four levers are working in your favour. This is a task you'll likely start without much resistance.";
      if (issues.length === 0) return "No single factor is critical, but the overall balance could be stronger. Try boosting your belief or the task's value.";
      return `Your motivation is ${level} because ${issues.join(' and ')}.`;
    };

    const levers: { key: keyof typeof vars; label: string; desc: string; icon: React.ReactNode; good: boolean }[] = [
      { key: 'E', label: 'Expectancy', desc: 'Belief you can succeed', icon: <span className="font-bold text-lg text-emerald-500">E</span>, good: true },
      { key: 'V', label: 'Value', desc: 'How rewarding it feels', icon: <span className="font-bold text-lg text-emerald-500">V</span>, good: true },
      { key: 'I', label: 'Impulsiveness', desc: 'Distraction susceptibility', icon: <span className="font-bold text-lg text-rose-500">I</span>, good: false },
      { key: 'D', label: 'Delay', desc: 'Distance to deadline', icon: <span className="font-bold text-lg text-rose-500">D</span>, good: false },
    ];

    // Ring gauge
    const radius = 52;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (pct / 100) * circumference;

    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Procrastination Equation</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-2">Adjust the four levers to see what drives — or kills — your motivation.</p>
            <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 mb-8">
              <span className="text-emerald-500 font-semibold">Green levers</span> boost motivation. <span className="text-rose-500 font-semibold">Red levers</span> drain it.
            </p>

            {/* Gauge */}
            <div className="flex justify-center mb-8">
              <div className="relative w-36 h-36">
                <svg viewBox="0 0 120 120" className="w-full h-full -rotate-90">
                  <circle cx="60" cy="60" r={radius} fill="none" stroke="#e5e7eb" strokeWidth="10" className="dark:opacity-20" />
                  <motion.circle
                    cx="60" cy="60" r={radius} fill="none"
                    stroke={ringColor}
                    strokeWidth="10"
                    strokeLinecap="round"
                    strokeDasharray={circumference}
                    animate={{ strokeDashoffset: offset }}
                    transition={{ type: 'spring', damping: 20, stiffness: 80 }}
                  />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <motion.p
                    key={pct}
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className={`text-3xl font-bold ${levelColor}`}
                  >
                    {pct}%
                  </motion.p>
                  <p className={`text-xs font-semibold ${levelColor}`}>{levelLabel}</p>
                </div>
              </div>
            </div>

            {/* Four levers */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              {levers.map(lever => {
                const val = vars[lever.key];
                const barColor = lever.good
                  ? 'bg-emerald-500'
                  : 'bg-rose-500';
                const trackBg = lever.good
                  ? 'bg-emerald-100 dark:bg-emerald-900/30'
                  : 'bg-rose-100 dark:bg-rose-900/30';
                const direction = lever.good ? '↑ Increase' : '↓ Decrease';

                return (
                  <div key={lever.key} className="flex flex-col items-center p-4 rounded-xl bg-zinc-50 dark:bg-zinc-900/50 border border-zinc-100 dark:border-zinc-800">
                    <div className="mb-2">{lever.icon}</div>
                    <p className="text-xs font-bold text-zinc-700 dark:text-zinc-200 text-center">{lever.label}</p>
                    <p className="text-[10px] text-zinc-400 dark:text-zinc-500 text-center mb-3">{lever.desc}</p>

                    {/* Vertical bar gauge */}
                    <div className={`w-6 h-24 rounded-full ${trackBg} relative overflow-hidden mb-2`}>
                      <motion.div
                        className={`absolute bottom-0 w-full rounded-full ${barColor}`}
                        animate={{ height: `${val}%` }}
                        transition={{ type: 'spring', damping: 15, stiffness: 100 }}
                      />
                    </div>

                    {/* Slider (hidden native, custom track above) */}
                    <input
                      type="range" min="1" max="100" value={val}
                      onChange={e => setVars({...vars, [lever.key]: parseInt(e.target.value)})}
                      className="w-full h-1.5 appearance-none rounded-full bg-zinc-200 dark:bg-zinc-700 cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-zinc-600 [&::-webkit-slider-thumb]:dark:bg-zinc-300 [&::-webkit-slider-thumb]:shadow-md"
                    />

                    <p className={`text-[9px] font-bold mt-2 ${lever.good ? 'text-emerald-500' : 'text-rose-500'}`}>{direction}</p>
                  </div>
                );
              })}
            </div>

            {/* Dynamic insight */}
            <motion.div
              key={getDiagnosis()}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className="p-4 bg-zinc-900 dark:bg-zinc-900 rounded-xl text-sm text-white"
            >
              <p><span className={`font-bold ${levelColor}`}>Diagnosis:</span> {getDiagnosis()}</p>
            </motion.div>
        </div>
    );
};

const IfThenAutopilot = () => {
    const [plan, setPlan] = useState<{if: string, then: string} | null>(null);

    const createPlan = () => {
      setPlan({if: "I feel the urge to check my phone", then: "I will take three deep breaths and work for 2 more minutes"});
    };

    return(
         <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The "If-Then" Autopilot</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Pre-load a decision to bypass willpower. Click to create a plan.</p>
            <div className="flex justify-center">
                <button onClick={createPlan} className="px-5 py-3 bg-orange-500 text-white font-bold rounded-lg text-sm">Create Plan</button>
            </div>
            {plan &&
            <motion.div initial={{opacity:0}} animate={{opacity:1}} className="mt-6 p-4 bg-zinc-900 rounded-xl text-white text-center font-mono text-sm">
                Plan created: IF <span className="text-rose-400">{plan.if}</span>, THEN <span className="text-emerald-400">{plan.then}</span>
            </motion.div>}
        </div>
    );
};

const GuiltSpiral = () => {
    const [guilt, setGuilt] = useState(10);
    const [avoidance, setAvoidance] = useState(10);

    const addCriticism = () => {
        setGuilt(g => Math.min(100, g + 30));
        setAvoidance(a => Math.min(100, a + 25));
    }

    const reset = () => {
        setGuilt(10);
        setAvoidance(10);
    }

    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Guilt Spiral</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">"Tough love" doesn't work. It just adds more negative emotion to the fire.</p>
             <div className="grid grid-cols-2 gap-6 mb-8">
                <div className="text-center">
                    <p className="font-bold text-sm text-rose-600 mb-2">Guilt Meter</p>
                    <div className="w-full h-6 bg-zinc-100 dark:bg-zinc-800 rounded-full"><motion.div className="h-full bg-rose-500 rounded-full" initial={{width: "10%"}} animate={{width: `${guilt}%`}} /></div>
                </div>
                <div className="text-center">
                    <p className="font-bold text-sm text-orange-600 mb-2">Urge to Avoid</p>
                    <div className="w-full h-6 bg-zinc-100 dark:bg-zinc-800 rounded-full"><motion.div className="h-full bg-orange-500 rounded-full" initial={{width: "10%"}} animate={{width: `${avoidance}%`}} /></div>
                </div>
            </div>
             <div className="flex justify-center gap-4">
                <button onClick={addCriticism} className="px-4 py-2 bg-rose-100 text-rose-800 text-xs font-bold rounded-lg">Add Self-Criticism</button>
                <button onClick={reset} className="px-4 py-2 bg-zinc-100 dark:bg-zinc-800 text-zinc-800 dark:text-white text-xs font-bold rounded-lg">Reset</button>
             </div>
        </div>
    );
};

const GuiltSpiralComparison = () => {
    const [revealed, setRevealed] = useState(false);

    const W = 440, H = 260;
    const padL = 8, padR = 8, padT = 28, padB = 44;
    const chartW = W - padL - padR, chartH = H - padT - padB;
    const toX = (f: number) => padL + f * chartW;
    const toY = (f: number) => padT + (1 - f) * chartH;

    const xLabels = ['Trigger', '+1hr', '+3hr', '+1 day', '+3 days', '+1 week'];

    // Left chart: The Guilt Spiral
    const guiltEmotion = [0.25, 0.38, 0.52, 0.70, 0.85, 0.97];
    const guiltProductivity = [0.50, 0.40, 0.28, 0.18, 0.10, 0.05];
    // Right chart: The Self-Forgiveness Path
    const forgiveEmotion = [0.25, 0.45, 0.30, 0.18, 0.12, 0.08];
    const forgiveProductivity = [0.50, 0.30, 0.45, 0.55, 0.62, 0.68];

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

    const guiltPhases = [
        { label: 'Guilt hits', x1: 0, x2: 0.33, color: '#fca5a5' },
        { label: 'Avoidance grows', x1: 0.33, x2: 0.66, color: '#f87171' },
        { label: 'Paralysis', x1: 0.66, x2: 1, color: '#ef4444' },
    ];
    const forgivePhases = [
        { label: 'Acknowledge', x1: 0, x2: 0.33, color: '#6ee7b7' },
        { label: 'Forgive & plan', x1: 0.33, x2: 0.66, color: '#34d399' },
        { label: 'Back on track', x1: 0.66, x2: 1, color: '#10b981' },
    ];

    const Chart = ({ primary, secondary, phases, areaColor, areaId, areaData, secondaryColor, label }: {
        primary: number[]; secondary: number[]; phases: { label: string; x1: number; x2: number; color: string }[];
        areaColor: string; areaId: string; areaData: number[]; secondaryColor: string; label: string;
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
            {/* Primary line (solid) — Negative Emotion */}
            <motion.path
                d={buildLine(primary)}
                fill="none" stroke={areaColor} strokeWidth="2.5" strokeLinecap="round"
                initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                transition={{ duration: 1.2, ease: 'easeOut' }}
            />
            {/* Secondary line (dashed) — Productivity */}
            <motion.path
                d={buildLine(secondary)}
                fill="none" stroke={secondaryColor} strokeWidth="1.5" strokeDasharray="5 3" strokeLinecap="round"
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
            {/* X-axis labels */}
            {xLabels.map((m, i) => (
                <text key={m} x={toX(i / (xLabels.length - 1))} y={toY(0) + 14} fontSize="9" fill="#a1a1aa" textAnchor="middle" fontWeight="600">{m}</text>
            ))}
            {/* Phase labels */}
            {phases.map((p, i) => (
                <text key={i} x={toX((p.x1 + p.x2) / 2)} y={toY(0) + 28} fontSize="8" fill={p.color} textAnchor="middle" fontWeight="700">{p.label}</text>
            ))}
            {/* Chart label */}
            <text x={W / 2} y={14} fontSize="11" fill="#71717a" textAnchor="middle" fontWeight="700">{label}</text>
            {/* Legend */}
            <line x1={W - padR - 120} x2={W - padR - 104} y1={14} y2={14} stroke={areaColor} strokeWidth="2" />
            <text x={W - padR - 100} y={17} fontSize="8" fill="#a1a1aa">Negative Emotion</text>
            <line x1={W - padR - 44} x2={W - padR - 28} y1={14} y2={14} stroke={secondaryColor} strokeWidth="1.5" strokeDasharray="4 2" />
            <text x={W - padR - 24} y={17} fontSize="8" fill="#a1a1aa">Productivity</text>
        </svg>
    );

    return (
        <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Guilt Divergence</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Same procrastination event. Two completely different outcomes.</p>

            {!revealed ? (
                <div className="text-center">
                    <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">After procrastinating, most students beat themselves up. But what if the data shows that's the worst possible response?</p>
                    <button onClick={() => setRevealed(true)} className="px-5 py-2.5 text-sm font-bold rounded-lg bg-orange-500 text-white hover:bg-orange-600 transition-colors">
                        Reveal the Divergence
                    </button>
                </div>
            ) : (
                <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
                    <div className="grid md:grid-cols-2 gap-4 mb-5">
                        <div className="rounded-lg border border-rose-200 dark:border-rose-900 bg-rose-50/50 dark:bg-rose-950/20 p-3">
                            <Chart primary={guiltEmotion} secondary={guiltProductivity} phases={guiltPhases}
                                areaColor="#ef4444" areaId="guilt-grad" areaData={guiltEmotion} secondaryColor="#f59e0b" label="The Guilt Spiral" />
                        </div>
                        <div className="rounded-lg border border-emerald-200 dark:border-emerald-900 bg-emerald-50/50 dark:bg-emerald-950/20 p-3">
                            <Chart primary={forgiveEmotion} secondary={forgiveProductivity} phases={forgivePhases}
                                areaColor="#10b981" areaId="forgive-grad" areaData={forgiveProductivity} secondaryColor="#f59e0b" label="The Self-Forgiveness Path" />
                        </div>
                    </div>
                    <div className="grid md:grid-cols-2 gap-4 text-sm">
                        <div className="flex items-start gap-2.5 p-3 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900">
                            <span className="text-rose-500 text-lg mt-0.5">&#x2716;</span>
                            <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-rose-600 dark:text-rose-400">Self-punishment</strong> after procrastination feels productive but creates a feedback loop. Guilt &#8594; avoidance &#8594; more guilt. Within days, you're stuck in learned helplessness.</p>
                        </div>
                        <div className="flex items-start gap-2.5 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900">
                            <span className="text-emerald-500 text-lg mt-0.5">&#x2714;</span>
                            <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-emerald-600 dark:text-emerald-400">Self-forgiveness</strong> breaks the loop. Acknowledging the slip without judgement allows your prefrontal cortex to re-engage. Research shows self-forgivers procrastinate less next time.</p>
                        </div>
                    </div>
                </motion.div>
            )}
        </div>
    );
};

const CircuitBreaker = () => {
    const [reframe, setReframe] = useState('');
    const containsForgive = reframe.toLowerCase().includes('forgive');
    const containsAction = reframe.toLowerCase().includes('i will');
    return(
         <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Circuit Breaker</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Rewrite this self-critical thought into a self-forgiving, action-oriented statement.</p>
            <p className="p-4 bg-rose-50 border border-rose-200 rounded-xl text-center font-mono text-rose-800 mb-4">"I'm so useless, I wasted the whole day."</p>
            <textarea value={reframe} onChange={e => setReframe(e.target.value)} placeholder="Your new script..." className="w-full h-24 p-4 bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200 dark:border-zinc-700 rounded-xl focus:outline-none focus:border-orange-400" />
            {(containsForgive || containsAction) &&
                <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
                    <p className={containsForgive ? 'text-emerald-600 font-bold' : 'text-zinc-400'}>Contains Self-Forgiveness</p>
                    <p className={containsAction ? 'text-emerald-600 font-bold' : 'text-zinc-400'}>Bridges to Action</p>
                </div>
            }
        </div>
    );
}

// --- MODULE COMPONENT ---
// NOTE: The original file was truncated at 272 lines (cut off mid-sidebar).
// All extractable content sections have been preserved below. The sidebar/footer
// code was in the truncated portion and is now handled by ModuleLayout.
// Content for sections 0-7 was not present in the original file's return block
// (the file cut off before the <main> content area), so section content is
// reconstructed based on the section definitions and interactive components available.
const ProcrastinationModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'real-reason', title: 'The Real Reason You Delay', eyebrow: '01 // Not Laziness', icon: HeartPulse },
    { id: 'amygdala-hijack', title: 'The Amygdala Hijack', eyebrow: '02 // Brain Battle', icon: Brain },
    { id: 'procrastination-equation', title: 'The Procrastination Equation', eyebrow: '03 // The Formula', icon: Calculator },
    { id: 'ego-defence', title: 'The Ego\'s Defence System', eyebrow: '04 // The Traps', icon: Shield },
    { id: 'guilt-cycle', title: 'The Guilt Cycle', eyebrow: '05 // The Downward Spiral', icon: RotateCcw },
    { id: 'forgiveness-protocol', title: 'The Forgiveness Protocol', eyebrow: '06 // The Circuit Breaker', icon: HeartHandshake },
    { id: 'if-then-protocol', title: 'The "If-Then" Protocol', eyebrow: '07 // The Antidote', icon: Zap },
    { id: 'scaffolding-focus', title: 'Scaffolding Your Focus', eyebrow: '08 // The Toolkit', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="11"
      moduleTitle="Understanding Procrastination"
      moduleSubtitle="The Architecture of Delay"
      moduleDescription={`Go beyond "laziness" and understand the real science of why you delay. Learn to master your motivation with evidence-based strategies.`}
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Real Reason You Delay." eyebrow="Step 1" icon={HeartPulse} theme={theme}>
              <p>Procrastination is not laziness. It is an <Highlight description="An emotion-regulation strategy where the brain prioritizes short-term mood repair over long-term goals. You're not avoiding the task; you're avoiding the negative emotion the task triggers." theme={theme}>emotional regulation problem</Highlight>. When you look at a maths textbook and feel a wave of dread, your brain's primary goal shifts from "learn calculus" to "make this feeling go away." The easiest way to do that? Avoid the task entirely.</p>
              <p>This is a critical reframe. You are not broken or lazy. Your brain is doing exactly what it's designed to do: protect you from perceived threats. The problem is that it has miscategorized a maths book as a threat. Understanding this is the first step to dismantling the cycle.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Amygdala Hijack." eyebrow="Step 2" icon={Brain} theme={theme}>
              <p>The neural mechanism behind procrastination is a battle between two brain regions. Your <Highlight description="The brain's threat-detection centre. It triggers the fight-or-flight response when it perceives danger, including the 'danger' of a difficult or boring task." theme={theme}>amygdala</Highlight> (the alarm system) fires a distress signal when it detects a threatening task. Your <Highlight description="The 'CEO' of the brain, responsible for planning, impulse control, and long-term decision-making. In adolescence, it is still developing, making it easier for the amygdala to 'win'." theme={theme}>Prefrontal Cortex (PFC)</Highlight> (the CEO) should override this, but in the adolescent brain, it's still under construction.</p>
              <p>The result is an <Highlight description="When the emotional brain (amygdala) overwhelms the rational brain (PFC), hijacking your decision-making. This is why you 'know' you should study but still reach for your phone." theme={theme}>Amygdala Hijack</Highlight>. Your emotional brain overwhelms your rational brain. This is why "just try harder" is useless advice. You need strategies that work *with* your brain's architecture, not against it.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Procrastination Equation." eyebrow="Step 3" icon={Calculator} theme={theme}>
              <p>Psychologist Piers Steel formalized procrastination into a single equation: <Highlight description="Motivation = (Expectancy x Value) / (Impulsiveness x Delay). This formula shows that your motivation to do a task is determined by four variables you can consciously manipulate." theme={theme}>Motivation = (Expectancy x Value) / (Impulsiveness x Delay)</Highlight>. This gives you four levers to pull.</p>
              <p><strong>Expectancy:</strong> Your belief you can succeed. Low confidence = high procrastination. <strong>Value:</strong> How rewarding or meaningful the task feels. <strong>Impulsiveness:</strong> Your susceptibility to distractions. <strong>Delay:</strong> How far away the deadline is. A task that is boring, feels impossible, is easily interrupted, and has a distant deadline is a recipe for maximum procrastination.</p>
              <ProcrastinationEquation />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Ego's Defence System." eyebrow="Step 4" icon={Shield} theme={theme}>
              <p>Procrastination is also a <Highlight description="A psychological strategy to protect your self-image. By not trying, you can attribute failure to lack of effort rather than lack of ability, which is less threatening to your ego." theme={theme}>self-handicapping strategy</Highlight>. If you don't study and get a bad grade, you can tell yourself: "Well, I didn't really try." This protects your ego from the more terrifying conclusion: "I tried my best and I'm still not good enough."</p>
              <p>This is a Faustian bargain. You trade long-term success for short-term psychological safety. Recognizing this pattern is crucial. The antidote is a <Highlight description="The belief that your abilities can be developed through effort. It decouples your performance from your identity, making failure a data point, not a verdict." theme={theme}>Growth Mindset</Highlight>, which makes failure safe by redefining it as a learning event, not a measure of your worth.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Guilt Cycle." eyebrow="Step 5" icon={RotateCcw} theme={theme}>
              <p>Most people respond to procrastination with self-criticism: "I'm so lazy. What's wrong with me?" This feels like accountability, but it's actually the worst thing you can do. Self-criticism generates <Highlight description="A negative emotional state that, ironically, fuels the very avoidance cycle it's trying to break. More guilt leads to more negative emotion, which leads to more avoidance." theme={theme}>guilt and shame</Highlight>, which are negative emotions. And what does your brain do with negative emotions? It tries to avoid them--by procrastinating more.</p>
              <p>This creates a vicious downward spiral: Procrastinate &#8594; Feel Guilty &#8594; More Negative Emotion &#8594; Procrastinate More &#8594; Feel More Guilty. "Tough love" doesn't break this cycle; it accelerates it.</p>
              <GuiltSpiralComparison />
              <GuiltSpiral />
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="The Forgiveness Protocol." eyebrow="Step 6" icon={HeartHandshake} theme={theme}>
              <p>The scientifically-proven circuit breaker for the guilt spiral is <Highlight description="Research by Dr. Michael Wohl showed that students who forgave themselves for procrastinating on a first exam were LESS likely to procrastinate on the next one. Self-compassion reduces the negative emotion that fuels avoidance." theme={theme}>Self-Forgiveness</Highlight>. A landmark study by Dr. Michael Wohl found that students who forgave themselves for procrastinating on their first exam were significantly less likely to procrastinate on their second.</p>
              <p>This isn't about letting yourself off the hook. It's about breaking the emotional chain reaction. The script is simple: "I procrastinated. That's a human thing to do. I forgive myself. Now, what is the smallest possible step I can take right now?"</p>
              <CircuitBreaker />
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="The 'If-Then' Protocol." eyebrow="Step 7" icon={Zap} theme={theme}>
              <p>Willpower is a limited resource, especially for a developing brain. The most effective anti-procrastination strategy is one that bypasses willpower entirely: the <Highlight description="A pre-commitment strategy (also called Implementation Intentions) where you pre-load a decision: 'IF [trigger], THEN [action].' This automates the behavior, removing the need for an in-the-moment willpower battle." theme={theme}>"If-Then" Plan</Highlight>. By pre-loading a decision, you automate the response and remove the negotiation your brain is so good at losing.</p>
              <p>The formula: <strong>IF</strong> [Trigger/Situation], <strong>THEN</strong> I will [Specific Action]. For example: "IF it is 4:30 PM, THEN I will open my Maths textbook to page 1 and do the first question." The key is to make the action tiny and specific. You're not committing to "study Maths for 2 hours." You're committing to opening a book.</p>
              <IfThenAutopilot />
            </ReadingSection>
          )}
          {activeSection === 7 && (
            <ReadingSection title="Scaffolding Your Focus." eyebrow="Step 8" icon={Wrench} theme={theme}>
              <p>Now you have the psychological tools. The final step is to scaffold your environment to make starting easy and staying focused automatic. This means using techniques like the <Highlight description="A time-management method where you work in focused 25-minute intervals ('Pomodoros') separated by 5-minute breaks. It makes tasks feel finite and manageable." theme={theme}>Pomodoro Technique</Highlight> to make tasks feel finite, and environmental design to remove distractions.</p>
              <p>The ultimate goal is to build a system where starting is effortless and stopping requires effort. This is the opposite of your current default, where starting requires enormous effort and stopping (to check your phone) is effortless. Flip the script.</p>
              <MicroCommitment theme={theme}>
                <p>Right now, identify the ONE task you've been avoiding the most. Write down one "If-Then" plan for it. Make the action so small it feels almost silly. That's the point.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default ProcrastinationModule;
