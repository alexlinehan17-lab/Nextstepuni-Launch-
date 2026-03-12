
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  MessageCircle, BarChart, Brain, User, AlertTriangle, Settings
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { limeTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = limeTheme;

// --- INTERACTIVE COMPONENTS ---

const DweckExperimentSimulator = () => {
    const [step, setStep] = useState(0); // 0: Start, 1: Praise Choice, 2: Task Choice, 3: Failure, 4: Result
    const [praiseType, setPraiseType] = useState<'person'|'process'|null>(null);
    const [taskChoice, setTaskChoice] = useState<'easy'|'hard'|null>(null);

    const reset = () => {
        setStep(0);
        setPraiseType(null);
        setTaskChoice(null);
    };

    const handlePraise = (type: 'person'|'process') => {
        setPraiseType(type);
        setStep(1);
    };

    const handleTask = (type: 'easy'|'hard') => {
        setTaskChoice(type);
        setStep(2);
        setTimeout(() => setStep(3), 2000); // Auto-advance to failure
        setTimeout(() => setStep(4), 4000); // Auto-advance to result
    };

    let resilience = 50, performance = 50;
    if(praiseType === 'person'){
        if(taskChoice === 'easy') { resilience = 20; performance = 40; }
        if(taskChoice === 'hard') { resilience = 30; performance = 30; }
    }
    if(praiseType === 'process'){
        if(taskChoice === 'easy') { resilience = 70; performance = 60; }
        if(taskChoice === 'hard') { resilience = 90; performance = 80; }
    }


    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Praise Experiment</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">You just aced a test. Walk through this experiment and see what happens next depending on what you're told.</p>

             <div className="grid grid-cols-2 gap-6 mb-8">
                <div className="text-center">
                    <p className="font-bold text-sm text-rose-600 mb-2">Resilience Meter</p>
                    <div className="w-full h-4 bg-zinc-100 dark:bg-zinc-800 rounded-full"><motion.div className="h-full bg-rose-500 rounded-full" initial={{width: "50%"}} animate={{width: `${resilience}%`}} /></div>
                </div>
                <div className="text-center">
                    <p className="font-bold text-sm text-lime-600 mb-2">Performance Meter</p>
                    <div className="w-full h-4 bg-zinc-100 dark:bg-zinc-800 rounded-full"><motion.div className="h-full bg-lime-500 rounded-full" initial={{width: "50%"}} animate={{width: `${performance}%`}} /></div>
                </div>
            </div>

            <AnimatePresence mode="wait">
                <motion.div key={step} initial={{opacity:0, x:20}} animate={{opacity:1, x:0}} exit={{opacity:0, x:-20}} className="text-center">
                    {step === 0 && <>
                        <p className="font-bold mb-4">Phase 1: Choose your praise</p>
                        <div className="grid grid-cols-2 gap-4">
                            <button onClick={() => handlePraise('person')} className="p-4 bg-rose-50 border border-rose-200 rounded-xl">"You must be smart at this."</button>
                            <button onClick={() => handlePraise('process')} className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl">"You must have worked hard at this."</button>
                        </div>
                    </>}
                    {step === 1 && <>
                        <p className="font-bold mb-4">Phase 2: Choose your next task</p>
                         <div className="grid grid-cols-2 gap-4">
                            <button onClick={() => handleTask('easy')} className="p-4 bg-zinc-100 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-xl">An easy one (to look smart)</button>
                            <button onClick={() => handleTask('hard')} className="p-4 bg-zinc-100 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-xl">A hard one (to learn more)</button>
                        </div>
                    </>}
                    {step === 2 && <p className="font-bold text-blue-600">You chose the <span className="underline">{taskChoice}</span> task...</p>}
                    {step === 3 && <p className="font-bold text-rose-600">Phase 3: Induced Failure. You are given a much harder test and perform poorly...</p>}
                    {step === 4 && <>
                        <p className="font-bold text-lime-600 mb-4">Phase 4: Final Results</p>
                        {praiseType === 'person' && <p>Because your identity was tied to being "smart", failure was devastating. Your resilience and subsequent performance dropped.</p>}
                        {praiseType === 'process' && <p>Because your identity was tied to "working hard", the failure was seen as a challenge. Your resilience and subsequent performance increased.</p>}
                        <button onClick={reset} className="mt-4 px-4 py-2 bg-zinc-800 text-white font-bold rounded-lg text-xs">Run Again</button>
                    </>}
                </motion.div>
            </AnimatePresence>
        </div>
    );
};

