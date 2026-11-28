
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useId, useState, useRef } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import {
  Target, Brain, SlidersHorizontal, AlertTriangle, PenTool, Key, BookOpen, Wrench
} from 'lucide-react';
import { type ModuleProgress } from '../types';
import { grayTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory, ConceptCardGrid } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { AnswerGroup, AnswerLine, AnswerTick, ExerciseSheet } from './learning/Exercise';
import { Button } from './ui/Button';
import { ChoiceTile } from './ui/Choice';
import { AreaField } from './ui/Field';

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
        <ExerciseSheet title="Partial Credit Calculator" sub="Scenario: 10-mark Scale D Question. How many marks do you get?" name="PartialCreditCalculator">
             {/* What you did on the question: several may be chosen (a slip and a blunder replace each other) */}
             <AnswerGroup kind="several" columns={2}>
                <ChoiceTile kind="several" tile chosen={steps.formula} onClick={() => setSteps(s => ({...s, formula: !s.formula}))} label="Wrote correct formula" />
                <ChoiceTile kind="several" tile chosen={steps.sub} onClick={() => setSteps(s => ({...s, sub: !s.sub}))} label="Substituted a value" />
                <ChoiceTile kind="several" tile chosen={steps.slip} onClick={() => setSteps(s => ({...s, slip: !s.slip, blunder: false}))} label="Made a minor calculation 'Slip'" />
                <ChoiceTile kind="several" tile chosen={steps.blunder} onClick={() => setSteps(s => ({...s, blunder: !s.blunder, slip: false}))} label="Made a major concept 'Blunder'" />
             </AnswerGroup>
             {/* The marks it comes to: said under a hairline, the figure in ink (no green panel) */}
             <div className="ex-result">
                <p className="ex-sub">
                    You get <span className="ex-result-name">{marks}/10</span> marks.
                </p>
            </div>
        </ExerciseSheet>
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
        <ExerciseSheet title="Problem Sorter" sub="Train your discriminative skills: Is it a Permutation (order matters) or a Combination (order doesn't)?" name="ProblemSorter">
            {/* Each problem is its question; the right answer, once chosen, carries the green tick (no mint or coral fill) */}
            <div className="ex-questions">
            {problems.map(p => (
                <AnswerGroup key={p.id} kind="one" columns={2} chooseOnArrow={false} legend={p.text}>
                    <ChoiceTile tile chosen={choice[p.id] === 'p'} onClick={() => handleChoice(p.id, 'p')} label={<span className="inline-flex items-center gap-2">Permutation{choice[p.id] === 'p' && p.type === 'p' ? <AnswerTick /> : null}</span>} />
                    <ChoiceTile tile chosen={choice[p.id] === 'c'} onClick={() => handleChoice(p.id, 'c')} label={<span className="inline-flex items-center gap-2">Combination{choice[p.id] === 'c' && p.type === 'c' ? <AnswerTick /> : null}</span>} />
                </AnswerGroup>
            ))}
            </div>
        </ExerciseSheet>
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

  // The paper the student pressed, read back from the feedback while it shows (a right answer is the
  // question's paper, a wrong one the other), so the pressed answer carries the ink outline.
  const pressed = (paper: 'paper1' | 'paper2') =>
    feedback !== null && questions.length > 0 && (feedback.correct ? questions[currentIndex].answer === paper : questions[currentIndex].answer !== paper);

  return (
    <ExerciseSheet title="Paper Predictor" name="PaperPredictorGame">

      {phase === 'intro' && (
        <div className="ex-stack">
          <p className="ex-sub">
            <strong>Paper 1</strong> = Pure / Technical. <strong>Paper 2</strong> = Context / Applied.
          </p>
          <p className="ex-sub">Can you sort 12 question stems as fast as possible?</p>
          <div className="ex-actions">
            <Button onClick={startGame}>
              Start Game
            </Button>
          </div>
        </div>
      )}

      {phase === 'playing' && questions.length > 0 && (
        <div className="ex-stack">
          {/* Where you are, the score, the streak and the clock, in the readout (no pills) */}
          <div className="flex flex-wrap items-center justify-between gap-x-4 gap-y-1">
            <span className="ex-count ui-readout">
              {currentIndex + 1} / {questions.length}
            </span>
            <span className="ui-readout text-ink-primary">
              Score: {score}
            </span>
            <span className="ui-readout text-ink-primary">
              Streak: {streak}
            </span>
            <span className="ui-readout text-ink-muted">
              {formatTime(elapsedTime)}
            </span>
          </div>

          {/* The question: words you read, on the sheet under a hairline (no tinted card) */}
          <AnimatePresence mode="wait">
            <MotionDiv
              key={questions[currentIndex].id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.25 }}
              className="ex-block min-h-[96px]"
            >
              <p className="t-heading text-ink-primary">
                {questions[currentIndex].text}
              </p>
              {feedback && !feedback.correct && (
                <AnswerLine tone="note">
                  {feedback.explanation}
                </AnswerLine>
              )}
            </MotionDiv>
          </AnimatePresence>

          {/* The two answers: pressing one marks it and moves on (the right one carries the green tick) */}
          <AnswerGroup kind="one" columns={2} chooseOnArrow={false}>
            <ChoiceTile
              tile
              chosen={pressed('paper1')}
              onClick={() => handleAnswer('paper1')}
              disabled={feedback !== null}
              label={<span className="inline-flex items-center gap-2">Paper 1{pressed('paper1') && feedback?.correct ? <AnswerTick /> : null}</span>}
            />
            <ChoiceTile
              tile
              chosen={pressed('paper2')}
              onClick={() => handleAnswer('paper2')}
              disabled={feedback !== null}
              label={<span className="inline-flex items-center gap-2">Paper 2{pressed('paper2') && feedback?.correct ? <AnswerTick /> : null}</span>}
            />
          </AnswerGroup>
        </div>
      )}

      {phase === 'results' && (
        <div className="ex-stack">
          {/* Score display: the figure in ink, said in words under it */}
          <div className="ex-result">
            <p className="ex-result-name">{score}<span className="text-ink-muted">/{questions.length}</span></p>
            <p className="ex-sub">
              {Math.round((score / questions.length) * 100)}% accuracy in {formatTime(elapsedTime)}
            </p>
          </div>

          {/* Result stats, in the readout (no pills) */}
          <div className="flex flex-wrap items-center gap-x-4 gap-y-1">
            <span className="ui-readout text-ink-primary">
              Best streak: {bestStreak}
            </span>
            <span className="ui-readout text-ink-muted">
              Time: {formatTime(elapsedTime)}
            </span>
          </div>

          {/* Summary insight: words you read, under a hairline (no box) */}
          <div className="ex-block">
            <p className="ex-block-text">
              <strong>Paper 1</strong> = pure maths (algebra, calculus, proofs). <strong>Paper 2</strong> = maths in context (statistics, applied problems, modelling).
            </p>
          </div>

          <div className="ex-actions">
            <Button onClick={startGame}>
              Play Again
            </Button>
          </div>
        </div>
      )}
    </ExerciseSheet>
  );
};

