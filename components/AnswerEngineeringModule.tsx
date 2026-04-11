/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { AlertTriangle, Layers, FlaskConical, BarChart2, LifeBuoy, Wrench, Target } from 'lucide-react';
import { type ModuleProgress } from '../types';
import { redTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory, ConceptCardGrid } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = redTheme;

// --- INTERACTIVE COMPONENTS ---

// PEEL Builder
const peelExamples = [
  {
    subject: 'History',
    question: 'Why did the 1916 Rising fail militarily?',
    sentences: [
      { text: 'The rebels were vastly outnumbered, with approximately 1,600 volunteers facing 16,000 British troops by the end of the week.', type: 'E' },
      { text: 'The 1916 Rising was doomed to fail militarily due to a critical imbalance in manpower and resources.', type: 'P' },
      { text: 'This overwhelming numerical disadvantage, combined with British artillery, made it impossible to hold key positions like the GPO for more than five days.', type: 'E2' },
      { text: 'This demonstrates that the Rising was never intended as a winnable military campaign, but rather as a symbolic act of defiance.', type: 'L' },
    ],
    correctOrder: [1, 0, 2, 3],
  },
  {
    subject: 'Business',
    question: 'Evaluate the impact of technology on marketing.',
    sentences: [
      { text: 'For example, Ryanair uses targeted social media ads and dynamic pricing algorithms to reach specific customer segments at optimal times.', type: 'E' },
      { text: 'This shows that technology has fundamentally shifted marketing from broadcast to precision, enabling businesses to maximise ROI on their marketing spend.', type: 'L' },
      { text: 'Technology has revolutionised marketing by enabling businesses to target consumers with unprecedented accuracy.', type: 'P' },
      { text: 'This targeted approach allows Ryanair to reduce wasted advertising spend while increasing conversion rates, something impossible with traditional newspaper or TV advertising.', type: 'E2' },
    ],
    correctOrder: [2, 0, 3, 1],
  },
  {
    subject: 'Geography',
    question: 'Explain how human activity contributes to soil erosion.',
    sentences: [
      { text: 'Deforestation is one of the primary ways human activity accelerates soil erosion.', type: 'P' },
      { text: 'In the Amazon basin, areas cleared for cattle ranching lose up to 40 tonnes of topsoil per hectare annually, compared to less than 1 tonne under intact forest cover.', type: 'E' },
      { text: 'Without tree root systems to anchor the soil and canopy to break rainfall impact, exposed soil is directly vulnerable to both water erosion (splash and sheet) and wind erosion.', type: 'E2' },
      { text: 'This illustrates how removing natural vegetation cover disrupts the soil system and creates a cycle of degradation that is extremely difficult to reverse.', type: 'L' },
    ],
    correctOrder: [0, 1, 2, 3],
  },
];

const peelLabels: Record<string, { label: string; color: string; bg: string; border: string; hex: string }> = {
  P: { label: 'Point', color: 'text-blue-700 dark:text-blue-300', bg: 'bg-blue-100 dark:bg-blue-900/30', border: 'border-blue-300 dark:border-blue-700', hex: '#2563EB' },
  E: { label: 'Evidence', color: 'text-amber-700 dark:text-amber-300', bg: 'bg-amber-100 dark:bg-amber-900/30', border: 'border-amber-300 dark:border-amber-700', hex: '#D97706' },
  E2: { label: 'Explain', color: 'text-teal-700 dark:text-teal-300', bg: 'bg-teal-100 dark:bg-teal-900/30', border: 'border-teal-300 dark:border-teal-700', hex: '#059669' },
  L: { label: 'Link', color: 'text-purple-700 dark:text-purple-300', bg: 'bg-purple-100 dark:bg-purple-900/30', border: 'border-purple-300 dark:border-purple-700', hex: '#7C3AED' },
};

