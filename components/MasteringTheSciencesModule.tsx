/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import {
  Key, Leaf, Beaker, Atom, Sprout, BrainCircuit, Flag
} from 'lucide-react';
import { type ModuleProgress } from '../types';
import { emeraldTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useEssentialsMode } from '../hooks/useEssentialsMode';

const theme = emeraldTheme;

// --- INTERACTIVE COMPONENTS ---
const CurlyArrowDrill = () => {
    const [current, setCurrent] = useState(0);
    const [selected, setSelected] = useState<'a' | 'b' | null>(null);
    const [isCorrect, setIsCorrect] = useState(false);
    const [score, setScore] = useState(0);

    const scenarios = [
        { a: { formula: 'Cl\u207b', label: 'Chloride ion', isSource: true }, b: { formula: 'C\u207a', label: 'Carbocation', isSource: false },
          explanation: 'Cl\u207b has a lone pair (electron-rich) \u2192 donates to the electron-poor C\u207a.' },
        { a: { formula: 'H\u207a', label: 'Proton', isSource: false }, b: { formula: 'OH\u207b', label: 'Hydroxide ion', isSource: true },
          explanation: 'OH\u207b is electron-rich \u2192 arrow goes from OH\u207b lone pair to H\u207a.' },
        { a: { formula: 'BF\u2083', label: 'Boron trifluoride', isSource: false }, b: { formula: 'NH\u2083', label: 'Ammonia', isSource: true },
          explanation: 'NH\u2083 has a lone pair on nitrogen \u2192 donates to electron-deficient boron.' },
        { a: { formula: 'C=C', label: 'Alkene (\u03c0 bond)', isSource: true }, b: { formula: 'H\u207a', label: 'Proton', isSource: false },
          explanation: 'The \u03c0 bond is an electron source \u2192 arrow from C=C to H\u207a.' },
        { a: { formula: 'CH\u2083\u207a', label: 'Methyl cation', isSource: false }, b: { formula: 'H\u2082O', label: 'Water', isSource: true },
          explanation: 'H\u2082O has lone pairs \u2192 donates electrons to the electron-poor CH\u2083\u207a.' },
    ];

    const s = scenarios[current];
    const done = current >= scenarios.length;

    const handleSelect = (choice: 'a' | 'b') => {
        if (isCorrect) return;
        setSelected(choice);
        const right = (choice === 'a' && s.a.isSource) || (choice === 'b' && s.b.isSource);
        if (right) {
            setIsCorrect(true);
            setScore(prev => prev + 1);
        }
    };

    const handleNext = () => {
        setCurrent(prev => prev + 1);
        setSelected(null);
        setIsCorrect(false);
    };

    const btnStyle = (side: 'a' | 'b'): React.CSSProperties => {
        const isSource = side === 'a' ? s?.a.isSource : s?.b.isSource;
        if (isCorrect) {
            return isSource
                ? { backgroundColor: '#D1FAE5', border: '2.5px solid #059669', borderRadius: 14, boxShadow: '3px 3px 0px 0px #059669' }
                : { backgroundColor: '#FFFFFF', border: '2.5px solid #1C1917', borderRadius: 14, boxShadow: '3px 3px 0px 0px #1C1917', opacity: 0.4 };
        }
        if (selected === side && !isSource) {
            return { backgroundColor: '#FEE2E2', border: '2.5px solid #EF4444', borderRadius: 14, boxShadow: '3px 3px 0px 0px #EF4444' };
        }
        return { backgroundColor: '#FFFFFF', border: '2.5px solid #1C1917', borderRadius: 14, boxShadow: '3px 3px 0px 0px #1C1917' };
    };

    /* Curly arrow SVG: curves from source side to sink side */
    const arrowLR = 'M 6 18 Q 24 -2 42 18'; // left \u2192 right
    const arrowRL = 'M 42 18 Q 24 -2 6 18'; // right \u2192 left
    const headLR = '39,12 45,20 38,20';
    const headRL = '9,12 3,20 10,20';

    return (
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Curly Arrow Drill</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-2">Curly arrows always flow from electron SOURCE to electron SINK.</p>
            <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 mb-6">Click the electron source in each pair.</p>

            {/* Progress */}
            <div className="mb-6">
                <div className="flex items-center justify-between mb-1.5">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">Progress</span>
                    <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400">{Math.min(current + (isCorrect ? 1 : 0), scenarios.length)}/{scenarios.length}</span>
                </div>
                <div className="w-full h-2 bg-zinc-100 dark:bg-zinc-900 rounded-full overflow-hidden">
                    <motion.div
                        className="h-full rounded-full bg-emerald-400"
                        animate={{ width: `${(Math.min(current + (isCorrect ? 1 : 0), scenarios.length) / scenarios.length) * 100}%` }}
                        transition={{ type: 'spring', stiffness: 80, damping: 15 }}
                    />
                </div>
            </div>

            {!done ? (
                <AnimatePresence mode="wait">
                    <motion.div key={current} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}>
                        <p className="text-center text-xs text-zinc-500 dark:text-zinc-400 mb-4">
                            Which is the electron <span className="font-bold text-emerald-600 dark:text-emerald-400">SOURCE</span>?
                        </p>

                        {/* Reaction pair */}
                        <div className="flex items-center justify-center gap-3 mb-4">
                            <button onClick={() => handleSelect('a')} disabled={isCorrect} className="flex-1 max-w-[150px] p-4 text-center transition-all" style={btnStyle('a')}>
                                <p className="text-2xl font-mono font-bold text-zinc-800 dark:text-white">{s.a.formula}</p>
                                <p className="text-[10px] text-zinc-500 dark:text-zinc-400 mt-1">{s.a.label}</p>
                            </button>

                            <div className="flex-shrink-0 w-12 h-6 flex items-center justify-center">
                                {isCorrect ? (
                                    <motion.svg initial={{ opacity: 0 }} animate={{ opacity: 1 }} width="48" height="24" viewBox="0 0 48 24">
                                        <motion.path
                                            d={s.a.isSource ? arrowLR : arrowRL}
                                            fill="none" stroke="#10b981" strokeWidth="2.5" strokeLinecap="round"
                                            initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                                            transition={{ duration: 0.5 }}
                                        />
                                        <motion.polygon
                                            points={s.a.isSource ? headLR : headRL}
                                            fill="#10b981"
                                            initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                                            transition={{ delay: 0.4 }}
                                        />
                                    </motion.svg>
                                ) : (
                                    <span className="text-lg font-bold text-zinc-300 dark:text-zinc-600">+</span>
                                )}
                            </div>

                            <button onClick={() => handleSelect('b')} disabled={isCorrect} className="flex-1 max-w-[150px] p-4 text-center transition-all" style={btnStyle('b')}>
                                <p className="text-2xl font-mono font-bold text-zinc-800 dark:text-white">{s.b.formula}</p>
                                <p className="text-[10px] text-zinc-500 dark:text-zinc-400 mt-1">{s.b.label}</p>
                            </button>
                        </div>

                        {/* Feedback */}
                        <AnimatePresence>
                            {selected && !isCorrect && (
                                <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                                    className="text-center text-xs text-rose-500 dark:text-rose-400 mb-3">
                                    That&apos;s the electron sink &mdash; it&apos;s electron-poor. Try the source.
                                </motion.p>
                            )}
                        </AnimatePresence>
                        {isCorrect && (
                            <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
                                className="p-3 bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-800/40 rounded-xl text-center mb-4"
                            >
                                <p className="text-xs text-emerald-700 dark:text-emerald-300">{s.explanation}</p>
                            </motion.div>
                        )}
                        {isCorrect && (
                            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center">
                                <button onClick={handleNext}
                                    className="px-4 py-2 text-sm font-bold rounded-lg bg-emerald-500 hover:bg-emerald-600 text-white transition-colors">
                                    {current < scenarios.length - 1 ? 'Next Reaction' : 'See Results'}
                                </button>
                            </motion.div>
                        )}
                    </motion.div>
                </AnimatePresence>
            ) : (
                <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                    className="p-5 bg-emerald-50 dark:bg-emerald-950/20 rounded-xl border border-emerald-200 dark:border-emerald-800/40 text-center"
                >
                    <p className="text-3xl font-bold text-emerald-600 dark:text-emerald-400 mb-2">{score}/{scenarios.length}</p>
                    <p className="text-sm font-semibold text-emerald-700 dark:text-emerald-300">
                        {score === scenarios.length ? 'Perfect! You understand the source \u2192 sink principle.' : 'Remember: electrons always flow from rich to poor.'}
                    </p>
                    <p className="text-xs text-emerald-600/70 dark:text-emerald-400/60 mt-2">
                        The curly arrow always starts at the electron source (lone pair or bond) and points to the electron sink (electron-deficient atom).
                    </p>
                </motion.div>
            )}
        </div>
    );
};

