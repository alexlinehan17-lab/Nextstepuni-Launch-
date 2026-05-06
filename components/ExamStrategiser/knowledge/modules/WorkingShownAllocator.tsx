/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Working-Shown Allocator (Stage 2, E9).
 *
 * The mark provenance trail. The student walks through a worked Maths/
 * Science/Accounting answer step by step. Each revealed step adds a
 * marks-earned ribbon (and any penalty: slip −1, blunder −3, misread
 * −1). The trail visualises mark provenance — students see marks being
 * earned and lost in real time.
 *
 * Five answer paths can be loaded from the rewind picker:
 *   a. Blank — 0 marks
 *   b. Formula only — typically 3 / 10 (the attempt mark)
 *   c. Formula + substitution — 5 / 10
 *   d. Full working with one blunder — 7 / 10
 *   e. Full working, correct — 10 / 10
 *
 * "What if I had stopped here" button at every step shows the score-to-
 * date alongside the score-if-completed, making the cost of giving up
 * (and the cost of pushing past mistakes) visible.
 *
 * Library: 5 questions across Maths algebra, Maths geometry, Chemistry
 * mole calc, Physics mechanics, Accounting depreciation.
 *
 * Source: dossier § A2 (penalty grammar), § B4 (Sciences key phrases),
 * § B7 (Accounting calculator trap).
 *
 * Aesthetic: Stage 2 bold register — 2px #1a1a1a borders, ribbon-style
 * mark accruals, framer-motion ribbon entries.
 */

import React, { useMemo, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { WORKED_QUESTIONS } from '../../../../data/knowledge/workedQuestions';
import {
  type WorkingQuestion,
  type WorkingStep,
  type WorkingAnswerPath,
} from '../../../../types/knowledge';

const TEAL = '#2A7D6F';
const TEAL_DARK = '#1a5a4e';
const INK = '#1a1a1a';
const CREAM = '#FDF8F0';
const WARN = '#A8746E';

interface Props {
  onBack: () => void;
}

const WorkingShownAllocator: React.FC<Props> = ({ onBack }) => {
  const [questionId, setQuestionId] = useState<string>(WORKED_QUESTIONS[0].id);
  const question = useMemo(() => WORKED_QUESTIONS.find(q => q.id === questionId)!, [questionId]);

  const [pathId, setPathId] = useState<WorkingAnswerPath['id']>('blank');
  const path = useMemo(() => question.paths.find(p => p.id === pathId)!, [question, pathId]);

  const visibleSteps = useMemo(
    () => path.includedStepIds.map(id => question.steps.find(s => s.id === id)!).filter(Boolean),
    [path, question.steps],
  );

  const [whatIfStepIdx, setWhatIfStepIdx] = useState<number | null>(null);

  const switchQuestion = (id: string) => {
    setQuestionId(id);
    setPathId('blank');
    setWhatIfStepIdx(null);
  };

  const switchPath = (id: WorkingAnswerPath['id']) => {
    setPathId(id);
    setWhatIfStepIdx(null);
  };

  return (
    <div className="space-y-6" style={{ color: INK }}>
      <BackBar onBack={onBack} />
      <Hero />

      <QuestionStrip
        questions={WORKED_QUESTIONS}
        activeId={question.id}
        onChange={switchQuestion}
      />

      <QuestionHeader question={question} />

      <PathPicker
        paths={question.paths}
        activeId={pathId}
        onChange={switchPath}
      />

      <Scaffold
        question={question}
        steps={visibleSteps}
        path={path}
        whatIfStepIdx={whatIfStepIdx}
        onWhatIfHover={setWhatIfStepIdx}
      />

      <PathInsight path={path} question={question} whatIfStepIdx={whatIfStepIdx} steps={visibleSteps} />
    </div>
  );
};

// ─── Layout chrome ─────────────────────────────────────────────────────

const BackBar: React.FC<{ onBack: () => void }> = ({ onBack }) => (
  <button
    type="button"
    onClick={onBack}
    className="font-sans flex items-center gap-1.5"
    style={{ fontSize: 12, color: '#78716C', background: 'transparent', border: 'none', padding: 0, cursor: 'pointer' }}
  >
    <svg width="12" height="12" viewBox="0 0 16 16" fill="none" aria-hidden>
      <path d="M10 3L5 8L10 13" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
    Necessary Knowledge
  </button>
);

const Hero: React.FC = () => (
  <header>
    <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#9e9186' }}>
      Necessary Knowledge · Stage 2
    </p>
    <h1 className="font-serif" style={{ fontSize: 30, fontWeight: 600, color: INK, marginTop: 4, lineHeight: 1.15 }}>
      Working-Shown Allocator — see marks accrue.
    </h1>
    <p className="font-sans max-w-2xl" style={{ fontSize: 14.5, color: '#5a5550', marginTop: 8, lineHeight: 1.55 }}>
      Build the answer step by step. Marks land as ribbons next to each step. Slips and blunders are deducted in real time.
      Five answer paths show what each level of "showing your work" actually scores in the marking scheme.
    </p>
  </header>
);

// ─── Question strip ────────────────────────────────────────────────────

const QuestionStrip: React.FC<{
  questions: WorkingQuestion[];
  activeId: string;
  onChange: (id: string) => void;
}> = ({ questions, activeId, onChange }) => (
  <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
    {questions.map(q => {
      const active = q.id === activeId;
      return (
        <button
          key={q.id}
          type="button"
          onClick={() => onChange(q.id)}
          className="font-sans text-left rounded-xl"
          style={{
            backgroundColor: active ? INK : '#FFFFFF',
            color: active ? '#FFFFFF' : INK,
            border: `2px solid ${INK}`,
            padding: '10px 12px',
            cursor: 'pointer',
          }}
        >
          <p style={{ fontSize: 9.5, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, opacity: 0.7 }}>
            {q.subject}
          </p>
          <p style={{ fontSize: 12, fontWeight: 600, lineHeight: 1.3, marginTop: 2 }}>
            {q.topicLabel}
          </p>
        </button>
      );
    })}
  </div>
);

// ─── Question header ───────────────────────────────────────────────────

const QuestionHeader: React.FC<{ question: WorkingQuestion }> = ({ question }) => (
  <section
    className="rounded-2xl"
    style={{
      backgroundColor: '#FFFFFF',
      border: `2px solid ${INK}`,
      padding: '20px 24px',
    }}
  >
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 6 }}>
      Question
    </p>
    <p className="font-serif" style={{ fontSize: 16, fontWeight: 500, color: INK, lineHeight: 1.5, fontStyle: 'italic' }}>
      &ldquo;{question.questionPrompt}&rdquo;
    </p>
    <div className="flex items-center gap-4 mt-3 flex-wrap">
      <Pill label="Total marks" value={`${question.marksAvailable}`} />
      {question.scaleLabel && <Pill label="Scale" value={question.scaleLabel} />}
    </div>
  </section>
);

