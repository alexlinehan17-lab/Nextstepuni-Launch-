
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import {
  Target, Brain, SlidersHorizontal, AlertTriangle, PenTool, Key, BookOpen, Wrench
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { grayTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = grayTheme;

// --- INTERACTIVE COMPONENTS ---
const PartialCreditCalculator = () => {
    const [steps, setSteps] = useState({ formula: false, sub: false, slip: false, blunder: false });

    let marks = 0;
    if(steps.blunder) marks = 3;
    else if(steps.formula && steps.sub && steps.slip) marks = 8;
    else if(steps.formula && steps.sub) marks = 10;
    else if(steps.formula) marks = 5;

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Partial Credit Calculator</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Scenario: 10-mark Scale D Question. How many marks do you get?</p>
             <div className="grid grid-cols-2 gap-3">
                <button onClick={() => setSteps(s => ({...s, formula: !s.formula}))} className={`p-4 rounded-xl border ${steps.formula ? 'bg-emerald-50' : ''}`}>Wrote correct formula</button>
                <button onClick={() => setSteps(s => ({...s, sub: !s.sub}))} className={`p-4 rounded-xl border ${steps.sub ? 'bg-emerald-50' : ''}`}>Substituted a value</button>
                <button onClick={() => setSteps(s => ({...s, slip: !s.slip, blunder: false}))} className={`p-4 rounded-xl border ${steps.slip ? 'bg-amber-50' : ''}`}>Made a minor calculation 'Slip'</button>
                <button onClick={() => setSteps(s => ({...s, blunder: !s.blunder, slip: false}))} className={`p-4 rounded-xl border ${steps.blunder ? 'bg-rose-50' : ''}`}>Made a major concept 'Blunder'</button>
             </div>
             <div className="mt-8 p-4 bg-zinc-900 rounded-xl text-center text-white">
                You get <span className="font-bold text-2xl text-gray-400">{marks}/10</span> marks.
            </div>
        </div>
    );
};

const ProblemSorter = () => {
    const problems = [
        {id: 1, text: "How many ways can 5 books be arranged?", type: 'p'},
        {id: 2, text: "How many teams of 5 can be picked from 10 players?", type: 'c'}
    ];
    const [choice, setChoice] = useState<{[key: number]: string | null}>({});

    const handleChoice = (id: number, c: string) => {
        setChoice(prev => ({...prev, [id]: c}));
    };

    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Problem Sorter</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Train your discriminative skills: Is it a Permutation (order matters) or a Combination (order doesn't)?</p>
            {problems.map(p => (
                <div key={p.id} className="mb-4">
                    <p className="p-4 bg-zinc-100 dark:bg-zinc-800 rounded-lg text-center font-bold">{p.text}</p>
                    <div className="grid grid-cols-2 gap-2 mt-2">
                        <button onClick={() => handleChoice(p.id, 'p')} className={`p-2 rounded-lg border ${choice[p.id] && (choice[p.id] === 'p' && p.type === 'p' ? 'bg-emerald-100 border-emerald-300' : choice[p.id] === 'p' ? 'bg-rose-100 border-rose-300' : 'bg-zinc-100 border-zinc-200 dark:border-zinc-700')}`}>Permutation</button>
                        <button onClick={() => handleChoice(p.id, 'c')} className={`p-2 rounded-lg border ${choice[p.id] && (choice[p.id] === 'c' && p.type === 'c' ? 'bg-emerald-100 border-emerald-300' : choice[p.id] === 'c' ? 'bg-rose-100 border-rose-300' : 'bg-zinc-100 border-zinc-200 dark:border-zinc-700')}`}>Combination</button>
                    </div>
                </div>
            ))}
        </div>
    );
}

type PaperQuestion = {
  id: number;
  text: string;
  answer: 'paper1' | 'paper2';
  explanation: string;
};

const PAPER_QUESTIONS: PaperQuestion[] = [
  { id: 1, text: 'Solve 2x\u00B2 + 5x \u2212 3 = 0', answer: 'paper1', explanation: 'Pure algebra \u2192 Paper 1' },
  { id: 2, text: 'A farmer encloses a field with 200\u202Fm of fencing. Find the maximum area.', answer: 'paper2', explanation: 'Real-world context \u2192 Paper 2' },
  { id: 3, text: 'Differentiate f(x) = 3x\u2074 \u2212 2x + 7', answer: 'paper1', explanation: 'Pure calculus \u2192 Paper 1' },
  { id: 4, text: 'A survey of 100 students found that 60 play sport. Find the margin of error.', answer: 'paper2', explanation: 'Statistics in context \u2192 Paper 2' },
  { id: 5, text: 'Prove that \u221A2 is irrational.', answer: 'paper1', explanation: 'Pure proof \u2192 Paper 1' },
  { id: 6, text: 'A ball is thrown upward at 20\u202Fm/s. When does it reach maximum height?', answer: 'paper2', explanation: 'Applied context \u2192 Paper 2' },
  { id: 7, text: 'Find the sum of the first 20 terms of the series 3 + 6 + 12 + \u2026', answer: 'paper1', explanation: 'Pure sequences \u2192 Paper 1' },
  { id: 8, text: 'The probability of rain on any day is 0.3. Find P(rain on exactly 2 of 5 days).', answer: 'paper2', explanation: 'Probability in context \u2192 Paper 2' },
  { id: 9, text: 'Solve |2x \u2212 3| > 5', answer: 'paper1', explanation: 'Pure algebra \u2192 Paper 1' },
  { id: 10, text: 'A company\u2019s profit is modelled by P(x) = \u22122x\u00B2 + 40x \u2212 100. Find the break-even points.', answer: 'paper2', explanation: 'Real-world modelling \u2192 Paper 2' },
  { id: 11, text: 'Find the equation of the line perpendicular to 3x + 4y = 12 passing through (1, 2).', answer: 'paper1', explanation: 'Pure coordinate geometry \u2192 Paper 1' },
  { id: 12, text: 'A clinical trial tests a new drug. 45 out of 200 patients improved. Conduct a hypothesis test at 5% significance.', answer: 'paper2', explanation: 'Statistics in context \u2192 Paper 2' },
];

function shuffleArray<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

const PaperPredictorGame = () => {
  const [phase, setPhase] = useState<'intro' | 'playing' | 'results'>('intro');
  const [questions, setQuestions] = useState<PaperQuestion[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [score, setScore] = useState(0);
  const [streak, setStreak] = useState(0);
  const [bestStreak, setBestStreak] = useState(0);
  const [feedback, setFeedback] = useState<{ correct: boolean; explanation: string } | null>(null);
  const [elapsedTime, setElapsedTime] = useState(0);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const startTimeRef = useRef<number>(0);

  const startGame = () => {
    const shuffled = shuffleArray(PAPER_QUESTIONS);
    setQuestions(shuffled);
    setCurrentIndex(0);
    setScore(0);
    setStreak(0);
    setBestStreak(0);
    setFeedback(null);
    setElapsedTime(0);
    setPhase('playing');
    startTimeRef.current = Date.now();
    if (timerRef.current) clearInterval(timerRef.current);
    timerRef.current = setInterval(() => {
      setElapsedTime(Math.floor((Date.now() - startTimeRef.current) / 1000));
    }, 500);
  };

  const handleAnswer = (answer: 'paper1' | 'paper2') => {
    if (feedback) return;
    const q = questions[currentIndex];
    const correct = answer === q.answer;

    if (correct) {
      const newStreak = streak + 1;
      setScore(s => s + 1);
      setStreak(newStreak);
      if (newStreak > bestStreak) setBestStreak(newStreak);
    } else {
      setStreak(0);
    }

    setFeedback({ correct, explanation: q.explanation });

    const delay = correct ? 400 : 1200;
    setTimeout(() => {
      const nextIndex = currentIndex + 1;
      if (nextIndex >= questions.length) {
        if (timerRef.current) clearInterval(timerRef.current);
        setElapsedTime(Math.floor((Date.now() - startTimeRef.current) / 1000));
        setPhase('results');
      } else {
        setCurrentIndex(nextIndex);
      }
      setFeedback(null);
    }, delay);
  };

  const formatTime = (s: number) => {
    const mins = Math.floor(s / 60);
    const secs = s % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Paper Predictor</h4>

      {phase === 'intro' && (
        <div className="text-center mt-6">
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-2">
            <strong>Paper 1</strong> = Pure / Technical. <strong>Paper 2</strong> = Context / Applied.
          </p>
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-8">Can you sort 12 question stems as fast as possible?</p>
          <button
            onClick={startGame}
            className="px-8 py-3 rounded-xl bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 font-semibold text-sm hover:opacity-90 transition-opacity"
          >
            Start Game
          </button>
        </div>
      )}

      {phase === 'playing' && questions.length > 0 && (
        <div className="mt-6">
          {/* Stats pills */}
          <div className="flex flex-wrap items-center justify-center gap-2 mb-6">
            <span className="px-3 py-1 rounded-full text-xs font-medium bg-zinc-100 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-300">
              {currentIndex + 1} / {questions.length}
            </span>
            <span className="px-3 py-1 rounded-full text-xs font-medium bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300">
              Score: {score}
            </span>
            <span className="px-3 py-1 rounded-full text-xs font-medium bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300">
              Streak: {streak}
            </span>
            <span className="px-3 py-1 rounded-full text-xs font-medium bg-zinc-100 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-300">
              {formatTime(elapsedTime)}
            </span>
          </div>

          {/* Question card */}
          <AnimatePresence mode="wait">
            <MotionDiv
              key={questions[currentIndex].id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.25 }}
              className={`p-6 md:p-8 rounded-xl border-2 transition-colors duration-200 ${
                feedback === null
                  ? 'border-zinc-200 dark:border-zinc-600 bg-zinc-50 dark:bg-zinc-900/50'
                  : feedback.correct
                  ? 'border-emerald-400 bg-emerald-50 dark:bg-emerald-900/20'
                  : 'border-rose-400 bg-rose-50 dark:bg-rose-900/20'
              }`}
            >
              <p className="text-center text-lg md:text-xl font-medium text-zinc-800 dark:text-white leading-relaxed">
                {questions[currentIndex].text}
              </p>
              {feedback && !feedback.correct && (
                <p className="text-center text-sm text-rose-600 dark:text-rose-400 mt-4 font-medium">
                  {feedback.explanation}
                </p>
              )}
            </MotionDiv>
          </AnimatePresence>

          {/* Answer buttons */}
          <div className="grid grid-cols-2 gap-3 mt-6">
            <button
              onClick={() => handleAnswer('paper1')}
              disabled={feedback !== null}
              className="p-4 rounded-xl border-2 border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 font-semibold text-base hover:bg-blue-100 dark:hover:bg-blue-900/50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Paper 1
            </button>
            <button
              onClick={() => handleAnswer('paper2')}
              disabled={feedback !== null}
              className="p-4 rounded-xl border-2 border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300 font-semibold text-base hover:bg-amber-100 dark:hover:bg-amber-900/50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Paper 2
            </button>
          </div>
        </div>
      )}

      {phase === 'results' && (
        <div className="mt-6 text-center">
          {/* Score display */}
          <div className="mb-6">
            <p className="text-5xl font-bold text-zinc-800 dark:text-white">{score}<span className="text-2xl text-zinc-400 dark:text-zinc-500">/{questions.length}</span></p>
            <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1">
              {Math.round((score / questions.length) * 100)}% accuracy in {formatTime(elapsedTime)}
            </p>
          </div>

          {/* Result stats */}
          <div className="flex flex-wrap items-center justify-center gap-2 mb-6">
            <span className="px-3 py-1 rounded-full text-xs font-medium bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300">
              Best streak: {bestStreak}
            </span>
            <span className="px-3 py-1 rounded-full text-xs font-medium bg-zinc-100 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-300">
              Time: {formatTime(elapsedTime)}
            </span>
          </div>

          {/* Summary insight */}
          <div className="p-4 rounded-xl bg-zinc-50 dark:bg-zinc-900/50 border border-zinc-200 dark:border-zinc-700 mb-6">
            <p className="text-sm text-zinc-600 dark:text-zinc-300 leading-relaxed">
              <strong>Paper 1</strong> = pure maths (algebra, calculus, proofs). <strong>Paper 2</strong> = maths in context (statistics, applied problems, modelling).
            </p>
          </div>

          <button
            onClick={startGame}
            className="px-8 py-3 rounded-xl bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 font-semibold text-sm hover:opacity-90 transition-opacity"
          >
            Play Again
          </button>
        </div>
      )}
    </div>
  );
};

const ErrorLog = () => {
    const [error, setError] = useState('');
    const [type, setType] = useState<string | null>(null);

    return(
         <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">My Error Log</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Log a mistake from a practice question to turn it into a learning opportunity.</p>
             <div className="space-y-4">
                <textarea value={error} onChange={e => setError(e.target.value)} placeholder="Describe the mistake..." className="w-full h-24 p-4 bg-zinc-50 dark:bg-zinc-800/50 border rounded-xl focus:outline-none focus:border-gray-400"></textarea>
                <div className="grid grid-cols-3 gap-2">
                    <button onClick={() => setType('Concept')} className={`p-2 text-xs rounded-lg border ${type === 'Concept' ? 'bg-gray-800 text-white' : 'bg-zinc-100'}`}>Concept Error</button>
                    <button onClick={() => setType('Procedural')} className={`p-2 text-xs rounded-lg border ${type === 'Procedural' ? 'bg-gray-800 text-white' : 'bg-zinc-100'}`}>Procedural Error</button>
                    <button onClick={() => setType('Reading')} className={`p-2 text-xs rounded-lg border ${type === 'Reading' ? 'bg-gray-800 text-white' : 'bg-zinc-100'}`}>Reading Error</button>
                </div>
             </div>
             {error && type && <p className="text-center mt-4 text-sm font-bold text-emerald-600">Error logged. Now you won't make it again.</p>}
        </div>
    );
};

// --- MODULE COMPONENT ---
const LearningMathModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'new-game', title: 'The New Game', eyebrow: '01 // What Changed', icon: Target },
    { id: 'two-papers', title: 'The Two Papers', eyebrow: '02 // Paper 1 vs. Paper 2', icon: BookOpen },
    { id: 'deep-dive', title: 'The Five Strands', eyebrow: '03 // What You Need to Know', icon: SlidersHorizontal },
    { id: 'marking-scheme', title: 'How Marking Actually Works', eyebrow: '04 // Getting Marks You Deserve', icon: Key },
    { id: 'attempt-mark', title: 'Never Leave a Question Blank', eyebrow: '05 // Free Marks', icon: Wrench },
    { id: 'spotting-trends', title: 'Spotting the Patterns', eyebrow: '06 // Tricky Questions & Crossovers', icon: Brain },
    { id: 'examiners-mind', title: 'What Examiners Actually Look For', eyebrow: '07 // Common Mistakes', icon: AlertTriangle },
    { id: 'cognitive-toolkit', title: 'Study Smarter for Maths', eyebrow: '08 // How to Actually Learn This Stuff', icon: Brain },
    { id: 'h1-pathway', title: 'The H1 Pathway', eyebrow: '09 // Locking In Top Marks', icon: PenTool },
  ];

  return (
    <ModuleLayout
      moduleNumber="01"
      moduleTitle="Mastering Maths"
      moduleSubtitle="How to Beat the Exam"
      moduleDescription="Everything you need to know about how Higher Level Maths actually works -- the papers, the marking, and the tricks that earn you extra marks."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Crack the Code"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The New Game." eyebrow="Step 1" icon={Target} theme={theme}>
              <p>Leaving Cert Maths is not the same game it used to be. Project Maths changed the rules -- it's no longer about memorising formulas and repeating steps. Now it's about actually <Highlight description="It's not enough to know the formula. You need to understand why it works, so you can use it in questions you've never seen before." theme={theme}>understanding why things work</Highlight> and solving problems you've never seen before. It's a test of resilience, not just number-crunching.</p>
              <p>Then there are the <Highlight description="You get 25 extra CAO points just for getting a H6 or higher in Maths. That makes it the single most valuable subject for your points." theme={theme}>Bonus Points</Highlight> -- 25 extra CAO points just for getting a H6 or above. That means a H6 in Maths is worth more than a H3 in any other subject. It's a massive safety net, and it means aiming for Higher Level is worth it even if you're not a "maths person."</p>
              <PersonalStory name="Orlaith" role="6th Year, Tallaght">
                <p>I nearly dropped to Ordinary Level after 5th year because I got 38% in my summer exam. But my teacher said "just try Higher for the mocks." I started using the bonus points as motivation -- even a H7 would be worth it. I ended up getting a H5 in the real thing and those 25 bonus points got me into my course. Honestly, if I'd dropped down I wouldn't have made it.</p>
              </PersonalStory>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Two Papers." eyebrow="Step 2" icon={BookOpen} theme={theme}>
              <p>The exam is split into two papers, and they feel quite different. <strong>Paper 1</strong> is the <strong>"Technical"</strong> paper. It's mostly Algebra, Calculus, and Number -- the kind of maths where you need to be <Highlight description="Being able to do the steps quickly and accurately -- solving equations, differentiating, that kind of thing." theme={theme}>quick and accurate with the steps</Highlight>. Less reading, more doing.</p>
              <p><strong>Paper 2</strong> is the <strong>"Contextual"</strong> paper. This covers Statistics, Probability, Geometry, and Trigonometry -- and the questions are wrapped in real-world scenarios. It's often called the "unpredictable" paper because one weird diagram can throw you off if you've only memorised methods without actually understanding the ideas behind them.</p>
              <PaperPredictorGame />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Five Strands." eyebrow="Step 3" icon={SlidersHorizontal} theme={theme}>
              <p>The course is divided into five big areas. Here's the thing -- they're all connected. The exam deliberately mixes them together, so a question might use <Highlight description="Questions often blend topics together. You might need Algebra to solve a Geometry problem, or Probability inside a Calculus question." theme={theme}>Algebra to solve a Geometry problem</Highlight>. You can't just study one topic on its own and hope for the best.</p>
              <p>The five areas are: 1) <strong>Statistics & Probability</strong> (lots of reading and interpreting), 2) <strong>Geometry & Trigonometry</strong> (visual, diagrams everywhere), 3) <strong>Number</strong> (the basics, including Complex Numbers), 4) <strong>Algebra</strong> (it's the language that runs through everything), and 5) <strong>Functions & Calculus</strong> (the biggest chunk of Paper 1).</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="How Marking Actually Works." eyebrow="Step 4" icon={Key} theme={theme}>
              <p>Understanding how marks are given out is honestly your biggest advantage. The SEC uses <Highlight description="You get marks for what you get right -- they don't take marks away for mistakes. Any progress you show counts." theme={theme}>"Positive Marking"</Highlight> -- they reward you for what you get right, not punish you for what you get wrong. They use a Scale System (A, B, C, D) to decide how marks are split up.</p>
              <p><strong>Scale A</strong> (0 or 10) is rare -- it's all or nothing. <strong>Scale B</strong> (0, 5, or 10) is "hit or miss." But <strong>Scale C</strong> (0, 3, 7, 10) and <strong>Scale D</strong> (0, 3, 5, 8, 10) are the ones you'll see most. Here's the key: on a Scale D question, just writing down the right formula and plugging in one value can get you 3 marks out of 10. That's 30% for barely anything -- and it adds up fast across a whole paper.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Never Leave a Question Blank." eyebrow="Step 5" icon={Wrench} theme={theme}>
              <p>This is the golden rule of Higher Level Maths: <strong>never, ever leave a question blank</strong>. If you hit a 10-mark question that looks impossible, just write down the relevant formula from the log tables and substitute one value. That alone often gets you 3 marks. Leaving it blank gets you zero. It's that simple.</p>
              <p>Picking up these small marks across a whole paper can genuinely be the difference between a H4 and a H3. Your goal is to never score zero on any question. Even on the trickiest questions, there are marks going for writing a formula, defining a term, or drawing a diagram. Train yourself to hunt for those marks -- they're there for the taking.</p>
              <PartialCreditCalculator />
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Spotting the Patterns." eyebrow="Step 6" icon={Brain} theme={theme}>
              <p>If you look at past papers, clear patterns jump out. Paper 1 is asking more and more about applied Calculus (rates of change in real situations) and treating Complex Numbers like geometry. Paper 2 keeps throwing in <Highlight description="Those weird questions with diagrams or setups you've never seen before. They test whether you actually understand the ideas, not just the steps." theme={theme}>"Gremlin" questions</Highlight> -- the ones that look totally unfamiliar -- and <Highlight description="Questions that mix two topics together, like working out a probability using the area of a shape. They want to see if you can connect different ideas." theme={theme}>crossover questions</Highlight> that blend Probability with Geometry. These are designed to catch out anyone who's only memorised steps without understanding the ideas behind them.</p>
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="What Examiners Actually Look For." eyebrow="Step 7" icon={AlertTriangle} theme={theme}>
              <p>The Examiner's Reports tell you exactly where students lose marks every year. The biggest one is <Highlight description="You understand the idea, but you mess up the algebra -- wrong signs, index errors, silly slips that cost you marks." theme={theme}>sloppy algebra</Highlight> -- you get the concept but mess up the execution with sign errors or index mistakes. The second is <Highlight description="Not checking if your answer makes sense. Like getting a probability of 1.3 or a negative length -- a quick check would catch those." theme={theme}>not checking your answers</Highlight> (getting a probability greater than 1 and not noticing). The third is <Highlight description="When a question is wrapped in a real-world story you haven't seen before, and you freeze because it doesn't look like your textbook." theme={theme}>freezing on unfamiliar questions</Highlight> -- when a question is wrapped in a story you've never seen, your brain goes blank.</p>
              <p>One big trap: "Show That" questions. If you can't get to the answer they want, don't force it or fudge the working. Instead, write something like "I can't get to this result, but assuming x=5, I'll continue..." -- and then keep going. This way you can still pick up marks on the rest of the question.</p>
              <ProblemSorter />
            </ReadingSection>
          )}
          {activeSection === 7 && (
            <ReadingSection title="Study Smarter for Maths." eyebrow="Step 8" icon={Brain} theme={theme}>
              <p>Here's how to actually get better at Maths (not just feel like you're getting better). First, stop <Highlight description="When you do nothing but Algebra questions for a whole study session. It feels productive, but you're not training your brain to switch between topics like the exam requires." theme={theme}>doing the same topic for hours</Highlight>. Instead, <Highlight description="Mix up your topics in a single study session -- do an Algebra question, then a Geometry one, then Probability. It feels harder, but it trains your brain the way the exam actually works." theme={theme}>mix up your topics</Highlight> within a single session. It feels harder, but it's closer to what the actual exam is like, and it builds the kind of knowledge that sticks.</p>
              <p>Reading over your notes doesn't work for Maths. You need to <Highlight description="Close the book and try to do the problem from memory. If you can't, that tells you exactly what you need to work on." theme={theme}>test yourself</Highlight> -- close the book, try to do the problem, and see what happens. And keep an <Highlight description="Write down every mistake you make, sort it by type (didn't understand the idea, messed up the steps, or misread the question), and review it before exams." theme={theme}>Error Log</Highlight> -- write down every mistake you make on past papers, sort them by type, and review them. The real learning happens after you finish a past paper, when you figure out what went wrong.</p>
              <ErrorLog />
            </ReadingSection>
          )}
          {activeSection === 8 && (
            <ReadingSection title="The H1 Pathway." eyebrow="Step 9" icon={PenTool} theme={theme}>
              <p>If you're going for a H1, it's not just about knowing the material -- it's about speed and awareness. H1 students get through the routine Section A questions quickly so they have more time for the harder Section B questions. That speed comes from practice, not from being naturally faster.</p>
              <p>Here's a tip: there are a handful of things in Maths that you can just learn off by heart. These are your <Highlight description="Things like the proof by induction, the proof that root 2 is irrational, or definitions like 'injective function'. Learn them perfectly -- if they come up, they're easy marks." theme={theme}>guaranteed marks</Highlight>. A few formal proofs and definitions come up regularly, and if you know them perfectly, they're basically free marks on the day.</p>
              <MicroCommitment theme={theme}><p>Go to your log tables. Pick one proof (like the Cos(A+B) formula). Spend 15 minutes learning it by closing the book and writing it out from memory. You've just locked in a potential 10 marks.</p></MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default LearningMathModule;
