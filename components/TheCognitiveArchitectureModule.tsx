
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Server, Filter, Archive, BrainCircuit, Moon, ClipboardCheck
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { fuchsiaTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = fuchsiaTheme;

// --- INTERACTIVE COMPONENTS ---

const MemoryFlowVisualizer = () => {
  const [attention, setAttention] = useState(false);
  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Memory Pipeline</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Information is either lost or transferred. Attention is the gatekeeper.</p>
      <div className="flex items-center justify-between text-center font-bold text-xs h-24">
        <span>Sensory</span>
        <svg className="w-full h-px mx-4"><line x1="0" y1="0" x2="100%" y2="0" stroke="black" strokeDasharray="4"/></svg>
        <span>Short-Term</span>
        <svg className="w-full h-px mx-4"><line x1="0" y1="0" x2="100%" y2="0" stroke="black" strokeDasharray="4"/></svg>
        <span>Long-Term</span>
      </div>
      <div className="flex justify-center mt-6">
        <button onClick={() => setAttention(!attention)} className="px-4 py-2 bg-fuchsia-500 text-white font-bold text-sm rounded-lg">{attention ? 'De-Focus' : 'Pay Attention'}</button>
      </div>
    </div>
  );
};

const MotionDiv = motion.div as any;

// --- Chunking Challenge ---
const CONSONANTS = 'BCDFGHJKLMNPQRSTVWXYZ'.split('');
const CHUNKED_SETS = [
  ['FBI', 'CIA', 'NSA', 'BBC'],
  ['NBA', 'NFL', 'MLB', 'NHL'],
  ['BMW', 'KFC', 'CNN', 'MTV'],
  ['USB', 'GPS', 'VPN', 'PDF'],
  ['DNA', 'MRI', 'CPR', 'NHS'],
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
      <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
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
          <strong>Same number of letters.</strong> But chunking compressed 12 items into 4 meaningful groups — well within your working memory's ~4 slot limit. This is why experts outperform novices: they chunk information into larger, meaningful units.
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
      <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700 text-center">
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
      <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700 text-center">
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
      <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700 text-center">
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
          className="w-full max-w-sm mx-auto block p-3 text-center text-lg font-mono tracking-widest border border-zinc-300 dark:border-zinc-600 rounded-lg bg-white dark:bg-zinc-900 text-zinc-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-fuchsia-400"
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
      <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700 text-center">
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
      <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700 text-center">
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Results</h4>
        <p>You correctly recalled {result} out of {items.length} items.</p>
        <p className="text-xs text-zinc-500 dark:text-zinc-400">The original items were: {items.join(', ')}</p>
        <button onClick={startGame} className="mt-4 px-4 py-2 bg-fuchsia-500 text-white font-bold text-sm rounded-lg">Try Again</button>
      </div>
    );
  }

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700 text-center">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">STM Bottleneck Test</h4>
      {!showItems && items.length === 0 && <button onClick={startGame} className="px-4 py-2 bg-fuchsia-500 text-white font-bold text-sm rounded-lg">Start</button>}

      {showItems && <p className="text-3xl font-mono tracking-widest">{items.join(' ')}</p>}

      {!showItems && items.length > 0 &&
        <div>
          <input value={inputValue} onChange={e => setInputValue(e.target.value)} placeholder="Type the numbers, separated by spaces" className="w-full p-2 border rounded-md"/>
          <button onClick={checkAnswer} className="mt-4 px-4 py-2 bg-emerald-500 text-white font-bold text-sm rounded-lg">Check Answer</button>
        </div>
      }
    </div>
  );
};


