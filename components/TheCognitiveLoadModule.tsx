/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Cpu, SlidersHorizontal, AlertTriangle, Activity, Wrench } from 'lucide-react';
import { ModuleProgress } from '../types';
import { fuchsiaTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
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
          Your span: {span} items. Average: 4. This is your working memory's hard limit. Every study session must respect it. When you pack more than ~4 new concepts into a single sitting without pausing to consolidate, information simply drops out — and you won't even notice.
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
    { label: 'Schema building', x1: 0.66, x2: 1, color: '#10b981' },
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
      <text x={W - padR - 100} y={17} fontSize="8" fill="#a1a1aa">Extraneous Load</text>
      <line x1={W - padR - 44} x2={W - padR - 28} y1={14} y2={14} stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="4 2" />
      <text x={W - padR - 24} y={17} fontSize="8" fill="#a1a1aa">Actual Learning</text>
    </svg>
  );

  return (
    <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Cognitive Load in Action</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Two study sessions. Same material. Very different outcomes.</p>

      {!revealed ? (
        <div className="text-center">
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">Where does your mental energy go during a typical study session? Most of it is wasted on extraneous load.</p>
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
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-rose-600 dark:text-rose-400">Extraneous load dominates.</strong> Cluttered desk, phone buzzing, split-attention materials. Your 4 working memory slots are consumed by distractions, leaving almost nothing for actual learning.</p>
            </div>
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900">
              <span className="text-emerald-500 text-lg mt-0.5">&#x2714;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-emerald-600 dark:text-emerald-400">Germane load dominates.</strong> Clean environment, integrated materials, focused attention. Working memory is freed up for schema building — the actual learning.</p>
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
    { id: 'three-types-of-load', title: 'Three Types of Load', eyebrow: '02 // The Framework', icon: SlidersHorizontal },
    { id: 'split-attention-effect', title: 'The Split-Attention Effect', eyebrow: '03 // The Design Flaw', icon: AlertTriangle },
    { id: 'expertise-reversal-effect', title: 'The Expertise Reversal Effect', eyebrow: '04 // The Shifting Threshold', icon: Activity },
    { id: 'managing-your-load', title: 'Managing Your Load', eyebrow: '05 // The Protocol', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="47"
      moduleTitle="The Cognitive Load Protocol"
      moduleSubtitle="The Working Memory Blueprint"
      moduleDescription="Your working memory can hold only 4 items at once. Learn why most study sessions accidentally overload this bottleneck — and how to design sessions that respect your brain's limits."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Bottleneck." eyebrow="Step 1" icon={Cpu} theme={theme}>
              <p><Highlight description="George Miller's 1956 paper 'The Magical Number Seven, Plus or Minus Two' proposed that short-term memory holds 7 plus or minus 2 items. For decades this was accepted as gospel in cognitive psychology." theme={theme}>Miller (1956)</Highlight> famously proposed that working memory holds 7 plus or minus 2 items. For decades, this was the accepted number. But <Highlight description="Nelson Cowan (University of Missouri) published a landmark review in 2001 showing that when rehearsal and chunking strategies are controlled for, the true capacity of working memory is approximately 4 items — significantly less than Miller's estimate. This has been replicated across visual, auditory, and abstract domains." theme={theme}>Cowan (2001)</Highlight> demonstrated that the true capacity is much smaller: approximately 4 items when rehearsal and chunking are controlled. This is the hard limit on what your brain can process simultaneously.</p>
              <p>Every piece of new information, every instruction, every diagram label competes for those 4 slots. When you exceed them, information simply drops out — and you don't even notice it happening. This is called <Highlight description="Cognitive overload occurs when the demands on working memory exceed its capacity. The critical insight is that overload is silent: you don't feel a 'full' signal. Information simply fails to encode, and you remain unaware of what you missed." theme={theme}>cognitive overload</Highlight>, and its most dangerous feature is that it's invisible. You don't feel a "full" signal. Material just fails to encode, and you remain unaware of what you missed.</p>
              <p>This is why re-reading a dense paragraph three times still doesn't make sense: your working memory overflows on each pass. The words enter short-term storage, but there's no room left to actually process their meaning, connect them to prior knowledge, or build the <Highlight description="A schema is an organised framework of knowledge stored in long-term memory. Unlike individual facts, schemas allow you to process complex information as a single 'chunk,' effectively bypassing working memory limits. Schema building is the core mechanism of deep learning." theme={theme}>schemas</Highlight> that constitute real understanding. You're reading, but you're not learning. And because the text looks familiar on each re-read, you mistake that familiarity for comprehension.</p>
              <WorkingMemoryDemo />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Three Types of Load." eyebrow="Step 2" icon={SlidersHorizontal} theme={theme}>
              <p><Highlight description="John Sweller (University of New South Wales) developed Cognitive Load Theory beginning in 1988. His foundational insight was that instructional design should be guided by the architecture of human cognition — specifically, the limited capacity of working memory and the effectively unlimited capacity of long-term memory." theme={theme}>Sweller (1988, 1994)</Highlight> identified three types of cognitive load that compete for your working memory's limited slots. Understanding these three types is the key to optimising every study session.</p>
              <p>First: <Highlight description="Intrinsic load is determined by the inherent complexity of the material being learned and the learner's prior knowledge. A quadratic equation has higher intrinsic load than basic addition. You cannot eliminate intrinsic load — it IS the learning challenge. But you can manage it through sequencing and prerequisite mastery." theme={theme}>Intrinsic load</Highlight> — the inherent complexity of the material itself. Quantum mechanics has higher intrinsic load than basic arithmetic. You can't change this; it's a property of the subject matter combined with your current level of expertise. Second: <Highlight description="Extraneous load is caused by poor instructional design or a chaotic study environment — anything that forces working memory to process information that doesn't contribute to learning. Phone notifications, searching for materials, decoding cluttered layouts, and mentally integrating separated diagrams and text are all sources of extraneous load." theme={theme}>Extraneous load</Highlight> — cognitive effort wasted on poor design, distractions, or bad study materials. This is pure waste. Third: <Highlight description="Germane load is the cognitive effort devoted to constructing and automating schemas in long-term memory. It represents actual learning — the effortful processing of new information into lasting understanding. This is the only type of load you want to maximise." theme={theme}>Germane load</Highlight> — the effort devoted to actual learning, schema construction, and deep processing. This is what you want.</p>
              <p><Highlight description="Fred Paas and Jeroen van Merriënboer (Open University of the Netherlands) showed in 1994 that effective instruction works by minimising extraneous load to free up working memory capacity for germane processing. Their research demonstrated that the total cognitive load experienced by a learner is additive: intrinsic + extraneous + germane must fit within working memory's capacity." theme={theme}>Paas and van Merriënboer (1994)</Highlight> showed that effective instruction minimises extraneous load to free up capacity for germane processing. The equation is simple: your 4 working memory slots must accommodate all three types of load simultaneously. If extraneous load consumes 3 of those slots (phone buzzing, cluttered notes, split-attention materials), you have only 1 slot left for actual learning. Flip the ratio, and suddenly your brain has room to build understanding.</p>
              <CognitiveLoadComparison />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Split-Attention Effect." eyebrow="Step 3" icon={AlertTriangle} theme={theme}>
              <p><Highlight description="Paul Chandler and John Sweller (University of New South Wales) published a series of experiments in 1992 demonstrating that when learners must mentally integrate multiple sources of information that are physically or temporally separated, the act of integration itself consumes working memory capacity — leaving less room for actual learning." theme={theme}>Chandler and Sweller (1992)</Highlight> demonstrated one of the most common and insidious sources of extraneous load: the <Highlight description="The split-attention effect occurs when learners must mentally integrate two or more sources of information that could have been physically integrated. For example, a geometry diagram with labels numbered 1-5 and a separate legend explaining each label forces learners to hold the diagram in memory while searching the legend — consuming working memory for navigation rather than understanding." theme={theme}>split-attention effect</Highlight>. When a diagram and its explanatory text are physically separated — text at the bottom of the page, diagram at the top — learners must mentally integrate them. That integration process consumes working memory capacity that should be used for understanding the actual content.</p>
              <p>The research is unambiguous: <Highlight description="Integrated formats place explanatory text directly on or adjacent to the relevant part of a diagram, eliminating the need for learners to search and mentally combine separate information sources. Studies consistently show 30-50% better learning outcomes with integrated formats compared to split formats, with the effect being strongest for complex materials and novice learners." theme={theme}>integrated formats</Highlight> (labels placed directly on diagrams) dramatically outperform split formats. The effect size is substantial — learners who studied integrated materials performed 30 to 50% better on transfer tests than those who studied the same content in split format. This isn't a minor optimisation; it's a fundamental design principle.</p>
              <p>The practical implications are immediate. When studying from textbooks, <Highlight description="Annotating diagrams means writing explanatory labels, key terms, and brief notes directly onto the visual rather than keeping them in separate notes. This eliminates the split-attention effect at the source. Use different colours for different types of annotations (definitions, processes, exceptions) to add another layer of organisation." theme={theme}>annotate diagrams directly</Highlight> rather than reading captions separately. When making flashcards, integrate visual and verbal information on the same side rather than splitting them across front and back for related content. When using online resources, prefer those with inline annotations over those with footnotes or separate explanation panels. Every time you eliminate a split-attention source, you free up working memory for the thing that actually matters: building understanding.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Expertise Reversal Effect." eyebrow="Step 4" icon={Activity} theme={theme}>
              <p><Highlight description="Slava Kalyuga, Paul Ayres, Paul Chandler, and John Sweller published a comprehensive review in 2003 showing that instructional techniques beneficial for novice learners become ineffective or even detrimental for more experienced learners. This 'expertise reversal effect' has been replicated across mathematics, science, engineering, and language learning." theme={theme}>Kalyuga et al. (2003)</Highlight> discovered something deeply counterintuitive: instructional techniques that help beginners actually <em>hurt</em> experts. This finding, called the <Highlight description="The expertise reversal effect occurs because what constitutes 'extraneous' load changes with expertise. For a novice, a worked example reduces intrinsic load by providing scaffolding. For an expert, that same worked example is redundant information — they already have the relevant schemas in long-term memory. Processing the redundant example now adds extraneous load rather than reducing it." theme={theme}>Expertise Reversal Effect</Highlight>, fundamentally changes how you should think about study methods.</p>
              <p><Highlight description="Worked examples are step-by-step demonstrations of how to solve a problem or apply a concept. Research by Sweller and Cooper (1985) showed they are highly effective for novices because they reduce the need for means-ends analysis — a process that consumes enormous working memory capacity. But this advantage disappears and reverses as expertise develops." theme={theme}>Worked examples</Highlight> are excellent for novices because they reduce intrinsic load by providing scaffolding. The learner doesn't need to figure out the solution strategy — they can focus on understanding each step. But for advanced students who already possess relevant schemas, the same worked examples become redundant information. Processing that redundancy adds extraneous load — the expert's brain is wasting working memory on information it already knows.</p>
              <p>This means your optimal study method changes as you improve. Early in a topic: use worked examples, guided solutions, and scaffolded problems. These reduce the intrinsic load of unfamiliar material. Later, as you build expertise: switch to <Highlight description="Independent problem-solving and retrieval practice become superior to worked examples once a learner has developed sufficient schemas. At this stage, the 'generation effect' (producing answers from memory) creates stronger encoding than studying provided solutions. The transition point varies by individual and topic — calibration skills (knowing what you know) help you identify when to make the switch." theme={theme}>independent problem-solving and retrieval practice</Highlight>. The study methods that got you from 0 to 60% understanding will actively hold you back from 60 to 90%. The key is recognising when you've crossed that threshold — which is exactly why the metacognitive calibration skills from earlier modules matter so much here.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Managing Your Load." eyebrow="Step 5" icon={Wrench} theme={theme}>
              <p>Everything in this module converges on a single protocol for managing cognitive load during study. Step one: <Highlight description="Reducing extraneous load means systematically eliminating everything in your study environment and materials that wastes working memory without contributing to learning. Research by Mayer (2009) established the 'coherence principle' — removing all non-essential information, including interesting but irrelevant details, background music with lyrics, and decorative images that don't support the learning objective." theme={theme}>Reduce extraneous load</Highlight>. Clean desk. Phone in another room — not face-down on the desk, not on silent, in another room entirely. Close every browser tab except what you need. Use integrated study materials where text and diagrams are combined, not separated.</p>
              <p>Step two: <Highlight description="Managing intrinsic load means controlling the complexity of what you're trying to learn at any given moment. This doesn't mean avoiding hard material — it means breaking it into manageable chunks that fit within your 4-item working memory limit. Master prerequisite concepts before tackling advanced ones, so that prior knowledge can be leveraged as schemas that reduce the effective load of new material." theme={theme}>Manage intrinsic load</Highlight>. Break complex topics into smaller chunks that fit within your 4-item limit. Master prerequisites before advancing — if you don't understand algebra, calculus will overwhelm your working memory regardless of how well-designed the materials are. Use worked examples when learning new concepts, then transition to independent practice as your expertise grows.</p>
              <p>Step three: <Highlight description="Maximising germane load means using the working memory capacity freed up by steps one and two for generative processing — the cognitive activities that actually build schemas. Richard Mayer's 'contiguity principle' (2009) states that related text and visuals should be placed together in both space and time. Combined with self-explanation, elaboration, and practice testing, these techniques ensure your limited working memory is spent on genuine learning rather than overhead." theme={theme}>Maximise germane load</Highlight>. Once extraneous load is minimised, devote the freed-up capacity to generative processing: self-explanation (explaining concepts to yourself in your own words), elaboration (connecting new information to what you already know), and practice testing (retrieving information from memory rather than re-reading it). <Highlight description="Richard Mayer (University of California, Santa Barbara) synthesised decades of multimedia learning research into a set of evidence-based principles. The coherence principle (remove non-essential information) and the contiguity principle (place related text and visuals together in space and time) are two of the most robust and widely replicated findings in educational psychology." theme={theme}>Mayer (2009)</Highlight> formalised this as the "coherence principle" (remove all non-essential information) and the "contiguity principle" (place related text and visuals together). Together, these principles ensure that every unit of working memory capacity is spent on actual learning.</p>
              <MicroCommitment theme={theme}>
                <p>Before your next study session, spend 2 minutes reducing extraneous load: close every browser tab except what you need, put your phone in another room (not just face-down — another room), and ensure all notes and materials are within arm's reach so you don't break focus searching for them. Then study for 25 minutes. Notice the difference in depth of processing when your 4 working memory slots aren't wasted on distractions.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};

export default TheCognitiveLoadModule;
