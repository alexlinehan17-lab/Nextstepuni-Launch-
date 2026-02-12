
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Brain, SlidersHorizontal, Lightbulb, PauseCircle, Zap, Clock
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { purpleTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = purpleTheme;

// --- INTERACTIVE COMPONENTS ---

const PinballSimulator = () => {
    const [mode, setMode] = useState<'focused' | 'diffuse'>('focused');
    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Pinball Metaphor</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Toggle between modes to see how your thoughts travel.</p>
             <div className="w-full h-64 bg-zinc-900 rounded-xl p-4 relative overflow-hidden">
                <AnimatePresence>
                    {mode === 'focused' && [...Array(25)].map((_, i) => <motion.div key={`f${i}`} initial={{opacity:0, scale:0}} animate={{opacity:1, scale:1}} exit={{opacity:0, scale:0}} className="absolute w-4 h-4 bg-purple-400 rounded-full" style={{top: `${10 + Math.random()*80}%`, left: `${10 + Math.random()*80}%`}} />)}
                    {mode === 'diffuse' && [...Array(8)].map((_, i) => <motion.div key={`d${i}`} initial={{opacity:0, scale:0}} animate={{opacity:1, scale:1}} exit={{opacity:0, scale:0}} className="absolute w-4 h-4 bg-purple-400 rounded-full" style={{top: `${10 + Math.random()*80}%`, left: `${10 + Math.random()*80}%`}} />)}
                </AnimatePresence>
             </div>
             <div className="flex justify-center gap-4 mt-6">
                <button onClick={() => setMode('focused')} className="px-4 py-2 bg-purple-100 text-purple-800 rounded-lg">Focused Mode</button>
                <button onClick={() => setMode('diffuse')} className="px-4 py-2 bg-zinc-100 dark:bg-zinc-800 text-zinc-800 dark:text-white rounded-lg">Diffuse Mode</button>
             </div>
        </div>
    );
};

// --- INCUBATION EFFECT DEMO ---

const PUZZLES = [
  { letters: 'CSJUETI', answer: 'JUSTICE', hint: 'It\'s something you find in a courtroom.' },
  { letters: 'ATECRHE', answer: 'TEACHER', hint: 'Found in every school.' },
  { letters: 'LEMPROB', answer: 'PROBLEM', hint: 'What you\'re trying to solve right now.' },
];

const FUN_FACTS = [
  'Octopuses have three hearts.',
  'Honey never spoils.',
  'A group of flamingos is called a "flamboyance."',
];

