/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * QuestionList — shows available questions for the active subject.
 * Two grouping modes: by Year (papers) — the default — or by Type
 * (cross-question taxonomy from data/examStrategy/taskTypes.ts) so
 * students can see the recurring structural pattern.
 */

import React, { useState } from 'react';
import { type ExamQuestion } from '../../types/examStrategiser';
import { getTaskType } from '../../data/examStrategy/taskTypes';

const TEAL = '#2A7D6F';

type GroupBy = 'year' | 'type';

interface Props {
  questions: ExamQuestion[];
  onSelect: (q: ExamQuestion) => void;
}

const QuestionList: React.FC<Props> = ({ questions, onSelect }) => {
  const [groupBy, setGroupBy] = useState<GroupBy>('year');

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

  return (
    <div className="space-y-5">
      <GroupByToggle value={groupBy} onChange={setGroupBy} />
      {groupBy === 'year'
        ? <ByYear questions={questions} onSelect={onSelect} />
        : <ByType questions={questions} onSelect={onSelect} />}
    </div>
  );
};

// ── Toggle ─────────────────────────────────────────────────────────────

const GroupByToggle: React.FC<{ value: GroupBy; onChange: (g: GroupBy) => void }> = ({ value, onChange }) => (
  <div className="flex items-center gap-2">
    <span className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#A8A29E' }}>
      Group by
    </span>
    <div className="flex items-center gap-1 p-1 rounded-lg bg-zinc-100 dark:bg-zinc-800/50">
      {(['year', 'type'] as const).map(option => {
        const active = option === value;
        return (
          <button
            key={option}
            type="button"
            onClick={() => onChange(option)}
            className="rounded-md font-sans transition-colors"
            style={{
              padding: '5px 12px',
              fontSize: 12,
              fontWeight: 600,
              backgroundColor: active ? '#FFFFFF' : 'transparent',
              color: active ? TEAL : '#78716C',
              border: 'none',
              cursor: 'pointer',
              boxShadow: active ? '0 1px 2px rgba(0,0,0,0.04)' : 'none',
              textTransform: 'capitalize',
            }}
          >
            {option}
          </button>
        );
      })}
    </div>
  </div>
);

// ── By Year (existing behaviour) ───────────────────────────────────────

const ByYear: React.FC<Props> = ({ questions, onSelect }) => {
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

// ── By Type (new) ──────────────────────────────────────────────────────

const ByType: React.FC<Props> = ({ questions, onSelect }) => {
  // Group by taskType. Each section heading carries the registry's friendly
  // label + description so students learn the type vocabulary alongside the
  // questions.
  const groups: Record<string, ExamQuestion[]> = {};
  for (const q of questions) {
    const key = q.taskType || 'unknown';
    if (!groups[key]) groups[key] = [];
    groups[key].push(q);
  }
  // Sort questions within each group by year desc then question number, so
  // students see the most recent example first.
  for (const key of Object.keys(groups)) {
    groups[key].sort((a, b) => (b.year - a.year) || a.questionNumber.localeCompare(b.questionNumber));
  }
  // Order types by the count of questions desc — the types with the most
  // examples (the strongest pattern) surface first.
  const orderedKeys = Object.keys(groups).sort((a, b) => groups[b].length - groups[a].length);

  return (
    <div className="space-y-7">
      {orderedKeys.map(key => {
        const meta = getTaskType(key);
        const label = meta?.label ?? key;
        const description = meta?.description;
        const count = groups[key].length;
        return (
          <section key={key}>
            <div className="mb-2.5">
              <div className="flex items-baseline gap-2">
                <p className="font-serif" style={{ fontSize: 14, fontWeight: 600, color: '#1A1A1A' }}>
                  {label}
                </p>
                <span className="font-sans" style={{ fontSize: 10, fontWeight: 700, color: TEAL, backgroundColor: '#FAF7F4', border: `1px solid ${TEAL}33`, borderRadius: 999, padding: '1px 7px' }}>
                  {count}
                </span>
              </div>
              {description && (
                <p className="font-sans" style={{ fontSize: 12, color: '#78716C', marginTop: 3, lineHeight: 1.5 }}>
                  {description}
                </p>
              )}
            </div>
            <div className="space-y-2">
              {groups[key].map(q => <QuestionRow key={q.id} q={q} onSelect={onSelect} showPaper />)}
            </div>
          </section>
        );
      })}
    </div>
  );
};

// ── Row ────────────────────────────────────────────────────────────────

const QuestionRow: React.FC<{ q: ExamQuestion; onSelect: (q: ExamQuestion) => void; showPaper?: boolean }> = ({ q, onSelect, showPaper }) => (
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
          {q.year}
          {showPaper && q.paper ? <span className="font-sans" style={{ fontSize: 12, color: '#A8A29E', fontWeight: 500, marginLeft: 6 }}>· {q.paper}</span> : null}
          <span className="mx-1" style={{ color: '#A8A29E' }}>·</span>
          Question {q.questionNumber}
          {q.section && !showPaper ? <span className="font-sans" style={{ fontSize: 12, color: '#78716C', fontWeight: 400, marginLeft: 8 }}>· {q.section}</span> : null}
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
