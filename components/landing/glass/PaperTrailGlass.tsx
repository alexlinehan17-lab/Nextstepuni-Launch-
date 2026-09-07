/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The real Paper Trail (components/PaperTrail), signed out, with the sample
 * student's seven subjects under "My subjects". Mathematics is open — 200 of
 * its 222 papers carry answer maps — and the scripted cursor opens it; the
 * other six show with a lock, as do the "All subjects" switches.
 */

import React, { Suspense } from 'react';
import { ProgressProvider } from '../../../contexts/ProgressContext';
import { GlassStage, type AutoStep, type GlassLocks, type GlassProps } from './GlassStage';
import { DEMO_LEVELS, DEMO_SUBJECT_NAMES, PAPER_TRAIL_OPEN_SUBJECT } from './demoProfile';
import { openDemo } from './demoEvent';

const PaperTrail = React.lazy(() => import('../../PaperTrail'));

export const PAPERTRAIL_MODES_LIVE: { id: string; label: string }[] = [];

const LOCKS: GlassLocks = {
  names: [...DEMO_SUBJECT_NAMES.filter(s => s !== PAPER_TRAIL_OPEN_SUBJECT), 'All subjects', 'Browse all subjects'],
  nameOf: el => el.querySelector('.pt-subject-name')?.textContent?.trim() || undefined,
};

const AUTO: AutoStep[] = [{ text: PAPER_TRAIL_OPEN_SUBJECT, before: 1800, hold: 60000, then: 'top' }];

const PaperTrailGlass: React.FC<GlassProps> = ({ active, height = 720, logicalWidth }) => (
  <GlassStage active={active} height={height} logicalWidth={logicalWidth} locks={LOCKS} auto={AUTO}>
    {active && (
      <ProgressProvider>
      <Suspense fallback={null}>
        <div className="landing-glass-pad">
          <PaperTrail
            uid={undefined}
            studentSubjects={[...DEMO_SUBJECT_NAMES]}
            studentLevels={DEMO_LEVELS}
            studentCycle="leaving-cert"
            onOpenTool={() => openDemo('atlas')}
            onBack={() => undefined}
          />
        </div>
      </Suspense>
      </ProgressProvider>
    )}
  </GlassStage>
);

export default PaperTrailGlass;
