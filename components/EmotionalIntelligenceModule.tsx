/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Cpu, Brain, Heart, Zap, Shield, Utensils, ClipboardCheck
} from 'lucide-react';
import { type ModuleProgress } from '../types';
import { cyanTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useEssentialsMode } from '../hooks/useEssentialsMode';

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
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
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
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
          <div className="text-center mb-8">
            <span className="inline-block px-3 py-1 rounded-full text-[11px] font-bold tracking-wider uppercase mb-3" style={{ backgroundColor: '#e8f5f2', color: '#1a6358', border: '1px solid rgba(42,125,111,0.2)', letterSpacing: '0.06em' }}>Neuroscience Simulation</span>
            <h4 className="font-serif font-bold" style={{ fontSize: 24, color: '#1a1a1a' }}>PFC Shutdown Simulator</h4>
            <p className="text-sm mt-1" style={{ color: '#7a7068' }}>See what happens when your Amygdala hijacks your brain under exam stress.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            {/* Amygdala card */}
            <div className="bg-white dark:bg-zinc-900 text-center" style={{ border: '2px solid #E85D75', borderRadius: 14, padding: '20px 16px' }}>
              <motion.div
                animate={stressed ? { scale: [1, 1.1, 1] } : { scale: 1 }}
                transition={stressed ? { duration: 1.2, repeat: Infinity } : {}}
                style={{ width: 52, height: 52, borderRadius: '50%', background: '#fde4e4', border: '2px solid rgba(232,93,117,0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 12px' }}
              >
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#E85D75" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
                  <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
                </svg>
              </motion.div>
              <p className="font-serif font-bold" style={{ fontSize: 16, color: '#1a1a1a' }}>Amygdala</p>
              <p style={{ fontSize: 13, color: '#7a7068', marginBottom: 12 }}>Threat Response</p>

              <div style={{ height: 6, borderRadius: 3, backgroundColor: '#fde4e4', overflow: 'hidden', marginBottom: 8 }}>
                <motion.div animate={{ width: stressed ? '100%' : '20%' }} transition={{ duration: 0.8 }} style={{ height: '100%', backgroundColor: '#E85D75', borderRadius: 3 }} />
              </div>

              <span className="inline-block text-[10px] font-bold uppercase" style={{
                letterSpacing: '0.08em',
                backgroundColor: stressed ? '#fde4e4' : '#e8f5f2',
                color: stressed ? '#b33030' : '#1a6358',
                border: stressed ? '1px solid rgba(232,93,117,0.3)' : '1px solid rgba(42,125,111,0.3)',
                borderRadius: 20, padding: '3px 10px',
              }}>
                {stressed ? 'HIJACKING' : 'CALM'}
              </span>
            </div>

            {/* PFC card */}
            <div className="bg-white dark:bg-zinc-900 text-center" style={{ border: '2px solid #2A7D6F', borderRadius: 14, padding: '20px 16px' }}>
              <motion.div
                animate={{ opacity: stressed ? 0.3 : 1 }}
                transition={{ duration: 0.5 }}
                style={{ width: 52, height: 52, borderRadius: '50%', background: '#e8f5f2', border: '2px solid rgba(42,125,111,0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 12px' }}
              >
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#2A7D6F" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M9.5 2C7 2 5 4 5 6.5c0 .8.2 1.5.5 2.1C4.2 9.3 3 10.8 3 12.5 3 15 5 17 7.5 17H9v3h6v-3h1.5C19 17 21 15 21 12.5c0-1.7-1.2-3.2-2.5-3.9.3-.6.5-1.3.5-2.1C19 4 17 2 14.5 2c-1.2 0-2.3.5-3 1.3C10.8 2.5 9.7 2 9.5 2z"/>
                </svg>
              </motion.div>
              <p className="font-serif font-bold" style={{ fontSize: 16, color: '#1a1a1a' }}>Prefrontal Cortex</p>
              <p style={{ fontSize: 13, color: '#7a7068', marginBottom: 12 }}>Rational Thinking</p>

              <div className="space-y-2 text-left">
                {capabilities.map((cap, i) => (
                  <motion.div
                    key={cap.label}
                    animate={stressed ? { opacity: 0.3, x: 4 } : { opacity: 1, x: 0 }}
                    transition={{ duration: 0.4, delay: stressed ? i * 0.3 : (2 - i) * 0.2 }}
                    className="flex items-center justify-between"
                  >
                    <div>
                      <p className="text-xs font-semibold" style={{ color: '#1a1a1a' }}>{cap.label}</p>
                      <p style={{ fontSize: 10, color: '#9e9186' }}>{cap.desc}</p>
                    </div>
                    <span className="text-[10px] font-bold uppercase" style={{
                      letterSpacing: '0.06em',
                      backgroundColor: stressed ? '#f0ece6' : '#e8f5f2',
                      color: stressed ? '#9e9186' : '#1a6358',
                      border: stressed ? '1px solid #d0cdc8' : '1px solid rgba(42,125,111,0.3)',
                      borderRadius: 20, padding: '2px 8px',
                    }}>
                      {stressed ? 'OFFLINE' : 'ONLINE'}
                    </span>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>

          {/* Cortisol callout */}
          <AnimatePresence>
            {stressed && (
              <motion.div
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 6 }}
                className="mb-6"
                style={{ borderLeft: '3px solid #E85D75', backgroundColor: '#fde4e4', borderRadius: '0 10px 10px 0', padding: '12px 16px' }}
              >
                <p className="text-sm italic" style={{ color: '#b33030' }}>
                  Cortisol is blocking the connection between your PFC and your stored knowledge. Your memory isn't gone — the pathway is temporarily offline.
                </p>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Toggle button */}
          <div className="flex justify-center">
            <button
              onClick={() => setStressed(!stressed)}
              style={{
                backgroundColor: stressed ? '#2A7D6F' : '#E85D75',
                color: '#FFFFFF',
                border: stressed ? '2px solid #2A7D6F' : '2px solid #E85D75',
                borderRadius: 20,
                padding: '12px 24px',
                fontSize: 14,
                fontWeight: 600,
                cursor: 'pointer',
              }}
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
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
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
                 className="p-4 rounded-xl text-left text-sm font-medium transition-all"
                 style={attempt === 'calm' ? { backgroundColor: '#FCA5A5', border: '2.5px solid #DC2626', borderRadius: 14, boxShadow: '3px 3px 0px 0px #DC2626', color: '#7F1D1D' } : { backgroundColor: '#FFFFFF', border: '2.5px solid #1C1917', borderRadius: 14, boxShadow: '3px 3px 0px 0px #1C1917' }}
               >
                 <p className="font-bold">"Calm down."</p>
                 <p className="text-xs mt-1 opacity-70">Try to lower your arousal</p>
               </button>
               <button
                 onClick={() => handleAttempt('reframe')}
                 className="p-4 rounded-xl text-left text-sm font-medium transition-all"
                 style={attempt === 'reframe' ? { backgroundColor: '#6EE7B7', border: '2.5px solid #059669', borderRadius: 14, boxShadow: '3px 3px 0px 0px #059669', color: '#064E3B' } : { backgroundColor: '#FFFFFF', border: '2.5px solid #1C1917', borderRadius: 14, boxShadow: '3px 3px 0px 0px #1C1917' }}
               >
                 <p className="font-bold">"I'm excited!"</p>
                 <p className="text-xs mt-1 opacity-70">Reframe the same arousal</p>
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
                   <p className="text-emerald-600 dark:text-emerald-400 text-xs">Anxiety and excitement feel the same in your body -- same racing heart, same adrenaline. You only need to change the label, not the state. People who say "I'm excited" before a test actually perform noticeably better than those who try to calm down.</p>
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
    const _quarterArc = circumference / 4;

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
     <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
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
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'neurobiology-stress', title: 'Why Stress Messes With Your Brain', eyebrow: '01 // The Hardware', icon: Cpu },
    { id: 'emotional-intelligence', title: 'What is Emotional Intelligence?', eyebrow: '02 // The Software', icon: Brain },
    { id: 'self-awareness', title: 'Reading Your Own Body', eyebrow: '03 // Early Warning Signs', icon: Heart },
    { id: 'cognitive-regulation', title: 'Using Your Mind to Manage Stress', eyebrow: '04 // The Mind', icon: Zap },
    { id: 'physiological-regulation', title: 'Using Your Body to Calm Down', eyebrow: '05 // The Body', icon: Shield },
    { id: 'bio-support', title: 'Sleep, Food, and Water', eyebrow: '06 // Fuel & Maintenance', icon: Utensils },
    { id: 'integrated-timeline', title: 'Putting It All Together', eyebrow: '07 // The Plan', icon: ClipboardCheck },
  ];

  return (
    <ModuleLayout
      moduleNumber="13"
      moduleTitle="Emotional Intelligence"
      moduleSubtitle="The Stress Management Toolkit"
      moduleDescription={`Understand why your brain freaks out during exams and learn practical techniques -- both mental and physical -- to turn stress into something that works for you, not against you.`}
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Master Your Response"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Why Stress Messes With Your Brain." eyebrow="Step 1" icon={Cpu} theme={theme}>
              {essentials ? (
                <>
                  <p>Exam stress is not a character flaw. Your body floods you with cortisol under pressure. A little cortisol helps. Too much shuts down your thinking brain. That is why you "go blank."</p>
                  <p>Your thinking brain (prefrontal cortex) goes offline when stress is high. Your alarm brain takes over. Understanding this is the first step to beating it.</p>
                </>
              ) : (
                <>
                  <p>Exam stress isn't a character flaw -- it's your brain doing exactly what it's designed to do. Your body has a built-in alarm system called the <Highlight description="Your body's built-in alarm system. When your brain senses danger (like opening an exam paper), it fires off a chain reaction that floods you with stress hormones, especially cortisol." theme={theme}>HPA Axis</Highlight>, and it floods you with stress hormones like cortisol. A small hit of cortisol actually sharpens your focus. But the Leaving Cert isn't one scary moment -- it's months of pressure, and that's where things go wrong.</p>
                  <p>When stress stays high for weeks, all that cortisol basically takes your <Highlight description="Think of this as the 'boss' part of your brain. It handles planning, logic, and holding information in your head. It's still developing in your teens, which is why stress can knock it offline so easily at your age." theme={theme}>Prefrontal Cortex (PFC)</Highlight> offline. That's the part of your brain you need for thinking, planning, and remembering. This is the real reason you "go blank" in an exam -- your brain has switched into survival mode and shut down the thinking part. Understanding this isn't an excuse; it's the first step to taking back control.</p>
                </>
              )}
              <StressResponseComparison />
              <PFCShutdownSimulator />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="What is Emotional Intelligence?" eyebrow="Step 2" icon={Brain} theme={theme}>
              {essentials ? (
                <p>Emotional intelligence means noticing what you feel, understanding why, and doing something useful about it. You can train three skills: spotting stress early, naming the feeling, and using techniques to manage it.</p>
              ) : (
                <>
                  <p><Highlight description="Being able to notice what you're feeling, understand why, and then do something useful about it instead of just reacting on autopilot." theme={theme}>Emotional Intelligence (EI)</Highlight> isn't about being "nice." It's a practical set of skills for noticing what's going on inside you and doing something useful about it. Having good EI doesn't mean you don't feel stress -- it means you can turn that stress into fuel (<Highlight description="The good kind of stress -- the buzz you get before a match or a performance that actually helps you do better. Same racing heart, but it's working for you, not against you." theme={theme}>eustress</Highlight>) instead of letting it wreck your performance.</p>
                  <p>For the Leaving Cert, we can break EI into three skills you can actually train:</p>
                </>
              )}
              <div className="my-10 rounded-2xl p-5 md:p-6 space-y-3" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#93C5FD', border: '2.5px solid #2563EB', borderRadius: 16, boxShadow: '4px 4px 0px 0px #2563EB' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#2563EB' }}>1</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#1E3A8A' }}>Emotional Awareness</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#1E3A8A', opacity: 0.8 }}>Spotting the physical signs of stress early.</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#FCD34D', border: '2.5px solid #D97706', borderRadius: 16, boxShadow: '4px 4px 0px 0px #D97706' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#D97706' }}>2</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#78350F' }}>Emotional Understanding</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#78350F', opacity: 0.8 }}>Putting the right name on what you're feeling.</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#FDBA74', border: '2.5px solid #EA580C', borderRadius: 16, boxShadow: '4px 4px 0px 0px #EA580C' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#EA580C' }}>3</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#7C2D12' }}>Emotional Regulation</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#7C2D12', opacity: 0.8 }}>Using specific techniques to manage it.</p>
                  </div>
                </div>
              </div>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Reading Your Own Body." eyebrow="Step 3" icon={Heart} theme={theme}>
              {essentials ? (
                <p>Your body spots stress before your brain does. Learn to notice your early warning signs: tight stomach, shallow breathing, racing heart. A daily body scan builds this skill. Catch stress early and you can deal with it before panic takes over.</p>
              ) : (
                <>
                  <p>You can't manage what you don't notice. The first step is learning to read your own body -- what we call <Highlight description="Getting good at reading your own body -- noticing things like your heart speeding up, your breathing going shallow, or your shoulders tensing. It's like having an early warning system for stress." theme={theme}>Somatic Literacy</Highlight>. Your body usually picks up on stress before your brain does. Those early physical signs -- the tight stomach, the shallow breathing -- are your <Highlight description="Those physical feelings -- like a knot in your stomach or sweaty palms -- that show up before you even realise you're stressed. Your body is basically tapping you on the shoulder saying 'heads up.'" theme={theme}>Somatic Markers</Highlight>.</p>
                  <p>A quick daily "Body Scan" trains you to notice these signals. If you can catch stress early, you can deal with it before it spirals into full-on panic. It's the difference between "I'm freaking out" and "OK, my heart is racing -- I know what to do about that."</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Using Your Mind to Manage Stress." eyebrow="Step 4" icon={Zap} theme={theme}>
              {essentials ? (
                <p>Say "I am excited" instead of "I am anxious." They feel the same in your body. Relabelling is easier than calming down. When your brain says "I will fail," challenge it like a lawyer. What is the actual evidence? Try the tool below.</p>
              ) : (
                <>
                  <p>Once you've spotted the feeling, you need to manage it with your mind. This is <Highlight description="Using your thinking to change how you feel. Basically, your mind talks your body down from the ledge." theme={theme}>Top-Down Regulation</Highlight>. One surprisingly powerful trick is <Highlight description="Relabelling your nerves as excitement. Anxiety and excitement feel almost identical in your body -- same racing heart, same adrenaline. The only real difference is the story you tell yourself about what's happening." theme={theme}>Arousal Reappraisal</Highlight>. It's actually much easier for your brain to switch from "anxious" to "excited" than it is to just "calm down."</p>
                  <p>The second tool is <Highlight description="When your brain tells you something catastrophic like 'I'm going to fail everything,' you stop and challenge it like a lawyer -- what's the actual evidence? Usually the panic is way bigger than the reality." theme={theme}>Cognitive Restructuring</Highlight>. When your brain screams "I'm going to fail everything," you treat that thought like you're a defence lawyer -- what's the actual evidence? Is it really true, or is panic doing the talking?</p>
                </>
              )}
              <ArousalReappraisal/>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Using Your Body to Calm Down." eyebrow="Step 5" icon={Shield} theme={theme}>
              {essentials ? (
                <p>When you are too stressed to think, use your body. Box Breathing is your emergency tool: breathe in 4 seconds, hold 4, out 4, hold 4. It is invisible. It breaks the panic loop in under a minute. Practice it below.</p>
              ) : (
                <>
                  <p>Sometimes, your mind is too flooded to think straight. When that happens, trying to reason your way out won't work -- you need to use your body to calm your mind instead. This is <Highlight description="Using your body to calm your mind. When you're too stressed to think straight, physical tricks like breathing exercises can break the panic cycle for you." theme={theme}>Bottom-Up Regulation</Highlight>. The fastest tool you have is your breathing.</p>
                  <p><Highlight description="A dead simple breathing pattern: 4 seconds in, hold 4, out 4, hold 4. It activates your body's built-in calm-down system. You can do it silently in the exam hall and nobody will even notice." theme={theme}>Box Breathing</Highlight> is your emergency move for the exam hall. It's invisible, takes less than a minute, and it breaks the panic loop so your thinking brain can come back online.</p>
                </>
              )}
              <BoxBreathing />
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Sleep, Food, and Water." eyebrow="Step 6" icon={Utensils} theme={theme}>
              {essentials ? (
                <p>Your brain cannot manage stress if you are tired, hungry, or dehydrated. Eat slow-release food like porridge. Drink water. Sleep properly. Use short NSDR breaks (guided rest, 10-20 minutes) to reset during long study days.</p>
              ) : (
                <>
                  <p>Managing your emotions takes real energy. A tired, dehydrated, or hungry brain can't keep its cool, no matter how many techniques you know. Looking after the basics isn't optional -- it's the foundation everything else is built on.</p>
                  <p>For food, focus on slow-release energy like porridge and omega-3s from fish or walnuts to keep you steady. Even being slightly dehydrated tanks your concentration. And sleep is when your brain locks in what you've learned and clears out the junk that causes brain fog. During study days, short breaks using <Highlight description="Non-Sleep Deep Rest -- basically a guided relaxation where you lie down for 10-20 minutes without actually sleeping. It's a quick reset button that helps you feel sharper and less wrecked during a long study day." theme={theme}>NSDR</Highlight> are a great way to reset without losing your whole afternoon.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="Putting It All Together." eyebrow="Step 7" icon={ClipboardCheck} theme={theme}>
              {essentials ? (
                <p>Months before: practice body scans and box breathing daily. Morning of: eat well, avoid panicked friends, say "I am excited." In the hall: stop, breathe, clench and release toes, start with easiest question. After: never compare answers.</p>
              ) : (
                <p>You now have a full toolkit -- techniques that use your mind and techniques that use your body. The final step is knowing when to use what.</p>
              )}
              <div className="my-10 rounded-2xl p-5 md:p-6 space-y-3" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#93C5FD', border: '2.5px solid #2563EB', borderRadius: 16, boxShadow: '4px 4px 0px 0px #2563EB' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#2563EB' }}>1</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#1E3A8A' }}>Months Before</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#1E3A8A', opacity: 0.8 }}>Build your foundation. Practice daily Body Scans and learn Box Breathing while stress is low so it's automatic when you need it.</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#FCD34D', border: '2.5px solid #D97706', borderRadius: 16, boxShadow: '4px 4px 0px 0px #D97706' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#D97706' }}>2</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#78350F' }}>Morning Of</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#78350F', opacity: 0.8 }}>Managing your energy is everything. Eat a proper breakfast, stay away from panicked friends at the school gate, and tell yourself "I'm excited" instead of "I'm terrified."</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#FDBA74', border: '2.5px solid #EA580C', borderRadius: 16, boxShadow: '4px 4px 0px 0px #EA580C' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#EA580C' }}>3</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#7C2D12' }}>In The Hall</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#7C2D12', opacity: 0.8 }}>If panic hits, use the "Paper Panic" drill: Stop, Breathe (3 cycles of Box Breathing), clench and release your toes, and re-engage with the easiest question on the paper.</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#6EE7B7', border: '2.5px solid #059669', borderRadius: 16, boxShadow: '4px 4px 0px 0px #059669' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#059669' }}>4</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#064E3B' }}>Post-Exam</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#064E3B', opacity: 0.8 }}>Do not -- absolutely do not -- compare answers with friends afterwards. It only fuels anxiety for the next paper.</p>
                  </div>
                </div>
              </div>
              <MicroCommitment theme={theme}><p>Pick one technique from this module. Commit to practising it for 5 minutes every day for one week. This isn't just studying -- you're building a skill that kicks in automatically when you need it most.</p></MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default EmotionalIntelligenceModule;