// --- KEYWORD PRECISION TESTER ---
const KEYWORD_QUESTIONS = [
  {
    definition: 'The movement of molecules from an area of high concentration to an area of low concentration',
    options: ['Diffusion', 'Osmosis', 'Spreading'],
    correctIndex: 0,
  },
  {
    definition: 'The movement of water from a region of high water concentration to a region of low water concentration across a semi-permeable membrane',
    options: ['Diffusion', 'Osmosis', 'Absorption'],
    correctIndex: 1,
  },
  {
    definition: 'The breakdown of large insoluble molecules into small soluble molecules',
    options: ['Digestion', 'Decomposition', 'Metabolism'],
    correctIndex: 0,
  },
  {
    definition: 'A substance that speeds up a chemical reaction without being used up',
    options: ['Catalyst', 'Enzyme', 'Activator'],
    correctIndex: 0,
  },
  {
    definition: 'An organism that makes its own food',
    options: ['Producer', 'Autotroph', 'Plant'],
    correctIndex: 1,
  },
  {
    definition: 'The process by which green plants make food using sunlight',
    options: ['Respiration', 'Synthesis', 'Photosynthesis'],
    correctIndex: 2,
  },
  {
    definition: 'A change in the structure of a protein due to heat or pH',
    options: ['Denaturation', 'Degradation', 'Destruction'],
    correctIndex: 0,
  },
  {
    definition: 'The basic structural and functional unit of life',
    options: ['Organism', 'Cell', 'Tissue'],
    correctIndex: 1,
  },
  {
    definition: 'An organism that feeds on dead organic matter',
    options: ['Decomposer', 'Saprophyte', 'Scavenger'],
    correctIndex: 1,
  },
  {
    definition: 'A group of similar cells that perform the same function',
    options: ['Organ', 'Tissue', 'System'],
    correctIndex: 1,
  },
];

