
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Scaling, Brain, SlidersHorizontal, Thermometer, Puzzle, BarChartHorizontal
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { tealTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = tealTheme;

// --- INTERACTIVE COMPONENTS ---
const CognitiveLoadBalancer = () => {
    const [loads, setLoads] = useState({ intrinsic: 30, extraneous: 15, germane: 20 });
    const total = loads.intrinsic + loads.extraneous + loads.germane;
    const overload = total > 100;
    const germaneRoom = Math.max(0, 100 - loads.intrinsic - loads.extraneous);
    const healthy = total <= 85;

    const loadTypes: { key: 'intrinsic' | 'extraneous' | 'germane'; label: string; plain: string; example: string; direction: string; color: string; barColor: string; fixed?: boolean }[] = [
      { key: 'intrinsic', label: 'Intrinsic Load', plain: 'The difficulty of the topic itself', example: 'e.g., Probability is harder than basic addition', direction: 'Fixed — you can\'t change this, only manage around it', color: '#1a1a1a', barColor: '#e0dbd4', fixed: true },
      { key: 'extraneous', label: 'Extraneous Load', plain: 'Waste from distractions & confusion', example: 'e.g., Phone buzzing, noisy room, unclear instructions', direction: 'Minimize this — it steals space from learning', color: '#E85D75', barColor: '#E85D75' },
      { key: 'germane', label: 'Germane Load', plain: 'The productive effort that builds memory', example: 'e.g., Active recall, self-explanation, practice questions', direction: 'Maximize this — it\'s the only load that causes learning', color: '#2A7D6F', barColor: '#2A7D6F' },
    ];

    return (
      <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
        {/* Section chip + title */}
        <div className="text-center mb-8">
          <span className="inline-block px-3 py-1 rounded-full text-[11px] font-bold tracking-wider uppercase mb-3" style={{ backgroundColor: '#e8f5f2', color: '#1a6358', border: '1px solid rgba(42,125,111,0.2)', letterSpacing: '0.06em' }}>Interactive Simulation</span>
          <h4 className="font-serif font-bold" style={{ fontSize: 24, color: '#1a1a1a' }}>Cognitive Load Balancer</h4>
          <p className="text-sm mt-1" style={{ color: '#7a7068' }}>Your Working Memory is a small container. Three types of load compete for space inside it.</p>
        </div>

        {/* Stacked bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <span style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', color: '#9e9186', textTransform: 'uppercase' as const }}>Working Memory Capacity</span>
            <span className="font-semibold" style={{ fontSize: 13, color: overload ? '#E85D75' : '#2A7D6F' }}>{total}% / 100%</span>
          </div>
          <div className="bg-white dark:bg-zinc-900" style={{ border: '2px solid #1a1a1a', borderRadius: 12, overflow: 'hidden', height: 28 }}>
            <div className="flex h-full">
              <motion.div style={{ backgroundColor: '#e0dbd4' }} animate={{ width: `${Math.min(loads.intrinsic, 100)}%` }} transition={{ duration: 0.3 }} />
              <motion.div style={{ backgroundColor: '#E85D75' }} animate={{ width: `${Math.min(loads.extraneous, 100 - loads.intrinsic > 0 ? loads.extraneous : 0)}%` }} transition={{ duration: 0.3 }} />
              <motion.div style={{ backgroundColor: '#2A7D6F' }} animate={{ width: `${Math.min(loads.germane, germaneRoom > 0 ? loads.germane : 0)}%` }} transition={{ duration: 0.3 }} />
            </div>
          </div>
          {/* Legend */}
          <div className="flex gap-5 mt-3 justify-center">
            <div className="flex items-center gap-1.5">
              <div className="w-2 h-2 rounded-full" style={{ backgroundColor: '#e0dbd4' }} />
              <span style={{ fontSize: 12, color: '#7a7068' }}>Intrinsic</span>
            </div>
            <div className="flex items-center gap-1.5">
              <div className="w-2 h-2 rounded-full" style={{ backgroundColor: '#E85D75' }} />
              <span style={{ fontSize: 12, color: '#7a7068' }}>Extraneous</span>
            </div>
            <div className="flex items-center gap-1.5">
              <div className="w-2 h-2 rounded-full" style={{ backgroundColor: '#2A7D6F' }} />
              <span style={{ fontSize: 12, color: '#7a7068' }}>Germane</span>
            </div>
          </div>
        </div>

        {/* Slider cards */}
        <div className="space-y-3 mb-6">
          {loadTypes.map(l => (
            <div key={l.key} className="bg-white dark:bg-zinc-900" style={{ border: `2px solid ${l.color}`, borderRadius: 14, padding: '20px 22px' }}>
              <div className="flex items-start justify-between mb-1">
                <div>
                  <div className="flex items-center gap-2">
                    <p className="font-serif font-semibold" style={{ fontSize: 16, color: l.color }}>{l.label}</p>
                    {l.fixed && (
                      <span style={{ backgroundColor: '#f0ece6', color: '#9e9186', border: '1px solid #d0cdc8', borderRadius: 20, padding: '2px 8px', fontSize: 10, fontWeight: 700 }}>FIXED</span>
                    )}
                  </div>
                  <p style={{ fontSize: 14, color: '#5a5550' }}>{l.plain}</p>
                </div>
                <span className="font-serif font-bold ml-3" style={{ fontSize: 20, color: l.color }}>{loads[l.key]}%</span>
              </div>
              <p className="italic mb-2" style={{ fontSize: 13, color: '#9e9186' }}>{l.example}</p>
              <input
                type="range" min="5" max="70"
                value={loads[l.key]}
                onChange={e => setLoads({ ...loads, [l.key]: parseInt(e.target.value) })}
                className="chunky-slider chunky-slider-teal"
                disabled={l.fixed}
                style={l.fixed ? { opacity: 0.5 } : undefined}
              />
              <p className="font-semibold mt-1" style={{ fontSize: 12, color: l.color }}>{l.direction}</p>
            </div>
          ))}
        </div>

        {/* Diagnosis callout */}
        <AnimatePresence mode="wait">
          {overload ? (
            <motion.div key="overload" initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} style={{ borderLeft: '3px solid #E85D75', backgroundColor: '#fde4e4', borderRadius: '0 10px 10px 0', padding: '12px 16px' }}>
              <p className="text-sm italic" style={{ color: '#b33030' }}>Working memory overloaded — learning becomes very difficult at this point.</p>
            </motion.div>
          ) : healthy ? (
            <motion.div key="healthy" initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} style={{ borderLeft: '3px solid #2A7D6F', backgroundColor: '#f0faf8', borderRadius: '0 10px 10px 0', padding: '12px 16px' }}>
              <p className="text-sm italic" style={{ color: '#1a6358' }}>Good balance — your working memory has space to form lasting memories.</p>
            </motion.div>
          ) : (
            <motion.div key="moderate" initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} style={{ borderLeft: '3px solid #d0cdc8', backgroundColor: '#f8f6f2', borderRadius: '0 10px 10px 0', padding: '12px 16px' }}>
              <p className="text-sm italic" style={{ color: '#7a7068' }}>Within capacity, but push Germane load higher or reduce Extraneous to optimise learning.</p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    );
}

