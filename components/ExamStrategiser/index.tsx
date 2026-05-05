/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Exam Strategiser — top-level: subject tabs + question list + player switch.
 * No props — pulls all data from the static question registry. Eventually
 * will filter by the student's subject profile, but for now it shows all
 * subjects regardless.
 */

import React, { useMemo, useState } from 'react';
import { EXAM_SUBJECTS } from '../../data/examQuestions';
import { type ExamQuestion, type ExamSubject } from '../../types/examStrategiser';
import QuestionList from './QuestionList';
import QuestionPlayer from './QuestionPlayer';

const TEAL = '#2A7D6F';

const ExamStrategiser: React.FC = () => {
  const [subject, setSubject] = useState<ExamSubject>('english');
  const [activeQuestion, setActiveQuestion] = useState<ExamQuestion | null>(null);

  const questions = useMemo(
    () => EXAM_SUBJECTS.find(s => s.id === subject)?.questions ?? [],
    [subject],
  );

  if (activeQuestion) {
    return (
      <div className="max-w-4xl mx-auto w-full">
        <QuestionPlayer
          question={activeQuestion}
          onBackToList={() => setActiveQuestion(null)}
        />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto w-full space-y-6">
      <header>
        <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#A8A29E' }}>
          Exam Strategiser
        </p>
        <h1 className="font-serif" style={{ fontSize: 28, fontWeight: 600, color: '#1A1A1A', marginTop: 4, lineHeight: 1.2 }}>
          Real questions, decoded.
        </h1>
        <p className="font-sans max-w-xl" style={{ fontSize: 14, color: '#78716C', marginTop: 8, lineHeight: 1.55 }}>
          Predict before you see the answers. Then we walk through the question the way an examiner would — what to spot, what to avoid, where the marks live.
        </p>
      </header>

      <div className="flex items-center gap-1 p-1 rounded-xl bg-zinc-100 dark:bg-zinc-800/50 w-fit">
        {EXAM_SUBJECTS.map(s => {
          const active = s.id === subject;
          return (
            <button
              key={s.id}
              type="button"
              onClick={() => setSubject(s.id)}
              className="rounded-lg transition-colors font-sans"
              style={{
                padding: '8px 16px',
                fontSize: 13,
                fontWeight: 600,
                backgroundColor: active ? '#FFFFFF' : 'transparent',
                color: active ? TEAL : '#78716C',
                border: 'none',
                cursor: 'pointer',
                boxShadow: active ? '0 1px 2px rgba(0,0,0,0.04)' : 'none',
              }}
            >
              {s.label}
            </button>
          );
        })}
      </div>

      <QuestionList questions={questions} onSelect={(q) => setActiveQuestion(q)} />
    </div>
  );
};

export default ExamStrategiser;