function fisherYatesShuffle<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

interface ShuffledQuestion {
  definition: string;
  options: string[];
  correctIndex: number;
}

function buildShuffledRound(): ShuffledQuestion[] {
  const shuffledQuestions = fisherYatesShuffle(KEYWORD_QUESTIONS);
  return shuffledQuestions.map((q) => {
    const originalOptions = q.options;
    const correctTerm = originalOptions[q.correctIndex];
    const shuffledOptions = fisherYatesShuffle(originalOptions);
    const newCorrectIndex = shuffledOptions.indexOf(correctTerm);
    return { definition: q.definition, options: shuffledOptions, correctIndex: newCorrectIndex };
  });
}

const KeywordPrecisionTester = () => {
  const [questions, setQuestions] = useState<ShuffledQuestion[]>(() => buildShuffledRound());
  const [current, setCurrent] = useState(0);
  const [score, setScore] = useState(0);
  const [streak, setStreak] = useState(0);
  const [bestStreak, setBestStreak] = useState(0);
  const [selected, setSelected] = useState<number | null>(null);
  const [wasCorrect, setWasCorrect] = useState<boolean | null>(null);
  const [done, setDone] = useState(false);

  const q = questions[current];

  const handleSelect = (idx: number) => {
    if (selected !== null) return;
    setSelected(idx);
    const correct = idx === q.correctIndex;
    setWasCorrect(correct);
    if (correct) {
      setScore((s) => s + 1);
      setStreak((s) => {
        const next = s + 1;
        setBestStreak((b) => Math.max(b, next));
        return next;
      });
    } else {
      setStreak(0);
    }
    const delay = correct ? 1000 : 1500;
    setTimeout(() => {
      if (current < questions.length - 1) {
        setCurrent((c) => c + 1);
        setSelected(null);
        setWasCorrect(null);
      } else {
        setDone(true);
      }
    }, delay);
  };

  const handlePlayAgain = () => {
    setQuestions(buildShuffledRound());
    setCurrent(0);
    setScore(0);
    setStreak(0);
    setSelected(null);
    setWasCorrect(null);
    setDone(false);
  };

  const resultMessage =
    score >= 9
      ? "Examiner-ready precision. You're speaking the marking scheme's language."
      : score >= 6
        ? 'Good, but a few synonyms slipped in. Each wrong keyword is a lost mark.'
        : "The synonyms feel right, but the examiner only accepts exact terms. This is Biology's hidden trap.";

  const optionBtnStyle = (idx: number): React.CSSProperties => {
    if (selected === null) {
      return { backgroundColor: '#FFFFFF', border: '2.5px solid #1C1917', borderRadius: 14, boxShadow: '3px 3px 0px 0px #1C1917' };
    }
    if (idx === q.correctIndex) {
      return { backgroundColor: '#D1FAE5', border: '2.5px solid #059669', borderRadius: 14, boxShadow: '3px 3px 0px 0px #059669' };
    }
    if (idx === selected && idx !== q.correctIndex) {
      return { backgroundColor: '#FEE2E2', border: '2.5px solid #EF4444', borderRadius: 14, boxShadow: '3px 3px 0px 0px #EF4444', opacity: 0.8 };
    }
    return { backgroundColor: '#FFFFFF', border: '2.5px solid #1C1917', borderRadius: 14, boxShadow: '3px 3px 0px 0px #1C1917', opacity: 0.5 };
  };

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Keyword Precision Tester</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">
        In Biology, close enough is zero marks. Only the exact SEC keyword scores.
      </p>

      {/* Stats pills */}
      <div className="flex items-center justify-center gap-3 mb-6">
        <span className="px-3 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/20 text-xs font-bold text-emerald-700 dark:text-emerald-300">
          Score: {score}/{questions.length}
        </span>
        <span className="px-3 py-1 rounded-full bg-zinc-100 dark:bg-zinc-900 text-xs font-bold text-zinc-600 dark:text-zinc-300">
          Streak: {streak}
        </span>
        <span className="px-3 py-1 rounded-full bg-zinc-100 dark:bg-zinc-900 text-xs font-bold text-zinc-600 dark:text-zinc-300">
          Best: {bestStreak}
        </span>
      </div>

      {/* Progress bar */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">Progress</span>
          <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400">
            {done ? questions.length : current}/{questions.length}
          </span>
        </div>
        <div className="w-full h-2 bg-zinc-100 dark:bg-zinc-900 rounded-full overflow-hidden">
          <motion.div
            className="h-full rounded-full bg-emerald-400"
            animate={{ width: `${((done ? questions.length : current) / questions.length) * 100}%` }}
            transition={{ type: 'spring', stiffness: 80, damping: 15 }}
          />
        </div>
      </div>

      {!done ? (
        <AnimatePresence mode="wait">
          <MotionDiv key={current} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}>
            {/* Definition card */}
            <div className="p-5 bg-zinc-50 dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-700 mb-5">
              <p className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 mb-2">Definition</p>
              <p className="text-base font-medium text-zinc-800 dark:text-white leading-relaxed">{q.definition}</p>
            </div>

            {/* Option buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3 mb-5">
              {q.options.map((opt, idx) => (
                <button
                  key={opt}
                  onClick={() => handleSelect(idx)}
                  disabled={selected !== null}
                  className="px-5 py-3 text-sm font-semibold transition-all text-zinc-700 dark:text-zinc-200"
                  style={optionBtnStyle(idx)}
                >
                  {opt}
                </button>
              ))}
            </div>

            {/* Feedback */}
            <AnimatePresence>
              {wasCorrect === true && (
                <MotionDiv initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}
                  className="p-3 bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-800/40 rounded-xl text-center">
                  <p className="text-xs text-emerald-700 dark:text-emerald-300">
                    Correct — this is the exact term the examiner is looking for.
                  </p>
                </MotionDiv>
              )}
              {wasCorrect === false && (
                <MotionDiv initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}
                  className="p-3 bg-rose-50 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-800/40 rounded-xl text-center">
                  <p className="text-xs text-rose-700 dark:text-rose-300">
                    Close, but the marking scheme specifically requires <strong>{q.options[q.correctIndex]}</strong>.
                  </p>
                </MotionDiv>
              )}
            </AnimatePresence>
          </MotionDiv>
        </AnimatePresence>
      ) : (
        <MotionDiv initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
          className="p-6 bg-emerald-50 dark:bg-emerald-950/20 rounded-xl border border-emerald-200 dark:border-emerald-800/40 text-center">
          <p className="text-4xl font-bold text-emerald-600 dark:text-emerald-400 mb-2">{score}/{questions.length}</p>
          <p className="text-sm font-semibold text-emerald-700 dark:text-emerald-300 mb-3">{resultMessage}</p>
          <div className="flex items-center justify-center gap-3 mb-4">
            <span className="px-3 py-1 rounded-full bg-white dark:bg-zinc-800 text-xs font-bold text-zinc-600 dark:text-zinc-300">
              Best Streak: {bestStreak}
            </span>
          </div>
          <button onClick={handlePlayAgain}
            className="px-5 py-2.5 text-sm font-bold rounded-lg bg-emerald-500 hover:bg-emerald-600 text-white transition-colors">
            Play Again
          </button>
        </MotionDiv>
      )}
    </div>
  );
};

