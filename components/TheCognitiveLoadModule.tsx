/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Cpu, SlidersHorizontal, AlertTriangle, Activity, Wrench } from 'lucide-react';
import { ModuleProgress } from '../types';
import { fuchsiaTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = fuchsiaTheme;
const MotionDiv = motion.div as any;

// --- INTERACTIVE COMPONENTS ---

// 1. WORKING MEMORY DEMO — Digit span test
const WorkingMemoryDemo = () => {
  const [phase, setPhase] = useState<'ready' | 'showing' | 'recalling' | 'result'>('ready');
  const [sequenceLength, setSequenceLength] = useState(3);
  const [digits, setDigits] = useState<number[]>([]);
  const [currentDigitIndex, setCurrentDigitIndex] = useState(0);
  const [userInput, setUserInput] = useState('');
  const [results, setResults] = useState<{ length: number; correct: boolean }[]>([]);
  const [failCount, setFailCount] = useState(0);
  const [bestSpan, setBestSpan] = useState(0);

  const generateDigits = useCallback((len: number) => {
    const d: number[] = [];
    for (let i = 0; i < len; i++) {
      d.push(Math.floor(Math.random() * 10));
    }
    return d;
  }, []);

  const startRound = useCallback(() => {
    const newDigits = generateDigits(sequenceLength);
    setDigits(newDigits);
    setCurrentDigitIndex(0);
    setUserInput('');
    setPhase('showing');
  }, [sequenceLength, generateDigits]);

  useEffect(() => {
    if (phase !== 'showing') return;
    if (currentDigitIndex >= digits.length) {
      const timer = setTimeout(() => {
        setPhase('recalling');
      }, 500);
      return () => clearTimeout(timer);
    }
    const timer = setTimeout(() => {
      setCurrentDigitIndex((prev) => prev + 1);
    }, 1000);
    return () => clearTimeout(timer);
  }, [phase, currentDigitIndex, digits.length]);

  const handleSubmit = () => {
    const correct = userInput === digits.join('');
    const newResults = [...results, { length: sequenceLength, correct }];
    setResults(newResults);

    if (correct) {
      setBestSpan(sequenceLength);
      setFailCount(0);
      if (sequenceLength < 9) {
        setSequenceLength((prev) => prev + 1);
        setPhase('ready');
      } else {
        setPhase('result');
      }
    } else {
      const newFailCount = failCount + 1;
      setFailCount(newFailCount);
      if (newFailCount >= 2) {
        setPhase('result');
      } else {
        setPhase('ready');
      }
    }
  };

  const reset = () => {
    setPhase('ready');
    setSequenceLength(3);
    setDigits([]);
    setCurrentDigitIndex(0);
    setUserInput('');
    setResults([]);
    setFailCount(0);
    setBestSpan(0);
  };

  if (phase === 'result') {
    const span = bestSpan || (results.find((r) => r.correct) ? Math.max(...results.filter((r) => r.correct).map((r) => r.length)) : 0);
    return (
      <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Your Working Memory Span</h4>
        <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-8">The longest sequence you recalled correctly.</p>

        <div className="text-center mb-6">
          <p className="text-5xl font-bold text-fuchsia-600 dark:text-fuchsia-400">{span}</p>
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-2">items</p>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-6 max-w-xs mx-auto">
          <div className="text-center p-4 rounded-xl bg-fuchsia-50 dark:bg-fuchsia-900/20 border border-fuchsia-200 dark:border-fuchsia-800">
            <p className="text-2xl font-bold text-fuchsia-700 dark:text-fuchsia-300">{span}</p>
            <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">Your Span</p>
          </div>
          <div className="text-center p-4 rounded-xl bg-zinc-50 dark:bg-zinc-900/50 border border-zinc-200 dark:border-zinc-700">
            <p className="text-2xl font-bold text-zinc-700 dark:text-zinc-300">4</p>
            <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">Average</p>
          </div>
        </div>

        <MotionDiv
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          className="p-4 rounded-xl text-sm font-medium bg-fuchsia-50 dark:bg-fuchsia-950/30 text-fuchsia-700 dark:text-fuchsia-300 border border-fuchsia-200 dark:border-fuchsia-800"
        >
          Your span: {span} items. Average: 4. This is the limit of what your brain can juggle at once. When you try to cram more than about 4 new ideas into a study session without taking a break, your brain quietly drops the rest — and you won't even realise it happened.
        </MotionDiv>

        <div className="mt-6 text-center">
          <button onClick={reset} className="px-5 py-2.5 bg-zinc-200 dark:bg-zinc-700 hover:bg-zinc-300 dark:hover:bg-zinc-600 text-zinc-700 dark:text-zinc-200 font-semibold rounded-xl transition-colors text-sm">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Digit Span Test</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-1 mb-6">How many digits can your working memory hold? Let's find out.</p>

      {phase === 'ready' && (
        <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center">
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-2">
            {results.length === 0
              ? 'Digits will flash on screen one at a time. Remember the sequence and type it back.'
              : `Sequence length: ${sequenceLength} digits`}
          </p>
          {failCount === 1 && (
            <p className="text-xs text-amber-500 dark:text-amber-400 mb-3">Incorrect. One more try at this length.</p>
          )}
          <button
            onClick={startRound}
            className="px-6 py-3 text-sm font-bold rounded-xl bg-fuchsia-500 text-white hover:bg-fuchsia-600 transition-colors"
          >
            {results.length === 0 ? 'Start' : 'Next Round'}
          </button>
        </MotionDiv>
      )}

      {phase === 'showing' && (
        <div className="text-center h-32 flex items-center justify-center">
          {currentDigitIndex < digits.length ? (
            <MotionDiv
              key={currentDigitIndex}
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="text-7xl font-bold text-fuchsia-600 dark:text-fuchsia-400 font-mono"
            >
              {digits[currentDigitIndex]}
            </MotionDiv>
          ) : (
            <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-zinc-400 text-sm">
              ...
            </MotionDiv>
          )}
        </div>
      )}

      {phase === 'recalling' && (
        <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center">
          <p className="text-sm font-medium text-zinc-600 dark:text-zinc-300 mb-4">Type the sequence you saw:</p>
          <input
            type="text"
            inputMode="numeric"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value.replace(/[^0-9]/g, ''))}
            onKeyDown={(e) => { if (e.key === 'Enter' && userInput.length > 0) handleSubmit(); }}
            className="w-48 mx-auto block text-center text-2xl font-mono font-bold tracking-widest p-3 rounded-xl border-2 border-fuchsia-300 dark:border-fuchsia-700 bg-zinc-50 dark:bg-zinc-900 text-zinc-800 dark:text-zinc-100 focus:outline-none focus:border-fuchsia-500"
            autoFocus
            maxLength={sequenceLength}
            placeholder={'_'.repeat(sequenceLength)}
          />
          <button
            onClick={handleSubmit}
            disabled={userInput.length === 0}
            className="mt-4 px-6 py-2.5 text-sm font-bold rounded-xl bg-fuchsia-500 text-white hover:bg-fuchsia-600 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
          >
            Submit
          </button>
        </MotionDiv>
      )}

      <div className="flex justify-center gap-1.5 mt-6">
        {results.map((r, i) => (
          <div
            key={i}
            className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${r.correct ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400' : 'bg-rose-100 dark:bg-rose-900/30 text-rose-600 dark:text-rose-400'}`}
          >
            {r.length}
          </div>
        ))}
      </div>
    </div>
  );
};

// 2. COGNITIVE LOAD COMPARISON — Dual chart (Planning Paradox style)
const CognitiveLoadComparison = () => {
  const [revealed, setRevealed] = useState(false);

  const W = 440, H = 260;
  const padL = 8, padR = 8, padT = 28, padB = 44;
  const chartW = W - padL - padR, chartH = H - padT - padB;
  const toX = (f: number) => padL + f * chartW;
  const toY = (f: number) => padT + (1 - f) * chartH;

  const xLabels = ['Start', '15min', '30min', '45min', '60min', '75min'];

  // Overloaded session: extraneous load HIGH and rising, germane load LOW
  const overExtran = [0.40, 0.50, 0.60, 0.68, 0.75, 0.82];
  const overGermane = [0.25, 0.20, 0.15, 0.12, 0.08, 0.05];

  // Optimized session: extraneous load LOW, germane load HIGH
  const optExtran = [0.10, 0.12, 0.10, 0.08, 0.10, 0.08];
  const optGermane = [0.55, 0.60, 0.65, 0.68, 0.72, 0.75];

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

  const overPhases = [
    { label: 'Cluttered setup', x1: 0, x2: 0.33, color: '#fca5a5' },
    { label: 'Multitasking', x1: 0.33, x2: 0.66, color: '#f87171' },
    { label: 'Overloaded', x1: 0.66, x2: 1, color: '#ef4444' },
  ];
  const optPhases = [
    { label: 'Clean setup', x1: 0, x2: 0.33, color: '#6ee7b7' },
    { label: 'Deep focus', x1: 0.33, x2: 0.66, color: '#34d399' },
    { label: 'Real learning', x1: 0.66, x2: 1, color: '#10b981' },
  ];

  const Chart = ({ extraneous, germane, phases, areaColor, areaId, label }: {
    extraneous: number[]; germane: number[]; phases: { label: string; x1: number; x2: number; color: string }[];
    areaColor: string; areaId: string; label: string;
  }) => (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full">
      <defs>
        <linearGradient id={areaId} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={areaColor} stopOpacity="0.5" />
          <stop offset="100%" stopColor={areaColor} stopOpacity="0.05" />
        </linearGradient>
      </defs>
      {/* Grid lines */}
      {[0.25, 0.5, 0.75, 1.0].map((v) => (
        <line key={v} x1={padL} x2={W - padR} y1={toY(v)} y2={toY(v)} stroke="#a1a1aa" strokeOpacity="0.15" strokeDasharray="3 3" />
      ))}
      {/* Baseline */}
      <line x1={padL} x2={W - padR} y1={toY(0)} y2={toY(0)} stroke="#a1a1aa" strokeOpacity="0.3" />
      {/* Extraneous load area */}
      <motion.path
        d={buildArea(extraneous)}
        fill={`url(#${areaId})`}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
      />
      {/* Extraneous load line (solid) */}
      <motion.path
        d={buildLine(extraneous)}
        fill="none" stroke={areaColor} strokeWidth="2.5" strokeLinecap="round"
        initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
        transition={{ duration: 1.2, ease: 'easeOut' }}
      />
      {/* Germane load line (dashed, amber) */}
      <motion.path
        d={buildLine(germane)}
        fill="none" stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="5 3" strokeLinecap="round"
        initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
        transition={{ duration: 1.2, ease: 'easeOut', delay: 0.3 }}
      />
      {/* Extraneous dots */}
      {extraneous.map((v, i) => (
        <motion.circle key={i} cx={toX(i / (extraneous.length - 1))} cy={toY(v)} r="3.5" fill={areaColor}
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
      <text x={W - padR - 100} y={17} fontSize="8" fill="#a1a1aa">Wasted Effort</text>
      <line x1={W - padR - 44} x2={W - padR - 28} y1={14} y2={14} stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="4 2" />
      <text x={W - padR - 24} y={17} fontSize="8" fill="#a1a1aa">Actual Learning</text>
    </svg>
  );

  return (
    <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Mental Load in Action</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Two study sessions. Same material. Very different outcomes.</p>

      {!revealed ? (
        <div className="text-center">
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">Where does your mental energy go during a typical study session? Most of it is wasted on distractions.</p>
          <button onClick={() => setRevealed(true)} className="px-5 py-2.5 text-sm font-bold rounded-lg bg-fuchsia-500 text-white hover:bg-fuchsia-600 transition-colors">
            Reveal the Comparison
          </button>
        </div>
      ) : (
        <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
          <div className="grid md:grid-cols-2 gap-4 mb-5">
            <div className="rounded-lg border border-rose-200 dark:border-rose-900 bg-rose-50/50 dark:bg-rose-950/20 p-3">
              <Chart extraneous={overExtran} germane={overGermane} phases={overPhases}
                areaColor="#ef4444" areaId="over-grad" label="Overloaded Study Session" />
            </div>
            <div className="rounded-lg border border-emerald-200 dark:border-emerald-900 bg-emerald-50/50 dark:bg-emerald-950/20 p-3">
              <Chart extraneous={optExtran} germane={optGermane} phases={optPhases}
                areaColor="#10b981" areaId="opt-grad" label="Optimized Study Session" />
            </div>
          </div>
          <div className="grid md:grid-cols-2 gap-4 text-sm">
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900">
              <span className="text-rose-500 text-lg mt-0.5">&#x2716;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-rose-600 dark:text-rose-400">Distractions dominate.</strong> Cluttered desk, phone buzzing, badly laid-out materials. Your brain's limited capacity is eaten up by distractions, leaving almost nothing for actual learning.</p>
            </div>
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900">
              <span className="text-emerald-500 text-lg mt-0.5">&#x2714;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-emerald-600 dark:text-emerald-400">Real learning dominates.</strong> Clean environment, well-organised materials, focused attention. Your brain is freed up for building real understanding — the stuff that actually sticks.</p>
            </div>
          </div>
        </MotionDiv>
      )}
    </div>
  );
};


// --- MODULE COMPONENT ---
const TheCognitiveLoadModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'the-bottleneck', title: 'The Bottleneck', eyebrow: '01 // The Hard Limit', icon: Cpu },
    { id: 'three-types-of-load', title: 'Three Kinds of Brain Drain', eyebrow: '02 // The Breakdown', icon: SlidersHorizontal },
    { id: 'split-attention-effect', title: 'Why Separate Diagrams Kill Learning', eyebrow: '03 // The Design Trap', icon: AlertTriangle },
    { id: 'expertise-reversal-effect', title: 'When Easy Becomes Harmful', eyebrow: '04 // The Plot Twist', icon: Activity },
    { id: 'managing-your-load', title: "Managing Your Brain's Limits", eyebrow: '05 // Your Game Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="47"
      moduleTitle="Cognitive Load"
      moduleSubtitle="Why Your Brain Gets Overloaded"
      moduleDescription="Your brain can only juggle about 4 things at once. Most study sessions accidentally blow past that limit — and you don't even notice. This module shows you how to stop wasting brainpower and start actually learning."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Lighten the Load"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Bottleneck." eyebrow="Step 1" icon={Cpu} theme={theme}>
              <p>For a long time, scientists thought your <Highlight description="Your short-term memory is like a tiny desk — it can only hold a few things at once before stuff starts falling off." theme={theme}>short-term memory</Highlight> could hold about 7 things at once. But more recent research showed the real number is much smaller: roughly 4 items. That's it. This is the hard limit on what your brain can juggle at any one time.</p>
              <p>Every piece of new information, every instruction, every diagram label competes for those 4 spots. When you go over the limit, information simply drops out — and you don't even notice it happening. This is called <Highlight description="Brain overload happens when you try to process more than your brain can handle at once. The scary part is you don't feel it happening — stuff just quietly disappears." theme={theme}>brain overload</Highlight>, and its most dangerous feature is that it's invisible. You don't feel a "full" signal. Material just fails to stick, and you have no idea what you missed.</p>
              <p>This is why re-reading a dense paragraph three times still doesn't make sense: your brain overflows on each pass. The words enter short-term storage, but there's no room left to actually process their meaning, connect them to what you already know, or build the <Highlight description="A mental framework is like a web of connected ideas in your long-term memory. Once you build one, you can handle complex topics much more easily because your brain treats the whole web as one 'thing'." theme={theme}>mental frameworks</Highlight> that make up real understanding. You're reading, but you're not learning. And because the text looks familiar on each re-read, you mistake that familiarity for actual comprehension.</p>
              <PersonalStory name="Aoife" role="6th Year, Galway">
                <p>I used to sit down with my Biology textbook and read the same chapter three or four times. I'd highlight loads, and it felt like I was really getting it. Then I'd go into the mock and just... blank. It was so frustrating. Once I learned that my brain can only hold about 4 things at a time, I stopped trying to take in a whole chapter at once. I break it into small chunks now, and I actually test myself after each one. It's slower, but I actually remember things in the exam.</p>
              </PersonalStory>
              <WorkingMemoryDemo />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Three Kinds of Brain Drain." eyebrow="Step 2" icon={SlidersHorizontal} theme={theme}>
              <p>Researchers figured out that there are three types of mental load that compete for your brain's limited capacity. Understanding these three types is the key to making every study session count.</p>
              <p>First: <Highlight description="Built-in difficulty is just how hard the topic naturally is. You can't make calculus as easy as basic addition, but you can break it into smaller pieces." theme={theme}>Built-in difficulty</Highlight> — this is just how hard the material naturally is. Higher Level Maths has more built-in difficulty than basic arithmetic. You can't change this; it comes with the subject. Second: <Highlight description="Wasted effort is all the brainpower you burn on things that have nothing to do with learning — phone notifications, messy notes, badly designed textbooks." theme={theme}>Wasted effort</Highlight> — mental energy burned on distractions, bad layouts, or chaotic study setups. This is pure waste. Third: <Highlight description="Actual learning effort is the brainpower you spend making sense of new ideas and connecting them to what you already know. This is the only type you want more of." theme={theme}>Actual learning effort</Highlight> — the energy you spend genuinely understanding new ideas, building connections, and making things stick. This is the good stuff.</p>
              <p>The research shows that good study setups work by cutting wasted effort so your brain has more room for real learning. The maths is simple: your brain's 4-item limit has to fit all three types at once. If distractions eat up 3 of those spots (phone buzzing, cluttered notes, badly laid-out materials), you've only got 1 spot left for actual learning. Flip that ratio, and suddenly your brain has room to build real understanding.</p>
              <CognitiveLoadComparison />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Why Separate Diagrams Kill Learning." eyebrow="Step 3" icon={AlertTriangle} theme={theme}>
              <p>One of the sneakiest ways your brain gets overloaded is something called <Highlight description="This happens when a diagram is on one part of the page and the explanation is somewhere else. Your brain wastes energy jumping back and forth instead of actually learning." theme={theme}>split attention</Highlight>. When a diagram and its explanation are in different places — text at the bottom of the page, diagram at the top — your brain has to mentally stitch them together. That stitching process eats up brainpower that should be going towards actually understanding the content.</p>
              <p>The research is clear: <Highlight description="Putting labels and explanations directly on the diagram means your brain doesn't have to jump around the page. Studies show this leads to 30-50% better results." theme={theme}>putting everything together</Highlight> (labels placed directly on diagrams) massively outperforms having things separated. Students who studied with combined materials performed 30 to 50% better than those who studied the same content with the text and images apart. This isn't a small difference; it's a game-changer.</p>
              <p>You can use this right away. When studying from textbooks, <Highlight description="Writing notes and labels directly onto a diagram saves your brain from constantly flipping between the image and the explanation." theme={theme}>write your notes directly onto diagrams</Highlight> rather than reading captions separately. When making flashcards, put the visual and the explanation on the same side rather than splitting them across front and back. When using online resources, pick ones with labels built into the images over ones with footnotes or separate panels. Every time you stop your brain from having to jump between two sources, you free it up for the thing that actually matters: understanding.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="When Easy Becomes Harmful." eyebrow="Step 4" icon={Activity} theme={theme}>
              <p>Here's something that surprises most people: study techniques that help beginners can actually <em>hurt</em> you once you get better at a topic. This <Highlight description="What helps you when you're new to a topic can actually slow you down once you've got the basics. Your brain starts wasting energy on stuff it already knows." theme={theme}>plot twist</Highlight> fundamentally changes how you should think about study methods.</p>
              <p><Highlight description="Step-by-step worked solutions are brilliant when you're starting out because they show you exactly how to approach a problem. But once you know the approach, reading through them again just wastes your brain's energy." theme={theme}>Worked examples</Highlight> (step-by-step solutions) are excellent when you're starting out because they give you the scaffolding you need. You don't have to figure out the approach — you can focus on understanding each step. But once you've already got a good grasp of the method, those same worked examples become pointless repetition. Going through them now just wastes brainpower on things you already know.</p>
              <p>This means your best study method changes as you improve. Early on in a topic: use worked examples, guided solutions, and practice problems with hints. These lower the difficulty of unfamiliar material. Later, as you get stronger: switch to <Highlight description="Once you know the basics well, testing yourself from memory and solving problems without help builds much stronger learning than re-reading worked examples." theme={theme}>solving problems on your own and testing yourself from memory</Highlight>. The methods that got you from 0 to 60% understanding will actively hold you back from 60 to 90%. The key is recognising when you've crossed that line — which is exactly why knowing what you actually know (from earlier modules) matters so much here.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Managing Your Brain's Limits." eyebrow="Step 5" icon={Wrench} theme={theme}>
              <p>Everything in this module comes down to a simple game plan for managing your mental load while studying. Step one: <Highlight description="Cut out everything in your study space that wastes brainpower without helping you learn — messy desk, open tabs, phone nearby, background noise with lyrics." theme={theme}>Cut the distractions</Highlight>. Clean desk. Phone in another room — not face-down on the desk, not on silent, in another room entirely. Close every browser tab except what you need. Use study materials where text and diagrams are together, not separated.</p>
              <p>Step two: <Highlight description="You can't make hard topics easy, but you can break them into smaller pieces that your brain can actually handle one at a time." theme={theme}>Break it down</Highlight>. Split complex topics into smaller chunks that fit within your brain's 4-item limit. Master the basics before jumping ahead — if you don't understand algebra, calculus will overwhelm your brain no matter how well-organised your notes are. Use worked examples when learning new concepts, then switch to solving problems on your own as you get better.</p>
              <p>Step three: <Highlight description="Once you've cleared away distractions and broken things into chunks, use that freed-up brainpower for the stuff that actually builds understanding." theme={theme}>Make every bit of brainpower count</Highlight>. Once you've cleared away the distractions, use the freed-up brainpower for things that actually build understanding: explaining concepts to yourself in your own words, connecting new information to what you already know, and testing yourself from memory rather than re-reading. Two key principles from the research: <Highlight description="Two simple rules backed by loads of research: remove anything from your study materials that doesn't help you learn, and always keep related images and text together." theme={theme}>remove anything non-essential from your materials</Highlight>, and always keep related text and images together. These two rules make sure every drop of brainpower goes toward real learning.</p>
              <MicroCommitment theme={theme}>
                <p>Before your next study session, spend 2 minutes clearing distractions: close every browser tab except what you need, put your phone in another room (not just face-down — another room), and make sure all your notes and materials are within arm's reach so you don't break focus searching for them. Then study for 25 minutes. Notice the difference when your brain isn't wasting energy on distractions.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};

export default TheCognitiveLoadModule;
