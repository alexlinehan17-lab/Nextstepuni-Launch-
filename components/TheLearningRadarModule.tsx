/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Target, AlertTriangle, Clock, Layers, Activity, Flag } from 'lucide-react';
import { ModuleProgress } from '../types';
import { violetTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = violetTheme;
const MotionDiv = motion.div as any;

// --- INTERACTIVE COMPONENTS ---

// 1. CALIBRATION QUIZ
const CALIBRATION_STATEMENTS = [
  { statement: 'The Great Wall of China is visible from space with the naked eye.', answer: false },
  { statement: 'Humans use only 10% of their brain.', answer: false },
  { statement: 'Sound travels faster through water than through air.', answer: true },
  { statement: 'An octopus has three hearts.', answer: true },
  { statement: 'Lightning never strikes the same place twice.', answer: false },
  { statement: 'Bananas grow on trees.', answer: false },
  { statement: 'The Sahara is the largest desert in the world.', answer: false },
  { statement: 'Diamond is the hardest natural substance on Earth.', answer: true },
];

const CONFIDENCE_LEVELS = [25, 50, 75, 100];

const CalibrationQuiz = () => {
  const [step, setStep] = useState(0); // 0-7 = questions, 8 = results
  const [phase, setPhase] = useState<'confidence' | 'answer'>('confidence');
  const [responses, setResponses] = useState<{ confidence: number; correct: boolean }[]>([]);
  const [currentConfidence, setCurrentConfidence] = useState<number | null>(null);

  const handleConfidence = (level: number) => {
    setCurrentConfidence(level);
    setPhase('answer');
  };

  const handleAnswer = (answer: boolean) => {
    const correct = answer === CALIBRATION_STATEMENTS[step].answer;
    setResponses((prev) => [...prev, { confidence: currentConfidence!, correct }]);
    setCurrentConfidence(null);
    setPhase('confidence');
    setStep((s) => s + 1);
  };

  const reset = () => {
    setStep(0);
    setPhase('confidence');
    setResponses([]);
    setCurrentConfidence(null);
  };

  // Calculate calibration data for results
  const getCalibrationData = () => {
    const buckets: Record<number, { total: number; correct: number }> = {};
    CONFIDENCE_LEVELS.forEach((l) => (buckets[l] = { total: 0, correct: 0 }));
    responses.forEach((r) => {
      buckets[r.confidence].total++;
      if (r.correct) buckets[r.confidence].correct++;
    });
    return CONFIDENCE_LEVELS.map((level) => ({
      level,
      predicted: level,
      actual: buckets[level].total > 0 ? Math.round((buckets[level].correct / buckets[level].total) * 100) : null,
      count: buckets[level].total,
    }));
  };

  if (step >= 8) {
    const data = getCalibrationData();
    const totalCorrect = responses.filter((r) => r.correct).length;
    const avgConfidence = Math.round(responses.reduce((s, r) => s + r.confidence, 0) / responses.length);
    const actualAccuracy = Math.round((totalCorrect / 8) * 100);
    const gap = avgConfidence - actualAccuracy;

    return (
      <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Your Calibration Report</h4>
        <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-8">How well did your confidence predict your accuracy?</p>

        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="text-center p-4 rounded-xl bg-violet-50 dark:bg-violet-900/20 border border-violet-200 dark:border-violet-800">
            <p className="text-2xl font-bold text-violet-700 dark:text-violet-300">{avgConfidence}%</p>
            <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">Avg Confidence</p>
          </div>
          <div className="text-center p-4 rounded-xl bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800">
            <p className="text-2xl font-bold text-emerald-700 dark:text-emerald-300">{actualAccuracy}%</p>
            <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">Actual Accuracy</p>
          </div>
          <div className={`text-center p-4 rounded-xl border ${gap > 10 ? 'bg-rose-50 dark:bg-rose-900/20 border-rose-200 dark:border-rose-800' : 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800'}`}>
            <p className={`text-2xl font-bold ${gap > 10 ? 'text-rose-700 dark:text-rose-300' : 'text-emerald-700 dark:text-emerald-300'}`}>{gap > 0 ? '+' : ''}{gap}%</p>
            <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">Calibration Gap</p>
          </div>
        </div>

        {/* Calibration chart */}
        <div className="space-y-3 mb-6">
          {data.filter((d) => d.count > 0).map((d) => (
            <div key={d.level} className="flex items-center gap-3">
              <span className="text-xs font-semibold text-zinc-500 w-20 text-right">{d.level}% conf.</span>
              <div className="flex-1 relative h-7 bg-zinc-100 dark:bg-zinc-700 rounded-full overflow-hidden">
                {/* Predicted bar */}
                <div className="absolute inset-y-0 left-0 bg-violet-200 dark:bg-violet-800/50 rounded-full" style={{ width: `${d.predicted}%` }} />
                {/* Actual bar */}
                <MotionDiv
                  initial={{ width: 0 }}
                  animate={{ width: `${d.actual ?? 0}%` }}
                  transition={{ duration: 0.8, delay: 0.2 }}
                  className={`absolute inset-y-0 left-0 rounded-full ${d.actual !== null && d.actual >= d.predicted - 10 ? 'bg-emerald-400 dark:bg-emerald-500' : 'bg-rose-400 dark:bg-rose-500'}`}
                />
                {/* Diagonal marker for predicted */}
                <div className="absolute inset-y-0 flex items-center" style={{ left: `${d.predicted}%` }}>
                  <div className="w-0.5 h-full bg-violet-600 dark:bg-violet-400" />
                </div>
              </div>
              <span className="text-xs font-bold w-16 text-zinc-600 dark:text-zinc-300">
                {d.actual !== null ? `${d.actual}% actual` : '—'}
              </span>
            </div>
          ))}
        </div>
        <div className="flex items-center justify-center gap-4 text-xs text-zinc-400 mb-6">
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-violet-200 dark:bg-violet-800/50 inline-block" /> Predicted</span>
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-emerald-400 dark:bg-emerald-500 inline-block" /> Actual (calibrated)</span>
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-rose-400 dark:bg-rose-500 inline-block" /> Actual (overconfident)</span>
        </div>

        <MotionDiv
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          className={`p-4 rounded-xl text-sm font-medium ${gap > 15 ? 'bg-rose-50 dark:bg-rose-950/30 text-rose-700 dark:text-rose-300 border border-rose-200 dark:border-rose-800' : gap > 5 ? 'bg-amber-50 dark:bg-amber-950/30 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800' : 'bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800'}`}
        >
          {gap > 15
            ? 'Significant overconfidence detected. This is normal — most people show this pattern. The gap between your confidence and your accuracy is your "metacognitive blind spot." The good news: awareness is the first step to calibration.'
            : gap > 5
            ? 'Mild overconfidence. You\'re slightly more confident than your accuracy warrants. With practice, you can close this gap and develop a sharper "learning radar."'
            : 'Well calibrated! Your confidence closely matches your accuracy. This is a strong metacognitive skill that will serve you well in exam preparation.'}
        </MotionDiv>

        <div className="mt-6 text-center">
          <button onClick={reset} className="px-5 py-2.5 bg-zinc-200 dark:bg-zinc-700 hover:bg-zinc-300 dark:hover:bg-zinc-600 text-zinc-700 dark:text-zinc-200 font-semibold rounded-xl transition-colors text-sm">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  const q = CALIBRATION_STATEMENTS[step];

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Calibration Quiz</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-1 mb-6">Rate your confidence, then answer. Let's see how well you know what you know.</p>

      <div className="text-center text-xs text-zinc-400 dark:text-zinc-500 mb-4">Question {step + 1} of 8</div>

      <div className="p-5 bg-zinc-50 dark:bg-zinc-900/50 rounded-xl border border-zinc-200 dark:border-zinc-700 mb-6">
        <p className="text-center font-semibold text-zinc-700 dark:text-zinc-200">"{q.statement}"</p>
      </div>

      {phase === 'confidence' ? (
        <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} key="conf">
          <p className="text-center text-sm font-medium text-zinc-600 dark:text-zinc-300 mb-4">How confident are you that you know the correct answer?</p>
          <div className="flex justify-center gap-3">
            {CONFIDENCE_LEVELS.map((level) => (
              <button
                key={level}
                onClick={() => handleConfidence(level)}
                className="px-4 py-2.5 rounded-xl border border-violet-200 dark:border-violet-800 bg-violet-50 dark:bg-violet-900/20 hover:bg-violet-100 dark:hover:bg-violet-900/40 text-violet-700 dark:text-violet-300 font-bold text-sm transition-colors"
              >
                {level}%
              </button>
            ))}
          </div>
        </MotionDiv>
      ) : (
        <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} key="ans">
          <p className="text-center text-sm font-medium text-zinc-600 dark:text-zinc-300 mb-4">Is this statement True or False?</p>
          <div className="flex justify-center gap-4">
            <button onClick={() => handleAnswer(true)} className="px-8 py-3 rounded-xl bg-emerald-100 dark:bg-emerald-900/30 hover:bg-emerald-200 dark:hover:bg-emerald-900/50 text-emerald-700 dark:text-emerald-300 font-bold text-sm border border-emerald-200 dark:border-emerald-800 transition-colors">True</button>
            <button onClick={() => handleAnswer(false)} className="px-8 py-3 rounded-xl bg-rose-100 dark:bg-rose-900/30 hover:bg-rose-200 dark:hover:bg-rose-900/50 text-rose-700 dark:text-rose-300 font-bold text-sm border border-rose-200 dark:border-rose-800 transition-colors">False</button>
          </div>
          <p className="text-center text-xs text-violet-400 mt-3">You rated: {currentConfidence}% confident</p>
        </MotionDiv>
      )}
    </div>
  );
};

