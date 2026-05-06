/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * QuestionPlayer — controls stage navigation for a single ExamQuestion.
 * Three stages: question → predict → debrief.
 * State (predictAnswers, predictSubmitted, current stage) lives here and
 * resets when the student returns to the question list.
 *
 * Forward gating: the top-bar forward arrow can advance from any stage
 * EXCEPT predict, where it requires the student to have submitted their
 * predictions. Stops accidental skip-aheads through the active-recall stage.
 *
 * Legacy detection: a dev-only console warning surfaces when a question
 * lacking the new-schema `debrief` / `biggestMistake` fields is loaded, so
 * the migration backlog stays visible. See /STRATEGISER_MIGRATION.md.
 */

import React, { useEffect, useMemo, useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { type ExamQuestion, type ExamStrategiserStage, type PredictAnswers } from '../../types/examStrategiser';
import StageProgress from './StageProgress';
import QuestionStage from './stages/QuestionStage';
import PredictStage from './stages/PredictStage';
import DebriefStage from './stages/DebriefStage';

interface Props {
  question: ExamQuestion;
  onBackToList: () => void;
}

const STAGES: ExamStrategiserStage[] = ['question', 'predict', 'debrief'];

const QuestionPlayer: React.FC<Props> = ({ question, onBackToList }) => {
  const [stageIdx, setStageIdx] = useState(0);
  const [answers, setAnswers] = useState<PredictAnswers>({});
  const [predictSubmitted, setPredictSubmitted] = useState(false);

  // Dev-only legacy-schema warning. Surfaces in the console when a question
  // hasn't been migrated to the per-prompt `debrief` + question-level
  // `biggestMistake` shape. Helps keep the migration backlog visible.
  useEffect(() => {
    if (!import.meta.env.DEV) return;
    const isLegacy = !question.biggestMistake
      || question.predictPrompts.some(p => !p.debrief);
    if (isLegacy) {
      console.warn(
        `[Strategiser] Legacy-format question loaded: "${question.id}". ` +
        `See /STRATEGISER_MIGRATION.md to track migration status.`,
      );
    }
  }, [question.id, question.biggestMistake, question.predictPrompts]);

  const stage = STAGES[stageIdx];

  const goBack = () => {
    if (stageIdx > 0) setStageIdx(i => i - 1);
    else onBackToList();
  };
  const goForward = () => {
    if (stageIdx < STAGES.length - 1) setStageIdx(i => i + 1);
    else onBackToList();
  };

  // Forward arrow gating — student-mode. The predict stage is the only
  // active-recall stage; advancing past it without engaging defeats the
  // pedagogy. Other stages are reveal-only, so forward is unconstrained.
  const canGoForward = stage !== 'predict' || predictSubmitted;

  return (
    <div>
      <button
        type="button"
        onClick={onBackToList}
        className="font-sans flex items-center gap-1.5 mb-5 transition-colors"
        style={{ fontSize: 12, color: '#78716C', background: 'transparent', border: 'none', padding: 0, cursor: 'pointer' }}
      >
        <svg width="12" height="12" viewBox="0 0 16 16" fill="none" aria-hidden>
          <path d="M10 3L5 8L10 13" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
        Back to questions
      </button>

      <StageProgress
        stages={STAGES}
        current={stage}
        onBack={goBack}
        onForward={goForward}
        canGoBack={stageIdx > 0}
        canGoForward={canGoForward}
        forwardLabel={stageIdx === STAGES.length - 1 ? 'Done' : 'Next'}
      />

      <AnimatePresence mode="wait">
        <MotionDiv
          key={stage}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -8 }}
          transition={{ duration: 0.22, ease: [0.22, 1, 0.36, 1] }}
        >
          {stage === 'question' && (
            <QuestionStage question={question} onPredictStart={() => setStageIdx(STAGES.indexOf('predict'))} />
          )}
          {stage === 'predict' && (
            <PredictStage
              question={question}
              answers={answers}
              submitted={predictSubmitted}
              onAnswer={(id, v) => setAnswers(prev => ({ ...prev, [id]: v }))}
              onMarkSubmitted={() => setPredictSubmitted(true)}
              onAdvance={() => setStageIdx(STAGES.indexOf('debrief'))}
            />
          )}
          {stage === 'debrief' && <DebriefStage question={question} answers={answers} />}
        </MotionDiv>
      </AnimatePresence>
    </div>
  );
};

export default QuestionPlayer;
