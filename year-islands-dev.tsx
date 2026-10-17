/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Dev-only harness for year islands — mirrors onboarding-dev.tsx. Renders the
 * real JourneyView as the Demo Account (no Firebase, no auth) with SAMPLE
 * classmates from data/sampleYearIslands.ts: `npx vite`, then open
 * /year-islands-dev.html. Add ?theme=dark for dark mode. Never part of the
 * production build (vite.config.ts lists its HTML inputs explicitly).
 */
import React, { useCallback, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import ProgressContext from './contexts/ProgressContext';
import JourneyView from './components/journey/JourneyView';
import { DEMO_STUDENT_UID } from './data/devStudent';
import { sampleOwnPaperIsland } from './data/sampleYearIslands';
import type { ProgressDocument } from './services/progressRepository';
import './index.css';

if (new URLSearchParams(window.location.search).get('theme') === 'dark') document.documentElement.classList.add('dark');

type ProgressValue = NonNullable<React.ContextType<typeof ProgressContext>>;

function Harness() {
  const [progress, setProgress] = useState<ProgressDocument>(() => ({
    pointsData: { totalEarned: 1460, totalSpent: 0 },
    paperIsland: sampleOwnPaperIsland(),
  }));
  // Stable, like the real provider's: usePaperIsland reopens the island when they change.
  const updateDemoProgress = useCallback((updater: (current: ProgressDocument) => ProgressDocument) => setProgress(current => updater(current)), []);
  const reloadProgress = useCallback(() => {}, []);
  const value = useMemo(() => ({ rawProgressDoc: progress, updateDemoProgress, reloadProgress }) as unknown as ProgressValue,
    [progress, updateDemoProgress, reloadProgress]);
  return (
    <ProgressContext.Provider value={value}>
      <JourneyView
        user={{ uid: DEMO_STUDENT_UID, name: 'Demo Student', avatar: 'star-crew:maker', role: 'student', school: 'marino', yearGroup: '5th' }}
        hasSeenWelcome
        onDismissWelcome={() => {}}
        onBack={() => console.log('[year-islands-dev] back')}
        northStar={null}
        onOpenNorthStar={() => {}}
        pointsBalance={0}
        onPointsReload={() => {}}
        onOpenSetup={() => console.log('[year-islands-dev] open setup')}
      />
    </ProgressContext.Provider>
  );
}

const root = document.getElementById('root');
if (root) createRoot(root).render(<Harness />);