// 2. DUNNING-KRUGER CURVE
const DunningKrugerCurve = () => {
  const [revealed, setRevealed] = useState(false);

  const W = 440, H = 240;
  const padL = 45, padR = 15, padT = 20, padB = 50;
  const chartW = W - padL - padR, chartH = H - padT - padB;
  const toX = (f: number) => padL + f * chartW;
  const toY = (f: number) => padT + (1 - f) * chartH;

  // The classic DK curve: confidence vs competence
  // Overconfidence peak → valley of despair → slope of enlightenment → plateau
  const dkPoints = [
    { x: 0, y: 0.15 },
    { x: 0.08, y: 0.55 },
    { x: 0.15, y: 0.92 }, // Mount Stupid
    { x: 0.25, y: 0.72 },
    { x: 0.38, y: 0.25 }, // Valley of Despair
    { x: 0.55, y: 0.40 },
    { x: 0.70, y: 0.58 }, // Slope of Enlightenment
    { x: 0.85, y: 0.72 },
    { x: 1.0, y: 0.78 },  // Plateau of Sustainability
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

  const labels = [
    { text: 'Peak of\nOverconfidence', x: 0.15, y: 0.92, anchor: 'middle' as const },
    { text: 'Valley of\nDespair', x: 0.38, y: 0.25, anchor: 'middle' as const },
    { text: 'Slope of\nEnlightenment', x: 0.70, y: 0.58, anchor: 'middle' as const },
    { text: 'Plateau of\nSustainability', x: 0.92, y: 0.78, anchor: 'middle' as const },
  ];

  return (
    <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Dunning-Kruger Effect</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Confidence vs. actual competence — the classic curve from Kruger & Dunning (1999).</p>

      {!revealed ? (
        <div className="text-center">
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">Where do you think your confidence sits relative to your actual knowledge?</p>
          <button onClick={() => setRevealed(true)} className="px-5 py-2.5 text-sm font-bold rounded-lg bg-violet-500 text-white hover:bg-violet-600 transition-colors">
            Reveal the Curve
          </button>
        </div>
      ) : (
        <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
          <div className="rounded-lg border border-violet-200 dark:border-violet-900 bg-violet-50/50 dark:bg-violet-950/20 p-3">
            <svg viewBox={`0 0 ${W} ${H}`} className="w-full">
              <defs>
                <linearGradient id="dk-grad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#8b5cf6" stopOpacity="0.4" />
                  <stop offset="100%" stopColor="#8b5cf6" stopOpacity="0.03" />
                </linearGradient>
              </defs>
              {/* Grid lines */}
              {[0.25, 0.5, 0.75, 1.0].map((v) => (
                <line key={v} x1={padL} x2={W - padR} y1={toY(v)} y2={toY(v)} stroke="#a1a1aa" strokeOpacity="0.15" strokeDasharray="3 3" />
              ))}
              <line x1={padL} x2={W - padR} y1={toY(0)} y2={toY(0)} stroke="#a1a1aa" strokeOpacity="0.3" />

              {/* Perfect calibration diagonal */}
              <line x1={toX(0)} y1={toY(0)} x2={toX(1)} y2={toY(1)} stroke="#a1a1aa" strokeWidth="1" strokeDasharray="6 4" strokeOpacity="0.4" />
              <text x={toX(0.85)} y={toY(0.88)} fontSize="8" fill="#a1a1aa" textAnchor="middle">Perfect calibration</text>

              {/* DK curve area */}
              <motion.path d={buildArea(dkPoints)} fill="url(#dk-grad)" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.8 }} />

              {/* DK curve line */}
              <motion.path d={buildCurve(dkPoints)} fill="none" stroke="#8b5cf6" strokeWidth="2.5" strokeLinecap="round" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1.5, ease: 'easeOut' }} />

              {/* Key point dots */}
              {dkPoints.filter((_, i) => [2, 4, 6, 8].includes(i)).map((p, i) => (
                <motion.circle key={i} cx={toX(p.x)} cy={toY(p.y)} r="4" fill="#8b5cf6" initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.5 + i * 0.3 }} />
              ))}

              {/* Labels */}
              {labels.map((l, i) => (
                <motion.g key={i} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.8 + i * 0.3 }}>
                  {l.text.split('\n').map((line, j) => (
                    <text key={j} x={toX(l.x)} y={toY(l.y) + (j === 0 ? -16 : -6)} fontSize="8" fill="#7c3aed" textAnchor={l.anchor} fontWeight="700">{line}</text>
                  ))}
                </motion.g>
              ))}

              {/* Axis labels */}
              <text x={padL + 2} y={toY(1.0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">High</text>
              <text x={padL + 2} y={toY(0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">Low</text>
              <text x={W / 2} y={H - 4} fontSize="9" fill="#a1a1aa" textAnchor="middle" fontWeight="600">Actual Competence →</text>
              <text x={8} y={H / 2} fontSize="9" fill="#a1a1aa" textAnchor="middle" fontWeight="600" transform={`rotate(-90, 8, ${H / 2})`}>Confidence →</text>
            </svg>
          </div>

          <div className="grid md:grid-cols-2 gap-4 mt-4 text-sm">
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900">
              <span className="text-rose-500 text-lg mt-0.5">&#x2716;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-rose-600 dark:text-rose-400">The Peak</strong> is where most students sit after passive study. They feel confident because the material looks familiar — but they can't actually retrieve it under exam conditions.</p>
            </div>
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900">
              <span className="text-emerald-500 text-lg mt-0.5">&#x2714;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-emerald-600 dark:text-emerald-400">The Plateau</strong> is where experts land. They've tested themselves enough to know exactly what they know — and what they don't. Their confidence matches reality.</p>
            </div>
          </div>
        </MotionDiv>
      )}
    </div>
  );
};

