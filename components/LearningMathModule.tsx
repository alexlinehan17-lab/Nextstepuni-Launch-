
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Target, Brain, SlidersHorizontal, AlertTriangle, PenTool, Key, BookOpen, Wrench
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { grayTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
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

const MotionDiv = motion.div as any;

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
    { id: 'new-game', title: 'The New Game', eyebrow: '01 // Project Maths', icon: Target },
    { id: 'two-papers', title: 'The Two Papers', eyebrow: '02 // Technical vs. Contextual', icon: BookOpen },
    { id: 'deep-dive', title: 'The Five Strands', eyebrow: '03 // Curriculum Deep Dive', icon: SlidersHorizontal },
    { id: 'marking-scheme', title: 'Decoding the Scheme', eyebrow: '04 // Positive Marking', icon: Key },
    { id: 'attempt-mark', title: 'The "Attempt Mark" Goldmine', eyebrow: '05 // Partial Credit', icon: Wrench },
    { id: 'spotting-trends', title: 'Spotting the Trends', eyebrow: '06 // Gremlins & Hybrids', icon: Brain },
    { id: 'examiners-mind', title: 'The Examiner\'s Mind', eyebrow: '07 // Common Errors', icon: AlertTriangle },
    { id: 'cognitive-toolkit', title: 'The Cognitive Toolkit', eyebrow: '08 // Learning Science for Maths', icon: Brain },
    { id: 'h1-pathway', title: 'The H1 Pathway', eyebrow: '09 // Bankable Marks', icon: PenTool },
  ];

  return (
    <ModuleLayout
      moduleNumber="01"
      moduleTitle="Mastering Maths"
      moduleSubtitle="Deconstructing the Exam"
      moduleDescription="A strategic deep-dive into the structure, marking schemes, and high-yield topics of the Leaving Cert Higher Level Maths exam."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The New Game." eyebrow="Step 1" icon={Target} theme={theme}>
              <p>Leaving Cert Maths is not the same game it used to be. The "Project Maths" initiative fundamentally changed the rules, shifting the focus from rote memorization of algorithms to genuine <Highlight description="The ability to understand the 'why' behind a mathematical rule, not just the 'how'." theme={theme}>conceptual understanding</Highlight> and problem-solving. It's a test of resilience, not just numeracy.</p>
              <p>The introduction of the <Highlight description="The 25 extra CAO points awarded for a H6 or higher, making Maths the single most valuable subject in the points race." theme={theme}>Bonus Points</Highlight> has also changed the strategic landscape. A H6 in Maths is worth more than a H3 in any other subject. This "safety net" encourages students to aim high, but requires a deep, strategic approach to the exam.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Two Papers." eyebrow="Step 2" icon={BookOpen} theme={theme}>
              <p>The exam is split into two papers designed to test different cognitive skills. <strong>Paper 1</strong> is the <strong>"Technical"</strong> paper. It's heavily weighted towards Algebra, Calculus, and Number. It rewards <Highlight description="The ability to perform mathematical operations (like solving equations or differentiating) quickly and accurately." theme={theme}>procedural fluency</Highlight> and is less "wordy."</p>
              <p><strong>Paper 2</strong> is the <strong>"Contextual"</strong> paper. This is the test of interpretation and spatial reasoning, covering Statistics, Probability, Geometry, and Trigonometry. It's often described as "volatile" because a single novel diagram can throw off students who rely on memorized procedures rather than a deep understanding of the concepts.</p>
              <PaperPredictorGame />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Five Strands." eyebrow="Step 3" icon={SlidersHorizontal} theme={theme}>
              <p>The syllabus is divided into five interconnected strands. Questions are deliberately <Highlight description="Requiring students to combine knowledge from multiple strands (e.g., using Algebra to solve a Geometry problem)." theme={theme}>synoptic</Highlight>, so you can't study topics in isolation.</p>
              <p>The strands are: 1) <strong>Statistics & Probability</strong> (literacy-heavy), 2) <strong>Geometry & Trigonometry</strong> (visual and spatial), 3) <strong>Number</strong> (the foundation, including Complex Numbers), 4) <strong>Algebra</strong> (the "language" of the course), and 5) <strong>Functions & Calculus</strong> (the heavyweight of Paper 1).</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Decoding the Marking Scheme." eyebrow="Step 4" icon={Key} theme={theme}>
              <p>Understanding how marks are awarded is your single greatest strategic asset. The SEC uses a <Highlight description="An ethos where marks are awarded for what is correct, not deducted for what is wrong. The goal is to reward any valid progress." theme={theme}>"Positive Marking"</Highlight> system. This is codified in the Scale System (A, B, C, D).</p>
              <p><strong>Scale A</strong> (0, 10) is rare. <strong>Scale B</strong> (0, 5, 10) is "hit or miss." But <strong>Scale C</strong> (0, 3, 7, 10) and <strong>Scale D</strong> (0, 3, 5, 8, 10) are the most common. The crucial insight is the "Low Partial" mark—you can get 30% of the marks for simply writing down the correct formula and attempting to substitute a value. This is a strategic goldmine.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The 'Attempt Mark' Goldmine." eyebrow="Step 5" icon={Wrench} theme={theme}>
              <p>The "Low Partial Credit" is your safety net. If you encounter a 10-mark question that seems impossible, simply writing down the relevant formula from the log tables and substituting one correct value often secures 3 marks. Leaving a question blank is a strategic failure of the highest order.</p>
              <p>Accumulating these "scrap" marks across an entire paper can be the difference between a H4 and a H3. The goal is to *never get a zero*. Even on the hardest "gremlin" question, there are marks available for defining terms, writing a relevant formula, or drawing a diagram. You must train yourself to hunt for these partial marks.</p>
              <PartialCreditCalculator />
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Spotting the Trends." eyebrow="Step 6" icon={Brain} theme={theme}>
              <p>Analysis of past papers reveals clear trends. Paper 1 is seeing the rise of applied Calculus (rates of change) and Complex Numbers treated as geometry. Paper 2 is increasingly defined by its <Highlight description="Novel questions with unfamiliar diagrams or scenarios that test a student's ability to apply core principles to new situations." theme={theme}>"Gremlin" questions</Highlight> and <Highlight description="Questions that fuse topics from different strands, such as calculating the probability that a point lies within a certain geometric region." theme={theme}>Probability-Geometry hybrids</Highlight>. These questions are designed to defeat rote learning and reward flexible, conceptual understanding.</p>
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="The Examiner's Mind." eyebrow="Step 7" icon={AlertTriangle} theme={theme}>
              <p>The Chief Examiner's Reports highlight the most common student errors. The biggest is <Highlight description="The tendency for students to understand a concept but fail in the algebraic execution (e.g., mishandling signs, index errors)." theme={theme}>"Algebraic Fragility."</Highlight> The second is the <Highlight description="The failure to check answers for reasonableness (e.g., calculating a probability greater than 1, or a negative distance)." theme={theme}>"Check" Deficit</Highlight>. The third is the <Highlight description="The struggle to translate a 'real-world' story problem into a mathematical model, often due to over-reliance on blocked practice." theme={theme}>"Unfamiliar Context" Block</Highlight>.</p>
              <p>A major pitfall is "forcing" an answer in "Show That" questions. It is strategically better to write, "I cannot derive the final step, but assuming x=5, I will proceed..." This allows you to gain partial credit on subsequent parts.</p>
              <ProblemSorter />
            </ReadingSection>
          )}
          {activeSection === 7 && (
            <ReadingSection title="The Cognitive Toolkit." eyebrow="Step 8" icon={Brain} theme={theme}>
              <p>To overcome these challenges, you must adopt strategies from cognitive science. <Highlight description="Studying one topic intensely (e.g., Algebra all week). It creates a false sense of mastery." theme={theme}>Blocking</Highlight> fails to train strategy selection. <Highlight description="Mixing up topics within a study session (e.g., one Algebra, one Geometry, one Probability). It feels harder but builds flexible, exam-ready knowledge." theme={theme}>Interleaving</Highlight> is crucial for Maths as it mimics the exam environment.</p>
              <p>Passive reading of notes is ineffective. <Highlight description="Closing the book and attempting to write out a proof or definition from memory. This strengthens the neural pathways." theme={theme}>Active Recall</Highlight> is essential. Finally, you must maintain an <Highlight description="A log where you categorize your mistakes (Concept, Procedural, Reading) to prevent repetition and target revision." theme={theme}>Error Log</Highlight>. The most valuable part of a past paper is the "post-mortem."</p>
              <ErrorLog />
            </ReadingSection>
          )}
          {activeSection === 8 && (
            <ReadingSection title="The H1 Pathway." eyebrow="Step 9" icon={PenTool} theme={theme}>
              <p>For students aiming for the top grade, the strategy goes beyond competence. It requires speed and tactical awareness. H1 students distinguish themselves by their fluency, completing routine Section A questions faster to "bank" time for the harder Section B questions.</p>
              <p>The final layer of strategy is to identify and master the few things in Maths that *can* be rote-learned. These are your <Highlight description="The small number of examinable proofs (e.g., Induction, irrationality of root 2) and definitions (e.g., 'injective function'). These should be learned perfectly as they are 'free marks' when they appear." theme={theme}>"Bankable Marks."</Highlight> A small number of formal proofs and definitions are examinable. These should be learned perfectly and are 'free marks' if they appear on the day.</p>
              <MicroCommitment theme={theme}><p>Go to your log tables. Pick one proof (e.g., Cos(A+B)). Spend 15 minutes learning it using active recall. You've just 'banked' a potential 10 marks.</p></MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default LearningMathModule;