const Pill: React.FC<{ label: string; value: string }> = ({ label, value }) => (
  <div>
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#9e9186' }}>
      {label}
    </p>
    <p className="font-serif" style={{ fontSize: 14, fontWeight: 700, color: INK }}>
      {value}
    </p>
  </div>
);

// ─── Path picker ───────────────────────────────────────────────────────

const PATH_PALETTE: Record<WorkingAnswerPath['id'], { tint: string; ink: string }> = {
  'blank':           { tint: '#F5F4F1', ink: '#9e9186' },
  'formula-only':    { tint: `${TEAL}15`, ink: TEAL_DARK },
  'formula-sub':     { tint: `${TEAL}28`, ink: TEAL_DARK },
  'full-with-slip':  { tint: `${WARN}26`, ink: WARN },
  'full-correct':    { tint: `${TEAL}45`, ink: TEAL_DARK },
};

const PathPicker: React.FC<{
  paths: WorkingAnswerPath[];
  activeId: WorkingAnswerPath['id'];
  onChange: (id: WorkingAnswerPath['id']) => void;
}> = ({ paths, activeId, onChange }) => (
  <section
    className="rounded-2xl"
    style={{
      backgroundColor: '#FFFFFF',
      border: `2px solid ${INK}`,
      padding: '18px 22px',
    }}
  >
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 10 }}>
      Rewind to a path
    </p>
    <div className="grid sm:grid-cols-5 gap-2">
      {paths.map(p => {
        const palette = PATH_PALETTE[p.id];
        const active = p.id === activeId;
        const pct = p.finalScore === 0 ? 0 : Math.round(p.finalScore * 10);
        return (
          <button
            key={p.id}
            type="button"
            onClick={() => onChange(p.id)}
            className="rounded-xl text-left transition-colors"
            style={{
              backgroundColor: active ? INK : palette.tint,
              color: active ? '#FFFFFF' : INK,
              border: `2px solid ${active ? INK : palette.ink}`,
              padding: '12px 14px',
              cursor: 'pointer',
            }}
          >
            <p className="font-sans" style={{ fontSize: 10.5, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, opacity: 0.85 }}>
              {p.label}
            </p>
            <p className="font-serif" style={{ fontSize: 22, fontWeight: 700, marginTop: 4 }}>
              {p.finalScore}<span style={{ fontSize: 13, opacity: 0.7, fontWeight: 500 }}> / 10</span>
            </p>
            <p className="font-sans" style={{ fontSize: 10.5, marginTop: 1, opacity: 0.85 }}>
              {pct}%
            </p>
          </button>
        );
      })}
    </div>
  </section>
);