// --- MODULE COMPONENT ---
const TheCognitiveArchitectureModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'three-stores', title: 'The Three Memory Stores', eyebrow: '01 // The Blueprint', icon: Server },
    { id: 'bottleneck', title: 'The Working Memory Bottleneck', eyebrow: '02 // The Bottleneck', icon: Filter },
    { id: 'filing-cabinet', title: 'The LTM Filing Cabinet', eyebrow: '03 // The Library', icon: Archive },
    { id: 'save-button', title: 'Hitting the "Save" Button', eyebrow: '04 // The Biology of Saving', icon: BrainCircuit },
    { id: 'night-shift', title: 'The Night Shift', eyebrow: '05 // The Role of Sleep', icon: Moon },
    { id: 'checklist', title: 'The Operator\'s Checklist', eyebrow: '06 // The Action Plan', icon: ClipboardCheck },
  ];

  return (
    <ModuleLayout moduleNumber="04" moduleTitle="Cognitive Architecture" moduleSubtitle="Your Brain's User Manual" moduleDescription="Understand the fundamental architecture of your memory to move information from the fragile workbench of Short-Term Memory to the permanent library of Long-Term Memory." theme={theme} sections={sections} onBack={onBack} progress={progress} onProgressUpdate={onProgressUpdate}>
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Three Memory Stores." eyebrow="Step 1" icon={Server} theme={theme}>
              <p>To win the Leaving Cert, you need to understand the machine you're working with: your own brain. The most useful model for this is the <Highlight description="A classic psychological model that proposes memory consists of three separate stores: Sensory Memory, Short-Term Memory (STM), and Long-Term Memory (LTM)." theme={theme}>Multi-Store Model</Highlight>. It breaks your memory into three parts.</p>
              <p>First, there's <Highlight description="An ultra-short-term buffer for information from your senses. It lasts for milliseconds and is mostly outside your conscious control." theme={theme}>Sensory Memory</Highlight>, the brief echo of what you see or hear. Anything you don't pay attention to here is gone forever. If you *do* pay attention, it moves to <Highlight description="A temporary storage space with very limited capacity and duration. Also known as Working Memory." theme={theme}>Short-Term Memory (STM)</Highlight>, your brain's mental workbench. From there, it has to be deliberately transferred to <Highlight description="The vast, durable library of your mind. This is where knowledge needs to end up to be useful in an exam." theme={theme}>Long-Term Memory (LTM)</Highlight>, the permanent hard drive. Your entire job as a student is to manage this transfer process effectively.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Working Memory Bottleneck." eyebrow="Step 2" icon={Filter} theme={theme}>
              <p>Your Short-Term Memory, or <Highlight description="The part of your mind that holds and actively manipulates a small amount of information for a short time. It's the 'RAM' of your brain." theme={theme}>Working Memory</Highlight>, is the biggest bottleneck in your learning. It's shockingly limited. Classic research suggested you can hold about 7 items, but for complex Leaving Cert topics, it's more like <strong>4 'chunks' of information</strong>.</p>
              <p>Even worse, without active effort, this information decays in about <strong>15-30 seconds</strong>. This is why you can read a whole page of a textbook and have no memory of it. The information entered your working memory but evaporated before it could be processed. Cramming jams this bottleneck, creating a fragile memory that feels strong but is quickly erased.</p>
              <ChunkingChallenge/>
              <WorkingMemorySimulator/>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The LTM Filing Cabinet." eyebrow="Step 3" icon={Archive} theme={theme}>
              <p>Your Long-Term Memory is not one big box; it's a sophisticated filing cabinet with different drawers for different types of knowledge. Knowing which drawer you're using helps you study smarter.</p>
              <p>The first is <Highlight description="Memory for facts, concepts, and general knowledge. This is your 'textbook' memory for things like Biology definitions or History dates." theme={theme}>Semantic Memory</Highlight>—your library of facts. The second is <Highlight description="Memory for personal experiences and specific events. Remembering a specific Chemistry experiment is episodic." theme={theme}>Episodic Memory</Highlight>—your personal photo album of events. The third, and most critical for many subjects, is <Highlight description="Memory for skills and 'how-to' knowledge, like how to solve a Maths equation or conjugate a French verb. It's your 'muscle memory' for the mind." theme={theme}>Procedural Memory</Highlight>. Maths isn't about memorizing facts; it's about building automated procedures.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Hitting the 'Save' Button." eyebrow="Step 4" icon={BrainCircuit} theme={theme}>
              <p>The transfer from your temporary workbench (STM) to your permanent hard drive (LTM) is called <Highlight description="The process of transforming temporary memories into durable, long-term ones. The 'depth' of this process determines the strength of the memory." theme={theme}>Encoding</Highlight>. Not all encoding is equal. <Highlight description="Processing information based on its surface features, like its sound or appearance (e.g., rote repetition). It creates weak memories." theme={theme}>Shallow Processing</Highlight>, like just re-reading a definition, creates weak, flimsy memories.</p>
              <p><Highlight description="Processing information based on its meaning and connecting it to your existing knowledge. This creates strong, interconnected memories." theme={theme}>Deep Processing</Highlight> is about linking new information to what you already know. For example, learning that "mitochondria is the powerhouse of the cell" is shallow. Understanding *how* it produces ATP and why that's essential for your muscles to work is deep. The biological basis for this is <Highlight description="The long-lasting strengthening of the connections (synapses) between neurons. It's the physical basis of memory, often summarized as 'neurons that fire together, wire together.'" theme={theme}>Long-Term Potentiation (LTP)</Highlight>—you're physically strengthening the wiring.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Night Shift." eyebrow="Step 5" icon={Moon} theme={theme}>
              <p>Here's a non-negotiable rule of your brain's biology: the final "save" button is hit while you sleep. During the day, new information is temporarily stored in a part of your brain called the <Highlight description="A seahorse-shaped structure in the brain that acts as a temporary buffer or 'inbox' for new memories. It's like your brain's RAM." theme={theme}>Hippocampus</Highlight>. It's a volatile, temporary storage space.</p>
              <p>During deep sleep, your brain runs a process called <Highlight description="The physiological process where memories are transferred from the temporary storage of the hippocampus to the permanent storage of the neocortex. This happens primarily during sleep." theme={theme}>System Consolidation</Highlight>. It replays the day's events and transfers important memories from the hippocampus to your main hard drive, the <Highlight description="The outer layer of the brain responsible for higher-order thinking. It's the 'hard drive' for your long-term memories." theme={theme}>Neocortex</Highlight>. Pulling an all-nighter is like trying to learn a new topic while constantly hitting 'cancel' on the save dialog. It's self-sabotage.</p>
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="The Operator's Checklist." eyebrow="Step 6" icon={ClipboardCheck} theme={theme}>
              <p>Understanding your cognitive architecture gives you an owner's manual for your own brain. It shows that high performance isn't about "natural talent"; it's about running the right processes. All the evidence-based strategies—Active Recall, Spacing, Interleaving—are simply ways to optimize this natural memory pipeline.</p>
              <p>But even the best strategies will fail if the hardware is compromised. Your <Highlight description="Your biological state, including sleep, nutrition, hydration, and stress levels. Your cognitive function is highly dependent on your physiological baseline." theme={theme}>Physiological State</Highlight> is the foundation. High stress floods your brain with <Highlight description="The 'stress hormone.' Chronically high levels can impair the function of your hippocampus, making it harder to form and retrieve memories." theme={theme}>Cortisol</Highlight>, effectively blocking memory retrieval. Dehydration and poor nutrition starve your brain of the resources it needs. Getting your baseline right isn't a 'wellness' tip; it's a core academic strategy.</p>
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