const ErrorLog = () => {
    const [error, setError] = useState('');
    const [type, setType] = useState<string | null>(null);
    const titleId = useId();

    return(
         <ExerciseSheet id={titleId} title="My Error Log" sub="Log a mistake from a practice question to turn it into a learning opportunity." name="ErrorLog">
                {/* The written answer, named by the exercise's title */}
                <AreaField aria-labelledby={titleId} value={error} onChange={e => setError(e.target.value)} placeholder="Describe the mistake..." rows={3} />
                {/* The kind of error: one answer */}
                <AnswerGroup kind="one">
                    <ChoiceTile chosen={type === 'Concept'} onClick={() => setType('Concept')} label="Concept Error" />
                    <ChoiceTile chosen={type === 'Procedural'} onClick={() => setType('Procedural')} label="Procedural Error" />
                    <ChoiceTile chosen={type === 'Reading'} onClick={() => setType('Reading')} label="Reading Error" />
                </AnswerGroup>
             {error && type && <AnswerLine>Error logged. Now you won't make it again.</AnswerLine>}
        </ExerciseSheet>
    );
};

// --- MODULE COMPONENT ---
const LearningMathModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
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
              {essentials ? (<>
              <p>Project Maths changed the rules. You need to <Highlight description="It's not enough to know the formula. You need to understand why it works, so you can use it in questions you've never seen before." theme={theme}>understand why things work</Highlight>, not just memorise steps. The <Highlight description="You get 25 extra CAO points just for getting a H6 or higher in Maths. That makes it the single most valuable subject for your points." theme={theme}>Bonus Points</Highlight> give you 25 extra CAO points for a H6 or above. With those bonus points a H6 in Maths (71 points) beats a H4 in any other subject (66 points). Higher Level is worth trying even if you find maths hard.</p>
              </>) : (<>
              <p>Leaving Cert Maths is not the same game it used to be. Project Maths changed the rules -- it's no longer about memorising formulas and repeating steps. Now it's about actually <Highlight description="It's not enough to know the formula. You need to understand why it works, so you can use it in questions you've never seen before." theme={theme}>understanding why things work</Highlight> and solving problems you've never seen before. It's a test of resilience, not just number-crunching.</p>
              <p>Then there are the <Highlight description="You get 25 extra CAO points just for getting a H6 or higher in Maths. That makes it the single most valuable subject for your points." theme={theme}>Bonus Points</Highlight> -- 25 extra CAO points just for getting a H6 or above. That means a H6 in Maths (71 points with the bonus) is worth more than a H4 in any other subject (66 points). It's a massive safety net, and it means aiming for Higher Level is worth it even if you're not a "maths person."</p>
              </>)}
              <PersonalStory name="Orlaith" role="6th Year, Tallaght">
                <p>I nearly dropped to Ordinary Level after 5th year because I got 38% in my summer exam. But my teacher said "just try Higher for the mocks." I started using the bonus points as motivation -- even a H6 would be worth it. I ended up getting a H5 in the real thing and those 25 bonus points got me into my course. Honestly, if I'd dropped down I wouldn't have made it.</p>
              </PersonalStory>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Two Papers." eyebrow="Step 2" icon={BookOpen} theme={theme}>
              {essentials ? (<>
              <p><strong>Paper 1</strong> is the "Technical" paper: Algebra, Calculus, and Number. You need to be <Highlight description="Being able to do the steps quickly and accurately -- solving equations, differentiating, that kind of thing." theme={theme}>quick and accurate with the steps</Highlight>. <strong>Paper 2</strong> is the "Contextual" paper: Statistics, Probability, Geometry, Trigonometry in real-world scenarios. It is unpredictable. You must understand ideas, not just memorise methods. Try the game below to practise sorting questions.</p>
              </>) : (<>
              <p>The exam is split into two papers, and they feel quite different. <strong>Paper 1</strong> is the <strong>"Technical"</strong> paper. It's mostly Algebra, Calculus, and Number -- the kind of maths where you need to be <Highlight description="Being able to do the steps quickly and accurately -- solving equations, differentiating, that kind of thing." theme={theme}>quick and accurate with the steps</Highlight>. Less reading, more doing.</p>
              <p><strong>Paper 2</strong> is the <strong>"Contextual"</strong> paper. This covers Statistics, Probability, Geometry, and Trigonometry -- and the questions are wrapped in real-world scenarios. It's often called the "unpredictable" paper because one weird diagram can throw you off if you've only memorised methods without actually understanding the ideas behind them.</p>
              </>)}
              <PaperPredictorGame />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Five Strands." eyebrow="Step 3" icon={SlidersHorizontal} theme={theme}>
              {essentials ? (<>
              <p>Five areas, all connected. The exam mixes them, so you might use <Highlight description="Questions often blend topics together. You might need Algebra to solve a Geometry problem, or Probability inside a Calculus question." theme={theme}>Algebra to solve a Geometry problem</Highlight>. You cannot study topics in isolation.</p>
              </>) : (<>
              <p>The course is divided into five big areas. Here's the thing -- they're all connected. The exam deliberately mixes them together, so a question might use <Highlight description="Questions often blend topics together. You might need Algebra to solve a Geometry problem, or Probability inside a Calculus question." theme={theme}>Algebra to solve a Geometry problem</Highlight>. You can't just study one topic on its own and hope for the best.</p>
              <p>The five areas are:</p>
              </>)}
              <ConceptCardGrid
                columns={2}
                cards={[
                  { number: 1, term: "Statistics & Probability", description: "Lots of reading and interpreting." },
                  { number: 2, term: "Geometry & Trigonometry", description: "Visual, diagrams everywhere." },
                  { number: 3, term: "Number", description: "The basics, including Complex Numbers." },
                  { number: 4, term: "Algebra", description: "It's the language that runs through everything." },
                  { number: 5, term: "Functions & Calculus", description: "The biggest chunk of Paper 1." },
                ]}
              />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="How Marking Actually Works." eyebrow="Step 4" icon={Key} theme={theme}>
              {essentials ? (<>
              <p>The SEC uses <Highlight description="You get marks for what you get right -- they don't take marks away for mistakes. Any progress you show counts." theme={theme}>"Positive Marking"</Highlight>. They reward what you get right. On Scale D questions (the most common), writing the formula and plugging in one value gets you 3 out of 10 marks. That is 30% for minimal work. This adds up fast across a whole paper.</p>
              </>) : (<>
              <p>Understanding how marks are given out is honestly your biggest advantage. The SEC uses <Highlight description="You get marks for what you get right -- they don't take marks away for mistakes. Any progress you show counts." theme={theme}>"Positive Marking"</Highlight> -- they reward you for what you get right, not punish you for what you get wrong. They use a Scale System (A, B, C, D) to decide how marks are split up.</p>
              <p><strong>Scale A</strong> (0 or 10) is rare -- it's all or nothing. <strong>Scale B</strong> (0, 5, or 10) is "hit or miss." But <strong>Scale C</strong> (0, 3, 7, 10) and <strong>Scale D</strong> (0, 3, 5, 8, 10) are the ones you'll see most. Here's the key: on a Scale D question, just writing down the right formula and plugging in one value can get you 3 marks out of 10. That's 30% for barely anything -- and it adds up fast across a whole paper.</p>
              </>)}
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Never Leave a Question Blank." eyebrow="Step 5" icon={Wrench} theme={theme}>
              {essentials ? (<>
              <p>Never leave a question blank. Write the formula and substitute one value. That alone gets you 3 marks. Blank gets you zero. These small marks across a paper can be the difference between a H4 and a H3. Hunt for every mark: formulas, definitions, diagrams.</p>
              </>) : (<>
              <p>This is the golden rule of Higher Level Maths: <strong>never, ever leave a question blank</strong>. If you hit a 10-mark question that looks impossible, just write down the relevant formula from the log tables and substitute one value. That alone often gets you 3 marks. Leaving it blank gets you zero. It's that simple.</p>
              <p>Picking up these small marks across a whole paper can genuinely be the difference between a H4 and a H3. Your goal is to never score zero on any question. Even on the trickiest questions, there are marks going for writing a formula, defining a term, or drawing a diagram. Train yourself to hunt for those marks -- they're there for the taking.</p>
              </>)}
              <PartialCreditCalculator />
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Spotting the Patterns." eyebrow="Step 6" icon={Brain} theme={theme}>
              {essentials ? (<>
              <p>Past papers reveal clear trends. Paper 1 asks more applied Calculus. Paper 2 has <Highlight description="Those weird questions with diagrams or setups you've never seen before. They test whether you actually understand the ideas, not just the steps." theme={theme}>"Gremlin" questions</Highlight> that look unfamiliar, plus <Highlight description="Questions that mix two topics together, like working out a probability using the area of a shape. They want to see if you can connect different ideas." theme={theme}>crossover questions</Highlight> blending topics. These catch anyone who only memorised steps. You must understand the ideas behind the methods.</p>
              </>) : (<>
              <p>If you look at past papers, clear patterns jump out. Paper 1 is asking more and more about applied Calculus (rates of change in real situations) and treating Complex Numbers like geometry. Paper 2 keeps throwing in <Highlight description="Those weird questions with diagrams or setups you've never seen before. They test whether you actually understand the ideas, not just the steps." theme={theme}>"Gremlin" questions</Highlight> -- the ones that look totally unfamiliar -- and <Highlight description="Questions that mix two topics together, like working out a probability using the area of a shape. They want to see if you can connect different ideas." theme={theme}>crossover questions</Highlight> that blend Probability with Geometry. These are designed to catch out anyone who's only memorised steps without understanding the ideas behind them.</p>
              </>)}
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="What Examiners Actually Look For." eyebrow="Step 7" icon={AlertTriangle} theme={theme}>
              {essentials ? (<>
              <p>Three common mistakes cost marks every year. <Highlight description="You understand the idea, but you mess up the algebra -- wrong signs, index errors, silly slips that cost you marks." theme={theme}>Sloppy algebra</Highlight>: sign errors and index mistakes. <Highlight description="Not checking if your answer makes sense. Like getting a probability of 1.3 or a negative length -- a quick check would catch those." theme={theme}>Not checking answers</Highlight>: like getting a probability over 1. <Highlight description="When a question is wrapped in a real-world story you haven't seen before, and you freeze because it doesn't look like your textbook." theme={theme}>Freezing on unfamiliar questions</Highlight>. For "Show That" questions, if you get stuck, write "Assuming x=5, I'll continue..." and keep going.</p>
              </>) : (<>
              <p>The Examiner's Reports tell you exactly where students lose marks every year. The biggest one is <Highlight description="You understand the idea, but you mess up the algebra -- wrong signs, index errors, silly slips that cost you marks." theme={theme}>sloppy algebra</Highlight> -- you get the concept but mess up the execution with sign errors or index mistakes. The second is <Highlight description="Not checking if your answer makes sense. Like getting a probability of 1.3 or a negative length -- a quick check would catch those." theme={theme}>not checking your answers</Highlight> (getting a probability greater than 1 and not noticing). The third is <Highlight description="When a question is wrapped in a real-world story you haven't seen before, and you freeze because it doesn't look like your textbook." theme={theme}>freezing on unfamiliar questions</Highlight> -- when a question is wrapped in a story you've never seen, your brain goes blank.</p>
              <p>One big trap: "Show That" questions. If you can't get to the answer they want, don't force it or fudge the working. Instead, write something like "I can't get to this result, but assuming x=5, I'll continue..." -- and then keep going. This way you can still pick up marks on the rest of the question.</p>
              </>)}
              <ProblemSorter />
            </ReadingSection>
          )}
          {activeSection === 7 && (
            <ReadingSection title="Study Smarter for Maths." eyebrow="Step 8" icon={Brain} theme={theme}>
              {essentials ? (<>
              <p>Stop <Highlight description="When you do nothing but Algebra questions for a whole study session. It feels productive, but you're not training your brain to switch between topics like the exam requires." theme={theme}>doing the same topic for hours</Highlight>. <Highlight description="Mix up your topics in a single study session -- do an Algebra question, then a Geometry one, then Probability. It feels harder, but it trains your brain the way the exam actually works." theme={theme}>Mix up your topics</Highlight> in each session. <Highlight description="Close the book and try to do the problem from memory. If you can't, that tells you exactly what you need to work on." theme={theme}>Test yourself</Highlight> with the book closed. Keep an <Highlight description="Write down every mistake you make, sort it by type (didn't understand the idea, messed up the steps, or misread the question), and review it before exams." theme={theme}>Error Log</Highlight>: write down every mistake, sort by type, review before exams.</p>
              </>) : (<>
              <p>Here's how to actually get better at Maths (not just feel like you're getting better). First, stop <Highlight description="When you do nothing but Algebra questions for a whole study session. It feels productive, but you're not training your brain to switch between topics like the exam requires." theme={theme}>doing the same topic for hours</Highlight>. Instead, <Highlight description="Mix up your topics in a single study session -- do an Algebra question, then a Geometry one, then Probability. It feels harder, but it trains your brain the way the exam actually works." theme={theme}>mix up your topics</Highlight> within a single session. It feels harder, but it's closer to what the actual exam is like, and it builds the kind of knowledge that sticks.</p>
              <p>Reading over your notes doesn't work for Maths. You need to <Highlight description="Close the book and try to do the problem from memory. If you can't, that tells you exactly what you need to work on." theme={theme}>test yourself</Highlight> -- close the book, try to do the problem, and see what happens. And keep an <Highlight description="Write down every mistake you make, sort it by type (didn't understand the idea, messed up the steps, or misread the question), and review it before exams." theme={theme}>Error Log</Highlight> -- write down every mistake you make on past papers, sort them by type, and review them. The real learning happens after you finish a past paper, when you figure out what went wrong.</p>
              </>)}
              <ErrorLog />
            </ReadingSection>
          )}
          {activeSection === 8 && (
            <ReadingSection title="The H1 Pathway." eyebrow="Step 9" icon={PenTool} theme={theme}>
              {essentials ? (<>
              <p>For a H1, speed matters. Get through Section A fast so you have time for Section B. Learn your <Highlight description="Things like the proof by induction, the proof that root 2 is irrational, or definitions like 'injective function'. Learn them perfectly -- if they come up, they're easy marks." theme={theme}>guaranteed marks</Highlight>: a few formal proofs and definitions come up regularly. Learn them perfectly. They are free marks on exam day.</p>
              </>) : (<>
              <p>If you're going for a H1, it's not just about knowing the material -- it's about speed and awareness. H1 students get through the routine Section A questions quickly so they have more time for the harder Section B questions. That speed comes from practice, not from being naturally faster.</p>
              <p>Here's a tip: there are a handful of things in Maths that you can just learn off by heart. These are your <Highlight description="Things like the proof by induction, the proof that root 2 is irrational, or definitions like 'injective function'. Learn them perfectly -- if they come up, they're easy marks." theme={theme}>guaranteed marks</Highlight>. A few formal proofs and definitions come up regularly, and if you know them perfectly, they're basically free marks on the day.</p>
              </>)}
              <MicroCommitment theme={theme}><p>Go to your log tables. Pick one proof (like the Cos(A+B) formula). Spend 15 minutes learning it by closing the book and writing it out from memory. You've just locked in a potential 10 marks.</p></MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default LearningMathModule;
