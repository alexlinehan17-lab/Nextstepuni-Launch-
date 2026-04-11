
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { MotionDiv } from './Motion';
import {
  Cpu, Moon, Coffee, Zap, Repeat, ClipboardCheck, CheckCircle2
} from 'lucide-react';
import { type ModuleProgress } from '../types';
import { slateTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = slateTheme;

// --- INTERACTIVE COMPONENTS ---

const GlycemicIndexSimulator = () => {
    const [selected, setSelected] = useState<Set<'high' | 'low'>>(new Set());

    const toggle = (type: 'high' | 'low') => {
      setSelected(prev => {
        const next = new Set(prev);
        if (next.has(type)) next.delete(type); else next.add(type);
        return next;
      });
    };

    // Chart dimensions (inside padding)
    const W = 360, H = 160;
    const padL = 40, padR = 16, padT = 16, padB = 28;
    const chartW = W - padL - padR;
    const chartH = H - padT - padB;

    // Map data points to SVG coords
    const toX = (hour: number) => padL + (hour / 3) * chartW;
    const toY = (level: number) => padT + chartH - (level / 100) * chartH; // 0-100 scale

    // Blood sugar curves (hour, level) — baseline is ~50
    const highGI = [
      [0, 50], [0.3, 65], [0.5, 88], [0.75, 92], [1, 78], [1.3, 55], [1.6, 35], [2, 30], [2.5, 38], [3, 45],
    ] as [number, number][];

    const lowGI = [
      [0, 50], [0.5, 58], [1, 65], [1.5, 68], [2, 66], [2.5, 62], [3, 58],
    ] as [number, number][];

    // Build smooth path from points
    const buildPath = (points: [number, number][]) => {
      if (points.length < 2) return '';
      const coords = points.map(([h, l]) => [toX(h), toY(l)]);
      let d = `M ${coords[0][0]} ${coords[0][1]}`;
      for (let i = 1; i < coords.length; i++) {
        const prev = coords[i - 1];
        const curr = coords[i];
        const cpx = (prev[0] + curr[0]) / 2;
        d += ` C ${cpx} ${prev[1]}, ${cpx} ${curr[1]}, ${curr[0]} ${curr[1]}`;
      }
      return d;
    };

    const highPath = buildPath(highGI);
    const lowPath = buildPath(lowGI);

    // Focus zone band (optimal blood sugar ~55-75)
    const focusTop = toY(75);
    const focusBottom = toY(55);

    const hours = [0, 1, 2, 3];
    const levels = [
      { val: 25, label: 'Low' },
      { val: 50, label: 'Normal' },
      { val: 75, label: 'High' },
    ];

    return (
      <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Glycemic Index Simulator</h4>
        <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Toggle each breakfast to compare what happens to your blood sugar over 3 hours.</p>

        {/* Buttons */}
        <div className="flex justify-center gap-3 mb-6">
          <button
            onClick={() => toggle('high')}
            className={`px-4 py-2 text-xs font-bold rounded-lg border transition-all ${
              selected.has('high')
                ? 'bg-rose-500 text-white border-rose-500'
                : 'bg-rose-50 text-rose-700 border-rose-200 hover:border-rose-400'
            }`}
          >
            Sugary Cereal (High-GI)
          </button>
          <button
            onClick={() => toggle('low')}
            className={`px-4 py-2 text-xs font-bold rounded-lg border transition-all ${
              selected.has('low')
                ? 'bg-emerald-500 text-white border-emerald-500'
                : 'bg-emerald-50 text-emerald-700 border-emerald-200 hover:border-emerald-400'
            }`}
          >
            Porridge (Low-GI)
          </button>
        </div>

        {/* Chart */}
        <div className="bg-zinc-50 dark:bg-zinc-900/30 rounded-xl border border-zinc-200 dark:border-zinc-700 p-2">
          <svg viewBox={`0 0 ${W} ${H}`} className="w-full h-auto">
            {/* Focus zone band */}
            <rect
              x={padL} y={focusTop}
              width={chartW} height={focusBottom - focusTop}
              fill="currentColor"
              className="text-emerald-100 dark:text-emerald-900/20"
            />
            <text
              x={padL + 4} y={focusTop + 11}
              className="text-[7px] font-bold"
              fill="#10b981"
              opacity={0.6}
            >
              FOCUS ZONE
            </text>

            {/* Gridlines */}
            {levels.map(l => (
              <line key={l.val} x1={padL} y1={toY(l.val)} x2={W - padR} y2={toY(l.val)} stroke="currentColor" className="text-zinc-200 dark:text-zinc-700" strokeWidth="0.5" />
            ))}
            {hours.map(h => (
              <line key={h} x1={toX(h)} y1={padT} x2={toX(h)} y2={H - padB} stroke="currentColor" className="text-zinc-200 dark:text-zinc-700" strokeWidth="0.5" />
            ))}

            {/* Y-axis labels */}
            {levels.map(l => (
              <text key={l.val} x={padL - 4} y={toY(l.val) + 3} textAnchor="end" className="text-[7px]" fill="#a1a1aa">{l.label}</text>
            ))}

            {/* X-axis labels */}
            {hours.map(h => (
              <text key={h} x={toX(h)} y={H - padB + 14} textAnchor="middle" className="text-[7px]" fill="#a1a1aa">{h}h</text>
            ))}

            {/* High-GI path */}
            {selected.has('high') && (
              <>
                <motion.path
                  d={highPath}
                  fill="none"
                  stroke="#f43f5e"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  initial={{ pathLength: 0 }}
                  animate={{ pathLength: 1 }}
                  transition={{ duration: 1.2, ease: 'easeOut' }}
                />
                {/* Crash annotation */}
                <motion.g
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.8 }}
                >
                  <line x1={toX(1.6)} y1={toY(35)} x2={toX(1.6)} y2={toY(35) - 18} stroke="#f43f5e" strokeWidth="0.8" strokeDasharray="2 2" />
                  <text x={toX(1.6)} y={toY(35) - 22} textAnchor="middle" className="text-[6px] font-bold" fill="#f43f5e">CRASH</text>
                </motion.g>
              </>
            )}

            {/* Low-GI path */}
            {selected.has('low') && (
              <motion.path
                d={lowPath}
                fill="none"
                stroke="#10b981"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ duration: 1.2, ease: 'easeOut' }}
              />
            )}
          </svg>
        </div>

        {/* Legend / insight */}
        {selected.size > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4 flex justify-center gap-5"
          >
            {selected.has('high') && (
              <div className="flex items-center gap-2">
                <div className="w-5 h-1 rounded-full bg-rose-500" />
                <span className="text-[10px] text-zinc-500 dark:text-zinc-400">Spike then crash — focus lost by hour 2</span>
              </div>
            )}
            {selected.has('low') && (
              <div className="flex items-center gap-2">
                <div className="w-5 h-1 rounded-full bg-emerald-500" />
                <span className="text-[10px] text-zinc-500 dark:text-zinc-400">Steady release — stays in focus zone for 3 hours</span>
              </div>
            )}
          </motion.div>
        )}

        {selected.size === 0 && (
          <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 mt-4">Select a breakfast to see its blood sugar curve.</p>
        )}
      </div>
    );
};

