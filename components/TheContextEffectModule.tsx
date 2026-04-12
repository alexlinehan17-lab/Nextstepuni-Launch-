/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { Map, Repeat, Activity, Brain, Wrench } from 'lucide-react';
import { type ModuleProgress } from '../types';
import { purpleTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory, ConceptCardGrid } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useEssentialsMode } from '../hooks/useEssentialsMode';

const theme = purpleTheme;

// --- INTERACTIVE COMPONENTS ---

// 1. CONTEXT MEMORY COMPARISON (Planning Paradox style dual-chart)
const ContextMemoryComparison = () => {
  const [revealed, setRevealed] = useState(false);

  const W = 440, H = 260;
  const padL = 8, padR = 8, padT = 28, padB = 44;
  const chartW = W - padL - padR, chartH = H - padT - padB;
  const toX = (f: number) => padL + f * chartW;
  const toY = (f: number) => padT + (1 - f) * chartH;

  const xLabels = ['Day 1', 'Day 3', 'Day 7', 'Day 14', 'Day 21', 'Day 30'];

  // Both charts share the same encoding strength
  const encodingStrength = [0.40, 0.55, 0.65, 0.72, 0.78, 0.82];

  // Same context: retrieval tracks closely
  const sameRetrieval = [0.35, 0.50, 0.60, 0.68, 0.72, 0.78];

  // Different context: retrieval drops significantly
  const diffRetrieval = [0.35, 0.42, 0.40, 0.38, 0.35, 0.30];

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

  const samePhases = [
    { label: 'Building', x1: 0, x2: 0.33, color: '#6ee7b7' },
    { label: 'Strengthening', x1: 0.33, x2: 0.66, color: '#34d399' },
    { label: 'Accessible', x1: 0.66, x2: 1, color: '#10b981' },
  ];
  const diffPhases = [
    { label: 'Building', x1: 0, x2: 0.33, color: '#fca5a5' },
    { label: 'Cues missing', x1: 0.33, x2: 0.66, color: '#f87171' },
    { label: 'Inaccessible', x1: 0.66, x2: 1, color: '#ef4444' },
  ];

  const Chart = ({ encoding, retrieval, phases, areaColor, areaId, label }: {
    encoding: number[]; retrieval: number[]; phases: { label: string; x1: number; x2: number; color: string }[];
    areaColor: string; areaId: string; label: string;
  }) => (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full">
      <defs>
        <linearGradient id={areaId} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={areaColor} stopOpacity="0.5" />
          <stop offset="100%" stopColor={areaColor} stopOpacity="0.05" />
        </linearGradient>
      </defs>
      {[0.25, 0.5, 0.75, 1.0].map((v) => (
        <line key={v} x1={padL} x2={W - padR} y1={toY(v)} y2={toY(v)} stroke="#a1a1aa" strokeOpacity="0.15" strokeDasharray="3 3" />
      ))}
      <line x1={padL} x2={W - padR} y1={toY(0)} y2={toY(0)} stroke="#a1a1aa" strokeOpacity="0.3" />

      {/* Encoding area */}
      <motion.path d={buildArea(encoding)} fill={`url(#${areaId})`} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.8 }} />
      {/* Encoding line (solid) */}
      <motion.path d={buildLine(encoding)} fill="none" stroke={areaColor} strokeWidth="2.5" strokeLinecap="round" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1.2, ease: 'easeOut' }} />
      {/* Retrieval line (dashed) */}
      <motion.path d={buildLine(retrieval)} fill="none" stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="5 3" strokeLinecap="round" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1.2, ease: 'easeOut', delay: 0.3 }} />
      {/* Encoding dots */}
      {encoding.map((v, i) => (
        <motion.circle key={i} cx={toX(i / (encoding.length - 1))} cy={toY(v)} r="3.5" fill={areaColor} initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2 * i + 0.3 }} />
      ))}

      <text x={padL + 2} y={toY(1.0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">High</text>
      <text x={padL + 2} y={toY(0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">Low</text>
      {xLabels.map((m, i) => (
        <text key={m} x={toX(i / (xLabels.length - 1))} y={toY(0) + 14} fontSize="9" fill="#a1a1aa" textAnchor="middle" fontWeight="600">{m}</text>
      ))}
      {phases.map((p, i) => (
        <text key={i} x={toX((p.x1 + p.x2) / 2)} y={toY(0) + 28} fontSize="8" fill={p.color} textAnchor="middle" fontWeight="700">{p.label}</text>
      ))}
      <text x={W / 2} y={14} fontSize="11" fill="#71717a" textAnchor="middle" fontWeight="700">{label}</text>
      <line x1={W - padR - 120} x2={W - padR - 104} y1={14} y2={14} stroke={areaColor} strokeWidth="2" />
      <text x={W - padR - 100} y={17} fontSize="8" fill="#a1a1aa">Learning Strength</text>
      <line x1={W - padR - 44} x2={W - padR - 28} y1={14} y2={14} stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="4 2" />
      <text x={W - padR - 24} y={17} fontSize="8" fill="#a1a1aa">Recall</text>
    </svg>
  );

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">How Your Study Spot Affects Your Memory</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">What happens to your memory when the environment changes?</p>

      {!revealed ? (
        <div className="text-center">
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">You study perfectly in your bedroom. But what happens when you sit down in the exam hall?</p>
          <button onClick={() => setRevealed(true)} className="px-5 py-2.5 text-sm font-bold rounded-lg bg-purple-500 text-white hover:bg-purple-600 transition-colors">
            See the Context Effect
          </button>
        </div>
      ) : (
        <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
          <div className="grid md:grid-cols-2 gap-4 mb-5">
            <div className="rounded-lg border border-emerald-200 dark:border-emerald-900 bg-emerald-50/50 dark:bg-emerald-950/20 p-3">
              <Chart encoding={encodingStrength} retrieval={sameRetrieval} phases={samePhases} areaColor="#10b981" areaId="same-ctx-grad" label="Same Context (Study & Test)" />
            </div>
            <div className="rounded-lg border border-rose-200 dark:border-rose-900 bg-rose-50/50 dark:bg-rose-950/20 p-3">
              <Chart encoding={encodingStrength} retrieval={diffRetrieval} phases={diffPhases} areaColor="#ef4444" areaId="diff-ctx-grad" label="Different Context (Study vs Test)" />
            </div>
          </div>
          <div className="grid md:grid-cols-2 gap-4 text-sm">
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900">
              <span className="text-emerald-500 text-lg mt-0.5">&#x2714;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-emerald-600 dark:text-emerald-400">Same-place recall</strong> works because familiar surroundings help your brain find what it learned. But exams are in a DIFFERENT place. If your memories depend on your study spot, they become fragile.</p>
            </div>
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900">
              <span className="text-rose-500 text-lg mt-0.5">&#x2716;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-rose-600 dark:text-rose-400">When the exam hall strips away all your familiar clues</strong>, place-dependent memories become unreachable. You need knowledge that works anywhere, not just in your bedroom.</p>
            </div>
          </div>
        </MotionDiv>
      )}
    </div>
  );
};

// 2. CONTEXT CUE EXPLORER (Section 1 interactive)
const CUE_ICONS: Record<string, React.ReactNode> = {
  music: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>,
  desk: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>,
  coffee: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M18 8h1a4 4 0 010 8h-1"/><path d="M2 8h16v9a4 4 0 01-4 4H6a4 4 0 01-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/></svg>,
  pet: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>,
  window: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="12" y1="3" x2="12" y2="21"/></svg>,
  lamp: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>,
  silence: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><line x1="23" y1="9" x2="17" y2="15"/><line x1="17" y1="9" x2="23" y2="15"/></svg>,
  clock: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>,
  people: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></svg>,
  notes: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>,
  snacks: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><line x1="16.5" y1="9.4" x2="7.5" y2="4.21"/><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 002 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>,
  hoodie: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M20.38 3.46L16 2a4 4 0 01-8 0L3.62 3.46a2 2 0 00-1.34 2.23l.58 3.57a1 1 0 00.99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 002-2V10h2.15a1 1 0 00.99-.84l.58-3.57a2 2 0 00-1.34-2.23z"/></svg>,
};

const STUDY_CUES = [
  { id: 'music', label: 'Music playing', survivesExam: false },
  { id: 'desk', label: 'Familiar desk', survivesExam: false },
  { id: 'coffee', label: 'Coffee / tea', survivesExam: false },
  { id: 'pet', label: 'Pet nearby', survivesExam: false },
  { id: 'window', label: 'Window view', survivesExam: false },
  { id: 'lamp', label: 'Desk lamp', survivesExam: false },
  { id: 'silence', label: 'Silence', survivesExam: true },
  { id: 'clock', label: 'Clock ticking', survivesExam: true },
  { id: 'people', label: 'Other people', survivesExam: true },
  { id: 'notes', label: 'Written notes', survivesExam: false },
  { id: 'snacks', label: 'Snacks', survivesExam: false },
  { id: 'hoodie', label: 'Comfy hoodie', survivesExam: true },
];

const ContextCueExplorer = () => {
  const [selectedCues, setSelectedCues] = useState<Set<string>>(new Set());
  const [revealed, setRevealed] = useState(false);

  const toggleCue = (id: string) => {
    if (revealed) return;
    setSelectedCues((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const selectedCount = selectedCues.size;
  const survivingCount = STUDY_CUES.filter((c) => selectedCues.has(c.id) && c.survivesExam).length;
  const lostPercent = selectedCount > 0 ? Math.round(((selectedCount - survivingCount) / selectedCount) * 100) : 0;

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Your Study Environment Audit</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Pick the things that are around you when you study, then see how many of them will be there in the exam hall.</p>

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2.5 mb-6">
        {STUDY_CUES.map((cue) => {
          const isSelected = selectedCues.has(cue.id);
          return (
            <button
              key={cue.id}
              onClick={() => toggleCue(cue.id)}
              className="flex items-center gap-3 text-left transition-all duration-200"
              style={{
                backgroundColor: isSelected ? '#e8f5f2' : '#FFFFFF',
                border: isSelected ? '2px solid #2A7D6F' : '2px solid #d0cdc8',
                borderRadius: 14,
                padding: '14px 18px',
                color: isSelected ? '#1a6358' : '#9e9186',
                cursor: revealed ? 'default' : 'pointer',
              }}
            >
              <span style={{ flexShrink: 0, color: isSelected ? '#2A7D6F' : '#9e9186' }}>{CUE_ICONS[cue.id]}</span>
              <span style={{ fontSize: 14, fontWeight: isSelected ? 600 : 500, color: isSelected ? '#1a6358' : '#5a5550' }}>{cue.label}</span>
            </button>
          );
        })}
      </div>

      {selectedCount > 0 && !revealed && (
        <div className="text-center">
          <p className="text-sm mb-3" style={{ color: '#7a7068' }}>{selectedCount} cue{selectedCount !== 1 ? 's' : ''} selected</p>
          <button onClick={() => setRevealed(true)} style={{ backgroundColor: '#2A7D6F', borderRadius: 20, padding: '12px 24px', fontSize: 14, fontWeight: 600, color: '#FFFFFF' }}>
            See the Exam Hall
          </button>
        </div>
      )}

      <AnimatePresence>
        {revealed && (
          <MotionDiv initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.5 }}>
            <div className="grid md:grid-cols-2 gap-4 mb-6">
              {/* Study room */}
              <div className="bg-white dark:bg-zinc-900" style={{ border: '2px solid #1a1a1a', borderRadius: 14, padding: '16px 20px' }}>
                <p className="font-serif font-semibold mb-2" style={{ fontSize: 14, color: '#1a1a1a' }}>Your Study Room — {selectedCount} cues</p>
                <div className="flex flex-wrap gap-1.5">
                  {STUDY_CUES.filter((c) => selectedCues.has(c.id)).map((c) => (
                    <span key={c.id} className="inline-flex items-center gap-1.5" style={{ backgroundColor: '#e8f5f2', border: '1px solid rgba(42,125,111,0.2)', borderRadius: 20, padding: '4px 10px', fontSize: 12, fontWeight: 500, color: '#1a6358' }}>
                      <span style={{ color: '#2A7D6F' }}>{CUE_ICONS[c.id]}</span> {c.label}
                    </span>
                  ))}
                </div>
              </div>
              {/* Exam hall */}
              <div className="bg-white dark:bg-zinc-900" style={{ border: '2px solid #1a1a1a', borderRadius: 14, padding: '16px 20px' }}>
                <p className="font-serif font-semibold mb-2" style={{ fontSize: 14, color: '#1a1a1a' }}>The Exam Hall — {survivingCount} cue{survivingCount !== 1 ? 's' : ''} remain</p>
                <div className="flex flex-wrap gap-1.5">
                  {STUDY_CUES.filter((c) => selectedCues.has(c.id) && c.survivesExam).map((c) => (
                    <span key={c.id} className="inline-flex items-center gap-1.5" style={{ backgroundColor: '#e8f5f2', border: '1px solid rgba(42,125,111,0.2)', borderRadius: 20, padding: '4px 10px', fontSize: 12, fontWeight: 500, color: '#1a6358' }}>
                      <span style={{ color: '#2A7D6F' }}>{CUE_ICONS[c.id]}</span> {c.label}
                    </span>
                  ))}
                  {survivingCount === 0 && (
                    <span className="italic" style={{ fontSize: 12, color: '#E85D75' }}>Nothing matches — your brain has zero familiar clues to help you remember</span>
                  )}
                </div>
              </div>
            </div>

            {/* Stacked bar */}
            <div className="mb-4">
              <p style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', color: '#9e9186', marginBottom: 6, textTransform: 'uppercase' as const }}>Memory clues that survive</p>
              <div className="flex" style={{ border: '2px solid #1a1a1a', borderRadius: 100, height: 28, overflow: 'hidden' }}>
                {survivingCount > 0 && (
                  <MotionDiv className="h-full flex items-center justify-center" style={{ backgroundColor: '#2A7D6F' }} initial={{ width: 0 }} animate={{ width: `${100 - lostPercent}%` }} transition={{ duration: 0.8, ease: 'easeOut' }}>
                    {(100 - lostPercent) > 15 && <span style={{ fontSize: 11, fontWeight: 600, color: '#FFFFFF' }}>{100 - lostPercent}% survive</span>}
                  </MotionDiv>
                )}
                <MotionDiv className="h-full flex items-center justify-center" style={{ backgroundColor: '#E85D75' }} initial={{ width: 0 }} animate={{ width: `${lostPercent}%` }} transition={{ duration: 0.8, ease: 'easeOut', delay: 0.2 }}>
                  {lostPercent > 15 && <span style={{ fontSize: 11, fontWeight: 600, color: '#FFFFFF' }}>{lostPercent}% lost</span>}
                </MotionDiv>
              </div>
            </div>

            <div style={{ borderLeft: '3px solid #E85D75', backgroundColor: '#fde4e4', borderRadius: '0 10px 10px 0', padding: '12px 16px' }}>
              <p className="text-sm" style={{ color: '#b33030' }}>
                <strong>You lost {lostPercent}% of the clues your brain uses to remember.</strong>{' '}
                {lostPercent >= 75
                  ? 'Your memories are tied tightly to your study spot. Studying in different places would help your brain remember without needing those clues.'
                  : lostPercent >= 50
                  ? 'More than half your clues disappear in the exam hall. Switching up your study spots would make a big difference.'
                  : 'Some clues still survive, but mixing up where you study would make your knowledge even stronger.'}
              </p>
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
  );
};

// 3. NOISE LEVEL CURVE
const NoiseLevelCurve = () => {
  const [revealed, setRevealed] = useState(false);

  const W = 480, H = 280;
  const padL = 50, padR = 20, padT = 30, padB = 60;
  const chartW = W - padL - padR, chartH = H - padT - padB;
  const toX = (f: number) => padL + f * chartW;
  const toY = (f: number) => padT + (1 - f) * chartH;

  const noiseLabels = ['Silent', 'Whisper', 'Library', 'Cafe', 'Office', 'Traffic', 'Concert'];

  // Inverted-U bell curve: rises to peak at Cafe (~index 3), then drops
  const curvePoints = [
    { x: 0, y: 0.30 },
    { x: 0.083, y: 0.42 },
    { x: 0.167, y: 0.58 },
    { x: 0.25, y: 0.75 },
    { x: 0.333, y: 0.88 },
    { x: 0.417, y: 0.95 },
    { x: 0.50, y: 0.97 },  // Peak (Cafe)
    { x: 0.583, y: 0.92 },
    { x: 0.667, y: 0.78 },
    { x: 0.75, y: 0.55 },
    { x: 0.833, y: 0.35 },
    { x: 0.917, y: 0.20 },
    { x: 1.0, y: 0.12 },
  ];

  const buildCurve = (points: { x: number; y: number }[]) => {
    const pts = points.map((p) => ({ x: toX(p.x), y: toY(p.y) }));
    let d = `M ${pts[0].x} ${pts[0].y}`;
    for (let i = 1; i < pts.length; i++) {
      const cx1 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.5;
      const cx2 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.5;
      d += ` C ${cx1} ${pts[i - 1].y}, ${cx2} ${pts[i].y}, ${pts[i].x} ${pts[i].y}`;
    }
    return d;
  };

  const buildArea = (points: { x: number; y: number }[]) => {
    return buildCurve(points) + ` L ${toX(1)} ${toY(0)} L ${toX(0)} ${toY(0)} Z`;
  };

  // Focused/analytical peak is slightly quieter (Library zone ~0.30)
  const focusedPeakX = 0.30;
  const focusedPeakY = 0.82;
  // Creative/conceptual peak is slightly louder (Cafe zone ~0.50)
  const creativePeakX = 0.50;
  const creativePeakY = 0.97;

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      <div className="text-center mb-6">
        <span className="inline-block px-3 py-1 rounded-full text-[11px] font-bold tracking-wider uppercase mb-3" style={{ backgroundColor: '#e8f5f2', color: '#1a6358', border: '1px solid rgba(42,125,111,0.2)', letterSpacing: '0.06em' }}>Research Evidence</span>
        <h4 className="font-serif font-bold" style={{ fontSize: 24, color: '#1a1a1a' }}>The Noise-Performance Curve</h4>
        <p className="text-sm mt-1" style={{ color: '#7a7068' }}>How noise level affects how well your brain performs.</p>
      </div>

      {!revealed ? (
        <div className="text-center">
          <p className="text-sm mb-4" style={{ color: '#7a7068' }}>Is silence always best for studying? Or does a little noise actually help?</p>
          <button onClick={() => setRevealed(true)} style={{ backgroundColor: '#2A7D6F', borderRadius: 20, padding: '12px 24px', fontSize: 14, fontWeight: 600, color: '#FFFFFF' }}>
            See the Noise Curve
          </button>
        </div>
      ) : (
        <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
          <div className="bg-white dark:bg-zinc-900" style={{ border: '2px solid #1a1a1a', borderRadius: 16, padding: '28px 24px' }}>
            <svg viewBox={`0 0 ${W} ${H}`} className="w-full">
              {/* Grid lines */}
              {[0.25, 0.5, 0.75, 1.0].map((v) => (
                <line key={v} x1={padL} x2={W - padR} y1={toY(v)} y2={toY(v)} stroke="#f0ece6" strokeWidth="1" />
              ))}
              <line x1={padL} x2={W - padR} y1={toY(0)} y2={toY(0)} stroke="#d0cdc8" strokeWidth="1.5" />
              <line x1={padL} y1={padT} x2={padL} y2={toY(0)} stroke="#d0cdc8" strokeWidth="1.5" />

              {/* Sweet spot zone */}
              <rect x={toX(0.22)} y={padT} width={toX(0.62) - toX(0.22)} height={chartH} fill="rgba(42,125,111,0.06)" rx="4" />
              <rect x={toX(0.22)} y={padT} width={toX(0.62) - toX(0.22)} height={chartH} fill="none" stroke="rgba(42,125,111,0.15)" strokeWidth="1" strokeDasharray="4 3" rx="4" />

              {/* Zone labels */}
              <text x={toX(0.08)} y={toY(0.05)} fontSize="10" fill="#9e9186" textAnchor="middle" fontWeight="600">Too quiet</text>
              <text x={toX(0.88)} y={toY(0.05)} fontSize="10" fill="#9e9186" textAnchor="middle" fontWeight="600">Too loud</text>

              {/* Sweet spot label — positioned above chart to avoid overlap */}
              <rect x={toX(0.42) - 32} y={padT - 20} width="64" height="16" rx="8" fill="white" stroke="rgba(42,125,111,0.2)" strokeWidth="1" />
              <text x={toX(0.42)} y={padT - 9} fontSize="9" fill="#1a6358" textAnchor="middle" fontWeight="700">Sweet spot</text>

              {/* Area fill */}
              <motion.path d={buildArea(curvePoints)} fill="rgba(42,125,111,0.08)" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.8 }} />

              {/* Curve line */}
              <motion.path d={buildCurve(curvePoints)} fill="none" stroke="#2A7D6F" strokeWidth="3" strokeLinecap="round" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1.5, ease: 'easeOut' }} />

              {/* Focused/Analytical marker — offset left to avoid overlap */}
              <motion.circle cx={toX(focusedPeakX)} cy={toY(focusedPeakY)} r="6" fill="#2A7D6F" stroke="white" strokeWidth="2.5" initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 1.0 }} />
              <motion.g initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.2 }}>
                <line x1={toX(focusedPeakX)} y1={toY(focusedPeakY) - 8} x2={toX(focusedPeakX) - 30} y2={toY(focusedPeakY) - 35} stroke="#d0cdc8" strokeWidth="1" />
                <rect x={toX(focusedPeakX) - 72} y={toY(focusedPeakY) - 47} width="84" height="18" rx="9" fill="white" stroke="rgba(42,125,111,0.2)" strokeWidth="1" />
                <text x={toX(focusedPeakX) - 30} y={toY(focusedPeakY) - 34} fontSize="9" fill="#2A7D6F" textAnchor="middle" fontWeight="600">Focused tasks</text>
              </motion.g>

              {/* Creative/Conceptual marker — offset right */}
              <motion.circle cx={toX(creativePeakX)} cy={toY(creativePeakY)} r="6" fill="#2A7D6F" stroke="white" strokeWidth="2.5" initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 1.3 }} />
              <motion.g initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.5 }}>
                <line x1={toX(creativePeakX)} y1={toY(creativePeakY) - 8} x2={toX(creativePeakX) + 30} y2={toY(creativePeakY) - 35} stroke="#d0cdc8" strokeWidth="1" />
                <rect x={toX(creativePeakX) - 12} y={toY(creativePeakY) - 47} width="84" height="18" rx="9" fill="white" stroke="rgba(42,125,111,0.2)" strokeWidth="1" />
                <text x={toX(creativePeakX) + 30} y={toY(creativePeakY) - 34} fontSize="9" fill="#2A7D6F" textAnchor="middle" fontWeight="600">Creative tasks</text>
              </motion.g>

              {/* X-axis labels */}
              {noiseLabels.map((label, i) => (
                <text key={label} x={toX(i / (noiseLabels.length - 1))} y={toY(0) + 16} fontSize="11" fill="#b0a898" textAnchor="middle">{label}</text>
              ))}

              {/* Axis labels */}
              <text x={W / 2} y={H - 4} fontSize="11" fill="#9e9186" textAnchor="middle" letterSpacing="0.05em">Noise Level →</text>
              <text x={12} y={H / 2} fontSize="11" fill="#9e9186" textAnchor="middle" letterSpacing="0.05em" transform={`rotate(-90, 12, ${H / 2})`}>Performance →</text>
              <text x={padL + 2} y={toY(1.0) - 4} fontSize="11" fill="#b0a898">High</text>
              <text x={padL + 2} y={toY(0) - 4} fontSize="11" fill="#b0a898">Low</text>
            </svg>
          </div>

          <div className="grid md:grid-cols-2 gap-3 mt-4">
            <div className="flex items-start gap-3" style={{ borderLeft: '3px solid #2A7D6F', backgroundColor: '#f0faf8', borderRadius: '0 10px 10px 0', padding: '12px 16px' }}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2A7D6F" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ flexShrink: 0, marginTop: 2 }}><circle cx="12" cy="12" r="10"/><line x1="22" y1="12" x2="18" y2="12"/><line x1="6" y1="12" x2="2" y2="12"/><line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/></svg>
              <p style={{ fontSize: 14, color: '#1a6358' }}><strong>Focused tasks</strong> (maths problems, memorisation) work best in quiet spots. Silence lets you concentrate without distraction.</p>
            </div>
            <div className="flex items-start gap-3" style={{ borderLeft: '3px solid #d0cdc8', backgroundColor: '#f4f0eb', borderRadius: '0 10px 10px 0', padding: '12px 16px' }}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7a7068" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ flexShrink: 0, marginTop: 2 }}><line x1="9" y1="18" x2="15" y2="18"/><line x1="10" y1="22" x2="14" y2="22"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0018 8 6 6 0 006 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 018.91 14"/></svg>
              <p style={{ fontSize: 14, color: '#7a7068' }}><strong style={{ color: '#5a5550' }}>Creative tasks</strong> (understanding concepts, making connections) benefit from a bit of background noise. The buzz of a cafe nudges your brain into bigger-picture thinking.</p>
            </div>
          </div>
        </MotionDiv>
      )}
    </div>
  );
};