const IncubationEffectDemo = () => {
  const [puzzleIndex, setPuzzleIndex] = useState(0);
  const [phase, setPhase] = useState<'focused' | 'diffuse' | 'return' | 'results'>('focused');
  const [input, setInput] = useState('');
  const [focusedTime, setFocusedTime] = useState(0);
  const [diffuseTime, setDiffuseTime] = useState(15);
  const [showStuckPrompt, setShowStuckPrompt] = useState(false);
  const [wrongAttempt, setWrongAttempt] = useState(false);
  const [returnAttempts, setReturnAttempts] = useState(0);
  const [revealAnswer, setRevealAnswer] = useState(false);
  const [activeFact, setActiveFact] = useState(0);
  const focusedTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const diffuseTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const factTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const puzzle = PUZZLES[puzzleIndex];

  // Focused mode timer
  useEffect(() => {
    if (phase === 'focused') {
      focusedTimerRef.current = setInterval(() => {
        setFocusedTime(prev => {
          if (prev >= 29) {
            setShowStuckPrompt(true);
          }
          return prev + 1;
        });
      }, 1000);
    }
    return () => {
      if (focusedTimerRef.current) clearInterval(focusedTimerRef.current);
    };
  }, [phase]);

  // Diffuse mode countdown
  useEffect(() => {
    if (phase === 'diffuse') {
      setDiffuseTime(15);
      setActiveFact(0);
      diffuseTimerRef.current = setInterval(() => {
        setDiffuseTime(prev => {
          if (prev <= 1) {
            if (diffuseTimerRef.current) clearInterval(diffuseTimerRef.current);
            setPhase('return');
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
      factTimerRef.current = setInterval(() => {
        setActiveFact(prev => (prev + 1) % FUN_FACTS.length);
      }, 5000);
    }
    return () => {
      if (diffuseTimerRef.current) clearInterval(diffuseTimerRef.current);
      if (factTimerRef.current) clearInterval(factTimerRef.current);
    };
  }, [phase]);

  const handleCheck = () => {
    const trimmed = input.trim().toUpperCase();
    if (trimmed === puzzle.answer) {
      setPhase('results');
    } else {
      setWrongAttempt(true);
      setShowStuckPrompt(true);
      setTimeout(() => setWrongAttempt(false), 1200);
    }
  };

  const handleReturnCheck = () => {
    const trimmed = input.trim().toUpperCase();
    if (trimmed === puzzle.answer) {
      setPhase('results');
    } else {
      setReturnAttempts(prev => prev + 1);
      setWrongAttempt(true);
      setTimeout(() => setWrongAttempt(false), 1200);
      if (returnAttempts >= 1) {
        setRevealAnswer(true);
      }
    }
  };

  const handleTryAnother = () => {
    setPuzzleIndex(prev => (prev + 1) % PUZZLES.length);
    setPhase('focused');
    setInput('');
    setFocusedTime(0);
    setDiffuseTime(15);
    setShowStuckPrompt(false);
    setWrongAttempt(false);
    setReturnAttempts(0);
    setRevealAnswer(false);
    setActiveFact(0);
  };

  const handleDiffuseBreak = () => {
    setInput('');
    setPhase('diffuse');
  };

  const MotionDiv = motion.div as any;

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Incubation Effect</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Experience how stepping away unlocks fresh insight.</p>

      <AnimatePresence mode="wait">
        {/* PHASE 1: FOCUSED MODE */}
        {phase === 'focused' && (
          <MotionDiv
            key="focused"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.4 }}
          >
            <div className="bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800 rounded-xl p-6">
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-semibold uppercase tracking-widest text-blue-600 dark:text-blue-400">Focused Mode</span>
                <span className="font-mono text-sm text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-900/50 px-3 py-1 rounded-full">{focusedTime}s</span>
              </div>
              <p className="text-zinc-700 dark:text-zinc-300 mb-4 text-sm">Rearrange these letters to form a common English word:</p>
              <div className="flex justify-center gap-2 mb-6 flex-wrap">
                {puzzle.letters.split('').map((letter, i) => (
                  <MotionDiv
                    key={`${puzzleIndex}-${i}`}
                    initial={{ scale: 0, rotateY: 180 }}
                    animate={{ scale: 1, rotateY: 0 }}
                    transition={{ delay: i * 0.08, type: 'spring', stiffness: 300, damping: 20 }}
                    className="w-12 h-12 bg-white dark:bg-zinc-700 border-2 border-blue-300 dark:border-blue-600 rounded-lg flex items-center justify-center text-xl font-bold text-zinc-800 dark:text-white shadow-sm"
                  >
                    {letter}
                  </MotionDiv>
                ))}
              </div>
              <div className="flex flex-col sm:flex-row gap-3 items-center justify-center">
                <input
                  type="text"
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && handleCheck()}
                  placeholder="Type your answer..."
                  className="w-full sm:w-48 px-4 py-2 rounded-lg border border-zinc-300 dark:border-zinc-600 bg-white dark:bg-zinc-700 text-zinc-800 dark:text-white text-center focus:outline-none focus:ring-2 focus:ring-blue-400"
                />
                <button
                  onClick={handleCheck}
                  className="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors"
                >
                  Check Answer
                </button>
              </div>
              {wrongAttempt && (
                <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center mt-3 text-red-500 dark:text-red-400 text-sm font-medium">
                  Not quite. Keep trying!
                </MotionDiv>
              )}
              {showStuckPrompt && (
                <MotionDiv
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="mt-6 p-4 bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800 rounded-lg text-center"
                >
                  <p className="text-amber-800 dark:text-amber-300 text-sm font-medium mb-3">Stuck? Your focused mode has hit a wall.</p>
                  <button
                    onClick={handleDiffuseBreak}
                    className="px-5 py-2 bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium rounded-lg transition-colors"
                  >
                    Take a Diffuse Break
                  </button>
                </MotionDiv>
              )}
            </div>
          </MotionDiv>
        )}

        {/* PHASE 2: DIFFUSE BREAK */}
        {phase === 'diffuse' && (
          <MotionDiv
            key="diffuse"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.5 }}
          >
            <div className="relative bg-gradient-to-br from-purple-100 via-indigo-50 to-violet-100 dark:from-purple-950/40 dark:via-indigo-950/30 dark:to-violet-950/40 border border-purple-200 dark:border-purple-800 rounded-xl p-8 overflow-hidden">
              {/* Floating dots background */}
              {[...Array(6)].map((_, i) => (
                <MotionDiv
                  key={`dot-${i}`}
                  className="absolute w-3 h-3 bg-purple-300/40 dark:bg-purple-500/20 rounded-full"
                  style={{ top: `${15 + i * 14}%`, left: `${10 + i * 15}%` }}
                  animate={{
                    y: [0, -12, 0, 12, 0],
                    x: [0, 8, 0, -8, 0],
                    opacity: [0.3, 0.6, 0.3],
                  }}
                  transition={{
                    duration: 4 + i,
                    repeat: Infinity,
                    ease: 'easeInOut',
                    delay: i * 0.5,
                  }}
                />
              ))}
              <div className="relative z-10 text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-purple-200/60 dark:bg-purple-800/40 mb-4">
                  <span className="font-mono text-2xl font-bold text-purple-700 dark:text-purple-300">{diffuseTime}</span>
                </div>
                <p className="text-purple-800 dark:text-purple-200 font-medium mb-2">Let your mind wander...</p>
                <p className="text-purple-600 dark:text-purple-400 text-sm mb-8">Your subconscious is still working on it.</p>
                <MotionDiv
                  key={activeFact}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.5 }}
                  className="bg-white/60 dark:bg-zinc-800/60 backdrop-blur-sm rounded-lg p-4 max-w-sm mx-auto"
                >
                  <p className="text-xs uppercase tracking-widest text-purple-500 dark:text-purple-400 mb-1">Fun Fact</p>
                  <p className="text-zinc-700 dark:text-zinc-300 text-sm">{FUN_FACTS[activeFact]}</p>
                </MotionDiv>
              </div>
            </div>
          </MotionDiv>
        )}

        {/* PHASE 3: RETURN WITH HINT */}
        {phase === 'return' && (
          <MotionDiv
            key="return"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.4 }}
          >
            <div className="bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800 rounded-xl p-6">
              <span className="text-xs font-semibold uppercase tracking-widest text-blue-600 dark:text-blue-400 mb-4 block">Back from your break</span>
              <div className="flex justify-center gap-2 mb-4 flex-wrap">
                {puzzle.letters.split('').map((letter, i) => (
                  <MotionDiv
                    key={`r-${puzzleIndex}-${i}`}
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: i * 0.06, type: 'spring', stiffness: 300, damping: 20 }}
                    className="w-12 h-12 bg-white dark:bg-zinc-700 border-2 border-blue-300 dark:border-blue-600 rounded-lg flex items-center justify-center text-xl font-bold text-zinc-800 dark:text-white shadow-sm"
                  >
                    {letter}
                  </MotionDiv>
                ))}
              </div>
              <MotionDiv
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.3 }}
                className="bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-700 rounded-lg p-3 mb-5 text-center"
              >
                <p className="text-amber-800 dark:text-amber-300 text-sm font-medium">Hint: {puzzle.hint}</p>
              </MotionDiv>
              <div className="flex flex-col sm:flex-row gap-3 items-center justify-center">
                <input
                  type="text"
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && handleReturnCheck()}
                  placeholder="Try again..."
                  className="w-full sm:w-48 px-4 py-2 rounded-lg border border-zinc-300 dark:border-zinc-600 bg-white dark:bg-zinc-700 text-zinc-800 dark:text-white text-center focus:outline-none focus:ring-2 focus:ring-blue-400"
                />
                <button
                  onClick={handleReturnCheck}
                  className="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors"
                >
                  Check Answer
                </button>
              </div>
              {wrongAttempt && !revealAnswer && (
                <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center mt-3 text-red-500 dark:text-red-400 text-sm font-medium">
                  Not quite. Try once more!
                </MotionDiv>
              )}
              {revealAnswer && (
                <MotionDiv
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="mt-4 text-center"
                >
                  <p className="text-zinc-600 dark:text-zinc-400 text-sm mb-1">The answer was:</p>
                  <p className="text-2xl font-bold text-purple-700 dark:text-purple-300 mb-3">{puzzle.answer}</p>
                  <button
                    onClick={() => setPhase('results')}
                    className="px-5 py-2 bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium rounded-lg transition-colors"
                  >
                    See the Science
                  </button>
                </MotionDiv>
              )}
            </div>
          </MotionDiv>
        )}

        {/* RESULTS PANEL */}
        {phase === 'results' && (
          <MotionDiv
            key="results"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.4 }}
          >
            <div className="bg-gradient-to-br from-purple-50 to-indigo-50 dark:from-purple-950/30 dark:to-indigo-950/30 border border-purple-200 dark:border-purple-800 rounded-xl p-6 text-center">
              <MotionDiv
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: 'spring', stiffness: 200, damping: 15 }}
                className="text-4xl mb-4"
              >
                <Lightbulb className="w-10 h-10 text-purple-600 dark:text-purple-400 mx-auto" />
              </MotionDiv>
              <h5 className="font-serif text-xl font-semibold text-zinc-800 dark:text-white mb-3">This is the Incubation Effect in action.</h5>
              <div className="max-w-md mx-auto space-y-3 mb-6">
                <p className="text-zinc-600 dark:text-zinc-400 text-sm">Your focused brain locked onto wrong patterns. The diffuse break let your subconscious restructure the problem — making the hint click instantly.</p>
                <p className="text-purple-700 dark:text-purple-300 text-sm font-medium">Stepping away from a hard problem is not laziness. It's strategy.</p>
              </div>
              <button
                onClick={handleTryAnother}
                className="px-5 py-2 bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium rounded-lg transition-colors"
              >
                Try Another Puzzle
              </button>
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
  );
};