const ErrorSignalVisualizer = () => {
    const [active, setActive] = useState(false);
    const [showExplainer, setShowExplainer] = useState(false);

    // SVG dimensions
    const W = 400, H = 100;
    const midY = H / 2;
    const errorX = W * 0.35; // where error occurs on timeline

    // Build waveform path: baseline noise → ERN spike (same for both) → Pe response (differs)
    const buildPath = (peAmplitude: number) => {
      const points: string[] = [];
      const step = 2;
      for (let x = 0; x <= W; x += step) {
        let y = midY;
        // Baseline noise (small random-looking sine mix)
        const noise = Math.sin(x * 0.15) * 2 + Math.sin(x * 0.3) * 1.5 + Math.cos(x * 0.08) * 1;
        y += noise;

        if (active) {
          // ERN spike (identical for both) - sharp negative deflection at error point
          const ernDist = x - errorX;
          if (ernDist > 0 && ernDist < 30) {
            const ernT = ernDist / 30;
            const ernWave = Math.sin(ernT * Math.PI) * -22;
            y += ernWave;
          }
          // Pe wave (differs by mindset) - positive deflection after ERN
          const peDist = x - (errorX + 35);
          if (peDist > 0 && peDist < 80) {
            const peT = peDist / 80;
            const peWave = Math.sin(peT * Math.PI) * peAmplitude;
            y += peWave;
          }
        }

        points.push(`${x === 0 ? 'M' : 'L'} ${x} ${y.toFixed(1)}`);
      }
      return points.join(' ');
    };

    const fixedPath = buildPath(8);   // Small Pe
    const growthPath = buildPath(32);  // Large Pe

    const traces = [
      { label: 'Fixed Mindset', path: fixedPath, color: '#f43f5e', peLabel: 'Small Pe', peDesc: 'Brain flinches away to protect your ego', bgClass: 'bg-rose-50 dark:bg-rose-950/20', borderClass: 'border-rose-200 dark:border-rose-800/40', labelClass: 'text-rose-600 dark:text-rose-400' },
      { label: 'Growth Mindset', path: growthPath, color: '#10b981', peLabel: 'Large Pe', peDesc: 'Brain pays close attention to learn from it', bgClass: 'bg-emerald-50 dark:bg-emerald-950/20', borderClass: 'border-emerald-200 dark:border-emerald-800/40', labelClass: 'text-emerald-600 dark:text-emerald-400' },
    ];

    return (
      <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">What Your Brain Does With Mistakes</h4>
        <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">When you make a mistake, your brain fires two signals. The second one is where your mindset makes all the difference.</p>

        <div className="space-y-4">
          {traces.map((trace, i) => (
            <div key={i} className={`p-4 rounded-xl border ${trace.bgClass} ${trace.borderClass}`}>
              <div className="flex items-center justify-between mb-2">
                <p className={`text-xs font-bold uppercase tracking-wider ${trace.labelClass}`}>{trace.label}</p>
                {active && (
                  <motion.p
                    initial={{ opacity: 0, x: 10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.6 }}
                    className={`text-[10px] font-bold ${trace.labelClass}`}
                  >
                    {trace.peLabel} — {trace.peDesc}
                  </motion.p>
                )}
              </div>

              <svg viewBox={`0 0 ${W} ${H}`} className="w-full h-auto" preserveAspectRatio="none">
                {/* Gridlines */}
                {[0.25, 0.5, 0.75].map(t => (
                  <line key={t} x1={0} y1={H * t} x2={W} y2={H * t} stroke="currentColor" className="text-zinc-200 dark:text-zinc-700" strokeWidth="0.5" />
                ))}
                {/* Baseline center */}
                <line x1={0} y1={midY} x2={W} y2={midY} stroke="currentColor" className="text-zinc-300 dark:text-zinc-600" strokeWidth="0.8" strokeDasharray="4 4" />

                {/* Error marker */}
                {active && (
                  <>
                    <motion.line
                      x1={errorX} y1={4} x2={errorX} y2={H - 4}
                      stroke={trace.color}
                      strokeWidth="1"
                      strokeDasharray="3 3"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 0.4 }}
                    />
                    <motion.text
                      x={errorX}
                      y={10}
                      textAnchor="middle"
                      fill={trace.color}
                      className="text-[8px] font-bold"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 0.6 }}
                    >
                      ERROR
                    </motion.text>
                    {/* Pe region shading */}
                    <motion.rect
                      x={errorX + 35}
                      y={2}
                      width={80}
                      height={H - 4}
                      rx={4}
                      fill={trace.color}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 0.06 }}
                      transition={{ delay: 0.4 }}
                    />
                    <motion.text
                      x={errorX + 75}
                      y={H - 6}
                      textAnchor="middle"
                      fill={trace.color}
                      className="text-[7px] font-bold"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 0.5 }}
                      transition={{ delay: 0.5 }}
                    >
                      Pe WINDOW
                    </motion.text>
                  </>
                )}

                {/* Signal trace */}
                <motion.path
                  d={trace.path}
                  fill="none"
                  stroke={trace.color}
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  initial={active ? { pathLength: 0 } : { pathLength: 1 }}
                  animate={{ pathLength: 1 }}
                  transition={{ duration: active ? 1.8 : 0, ease: 'easeOut' }}
                />
              </svg>

              {/* Axis labels */}
              <div className="flex justify-between mt-1">
                <span className="text-[9px] text-zinc-400 dark:text-zinc-500">0 ms</span>
                <span className="text-[9px] text-zinc-400 dark:text-zinc-500">Time</span>
                <span className="text-[9px] text-zinc-400 dark:text-zinc-500">800 ms</span>
              </div>
            </div>
          ))}
        </div>

        {/* Phase legend */}
        {active && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1 }}
            className="mt-4 flex justify-center gap-6"
          >
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-sm bg-zinc-400" />
              <span className="text-[10px] text-zinc-500 dark:text-zinc-400">ERN (Error detected — same for both)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-sm bg-lime-500" />
              <span className="text-[10px] text-zinc-500 dark:text-zinc-400">Pe (Attention to error — differs by mindset)</span>
            </div>
          </motion.div>
        )}

        <div className="flex justify-center gap-3 mt-6">
          <button
            onClick={() => setActive(!active)}
            className="px-6 py-2.5 bg-lime-500 text-white font-bold text-sm rounded-xl hover:bg-lime-600 shadow-lg shadow-lime-500/20 transition-all"
          >
            {active ? 'Reset Signal' : 'Make an Error'}
          </button>
          {active && (
            <motion.button
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              onClick={() => setShowExplainer(!showExplainer)}
              className="px-5 py-2.5 bg-zinc-100 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-300 font-bold text-sm rounded-xl hover:bg-zinc-200 dark:hover:bg-zinc-600 transition-all"
            >
              {showExplainer ? 'Hide Explanation' : 'What am I looking at?'}
            </motion.button>
          )}
        </div>

        <AnimatePresence>
          {showExplainer && active && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="overflow-hidden"
            >
              <div className="mt-6 p-5 bg-zinc-50 dark:bg-zinc-900/50 rounded-xl border border-zinc-200 dark:border-zinc-700 space-y-3">
                <p className="text-sm text-zinc-700 dark:text-zinc-300"><strong>ERN (the first signal)</strong> fires within a tenth of a second of making a mistake. Both mindsets produce the same signal here. Your brain always spots the error.</p>
                <p className="text-sm text-zinc-700 dark:text-zinc-300"><strong>Pe (the second signal)</strong> comes a fraction of a second later. This is where mindset makes the difference. It shows how much <em>attention</em> your brain gives to the mistake.</p>
                <p className="text-sm text-zinc-700 dark:text-zinc-300">A <strong className="text-rose-500">fixed mindset</strong> brain produces a tiny Pe — it spots the error but quickly looks away to protect your ego. A <strong className="text-emerald-500">growth mindset</strong> brain produces a huge Pe — it zooms in on the error, trying to figure out what went wrong so it can do better next time. This is why growth-minded students improve after mistakes while fixed-minded students keep making the same ones.</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    );
};