const StairsEscalator = () => {
    const [choice, setChoice] = useState<'stairs' | 'escalator' | null>(null);
    return(
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Stairs vs. Escalator</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Which path leads to real learning?</p>
            <div className="grid grid-cols-2 gap-4">
                <button onClick={() => setChoice('escalator')} className="p-4 rounded-xl text-center font-medium transition-all" style={choice === 'escalator' ? { backgroundColor: '#FCA5A5', border: '2.5px solid #DC2626', borderRadius: 14, boxShadow: '3px 3px 0px 0px #DC2626', color: '#7F1D1D' } : { backgroundColor: '#FFFFFF', border: '2.5px solid #1C1917', borderRadius: 14, boxShadow: '3px 3px 0px 0px #1C1917' }}><strong>The Escalator:</strong> A perfectly clear lecture, re-reading your notes.</button>
                <button onClick={() => setChoice('stairs')} className="p-4 rounded-xl text-center font-medium transition-all" style={choice === 'stairs' ? { backgroundColor: '#6EE7B7', border: '2.5px solid #059669', borderRadius: 14, boxShadow: '3px 3px 0px 0px #059669', color: '#064E3B' } : { backgroundColor: '#FFFFFF', border: '2.5px solid #1C1917', borderRadius: 14, boxShadow: '3px 3px 0px 0px #1C1917' }}><strong>The Stairs:</strong> Struggling with a past paper, trying to explain a topic.</button>
            </div>
            {choice &&
            <motion.div initial={{opacity:0}} animate={{opacity:1}} className="mt-6 p-4 rounded-xl text-sm" style={choice === 'stairs' ? { backgroundColor: '#6EE7B7', border: '2.5px solid #059669', boxShadow: '3px 3px 0px 0px #059669', color: '#064E3B' } : { backgroundColor: '#FCA5A5', border: '2.5px solid #DC2626', boxShadow: '3px 3px 0px 0px #DC2626', color: '#7F1D1D' }}>
                {choice === 'escalator' && <p><strong>You chose the escalator.</strong> It feels smooth and effortless. You arrive at the top (the answer) quickly. But your muscles (your brain) did no work. The feeling of fluency is high, but long-term learning is low.</p>}
                {choice === 'stairs' && <p><strong>You chose the stairs.</strong> It's slow and feels hard. You might stumble (make mistakes). But this effort is what strengthens your cardiovascular system (your long-term memory). The feeling of learning is low, but the actual result is high.</p>}
            </motion.div>}
        </div>
    );
};

const IllusionOfCompetenceChart = () => {
    const [view, setView] = useState<'prediction' | 'reality'>('prediction');
    const ssssData = { prediction: 90, reality: 40 };
    const stttData = { prediction: 40, reality: 61 };

    const passiveH = view === 'prediction' ? ssssData.prediction : ssssData.reality;
    const activeH = view === 'prediction' ? stttData.prediction : stttData.reality;

    return (
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            {/* Section chip + title */}
            <div className="text-center mb-8">
                <span className="inline-block px-3 py-1 rounded-full text-[11px] font-bold tracking-wider uppercase mb-3" style={{ backgroundColor: '#e8f5f2', color: '#1a6358', border: '1px solid rgba(42,125,111,0.2)', letterSpacing: '0.06em' }}>Research Evidence</span>
                <h4 className="font-serif font-bold" style={{ fontSize: 24, color: '#1a1a1a' }}>The Great Deception</h4>
                <p className="text-sm mt-1" style={{ color: '#7a7068' }}>The gap between what <em>feels</em> effective and what <em>is</em> effective is massive.</p>
            </div>

            {/* Chart card */}
            <div className="bg-white dark:bg-zinc-900" style={{ border: '2px solid #1a1a1a', borderRadius: 16, padding: 24 }}>
                <div className="grid grid-cols-2 gap-8">
                    {/* Passive Re-reading column */}
                    <div className="text-center">
                        <h5 className="font-serif font-semibold mb-4" style={{ fontSize: 16, color: '#1a1a1a' }}>Passive Re-reading</h5>
                        <div className="relative flex items-end justify-center" style={{ height: 200 }}>
                            <motion.div
                                className="w-full relative"
                                style={{ backgroundColor: '#d0cdc8', borderRadius: '8px 8px 0 0', maxWidth: 80 }}
                                initial={{ height: 0 }}
                                animate={{ height: `${passiveH}%` }}
                                transition={{ type: 'spring', stiffness: 100 }}
                            >
                                <span className="absolute top-2 left-0 right-0 text-center font-serif font-bold" style={{ fontSize: 22, color: '#5a5550' }}>{passiveH}%</span>
                            </motion.div>
                        </div>
                        <div style={{ height: 1, backgroundColor: '#d0cdc8' }} />
                    </div>

                    {/* Active Self-Testing column */}
                    <div className="text-center">
                        <h5 className="font-serif font-semibold mb-4" style={{ fontSize: 16, color: '#1a1a1a' }}>Active Self-Testing</h5>
                        <div className="relative flex items-end justify-center" style={{ height: 200 }}>
                            <motion.div
                                className="w-full relative"
                                style={{ backgroundColor: '#2A7D6F', borderRadius: '8px 8px 0 0', maxWidth: 80 }}
                                initial={{ height: 0 }}
                                animate={{ height: `${activeH}%` }}
                                transition={{ type: 'spring', stiffness: 100 }}
                            >
                                <span className="absolute top-2 left-0 right-0 text-center font-serif font-bold" style={{ fontSize: 22, color: '#FFFFFF' }}>{activeH}%</span>
                            </motion.div>
                        </div>
                        <div style={{ height: 1, backgroundColor: '#d0cdc8' }} />
                    </div>
                </div>
            </div>

            {/* Toggle buttons */}
            <div className="flex justify-center gap-2 mt-5">
                <button
                    onClick={() => setView('prediction')}
                    style={{
                        padding: '10px 20px',
                        borderRadius: 20,
                        fontSize: 13,
                        fontWeight: 600,
                        backgroundColor: view === 'prediction' ? '#2A7D6F' : '#FFFFFF',
                        color: view === 'prediction' ? '#FFFFFF' : '#7a7068',
                        border: view === 'prediction' ? '2px solid #2A7D6F' : '2px solid #d0cdc8',
                        cursor: 'pointer',
                    }}
                >
                    What students predicted
                </button>
                <button
                    onClick={() => setView('reality')}
                    style={{
                        padding: '10px 20px',
                        borderRadius: 20,
                        fontSize: 13,
                        fontWeight: 600,
                        backgroundColor: view === 'reality' ? '#2A7D6F' : '#FFFFFF',
                        color: view === 'reality' ? '#FFFFFF' : '#7a7068',
                        border: view === 'reality' ? '2px solid #2A7D6F' : '2px solid #d0cdc8',
                        cursor: 'pointer',
                    }}
                >
                    Actual test results (1 week later)
                </button>
            </div>

            {/* Insight callout — only on reality view */}
            <AnimatePresence>
                {view === 'reality' && (
                    <motion.div
                        initial={{ opacity: 0, y: 6 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 6 }}
                        className="mt-4 max-w-lg mx-auto"
                        style={{ borderLeft: '3px solid #2A7D6F', backgroundColor: '#f0faf8', borderRadius: '0 10px 10px 0', padding: '12px 16px' }}
                    >
                        <p className="text-sm italic" style={{ color: '#1a6358' }}>Active self-testing produces 3× better retention — but most students never use it because it feels harder.</p>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

const ScenarioDiagnosis = () => {
  const scenarios = [
    {
      situation: 'Re-reading your History notes in a noisy kitchen while your family watches TV.',
      answer: 'extraneous',
      explanation: 'The task itself (re-reading) is too easy (Comfort Zone) AND the environment is full of distractions (high Extraneous Load). The primary fix is the environment — move somewhere quiet, then switch to active recall.',
    },
    {
      situation: 'Doing a past paper question from memory in a quiet room, on a topic you studied last week.',
      answer: 'optimal',
      explanation: 'This is Optimized Friction. The task is in your ZPD (hard but doable), the environment is clean (low Extraneous Load), and retrieval practice is a Desirable Difficulty. This is what effective study looks like.',
    },
    {
      situation: 'Watching a perfectly clear YouTube explainer on a topic you already understand well.',
      answer: 'zpd',
      explanation: 'The task is in the Comfort Zone — it feels productive because the explanation is fluent, but your brain is doing zero work. No struggle means no growth. You need to attempt harder problems on this topic.',
    },
    {
      situation: 'Attempting a university-level Maths proof with no guidance on a topic you haven\'t covered.',
      answer: 'zpd',
      explanation: 'This is the Frustration Zone. The task is so far beyond your current level that Working Memory overloads immediately. You need to step back to a worked example or ask for help to bring it into your ZPD.',
    },
    {
      situation: 'Highlighting your textbook in five different colours with a colour-coded system you invented.',
      answer: 'desirable',
      explanation: 'This feels effortful but it\'s fake friction. Highlighting is a passive task that doesn\'t force retrieval or generation. The effort is going into the system, not into learning. Replace it with a Brain Dump or practice questions.',
    },
    {
      situation: 'Trying to write an essay plan from memory, but your phone keeps buzzing with notifications.',
      answer: 'extraneous',
      explanation: 'The task is right (retrieval practice in the ZPD) but the environment is sabotaging it. Each notification hijacks your Working Memory, wiping out the very information you\'re trying to hold. Phone in another room.',
    },
  ];

  const pillars = [
    { key: 'zpd', label: 'Wrong Zone', desc: 'Too easy or too hard', color: 'bg-blue-500 text-white', borderActive: 'border-blue-500' },
    { key: 'extraneous', label: 'Too Much Noise', desc: 'Extraneous load is high', color: 'bg-rose-500 text-white', borderActive: 'border-rose-500' },
    { key: 'desirable', label: 'Fake Friction', desc: 'No desirable difficulties', color: 'bg-amber-500 text-white', borderActive: 'border-amber-500' },
    { key: 'optimal', label: 'Optimized', desc: 'All three pillars aligned', color: 'bg-emerald-500 text-white', borderActive: 'border-emerald-500' },
  ];

  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState<{ [key: number]: string }>({});
  const [revealed, setRevealed] = useState<Set<number>>(new Set());

  const handleAnswer = (pillarKey: string) => {
    if (revealed.has(current)) return;
    setAnswers(prev => ({ ...prev, [current]: pillarKey }));
    setRevealed(prev => new Set(prev).add(current));
  };

  const correct = Object.entries(answers).filter(([i, a]) => a === scenarios[parseInt(i)].answer).length;
  const allDone = revealed.size === scenarios.length;

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Unified Model: Diagnose the Study Session</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Read each scenario and identify the primary problem — or if the session is already optimized.</p>

      {/* Progress */}
      <div className="flex gap-1.5 mb-6">
        {scenarios.map((_, i) => (
          <button
            key={i}
            onClick={() => setCurrent(i)}
            className={`flex-1 h-2 rounded-full transition-all ${
              revealed.has(i)
                ? answers[i] === scenarios[i].answer ? 'bg-emerald-500' : 'bg-rose-400'
                : i === current ? 'bg-teal-400' : 'bg-zinc-200 dark:bg-zinc-700'
            }`}
          />
        ))}
      </div>

      {/* Scenario card */}
      <AnimatePresence mode="wait">
        <motion.div
          key={current}
          initial={{ opacity: 0, x: 15 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -15 }}
        >
          <div className="p-5 bg-zinc-50 dark:bg-zinc-900/30 rounded-xl border border-zinc-200 dark:border-zinc-700 mb-5">
            <p className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 mb-2">Scenario {current + 1} of {scenarios.length}</p>
            <p className="text-sm font-medium text-zinc-800 dark:text-zinc-200 leading-relaxed">{scenarios[current].situation}</p>
          </div>

          {/* Diagnosis buttons */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mb-5">
            {pillars.map(p => {
              const isChosen = answers[current] === p.key;
              const isCorrect = scenarios[current].answer === p.key;
              const isRevealed = revealed.has(current);

              let btnStyle: React.CSSProperties = { backgroundColor: '#FFFFFF', border: '2.5px solid #1C1917', borderRadius: 14, boxShadow: '3px 3px 0px 0px #1C1917' };
              let btnTextColor = '';
              if (isRevealed && isChosen && isCorrect) { btnStyle = { backgroundColor: '#6EE7B7', border: '2.5px solid #059669', borderRadius: 14, boxShadow: '3px 3px 0px 0px #059669' }; btnTextColor = '#064E3B'; }
              else if (isRevealed && isChosen && !isCorrect) { btnStyle = { backgroundColor: '#FCA5A5', border: '2.5px solid #DC2626', borderRadius: 14, boxShadow: '3px 3px 0px 0px #DC2626' }; btnTextColor = '#7F1D1D'; }
              else if (isRevealed && isCorrect) { btnStyle = { backgroundColor: '#6EE7B7', border: '2.5px solid #059669', borderRadius: 14, boxShadow: '3px 3px 0px 0px #059669', opacity: 0.7 }; btnTextColor = '#064E3B'; }

              return (
                <button
                  key={p.key}
                  onClick={() => handleAnswer(p.key)}
                  disabled={isRevealed}
                  className="p-3 rounded-xl text-center transition-all"
                  style={{ ...btnStyle, color: btnTextColor || undefined }}
                >
                  <p className="text-xs font-bold">{p.label}</p>
                  <p className="text-[9px] opacity-70 mt-0.5">{p.desc}</p>
                </button>
              );
            })}
          </div>

          {/* Feedback */}
          {revealed.has(current) && (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className={`p-4 rounded-xl border ${
                answers[current] === scenarios[current].answer
                  ? 'bg-emerald-50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40'
                  : 'bg-rose-50 dark:bg-rose-950/20 border-rose-200 dark:border-rose-800/40'
              }`}
            >
              <p className={`text-xs font-bold mb-1 ${answers[current] === scenarios[current].answer ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}`}>
                {answers[current] === scenarios[current].answer ? 'Correct' : 'Not quite'}
              </p>
              <p className="text-sm text-zinc-700 dark:text-zinc-300">{scenarios[current].explanation}</p>
            </motion.div>
          )}
        </motion.div>
      </AnimatePresence>

      {/* Navigation */}
      <div className="flex justify-between mt-6">
        <button
          onClick={() => setCurrent(c => Math.max(0, c - 1))}
          disabled={current === 0}
          className="px-4 py-2 text-xs font-bold text-zinc-500 dark:text-zinc-400 disabled:opacity-30"
        >
          Previous
        </button>
        {current < scenarios.length - 1 ? (
          <button
            onClick={() => setCurrent(c => c + 1)}
            className="px-4 py-2 text-xs font-bold text-teal-600 dark:text-teal-400"
          >
            Next
          </button>
        ) : allDone ? (
          <span className="px-4 py-2 text-xs font-bold text-emerald-600 dark:text-emerald-400">
            {correct}/{scenarios.length} correct
          </span>
        ) : null}
      </div>

      {/* Final insight */}
      {allDone && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-4 p-4 bg-teal-50 dark:bg-teal-950/20 rounded-xl border border-teal-200 dark:border-teal-800/40 text-center"
        >
          <p className="text-sm font-semibold text-teal-700 dark:text-teal-300">
            The formula: Right Zone + Low Noise + Real Friction = Optimized Learning.
          </p>
          <p className="text-xs text-teal-600/70 dark:text-teal-400/60 mt-1">
            Before every study session, run this quick diagnostic on your setup.
          </p>
        </motion.div>
      )}
    </div>
  );
}


const ConfidenceRetentionParadox = () => {
    const [revealed, setRevealed] = useState(false);

    const W = 440, H = 260;
    const padL = 8, padR = 8, padT = 28, padB = 44;
    const chartW = W - padL - padR, chartH = H - padT - padB;
    const toX = (f: number) => padL + f * chartW;
    const toY = (f: number) => padT + (1 - f) * chartH;

    const days = ['Day 0', 'Day 1', 'Day 3', 'Day 7', 'Day 14', 'Day 30'];
    // Passive Re-reading: Confidence stays high, Retention crashes
    const passiveConfidence = [0.90, 0.88, 0.82, 0.78, 0.72, 0.68];
    const passiveRetention  = [0.85, 0.55, 0.38, 0.28, 0.22, 0.18];
    // Active Recall: Confidence starts low and stays moderate, Retention holds
    const activeConfidence = [0.35, 0.40, 0.45, 0.50, 0.55, 0.60];
    const activeRetention  = [0.50, 0.52, 0.55, 0.58, 0.60, 0.61];

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

    const passivePhases = [
        { label: 'Feels easy', x1: 0, x2: 0.33, color: '#fca5a5' },
        { label: 'Still confident', x1: 0.33, x2: 0.66, color: '#f87171' },
        { label: 'Exam shock', x1: 0.66, x2: 1, color: '#ef4444' },
    ];
    const activePhases = [
        { label: 'Feels hard', x1: 0, x2: 0.33, color: '#6ee7b7' },
        { label: 'Building', x1: 0.33, x2: 0.66, color: '#34d399' },
        { label: 'Exam ready', x1: 0.66, x2: 1, color: '#10b981' },
    ];

    const Chart = ({ confidence, retention, phases, areaColor, areaId, areaData, label }: {
        confidence: number[]; retention: number[]; phases: { label: string; x1: number; x2: number; color: string }[];
        areaColor: string; areaId: string; areaData: number[]; label: string;
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
            {/* Confidence line (solid — primary) */}
            <motion.path
                d={buildLine(confidence)}
                fill="none" stroke={areaColor} strokeWidth="2.5" strokeLinecap="round"
                initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                transition={{ duration: 1.2, ease: 'easeOut' }}
            />
            {/* Retention line (dashed — secondary) */}
            <motion.path
                d={buildLine(retention)}
                fill="none" stroke={areaColor} strokeWidth="1.5" strokeDasharray="5 3" strokeLinecap="round"
                initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                transition={{ duration: 1.2, ease: 'easeOut', delay: 0.3 }}
            />
            {/* Confidence dots */}
            {confidence.map((v, i) => (
                <motion.circle key={i} cx={toX(i / (confidence.length - 1))} cy={toY(v)} r="3.5" fill={areaColor}
                    initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2 * i + 0.3 }}
                />
            ))}
            {/* Y-axis labels */}
            <text x={padL + 2} y={toY(1.0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">High</text>
            <text x={padL + 2} y={toY(0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">Low</text>
            {/* Day labels */}
            {days.map((d, i) => (
                <text key={d} x={toX(i / (days.length - 1))} y={toY(0) + 14} fontSize="9" fill="#a1a1aa" textAnchor="middle" fontWeight="600">{d}</text>
            ))}
            {/* Phase labels */}
            {phases.map((p, i) => (
                <text key={i} x={toX((p.x1 + p.x2) / 2)} y={toY(0) + 28} fontSize="8" fill={p.color} textAnchor="middle" fontWeight="700">{p.label}</text>
            ))}
            {/* Chart label */}
            <text x={W / 2} y={14} fontSize="11" fill="#71717a" textAnchor="middle" fontWeight="700">{label}</text>
            {/* Legend */}
            <line x1={W - padR - 108} x2={W - padR - 92} y1={14} y2={14} stroke={areaColor} strokeWidth="2" />
            <text x={W - padR - 88} y={17} fontSize="8" fill="#a1a1aa">Confidence</text>
            <line x1={W - padR - 44} x2={W - padR - 28} y1={14} y2={14} stroke={areaColor} strokeWidth="1.5" strokeDasharray="4 2" />
            <text x={W - padR - 24} y={17} fontSize="8" fill="#a1a1aa">Retention</text>
        </svg>
    );

    return (
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Confidence Trap</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">What feels best works worst. What feels worst works best.</p>

            {!revealed ? (
                <div className="text-center">
                    <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">Most students judge their learning by how confident they feel. What does that confidence actually track over time?</p>
                    <button onClick={() => setRevealed(true)} className="px-5 py-2.5 text-sm font-bold rounded-lg bg-teal-500 text-white hover:bg-teal-600 transition-colors">
                        Reveal the Trap
                    </button>
                </div>
            ) : (
                <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
                    <div className="grid md:grid-cols-2 gap-4 mb-5">
                        <div className="rounded-lg border border-rose-200 dark:border-rose-900 bg-rose-50/50 dark:bg-rose-950/20 p-3">
                            <Chart confidence={passiveConfidence} retention={passiveRetention} phases={passivePhases}
                                areaColor="#ef4444" areaId="passive-grad" areaData={passiveConfidence} label="Passive Re-reading" />
                        </div>
                        <div className="rounded-lg border border-emerald-200 dark:border-emerald-900 bg-emerald-50/50 dark:bg-emerald-950/20 p-3">
                            <Chart confidence={activeConfidence} retention={activeRetention} phases={activePhases}
                                areaColor="#10b981" areaId="active-grad" areaData={activeRetention} label="Active Recall" />
                        </div>
                    </div>
                    <div className="grid md:grid-cols-2 gap-4 text-sm">
                        <div className="flex items-start gap-2.5 p-3 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900">
                            <span className="text-rose-500 text-lg mt-0.5">&#x2716;</span>
                            <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-rose-600 dark:text-rose-400">Re-reading</strong> creates fluency — the material feels familiar. But recognition isn't recall. When the exam asks you to produce answers, the knowledge isn't there.</p>
                        </div>
                        <div className="flex items-start gap-2.5 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900">
                            <span className="text-emerald-500 text-lg mt-0.5">&#x2714;</span>
                            <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-emerald-600 dark:text-emerald-400">Active recall</strong> feels effortful and uncertain. But that struggle is the learning happening. Each retrieval strengthens the memory trace.</p>
                        </div>
                    </div>
                </motion.div>
            )}
        </div>
    );
};

// --- MODULE COMPONENT ---
const EffectiveStruggleAndGrowthModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'fallacy-of-ease', title: 'The Fallacy of Ease', eyebrow: '01 // The Illusion', icon: Thermometer },
    { id: 'cognitive-load', title: 'Your Brain\'s Bottleneck', eyebrow: '02 // The Governor', icon: Brain },
    { id: 'zpd', title: 'The Sweet Spot', eyebrow: '03 // The Boundary', icon: Scaling },
    { id: 'desirable-difficulties', title: 'The Engine of Memory', eyebrow: '04 // The Engine', icon: Puzzle },
    { id: 'unified-model', title: 'The Unified Model', eyebrow: '05 // The Formula', icon: SlidersHorizontal },
    { id: 'recalibrate', title: 'Recalibrate Your Dashboard', eyebrow: '06 // The Feeling', icon: BarChartHorizontal },
  ];

  return (
    <ModuleLayout
      moduleNumber="04"
      moduleTitle="Effective Struggle"
      moduleSubtitle="Why the Hard Stuff Is the Stuff That Works"
      moduleDescription={`That frustrated feeling when you're stuck on a hard question? It's not a sign you're failing — it's actually how real learning happens. Here's how to use it.`}
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Embrace the Struggle"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Fallacy of Ease." eyebrow="Step 1" icon={Thermometer} theme={theme}>
              <p>Our intuition tells us that learning should feel easy. We think that if a teacher explains something perfectly and we understand it without any friction, that's a sign of great learning. This is the <Highlight description="Basically, your brain tricks you into thinking that if something feels easy to learn, you must be learning it well. But it's the opposite — the easy stuff slides right out of your memory." theme={theme}>Intuitive Fallacy of Ease</Highlight>, and it's the single biggest trap students fall into.</p>
              <ConfidenceRetentionParadox />
              <p>Here's the thing most people get wrong: your feeling of how well you're learning is often the exact opposite of what's actually happening in your brain. Easy learning feels good but gets forgotten fast. Hard, effortful learning feels rough but it sticks. It's the difference between taking an escalator and taking the stairs. Only one of them makes you stronger.</p>
              <StairsEscalator />
              <p>This isn't just a vibe — it's been tested. In one experiment, students who just re-read their notes predicted they'd remember 90% of it. Students who tested themselves predicted only 40%. But when they were actually tested a week later, the re-readers scored just 40%, while the self-testers scored 61%. The strategy that felt worse was way more effective. Toggle the chart below to see the gap between confidence and reality.</p>
              <IllusionOfCompetenceChart />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="Your Brain's Bottleneck." eyebrow="Step 2" icon={Brain} theme={theme}>
              <p>To understand why difficulty is necessary, you need to know about a bottleneck in your brain called <Highlight description="Think of this as your brain's tiny desk. You can only hold about 3-5 things on it at once. If you pile on too much, stuff falls off and nothing gets learned." theme={theme}>Working Memory</Highlight>. Everything you learn has to pass through it, and if you overload it, learning just stops.</p>
              <p>There are three types of "load": <Highlight description="This is the useless stuff clogging up your brain — your phone buzzing, a noisy room, confusing instructions. It's not helping you learn, it's just taking up space. Get rid of as much of it as you can." theme={theme}>Extraneous Load</Highlight> (the bad stuff), <Highlight description="This is just how hard the topic actually is. Probability is harder than basic addition — you can't change that, you just have to work with it." theme={theme}>Intrinsic Load</Highlight> (the topic itself), and <Highlight description="This is the good kind of effort — the mental work that actually builds understanding. Things like testing yourself, explaining ideas out loud, or working through problems. You want as much of this as possible." theme={theme}>Germane Load</Highlight> (the good stuff). The art of learning is to clear out all the 'bad' difficulty so you have enough mental space for the 'good' difficulty that actually builds memory.</p>
              <CognitiveLoadBalancer />
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The Sweet Spot." eyebrow="Step 3" icon={Scaling} theme={theme}>
              <p>The perfect level of difficulty is not too hard and not too easy. In psychology, this is called the <Highlight description="Your sweet spot. It's that zone where something is just hard enough that you have to think, but not so hard that you're completely lost. With a bit of effort or a hint, you can get there. That's where the real learning happens." theme={theme}>Zone of Proximal Development (ZPD)</Highlight>. It's the Goldilocks zone of learning.</p>
              <p>Imagine three zones. The <strong>Comfort Zone</strong> is where you do things you've already mastered. You can do them fine, but you're learning nothing new. The <strong>Frustration Zone</strong> is where the task is so far beyond you that you can't even get started — your brain just freezes and you want to give up. The <strong>ZPD</strong> is the sweet spot in between, where you're stretched but not overwhelmed. This is the only place where real growth happens.</p>
              <MicroCommitment theme={theme}>
                <p>Think about your hardest subject. What's one topic that feels just out of reach? Can you find a worked example or ask a friend for help to bring it into your ZPD?</p>
              </MicroCommitment>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Engine of Memory." eyebrow="Step 4" icon={Puzzle} theme={theme}>
              <p>So why does the "sweet spot" feel so hard? Because of how memory actually works. It turns out memory has two strengths: <Highlight description="How easily something comes to mind right now. It's high right after you've just read your notes, but it fades fast. This is the one that tricks you into feeling confident." theme={theme}>Retrieval Strength</Highlight> (how easy it is to access now) and <Highlight description="How deeply something is actually locked into your brain for the long haul. This only grows when you struggle to remember something — not when you passively read it again. This is what actual learning looks like." theme={theme}>Storage Strength</Highlight> (how well you've actually learned it).</p>
              <p>Here's the paradox: your brain only increases Storage Strength when Retrieval Strength is <em>low</em>. In other words, you have to forget something a little bit before your brain will put in the effort to store it properly for the long term. This is why re-reading your notes feels easy (high retrieval strength) but does nothing for long-term memory. You need the "desirable difficulty" of struggling to remember.</p>
              <p>This was proven clearly in <Highlight description="A famous experiment where one group re-read their notes four times, and the other group read once then tested themselves three times. A week later, the self-testers remembered way more — even though the re-readers had felt more confident." theme={theme}>a well-known experiment</Highlight>. Two groups of students studied the same text. One group re-read it four times. The other group read it once and then tested themselves on it three times. After five minutes, the re-readers did slightly better — which makes sense, it was still fresh. But after one week, the results completely flipped: the re-readers had forgotten more than half of the material, while the self-testing group held onto much more. This is the <Highlight description="Testing yourself isn't just a way to check what you know — it's one of the best ways to actually learn. Every time you try to pull something out of your memory, you make that memory stronger. So quizzing yourself beats re-reading every time." theme={theme}>Testing Effect</Highlight> in action.</p>
              <p>Here's the kicker: the re-readers were also more <em>confident</em>. They predicted higher scores. They genuinely felt like they knew the material better. But their confidence was completely wrong. The students who struggled through self-testing — who felt less confident, who made mistakes, who found it uncomfortable — were the ones who actually learned. That's the engine of memory: the struggle to pull something out of your brain is the signal that tells it "this matters, lock it in."</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Unified Model." eyebrow="Step 5" icon={SlidersHorizontal} theme={theme}>
                <p>Now let's put everything together into one simple formula for studying that actually works.</p>
                <ScenarioDiagnosis />
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Recalibrate Your Dashboard." eyebrow="Step 6" icon={BarChartHorizontal} theme={theme}>
              <p>Your brain is lazy by design. It prefers the escalator to the stairs. This means your gut feeling about how well you're learning is basically broken. You have to learn to override it.</p>
              <p>From now on, when learning feels slow, frustrating, and difficult, that's not a sign you should stop. It's a sign that you're in the sweet spot. It's the feeling of your brain actually rewiring itself. You're not "confused" — you're building real understanding. You're not "slow" — you're building long-term memory. If it feels like a struggle, it's working.</p>
              <p>Here's a bonus: regular low-stakes self-testing doesn't just improve your memory — it also crushes exam anxiety. Think about it: anxiety usually comes from uncertainty. You *think* you know the material, but you've never actually tested that belief until the Leaving Cert. Quizzing yourself regularly is a form of <Highlight description="Getting honest with yourself about what you actually know vs. what you just think you know. When you quiz yourself regularly, you stop guessing and start knowing exactly where your gaps are — so there are no nasty surprises on exam day." theme={theme}>Metacognitive Calibration</Highlight> — it replaces false confidence with honest self-knowledge. When you test yourself regularly, you walk into the exam hall knowing exactly what you know and what you don't. No surprises, no panic. You've already faced the hard stuff at home.</p>
              <MicroCommitment theme={theme}>
                <p>Commit to the <strong>10/20 Rule</strong>: for every 30-minute study session, spend only 10 minutes reading or reviewing the material, and then spend 20 minutes testing yourself with the book closed. Write everything you can remember, do practice questions, or explain the topic out loud. This single shift — from mostly reading to mostly recalling — will transform your retention and eliminate exam-day surprises. Start with your very next study session.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default EffectiveStruggleAndGrowthModule;
