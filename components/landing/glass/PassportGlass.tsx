/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The real Points Passport (components/PointsPassport) with locally editable sample grades
 * and a What-If Explorer. It
 * runs with an empty uid, which every hook underneath treats as "nobody":
 * nothing is loaded from or written to Firestore.
 */

import React, { Suspense, useState } from 'react';
import { ProgressProvider } from '../../../contexts/ProgressContext';
import { InnovationDataProvider } from '../../../contexts/InnovationDataContext';
import { GlassStage, type GlassLocks, type GlassProps } from './GlassStage';
import { DEMO_PROFILE } from './demoProfile';

const PointsPassport = React.lazy(() => import('../../PointsPassport'));

export const PASSPORT_MODES_LIVE: { id: string; label: string }[] = [];

const LOCKED_TABS = new Set(['Mock Tracker', 'Scenarios', 'Best Moves']);
/** The simulator owns its Overview lock so keyboard navigation respects it too. */
const LOCKS: GlassLocks = { test: (name, el) => el.getAttribute('role') === 'tab' && LOCKED_TABS.has(name) };

const PassportGlass: React.FC<GlassProps> = ({ active, height = 720, logicalWidth }) => {
  const [profile, setProfile] = useState(DEMO_PROFILE);
  return (
  <GlassStage active={active} height={height} logicalWidth={logicalWidth} locks={LOCKS}>
    {active && (
      <ProgressProvider>
        <InnovationDataProvider uid={undefined} subjectProfile={profile}>
        <Suspense fallback={null}>
          <div className="landing-glass-pad landing-glass-pad--airy">
            <PointsPassport uid="" profile={profile} onProfileChange={setProfile} initialTab="overview" lockSimulatorOverview />
          </div>
        </Suspense>
        </InnovationDataProvider>
      </ProgressProvider>
    )}
  </GlassStage>
  );
};

export default PassportGlass;