// 3. JOL TIMING COMPARISON (Planning Paradox style)
const JOLTimingComparison = () => {
  const [revealed, setRevealed] = useState(false);

  const W = 440, H = 260;
  const padL = 8, padR = 8, padT = 28, padB = 44;
  const chartW = W - padL - padR, chartH = H - padT - padB;
  const toX = (f: number) => padL + f * chartW;
  const toY = (f: number) => padT + (1 - f) * chartH;

  const xLabels = ['Study', '+1hr', '+1 day', '+3 days', '+7 days', '+14 days'];

  // Immediate JOLs: confidence stays high, actual recall crashes
  const immConfidence = [0.90, 0.88, 0.85, 0.82, 0.78, 0.75];
  const immRecall = [0.88, 0.55, 0.35, 0.25, 0.18, 0.12];

  // Delayed JOLs: confidence is lower but tracks actual recall closely
  const delConfidence = [0.50, 0.48, 0.45, 0.42, 0.40, 0.38];
  const delRecall = [0.55, 0.48, 0.42, 0.38, 0.35, 0.32];

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

  const immPhases = [
    { label: 'Feels obvious', x1: 0, x2: 0.33, color: '#fca5a5' },
    { label: 'Still confident', x1: 0.33, x2: 0.66, color: '#f87171' },
    { label: 'Blind to decay', x1: 0.66, x2: 1, color: '#ef4444' },
  ];
  const delPhases = [
    { label: 'Honest check', x1: 0, x2: 0.33, color: '#6ee7b7' },
    { label: 'Tracks reality', x1: 0.33, x2: 0.66, color: '#34d399' },
    { label: 'Calibrated', x1: 0.66, x2: 1, color: '#10b981' },
  ];

  const Chart = ({ confidence, recall, phases, areaColor, areaId, label }: {
    confidence: number[]; recall: number[]; phases: { label: string; x1: number; x2: number; color: string }[];
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

      {/* Confidence area */}
      <motion.path d={buildArea(confidence)} fill={`url(#${areaId})`} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.8 }} />
      {/* Confidence line (solid) */}
      <motion.path d={buildLine(confidence)} fill="none" stroke={areaColor} strokeWidth="2.5" strokeLinecap="round" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1.2, ease: 'easeOut' }} />
      {/* Recall line (dashed) */}
      <motion.path d={buildLine(recall)} fill="none" stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="5 3" strokeLinecap="round" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1.2, ease: 'easeOut', delay: 0.3 }} />
      {/* Confidence dots */}
      {confidence.map((v, i) => (
        <motion.circle key={i} cx={toX(i / (confidence.length - 1))} cy={toY(v)} r="3.5" fill={areaColor} initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2 * i + 0.3 }} />
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
      <line x1={W - padR - 100} x2={W - padR - 84} y1={14} y2={14} stroke={areaColor} strokeWidth="2" />
      <text x={W - padR - 80} y={17} fontSize="8" fill="#a1a1aa">Confidence</text>
      <line x1={W - padR - 44} x2={W - padR - 28} y1={14} y2={14} stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="4 2" />
      <text x={W - padR - 24} y={17} fontSize="8" fill="#a1a1aa">Recall</text>
    </svg>
  );

  return (
    <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The JOL Timing Effect</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">When you judge your learning changes everything. Nelson & Dunlosky (1991).</p>

      {!revealed ? (
        <div className="text-center">
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">Right after studying, everything feels familiar. But what happens when you check your confidence 24 hours later?</p>
          <button onClick={() => setRevealed(true)} className="px-5 py-2.5 text-sm font-bold rounded-lg bg-violet-500 text-white hover:bg-violet-600 transition-colors">
            Reveal the Timing Effect
          </button>
        </div>
      ) : (
        <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
          <div className="grid md:grid-cols-2 gap-4 mb-5">
            <div className="rounded-lg border border-rose-200 dark:border-rose-900 bg-rose-50/50 dark:bg-rose-950/20 p-3">
              <Chart confidence={immConfidence} recall={immRecall} phases={immPhases} areaColor="#ef4444" areaId="imm-grad" label="Immediate JOL" />
            </div>
            <div className="rounded-lg border border-emerald-200 dark:border-emerald-900 bg-emerald-50/50 dark:bg-emerald-950/20 p-3">
              <Chart confidence={delConfidence} recall={delRecall} phases={delPhases} areaColor="#10b981" areaId="del-grad" label="Delayed JOL (24hrs)" />
            </div>
          </div>
          <div className="grid md:grid-cols-2 gap-4 text-sm">
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900">
              <span className="text-rose-500 text-lg mt-0.5">&#x2716;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-rose-600 dark:text-rose-400">Immediate judgements</strong> are based on short-term memory. The material is still "in the room." Your confidence stays high while your actual retention collapses — creating a dangerous blind spot.</p>
            </div>
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900">
              <span className="text-emerald-500 text-lg mt-0.5">&#x2714;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-emerald-600 dark:text-emerald-400">Delayed judgements</strong> force actual retrieval from long-term memory. Your confidence drops — but it accurately reflects what you'll remember. The discomfort IS the accuracy.</p>
            </div>
          </div>
        </MotionDiv>
      )}
    </div>
  );
};

