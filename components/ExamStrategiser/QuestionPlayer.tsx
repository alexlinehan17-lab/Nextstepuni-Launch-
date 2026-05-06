/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * QuestionPlayer — controls stage navigation for a single ExamQuestion.
 * State (predictAnswers, predictSubmitted, current stage) lives here and
 * resets when the student returns to the question list.
 *
 * Student-mode forward gating: the top-bar forward arrow can advance from
 * any stage EXCEPT predict, where it requires the student to have submitted
 * their predictions. This stops accidental skip-aheads through the active-
 * recall stage.
 */

import React, { useMemo, useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { type ExamQuestion, type ExamStrategiserStage, type PredictAnswers } from '../../types/examStrategiser';
import StageProgress from './StageProgress';
import RawQuestionStage from './stages/RawQuestionStage';
import PredictStage from './stages/PredictStage';
import AnnotationStage from './stages/AnnotationStage';
import InsightsStage from './stages/InsightsStage';
import MarkSchemeStage from './stages/MarkSchemeStage';

interface Props {
  question: ExamQuestion;
  onBackToList: () => void;
}

const QuestionPlayer: React.FC<Props> = ({ question, onBackToList }) => {
  const stages: ExamStrategiserStage[] = useMemo(() => {
    const base: ExamStrategiserStage[] = ['raw', 'predict', 'annotation', 'insights'];
    if (question.markScheme) base.push('mark-scheme');
    return base;
  }, [question.markScheme]);

  const [stageIdx, setStageIdx] = useState(0);
  const [answers, setAnswers] = useState<PredictAnswers>({});
  const [predictSubmitted, setPredictSubmitted] = useState(false);

  const stage = stages[stageIdx];

  const goBack = () => {
    if (stageIdx > 0) setStageIdx(i => i - 1);
    else onBackToList();
  };
  const goForward = () => {
    if (stageIdx < stages.length - 1) setStageIdx(i => i + 1);
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
        stages={stages}
        current={stage}
        onBack={goBack}
        onForward={goForward}
        canGoBack={stageIdx > 0}
        canGoForward={canGoForward}
        forwardLabel={stageIdx === stages.length - 1 ? 'Done' : 'Next'}
      />

      <AnimatePresence mode="wait">
        <MotionDiv
          key={stage}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -8 }}
          transition={{ duration: 0.22, ease: [0.22, 1, 0.36, 1] }}
        >
          {stage === 'raw' && (
            <RawQuestionStage question={question} onPredictStart={() => setStageIdx(stages.indexOf('predict'))} />
          )}
          {stage === 'predict' && (
            <PredictStage
              question={question}
              answers={answers}
              submitted={predictSubmitted}
              onAnswer={(id, v) => setAnswers(prev => ({ ...prev, [id]: v }))}
              onMarkSubmitted={() => setPredictSubmitted(true)}
              onAdvance={() => setStageIdx(stages.indexOf('annotation'))}
            />
          )}
          {stage === 'annotation' && <AnnotationStage question={question} />}
          {stage === 'insights' && <InsightsStage question={question} />}
          {stage === 'mark-scheme' && <MarkSchemeStage question={question} />}
        </MotionDiv>
      </AnimatePresence>
    </div>
  );
};

export default QuestionPlayer;
