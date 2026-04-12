
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import {
  Server, Filter, Archive, BrainCircuit, Moon, ClipboardCheck
} from 'lucide-react';
import { type ModuleProgress } from '../types';
import { fuchsiaTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useEssentialsMode } from '../hooks/useEssentialsMode';

const theme = fuchsiaTheme;

// --- INTERACTIVE COMPONENTS ---

const _MemoryFlowVisualizer = () => {
  const [attention, setAttention] = useState(false);

  const particleCount = 5;
  const particles = Array.from({ length: particleCount }, (_, i) => i);

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Memory Pipeline</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">
        {attention
          ? 'Attention is ON — information flows all the way to Long-Term Memory.'
          : 'Without attention, information fades after Sensory Memory. Hit "Pay Attention" to see the difference.'}
      </p>

      {/* Pipeline visualization */}
      <div className="relative flex items-center justify-between gap-2 md:gap-4 mb-4 px-2">
        {/* Sensory box */}
        <div className="flex-shrink-0 w-24 md:w-28">
          <motion.div
            className="rounded-xl border-2 p-3 md:p-4 text-center"
            animate={{
              borderColor: attention ? '#d946ef' : '#a1a1aa',
              backgroundColor: attention ? 'rgba(217, 70, 239, 0.08)' : 'rgba(161, 161, 170, 0.05)',
            }}
            transition={{ duration: 0.4 }}
          >
            <p className="text-xs font-bold text-zinc-800 dark:text-zinc-200">Sensory</p>
            <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-0.5">Split-second</p>
          </motion.div>
        </div>

        {/* Arrow 1: Sensory to Short-Term */}
        <div className="flex-1 relative h-12 overflow-hidden">
          <svg className="absolute inset-0 w-full h-full" preserveAspectRatio="none">
            <defs>
              <marker id="mem-arrow1" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
                <polygon points="0 0, 8 3, 0 6" fill={attention ? '#d946ef' : '#a1a1aa'} />
              </marker>
            </defs>
            <line x1="0" y1="24" x2="100%" y2="24" stroke={attention ? '#d946ef' : '#a1a1aa'} strokeWidth="2" strokeDasharray="6 4" markerEnd="url(#mem-arrow1)" />
          </svg>
          <AnimatePresence>
            {particles.map(i => (
              <motion.div
                key={`p1-${i}-${attention}`}
                className="absolute top-1/2 -translate-y-1/2 w-3 h-3 rounded-full"
                style={{ backgroundColor: attention ? '#d946ef' : '#f472b6' }}
                initial={{ left: '-5%', opacity: 0, scale: 0.5 }}
                animate={attention ? {
                  left: ['0%', '100%'],
                  opacity: [0, 1, 1, 0],
                  scale: [0.5, 1, 1, 0.5],
                } : {
                  left: ['0%', '50%'],
                  opacity: [0, 1, 0],
                  scale: [0.5, 1, 0],
                }}
                transition={{
                  duration: attention ? 1.8 : 1.2,
                  delay: i * 0.5,
                  repeat: Infinity,
                  repeatDelay: particleCount * 0.5 - (attention ? 1.8 : 1.2) + 0.5,
                  ease: 'easeInOut',
                }}
              />
            ))}
          </AnimatePresence>
          {!attention && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="absolute right-0 -bottom-0.5 text-[9px] font-bold text-rose-400 dark:text-rose-500"
            >
              Lost!
            </motion.p>
          )}
        </div>

        {/* Short-Term box */}
        <div className="flex-shrink-0 w-24 md:w-28">
          <motion.div
            className="rounded-xl border-2 p-3 md:p-4 text-center"
            animate={{
              borderColor: attention ? '#d946ef' : '#52525b',
              backgroundColor: attention ? 'rgba(217, 70, 239, 0.08)' : 'rgba(82, 82, 91, 0.05)',
              opacity: attention ? 1 : 0.5,
            }}
            transition={{ duration: 0.4 }}
          >
            <p className="text-xs font-bold text-zinc-800 dark:text-zinc-200">Short-Term</p>
            <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-0.5">15-30 sec</p>
          </motion.div>
        </div>

        {/* Arrow 2: Short-Term to Long-Term */}
        <div className="flex-1 relative h-12 overflow-hidden">
          <svg className="absolute inset-0 w-full h-full" preserveAspectRatio="none">
            <defs>
              <marker id="mem-arrow2" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
                <polygon points="0 0, 8 3, 0 6" fill={attention ? '#d946ef' : '#a1a1aa'} />
              </marker>
            </defs>
            <line x1="0" y1="24" x2="100%" y2="24" stroke={attention ? '#d946ef' : '#a1a1aa'} strokeWidth="2" strokeDasharray="6 4" markerEnd="url(#mem-arrow2)" />
          </svg>
          <AnimatePresence>
            {attention && particles.map(i => (
              <motion.div
                key={`p2-${i}`}
                className="absolute top-1/2 -translate-y-1/2 w-3 h-3 rounded-full bg-fuchsia-500"
                initial={{ left: '-5%', opacity: 0, scale: 0.5 }}
                animate={{
                  left: ['0%', '100%'],
                  opacity: [0, 1, 1, 0],
                  scale: [0.5, 1, 1, 0.5],
                }}
                transition={{
                  duration: 1.8,
                  delay: i * 0.5 + 0.9,
                  repeat: Infinity,
                  repeatDelay: particleCount * 0.5 - 1.8 + 0.5,
                  ease: 'easeInOut',
                }}
              />
            ))}
          </AnimatePresence>
        </div>

        {/* Long-Term box */}
        <div className="flex-shrink-0 w-24 md:w-28">
          <motion.div
            className="rounded-xl border-2 p-3 md:p-4 text-center"
            animate={{
              borderColor: attention ? '#10b981' : '#52525b',
              backgroundColor: attention ? 'rgba(16, 185, 129, 0.08)' : 'rgba(82, 82, 91, 0.05)',
              opacity: attention ? 1 : 0.4,
            }}
            transition={{ duration: 0.4 }}
          >
            <p className="text-xs font-bold text-zinc-800 dark:text-zinc-200">Long-Term</p>
            <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-0.5">Permanent</p>
          </motion.div>
        </div>
      </div>

      {/* Status indicator */}
      <p className={`text-center text-xs font-bold mb-6 ${attention ? 'text-emerald-500' : 'text-rose-400'}`}>
        {attention ? 'Information is being encoded into Long-Term Memory' : 'Information is decaying — nothing reaches Long-Term Memory'}
      </p>

      <div className="flex justify-center">
        <button onClick={() => setAttention(!attention)}
          className={`px-5 py-2.5 font-bold text-sm rounded-lg transition-colors ${
            attention
              ? 'bg-zinc-200 dark:bg-zinc-700 text-zinc-800 dark:text-white hover:bg-zinc-300 dark:hover:bg-zinc-600'
              : 'bg-fuchsia-500 hover:bg-fuchsia-600 text-white'
          }`}
        >
          {attention ? 'De-Focus' : 'Pay Attention'}
        </button>
      </div>
    </div>
  );
};