const PEELBuilder = () => {
  const [exampleIndex, setExampleIndex] = useState(0);
  const [phase, setPhase] = useState<'building' | 'result'>('building');
  const [placed, setPlaced] = useState<(number | null)[]>([null, null, null, null]);
  const [score, setScore] = useState(0);

  const ex = peelExamples[exampleIndex];

  const placedSet = new Set(placed.filter(p => p !== null));
  const availableSentences = ex.sentences.map((_, i) => i).filter(i => !placedSet.has(i));

  const handlePlaceSentence = (sentenceIndex: number) => {
    const firstEmpty = placed.indexOf(null);
    if (firstEmpty === -1) return;
    const newPlaced = [...placed];
    newPlaced[firstEmpty] = sentenceIndex;
    setPlaced(newPlaced);
  };

  const handleRemoveFromSlot = (slotIndex: number) => {
    if (phase === 'result') return;
    const newPlaced = [...placed];
    newPlaced[slotIndex] = null;
    setPlaced(newPlaced);
  };

  const handleSubmit = () => {
    const correct = placed.map((p, i) => p === ex.correctOrder[i]).filter(Boolean).length;
    setScore(correct);
    setPhase('result');
  };

  const handleNextExample = () => {
    const next = exampleIndex + 1;
    if (next < peelExamples.length) {
      setExampleIndex(next);
      setPlaced([null, null, null, null]);
      setPhase('building');
      setScore(0);
    }
  };

  const handleReset = () => {
    setExampleIndex(0);
    setPlaced([null, null, null, null]);
    setPhase('building');
    setScore(0);
  };

  const slotLabels = ['P', 'E', 'E2', 'L'];
  const allPlaced = placed.every(p => p !== null);

  return (
    <div className="my-10 p-6 md:p-10 rounded-xl border border-zinc-200 dark:border-zinc-700 bg-[#FAF7F4] dark:bg-zinc-800">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">PEEL Builder</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-1 mb-2">Arrange the sentences in the correct PEEL order.</p>

      {/* Subject tabs */}
      <div className="flex gap-2 mb-4 justify-center">
        {peelExamples.map((e, i) => (
          <button key={i} onClick={() => { if (phase === 'building') { setExampleIndex(i); setPlaced([null, null, null, null]); } }}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-colors ${
              exampleIndex === i ? 'bg-red-500 text-white' : 'bg-zinc-100 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-300 hover:bg-zinc-200 dark:hover:bg-zinc-600'
            }`}>
            {e.subject}
          </button>
        ))}
      </div>

      {/* Question */}
      <div className="text-center mb-5">
        <span className="text-xs font-bold uppercase tracking-wider text-zinc-400">{ex.subject}</span>
        <p className="font-serif text-lg font-semibold text-zinc-800 dark:text-white mt-1">{ex.question}</p>
      </div>

      {/* Slots */}
      <div className="space-y-3 mb-5">
        {slotLabels.map((label, slotIdx) => {
          const sentIdx = placed[slotIdx];
          const pl = peelLabels[label];
          const isCorrect = phase === 'result' && sentIdx === ex.correctOrder[slotIdx];
          const isWrong = phase === 'result' && sentIdx !== null && sentIdx !== ex.correctOrder[slotIdx];
          const correctSentIdx = phase === 'result' ? ex.correctOrder[slotIdx] : null;
          const borderColor = isCorrect ? '#059669' : isWrong ? '#DC2626' : '#1C1917';

          return (
            <div key={slotIdx}>
              <div
                className="bg-white dark:bg-zinc-900 transition-all"
                style={{ border: `2.5px solid ${borderColor}`, borderRadius: 18, boxShadow: `4px 4px 0px 0px ${borderColor}`, overflow: 'hidden' }}
              >
                {/* Header bar */}
                <div
                  className="text-[13px] font-medium tracking-wider uppercase text-white text-center"
                  style={{ backgroundColor: pl.hex, padding: '10px 16px', borderBottom: `2.5px solid ${borderColor}` }}
                >
                  {slotIdx + 1}. {pl.label}
                </div>
                {/* Body */}
                <div
                  className={`p-4 min-h-[56px] flex items-center ${sentIdx !== null && phase === 'building' ? 'cursor-pointer' : ''}`}
                  onClick={() => sentIdx !== null && phase === 'building' ? handleRemoveFromSlot(slotIdx) : undefined}
                >
                  {sentIdx !== null ? (
                    <div
                      className="text-[13px] text-zinc-700 dark:text-zinc-200 w-full"
                      style={{ backgroundColor: '#FFFFFF', border: `2px solid ${pl.hex}`, borderRadius: 12, boxShadow: `2px 2px 0px 0px ${pl.hex}`, padding: '8px 12px' }}
                    >
                      {ex.sentences[sentIdx].text}
                    </div>
                  ) : (
                    <span className="text-sm text-zinc-400 dark:text-zinc-500 italic">Click a sentence below to place it here</span>
                  )}
                </div>
              </div>
              {isWrong && correctSentIdx !== null && (
                <div className="mt-1 ml-2 text-xs text-emerald-600 dark:text-emerald-400 italic">
                  Correct: {ex.sentences[correctSentIdx].text.slice(0, 80)}...
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Available sentences */}
      {phase === 'building' && availableSentences.length > 0 && (
        <div className="space-y-2 mb-5">
          <p className="text-xs font-bold uppercase tracking-wider text-zinc-400 mb-2">Available sentences</p>
          {availableSentences.map(i => (
            <button key={i} onClick={() => handlePlaceSentence(i)}
              className="w-full text-left p-3 rounded-lg border border-zinc-200 dark:border-zinc-600 bg-white dark:bg-zinc-800 text-sm text-zinc-700 dark:text-zinc-200 hover:border-teal-400 dark:hover:border-teal-600 hover:bg-teal-50 dark:hover:bg-teal-900/20 transition-all cursor-pointer"
              style={{ borderColor: undefined }}>
              {ex.sentences[i].text}
            </button>
          ))}
        </div>
      )}

      {/* Actions */}
      <div className="text-center">
        {phase === 'building' && allPlaced && (
          <button onClick={handleSubmit} className="px-6 py-3 bg-red-500 hover:bg-red-600 text-white font-bold text-sm rounded-lg transition-colors">
            Check Order
          </button>
        )}
        {phase === 'result' && (
          <MotionDiv initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
            <div className="flex justify-center my-4">
              <div className="text-center px-5 py-3 rounded-xl bg-zinc-100 dark:bg-zinc-700">
                <div className="text-2xl font-bold text-zinc-800 dark:text-white">{score}/4</div>
                <div className="text-xs font-semibold text-zinc-500 dark:text-zinc-400 mt-0.5">Correct</div>
              </div>
            </div>
            {exampleIndex < peelExamples.length - 1 ? (
              <button onClick={handleNextExample} className="px-5 py-2.5 bg-red-500 hover:bg-red-600 text-white font-bold text-sm rounded-lg transition-colors">
                Next Example
              </button>
            ) : (
              <button onClick={handleReset} className="px-5 py-2.5 bg-red-500 hover:bg-red-600 text-white font-bold text-sm rounded-lg transition-colors">
                Try Again
              </button>
            )}
          </MotionDiv>
        )}
      </div>
    </div>
  );
};

// Stack Builder (Science Answer Stack)
const stackProblem = {
  question: 'A car accelerates from 10 m/s to 30 m/s in 5 seconds. Calculate the acceleration.',
  steps: [
    {
      label: 'State the formula',
      correct: 'a = (v - u) / t',
      wrong: ['a = v \u00d7 t', 's = ut + \u00bdat\u00b2'],
      marks: 3,
    },
    {
      label: 'Substitute values',
      correct: 'a = (30 - 10) / 5',
      wrong: ['a = 30 \u00d7 5', 'a = (10 - 30) / 5'],
      marks: 3,
    },
    {
      label: 'Solve',
      correct: 'a = 20 / 5 = 4',
      wrong: ['a = 150', 'a = 20'],
      marks: 3,
    },
    {
      label: 'Final answer with units',
      correct: 'a = 4 m/s\u00b2',
      wrong: ['a = 4', 'a = 4 m/s'],
      marks: 3,
    },
  ],
  totalMarks: 12,
};

const StackBuilder = () => {
  const [phase, setPhase] = useState<'ready' | 'building' | 'done'>('ready');
  const [stepIndex, setStepIndex] = useState(0);
  const [choices, setChoices] = useState<(string | null)[]>(Array(stackProblem.steps.length).fill(null));
  const [showStepFeedback, setShowStepFeedback] = useState(false);
  const [shuffledOptions, setShuffledOptions] = useState<string[][]>([]);
  const timerRef = React.useRef<ReturnType<typeof setTimeout> | null>(null);

  React.useEffect(() => {
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, []);

  const startBuild = () => {
    // Shuffle options for each step
    const shuffled = stackProblem.steps.map(step => {
      const opts = [step.correct, ...step.wrong];
      for (let i = opts.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [opts[i], opts[j]] = [opts[j], opts[i]];
      }
      return opts;
    });
    setShuffledOptions(shuffled);
    setPhase('building');
    setStepIndex(0);
    setChoices(Array(stackProblem.steps.length).fill(null));
    setShowStepFeedback(false);
  };

  const handleChoice = (choice: string) => {
    if (showStepFeedback) return;
    const newChoices = [...choices];
    newChoices[stepIndex] = choice;
    setChoices(newChoices);
    setShowStepFeedback(true);
    timerRef.current = setTimeout(() => {
      setShowStepFeedback(false);
      if (stepIndex + 1 >= stackProblem.steps.length) {
        setPhase('done');
      } else {
        setStepIndex(s => s + 1);
      }
    }, 2000);
  };

  const earnedMarks = choices.reduce((sum, c, i) => sum + (c === stackProblem.steps[i].correct ? stackProblem.steps[i].marks : 0), 0);

  if (phase === 'ready') {
    return (
      <div className="my-10 p-8 md:p-12 rounded-xl border border-zinc-200 dark:border-zinc-700 text-center bg-[#FAF7F4] dark:bg-zinc-800">
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white">Stack Builder</h4>
        <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-2 max-w-md mx-auto">Build a science answer step by step and see how marks accumulate.</p>
        <div className="p-4 bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-600 mb-5 max-w-md mx-auto">
          <p className="text-xs font-bold uppercase tracking-wider text-zinc-400 mb-1">Physics Problem</p>
          <p className="text-sm font-semibold text-zinc-800 dark:text-white">{stackProblem.question}</p>
        </div>
        <button onClick={startBuild} className="px-6 py-3 bg-red-500 hover:bg-red-600 text-white font-bold text-sm rounded-lg transition-colors">Start Building</button>
      </div>
    );
  }

  if (phase === 'done') {
    return (
      <div className="my-10 p-6 md:p-10 rounded-xl border border-zinc-200 dark:border-zinc-700 bg-[#FAF7F4] dark:bg-zinc-800">
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Stack Builder Results</h4>
        <div className="flex justify-center my-5">
          <div className="text-center px-5 py-3 rounded-xl bg-zinc-100 dark:bg-zinc-700">
            <div className="text-2xl font-bold text-zinc-800 dark:text-white">{earnedMarks}/{stackProblem.totalMarks}</div>
            <div className="text-xs font-semibold text-zinc-500 dark:text-zinc-400 mt-0.5">Marks Earned</div>
          </div>
        </div>
        <div className="space-y-2.5 mb-6">
          {stackProblem.steps.map((step, i) => {
            const got = choices[i];
            const correct = got === step.correct;
            return (
              <div key={i} className={`p-3 rounded-lg border ${correct ? 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-300 dark:border-emerald-700' : 'bg-rose-50 dark:bg-rose-900/20 border-rose-300 dark:border-rose-700'}`}>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-bold text-zinc-500">{step.label}</span>
                  <span className={`text-xs font-bold ${correct ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}`}>
                    {correct ? `+${step.marks} marks` : '0 marks'}
                  </span>
                </div>
                <p className="text-sm font-mono text-zinc-700 dark:text-zinc-200">{got}</p>
                {!correct && (
                  <p className="text-xs text-emerald-600 dark:text-emerald-400 mt-1 italic">Correct: {step.correct}</p>
                )}
              </div>
            );
          })}
        </div>
        <p className="text-sm text-zinc-500 dark:text-zinc-400 text-center mb-4 italic">
          {earnedMarks === stackProblem.totalMarks
            ? 'Perfect! Every step earned its marks.'
            : earnedMarks >= stackProblem.totalMarks * 0.75
            ? 'Great work! Even the steps you got right earned marks independently.'
            : 'Notice how each correct step earns marks independently. Even with mistakes, the right steps still count.'}
        </p>
        <div className="text-center">
          <button onClick={startBuild} className="px-5 py-2.5 bg-red-500 hover:bg-red-600 text-white font-bold text-sm rounded-lg transition-colors">Try Again</button>
        </div>
      </div>
    );
  }

  const step = stackProblem.steps[stepIndex];
  const isCorrect = showStepFeedback && choices[stepIndex] === step.correct;
  const isWrong = showStepFeedback && choices[stepIndex] !== step.correct;

  return (
    <div className="my-10 p-6 md:p-10 rounded-xl border border-zinc-200 dark:border-zinc-700 bg-[#FAF7F4] dark:bg-zinc-800">
      <div className="flex items-center justify-between mb-2">
        <h4 className="font-serif text-lg font-semibold text-zinc-800 dark:text-white">Stack Builder</h4>
        <span className="text-xs font-bold text-zinc-400">Step {stepIndex + 1} / {stackProblem.steps.length}</span>
      </div>

      {/* Question reminder */}
      <div className="p-3 bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-600 mb-4">
        <p className="text-xs text-zinc-400 font-bold mb-0.5">Question</p>
        <p className="text-sm text-zinc-700 dark:text-zinc-200">{stackProblem.question}</p>
      </div>

      {/* Running marks */}
      <div className="flex items-center gap-2 mb-4">
        <span className="text-xs font-bold text-zinc-400">Marks so far:</span>
        <div className="flex-1 h-2 bg-zinc-200 dark:bg-zinc-600 rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-teal-500 rounded-full"
            animate={{ width: `${(earnedMarks / stackProblem.totalMarks) * 100}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
        <span className="text-xs font-bold text-teal-600 dark:text-teal-400">{earnedMarks}/{stackProblem.totalMarks}</span>
      </div>

      {/* Step prompt */}
      <AnimatePresence mode="wait">
        <motion.div key={stepIndex} initial={{ opacity: 0, x: 24 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -24 }}
          className={`p-5 rounded-xl border mb-5 transition-colors ${
            isCorrect ? 'bg-emerald-50 dark:bg-emerald-900/30 border-emerald-300 dark:border-emerald-700' :
            isWrong ? 'bg-rose-50 dark:bg-rose-900/30 border-rose-300 dark:border-rose-700' :
            'bg-white dark:bg-zinc-800 border-zinc-200 dark:border-zinc-600'
          }`}>
          <p className="text-xs font-bold uppercase tracking-wider text-zinc-400 mb-2">{step.label}</p>
          <p className="text-sm text-zinc-600 dark:text-zinc-300">Choose the correct step worth <strong>{step.marks} marks</strong>:</p>
          {showStepFeedback && (
            <motion.p initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }}
              className={`text-xs mt-3 italic ${isCorrect ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}`}>
              {isCorrect ? `Correct! +${step.marks} marks` : `Not quite. The correct step was: ${step.correct}`}
            </motion.p>
          )}
        </motion.div>
      </AnimatePresence>

      {/* Options */}
      <div className="space-y-2">
        {shuffledOptions[stepIndex]?.map((opt, i) => {
          const selected = showStepFeedback && choices[stepIndex] === opt;
          const isAnswer = showStepFeedback && opt === step.correct;
          return (
            <button key={i} onClick={() => handleChoice(opt)} disabled={showStepFeedback}
              className={`w-full text-left p-3 rounded-xl font-mono text-sm border transition-all ${
                isAnswer ? 'bg-emerald-50 dark:bg-emerald-900/30 border-emerald-400 dark:border-emerald-600 ring-2 ring-emerald-500 ring-offset-1' :
                selected && !isAnswer ? 'bg-rose-50 dark:bg-rose-900/30 border-rose-400 dark:border-rose-600' :
                'bg-white dark:bg-zinc-800 border-zinc-200 dark:border-zinc-600 hover:border-teal-400 dark:hover:border-teal-600 hover:bg-teal-50 dark:hover:bg-teal-900/20'
              } ${showStepFeedback ? 'cursor-default' : 'cursor-pointer'}`}>
              {opt}
            </button>
          );
        })}
      </div>

      {/* Progress dots */}
      <div className="flex justify-center gap-1.5 mt-5">
        {stackProblem.steps.map((_, i) => (
          <div key={i} className={`w-2 h-2 rounded-full transition-colors ${
            i < stepIndex ? (choices[i] === stackProblem.steps[i].correct ? 'bg-emerald-500' : 'bg-rose-500') :
            i === stepIndex ? 'bg-red-500' : 'bg-zinc-200 dark:bg-zinc-600'
          }`} />
        ))}
      </div>
    </div>
  );
};

// Shape Quiz (Marks-Shape Connection)
const shapeQuestions = [
  { marks: '(6 marks)', correct: 'Two clear sentences \u2014 name and briefly explain', wrong: ['A full page essay', 'Just one word'] },
  { marks: '(3 \u00d7 5 marks)', correct: 'Three separate short paragraphs, one per point', wrong: ['One long paragraph covering everything', 'Three single words'] },
  { marks: '(30 marks)', correct: 'A structured essay with intro, 3-4 body paragraphs, conclusion', wrong: ['A list of 30 bullet points', 'Two short paragraphs'] },
  { marks: '(2 \u00d7 8 marks)', correct: 'Two developed points with evidence, roughly equal length', wrong: ['One very detailed point and one brief mention', 'Eight short sentences'] },
  { marks: '(4 marks)', correct: 'One or two clear sentences', wrong: ['A full paragraph with examples', 'A diagram'] },
  { marks: '(20 marks)', correct: 'A mini-essay: short intro, 2-3 body paragraphs, brief conclusion', wrong: ['A single long paragraph', 'Twenty separate points'] },
];

const ShapeQuiz = () => {
  const [phase, setPhase] = useState<'ready' | 'quiz' | 'done'>('ready');
  const [qIndex, setQIndex] = useState(0);
  const [choices, setChoices] = useState<(string | null)[]>(Array(shapeQuestions.length).fill(null));
  const [showFeedback, setShowFeedback] = useState(false);
  const [shuffledOptions, setShuffledOptions] = useState<string[][]>([]);
  const timerRef = React.useRef<ReturnType<typeof setTimeout> | null>(null);

  React.useEffect(() => {
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, []);

  const startQuiz = () => {
    const shuffled = shapeQuestions.map(q => {
      const opts = [q.correct, ...q.wrong];
      for (let i = opts.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [opts[i], opts[j]] = [opts[j], opts[i]];
      }
      return opts;
    });
    setShuffledOptions(shuffled);
    setPhase('quiz');
    setQIndex(0);
    setChoices(Array(shapeQuestions.length).fill(null));
    setShowFeedback(false);
  };

  const handleChoice = (choice: string) => {
    if (showFeedback) return;
    const newChoices = [...choices];
    newChoices[qIndex] = choice;
    setChoices(newChoices);
    setShowFeedback(true);
    timerRef.current = setTimeout(() => {
      setShowFeedback(false);
      if (qIndex + 1 >= shapeQuestions.length) {
        setPhase('done');
      } else {
        setQIndex(q => q + 1);
      }
    }, 2200);
  };

  const score = choices.filter((c, i) => c === shapeQuestions[i].correct).length;

  if (phase === 'ready') {
    return (
      <div className="my-10 bg-white dark:bg-zinc-900 text-center" style={{ border: '2px solid #1a1a1a', borderRadius: 16, padding: 24 }}>
        <span className="inline-block px-3 py-1 rounded-full text-[11px] font-bold tracking-wider uppercase mb-3" style={{ backgroundColor: '#e8f5f2', color: '#1a6358', border: '1px solid rgba(42,125,111,0.2)', letterSpacing: '0.06em' }}>Exam Skills Quiz</span>
        <h4 className="font-serif font-semibold" style={{ fontSize: 20, color: '#1a1a1a' }}>Shape Quiz</h4>
        <p className="text-sm mt-2 mb-6 max-w-md mx-auto" style={{ color: '#7a7068' }}>Can you match the mark allocation to the right answer shape?</p>
        <button onClick={startQuiz} style={{ backgroundColor: '#2A7D6F', borderRadius: 20, padding: '12px 24px', fontSize: 14, fontWeight: 600, color: '#FFFFFF' }}>Start Quiz</button>
      </div>
    );
  }

  if (phase === 'done') {
    return (
      <div className="my-10 bg-white dark:bg-zinc-900" style={{ border: '2px solid #1a1a1a', borderRadius: 16, padding: 24 }}>
        <h4 className="font-serif font-semibold text-center" style={{ fontSize: 20, color: '#1a1a1a' }}>Shape Quiz Results</h4>
        <div className="flex justify-center my-5">
          <div className="text-center" style={{ backgroundColor: '#e8f5f2', border: '2px solid #2A7D6F', borderRadius: 14, padding: '14px 20px' }}>
            <div className="font-serif font-bold" style={{ fontSize: 28, color: '#2A7D6F' }}>{score}/{shapeQuestions.length}</div>
            <div style={{ fontSize: 11, fontWeight: 600, color: '#9e9186' }}>Correct</div>
          </div>
        </div>
        <div className="space-y-2 mb-6">
          {shapeQuestions.map((q, i) => {
            const got = choices[i];
            const correct = got === q.correct;
            return (
              <div key={i} className="bg-white dark:bg-zinc-900" style={{ border: correct ? '2px solid #2A7D6F' : '2px solid #1a1a1a', borderLeft: correct ? undefined : '4px solid #E85D75', borderRadius: 14, padding: '14px 16px' }}>
                <div className="flex items-center justify-between mb-1">
                  <span className="font-serif font-bold" style={{ fontSize: 14, color: '#1a1a1a' }}>{q.marks}</span>
                  <span style={{ fontSize: 12, fontWeight: 700, color: correct ? '#1a6358' : '#b33030' }}>{correct ? '✓ Correct' : '✗ Incorrect'}</span>
                </div>
                <p style={{ fontSize: 14, color: '#5a5550' }}>{q.correct}</p>
                {!correct && got && <p className="italic mt-1" style={{ fontSize: 12, color: '#b33030' }}>You said: {got}</p>}
              </div>
            );
          })}
        </div>
        <div className="text-center">
          <button onClick={startQuiz} style={{ backgroundColor: '#2A7D6F', borderRadius: 20, padding: '12px 24px', fontSize: 14, fontWeight: 600, color: '#FFFFFF' }}>Try Again</button>
        </div>
      </div>
    );
  }

  const q = shapeQuestions[qIndex];
  const isCorrect = showFeedback && choices[qIndex] === q.correct;
  const _isWrong = showFeedback && choices[qIndex] !== null && choices[qIndex] !== q.correct;

  return (
    <div className="my-10 bg-white dark:bg-zinc-900" style={{ border: '2px solid #1a1a1a', borderRadius: 16, padding: 24 }}>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className="inline-block px-2.5 py-0.5 rounded-full text-[10px] font-bold tracking-wider uppercase" style={{ backgroundColor: '#e8f5f2', color: '#1a6358', border: '1px solid rgba(42,125,111,0.2)' }}>Exam Skills Quiz</span>
          <h4 className="font-serif font-semibold" style={{ fontSize: 18, color: '#1a1a1a' }}>Shape Quiz</h4>
        </div>
        <span style={{ fontSize: 13, fontWeight: 600, color: '#9e9186', backgroundColor: '#f0ece6', border: '1px solid #d0cdc8', borderRadius: 20, padding: '3px 10px' }}>{qIndex + 1} / {shapeQuestions.length}</span>
      </div>

      {/* Mark allocation */}
      <AnimatePresence mode="wait">
        <motion.div key={qIndex} initial={{ opacity: 0, x: 24 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -24 }}
          className="mb-5" style={{ backgroundColor: '#f4f0eb', border: '1.5px solid #d0cdc8', borderRadius: 12, padding: '14px 18px', minHeight: 80, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <p style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', color: '#9e9186', marginBottom: 8, textTransform: 'uppercase' as const }}>Mark allocation</p>
          <p style={{ lineHeight: 1 }}>
            <span className="font-serif font-bold" style={{ fontSize: 32, color: '#2A7D6F' }}>{q.marks.replace(/[()]/g, '')}</span>
          </p>
          {showFeedback && (
            <motion.p initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} className="italic mt-3" style={{ fontSize: 13, color: isCorrect ? '#1a6358' : '#b33030' }}>
              {isCorrect ? 'Correct! You can read the marks.' : `Not quite — the right shape is: ${q.correct}`}
            </motion.p>
          )}
        </motion.div>
      </AnimatePresence>

      {/* Options */}
      <div className="space-y-2">
        {shuffledOptions[qIndex]?.map((opt, i) => {
          const selected = showFeedback && choices[qIndex] === opt;
          const isAnswer = showFeedback && opt === q.correct;
          return (
            <button key={i} onClick={() => handleChoice(opt)} disabled={showFeedback} className="w-full text-left transition-all" style={
              isAnswer
                ? { backgroundColor: '#e8f5f2', border: '2px solid #2A7D6F', borderRadius: 12, padding: '14px 18px', fontSize: 14, fontWeight: 600, color: '#1a6358', cursor: 'default' }
                : selected && !isAnswer
                ? { backgroundColor: '#fde4e4', border: '2px solid #E85D75', borderLeft: '4px solid #E85D75', borderRadius: 12, padding: '14px 18px', fontSize: 14, fontWeight: 500, color: '#b33030', cursor: 'default' }
                : showFeedback
                ? { backgroundColor: '#FFFFFF', border: '2px solid #1a1a1a', borderRadius: 12, padding: '14px 18px', fontSize: 14, fontWeight: 500, color: '#1a1a1a', opacity: 0.5, cursor: 'not-allowed' }
                : { backgroundColor: '#FFFFFF', border: '2px solid #1a1a1a', borderRadius: 12, padding: '14px 18px', fontSize: 14, fontWeight: 500, color: '#1a1a1a', cursor: 'pointer' }
            }>
              {isAnswer && '✓ '}{opt}
            </button>
          );
        })}
      </div>

      {/* Progress dots */}
      <div className="flex justify-center gap-1.5 mt-5">
        {shapeQuestions.map((_, i) => (
          <div key={i} style={{ width: 10, height: 10, borderRadius: '50%', backgroundColor: i <= qIndex ? '#2A7D6F' : '#d0cdc8', transition: 'background-color 0.3s' }} />
        ))}
      </div>
    </div>
  );
};

// --- MODULE COMPONENT ---
const AnswerEngineeringModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'the-structure-gap', title: 'The Structure Gap', eyebrow: '01 // The Problem', icon: AlertTriangle },
    { id: 'the-peel-framework', title: 'The PEEL Framework', eyebrow: '02 // The Essay Engine', icon: Layers },
    { id: 'the-science-answer-stack', title: 'The Science Answer Stack', eyebrow: '03 // The Formula', icon: FlaskConical },
    { id: 'the-marks-shape-connection', title: 'The Marks-Shape Connection', eyebrow: '04 // The Decoder', icon: BarChart2 },
    { id: 'the-sixty-percent-answer', title: 'The 60% Answer', eyebrow: '05 // The Rescue', icon: LifeBuoy },
    { id: 'subject-specific-structures', title: 'Subject-Specific Structures', eyebrow: '06 // The Toolkit', icon: Wrench },
    { id: 'your-engineering-toolkit', title: 'Your Engineering Toolkit', eyebrow: '07 // The Plan', icon: Target },
  ];

  return (
    <ModuleLayout
      moduleNumber="EZ08"
      moduleTitle="Answer Engineering"
      moduleSubtitle="Why Some Students Get More Marks for the Same Knowledge"
      moduleDescription="Two students know the same content. One gets a H3, the other gets a H1. The difference is how they structure their answers. This module teaches you the frameworks."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Engineer Better Answers"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Structure Gap." eyebrow="01 // The Problem" icon={AlertTriangle} theme={theme}>
              <p>Two students know the same Biology. One gets a H3, the other gets a H1. The difference is not knowledge — it is <Highlight description="Structure means your answer has a visible architecture that the examiner can follow. Each point is clearly separated, each piece of evidence is connected to a claim, and the logic flows from start to finish." theme={theme}>structure</Highlight>. The H1 student's answers have a visible architecture — the examiner can SEE each point, FIND each piece of evidence, FOLLOW the logic. The H3 student's answer is a wall of text with good ideas buried inside it.</p>
              <p>Examiners read <strong>400+ scripts</strong>. They spend <Highlight description="SEC examiners work through enormous volumes of scripts during marking conferences. They are experienced, professional, and efficient — but they are human. The easier you make it for them to find your points, the more marks you collect." theme={theme}>2-3 minutes per answer</Highlight>. If they cannot FIND your points, they cannot MARK your points. This is not about what you know. This is about how you <em>package</em> what you know so the examiner can see every mark you deserve.</p>
              <p>Think of it this way: the examiner has a checklist. For each answer, they are scanning for specific things — a clear point, supporting evidence, a logical connection back to the question. If those things are buried inside a long, unstructured paragraph, some of them will be missed. Not because the examiner is unfair, but because they are human and they are working fast.</p>
              <p>This module teaches you the <strong>structural frameworks</strong> for building answers — how to organise and construct answers so examiners find every mark. It is the difference between "knowing the content" and "knowing how to package it."</p>
              <PersonalStory name="Sean, Leaving Cert 2024, Cork">
                <p>"I knew the content but my mock results didn't show it. My teacher told me 'I can see you know this, but I had to hunt for your points.' That one sentence changed everything."</p>
              </PersonalStory>
              <MicroCommitment theme={theme}>
                <p>Look at your most recent test. Can the examiner find your main points in 10 seconds? Pick one answer and read it with fresh eyes. If the key points are not immediately visible, this module is going to change your results.</p>
              </MicroCommitment>
            </ReadingSection>
          )}

          {activeSection === 1 && (
            <ReadingSection title="The PEEL Framework." eyebrow="02 // The Essay Engine" icon={Layers} theme={theme}>
              <p>For any essay-style question — English, History, Business, Geography, and more — <Highlight description="PEEL stands for Point, Evidence, Explain, Link. It gives you a paragraph skeleton that ensures every paragraph in your essay has a clear structure the examiner can follow and award marks to." theme={theme}>PEEL</Highlight> gives you a paragraph skeleton that ensures every paragraph earns its full marks:</p>
              <div className="my-6 space-y-3">
                <div className="flex items-start gap-3 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
                  <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-blue-100 dark:bg-blue-800 text-blue-700 dark:text-blue-300 border border-blue-300 dark:border-blue-700 flex-shrink-0">P</span>
                  <div><strong className="text-blue-700 dark:text-blue-300">Point</strong> — State your argument in one clear sentence. This tells the examiner exactly what this paragraph is about.</div>
                </div>
                <div className="flex items-start gap-3 p-4 bg-amber-50 dark:bg-amber-900/20 rounded-lg border border-amber-200 dark:border-amber-800">
                  <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-amber-100 dark:bg-amber-800 text-amber-700 dark:text-amber-300 border border-amber-300 dark:border-amber-700 flex-shrink-0">E</span>
                  <div><strong className="text-amber-700 dark:text-amber-300">Evidence</strong> — Give a specific example, quote, or fact. Not a vague reference — something concrete.</div>
                </div>
                <div className="flex items-start gap-3 p-4 bg-teal-50 dark:bg-teal-900/20 rounded-lg border border-teal-200 dark:border-teal-800">
                  <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-teal-100 dark:bg-teal-800 text-teal-700 dark:text-teal-300 border border-teal-300 dark:border-teal-700 flex-shrink-0">E</span>
                  <div><strong className="text-teal-700 dark:text-teal-300">Explain</strong> — Say WHY this evidence supports your point. This is the step most students skip, and it is where the real marks are.</div>
                </div>
                <div className="flex items-start gap-3 p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-800">
                  <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-purple-100 dark:bg-purple-800 text-purple-700 dark:text-purple-300 border border-purple-300 dark:border-purple-700 flex-shrink-0">L</span>
                  <div><strong className="text-purple-700 dark:text-purple-300">Link</strong> — Connect back to the question asked. This closes the loop and shows the examiner you are directly answering what was asked.</div>
                </div>
              </div>
              <p>Each paragraph = one PEEL cycle. A <strong>60-mark essay = 4-5 PEEL paragraphs + intro + conclusion</strong>. That is it. That is the entire structure of a top-grade essay.</p>
              <p>PEEL does not make your writing boring — it makes your <Highlight description="The examiner is not looking for creative writing. They are looking for clear, structured arguments with evidence. PEEL makes your thinking visible so they can award marks at every step of your paragraph." theme={theme}>THINKING visible</Highlight>. You can still be creative within the structure. The best essays in any subject combine strong ideas with clear organisation. PEEL gives you the organisation so you can focus on the ideas.</p>
              <PEELBuilder />
            </ReadingSection>
          )}

          {activeSection === 2 && (
            <ReadingSection title="The Science Answer Stack." eyebrow="03 // The Formula" icon={FlaskConical} theme={theme}>
              <p>For Maths, Physics, Chemistry, and Applied Maths, there is a specific structure that maximises marks. We call it <Highlight description="S-cubed-S stands for State, Substitute, Solve, State. It is a four-step process that earns marks at every step. Even if your final answer is wrong, the first three steps earn method marks independently." theme={theme}>S&sup3;S</Highlight>:</p>
              <ConceptCardGrid
                cards={[
                  { number: 1, term: "State", description: "Write the formula or law you are using. This immediately earns method marks." },
                  { number: 2, term: "Substitute", description: "Plug in the given values WITH units. This earns more method marks." },
                  { number: 3, term: "Solve", description: "Show each calculation step on its own line. Never skip steps." },
                  { number: 4, term: "State", description: "Write the final answer with correct units, circled or underlined." },
                ]}
              />
              <p>This pattern earns marks at <strong>EVERY step</strong>. Even if your final answer is wrong, steps 1-3 earn method marks independently.</p>
              <p>In a <strong>25-mark Maths question</strong>, the final answer is typically worth only <Highlight description="The final numerical answer in most science and maths questions is worth only 4-5 out of 25 marks. The other 20 marks are for showing your process. Students who jump straight to the answer are skipping 80% of the available marks." theme={theme}>4-5 marks</Highlight>. The other 20 marks are for showing your process. Students who jump to the answer skip 80% of the available marks.</p>
              <p>Remember the three types of marks from the Marking Scheme Decoder? This structure hits all three: attempt marks for writing the formula, method marks for substituting and solving, and answer marks for the final result.</p>
              <StackBuilder />
            </ReadingSection>
          )}

          {activeSection === 3 && (
            <ReadingSection title="The Marks-Shape Connection." eyebrow="04 // The Decoder" icon={BarChart2} theme={theme}>
              <p>The marks beside a question tell you <em>exactly</em> what <Highlight description="The 'shape' of an answer means its length and structure. A 4-mark answer should look completely different from a 20-mark answer. The marks are a blueprint telling you exactly how much to write and how to organise it." theme={theme}>SHAPE</Highlight> your answer should be. Here is how to decode them:</p>
              <div className="my-6 space-y-2.5">
                <div className="p-4 bg-zinc-50 dark:bg-zinc-700/50 rounded-lg border border-zinc-200 dark:border-zinc-600">
                  <span className="font-mono font-bold text-zinc-800 dark:text-white">(4 marks)</span>
                  <span className="text-zinc-500 dark:text-zinc-400 mx-2">=</span>
                  <span className="text-zinc-600 dark:text-zinc-300">1-2 sentences. Name it and briefly explain.</span>
                </div>
                <div className="p-4 bg-zinc-50 dark:bg-zinc-700/50 rounded-lg border border-zinc-200 dark:border-zinc-600">
                  <span className="font-mono font-bold text-zinc-800 dark:text-white">(10 marks)</span>
                  <span className="text-zinc-500 dark:text-zinc-400 mx-2">=</span>
                  <span className="text-zinc-600 dark:text-zinc-300">A developed paragraph. Make a point, support it, explain it.</span>
                </div>
                <div className="p-4 bg-zinc-50 dark:bg-zinc-700/50 rounded-lg border border-zinc-200 dark:border-zinc-600">
                  <span className="font-mono font-bold text-zinc-800 dark:text-white">(15 marks)</span>
                  <span className="text-zinc-500 dark:text-zinc-400 mx-2">=</span>
                  <span className="text-zinc-600 dark:text-zinc-300">Two developed paragraphs OR one long one with multiple examples.</span>
                </div>
                <div className="p-4 bg-zinc-50 dark:bg-zinc-700/50 rounded-lg border border-zinc-200 dark:border-zinc-600">
                  <span className="font-mono font-bold text-zinc-800 dark:text-white">(20-25 marks)</span>
                  <span className="text-zinc-500 dark:text-zinc-400 mx-2">=</span>
                  <span className="text-zinc-600 dark:text-zinc-300">A structured mini-essay. Introduction, 2-3 body paragraphs, brief conclusion.</span>
                </div>
                <div className="p-4 bg-zinc-50 dark:bg-zinc-700/50 rounded-lg border border-zinc-200 dark:border-zinc-600">
                  <span className="font-mono font-bold text-zinc-800 dark:text-white">(30+ marks)</span>
                  <span className="text-zinc-500 dark:text-zinc-400 mx-2">=</span>
                  <span className="text-zinc-600 dark:text-zinc-300">Full essay structure. Every mark corresponds to roughly one strong sentence.</span>
                </div>
                <div className="p-4 bg-zinc-50 dark:bg-zinc-700/50 rounded-lg border border-zinc-200 dark:border-zinc-600">
                  <span className="font-mono font-bold text-zinc-800 dark:text-white">(3 &times; 5 marks)</span>
                  <span className="text-zinc-500 dark:text-zinc-400 mx-2">=</span>
                  <span className="text-zinc-600 dark:text-zinc-300">Three SEPARATE short answers, not one long one. Examiners mark each independently.</span>
                </div>
                <div className="p-4 bg-zinc-50 dark:bg-zinc-700/50 rounded-lg border border-zinc-200 dark:border-zinc-600">
                  <span className="font-mono font-bold text-zinc-800 dark:text-white">(2 &times; 10 marks)</span>
                  <span className="text-zinc-500 dark:text-zinc-400 mx-2">=</span>
                  <span className="text-zinc-600 dark:text-zinc-300">Two developed points. Give EXACTLY two, not three.</span>
                </div>
              </div>
              <p>The most common mistake is writing a <Highlight description="Writing too much for a small question wastes time. Writing too little for a big question loses marks. The mark allocation is the examiner's way of telling you exactly how much they expect." theme={theme}>4-mark answer for a 15-mark question</Highlight>, or a 15-mark answer for a 4-mark question. The marks tell you exactly how much to write. Reading them correctly is one of the simplest ways to improve your results.</p>
              <ShapeQuiz />
            </ReadingSection>
          )}

          {activeSection === 4 && (
            <ReadingSection title="The 60% Answer." eyebrow="05 // The Rescue" icon={LifeBuoy} theme={theme}>
              <p>What do you do when you only <em>half</em>-know the answer? This is not about attempt marks — that is about whether to write <em>anything at all</em>. This is about how to <Highlight description="A structured partial answer uses clear formatting — numbered points, definitions, diagrams, question language — to make sure every piece of knowledge you DO have is visible and earnable. It is about maximising what you get from what you know." theme={theme}>STRUCTURE a partial answer</Highlight> to maximise marks when you know some of the content but not all of it.</p>
              <p>Here is the strategy:</p>
              <ConceptCardGrid
                cards={[
                  { number: 1, term: "Start with what you DO know", description: "Even if it is just the definition of a key term in the question — a correct definition earns marks immediately." },
                  { number: 2, term: "Use the question's own language", description: "Mirror the wording back in your answer. It signals relevance to the examiner and shows you understand what is being asked." },
                  { number: 3, term: "Draw a diagram if applicable", description: "Labelled diagrams earn independent marks. Even a basic diagram with correct labels picks up marks the examiner could not give you from text alone." },
                  { number: 4, term: "Break your answer into numbered points", description: "Even if you only have 2 out of 4. Numbered points are easier to find and mark than ideas buried in paragraphs." },
                  { number: 5, term: "Write a concluding sentence", description: "Link back to the question directly. This wraps your answer and shows the examiner you understood the task.", highlight: true },
                ]}
              />
              <p>The key insight: a <strong>structured 60% answer scores higher than an unstructured 80% answer</strong>. The examiner can find and award <Highlight description="When your answer is structured with numbered points, definitions, and diagrams, the examiner can see every piece of knowledge you have. When it is buried in a paragraph, they might miss things — and missed points are missed marks." theme={theme}>every point you make</Highlight>, instead of hunting through a paragraph for buried insights.</p>
              <PersonalStory name="Niamh, Leaving Cert 2023, Waterford">
                <p>"In my Chemistry exam, I got a question I barely knew. I wrote the formula, defined the terms, drew a diagram, and wrote what I did know in numbered points. I got 18 out of 25. My friend who knew more but wrote it as a paragraph got 14."</p>
              </PersonalStory>
            </ReadingSection>
          )}

          {activeSection === 5 && (
            <ReadingSection title="Subject-Specific Structures." eyebrow="06 // The Toolkit" icon={Wrench} theme={theme}>
              <p>Here is a quick reference for the dominant answer structure in each subject family. Keep this in mind as you practise past papers.</p>
              <div className="my-6 space-y-3">
                <div className="p-5 bg-zinc-50 dark:bg-zinc-700/50 rounded-xl border border-zinc-200 dark:border-zinc-600">
                  <h4 className="font-bold text-zinc-800 dark:text-white mb-2">Languages (English, Irish, French etc.)</h4>
                  <p className="text-sm text-zinc-600 dark:text-zinc-300"><strong>PEEL for essays</strong>, quote-integrate-analyse for poetry and prose. Always embed quotes rather than dropping them in. Every paragraph should have a clear topic sentence.</p>
                </div>
                <div className="p-5 bg-zinc-50 dark:bg-zinc-700/50 rounded-xl border border-zinc-200 dark:border-zinc-600">
                  <h4 className="font-bold text-zinc-800 dark:text-white mb-2">Sciences (Biology, Chemistry, Physics)</h4>
                  <p className="text-sm text-zinc-600 dark:text-zinc-300"><strong>S&sup3;S for calculations</strong>, "State-Explain-Example" for definitions, labelled diagrams everywhere. Every label on a diagram is a potential mark.</p>
                </div>
                <div className="p-5 bg-zinc-50 dark:bg-zinc-700/50 rounded-xl border border-zinc-200 dark:border-zinc-600">
                  <h4 className="font-bold text-zinc-800 dark:text-white mb-2">Business Subjects</h4>
                  <p className="text-sm text-zinc-600 dark:text-zinc-300"><strong>Point-Explain-Example-Apply</strong> (the business PEEL variant). Always apply to a real business or the case study in the question.</p>
                </div>
                <div className="p-5 bg-zinc-50 dark:bg-zinc-700/50 rounded-xl border border-zinc-200 dark:border-zinc-600">
                  <h4 className="font-bold text-zinc-800 dark:text-white mb-2">Maths</h4>
                  <p className="text-sm text-zinc-600 dark:text-zinc-300"><strong>Every line is a mark</strong> — never skip steps. Use the left column for working, right column for answers. Circle or underline final answers.</p>
                </div>
                <div className="p-5 bg-zinc-50 dark:bg-zinc-700/50 rounded-xl border border-zinc-200 dark:border-zinc-600">
                  <h4 className="font-bold text-zinc-800 dark:text-white mb-2">History / Geography</h4>
                  <p className="text-sm text-zinc-600 dark:text-zinc-300"><strong>PEEL for essays</strong>, "Describe-Explain-Evaluate" for source analysis. Case Study structure for Geography — always name, locate, and describe the process.</p>
                </div>
                <div className="p-5 bg-zinc-50 dark:bg-zinc-700/50 rounded-xl border border-zinc-200 dark:border-zinc-600">
                  <h4 className="font-bold text-zinc-800 dark:text-white mb-2">Practical Subjects</h4>
                  <p className="text-sm text-zinc-600 dark:text-zinc-300"><strong>Process documentation</strong> — materials, method, outcome, evaluation. Always explain <em>why</em> you chose a material or method, not just what you did.</p>
                </div>
              </div>
              <p>This is a reference card, not deep teaching. Bookmark this section and come back to it when you are practising past papers in a specific subject.</p>
            </ReadingSection>
          )}

          {activeSection === 6 && (
            <ReadingSection title="Your Engineering Toolkit." eyebrow="07 // The Plan" icon={Target} theme={theme}>
              <p>You now have <strong>four frameworks</strong> for building better answers:</p>
              <div className="my-6 space-y-2.5">
                <div className="flex items-center gap-3 p-4 bg-zinc-50 dark:bg-zinc-700/50 rounded-lg border border-zinc-200 dark:border-zinc-600">
                  <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-blue-100 dark:bg-blue-800 text-blue-700 dark:text-blue-300 border border-blue-300 dark:border-blue-700 flex-shrink-0">1</span>
                  <div className="text-zinc-700 dark:text-zinc-200"><strong>PEEL</strong> for essay paragraphs</div>
                </div>
                <div className="flex items-center gap-3 p-4 bg-zinc-50 dark:bg-zinc-700/50 rounded-lg border border-zinc-200 dark:border-zinc-600">
                  <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-amber-100 dark:bg-amber-800 text-amber-700 dark:text-amber-300 border border-amber-300 dark:border-amber-700 flex-shrink-0">2</span>
                  <div className="text-zinc-700 dark:text-zinc-200"><strong>S&sup3;S</strong> for science and maths calculations</div>
                </div>
                <div className="flex items-center gap-3 p-4 bg-zinc-50 dark:bg-zinc-700/50 rounded-lg border border-zinc-200 dark:border-zinc-600">
                  <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-teal-100 dark:bg-teal-800 text-teal-700 dark:text-teal-300 border border-teal-300 dark:border-teal-700 flex-shrink-0">3</span>
                  <div className="text-zinc-700 dark:text-zinc-200"><strong>The marks-shape decoder</strong> for reading mark allocations</div>
                </div>
                <div className="flex items-center gap-3 p-4 bg-zinc-50 dark:bg-zinc-700/50 rounded-lg border border-zinc-200 dark:border-zinc-600">
                  <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-purple-100 dark:bg-purple-800 text-purple-700 dark:text-purple-300 border border-purple-300 dark:border-purple-700 flex-shrink-0">4</span>
                  <div className="text-zinc-700 dark:text-zinc-200"><strong>The 60% rescue strategy</strong> for partial answers</div>
                </div>
              </div>
              <MicroCommitment theme={theme}>
                <p>Pick one past exam question from your <strong>strongest</strong> subject. Answer it using the right framework. Then pick one from your <strong>weakest</strong> subject. Compare how it feels — that is the difference structure makes.</p>
              </MicroCommitment>
              <p className="mt-8 text-center font-serif text-lg font-semibold text-zinc-800 dark:text-white">Knowledge gets you in the door. Structure gets you the marks. You have always had the knowledge — now you have the engineering.</p>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};

export default AnswerEngineeringModule;
