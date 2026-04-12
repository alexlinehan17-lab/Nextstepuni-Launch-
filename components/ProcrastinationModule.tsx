/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  HeartPulse, Calculator, Shield, Zap, Wrench, Brain, RotateCcw, HeartHandshake
} from 'lucide-react';
import { type ModuleProgress } from '../types';
import { orangeTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { useNorthStar } from '../hooks/useNorthStar';
import NorthStarCallout from './NorthStarCallout';
import { COMPACT_CALLOUT_PLACEMENTS } from '../northStarData';

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

    const levers: { key: keyof typeof vars; label: string; desc: string; letter: string; good: boolean }[] = [
      { key: 'E', label: 'Expectancy', desc: 'Belief you can succeed', letter: 'E', good: true },
      { key: 'V', label: 'Value', desc: 'How rewarding it feels', letter: 'V', good: true },
      { key: 'I', label: 'Impulsiveness', desc: 'Distraction susceptibility', letter: 'I', good: false },
      { key: 'D', label: 'Delay', desc: 'Distance to deadline', letter: 'D', good: false },
    ];

    // Ring gauge
    const radius = 52;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (pct / 100) * circumference;

    return(
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Procrastination Equation</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-2">Adjust the four levers to see what drives — or kills — your motivation.</p>
            <p className="text-center text-xs mb-8" style={{ color: '#7a7068' }}>
              <span className="font-semibold" style={{ color: '#2A7D6F' }}>E and V</span> boost motivation. <span className="font-semibold" style={{ color: '#1a1a1a' }}>I and D</span> drain it.
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
                const isPositive = lever.good;
                const direction = isPositive ? '↑ Increase' : '↓ Decrease';

                return (
                  <div
                    key={lever.key}
                    className="flex flex-col items-center bg-white dark:bg-zinc-900"
                    style={{ border: '2px solid #1a1a1a', borderRadius: 16, padding: '20px 16px' }}
                  >
                    {/* Letter */}
                    <p className="font-serif font-bold" style={{ fontSize: 32, color: isPositive ? '#2A7D6F' : '#1a1a1a' }}>{lever.letter}</p>
                    {/* Term */}
                    <p className="text-xs font-bold text-center mt-1" style={{ color: '#1a1a1a' }}>{lever.label}</p>
                    {/* Description */}
                    <p className="text-[10px] text-center mb-0" style={{ color: '#7a7068' }}>{lever.desc}</p>

                    {/* Vertical bar — standalone block, no overlap */}
                    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', margin: '16px 0 12px' }}>
                      <div style={{
                        width: 32,
                        height: 120,
                        backgroundColor: isPositive ? '#d1fae5' : '#fee2e2',
                        borderRadius: 16,
                        position: 'relative',
                        overflow: 'hidden',
                      }}>
                        <motion.div
                          style={{
                            position: 'absolute',
                            bottom: 0,
                            left: 0,
                            right: 0,
                            backgroundColor: isPositive ? '#2A7D6F' : '#E85D75',
                            borderRadius: 16,
                          }}
                          animate={{ height: `${val}%` }}
                          transition={{ type: 'spring', damping: 15, stiffness: 100 }}
                        />
                      </div>
                    </div>

                    {/* Slider — clearly below the bar */}
                    <div style={{ width: '100%', padding: '0 4px', marginBottom: 8 }}>
                      <input
                        type="range" min="1" max="100" value={val}
                        onChange={e => setVars({...vars, [lever.key]: parseInt(e.target.value)})}
                        className="chunky-slider chunky-slider-teal"
                      />
                    </div>

                    {/* Direction label */}
                    <p className="text-xs font-semibold" style={{ color: isPositive ? '#2A7D6F' : '#7a7068' }}>{direction}</p>
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
              className="p-4 rounded-xl text-sm"
              style={level === 'high' ? { backgroundColor: '#6EE7B7', border: '2.5px solid #059669', boxShadow: '3px 3px 0px 0px #059669', color: '#064E3B' } : level === 'medium' ? { backgroundColor: '#FDE68A', border: '2.5px solid #D97706', boxShadow: '3px 3px 0px 0px #D97706', color: '#78350F' } : { backgroundColor: '#FCA5A5', border: '2.5px solid #DC2626', boxShadow: '3px 3px 0px 0px #DC2626', color: '#7F1D1D' }}
            >
              <p><span className="font-bold">Diagnosis:</span> {getDiagnosis()}</p>
            </motion.div>
        </div>
    );
};

const IfThenAutopilot = () => {
    const [ifText, setIfText] = useState('');
    const [thenText, setThenText] = useState('');
    const [submitted, setSubmitted] = useState(false);

    const templates = [
      { trigger: 'IF I open Instagram during study time', action: 'THEN I will close the app and do one practice question' },
      { trigger: 'IF I feel overwhelmed by a topic', action: 'THEN I will break it into 3 smaller parts and tackle just the first one' },
      { trigger: "IF I haven't started by 4pm", action: 'THEN I will open my textbook to page 1 and read for 2 minutes' },
      { trigger: 'IF I finish a Pomodoro', action: 'THEN I will stand up, stretch, and drink some water' },
    ];

    const handleTemplateClick = (t: typeof templates[0]) => {
      setIfText(t.trigger.replace('IF ', ''));
      setThenText(t.action.replace('THEN ', ''));
      setSubmitted(false);
    };

    const bothFilled = ifText.trim().length > 0 && thenText.trim().length > 0;

    return(
         <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The "If-Then" Autopilot</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Pre-load a decision to bypass willpower. Fill in both fields or pick a template below.</p>

            {/* Template suggestions */}
            <div className="flex flex-wrap justify-center gap-2 mb-6">
              {templates.map((t, i) => (
                <button key={i} onClick={() => handleTemplateClick(t)}
                  className="px-3 py-1.5 text-xs font-medium rounded-full bg-zinc-100 dark:bg-zinc-900/50 text-zinc-600 dark:text-zinc-400 border border-zinc-200 dark:border-zinc-700 hover:border-orange-400 hover:text-orange-600 dark:hover:text-orange-400 transition-colors">
                  {t.trigger}
                </button>
              ))}
            </div>

            {/* Form inputs */}
            <div className="space-y-4 mb-6">
              <div>
                <label className="block text-xs font-bold text-zinc-500 dark:text-zinc-400 mb-1 uppercase tracking-wider">IF (trigger)</label>
                <input
                  type="text" value={ifText}
                  onChange={e => { setIfText(e.target.value); setSubmitted(false); }}
                  placeholder="e.g. I open Instagram during study time"
                  className="w-full bg-white dark:bg-zinc-800 rounded-xl px-5 py-3.5 text-sm font-medium text-zinc-800 dark:text-white placeholder-zinc-400 outline-none transition-all"
                  style={{ border: '1.5px solid #E7E5E4' }}
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-zinc-500 dark:text-zinc-400 mb-1 uppercase tracking-wider">THEN (action)</label>
                <input
                  type="text" value={thenText}
                  onChange={e => { setThenText(e.target.value); setSubmitted(false); }}
                  placeholder="e.g. I will close the app and do one practice question"
                  className="w-full bg-white dark:bg-zinc-800 rounded-xl px-5 py-3.5 text-sm font-medium text-zinc-800 dark:text-white placeholder-zinc-400 outline-none transition-all"
                  style={{ border: '1.5px solid #E7E5E4' }}
                />
              </div>
            </div>

            <div className="flex justify-center">
              <button
                onClick={() => setSubmitted(true)}
                disabled={!bothFilled}
                className="px-5 py-3 bg-orange-500 hover:bg-orange-600 disabled:opacity-40 disabled:cursor-not-allowed text-white font-bold rounded-lg text-sm transition-colors">
                Lock In Plan
              </button>
            </div>

            <AnimatePresence>
              {submitted && bothFilled && (
                <motion.div
                  initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }}
                  className="mt-6 p-5 rounded-xl"
                  style={{ backgroundColor: '#6EE7B7', border: '2.5px solid #059669', boxShadow: '3px 3px 0px 0px #059669' }}
                >
                  <p className="text-xs font-bold uppercase tracking-wider mb-2 text-center" style={{ color: '#065F46' }}>Your Autopilot Plan</p>
                  <p className="text-center text-sm leading-relaxed" style={{ color: '#064E3B' }}>
                    <span className="font-bold" style={{ color: '#065F46' }}>IF</span>{' '}
                    <span className="font-semibold">{ifText}</span>
                    <span className="mx-2">&rarr;</span>
                    <span className="font-bold" style={{ color: '#065F46' }}>THEN</span>{' '}
                    <span className="font-semibold">{thenText}</span>
                  </p>
                </motion.div>
              )}
            </AnimatePresence>
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

    const practiceForgiveness = () => {
        setGuilt(g => Math.max(0, g - 18));
        setAvoidance(a => Math.max(0, a - 15));
    }

    const reset = () => {
        setGuilt(10);
        setAvoidance(10);
    }

    return(
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Guilt Spiral</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">"Tough love" doesn't work. It just adds more negative emotion to the fire. Try both buttons to see the difference.</p>
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
             <div className="flex justify-center gap-3 flex-wrap">
                <button onClick={addCriticism} className="px-4 py-2 bg-rose-100 dark:bg-rose-900/30 text-rose-800 dark:text-rose-300 text-xs font-bold rounded-lg border border-rose-200 dark:border-rose-800">Add Self-Criticism</button>
                <button onClick={practiceForgiveness} className="px-4 py-2 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-800 dark:text-emerald-300 text-xs font-bold rounded-lg border border-emerald-200 dark:border-emerald-800">Practice Self-Forgiveness</button>
                <button onClick={reset} className="px-4 py-2 bg-zinc-100 dark:bg-zinc-700 text-zinc-800 dark:text-zinc-200 text-xs font-bold rounded-lg border border-zinc-200 dark:border-zinc-700">Reset</button>
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
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
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
                            <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-rose-600 dark:text-rose-400">Self-punishment</strong> after procrastinating feels like you're being responsible, but it just makes things worse. Guilt &#8594; avoidance &#8594; more guilt. Within days, you feel completely stuck.</p>
                        </div>
                        <div className="flex items-start gap-2.5 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900">
                            <span className="text-emerald-500 text-lg mt-0.5">&#x2714;</span>
                            <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-emerald-600 dark:text-emerald-400">Self-forgiveness</strong> breaks the loop. When you accept the slip without hammering yourself, your brain calms down enough to actually get back to work. People who forgive themselves for procrastinating end up procrastinating less next time.</p>
                        </div>
                    </div>
                </motion.div>
            )}
        </div>
    );
};

