/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { AnimatePresence,motion } from 'framer-motion';
import {
AlertTriangle,
BarChart,Brain,
MessageCircle,
Settings,
User
} from 'lucide-react';
import React,{ useEffect,useRef,useState } from 'react';
import { PRAISE_PROTOCOL_REFERENCE_LIST } from '../data/references/praiseProtocol';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { limeTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { Highlight,MicroCommitment,ReadingSection } from './ModuleShared';
import { MotionDiv } from './Motion';
import { AnswerGroup,AnswerLine,ExerciseLabel,ExerciseSheet } from './learning/Exercise';
import { Button,TextButton } from './ui/Button';
import { ChoiceTile } from './ui/Choice';

const theme = limeTheme;

// --- INTERACTIVE COMPONENTS ---

const DweckExperimentSimulator = () => {
    const [step, setStep] = useState(0); // 0: Start, 1: Praise Choice, 2: Task Choice, 3: Failure, 4: Result
    const [praiseType, setPraiseType] = useState<'person'|'process'|null>(null);
    const [taskChoice, setTaskChoice] = useState<'easy'|'hard'|null>(null);
    const failureTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
    const resultTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

    useEffect(() => {
        return () => {
            if (failureTimerRef.current) clearTimeout(failureTimerRef.current);
            if (resultTimerRef.current) clearTimeout(resultTimerRef.current);
        };
    }, []);

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
        failureTimerRef.current = setTimeout(() => setStep(3), 2000); // Auto-advance to failure
        resultTimerRef.current = setTimeout(() => setStep(4), 4000); // Auto-advance to result
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
        <ExerciseSheet title="The Praise Experiment" sub="You just aced a test. Walk through this experiment and see what happens next depending on what you're told." name="DweckExperimentSimulator">
             {/* The two meters: an ink fill on a hairline track (no coral or green bars) */}
             <div className="grid grid-cols-2 gap-6">
                <div className="flex flex-col gap-2">
                    <p className="ex-label">Resilience Meter</p>
                    <div className="w-full h-2 rounded" style={{ backgroundColor: 'var(--hairline)' }}><motion.div className="h-full rounded" style={{ backgroundColor: 'var(--ink-primary)' }} initial={{width: "50%"}} animate={{width: `${resilience}%`}} /></div>
                </div>
                <div className="flex flex-col gap-2">
                    <p className="ex-label">Performance Meter</p>
                    <div className="w-full h-2 rounded" style={{ backgroundColor: 'var(--hairline)' }}><motion.div className="h-full rounded" style={{ backgroundColor: 'var(--ink-primary)' }} initial={{width: "50%"}} animate={{width: `${performance}%`}} /></div>
                </div>
            </div>

            <AnimatePresence mode="wait">
                <motion.div key={step} initial={{opacity:0, x:20}} animate={{opacity:1, x:0}} exit={{opacity:0, x:-20}} className="ex-stack">
                    {step === 0 && <>
                        <AnswerGroup kind="one" legend="Phase 1: Choose your praise" columns={2} chooseOnArrow={false}>
                            <ChoiceTile tile chosen={praiseType === 'person'} onClick={() => handlePraise('person')} label={'"You must be smart at this."'} />
                            <ChoiceTile tile chosen={praiseType === 'process'} onClick={() => handlePraise('process')} label={'"You must have worked hard at this."'} />
                        </AnswerGroup>
                    </>}
                    {step === 1 && <>
                        <AnswerGroup kind="one" legend="Phase 2: Choose your next task" columns={2} chooseOnArrow={false}>
                            <ChoiceTile tile chosen={taskChoice === 'easy'} onClick={() => handleTask('easy')} label="An easy one (to look smart)" />
                            <ChoiceTile tile chosen={taskChoice === 'hard'} onClick={() => handleTask('hard')} label="A hard one (to learn more)" />
                        </AnswerGroup>
                    </>}
                    {step === 2 && <p className="t-body text-ink-primary">You chose the <b>{taskChoice}</b> task...</p>}
                    {step === 3 && <AnswerLine tone="note">Phase 3: Induced Failure. You are given a much harder test and perform poorly...</AnswerLine>}
                    {step === 4 && <>
                        <ExerciseLabel>Phase 4: Final Results</ExerciseLabel>
                        {praiseType === 'person' && <AnswerLine tone="note">Because your identity was tied to being "smart", failure was devastating. Your resilience and subsequent performance dropped.</AnswerLine>}
                        {praiseType === 'process' && <AnswerLine>Because your identity was tied to "working hard", the failure was seen as a challenge. Your resilience and subsequent performance increased.</AnswerLine>}
                        <div className="ex-actions">
                            <Button onClick={reset}>Run Again</Button>
                        </div>
                    </>}
                </motion.div>
            </AnimatePresence>
        </ExerciseSheet>
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

    // Each trace is drawn in ink on the sheet under its own label (no coral or mint panel behind it).
    const traces = [
      { label: 'Fixed Mindset', path: fixedPath, color: "var(--ink-primary)", peLabel: 'Small Pe', peDesc: 'Brain flinches away to protect your ego' },
      { label: 'Growth Mindset', path: growthPath, color: "var(--ink-primary)", peLabel: 'Large Pe', peDesc: 'Brain pays close attention to learn from it' },
    ];

    return (
      <ExerciseSheet title="What Your Brain Does With Mistakes" sub="When you make a mistake, your brain fires two signals. The second one is where your mindset makes all the difference." name="ErrorSignalVisualizer">
        <div className="ex-list">
          {traces.map((trace, i) => (
            <div key={i}>
              <div className="flex flex-wrap items-baseline justify-between gap-x-3 gap-y-1">
                <p className="ex-label">{trace.label}</p>
                {active && (
                  <motion.p
                    initial={{ opacity: 0, x: 10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.6 }}
                    className="t-meta text-ink-secondary"
                  >
                    {trace.peLabel} — {trace.peDesc}
                  </motion.p>
                )}
              </div>

              <svg viewBox={`0 0 ${W} ${H}`} className="w-full h-auto" preserveAspectRatio="none">
                {/* Gridlines */}
                {[0.25, 0.5, 0.75].map(t => (
                  <line key={t} x1={0} y1={H * t} x2={W} y2={H * t} stroke="var(--hairline)" strokeWidth="0.5" />
                ))}
                {/* Baseline center */}
                <line x1={0} y1={midY} x2={W} y2={midY} stroke="var(--outline-soft)" strokeWidth="0.8" strokeDasharray="4 4" />

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
                      fill="var(--ink-muted)"
                      fontSize="11"
                      style={{ fontFamily: 'var(--font-ui)' }}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
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
                      fill="var(--ink-muted)"
                      fontSize="11"
                      style={{ fontFamily: 'var(--font-ui)' }}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
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
              <div className="ex-slider-ends">
                <span>0 ms</span>
                <span>Time</span>
                <span>800 ms</span>
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
            className="flex flex-wrap gap-x-6 gap-y-2"
          >
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-sm shrink-0" style={{ border: '1.5px dashed var(--ink-primary)' }} />
              <span className="t-meta">ERN (Error detected — same for both)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-sm shrink-0" style={{ backgroundColor: 'var(--outline-soft)' }} />
              <span className="t-meta">Pe (Attention to error — differs by mindset)</span>
            </div>
          </motion.div>
        )}

        <div className="ex-actions">
          <Button onClick={() => setActive(!active)}>
            {active ? 'Reset Signal' : 'Make an Error'}
          </Button>
          {active && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
            >
              <TextButton onClick={() => setShowExplainer(!showExplainer)}>
                {showExplainer ? 'Hide Explanation' : 'What am I looking at?'}
              </TextButton>
            </motion.div>
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
              {/* The explanation: words you read, under a hairline, not in a box */}
              <div className="ex-block">
                <p className="ex-block-text"><strong>ERN (the first signal)</strong> fires within a tenth of a second of making a mistake. Both mindsets produce the same signal here. Your brain always spots the error.</p>
                <p className="ex-block-text"><strong>Pe (the second signal)</strong> comes a fraction of a second later. This is where mindset makes the difference. It shows how much <em>attention</em> your brain gives to the mistake.</p>
                <p className="ex-block-text">A <strong>fixed mindset</strong> brain produces a tiny Pe — it spots the error but quickly looks away to protect your ego. A <strong>growth mindset</strong> brain produces a huge Pe — it zooms in on the error, trying to figure out what went wrong so it can do better next time. This is why students with a growth mindset tend to pay more attention to an error and improve on the next try.</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </ExerciseSheet>
    );
};

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

  // The clock is ink once ten seconds are left; until then it sits with the other readouts in ink-3.
  const timerColor = timeLeft <= 10 ? "text-ink-primary" : "text-ink-muted";

  return (
    <ExerciseSheet title="Praise Decoder Game" sub="Categorise each praise statement as fast as you can. You have 30 seconds." name="PraiseDecoderGame">
      {gameState === 'idle' && (
        <div className="ex-stack">
          {/* How to play: words on the sheet, the two categories as small capitals (no tinted pills) */}
          <div className="ex-block">
            <p className="ex-block-text">Praise statements will flash on screen. Tap the correct category:</p>
            <div className="flex flex-wrap gap-x-6 gap-y-1">
              <span className="ex-label">Person Praise</span>
              <span className="ex-label">Process Praise</span>
            </div>
          </div>
          <div className="ex-actions">
            <Button onClick={startGame}>
              Start Game
            </Button>
          </div>
        </div>
      )}

      {gameState === 'playing' && currentStatement && (
        <div className="ex-stack">
          {/* Stats row: readouts, not tinted pills */}
          <div className="flex flex-wrap gap-x-5 gap-y-1">
            <span className={`ui-readout ${timerColor}`}>
              {timeLeft}s
            </span>
            <span className="ui-readout text-ink-muted">
              Score: {score}
            </span>
            <span className="ui-readout text-ink-muted">
              Streak: {streak}
            </span>
            <span className="ui-readout text-ink-muted">
              Accuracy: {accuracy}%
            </span>
          </div>

          {/* The statement: words you read, set large on the sheet (no box round them) */}
          <AnimatePresence mode="wait">
            <MotionDiv
              key={currentIndex + '-' + statements[currentIndex]?.text}
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{
                opacity: 1,
                scale: 1,
                y: 0,
              }}
              exit={{ opacity: 0, scale: 0.9, y: -20 }}
              transition={{ type: 'spring', stiffness: 300, damping: 25 }}
              className="ex-thought py-4"
              style={{ borderTop: '1px solid var(--hairline)', borderBottom: '1px solid var(--hairline)' }}
            >
              <p className="ex-thought-words">
                {currentStatement.text}
              </p>
              {feedback === 'wrong' && wrongExplanation && (
                <motion.div
                  initial={{ opacity: 0, y: 5 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  <AnswerLine tone="note">{wrongExplanation}</AnswerLine>
                </motion.div>
              )}
            </MotionDiv>
          </AnimatePresence>

          {/* Buttons: the exercise's own white buttons; disabled while a card shows its feedback, as before */}
          <div className="grid grid-cols-2 gap-3 w-full">
            <Button
              block
              onClick={() => handleAnswer('person')}
              className="disabled:opacity-50"
              {...{ disabled: feedback !== null }}
            >
              Person Praise
            </Button>
            <Button
              block
              onClick={() => handleAnswer('process')}
              className="disabled:opacity-50"
              {...{ disabled: feedback !== null }}
            >
              Process Praise
            </Button>
          </div>
        </div>
      )}

      {gameState === 'finished' && (
        <MotionDiv
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ type: 'spring', stiffness: 200, damping: 20 }}
          className="ex-stack"
        >
          {/* The result: the score in ink and its words under it, not in boxes */}
          <div className="ex-result">
            <p className="ex-result-name">{score}</p>
            <p className="ex-sub">correct answers</p>
          </div>

          <div className="grid grid-cols-3 gap-4 pt-3" style={{ borderTop: '1px solid var(--hairline)' }}>
            <div className="flex flex-col gap-1">
              <p className="t-row text-ink-primary">{accuracy}%</p>
              <p className="ex-label">Accuracy</p>
            </div>
            <div className="flex flex-col gap-1">
              <p className="t-row text-ink-primary">{bestStreak}</p>
              <p className="ex-label">Best Streak</p>
            </div>
            <div className="flex flex-col gap-1">
              <p className="t-row text-ink-primary">{totalAnswered}</p>
              <p className="ex-label">Answered</p>
            </div>
          </div>

          {accuracy >= 80 && (
            <AnswerLine>
              Excellent! You can clearly distinguish person praise from process praise. That awareness is the first step to rewiring your mindset.
            </AnswerLine>
          )}
          {accuracy >= 50 && accuracy < 80 && (
            <AnswerLine tone="note">
              Good effort! Some of those statements are tricky. Play again to sharpen your decoder skills.
            </AnswerLine>
          )}
          {accuracy < 50 && (
            <AnswerLine tone="note">
              The line between person and process praise can be subtle. Give it another go — your brain will get faster at spotting the difference.
            </AnswerLine>
          )}

          <div className="ex-actions">
            <Button onClick={startGame}>
              Play Again
            </Button>
          </div>
        </MotionDiv>
      )}
    </ExerciseSheet>
  );
};

// --- MODULE COMPONENT ---
const ThePraiseProtocolModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
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
      references={PRAISE_PROTOCOL_REFERENCE_LIST}
      finishButtonText="Choose Your Words"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Praise Paradox." eyebrow="Step 1" icon={MessageCircle} theme={theme}>
              {essentials ? (
                <>
                  <p>Not all praise helps you. Some praise actually makes you afraid to fail. There are two types. <Highlight description="Praising who you are — 'You're so smart.' Makes you fear mistakes." theme={theme}>Person Praise</Highlight> focuses on who you are. <Highlight description="Praising what you did — 'You worked hard.' Makes you want to keep improving." theme={theme}>Process Praise</Highlight> focuses on what you do. Person praise makes you fragile. Process praise makes you resilient. Learn to spot the difference below.</p>
                </>
              ) : (
                <>
                  <p>We've been told our whole lives that praise builds confidence. But what if some types of praise are actually a trap? This is the praise paradox. The words you hear — and the words you tell yourself — aren't just nice things to say. They actually shape how your brain deals with success and failure going forward.</p>
                  <p>There are basically two types of praise. <Highlight description="This is when someone praises who you are — like saying 'You're so smart' or 'You're a natural.' It sounds nice, but it makes you afraid to mess up because you start thinking your ability is just something you either have or don't." theme={theme}>Person Praise</Highlight> focuses on who you <em>are</em>. <Highlight description="This is when someone praises what you did — like 'You worked really hard on that' or 'That was a great strategy.' This kind of praise is way more useful because it makes you want to keep trying and improving." theme={theme}>Process Praise</Highlight> focuses on what you <em>do</em>. One makes you fragile, the other makes you resilient. Knowing the difference is a game-changer.</p>
                </>
              )}
              <PraiseDecoderGame />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Praise Experiment." eyebrow="Step 2" icon={BarChart} theme={theme}>
                {essentials ? (
                  <>
                    <p>Students aced a test. Half were told "you're smart." Half were told "you worked hard." One sentence changed everything. The "smart" group played it safe and gave up after failure. Nearly 40% lied about their scores.<Cite n={1} /> The "hard-working" group chose harder tasks and bounced back. Try the simulation below.</p>
                  </>
                ) : (
                  <>
                    <p>Here's an experiment that shows just how powerful one sentence of praise can be. A group of students were all given a test, told they did well, and then given one of two responses: "You must be smart" (Person Praise) or "You must have worked hard" (Process Praise). That's it — one sentence.</p>
                    <p>The findings were striking. The "smart" kids immediately started playing it safe, choosing easier tasks so they wouldn't risk looking stupid. When they hit a harder problem and failed, they gave up, their scores tanked, and nearly 40% of them lied about how they did.<Cite n={1} /> The "hard-working" kids went the other way: they picked harder challenges, actually enjoyed the struggle, bounced back after failing, and were far more honest about their scores. Let's run the simulation.</p>
                  </>
                )}
                <DweckExperimentSimulator />
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The Brain on Praise." eyebrow="Step 3" icon={Brain} theme={theme}>
              {essentials ? (
                <>
                  <p>Praise feels rewarding — but the two types attach that good feeling to different things. Person praise ties it to who you are, so failure feels personal. Process praise ties it to effort, something you can always repeat, so setbacks feel less threatening. That is why the same failure can crush one student and motivate another. Your brain also fires an error signal when you make mistakes. People with a <Highlight description="Believing intelligence is fixed." theme={theme}>Fixed Mindset</Highlight> tend to produce a smaller signal; people with a <Highlight description="Believing intelligence can grow." theme={theme}>Growth Mindset</Highlight> produce a larger one — and a larger signal is linked to learning more from the mistake.<Cite n={2} /></p>
                </>
              ) : (
                <>
                  <p>Why does one sentence make such a big difference? It comes down to what the praise attaches to. Praise feels good — but person praise attaches that feeling to <em>who you are</em>, so any failure can land like a personal attack and motivation crashes. Process praise attaches it to <em>the work you put in</em> — something you can always do again — so setbacks feel less threatening.</p>
                  <p>There's also a difference in how the brain responds to mistakes. Researchers tracked an error signal in the brain (sometimes called the "Pe wave") and found it was <em>larger</em> in people with a <Highlight description="Thinking your intelligence can grow with effort. If you believe this, failure is just information — a chance to figure out what went wrong and do better." theme={theme}>Growth Mindset</Highlight> than in those with a <Highlight description="Thinking your intelligence is set in stone. If you believe this, every failure feels like proof you're just not good enough." theme={theme}>Fixed Mindset</Highlight> — and a bigger signal went hand in hand with paying more attention to the error and doing better on the next try.<Cite n={2} /></p>
                </>
              )}
              <ErrorSignalVisualizer />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Real World Data." eyebrow="Step 4" icon={User} theme={theme}>
              {essentials ? (
                <>
                  <p>A long-term study found that toddlers who got more process praise developed stronger growth mindsets five years later.<Cite n={3} /> A follow-up found that this early praise predicted better Maths and reading results in fourth grade, with mindset as the link.<Cite n={4} /> The first study also found a gender gap. Boys got more process praise from a very young age. Girls got more person praise. This may be one reason some high-achieving girls develop fixed mindsets.</p>
                </>
              ) : (
                <>
                  <p>This isn't just something that works in a lab. A long-term study followed families from when their kids were toddlers all the way through primary school. It found that the amount of process praise parents used (on average, just 18% of all praise) predicted whether their child would develop a growth mindset five years later.<Cite n={3} /> A follow-up tracked the same children to fourth grade and found that early process praise predicted stronger Maths and reading achievement, with the child's mindset acting as the link between the two.<Cite n={4} /></p>
                  <p>The first study also found a big gender gap. From as young as 14 months, boys tended to get more process praise ("You built that tower so high!"), while girls were more likely to hear trait-based praise ("You're such a good girl"). This difference in how boys and girls are talked to from a very young age may be one reason high-achieving girls can sometimes be more likely to develop a fixed mindset later on.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The 'Effort' Trap." eyebrow="Step 5" icon={AlertTriangle} theme={theme}>
                {essentials ? (
                  <>
                    <p>Praising effort alone is not enough. Saying "you tried your best" after failure is <Highlight description="Praising effort without helping fix the problem. Sounds kind but feels discouraging." theme={theme}>Consolation Praise</Highlight>. It tells you there is nothing more you can do. Good process praise connects effort to what worked and what did not. Say "your method didn't click — let's try a different approach." Effort must be pointed in the right direction.</p>
                  </>
                ) : (
                  <>
                    <p>As these ideas got popular, people started getting them wrong. The biggest mistake is thinking that a growth mindset just means praising effort. Imagine you fail a test after studying hard, and someone says, "Don't worry, you tried your best!" This is <Highlight description="When someone praises your effort but doesn't help you figure out what went wrong. It sounds kind, but it basically says 'you gave it everything and it still wasn't enough' — which is actually pretty discouraging." theme={theme}>Consolation Praise</Highlight>, and it actually does more harm than good. It sends the message: "Your best isn't good enough, and there's nothing more you can do."</p>
                    <p>Good process praise connects effort to *what worked* and *what didn't*. A better response would be: "I can see you worked hard, but the study method you used didn't click. Let's look at your mistakes and try a different approach." Effort on its own isn't enough — it has to be pointed in the right direction.</p>
                  </>
                )}
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="The Feedback Audit." eyebrow="Step 6" icon={Settings} theme={theme}>
              {essentials ? (
                <p>Start noticing praise around you. For one day, sort every piece of feedback you hear. Is it Person Praise, Process Praise, or vague ("good job")? Pay special attention to how you talk to yourself.</p>
              ) : (
                <p>Now that you know the difference, start paying attention to the feedback around you — from teachers, family, and especially how you talk to yourself. The "Feedback Audit" is simple: for one day, just notice the praise you hear and sort it. Is it Person Praise, Process Praise, or just vague outcome stuff ("Good job")?</p>
              )}
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