// --- Chunking Challenge ---
const CONSONANTS = 'BCDFGHJKLMNPQRSTVWXYZ'.split('');
const CHUNKED_SETS = [
  ['GAA', 'FAI', 'RTÉ', 'BBC'],
  ['TCD', 'UCD', 'DCU', 'UCC'],
  ['CAO', 'HSE', 'ESB', 'DAA'],
  ['USB', 'GPS', 'VPN', 'PDF'],
  ['DNA', 'MRI', 'CPR', 'WHO'],
];

type ChallengePhase = 'idle' | 'memorise' | 'recall' | 'scored';
type ChallengeRound = 1 | 2;

const generateRandomLetters = (): string[] => {
  const letters: string[] = [];
  for (let i = 0; i < 12; i++) {
    letters.push(CONSONANTS[Math.floor(Math.random() * CONSONANTS.length)]);
  }
  return letters;
};

const pickChunkedSet = (): string[] => {
  return CHUNKED_SETS[Math.floor(Math.random() * CHUNKED_SETS.length)];
};

const scoreAnswer = (correct: string[], answer: string): number => {
  const cleaned = answer.toUpperCase().replace(/[^A-Z]/g, '');
  let hits = 0;
  for (let i = 0; i < correct.length; i++) {
    if (cleaned[i] === correct[i]) hits++;
  }
  return hits;
};