const CircuitBreaker = () => {
    const [reframe, setReframe] = useState('');
    const lower = reframe.toLowerCase();

    const forgivenessWords = ['forgive', 'okay', "it's fine", "it's ok", "that's ok", 'human', 'everyone', 'normal', 'mistake'];
    const actionWords = ['i will', 'next time', 'tomorrow', 'going to', 'start', 'try', 'plan', 'can'];
    const compassionWords = ['kind', 'gentle', 'breathe', 'calm', 'deserve'];

    const containsForgiveness = forgivenessWords.some(w => lower.includes(w));
    const containsAction = actionWords.some(w => lower.includes(w));
    const containsCompassion = compassionWords.some(w => lower.includes(w));

    const allDetected = containsForgiveness && containsAction && containsCompassion;
    const qualities = [
      { label: 'Self-Forgiveness', detected: containsForgiveness },
      { label: 'Forward Action', detected: containsAction },
      { label: 'Self-Compassion', detected: containsCompassion },
    ];

    return(
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-bold text-center" style={{ color: '#1a1a1a' }}>The Circuit Breaker</h4>
            <p className="text-center text-sm mt-1 mb-8" style={{ color: '#7a7068' }}>Rewrite this self-critical thought into something kinder and more action-focused.</p>

            {/* Section 1 — Negative thought */}
            <div className="bg-white dark:bg-zinc-900 max-w-lg mx-auto" style={{ border: '2px solid #1a1a1a', borderRadius: 14, borderLeft: '4px solid #E85D75', padding: '20px 24px' }}>
              <span className="inline-block text-[10px] font-bold uppercase tracking-wider mb-2" style={{ backgroundColor: '#fde4e4', color: '#b33030', borderRadius: 20, padding: '3px 10px' }}>Self-critical thought</span>
              <p className="font-serif italic" style={{ fontSize: 18, color: '#1a1a1a' }}>I'm so useless, I wasted the whole day.</p>
            </div>

            {/* Transformation connector */}
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', margin: '16px 0' }}>
              <div style={{ width: 2, height: 20, background: '#d0cdc8' }} />
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, background: '#e8f5f2', border: '1.5px solid rgba(42,125,111,0.3)', borderRadius: 20, padding: '6px 14px' }}>
                <span style={{ fontSize: 12, fontWeight: 700, color: '#1a6358', letterSpacing: '0.05em' }}>REWRITE IT</span>
              </div>
              <div style={{ width: 2, height: 20, background: '#d0cdc8' }} />
              <svg width="16" height="10" viewBox="0 0 16 10" fill="none">
                <path d="M1 1L8 8L15 1" stroke="#2A7D6F" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>

            {/* Section 2 — Rewrite textarea */}
            <div className="max-w-lg mx-auto" style={{ backgroundColor: '#f0faf8', border: '2px solid #2A7D6F', borderRadius: 14, padding: 20 }}>
              <span className="inline-block text-[10px] font-bold uppercase tracking-wider mb-3" style={{ backgroundColor: '#d0ede8', color: '#1a6358', borderRadius: 20, padding: '3px 10px' }}>Your rewrite</span>
              <textarea
                value={reframe}
                onChange={e => setReframe(e.target.value)}
                placeholder="Rewrite this into something kinder and more action-focused..."
                className="w-full outline-none font-serif"
                style={{ backgroundColor: '#FFFFFF', border: '1.5px solid #d0d8d4', borderRadius: 10, padding: '14px 16px', fontSize: 15, color: '#1a1a1a', lineHeight: 1.6, minHeight: 100, resize: 'none' }}
                onFocus={(e) => { e.currentTarget.style.borderColor = '#2A7D6F'; }}
                onBlur={(e) => { e.currentTarget.style.borderColor = '#d0d8d4'; }}
              />

              {/* Section 3 — Quality detection chips */}
              <p className="text-[10px] font-semibold uppercase tracking-wider mt-4 mb-2" style={{ color: '#9e9186', letterSpacing: '0.08em' }}>Qualities detected in your rewrite</p>
              <div className="flex flex-wrap gap-2">
                {qualities.map(q => (
                  <motion.span
                    key={q.label}
                    animate={q.detected ? { scale: [1, 1.05, 1] } : {}}
                    transition={{ duration: 0.3 }}
                    className="inline-flex items-center gap-2"
                    style={{
                      backgroundColor: q.detected ? '#e8f5f2' : '#FFFFFF',
                      border: q.detected ? '2px solid #2A7D6F' : '2px solid #d0cdc8',
                      borderRadius: 20,
                      padding: '8px 16px',
                    }}
                  >
                    <span className="w-2 h-2 rounded-full" style={{ backgroundColor: q.detected ? '#2A7D6F' : '#d0cdc8' }} />
                    <span className="text-[13px] font-semibold" style={{ color: q.detected ? '#1a6358' : '#b0a898' }}>
                      {q.detected && <span style={{ color: '#2A7D6F', fontWeight: 700, marginRight: 4 }}>✓</span>}
                      {q.label}
                    </span>
                  </motion.span>
                ))}
              </div>

              {/* Completion state */}
              {allDetected && (
                <motion.div
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  style={{ marginTop: 16, background: '#e8f5f2', border: '2px solid #2A7D6F', borderRadius: 14, padding: '16px 20px', display: 'flex', alignItems: 'center', gap: 12 }}
                >
                  <div style={{ width: 36, height: 36, borderRadius: '50%', background: '#2A7D6F', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0, fontSize: 18, color: 'white' }}>✓</div>
                  <div>
                    <p style={{ fontSize: 14, fontWeight: 700, color: '#1a6358', marginBottom: 2 }}>Circuit broken.</p>
                    <p style={{ fontSize: 13, color: '#2A7D6F' }}>You rewrote a harmful thought into something that actually helps you move forward.</p>
                  </div>
                </motion.div>
              )}
            </div>
        </div>
    );
}

