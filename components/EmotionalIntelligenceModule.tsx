/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Cpu, Brain, Heart, Zap, Shield, Utensils, ClipboardCheck
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { cyanTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = cyanTheme;

// --- INTERACTIVE COMPONENTS ---
const StressResponseComparison = () => {
    const [revealed, setRevealed] = useState(false);

    const W = 540, H = 280;
    const padL = 8, padR = 8, padT = 28, padB = 56;
    const chartW = W - padL - padR, chartH = H - padT - padB;
    const toX = (f: number) => padL + f * chartW;
    const toY = (f: number) => padT + (1 - f) * chartH;

    const labels = ['Calm', 'Mild stress', 'Moderate', 'High stress', 'Panic', 'Meltdown'];
    const pfcData = [0.90, 0.82, 0.68, 0.45, 0.25, 0.12];
    const amygData = [0.10, 0.22, 0.40, 0.62, 0.82, 0.95];

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

    const phases = [
        { label: 'Thinking zone', x1: 0, x2: 0.33, color: '#10b981' },
        { label: 'Tipping point', x1: 0.33, x2: 0.66, color: '#f59e0b' },
        { label: 'Survival mode', x1: 0.66, x2: 1, color: '#ef4444' },
    ];

    const Chart = () => (
        <svg viewBox={`0 0 ${W} ${H}`} className="w-full">
            <defs>
                <linearGradient id="pfc-grad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#10b981" stopOpacity="0.4" />
                    <stop offset="100%" stopColor="#10b981" stopOpacity="0.03" />
                </linearGradient>
                <linearGradient id="amyg-grad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#ef4444" stopOpacity="0.4" />
                    <stop offset="100%" stopColor="#ef4444" stopOpacity="0.03" />
                </linearGradient>
            </defs>
            {/* Grid lines */}
            {[0.25, 0.5, 0.75, 1.0].map(v => (
                <line key={v} x1={padL} x2={W - padR} y1={toY(v)} y2={toY(v)} stroke="#a1a1aa" strokeOpacity="0.15" strokeDasharray="3 3" />
            ))}
            {/* Baseline */}
            <line x1={padL} x2={W - padR} y1={toY(0)} y2={toY(0)} stroke="#a1a1aa" strokeOpacity="0.3" />
            {/* PFC area */}
            <motion.path
                d={buildArea(pfcData)}
                fill="url(#pfc-grad)"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.8 }}
            />
            {/* Amygdala area */}
            <motion.path
                d={buildArea(amygData)}
                fill="url(#amyg-grad)"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.8, delay: 0.15 }}
            />
            {/* PFC line */}
            <motion.path
                d={buildLine(pfcData)}
                fill="none" stroke="#10b981" strokeWidth="2.5" strokeLinecap="round"
                initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                transition={{ duration: 1.2, ease: 'easeOut' }}
            />
            {/* Amygdala line */}
            <motion.path
                d={buildLine(amygData)}
                fill="none" stroke="#ef4444" strokeWidth="2.5" strokeLinecap="round"
                initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                transition={{ duration: 1.2, ease: 'easeOut', delay: 0.3 }}
            />
            {/* PFC dots */}
            {pfcData.map((v, i) => (
                <motion.circle key={`pfc-${i}`} cx={toX(i / (pfcData.length - 1))} cy={toY(v)} r="3.5" fill="#10b981"
                    initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2 * i + 0.3 }}
                />
            ))}
            {/* Amygdala dots */}
            {amygData.map((v, i) => (
                <motion.circle key={`amyg-${i}`} cx={toX(i / (amygData.length - 1))} cy={toY(v)} r="3.5" fill="#ef4444"
                    initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2 * i + 0.5 }}
                />
            ))}
            {/* Y-axis labels */}
            <text x={padL + 2} y={toY(1.0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">High</text>
            <text x={padL + 2} y={toY(0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">Low</text>
            {/* X-axis labels */}
            {labels.map((m, i) => (
                <text key={m} x={toX(i / (labels.length - 1))} y={toY(0) + 14} fontSize="8" fill="#a1a1aa" textAnchor="middle" fontWeight="600">{m}</text>
            ))}
            {/* Phase labels */}
            {phases.map((p, i) => (
                <text key={i} x={toX((p.x1 + p.x2) / 2)} y={toY(0) + 28} fontSize="8" fill={p.color} textAnchor="middle" fontWeight="700">{p.label}</text>
            ))}
            {/* Chart label */}
            <text x={W / 2} y={14} fontSize="11" fill="#71717a" textAnchor="middle" fontWeight="700">Brain Activity Under Exam Stress</text>
            {/* Legend */}
            <line x1={W - padR - 168} x2={W - padR - 152} y1={14} y2={14} stroke="#10b981" strokeWidth="2" />
            <text x={W - padR - 148} y={17} fontSize="8" fill="#a1a1aa">Prefrontal Cortex</text>
            <line x1={W - padR - 64} x2={W - padR - 48} y1={14} y2={14} stroke="#ef4444" strokeWidth="2" />
            <text x={W - padR - 44} y={17} fontSize="8" fill="#a1a1aa">Amygdala</text>
        </svg>
    );

    return (
        <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Neural Tug of War</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">As stress rises, your thinking brain loses the battle.</p>

            {!revealed ? (
                <div className="text-center">
                    <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">Your brain has two competing systems fighting for control during an exam. What happens as the pressure builds?</p>
                    <button onClick={() => setRevealed(true)} className="px-5 py-2.5 text-sm font-bold rounded-lg bg-sky-500 text-white hover:bg-sky-600 transition-colors">
                        See the Neural Shift
                    </button>
                </div>
            ) : (
                <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
                    <div className="mb-5">
                        <div className="rounded-lg border border-zinc-200 dark:border-zinc-700 bg-zinc-50/50 dark:bg-zinc-900/20 p-3">
                            <Chart />
                        </div>
                    </div>
                    <div className="grid md:grid-cols-2 gap-4 text-sm">
                        <div className="flex items-start gap-2.5 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900">
                            <span className="text-emerald-500 text-lg mt-0.5">&#x1F9E0;</span>
                            <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-emerald-600 dark:text-emerald-400">Your PFC</strong> handles planning, working memory, and rational thinking. It's your exam brain. But it shuts down as cortisol rises.</p>
                        </div>
                        <div className="flex items-start gap-2.5 p-3 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900">
                            <span className="text-rose-500 text-lg mt-0.5">&#x26A1;</span>
                            <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-rose-600 dark:text-rose-400">Your amygdala</strong> handles threat detection and survival. It hijacks control when stress crosses the tipping point. You can't think clearly in survival mode.</p>
                        </div>
                    </div>
                </motion.div>
            )}
        </div>
    );
};

const PFCShutdownSimulator = () => {
    const [stressed, setStressed] = useState(false);

    const capabilities = [
      { label: 'Memory Retrieval', desc: 'Access to stored knowledge' },
      { label: 'Logical Reasoning', desc: 'Problem-solving and analysis' },
      { label: 'Planning & Strategy', desc: 'Organising and sequencing' },
    ];

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">PFC Shutdown Simulator</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">See what happens when your Amygdala hijacks your brain under exam stress.</p>

             <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
               {/* Amygdala panel */}
               <div className={`p-5 rounded-xl border transition-all duration-500 ${
                 stressed
                   ? 'bg-rose-50 dark:bg-rose-950/30 border-rose-300 dark:border-rose-800'
                   : 'bg-zinc-50 dark:bg-zinc-900/30 border-zinc-200 dark:border-zinc-700'
               }`}>
                 <div className="flex items-center gap-3 mb-3">
                   <motion.div
                     animate={stressed ? { scale: [1, 1.15, 1] } : { scale: 1 }}
                     transition={stressed ? { duration: 1.2, repeat: Infinity } : {}}
                     className={`w-10 h-10 rounded-full flex items-center justify-center ${
                       stressed ? 'bg-rose-500 text-white' : 'bg-zinc-200 dark:bg-zinc-700 text-zinc-500'
                     }`}
                   >
                     <Zap size={20} />
                   </motion.div>
                   <div>
                     <p className="font-bold text-sm text-zinc-800 dark:text-white">Amygdala</p>
                     <p className="text-[10px] text-zinc-400 dark:text-zinc-500">Threat Detection</p>
                   </div>
                 </div>
                 <motion.div
                   animate={{ width: stressed ? '100%' : '20%' }}
                   transition={{ duration: 0.8, ease: 'easeOut' }}
                   className={`h-2 rounded-full ${stressed ? 'bg-rose-500' : 'bg-zinc-300 dark:bg-zinc-600'}`}
                 />
                 <p className={`text-xs font-semibold mt-2 ${stressed ? 'text-rose-500' : 'text-zinc-400'}`}>
                   {stressed ? 'ACTIVE — Flooding cortisol' : 'Standby'}
                 </p>
               </div>

               {/* PFC panel */}
               <div className={`p-5 rounded-xl border transition-all duration-500 ${
                 stressed
                   ? 'bg-zinc-100 dark:bg-zinc-900/50 border-zinc-200 dark:border-zinc-800'
                   : 'bg-blue-50 dark:bg-blue-950/20 border-blue-200 dark:border-blue-800/50'
               }`}>
                 <div className="flex items-center gap-3 mb-3">
                   <motion.div
                     animate={{ opacity: stressed ? 0.3 : 1 }}
                     transition={{ duration: 0.5 }}
                     className={`w-10 h-10 rounded-full flex items-center justify-center ${
                       stressed ? 'bg-zinc-300 dark:bg-zinc-700 text-zinc-500' : 'bg-blue-500 text-white'
                     }`}
                   >
                     <Brain size={20} />
                   </motion.div>
                   <div>
                     <p className="font-bold text-sm text-zinc-800 dark:text-white">Prefrontal Cortex</p>
                     <p className="text-[10px] text-zinc-400 dark:text-zinc-500">Command Centre</p>
                   </div>
                 </div>
                 <div className="space-y-2">
                   {capabilities.map((cap, i) => (
                     <motion.div
                       key={cap.label}
                       animate={stressed
                         ? { opacity: 0.3, x: 4 }
                         : { opacity: 1, x: 0 }
                       }
                       transition={{ duration: 0.4, delay: stressed ? i * 0.3 : (2 - i) * 0.2 }}
                       className="flex items-center justify-between"
                     >
                       <div>
                         <p className="text-xs font-semibold text-zinc-700 dark:text-zinc-300">{cap.label}</p>
                         <p className="text-[10px] text-zinc-400 dark:text-zinc-500">{cap.desc}</p>
                       </div>
                       <motion.span
                         animate={stressed
                           ? { opacity: 1 }
                           : { opacity: 1 }
                         }
                         transition={{ duration: 0.3, delay: stressed ? i * 0.3 : (2 - i) * 0.2 }}
                         className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                           stressed
                             ? 'bg-rose-100 dark:bg-rose-900/40 text-rose-600 dark:text-rose-400'
                             : 'bg-emerald-100 dark:bg-emerald-900/40 text-emerald-600 dark:text-emerald-400'
                         }`}
                       >
                         {stressed ? 'OFFLINE' : 'ONLINE'}
                       </motion.span>
                     </motion.div>
                   ))}
                 </div>
               </div>
             </div>

             {/* Cortisol wave */}
             {stressed && (
               <motion.div
                 initial={{ opacity: 0, y: 6 }}
                 animate={{ opacity: 1, y: 0 }}
                 className="p-3 mb-6 bg-rose-50 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-800/50 rounded-xl text-center"
               >
                 <p className="text-xs text-rose-600 dark:text-rose-400 font-medium">
                   Cortisol is blocking the connection between your PFC and your stored knowledge. Your memory isn't gone — the pathway is temporarily offline.
                 </p>
               </motion.div>
             )}

             <div className="flex justify-center">
               <button
                 onClick={() => setStressed(!stressed)}
                 className={`px-6 py-2.5 font-bold text-sm rounded-xl transition-all ${
                   stressed
                     ? 'bg-blue-500 text-white hover:bg-blue-600 shadow-lg shadow-blue-500/20'
                     : 'bg-rose-500 text-white hover:bg-rose-600 shadow-lg shadow-rose-500/20'
                 }`}
               >
                 {stressed ? 'De-escalate' : 'Trigger Stress Response'}
               </button>
             </div>
        </div>
    );
}

const ArousalReappraisal = () => {
    const [attempt, setAttempt] = useState<'none' | 'calm' | 'reframe'>('none');
    const [animKey, setAnimKey] = useState(0);

    const handleAttempt = (type: 'calm' | 'reframe') => {
      setAttempt(type);
      setAnimKey(k => k + 1);
    };

    // Grid positions (percentage-based)
    // X: Valence (0=negative, 100=positive)
    // Y: Arousal (0=high, 100=low) — inverted so high arousal is at top
    const emotions = {
      anxiety:    { x: 15, y: 12, label: 'Anxiety',    color: 'bg-rose-500' },
      excitement: { x: 85, y: 12, label: 'Excitement', color: 'bg-emerald-500' },
      calm:       { x: 85, y: 85, label: 'Calm',       color: 'bg-blue-500' },
      boredom:    { x: 15, y: 85, label: 'Boredom',    color: 'bg-zinc-400' },
    };

    // Dot target
    const dotTarget = attempt === 'reframe'
      ? { x: emotions.excitement.x, y: emotions.excitement.y }
      : attempt === 'calm'
        ? { x: 50, y: 50 } // gets stuck halfway
        : { x: emotions.anxiety.x, y: emotions.anxiety.y };

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Arousal Reappraisal</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-2">Scenario: Your heart is racing before an exam. What do you do?</p>
             <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 mb-6">The emotion map shows two dimensions: how activated you feel (arousal) and whether it feels good or bad (valence).</p>

             {/* Emotion grid */}
             <div className="relative w-full aspect-square max-w-sm mx-auto mb-6">
               {/* Background quadrants */}
               <div className="absolute inset-0 grid grid-cols-2 grid-rows-2 rounded-xl overflow-hidden">
                 <div className="bg-rose-50 dark:bg-rose-950/15" />
                 <div className="bg-emerald-50 dark:bg-emerald-950/15" />
                 <div className="bg-zinc-50 dark:bg-zinc-800/30" />
                 <div className="bg-blue-50 dark:bg-blue-950/15" />
               </div>

               {/* Axis labels */}
               <div className="absolute top-2 left-1/2 -translate-x-1/2 text-[9px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">High Arousal</div>
               <div className="absolute bottom-2 left-1/2 -translate-x-1/2 text-[9px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Low Arousal</div>
               <div className="absolute left-2 top-1/2 -translate-y-1/2 text-[9px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 [writing-mode:vertical-lr] rotate-180">Negative</div>
               <div className="absolute right-2 top-1/2 -translate-y-1/2 text-[9px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 [writing-mode:vertical-lr]">Positive</div>

               {/* Axis lines */}
               <div className="absolute left-1/2 top-0 bottom-0 w-px bg-zinc-200 dark:bg-zinc-700" />
               <div className="absolute top-1/2 left-0 right-0 h-px bg-zinc-200 dark:bg-zinc-700" />

               {/* Emotion labels */}
               {Object.values(emotions).map(e => (
                 <div key={e.label} className="absolute" style={{ left: `${e.x}%`, top: `${e.y}%`, transform: 'translate(-50%, -50%)' }}>
                   <div className={`w-3 h-3 rounded-full ${e.color} mx-auto mb-1`} />
                   <p className="text-[10px] font-bold text-zinc-600 dark:text-zinc-300 text-center whitespace-nowrap">{e.label}</p>
                 </div>
               ))}

               {/* Animated "You" dot */}
               <motion.div
                 key={animKey}
                 initial={{ left: `${emotions.anxiety.x}%`, top: `${emotions.anxiety.y}%` }}
                 animate={{ left: `${dotTarget.x}%`, top: `${dotTarget.y}%` }}
                 transition={attempt === 'calm'
                   ? { duration: 1.5, ease: 'easeOut' }
                   : { duration: 0.6, ease: [0.16, 1, 0.3, 1] }
                 }
                 className="absolute z-10"
                 style={{ transform: 'translate(-50%, -50%)' }}
               >
                 <div className="relative">
                   <div className={`w-6 h-6 rounded-full border-2 border-white shadow-lg ${
                     attempt === 'reframe' ? 'bg-emerald-500' : attempt === 'calm' ? 'bg-amber-500' : 'bg-rose-500'
                   }`} />
                   <p className="absolute -bottom-5 left-1/2 -translate-x-1/2 text-[9px] font-bold text-zinc-500 dark:text-zinc-400 whitespace-nowrap">YOU</p>
                 </div>
               </motion.div>

               {/* Path trails */}
               {attempt === 'reframe' && (
                 <motion.div
                   key={`trail-r-${animKey}`}
                   initial={{ opacity: 0 }}
                   animate={{ opacity: 0.6 }}
                   transition={{ delay: 0.3 }}
                   className="absolute top-0 left-0 w-full h-full pointer-events-none"
                 >
                   <svg className="w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
                     <motion.line
                       x1={emotions.anxiety.x} y1={emotions.anxiety.y}
                       x2={emotions.excitement.x} y2={emotions.excitement.y}
                       stroke="#10b981" strokeWidth="0.8" strokeDasharray="2 2"
                       initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                       transition={{ duration: 0.5 }}
                     />
                   </svg>
                   <div className="absolute text-[8px] font-bold text-emerald-500" style={{ left: '50%', top: `${emotions.anxiety.y}%`, transform: 'translate(-50%, -150%)' }}>
                     Short path (same arousal)
                   </div>
                 </motion.div>
               )}
               {attempt === 'calm' && (
                 <motion.div
                   key={`trail-c-${animKey}`}
                   initial={{ opacity: 0 }}
                   animate={{ opacity: 0.6 }}
                   transition={{ delay: 0.3 }}
                   className="absolute top-0 left-0 w-full h-full pointer-events-none"
                 >
                   <svg className="w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
                     <motion.line
                       x1={emotions.anxiety.x} y1={emotions.anxiety.y}
                       x2={emotions.calm.x} y2={emotions.calm.y}
                       stroke="#f59e0b" strokeWidth="0.8" strokeDasharray="2 2"
                       initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                       transition={{ duration: 1.2 }}
                     />
                   </svg>
                   <div className="absolute text-[8px] font-bold text-amber-500" style={{ left: '55%', top: '50%', transform: 'translate(-50%, -50%)' }}>
                     Long path (change arousal)
                   </div>
                 </motion.div>
               )}
             </div>

             {/* Buttons */}
             <div className="grid grid-cols-2 gap-3 mb-4">
               <button
                 onClick={() => handleAttempt('calm')}
                 className={`p-4 rounded-xl text-left text-sm font-medium transition-all border ${
                   attempt === 'calm'
                     ? 'bg-amber-50 dark:bg-amber-950/20 border-amber-300 dark:border-amber-800'
                     : 'bg-zinc-50 dark:bg-zinc-900/30 border-zinc-200 dark:border-zinc-700 hover:border-zinc-300 dark:hover:border-zinc-600'
                 }`}
               >
                 <p className="font-bold text-zinc-800 dark:text-white">"Calm down."</p>
                 <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">Try to lower your arousal</p>
               </button>
               <button
                 onClick={() => handleAttempt('reframe')}
                 className={`p-4 rounded-xl text-left text-sm font-medium transition-all border ${
                   attempt === 'reframe'
                     ? 'bg-emerald-50 dark:bg-emerald-950/20 border-emerald-300 dark:border-emerald-800'
                     : 'bg-zinc-50 dark:bg-zinc-900/30 border-zinc-200 dark:border-zinc-700 hover:border-zinc-300 dark:hover:border-zinc-600'
                 }`}
               >
                 <p className="font-bold text-zinc-800 dark:text-white">"I'm excited!"</p>
                 <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">Reframe the same arousal</p>
               </button>
             </div>

             {/* Result insight */}
             <AnimatePresence mode="wait">
               {attempt === 'calm' && (
                 <motion.div key="calm-result" initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                   className="p-4 bg-amber-50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-800/50 rounded-xl text-sm"
                 >
                   <p className="font-bold text-amber-700 dark:text-amber-300 mb-1">Difficult path.</p>
                   <p className="text-amber-600 dark:text-amber-400 text-xs">Telling yourself to "calm down" requires changing your entire arousal state — fighting your physiology. Your body is flooded with adrenaline; you can't just switch it off by willpower. The dot gets stuck halfway.</p>
                 </motion.div>
               )}
               {attempt === 'reframe' && (
                 <motion.div key="reframe-result" initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                   className="p-4 bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-800/50 rounded-xl text-sm"
                 >
                   <p className="font-bold text-emerald-700 dark:text-emerald-300 mb-1">Easy path.</p>
                   <p className="text-emerald-600 dark:text-emerald-400 text-xs">Anxiety and excitement are physiologically identical — same racing heart, same adrenaline. You only need to change the label, not the state. Research shows saying "I'm excited" before a test improves performance significantly.</p>
                 </motion.div>
               )}
             </AnimatePresence>
        </div>
    );
};

const BoxBreathing = () => {
    const [active, setActive] = useState(false);
    const [phase, setPhase] = useState(0); // 0=inhale, 1=hold, 2=exhale, 3=hold
    const [count, setCount] = useState(4);
    const [cycle, setCycle] = useState(0);
    const totalCycles = 3;

    const phases = [
      { label: 'Breathe In', color: 'text-cyan-500' },
      { label: 'Hold', color: 'text-sky-400' },
      { label: 'Breathe Out', color: 'text-teal-500' },
      { label: 'Hold', color: 'text-sky-400' },
    ];

    // Ring arc: each phase is a quarter of the circle
    const arcColors = ['#06b6d4', '#38bdf8', '#14b8a6', '#38bdf8']; // cyan, sky, teal, sky
    const radius = 88;
    const circumference = 2 * Math.PI * radius;
    const quarterArc = circumference / 4;

    const getArcPath = (index: number) => {
      const startAngle = (index * 90 - 90) * (Math.PI / 180);
      const endAngle = ((index + 1) * 90 - 90) * (Math.PI / 180);
      const x1 = 100 + radius * Math.cos(startAngle);
      const y1 = 100 + radius * Math.sin(startAngle);
      const x2 = 100 + radius * Math.cos(endAngle);
      const y2 = 100 + radius * Math.sin(endAngle);
      return `M ${x1} ${y1} A ${radius} ${radius} 0 0 1 ${x2} ${y2}`;
    };

    // Breathing circle scale
    const breathScale = phase === 0 ? 1.3 : phase === 2 ? 0.7 : phase === 1 ? 1.3 : 0.7;

    React.useEffect(() => {
      if (!active) return;
      const interval = setInterval(() => {
        setCount(c => {
          if (c <= 1) {
            setPhase(p => {
              const next = (p + 1) % 4;
              if (next === 0) {
                setCycle(cy => {
                  if (cy + 1 >= totalCycles) {
                    setActive(false);
                    return 0;
                  }
                  return cy + 1;
                });
              }
              return next;
            });
            return 4;
          }
          return c - 1;
        });
      }, 1000);
      return () => clearInterval(interval);
    }, [active]);

    const handleStart = () => {
      setPhase(0);
      setCount(4);
      setCycle(0);
      setActive(true);
    };

    const done = !active && cycle === 0 && phase === 0;

    return (
     <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
         <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Box Breathing</h4>
         <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Your emergency protocol for the exam hall. 4 seconds per phase, 3 cycles.</p>

         <div className="flex justify-center mb-6">
           <div className="relative w-52 h-52">
             {/* Outer phase ring */}
             <svg viewBox="0 0 200 200" className="w-full h-full absolute inset-0">
               {[0, 1, 2, 3].map(i => (
                 <motion.path
                   key={i}
                   d={getArcPath(i)}
                   fill="none"
                   stroke={arcColors[i]}
                   strokeWidth={active && i === phase ? 6 : 3}
                   strokeLinecap="round"
                   animate={{
                     opacity: active ? (i === phase ? 1 : 0.2) : 0.15,
                     strokeWidth: active && i === phase ? 6 : 3,
                   }}
                   transition={{ duration: 0.4 }}
                 />
               ))}
             </svg>

             {/* Phase labels on each side */}
             <div className={`absolute -top-6 left-1/2 -translate-x-1/2 text-[9px] font-bold uppercase tracking-wider transition-opacity duration-300 ${active && phase === 0 ? 'text-cyan-500 opacity-100' : 'text-zinc-300 dark:text-zinc-600 opacity-60'}`}>Inhale</div>
             <div className={`absolute top-1/2 -right-10 -translate-y-1/2 text-[9px] font-bold uppercase tracking-wider transition-opacity duration-300 ${active && phase === 1 ? 'text-sky-400 opacity-100' : 'text-zinc-300 dark:text-zinc-600 opacity-60'}`}>Hold</div>
             <div className={`absolute -bottom-6 left-1/2 -translate-x-1/2 text-[9px] font-bold uppercase tracking-wider transition-opacity duration-300 ${active && phase === 2 ? 'text-teal-500 opacity-100' : 'text-zinc-300 dark:text-zinc-600 opacity-60'}`}>Exhale</div>
             <div className={`absolute top-1/2 -left-8 -translate-y-1/2 text-[9px] font-bold uppercase tracking-wider transition-opacity duration-300 ${active && phase === 3 ? 'text-sky-400 opacity-100' : 'text-zinc-300 dark:text-zinc-600 opacity-60'}`}>Hold</div>

             {/* Inner breathing circle */}
             <div className="absolute inset-0 flex items-center justify-center">
               <motion.div
                 animate={{
                   scale: active ? breathScale : 1,
                 }}
                 transition={{ duration: 3.8, ease: 'easeInOut' }}
                 className="w-28 h-28 rounded-full bg-cyan-50 dark:bg-cyan-950/30 border-2 border-cyan-200 dark:border-cyan-800/50 flex flex-col items-center justify-center"
               >
                 {active ? (
                   <>
                     <motion.p
                       key={`${phase}-${count}`}
                       initial={{ scale: 1.2, opacity: 0 }}
                       animate={{ scale: 1, opacity: 1 }}
                       className="text-3xl font-bold text-cyan-600 dark:text-cyan-400"
                     >
                       {count}
                     </motion.p>
                     <p className={`text-[10px] font-bold ${phases[phase].color}`}>{phases[phase].label}</p>
                   </>
                 ) : (
                   <p className="text-xs font-semibold text-zinc-400 dark:text-zinc-500">Ready</p>
                 )}
               </motion.div>
             </div>
           </div>
         </div>

         {/* Cycle progress */}
         {active && (
           <div className="flex justify-center gap-2 mb-6">
             {Array.from({ length: totalCycles }).map((_, i) => (
               <div key={i} className={`w-2 h-2 rounded-full transition-colors ${i < cycle ? 'bg-cyan-500' : i === cycle ? 'bg-cyan-300' : 'bg-zinc-200 dark:bg-zinc-700'}`} />
             ))}
           </div>
         )}

         <div className="flex justify-center">
           {!active ? (
             <button
               onClick={handleStart}
               className="px-6 py-2.5 bg-cyan-500 text-white font-bold text-sm rounded-xl hover:bg-cyan-600 shadow-lg shadow-cyan-500/20 transition-all"
             >
               {done ? 'Begin' : 'Start Again'}
             </button>
           ) : (
             <button
               onClick={() => setActive(false)}
               className="px-6 py-2.5 bg-zinc-100 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-300 font-bold text-sm rounded-xl hover:bg-zinc-200 dark:hover:bg-zinc-600 transition-all"
             >
               Stop
             </button>
           )}
         </div>
    </div>
    );
};

// --- MODULE COMPONENT ---
const EmotionalIntelligenceModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'neurobiology-stress', title: 'The Neurobiology of Stress', eyebrow: '01 // The Hardware', icon: Cpu },
    { id: 'emotional-intelligence', title: 'What is Emotional Intelligence?', eyebrow: '02 // The Software', icon: Brain },
    { id: 'self-awareness', title: 'Building Self-Awareness', eyebrow: '03 // Somatic Literacy', icon: Heart },
    { id: 'cognitive-regulation', title: 'Cognitive Regulation (Top-Down)', eyebrow: '04 // The Mind', icon: Zap },
    { id: 'physiological-regulation', title: 'Physiological Regulation (Bottom-Up)', eyebrow: '05 // The Body', icon: Shield },
    { id: 'bio-support', title: 'The Bio-Support System', eyebrow: '06 // Fuel & Maintenance', icon: Utensils },
    { id: 'integrated-timeline', title: 'The Integrated Timeline', eyebrow: '07 // The Plan', icon: ClipboardCheck },
  ];

  return (
    <ModuleLayout
      moduleNumber="13"
      moduleTitle="Emotional Intelligence"
      moduleSubtitle="The Stress Management Toolkit"
      moduleDescription={`Learn the neurobiology of exam stress and master the "top-down" and "bottom-up" strategies to transform anxiety into a high-performance state.`}
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Neurobiology of Stress." eyebrow="Step 1" icon={Cpu} theme={theme}>
              <p>Exam stress isn't a character flaw; it's a predictable neuroendocrine response. Your brain's alarm system, the <Highlight description="The Hypothalamic-Pituitary-Adrenal axis is the body's central stress response system. When a threat is perceived, it releases a cascade of hormones, culminating in cortisol." theme={theme}>HPA Axis</Highlight>, floods your system with cortisol. In the short term, this is good--it sharpens focus. But the Leaving Cert is a chronic stressor.</p>
              <p>Under chronic stress, high levels of cortisol effectively take your <Highlight description="The 'CEO' of your brain, responsible for planning, logic, and working memory. It is the last part of the brain to fully mature, making it vulnerable during adolescence." theme={theme}>Prefrontal Cortex (PFC)</Highlight> "offline." This is the biological reason for "going blank." Your brain has prioritized survival over cognition. Understanding this isn't an excuse; it's the first step to taking back control.</p>
              <StressResponseComparison />
              <PFCShutdownSimulator />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="What is Emotional Intelligence?" eyebrow="Step 2" icon={Brain} theme={theme}>
              <p><Highlight description="The capacity to be aware of, control, and express one's emotions, and to handle interpersonal relationships judiciously and empathetically." theme={theme}>Emotional Intelligence (EI)</Highlight> isn't about being "nice." In an academic context, it's a set of high-level cognitive skills for monitoring and regulating your internal state. High EI doesn't mean you don't feel stress; it means you can use that stress as fuel (<Highlight description="A positive, motivating form of stress that can improve performance." theme={theme}>eustress</Highlight>) instead of letting it become a debilitating force.</p>
              <p>For the Leaving Cert, we can break EI into three trainable skills: 1) <strong>Emotional Awareness:</strong> Noticing the physical signals of stress early. 2) <strong>Emotional Understanding:</strong> Correctly labeling the emotion. 3) <strong>Emotional Regulation:</strong> Using specific strategies to manage it.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Building Self-Awareness." eyebrow="Step 3" icon={Heart} theme={theme}>
              <p>You can't manage what you don't measure. The first step is to develop <Highlight description="The ability to read your body's internal physical signals, such as heart rate, breathing, and muscle tension." theme={theme}>Somatic Literacy</Highlight>. Your body often registers stress before your conscious mind does. These physical signals are called <Highlight description="Physical sensations (e.g., racing heart, tight stomach) that act as early warning signs for an emotional response." theme={theme}>Somatic Markers</Highlight>.</p>
              <p>A simple daily "Body Scan" can train your ability to notice these markers. By checking in with your body, you can catch the stress response early, before it cascades into a full-blown panic attack. It's about moving from "I'm freaking out" to "I am noticing the sensation of a rapid heartbeat."</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Cognitive Regulation (Top-Down)." eyebrow="Step 4" icon={Zap} theme={theme}>
              <p>Once you've noticed the feeling, you need to manage it with your mind. This is <Highlight description="Using your thoughts and beliefs (cognition) to influence your emotional state." theme={theme}>Top-Down Regulation</Highlight>. A counter-intuitive but powerful strategy is <Highlight description="The act of reinterpreting the meaning of a high-arousal state. Physiologically, anxiety and excitement are almost identical; the only difference is the cognitive label you apply." theme={theme}>Arousal Reappraisal</Highlight>. It's neurologically easier to shift from "anxious" to "excited" than it is to "calm down."</p>
              <p>The second tool is <Highlight description="A core CBT technique where you challenge the validity of your negative automatic thoughts by examining the evidence for and against them." theme={theme}>Cognitive Restructuring</Highlight>. You treat your catastrophic thought ("I'm going to fail everything") like a prosecutor's claim in a courtroom and you become the defence lawyer, looking for counter-evidence.</p>
              <ArousalReappraisal/>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Physiological Regulation (Bottom-Up)." eyebrow="Step 5" icon={Shield} theme={theme}>
              <p>Sometimes, your mind is too flooded to think straight. In these moments, you need to use your body to calm your mind. This is <Highlight description="Using physiological interventions (like breathing) to change your emotional state." theme={theme}>Bottom-Up Regulation</Highlight>. The fastest tool is breathing.</p>
              <p><Highlight description="A simple 4-4-4-4 breathing pattern that stimulates the Vagus nerve, a key part of your parasympathetic ('rest and digest') nervous system, acting as a physiological brake on the stress response." theme={theme}>Box Breathing</Highlight> is your emergency protocol for the exam hall. It's invisible and takes less than a minute to interrupt the panic loop and restore blood flow to your PFC.</p>
              <BoxBreathing />
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="The Bio-Support System." eyebrow="Step 6" icon={Utensils} theme={theme}>
              <p>Emotional regulation is biologically expensive. A tired, dehydrated, or malnourished brain cannot regulate itself effectively, no matter how good your psychological tools are. Your baseline biology is non-negotiable.</p>
              <p>The "Anti-Cortisol" diet focuses on slow-release carbs (oats) and omega-3s (fish, walnuts) to stabilize your energy. Even mild dehydration (1-2%) significantly impairs concentration. And most importantly, sleep is when your brain consolidates learning and flushes out the metabolic waste that causes "brain fog." Strategic breaks, especially using <Highlight description="Non-Sleep Deep Rest: A guided meditation protocol that rapidly reduces cortisol and replenishes dopamine, making it an ideal 'reset button' during the study day." theme={theme}>NSDR</Highlight>, are also critical for recovery.</p>
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="The Integrated Timeline." eyebrow="Step 7" icon={ClipboardCheck} theme={theme}>
              <p>You now have a complete toolkit of top-down and bottom-up strategies. The final step is to integrate them into a clear timeline.</p>
              <p><strong>Months Before:</strong> Build resilience. Practice daily Body Scans and learn Box Breathing when stress is low. <strong>Morning Of:</strong> Arousal regulation is key. Eat the "Exam Breakfast," stay away from panicked friends, and use the "Get Excited" reframe. <strong>In The Hall:</strong> If panic hits, use the "Paper Panic" drill: Stop, Breathe (3 cycles of Box Breathing), Micro-PMR (clench toes), and Re-engage with the easiest question. <strong>Post-Exam:</strong> A strict Post-Mortem Ban is essential to contain anxiety for the next paper.</p>
              <MicroCommitment theme={theme}><p>Choose one protocol from this module. Commit to practicing it for 5 minutes every day for one week. You are not just studying; you are training your nervous system.</p></MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default EmotionalIntelligenceModule;