// ─── Scaffold ──────────────────────────────────────────────────────────

const Scaffold: React.FC<{
  question: WorkingQuestion;
  steps: WorkingStep[];
  path: WorkingAnswerPath;
  whatIfStepIdx: number | null;
  onWhatIfHover: (idx: number | null) => void;
}> = ({ question, steps, path, whatIfStepIdx, onWhatIfHover }) => {
  // Running marks per step
  const runningMarks = useMemo(() => {
    let total = 0;
    return steps.map((s, i) => {
      total += s.marksEarned;
      if (s.penalty) total += s.penalty.amount; // amount is negative
      return { stepIdx: i, total: Math.max(0, total) };
    });
  }, [steps]);

  return (
    <section
      className="rounded-2xl"
      style={{
        backgroundColor: '#FFFFFF',
        border: `2px solid ${INK}`,
        padding: '24px 26px',
      }}
    >
      <div className="flex items-baseline justify-between gap-3 mb-4 flex-wrap">
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL }}>
          Answer scaffold · {path.label}
        </p>
        <ScoreReadout finalScore={path.finalScore} marksAvailable={question.marksAvailable} />
      </div>

      {steps.length === 0 ? (
        <BlankAnswerHint marksAvailable={question.marksAvailable} />
      ) : (
        <div className="space-y-3">
          <AnimatePresence>
            {steps.map((step, idx) => (
              <ScaffoldRow
                key={`${path.id}-${step.id}`}
                step={step}
                idx={idx}
                isLast={idx === steps.length - 1}
                runningMarksAfter={runningMarks[idx]?.total ?? 0}
                marksAvailable={question.marksAvailable}
                whatIfActive={whatIfStepIdx === idx}
                onWhatIfHover={onWhatIfHover}
              />
            ))}
          </AnimatePresence>
        </div>
      )}
    </section>
  );
};

const ScoreReadout: React.FC<{ finalScore: number; marksAvailable: number }> = ({ finalScore, marksAvailable }) => (
  <div className="font-serif text-right">
    <span style={{ fontSize: 28, fontWeight: 700, color: INK }}>{finalScore}</span>
    <span style={{ fontSize: 13, color: '#9e9186', fontWeight: 500 }}> / {marksAvailable}</span>
  </div>
);

const BlankAnswerHint: React.FC<{ marksAvailable: number }> = ({ marksAvailable }) => (
  <div
    className="rounded-xl"
    style={{
      backgroundColor: CREAM,
      border: `1.5px dashed ${INK}`,
      padding: '32px 24px',
      textAlign: 'center',
    }}
  >
    <p className="font-serif" style={{ fontSize: 18, fontWeight: 600, color: INK }}>
      The page is blank.
    </p>
    <p className="font-sans" style={{ fontSize: 13, color: '#5a5550', marginTop: 6, lineHeight: 1.55, maxWidth: 400, margin: '6px auto 0' }}>
      Even a known correct answer scores 0 with no working shown. From the 2015 Maths Chief Examiner Report:
      "if you write nothing the examiner cannot award any marks."
    </p>
    <p className="font-sans" style={{ fontSize: 11.5, color: '#9e9186', marginTop: 14 }}>
      Pick a path above to see how marks accrue. {marksAvailable} marks are at stake.
    </p>
  </div>
);

