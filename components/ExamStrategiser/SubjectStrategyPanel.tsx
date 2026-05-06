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
        backgroundColor: '#FAF7F4',
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

      {pinned.length > 0 && (
        <div className="space-y-2.5 mb-3">
          {pinned.map(rule => (
            <article
              key={rule.id}
              className="rounded-xl"
              style={{
                backgroundColor: '#FFFFFF',
                border: `1px solid ${TEAL}55`,
                padding: '14px 16px',
                boxShadow: `0 0 0 1px ${TEAL}11`,
              }}
            >
              <div className="flex items-baseline gap-2 mb-1.5">
                <PinIcon />
                <h4 className="font-serif" style={{ fontSize: 14.5, fontWeight: 600, color: '#1A1A1A' }}>
                  {rule.title}
                </h4>
              </div>
              <p className="font-sans" style={{ fontSize: 13, color: '#3F3B36', lineHeight: 1.55 }}>
                {rule.body}
              </p>
            </article>
          ))}
        </div>
      )}

      <div className="space-y-2">
        {others.map(rule => (
          <article
            key={rule.id}
            className="rounded-xl"
            style={{
              backgroundColor: '#FFFFFF',
              border: '1px solid #EDEBE8',
              padding: '13px 16px',
            }}
          >
            <h4 className="font-serif" style={{ fontSize: 14, fontWeight: 600, color: '#1A1A1A', marginBottom: 4 }}>
              {rule.title}
            </h4>
            <p className="font-sans" style={{ fontSize: 12.5, color: '#5C5852', lineHeight: 1.55 }}>
              {rule.body}
            </p>
          </article>
        ))}
      </div>

      <div className="mt-4 pt-4" style={{ borderTop: '1px solid #EDEBE8' }}>
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#A8A29E', marginBottom: 6 }}>
          Marks → minutes
        </p>
        <p className="font-sans" style={{ fontSize: 12.5, color: '#3F3B36', marginBottom: 6, fontWeight: 500 }}>
          {strategy.marksToMinutes.summary}
        </p>
        <ul className="space-y-0.5">
          {strategy.marksToMinutes.examples.map((ex, i) => (
            <li key={i} className="font-sans" style={{ fontSize: 12, color: '#78716C', lineHeight: 1.5, paddingLeft: 12, position: 'relative' }}>
              <span style={{ position: 'absolute', left: 0, color: TEAL }}>·</span>
              {ex}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
};

const PinIcon: React.FC = () => (
  <svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden style={{ flexShrink: 0, marginTop: 2 }}>
    <path d="M6 1.5L7.4 4.6L10.5 5L8.2 7.2L8.8 10.5L6 9L3.2 10.5L3.8 7.2L1.5 5L4.6 4.6L6 1.5Z" stroke={TEAL} strokeWidth="1.3" fill="none" strokeLinejoin="round" />
  </svg>
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