// 4. TRAFFIC LIGHT AUDIT
const AUDIT_TOPICS = [
  {
    topic: 'Active Recall',
    question: 'What makes active recall more effective than re-reading?',
    options: ['It is faster to do', 'It creates desirable difficulty that strengthens retrieval pathways', 'It is less tiring on the brain', 'It covers more material per session'],
    correct: 1,
  },
  {
    topic: 'The Spacing Effect',
    question: 'Why does spacing out study sessions improve memory?',
    options: ['Your brain gets bored with the same topic', 'It gives you time to find more resources', 'Forgetting between sessions forces retrieval effort that strengthens memory', 'It reduces total study time needed'],
    correct: 2,
  },
  {
    topic: 'Interleaving',
    question: 'What is the main benefit of interleaving different topics?',
    options: ['It keeps you entertained', 'It trains your brain to discriminate between problem types', 'It covers the syllabus faster', 'It is easier than blocked practice'],
    correct: 1,
  },
  {
    topic: 'Growth Mindset',
    question: 'According to Carol Dweck, what is a growth mindset?',
    options: ['Believing you will naturally get smarter as you age', 'Setting bigger goals each year', 'Believing abilities can be developed through effort and strategy', 'Thinking positively about exams'],
    correct: 2,
  },
  {
    topic: 'Desirable Difficulties',
    question: 'Why are desirable difficulties beneficial for learning?',
    options: ['They build character and resilience', 'They make studying more enjoyable', 'Conditions that feel harder during study lead to stronger long-term retention', 'They help you study faster'],
    correct: 2,
  },
  {
    topic: 'The Forgetting Curve',
    question: 'According to Ebbinghaus, what happens to newly learned information without review?',
    options: ['It is stored permanently but becomes harder to access', 'You lose the majority within 24 hours through exponential decay', 'It stays stable for about a week then drops', 'It disappears completely after exactly 30 days'],
    correct: 1,
  },
];

type Rating = 'green' | 'amber' | 'red';