// --- MODULE COMPONENT ---
const BimodalBrainModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'two-modes', title: 'The Two Modes of Thinking', eyebrow: '01 // The Discovery', icon: Brain },
    { id: 'focused-engine', title: 'The Focused Engine', eyebrow: '02 // Deep Work', icon: Zap },
    { id: 'diffuse-network', title: 'The Diffuse Network', eyebrow: '03 // Creative Insights', icon: Lightbulb },
    { id: 'toggling', title: 'Toggling the Switch', eyebrow: '04 // The Art of the Break', icon: PauseCircle },
    { id: 'procrastination-link', title: 'The Procrastination Link', eyebrow: '05 // Why We Delay', icon: Clock },
    { id: 'blueprint', title: 'The Bimodal Blueprint', eyebrow: '06 // Your Action Plan', icon: SlidersHorizontal },
  ];

  return (
    <ModuleLayout
      moduleNumber="08"
      moduleTitle="The Bimodal Brain"
      moduleSubtitle="The Bimodal Brain Protocol"
      moduleDescription="Your brain has two gears. Learn to switch between intense focus and creative relaxation to unlock deep learning and solve complex problems."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Two Modes of Thinking." eyebrow="Step 1" icon={Brain} theme={theme}>
              <p>Your brain doesn't have just one mode of thinking; it has two, fundamentally different systems. The <Highlight description="A state of high-attention, analytical thought. It's what you use for solving familiar problems and executing procedures." theme={theme}>Focused Mode</Highlight> is your analytical workhorse. It's a state of intense concentration, perfect for solving a maths problem you already know how to do. The <Highlight description="A relaxed, low-attention state where your brain makes broad connections. It's the source of creative insights and 'Aha!' moments." theme={theme}>Diffuse Mode</Highlight> is your creative wanderer. It's a state of relaxed mind-wandering that allows your brain to make surprising new connections.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Focused Engine." eyebrow="Step 2" icon={Zap} theme={theme}>
                <p>The Focused Mode is like a pinball machine with tightly packed bumpers. Your thoughts bounce around in a small, localized area, working through the details of a problem you understand. This is essential for procedural fluency in subjects like Maths and Chemistry. It's the mode you're in during a Pomodoro sprint. However, if you get stuck on a new or difficult problem, this mode can be a trap. Your thoughts just keep hitting the same bumpers, leading to frustration.</p>
                <PinballSimulator />
            </ReadingSection>
          )}
          {activeSection === 2 && (
             <ReadingSection title="The Diffuse Network." eyebrow="Step 3" icon={Lightbulb} theme={theme}>
                <p>The Diffuse Mode is when the bumpers are far apart. Your thoughts can travel long distances across your brain, connecting ideas from different subjects and experiences. This is where your 'Aha!' moments come from. You can't force this mode; you can only create the conditions for it to emerge. This happens when you relax your focus—by taking a walk, having a shower, or even just staring out the window.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
             <ReadingSection title="Toggling the Switch." eyebrow="Step 4" icon={PauseCircle} theme={theme}>
                <p>The key to effective learning and problem-solving is learning to switch between these two modes. Work intensely in Focused Mode on a hard problem. When you get stuck, deliberately switch to Diffuse Mode by taking a break. Your brain will continue to work on the problem in the background (the <Highlight description="The subconscious processing of a problem that occurs when you are not actively thinking about it." theme={theme}>Incubation Effect</Highlight>). When you return to the problem, the solution will often seem obvious.</p>
                <IncubationEffectDemo />
                <MicroCommitment theme={theme}><p>The next time you're stuck on a homework problem, don't just push harder. Get up and walk around for 5 minutes. You're not giving up; you're using a different part of your brain.</p></MicroCommitment>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Procrastination Link." eyebrow="Step 5" icon={Clock} theme={theme}>
                <p>Procrastination is often caused by the discomfort of entering Focused Mode for a difficult task. The solution is to use a "Diffuse Mode warm-up." Instead of trying to force yourself into a 60-minute focused session, just commit to 5 minutes. This lowers the initial barrier and allows you to ease into the task. The pain of starting is always worse than the pain of continuing.</p>
            </ReadingSection>
          )}
          {activeSection === 5 && (
             <ReadingSection title="The Bimodal Blueprint." eyebrow="Step 6" icon={SlidersHorizontal} theme={theme}>
                <p>You now have the user manual for your brain's two gears. The strategic implication is clear: your study schedule must include both focused work *and* scheduled, unstructured breaks. This is not a luxury; it's a neurobiological necessity for deep learning and creativity.</p>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default BimodalBrainModule;
