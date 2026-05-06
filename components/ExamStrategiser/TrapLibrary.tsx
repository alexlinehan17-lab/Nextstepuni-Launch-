/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * TrapLibrary — cross-subject catalog of recurring trap patterns. Each
 * pattern carries a description, "how to spot it" diagnostic, and 1-3
 * example links to real questions in the bank. Clicking an example
 * navigates to that question.
 */

import React, { useMemo, useState } from 'react';
import { type ExamSubject, type TrapPattern } from '../../types/examStrategiser';
import { TRAP_PATTERNS } from '../../data/examStrategy';

const TEAL = '#2A7D6F';

interface Props {
  /** Called when a student clicks an example. Navigates to the question. */
  onOpenQuestion: (questionId: string) => void;
}

type SubjectFilter = 'all' | ExamSubject;

const SUBJECT_LABELS: Record<SubjectFilter, string> = {
  all: 'All',
  english: 'English',
  irish: 'Irish',
  maths: 'Maths',
  geography: 'Geography',
};

const TrapLibrary: React.FC<Props> = ({ onOpenQuestion }) => {
  const [filter, setFilter] = useState<SubjectFilter>('all');

  const patterns = useMemo(() => {
    if (filter === 'all') return TRAP_PATTERNS;
    return TRAP_PATTERNS.filter(p => p.subjects.includes(filter));
  }, [filter]);

  return (
    <div className="space-y-6">
      <header>
        <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#A8A29E' }}>
          Trap Library
        </p>
        <h1 className="font-serif" style={{ fontSize: 28, fontWeight: 600, color: '#1A1A1A', marginTop: 4, lineHeight: 1.2 }}>
          The same traps, again and again.
        </h1>
        <p className="font-sans max-w-xl" style={{ fontSize: 14, color: '#78716C', marginTop: 8, lineHeight: 1.55 }}>
          Examiners reuse the same trap shapes across subjects and years. Learn the pattern once, recognise it everywhere. Each entry links to the real questions where it appears.
        </p>
      </header>

      <FilterStrip value={filter} onChange={setFilter} />

      <div className="space-y-3">
        {patterns.map(p => (
          <PatternCard key={p.id} pattern={p} onOpenQuestion={onOpenQuestion} />
        ))}
      </div>

      {patterns.length === 0 && (
        <div
          className="rounded-2xl text-center"
          style={{
            backgroundColor: '#FAF7F4',
            border: '1px solid #EDEBE8',
            padding: '36px 24px',
          }}
        >
          <p className="font-serif" style={{ fontSize: 16, fontWeight: 600, color: '#1A1A1A', marginBottom: 4 }}>
            No trap patterns for this subject yet
          </p>
          <p className="font-sans" style={{ fontSize: 13, color: '#78716C' }}>
            Patterns are added as more questions are authored.
          </p>
        </div>
      )}
    </div>
  );
};

// ── Filter strip ───────────────────────────────────────────────────────

const FilterStrip: React.FC<{ value: SubjectFilter; onChange: (v: SubjectFilter) => void }> = ({ value, onChange }) => (
  <div className="flex items-center gap-1 p-1 rounded-xl bg-zinc-100 dark:bg-zinc-800/50 w-fit overflow-x-auto">
    {(['all', 'english', 'irish', 'maths', 'geography'] as const).map(option => {
      const active = option === value;
      return (
        <button
          key={option}
          type="button"
          onClick={() => onChange(option)}
          className="rounded-lg transition-colors font-sans whitespace-nowrap"
          style={{
            padding: '8px 14px',
            fontSize: 13,
            fontWeight: 600,
            backgroundColor: active ? '#FFFFFF' : 'transparent',
            color: active ? TEAL : '#78716C',
            border: 'none',
            cursor: 'pointer',
            boxShadow: active ? '0 1px 2px rgba(0,0,0,0.04)' : 'none',
          }}
        >
          {SUBJECT_LABELS[option]}
        </button>
      );
    })}
  </div>
);

// ── Pattern card ───────────────────────────────────────────────────────

const PatternCard: React.FC<{ pattern: TrapPattern; onOpenQuestion: (id: string) => void }> = ({ pattern, onOpenQuestion }) => (
  <article
    className="rounded-2xl"
    style={{
      backgroundColor: '#FFFFFF',
      border: '1px solid #EDEBE8',
      padding: '22px 24px',
    }}
  >
    <header className="flex flex-wrap items-baseline gap-x-3 gap-y-1 mb-3">
      <h3 className="font-serif" style={{ fontSize: 17, fontWeight: 600, color: '#1A1A1A' }}>
        {pattern.name}
      </h3>
      <div className="flex flex-wrap gap-1">
        {pattern.subjects.map(s => (
          <span
            key={s}
            className="font-sans"
            style={{
              fontSize: 10,
              fontWeight: 700,
              textTransform: 'uppercase',
              letterSpacing: 0.5,
              color: TEAL,
              backgroundColor: '#FAF7F4',
              border: `1px solid ${TEAL}33`,
              borderRadius: 999,
              padding: '2px 8px',
            }}
          >
            {s}
          </span>
        ))}
      </div>
    </header>

    <p className="font-sans" style={{ fontSize: 13.5, color: '#3F3B36', lineHeight: 1.55, marginBottom: 12 }}>
      {pattern.description}
    </p>

    <div className="rounded-lg" style={{ backgroundColor: '#FAF7F4', border: '1px solid #EDEBE8', padding: '10px 14px', marginBottom: 14 }}>
      <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 4 }}>
        How to spot it
      </p>
      <p className="font-sans" style={{ fontSize: 12.5, color: '#3F3B36', lineHeight: 1.55 }}>
        {pattern.diagnostic}
      </p>
    </div>

    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#A8A29E', marginBottom: 8 }}>
      Where it appears
    </p>
    <ul className="space-y-2">
      {pattern.examples.map((ex, i) => (
        <li key={i}>
          <button
            type="button"
            onClick={() => onOpenQuestion(ex.questionId)}
            className="w-full text-left rounded-lg transition-colors"
            style={{
              backgroundColor: '#FFFFFF',
              border: '1px solid #EDEBE8',
              padding: '10px 14px',
              cursor: 'pointer',
            }}
            onMouseEnter={(e) => { e.currentTarget.style.borderColor = TEAL + '55'; e.currentTarget.style.backgroundColor = '#FAF7F4'; }}
            onMouseLeave={(e) => { e.currentTarget.style.borderColor = '#EDEBE8'; e.currentTarget.style.backgroundColor = '#FFFFFF'; }}
          >
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0 flex-1">
                <p className="font-mono" style={{ fontSize: 10.5, fontWeight: 600, color: '#A8A29E', marginBottom: 3, letterSpacing: 0.2 }}>
                  {ex.questionId}
                </p>
                <p className="font-sans" style={{ fontSize: 12.5, color: '#3F3B36', lineHeight: 1.5 }}>
                  {ex.snippet}
                </p>
              </div>
              <ArrowIcon />
            </div>
          </button>
        </li>
      ))}
    </ul>
  </article>
);

const ArrowIcon: React.FC = () => (
  <svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden style={{ flexShrink: 0, color: TEAL, marginTop: 2 }}>
    <path d="M5 3L10 8L5 13" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

export default TrapLibrary;