const ScaffoldRow: React.FC<{
  step: WorkingStep;
  idx: number;
  isLast: boolean;
  runningMarksAfter: number;
  marksAvailable: number;
  whatIfActive: boolean;
  onWhatIfHover: (idx: number | null) => void;
}> = ({ step, idx, isLast, runningMarksAfter, marksAvailable, whatIfActive, onWhatIfHover }) => {
  const hasPenalty = !!step.penalty;
  const netDelta = step.marksEarned + (step.penalty?.amount ?? 0);
  const stepNum = idx + 1;

  return (
    <motion.div
      layout
      initial={{ opacity: 0, x: -8 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.35, ease: 'easeOut', delay: idx * 0.08 }}
      className="rounded-xl relative"
      style={{
        backgroundColor: hasPenalty ? `${WARN}10` : `${TEAL}08`,
        border: `1.5px solid ${hasPenalty ? WARN : INK}`,
        padding: '14px 16px 14px 18px',
        display: 'grid',
        gridTemplateColumns: '36px 1fr auto',
        gap: 14,
      }}
    >
      {/* Step number */}
      <div>
        <span
          className="font-serif inline-flex items-center justify-center"
          style={{
            backgroundColor: INK,
            color: '#FFFFFF',
            borderRadius: 999,
            width: 28,
            height: 28,
            fontSize: 13,
            fontWeight: 700,
          }}
        >
          {stepNum}
        </span>
      </div>

      {/* Step content */}
      <div>
        <p className="font-serif" style={{ fontSize: 14, fontWeight: 600, color: INK, marginBottom: 6, lineHeight: 1.35 }}>
          {step.label}
        </p>
        <div
          className="rounded-md font-mono"
          style={{
            backgroundColor: '#FFFFFF',
            border: '1px solid #d0cdc8',
            padding: '8px 12px',
            fontSize: 13,
            color: INK,
            lineHeight: 1.65,
            whiteSpace: 'pre-wrap',
          }}
        >
          {step.contentLines.map((line, i) => (
            <div key={i}>{line}</div>
          ))}
        </div>
        <p className="font-sans" style={{ fontSize: 11.5, color: '#5a5550', marginTop: 8, lineHeight: 1.55 }}>
          {step.annotation}
        </p>

        {/* What-if button */}
        {!isLast && (
          <button
            type="button"
            onMouseEnter={() => onWhatIfHover(idx)}
            onMouseLeave={() => onWhatIfHover(null)}
            onFocus={() => onWhatIfHover(idx)}
            onBlur={() => onWhatIfHover(null)}
            className="font-sans inline-flex items-center gap-1 mt-3"
            style={{
              fontSize: 11,
              color: whatIfActive ? TEAL_DARK : '#78716C',
              backgroundColor: whatIfActive ? `${TEAL}15` : 'transparent',
              border: `1px dashed ${whatIfActive ? TEAL_DARK : '#d0cdc8'}`,
              padding: '4px 10px',
              borderRadius: 999,
              cursor: 'help',
            }}
          >
            <svg width="11" height="11" viewBox="0 0 12 12" fill="none" aria-hidden>
              <circle cx="6" cy="6" r="5" stroke="currentColor" strokeWidth="1.4" />
              <path d="M6 5.5V8.5M6 3.5V4" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
            </svg>
            What if I had stopped here?
          </button>
        )}

        {whatIfActive && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="font-sans"
            style={{ fontSize: 11.5, color: TEAL_DARK, marginTop: 6, lineHeight: 1.55 }}
          >
            Stopping after step {stepNum}: <strong>{runningMarksAfter} / {marksAvailable}</strong> ({Math.round((runningMarksAfter / marksAvailable) * 100)}%).
            Continuing earns more — but every step has its own risk profile.
          </motion.p>
        )}
      </div>

      {/* Mark ribbons */}
      <div className="flex flex-col items-end gap-1.5">
        <Ribbon kind="earned" amount={step.marksEarned} />
        {step.penalty && (
          <Ribbon kind={step.penalty.kind} amount={step.penalty.amount} reason={step.penalty.reason} />
        )}
        <div
          className="font-serif"
          style={{
            fontSize: 11,
            fontWeight: 700,
            color: netDelta < 0 ? WARN : netDelta === 0 ? '#9e9186' : TEAL_DARK,
            marginTop: 2,
            whiteSpace: 'nowrap',
          }}
        >
          {netDelta > 0 ? `+${netDelta}` : netDelta} net
        </div>
        <div className="font-sans" style={{ fontSize: 10, color: '#9e9186', marginTop: 4 }}>
          Running: {runningMarksAfter}
        </div>
      </div>
    </motion.div>
  );
};

