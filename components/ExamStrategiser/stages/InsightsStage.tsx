/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { type ExamQuestion } from '../../../types/examStrategiser';

const TEAL = '#2A7D6F';

interface Props {
  question: ExamQuestion;
}

const InsightsStage: React.FC<Props> = ({ question }) => (
  <div className="space-y-6">
    <header>
      <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#A8A29E' }}>
        Stage 4 · Insights
      </p>
      <h2 className="font-serif" style={{ fontSize: 24, fontWeight: 600, color: '#1A1A1A', marginTop: 4 }}>
        What separates a top answer from a middling one.
      </h2>
    </header>

    <div className="grid md:grid-cols-2 gap-4">
      <Panel title="What a top answer includes" items={question.topAnswerIncludes} kind="positive" />
      <Panel title="Common traps" items={question.commonTraps} kind="trap" />
    </div>
  </div>
);

const Panel: React.FC<{ title: string; items: string[]; kind: 'positive' | 'trap' }> = ({ title, items, kind }) => (
  <section
    className="rounded-2xl"
    style={{
      backgroundColor: kind === 'positive' ? '#FFFFFF' : '#FAF7F4',
      border: `1px solid ${kind === 'positive' ? '#EDEBE8' : `${TEAL}33`}`,
      padding: '22px 24px',
    }}
  >
    <div className="flex items-center gap-2 mb-4">
      {kind === 'positive' ? <CheckIcon /> : <AlertIcon />}
      <h3 className="font-serif" style={{ fontSize: 15, fontWeight: 600, color: '#1A1A1A' }}>{title}</h3>
    </div>
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

const CheckIcon: React.FC = () => (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden>
    <circle cx="8" cy="8" r="7" stroke={TEAL} strokeWidth="1.4" />
    <path d="M5 8.2 L7 10.2 L11 6" stroke={TEAL} strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" fill="none" />
  </svg>
);

const AlertIcon: React.FC = () => (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden>
    <path d="M8 2 L14.5 13 H1.5 L8 2 Z" stroke={TEAL} strokeWidth="1.4" fill="none" strokeLinejoin="round" />
    <line x1="8" y1="6.5" x2="8" y2="9.5" stroke={TEAL} strokeWidth="1.6" strokeLinecap="round" />
    <circle cx="8" cy="11.5" r="0.7" fill={TEAL} />
  </svg>
);

export default InsightsStage;