// 4. TASK ENVIRONMENT MATCHER (Section 3 interactive)
const TASK_ITEMS = [
  { id: 'maths', label: 'Maths past paper', correct: 'quiet' as const, reason: 'Maths needs careful step-by-step focus — noise breaks your concentration when you need it most.' },
  { id: 'history', label: 'History essay planning', correct: 'moderate' as const, reason: 'Essay planning is creative work — a bit of background noise actually helps you think more broadly.' },
  { id: 'vocab', label: 'Language vocabulary drill', correct: 'quiet' as const, reason: 'Memorising vocab needs sharp focus — even a little noise makes it harder to lock new words into your memory.' },
  { id: 'physics', label: 'Physics concept mapping', correct: 'moderate' as const, reason: 'Connecting physics ideas is creative thinking — some background noise nudges your brain into bigger-picture mode.' },
  { id: 'chem', label: 'Chemistry equation balancing', correct: 'quiet' as const, reason: 'Balancing equations is precise, step-by-step work — noise pulls your attention away from the details.' },
  { id: 'english', label: 'English literature analysis', correct: 'moderate' as const, reason: 'Analysing literature means making connections between ideas — a bit of noise helps your brain think more creatively.' },
];

const TaskEnvironmentMatcher = () => {
  const [answers, setAnswers] = useState<Record<string, 'quiet' | 'moderate'>>({});
  const [submitted, setSubmitted] = useState(false);

  const allAnswered = TASK_ITEMS.every((t) => answers[t.id]);
  const score = submitted ? TASK_ITEMS.filter((t) => answers[t.id] === t.correct).length : 0;

  const setAnswer = (id: string, val: 'quiet' | 'moderate') => {
    if (submitted) return;
    setAnswers((prev) => ({ ...prev, [id]: val }));
  };

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Match the Task to the Environment</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">For each study task, decide: quiet or moderate noise?</p>

      <div className="space-y-3 mb-6">
        {TASK_ITEMS.map((task) => {
          const answer = answers[task.id];
          const isCorrect = submitted && answer === task.correct;
          const _isWrong = submitted && answer !== task.correct;
          return (
            <div key={task.id} className="rounded-xl p-3 transition-colors" style={{
              backgroundColor: submitted ? (isCorrect ? '#6EE7B7' : '#FCA5A5') : '#FFFFFF',
              border: submitted ? `2.5px solid ${isCorrect ? '#059669' : '#DC2626'}` : '1.5px solid #E7E5E4',
              boxShadow: submitted ? `3px 3px 0px 0px ${isCorrect ? '#059669' : '#DC2626'}` : 'none',
            }}>
              <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4">
                <p className="text-sm font-semibold text-zinc-700 dark:text-zinc-200 flex-1">{task.label}</p>
                <div className="flex gap-2">
                  <button
                    onClick={() => setAnswer(task.id, 'quiet')}
                    className={`px-3 py-1.5 rounded-lg text-xs font-bold ${submitted ? 'cursor-default' : 'cursor-pointer'}`}
                    style={{
                      backgroundColor: answer === 'quiet' ? '#93C5FD' : '#FFFFFF',
                      border: `2px solid ${answer === 'quiet' ? '#2563EB' : '#1C1917'}`,
                      borderRadius: 10,
                      boxShadow: answer === 'quiet' ? 'none' : '2px 2px 0px 0px #1C1917',
                      color: answer === 'quiet' ? '#1E3A8A' : '#1C1917',
                    }}
                  >
                    Quiet
                  </button>
                  <button
                    onClick={() => setAnswer(task.id, 'moderate')}
                    className={`px-3 py-1.5 rounded-lg text-xs font-bold ${submitted ? 'cursor-default' : 'cursor-pointer'}`}
                    style={{
                      backgroundColor: answer === 'moderate' ? '#FCD34D' : '#FFFFFF',
                      border: `2px solid ${answer === 'moderate' ? '#D97706' : '#1C1917'}`,
                      borderRadius: 10,
                      boxShadow: answer === 'moderate' ? 'none' : '2px 2px 0px 0px #1C1917',
                      color: answer === 'moderate' ? '#78350F' : '#1C1917',
                    }}
                  >
                    Moderate Noise
                  </button>
                </div>
              </div>
              {submitted && (
                <MotionDiv initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} transition={{ duration: 0.3 }}>
                  <div className="mt-2 flex items-start gap-2">
                    <span className={`text-sm mt-0.5 ${isCorrect ? 'text-emerald-500' : 'text-rose-500'}`}>
                      {isCorrect ? '✓' : '✗'}
                    </span>
                    <p className="text-xs text-zinc-500 dark:text-zinc-400">
                      <strong className={isCorrect ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}>
                        {isCorrect ? 'Correct' : `Correct answer: ${task.correct === 'quiet' ? 'Quiet' : 'Moderate Noise'}`}
                      </strong>{' — '}
                      {task.reason}
                    </p>
                  </div>
                </MotionDiv>
              )}
            </div>
          );
        })}
      </div>

      {!submitted && allAnswered && (
        <div className="text-center">
          <button onClick={() => setSubmitted(true)} className="px-5 py-2.5 text-sm font-bold rounded-lg bg-purple-500 text-white hover:bg-purple-600 transition-colors">
            Check My Answers
          </button>
        </div>
      )}

      <AnimatePresence>
        {submitted && (
          <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.4 }}>
            <div className="p-4 rounded-xl text-center" style={{
              backgroundColor: score >= 5 ? '#6EE7B7' : score >= 3 ? '#FCD34D' : '#FCA5A5',
              border: `2.5px solid ${score >= 5 ? '#059669' : score >= 3 ? '#D97706' : '#DC2626'}`,
              boxShadow: `3px 3px 0px 0px ${score >= 5 ? '#059669' : score >= 3 ? '#D97706' : '#DC2626'}`,
            }}>
              <p className="text-3xl font-bold text-zinc-800 dark:text-white mb-1">{score}/{TASK_ITEMS.length}</p>
              <p className="text-sm text-zinc-500 dark:text-zinc-400">
                {score === 6
                  ? 'Perfect! You understand exactly how to match tasks to environments.'
                  : score >= 4
                  ? 'Strong intuition — the key principle is: focused/precise tasks need quiet, creative/conceptual tasks benefit from moderate noise.'
                  : 'The rule of thumb: if a task needs precise, step-by-step processing, choose quiet. If it involves making connections or creative thinking, moderate noise helps.'}
              </p>
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
  );
};