const Ribbon: React.FC<{
  kind: 'earned' | 'slip' | 'blunder' | 'misread';
  amount: number;
  reason?: string;
}> = ({ kind, amount, reason }) => {
  const isPositive = kind === 'earned';
  const label =
    kind === 'earned' ? `+${amount}` :
    kind === 'slip' ? `${amount} slip` :
    kind === 'blunder' ? `${amount} blunder` :
    `${amount} misread`;
  const bg = isPositive ? TEAL : WARN;
  return (
    <motion.div
      layout
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ type: 'spring', stiffness: 380, damping: 22 }}
      title={reason}
      className="font-sans"
      style={{
        backgroundColor: bg,
        color: '#FFFFFF',
        border: `1.5px solid ${isPositive ? TEAL_DARK : '#7A4944'}`,
        borderRadius: 6,
        padding: '4px 10px',
        fontSize: 11,
        fontWeight: 700,
        whiteSpace: 'nowrap',
        boxShadow: isPositive ? '2px 2px 0 0 #1a5a4e' : '2px 2px 0 0 #7A4944',
      }}
    >
      {label}
    </motion.div>
  );
};

// ─── Path insight ──────────────────────────────────────────────────────

const PathInsight: React.FC<{
  path: WorkingAnswerPath;
  question: WorkingQuestion;
  whatIfStepIdx: number | null;
  steps: WorkingStep[];
}> = ({ path, question, whatIfStepIdx }) => {
  const lostToBest = question.marksAvailable - path.finalScore;
  const allPathScores = question.paths.map(p => p.finalScore);
  const minScore = Math.min(...allPathScores);
  const maxScore = Math.max(...allPathScores);

  return (
    <section
      className="rounded-2xl"
      style={{
        backgroundColor: INK,
        color: '#FFFFFF',
        padding: '24px 28px',
      }}
    >
      <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#FFD8A8', opacity: 0.85, marginBottom: 8 }}>
        Path characterisation
      </p>
      <h4 className="font-serif" style={{ fontSize: 18, fontWeight: 600, lineHeight: 1.4 }}>
        {path.characterisation}
      </h4>

      {/* Path-vs-path comparison sparkline */}
      <div className="mt-5">
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#FFD8A8', opacity: 0.75, marginBottom: 8 }}>
          All five paths · {minScore} → {maxScore} marks
        </p>
        <SparklineBars
          paths={question.paths}
          activeId={path.id}
          marksAvailable={question.marksAvailable}
        />
      </div>

      <p className="font-sans" style={{ fontSize: 12.5, color: '#E8E4DE', marginTop: 16, lineHeight: 1.6 }}>
        {path.id === 'blank' && 'A panic-blank costs every available mark. Recognising the formula alone earns 30%.'}
        {path.id === 'formula-only' && 'The formula alone is worth a third of the available marks. Most students who run out of time and scribble the formula on the way out earn more than they expect.'}
        {path.id === 'formula-sub' && 'Five marks for half the work. The student understood the structure. The next step — the actual computation — is where confidence usually breaks.'}
        {path.id === 'full-with-slip' && `Three marks lost to a single mistake. ${lostToBest} marks separates this from full marks — the slip vs full-correct gap is the highest-leverage 30 seconds in any Maths/Science paper. The sanity check would have caught it.`}
        {path.id === 'full-correct' && 'Full marks. Working visible at every step, units present, sanity check applied. The marker has no reason to deduct.'}
      </p>
    </section>
  );
};

const SparklineBars: React.FC<{
  paths: WorkingAnswerPath[];
  activeId: WorkingAnswerPath['id'];
  marksAvailable: number;
}> = ({ paths, activeId, marksAvailable }) => (
  <div className="flex items-end gap-1.5" style={{ height: 90 }}>
    {paths.map(p => {
      const heightPct = (p.finalScore / marksAvailable) * 100;
      const isActive = p.id === activeId;
      return (
        <div key={p.id} className="flex-1 flex flex-col items-center gap-1.5">
          <div
            style={{
              width: '100%',
              height: '100%',
              display: 'flex',
              alignItems: 'flex-end',
            }}
          >
            <motion.div
              animate={{ height: `${Math.max(heightPct, 4)}%` }}
              transition={{ duration: 0.45, ease: 'easeOut' }}
              style={{
                width: '100%',
                backgroundColor: isActive ? '#FFFFFF' : '#5a5550',
                borderRadius: 3,
                minHeight: 2,
              }}
            />
          </div>
          <span className="font-sans" style={{ fontSize: 10, color: isActive ? '#FFFFFF' : '#9e9186', fontWeight: isActive ? 700 : 500, textAlign: 'center', lineHeight: 1.2 }}>
            {p.finalScore}/{marksAvailable}
          </span>
        </div>
      );
    })}
  </div>
);

export default WorkingShownAllocator;