const WAKE_OPTIONS = [
  { label: '6:00 AM', hour: 6 },
  { label: '7:00 AM', hour: 7 },
  { label: '8:00 AM', hour: 8 },
  { label: '9:00 AM', hour: 9 },
];

const formatTime = (hour24: number): string => {
  const h = Math.floor(hour24) % 24;
  const m = Math.round((hour24 - Math.floor(hour24)) * 60);
  const period = h >= 12 ? 'PM' : 'AM';
  const display = h === 0 ? 12 : h > 12 ? h - 12 : h;
  return `${display}:${m.toString().padStart(2, '0')} ${period}`;
};

const getZone = (hoursAwake: number): { fill: string; bg: string; border: string; text: string; label: string; desc: string; zoneIdx: number } => {
  if (hoursAwake < 12) return { fill: '#2A7D6F', bg: '#e8f5f2', border: '#2A7D6F', text: '#1a6358', label: 'Sharp', desc: 'Peak cognitive performance window', zoneIdx: 0 };
  if (hoursAwake < 15) return { fill: '#9e9186', bg: '#f4f0eb', border: '#d0cdc8', text: '#5a5550', label: 'Declining', desc: 'Focus and recall starting to dip', zoneIdx: 1 };
  if (hoursAwake < 17) return { fill: '#E85D75', bg: '#fde4e4', border: '#E85D75', text: '#b33030', label: 'Impaired', desc: 'Significant reduction in working memory', zoneIdx: 2 };
  return { fill: '#b33030', bg: '#fde4e4', border: '#b33030', text: '#7a0000', label: 'Critical', desc: 'Equivalent to mild alcohol impairment', zoneIdx: 3 };
};