const TrafficLightAudit = () => {
  const [phase, setPhase] = useState<'rate' | 'quiz' | 'results'>('rate');
  const [ratings, setRatings] = useState<Record<number, Rating>>({});
  const [quizStep, setQuizStep] = useState(0);
  const [answers, setAnswers] = useState<Record<number, number>>({});

  const handleRate = (idx: number, rating: Rating) => {
    setRatings((prev) => ({ ...prev, [idx]: rating }));
  };

  const startQuiz = () => setPhase('quiz');

  const handleQuizAnswer = (optionIdx: number) => {
    setAnswers((prev) => ({ ...prev, [quizStep]: optionIdx }));
    if (quizStep < AUDIT_TOPICS.length - 1) {
      setQuizStep((s) => s + 1);
    } else {
      setPhase('results');
    }
  };

  const reset = () => {
    setPhase('rate');
    setRatings({});
    setQuizStep(0);
    setAnswers({});
  };

  const ratingColors = {
    green: { bg: 'bg-emerald-100 dark:bg-emerald-900/30', border: 'border-emerald-400', text: 'text-emerald-700 dark:text-emerald-300', label: 'Green' },
    amber: { bg: 'bg-amber-100 dark:bg-amber-900/30', border: 'border-amber-400', text: 'text-amber-700 dark:text-amber-300', label: 'Amber' },
    red: { bg: 'bg-rose-100 dark:bg-rose-900/30', border: 'border-rose-400', text: 'text-rose-700 dark:text-rose-300', label: 'Red' },
  };

  if (phase === 'rate') {
    const allRated = Object.keys(ratings).length === AUDIT_TOPICS.length;
    return (
      <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Traffic Light Audit</h4>
        <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-8">Rate your knowledge of each concept honestly. Then we'll test you.</p>
        <div className="space-y-3">
          {AUDIT_TOPICS.map((t, i) => (
            <div key={i} className="flex items-center justify-between p-4 bg-zinc-50 dark:bg-zinc-900/50 rounded-xl border border-zinc-200 dark:border-zinc-700">
              <span className="font-semibold text-sm text-zinc-700 dark:text-zinc-200">{t.topic}</span>
              <div className="flex gap-2">
                {(['green', 'amber', 'red'] as Rating[]).map((r) => (
                  <button
                    key={r}
                    onClick={() => handleRate(i, r)}
                    className={`w-8 h-8 rounded-full border-2 transition-all ${ratings[i] === r ? `${ratingColors[r].border} ${ratingColors[r].bg} scale-110` : 'border-zinc-300 dark:border-zinc-600 opacity-40 hover:opacity-70'}`}
                    style={{ backgroundColor: ratings[i] === r ? undefined : r === 'green' ? '#d1fae5' : r === 'amber' ? '#fef3c7' : '#ffe4e6' }}
                  />
                ))}
              </div>
            </div>
          ))}
        </div>
        {allRated && (
          <MotionDiv initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="mt-6 text-center">
            <button onClick={startQuiz} className="px-6 py-3 bg-violet-500 hover:bg-violet-600 text-white font-bold rounded-xl transition-colors text-sm">
              Now Test Me
            </button>
          </MotionDiv>
        )}
      </div>
    );
  }

  if (phase === 'quiz') {
    const t = AUDIT_TOPICS[quizStep];
    const r = ratings[quizStep];
    return (
      <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Traffic Light Audit</h4>
        <div className="flex items-center justify-center gap-2 mt-2 mb-6">
          <span className="text-xs text-zinc-400">Question {quizStep + 1} of {AUDIT_TOPICS.length}</span>
          <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${ratingColors[r].bg} ${ratingColors[r].text}`}>You rated: {ratingColors[r].label}</span>
        </div>
        <p className="text-center font-semibold text-zinc-700 dark:text-zinc-200 mb-6">{t.question}</p>
        <div className="space-y-2 max-w-lg mx-auto">
          {t.options.map((opt, i) => (
            <button
              key={i}
              onClick={() => handleQuizAnswer(i)}
              className="w-full text-left p-3.5 rounded-xl border border-zinc-200 dark:border-zinc-700 hover:border-violet-400 dark:hover:border-violet-600 hover:bg-violet-50 dark:hover:bg-violet-900/20 text-sm text-zinc-700 dark:text-zinc-200 transition-colors"
            >
              {opt}
            </button>
          ))}
        </div>
      </div>
    );
  }

  // Results phase
  const results = { green: { total: 0, correct: 0 }, amber: { total: 0, correct: 0 }, red: { total: 0, correct: 0 } };
  AUDIT_TOPICS.forEach((t, i) => {
    const r = ratings[i];
    results[r].total++;
    if (answers[i] === t.correct) results[r].correct++;
  });

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Your Audit Results</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-8">How well did your traffic lights match reality?</p>

      <div className="grid grid-cols-3 gap-4 mb-6">
        {(['green', 'amber', 'red'] as Rating[]).map((r) => {
          const pct = results[r].total > 0 ? Math.round((results[r].correct / results[r].total) * 100) : null;
          const isCalibrated = r === 'green' ? (pct !== null && pct >= 80) : r === 'red' ? true : (pct !== null && pct >= 40 && pct <= 80);
          return (
            <div key={r} className={`text-center p-4 rounded-xl border ${ratingColors[r].bg} ${ratingColors[r].border}`}>
              <p className={`text-2xl font-bold ${ratingColors[r].text}`}>
                {results[r].total > 0 ? `${results[r].correct}/${results[r].total}` : '—'}
              </p>
              <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">{ratingColors[r].label} rated</p>
              {pct !== null && (
                <p className={`text-xs mt-1 font-semibold ${isCalibrated ? 'text-emerald-600' : 'text-rose-600'}`}>
                  {pct}% correct
                </p>
              )}
            </div>
          );
        })}
      </div>

      {results.green.total > 0 && results.green.correct < results.green.total && (
        <MotionDiv initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="p-4 rounded-xl bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-800 text-sm text-rose-700 dark:text-rose-300 font-medium mb-4">
          You rated {results.green.total - results.green.correct} topic(s) as Green but got them wrong. These are your metacognitive blind spots — topics where you feel confident but aren't actually prepared. This is exactly what catches students in exams.
        </MotionDiv>
      )}

      <div className="mt-4 text-center">
        <button onClick={reset} className="px-5 py-2.5 bg-zinc-200 dark:bg-zinc-700 hover:bg-zinc-300 dark:hover:bg-zinc-600 text-zinc-700 dark:text-zinc-200 font-semibold rounded-xl transition-colors text-sm">
          Try Again
        </button>
      </div>
    </div>
  );
};

// 5. PREDICTION TRACKER
const PREDICTION_QUESTIONS = [
  { question: 'What is the capital of Australia?', options: ['Sydney', 'Melbourne', 'Canberra', 'Perth'], correct: 2 },
  { question: 'Which element has the chemical symbol Fe?', options: ['Fluorine', 'Fermium', 'Iron', 'Francium'], correct: 2 },
  { question: 'How many chromosomes do humans have?', options: ['23', '46', '48', '64'], correct: 1 },
  { question: 'What year did World War I begin?', options: ['1912', '1914', '1916', '1918'], correct: 1 },
  { question: 'What is the SI unit of force?', options: ['Joule', 'Watt', 'Newton', 'Pascal'], correct: 2 },
];

const PredictionTracker = () => {
  const [step, setStep] = useState(0);
  const [phase, setPhase] = useState<'predict' | 'answer' | 'done'>('predict');
  const [predictions, setPredictions] = useState<boolean[]>([]);
  const [answers, setAnswers] = useState<number[]>([]);

  const handlePredict = (confident: boolean) => {
    setPredictions((prev) => [...prev, confident]);
    setPhase('answer');
  };

  const handleAnswer = (idx: number) => {
    setAnswers((prev) => [...prev, idx]);
    if (step < PREDICTION_QUESTIONS.length - 1) {
      setStep((s) => s + 1);
      setPhase('predict');
    } else {
      setPhase('done');
    }
  };

  const reset = () => {
    setStep(0);
    setPhase('predict');
    setPredictions([]);
    setAnswers([]);
  };

  if (phase === 'done') {
    const results = PREDICTION_QUESTIONS.map((q, i) => ({
      question: q.question,
      predicted: predictions[i],
      actual: answers[i] === q.correct,
    }));
    const correctPredictions = results.filter((r) => r.predicted === r.actual).length;
    const accuracy = Math.round((correctPredictions / results.length) * 100);
    const overconfident = results.filter((r) => r.predicted && !r.actual).length;
    const underconfident = results.filter((r) => !r.predicted && r.actual).length;

    return (
      <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Prediction Results</h4>
        <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-6">How accurately did you predict your own performance?</p>

        <div className="text-center mb-6">
          <p className="text-4xl font-bold text-violet-600 dark:text-violet-400">{accuracy}%</p>
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1">Prediction Accuracy</p>
        </div>

        <div className="space-y-2 mb-6">
          {results.map((r, i) => (
            <div key={i} className={`flex items-center justify-between p-3 rounded-lg text-sm ${r.predicted === r.actual ? 'bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-800' : 'bg-rose-50 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-800'}`}>
              <span className="text-zinc-700 dark:text-zinc-200 font-medium">{r.question}</span>
              <div className="flex items-center gap-2 shrink-0 ml-3">
                <span className={`text-xs font-bold ${r.actual ? 'text-emerald-600' : 'text-rose-600'}`}>{r.actual ? 'Correct' : 'Wrong'}</span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${r.predicted === r.actual ? 'bg-emerald-200 text-emerald-700' : 'bg-rose-200 text-rose-700'}`}>
                  {r.predicted === r.actual ? 'Predicted' : r.predicted ? 'Overconfident' : 'Underconfident'}
                </span>
              </div>
            </div>
          ))}
        </div>

        {overconfident > 0 && (
          <p className="text-sm text-rose-600 dark:text-rose-400 font-medium mb-2">
            You predicted correctly {overconfident} time(s) but were wrong — these are blind spots.
          </p>
        )}
        {underconfident > 0 && (
          <p className="text-sm text-amber-600 dark:text-amber-400 font-medium mb-2">
            You doubted yourself {underconfident} time(s) but were actually right — trust your knowledge more.
          </p>
        )}

        <div className="mt-4 text-center">
          <button onClick={reset} className="px-5 py-2.5 bg-zinc-200 dark:bg-zinc-700 hover:bg-zinc-300 dark:hover:bg-zinc-600 text-zinc-700 dark:text-zinc-200 font-semibold rounded-xl transition-colors text-sm">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  const q = PREDICTION_QUESTIONS[step];

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Prediction Tracker</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-1 mb-6">Predict first, then answer. Train your metacognitive accuracy.</p>
      <div className="text-center text-xs text-zinc-400 dark:text-zinc-500 mb-4">Question {step + 1} of {PREDICTION_QUESTIONS.length}</div>

      <div className="p-5 bg-zinc-50 dark:bg-zinc-900/50 rounded-xl border border-zinc-200 dark:border-zinc-700 mb-6">
        <p className="text-center font-semibold text-zinc-700 dark:text-zinc-200">{q.question}</p>
      </div>

      {phase === 'predict' ? (
        <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} key="pred">
          <p className="text-center text-sm font-medium text-zinc-600 dark:text-zinc-300 mb-4">Do you think you'll get this right?</p>
          <div className="flex justify-center gap-4">
            <button onClick={() => handlePredict(true)} className="px-8 py-3 rounded-xl bg-emerald-100 dark:bg-emerald-900/30 hover:bg-emerald-200 dark:hover:bg-emerald-900/50 text-emerald-700 dark:text-emerald-300 font-bold text-sm border border-emerald-200 dark:border-emerald-800 transition-colors">Yes, I know this</button>
            <button onClick={() => handlePredict(false)} className="px-8 py-3 rounded-xl bg-amber-100 dark:bg-amber-900/30 hover:bg-amber-200 dark:hover:bg-amber-900/50 text-amber-700 dark:text-amber-300 font-bold text-sm border border-amber-200 dark:border-amber-800 transition-colors">Not sure</button>
          </div>
        </MotionDiv>
      ) : (
        <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} key="ans">
          <div className="space-y-2 max-w-lg mx-auto">
            {q.options.map((opt, i) => (
              <button
                key={i}
                onClick={() => handleAnswer(i)}
                className="w-full text-left p-3.5 rounded-xl border border-zinc-200 dark:border-zinc-700 hover:border-violet-400 dark:hover:border-violet-600 hover:bg-violet-50 dark:hover:bg-violet-900/20 text-sm text-zinc-700 dark:text-zinc-200 transition-colors"
              >
                {opt}
              </button>
            ))}
          </div>
        </MotionDiv>
      )}
    </div>
  );
};


