/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * DebriefStage — Stage 3. Replaces the old Annotation + Insights stages.
 *
 * For each predict prompt:
 *   - Student's answer (highlighted) vs the correct answer
 *   - The strategic principle being tested (one short line)
 *   - Common wrong answer + why students pick it (sourced where possible)
 *
 * Followed by ONE closing card: "The biggest mistake on this question type"
 * — drawn from chief examiner reports.
 *
 * Legacy fallback: when a question hasn't been migrated yet (no per-prompt
 * `debrief`, no `biggestMistake`), we render the old two-panel
 * "What a top answer includes" / "Common traps" view sourced from the
 * deprecated `topAnswerIncludes` / `commonTraps` fields. Migration status is
 * tracked in /STRATEGISER_MIGRATION.md.
 */

import React from 'react';
import {
  type ExamQuestion,
  type ExaminerSource,
  type PredictAnswers,
  type PredictPrompt,
  type PromptDebrief,
  type TrapPattern,
} from '../../../types/examStrategiser';
import CollapsibleQuestionCard from '../CollapsibleQuestionCard';
import { TRAP_PATTERNS } from '../../../data/examStrategy';

const TEAL = '#2A7D6F';

interface Props {
  question: ExamQuestion;
  /** Predict answers the student gave — used to render their attempt
   *  alongside the correct answer in the per-prompt debrief. */
  answers: PredictAnswers;
  /** Optional reverse-nav: when provided, the Related Trap Patterns card
   *  is rendered as a clickable affordance into the Trap Patterns view. */
  onOpenTrapPatterns?: () => void;
}

const DebriefStage: React.FC<Props> = ({ question, answers, onOpenTrapPatterns }) => {
  const relatedPatterns = TRAP_PATTERNS.filter(
    p => p.examples.some(e => e.questionId === question.id),
  );

  return (
    <div className="space-y-6">
      <CollapsibleQuestionCard question={question} showAnnotations />

      <header>
        <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#A8A29E' }}>
          Stage 3 · Debrief
        </p>
        <h2 className="font-serif" style={{ fontSize: 24, fontWeight: 600, color: '#1A1A1A', marginTop: 4 }}>
          What you predicted, what the examiner sees.
        </h2>
      </header>

      <div className="space-y-3">
        {question.predictPrompts.map((prompt, idx) => (
          <PromptDebriefCard
            key={prompt.id}
            prompt={prompt}
            index={idx}
            studentAnswer={answers[prompt.id]}
          />
        ))}
      </div>

      {question.biggestMistake && (
        <BiggestMistakeCard mistake={question.biggestMistake} />
      )}

      {relatedPatterns.length > 0 && onOpenTrapPatterns && (
        <RelatedPatternsCard patterns={relatedPatterns} onOpen={onOpenTrapPatterns} />
      )}
    </div>
  );
};

const PromptDebriefCard: React.FC<{
  prompt: PredictPrompt;
  index: number;
  studentAnswer: string | number | undefined;
}> = ({ prompt, index, studentAnswer }) => {
  const debrief: PromptDebrief | undefined = prompt.debrief;
  const correct = prompt.correctAnswer;
  const isCorrect =
    correct !== undefined &&
    studentAnswer !== undefined &&
    String(studentAnswer).trim().toLowerCase() === String(correct).trim().toLowerCase();

  return (
    <article
      className="rounded-2xl"
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
        <p className="font-serif flex-1" style={{ fontSize: 15, fontWeight: 500, color: '#1A1A1A', lineHeight: 1.4 }}>
          {prompt.prompt}
        </p>
      </div>

      <div className="grid sm:grid-cols-2 gap-2.5">
        <AnswerBox label="You said" value={studentAnswer} kind={isCorrect ? 'correct' : 'student'} />
        <AnswerBox label="Examiner's answer" value={correct} kind="correct" />
      </div>

      {debrief && (
        <>
          <Block label="Strategic principle">
            <p className="font-sans" style={{ fontSize: 13, color: '#3F3B36', lineHeight: 1.55 }}>
              {debrief.strategicPrinciple}
            </p>
          </Block>

          <Block label="Common wrong answer">
            <p className="font-sans" style={{ fontSize: 13, color: '#3F3B36', lineHeight: 1.55 }}>
              <span style={{ fontWeight: 600 }}>"{debrief.commonWrongAnswer.answer}"</span>
              <span style={{ color: '#78716C' }}> — {debrief.commonWrongAnswer.reason}</span>
              {debrief.commonWrongAnswer.source && (
                <SourceCitation source={debrief.commonWrongAnswer.source} />
              )}
            </p>
          </Block>
        </>
      )}
    </article>
  );
};