const getMilestone = (hoursAwake: number): string | null => {
  if (hoursAwake >= 19) return 'You are now LEGALLY DRUNK in terms of cognitive function';
  if (hoursAwake >= 17) return 'You are now as impaired as someone who has been drinking';
  if (hoursAwake >= 16) return 'Working memory reduced by 30%';
  return null;
};

const CognitiveImpairmentClock = () => {
  const [wakeHour, setWakeHour] = useState<number | null>(null);
  const [hoursAwake, setHoursAwake] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [paused, setPaused] = useState(false);
  const [finished, setFinished] = useState(false);
  const [lastMilestone, setLastMilestone] = useState<string | null>(null);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const MAX_HOURS = 22;

  useEffect(() => {
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, []);

  const startAnimation = () => {
    if (wakeHour === null) return;
    setHoursAwake(0);
    setFinished(false);
    setLastMilestone(null);
    setPlaying(true);
    setPaused(false);

    if (intervalRef.current) clearInterval(intervalRef.current);
    let current = 0;
    intervalRef.current = setInterval(() => {
      current += 0.5;
      setHoursAwake(current);

      const milestone = getMilestone(current);
      if (milestone) setLastMilestone(milestone);

      if (current >= MAX_HOURS) {
        if (intervalRef.current) clearInterval(intervalRef.current);
        intervalRef.current = null;
        setPlaying(false);
        setFinished(true);
      }
    }, 500);
  };

  const togglePause = () => {
    if (paused) {
      let current = hoursAwake;
      intervalRef.current = setInterval(() => {
        current += 0.5;
        setHoursAwake(current);

        const milestone = getMilestone(current);
        if (milestone) setLastMilestone(milestone);

        if (current >= MAX_HOURS) {
          if (intervalRef.current) clearInterval(intervalRef.current);
          intervalRef.current = null;
          setPlaying(false);
          setFinished(true);
        }
      }, 500);
      setPaused(false);
    } else {
      if (intervalRef.current) clearInterval(intervalRef.current);
      intervalRef.current = null;
      setPaused(true);
    }
  };

  const reset = () => {
    if (intervalRef.current) clearInterval(intervalRef.current);
    intervalRef.current = null;
    setWakeHour(null);
    setHoursAwake(0);
    setPlaying(false);
    setPaused(false);
    setFinished(false);
    setLastMilestone(null);
  };

  const zone = getZone(hoursAwake);
  const meterPercent = Math.min((hoursAwake / MAX_HOURS) * 100, 100);
  const currentTime = wakeHour !== null ? formatTime(wakeHour + hoursAwake) : '';
  const impairedTime = wakeHour !== null ? formatTime(wakeHour + 17) : '';
  const decliningTime = wakeHour !== null ? formatTime(wakeHour + 15) : '';
  const zoneLabels = ['SHARP', 'DECLINING', 'IMPAIRED', 'CRITICAL'];

  // Split currentTime into time and period
  const timeParts = currentTime.split(' ');
  const timeStr = timeParts[0] || '';
  const periodStr = timeParts[1] || '';

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      <div className="text-center mb-8">
        <span className="inline-block px-3 py-1 rounded-full text-[11px] font-bold tracking-wider uppercase mb-3" style={{ backgroundColor: '#e8f5f2', color: '#1a6358', border: '1px solid rgba(42,125,111,0.2)', letterSpacing: '0.06em' }}>Neuroscience Simulation</span>
        <h4 className="font-serif font-bold" style={{ fontSize: 24, color: '#1a1a1a' }}>Cognitive Impairment Clock</h4>
        <p className="text-sm mt-1" style={{ color: '#7a7068' }}>Pick your wake-up time and watch how wakefulness erodes your brain power throughout the day.</p>
      </div>

      {/* Wake time selection */}
      {!playing && !finished && (
        <MotionDiv initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="flex flex-col items-center gap-5">
          <p style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', color: '#9e9186', textTransform: 'uppercase' as const }}>Wake-up Time</p>
          <div className="flex flex-wrap justify-center gap-3">
            {WAKE_OPTIONS.map(opt => (
              <button
                key={opt.hour}
                onClick={() => { setWakeHour(opt.hour); setHoursAwake(0); setFinished(false); setLastMilestone(null); }}
                style={{
                  backgroundColor: wakeHour === opt.hour ? '#e8f5f2' : '#FFFFFF',
                  border: wakeHour === opt.hour ? '2px solid #2A7D6F' : '2px solid #1a1a1a',
                  borderRadius: 20,
                  padding: '10px 20px',
                  fontSize: 14,
                  fontWeight: 600,
                  color: wakeHour === opt.hour ? '#1a6358' : '#1a1a1a',
                  cursor: 'pointer',
                }}
              >
                {opt.label}
              </button>
            ))}
          </div>
          {wakeHour !== null && (
            <MotionDiv initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}>
              <button onClick={startAnimation} className="mt-2 text-white font-semibold" style={{ backgroundColor: '#2A7D6F', borderRadius: 100, padding: '14px 32px', fontSize: 15 }}>
                Play Day
              </button>
            </MotionDiv>
          )}
        </MotionDiv>
      )}

      {/* Animation in progress */}
      {(playing || paused) && wakeHour !== null && (
        <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-5">
          {/* Clock card */}
          <div className="bg-white dark:bg-zinc-900 text-center" style={{ border: '2px solid #1a1a1a', borderRadius: 16, padding: '28px 32px', maxWidth: 380, margin: '0 auto' }}>
            <p style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', color: '#9e9186', textTransform: 'uppercase' as const, marginBottom: 8 }}>Current Time</p>
            <p style={{ lineHeight: 1 }}>
              <span className="font-serif font-semibold" style={{ fontSize: 56, color: '#1a1a1a', letterSpacing: '-0.02em' }}>{timeStr}</span>
              <span className="font-serif" style={{ fontSize: 24, color: '#9e9186', marginLeft: 8, verticalAlign: 'middle' }}>{periodStr}</span>
            </p>
            <p className="mt-2" style={{ fontSize: 14, color: '#7a7068' }}>{Math.floor(hoursAwake)} hours awake</p>
          </div>

          {/* Impairment bar */}
          <div>
            <div className="flex justify-between mb-2 px-1">
              {zoneLabels.map((lbl, li) => (
                <span key={lbl} style={{ fontSize: 9, fontWeight: zone.zoneIdx === li ? 700 : 400, letterSpacing: '0.1em', color: zone.zoneIdx === li ? '#1a1a1a' : '#b0a898', textTransform: 'uppercase' as const }}>{lbl}</span>
              ))}
            </div>
            <div className="relative" style={{ backgroundColor: '#f4f0eb', border: '2px solid #1a1a1a', borderRadius: 100, height: 20, overflow: 'hidden' }}>
              <MotionDiv style={{ height: '100%', backgroundColor: zone.fill, borderRadius: 100 }} initial={false} animate={{ width: `${meterPercent}%` }} transition={{ duration: 0.4, ease: 'linear' }} />
              {/* Tick marks */}
              {[37.5, 62.5, 87.5].map(pct => (
                <div key={pct} className="absolute top-0 bottom-0" style={{ left: `${pct}%`, width: 2, backgroundColor: 'rgba(255,255,255,0.7)' }} />
              ))}
            </div>
          </div>

          {/* Status card */}
          <MotionDiv key={zone.label} initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} className="max-w-sm mx-auto" style={{ backgroundColor: zone.bg, border: `2px solid ${zone.border}`, borderRadius: 14, padding: '16px 20px', textAlign: 'center' }}>
            <p style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', color: '#9e9186', textTransform: 'uppercase' as const, marginBottom: 6 }}>Cognitive Status</p>
            <p className="font-serif font-semibold" style={{ fontSize: 22, color: zone.text }}>{zone.label}</p>
            <p style={{ fontSize: 13, color: '#7a7068', marginTop: 4 }}>{zone.desc}</p>
          </MotionDiv>

          {/* Milestone flash */}
          {lastMilestone && (
            <MotionDiv key={lastMilestone} initial={{ opacity: 0, scale: 0.85 }} animate={{ opacity: 1, scale: 1 }} transition={{ type: 'spring', stiffness: 300, damping: 20 }} style={{ borderLeft: '3px solid #E85D75', backgroundColor: '#fde4e4', borderRadius: '0 10px 10px 0', padding: '12px 16px' }}>
              <p className="text-sm font-bold italic" style={{ color: '#b33030' }}>{lastMilestone}</p>
            </MotionDiv>
          )}

          {/* Controls */}
          <div className="flex justify-center gap-3 pt-2">
            <button onClick={togglePause} style={{ backgroundColor: paused ? '#2A7D6F' : '#FFFFFF', color: paused ? '#FFFFFF' : '#1a1a1a', border: paused ? '2px solid #2A7D6F' : '2px solid #1a1a1a', borderRadius: 20, padding: '10px 24px', fontSize: 14, fontWeight: 600 }}>
              {paused ? 'Resume' : 'Pause'}
            </button>
            <button onClick={reset} className="font-medium" style={{ fontSize: 13, color: '#9e9186', background: 'none', border: 'none' }}>
              Reset
            </button>
          </div>
        </MotionDiv>
      )}

      {/* Finished summary */}
      {finished && wakeHour !== null && (
        <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="space-y-5">
          <div className="bg-white dark:bg-zinc-900 text-center" style={{ border: '2px solid #1a1a1a', borderRadius: 16, padding: '28px 32px', maxWidth: 380, margin: '0 auto' }}>
            <p style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', color: '#9e9186', textTransform: 'uppercase' as const, marginBottom: 8 }}>Impairment Begins At</p>
            <p className="font-serif font-semibold" style={{ fontSize: 48, color: '#E85D75', letterSpacing: '-0.02em' }}>{impairedTime}</p>
            <p className="mt-2" style={{ fontSize: 14, color: '#7a7068' }}>This is when you become cognitively impaired.</p>
          </div>

          <div style={{ borderLeft: '3px solid #E85D75', backgroundColor: '#fde4e4', borderRadius: '0 10px 10px 0', padding: '12px 16px' }}>
            <p className="text-sm" style={{ color: '#b33030' }}>
              <span className="font-bold">If you wake at {formatTime(wakeHour)}</span>, your cognition starts declining by{' '}
              <span className="font-bold">{decliningTime}</span> and you are cognitively impaired by{' '}
              <span className="font-bold">{impairedTime}</span>.
            </p>
            <p className="text-sm font-bold mt-1" style={{ color: '#b33030' }}>
              Studying after {impairedTime} is like studying drunk.
            </p>
          </div>

          <div className="flex justify-center">
            <button onClick={reset} className="text-white font-semibold" style={{ backgroundColor: '#2A7D6F', borderRadius: 100, padding: '14px 32px', fontSize: 15 }}>
              Try a Different Wake Time
            </button>
          </div>
        </MotionDiv>
      )}
    </div>
  );
};