const MotionDiv = motion.div as any;

type PraiseCategory = 'person' | 'process';

interface PraiseStatement {
  text: string;
  type: PraiseCategory;
  explanation: string;
}

const PRAISE_STATEMENTS: PraiseStatement[] = [
  { text: "\"You're so smart!\"", type: 'person', explanation: 'This praises a fixed trait (intelligence) rather than anything the person did.' },
  { text: "\"You worked really hard on that problem.\"", type: 'process', explanation: 'This praises effort — a controllable, repeatable behaviour.' },
  { text: "\"You're a natural at this.\"", type: 'person', explanation: 'Being a "natural" implies innate ability, not earned skill.' },
  { text: "\"I can see you tried a different strategy this time.\"", type: 'process', explanation: 'This highlights strategic thinking — a learnable process.' },
  { text: "\"You're brilliant.\"", type: 'person', explanation: 'Brilliance is framed as a fixed identity, not an action.' },
  { text: "\"You didn't give up even when it got tough.\"", type: 'process', explanation: 'This praises persistence — a behaviour anyone can choose.' },
  { text: "\"You must be gifted.\"", type: 'person', explanation: '"Gifted" implies a trait you either have or don\'t.' },
  { text: "\"Your practice is really paying off.\"", type: 'process', explanation: 'This links improvement to the process of practising.' },
  { text: "\"You're the best in the class.\"", type: 'person', explanation: 'This ties identity to rank — a fragile, comparative label.' },
  { text: "\"I like how you broke that problem into smaller parts.\"", type: 'process', explanation: 'This praises a specific strategy the student chose to use.' },
  { text: "\"You're a born leader.\"", type: 'person', explanation: '"Born" leader implies leadership is innate, not developed.' },
  { text: "\"You kept going even after making mistakes.\"", type: 'process', explanation: 'This praises resilience in the face of error — pure process.' },
  { text: "\"Some people just have it.\"", type: 'person', explanation: 'This frames ability as something you\'re born with.' },
  { text: "\"That revision technique clearly worked well.\"", type: 'process', explanation: 'This connects success to a specific technique — replicable and strategic.' },
  { text: "\"You're talented.\"", type: 'person', explanation: 'Talent is framed as a fixed trait, not an outcome of effort.' },
  { text: "\"I noticed you asked for help when you were stuck — that's a great strategy.\"", type: 'process', explanation: 'This praises help-seeking as a deliberate, smart strategy.' },
];

