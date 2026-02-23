/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Target, AlertTriangle, Clock, Layers, Activity, Flag } from 'lucide-react';
import { ModuleProgress } from '../types';
import { violetTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
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
            ? 'You were quite a bit more confident than your accuracy shows. Don\'t worry — most people are. The gap between what you thought you knew and what you actually got right is your blind spot. The good news? Now that you can see it, you can start fixing it.'
            : gap > 5
            ? 'You were a little more confident than your results suggest. That\'s pretty normal. With practice, you can close this gap and get much better at knowing what you actually know.'
            : 'Nice one! Your confidence closely matches your accuracy. That\'s a really valuable skill — it means you can trust your gut when deciding what to study and what to skip.'}
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
  // Overconfidence peak → valley of doubt → steady improvement → realistic confidence
  const dkPoints = [
    { x: 0, y: 0.15 },
    { x: 0.08, y: 0.55 },
    { x: 0.15, y: 0.92 }, // Peak of Overconfidence
    { x: 0.25, y: 0.72 },
    { x: 0.38, y: 0.25 }, // Valley of Doubt
    { x: 0.55, y: 0.40 },
    { x: 0.70, y: 0.58 }, // Steady Improvement
    { x: 0.85, y: 0.72 },
    { x: 1.0, y: 0.78 },  // Realistic Confidence
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
    { text: 'Valley of\nDoubt', x: 0.38, y: 0.25, anchor: 'middle' as const },
    { text: 'Steady\nImprovement', x: 0.70, y: 0.58, anchor: 'middle' as const },
    { text: 'Realistic\nConfidence', x: 0.92, y: 0.78, anchor: 'middle' as const },
  ];

  return (
    <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Confidence vs. Reality Curve</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">How confidence and actual ability don't always match up.</p>

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
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-rose-600 dark:text-rose-400">The Peak</strong> is where most students sit after just reading their notes. They feel confident because the material looks familiar — but they can't actually pull it out of their heads under exam conditions.</p>
            </div>
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900">
              <span className="text-emerald-500 text-lg mt-0.5">&#x2714;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-emerald-600 dark:text-emerald-400">Realistic Confidence</strong> is where well-prepared students land. They've tested themselves enough to know exactly what they know — and what they don't. Their confidence matches reality.</p>
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
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Timing Effect</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">When you check your learning changes everything.</p>

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
              <Chart confidence={immConfidence} recall={immRecall} phases={immPhases} areaColor="#ef4444" areaId="imm-grad" label="Checking Straight Away" />
            </div>
            <div className="rounded-lg border border-emerald-200 dark:border-emerald-900 bg-emerald-50/50 dark:bg-emerald-950/20 p-3">
              <Chart confidence={delConfidence} recall={delRecall} phases={delPhases} areaColor="#10b981" areaId="del-grad" label="Checking After 24 Hours" />
            </div>
          </div>
          <div className="grid md:grid-cols-2 gap-4 text-sm">
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900">
              <span className="text-rose-500 text-lg mt-0.5">&#x2716;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-rose-600 dark:text-rose-400">Checking straight away</strong> tricks you because everything is still fresh. The material is still "in the room." Your confidence stays high while your actual memory of it collapses — creating a dangerous blind spot.</p>
            </div>
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900">
              <span className="text-emerald-500 text-lg mt-0.5">&#x2714;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-emerald-600 dark:text-emerald-400">Checking after a delay</strong> forces your brain to actually pull the information from memory. Your confidence drops — but it honestly reflects what you'll remember in the exam. The discomfort IS the honesty.</p>
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
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-1 mb-6">Predict first, then answer. See how well you really know what you know.</p>
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
    { id: 'calibration-problem', title: 'You Don\'t Know What You Don\'t Know', eyebrow: '01 // The Blind Spot', icon: Target },
    { id: 'dunning-kruger', title: 'Why the Least Prepared Feel Most Confident', eyebrow: '02 // The Confidence Trap', icon: AlertTriangle },
    { id: 'judgements-of-learning', title: 'When to Check If You\'ve Learned Something', eyebrow: '03 // The Timing Trick', icon: Clock },
    { id: 'traffic-light-audit', title: 'The Traffic Light Audit', eyebrow: '04 // The Reality Check', icon: Layers },
    { id: 'monitoring-during-study', title: 'Checking Yourself During Study', eyebrow: '05 // The Signals', icon: Activity },
    { id: 'prediction-protocol', title: 'The Prediction Game', eyebrow: '06 // The Training Ground', icon: Flag },
  ];

  return (
    <ModuleLayout
      moduleNumber="44"
      moduleTitle="The Learning Radar"
      moduleSubtitle="Know What You Actually Know"
      moduleDescription="Most students think they know more than they do — and it costs them marks. This module shows you how to spot your blind spots and study smarter."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Scan Your Blind Spots"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="You Don't Know What You Don't Know." eyebrow="Step 1" icon={Target} theme={theme}>
              <p>Before you read another word, answer this: how confident are you that you could pass a test right now on whatever you studied most recently? Hold that number in your head. Now consider this: across over 100 studies, <Highlight description="Researchers looked at how well students predict their own exam results. Turns out, most students are terrible at it — their guesses were barely better than flipping a coin." theme={theme}>researchers found</Highlight> that the link between how well students think they'll do and how they actually do is shockingly weak. Barely better than chance.</p>
              <p>In one well-known study, <Highlight description="Students were asked to learn word pairs and predict how many they'd remember. They guessed about 70%. They actually remembered 37%. That massive gap is your brain fooling you into thinking you know more than you do." theme={theme}>researchers</Highlight> asked students to learn word pairs and then predict how many they'd recall on a test. Students predicted they'd remember about 70%. They actually remembered 37%. That 33-point gap isn't a small error — it's your brain consistently fooling you. It means when you sit down to study and think "I know this," there's a very high chance that you don't. This gap is basically a <Highlight description="When your confidence in what you know doesn't match what you can actually do. You feel like you've got it, but when it comes to the exam, you can't pull it out of your head. You can't tell the difference between 'I recognise this' and 'I actually know this.'" theme={theme}>confidence blind spot</Highlight>.</p>
              <p>This isn't about intelligence. The smartest students can have the worst blind spots. It's a skill — and like any skill, it can be trained. This module will teach you how to build a <Highlight description="Being able to honestly tell the difference between what you actually know and what you just think you know. It's like having a built-in detector that tells you where your real gaps are." theme={theme}>Learning Radar</Highlight>: the ability to spot the difference between what you actually know and what just looks familiar.</p>
              <CalibrationQuiz />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Why the Least Prepared Feel Most Confident." eyebrow="Step 2" icon={AlertTriangle} theme={theme}>
              <p>In 1999, two psychologists ran <Highlight description="They tested people on things like logic and grammar, then asked them to guess how well they did. The people who scored the worst massively overestimated their results. They thought they were above average when they were actually near the bottom." theme={theme}>a now-famous experiment</Highlight>. They tested people on things like logic and grammar, then asked everyone to guess how well they'd done compared to others. The results were wild: the people who scored in the bottom 25% thought they'd finished in the top half. Their actual rank? Near the bottom. That's a 50-point gap between how good they thought they were and how good they actually were.</p>
              <p>But here's the really unfair part — the <Highlight description="To know whether your answer is right, you need the same skills you'd need to get it right in the first place. If you don't understand the topic, you also can't tell that you don't understand it. You're not just wrong — you're confidently wrong, and you have no idea." theme={theme}>Confidence Trap</Highlight>. The skills you need to get a question right are the exact same skills you need to recognise whether your answer is right. If you don't understand the chain rule in Maths, you also can't tell whether your attempt at it was any good. You're not just getting it wrong — you don't have the tools to know you're getting it wrong.</p>
              <p>Meanwhile, top performers tend to slightly underestimate how well they've done. When you really know a subject, you can see how much more there is to learn, so you stay humble. This is why the most prepared student in the room is often the most nervous, while the least prepared is mysteriously confident.</p>
              <DunningKrugerCurve />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="When to Check If You've Learned Something." eyebrow="Step 3" icon={Clock} theme={theme}>
              <p>If we're so bad at judging what we know, is there a way to get better at it? Yes — and the secret is <Highlight description="The gap between when you study something and when you check whether it stuck. If you check straight away, your brain tricks you into thinking you know it. If you wait a day and then check, you get a much more honest answer." theme={theme}>timing</Highlight>. <Highlight description="Researchers found that when students guessed how well they'd learned something right after studying, their guesses were basically useless. But when they waited 24 hours and then guessed, they were almost perfectly accurate. Just by changing when you check yourself, you go from clueless to spot-on." theme={theme}>Researchers discovered</Highlight> something powerful about how we <Highlight description="Your personal prediction of whether you'll remember something on a test. Basically: 'Do I actually know this or not?' Getting good at these predictions is one of the most useful study skills you can build." theme={theme}>judge our own learning</Highlight>.</p>
              <p>When students checked how well they'd learned something straight after studying, their self-assessment was basically worthless. But when they waited 24 hours and then checked, their accuracy jumped to nearly perfect. Why? Right after studying, everything is still fresh in your short-term memory. It all feels familiar. Your brain mistakes that familiarity for real knowledge. But after 24 hours, the short-term stuff has faded. Checking yourself now forces you to actually pull information from long-term memory — and that gives you honest feedback.</p>
              <p>The practical rule is simple: never judge whether you've learned something in the same session you studied it. Come back tomorrow, close your notes, and ask yourself what you remember. That delayed self-check is worth more than hours of confident re-reading.</p>
              <JOLTimingComparison />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Traffic Light Audit." eyebrow="Step 4" icon={Layers} theme={theme}>
              <p>Now you know that checking yourself after a delay is more accurate — but you need an actual system to do it. The <Highlight description="A simple system where you go through every topic on your syllabus and rate it Green (I could explain this from memory right now), Amber (I sort of know it but couldn't fully explain it), or Red (I'm lost on this). Then you test yourself on the Greens to see if you're being honest." theme={theme}>Traffic Light Audit</Highlight> is that system. It works in two steps: rate yourself, then test yourself.</p>
              <p><Highlight description="Studies showed that students who tested themselves after rating their own confidence became way better at knowing what they actually knew. Testing yourself doesn't just check your knowledge — it trains your brain to be more honest about what's really sticking." theme={theme}>Research shows</Highlight> that students who test themselves after rating their knowledge get dramatically better at judging what they actually know. Testing doesn't just measure your knowledge — it trains your brain to be more honest. You start to learn the difference between "I recognise this" (Amber) and "I could actually explain this in an exam" (Green).</p>
              <p>Here's how it works: take your subject syllabus and rate every topic Green, Amber, or Red. Green means "I could explain this to someone from memory." Amber means "I sort of know it but couldn't fully explain it." Red means "I don't know this." Then — and this is the key step — test yourself on your Greens. Most students discover that loads of their "Greens" are actually Ambers when put to the test. That's uncomfortable, but it's the most useful information you can have before an exam.</p>
              <TrafficLightAudit />
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Checking Yourself During Study." eyebrow="Step 5" icon={Activity} theme={theme}>
              <p>Your Learning Radar isn't just something you use once — it's a habit you can build into every single study session. <Highlight description="Research shows that the best students don't just read their notes — they're constantly checking in with themselves: 'Am I actually taking this in, or am I just staring at the page?' That habit is what separates real studying from wasted time." theme={theme}>Research shows</Highlight> that the best learners constantly check their own understanding while studying. They don't just read — they keep asking themselves: "Am I actually learning this, or just looking at it?"</p>
              <p>There are clear signals that tell you whether you're actually learning or just going through the motions. <Highlight description="If you can close your book and list the key ideas from what you just studied, the information is actually going in. If you can't, you've basically been staring at the page without absorbing anything. It's a quick and honest test." theme={theme}>One powerful trick</Highlight>: after studying a section, try to list the key ideas from memory. If you've been studying a chapter and you can close the book and name the five main points, you're on track. If you can't, you've been reading without learning.</p>
              <p>Here are three quick checks you can use during any study session. The <Highlight description="Close your notes and try to say or write down everything you just studied. If you can hit the main points, it's working. If your mind goes blank, you were reading on autopilot and need to change your approach." theme={theme}>"Close the Book" test</Highlight>: can you recall the main ideas without looking? The <Highlight description="Try to come up with your own example of what you just learned. If you can, it means you actually understand the idea, not just the specific case you read about. That's the difference between surface learning and deep learning." theme={theme}>"Make Your Own Example" test</Highlight>: can you come up with a new example? The <Highlight description="Try to connect what you just learned to something you already know. If you can make that link, the new information is sticking to what's already in your brain, which makes it way harder to forget." theme={theme}>"Connect the Dots" test</Highlight>: can you link this to something you already know? If you can do all three, you're genuinely learning. If you can't, you're in the familiarity trap — and now you know to switch up your approach.</p>
              <PersonalStory name="Ciara" role="5th Year, Cork">
                I used to spend hours reading my Biology notes and feel grand about it. Then I tried the "Close the Book" test and I literally couldn't remember a single thing I'd just read. It was a shock. Now I stop every 20 minutes and try to write down the main points without looking. It's way harder but I actually remember stuff for tests now.
              </PersonalStory>
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="The Prediction Game." eyebrow="Step 6" icon={Flag} theme={theme}>
              <p>The best way to train your Learning Radar? Start predicting. <Highlight description="Researchers tracked students who predicted their exam scores before each test throughout a whole school year. By the end, their predictions were about 50% more accurate. Just by guessing your score and then seeing how close you were, your brain gets better and better at knowing what it actually knows." theme={theme}>Researchers</Highlight> tracked students who predicted their exam scores before each test and then compared their predictions to reality. By the end of the year, their prediction accuracy had improved by about 50%. The simple act of guessing your score and seeing how close you were trained their brain to be more honest with itself.</p>
              <p>Even better: <Highlight description="Students who practised predicting their scores in one subject actually got better at knowing what they knew in completely different subjects. This isn't a subject-specific trick — it's a general brain skill. Train it in Maths and it helps you in History too." theme={theme}>this skill transfers across subjects</Highlight>. Students who practised predicting in one subject showed better self-awareness in completely unrelated subjects. This isn't a trick that only works for one topic — it's a general skill. Train it in Maths and it helps you in History too.</p>
              <p>Here's the game: before every test, mock exam, or practice paper, predict your score for each section. Write it down. After the test, compare your predictions to your actual results. The gap between what you predicted and what you got is your <Highlight description="The difference between what you predicted you'd score and what you actually scored. Track this number over time. As it gets smaller, you're getting better at knowing what you know — which means you spend your study time on the stuff that actually needs work instead of wasting it." theme={theme}>prediction gap</Highlight>. Track it over time. Watch it shrink. That shrinking gap means your Learning Radar is getting sharper — and it means every hour you spend studying is targeted at the right material, not wasted on topics you only think you need to review.</p>
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