const HighPerformanceChecklist = () => {
    const [checks, setChecks] = useState<{[key: string]: boolean}>({});
    const toggle = (key: string) => setChecks(prev => ({...prev, [key]: !prev[key]}));
    const items = [
        { key: 'wake', time: '08:30', task: 'Wake + Light Exposure', details: '10 mins outside. Helps your body clock reset.' },
        { key: 'fuel', time: '08:45', task: 'Hydration + Breakfast', details: '500ml water. Porridge or eggs — something slow-burning.' },
        { key: 'deep1', time: '09:30', task: 'Study Block 1 (Deep Work)', details: '90 mins on your hardest subject while your brain is fresh.' },
        { key: 'break1', time: '11:00', task: 'Active Break', details: '15 mins walking. Leave the phone behind.' },
        { key: 'exercise', time: '16:00', task: 'EXERCISE (The Reset)', details: '45 mins. Gets your brain ready to learn again.' },
        { key: 'review', time: '18:30', task: 'Review Block (Active Recall)', details: '60 mins. Quiz yourself on what you studied this morning.' },
        { key: 'tech', time: '22:00', task: 'Screens Off', details: 'No screens. Your brain needs darkness to start winding down.' },
        { key: 'sleep', time: '23:00', task: 'Sleep', details: 'Aim for 8.5 to 9 hours.' },
    ];

    return(
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">High-Performance Checklist</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">A solid study day from start to finish. Tick each one off as you go.</p>
            <div className="space-y-3">
                {items.map(item => (
                    <div key={item.key} onClick={() => toggle(item.key)} className="p-4 rounded-xl flex items-center gap-4 cursor-pointer transition-all" style={checks[item.key] ? { backgroundColor: '#6EE7B7', border: '2.5px solid #059669', borderRadius: 14, boxShadow: '3px 3px 0px 0px #059669' } : { backgroundColor: '#FFFFFF', border: '2.5px solid #1C1917', borderRadius: 14, boxShadow: '3px 3px 0px 0px #1C1917' }}>
                        <span className="font-mono text-xs font-bold w-12">{item.time}</span>
                        <div className="flex-grow">
                            <p className="font-bold text-sm">{item.task}</p>
                            <p className="text-xs text-zinc-500 dark:text-zinc-400">{item.details}</p>
                        </div>
                        <div className={`w-6 h-6 rounded-full flex-shrink-0 flex items-center justify-center ${checks[item.key] ? 'bg-emerald-500' : 'bg-zinc-300'}`}><CheckCircle2 size={12} className="text-white"/></div>
                    </div>
                ))}
            </div>
        </div>
    );
}

