/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { type ExamQuestion, type PredictAnswers, type PredictPrompt } from '../../../types/examStrategiser';
import CollapsibleQuestionCard from '../CollapsibleQuestionCard';

const TEAL = '#2A7D6F';

interface Props {
  question: ExamQuestion;
  answers: PredictAnswers;
  /** Lifted from QuestionPlayer so the top-bar forward arrow can gate on it. */
  submitted: boolean;
  onAnswer: (promptId: string, value: string | number) => void;
  /** Marks the predict stage as submitted (reveals correct answers + advance CTA). */
  onMarkSubmitted: () => void;
  /** Advances to the annotation stage. */
  onAdvance: () => void;
}

const PredictStage: React.FC<Props> = ({ question, answers, submitted, onAnswer, onMarkSubmitted, onAdvance }) => {
  const allAnswered = question.predictPrompts.every(p => answers[p.id] !== undefined && answers[p.id] !== '');

  return (
    <div className="space-y-6">
      <CollapsibleQuestionCard question={question} />

      <header>
        <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#A8A29E' }}>
          Stage 2 · Predict
        </p>
        <h2 className="font-serif" style={{ fontSize: 24, fontWeight: 600, color: '#1A1A1A', marginTop: 4 }}>
          Predict before the debrief.
        </h2>
        <p className="font-sans" style={{ fontSize: 13, color: '#78716C', marginTop: 4 }}>
          Predicting before you see the examiner's view makes the debrief stick. Don't worry about being right.
        </p>
      </header>

      <div className="space-y-4">
        {question.predictPrompts.map((prompt, idx) => (
          <PromptCard
            key={prompt.id}
            prompt={prompt}
            index={idx}
            answer={answers[prompt.id]}
            submitted={submitted}
            onAnswer={(v) => onAnswer(prompt.id, v)}
          />
        ))}
      </div>

      <div className="flex justify-end pt-2">
        {!submitted ? (
          <button
            type="button"
            onClick={onMarkSubmitted}
            disabled={!allAnswered}
            className="rounded-full transition-colors"
            style={{
              backgroundColor: allAnswered ? TEAL : '#F5F4F1',
              color: allAnswered ? '#FFFFFF' : '#C4C0BC',
              padding: '11px 24px',
              fontSize: 13,
              fontWeight: 600,
              border: 'none',
              cursor: allAnswered ? 'pointer' : 'not-allowed',
            }}
          >
            Submit predictions
          </button>
        ) : (
          <button
            type="button"
            onClick={onAdvance}
            className="rounded-full transition-colors"
            style={{
              backgroundColor: TEAL,
              color: '#FFFFFF',
              padding: '11px 24px',
              fontSize: 13,
              fontWeight: 600,
              border: 'none',
              cursor: 'pointer',
            }}
          >
            See examiner's notes
          </button>
        )}
      </div>
    </div>
  );
};

const PromptCard: React.FC<{
  prompt: PredictPrompt;
  index: number;
  answer: string | number | undefined;
  submitted: boolean;
  onAnswer: (v: string | number) => void;
}> = ({ prompt, index, answer, submitted, onAnswer }) => {
  const isCorrect = submitted && prompt.correctAnswer !== undefined &&
    String(answer).trim().toLowerCase() === String(prompt.correctAnswer).trim().toLowerCase();
  const isWrong = submitted && prompt.correctAnswer !== undefined && !isCorrect;

  return (
    <div
      className="rounded-xl"
      style={{
        backgroundColor: '#FFFFFF',
        border: '1px solid #EDEBE8',
        padding: '18px 20px',
      }}
    >
      <div className="flex items-baseline gap-3 mb-3">
        <span className="font-sans" style={{ fontSize: 11, fontWeight: 700, color: '#C4C0BC' }}>
          {String(index + 1).padStart(2, '0')}
        </span>
        <p className="font-serif flex-1" style={{ fontSize: 16, fontWeight: 500, color: '#1A1A1A', lineHeight: 1.4 }}>
          {prompt.prompt}
        </p>
      </div>

      {prompt.type === 'multiple-choice' && prompt.options && (
        <div className="grid grid-cols-2 gap-2">
          {prompt.options.map(opt => {
            const selected = answer === opt;
            return (
              <button
                key={opt}
                type="button"
                onClick={() => !submitted && onAnswer(opt)}
                disabled={submitted}
                className="rounded-lg transition-colors text-left"
                style={{
                  padding: '10px 14px',
                  fontSize: 13,
                  fontWeight: 500,
                  fontFamily: 'DM Sans, system-ui, sans-serif',
                  backgroundColor: selected ? TEAL : '#FFFFFF',
                  color: selected ? '#FFFFFF' : '#1A1A1A',
                  border: `1px solid ${selected ? TEAL : '#EDEBE8'}`,
                  cursor: submitted ? 'default' : 'pointer',
                  opacity: submitted && !selected ? 0.45 : 1,
                }}
              >
                {opt}
              </button>
            );
          })}
        </div>
      )}

      {prompt.type === 'short-text' && (
        <input
          type="text"
          value={answer === undefined ? '' : String(answer)}
          onChange={(e) => onAnswer(e.target.value)}
          disabled={submitted}
          placeholder="Type your answer…"
          maxLength={120}
          className="w-full rounded-lg"
          style={{
            padding: '10px 14px',
            fontSize: 14,
            fontFamily: 'DM Sans, system-ui, sans-serif',
            backgroundColor: '#FFFFFF',
            color: '#1A1A1A',
            border: '1px solid #EDEBE8',
            outline: 'none',
          }}
        />
      )}

      {prompt.type === 'number' && (
        <input
          type="number"
          value={answer === undefined ? '' : String(answer)}
          onChange={(e) => onAnswer(e.target.value === '' ? '' : Number(e.target.value))}
          disabled={submitted}
          placeholder="Type a number…"
          className="w-full rounded-lg"
          style={{
            padding: '10px 14px',
            fontSize: 14,
            fontFamily: 'DM Sans, system-ui, sans-serif',
            backgroundColor: '#FFFFFF',
            color: '#1A1A1A',
            border: '1px solid #EDEBE8',
            outline: 'none',
          }}
        />
      )}

      {prompt.hint && !submitted && (
        <p className="font-sans" style={{ fontSize: 11, color: '#A8A29E', marginTop: 6 }}>
          Hint · {prompt.hint}
        </p>
      )}

      {submitted && prompt.correctAnswer !== undefined && (
        <div className="font-sans" style={{ fontSize: 12, marginTop: 8, color: isCorrect ? TEAL : isWrong ? '#78716C' : '#78716C' }}>
          {isCorrect && <span style={{ fontWeight: 700 }}>Correct.</span>}
          {isWrong && (
            <>
              <span style={{ fontWeight: 700 }}>Examiner's answer: </span>
              <span>{String(prompt.correctAnswer)}</span>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default PredictStage;