function shuffleArray<T>(arr: T[]): T[] {
  const shuffled = [...arr];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

const PraiseDecoderGame = () => {
  const [gameState, setGameState] = useState<'idle' | 'playing' | 'finished'>('idle');
  const [statements, setStatements] = useState<PraiseStatement[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [timeLeft, setTimeLeft] = useState(30);
  const [score, setScore] = useState(0);
  const [totalAnswered, setTotalAnswered] = useState(0);
  const [streak, setStreak] = useState(0);
  const [bestStreak, setBestStreak] = useState(0);
  const [feedback, setFeedback] = useState<'correct' | 'wrong' | null>(null);
  const [wrongExplanation, setWrongExplanation] = useState('');
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const feedbackTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const startGame = () => {
    setStatements(shuffleArray(PRAISE_STATEMENTS));
    setCurrentIndex(0);
    setTimeLeft(30);
    setScore(0);
    setTotalAnswered(0);
    setStreak(0);
    setBestStreak(0);
    setFeedback(null);
    setWrongExplanation('');
    setGameState('playing');
  };

  useEffect(() => {
    if (gameState === 'playing') {
      timerRef.current = setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            if (timerRef.current) clearInterval(timerRef.current);
            setGameState('finished');
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [gameState]);

  const advanceCard = () => {
    setFeedback(null);
    setWrongExplanation('');
    setCurrentIndex((prev) => {
      const next = prev + 1;
      if (next >= statements.length) {
        // Reshuffle and start from beginning if we run out
        setStatements(shuffleArray(PRAISE_STATEMENTS));
        return 0;
      }
      return next;
    });
  };

  const handleAnswer = (answer: PraiseCategory) => {
    if (gameState !== 'playing' || feedback !== null) return;
    const current = statements[currentIndex];
    const isCorrect = answer === current.type;

    setTotalAnswered((prev) => prev + 1);

    if (isCorrect) {
      setScore((prev) => prev + 1);
      setStreak((prev) => {
        const newStreak = prev + 1;
        setBestStreak((best) => Math.max(best, newStreak));
        return newStreak;
      });
      setFeedback('correct');
      if (feedbackTimeoutRef.current) clearTimeout(feedbackTimeoutRef.current);
      feedbackTimeoutRef.current = setTimeout(() => {
        advanceCard();
      }, 400);
    } else {
      setStreak(0);
      setFeedback('wrong');
      setWrongExplanation(current.explanation);
      if (feedbackTimeoutRef.current) clearTimeout(feedbackTimeoutRef.current);
      feedbackTimeoutRef.current = setTimeout(() => {
        advanceCard();
      }, 1200);
    }
  };

  useEffect(() => {
    return () => {
      if (feedbackTimeoutRef.current) clearTimeout(feedbackTimeoutRef.current);
    };
  }, []);

  const accuracy = totalAnswered > 0 ? Math.round((score / totalAnswered) * 100) : 0;
  const currentStatement = statements[currentIndex];

  const timerColor = timeLeft <= 10 ? 'text-rose-500' : timeLeft <= 20 ? 'text-amber-500' : 'text-lime-600 dark:text-lime-400';

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Praise Decoder Game</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">
        Categorise each praise statement as fast as you can. You have 30 seconds.
      </p>

      {gameState === 'idle' && (
        <div className="flex flex-col items-center gap-6">
          <div className="p-6 bg-zinc-50 dark:bg-zinc-900/50 rounded-xl border border-zinc-200 dark:border-zinc-700 max-w-md text-center">
            <p className="text-sm text-zinc-600 dark:text-zinc-300 mb-2">Praise statements will flash on screen. Tap the correct category:</p>
            <div className="flex justify-center gap-3 mt-3">
              <span className="px-3 py-1 text-xs font-bold bg-rose-100 dark:bg-rose-900/30 text-rose-600 dark:text-rose-400 rounded-full">Person Praise</span>
              <span className="px-3 py-1 text-xs font-bold bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 rounded-full">Process Praise</span>
            </div>
          </div>
          <button
            onClick={startGame}
            className="px-8 py-3 bg-lime-500 text-white font-bold text-sm rounded-xl hover:bg-lime-600 shadow-lg shadow-lime-500/20 transition-all"
          >
            Start Game
          </button>
        </div>
      )}

      {gameState === 'playing' && currentStatement && (
        <div className="flex flex-col items-center gap-6">
          {/* Stats row */}
          <div className="flex flex-wrap justify-center gap-3">
            <span className={`px-3 py-1 text-sm font-bold rounded-full bg-zinc-100 dark:bg-zinc-700 ${timerColor}`}>
              {timeLeft}s
            </span>
            <span className="px-3 py-1 text-xs font-bold rounded-full bg-lime-100 dark:bg-lime-900/30 text-lime-700 dark:text-lime-300">
              Score: {score}
            </span>
            <span className="px-3 py-1 text-xs font-bold rounded-full bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300">
              Streak: {streak}
            </span>
            <span className="px-3 py-1 text-xs font-bold rounded-full bg-zinc-100 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-300">
              Accuracy: {accuracy}%
            </span>
          </div>

          {/* Card */}
          <AnimatePresence mode="wait">
            <MotionDiv
              key={currentIndex + '-' + statements[currentIndex]?.text}
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{
                opacity: 1,
                scale: 1,
                y: 0,
                backgroundColor: feedback === 'correct'
                  ? 'rgba(16, 185, 129, 0.1)'
                  : feedback === 'wrong'
                    ? 'rgba(244, 63, 94, 0.1)'
                    : 'rgba(0, 0, 0, 0)',
              }}
              exit={{ opacity: 0, scale: 0.9, y: -20 }}
              transition={{ type: 'spring', stiffness: 300, damping: 25 }}
              className="w-full max-w-lg p-8 rounded-2xl border-2 text-center"
              style={{
                borderColor: feedback === 'correct'
                  ? '#10b981'
                  : feedback === 'wrong'
                    ? '#f43f5e'
                    : '#e4e4e7',
              }}
            >
              <p className="font-serif text-xl md:text-2xl font-medium text-zinc-800 dark:text-white leading-relaxed">
                {currentStatement.text}
              </p>
              {feedback === 'wrong' && wrongExplanation && (
                <motion.p
                  initial={{ opacity: 0, y: 5 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="mt-4 text-sm text-rose-600 dark:text-rose-400 font-medium"
                >
                  {wrongExplanation}
                </motion.p>
              )}
            </MotionDiv>
          </AnimatePresence>

          {/* Buttons */}
          <div className="grid grid-cols-2 gap-4 w-full max-w-lg">
            <button
              onClick={() => handleAnswer('person')}
              disabled={feedback !== null}
              className="px-6 py-4 bg-rose-50 dark:bg-rose-900/20 border-2 border-rose-200 dark:border-rose-800/40 rounded-xl font-bold text-rose-600 dark:text-rose-400 hover:bg-rose-100 dark:hover:bg-rose-900/40 transition-all disabled:opacity-50"
            >
              Person Praise
            </button>
            <button
              onClick={() => handleAnswer('process')}
              disabled={feedback !== null}
              className="px-6 py-4 bg-emerald-50 dark:bg-emerald-900/20 border-2 border-emerald-200 dark:border-emerald-800/40 rounded-xl font-bold text-emerald-600 dark:text-emerald-400 hover:bg-emerald-100 dark:hover:bg-emerald-900/40 transition-all disabled:opacity-50"
            >
              Process Praise
            </button>
          </div>
        </div>
      )}

      {gameState === 'finished' && (
        <MotionDiv
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ type: 'spring', stiffness: 200, damping: 20 }}
          className="flex flex-col items-center gap-6"
        >
          <div className="text-center">
            <p className="text-5xl font-bold text-lime-600 dark:text-lime-400">{score}</p>
            <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1">correct answers</p>
          </div>

          <div className="flex flex-wrap justify-center gap-3">
            <div className="px-4 py-2 bg-zinc-100 dark:bg-zinc-700 rounded-xl text-center">
              <p className="text-lg font-bold text-zinc-800 dark:text-white">{accuracy}%</p>
              <p className="text-[10px] text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">Accuracy</p>
            </div>
            <div className="px-4 py-2 bg-zinc-100 dark:bg-zinc-700 rounded-xl text-center">
              <p className="text-lg font-bold text-zinc-800 dark:text-white">{bestStreak}</p>
              <p className="text-[10px] text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">Best Streak</p>
            </div>
            <div className="px-4 py-2 bg-zinc-100 dark:bg-zinc-700 rounded-xl text-center">
              <p className="text-lg font-bold text-zinc-800 dark:text-white">{totalAnswered}</p>
              <p className="text-[10px] text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">Answered</p>
            </div>
          </div>

          {accuracy >= 80 && (
            <p className="text-sm text-emerald-600 dark:text-emerald-400 font-medium text-center max-w-sm">
              Excellent! You can clearly distinguish person praise from process praise. That awareness is the first step to rewiring your mindset.
            </p>
          )}
          {accuracy >= 50 && accuracy < 80 && (
            <p className="text-sm text-amber-600 dark:text-amber-400 font-medium text-center max-w-sm">
              Good effort! Some of those statements are tricky. Play again to sharpen your decoder skills.
            </p>
          )}
          {accuracy < 50 && (
            <p className="text-sm text-rose-600 dark:text-rose-400 font-medium text-center max-w-sm">
              The line between person and process praise can be subtle. Give it another go — your brain will get faster at spotting the difference.
            </p>
          )}

          <button
            onClick={startGame}
            className="px-8 py-3 bg-lime-500 text-white font-bold text-sm rounded-xl hover:bg-lime-600 shadow-lg shadow-lime-500/20 transition-all"
          >
            Play Again
          </button>
        </MotionDiv>
      )}
    </div>
  );
};

// --- MODULE COMPONENT ---
const ThePraiseProtocolModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'praise-paradox', title: 'The Praise Paradox', eyebrow: '01 // The Big Idea', icon: MessageCircle },
    { id: 'dweck-experiment', title: 'The Praise Experiment', eyebrow: '02 // What Actually Happens', icon: BarChart },
    { id: 'brain-on-praise', title: 'The Brain on Praise', eyebrow: '03 // What Your Brain Does', icon: Brain },
    { id: 'real-world-data', title: 'The Real World Data', eyebrow: '04 // The Gender Gap', icon: User },
    { id: 'false-growth', title: 'The "Effort" Trap', eyebrow: '05 // The Common Mistake', icon: AlertTriangle },
    { id: 'feedback-audit', title: 'The Feedback Audit', eyebrow: '06 // Your Action Plan', icon: Settings },
  ];

  return (
    <ModuleLayout
      moduleNumber="03"
      moduleTitle="The Power of Praise"
      moduleSubtitle="How Words Shape Your Mindset"
      moduleDescription="The way people praise you — and the way you talk to yourself — can either set you up to grow or keep you stuck. Here's how to tell the difference."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Choose Your Words"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Praise Paradox." eyebrow="Step 1" icon={MessageCircle} theme={theme}>
              <p>We've been told our whole lives that praise builds confidence. But what if some types of praise are actually a trap? This is the praise paradox. The words you hear — and the words you tell yourself — aren't just nice things to say. They actually shape how your brain deals with success and failure going forward.</p>
              <p>There are basically two types of praise. <Highlight description="This is when someone praises who you are — like saying 'You're so smart' or 'You're a natural.' It sounds nice, but it makes you afraid to mess up because you start thinking your ability is just something you either have or don't." theme={theme}>Person Praise</Highlight> focuses on who you <em>are</em>. <Highlight description="This is when someone praises what you did — like 'You worked really hard on that' or 'That was a great strategy.' This kind of praise is way more useful because it makes you want to keep trying and improving." theme={theme}>Process Praise</Highlight> focuses on what you <em>do</em>. One makes you fragile, the other makes you resilient. Knowing the difference is a game-changer.</p>
              <PraiseDecoderGame />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Praise Experiment." eyebrow="Step 2" icon={BarChart} theme={theme}>
                <p>Here's an experiment that shows just how powerful one sentence of praise can be. A group of students were all given a test, told they did well, and then given one of two responses: "You must be smart" (Person Praise) or "You must have worked hard" (Process Praise). That's it — one sentence.</p>
                <p>The findings were striking. The "smart" kids immediately started playing it safe, choosing easier tasks so they wouldn't risk looking stupid. When they hit a harder problem and failed, they gave up, their scores tanked, and nearly 40% of them lied about how they did. The "hard-working" kids went the other way: they picked harder challenges, actually enjoyed the struggle, bounced back after failing, and were three times more honest about their scores. Let's run the simulation.</p>
                <DweckExperimentSimulator />
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The Brain on Praise." eyebrow="Step 3" icon={Brain} theme={theme}>
              <p>Why does one sentence make such a big difference? Because the two types of praise light up different parts of your brain. When you get praised, your brain releases <Highlight description="A chemical in your brain that makes you feel good and want to do something again. It's basically your brain's reward signal." theme={theme}>dopamine</Highlight> — the feel-good chemical. Process praise connects that feeling to <em>the work you put in</em>, so your brain starts craving effort. Person praise connects it to <em>who you are</em>, so any failure feels like a personal attack and your motivation crashes.</p>
              <p>It goes even deeper than that. When we make a mistake, our brains produce an error signal (called the "Pe wave"). With a <Highlight description="Thinking your intelligence is set in stone. If you believe this, every failure feels like proof you're just not good enough." theme={theme}>Fixed Mindset</Highlight>, that signal is tiny — your brain basically flinches away from the mistake to protect your ego. With a <Highlight description="Thinking your intelligence can grow with effort. If you believe this, failure is just information — a chance to figure out what went wrong and do better." theme={theme}>Growth Mindset</Highlight>, the signal is massive — your brain locks onto the mistake and tries to learn from it.</p>
              <ErrorSignalVisualizer />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Real World Data." eyebrow="Step 4" icon={User} theme={theme}>
              <p>This isn't just something that works in a lab. A long-term study followed families from when their kids were toddlers all the way through primary school. It found that the amount of process praise parents used (on average, just 18% of all praise) predicted whether their child would develop a growth mindset five years later. More process praise meant a stronger growth mindset, which led to better results in Maths and English.</p>
              <p>The study also found a big gender gap. From as young as 14 months, boys tended to get more process praise ("You built that tower so high!"), while girls were more likely to hear trait-based praise ("You're such a good girl"). This difference in how boys and girls are talked to from a very young age helps explain why high-achieving girls can sometimes be more likely to develop a fixed mindset later on.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The 'Effort' Trap." eyebrow="Step 5" icon={AlertTriangle} theme={theme}>
                <p>As these ideas got popular, people started getting them wrong. The biggest mistake is thinking that a growth mindset just means praising effort. Imagine you fail a test after studying hard, and someone says, "Don't worry, you tried your best!" This is <Highlight description="When someone praises your effort but doesn't help you figure out what went wrong. It sounds kind, but it basically says 'you gave it everything and it still wasn't enough' — which is actually pretty discouraging." theme={theme}>Consolation Praise</Highlight>, and it actually does more harm than good. It sends the message: "Your best isn't good enough, and there's nothing more you can do."</p>
                <p>Good process praise connects effort to *what worked* and *what didn't*. A better response would be: "I can see you worked hard, but the study method you used didn't click. Let's look at your mistakes and try a different approach." Effort on its own isn't enough — it has to be pointed in the right direction.</p>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="The Feedback Audit." eyebrow="Step 6" icon={Settings} theme={theme}>
              <p>Now that you know the difference, start paying attention to the feedback around you — from teachers, family, and especially how you talk to yourself. The "Feedback Audit" is simple: for one day, just notice the praise you hear and sort it. Is it Person Praise, Process Praise, or just vague outcome stuff ("Good job")?</p>
              <MicroCommitment theme={theme}>
                <p>Tonight, when you're reviewing your day, think of one piece of feedback you received (from yourself or others). Was it Person or Process praise? Just noticing is the first step.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default ThePraiseProtocolModule;
