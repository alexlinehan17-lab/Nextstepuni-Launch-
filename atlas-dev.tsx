/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * DEV-ONLY harness: mounts the Topic Vault (ReviseByTopic) directly, no auth,
 * for visual iteration. Served only in `npm run dev` (vite serves any root
 * .html); the production build's single rollup input ignores it.
 */
import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import ReviseByTopic from './components/PaperTrail/ReviseByTopic';
import { taggedSubjects } from './components/PaperTrail/topics';
import { PAPER_TRAIL_SUBJECTS } from './paperTrailData';

const labels = new Map(PAPER_TRAIL_SUBJECTS.map(s => [s.id, s.name] as const));
const subjects = taggedSubjects()
  .filter(id => labels.has(id))
  .map(id => ({ id, label: labels.get(id)! }))
  .sort((a, b) => a.label.localeCompare(b.label));

const App = () => (
  <ReviseByTopic
    subjects={subjects}
    mineIds={['biology', 'english', 'mathematics']}
    uid={undefined}
    subjectLabel={(id: string) => labels.get(id) ?? id}
    onOpenQuestion={(t) => window.alert(`open ${t.year} ${t.level} Q${t.n}`)}
    onBack={() => window.alert('back')}
  />
);
createRoot(document.getElementById('root')!).render(<App />);
