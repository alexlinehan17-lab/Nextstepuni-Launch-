/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * QuestionList — shows available questions for the active subject, grouped
 * by paper when paper metadata is present, falling back to a flat list.
 */

import React from 'react';
import { type ExamQuestion } from '../../types/examStrategiser';

const TEAL = '#2A7D6F';

interface Props {
  questions: ExamQuestion[];
  onSelect: (q: ExamQuestion) => void;
}

const QuestionList: React.FC<Props> = ({ questions, onSelect }) => {
  if (questions.length === 0) {
    return (
      <div
        className="rounded-2xl text-center"
        style={{
          backgroundColor: '#FAF7F4',
          border: '1px solid #EDEBE8',
          padding: '36px 24px',
        }}
      >
        <p className="font-serif" style={{ fontSize: 18, fontWeight: 600, color: '#1A1A1A', marginBottom: 6 }}>
          No questions for this subject yet
        </p>
        <p className="font-sans" style={{ fontSize: 13, color: '#78716C' }}>
          We're adding questions one at a time so each one gets the full examiner treatment.
        </p>
      </div>
    );
  }

  // Group by paper if any question declares one.
  const hasPapers = questions.some(q => q.paper);
  if (!hasPapers) {
    return <div className="space-y-2">{questions.map(q => <QuestionRow key={q.id} q={q} onSelect={onSelect} />)}</div>;
  }

  const groups: Record<string, ExamQuestion[]> = {};
  for (const q of questions) {
    const key = q.paper ?? 'Other';
    if (!groups[key]) groups[key] = [];
    groups[key].push(q);
  }
  const orderedKeys = Object.keys(groups).sort((a, b) => a.localeCompare(b));

  return (
    <div className="space-y-6">
      {orderedKeys.map(key => (
        <section key={key}>
          <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#A8A29E', marginBottom: 8 }}>
            {key}
          </p>
          <div className="space-y-2">
            {groups[key].map(q => <QuestionRow key={q.id} q={q} onSelect={onSelect} />)}
          </div>
        </section>
      ))}
    </div>
  );
};

const QuestionRow: React.FC<{ q: ExamQuestion; onSelect: (q: ExamQuestion) => void }> = ({ q, onSelect }) => (
  <button
    type="button"
    onClick={() => onSelect(q)}
    className="w-full text-left rounded-xl transition-colors"
    style={{
      backgroundColor: '#FFFFFF',
      border: '1px solid #EDEBE8',
      padding: '16px 18px',
      cursor: 'pointer',
    }}
    onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = '#FAF7F4'; }}
    onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = '#FFFFFF'; }}
  >
    <div className="flex items-baseline justify-between gap-3">
      <div className="flex-1 min-w-0">
        <p className="font-serif" style={{ fontSize: 16, fontWeight: 600, color: '#1A1A1A' }}>
          {q.year} · Question {q.questionNumber}
          {q.section ? <span className="font-sans" style={{ fontSize: 12, color: '#78716C', fontWeight: 400, marginLeft: 8 }}>· {q.section}</span> : null}
        </p>
        {q.commandWords.length > 0 && (
          <p className="font-sans" style={{ fontSize: 12, color: '#78716C', marginTop: 3 }}>
            {q.commandWords.join(', ')}
          </p>
        )}
      </div>
      <div className="flex items-center gap-2 shrink-0">
        {q.level && (
          <span className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.4, color: '#A8A29E' }}>
            {q.level}
          </span>
        )}
        <span
          className="font-sans"
          style={{
            fontSize: 11,
            fontWeight: 700,
            color: TEAL,
            backgroundColor: '#FAF7F4',
            border: `1px solid ${TEAL}33`,
            borderRadius: 999,
            padding: '3px 9px',
          }}
        >
          {q.marks} marks
        </span>
      </div>
    </div>
  </button>
);

export default QuestionList;