const AnswerBox: React.FC<{
  label: string;
  value: string | number | undefined;
  kind: 'student' | 'correct';
}> = ({ label, value, kind }) => {
  const isCorrect = kind === 'correct';
  return (
    <div
      className="rounded-lg"
      style={{
        backgroundColor: isCorrect ? '#F0FAF8' : '#FFFFFF',
        border: `1px solid ${isCorrect ? `${TEAL}33` : '#EDEBE8'}`,
        padding: '10px 14px',
      }}
    >
      <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: isCorrect ? TEAL : '#A8A29E', marginBottom: 4 }}>
        {label}
      </p>
      <p className="font-sans" style={{ fontSize: 13, color: '#1A1A1A', lineHeight: 1.45, fontWeight: isCorrect ? 600 : 500 }}>
        {value === undefined || value === '' ? <em style={{ color: '#A8A29E', fontWeight: 400 }}>No answer</em> : String(value)}
      </p>
    </div>
  );
};

const Block: React.FC<{ label: string; children: React.ReactNode }> = ({ label, children }) => (
  <div className="mt-4">
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: TEAL, marginBottom: 5 }}>
      {label}
    </p>
    {children}
  </div>
);

const SourceCitation: React.FC<{ source: ExaminerSource }> = ({ source }) => {
  const label =
    source.type === 'chief-examiner'
      ? `Chief Examiner ${source.year}`
      : source.type === 'marking-scheme'
      ? `Marking scheme ${source.year}`
      : `Sample paper ${source.year}`;
  return (
    <span className="font-sans" style={{ fontSize: 11, color: '#A8A29E', marginLeft: 6, fontStyle: 'italic' }}>
      ({label}{source.pageRef ? `, ${source.pageRef}` : ''})
    </span>
  );
};

const BiggestMistakeCard: React.FC<{ mistake: NonNullable<ExamQuestion['biggestMistake']> }> = ({ mistake }) => (
  <article
    className="rounded-2xl"
    style={{
      backgroundColor: '#F0FAF8',
      border: `1px solid ${TEAL}33`,
      padding: '20px 22px',
    }}
  >
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 6 }}>
      The biggest mistake on this question type
    </p>
    <h3 className="font-serif" style={{ fontSize: 17, fontWeight: 600, color: '#1A1A1A', marginBottom: 8, lineHeight: 1.35 }}>
      {mistake.title}
    </h3>
    <p className="font-sans" style={{ fontSize: 13.5, color: '#3F3B36', lineHeight: 1.6 }}>
      {mistake.body}
      {mistake.source && <SourceCitation source={mistake.source} />}
    </p>
  </article>
);

// ── Related trap patterns ─────────────────────────────────────────────

const RelatedPatternsCard: React.FC<{ patterns: TrapPattern[]; onOpen: () => void }> = ({ patterns, onOpen }) => (
  <section
    className="rounded-2xl"
    style={{
      backgroundColor: '#F0FAF8',
      border: `1px solid ${TEAL}33`,
      padding: '18px 20px',
    }}
  >
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 6 }}>
      Recognised in {patterns.length} trap pattern{patterns.length === 1 ? '' : 's'}
    </p>
    <p className="font-sans" style={{ fontSize: 12.5, color: '#5a5550', lineHeight: 1.55, marginBottom: 12 }}>
      This question is one example of a recurring trap shape. Studying the pattern across multiple questions builds the recognition habit.
    </p>
    <ul className="space-y-1.5">
      {patterns.map(p => (
        <li key={p.id} className="font-sans" style={{ fontSize: 13, color: '#1A1A1A' }}>
          <span style={{ color: TEAL, marginRight: 6 }}>·</span>
          <span style={{ fontWeight: 600 }}>{p.name}</span>
        </li>
      ))}
    </ul>
    <button
      type="button"
      onClick={onOpen}
      className="font-sans inline-flex items-center gap-1 mt-4"
      style={{ fontSize: 12, fontWeight: 600, color: TEAL, background: 'transparent', border: 'none', padding: 0, cursor: 'pointer' }}
    >
      See all trap patterns
      <svg width="11" height="11" viewBox="0 0 12 12" fill="none" aria-hidden>
        <path d="M4 3L7 6L4 9" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </button>
  </section>
);

export default DebriefStage;