// 5. STUDY LOCATION PLANNER (Section 5 interactive)
const PLANNER_SUBJECTS = ['Biology', 'Maths', 'English', 'History'];
const PLANNER_DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
const PLANNER_LOCATIONS = [
  { id: 'none', label: '—', bgClass: 'bg-zinc-100 dark:bg-zinc-700', textClass: 'text-zinc-400 dark:text-zinc-500' },
  { id: 'bedroom', label: 'Bedroom', bgClass: 'bg-blue-100 dark:bg-blue-900/50', textClass: 'text-blue-700 dark:text-blue-300' },
  { id: 'kitchen', label: 'Kitchen', bgClass: 'bg-amber-100 dark:bg-amber-900/50', textClass: 'text-amber-700 dark:text-amber-300' },
  { id: 'library', label: 'Library', bgClass: 'bg-emerald-100 dark:bg-emerald-900/50', textClass: 'text-emerald-700 dark:text-emerald-300' },
  { id: 'cafe', label: 'Cafe', bgClass: 'bg-purple-100 dark:bg-purple-900/50', textClass: 'text-purple-700 dark:text-purple-300' },
  { id: 'school', label: 'School', bgClass: 'bg-rose-100 dark:bg-rose-900/50', textClass: 'text-rose-700 dark:text-rose-300' },
];

