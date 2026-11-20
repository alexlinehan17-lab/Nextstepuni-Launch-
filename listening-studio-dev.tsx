/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Dev-only harness for Listening Studio, on the pattern of study-quiz-dev.tsx.
 * Renders the real tool as the Demo Account (no auth; the review deck writes
 * are no-ops for the demo uid) over a REAL Mark Bank deck:
 * `npx vite`, then open /listening-studio-dev.html. Query options:
 *   ?subject=Music&level=higher   which deck (defaults shown)
 *   ?theme=dark                   dark mode
 * Never part of the production build (vite.config.ts lists its HTML inputs
 * explicitly).
 */
import React from 'react';
import { createRoot } from 'react-dom/client';
import MarkBank from './components/MarkBank/MarkBank';
import { DEMO_STUDENT_UID } from './data/devStudent';
import './index.css';

const params = new URLSearchParams(window.location.search);
if (params.get('theme') === 'dark') document.documentElement.classList.add('dark');
const subject = params.get('subject') ?? 'Music';
const level = params.get('level') ?? 'higher';

const root = document.getElementById('root');
if (root) {
  createRoot(root).render(
    <div className="product-shell" style={{ maxWidth: 1140, margin: '0 auto', padding: '24px 20px' }}>
      <MarkBank studio uid={DEMO_STUDENT_UID} studentSubjects={[{ subjectName: subject, level }]} />
    </div>,
  );
}