// --- MODULE COMPONENT ---
const ControllableVariablesModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'engine', title: 'The Performance Engine', eyebrow: '01 // The Core Idea', icon: Cpu },
    { id: 'sleep', title: 'The Save Button: Sleep', eyebrow: '02 // The Foundation', icon: Moon },
    { id: 'nutrition', title: 'The Fuel Supply: Nutrition', eyebrow: '03 // The Energy', icon: Coffee },
    { id: 'exercise', title: 'The Upgrade: Exercise', eyebrow: '04 // The Catalyst', icon: Zap },
    { id: 'vicious-cycle', title: 'The Vicious Cycle', eyebrow: '05 // The Feedback Loop', icon: Repeat },
    { id: 'blueprint', title: 'The High-Performance Blueprint', eyebrow: '06 // Your Protocol', icon: ClipboardCheck },
  ];

  return (
    <ModuleLayout
      moduleNumber="09"
      moduleTitle="Controllable Variables"
      moduleSubtitle="Sleep, Food, and Exercise"
      moduleDescription="Your brain runs on three things: sleep, food, and exercise. Get these right and everything else gets easier. This module shows you how they actually work and what to do about it."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Fuel Your Brain"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Performance Engine." eyebrow="Step 1" icon={Cpu} theme={theme}>
              <p>Most of us treat our brains like they just run on willpower. But learning, memory, and focus are physical processes — they depend on what you put into your body. Think of your brain less like a laptop and more like a high-performance engine. What comes out depends entirely on what goes in. How well you can learn on any given day comes down to three things: <Highlight description="This is basically the save button for everything you study. Without proper sleep, your brain can't hold onto what you learned." theme={theme}>Sleep</Highlight>, <Highlight description="Your brain's fuel. The right food keeps you focused; the wrong food leaves you in a fog." theme={theme}>Nutrition</Highlight>, and <Highlight description="Moving your body actually makes your brain better at learning. It's not just about fitness." theme={theme}>Exercise</Highlight>.</p>
              <p>Right behind your forehead is your <Highlight description="This is the part of your brain that lets you hold a tricky Maths problem in your head or plan out an English essay. It's like the boss of your brain — but it's still developing in your teens, which makes it powerful but also easy to throw off." theme={theme}>Prefrontal Cortex (PFC)</Highlight> — the part of your brain that handles complex thinking, like working through a Maths problem or planning an English essay. During your teenage years, this area is basically under construction, which makes it really capable but also really sensitive. When you're running on no sleep or skipping meals, your brain starts shutting down the connection between this thinking part and your emotional brain — something called <Highlight description="When you're tired or running on empty, your brain basically cuts the line between the part that thinks clearly and the part that panics. That's why everything feels more stressful when you're wrecked." theme={theme}>Neural Decoupling</Highlight>. You're not just tired — your brain literally can't work properly.</p>
              <p>This module is about giving you the full picture of how sleep, food, and exercise affect your Leaving Cert performance. Forget vague advice like "get more sleep." We're going to show you exactly what happens in your brain and what you can actually do about it. The big idea here is simple: stop obsessing over time management and start thinking about <Highlight description="Instead of just trying to study more hours, focus on the things that give you more energy and sharper focus — sleep, food, and exercise. That's what actually decides how good your study sessions are." theme={theme}>energy management</Highlight>.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Save Button: Sleep." eyebrow="Step 2" icon={Moon} theme={theme}>
              <p>Learning actually happens in two steps. The first step, <Highlight description="This is when you first take in new information — reading your notes, listening in class. But at this point, the memory is shaky and easy to lose." theme={theme}>encoding</Highlight>, is when you study and take in new information. But that information is fragile — it's sitting in a temporary holding area in your brain called the <Highlight description="Think of this as your brain's short-term storage. It holds new stuff temporarily, but if you don't sleep properly, it gets wiped." theme={theme}>hippocampus</Highlight>. Without the second step, <Highlight description="This is when your brain takes everything you learned during the day and saves it properly into long-term memory. It mostly happens while you sleep." theme={theme}>consolidation</Highlight>, that learning gets wiped. Sleep is literally the save button. A student who studies for five hours and sleeps for five has actually learned less than someone who studies for three and sleeps for eight.</p>
              <p>Your brain goes through different types of sleep during the night. <Highlight description="This is the really deep sleep you get in the first few hours of the night. It's when your brain saves facts, dates, definitions — the stuff you need for exams." theme={theme}>Slow-Wave Sleep (SWS)</Highlight>, which happens mostly in the first half of the night, is when your brain saves facts and definitions. <Highlight description="This is the lighter, dreamy sleep you get later in the night. It's when your brain makes connections between ideas and solves problems — basically your creative thinking sleep." theme={theme}>REM Sleep</Highlight>, which happens more in the second half, is when your brain connects ideas and works through problems. When you cut your sleep short, you're mostly losing REM sleep — which tanks your ability to think creatively and solve problems the next day.</p>
              <p>Here's how bad it gets. After just one week of 5-hour nights, your working memory drops by about <Highlight description="One week of only 5 hours sleep per night drops your working memory accuracy by 17%. That's enough to take you from an A to a C in terms of how well your brain is actually functioning." theme={theme}>17%</Highlight> — that's enough to drop you from an A to a C. And there's something even worse: <Highlight description="After being awake for 17-19 hours straight, your brain works about as well as if you'd been drinking. So if you got up at 6am, by 11pm your thinking is as impaired as someone who is legally drunk." theme={theme}>the drunk comparison</Highlight>. After 17-19 hours awake, your brain is as impaired as if you had a blood alcohol level of 0.05%. If you wake up at 6 AM, by 11 PM you're basically studying drunk. And "catching up at the weekend" doesn't really fix it — two nights of extra sleep isn't enough to undo the damage.</p>
              <CognitiveImpairmentClock />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Fuel Supply: Nutrition." eyebrow="Step 3" icon={Coffee} theme={theme}>
              <p>Your brain uses about 20% of all the energy your body produces. That's a huge amount for something that weighs less than a bag of sugar. What you eat isn't just about staying healthy — it directly affects how well you can think, focus, and remember things.</p>
              <p>The key thing is how quickly your food releases energy. High-<Highlight description="This is basically a measure of how fast a food hits your blood sugar. Sugary cereal and white bread spike it fast and then you crash. Porridge and brown bread release energy slowly and keep you steady." theme={theme}>Glycemic Index (GI)</Highlight> foods like sugary cereal give you a quick spike of energy followed by a crash — right in the middle of when you need to focus. Low-GI foods like porridge give you a slow, steady release that keeps you going. Your brain also needs certain nutrients to work properly. Not getting enough <Highlight description="These are healthy fats found in oily fish like salmon and mackerel. They help your brain cells communicate properly — think of them as keeping the wiring in good shape." theme={theme}>Omega-3s</Highlight> or <Highlight description="These vitamins (B6, B9, B12) help your brain make the chemicals it needs to stay focused and in a good mood. Low levels can leave you feeling foggy and slow." theme={theme}>B-Vitamins</Highlight> can leave you feeling foggy and slow. And don't forget water — even mild dehydration (losing just 1% of your body weight in water) is enough to mess with your working memory.</p>
              <GlycemicIndexSimulator />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Upgrade: Exercise." eyebrow="Step 4" icon={Zap} theme={theme}>
                <p>Exercise isn't a break from studying — it actually makes your brain better at learning. When you exercise, your brain gets better at <Highlight description="Your brain's ability to change, adapt, and form new connections. Exercise is one of the best ways to boost this." theme={theme}>neuroplasticity</Highlight> — its ability to rewire itself. The reason is a protein called <Highlight description="A protein your brain releases when you exercise. Think of it like fertiliser for your brain — it helps grow new connections and makes existing ones stronger. More of it means faster learning." theme={theme}>BDNF</Highlight>, which is basically fertiliser for your brain cells. When you exercise, your body ramps up production of this stuff. Someone who exercises regularly will genuinely learn faster and remember more than someone who doesn't.</p>
                <p>When you exercise matters too. Working out before studying helps you focus and pay attention. But exercising a few hours after studying might be even better for actually remembering what you learned — that's the <Highlight description="If you exercise a few hours after studying, your brain treats those memories as more important and does a better job of saving them. It's like flagging your study session as 'worth keeping'." theme={theme}>Consolidation Hack</Highlight>. And even on your rest days, something low-key like a walk is way better than just sitting on the couch scrolling. That kind of <Highlight description="Light movement like walking or stretching. It helps your brain clear out stress and tiredness much better than just sitting around on your phone." theme={theme}>Active Recovery</Highlight> clears out stress and mental fatigue far better than doing nothing.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Vicious Cycle." eyebrow="Step 5" icon={Repeat} theme={theme}>
              <p>Sleep and food aren't separate problems — they feed into each other in a nasty loop. When you don't sleep enough, it messes with two hunger hormones called <Highlight description="When you're sleep-deprived, the hormone that tells you you're full (leptin) drops, and the one that makes you hungry (ghrelin) spikes. So your body literally craves junk food. It's not a willpower thing — it's chemistry." theme={theme}>leptin and ghrelin</Highlight>. Basically, your body starts craving sugary, high-calorie food. You wake up wrecked, and the last thing you want is eggs — you reach for the sugary cereal instead.</p>
              <p>But then that sugary food messes with your sleep. The spikes and dips in your blood sugar can interfere with <Highlight description="The really deep sleep you get early in the night — the kind that saves facts and definitions to long-term memory. Eating loads of sugar makes it harder to get enough of this." theme={theme}>Slow-Wave Sleep (SWS)</Highlight>, which is the deep sleep your brain needs to save what you studied. So bad sleep leads to bad food, which leads to even worse sleep. Over a few weeks or months, this loop quietly makes it harder and harder to think clearly. The good news? You can break it from either end — start sleeping better, or start with a decent breakfast. Either one helps.</p>
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="The High-Performance Blueprint." eyebrow="Step 6" icon={ClipboardCheck} theme={theme}>
              <p>Now that you know how sleep, food, and exercise work together, here's what a great study day actually looks like. The whole point is to stop just managing your time and start managing your energy.</p>
              <p>This checklist is built around a day off school — a study day at home. It's designed to work with how your body and brain naturally operate as a teenager, so you get the most out of every hour. It's not about being perfect every day — it's about having a solid structure that actually works.</p>
              <HighPerformanceChecklist />
              <MicroCommitment theme={theme}>
                <p><strong>The Breakfast Experiment:</strong> Try two mornings with different breakfasts. <strong>Day 1:</strong> Eat a sugary breakfast (cereal, fruit juice, white toast). At 10:30 AM, rate your energy and focus from 1-10. <strong>Day 2:</strong> Eat a slow-burning breakfast (porridge, eggs, yogurt). At 10:30 AM, rate your energy and focus from 1-10. Compare the two and see the difference for yourself.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default ControllableVariablesModule;