const StudyLocationPlanner = () => {
  // grid[subjectIndex][dayIndex] = locationIndex (0=none, 1-5=locations)
  const [grid, setGrid] = useState<number[][]>(
    PLANNER_SUBJECTS.map(() => PLANNER_DAYS.map(() => 0))
  );
  const [scored, setScored] = useState(false);

  const cycleCell = (si: number, di: number) => {
    if (scored) return;
    setGrid((prev) => {
      const next = prev.map((row) => [...row]);
      next[si][di] = (next[si][di] + 1) % PLANNER_LOCATIONS.length;
      return next;
    });
  };

  const getSubjectScore = (subjectRow: number[]): number => {
    const usedLocations = new Set(subjectRow.filter((v) => v > 0));
    const filledDays = subjectRow.filter((v) => v > 0).length;
    if (filledDays <= 1) return 0;
    // Score = unique locations / filled days, scaled to 100
    return Math.round((usedLocations.size / filledDays) * 100);
  };

  const subjectScores = grid.map(getSubjectScore);
  const hasAnyFilled = grid.some((row) => row.some((v) => v > 0));
  const overallScore = Math.round(subjectScores.reduce((a, b) => a + b, 0) / PLANNER_SUBJECTS.length);

  const getVerdict = (score: number): { label: string; colorClass: string } => {
    if (score >= 80) return { label: 'Great variety (strong)', colorClass: 'text-emerald-600 dark:text-emerald-400' };
    if (score >= 50) return { label: 'Some variety', colorClass: 'text-amber-600 dark:text-amber-400' };
    return { label: 'Stuck in one spot (risky)', colorClass: 'text-rose-600 dark:text-rose-400' };
  };

  // Ring gauge SVG
  const ringRadius = 40;
  const ringCircumference = 2 * Math.PI * ringRadius;
  const ringOffset = ringCircumference - (overallScore / 100) * ringCircumference;

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Your Weekly Location Planner</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Click each cell to assign a study location. Mix up your spots across the week so your knowledge works anywhere.</p>

      {/* Planner grid */}
      <div className="overflow-x-auto mb-6">
        <table className="w-full border-collapse text-center">
          <thead>
            <tr>
              <th className="p-2 text-xs font-bold text-zinc-400 dark:text-zinc-500 text-left w-24"></th>
              {PLANNER_DAYS.map((day) => (
                <th key={day} className="p-2 text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">{day}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {PLANNER_SUBJECTS.map((subject, si) => (
              <tr key={subject}>
                <td className="p-2 text-sm font-semibold text-zinc-700 dark:text-zinc-200 text-left">{subject}</td>
                {PLANNER_DAYS.map((_, di) => {
                  const loc = PLANNER_LOCATIONS[grid[si][di]];
                  return (
                    <td key={di} className="p-1">
                      <button
                        onClick={() => cycleCell(si, di)}
                        className={`w-full py-2 px-1 rounded-md text-[11px] font-bold border border-transparent transition-all duration-150 ${loc.bgClass} ${loc.textClass} ${scored ? 'cursor-default' : 'cursor-pointer hover:scale-105 active:scale-95'}`}
                      >
                        {loc.label}
                      </button>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Legend */}
      <div className="flex flex-wrap justify-center gap-2 mb-6">
        {PLANNER_LOCATIONS.slice(1).map((loc) => (
          <span key={loc.id} className={`inline-flex items-center px-2 py-1 rounded-md text-[10px] font-bold ${loc.bgClass} ${loc.textClass}`}>
            {loc.label}
          </span>
        ))}
      </div>

      {hasAnyFilled && !scored && (
        <div className="text-center">
          <button onClick={() => setScored(true)} className="px-5 py-2.5 text-sm font-bold rounded-lg bg-purple-500 text-white hover:bg-purple-600 transition-colors">
            See My Score
          </button>
        </div>
      )}

      <AnimatePresence>
        {scored && (
          <MotionDiv initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.5 }}>
            <div className="flex flex-col items-center mb-6">
              <svg width="100" height="100" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r={ringRadius} fill="none" stroke="#e4e4e7" className="dark:stroke-zinc-700" strokeWidth="8" />
                <motion.circle
                  cx="50" cy="50" r={ringRadius}
                  fill="none"
                  stroke={overallScore >= 60 ? '#10b981' : overallScore >= 30 ? '#f59e0b' : '#ef4444'}
                  strokeWidth="8"
                  strokeLinecap="round"
                  strokeDasharray={ringCircumference}
                  strokeDashoffset={ringCircumference}
                  animate={{ strokeDashoffset: ringOffset }}
                  transition={{ duration: 1, ease: 'easeOut' }}
                  transform="rotate(-90 50 50)"
                />
                <text x="50" y="46" textAnchor="middle" fontSize="18" fontWeight="bold" fill="currentColor" className="text-zinc-800 dark:text-white">{overallScore}</text>
                <text x="50" y="60" textAnchor="middle" fontSize="9" fill="#a1a1aa">/ 100</text>
              </svg>
              <p className="text-sm font-bold text-zinc-700 dark:text-zinc-200 mt-2">Location Variety Score</p>
            </div>

            <div className="space-y-2">
              {PLANNER_SUBJECTS.map((subject, si) => {
                const s = subjectScores[si];
                const v = getVerdict(s);
                const filledDays = grid[si].filter((val) => val > 0).length;
                return (
                  <div key={subject} className="flex items-center gap-3 p-2.5 rounded-lg bg-zinc-50 dark:bg-zinc-900/40 border border-zinc-200 dark:border-zinc-700">
                    <span className="text-sm font-semibold text-zinc-700 dark:text-zinc-200 w-20">{subject}</span>
                    <div className="flex-1 h-2 rounded-full bg-zinc-200 dark:bg-zinc-700 overflow-hidden">
                      <MotionDiv
                        className={`h-full rounded-full ${s >= 80 ? 'bg-emerald-500' : s >= 50 ? 'bg-amber-500' : 'bg-rose-500'}`}
                        initial={{ width: 0 }}
                        animate={{ width: `${s}%` }}
                        transition={{ duration: 0.6, ease: 'easeOut' }}
                      />
                    </div>
                    <span className="text-xs font-bold w-8 text-right text-zinc-500 dark:text-zinc-400">{s}%</span>
                    <span className={`text-xs font-bold w-44 text-right ${v.colorClass}`}>
                      {filledDays === 0 ? 'No sessions planned' : v.label}
                    </span>
                  </div>
                );
              })}
            </div>

            <div className="mt-4 p-3 rounded-lg bg-purple-50 dark:bg-purple-950/30 border border-purple-200 dark:border-purple-900">
              <p className="text-sm text-zinc-600 dark:text-zinc-300">
                {overallScore >= 70
                  ? <><strong className="text-emerald-600 dark:text-emerald-400">Excellent variety!</strong> Your study plan means your knowledge will work anywhere, including the exam hall.</>
                  : overallScore >= 40
                  ? <><strong className="text-amber-600 dark:text-amber-400">Good start, but more variety would help.</strong> Try adding a second or third spot for each subject so your memories are not tied to one place.</>
                  : <><strong className="text-rose-600 dark:text-rose-400">Your knowledge is stuck in one spot.</strong> Each subject should be studied in at least 2 different places across the week so you can remember it anywhere.</>
                }
              </p>
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
  );
};

// --- MODULE COMPONENT ---
const TheContextEffectModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'context-dependent-memory', title: 'Why You Blank in the Exam Hall', eyebrow: '01 // The Problem', icon: Map },
    { id: 'variation-advantage', title: "The 'Switch It Up' Fix", eyebrow: '02 // The Solution', icon: Repeat },
    { id: 'noise-question', title: 'Does Noise Help or Hurt?', eyebrow: '03 // The Noise Question', icon: Activity },
    { id: 'encoding-variability', title: 'Why Switching Spots Works', eyebrow: '04 // How It Works', icon: Brain },
    { id: 'designing-environments', title: 'Setting Up Your Study Rotation', eyebrow: '05 // Your Game Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="49"
      moduleTitle="The Context Effect"
      moduleSubtitle="Where You Study Matters"
      moduleDescription="Where you study changes what you remember. Learn why switching study spots beats sticking to one 'perfect' place."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Switch It Up"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Why You Blank in the Exam Hall." eyebrow="Step 1" icon={Map} theme={theme}>
              {essentials ? (
                <>
                  <p>Your brain links what you learn to where you learn it. The room, the sounds, the lighting all become memory clues. People tested in the same place they studied recalled 40% more.</p>
                  <p>This is why you blank in the exam hall. It strips away every familiar clue your brain was relying on. The knowledge is still there -- your brain just cannot find the path to it.</p>
                </>
              ) : (
                <>
                  <p>In one of psychology's most famous experiments, divers learned word lists either underwater or on dry land, then were tested in either the same or a different environment. The result? Those tested in the <Highlight description="The place where you study — the room, the sounds, the lighting — all get tangled up with what you learn. Your brain links the info to the surroundings, so the same surroundings help you remember." theme={theme}>same environment</Highlight> they learned in recalled about 40% more. Your brain doesn't just store the information — it stores the whole scene around you: the room, the lighting, the sounds, even the smell.</p>
                  <PersonalStory name="Aoife" role="5th Year, Cork">
                    <p>I used to do all my study in my bedroom with music on. I felt like I knew everything. Then I'd sit down in the exam hall and my mind would just go blank. I couldn't understand it — I'd studied for hours. It was like my brain left everything back in my room.</p>
                  </PersonalStory>
                  <p>These <Highlight description="Things in your surroundings �� background noise, the feel of your chair, the lighting, even your posture — that get linked to what you're learning. Your brain uses them like bookmarks to find the right memory later." theme={theme}>study environment clues</Highlight> become the paths your brain uses to find what it learned. This is why you can remember something perfectly in your bedroom but draw a complete blank in the exam hall. The exam hall has stripped away every familiar clue your brain was relying on.</p>
                  <p>If you only ever study in one place, your memories become <Highlight description="When a memory is strongly linked to one specific place, you can only pull it back reliably in that place. The knowledge is still in your brain, but without the right surroundings your brain can't find it. It's not that you didn't learn it — your brain just lost the path to it." theme={theme}>stuck to that spot</Highlight> — deeply tied to that specific environment. They feel solid and easy to access in your bedroom. But move to an unfamiliar exam hall with fluorescent lights and rows of desks, and those same memories can suddenly feel unreachable. The knowledge is still there; your brain just can't find the path to it without its usual signposts.</p>
                </>
              )}
              <ContextMemoryComparison />
              <ContextCueExplorer />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The 'Switch It Up' Fix." eyebrow="Step 2" icon={Repeat} theme={theme}>
              {essentials ? (
                <>
                  <p>Students who studied in two different rooms recalled 40% more than those who stayed in one room. When you study in multiple places, your brain creates <strong>location-proof memories</strong> that work anywhere.</p>
                  <p>Each new place adds different connections to the same information. More connections means more ways your brain can find it -- even in an unfamiliar exam hall.</p>
                </>
              ) : (
                <>
                  <p>Researchers found something surprising: students who studied the same material in <Highlight description="When you study the same thing in two different places, your brain can't rely on any single room to help it remember. So it stores the information in a way that works anywhere." theme={theme}>two different rooms</Highlight> recalled about 40% more than those who studied in the same room twice. This seems to go against what we just learned about your brain linking memories to places — but it actually goes one step further.</p>
                  <p>When you study in multiple places, your brain can't rely on any single place as a clue, so it creates <Highlight description="Memories that aren't tied to any one place. Instead of needing your bedroom lamp or the sound of rain to remember, your brain connects the info to the ideas themselves. That makes the knowledge portable — it works anywhere, including the exam hall." theme={theme}>location-proof memories</Highlight>. The knowledge becomes portable — it works anywhere, including an unfamiliar exam hall. Instead of storing "this fact + my bedroom lamp + the sound of rain," your brain stores "this fact + lots of different connections," creating a web of memory paths that doesn't depend on any single place.</p>
                  <p>This is sometimes called the <Highlight description="When you study the same thing in different places, each place adds a new set of connections to that memory. More connections means more ways your brain can find the information later, even in a totally new setting like an exam hall." theme={theme}>variety advantage</Highlight>: different study spots create multiple paths to the same information. Each new place adds a different set of connections — the hum of a cafe, the silence of a library, the kitchen radio in the background. When exam day arrives and none of those specific clues are around, it doesn't matter. Your brain has so many alternative paths that some of them will activate, letting you remember even in a completely new setting.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Does Noise Help or Hurt?" eyebrow="Step 3" icon={Activity} theme={theme}>
              {essentials ? (
                <>
                  <p>Moderate background noise boosts creative thinking. But for focused tasks like maths problems or memorisation, quiet is better. The rule is simple: match your noise level to your task.</p>
                  <p>Reading a chapter for understanding? A cafe might help. Drilling past papers or memorising vocab? You need silence. Choose your environment based on what you are doing.</p>
                </>
              ) : (
                <>
                  <p>Here's a surprising finding: moderate background noise (about the level of a busy cafe) actually <Highlight description="A bit of background buzz — like in a cafe ��� gives your brain just enough of a challenge to push it into bigger-picture thinking. It's not so loud that it distracts you, but it's enough to stop you from getting too narrowly focused." theme={theme}>boosts creative thinking</Highlight> compared to both total silence and loud noise. A bit of background buzz creates just enough of a challenge — a kind of <Highlight description="Sometimes making studying feel a little harder actually helps you learn better in the long run. A small amount of background noise is one example — it slightly disrupts your focus, which pushes your brain into a broader way of thinking that helps with creative tasks." theme={theme}>helpful challenge</Highlight> — to push your thinking from narrow, step-by-step mode into bigger-picture mode.</p>
                  <p>However, decades of research have shown that for tasks needing focused concentration — like maths problem-solving or detailed memorisation — <Highlight description="Research across many studies found that noise consistently hurts performance on tasks that need careful, focused attention. But for creative or big-picture tasks, a moderate amount of noise can sometimes help." theme={theme}>quiet is better</Highlight>. Noise gets in the way of the careful, step-by-step thinking these tasks need. The practical rule is simple: use moderate noise for understanding and connecting ideas, use silence for memorisation and practice problems.</p>
                  <p>This means your study environment should match your task. Reading a history chapter to understand the big picture? A cafe might actually help your thinking. Drilling past paper questions in maths or memorising vocabulary? You need silence. The environment isn't just a backdrop — it's an active ingredient in how well your brain works. Planning your study sessions around this means deliberately choosing where you work based on what you're working on.</p>
                </>
              )}
              <NoiseLevelCurve />
              <TaskEnvironmentMatcher />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Why Switching Spots Works." eyebrow="Step 4" icon={Brain} theme={theme}>
              {essentials ? (
                <>
                  <p>Each new study location wraps your information in different clues. More varied clues means more routes your brain has to find the memory. Think of it as building multiple roads to the same city.</p>
                  <p>This effect stacks with other good habits like spaced repetition and self-testing. Switching spots is not a replacement for good study techniques -- it is a booster on top of them.</p>
                </>
              ) : (
                <>
                  <p>Here's the science behind it: every time you study the same material in a different place, you create a <Highlight description="Each time you study in a new spot, your brain wraps the information in different surroundings — the sounds, the feel of the chair, the lighting. Each version gives your brain a different path to find that memory later." theme={theme}>new set of connections</Highlight>. Each place adds different clues. The more varied those clues are, the more routes your brain has to find the memory. Think of it like building roads to a city — one road is vulnerable to a single blocked bridge, but five roads from different directions means you can always find a way through.</p>
                  <p>This is why studying the same flashcards on the bus, in your bedroom, and in the library creates stronger memories than studying them three times in the same spot. Each location wraps the information in a different package. The bus adds the rumble of the engine and the movement. Your bedroom adds the familiar sounds of home. The library adds the particular quality of silence and the presence of other students. Each version of the memory is slightly different, and those differences create <Highlight description="Your brain doesn't store memories in just one place — it builds a web of connections. Each time you study in a new spot, you add another thread to that web. More threads means more ways to pull the memory back, so even if one path is blocked, others still work." theme={theme}>backup paths to the same information</Highlight>.</p>
                  <p>Research has confirmed that studying in different places reliably <Highlight description="Studies show this effect is real and consistent. It's not huge on its own, but it stacks on top of other good study habits like spaced repetition and mixing topics. Together, they make a much bigger difference." theme={theme}>improves how well you remember</Highlight>. The effect is not massive on its own, but it stacks with other good habits like spaced repetition and mixing topics. This is key — switching study spots is not a replacement for other good study strategies; it's a booster. When you combine varied locations with regular self-testing and mixed topics, the combined effect on long-term memory is much bigger than any single trick alone.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Setting Up Your Study Rotation." eyebrow="Step 5" icon={Wrench} theme={theme}>
              {essentials ? (
                <p>Pick 2-3 genuinely different study spots. Study each subject in at least two different places per week. Use quiet for practice problems and moderate noise for reading. Practise in exam-like conditions too.</p>
              ) : (
                <p>The research points to a simple game plan.</p>
              )}
              <ConceptCardGrid
                cards={[
                  { number: 1, term: "Pick 2-3 Study Spots", description: "Rotate between genuinely different places — bedroom, kitchen table, library, cafe. They don't need to be fancy; the differences between these spaces are what give your brain the variety it needs." },
                  { number: 2, term: "Same Subject, Different Spots", description: "Study the same subject in at least two different spots across the week. Study Biology in your bedroom on Monday and in the library on Wednesday. Same content, different places, more paths to the memory." },
                  { number: 3, term: "Match Your Noise Level", description: "Quiet for practice problems and memorisation, a bit of background noise for reading and understanding. The best noise level depends on what you're doing." },
                  { number: 4, term: "Practise in Exam-Like Conditions", description: "Sit at a quiet desk with a timer, recreating the exam hall as closely as you can. Students who practised remembering things in exam-like conditions did better in the real exam.", highlight: true },
                ]}
              />
              <StudyLocationPlanner />
              <MicroCommitment theme={theme}>
                <p>This week, take one subject you'd normally study in the same spot and split it across two different locations. Study the same material in your bedroom on Tuesday and in the school library or kitchen on Thursday. Notice how remembering the same content in a different setting feels harder — that extra effort is what builds memories that work anywhere, including the exam hall.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};

export default TheContextEffectModule;
