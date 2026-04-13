/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { Cpu, Zap, Shield, Moon, Utensils, ClipboardList, Flag, Brain } from 'lucide-react';
import { type ModuleProgress } from '../types';
import { skyTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useEssentialsMode } from '../hooks/useEssentialsMode';

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
        { min: 0, max: 15, label: 'Calm', desc: 'Too relaxed. You\'re chilled out but not switched on — not enough energy to perform.', color: '#2A7D6F', zone: 'low' as const },
        { min: 15, max: 35, label: 'Focused', desc: 'A bit of stress is sharpening you up. Your thinking brain is fully in charge and your memory is working well.', color: '#2A7D6F', zone: 'good' as const },
        { min: 35, max: 55, label: 'Optimal', desc: 'The sweet spot. Just the right amount of adrenaline — you\'re alert, fast, and accurate.', color: '#2A7D6F', zone: 'good' as const },
        { min: 55, max: 72, label: 'Anxious', desc: 'Stress is tipping over. Your focus is narrowing. You re-read questions without taking them in.', color: '#9e9186', zone: 'past' as const },
        { min: 72, max: 88, label: 'Panic', desc: 'Your alarm brain is taking over. Heart racing, shallow breathing. Your thinking brain is losing control.', color: '#E85D75', zone: 'danger' as const },
        { min: 88, max: 101, label: 'Going Blank', desc: 'Full shutdown. You stare at the page and nothing comes. Your thinking brain has gone offline.', color: '#E85D75', zone: 'danger' as const },
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

    const calloutStyle = stage.zone === 'good' || stage.zone === 'low'
      ? { borderLeft: '3px solid #2A7D6F', backgroundColor: '#f0faf8', iconBg: '#e8f5f2', iconColor: '#2A7D6F', labelColor: '#1a6358', textColor: '#5a5550' }
      : stage.zone === 'past'
      ? { borderLeft: '3px solid #9e9186', backgroundColor: '#FFFFFF', iconBg: '#f0ece6', iconColor: '#9e9186', labelColor: '#5a5550', textColor: '#5a5550' }
      : { borderLeft: '3px solid #E85D75', backgroundColor: '#fde4e4', iconBg: '#fde4e4', iconColor: '#E85D75', labelColor: '#b33030', textColor: '#5a5550' };

    // Peak is at index 22-23 (stress=44-46), which is ~45% of the 51 points
    const _peakIdx = Math.round(22.5);

    return (
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            <div className="text-center mb-5">
                <span className="inline-block px-3 py-1 rounded-full text-[11px] font-bold tracking-wider uppercase mb-3" style={{ backgroundColor: '#e8f5f2', color: '#1a6358', border: '1px solid rgba(42,125,111,0.2)', letterSpacing: '0.06em' }}>Neuroscience Simulation</span>
                <h4 className="font-serif font-bold" style={{ fontSize: 24, color: '#1a1a1a' }}>Hot vs. Cold Cognition</h4>
                <p className="text-sm mt-1" style={{ color: '#7a7068' }}>Drag the slider to see how stress affects your brain during an exam.</p>
            </div>

            {/* Chart card */}
            <div className="bg-white dark:bg-zinc-900" style={{ border: '2px solid #1a1a1a', borderRadius: 16, padding: 24 }}>
                <svg viewBox={`0 0 ${W} ${H}`} className="w-full mb-1">
                    {/* Grid */}
                    {[0.25, 0.5, 0.75, 1.0].map(v => (
                        <line key={v} x1={padL} x2={W - padR} y1={toY(v)} y2={toY(v)} stroke="#f0ece6" strokeWidth="1" />
                    ))}
                    <line x1={padL} x2={W - padR} y1={toY(0)} y2={toY(0)} stroke="#d0cdc8" strokeWidth="1.5" />
                    <line x1={padL} y1={padT} x2={padL} y2={toY(0)} stroke="#d0cdc8" strokeWidth="1.5" />

                    {/* Optimal zone */}
                    <rect x={toX(0.30)} y={padT} width={toX(0.60) - toX(0.30)} height={chartH} fill="rgba(42,125,111,0.06)" rx="4" />
                    <rect x={toX(0.30)} y={padT} width={toX(0.60) - toX(0.30)} height={chartH} fill="none" stroke="rgba(42,125,111,0.2)" strokeWidth="1" strokeDasharray="4 3" rx="4" />
                    <text x={(toX(0.30) + toX(0.60)) / 2} y={toY(0) - 4} fontSize="10" fill="#1a6358" textAnchor="middle" fontWeight="700" letterSpacing="0.08em">OPTIMAL ZONE</text>

                    {/* Area fill — two-tone */}
                    <clipPath id="left-clip"><rect x={padL} y={padT} width={toX(0.45) - padL} height={chartH} /></clipPath>
                    <clipPath id="right-clip"><rect x={toX(0.45)} y={padT} width={W - padR - toX(0.45)} height={chartH} /></clipPath>
                    <path d={areaPath} fill="rgba(42,125,111,0.08)" clipPath="url(#left-clip)" />
                    <path d={areaPath} fill="rgba(232,93,117,0.07)" clipPath="url(#right-clip)" />

                    {/* Curve — two-tone via clip paths */}
                    <path d={curvePath} fill="none" stroke="#2A7D6F" strokeWidth="3" strokeLinecap="round" clipPath="url(#left-clip)" />
                    <path d={curvePath} fill="none" stroke="#E85D75" strokeWidth="3" strokeLinecap="round" clipPath="url(#right-clip)" />

                    {/* Tracking line */}
                    <line x1={dotX} x2={dotX} y1={dotY} y2={toY(0)} stroke={stress <= 55 ? 'rgba(42,125,111,0.3)' : 'rgba(232,93,117,0.3)'} strokeWidth="1" strokeDasharray="4 3" />

                    {/* Dot */}
                    <circle cx={dotX} cy={dotY} r="6" fill={stage.color} stroke="white" strokeWidth="2.5" />

                    {/* Axes */}
                    <text x={padL - 4} y={toY(1.0) + 3} fontSize="11" fill="#b0a898" textAnchor="end">High</text>
                    <text x={padL - 4} y={toY(0) + 3} fontSize="11" fill="#b0a898" textAnchor="end">Low</text>
                    <text x={padL - 4} y={toY(0.5) + 3} fontSize="9" fill="#b0a898" textAnchor="end">Med</text>
                    <text x={toX(0)} y={toY(0) + 14} fontSize="11" fill="#b0a898" textAnchor="middle">Low</text>
                    <text x={toX(0.5)} y={toY(0) + 14} fontSize="11" fill="#b0a898" textAnchor="middle">Moderate</text>
                    <text x={toX(1)} y={toY(0) + 14} fontSize="11" fill="#b0a898" textAnchor="middle">Extreme</text>
                    <text x={12} y={H / 2} fontSize="11" fill="#9e9186" textAnchor="middle" transform={`rotate(-90, 12, ${H / 2})`}>Performance</text>
                    <text x={toX(0.5)} y={toY(0) + 28} fontSize="13" fill="#1a1a1a" textAnchor="middle" fontWeight="600">Stress Level</text>
                </svg>

                {/* Slider */}
                <div className="px-2">
                    <input type="range" min="0" max="100" value={stress} onChange={e => setStress(Number(e.target.value))} className="chunky-slider chunky-slider-teal" />
                </div>
            </div>

            {/* Callout */}
            <div className="mt-5 flex items-start gap-4" style={{ borderLeft: calloutStyle.borderLeft, backgroundColor: calloutStyle.backgroundColor, borderRadius: '0 10px 10px 0', padding: '16px 20px' }}>
                <div className="flex-shrink-0 w-9 h-9 rounded-full flex items-center justify-center" style={{ backgroundColor: calloutStyle.iconBg }}>
                    {stress < 55 ? (
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke={calloutStyle.iconColor} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><line x1="9" y1="18" x2="15" y2="18"/><line x1="10" y1="22" x2="14" y2="22"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0018 8 6 6 0 006 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 018.91 14"/></svg>
                    ) : (
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke={calloutStyle.iconColor} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                    )}
                </div>
                <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                        <span className="font-serif font-semibold" style={{ fontSize: 16, color: calloutStyle.labelColor }}>{stage.label}</span>
                        <span style={{ fontSize: 13, color: '#9e9186' }}>Stress: {stress}%</span>
                    </div>
                    <p style={{ fontSize: 14, color: calloutStyle.textColor }}>{stage.desc}</p>
                </div>
            </div>

            {/* PFC vs Amygdala */}
            <div className="grid grid-cols-2 gap-3 mt-4">
                <div className="bg-white dark:bg-zinc-900" style={{ border: '1.5px solid #d0cdc8', borderRadius: 12, padding: 12 }}>
                    <div className="flex items-center justify-between mb-1.5">
                        <span className="text-xs font-bold flex items-center gap-1" style={{ color: '#2A7D6F' }}><Brain size={12} /> Thinking Brain</span>
                        <span className="text-xs font-bold" style={{ color: '#9e9186' }}>{pfcPct}%</span>
                    </div>
                    <div style={{ height: 6, backgroundColor: '#e0dbd4', borderRadius: 3 }}>
                        <motion.div style={{ height: '100%', backgroundColor: '#2A7D6F', borderRadius: 3 }} animate={{ width: `${pfcPct}%` }} transition={{ type: 'spring', stiffness: 120, damping: 20 }} />
                    </div>
                    <p className="text-xs mt-1" style={{ color: '#9e9186' }}>Logic, planning, working memory</p>
                </div>
                <div className="bg-white dark:bg-zinc-900" style={{ border: '1.5px solid #d0cdc8', borderRadius: 12, padding: 12 }}>
                    <div className="flex items-center justify-between mb-1.5">
                        <span className="text-xs font-bold flex items-center gap-1" style={{ color: '#E85D75' }}><Zap size={12} /> Alarm Brain</span>
                        <span className="text-xs font-bold" style={{ color: '#9e9186' }}>{amygPct}%</span>
                    </div>
                    <div style={{ height: 6, backgroundColor: '#e0dbd4', borderRadius: 3 }}>
                        <motion.div style={{ height: '100%', backgroundColor: '#E85D75', borderRadius: 3 }} animate={{ width: `${amygPct}%` }} transition={{ type: 'spring', stiffness: 120, damping: 20 }} />
                    </div>
                    <p className="text-xs mt-1" style={{ color: '#9e9186' }}>Fear, threat detection, survival mode</p>
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
        idle: { label: '', instruction: '', color: '#d0cdc8', scale: 0.45 },
        inhale1: { label: 'Inhale', instruction: 'Breathe in through your nose', color: '#2A7D6F', scale: 0.45 + progress * 0.35 },
        inhale2: { label: 'Inhale', instruction: 'Quick second sip of air', color: '#2A7D6F', scale: 0.8 + progress * 0.2 },
        exhale: { label: 'Exhale', instruction: 'Slow exhale through your mouth', color: '#2A7D6F', scale: 1.0 - progress * 0.55 },
        done: { label: '', instruction: '', color: '#2A7D6F', scale: 0.45 },
    };
    const cfg = phaseConfig[phase];

    // SVG breathing circle
    const cx = 100, cy = 100, maxR = 80;
    const r = maxR * cfg.scale;
    const circumference = 2 * Math.PI * 44;

    const isActive = phase !== 'idle' && phase !== 'done';
    const phaseOrder = ['inhale1', 'inhale2', 'exhale'] as const;
    const phaseIdx = phaseOrder.indexOf(phase as any);

    return (
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            <div className="text-center mb-6">
                <span className="inline-block px-3 py-1 rounded-full text-[11px] font-bold tracking-wider uppercase mb-3" style={{ backgroundColor: '#e8f5f2', color: '#1a6358', border: '1px solid rgba(42,125,111,0.2)', letterSpacing: '0.06em' }}>Breathing Technique</span>
                <h4 className="font-serif font-bold" style={{ fontSize: 24, color: '#1a1a1a' }}>The Physiological Sigh</h4>
                <p className="text-sm mt-1" style={{ color: '#7a7068' }}>Your emergency brake for acute panic. Two quick inhales, one long exhale.</p>
            </div>

            <div className="flex flex-col items-center">
                {/* Breathing circle */}
                <div className="relative w-48 h-48 mb-4">
                    <svg viewBox="0 0 200 200" className="w-full h-full">
                        <circle cx={cx} cy={cy} r="44" fill="none" stroke="#e0dbd4" strokeWidth="8" />
                        {isActive && (
                            <circle cx={cx} cy={cy} r="44" fill="none" stroke="#2A7D6F" strokeWidth="8" strokeLinecap="round" strokeDasharray={circumference} strokeDashoffset={circumference * (1 - progress)} transform={`rotate(-90 ${cx} ${cy})`} />
                        )}
                        {phase === 'done' && (
                            <circle cx={cx} cy={cy} r="44" fill="none" stroke="#2A7D6F" strokeWidth="8" strokeDasharray={circumference} strokeDashoffset={0} transform={`rotate(-90 ${cx} ${cy})`} />
                        )}
                        <motion.circle cx={cx} cy={cy} fill="#2A7D6F" fillOpacity="0.1" animate={{ r }} transition={{ type: 'tween', ease: 'easeInOut', duration: 0.15 }} />
                        <motion.circle cx={cx} cy={cy} fill="#2A7D6F" fillOpacity="0.05" animate={{ r: r + 8 }} transition={{ type: 'tween', ease: 'easeInOut', duration: 0.15 }} />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                        {phase === 'idle' && (
                            <button onClick={start} className="text-white font-semibold" style={{ backgroundColor: '#2A7D6F', borderRadius: 20, padding: '12px 24px', fontSize: 14 }}>Begin</button>
                        )}
                        {phase === 'done' && (
                            <div className="text-center">
                                <p className="font-serif font-semibold mb-2" style={{ fontSize: 16, color: '#1a6358' }}>Complete</p>
                                <button onClick={reset} className="font-medium" style={{ fontSize: 13, color: '#9e9186' }}>Again</button>
                            </div>
                        )}
                        {isActive && (
                            <div className="text-center">
                                <p className="font-serif font-semibold" style={{ fontSize: 24, color: '#2A7D6F' }}>{cfg.label}</p>
                                <p className="mt-0.5 max-w-[120px]" style={{ fontSize: 14, color: '#7a7068' }}>{cfg.instruction}</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Cycle dots */}
                <div className="flex items-center gap-2 mb-3">
                    {Array.from({ length: totalCycles }).map((_, i) => (
                        <div key={i} style={{ width: i === cycle && running ? 12 : 10, height: i === cycle && running ? 12 : 10, borderRadius: '50%', backgroundColor: i < cycle || phase === 'done' ? '#2A7D6F' : i === cycle && running ? '#2A7D6F' : '#d0cdc8', transition: 'all 0.3s' }} />
                    ))}
                    <span style={{ fontSize: 12, color: '#9e9186', marginLeft: 4 }}>{phase === 'done' ? '3/3' : running ? `${cycle + 1}/3` : '0/3'}</span>
                </div>

                {/* Phase labels */}
                {running && phase !== 'done' && (
                    <div className="flex items-center gap-1.5 text-xs font-bold">
                        <span style={{ color: phaseIdx >= 0 ? '#2A7D6F' : '#d0cdc8', fontWeight: phaseIdx === 0 ? 700 : 600 }}>Inhale 1</span>
                        <span style={{ color: '#d0cdc8' }}>→</span>
                        <span style={{ color: phaseIdx >= 1 ? '#2A7D6F' : '#d0cdc8', fontWeight: phaseIdx === 1 ? 700 : 600 }}>Inhale 2</span>
                        <span style={{ color: '#d0cdc8' }}>→</span>
                        <span style={{ color: phaseIdx >= 2 ? '#2A7D6F' : '#d0cdc8', fontWeight: phaseIdx === 2 ? 700 : 600 }}>Exhale</span>
                    </div>
                )}

                {/* Step cards */}
                <div className="mt-5 grid grid-cols-3 gap-3 w-full max-w-sm text-center">
                    {[
                        { label: 'Inhale 1', desc: 'Sharp nose breath', key: 'inhale1' },
                        { label: 'Inhale 2', desc: 'Quick sip on top', key: 'inhale2' },
                        { label: 'Exhale', desc: 'Long slow mouth', key: 'exhale' },
                    ].map(step => {
                        const isStepActive = phase === step.key;
                        return (
                            <div key={step.key} className="bg-white dark:bg-zinc-900" style={{
                                border: isStepActive ? '2px solid #2A7D6F' : '1.5px solid #d0cdc8',
                                borderRadius: 14,
                                padding: '12px 8px',
                                backgroundColor: isStepActive ? '#e8f5f2' : '#FFFFFF',
                            }}>
                                <p className="font-serif font-semibold" style={{ fontSize: 15, color: isStepActive ? '#1a6358' : '#9e9186' }}>{step.label}</p>
                                <p style={{ fontSize: 13, color: isStepActive ? '#5a5550' : '#b0a898', marginTop: 2 }}>{step.desc}</p>
                            </div>
                        );
                    })}
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

    const consequenceStyle = (quality: 'bad' | 'ok' | 'good') => {
        if (quality === 'good') return { bg: '#f0faf8', border: '#2A7D6F', text: '#1a6358', label: '#1a6358' };
        if (quality === 'ok') return { bg: '#f4f0eb', border: '#9e9186', text: '#5a5550', label: '#5a5550' };
        return { bg: '#fde4e4', border: '#E85D75', text: '#5a5550', label: '#b33030' };
    };

    return (
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            <div className="text-center mb-8">
                <span className="inline-block px-3 py-1 rounded-full text-[11px] font-bold tracking-wider uppercase mb-3" style={{ backgroundColor: '#e8f5f2', color: '#1a6358', border: '1px solid rgba(42,125,111,0.2)', letterSpacing: '0.06em' }}>Exam Skills Trainer</span>
                <h4 className="font-serif font-bold" style={{ fontSize: 24, color: '#1a1a1a' }}>Crisis Scenario Trainer</h4>
                <p className="text-sm mt-1" style={{ color: '#7a7068' }}>Your brain will default to its training. Build the right instincts now.</p>
            </div>

            <AnimatePresence mode="wait">
                {!finished ? (
                    <MotionDiv key={`scenario-${scenarioIndex}`} initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -16 }} transition={{ duration: 0.3 }}>
                        {/* Progress */}
                        <div className="flex items-center justify-between mb-6">
                            <span style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', color: '#9e9186', textTransform: 'uppercase' as const }}>Scenario {scenarioIndex + 1}/4</span>
                            <div className="flex gap-1.5">
                                {crisisScenarios.map((_, i) => (
                                    <div key={i} style={{ width: 10, height: 10, borderRadius: '50%', backgroundColor: i <= scenarioIndex ? '#2A7D6F' : '#d0cdc8', transition: 'background-color 0.3s' }} />
                                ))}
                            </div>
                        </div>

                        {/* Scenario card */}
                        <div className="bg-white dark:bg-zinc-900 mb-6 flex items-start gap-3" style={{ border: '2px solid #1a1a1a', borderLeft: '5px solid #E85D75', borderRadius: 14, padding: '20px 24px' }}>
                            <div className="flex-shrink-0 w-9 h-9 rounded-full flex items-center justify-center mt-0.5" style={{ backgroundColor: '#fde4e4' }}>
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#E85D75" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                            </div>
                            <div>
                                <span className="inline-block mb-2" style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.1em', backgroundColor: '#fde4e4', color: '#b33030', borderRadius: 20, padding: '3px 10px', textTransform: 'uppercase' as const }}>Crisis Scenario</span>
                                <p className="font-serif" style={{ fontSize: 17, color: '#1a1a1a', lineHeight: 1.5 }}>{scenario.situation}</p>
                            </div>
                        </div>

                        {/* Options */}
                        <div className="space-y-3 mb-4">
                            {scenario.responses.map((response, idx) => {
                                const isChosen = chosenIndex === idx;
                                const isRevealed = chosenIndex !== null;
                                const cs = consequenceStyle(response.quality);

                                return (
                                    <div key={idx}>
                                        <button onClick={() => handleChoose(idx)} disabled={isRevealed} className="w-full text-left p-4 transition-all duration-200" style={
                                            isRevealed
                                                ? isChosen
                                                    ? response.quality === 'good'
                                                        ? { backgroundColor: '#e8f5f2', border: '2px solid #2A7D6F', borderRadius: 14 }
                                                        : response.quality === 'bad'
                                                            ? { backgroundColor: '#fde4e4', border: '2px solid #E85D75', borderLeft: '4px solid #E85D75', borderRadius: 14 }
                                                            : { backgroundColor: '#f4f0eb', border: '2px solid #9e9186', borderRadius: 14 }
                                                    : { backgroundColor: '#FFFFFF', border: '2px solid #d0cdc8', borderRadius: 14, opacity: 0.4 }
                                                : { backgroundColor: '#FFFFFF', border: '2px solid #1a1a1a', borderRadius: 14, cursor: 'pointer' }
                                        }>
                                            <div className="flex items-start gap-3">
                                                <span className="flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold mt-0.5" style={{
                                                    backgroundColor: isRevealed && isChosen
                                                        ? response.quality === 'good' ? '#2A7D6F' : response.quality === 'bad' ? '#E85D75' : '#9e9186'
                                                        : '#f0ece6',
                                                    color: isRevealed && isChosen ? '#FFFFFF' : '#9e9186',
                                                }}>
                                                    {String.fromCharCode(65 + idx)}
                                                </span>
                                                <span style={{ fontSize: 14, fontWeight: 500, color: isRevealed && !isChosen ? '#b0a898' : '#1a1a1a' }}>{response.text}</span>
                                            </div>
                                        </button>

                                        <AnimatePresence>
                                            {isChosen && isRevealed && (
                                                <MotionDiv initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }} transition={{ duration: 0.35, ease: 'easeOut' }} className="overflow-hidden">
                                                    <div className="mt-2" style={{ borderLeft: `3px solid ${cs.border}`, backgroundColor: cs.bg, borderRadius: '0 10px 10px 0', padding: '16px 20px' }}>
                                                        <p className="font-semibold text-sm mb-1" style={{ color: cs.label }}>{response.consequence}</p>
                                                        <p className="text-sm leading-relaxed" style={{ color: cs.text }}>{response.explanation}</p>
                                                    </div>
                                                </MotionDiv>
                                            )}
                                        </AnimatePresence>
                                    </div>
                                );
                            })}
                        </div>

                        <AnimatePresence>
                            {chosenIndex !== null && (
                                <MotionDiv initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3, duration: 0.25 }} className="flex justify-end mt-6">
                                    <button onClick={handleNext} style={{ backgroundColor: '#2A7D6F', borderRadius: 20, padding: '12px 24px', fontSize: 14, fontWeight: 600, color: '#FFFFFF' }}>
                                        {scenarioIndex + 1 >= crisisScenarios.length ? 'See Results' : 'Next Scenario'}
                                    </button>
                                </MotionDiv>
                            )}
                        </AnimatePresence>
                    </MotionDiv>
                ) : (
                    <MotionDiv key="results" initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -16 }} transition={{ duration: 0.35 }} className="text-center">
                        <div className="mb-6">
                            <div className="inline-flex items-center justify-center w-20 h-20 rounded-full mb-4" style={{ backgroundColor: '#e8f5f2' }}>
                                <span className="font-serif font-bold" style={{ fontSize: 28, color: '#2A7D6F' }}>{optimalCount}/4</span>
                            </div>
                            <p className="font-serif font-semibold text-lg mb-1" style={{ color: '#1a1a1a' }}>{optimalCount}/4 optimal responses</p>
                        </div>

                        <div className="mb-6" style={
                            optimalCount === 4
                                ? { borderLeft: '3px solid #2A7D6F', backgroundColor: '#f0faf8', borderRadius: '0 10px 10px 0', padding: '16px 20px', textAlign: 'left' }
                                : optimalCount >= 2
                                    ? { borderLeft: '3px solid #9e9186', backgroundColor: '#f4f0eb', borderRadius: '0 10px 10px 0', padding: '16px 20px', textAlign: 'left' }
                                    : { borderLeft: '3px solid #E85D75', backgroundColor: '#fde4e4', borderRadius: '0 10px 10px 0', padding: '16px 20px', textAlign: 'left' }
                        }>
                            <p className="text-sm leading-relaxed" style={{ color: optimalCount === 4 ? '#1a6358' : optimalCount >= 2 ? '#5a5550' : '#b33030' }}>
                                {optimalCount === 4 ? "You\u2019ve built exam-crisis muscle memory. When panic hits, your training will take over." : optimalCount >= 2 ? "Good instincts, but some panic responses slipped through. Review the scenarios where you chose poorly." : "Under pressure, your brain defaulted to panic. That\u2019s exactly why we practice. Run through these again."}
                            </p>
                        </div>

                        <div className="flex justify-center gap-2 mb-6">
                            {results.map((r, i) => (
                                <div key={i} className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold" style={{
                                    backgroundColor: r === 'good' ? '#2A7D6F' : r === 'ok' ? '#9e9186' : '#E85D75',
                                    color: '#FFFFFF',
                                }}>{i + 1}</div>
                            ))}
                        </div>

                        <button onClick={handlePlayAgain} style={{ backgroundColor: '#2A7D6F', borderRadius: 20, padding: '12px 24px', fontSize: 14, fontWeight: 600, color: '#FFFFFF' }}>Play Again</button>
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
    accentCardDot: string;
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
        accentCardDot: 'bg-emerald-500',
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
        accentCardDot: 'bg-amber-500',
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
        accentCardDot: 'bg-rose-500',
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
        accentCardDot: 'bg-blue-500',
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
        <div className="my-10 rounded-2xl p-8 md:p-12" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
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
                                    <div key={i} className="pl-4">
                                        <div className="flex items-center gap-2 mb-2">
                                            <span className={`w-2 h-2 rounded-full flex-shrink-0 ${ws.accentCardDot}`} />
                                            <h6 className={`text-sm font-bold uppercase tracking-wider ${ws.accentText}`}>{ws.title}</h6>
                                        </div>
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
  const essentials = useEssentialsMode();
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
              {essentials ? (
                <>
                  <p>Going blank is not stupidity. It is a physical stress response. Your alarm brain hijacks your thinking brain. Your memory is still there. The connection is just temporarily cut off.</p>
                  <p>Understanding this is the first step. Once you know what is happening, you can use the tools in this module to stay in control. Try the simulator and scenario trainer below.</p>
                </>
              ) : (
                <>
                  <p>Going "blank" in an exam isn't you being stupid or unprepared. It's a physical stress response. Your brain's alarm system hijacks its thinking centre. To beat it, you need to understand the two modes your brain works in: <Highlight description="Your calm, clear-headed mode. The thinking part of your brain is in charge, so you can reason things out and pull information from memory easily." theme={theme}>Cold Cognition</Highlight> and <Highlight description="Your stressed, panicky mode. The alarm part of your brain takes over, shutting down clear thinking and blocking your access to memories you definitely have." theme={theme}>Hot Cognition</Highlight>.</p>
                  <p>When you see a question you don't know, your brain can treat it as a threat. This triggers a <Highlight description="When your alarm brain hijacks your thinking brain. Stress hormones flood your system and cut the connection to your memory. You know the stuff -- you just can't reach it." theme={theme}>brain hijack</Highlight>, switching you from "cold" to "hot" mode. Your memory isn't gone; the connection is just temporarily cut off. This isn't a knowledge problem; it's a wiring problem.</p>
                  <PersonalStory name="Roisin" role="6th Year, Limerick">
                    <p>In my mocks, I opened the History paper and my mind just went completely white. I'd studied for weeks but I couldn't remember a single date. I sat there for about ten minutes just staring. Afterwards I was in bits -- I thought there was something wrong with me. Turns out it's just what stress does to your brain. Once I learned that, it stopped scaring me so much. In the real exam, the same thing started to happen, but this time I knew what it was and I had a plan.</p>
                  </PersonalStory>
                </>
              )}
              <CognitionShiftVisualizer />
              <CrisisScenarioTrainer />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The 'Blank Mind' Fix." eyebrow="Step 2" icon={Zap} theme={theme}>
                {essentials ? (
                  <p>The fix is physical, not mental. Use the Physiological Sigh: two quick nose inhales, one long mouth exhale. Then ground yourself by noticing what you can see and hear. Then start with the easiest question on the paper. Practice below.</p>
                ) : (
                  <>
                    <p>Since the problem is physical, the fix has to be physical too. You can't "think" your way out of a panic because the thinking part of your brain is offline. You need to use your body to send a "you're safe" signal to your brain. The idea is simple: <Highlight description="Using your body (like your breathing) to calm your mind, instead of trying to think your way out of panic. Your body can reset your brain faster than your thoughts can." theme={theme}>calm the body first, and the mind follows</Highlight>.</p>
                    <p>The fastest way to do this is the <Highlight description="A quick breathing trick: two short inhales through your nose, then one long exhale through your mouth. It forces your nervous system to calm down in seconds. Think of it as a hard reset button." theme={theme}>Physiological Sigh</Highlight>. It's your "hard reset" button. Once the panic wave passes, you bring your thinking brain back online with a <Highlight description="The 5-4-3-2-1 trick: name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste. It pulls your brain out of the panic loop and back into the real world." theme={theme}>Sensory Grounding</Highlight> exercise. Finally, you get your brain moving again with an <Highlight description="Find the easiest question on the paper and answer it first. That small success gives your brain a confidence boost and helps clear the stress fog so you can tackle the harder stuff." theme={theme}>'Easy Win'</Highlight>.</p>
                  </>
                )}
                <PhysiologicalSighGuide/>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Protect Your Head After Exams." eyebrow="Step 3" icon={Shield} theme={theme}>
              {essentials ? (
                <p>Do not compare answers after an exam. Other people's panic is contagious. Put headphones in, walk away, and protect your energy for the next paper. The exam is done. Let it go.</p>
              ) : (
                <>
                  <p>The crisis doesn't end when you put your pen down. The minutes after an exam are a minefield of <Highlight description="When other people's stress rubs off on you. Standing around after an exam while everyone panics about answers is one of the fastest ways to wreck your head before the next paper." theme={theme}>catching other people's anxiety</Highlight>. Discussing answers with stressed-out friends is one of the worst things you can do. It keeps your stress levels high and stops you recovering for the next exam.</p>
                  <p>That urge to compare answers? It's driven by your brain's <Highlight description="Your brain hates not knowing. After an exam, the uncertainty is torture -- so your brain desperately wants to compare answers to close the loop. But doing that almost always makes you feel worse, not better." theme={theme}>desperation for answers</Highlight>. You have to train yourself to sit with the uncertainty. This means having a strict <Highlight description="A personal rule: walk out of the exam hall and don't discuss the paper with anyone until the entire exam period is over. Put your headphones in, text a mate about something else, just get away from the chat." theme={theme}>"Post-Exam Ban"</Highlight> on discussing the paper. This isn't anti-social; it's protecting your energy for the next exam.</p>
                </>
              )}
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="Sleep: Your Secret Weapon." eyebrow="Step 4" icon={Moon} theme={theme}>
              {essentials ? (
                <p>Sleep is your brain's best recovery tool. Bank extra sleep the week before exams. Your brain cleans itself during sleep. Pulling an all-nighter skips that cleanup and leaves you foggy.</p>
              ) : (
                <>
                  <p>Think of the weeks before the Leaving Cert like a championship season. Your brain is the muscle that matters most right now. And sleep is the single best thing you can do for it.</p>
                  <p>In the week before exams, try <Highlight description="Getting an extra hour of sleep per night in the days before exams. It builds up a reserve so that if you sleep badly the night before a paper, you've got a buffer and your brain still works well." theme={theme}>sleep banking</Highlight> -- getting an extra hour of sleep per night. This builds a reserve that protects you if you sleep badly the night before a paper. While you sleep, your brain also runs its own <Highlight description="While you sleep, your brain literally flushes out the waste that builds up during the day -- the stuff that causes brain fog and makes it hard to concentrate. Pulling an all-nighter means skipping this clean-up." theme={theme}>cleaning cycle</Highlight>, flushing out the waste that causes brain fog. Pulling an all-nighter means skipping that clean-up entirely.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Food and Focus." eyebrow="Step 5" icon={Utensils} theme={theme}>
              {essentials ? (
                <p>Eat slow-release food 3 hours before exams: porridge, wholegrain toast, eggs. Avoid sugar and energy drinks. They crash mid-exam. Cut caffeine the week before so a normal cup on exam morning actually works.</p>
              ) : (
                <>
                  <p>Your brain runs on sugar from food, but it needs a steady supply, not a sugar rush. <Highlight description="Foods like sweets, white bread, and energy drinks that give you a quick spike of energy followed by a crash. That crash will hit you right in the middle of your exam." theme={theme}>Quick-burn foods</Highlight> (sweets, white bread, energy drinks) cause a crash that will hit you right in the middle of your exam. Your pre-exam meal should be slow-release stuff -- porridge, wholegrain toast, eggs -- about 3 hours before.</p>
                  <p>You can also use caffeine smartly. <Highlight description="Cutting back on coffee and energy drinks in the week before exams so that when you have a normal cup on exam morning, it actually hits properly instead of barely making a difference." theme={theme}>Caffeine tapering</Highlight> means cutting back on coffee and energy drinks in the week before exams. Then a normal cup on exam morning will actually wake you up properly. If tea is more your thing, even better -- it has a natural ingredient that gives you calm focus without the jitters.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Your Personal Crisis Plan." eyebrow="Step 6" icon={ClipboardList} theme={theme}>
              {essentials ? (
                <p>Build a crisis plan while you are calm. Your WRAP has four parts: daily maintenance habits, your personal triggers, early warning signs, and your specific crisis actions. Write it now so you do not have to think when you are panicking.</p>
              ) : (
                <>
                  <p>The best time to make a plan for a crisis is before the crisis happens. The <Highlight description="A Wellness Recovery Action Plan. Basically, you write down what keeps you well, what stresses you out, and what you'll do if things go really wrong -- all while you're calm and thinking clearly." theme={theme}>WRAP</Highlight> is a tool for doing exactly that. Instead of panicking and making it up as you go, you follow a plan your calm self already wrote.</p>
                  <p>Your WRAP has four parts:</p>
                </>
              )}
              <div className="my-10 rounded-2xl p-5 md:p-6 space-y-3" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#93C5FD', border: '2.5px solid #2563EB', borderRadius: 16, boxShadow: '4px 4px 0px 0px #2563EB' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#2563EB' }}>1</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#1E3A8A' }}>Daily Maintenance</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#1E3A8A', opacity: 0.8 }}>What do you need to do every day to stay well?</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#FCD34D', border: '2.5px solid #D97706', borderRadius: 16, boxShadow: '4px 4px 0px 0px #D97706' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#D97706' }}>2</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#78350F' }}>Triggers</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#78350F', opacity: 0.8 }}>What external events throw you off?</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#FDBA74', border: '2.5px solid #EA580C', borderRadius: 16, boxShadow: '4px 4px 0px 0px #EA580C' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#EA580C' }}>3</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#7C2D12' }}>Early Warning Signs</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#7C2D12', opacity: 0.8 }}>What are the first signs you're heading toward a bad place?</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#6EE7B7', border: '2.5px solid #059669', borderRadius: 16, boxShadow: '4px 4px 0px 0px #059669' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#059669' }}>4</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#064E3B' }}>Crisis Plan</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#064E3B', opacity: 0.8 }}>Your "break glass" instructions for when things get really bad. By writing this down now, while you're calm, you don't have to make decisions when you're panicking.</p>
                  </div>
                </div>
              </div>
              <WRAPBuilder />
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="The 7-Day Countdown." eyebrow="Step 7" icon={Flag} theme={theme}>
              {essentials ? (
                <p>7 days out: cut caffeine. 5 days out: fix your sleep to exam times. 3 days out: switch to steady-energy food. Day before: stop heavy study by 6pm. You are getting your brain ready to perform, not cramming more in.</p>
              ) : (
                <>
                  <p>This is where it all comes together. The final week before the exams is your countdown. Just like an athlete before a final, you ease off to let your body and mind recover and peak at the right moment. This is not the time for cramming.</p>
                  <p>Your 7-day countdown should include: <strong>Cut back on caffeine</strong> (7 days out), <strong>Fix your sleep schedule</strong> (5 days out -- start waking up at exam time), and <strong>Switch to steady-energy food</strong> (3 days out -- porridge, pasta, plenty of water). The day before the exam, stop all heavy study. You're not building knowledge any more; you're getting your brain ready to use what it already knows.</p>
                </>
              )}
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
