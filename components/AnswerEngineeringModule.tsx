/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { AnimatePresence,motion } from 'framer-motion';
import { AlertTriangle,BarChart2,FlaskConical,Layers,LifeBuoy,Target,Wrench } from 'lucide-react';
import React,{ useState } from 'react';
import { ANSWER_ENGINEERING_REFERENCE_LIST } from '../data/references/answerEngineering';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { redTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { ConceptCardGrid,Highlight,MicroCommitment,PersonalStory,ReadingSection } from './ModuleShared';
import { MotionDiv } from './Motion';
import { AnswerGroup,AnswerLine,AnswerTick,ExerciseLabel,ExerciseSheet } from './learning/Exercise';
import { Button } from './ui/Button';
import { ChoiceTile,SelectionBar } from './ui/Choice';
import { PressBox } from './ui/List';

const theme = redTheme;

/** A quiz's progress: a row of step marks (done and right in the tick's green, done and wrong in ink-3, the current one
 *  ringed in ink, the rest a hairline ring). Drawn from the module's own state; no words. */
const stepMarkStyle = (done: boolean, right: boolean, current: boolean): React.CSSProperties =>
  done ? { background: right ? 'var(--success-hex)' : 'var(--ink-muted)' }
    : current ? { border: '1.5px solid var(--ink-primary)' } : { border: '1px solid var(--outline-soft)' };

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

// Each slot's name (no colour per slot: the name says which it is).
const peelLabels: Record<string, { label: string }> = {
  P: { label: 'Point' },
  E: { label: 'Evidence' },
  E2: { label: 'Explain' },
  L: { label: 'Link' },
};

/** The builder's title, also the name of its subject bar for screen readers. */
const PEEL_BUILDER_TITLE = 'PEEL Builder';

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
    <ExerciseSheet title={PEEL_BUILDER_TITLE} sub="Arrange the sentences in the correct PEEL order." name="PEELBuilder">
      {/* Subject tabs: the system's selection bar, named by the sheet's own title (it changes the example only while building, as before) */}
      <SelectionBar
        label={PEEL_BUILDER_TITLE}
        value={String(exampleIndex)}
        onChange={(v) => { const i = Number(v); if (phase === 'building') { setExampleIndex(i); setPlaced([null, null, null, null]); } }}
        options={peelExamples.map((e, i) => ({ value: String(i), label: e.subject }))}
      />

      {/* Question: under its subject label, set large (no box) */}
      <div className="ex-thought">
        <ExerciseLabel>{ex.subject}</ExerciseLabel>
        <p className="ex-thought-words">{ex.question}</p>
      </div>

      {/* Slots: each under its own label; a placed sentence is a box you press to take it back out; an empty slot is a
          dashed hairline; once checked, each sentence is a line in ink (the tick where it is in the right place) */}
      <div className="ex-questions">
        {slotLabels.map((label, slotIdx) => {
          const sentIdx = placed[slotIdx];
          const pl = peelLabels[label];
          const isCorrect = phase === 'result' && sentIdx === ex.correctOrder[slotIdx];
          const isWrong = phase === 'result' && sentIdx !== null && sentIdx !== ex.correctOrder[slotIdx];
          const correctSentIdx = phase === 'result' ? ex.correctOrder[slotIdx] : null;

          return (
            <div key={slotIdx} className="flex flex-col gap-2">
              {/* Header */}
              <p className="ex-label">
                {slotIdx + 1}. {pl.label}
              </p>
              {/* Body */}
              {sentIdx !== null ? (
                phase === 'building' ? (
                  <PressBox onPress={() => handleRemoveFromSlot(slotIdx)}>
                    <span className="block t-sub text-ink-primary">{ex.sentences[sentIdx].text}</span>
                  </PressBox>
                ) : (
                  <AnswerLine tone={isCorrect ? 'ok' : 'note'}>{ex.sentences[sentIdx].text}</AnswerLine>
                )
              ) : (
                <p className="min-h-[56px] flex items-center t-meta" style={{ padding: '12px 16px', border: '1px dashed var(--outline-soft)', borderRadius: 'var(--r-box)' }}>Click a sentence below to place it here</p>
              )}
              {isWrong && correctSentIdx !== null && (
                <p className="t-meta text-ink-secondary">
                  Correct: {ex.sentences[correctSentIdx].text.slice(0, 80)}...
                </p>
              )}
            </div>
          );
        })}
      </div>

      {/* Available sentences: each a box you press to place it */}
      {phase === 'building' && availableSentences.length > 0 && (
        <div className="ex-stack">
          <ExerciseLabel>Available sentences</ExerciseLabel>
          <div className="ex-cards">
            {availableSentences.map(i => (
              <PressBox key={i} onPress={() => handlePlaceSentence(i)}>
                <span className="block t-sub text-ink-primary">{ex.sentences[i].text}</span>
              </PressBox>
            ))}
          </div>
        </div>
      )}

      {/* Actions */}
      {phase === 'building' && allPlaced && (
        <div className="ex-actions">
          <Button onClick={handleSubmit}>
            Check Order
          </Button>
        </div>
      )}
      {phase === 'result' && (
        <MotionDiv initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="ex-stack">
          {/* The score: the number in ink with its word under it (no box) */}
          <div className="flex flex-col">
            <p className="t-number text-ink-primary">{score}/4</p>
            <p className="ex-label">Correct</p>
          </div>
          <div className="ex-actions">
            {exampleIndex < peelExamples.length - 1 ? (
              <Button onClick={handleNextExample}>
                Next Example
              </Button>
            ) : (
              <Button onClick={handleReset}>
                Try Again
              </Button>
            )}
          </div>
        </MotionDiv>
      )}
    </ExerciseSheet>
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
      <ExerciseSheet title="Stack Builder" sub="Build a science answer step by step and see how marks accumulate." name="StackBuilder">
        {/* The problem: words you read, under their label (no box) */}
        <div className="ex-thought">
          <ExerciseLabel>Physics Problem</ExerciseLabel>
          <p className="ex-quote">{stackProblem.question}</p>
        </div>
        <div className="ex-actions">
          <Button onClick={startBuild}>Start Building</Button>
        </div>
      </ExerciseSheet>
    );
  }

  if (phase === 'done') {
    return (
      <ExerciseSheet title="Stack Builder Results" name="StackBuilder">
        {/* The score: the number in ink with its words under it (no box) */}
        <div className="flex flex-col">
          <p className="t-number text-ink-primary">{earnedMarks}/{stackProblem.totalMarks}</p>
          <p className="ex-label">Marks Earned</p>
        </div>
        {/* Each step ruled like a row: its name, its marks (the green tick when earned), your step, the right one */}
        <div className="ex-list">
          {stackProblem.steps.map((step, i) => {
            const got = choices[i];
            const correct = got === step.correct;
            return (
              <div key={i}>
                <div className="flex items-center justify-between gap-3">
                  <span className="ex-label">{step.label}</span>
                  <span className="flex items-center gap-1 t-meta text-ink-primary">
                    {correct ? <AnswerTick /> : null}
                    {correct ? `+${step.marks} marks` : '0 marks'}
                  </span>
                </div>
                <p className="t-body text-ink-primary">{got}</p>
                {!correct && (
                  <p className="t-meta text-ink-secondary">Correct: {step.correct}</p>
                )}
              </div>
            );
          })}
        </div>
        <AnswerLine tone={earnedMarks === stackProblem.totalMarks ? 'ok' : 'note'}>
          {earnedMarks === stackProblem.totalMarks
            ? 'Perfect! Every step earned its marks.'
            : earnedMarks >= stackProblem.totalMarks * 0.75
            ? 'Great work! Even the steps you got right earned marks independently.'
            : 'Notice how each correct step earns marks independently. Even with mistakes, the right steps still count.'}
        </AnswerLine>
        <div className="ex-actions">
          <Button onClick={startBuild}>Try Again</Button>
        </div>
      </ExerciseSheet>
    );
  }

  const step = stackProblem.steps[stepIndex];
  const isCorrect = showStepFeedback && choices[stepIndex] === step.correct;

  return (
    <ExerciseSheet title="Stack Builder" name="StackBuilder">
      <p className="ex-count ui-readout">Step {stepIndex + 1} / {stackProblem.steps.length}</p>

      {/* Question reminder: under a hairline and its label (no box) */}
      <div className="ex-block">
        <p className="ex-label">Question</p>
        <p className="ex-block-text">{stackProblem.question}</p>
      </div>

      {/* Running marks: the student's own marks, ink on a hairline track */}
      <div className="flex items-center gap-3">
        <span className="t-meta">Marks so far:</span>
        <div className="flex-1 h-2 rounded-full overflow-hidden" style={{ background: 'var(--hairline)' }}>
          <motion.div
            className="h-full rounded-full"
            style={{ background: 'var(--ink-primary)' }}
            animate={{ width: `${(earnedMarks / stackProblem.totalMarks) * 100}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
        <span className="ui-readout text-ink-primary">{earnedMarks}/{stackProblem.totalMarks}</span>
      </div>

      {/* Step prompt: on the sheet (no tinted card); the feedback is a line in ink, the tick when right */}
      <AnimatePresence mode="wait">
        <motion.div key={stepIndex} initial={{ opacity: 0, x: 24 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -24 }}
          className="ex-stack">
          <p className="ex-label">{step.label}</p>
          <p className="t-body text-ink-primary">Choose the correct step worth <strong>{step.marks} marks</strong>:</p>
          {showStepFeedback && (
            <motion.div initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }}>
              <AnswerLine tone={isCorrect ? 'ok' : 'note'}>
                {isCorrect ? `Correct! +${step.marks} marks` : `Not quite. The correct step was: ${step.correct}`}
              </AnswerLine>
            </motion.div>
          )}
        </motion.div>
      </AnimatePresence>

      {/* Options: one answer locks in while its feedback shows (disabled, as before); the chosen one and the right one
          stay at full strength */}
      <AnswerGroup kind="one" chooseOnArrow={false}>
        {shuffledOptions[stepIndex]?.map((opt, i) => {
          const selected = showStepFeedback && choices[stepIndex] === opt;
          const isAnswer = showStepFeedback && opt === step.correct;
          return (
            <ChoiceTile key={i} onClick={() => handleChoice(opt)} disabled={showStepFeedback}
              chosen={selected}
              style={selected || isAnswer ? { opacity: 1 } : undefined}
              label={opt}
            />
          );
        })}
      </AnswerGroup>

      {/* Progress: a row of step marks */}
      <ol className="ex-steps justify-center">
        {stackProblem.steps.map((_, i) => (
          <li key={i} className="w-2 h-2 rounded-full box-border" style={stepMarkStyle(i < stepIndex, choices[i] === stackProblem.steps[i].correct, i === stepIndex)} />
        ))}
      </ol>
    </ExerciseSheet>
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
      <ExerciseSheet label="Exam Skills Quiz" title="Shape Quiz" sub="Can you match the mark allocation to the right answer shape?" name="ShapeQuiz">
        <div className="ex-actions">
          <Button onClick={startQuiz}>Start Quiz</Button>
        </div>
      </ExerciseSheet>
    );
  }

  if (phase === 'done') {
    return (
      <ExerciseSheet title="Shape Quiz Results" name="ShapeQuiz">
        {/* The score: the number in ink with its word under it (no orange box) */}
        <div className="flex flex-col">
          <p className="t-number text-ink-primary">{score}/{shapeQuestions.length}</p>
          <p className="ex-label">Correct</p>
        </div>
        {/* Each question ruled like a row: its marks, how you did, the right shape, what you said */}
        <div className="ex-list">
          {shapeQuestions.map((q, i) => {
            const got = choices[i];
            const correct = got === q.correct;
            return (
              <div key={i}>
                <div className="flex items-center justify-between gap-3">
                  <span className="t-row text-ink-primary">{q.marks}</span>
                  <span className="t-meta text-ink-primary">{correct ? '✓ Correct' : '✗ Incorrect'}</span>
                </div>
                <p className="t-body text-ink-primary">{q.correct}</p>
                {!correct && got && <p className="t-meta text-ink-secondary">You said: {got}</p>}
              </div>
            );
          })}
        </div>
        <div className="ex-actions">
          <Button onClick={startQuiz}>Try Again</Button>
        </div>
      </ExerciseSheet>
    );
  }

  const q = shapeQuestions[qIndex];
  const isCorrect = showFeedback && choices[qIndex] === q.correct;
  const _isWrong = showFeedback && choices[qIndex] !== null && choices[qIndex] !== q.correct;

  return (
    <ExerciseSheet label="Exam Skills Quiz" title="Shape Quiz" name="ShapeQuiz">
      <p className="ex-count ui-readout">{qIndex + 1} / {shapeQuestions.length}</p>

      {/* Mark allocation: under its label, the marks as a number in ink (no box); the feedback is a line in ink, the tick when right */}
      <AnimatePresence mode="wait">
        <motion.div key={qIndex} initial={{ opacity: 0, x: 24 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -24 }}
          className="ex-stack min-h-[80px] justify-center">
          <ExerciseLabel>Mark allocation</ExerciseLabel>
          <p className="t-number text-ink-primary">{q.marks.replace(/[()]/g, '')}</p>
          {showFeedback && (
            <motion.div initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }}>
              <AnswerLine tone={isCorrect ? 'ok' : 'note'}>
                {isCorrect ? 'Correct! You can read the marks.' : `Not quite — the right shape is: ${q.correct}`}
              </AnswerLine>
            </motion.div>
          )}
        </motion.div>
      </AnimatePresence>

      {/* Options: one answer locks in while its feedback shows (disabled, as before); the chosen one and the right one
          (still marked "✓ ") stay at full strength, the others fade as today */}
      <AnswerGroup kind="one" chooseOnArrow={false}>
        {shuffledOptions[qIndex]?.map((opt, i) => {
          const selected = showFeedback && choices[qIndex] === opt;
          const isAnswer = showFeedback && opt === q.correct;
          return (
            <ChoiceTile key={i} onClick={() => handleChoice(opt)} disabled={showFeedback}
              chosen={selected}
              style={selected || isAnswer ? { opacity: 1 } : showFeedback ? { opacity: 0.5 } : undefined}
              label={<>{isAnswer && '✓ '}{opt}</>}
            />
          );
        })}
      </AnswerGroup>

      {/* Progress: a row of step marks (reached ones ink, the rest a hairline ring) */}
      <ol className="ex-steps justify-center">
        {shapeQuestions.map((_, i) => (
          <li key={i} className="rounded-full box-border" style={{ width: 10, height: 10, transition: 'background-color 0.3s', ...(i <= qIndex ? { background: 'var(--ink-primary)' } : { border: '1px solid var(--outline-soft)' }) }} />
        ))}
      </ol>
    </ExerciseSheet>
  );
};

// --- MODULE COMPONENT ---
const AnswerEngineeringModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();

  const sections = essentials ? [
    { id: 'the-structure-gap', title: 'The Structure Gap', eyebrow: '01 // The Problem', icon: AlertTriangle },
    { id: 'the-peel-framework', title: 'The PEEL Framework', eyebrow: '02 // The Essay Engine', icon: Layers },
    { id: 'the-science-answer-stack', title: 'Science & Marks', eyebrow: '03 // The Formula & Decoder', icon: FlaskConical },
    { id: 'your-engineering-toolkit', title: 'Your Engineering Toolkit', eyebrow: '04 // The Plan', icon: Target },
  ] : [
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
      references={ANSWER_ENGINEERING_REFERENCE_LIST}
      fullSectionsCount={7}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Engineer Better Answers"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Structure Gap." eyebrow="01 // The Problem" icon={AlertTriangle} theme={theme}>
              {essentials ? (
                <>
                  <p>Two students know the same content. One gets a H3, the other a H1. The difference is <Highlight description="Structure means your answer has a visible architecture that the examiner can follow. Each point is clearly separated, each piece of evidence is connected to a claim, and the logic flows from start to finish." theme={theme}>structure</Highlight>. Examiners work through <Highlight description="SEC examiners work through enormous volumes of scripts during marking conferences. They are experienced, professional, and efficient — but they are human. The easier you make it for them to find your points, the more marks you collect." theme={theme}>large volumes of scripts under time pressure</Highlight>. If they can't find your points, they can't mark them.<Cite n={1} /> Developed, clearly-made points score where one-word or buried answers do not.<Cite n={2} /></p>
                  <p>This module gives you frameworks for packaging answers. The examiner has a checklist. Make your points visible and you collect every mark.</p>
                </>
              ) : (
                <>
                  <p>Two students know the same Biology. One gets a H3, the other gets a H1. The difference is not knowledge — it is <Highlight description="Structure means your answer has a visible architecture that the examiner can follow. Each point is clearly separated, each piece of evidence is connected to a claim, and the logic flows from start to finish." theme={theme}>structure</Highlight>. The H1 student's answers have a visible architecture — the examiner can SEE each point, FIND each piece of evidence, FOLLOW the logic. The H3 student's answer is a wall of text with good ideas buried inside it.</p>
                  <p>Examiners work through <strong>large volumes of scripts</strong> under real time pressure during marking conferences. They give <Highlight description="SEC examiners work through enormous volumes of scripts during marking conferences. They are experienced, professional, and efficient — but they are human. The easier you make it for them to find your points, the more marks you collect." theme={theme}>limited time to each answer</Highlight>. If they cannot FIND your points, they cannot MARK your points.<Cite n={1} /> This is not about what you know. This is about how you <em>package</em> what you know so the examiner can see every mark you deserve. Chief Examiner reports repeatedly reward developed, clearly-structured points over one-word or buried answers.<Cite n={2} /></p>
                  <p>Think of it this way: the examiner has a checklist. For each answer, they are scanning for specific things — a clear point, supporting evidence, a logical connection back to the question. If those things are buried inside a long, unstructured paragraph, some of them will be missed. Not because the examiner is unfair, but because they are human and they are working fast.</p>
                  <p>This module teaches you the <strong>structural frameworks</strong> for building answers — how to organise and construct answers so examiners find every mark. It is the difference between "knowing the content" and "knowing how to package it."</p>
                  <PersonalStory name="Sean, Leaving Cert 2024, Cork">
                    <p>"I knew the content but my mock results didn't show it. My teacher told me 'I can see you know this, but I had to hunt for your points.' That one sentence changed everything."</p>
                  </PersonalStory>
                </>
              )}
              <MicroCommitment theme={theme}>
                <p>Look at your most recent test. Can the examiner find your main points in 10 seconds? Pick one answer and read it with fresh eyes. If the key points are not immediately visible, this module is going to change your results.</p>
              </MicroCommitment>
            </ReadingSection>
          )}

          {activeSection === 1 && (
            <ReadingSection title="The PEEL Framework." eyebrow="02 // The Essay Engine" icon={Layers} theme={theme}>
              <p>{essentials ? 'For essay questions, use' : 'For any essay-style question — English, History, Business, Geography, and more —'} <Highlight description="PEEL stands for Point, Evidence, Explain, Link. It gives you a paragraph skeleton that ensures every paragraph in your essay has a clear structure the examiner can follow and award marks to." theme={theme}>PEEL</Highlight>{essentials ? '. Each paragraph follows four steps:' : ' gives you a paragraph skeleton that ensures every paragraph earns its full marks:'}</p>
              {/* The four steps as lettered lines on the page (no boxes, no bordered letter tags) */}
              <ol className="ex-nums">
                <li>
                  <span className="ex-num">P</span>
                  <div className="ex-num-copy"><p className="ex-num-sub"><strong className="text-ink-primary">Point</strong> — State your argument in one clear sentence. This tells the examiner exactly what this paragraph is about.</p></div>
                </li>
                <li>
                  <span className="ex-num">E</span>
                  <div className="ex-num-copy"><p className="ex-num-sub"><strong className="text-ink-primary">Evidence</strong> — Give a specific example, quote, or fact. Not a vague reference — something concrete.</p></div>
                </li>
                <li>
                  <span className="ex-num">E</span>
                  <div className="ex-num-copy"><p className="ex-num-sub"><strong className="text-ink-primary">Explain</strong> — Say WHY this evidence supports your point. This is the step most students skip, and it is where the real marks are.</p></div>
                </li>
                <li>
                  <span className="ex-num">L</span>
                  <div className="ex-num-copy"><p className="ex-num-sub"><strong className="text-ink-primary">Link</strong> — Connect back to the question asked. This closes the loop and shows the examiner you are directly answering what was asked.</p></div>
                </li>
              </ol>
              {essentials ? (
                <p>A 60-mark essay = 4-5 PEEL paragraphs + intro + conclusion. PEEL makes your <Highlight description="The examiner is not looking for creative writing. They are looking for clear, structured arguments with evidence. PEEL makes your thinking visible so they can award marks at every step of your paragraph." theme={theme}>THINKING visible</Highlight>.</p>
              ) : (
                <>
                  <p>Each paragraph = one PEEL cycle. A <strong>60-mark essay = 4-5 PEEL paragraphs + intro + conclusion</strong>. That is it. That is the entire structure of a top-grade essay.</p>
                  <p>PEEL does not make your writing boring — it makes your <Highlight description="The examiner is not looking for creative writing. They are looking for clear, structured arguments with evidence. PEEL makes your thinking visible so they can award marks at every step of your paragraph." theme={theme}>THINKING visible</Highlight>. You can still be creative within the structure. The best essays in any subject combine strong ideas with clear organisation. PEEL gives you the organisation so you can focus on the ideas.</p>
                </>
              )}
              <PEELBuilder />
            </ReadingSection>
          )}

          {(essentials ? activeSection === 2 : activeSection === 2) && (
            <ReadingSection title={essentials ? "Science & Marks." : "The Science Answer Stack."} eyebrow={essentials ? "03 // The Formula & Decoder" : "03 // The Formula"} icon={FlaskConical} theme={theme}>
              <p>{essentials ? 'For science and maths, use' : 'For Maths, Physics, Chemistry, and Applied Maths, there is a specific structure that maximises marks. We call it'} <Highlight description="S-cubed-S stands for State, Substitute, Solve, State. It is a four-step process that earns marks at every step. Even if your final answer is wrong, the first three steps earn method marks independently." theme={theme}>S&sup3;S</Highlight>{essentials ? ':' : ':'}</p>
              <ConceptCardGrid
                cards={[
                  { number: 1, term: "State", description: "Write the formula or law you are using. This immediately earns method marks." },
                  { number: 2, term: "Substitute", description: "Plug in the given values WITH units. This earns more method marks." },
                  { number: 3, term: "Solve", description: "Show each calculation step on its own line. Never skip steps." },
                  { number: 4, term: "State", description: "Write the final answer with correct units, circled or underlined." },
                ]}
              />
              {essentials ? (
                <>
                  <p>Even if your final answer is wrong, steps 1-3 earn marks independently. In a 25-mark question, the final answer is only <Highlight description="In most science and maths questions the final answer earns only a small share of the marks; the majority are awarded for showing your method and working. Jumping straight to the answer leaves most of those marks uncollected." theme={theme}>a small part of the marks</Highlight> — most are for showing your method.<Cite n={1} /> Show every step.</p>
                  <StackBuilder />
                  <p>The marks beside a question also tell you the <Highlight description="The 'shape' of an answer means its length and structure. A 4-mark answer should look completely different from a 20-mark answer. The marks are a blueprint telling you exactly how much to write and how to organise it." theme={theme}>SHAPE</Highlight> of your answer. 4 marks = 1-2 sentences. 10 marks = a paragraph. 30+ marks = full essay. Match your answer length to the marks.<Cite n={1} /></p>
                  <ShapeQuiz />
                </>
              ) : (
                <>
                  <p>This pattern earns marks at <strong>EVERY step</strong>. Even if your final answer is wrong, steps 1-3 earn method marks independently.</p>
                  <p>In a <strong>25-mark Maths question</strong>, the final answer earns only <Highlight description="In most science and maths questions the final answer earns only a small share of the marks; the majority are awarded for showing your method and working. Jumping straight to the answer leaves most of those marks uncollected." theme={theme}>a small share of the marks</Highlight> — the majority are for showing your process. Students who jump to the answer leave most of the available marks uncollected.<Cite n={1} /></p>
                  <p>Remember the three types of marks from the Marking Scheme Decoder? This structure hits all three: attempt marks for writing the formula, method marks for substituting and solving, and answer marks for the final result.</p>
                  <StackBuilder />
                </>
              )}
            </ReadingSection>
          )}

          {!essentials && activeSection === 3 && (
            <ReadingSection title="The Marks-Shape Connection." eyebrow="04 // The Decoder" icon={BarChart2} theme={theme}>
              <p>The marks beside a question tell you <em>exactly</em> what <Highlight description="The 'shape' of an answer means its length and structure. A 4-mark answer should look completely different from a 20-mark answer. The marks are a blueprint telling you exactly how much to write and how to organise it." theme={theme}>SHAPE</Highlight> your answer should be. Here is how to decode them:</p>
              {/* The decoder: read-only lines ruled like rows (no boxes); the marks in ink, the meaning beside them */}
              <ul className="ex-list my-6">
                <li><p><span className="t-row text-ink-primary">(4 marks)</span><span className="text-ink-muted mx-2">=</span><span className="text-ink-primary">1-2 sentences. Name it and briefly explain.</span></p></li>
                <li><p><span className="t-row text-ink-primary">(10 marks)</span><span className="text-ink-muted mx-2">=</span><span className="text-ink-primary">A developed paragraph. Make a point, support it, explain it.</span></p></li>
                <li><p><span className="t-row text-ink-primary">(15 marks)</span><span className="text-ink-muted mx-2">=</span><span className="text-ink-primary">Two developed paragraphs OR one long one with multiple examples.</span></p></li>
                <li><p><span className="t-row text-ink-primary">(20-25 marks)</span><span className="text-ink-muted mx-2">=</span><span className="text-ink-primary">A structured mini-essay. Introduction, 2-3 body paragraphs, brief conclusion.</span></p></li>
                <li><p><span className="t-row text-ink-primary">(30+ marks)</span><span className="text-ink-muted mx-2">=</span><span className="text-ink-primary">Full essay structure. Every mark corresponds to roughly one strong sentence.</span></p></li>
                <li><p><span className="t-row text-ink-primary">(3 &times; 5 marks)</span><span className="text-ink-muted mx-2">=</span><span className="text-ink-primary">Three SEPARATE short answers, not one long one. Examiners mark each independently.</span></p></li>
                <li><p><span className="t-row text-ink-primary">(2 &times; 10 marks)</span><span className="text-ink-muted mx-2">=</span><span className="text-ink-primary">Two developed points. Give EXACTLY two, not three.</span></p></li>
              </ul>
              <p>The most common mistake is writing a <Highlight description="Writing too much for a small question wastes time. Writing too little for a big question loses marks. The mark allocation is the examiner's way of telling you exactly how much they expect." theme={theme}>4-mark answer for a 15-mark question</Highlight>, or a 15-mark answer for a 4-mark question. The marks tell you exactly how much to write. Reading them correctly is one of the simplest ways to improve your results.<Cite n={1} /></p>
              <ShapeQuiz />
            </ReadingSection>
          )}

          {!essentials && activeSection === 4 && (
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
              <p>The key insight: a <strong>well-structured partial answer collects every mark it earns — and can outscore a stronger but muddled one</strong>. The examiner can find and award <Highlight description="When your answer is structured with numbered points, definitions, and diagrams, the examiner can see every piece of knowledge you have. When it is buried in a paragraph, they might miss things — and missed points are missed marks." theme={theme}>every point you make</Highlight>, instead of hunting through a paragraph for buried insights.<Cite n={1} /></p>
              <PersonalStory name="Niamh, Leaving Cert 2023, Waterford">
                <p>"In my Chemistry exam, I got a question I barely knew. I wrote the formula, defined the terms, drew a diagram, and wrote what I did know in numbered points. I got 18 out of 25. My friend who knew more but wrote it as a paragraph got 14."</p>
              </PersonalStory>
            </ReadingSection>
          )}

          {!essentials && activeSection === 5 && (
            <ReadingSection title="Subject-Specific Structures." eyebrow="06 // The Toolkit" icon={Wrench} theme={theme}>
              <p>Here is a quick reference for the dominant answer structure in each subject family. Keep this in mind as you practise past papers.</p>
              {/* The reference card: one block per subject family, ruled like rows (no boxes) */}
              <div className="ex-list my-6">
                <div>
                  <h4 className="ex-block-title">Languages (English, Irish, French etc.)</h4>
                  <p className="ex-block-text"><strong className="text-ink-primary">PEEL for essays</strong>, quote-integrate-analyse for poetry and prose. Always embed quotes rather than dropping them in. Every paragraph should have a clear topic sentence.</p>
                </div>
                <div>
                  <h4 className="ex-block-title">Sciences (Biology, Chemistry, Physics)</h4>
                  <p className="ex-block-text"><strong className="text-ink-primary">S&sup3;S for calculations</strong>, "State-Explain-Example" for definitions, labelled diagrams everywhere. Every label on a diagram is a potential mark.</p>
                </div>
                <div>
                  <h4 className="ex-block-title">Business Subjects</h4>
                  <p className="ex-block-text"><strong className="text-ink-primary">Point-Explain-Example-Apply</strong> (the business PEEL variant). Always apply to a real business or the case study in the question.</p>
                </div>
                <div>
                  <h4 className="ex-block-title">Maths</h4>
                  <p className="ex-block-text"><strong className="text-ink-primary">Every line is a mark</strong> — never skip steps. Use the left column for working, right column for answers. Circle or underline final answers.</p>
                </div>
                <div>
                  <h4 className="ex-block-title">History / Geography</h4>
                  <p className="ex-block-text"><strong className="text-ink-primary">PEEL for essays</strong>, "Describe-Explain-Evaluate" for source analysis. Case Study structure for Geography — always name, locate, and describe the process.</p>
                </div>
                <div>
                  <h4 className="ex-block-title">Practical Subjects</h4>
                  <p className="ex-block-text"><strong className="text-ink-primary">Process documentation</strong> — materials, method, outcome, evaluation. Always explain <em>why</em> you chose a material or method, not just what you did.</p>
                </div>
              </div>
              <p>These command-word structures mirror what the marking schemes and Chief Examiner reports reward — for example, Business answers that State, Explain, and Example a developed point rather than name it in one word.<Cite n={2} /> This is a reference card, not deep teaching. Bookmark this section and come back to it when you are practising past papers in a specific subject.</p>
            </ReadingSection>
          )}

          {(essentials ? activeSection === 3 : activeSection === 6) && (
            <ReadingSection title="Your Engineering Toolkit." eyebrow={essentials ? "04 // The Plan" : "07 // The Plan"} icon={Target} theme={theme}>
              {essentials ? (
                <p>You now have the key frameworks: PEEL for essays, S&sup3;S for science, the marks-shape decoder, and the 60% rescue strategy.</p>
              ) : (
                <p>You now have <strong>four frameworks</strong> for building better answers:</p>
              )}
              {/* The four frameworks as numbered lines on the page (no boxes, no bordered number tags) */}
              <ol className="ex-nums">
                <li>
                  <span className="ex-num">1</span>
                  <div className="ex-num-copy"><p className="ex-num-title"><strong>PEEL</strong> for essay paragraphs</p></div>
                </li>
                <li>
                  <span className="ex-num">2</span>
                  <div className="ex-num-copy"><p className="ex-num-title"><strong>S&sup3;S</strong> for science and maths calculations</p></div>
                </li>
                <li>
                  <span className="ex-num">3</span>
                  <div className="ex-num-copy"><p className="ex-num-title"><strong>The marks-shape decoder</strong> for reading mark allocations</p></div>
                </li>
                <li>
                  <span className="ex-num">4</span>
                  <div className="ex-num-copy"><p className="ex-num-title"><strong>The 60% rescue strategy</strong> for partial answers</p></div>
                </li>
              </ol>
              <MicroCommitment theme={theme}>
                <p>Pick one past exam question from your <strong>strongest</strong> subject. Answer it using the right framework. Then pick one from your <strong>weakest</strong> subject. Compare how it feels — that is the difference structure makes.</p>
              </MicroCommitment>
              <p className="mt-8 t-row text-ink-primary">Knowledge gets you in the door. Structure gets you the marks. You have always had the knowledge — now you have the engineering.</p>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};

export default AnswerEngineeringModule;
