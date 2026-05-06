/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * QuickCheck — reusable end-of-module quiz. Mirrors the predict-stage
 * shape from the existing Strategiser: in-memory state, multiple-choice,
 * post-submission feedback with explanation per question.
 */

import React, { useState } from 'react';
import { type QuickCheckQuestion } from '../../../types/knowledge';

const TEAL = '#2A7D6F';

interface Props {
  questions: QuickCheckQuestion[];
  /** Optional heading override. Defaults to "Test yourself". */
  heading?: string;
}

const QuickCheck: React.FC<Props> = ({ questions, heading = 'Test yourself' }) => {
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState(false);

  const allAnswered = questions.every(q => answers[q.id] !== undefined);
  const correctCount = questions.filter(q => answers[q.id] === q.correctAnswer).length;

  return (
    <section
      className="rounded-2xl"
      style={{
        backgroundColor: '#FFFFFF',
        border: '1px solid #EDEBE8',
        padding: '24px 26px',
      }}
    >
      <header className="mb-5">
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 4 }}>
          Quick check
        </p>
        <h3 className="font-serif" style={{ fontSize: 18, fontWeight: 600, color: '#1A1A1A' }}>
          {heading}
        </h3>
      </header>

      <div className="space-y-4">
        {questions.map((q, idx) => (
          <QuestionCard
            key={q.id}
            question={q}
            index={idx}
            answer={answers[q.id]}
            submitted={submitted}
            onAnswer={(v) => setAnswers(prev => ({ ...prev, [q.id]: v }))}
          />
        ))}
      </div>

      <div className="mt-5 flex items-center justify-between">
        {submitted ? (
          <p className="font-sans" style={{ fontSize: 13, color: '#3F3B36', fontWeight: 500 }}>
            <span style={{ color: TEAL, fontWeight: 700 }}>{correctCount} / {questions.length}</span>
            {' correct'}
          </p>
        ) : (
          <p className="font-sans" style={{ fontSize: 12, color: '#A8A29E' }}>
            {Object.keys(answers).length} / {questions.length} answered
          </p>
        )}
        {!submitted && (
          <button
            type="button"
            onClick={() => setSubmitted(true)}
            disabled={!allAnswered}
            className="rounded-full transition-colors font-sans"
            style={{
              backgroundColor: allAnswered ? TEAL : '#F5F4F1',
              color: allAnswered ? '#FFFFFF' : '#C4C0BC',
              padding: '9px 20px',
              fontSize: 13,
              fontWeight: 600,
              border: 'none',
              cursor: allAnswered ? 'pointer' : 'not-allowed',
            }}
          >
            Check answers
          </button>
        )}
      </div>
    </section>
  );
};

const QuestionCard: React.FC<{
  question: QuickCheckQuestion;
  index: number;
  answer: string | undefined;
  submitted: boolean;
  onAnswer: (v: string) => void;
}> = ({ question, index, answer, submitted, onAnswer }) => {
  const isCorrect = submitted && answer === question.correctAnswer;
  const isWrong = submitted && answer !== undefined && answer !== question.correctAnswer;

  return (
    <div
      className="rounded-xl"
      style={{
        backgroundColor: '#FAF7F4',
        border: '1px solid #EDEBE8',
        padding: '14px 16px',
      }}
    >
      <div className="flex items-baseline gap-3 mb-3">
        <span className="font-sans" style={{ fontSize: 11, fontWeight: 700, color: '#C4C0BC' }}>
          {String(index + 1).padStart(2, '0')}
        </span>
        <p className="font-serif flex-1" style={{ fontSize: 14, fontWeight: 500, color: '#1A1A1A', lineHeight: 1.45 }}>
          {question.prompt}
        </p>
      </div>

      <div className="space-y-1.5">
        {question.options.map(opt => {
          const selected = answer === opt;
          const isCorrectOpt = submitted && opt === question.correctAnswer;
          const isWrongSelected = submitted && selected && opt !== question.correctAnswer;
          return (
            <button
              key={opt}
              type="button"
              onClick={() => !submitted && onAnswer(opt)}
              disabled={submitted}
              className="w-full text-left rounded-lg transition-colors font-sans"
              style={{
                padding: '9px 14px',
                fontSize: 13,
                fontWeight: 500,
                backgroundColor: isCorrectOpt
                  ? TEAL
                  : selected && !submitted
                  ? TEAL
                  : '#FFFFFF',
                color: isCorrectOpt || (selected && !submitted) ? '#FFFFFF' : '#1A1A1A',
                border: `1px solid ${
                  isCorrectOpt
                    ? TEAL
                    : isWrongSelected
                    ? '#C4C0BC'
                    : selected && !submitted
                    ? TEAL
                    : '#EDEBE8'
                }`,
                cursor: submitted ? 'default' : 'pointer',
                opacity: submitted && !isCorrectOpt && !isWrongSelected ? 0.5 : 1,
              }}
            >
              {opt}
              {isWrongSelected && (
                <span className="ml-2" style={{ fontSize: 11, color: '#A8A29E', fontWeight: 600 }}>
                  — your answer
                </span>
              )}
            </button>
          );
        })}
      </div>

      {submitted && (
        <p
          className="font-sans"
          style={{
            marginTop: 10,
            fontSize: 12.5,
            color: '#3F3B36',
            lineHeight: 1.55,
            paddingTop: 10,
            borderTop: '1px solid #EDEBE8',
          }}
        >
          <span style={{ color: isCorrect ? TEAL : '#78716C', fontWeight: 700, fontSize: 11, textTransform: 'uppercase', letterSpacing: 0.5 }}>
            {isCorrect ? 'Correct · ' : isWrong ? 'Examiner\'s answer · ' : 'Note · '}
          </span>
          {question.explanation}
        </p>
      )}
    </div>
  );
};

export default QuickCheck;
