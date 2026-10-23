/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Dev-only harness for the end-of-session quiz — mirrors year-islands-dev.tsx.
 * Renders the real StudySessionQuiz as the Demo Account (no auth; the review
 * deck writes are no-ops for the demo uid) over a REAL Mark Bank deck, because
 * a real session has to run for five minutes before it can be saved:
 * `npx vite`, then open /study-quiz-dev.html. Query options:
 *   ?subject=Chemistry&level=ordinary   which deck (defaults shown)
 *   ?theme=dark                         dark mode
 * Never part of the production build (vite.config.ts lists its HTML inputs
 * explicitly).
 */
import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import StudySessionQuiz from './components/study/quiz/StudySessionQuiz';
import type { QuizResult } from './components/study/quiz/studyQuizPlan';
import { DEMO_STUDENT_UID } from './data/devStudent';
import './index.css';

const params = new URLSearchParams(window.location.search);
if (params.get('theme') === 'dark') document.documentElement.classList.add('dark');
const subject = params.get('subject') ?? 'Chemistry';
const level = params.get('level') ?? 'ordinary';

function Harness() {
  const [outcome, setOutcome] = useState<string | null>(null);
  if (outcome) {
    return (
      <main style={{ padding: 40, fontFamily: 'DM Sans, sans-serif' }}>
        <p>{outcome}</p>
        <button type="button" onClick={() => window.location.reload()}>Run it again</button>
      </main>
    );
  }
  return (
    <StudySessionQuiz
      uid={DEMO_STUDENT_UID}
      subject={subject}
      profileSubjects={[{ subjectName: subject, level: level as 'higher' | 'ordinary' | 'common' }]}
      character="star-crew:maker"
      onDone={(results: QuizResult[]) => setOutcome(results.length
        ? `Done: ${results.reduce((n, r) => n + r.marksClaimed, 0)} of ${results.reduce((n, r) => n + r.marksAvailable, 0)} marks over ${results.length} questions.`
        : 'Nothing to quiz for this deck (no short cards, or no deck).')}
      onSkip={() => setOutcome('Skipped.')}
    />
  );
}

const root = document.getElementById('root');
if (root) createRoot(root).render(<Harness />);