// --- MODULE COMPONENT ---
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

  const essentials = useEssentialsMode();
  const { northStar } = useNorthStar();

  return (
    <ModuleLayout
      moduleNumber="11"
      moduleTitle="Understanding Procrastination"
      moduleSubtitle="The Architecture of Delay"
      moduleDescription={`Procrastination isn't laziness -- your brain is just wired to avoid things that feel bad. Once you understand what's actually going on, you can start beating it.`}
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Get Moving"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Real Reason You Delay." eyebrow="Step 1" icon={HeartPulse} theme={theme}>
              {essentials ? (
                <>
                  <p>Procrastination is not laziness. It is an <Highlight description="Your brain would rather feel okay right now than do something hard for later. You're not dodging the task itself -- you're dodging the bad feeling the task gives you." theme={theme}>emotional regulation problem</Highlight>. You avoid tasks because they feel bad. Your brain is protecting you from a perceived threat. A maths book is not a real threat. But your brain treats it like one. You are not broken. Once you understand this, you can start fixing it.</p>
                </>
              ) : (
                <>
                  <p>Procrastination is not laziness. It is an <Highlight description="Your brain would rather feel okay right now than do something hard for later. You're not dodging the task itself -- you're dodging the bad feeling the task gives you." theme={theme}>emotional regulation problem</Highlight>. When you look at a maths textbook and feel a wave of dread, your brain's primary goal shifts from "learn calculus" to "make this feeling go away." The easiest way to do that? Avoid the task entirely.</p>
                  <p>This is a critical reframe. You are not broken or lazy. Your brain is doing exactly what it's designed to do: protect you from perceived threats. The problem is that it has miscategorized a maths book as a threat. Understanding this is the first step to dismantling the cycle.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Amygdala Hijack." eyebrow="Step 2" icon={Brain} theme={theme}>
              {essentials ? (
                <>
                  <p>Two parts of your brain are fighting. Your <Highlight description="The part of your brain that acts like a smoke alarm. It goes off when it senses danger -- and unfortunately, it treats a hard maths problem the same as an actual threat." theme={theme}>amygdala</Highlight> is your alarm system. It panics at hard tasks. Your <Highlight description="The boss of your brain -- it handles planning, self-control, and thinking about the future. The catch? At your age, it's still being built, so your alarm system can easily overrule it." theme={theme}>Prefrontal Cortex (PFC)</Highlight> handles planning and self-control. At your age, the PFC is still being built. So your alarm system often wins. This is an <Highlight description="When your emotional brain completely takes over your logical brain. It's why you can know you should be studying but still end up scrolling your phone without even deciding to." theme={theme}>Amygdala Hijack</Highlight>. "Just try harder" will not fix this. You need smarter tricks.</p>
                </>
              ) : (
                <>
                  <p>Procrastination is basically a tug-of-war inside your head between two parts of your brain. Your <Highlight description="The part of your brain that acts like a smoke alarm. It goes off when it senses danger -- and unfortunately, it treats a hard maths problem the same as an actual threat." theme={theme}>amygdala</Highlight> (the alarm system) freaks out when it spots something that feels threatening. Your <Highlight description="The boss of your brain -- it handles planning, self-control, and thinking about the future. The catch? At your age, it's still being built, so your alarm system can easily overrule it." theme={theme}>Prefrontal Cortex (PFC)</Highlight> (the boss) is supposed to step in and calm things down, but at your age, it's still being built -- so it often loses the fight.</p>
                  <p>The result is an <Highlight description="When your emotional brain completely takes over your logical brain. It's why you can know you should be studying but still end up scrolling your phone without even deciding to." theme={theme}>Amygdala Hijack</Highlight>. Your emotional brain steamrolls your logical brain. That's why "just try harder" is useless advice. You need tricks that work <em>with</em> how your brain actually works, not against it.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Procrastination Equation." eyebrow="Step 3" icon={Calculator} theme={theme}>
              {essentials ? (
                <p>Procrastination follows a formula: <Highlight description="Your motivation comes down to four things you can actually control: how confident you feel, how much the task matters to you, how easily you get distracted, and how far away the deadline is." theme={theme}>Motivation = (Expectancy x Value) / (Impulsiveness x Delay)</Highlight>. You have four levers. Boost your confidence (E) and make tasks meaningful (V). Reduce distractions (I) and shorten deadlines (D). Use the interactive tool below to see how each lever affects your motivation.</p>
              ) : (
                <p>There's actually a formula that explains procrastination: <Highlight description="Your motivation comes down to four things you can actually control: how confident you feel, how much the task matters to you, how easily you get distracted, and how far away the deadline is." theme={theme}>Motivation = (Expectancy x Value) / (Impulsiveness x Delay)</Highlight>. This gives you four levers to pull.</p>
              )}
              <div className="my-10 rounded-2xl p-5 md:p-6 space-y-3" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#93C5FD', border: '2.5px solid #2563EB', borderRadius: 16, boxShadow: '4px 4px 0px 0px #2563EB' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#2563EB' }}>E</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#1E3A8A' }}>Expectancy</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#1E3A8A', opacity: 0.8 }}>Your belief you can succeed. Low confidence = high procrastination.</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#FCD34D', border: '2.5px solid #D97706', borderRadius: 16, boxShadow: '4px 4px 0px 0px #D97706' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#D97706' }}>V</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#78350F' }}>Value</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#78350F', opacity: 0.8 }}>How rewarding or meaningful the task feels.</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#FDBA74', border: '2.5px solid #EA580C', borderRadius: 16, boxShadow: '4px 4px 0px 0px #EA580C' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#EA580C' }}>I</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#7C2D12' }}>Impulsiveness</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#7C2D12', opacity: 0.8 }}>Your susceptibility to distractions.</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#6EE7B7', border: '2.5px solid #059669', borderRadius: 16, boxShadow: '4px 4px 0px 0px #059669' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#059669' }}>D</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#064E3B' }}>Delay</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#064E3B', opacity: 0.8 }}>How far away the deadline is. A task that is boring, feels impossible, is easily interrupted, and has a distant deadline is a recipe for maximum procrastination.</p>
                  </div>
                </div>
              </div>
              <ProcrastinationEquation />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Ego's Defence System." eyebrow="Step 4" icon={Shield} theme={theme}>
              {essentials ? (
                <>
                  <p>Procrastination is a <Highlight description="A sneaky way your brain protects your self-image. If you don't try, you can always blame the result on not trying -- which feels way less scary than trying your best and still falling short." theme={theme}>self-handicapping strategy</Highlight>. If you don't try, you can blame the bad result on not trying. That feels safer than trying and failing. The fix is a <Highlight description="Believing that you can get better at things through effort. When you think this way, a bad result just means 'I need more practice' instead of 'I'm not smart enough.'" theme={theme}>Growth Mindset</Highlight>. A bad result just means "I need more practice." It makes failure safe. You stop avoiding tasks.</p>
                </>
              ) : (
                <>
                  <p>Procrastination is also a <Highlight description="A sneaky way your brain protects your self-image. If you don't try, you can always blame the result on not trying -- which feels way less scary than trying your best and still falling short." theme={theme}>self-handicapping strategy</Highlight>. If you don't study and get a bad grade, you can tell yourself: "Well, I didn't really try." This protects your ego from the more terrifying conclusion: "I tried my best and I'm still not good enough."</p>
                  <p>It's a bad deal. You trade long-term success for short-term comfort. But once you spot the pattern, you can break it. The fix is a <Highlight description="Believing that you can get better at things through effort. When you think this way, a bad result just means 'I need more practice' instead of 'I'm not smart enough.'" theme={theme}>Growth Mindset</Highlight> -- which makes it safe to fail, because a bad result just means "I need to try differently" instead of "I'm not good enough."</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Guilt Cycle." eyebrow="Step 5" icon={RotateCcw} theme={theme}>
              {northStar && (() => { const p = COMPACT_CALLOUT_PLACEMENTS.find(p => p.moduleId === 'procrastination-protocol'); return p ? <NorthStarCallout northStar={northStar} variant="compact" message={p.message} /> : null; })()}
              {essentials ? (
                <>
                  <p>Self-criticism after procrastinating feels responsible. It is the worst response. It creates <Highlight description="That horrible sinking feeling after you've wasted time. The cruel twist is that feeling guilty makes you want to avoid even more, which creates even more guilt. It feeds itself." theme={theme}>guilt and shame</Highlight>. Guilt is a negative emotion. Your brain avoids negative emotions by procrastinating more. This creates a spiral: procrastinate, feel guilty, procrastinate more. Tough love makes it worse.</p>
                </>
              ) : (
                <>
                  <p>Most people respond to procrastination with self-criticism: "I'm so lazy. What's wrong with me?" This feels like accountability, but it's actually the worst thing you can do. Self-criticism generates <Highlight description="That horrible sinking feeling after you've wasted time. The cruel twist is that feeling guilty makes you want to avoid even more, which creates even more guilt. It feeds itself." theme={theme}>guilt and shame</Highlight>, which are negative emotions. And what does your brain do with negative emotions? It tries to avoid them--by procrastinating more.</p>
                  <p>This creates a vicious downward spiral: Procrastinate &#8594; Feel Guilty &#8594; More Negative Emotion &#8594; Procrastinate More &#8594; Feel More Guilty. "Tough love" doesn't break this cycle; it accelerates it.</p>
                </>
              )}
              <GuiltSpiralComparison />
              <GuiltSpiral />
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="The Forgiveness Protocol." eyebrow="Step 6" icon={HeartHandshake} theme={theme}>
              {essentials ? (
                <>
                  <p><Highlight description="Letting go of the guilt instead of beating yourself up. It sounds soft, but students who forgive themselves for procrastinating actually procrastinate less the next time. The guilt is what keeps you stuck." theme={theme}>Self-Forgiveness</Highlight> breaks the guilt spiral. Students who forgave themselves procrastinated less next time. This is not letting yourself off the hook. It breaks the emotional chain. Use this script: "I procrastinated. That is human. I forgive myself. What is the smallest step I can take right now?"</p>
                </>
              ) : (
                <>
                  <p>The thing that actually breaks the guilt spiral is <Highlight description="Letting go of the guilt instead of beating yourself up. It sounds soft, but students who forgive themselves for procrastinating actually procrastinate less the next time. The guilt is what keeps you stuck." theme={theme}>Self-Forgiveness</Highlight>. It sounds too simple, but it works: students who forgave themselves for procrastinating before one exam were way less likely to procrastinate before the next one.</p>
                  <p>This isn't about letting yourself off the hook. It's about breaking the emotional chain reaction. The script is simple: "I procrastinated. That's a human thing to do. I forgive myself. Now, what is the smallest possible step I can take right now?"</p>
                </>
              )}
              <CircuitBreaker />
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="The 'If-Then' Protocol." eyebrow="Step 7" icon={Zap} theme={theme}>
              <p>Willpower runs out, especially when you're tired or stressed. So the best trick is to stop relying on willpower altogether and use an <Highlight description="You decide in advance what you'll do when a specific situation comes up. Because you've already made the decision, you don't have to fight yourself in the moment -- it just happens." theme={theme}>"If-Then" Plan</Highlight>. You make the decision ahead of time, so when the moment comes, there's nothing to argue about -- you just do the thing.</p>
              <p>The formula: <strong>IF</strong> [Trigger/Situation], <strong>THEN</strong> I will [Specific Action]. For example: "IF it is 4:30 PM, THEN I will open my Maths textbook to page 1 and do the first question." The key is to make the action tiny and specific. You're not committing to "study Maths for 2 hours." You're committing to opening a book.</p>
              <IfThenAutopilot />
            </ReadingSection>
          )}
          {activeSection === 7 && (
            <ReadingSection title="Scaffolding Your Focus." eyebrow="Step 8" icon={Wrench} theme={theme}>
              <p>Now you have the mental tools. The last step is to set up your environment so that starting is easy and staying focused happens naturally. Use things like the <Highlight description="Work for 25 minutes, then take a 5-minute break. That's it. Knowing you only have to focus for 25 minutes makes it way easier to actually start." theme={theme}>Pomodoro Technique</Highlight> to make tasks feel manageable, and set up your space so distractions aren't within arm's reach.</p>
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
