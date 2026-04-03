/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { Cpu, Zap, Shield, Moon, Utensils, ClipboardList, Flag, Brain } from 'lucide-react';
import { ModuleProgress } from '../types';
import { skyTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = skyTheme;

// --- INTERACTIVE COMPONENTS ---
const CognitionShiftVisualizer = () => {
    const [stress, setStress] = useState(20);

    // Yerkes-Dodson: performance peaks around 45, collapses after 70
    const perf = stress <= 45
        ? 0.15 + (stress / 45) * 0.85
        : Math.max(0.05, 1.0 - ((stress - 45) / 55) * 1.1);
    const pfcPct = Math.max(5, Math.round((1 - stress / 100) * 100));
    const amygPct = Math.max(5, Math.round((stress / 100) * 100));

    const stages = [
        { min: 0, max: 15, label: 'Calm', desc: 'Too relaxed. You\'re chilled out but not switched on — not enough energy to perform.', color: '#60a5fa' },
        { min: 15, max: 35, label: 'Focused', desc: 'A bit of stress is sharpening you up. Your thinking brain is fully in charge and your memory is working well.', color: '#34d399' },
        { min: 35, max: 55, label: 'Optimal', desc: 'The sweet spot. Just the right amount of adrenaline — you\'re alert, fast, and accurate.', color: '#10b981' },
        { min: 55, max: 72, label: 'Anxious', desc: 'Stress is tipping over. Your focus is narrowing. You re-read questions without taking them in.', color: '#f59e0b' },
        { min: 72, max: 88, label: 'Panic', desc: 'Your alarm brain is taking over. Heart racing, shallow breathing. Your thinking brain is losing control.', color: '#f97316' },
        { min: 88, max: 101, label: 'Going Blank', desc: 'Full shutdown. You stare at the page and nothing comes. Your thinking brain has gone offline.', color: '#ef4444' },
    ];
    const stage = stages.find(s => stress >= s.min && stress < s.max) || stages[stages.length - 1];

    // SVG curve
    const W = 420, H = 200;
    const padL = 36, padR = 24, padT = 28, padB = 36;
    const chartW = W - padL - padR, chartH = H - padT - padB;
    const toX = (f: number) => padL + f * chartW;
    const toY = (f: number) => padT + (1 - f) * chartH;

    // Build Yerkes-Dodson curve
    const curvePoints: { x: number; y: number }[] = [];
    for (let i = 0; i <= 100; i += 2) {
        const p = i <= 45
            ? 0.15 + (i / 45) * 0.85
            : Math.max(0.05, 1.0 - ((i - 45) / 55) * 1.1);
        curvePoints.push({ x: toX(i / 100), y: toY(p) });
    }
    let curvePath = `M ${curvePoints[0].x} ${curvePoints[0].y}`;
    for (let i = 1; i < curvePoints.length; i++) {
        const prev = curvePoints[i - 1];
        const cur = curvePoints[i];
        const cx1 = prev.x + (cur.x - prev.x) * 0.4;
        const cx2 = prev.x + (cur.x - prev.x) * 0.6;
        curvePath += ` C ${cx1} ${prev.y}, ${cx2} ${cur.y}, ${cur.x} ${cur.y}`;
    }
    // Area path
    const areaPath = curvePath + ` L ${curvePoints[curvePoints.length - 1].x} ${toY(0)} L ${curvePoints[0].x} ${toY(0)} Z`;

    const dotX = toX(stress / 100);
    const dotY = toY(perf);

    return (
        <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Hot vs. Cold Cognition</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-5">Drag the slider to see how stress affects your brain during an exam.</p>

            {/* SVG Curve */}
            <svg viewBox={`0 0 ${W} ${H}`} className="w-full mb-1">
                <defs>
                    <linearGradient id="perf-grad" x1="0" y1="0" x2="1" y2="0">
                        <stop offset="0%" stopColor="#60a5fa" stopOpacity="0.15" />
                        <stop offset="35%" stopColor="#10b981" stopOpacity="0.2" />
                        <stop offset="55%" stopColor="#f59e0b" stopOpacity="0.15" />
                        <stop offset="100%" stopColor="#ef4444" stopOpacity="0.1" />
                    </linearGradient>
                    <linearGradient id="perf-stroke" x1="0" y1="0" x2="1" y2="0">
                        <stop offset="0%" stopColor="#60a5fa" />
                        <stop offset="35%" stopColor="#10b981" />
                        <stop offset="55%" stopColor="#f59e0b" />
                        <stop offset="100%" stopColor="#ef4444" />
                    </linearGradient>
                </defs>
                {/* Grid */}
                {[0.25, 0.5, 0.75, 1.0].map(v => (
                    <line key={v} x1={padL} x2={W - padR} y1={toY(v)} y2={toY(v)} stroke="#a1a1aa" strokeOpacity="0.12" strokeDasharray="3 3" />
                ))}
                <line x1={padL} x2={W - padR} y1={toY(0)} y2={toY(0)} stroke="#a1a1aa" strokeOpacity="0.25" />
                {/* Optimal zone band */}
                <rect x={toX(0.30)} y={padT} width={toX(0.60) - toX(0.30)} height={chartH} fill="#10b981" fillOpacity="0.06" rx="4" />
                <text x={(toX(0.30) + toX(0.60)) / 2} y={toY(0) - 4} fontSize="7" fill="#10b981" textAnchor="middle" fontWeight="700" opacity="0.6">OPTIMAL ZONE</text>
                {/* Area fill */}
                <path d={areaPath} fill="url(#perf-grad)" />
                {/* Curve line */}
                <path d={curvePath} fill="none" stroke="url(#perf-stroke)" strokeWidth="2.5" strokeLinecap="round" />
                {/* Vertical tracking line */}
                <line x1={dotX} x2={dotX} y1={dotY} y2={toY(0)} stroke={stage.color} strokeWidth="1" strokeDasharray="4 3" opacity="0.5" />
                {/* Dot */}
                <circle cx={dotX} cy={dotY} r="5" fill={stage.color} stroke="#fff" strokeWidth="2" />
                <circle cx={dotX} cy={dotY} r="9" fill={stage.color} fillOpacity="0.15" />
                {/* Y-axis */}
                <text x={padL - 4} y={toY(1.0) + 3} fontSize="8" fill="#a1a1aa" textAnchor="end" fontWeight="600">High</text>
                <text x={padL - 4} y={toY(0) + 3} fontSize="8" fill="#a1a1aa" textAnchor="end" fontWeight="600">Low</text>
                <text x={padL - 4} y={toY(0.5) + 3} fontSize="7" fill="#a1a1aa" textAnchor="end">Med</text>
                {/* X-axis labels */}
                <text x={toX(0)} y={toY(0) + 14} fontSize="8" fill="#a1a1aa" textAnchor="middle" fontWeight="600">Low</text>
                <text x={toX(0.5)} y={toY(0) + 14} fontSize="8" fill="#a1a1aa" textAnchor="middle" fontWeight="600">Moderate</text>
                <text x={toX(1)} y={toY(0) + 14} fontSize="8" fill="#a1a1aa" textAnchor="middle" fontWeight="600">Extreme</text>
                {/* Axis titles */}
                <text x={padL - 4} y={toY(0.5) - 14} fontSize="8" fill="#71717a" textAnchor="end" fontWeight="700" transform={`rotate(-90, ${padL - 16}, ${toY(0.5)})`}>Performance</text>
                <text x={toX(0.5)} y={toY(0) + 28} fontSize="8" fill="#71717a" textAnchor="middle" fontWeight="700">Stress Level</text>
            </svg>

            {/* Slider */}
            <div className="px-2">
                <input type="range" min="0" max="100" value={stress} onChange={e => setStress(Number(e.target.value))}
                    className="w-full h-2 rounded-full appearance-none cursor-pointer"
                    style={{ accentColor: stage.color, background: `linear-gradient(to right, #60a5fa, #10b981 35%, #f59e0b 55%, #ef4444)` }} />
            </div>

            {/* Stage label + description */}
            <div className="mt-5 flex items-start gap-4 p-4 rounded-xl border transition-colors" style={{ borderColor: stage.color + '40', backgroundColor: stage.color + '0a' }}>
                <div className="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center" style={{ backgroundColor: stage.color + '20' }}>
                    {stress < 55 ? <Brain size={20} style={{ color: stage.color }} /> : <Zap size={20} style={{ color: stage.color }} />}
                </div>
                <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                        <span className="font-bold text-sm" style={{ color: stage.color }}>{stage.label}</span>
                        <span className="text-xs text-zinc-400">Stress: {stress}%</span>
                    </div>
                    <p className="text-sm text-zinc-600 dark:text-zinc-300">{stage.desc}</p>
                </div>
            </div>

            {/* PFC vs Amygdala bars */}
            <div className="grid grid-cols-2 gap-3 mt-4">
                <div className="p-3 rounded-lg bg-zinc-50 dark:bg-zinc-700/50">
                    <div className="flex items-center justify-between mb-1.5">
                        <span className="text-xs font-bold text-blue-600 dark:text-blue-400 flex items-center gap-1"><Brain size={12} /> Thinking Brain</span>
                        <span className="text-xs font-bold text-zinc-500">{pfcPct}%</span>
                    </div>
                    <div className="w-full h-2 bg-zinc-200 dark:bg-zinc-600 rounded-full">
                        <motion.div className="h-full bg-blue-500 rounded-full" animate={{ width: `${pfcPct}%` }} transition={{ type: 'spring', stiffness: 120, damping: 20 }} />
                    </div>
                    <p className="text-xs text-zinc-400 mt-1">Logic, planning, working memory</p>
                </div>
                <div className="p-3 rounded-lg bg-zinc-50 dark:bg-zinc-700/50">
                    <div className="flex items-center justify-between mb-1.5">
                        <span className="text-xs font-bold text-rose-600 dark:text-rose-400 flex items-center gap-1"><Zap size={12} /> Alarm Brain</span>
                        <span className="text-xs font-bold text-zinc-500">{amygPct}%</span>
                    </div>
                    <div className="w-full h-2 bg-zinc-200 dark:bg-zinc-600 rounded-full">
                        <motion.div className="h-full bg-rose-500 rounded-full" animate={{ width: `${amygPct}%` }} transition={{ type: 'spring', stiffness: 120, damping: 20 }} />
                    </div>
                    <p className="text-xs text-zinc-400 mt-1">Fear, threat detection, survival mode</p>
                </div>
            </div>
        </div>
    );
};

const PhysiologicalSighGuide = () => {
    const [running, setRunning] = useState(false);
    const [cycle, setCycle] = useState(0);
    const [phase, setPhase] = useState<'idle' | 'inhale1' | 'inhale2' | 'exhale' | 'done'>('idle');
    const [progress, setProgress] = useState(0);
    const totalCycles = 3;

    // Phase durations in ms
    const durations = { inhale1: 1800, inhale2: 1000, exhale: 4000 };

    React.useEffect(() => {
        if (!running || phase === 'idle' || phase === 'done') return;
        const dur = durations[phase];
        const interval = 30;
        let elapsed = 0;
        const timer = setInterval(() => {
            elapsed += interval;
            setProgress(Math.min(1, elapsed / dur));
            if (elapsed >= dur) {
                clearInterval(timer);
                setProgress(0);
                if (phase === 'inhale1') setPhase('inhale2');
                else if (phase === 'inhale2') setPhase('exhale');
                else if (phase === 'exhale') {
                    if (cycle + 1 >= totalCycles) { setPhase('done'); setRunning(false); }
                    else { setCycle(c => c + 1); setPhase('inhale1'); }
                }
            }
        }, interval);
        return () => clearInterval(timer);
    }, [running, phase, cycle]);

    const start = () => { setCycle(0); setPhase('inhale1'); setProgress(0); setRunning(true); };
    const reset = () => { setRunning(false); setPhase('idle'); setCycle(0); setProgress(0); };

    const phaseConfig = {
        idle: { label: '', instruction: '', color: '#a1a1aa', scale: 0.45 },
        inhale1: { label: 'Inhale', instruction: 'Breathe in through your nose', color: '#0ea5e9', scale: 0.45 + progress * 0.35 },
        inhale2: { label: 'Inhale', instruction: 'Quick second sip of air', color: '#0ea5e9', scale: 0.8 + progress * 0.2 },
        exhale: { label: 'Exhale', instruction: 'Slow exhale through your mouth', color: '#6366f1', scale: 1.0 - progress * 0.55 },
        done: { label: '', instruction: '', color: '#10b981', scale: 0.45 },
    };
    const cfg = phaseConfig[phase];

    // SVG breathing circle
    const cx = 100, cy = 100, maxR = 80;
    const r = maxR * cfg.scale;
    const circumference = 2 * Math.PI * 44;

    return (
        <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Physiological Sigh</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Your emergency brake for acute panic. Two quick inhales, one long exhale.</p>

            <div className="flex flex-col items-center">
                {/* Breathing circle */}
                <div className="relative w-48 h-48 mb-4">
                    <svg viewBox="0 0 200 200" className="w-full h-full">
                        {/* Outer ring track */}
                        <circle cx={cx} cy={cy} r="44" fill="none" stroke="#e5e7eb" strokeWidth="3" className="dark:opacity-20" />
                        {/* Progress ring */}
                        {phase !== 'idle' && phase !== 'done' && (
                            <circle cx={cx} cy={cy} r="44" fill="none" stroke={cfg.color} strokeWidth="3" strokeLinecap="round"
                                strokeDasharray={circumference} strokeDashoffset={circumference * (1 - progress)}
                                transform={`rotate(-90 ${cx} ${cy})`} />
                        )}
                        {phase === 'done' && (
                            <circle cx={cx} cy={cy} r="44" fill="none" stroke="#10b981" strokeWidth="3" strokeDasharray={circumference} strokeDashoffset={0}
                                transform={`rotate(-90 ${cx} ${cy})`} />
                        )}
                        {/* Breathing bubble */}
                        <motion.circle cx={cx} cy={cy} fill={cfg.color} fillOpacity="0.12"
                            animate={{ r }} transition={{ type: 'tween', ease: 'easeInOut', duration: 0.15 }} />
                        <motion.circle cx={cx} cy={cy} fill={cfg.color} fillOpacity="0.08"
                            animate={{ r: r + 8 }} transition={{ type: 'tween', ease: 'easeInOut', duration: 0.15 }} />
                    </svg>
                    {/* Center text */}
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                        {phase === 'idle' && (
                            <button onClick={start} className="px-5 py-2.5 bg-sky-500 hover:bg-sky-600 text-white font-bold text-sm rounded-lg transition-colors">Begin</button>
                        )}
                        {phase === 'done' && (
                            <div className="text-center">
                                <p className="text-sm font-bold text-emerald-600 dark:text-emerald-400 mb-2">Complete</p>
                                <button onClick={reset} className="px-4 py-1.5 bg-zinc-200 dark:bg-zinc-600 text-zinc-700 dark:text-zinc-200 font-bold text-xs rounded-lg">Again</button>
                            </div>
                        )}
                        {phase !== 'idle' && phase !== 'done' && (
                            <div className="text-center">
                                <p className="text-lg font-bold" style={{ color: cfg.color }}>{cfg.label}</p>
                                <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5 max-w-[120px]">{cfg.instruction}</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Cycle indicators */}
                <div className="flex items-center gap-2 mb-3">
                    {Array.from({ length: totalCycles }).map((_, i) => (
                        <div key={i} className={`w-2.5 h-2.5 rounded-full transition-colors ${
                            i < cycle || phase === 'done' ? 'bg-emerald-500' : i === cycle && running ? 'bg-sky-500' : 'bg-zinc-200 dark:bg-zinc-600'
                        }`} />
                    ))}
                    <span className="text-xs text-zinc-400 ml-1">{phase === 'done' ? '3/3' : running ? `${cycle + 1}/3` : '0/3'}</span>
                </div>

                {/* Phase timeline */}
                {running && phase !== 'done' && (
                    <div className="flex items-center gap-1.5 text-xs font-bold">
                        <span className={phase === 'inhale1' ? 'text-sky-500' : phase === 'inhale2' || phase === 'exhale' ? 'text-emerald-500' : 'text-zinc-300 dark:text-zinc-600'}>Inhale 1</span>
                        <span className="text-zinc-300 dark:text-zinc-600">&rarr;</span>
                        <span className={phase === 'inhale2' ? 'text-sky-500' : phase === 'exhale' ? 'text-emerald-500' : 'text-zinc-300 dark:text-zinc-600'}>Inhale 2</span>
                        <span className="text-zinc-300 dark:text-zinc-600">&rarr;</span>
                        <span className={phase === 'exhale' ? 'text-indigo-500' : 'text-zinc-300 dark:text-zinc-600'}>Exhale</span>
                    </div>
                )}

                {/* Technique summary */}
                <div className="mt-5 grid grid-cols-3 gap-3 w-full max-w-sm text-center">
                    <div className="p-2.5 rounded-lg bg-sky-50 dark:bg-sky-900/20 border border-sky-200 dark:border-sky-800">
                        <p className="text-xs font-bold text-sky-600 dark:text-sky-400">Inhale 1</p>
                        <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">Sharp nose breath</p>
                    </div>
                    <div className="p-2.5 rounded-lg bg-sky-50 dark:bg-sky-900/20 border border-sky-200 dark:border-sky-800">
                        <p className="text-xs font-bold text-sky-600 dark:text-sky-400">Inhale 2</p>
                        <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">Quick sip on top</p>
                    </div>
                    <div className="p-2.5 rounded-lg bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-200 dark:border-indigo-800">
                        <p className="text-xs font-bold text-indigo-600 dark:text-indigo-400">Exhale</p>
                        <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">Long slow mouth</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

type CrisisResponse = {
    text: string;
    quality: 'bad' | 'ok' | 'good';
    consequence: string;
    explanation: string;
};

type CrisisScenario = {
    situation: string;
    responses: CrisisResponse[];
};

const crisisScenarios: CrisisScenario[] = [
    {
        situation: "You open the exam paper. Question 1 is on a topic you barely revised.",
        responses: [
            {
                text: "Panic \u2014 read it again and again hoping it changes",
                quality: 'bad',
                consequence: "Thinking brain shuts down. Alarm brain takes over. You spiral.",
                explanation: "Stress hormones flood your system. Your ability to think shrinks. You can\u2019t focus on Q2\u2013Q6 either.",
            },
            {
                text: "Skip it and move on immediately",
                quality: 'ok',
                consequence: "Partial recovery. Anxiety lingers.",
                explanation: "Smart tactically, but you haven\u2019t calmed your body down. The anxiety follows you to Q2.",
            },
            {
                text: "Close your eyes. Take one deep double-breath. Then skip to your strongest question.",
                quality: 'good',
                consequence: "Thinking brain stays online. You stay in control.",
                explanation: "The breathing technique calms your nervous system in seconds. Starting with a strong question builds momentum. You can return to Q1 later with a clear head.",
            },
        ],
    },
    {
        situation: "You\u2019re halfway through an essay and realise you\u2019ve been answering the wrong question.",
        responses: [
            {
                text: "Scribble it all out and start over in a frenzy",
                quality: 'bad',
                consequence: "Thinking brain shuts down. Alarm brain takes over. You spiral.",
                explanation: "Panic wastes 5+ minutes. Your handwriting deteriorates. The examiner sees chaos.",
            },
            {
                text: "Keep going with the wrong answer \u2014 at least it\u2019s something",
                quality: 'bad',
                consequence: "Thinking brain shuts down. Alarm brain takes over. You spiral.",
                explanation: "You\u2019ll score near zero for relevance. The marking scheme rewards answering the actual question, not volume.",
            },
            {
                text: "Draw a single line through it. Take a breath. Start the correct answer on the next page.",
                quality: 'good',
                consequence: "Thinking brain stays online. You stay in control.",
                explanation: "A single line is neat and acceptable. You preserve time, composure, and the examiner\u2019s goodwill. Partial marks on the correct question beat full marks on the wrong one.",
            },
        ],
    },
    {
        situation: "Your mind goes completely blank on a question you definitely know.",
        responses: [
            {
                text: "Stare at the page harder until it comes back",
                quality: 'bad',
                consequence: "Thinking brain shuts down. Alarm brain takes over. You spiral.",
                explanation: "The harder you force it, the more blocked it becomes. Your brain interprets the blank as a threat and locks up even more.",
            },
            {
                text: "Write anything vaguely related and hope for the best",
                quality: 'ok',
                consequence: "Partial recovery. Anxiety lingers.",
                explanation: "You might accidentally jog your memory, but unstructured writing rarely scores well.",
            },
            {
                text: "Write the topic title. List 3 related keywords. Sketch a quick mind map in the margin.",
                quality: 'good',
                consequence: "Thinking brain stays online. You stay in control.",
                explanation: "Writing things down gives your brain something to latch onto. Related words trigger connected memories \u2014 it\u2019s like opening one drawer that leads to another, and the answer surfaces.",
            },
        ],
    },
    {
        situation: "You look at the clock and realise you have 20 minutes left but two full questions to answer.",
        responses: [
            {
                text: "Pick one question and write a perfect answer, skip the other",
                quality: 'bad',
                consequence: "Thinking brain shuts down. Alarm brain takes over. You spiral.",
                explanation: "Leaving a full question blank means zero marks. Your 8th paragraph on Q5 is worth way less than a first paragraph on Q6.",
            },
            {
                text: "Rush through both as fast as possible",
                quality: 'ok',
                consequence: "Partial recovery. Anxiety lingers.",
                explanation: "Better than skipping one, but panic-writing produces illegible, unstructured answers.",
            },
            {
                text: "Split the time: 10 minutes each. Write a clear introduction + 3 bullet-point arguments for each.",
                quality: 'good',
                consequence: "Thinking brain stays online. You stay in control.",
                explanation: "Structured bullet points with key terms score nearly as well as full paragraphs. The examiner can award marks for every valid point. Two partial answers beat one complete plus one blank.",
            },
        ],
    },
];

const CrisisScenarioTrainer = () => {
    const [scenarioIndex, setScenarioIndex] = useState(0);
    const [chosenIndex, setChosenIndex] = useState<number | null>(null);
    const [results, setResults] = useState<('bad' | 'ok' | 'good')[]>([]);
    const [finished, setFinished] = useState(false);

    const scenario = crisisScenarios[scenarioIndex];
    const chosenResponse = chosenIndex !== null ? scenario.responses[chosenIndex] : null;

    const handleChoose = (idx: number) => {
        if (chosenIndex !== null) return;
        setChosenIndex(idx);
    };

    const handleNext = () => {
        if (chosenResponse) {
            const newResults = [...results, chosenResponse.quality];
            setResults(newResults);
            if (scenarioIndex + 1 >= crisisScenarios.length) {
                setFinished(true);
            } else {
                setScenarioIndex(s => s + 1);
                setChosenIndex(null);
            }
        }
    };

    const handlePlayAgain = () => {
        setScenarioIndex(0);
        setChosenIndex(null);
        setResults([]);
        setFinished(false);
    };

    const optimalCount = results.filter(r => r === 'good').length;

    const consequenceBg = (quality: 'bad' | 'ok' | 'good') => {
        if (quality === 'bad') return 'bg-rose-50 dark:bg-rose-900/20 border-rose-200 dark:border-rose-800';
        if (quality === 'ok') return 'bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-800';
        return 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800';
    };

    const consequenceTextColor = (quality: 'bad' | 'ok' | 'good') => {
        if (quality === 'bad') return 'text-rose-700 dark:text-rose-300';
        if (quality === 'ok') return 'text-amber-700 dark:text-amber-300';
        return 'text-emerald-700 dark:text-emerald-300';
    };

    const consequenceAccent = (quality: 'bad' | 'ok' | 'good') => {
        if (quality === 'bad') return 'text-rose-600 dark:text-rose-400';
        if (quality === 'ok') return 'text-amber-600 dark:text-amber-400';
        return 'text-emerald-600 dark:text-emerald-400';
    };

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Crisis Scenario Trainer</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Your brain will default to its training. Build the right instincts now.</p>

            <AnimatePresence mode="wait">
                {!finished ? (
                    <MotionDiv
                        key={`scenario-${scenarioIndex}`}
                        initial={{ opacity: 0, y: 16 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -16 }}
                        transition={{ duration: 0.3 }}
                    >
                        {/* Progress indicator */}
                        <div className="flex items-center justify-between mb-6">
                            <span className="text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Scenario {scenarioIndex + 1}/4</span>
                            <div className="flex gap-1.5">
                                {crisisScenarios.map((_, i) => (
                                    <div key={i} className={`w-2.5 h-2.5 rounded-full transition-colors ${
                                        i < scenarioIndex ? 'bg-sky-500' : i === scenarioIndex ? 'bg-sky-400 ring-2 ring-sky-200 dark:ring-sky-800' : 'bg-zinc-200 dark:bg-zinc-600'
                                    }`} />
                                ))}
                            </div>
                        </div>

                        {/* Situation card */}
                        <div className="p-5 md:p-6 rounded-xl bg-zinc-900 dark:bg-zinc-950 border border-zinc-700 mb-6">
                            <div className="flex items-start gap-3">
                                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-rose-500/20 flex items-center justify-center mt-0.5">
                                    <Zap size={16} className="text-rose-400" />
                                </div>
                                <p className="text-white font-medium text-base md:text-lg leading-relaxed">{scenario.situation}</p>
                            </div>
                        </div>

                        {/* Response options */}
                        <div className="space-y-3 mb-4">
                            {scenario.responses.map((response, idx) => {
                                const isChosen = chosenIndex === idx;
                                const isRevealed = chosenIndex !== null;

                                return (
                                    <div key={idx}>
                                        <button
                                            onClick={() => handleChoose(idx)}
                                            disabled={isRevealed}
                                            className={`w-full text-left p-4 rounded-xl border-2 transition-all duration-200 ${
                                                isRevealed
                                                    ? isChosen
                                                        ? response.quality === 'good'
                                                            ? 'border-emerald-400 dark:border-emerald-500 bg-emerald-50/50 dark:bg-emerald-900/10'
                                                            : response.quality === 'ok'
                                                                ? 'border-amber-400 dark:border-amber-500 bg-amber-50/50 dark:bg-amber-900/10'
                                                                : 'border-rose-400 dark:border-rose-500 bg-rose-50/50 dark:bg-rose-900/10'
                                                        : 'border-zinc-100 dark:border-zinc-700 opacity-40'
                                                    : 'border-zinc-200 dark:border-zinc-600 hover:border-sky-300 dark:hover:border-sky-600 hover:bg-sky-50/50 dark:hover:bg-sky-900/10 cursor-pointer'
                                            }`}
                                        >
                                            <div className="flex items-start gap-3">
                                                <span className={`flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold mt-0.5 ${
                                                    isRevealed && isChosen
                                                        ? response.quality === 'good'
                                                            ? 'bg-emerald-500 text-white'
                                                            : response.quality === 'ok'
                                                                ? 'bg-amber-500 text-white'
                                                                : 'bg-rose-500 text-white'
                                                        : 'bg-zinc-100 dark:bg-zinc-700 text-zinc-500 dark:text-zinc-400'
                                                }`}>
                                                    {String.fromCharCode(65 + idx)}
                                                </span>
                                                <span className={`text-sm font-medium ${
                                                    isRevealed && !isChosen ? 'text-zinc-400 dark:text-zinc-500' : 'text-zinc-700 dark:text-zinc-200'
                                                }`}>{response.text}</span>
                                            </div>
                                        </button>

                                        {/* Consequence panel */}
                                        <AnimatePresence>
                                            {isChosen && isRevealed && (
                                                <MotionDiv
                                                    initial={{ opacity: 0, height: 0 }}
                                                    animate={{ opacity: 1, height: 'auto' }}
                                                    exit={{ opacity: 0, height: 0 }}
                                                    transition={{ duration: 0.35, ease: 'easeOut' }}
                                                    className="overflow-hidden"
                                                >
                                                    <div className={`mt-2 p-4 rounded-xl border ${consequenceBg(response.quality)}`}>
                                                        <p className={`text-sm font-bold mb-1.5 ${consequenceAccent(response.quality)}`}>
                                                            {response.consequence}
                                                        </p>
                                                        <p className={`text-sm leading-relaxed ${consequenceTextColor(response.quality)}`}>
                                                            {response.explanation}
                                                        </p>
                                                    </div>
                                                </MotionDiv>
                                            )}
                                        </AnimatePresence>
                                    </div>
                                );
                            })}
                        </div>

                        {/* Next button */}
                        <AnimatePresence>
                            {chosenIndex !== null && (
                                <MotionDiv
                                    initial={{ opacity: 0, y: 8 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: 0.3, duration: 0.25 }}
                                    className="flex justify-end mt-6"
                                >
                                    <button
                                        onClick={handleNext}
                                        className="px-5 py-2.5 bg-sky-500 hover:bg-sky-600 text-white font-bold text-sm rounded-lg transition-colors"
                                    >
                                        {scenarioIndex + 1 >= crisisScenarios.length ? 'See Results' : 'Next Scenario'}
                                    </button>
                                </MotionDiv>
                            )}
                        </AnimatePresence>
                    </MotionDiv>
                ) : (
                    <MotionDiv
                        key="results"
                        initial={{ opacity: 0, y: 16 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -16 }}
                        transition={{ duration: 0.35 }}
                        className="text-center"
                    >
                        {/* Score */}
                        <div className="mb-6">
                            <div className={`inline-flex items-center justify-center w-20 h-20 rounded-full mb-4 ${
                                optimalCount === 4 ? 'bg-emerald-100 dark:bg-emerald-900/30' :
                                optimalCount >= 2 ? 'bg-amber-100 dark:bg-amber-900/30' :
                                'bg-rose-100 dark:bg-rose-900/30'
                            }`}>
                                <span className={`text-3xl font-bold ${
                                    optimalCount === 4 ? 'text-emerald-600 dark:text-emerald-400' :
                                    optimalCount >= 2 ? 'text-amber-600 dark:text-amber-400' :
                                    'text-rose-600 dark:text-rose-400'
                                }`}>{optimalCount}/4</span>
                            </div>
                            <p className={`text-lg font-bold mb-1 ${
                                optimalCount === 4 ? 'text-emerald-700 dark:text-emerald-300' :
                                optimalCount >= 2 ? 'text-amber-700 dark:text-amber-300' :
                                'text-rose-700 dark:text-rose-300'
                            }`}>{optimalCount}/4 optimal responses</p>
                        </div>

                        {/* Feedback */}
                        <div className={`p-5 rounded-xl border mb-6 ${
                            optimalCount === 4 ? 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800' :
                            optimalCount >= 2 ? 'bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-800' :
                            'bg-rose-50 dark:bg-rose-900/20 border-rose-200 dark:border-rose-800'
                        }`}>
                            <p className={`text-sm leading-relaxed ${
                                optimalCount === 4 ? 'text-emerald-700 dark:text-emerald-300' :
                                optimalCount >= 2 ? 'text-amber-700 dark:text-amber-300' :
                                'text-rose-700 dark:text-rose-300'
                            }`}>
                                {optimalCount === 4
                                    ? "You\u2019ve built exam-crisis muscle memory. When panic hits, your training will take over."
                                    : optimalCount >= 2
                                        ? "Good instincts, but some panic responses slipped through. Review the scenarios where you chose poorly."
                                        : "Under pressure, your brain defaulted to panic. That\u2019s exactly why we practice. Run through these again."
                                }
                            </p>
                        </div>

                        {/* Scenario results summary */}
                        <div className="flex justify-center gap-2 mb-6">
                            {results.map((r, i) => (
                                <div key={i} className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold text-white ${
                                    r === 'good' ? 'bg-emerald-500' : r === 'ok' ? 'bg-amber-500' : 'bg-rose-500'
                                }`}>
                                    {i + 1}
                                </div>
                            ))}
                        </div>

                        <button
                            onClick={handlePlayAgain}
                            className="px-6 py-2.5 bg-sky-500 hover:bg-sky-600 text-white font-bold text-sm rounded-lg transition-colors"
                        >
                            Play Again
                        </button>
                    </MotionDiv>
                )}
            </AnimatePresence>
        </div>
    );
};

// --- WRAP BUILDER ---
type WRAPSection = {
    title: string;
    prompt: string;
    suggestions: string[];
    accentColor: string;
    accentBg: string;
    accentBorder: string;
    accentText: string;
    accentRing: string;
    accentPillBg: string;
    accentPillBorder: string;
    accentPillText: string;
    accentPillSelectedBg: string;
    accentPillSelectedText: string;
    accentCardBorder: string;
};

const wrapSections: WRAPSection[] = [
    {
        title: 'Daily Maintenance',
        prompt: 'What do you need to do EVERY DAY to stay mentally well during exam season?',
        suggestions: ['8 hours sleep', 'Exercise or walk', 'Eat 3 meals', 'Talk to someone', 'Take breaks', 'Limit social media'],
        accentColor: '#10b981',
        accentBg: 'bg-emerald-50 dark:bg-emerald-900/20',
        accentBorder: 'border-emerald-200 dark:border-emerald-800',
        accentText: 'text-emerald-600 dark:text-emerald-400',
        accentRing: 'ring-emerald-500',
        accentPillBg: 'bg-emerald-50 dark:bg-emerald-900/20',
        accentPillBorder: 'border-emerald-300 dark:border-emerald-700',
        accentPillText: 'text-emerald-700 dark:text-emerald-300',
        accentPillSelectedBg: 'bg-emerald-500 dark:bg-emerald-600',
        accentPillSelectedText: 'text-white',
        accentCardBorder: 'border-l-emerald-500',
    },
    {
        title: 'Triggers',
        prompt: 'What situations or events tend to push you toward crisis?',
        suggestions: ['Poor exam result', 'Comparing myself to others', 'Falling behind schedule', 'Sleep deprivation', 'Conflict with family/friends'],
        accentColor: '#f59e0b',
        accentBg: 'bg-amber-50 dark:bg-amber-900/20',
        accentBorder: 'border-amber-200 dark:border-amber-800',
        accentText: 'text-amber-600 dark:text-amber-400',
        accentRing: 'ring-amber-500',
        accentPillBg: 'bg-amber-50 dark:bg-amber-900/20',
        accentPillBorder: 'border-amber-300 dark:border-amber-700',
        accentPillText: 'text-amber-700 dark:text-amber-300',
        accentPillSelectedBg: 'bg-amber-500 dark:bg-amber-600',
        accentPillSelectedText: 'text-white',
        accentCardBorder: 'border-l-amber-500',
    },
    {
        title: 'Warning Signs',
        prompt: 'What are the early signs that you\'re heading into crisis?',
        suggestions: ['Can\'t concentrate', 'Not sleeping', 'Withdrawing from people', 'Irritability', 'Feeling hopeless'],
        accentColor: '#f43f5e',
        accentBg: 'bg-rose-50 dark:bg-rose-900/20',
        accentBorder: 'border-rose-200 dark:border-rose-800',
        accentText: 'text-rose-600 dark:text-rose-400',
        accentRing: 'ring-rose-500',
        accentPillBg: 'bg-rose-50 dark:bg-rose-900/20',
        accentPillBorder: 'border-rose-300 dark:border-rose-700',
        accentPillText: 'text-rose-700 dark:text-rose-300',
        accentPillSelectedBg: 'bg-rose-500 dark:bg-rose-600',
        accentPillSelectedText: 'text-white',
        accentCardBorder: 'border-l-rose-500',
    },
    {
        title: 'Crisis Plan',
        prompt: 'When you\'re in crisis, what specific actions will you take?',
        suggestions: ['Call a trusted person', 'Use physiological sigh breathing', 'Go for a walk outside', 'Take a full day off studying'],
        accentColor: '#3b82f6',
        accentBg: 'bg-blue-50 dark:bg-blue-900/20',
        accentBorder: 'border-blue-200 dark:border-blue-800',
        accentText: 'text-blue-600 dark:text-blue-400',
        accentRing: 'ring-blue-500',
        accentPillBg: 'bg-blue-50 dark:bg-blue-900/20',
        accentPillBorder: 'border-blue-300 dark:border-blue-700',
        accentPillText: 'text-blue-700 dark:text-blue-300',
        accentPillSelectedBg: 'bg-blue-500 dark:bg-blue-600',
        accentPillSelectedText: 'text-white',
        accentCardBorder: 'border-l-blue-500',
    },
];

const WRAPBuilder = () => {
    const [step, setStep] = useState(0); // 0-3 = sections, 4 = complete
    const [selections, setSelections] = useState<string[][]>([[], [], [], []]);
    const [customInputs, setCustomInputs] = useState(['', '', '', '']);

    const toggleItem = (sectionIdx: number, item: string) => {
        setSelections(prev => {
            const updated = prev.map(s => [...s]);
            const idx = updated[sectionIdx].indexOf(item);
            if (idx >= 0) updated[sectionIdx].splice(idx, 1);
            else updated[sectionIdx].push(item);
            return updated;
        });
    };

    const addCustom = (sectionIdx: number) => {
        const val = customInputs[sectionIdx].trim();
        if (!val) return;
        if (!selections[sectionIdx].includes(val)) {
            setSelections(prev => {
                const updated = prev.map(s => [...s]);
                updated[sectionIdx].push(val);
                return updated;
            });
        }
        setCustomInputs(prev => {
            const updated = [...prev];
            updated[sectionIdx] = '';
            return updated;
        });
    };

    const handleNext = () => {
        if (step < 3) setStep(s => s + 1);
        else setStep(4);
    };

    const handleEdit = () => setStep(0);

    const section = step < 4 ? wrapSections[step] : null;

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Build Your WRAP</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">A personal crisis plan you write now, so you don't have to think under pressure.</p>

            {/* Progress dots */}
            <div className="flex items-center justify-center gap-2 mb-8">
                {wrapSections.map((ws, i) => (
                    <div key={i} className="flex items-center gap-2">
                        <div
                            className={`w-3 h-3 rounded-full transition-all duration-300 ${
                                step === 4 || i < step
                                    ? 'scale-100'
                                    : i === step
                                        ? 'scale-110 ring-2 ring-offset-2 ring-offset-white dark:ring-offset-zinc-800'
                                        : 'bg-zinc-200 dark:bg-zinc-600'
                            } ${i === step && step < 4 ? ws.accentRing : ''}`}
                            style={{
                                backgroundColor: step === 4 || i < step
                                    ? wrapSections[i].accentColor
                                    : i === step
                                        ? wrapSections[i].accentColor
                                        : undefined,
                            }}
                        />
                        {i < 3 && (
                            <div className={`w-6 h-0.5 rounded-full transition-colors ${
                                step === 4 || i < step ? 'bg-zinc-300 dark:bg-zinc-600' : 'bg-zinc-200 dark:bg-zinc-700'
                            }`} />
                        )}
                    </div>
                ))}
            </div>

            <AnimatePresence mode="wait">
                {step < 4 && section ? (
                    <MotionDiv
                        key={`wrap-step-${step}`}
                        initial={{ opacity: 0, x: 24 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -24 }}
                        transition={{ duration: 0.3 }}
                    >
                        {/* Step label */}
                        <div className="flex items-center gap-2 mb-3">
                            <span className={`text-xs font-bold uppercase tracking-wider ${section.accentText}`}>
                                {section.title}
                            </span>
                            <span className="text-xs text-zinc-400 dark:text-zinc-500">Step {step + 1} of 4</span>
                        </div>

                        {/* Prompt */}
                        <p className="text-base font-medium text-zinc-700 dark:text-zinc-200 mb-5">{section.prompt}</p>

                        {/* Toggleable pills */}
                        <div className="flex flex-wrap gap-2 mb-5">
                            {section.suggestions.map(item => {
                                const isSelected = selections[step].includes(item);
                                return (
                                    <button
                                        key={item}
                                        onClick={() => toggleItem(step, item)}
                                        className={`px-4 py-2 rounded-full text-sm font-medium border transition-all duration-200 ${
                                            isSelected
                                                ? `${section.accentPillSelectedBg} ${section.accentPillSelectedText} border-transparent`
                                                : `${section.accentPillBg} ${section.accentPillBorder} ${section.accentPillText} hover:opacity-80`
                                        }`}
                                    >
                                        {item}
                                    </button>
                                );
                            })}
                            {/* Show custom items as selected pills */}
                            {selections[step]
                                .filter(item => !section.suggestions.includes(item))
                                .map(item => (
                                    <button
                                        key={item}
                                        onClick={() => toggleItem(step, item)}
                                        className={`px-4 py-2 rounded-full text-sm font-medium border transition-all duration-200 ${section.accentPillSelectedBg} ${section.accentPillSelectedText} border-transparent`}
                                    >
                                        {item} &times;
                                    </button>
                                ))}
                        </div>

                        {/* Custom input */}
                        <div className="flex gap-2 mb-6">
                            <input
                                type="text"
                                value={customInputs[step]}
                                onChange={e => {
                                    const idx = step;
                                    setCustomInputs(prev => {
                                        const updated = [...prev];
                                        updated[idx] = e.target.value;
                                        return updated;
                                    });
                                }}
                                onKeyDown={e => { if (e.key === 'Enter') addCustom(step); }}
                                placeholder="Add your own..."
                                className="flex-1 px-4 py-2 rounded-lg border border-zinc-200 dark:border-zinc-600 bg-zinc-50 dark:bg-zinc-700/50 text-sm text-zinc-700 dark:text-zinc-200 placeholder-zinc-400 dark:placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-offset-1"
                                style={{ '--tw-ring-color': section.accentColor } as React.CSSProperties}
                            />
                            <button
                                onClick={() => addCustom(step)}
                                className="px-4 py-2 rounded-lg text-sm font-bold text-white transition-colors"
                                style={{ backgroundColor: section.accentColor }}
                            >
                                Add
                            </button>
                        </div>

                        {/* Next button */}
                        <div className="flex justify-end">
                            <button
                                onClick={handleNext}
                                className="px-6 py-2.5 bg-sky-500 hover:bg-sky-600 text-white font-bold text-sm rounded-lg transition-colors"
                            >
                                {step === 3 ? 'Complete My WRAP' : 'Next'}
                            </button>
                        </div>
                    </MotionDiv>
                ) : step === 4 ? (
                    <MotionDiv
                        key="wrap-complete"
                        initial={{ opacity: 0, y: 16 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -16 }}
                        transition={{ duration: 0.4 }}
                    >
                        {/* Completed WRAP card */}
                        <div className="bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-700 shadow-lg overflow-hidden">
                            {/* Card header */}
                            <div className="px-6 py-5 bg-zinc-50 dark:bg-zinc-800/80 border-b border-zinc-200 dark:border-zinc-700">
                                <h5 className="font-serif text-xl font-bold text-zinc-800 dark:text-white text-center">My Wellness Recovery Action Plan</h5>
                            </div>

                            {/* Card sections */}
                            <div className="p-6 space-y-6">
                                {wrapSections.map((ws, i) => (
                                    <div key={i} className={`pl-4 border-l-4 ${ws.accentCardBorder}`}>
                                        <h6 className={`text-sm font-bold uppercase tracking-wider mb-2 ${ws.accentText}`}>{ws.title}</h6>
                                        {selections[i].length > 0 ? (
                                            <ul className="space-y-1">
                                                {selections[i].map((item, j) => (
                                                    <li key={j} className="flex items-start gap-2 text-sm text-zinc-700 dark:text-zinc-300">
                                                        <span className="mt-1.5 w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ backgroundColor: ws.accentColor }} />
                                                        {item}
                                                    </li>
                                                ))}
                                            </ul>
                                        ) : (
                                            <p className="text-sm text-zinc-400 dark:text-zinc-500 italic">No items added</p>
                                        )}
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Summary text */}
                        <p className="mt-6 text-sm text-zinc-600 dark:text-zinc-300 text-center leading-relaxed font-medium">
                            Screenshot this plan. Pin it on your wall. When crisis hits, you won't need to think -- just follow your plan.
                        </p>

                        {/* Edit button */}
                        <div className="flex justify-center mt-5">
                            <button
                                onClick={handleEdit}
                                className="px-6 py-2.5 bg-zinc-200 dark:bg-zinc-600 hover:bg-zinc-300 dark:hover:bg-zinc-500 text-zinc-700 dark:text-zinc-200 font-bold text-sm rounded-lg transition-colors"
                            >
                                Edit My WRAP
                            </button>
                        </div>
                    </MotionDiv>
                ) : null}
            </AnimatePresence>
        </div>
    );
};

// --- MODULE COMPONENT ---
const ExamCrisisManagementModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'anatomy-of-blank', title: 'Why You "Go Blank"', eyebrow: '01 // Stress vs. Your Brain', icon: Cpu },
    { id: 'blank-mind-protocol', title: 'The "Blank Mind" Fix', eyebrow: '02 // Body-Based Fixes', icon: Zap },
    { id: 'social-containment', title: 'Protect Your Head After Exams', eyebrow: '03 // The Post-Exam Trap', icon: Shield },
    { id: 'cognitive-athlete-sleep', title: 'Sleep: Your Secret Weapon', eyebrow: '04 // Sleep for Exams', icon: Moon },
    { id: 'cognitive-athlete-nutrition', title: 'Food and Focus', eyebrow: '05 // Eating for Exam Day', icon: Utensils },
    { id: 'crisis-planning', title: 'Your Personal Crisis Plan', eyebrow: '06 // Plan Before Panic Hits', icon: ClipboardList },
    { id: 'implementation', title: 'The 7-Day Countdown', eyebrow: '07 // Your Final Week Plan', icon: Flag },
  ];

  return (
    <ModuleLayout
      moduleNumber="05"
      moduleTitle="Exam Crisis Management"
      moduleSubtitle="Your Exam Survival Guide"
      moduleDescription={`Understand why your brain freezes under pressure and learn practical techniques to stay calm, think clearly, and bounce back when things go wrong in an exam.`}
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Stay in Control"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Why You 'Go Blank'." eyebrow="Step 1" icon={Cpu} theme={theme}>
              <p>Going "blank" in an exam isn't you being stupid or unprepared. It's a physical stress response. Your brain's alarm system hijacks its thinking centre. To beat it, you need to understand the two modes your brain works in: <Highlight description="Your calm, clear-headed mode. The thinking part of your brain is in charge, so you can reason things out and pull information from memory easily." theme={theme}>Cold Cognition</Highlight> and <Highlight description="Your stressed, panicky mode. The alarm part of your brain takes over, shutting down clear thinking and blocking your access to memories you definitely have." theme={theme}>Hot Cognition</Highlight>.</p>
              <p>When you see a question you don't know, your brain can treat it as a threat. This triggers a <Highlight description="When your alarm brain hijacks your thinking brain. Stress hormones flood your system and cut the connection to your memory. You know the stuff -- you just can't reach it." theme={theme}>brain hijack</Highlight>, switching you from "cold" to "hot" mode. Your memory isn't gone; the connection is just temporarily cut off. This isn't a knowledge problem; it's a wiring problem.</p>
              <PersonalStory name="Roisin" role="6th Year, Limerick">
                <p>In my mocks, I opened the History paper and my mind just went completely white. I'd studied for weeks but I couldn't remember a single date. I sat there for about ten minutes just staring. Afterwards I was in bits -- I thought there was something wrong with me. Turns out it's just what stress does to your brain. Once I learned that, it stopped scaring me so much. In the real exam, the same thing started to happen, but this time I knew what it was and I had a plan.</p>
              </PersonalStory>
              <CognitionShiftVisualizer />
              <CrisisScenarioTrainer />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The 'Blank Mind' Fix." eyebrow="Step 2" icon={Zap} theme={theme}>
                <p>Since the problem is physical, the fix has to be physical too. You can't "think" your way out of a panic because the thinking part of your brain is offline. You need to use your body to send a "you're safe" signal to your brain. The idea is simple: <Highlight description="Using your body (like your breathing) to calm your mind, instead of trying to think your way out of panic. Your body can reset your brain faster than your thoughts can." theme={theme}>calm the body first, and the mind follows</Highlight>.</p>
                <p>The fastest way to do this is the <Highlight description="A quick breathing trick: two short inhales through your nose, then one long exhale through your mouth. It forces your nervous system to calm down in seconds. Think of it as a hard reset button." theme={theme}>Physiological Sigh</Highlight>. It's your "hard reset" button. Once the panic wave passes, you bring your thinking brain back online with a <Highlight description="The 5-4-3-2-1 trick: name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste. It pulls your brain out of the panic loop and back into the real world." theme={theme}>Sensory Grounding</Highlight> exercise. Finally, you get your brain moving again with an <Highlight description="Find the easiest question on the paper and answer it first. That small success gives your brain a confidence boost and helps clear the stress fog so you can tackle the harder stuff." theme={theme}>'Easy Win'</Highlight>.</p>
                <PhysiologicalSighGuide/>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Protect Your Head After Exams." eyebrow="Step 3" icon={Shield} theme={theme}>
              <p>The crisis doesn't end when you put your pen down. The minutes after an exam are a minefield of <Highlight description="When other people's stress rubs off on you. Standing around after an exam while everyone panics about answers is one of the fastest ways to wreck your head before the next paper." theme={theme}>catching other people's anxiety</Highlight>. Discussing answers with stressed-out friends is one of the worst things you can do. It keeps your stress levels high and stops you recovering for the next exam.</p>
              <p>That urge to compare answers? It's driven by your brain's <Highlight description="Your brain hates not knowing. After an exam, the uncertainty is torture -- so your brain desperately wants to compare answers to close the loop. But doing that almost always makes you feel worse, not better." theme={theme}>desperation for answers</Highlight>. You have to train yourself to sit with the uncertainty. This means having a strict <Highlight description="A personal rule: walk out of the exam hall and don't discuss the paper with anyone until the entire exam period is over. Put your headphones in, text a mate about something else, just get away from the chat." theme={theme}>"Post-Exam Ban"</Highlight> on discussing the paper. This isn't anti-social; it's protecting your energy for the next exam.</p>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="Sleep: Your Secret Weapon." eyebrow="Step 4" icon={Moon} theme={theme}>
              <p>Think of the weeks before the Leaving Cert like a championship season. Your brain is the muscle that matters most right now. And sleep is the single best thing you can do for it.</p>
              <p>In the week before exams, try <Highlight description="Getting an extra hour of sleep per night in the days before exams. It builds up a reserve so that if you sleep badly the night before a paper, you've got a buffer and your brain still works well." theme={theme}>sleep banking</Highlight> -- getting an extra hour of sleep per night. This builds a reserve that protects you if you sleep badly the night before a paper. While you sleep, your brain also runs its own <Highlight description="While you sleep, your brain literally flushes out the waste that builds up during the day -- the stuff that causes brain fog and makes it hard to concentrate. Pulling an all-nighter means skipping this clean-up." theme={theme}>cleaning cycle</Highlight>, flushing out the waste that causes brain fog. Pulling an all-nighter means skipping that clean-up entirely.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Food and Focus." eyebrow="Step 5" icon={Utensils} theme={theme}>
              <p>Your brain runs on sugar from food, but it needs a steady supply, not a sugar rush. <Highlight description="Foods like sweets, white bread, and energy drinks that give you a quick spike of energy followed by a crash. That crash will hit you right in the middle of your exam." theme={theme}>Quick-burn foods</Highlight> (sweets, white bread, energy drinks) cause a crash that will hit you right in the middle of your exam. Your pre-exam meal should be slow-release stuff -- porridge, wholegrain toast, eggs -- about 3 hours before.</p>
              <p>You can also use caffeine smartly. <Highlight description="Cutting back on coffee and energy drinks in the week before exams so that when you have a normal cup on exam morning, it actually hits properly instead of barely making a difference." theme={theme}>Caffeine tapering</Highlight> means cutting back on coffee and energy drinks in the week before exams. Then a normal cup on exam morning will actually wake you up properly. If tea is more your thing, even better -- it has a natural ingredient that gives you calm focus without the jitters.</p>
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Your Personal Crisis Plan." eyebrow="Step 6" icon={ClipboardList} theme={theme}>
              <p>The best time to make a plan for a crisis is before the crisis happens. The <Highlight description="A Wellness Recovery Action Plan. Basically, you write down what keeps you well, what stresses you out, and what you'll do if things go really wrong -- all while you're calm and thinking clearly." theme={theme}>WRAP</Highlight> is a tool for doing exactly that. Instead of panicking and making it up as you go, you follow a plan your calm self already wrote.</p>
              <p>Your WRAP has four parts. <strong>1. Daily Maintenance:</strong> What do you need to do every day to stay well? <strong>2. Triggers:</strong> What external events throw you off? <strong>3. Early Warning Signs:</strong> What are the first signs you're heading toward a bad place? <strong>4. Crisis Plan:</strong> Your "break glass" instructions for when things get really bad. By writing this down now, while you're calm, you don't have to make decisions when you're panicking.</p>
              <WRAPBuilder />
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="The 7-Day Countdown." eyebrow="Step 7" icon={Flag} theme={theme}>
              <p>This is where it all comes together. The final week before the exams is your countdown. Just like an athlete before a final, you ease off to let your body and mind recover and peak at the right moment. This is not the time for cramming.</p>
              <p>Your 7-day countdown should include: <strong>Cut back on caffeine</strong> (7 days out), <strong>Fix your sleep schedule</strong> (5 days out -- start waking up at exam time), and <strong>Switch to steady-energy food</strong> (3 days out -- porridge, pasta, plenty of water). The day before the exam, stop all heavy study. You're not building knowledge any more; you're getting your brain ready to use what it already knows.</p>
              <MicroCommitment theme={theme}>
                <p>Take out your phone. Find the date one week before your first exam. Set a reminder called "Start 7-Day Countdown." That's it -- you've just taken the first step.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default ExamCrisisManagementModule;
