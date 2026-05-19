/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * SubjectStrategyPanel — meta-rules read once before opening any specific
 * question. Sits above the question list per subject.
 *
 * Collapse state persists per subject in localStorage so power users who've
 * internalised the rules don't have to dismiss it on every visit.
 */

import React, { useState, useEffect } from 'react';
import { type ExamSubject } from '../../types/examStrategiser';
import { getSubjectStrategy } from '../../data/examStrategy';

const TEAL = '#2A7D6F';
const STORAGE_KEY_PREFIX = 'examStrategiser:strategy:hidden:';

interface Props {
  subject: ExamSubject;
}

const SubjectStrategyPanel: React.FC<Props> = ({ subject }) => {
  const strategy = getSubjectStrategy(subject);
  const storageKey = STORAGE_KEY_PREFIX + subject;

  // Load hidden state from localStorage on mount + on subject change.
  const [hidden, setHidden] = useState(false);
  useEffect(() => {
    try {
      const v = localStorage.getItem(storageKey);
      setHidden(v === '1');
    } catch {
      setHidden(false);
    }
  }, [storageKey]);

  const toggle = (next: boolean) => {
    setHidden(next);
    try {
      localStorage.setItem(storageKey, next ? '1' : '0');
    } catch {
      // localStorage unavailable — non-fatal
    }
  };

  if (hidden) {
    return (
      <button
        type="button"
        onClick={() => toggle(false)}
        className="font-sans flex items-center gap-1.5 transition-colors"
        style={{
          fontSize: 12,
          color: TEAL,
          background: 'transparent',
          border: 'none',
          padding: 0,
          cursor: 'pointer',
          fontWeight: 600,
        }}
      >
        <ChevronIcon direction="down" />
        Show strategy guide
      </button>
    );
  }

  const pinned = strategy.rules.filter(r => r.pinned);
  const others = strategy.rules.filter(r => !r.pinned);

  return (
    <section
      className="rounded-2xl"
      style={{
        backgroundColor: '#F0FAF8',
        border: '1px solid #EDEBE8',
        padding: '24px 26px',
      }}
    >
      <header className="flex items-start justify-between gap-4 mb-4">
        <div className="min-w-0">
          <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL }}>
            Read me first
          </p>
          <h3 className="font-serif" style={{ fontSize: 19, fontWeight: 600, color: '#1A1A1A', marginTop: 3, lineHeight: 1.3 }}>
            {strategy.headline}
          </h3>
          <p className="font-sans" style={{ fontSize: 13, color: '#5C5852', marginTop: 6, lineHeight: 1.55, maxWidth: '60ch' }}>
            {strategy.intro}
          </p>
        </div>
        <button
          type="button"
          onClick={() => toggle(true)}
          className="font-sans shrink-0 transition-colors"
          style={{
            fontSize: 11,
            fontWeight: 600,
            color: '#78716C',
            background: 'transparent',
            border: 'none',
            padding: 0,
            cursor: 'pointer',
            whiteSpace: 'nowrap',
          }}
        >
          Hide
        </button>
      </header>

      <div className="space-y-2">
        {pinned.map(rule => (
          <RuleCard key={rule.id} rule={rule} isKey />
        ))}
        {others.map(rule => (
          <RuleCard key={rule.id} rule={rule} />
        ))}
      </div>

      <div className="mt-4 pt-4" style={{ borderTop: '1px solid #EDEBE8' }}>
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#A8A29E', marginBottom: 6 }}>
          Marks → minutes
        </p>
        <p className="font-sans" style={{ fontSize: 12.5, color: '#3F3B36', lineHeight: 1.55 }}>
          {strategy.marksToMinutes.summary}
          {strategy.marksToMinutes.examples.length > 0 && (
            <span style={{ color: '#78716C' }}>
              {' '}{strategy.marksToMinutes.examples.join(' · ')}
            </span>
          )}
        </p>
      </div>
    </section>
  );
};

const RuleCard: React.FC<{ rule: { id: string; title: string; body: string }; isKey?: boolean }> = ({ rule, isKey }) => (
  <article
    className="rounded-xl"
    style={{
      backgroundColor: '#FFFFFF',
      border: '1px solid #EDEBE8',
      padding: '13px 16px',
    }}
  >
    <div className="flex items-baseline gap-2 mb-1">
      {isKey && (
        <span className="font-sans" style={{ fontSize: 9, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, flexShrink: 0 }}>
          Key
        </span>
      )}
      <h4 className="font-serif" style={{ fontSize: 14, fontWeight: 600, color: '#1A1A1A' }}>
        {rule.title}
      </h4>
    </div>
    <p className="font-sans" style={{ fontSize: 12.5, color: '#5C5852', lineHeight: 1.55 }}>
      {rule.body}
    </p>
  </article>
);

const ChevronIcon: React.FC<{ direction: 'up' | 'down' }> = ({ direction }) => (
  <svg width="11" height="11" viewBox="0 0 12 12" fill="none" aria-hidden>
    <path
      d={direction === 'down' ? 'M3 4.5L6 7.5L9 4.5' : 'M3 7.5L6 4.5L9 7.5'}
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

export default SubjectStrategyPanel;
