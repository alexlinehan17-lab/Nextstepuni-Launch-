
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import {
  Brain, SlidersHorizontal, Lightbulb, PauseCircle, Zap, Clock
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { purpleTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = purpleTheme;

// --- INTERACTIVE COMPONENTS ---

const FOCUSED_DOTS = Array.from({ length: 25 }, (_, i) => ({ id: `f${i}`, top: 10 + Math.random() * 80, left: 10 + Math.random() * 80 }));
const DIFFUSE_DOTS = Array.from({ length: 8 }, (_, i) => ({ id: `d${i}`, top: 10 + Math.random() * 80, left: 10 + Math.random() * 80 }));

const PinballSimulator = () => {
    const [mode, setMode] = useState<'focused' | 'diffuse'>('focused');
    const isFocused = mode === 'focused';
    return(
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
          <div className="text-center mb-8">
            <span className="inline-block px-3 py-1 rounded-full text-[11px] font-bold tracking-wider uppercase mb-3" style={{ backgroundColor: '#e8f5f2', color: '#1a6358', border: '1px solid rgba(42,125,111,0.2)', letterSpacing: '0.06em' }}>Interactive Simulation</span>
            <h4 className="font-serif font-bold" style={{ fontSize: 24, color: '#1a1a1a' }}>The Pinball Metaphor</h4>
            <p className="text-sm mt-1" style={{ color: '#7a7068' }}>Toggle between modes to see how your thoughts travel.</p>
          </div>

          {/* Canvas */}
          <div className="w-full h-64 relative overflow-hidden" style={{
            backgroundColor: 'white',
            border: '2px solid #1a1a1a',
            borderRadius: 16,
            backgroundImage: 'radial-gradient(circle, #e0dbd4 1px, transparent 1px)',
            backgroundSize: '24px 24px',
            boxShadow: isFocused ? 'inset 0 0 0 3px rgba(42,125,111,0.15)' : 'inset 0 0 0 3px rgba(0,0,0,0.04)',
          }}>
            {/* Mode chip */}
            <div className="absolute top-3 left-3 z-10">
              <span style={{
                fontSize: 9, fontWeight: 700, letterSpacing: '0.08em',
                backgroundColor: isFocused ? '#e8f5f2' : '#f0ece6',
                color: isFocused ? '#1a6358' : '#9e9186',
                border: isFocused ? '1px solid rgba(42,125,111,0.2)' : '1px solid #d0cdc8',
                borderRadius: 20, padding: '2px 8px',
                textTransform: 'uppercase' as const,
              }}>
                {isFocused ? 'Focused' : 'Diffuse'}
              </span>
            </div>

            <AnimatePresence>
              {isFocused && FOCUSED_DOTS.map(d => (
                <motion.div
                  key={d.id}
                  initial={{ opacity: 0, scale: 0 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0 }}
                  className="absolute rounded-full"
                  style={{ width: 12, height: 12, backgroundColor: '#2A7D6F', border: '1.5px solid #1a5a4e', top: `${d.top}%`, left: `${d.left}%` }}
                />
              ))}
              {!isFocused && DIFFUSE_DOTS.map(d => (
                <motion.div
                  key={d.id}
                  initial={{ opacity: 0, scale: 0 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0 }}
                  className="absolute rounded-full"
                  style={{ width: 16, height: 16, backgroundColor: '#9e9186', border: '1px solid #7a7068', top: `${d.top}%`, left: `${d.left}%` }}
                />
              ))}
            </AnimatePresence>
          </div>

          {/* Toggle buttons */}
          <div className="flex justify-center gap-3 mt-6">
            <button onClick={() => setMode('focused')} style={{
              backgroundColor: isFocused ? '#2A7D6F' : '#FFFFFF',
              border: isFocused ? '2px solid #2A7D6F' : '2px solid #d0cdc8',
              borderRadius: 20, padding: '12px 24px',
              fontSize: 14, fontWeight: 600,
              color: isFocused ? '#FFFFFF' : '#7a7068',
              cursor: 'pointer',
            }}>
              Focused Mode
            </button>
            <button onClick={() => setMode('diffuse')} style={{
              backgroundColor: !isFocused ? '#2A7D6F' : '#FFFFFF',
              border: !isFocused ? '2px solid #2A7D6F' : '2px solid #d0cdc8',
              borderRadius: 20, padding: '12px 24px',
              fontSize: 14, fontWeight: 600,
              color: !isFocused ? '#FFFFFF' : '#7a7068',
              cursor: 'pointer',
            }}>
              Diffuse Mode
            </button>
          </div>

          {/* Insight callout */}
          <motion.div
            key={mode}
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4"
            style={isFocused
              ? { borderLeft: '3px solid #2A7D6F', backgroundColor: '#f0faf8', borderRadius: '0 10px 10px 0', padding: '12px 16px' }
              : { borderLeft: '3px solid #d0cdc8', backgroundColor: '#f4f0eb', borderRadius: '0 10px 10px 0', padding: '12px 16px' }
            }
          >
            <p className="text-sm italic" style={{ color: isFocused ? '#1a6358' : '#7a7068' }}>
              {isFocused
                ? 'Focused mode: thoughts bounce between closely connected ideas. Great for execution and problem-solving.'
                : 'Diffuse mode: thoughts roam freely. This is where creative connections and insight happen.'}
            </p>
          </motion.div>
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
  const wrongAttemptTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => {
      if (wrongAttemptTimerRef.current) clearTimeout(wrongAttemptTimerRef.current);
    };
  }, []);

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
      wrongAttemptTimerRef.current = setTimeout(() => setWrongAttempt(false), 1200);
    }
  };

  const handleReturnCheck = () => {
    const trimmed = input.trim().toUpperCase();
    if (trimmed === puzzle.answer) {
      setPhase('results');
    } else {
      setReturnAttempts(prev => prev + 1);
      setWrongAttempt(true);
      wrongAttemptTimerRef.current = setTimeout(() => setWrongAttempt(false), 1200);
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



  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      <div className="text-center mb-8">
        <span className="inline-block px-3 py-1 rounded-full text-[11px] font-bold tracking-wider uppercase mb-3" style={{ backgroundColor: '#e8f5f2', color: '#1a6358', border: '1px solid rgba(42,125,111,0.2)', letterSpacing: '0.06em' }}>Interactive Experiment</span>
        <h4 className="font-serif font-bold" style={{ fontSize: 24, color: '#1a1a1a' }}>The Incubation Effect</h4>
        <p className="text-sm mt-1" style={{ color: '#7a7068' }}>Experience how stepping away unlocks fresh insight.</p>
      </div>

      <AnimatePresence mode="wait">
        {/* FOCUSED MODE */}
        {phase === 'focused' && (
          <MotionDiv key="focused" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }} transition={{ duration: 0.4 }}>
            <div className="bg-white dark:bg-zinc-900" style={{ border: '2px solid #1a1a1a', borderRadius: 16, padding: 24 }}>
              <div className="flex items-center justify-between mb-4">
                <span style={{ fontSize: 11, fontWeight: 700, letterSpacing: '0.12em', backgroundColor: '#e8f5f2', color: '#1a6358', border: '1px solid rgba(42,125,111,0.2)', borderRadius: 20, padding: '3px 10px', textTransform: 'uppercase' as const }}>Focused Mode</span>
                <span style={{ fontSize: 13, fontWeight: 600, backgroundColor: focusedTime >= 25 ? '#fde4e4' : '#f0ece6', color: focusedTime >= 25 ? '#b33030' : '#5a5550', border: `1.5px solid ${focusedTime >= 25 ? 'rgba(227,93,117,0.3)' : '#d0cdc8'}`, borderRadius: 20, padding: '4px 12px' }}>{focusedTime}s</span>
              </div>
              <p style={{ fontSize: 15, color: '#5a5550', marginBottom: 16 }}>Rearrange these letters to form a common English word:</p>
              <div className="flex justify-center gap-2 mb-6 flex-wrap">
                {puzzle.letters.split('').map((letter, i) => (
                  <MotionDiv key={`${puzzleIndex}-${i}`} initial={{ scale: 0, rotateY: 180 }} animate={{ scale: 1, rotateY: 0 }} transition={{ delay: i * 0.08, type: 'spring', stiffness: 300, damping: 20 }} className="flex items-center justify-center bg-white dark:bg-zinc-800" style={{ width: 52, height: 52, border: '2px solid #1a1a1a', borderRadius: 10 }}>
                    <span className="font-serif font-bold" style={{ fontSize: 22, color: '#1a1a1a' }}>{letter}</span>
                  </MotionDiv>
                ))}
              </div>
              <div className="flex flex-col sm:flex-row gap-3 items-center justify-center">
                <input type="text" value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && handleCheck()} placeholder="Type your answer..." className="w-full sm:w-48 outline-none text-center" style={{ backgroundColor: '#FFFFFF', border: '1.5px solid #d0d8d4', borderRadius: 10, padding: '12px 16px', fontSize: 15, color: '#1a1a1a' }} onFocus={(e) => { e.currentTarget.style.borderColor = '#2A7D6F'; }} onBlur={(e) => { e.currentTarget.style.borderColor = '#d0d8d4'; }} />
                <button onClick={handleCheck} style={{ backgroundColor: '#2A7D6F', borderRadius: 20, padding: '12px 24px', fontSize: 14, fontWeight: 600, color: '#FFFFFF' }}>Check Answer</button>
              </div>
              {wrongAttempt && (
                <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center mt-3" style={{ fontSize: 14, color: '#E85D75', fontWeight: 500 }}>Not quite. Keep trying!</MotionDiv>
              )}
              {showStuckPrompt && (
                <MotionDiv initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-6" style={{ borderLeft: '3px solid #2A7D6F', backgroundColor: '#f0faf8', borderRadius: '0 10px 10px 0', padding: '16px 20px', textAlign: 'center' }}>
                  <p className="italic mb-3" style={{ fontSize: 14, color: '#1a6358' }}>Stuck? Your focused mode has hit a wall.</p>
                  <motion.button onClick={handleDiffuseBreak} whileTap={{ y: 3 }} className="text-white font-semibold" style={{ backgroundColor: '#2A7D6F', borderRadius: 100, padding: '13px 28px', fontSize: 15, borderBottom: '3px solid #1a5a4e', boxShadow: '0 4px 0 #1a5a4e' }}>Take a Diffuse Break</motion.button>
                </MotionDiv>
              )}
            </div>
          </MotionDiv>
        )}

        {/* DIFFUSE BREAK */}
        {phase === 'diffuse' && (
          <MotionDiv key="diffuse" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }} transition={{ duration: 0.5 }}>
            <div className="bg-white dark:bg-zinc-900 text-center" style={{ border: '2px solid #1a1a1a', borderRadius: 16, padding: '32px 28px' }}>
              <div className="flex items-center justify-center mb-5" style={{ width: 80, height: 80, borderRadius: '50%', backgroundColor: '#e8f5f2', border: '2px solid rgba(42,125,111,0.25)', margin: '0 auto' }}>
                <span className="font-serif font-bold" style={{ fontSize: 36, color: '#2A7D6F' }}>{diffuseTime}</span>
              </div>
              {/* Progress bar */}
              <div className="mx-auto mb-5" style={{ height: 4, backgroundColor: '#e0dbd4', borderRadius: 2, maxWidth: 200 }}>
                <div style={{ height: '100%', backgroundColor: '#2A7D6F', borderRadius: 2, width: `${(diffuseTime / 15) * 100}%`, transition: 'width 1s linear' }} />
              </div>
              <p className="font-serif font-semibold" style={{ fontSize: 22, color: '#1a1a1a', marginBottom: 4 }}>Let your mind wander...</p>
              <p style={{ fontSize: 15, color: '#7a7068', marginBottom: 24 }}>Your subconscious is still working on it.</p>
              <MotionDiv key={activeFact} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }} style={{ backgroundColor: '#f4f0eb', border: '1.5px solid #d0cdc8', borderRadius: 12, padding: '16px 20px', maxWidth: 340, margin: '0 auto' }}>
                <p style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.1em', color: '#9e9186', marginBottom: 6, textTransform: 'uppercase' as const }}>Fun Fact</p>
                <p style={{ fontSize: 15, color: '#3a3530' }}>{FUN_FACTS[activeFact]}</p>
              </MotionDiv>
            </div>
          </MotionDiv>
        )}

        {/* RETURN WITH HINT */}
        {phase === 'return' && (
          <MotionDiv key="return" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }} transition={{ duration: 0.4 }}>
            <div className="bg-white dark:bg-zinc-900" style={{ border: '2px solid #1a1a1a', borderRadius: 16, padding: 24 }}>
              <span className="inline-block mb-4" style={{ fontSize: 11, fontWeight: 700, letterSpacing: '0.12em', backgroundColor: '#e8f5f2', color: '#1a6358', border: '1px solid rgba(42,125,111,0.2)', borderRadius: 20, padding: '3px 10px', textTransform: 'uppercase' as const }}>Back from your break</span>
              <div className="flex justify-center gap-2 mb-4 flex-wrap">
                {puzzle.letters.split('').map((letter, i) => (
                  <MotionDiv key={`r-${puzzleIndex}-${i}`} initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: i * 0.06, type: 'spring', stiffness: 300, damping: 20 }} className="flex items-center justify-center bg-white dark:bg-zinc-800" style={{ width: 52, height: 52, border: '2px solid #1a1a1a', borderRadius: 10 }}>
                    <span className="font-serif font-bold" style={{ fontSize: 22, color: '#1a1a1a' }}>{letter}</span>
                  </MotionDiv>
                ))}
              </div>
              <MotionDiv initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.3 }} className="mb-5 text-center" style={{ borderLeft: '3px solid #2A7D6F', backgroundColor: '#f0faf8', borderRadius: '0 10px 10px 0', padding: '12px 16px' }}>
                <p className="text-sm italic" style={{ color: '#1a6358' }}>Hint: {puzzle.hint}</p>
              </MotionDiv>
              <div className="flex flex-col sm:flex-row gap-3 items-center justify-center">
                <input type="text" value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && handleReturnCheck()} placeholder="Try again..." className="w-full sm:w-48 outline-none text-center" style={{ backgroundColor: '#FFFFFF', border: '1.5px solid #d0d8d4', borderRadius: 10, padding: '12px 16px', fontSize: 15, color: '#1a1a1a' }} onFocus={(e) => { e.currentTarget.style.borderColor = '#2A7D6F'; }} onBlur={(e) => { e.currentTarget.style.borderColor = '#d0d8d4'; }} />
                <button onClick={handleReturnCheck} style={{ backgroundColor: '#2A7D6F', borderRadius: 20, padding: '12px 24px', fontSize: 14, fontWeight: 600, color: '#FFFFFF' }}>Check Answer</button>
              </div>
              {wrongAttempt && !revealAnswer && (
                <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center mt-3" style={{ fontSize: 14, color: '#E85D75', fontWeight: 500 }}>Not quite. Try once more!</MotionDiv>
              )}
              {revealAnswer && (
                <MotionDiv initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-4 text-center">
                  <p style={{ fontSize: 14, color: '#7a7068', marginBottom: 4 }}>The answer was:</p>
                  <p className="font-serif font-bold" style={{ fontSize: 28, color: '#2A7D6F', marginBottom: 12 }}>{puzzle.answer}</p>
                  <button onClick={() => setPhase('results')} style={{ backgroundColor: '#2A7D6F', borderRadius: 20, padding: '12px 24px', fontSize: 14, fontWeight: 600, color: '#FFFFFF' }}>See the Science</button>
                </MotionDiv>
              )}
            </div>
          </MotionDiv>
        )}

        {/* RESULTS */}
        {phase === 'results' && (
          <MotionDiv key="results" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }} transition={{ duration: 0.4 }}>
            <div className="bg-white dark:bg-zinc-900 text-center" style={{ border: '2px solid #1a1a1a', borderRadius: 16, padding: '28px 24px' }}>
              <MotionDiv initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: 'spring', stiffness: 200, damping: 15 }} className="mb-4">
                <div className="mx-auto flex items-center justify-center" style={{ width: 56, height: 56, borderRadius: '50%', backgroundColor: '#e8f5f2', border: '2px solid rgba(42,125,111,0.25)' }}>
                  <Lightbulb style={{ width: 28, height: 28, color: '#2A7D6F' }} />
                </div>
              </MotionDiv>
              <h5 className="font-serif font-semibold mb-3" style={{ fontSize: 20, color: '#1a1a1a' }}>This is the Incubation Effect in action.</h5>
              <div className="max-w-md mx-auto space-y-3 mb-6">
                <p style={{ fontSize: 14, color: '#5a5550' }}>Your focused brain locked onto wrong patterns. The diffuse break let your subconscious restructure the problem — making the hint click instantly.</p>
                <p className="font-semibold" style={{ fontSize: 14, color: '#2A7D6F' }}>Stepping away from a hard problem is not laziness. It's strategy.</p>
              </div>
              <button onClick={handleTryAnother} style={{ backgroundColor: '#2A7D6F', borderRadius: 20, padding: '12px 24px', fontSize: 14, fontWeight: 600, color: '#FFFFFF' }}>Try Another Puzzle</button>
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
    { id: 'two-modes', title: 'Your Brain Has Two Gears', eyebrow: '01 // The Big Idea', icon: Brain },
    { id: 'focused-engine', title: 'Gear One: Laser Focus', eyebrow: '02 // Locking In', icon: Zap },
    { id: 'diffuse-network', title: 'Gear Two: The Wandering Mind', eyebrow: '03 // Letting Go', icon: Lightbulb },
    { id: 'toggling', title: 'Switching Between Gears', eyebrow: '04 // The Art of the Break', icon: PauseCircle },
    { id: 'procrastination-link', title: 'Why We Put Things Off', eyebrow: '05 // Why We Delay', icon: Clock },
    { id: 'blueprint', title: 'Your Two-Gear Game Plan', eyebrow: '06 // Your Action Plan', icon: SlidersHorizontal },
  ];

  return (
    <ModuleLayout
      moduleNumber="08"
      moduleTitle="The Bimodal Brain"
      moduleSubtitle="The Bimodal Brain"
      moduleDescription="Your brain has two modes — one for grinding through problems, one for creative breakthroughs. Learning when to switch between them is a game-changer for your study."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Switch Your Mode"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Your Brain Has Two Gears." eyebrow="Step 1" icon={Brain} theme={theme}>
              <p>Here's something most people never get told: your brain doesn't just think one way — it has two completely different modes. <Highlight description="When you're fully locked in on something — like working through a maths problem step by step. Your brain is zoomed in and focused on the details." theme={theme}>Focused Mode</Highlight> is your "head down, get it done" gear. It's what kicks in when you're working through a maths problem you know how to solve. Then there's <Highlight description="When your mind is relaxed and wandering — like daydreaming in the shower. Your brain is making connections in the background that you'd never spot while concentrating hard." theme={theme}>Diffuse Mode</Highlight> — your "chill out and let ideas come to you" gear. It's that relaxed, mind-wandering state where your brain quietly connects dots you didn't even know were there.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Gear One: Laser Focus." eyebrow="Step 2" icon={Zap} theme={theme}>
                <p>Think of Focused Mode like a pinball machine with tightly packed bumpers. Your thoughts bounce around in a small area, working through something familiar step by step. This is the gear you need for practising equations in Maths or balancing reactions in Chemistry — anything where you're following a method you've already learned. It's the mode you're in during a focused study sprint. But here's the catch: if you hit a wall on something new or tricky, this mode can actually work against you. Your thoughts just keep bouncing off the same spots, and you end up more frustrated than when you started.</p>
                <PinballSimulator />
            </ReadingSection>
          )}
          {activeSection === 2 && (
             <ReadingSection title="Gear Two: The Wandering Mind." eyebrow="Step 3" icon={Lightbulb} theme={theme}>
                <p>Now picture the pinball machine with the bumpers spread way apart. Your thoughts can travel across your whole brain, linking up ideas from completely different places — maybe something from History clicks with a Biology concept, or a song lyric helps you remember a formula. This is where those "Aha!" moments come from. The thing is, you can't force it. You just have to create the right conditions — go for a walk, have a shower, stare out the window for a bit. When you stop trying so hard, your brain does some of its best work.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
             <ReadingSection title="Switching Between Gears." eyebrow="Step 4" icon={PauseCircle} theme={theme}>
                <p>This is the real skill: knowing when to switch gears. Grind away in Focused Mode on a tough problem. When you hit a wall, step away on purpose — take a break, go for a walk, do something completely different. Here's what's cool: your brain keeps working on the problem in the background even when you're not thinking about it (this is called the <Highlight description="That thing where the answer just 'pops' into your head after you've walked away from a problem for a while. Your brain was quietly working on it the whole time." theme={theme}>Incubation Effect</Highlight>). When you come back to the problem, the answer often just clicks.</p>
                <IncubationEffectDemo />
                <MicroCommitment theme={theme}><p>The next time you're stuck on a homework problem, don't just push harder. Get up and walk around for 5 minutes. You're not giving up — you're using a different part of your brain.</p></MicroCommitment>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Why We Put Things Off." eyebrow="Step 5" icon={Clock} theme={theme}>
                <p>Ever notice how the hardest part of studying is just... starting? That's because your brain doesn't like the discomfort of switching into Focused Mode for something hard. It feels painful before you begin, so you scroll your phone instead. The trick? Don't tell yourself you need to study for an hour. Just commit to 5 minutes. That's it. Once you're actually going, the pain fades and it's way easier to keep at it. Starting is always the worst bit — once you're in, you're in.</p>
            </ReadingSection>
          )}
          {activeSection === 5 && (
             <ReadingSection title="Your Two-Gear Game Plan." eyebrow="Step 6" icon={SlidersHorizontal} theme={theme}>
                <p>So here's the bottom line: your study sessions need both gears. Blocks of proper, focused work AND real breaks where you actually switch off. Not "I'll check Instagram for a sec" breaks — proper ones. A walk. Some music. Staring at the ceiling. This isn't being lazy; it's how your brain actually learns. Build both into your study routine and you'll get more done in less time than if you just tried to grind for hours straight.</p>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default BimodalBrainModule;
