
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
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Leaving Cert Allostatic Load</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-2">Your brain's "wear and tear" builds over time and spikes during exam clusters.</p>
            <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 mb-6">This is why endurance training matters — not just knowledge.</p>

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
                The exam spikes aren't the real danger — it's the <span className="font-semibold text-orange-600 dark:text-orange-400">accumulated load underneath</span> that determines whether you crash or endure.
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
    { id: 'marathon-mindset', title: 'The Marathon Mindset', eyebrow: '01 // The Construct', icon: Brain },
    { id: 'sleep-banking', title: 'The Sleep Banking Strategy', eyebrow: '02 // The Non-Negotiable', icon: Moon },
    { id: 'fueling-engine', title: 'Fueling the Engine', eyebrow: '03 // Nutrition & Hydration', icon: Coffee },
    { id: 'in-exam-tools', title: 'The In-Exam Toolkit', eyebrow: '04 // Psychological Protocols', icon: HeartPulse },
    { id: 'training-plan', title: 'The Training Plan', eyebrow: '05 // Progressive Overload', icon: SlidersHorizontal },
    { id: 'recovery-protocol', title: 'The Recovery Protocol', eyebrow: '06 // Active Recovery', icon: Battery },
  ];

  return (
    <ModuleLayout
      moduleNumber="06"
      moduleTitle="Cognitive Endurance"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Marathon Mindset." eyebrow="Step 1" icon={Brain} theme={theme}>
              <p>The Leaving Cert isn't a sprint; it's a marathon. Success isn't just about knowing the material. It's about being able to access that knowledge at 4 PM on a Friday after a brutal week of exams. This is <Highlight description="The ability to sustain high-level mental performance, maintain focus, and resist distraction over extended periods of effortful thinking." theme={theme}>Cognitive Endurance</Highlight>.</p>
              <p>It's a biological skill, not a measure of willpower. Your brain is an organ that consumes 20% of your body's energy. Under the chronic stress of the Leaving Cert, your brain accumulates "wear and tear"—a concept scientists call <Highlight description="The cumulative physiological 'wear and tear' on the body and brain that results from chronic stress. High allostatic load impairs PFC function and emotional regulation." theme={theme}>Allostatic Load</Highlight>. Building cognitive endurance is about training your brain to handle this load.</p>
              <AllostaticLoadVisualizer />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Sleep Banking Strategy." eyebrow="Step 2" icon={Moon} theme={theme}>
              <p>Sleep is the single most powerful tool for building endurance. It's not rest; it's when your brain consolidates memory and clears out metabolic waste like <Highlight description="A metabolic byproduct that accumulates in the brain during waking hours. It binds to receptors and inhibits neural activity, creating the feeling of 'sleep pressure' or 'brain fog'." theme={theme}>adenosine</Highlight>.</p>
              <p>As a teenager, your brain has a natural "phase delay," meaning you want to sleep late and wake up late. The exam schedule fights this. Crucially, the final hours of your sleep are dense with <Highlight description="Rapid Eye Movement sleep is critical for consolidating procedural (skill) memory and for emotional regulation. It is disproportionately lost when you wake up early." theme={theme}>REM Sleep</Highlight>, which is vital for problem-solving skills and emotional stability. Cutting sleep short is like skipping the most important part of your training.</p>
              <SleepCycleArchitect />
              <MicroCommitment theme={theme}><p>For the next 10 days, wake up at the same time every single day—even weekends. This 'Fixed Wake-Up' protocol is the fastest way to reset your body clock and align your peak alertness with exam time.</p></MicroCommitment>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Fueling the Engine." eyebrow="Step 3" icon={Coffee} theme={theme}>
              <p>Your brain runs on glucose. An unstable fuel supply leads to unstable focus. High-sugar snacks cause a spike-and-crash cycle called <Highlight description="A state of low blood sugar that occurs 60-90 minutes after a high-sugar meal. It manifests as brain fog, irritability, and a loss of willpower, often coinciding with the middle of an exam." theme={theme}>Reactive Hypoglycemia</Highlight>, sabotaging your performance mid-exam.</p>
              <p>A cutting-edge hack from sports science is the <Highlight description="The finding that merely rinsing the mouth with a carbohydrate solution (without swallowing) can trick the brain into reducing the perception of fatigue and increasing neural drive." theme={theme}>Carbohydrate Mouth Rinse</Highlight>. Swishing a sports drink for 10 seconds activates reward centres in the brain, tricking it into thinking fuel is on the way. This can provide a vital mental boost in the final, gruelling hour of a long exam.</p>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The In-Exam Toolkit." eyebrow="Step 4" icon={HeartPulse} theme={theme}>
                <p>Anxiety is the enemy of endurance. It hijacks your brain, diverting blood flow from your rational <Highlight description="The 'CEO' of your brain, responsible for executive functions like working memory and impulse control. Its function is severely impaired by stress and fatigue." theme={theme}>Prefrontal Cortex (PFC)</Highlight> to your emotional <Highlight description="The brain's primitive fear centre. When it becomes overactive, it can 'hijack' the PFC, leading to a 'blanking out' phenomenon." theme={theme}>amygdala</Highlight>. You need tools to manage this in real-time.</p>
                <p>The fastest way to calm your nervous system is the <Highlight description="A specific breathing pattern (two sharp inhales through the nose, one long exhale through the mouth) that reinflates collapsed air sacs in the lungs, rapidly offloading carbon dioxide and reducing autonomic arousal." theme={theme}>Physiological Sigh</Highlight>. It takes less than 10 seconds. When you feel panic rising after a tough question, this is your emergency brake.</p>
                <p>For your eyes, use the <strong>20-20-20 Rule</strong>: every 20 minutes, look at something 20 feet away for 20 seconds. This relaxes your eye muscles and fights the visual fatigue that causes headaches and slows reading speed.</p>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="The Training Plan." eyebrow="Step 5" icon={SlidersHorizontal} theme={theme}>
              <p>You can't train for a marathon by only running sprints. Likewise, you can't prepare for a 3-hour exam by only studying in 20-minute bursts. You need to train your focus using <Highlight description="The core principle of all training. To improve, you must gradually increase the duration, intensity, or difficulty of the task over time." theme={theme}>Progressive Overload</Highlight>.</p>
              <p>This means structuring your study in phases. Start with short, focused bursts (like the Pomodoro Technique) to build your base. Then, gradually increase the duration of your focus blocks, training your brain to push past the "boredom barrier." In the final weeks, you should be doing full "Simulation Blocks"—studying under exam conditions for 90-120 minutes straight. This is not about learning more content; it's about building mental muscle.</p>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="The Recovery Protocol." eyebrow="Step 6" icon={Battery} theme={theme}>
              <p>Recovery is not the absence of work; it's an active process. Lying on the couch scrolling through TikTok is not rest. It's <Highlight description="Low-quality rest that involves high-dopamine, high-input cognitive load (e.g., social media). It fragments attention and prevents true neural recovery." theme={theme}>Passive Recovery</Highlight>, and it can actually increase your cognitive fatigue.</p>
              <p><Highlight description="High-quality rest that involves low cognitive load and specific physiological benefits. Examples include light exercise, time in nature, and NSDR." theme={theme}>Active Recovery</Highlight> strategies are far superior. A 20-minute walk clears stress hormones. Even better is <Highlight description="Non-Sleep Deep Rest (NSDR) is a guided meditation technique that brings the brain into a state of deep relaxation while maintaining consciousness. It rapidly replenishes dopamine and reduces cortisol." theme={theme}>NSDR</Highlight>, a 10-20 minute guided relaxation that acts as a "system reset" for your brain. In the crucial break between two exams on the same day, a 20-minute NSDR session is the single most effective way to restore your cognitive endurance for the afternoon paper.</p>
              <MicroCommitment theme={theme}><p>Find a 10-minute NSDR or Yoga Nidra script on YouTube. Try it once this week instead of scrolling on your phone during a study break.</p></MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default CognitiveEnduranceModule;
