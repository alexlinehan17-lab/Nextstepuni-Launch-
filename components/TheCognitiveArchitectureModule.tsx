/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { AnimatePresence,motion } from 'framer-motion';
import {
Archive,BrainCircuit,
ClipboardCheck,
Filter,
Moon,
Server
} from 'lucide-react';
import React,{ useEffect,useId,useRef,useState } from 'react';
import { HOW_MEMORY_WORKS_REFERENCE_LIST } from '../data/references/howMemoryWorks';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { fuchsiaTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { Highlight,MicroCommitment,ReadingSection } from './ModuleShared';
import { MotionDiv } from './Motion';
import { AnswerLine,ExerciseSheet } from './learning/Exercise';
import { Button,TextButton } from './ui/Button';
import { Field } from './ui/Field';

const theme = fuchsiaTheme;

// --- INTERACTIVE COMPONENTS ---

const _MemoryFlowVisualizer = () => {
  const [attention, setAttention] = useState(false);

  const particleCount = 5;
  const particles = Array.from({ length: particleCount }, (_, i) => i);

  return (
    <ExerciseSheet title="The Memory Pipeline" sub={attention
          ? 'Attention is ON — information flows all the way to Long-Term Memory.'
          : 'Without attention, information fades after Sensory Memory. Hit "Pay Attention" to see the difference.'} name="MemoryFlowVisualizer">
      {/* Pipeline visualization: the module's drawing, in ink on the sheet */}
      <div className="relative flex items-center justify-between gap-2 md:gap-4 px-2">
        {/* Sensory box */}
        <div className="flex-shrink-0 w-24 md:w-28">
          <div className="rounded-xl border p-3 md:p-4 text-center" style={{ borderColor: 'var(--outline-soft)', backgroundColor: 'var(--surface-paper)' }}>
            <p className="t-sub text-ink-primary">Sensory</p>
            <p className="text-[11px] leading-[14px] text-ink-muted mt-0.5">Split-second</p>
          </div>
        </div>

        {/* Arrow 1: Sensory to Short-Term */}
        <div className="flex-1 relative h-12 overflow-hidden">
          <svg className="absolute inset-0 w-full h-full" preserveAspectRatio="none">
            <defs>
              <marker id="mem-arrow1" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
                <polygon points="0 0, 8 3, 0 6" fill={attention ? "var(--ink-primary)" : "var(--ink-muted)"} />
              </marker>
            </defs>
            <line x1="0" y1="24" x2="100%" y2="24" stroke={attention ? "var(--ink-primary)" : "var(--ink-muted)"} strokeWidth="2" strokeDasharray="6 4" markerEnd="url(#mem-arrow1)" />
          </svg>
          <AnimatePresence>
            {particles.map(i => (
              <motion.div
                key={`p1-${i}-${attention}`}
                className="absolute top-1/2 -translate-y-1/2 w-3 h-3 rounded-full"
                style={{ backgroundColor: attention ? 'var(--ink-primary)' : 'var(--ink-muted)' }}
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
              className="absolute right-0 -bottom-0.5 text-[11px] leading-[14px] text-ink-secondary"
            >
              Lost!
            </motion.p>
          )}
        </div>

        {/* Short-Term box */}
        <div className="flex-shrink-0 w-24 md:w-28">
          <motion.div
            className="rounded-xl border p-3 md:p-4 text-center"
            style={{ borderColor: 'var(--outline-soft)', backgroundColor: 'var(--surface-paper)' }}
            animate={{
              opacity: attention ? 1 : 0.5,
            }}
            transition={{ duration: 0.4 }}
          >
            <p className="t-sub text-ink-primary">Short-Term</p>
            <p className="text-[11px] leading-[14px] text-ink-muted mt-0.5">15-30 sec</p>
          </motion.div>
        </div>

        {/* Arrow 2: Short-Term to Long-Term */}
        <div className="flex-1 relative h-12 overflow-hidden">
          <svg className="absolute inset-0 w-full h-full" preserveAspectRatio="none">
            <defs>
              <marker id="mem-arrow2" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
                <polygon points="0 0, 8 3, 0 6" fill={attention ? "var(--ink-primary)" : "var(--ink-muted)"} />
              </marker>
            </defs>
            <line x1="0" y1="24" x2="100%" y2="24" stroke={attention ? "var(--ink-primary)" : "var(--ink-muted)"} strokeWidth="2" strokeDasharray="6 4" markerEnd="url(#mem-arrow2)" />
          </svg>
          <AnimatePresence>
            {attention && particles.map(i => (
              <motion.div
                key={`p2-${i}`}
                className="absolute top-1/2 -translate-y-1/2 w-3 h-3 rounded-full"
                style={{ backgroundColor: 'var(--ink-primary)' }}
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
            className="rounded-xl border p-3 md:p-4 text-center"
            style={{ borderColor: 'var(--outline-soft)', backgroundColor: 'var(--surface-paper)' }}
            animate={{
              opacity: attention ? 1 : 0.4,
            }}
            transition={{ duration: 0.4 }}
          >
            <p className="t-sub text-ink-primary">Long-Term</p>
            <p className="text-[11px] leading-[14px] text-ink-muted mt-0.5">Permanent</p>
          </motion.div>
        </div>
      </div>

      {/* Status indicator: a line in ink, the tick while information is encoded */}
      <AnswerLine tone={attention ? 'ok' : 'note'}>
        {attention ? 'Information is being encoded into Long-Term Memory' : 'Information is decaying — nothing reaches Long-Term Memory'}
      </AnswerLine>

      <div className="ex-actions">
        <Button onClick={() => setAttention(!attention)} aria-pressed={!!(attention)}>
          {attention ? 'De-Focus' : 'Pay Attention'}
        </Button>
      </div>
    </ExerciseSheet>
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
  const recallTitleId = useId();

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
      <ExerciseSheet title="Results" sub="How did chunking change your recall?" name="ChunkingChallenge">
        {/* The two scores as bars: an ink fill on a hairline track, the score in the readout */}
        <div className="flex flex-col gap-6">
          {/* Unchunked bar */}
          <div>
            <div className="flex justify-between gap-3 mb-2">
              <span className="t-sub text-ink-primary">Unchunked (Random)</span>
              <span className="t-readout text-ink-primary">{scoreR1}/12</span>
            </div>
            <div className="h-2 w-full rounded-full overflow-hidden" style={{ backgroundColor: 'var(--hairline)' }}>
              <MotionDiv
                initial={{ width: 0 }}
                animate={{ width: `${(scoreR1 / maxBar) * 100}%` }}
                transition={{ duration: 0.8, ease: 'easeOut' }}
                className="h-full rounded-full"
                style={{ backgroundColor: 'var(--ink-primary)' }}
              />
            </div>
          </div>

          {/* Chunked bar */}
          <div>
            <div className="flex justify-between gap-3 mb-2">
              <span className="t-sub text-ink-primary">Chunked (Acronyms)</span>
              <span className="t-readout text-ink-primary">{scoreR2}/12</span>
            </div>
            <div className="h-2 w-full rounded-full overflow-hidden" style={{ backgroundColor: 'var(--hairline)' }}>
              <MotionDiv
                initial={{ width: 0 }}
                animate={{ width: `${(scoreR2 / maxBar) * 100}%` }}
                transition={{ duration: 0.8, ease: 'easeOut', delay: 0.3 }}
                className="h-full rounded-full"
                style={{ backgroundColor: 'var(--ink-primary)' }}
              />
            </div>
          </div>
        </div>

        {/* What it shows: a line in ink, not a panel */}
        <AnswerLine>
          <strong>Same number of letters.</strong> But grouping them turned 12 random items into 4 familiar acronyms — easy for your brain to hold. This is why organising information into meaningful groups makes such a huge difference when you're studying.
        </AnswerLine>

        <div className="ex-actions">
          <TextButton tone="quiet" onClick={handleReset}>
            Try Again
          </TextButton>
        </div>
      </ExerciseSheet>
    );
  }

  // --- Idle: prompt to start ---
  if (phase === 'idle') {
    return (
      <ExerciseSheet title="The Chunking Challenge" sub="Can you memorise 12 letters in 5 seconds? Two rounds will show you the power of chunking." name="ChunkingChallenge">
        <div className="ex-actions">
          <Button onClick={handleStartRound1}>
            Start Round 1
          </Button>
        </div>
      </ExerciseSheet>
    );
  }

  // --- Memorise phase ---
  if (phase === 'memorise') {
    return (
      <ExerciseSheet title={round === 1 ? 'Round 1: Random Letters' : 'Round 2: Chunked Letters'} sub="Memorise these letters!" name="ChunkingChallenge">
        {/* The letters, set large in ink on the sheet; the countdown in a neutral ring */}
        <MotionDiv
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-3xl md:text-4xl tracking-widest text-ink-primary text-center py-4"
        >
          {displayLetters()}
        </MotionDiv>

        <div className="flex justify-center">
          <span className="inline-flex items-center justify-center w-14 h-14 rounded-full text-ink-primary text-2xl" style={{ border: '1.5px solid var(--outline-soft)' }}>
            {countdown}
          </span>
        </div>
      </ExerciseSheet>
    );
  }

  // --- Recall phase ---
  if (phase === 'recall') {
    return (
      <ExerciseSheet title={round === 1 ? 'Round 1: Recall' : 'Round 2: Recall'} sub="Type the 12 letters you saw (no spaces needed)." name="ChunkingChallenge" id={recallTitleId}>
        <Field
          aria-labelledby={recallTitleId}
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="e.g. XKMBRF..."
          maxLength={24}
          autoFocus
          className="w-full max-w-sm mx-auto [&_input]:text-center [&_input]:tracking-widest"
        />
        <div className="ex-actions">
          <Button
            onClick={handleSubmit}
            {...{ disabled: input.trim().length === 0 }}
            className="disabled:opacity-40"
          >
            Submit
          </Button>
        </div>
      </ExerciseSheet>
    );
  }

  // --- Scored (between rounds) ---
  if (phase === 'scored' && round === 1) {
    return (
      <ExerciseSheet title="Round 1 Score" name="ChunkingChallenge">
        {/* The score, said under a hairline */}
        <div className="ex-result">
          <p className="ex-result-name">{scoreR1}/12</p>
          <p className="ex-sub">Now let's try the same task — but with chunked letters.</p>
        </div>
        <div className="ex-actions">
          <Button onClick={handleStartRound2}>
            Start Round 2
          </Button>
        </div>
      </ExerciseSheet>
    );
  }

  return null;
};

const WorkingMemorySimulator = () => {
  const [items, setItems] = useState<string[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [showItems, setShowItems] = useState(false);
  const [result, setResult] = useState<number|null>(null);
  const testTitleId = useId();

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
      <ExerciseSheet title="Results" name="WorkingMemorySimulator">
        <AnswerLine tone={result === items.length ? 'ok' : 'note'}>You correctly recalled {result} out of {items.length} items.</AnswerLine>
        <p className="t-meta">The original items were: {items.join(', ')}</p>
        <div className="ex-actions">
          <TextButton tone="quiet" onClick={startGame}>Try Again</TextButton>
        </div>
      </ExerciseSheet>
    );
  }

  return (
    <ExerciseSheet title="Short-Term Memory Test" name="WorkingMemorySimulator" id={testTitleId}>
      {!showItems && items.length === 0 && <div className="ex-actions"><Button onClick={startGame}>Start</Button></div>}

      {showItems && <p className="text-3xl tracking-widest text-ink-primary text-center">{items.join(' ')}</p>}

      {!showItems && items.length > 0 &&
        <div className="ex-stack">
          <Field aria-labelledby={testTitleId} value={inputValue} onChange={e => setInputValue(e.target.value)} placeholder="Type the numbers, separated by spaces" />
          <div className="ex-actions">
            <Button onClick={checkAnswer}>Check Answer</Button>
          </div>
        </div>
      }
    </ExerciseSheet>
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
    <ModuleLayout moduleNumber="04" moduleTitle="How Your Memory Works" moduleSubtitle="Your Brain's User Manual" moduleDescription="Learn how your memory actually works — how information gets in, why most of it falls out, and what you can do to make the important stuff stick when it counts." theme={theme} sections={sections} onBack={onBack} progress={progress} onProgressUpdate={onProgressUpdate} finishButtonText="Map Your Memory" references={HOW_MEMORY_WORKS_REFERENCE_LIST}>
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Your Three Types of Memory." eyebrow="Step 1" icon={Server} theme={theme}>
              {essentials ? (
                <>
                  <p>Your memory works in three stages. First, <strong>Sensory Memory</strong> catches a quick flash of what you see or hear.<Cite n={1} /> If you pay attention, it moves to <strong>Short-Term Memory</strong> -- your mental workbench. From there, you need to deliberately move it into <strong>Long-Term Memory</strong> -- the permanent store.</p>
                  <p>Your whole job as a student is getting better at moving information from that workbench into long-term storage. That is what good study techniques help you do.</p>
                </>
              ) : (
                <>
                  <p>To do well in school, it really helps to understand how the machine you're working with — your own brain — actually handles information. The simplest way to think about it is that your memory has <Highlight description="A simple way of understanding memory: it comes in three stages — a quick flash, a short holding space, and a long-term store." theme={theme}>three stages</Highlight>.<Cite n={1} /></p>
                  <p>First, there's <Highlight description="The very first stage of memory — a split-second snapshot of what you see or hear. If you don't pay attention to it, it's gone instantly." theme={theme}>Sensory Memory</Highlight>, the brief flash of what you see or hear. Anything you don't pay attention to here is gone forever. If you <em>do</em> pay attention, it moves to <Highlight description="Your brain's temporary holding space. It can only hold a small amount of information for a short time — think of it as your mental workbench." theme={theme}>Short-Term Memory</Highlight>, your brain's mental workbench. From there, it has to be deliberately moved to <Highlight description="Your brain's permanent storage. This is where knowledge needs to end up if you want to remember it in an exam." theme={theme}>Long-Term Memory</Highlight>, the permanent hard drive. Your entire job as a student is to get better at moving stuff from that workbench into long-term storage.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Why Your Brain Gets Overloaded." eyebrow="Step 2" icon={Filter} theme={theme}>
              {essentials ? (
                <>
                  <p>Your short-term memory can only hold about <strong>4 chunks</strong> at once.<Cite n={2} /><Cite n={3} /> Without active effort, information fades in 15-30 seconds.<Cite n={4} /> This is why you can read a page and remember nothing.</p>
                  <p>Cramming jams this bottleneck. It creates memories that feel strong but vanish quickly. You need strategies that move information into long-term storage instead.</p>
                </>
              ) : (
                <>
                  <p>Your Short-Term Memory — the part of your brain that <Highlight description="The part of your brain that holds and works with information right now. Think of it as your mental desk — it can only fit a few things on it at once." theme={theme}>holds and works with information right now</Highlight> — is the biggest bottleneck in your learning. It's shockingly limited. You might think you can juggle loads of info, but realistically your brain can only hold about <strong>4 chunks of information</strong> at a time when dealing with complex schoolwork.<Cite n={2} /><Cite n={3} /></p>
                  <p>Even worse, without active effort, this information fades in about <strong>15-30 seconds</strong>.<Cite n={4} /> This is why you can read a whole page of a textbook and have no memory of it. The information landed on your mental desk but disappeared before it could be saved anywhere. Cramming jams this bottleneck, creating a memory that feels strong but vanishes quickly.</p>
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
                  <p>Your long-term memory has three types. <strong>Fact memory</strong> stores definitions and dates. <strong>Experience memory</strong> stores things that happened to you. <strong>Skill memory</strong> stores how-to knowledge.<Cite n={5} /></p>
                  <p>For many subjects, skill memory matters most. Maths is not about memorising facts. It is about practising steps until they become automatic. Study the type that matches your subject.</p>
                </>
              ) : (
                <>
                  <p>Your Long-Term Memory isn't one big box; it's more like a filing cabinet with different drawers for different types of knowledge. Knowing which drawer you're using helps you study smarter.</p>
                  <p>The first drawer is <Highlight description="Your store of facts and general knowledge — things like Biology definitions, History dates, or what the capital of France is." theme={theme}>fact memory</Highlight> — your library of facts and definitions. The second is <Highlight description="Your store of personal experiences — like remembering a specific Chemistry experiment or what happened in class last Tuesday." theme={theme}>experience memory</Highlight> — your personal collection of things that happened to you. The third, and most important for many subjects, is <Highlight description="Your store of skills and 'how-to' knowledge — like how to solve a Maths equation or conjugate a French verb. It's muscle memory for your brain." theme={theme}>skill memory</Highlight>. Maths isn't about memorising facts; it's about practising steps until they become automatic.<Cite n={5} /></p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="How to Actually Save What You Learn." eyebrow="Step 4" icon={BrainCircuit} theme={theme}>
              {essentials ? (
                <>
                  <p>Moving information into long-term memory is called <strong>encoding</strong>. Re-reading creates weak memories. Connecting new information to what you already know creates strong ones.<Cite n={6} /></p>
                  <p>Deep studying means thinking about what something means. Your brain cells physically strengthen their connections the more you use them. Use a pathway often and it becomes automatic.</p>
                </>
              ) : (
                <>
                  <p>Moving information from your temporary workbench to your permanent hard drive is called <Highlight description="The process of turning a temporary memory into a lasting one. How deeply you think about something decides how well you'll remember it." theme={theme}>encoding</Highlight> — basically, hitting the 'save' button. But not all saving is equal. <Highlight description="When you only skim the surface of something — like re-reading a definition without really thinking about it. This creates weak memories that fade fast." theme={theme}>Surface-level studying</Highlight>, like just re-reading a definition, creates weak, flimsy memories.<Cite n={6} /></p>
                  <p><Highlight description="When you really think about what something means and connect it to things you already know. This creates strong memories that last." theme={theme}>Deep studying</Highlight> is about connecting new information to what you already know. For example, learning that "mitochondria is the powerhouse of the cell" is surface-level. Understanding <em>how</em> it produces energy and why that's essential for your muscles to work is deep. What's actually happening in your brain is that <Highlight description="When brain cells fire together repeatedly, the connections between them get physically stronger — like a path getting worn into a field the more you walk it." theme={theme}>the connections between your brain cells get physically stronger</Highlight> — the more you use a pathway, the easier it becomes to use again.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Why Sleep Is Non-Negotiable." eyebrow="Step 5" icon={Moon} theme={theme}>
              {essentials ? (
                <>
                  <p>Your brain saves what you learned during deep sleep. New information sits in a temporary inbox during the day. While you sleep, your brain replays it and moves the important stuff into permanent storage.<Cite n={7} /></p>
                  <p>Pulling an all-nighter cancels this saving process. You need proper sleep for your studying to actually stick.</p>
                </>
              ) : (
                <>
                  <p>Here's something your brain absolutely needs: the final "save" button gets hit while you sleep. During the day, new information sits in a <Highlight description="A small part of your brain that acts like a temporary inbox. Everything you learn during the day lands here first — but it can only hold stuff temporarily." theme={theme}>temporary inbox</Highlight> in your brain. It can hold things for a while, but nothing is permanent yet.</p>
                  <p>During deep sleep, your brain <Highlight description="While you sleep, your brain replays what you learned during the day and moves the important stuff from temporary storage into permanent storage. No sleep = no proper saving." theme={theme}>replays what you learned</Highlight> and moves the important memories from that temporary inbox into permanent storage in the <Highlight description="The outer layer of your brain where long-term memories are permanently stored. Think of it as your brain's hard drive." theme={theme}>main part of your brain</Highlight>.<Cite n={7} /> Pulling an all-nighter is like trying to save a file while constantly hitting 'cancel' on the save dialog. It's self-sabotage.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Your Action Plan." eyebrow="Step 6" icon={ClipboardCheck} theme={theme}>
              {essentials ? (
                <>
                  <p>Good results come from using the right approach, not natural talent. Test yourself, space out your study, and mix topics. These work with how your memory naturally operates.<Cite n={8} /></p>
                  <p>Sleep, food, water, and stress levels directly affect your brain. High stress blocks memory.<Cite n={9} /> Look after yourself -- it is one of the best things you can do for your grades.</p>
                </>
              ) : (
                <>
                  <p>Understanding how your memory works gives you an owner's manual for your own brain. It shows that doing well isn't about "natural talent" — it's about using the right approach. Strategies like testing yourself, spacing out your study, and mixing topics are all just ways to work with how your memory naturally operates.<Cite n={8} /></p>
                  <p>But even the best strategies will fail if you're running on empty. Your <Highlight description="How well your body is doing — your sleep, what you're eating, whether you're drinking enough water, and your stress levels. All of these directly affect how well your brain works." theme={theme}>physical state</Highlight> is the foundation. When you're really stressed, your brain releases <Highlight description="A stress hormone. When it stays high for too long, it actually makes it harder for your brain to store and recall memories." theme={theme}>stress hormones</Highlight> that actually block your ability to remember things.<Cite n={9} /> Dehydration and poor nutrition starve your brain of the resources it needs. Looking after yourself isn't a 'wellness' tip — it's one of the most important things you can do for your grades.</p>
                </>
              )}
              <MicroCommitment theme={theme}>
                <p>Tonight, set an alarm to put your phone away 60 minutes before you go to bed. This single act of 'sleep hygiene' protects the deep sleep your memory relies on to lock in what you studied.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default TheCognitiveArchitectureModule;
