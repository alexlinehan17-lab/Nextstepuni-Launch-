/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The real Points Passport (components/PointsPassport) opened on its Grade
 * Planner tab for the sample student; the other four tabs show locked. It
 * runs with an empty uid, which every hook underneath treats as "nobody":
 * nothing is loaded from or written to Firestore.
 */

import React, { Suspense } from 'react';
import { ProgressProvider } from '../../../contexts/ProgressContext';
import { InnovationDataProvider } from '../../../contexts/InnovationDataContext';
import { GlassStage, type GlassLocks, type GlassProps } from './GlassStage';
import { DEMO_PROFILE } from './demoProfile';

const PointsPassport = React.lazy(() => import('../../PointsPassport'));

export const PASSPORT_MODES_LIVE: { id: string; label: string }[] = [];

const LOCKED_TABS = new Set(['Overview', 'Mock Tracker', 'Scenarios', 'Best Moves']);
/** Only the section tabs — the Grade Planner has its own "Overview" toggle, which stays live. */
const LOCKS: GlassLocks = { test: (name, el) => el.getAttribute('role') === 'tab' && LOCKED_TABS.has(name) };

const PassportGlass: React.FC<GlassProps> = ({ active, height = 720, logicalWidth }) => (
  <GlassStage active={active} height={height} logicalWidth={logicalWidth} locks={LOCKS}>
    {active && (
      <ProgressProvider>
        <InnovationDataProvider uid={undefined} subjectProfile={DEMO_PROFILE}>
        <Suspense fallback={null}>
          <div className="landing-glass-pad">
            <PointsPassport uid="" profile={DEMO_PROFILE} onOpenSettings={() => undefined} initialTab="planner" />
          </div>
        </Suspense>
        </InnovationDataProvider>
      </ProgressProvider>
    )}
  </GlassStage>
);

export default PassportGlass;