const ChunkingChallenge = () => {
  const [round, setRound] = useState<ChallengeRound>(1);
  const [phase, setPhase] = useState<ChallengePhase>('idle');
  const [countdown, setCountdown] = useState(5);
  const [letters, setLetters] = useState<string[]>([]);
  const [chunks, setChunks] = useState<string[]>([]);
  const [input, setInput] = useState('');
  const [scoreR1, setScoreR1] = useState<number | null>(null);
  const [scoreR2, setScoreR2] = useState<number | null>(null);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const clearTimer = () => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  };

  useEffect(() => {
    return () => clearTimer();
  }, []);

  const startMemorisePhase = (letterArr: string[]) => {
    setLetters(letterArr);
    setPhase('memorise');
    setCountdown(5);
    setInput('');

    clearTimer();
    let t = 5;
    timerRef.current = setInterval(() => {
      t -= 1;
      setCountdown(t);
      if (t <= 0) {
        clearTimer();
        setPhase('recall');
      }
    }, 1000);
  };

  const handleStartRound1 = () => {
    setRound(1);
    setScoreR1(null);
    setScoreR2(null);
    const randomLetters = generateRandomLetters();
    startMemorisePhase(randomLetters);
  };

  const handleStartRound2 = () => {
    setRound(2);
    const chunked = pickChunkedSet();
    setChunks(chunked);
    const allLetters = chunked.join('').split('');
    startMemorisePhase(allLetters);
  };

  const handleSubmit = () => {
    const score = scoreAnswer(letters, input);
    if (round === 1) {
      setScoreR1(score);
      setPhase('scored');
    } else {
      setScoreR2(score);
      setPhase('scored');
    }
  };

  const handleReset = () => {
    clearTimer();
    setPhase('idle');
    setRound(1);
    setScoreR1(null);
    setScoreR2(null);
    setLetters([]);
    setChunks([]);
    setInput('');
    setCountdown(5);
  };

  const displayLetters = () => {
    if (round === 2 && chunks.length > 0) {
      return chunks.join('   ');
    }
    return letters.join(' ');
  };

  // --- Results view ---
  if (scoreR1 !== null && scoreR2 !== null) {
    const maxBar = 12;
    return (
      <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Results</h4>
        <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-1 mb-8">How did chunking change your recall?</p>

        <div className="space-y-6 max-w-md mx-auto">
          {/* Unchunked bar */}
          <div>
            <div className="flex justify-between text-sm font-semibold mb-1">
              <span className="text-zinc-700 dark:text-zinc-300">Unchunked (Random)</span>
              <span className="text-rose-600 dark:text-rose-400">{scoreR1}/12</span>
            </div>
            <div className="h-6 w-full bg-zinc-100 dark:bg-zinc-700 rounded-full overflow-hidden">
              <MotionDiv
                initial={{ width: 0 }}
                animate={{ width: `${(scoreR1 / maxBar) * 100}%` }}
                transition={{ duration: 0.8, ease: 'easeOut' }}
                className="h-full bg-rose-500 rounded-full"
              />
            </div>
          </div>

          {/* Chunked bar */}
          <div>
            <div className="flex justify-between text-sm font-semibold mb-1">
              <span className="text-zinc-700 dark:text-zinc-300">Chunked (Acronyms)</span>
              <span className="text-emerald-600 dark:text-emerald-400">{scoreR2}/12</span>
            </div>
            <div className="h-6 w-full bg-zinc-100 dark:bg-zinc-700 rounded-full overflow-hidden">
              <MotionDiv
                initial={{ width: 0 }}
                animate={{ width: `${(scoreR2 / maxBar) * 100}%` }}
                transition={{ duration: 0.8, ease: 'easeOut', delay: 0.3 }}
                className="h-full bg-emerald-500 rounded-full"
              />
            </div>
          </div>
        </div>

        <div className="mt-8 p-4 bg-fuchsia-50 dark:bg-fuchsia-900/20 border border-fuchsia-200 dark:border-fuchsia-800 rounded-lg text-sm text-zinc-700 dark:text-zinc-300 leading-relaxed">
          <strong>Same number of letters.</strong> But grouping them turned 12 random items into 4 familiar acronyms — easy for your brain to hold. This is why organising information into meaningful groups makes such a huge difference when you're studying.
        </div>

        <div className="flex justify-center mt-6">
          <button onClick={handleReset} className="px-5 py-2.5 bg-fuchsia-500 hover:bg-fuchsia-600 text-white font-bold text-sm rounded-lg transition-colors">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  // --- Idle: prompt to start ---
  if (phase === 'idle') {
    return (
      <div className="my-10 rounded-2xl p-6 md:p-8 text-center" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white">The Chunking Challenge</h4>
        <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-6 max-w-md mx-auto">Can you memorise 12 letters in 5 seconds? Two rounds will show you the power of chunking.</p>
        <button onClick={handleStartRound1} className="px-5 py-2.5 bg-fuchsia-500 hover:bg-fuchsia-600 text-white font-bold text-sm rounded-lg transition-colors">
          Start Round 1
        </button>
      </div>
    );
  }

  // --- Memorise phase ---
  if (phase === 'memorise') {
    return (
      <div className="my-10 rounded-2xl p-6 md:p-8 text-center" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white">
          {round === 1 ? 'Round 1: Random Letters' : 'Round 2: Chunked Letters'}
        </h4>
        <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1 mb-6">Memorise these letters!</p>

        <MotionDiv
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-3xl md:text-4xl font-mono tracking-widest text-zinc-800 dark:text-white py-4"
        >
          {displayLetters()}
        </MotionDiv>

        <div className="mt-6">
          <span className="inline-flex items-center justify-center w-14 h-14 rounded-full bg-fuchsia-100 dark:bg-fuchsia-900/40 text-fuchsia-600 dark:text-fuchsia-300 text-2xl font-bold">
            {countdown}
          </span>
        </div>
      </div>
    );
  }

  // --- Recall phase ---
  if (phase === 'recall') {
    return (
      <div className="my-10 rounded-2xl p-6 md:p-8 text-center" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white">
          {round === 1 ? 'Round 1: Recall' : 'Round 2: Recall'}
        </h4>
        <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1 mb-6">Type the 12 letters you saw (no spaces needed).</p>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="e.g. XKMBRF..."
          maxLength={24}
          autoFocus
          className="w-full max-w-sm mx-auto block text-center text-lg font-mono tracking-widest bg-white dark:bg-zinc-800 rounded-xl px-5 py-3 text-zinc-800 dark:text-white outline-none"
          style={{ border: '1.5px solid #E7E5E4' }}
        />
        <button
          onClick={handleSubmit}
          disabled={input.trim().length === 0}
          className="mt-4 px-5 py-2.5 bg-emerald-500 hover:bg-emerald-600 disabled:opacity-40 text-white font-bold text-sm rounded-lg transition-colors"
        >
          Submit
        </button>
      </div>
    );
  }

  // --- Scored (between rounds) ---
  if (phase === 'scored' && round === 1) {
    return (
      <div className="my-10 rounded-2xl p-6 md:p-8 text-center" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white">Round 1 Score</h4>
        <p className="text-4xl font-bold text-rose-500 mt-4">{scoreR1}/12</p>
        <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-6">Now let's try the same task — but with chunked letters.</p>
        <button onClick={handleStartRound2} className="px-5 py-2.5 bg-fuchsia-500 hover:bg-fuchsia-600 text-white font-bold text-sm rounded-lg transition-colors">
          Start Round 2
        </button>
      </div>
    );
  }

  return null;
};

const WorkingMemorySimulator = () => {
  const [items, setItems] = useState<string[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [showItems, setShowItems] = useState(false);
  const [result, setResult] = useState<number|null>(null);

  useEffect(() => {
    if (showItems) {
      const timer = setTimeout(() => setShowItems(false), 3000);
      return () => clearTimeout(timer);
    }
  }, [showItems]);

  const startGame = () => {
    const newItems = Array.from({length: 7}, () => Math.floor(Math.random() * 90 + 10).toString());
    setItems(newItems);
    setShowItems(true);
    setResult(null);
    setInputValue('');
  };

  const checkAnswer = () => {
    const userItems = inputValue.split(' ').filter(Boolean);
    const score = items.filter(item => userItems.includes(item)).length;
    setResult(score);
  };

  if (result !== null) {
    return (
      <div className="my-10 rounded-2xl p-6 md:p-8 text-center" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Results</h4>
        <p>You correctly recalled {result} out of {items.length} items.</p>
        <p className="text-xs text-zinc-500 dark:text-zinc-400">The original items were: {items.join(', ')}</p>
        <button onClick={startGame} className="mt-4 px-4 py-2 bg-fuchsia-500 text-white font-bold text-sm rounded-lg">Try Again</button>
      </div>
    );
  }

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8 text-center" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Short-Term Memory Test</h4>
      {!showItems && items.length === 0 && <button onClick={startGame} className="px-4 py-2 bg-fuchsia-500 text-white font-bold text-sm rounded-lg">Start</button>}

      {showItems && <p className="text-3xl font-mono tracking-widest">{items.join(' ')}</p>}

      {!showItems && items.length > 0 &&
        <div>
          <input value={inputValue} onChange={e => setInputValue(e.target.value)} placeholder="Type the numbers, separated by spaces" className="w-full bg-white dark:bg-zinc-800 rounded-xl px-5 py-3.5 text-sm font-medium text-zinc-800 dark:text-white placeholder-zinc-400 outline-none" style={{ border: '1.5px solid #E7E5E4' }} />
          <button onClick={checkAnswer} className="mt-4 px-4 py-2 bg-emerald-500 text-white font-bold text-sm rounded-lg">Check Answer</button>
        </div>
      }
    </div>
  );
};

// --- MODULE COMPONENT ---
const TheCognitiveArchitectureModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'three-stores', title: 'Your Three Types of Memory', eyebrow: '01 // The Basics', icon: Server },
    { id: 'bottleneck', title: 'Why Your Brain Gets Overloaded', eyebrow: '02 // The Bottleneck', icon: Filter },
    { id: 'filing-cabinet', title: 'How Long-Term Memory Is Organised', eyebrow: '03 // The Library', icon: Archive },
    { id: 'save-button', title: 'How to Actually Save What You Learn', eyebrow: '04 // Making It Stick', icon: BrainCircuit },
    { id: 'night-shift', title: 'Why Sleep Is Non-Negotiable', eyebrow: '05 // The Night Shift', icon: Moon },
    { id: 'checklist', title: 'Your Action Plan', eyebrow: '06 // Next Steps', icon: ClipboardCheck },
  ];

  return (
    <ModuleLayout moduleNumber="04" moduleTitle="How Your Memory Works" moduleSubtitle="Your Brain's User Manual" moduleDescription="Learn how your memory actually works — how information gets in, why most of it falls out, and what you can do to make the important stuff stick for the Leaving Cert." theme={theme} sections={sections} onBack={onBack} progress={progress} onProgressUpdate={onProgressUpdate} finishButtonText="Map Your Memory">
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Your Three Types of Memory." eyebrow="Step 1" icon={Server} theme={theme}>
              {essentials ? (
                <>
                  <p>Your memory works in three stages. First, <strong>Sensory Memory</strong> catches a quick flash of what you see or hear. If you pay attention, it moves to <strong>Short-Term Memory</strong> -- your mental workbench. From there, you need to deliberately move it into <strong>Long-Term Memory</strong> -- the permanent store.</p>
                  <p>Your whole job as a student is getting better at moving information from that workbench into long-term storage. That is what good study techniques help you do.</p>
                </>
              ) : (
                <>
                  <p>To do well in the Leaving Cert, it really helps to understand how the machine you're working with — your own brain — actually handles information. The simplest way to think about it is that your memory has <Highlight description="A simple way of understanding memory: it comes in three stages — a quick flash, a short holding space, and a long-term store." theme={theme}>three stages</Highlight>.</p>
                  <p>First, there's <Highlight description="The very first stage of memory — a split-second snapshot of what you see or hear. If you don't pay attention to it, it's gone instantly." theme={theme}>Sensory Memory</Highlight>, the brief flash of what you see or hear. Anything you don't pay attention to here is gone forever. If you <em>do</em> pay attention, it moves to <Highlight description="Your brain's temporary holding space. It can only hold a small amount of information for a short time — think of it as your mental workbench." theme={theme}>Short-Term Memory</Highlight>, your brain's mental workbench. From there, it has to be deliberately moved to <Highlight description="Your brain's permanent storage. This is where knowledge needs to end up if you want to remember it in an exam." theme={theme}>Long-Term Memory</Highlight>, the permanent hard drive. Your entire job as a student is to get better at moving stuff from that workbench into long-term storage.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Why Your Brain Gets Overloaded." eyebrow="Step 2" icon={Filter} theme={theme}>
              {essentials ? (
                <>
                  <p>Your short-term memory can only hold about <strong>4 chunks</strong> at once. Without active effort, information fades in 15-30 seconds. This is why you can read a page and remember nothing.</p>
                  <p>Cramming jams this bottleneck. It creates memories that feel strong but vanish quickly. You need strategies that move information into long-term storage instead.</p>
                </>
              ) : (
                <>
                  <p>Your Short-Term Memory — the part of your brain that <Highlight description="The part of your brain that holds and works with information right now. Think of it as your mental desk — it can only fit a few things on it at once." theme={theme}>holds and works with information right now</Highlight> — is the biggest bottleneck in your learning. It's shockingly limited. You might think you can juggle loads of info, but realistically your brain can only hold about <strong>4 chunks of information</strong> at a time when dealing with complex Leaving Cert material.</p>
                  <p>Even worse, without active effort, this information fades in about <strong>15-30 seconds</strong>. This is why you can read a whole page of a textbook and have no memory of it. The information landed on your mental desk but disappeared before it could be saved anywhere. Cramming jams this bottleneck, creating a memory that feels strong but vanishes quickly.</p>
                </>
              )}
              <ChunkingChallenge/>
              <WorkingMemorySimulator/>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="How Long-Term Memory Is Organised." eyebrow="Step 3" icon={Archive} theme={theme}>
              {essentials ? (
                <>
                  <p>Your long-term memory has three types. <strong>Fact memory</strong> stores definitions and dates. <strong>Experience memory</strong> stores things that happened to you. <strong>Skill memory</strong> stores how-to knowledge.</p>
                  <p>For many subjects, skill memory matters most. Maths is not about memorising facts. It is about practising steps until they become automatic. Study the type that matches your subject.</p>
                </>
              ) : (
                <>
                  <p>Your Long-Term Memory isn't one big box; it's more like a filing cabinet with different drawers for different types of knowledge. Knowing which drawer you're using helps you study smarter.</p>
                  <p>The first drawer is <Highlight description="Your store of facts and general knowledge — things like Biology definitions, History dates, or what the capital of France is." theme={theme}>fact memory</Highlight> — your library of facts and definitions. The second is <Highlight description="Your store of personal experiences — like remembering a specific Chemistry experiment or what happened in class last Tuesday." theme={theme}>experience memory</Highlight> — your personal collection of things that happened to you. The third, and most important for many subjects, is <Highlight description="Your store of skills and 'how-to' knowledge — like how to solve a Maths equation or conjugate a French verb. It's muscle memory for your brain." theme={theme}>skill memory</Highlight>. Maths isn't about memorising facts; it's about practising steps until they become automatic.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="How to Actually Save What You Learn." eyebrow="Step 4" icon={BrainCircuit} theme={theme}>
              {essentials ? (
                <>
                  <p>Moving information into long-term memory is called <strong>encoding</strong>. Re-reading creates weak memories. Connecting new information to what you already know creates strong ones.</p>
                  <p>Deep studying means thinking about what something means. Your brain cells physically strengthen their connections the more you use them. Use a pathway often and it becomes automatic.</p>
                </>
              ) : (
                <>
                  <p>Moving information from your temporary workbench to your permanent hard drive is called <Highlight description="The process of turning a temporary memory into a lasting one. How deeply you think about something decides how well you'll remember it." theme={theme}>encoding</Highlight> — basically, hitting the 'save' button. But not all saving is equal. <Highlight description="When you only skim the surface of something — like re-reading a definition without really thinking about it. This creates weak memories that fade fast." theme={theme}>Surface-level studying</Highlight>, like just re-reading a definition, creates weak, flimsy memories.</p>
                  <p><Highlight description="When you really think about what something means and connect it to things you already know. This creates strong memories that last." theme={theme}>Deep studying</Highlight> is about connecting new information to what you already know. For example, learning that "mitochondria is the powerhouse of the cell" is surface-level. Understanding <em>how</em> it produces energy and why that's essential for your muscles to work is deep. What's actually happening in your brain is that <Highlight description="When brain cells fire together repeatedly, the connections between them get physically stronger — like a path getting worn into a field the more you walk it." theme={theme}>the connections between your brain cells get physically stronger</Highlight> — the more you use a pathway, the easier it becomes to use again.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Why Sleep Is Non-Negotiable." eyebrow="Step 5" icon={Moon} theme={theme}>
              {essentials ? (
                <>
                  <p>Your brain saves what you learned during deep sleep. New information sits in a temporary inbox during the day. While you sleep, your brain replays it and moves the important stuff into permanent storage.</p>
                  <p>Pulling an all-nighter cancels this saving process. You need proper sleep for your studying to actually stick.</p>
                </>
              ) : (
                <>
                  <p>Here's something your brain absolutely needs: the final "save" button gets hit while you sleep. During the day, new information sits in a <Highlight description="A small part of your brain that acts like a temporary inbox. Everything you learn during the day lands here first — but it can only hold stuff temporarily." theme={theme}>temporary inbox</Highlight> in your brain. It can hold things for a while, but nothing is permanent yet.</p>
                  <p>During deep sleep, your brain <Highlight description="While you sleep, your brain replays what you learned during the day and moves the important stuff from temporary storage into permanent storage. No sleep = no proper saving." theme={theme}>replays what you learned</Highlight> and moves the important memories from that temporary inbox into permanent storage in the <Highlight description="The outer layer of your brain where long-term memories are permanently stored. Think of it as your brain's hard drive." theme={theme}>main part of your brain</Highlight>. Pulling an all-nighter is like trying to save a file while constantly hitting 'cancel' on the save dialog. It's self-sabotage.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Your Action Plan." eyebrow="Step 6" icon={ClipboardCheck} theme={theme}>
              {essentials ? (
                <>
                  <p>Good results come from using the right approach, not natural talent. Test yourself, space out your study, and mix topics. These work with how your memory naturally operates.</p>
                  <p>Sleep, food, water, and stress levels directly affect your brain. High stress blocks memory. Look after yourself -- it is one of the best things you can do for your grades.</p>
                </>
              ) : (
                <>
                  <p>Understanding how your memory works gives you an owner's manual for your own brain. It shows that doing well isn't about "natural talent" — it's about using the right approach. Strategies like testing yourself, spacing out your study, and mixing topics are all just ways to work with how your memory naturally operates.</p>
                  <p>But even the best strategies will fail if you're running on empty. Your <Highlight description="How well your body is doing — your sleep, what you're eating, whether you're drinking enough water, and your stress levels. All of these directly affect how well your brain works." theme={theme}>physical state</Highlight> is the foundation. When you're really stressed, your brain releases <Highlight description="A stress hormone. When it stays high for too long, it actually makes it harder for your brain to store and recall memories." theme={theme}>stress hormones</Highlight> that actually block your ability to remember things. Dehydration and poor nutrition starve your brain of the resources it needs. Looking after yourself isn't a 'wellness' tip — it's one of the most important things you can do for your grades.</p>
                </>
              )}
              <MicroCommitment theme={theme}>
                <p>Tonight, set an alarm to put your phone away 60 minutes before you go to bed. This single act of 'sleep hygiene' has a bigger impact on your memory than an extra hour of cramming.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default TheCognitiveArchitectureModule;