// --- MODULE COMPONENT ---
const TheLearningRadarModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'calibration-problem', title: 'The Calibration Problem', eyebrow: '01 // The Blind Spot', icon: Target },
    { id: 'dunning-kruger', title: 'The Dunning-Kruger Trap', eyebrow: '02 // The Double Curse', icon: AlertTriangle },
    { id: 'judgements-of-learning', title: 'Judgements of Learning', eyebrow: '03 // The Timing Effect', icon: Clock },
    { id: 'traffic-light-audit', title: 'The Traffic Light Audit', eyebrow: '04 // The Reality Check', icon: Layers },
    { id: 'monitoring-during-study', title: 'Monitoring During Study', eyebrow: '05 // The Signals', icon: Activity },
    { id: 'prediction-protocol', title: 'The Prediction Protocol', eyebrow: '06 // The Training Ground', icon: Flag },
  ];

  return (
    <ModuleLayout
      moduleNumber="44"
      moduleTitle="The Learning Radar"
      moduleSubtitle="The Metacognitive Calibration Guide"
      moduleDescription="Discover why most students can't accurately judge what they know — and learn the trainable skill that fixes it."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Calibration Problem." eyebrow="Step 1" icon={Target} theme={theme}>
              <p>Before you read another word, answer this: how confident are you that you could pass a test right now on whatever you studied most recently? Hold that number in your head. Now consider this: across over 100 studies analysed by <Highlight description="John Dunlosky (Kent State) and Amanda Lipko conducted a comprehensive meta-analysis of Judgement of Learning accuracy in 2007, finding that the average correlation between students' predicted and actual performance was shockingly low." theme={theme}>Dunlosky and Lipko (2007)</Highlight>, the correlation between students' predicted exam performance and their actual performance is just r = 0.27. That's barely better than chance.</p>
              <p>In a landmark study, <Highlight description="Nate Kornell (Williams College) and Robert Bjork (UCLA) found that students predicted they would recall approximately 70% of word pairs they'd studied, but actually recalled only 37%. The 33-percentage-point gap is the 'metacognitive blind spot.'" theme={theme}>Kornell and Bjork (2009)</Highlight> asked students to learn word pairs and then predict how many they'd recall on a test. Students predicted they'd remember about 70%. They actually remembered 37%. That 33-point gap isn't a small error — it's a systematic cognitive bias. It means when you sit down to study and think "I know this," there is a very high chance that you don't. This gap has a name: <Highlight description="The degree to which your subjective confidence in your knowledge differs from your objective ability to recall and apply that knowledge. Poor calibration means you can't tell what you know from what you merely recognise." theme={theme}>metacognitive miscalibration</Highlight>.</p>
              <p>This isn't about intelligence. The smartest students can have the worst calibration. It's a skill — and like any skill, it can be trained. This module will teach you how to build a <Highlight description="The ability to accurately monitor your own knowledge states in real-time — knowing what you know, what you don't know, and crucially, what you only think you know." theme={theme}>Learning Radar</Highlight>: the ability to accurately detect what you actually know versus what you merely recognise.</p>
              <CalibrationQuiz />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Dunning-Kruger Trap." eyebrow="Step 2" icon={AlertTriangle} theme={theme}>
              <p>In 1999, psychologists <Highlight description="Justin Kruger and David Dunning (Cornell University) published 'Unskilled and Unaware of It' — one of the most replicated findings in cognitive psychology. Their studies across humour, logic, and grammar showed that the least competent individuals dramatically overestimated their performance." theme={theme}>Justin Kruger and David Dunning</Highlight> published a paper that would become one of the most cited in all of psychology. They tested participants on humour, logical reasoning, and English grammar, then asked them to estimate how they'd ranked. The results were striking: participants in the bottom quartile (the lowest 25%) estimated they had performed in the 62nd percentile. Their actual rank? The 12th percentile. That's a 50-point overestimation.</p>
              <p>But here's the cruel twist — the <Highlight description="You need the very same skills to produce a correct answer as you do to recognise what a correct answer looks like. If you lack the skill, you lack the ability to know you lack the skill. You're not just wrong — you're confidently wrong." theme={theme}>Double Curse</Highlight>. The skills you need to produce a correct answer are the exact same skills you need to recognise what a correct answer looks like. If you don't know the chain rule in Maths, you also can't tell whether your attempt at the chain rule was correct. You're not just getting it wrong — you don't have the equipment to know you're getting it wrong.</p>
              <p>Conversely, top performers slightly underestimate their ability (they predicted 75th percentile; they were actually at the 87th). Expertise brings humility because you can see the full landscape of what there is to know. This is why the most prepared student in the room is often the most nervous, while the least prepared is mysteriously confident.</p>
              <DunningKrugerCurve />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Judgements of Learning." eyebrow="Step 3" icon={Clock} theme={theme}>
              <p>If our self-assessments are so unreliable, is there a way to make them more accurate? The answer is yes — and the key is <Highlight description="The time interval between studying material and judging whether you've learned it. Immediate JOLs (right after study) are highly inaccurate. Delayed JOLs (made hours or days later) are dramatically more accurate because they require actual retrieval from long-term memory." theme={theme}>timing</Highlight>. In a foundational study, <Highlight description="Thomas Nelson (University of Maryland) and John Dunlosky demonstrated that JOLs made immediately after study had a gamma correlation of just 0.0–0.2 with actual recall, while JOLs made 24 hours later showed a correlation of 0.8–0.9 — a massive improvement simply from changing when you make the judgement." theme={theme}>Nelson and Dunlosky (1991)</Highlight> discovered something remarkable about <Highlight description="Judgements of Learning — your self-rated prediction of how likely you are to remember a piece of information on a future test. They are the most studied form of metacognitive monitoring." theme={theme}>Judgements of Learning (JOLs)</Highlight>.</p>
              <p>When students judged their learning immediately after studying, the correlation with actual recall was nearly zero (gamma = 0.0 to 0.2). Essentially useless. But when students waited 24 hours before judging their learning, the correlation jumped to 0.8–0.9. Nearly perfect. Why? <Highlight description="Asher Koriat (University of Haifa) showed in 1997 that people base their JOLs on 'ease of processing' — how fluently information comes to mind. Immediately after study, everything feels fluent because it's still in short-term memory. After a delay, fluency accurately reflects long-term memory strength." theme={theme}>Koriat (1997)</Highlight> explained it: immediately after studying, everything is still in your short-term memory. It feels fluent and familiar. Your brain mistakes that familiarity for durable knowledge. After 24 hours, short-term memory has cleared. Judging your knowledge now requires actual retrieval from long-term memory — and that retrieval attempt gives you honest data.</p>
              <p>The practical rule is simple but powerful: never judge whether you've learned something in the same session you studied it. Come back tomorrow, close your notes, and ask yourself what you remember. That delayed self-check is worth more than hours of confident re-reading.</p>
              <JOLTimingComparison />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Traffic Light Audit." eyebrow="Step 4" icon={Layers} theme={theme}>
              <p>Knowing that delayed self-assessment is more accurate is useful, but you need a practical system to apply it. The <Highlight description="A structured self-assessment protocol where you rate every topic or subtopic as Green (I could explain this from memory), Amber (I recognise it but couldn't fully reproduce it), or Red (I don't know this). The critical step is then testing yourself to verify your ratings." theme={theme}>Traffic Light Audit</Highlight> is that system. It works in two phases: rate, then verify.</p>
              <p>Research by <Highlight description="Anique de Bruin and colleagues (Maastricht University) demonstrated in 2011 that students who self-tested after making confidence ratings dramatically improved their calibration accuracy. The act of testing exposes the gap between perceived and actual knowledge, which recalibrates future judgements." theme={theme}>de Bruin et al. (2011)</Highlight> showed that students who self-tested after rating their knowledge dramatically improved their calibration accuracy. The act of testing doesn't just measure your knowledge — it recalibrates your internal radar. You start to learn the difference between "I recognise this" (Amber) and "I could reproduce this under exam conditions" (Green).</p>
              <p>Here's how it works: take your subject syllabus and rate every topic Green, Amber, or Red. Green means "I could explain this to someone from memory." Amber means "I recognise it but couldn't fully reproduce it." Red means "I don't know this." Then — and this is the critical step — test yourself on your Greens. Most students discover that a significant number of their "Greens" are actually Ambers when put to the test. That discovery is uncomfortable, but it's the most valuable information you can have before an exam.</p>
              <TrafficLightAudit />
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Monitoring During Study." eyebrow="Step 5" icon={Activity} theme={theme}>
              <p>Calibration isn't just a one-time audit — it's a moment-to-moment skill you can deploy during every study session. <Highlight description="Robert Bjork, John Dunlosky, and Nate Kornell published a comprehensive review in 2013 showing that effective self-regulated learners continuously monitor their comprehension during study, using specific signals to detect whether genuine encoding is occurring." theme={theme}>Bjork, Dunlosky, and Kornell (2013)</Highlight> found that effective self-regulated learners continuously monitor their comprehension during study. They don't just read — they constantly check: "Am I actually learning this, or just looking at it?"</p>
              <p>There are concrete signals that distinguish real learning from the illusion of learning. <Highlight description="Thiede et al. (2003) demonstrated that generating keywords from memory after a delay significantly improved students' ability to monitor their own comprehension accuracy — a practical technique for enhancing metacognitive monitoring during study." theme={theme}>Thiede et al. (2003)</Highlight> found that one powerful signal is the ability to generate keywords from memory after a delay. If you've been studying a chapter and you can close the book and list the five key concepts, you're encoding. If you can't, you've been reading without learning.</p>
              <p>Here are the real-time monitoring signals to train yourself to notice. The <Highlight description="After studying a section, close your notes and try to write or say everything you remember. If you can recall the main points and their connections, encoding is happening. If you draw a blank, you were reading without processing." theme={theme}>"Close the Book" test</Highlight>: can you recall the main ideas without looking? <Highlight description="Can you create a novel example of the concept you just studied? If yes, you understand the principle, not just the specific case. This tests for transfer, which is the deepest form of learning." theme={theme}>Self-explanation</Highlight>: can you generate your own example? <Highlight description="Can you connect what you just studied to something you already know? If you can build a bridge to prior knowledge, the new information is being integrated into your existing schema, which makes it far more durable." theme={theme}>Connection-building</Highlight>: can you link this to something you already know? If you can do all three, you're genuinely learning. If you can't, you're in the fluency trap — and now you know to adjust.</p>
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="The Prediction Protocol." eyebrow="Step 6" icon={Flag} theme={theme}>
              <p>The ultimate metacognitive training tool is prediction. <Highlight description="Douglas Hacker and colleagues (University of Utah) tracked students across a semester who predicted their exam scores before each test. By the end of the semester, prediction accuracy had improved by approximately 50% — demonstrating that metacognitive calibration is trainable with repeated practice." theme={theme}>Hacker et al. (2000)</Highlight> tracked students across an entire semester who predicted their exam scores before each test and then compared predictions to reality. By the end of the semester, their prediction accuracy had improved by approximately 50%. The simple act of predicting and receiving feedback trained their metacognitive radar.</p>
              <p><Highlight description="Timothy Miller and Lisa Geraci (Texas A&M University) demonstrated in 2011 that calibration training transfers across domains — students who practiced prediction accuracy in one subject showed improved metacognitive monitoring in unrelated subjects, suggesting it is a general cognitive skill." theme={theme}>Miller and Geraci (2011)</Highlight> showed something even more powerful: calibration training transfers across domains. Students who practiced prediction accuracy in one subject showed improved metacognitive monitoring in completely unrelated subjects. This means metacognition isn't topic-specific — it's a general cognitive skill. Train it once, and it improves everywhere.</p>
              <p>The protocol is simple: before every test, mock, or practice paper, predict your score for each section. Write it down. After the test, compare your predictions to your actual results. The gap between prediction and reality is your <Highlight description="A quantitative measure of your metacognitive accuracy. Track this number over time. As it shrinks, your ability to self-assess is improving — which means your study time becomes dramatically more efficient because you're always working on what you actually need to work on." theme={theme}>calibration gap</Highlight>. Track it over time. Watch it shrink. That shrinking gap is your Learning Radar getting sharper — and it means every hour you spend studying is now targeted at the right material, not wasted on topics you only think you need to review.</p>
              <PredictionTracker />
              <MicroCommitment theme={theme}>
                <p>Before your next study session, take 2 minutes to rate your top 5 exam topics as Green, Amber, or Red. Then test yourself on one of your "Greens" — close your notes and try to explain it from memory. If you stumble, congratulations: you've just found a blind spot that would have cost you marks. That's your Learning Radar in action.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};

export default TheLearningRadarModule;
