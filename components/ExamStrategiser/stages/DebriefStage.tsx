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
} from '../../../types/examStrategiser';
import CollapsibleQuestionCard from '../CollapsibleQuestionCard';

const TEAL = '#2A7D6F';

interface Props {
  question: ExamQuestion;
  /** Predict answers the student gave — used to render their attempt
   *  alongside the correct answer in the per-prompt debrief. */
  answers: PredictAnswers;
}

const DebriefStage: React.FC<Props> = ({ question, answers }) => {
  const isMigrated =
    !!question.biggestMistake ||
    question.predictPrompts.some(p => !!p.debrief);

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

      {isMigrated ? (
        <MigratedDebrief question={question} answers={answers} />
      ) : (
        <LegacyDebrief question={question} />
      )}
    </div>
  );
};

// ── Migrated rendering ────────────────────────────────────────────────

const MigratedDebrief: React.FC<Props> = ({ question, answers }) => (
  <>
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
  </>
);

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
        padding: '20px 22px',
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

      <div className="grid sm:grid-cols-2 gap-3 mb-3">
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
        backgroundColor: isCorrect ? '#FAF7F4' : '#FFFFFF',
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
  <div className="mt-3 pt-3" style={{ borderTop: '1px solid #EDEBE8' }}>
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
      backgroundColor: '#FAF7F4',
      border: `1px solid ${TEAL}55`,
      padding: '22px 24px',
      boxShadow: `0 0 0 1px ${TEAL}11`,
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

// ── Legacy fallback ───────────────────────────────────────────────────

const LegacyDebrief: React.FC<{ question: ExamQuestion }> = ({ question }) => {
  const top = question.topAnswerIncludes ?? [];
  const traps = question.commonTraps ?? [];
  if (top.length === 0 && traps.length === 0) {
    return (
      <p className="font-sans" style={{ fontSize: 13, color: '#A8A29E', textAlign: 'center', padding: '40px 16px' }}>
        Debrief content for this question hasn't been authored yet.
      </p>
    );
  }
  return (
    <div className="grid md:grid-cols-2 gap-4">
      <LegacyPanel title="What a top answer includes" items={top} kind="positive" />
      <LegacyPanel title="Common traps" items={traps} kind="trap" />
    </div>
  );
};

const LegacyPanel: React.FC<{ title: string; items: string[]; kind: 'positive' | 'trap' }> = ({ title, items, kind }) => (
  <section
    className="rounded-2xl"
    style={{
      backgroundColor: kind === 'positive' ? '#FFFFFF' : '#FAF7F4',
      border: `1px solid ${kind === 'positive' ? '#EDEBE8' : `${TEAL}33`}`,
      padding: '22px 24px',
    }}
  >
    <h3 className="font-serif" style={{ fontSize: 15, fontWeight: 600, color: '#1A1A1A', marginBottom: 12 }}>
      {title}
    </h3>
    <ul className="space-y-2.5">
      {items.map((item, i) => (
        <li key={i} className="flex gap-2.5" style={{ fontSize: 13.5, lineHeight: 1.55, color: '#3F3B36', fontFamily: 'DM Sans, system-ui, sans-serif' }}>
          <span style={{ color: TEAL, fontWeight: 700, flexShrink: 0 }}>·</span>
          <span>{item}</span>
        </li>
      ))}
    </ul>
  </section>
);

export default DebriefStage;
