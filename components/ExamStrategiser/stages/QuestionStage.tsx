/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * QuestionStage — Stage 1. Renders the question full-width with a clear
 * "Predict before revealing" CTA. Question text is RAW here — no
 * annotations spoiling anything. Annotations are revealed in the Debrief
 * stage as part of the examiner's view.
 */

import React from 'react';
import { type ExamQuestion } from '../../../types/examStrategiser';
import AnnotatedText from '../AnnotatedText';

const TEAL = '#2A7D6F';

interface Props {
  question: ExamQuestion;
  onPredictStart: () => void;
}

const QuestionStage: React.FC<Props> = ({ question, onPredictStart }) => {
  return (
    <div className="space-y-6">
      <QuestionHeader question={question} />
      <article
        className="rounded-2xl"
        style={{
          backgroundColor: '#FFFFFF',
          border: '1px solid #EDEBE8',
          padding: '28px 32px',
        }}
      >
        <AnnotatedText parts={question.questionText} mode="raw" />
      </article>
      <div className="flex flex-col items-center gap-2 pt-2">
        <button
          type="button"
          onClick={onPredictStart}
          className="rounded-full transition-colors"
          style={{
            backgroundColor: TEAL,
            color: '#FFFFFF',
            padding: '12px 28px',
            fontSize: 14,
            fontWeight: 600,
            border: 'none',
            cursor: 'pointer',
          }}
        >
          Predict before revealing
        </button>
        <p className="font-sans" style={{ fontSize: 12, color: '#A8A29E' }}>
          A few quick prompts about the question itself — then the debrief.
        </p>
      </div>
    </div>
  );
};

const QuestionHeader: React.FC<{ question: ExamQuestion }> = ({ question }) => (
  <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
    <span className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#A8A29E' }}>
      {question.year} · {question.paper ?? 'Paper'}
      {question.section ? ` · ${question.section}` : ''}
      {question.level ? ` · ${question.level}` : ''}
    </span>
    <span className="font-serif" style={{ fontSize: 22, fontWeight: 600, color: '#1A1A1A' }}>
      Question {question.questionNumber}
    </span>
    <span className="font-sans" style={{ fontSize: 12, color: '#78716C' }}>
      ({question.marks} marks)
    </span>
  </div>
);

export default QuestionStage;