// --- MODULE COMPONENT ---
const MasteringTheSciencesModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'hidden-curriculum', title: 'What They Don\'t Teach You', eyebrow: '01 // The Big Picture', icon: Key },
    { id: 'biology', title: 'Biology: Every Word Counts', eyebrow: '02 // Know Your Keywords', icon: Leaf },
    { id: 'chemistry', title: 'Chemistry: Seeing the Molecules', eyebrow: '03 // Build the Logic', icon: Beaker },
    { id: 'physics', title: 'Physics: Problem-Solving Mindset', eyebrow: '04 // Think It Through', icon: Atom },
    { id: 'ag-science', title: 'Ag Science: Think Like a Scientist', eyebrow: '05 // Get Investigative', icon: Sprout },
    { id: 'cognitive-strategies', title: 'Study Smarter for Science', eyebrow: '06 // Your Toolkit', icon: BrainCircuit },
    { id: 'action-plan', title: 'Your Action Plan', eyebrow: '07 // Get Started', icon: Flag },
  ];

  return (
    <ModuleLayout
      moduleNumber="04"
      moduleTitle="Mastering the Sciences"
      moduleSubtitle="Your Science Subjects, Decoded"
      moduleDescription="Each science exam has its own unwritten rules. This module breaks them down so you know exactly what the examiner is looking for."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Decode the Exams"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="What They Don't Teach You." eyebrow="Step 1" icon={Key} theme={theme}>
              {essentials ? (
                <>
                  <p>Each science subject has unwritten rules. The marking scheme rewards certain approaches. If you do not know them, you lose marks even when you understand the material. This module shows you what the examiner actually wants for each subject.</p>
                  <PersonalStory name="Róisín" role="6th Year, Tullamore">
                    <p>I was getting B3s in Biology even though I was studying loads. Turns out I was using my own words for definitions instead of the exact terms from the book. Once I started learning the keywords the examiner wanted, my marks jumped two grades in the mocks. It felt like I'd been playing the wrong game the whole time.</p>
                  </PersonalStory>
                </>
              ) : (
                <>
                  <p>Here's the thing about the Leaving Cert sciences: knowing your stuff is only half the battle. Each subject -- Biology, Chemistry, Physics, and Ag Science -- has its own set of unwritten rules. The marking scheme rewards certain approaches, and if you don't know what those are, you'll lose marks even when you understand the material.</p>
                  <p>This module breaks down each science subject so you can see what the examiner is actually looking for. You'll learn which topics come up most, which mistakes cost the most marks, and how to write answers that tick every box on the marking scheme.</p>
                  <PersonalStory name="Róisín" role="6th Year, Tullamore">
                    <p>I was getting B3s in Biology even though I was studying loads. Turns out I was using my own words for definitions instead of the exact terms from the book. Once I started learning the keywords the examiner wanted, my marks jumped two grades in the mocks. It felt like I'd been playing the wrong game the whole time.</p>
                  </PersonalStory>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Biology: Every Word Counts." eyebrow="Step 2" icon={Leaf} theme={theme}>
              {essentials ? (
                <p>The biggest trap in Biology is <Highlight description="The examiner only accepts the exact keyword from the marking scheme." theme={theme}>using the exact right words</Highlight>. "Spreading out" instead of "diffusion" gets zero marks. Learn definitions word-for-word. Know all 22 mandatory experiments. Watch the <Highlight description="Writing more answers than asked can cancel a correct one." theme={theme}>extra answer trap</Highlight>: only answer what is asked.</p>
              ) : (
                <p>Biology is massive -- there's a lot to learn. But the biggest trap isn't the volume of content, it's <Highlight description="The examiner wants the exact keyword from the marking scheme. If it says 'diffusion', writing 'spreading out' gets zero marks, even if you understand the concept perfectly." theme={theme}>using the exact right words</Highlight>. If the marking scheme says "diffusion" and you write "spreading out", you get zero -- even though you clearly know what you're talking about. Definitions need to be learned word-for-word. The exam is split into short questions, experiment questions, and long questions. Make sure you know all 22 mandatory experiments -- they come up every year. And watch out for the <Highlight description="If a question asks for two examples and you write three, a wrong third answer can cancel out a correct one. Only answer what's asked." theme={theme}>extra answer trap</Highlight> in short questions: if you write more answers than asked for and one is wrong, it can cancel out a right one.</p>
              )}
              <KeywordPrecisionTester />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Chemistry: Seeing the Molecules." eyebrow="Step 3" icon={Beaker} theme={theme}>
              {essentials ? (
                <p>Section A (experiments) is your <Highlight description="Predictable questions worth up to 38% of your grade." theme={theme}>easiest source of marks</Highlight>. Know titrations cold. Organic Chemistry is 40% of the paper. Learn reaction pathways and <Highlight description="Arrows showing where electrons move in a reaction." theme={theme}>curly arrows</Highlight>. Never draw carbon with five bonds. For calculations, always start by converting to moles.</p>
              ) : (
                <>
                  <p>Chemistry is about two things: picturing what molecules are doing and being able to do the calculations. The experiment section (Section A) is your <Highlight description="The experiment questions are very predictable -- titrations come up nearly every year. Nailing these can be worth up to 38% of your total grade." theme={theme}>easiest source of marks</Highlight> because the same types of questions keep coming up. Get your titration steps down cold and know how to draw the apparatus.</p>
                  <p>Organic Chemistry makes up about 40% of the paper, so it's worth serious time. You need to know your reaction pathways and understand <Highlight description="Curly arrows show where electrons move. They always start from where electrons are (a lone pair or a bond) and point to where they're going. Drawing them wrong loses you marks." theme={theme}>curly arrows</Highlight> for reaction mechanisms. A classic mistake is drawing a carbon with five bonds instead of four -- that's an instant zero. For calculations, always start by converting to moles. It's the foundation of every chemistry calculation.</p>
                </>
              )}
              <CurlyArrowDrill />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Physics: Problem-Solving Mindset." eyebrow="Step 4" icon={Atom} theme={theme}>
              {essentials ? (
                <p>Experiments give you reliable marks. Learn <Highlight description="Independent variable on X-axis. Use line of best fit for slope." theme={theme}>graphs properly</Highlight>. Memorise derivations including geometry steps. When stuck, <Highlight description="If units do not match on both sides, something is wrong." theme={theme}>check your units</Highlight>. The top mistake is forgetting to convert cm to m. Always set your calculator to Degree mode for trig.</p>
              ) : (
                <>
                  <p>Physics is about applying ideas to problems you might not have seen before. The experiment section is where you pick up reliable marks if you know the basics of <Highlight description="Always put the thing you changed (independent variable) on the X-axis. Calculate slope from the line of best fit, not from random points in your table." theme={theme}>drawing and reading graphs properly</Highlight>. Learn all your derivations by heart -- including the geometry steps, not just the final formula.</p>
                  <p>When you hit a tricky question, your best friend is <Highlight description="You can use units to figure out or double-check a formula. If Force is in Newtons and Area is in metres squared, then Pressure must be in Newtons per metre squared." theme={theme}>checking your units</Highlight>. If the units on both sides of your equation don't match, something has gone wrong. The number one reason students lose marks in Physics? Forgetting to convert cm to m. Also, always check your calculator is in <strong>Degree</strong> mode before doing any trig.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Ag Science: Think Like a Scientist." eyebrow="Step 5" icon={Sprout} theme={theme}>
              {essentials ? (
                <p>The <Highlight description="A research project worth 25% of your grade." theme={theme}>IIS</Highlight> is worth 25%. You need a clear testable question and real data. The written paper asks you to <Highlight description="Linking ideas from different parts of the course." theme={theme}>connect ideas across topics</Highlight>. Link Crops to Environment, for example. Treat experiment questions with the same detail as Biology or Physics.</p>
              ) : (
                <>
                  <p>Ag Science has changed a lot -- it's not just about farming facts anymore, it's about thinking scientifically. The <Highlight description="This is a big research project worth 25% of your total grade. You need a clear question you can test, a proper experiment, and real data analysis. A vague or descriptive project will lose you serious marks." theme={theme}>Individual Investigative Study (IIS)</Highlight> is worth a quarter of your grade, so it needs proper effort. You need a clear, testable question and a proper write-up with real data -- not just a description of what you did.</p>
                  <p>The written paper now asks you to <Highlight description="This means connecting ideas across different parts of the course. For example, how fertiliser use in the Crops section links to water quality in the Environment section." theme={theme}>connect ideas across topics</Highlight>, not just memorise isolated facts. You might need to link something from the Crops section to the Environment section, for example. The experiment questions are just as detailed as Biology or Physics, so treat them with the same care.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Study Smarter for Science." eyebrow="Step 6" icon={BrainCircuit} theme={theme}>
              {essentials ? (
                <p>Stop re-reading notes. Start <Highlight description="Mix Physics, Chemistry, and Biology in one session." theme={theme}>mixing up your topics</Highlight> in each session. It feels harder but you learn faster. For definitions, combine <Highlight description="Write definitions from memory without looking." theme={theme}>testing yourself from memory</Highlight> with <Highlight description="Review at increasing gaps: 1 day, 3 days, 1 week, 1 month." theme={theme}>spaced revision</Highlight>. Use Anki or Quizlet for the scheduling.</p>
              ) : (
                <>
                  <p>If you're just re-reading your notes over and over, you're wasting time. One of the best things you can do for science subjects is <Highlight description="Instead of studying one topic for ages, mix it up. Do a Physics problem, then a Chemistry equation, then a Biology definition. It feels harder, but it trains your brain to switch between different types of thinking." theme={theme}>mixing up your topics</Highlight> within a single study session. Instead of doing an hour of just Biology, try doing a Physics problem, then a Chemistry equation, then a Biology definition all in the same 90-minute block. It feels harder, but that's the point -- your brain gets better at telling different types of problems apart.</p>
                  <p>For memorising the hundreds of definitions in Biology and Ag Science, the winning combination is <Highlight description="Instead of just reading definitions, close your book and try to write them from memory. The effort of pulling the information out of your brain is what makes it stick." theme={theme}>testing yourself from memory</Highlight> and <Highlight description="Review your flashcards or notes at increasing gaps -- after 1 day, then 3 days, then a week, then a month. Free apps like Anki or Quizlet can automate this for you." theme={theme}>spacing out your revision</Highlight>. Free apps like Anki or Quizlet can handle the scheduling for you -- you just need to show up and do the reps.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="Your Action Plan." eyebrow="Step 7" icon={Flag} theme={theme}>
              {essentials ? (
                <p>You now know the unwritten rules for each science. Getting a H1 is about knowing the game, not grinding harder.</p>
              ) : (
                <p>You now know the unwritten rules for each of the Leaving Cert sciences. You know what the examiner is actually looking for and which study methods work best for these subjects. Getting a H1 isn't about grinding harder -- it's about knowing the game you're playing and making every study session count.</p>
              )}
              <MicroCommitment theme={theme}>
                <p>Pick ONE subject. Go to the SEC website (examinations.ie) and download the most recent Chief Examiner's Report for that subject. Read just the "Recommendations to Candidates" section. It's basically the examiner telling you exactly what to do differently -- and it's free.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default MasteringTheSciencesModule;
