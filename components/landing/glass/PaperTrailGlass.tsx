/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The real Paper Trail (components/PaperTrail), signed out, with the same
 * fifteen subjects as Mark Bank on its grid. Mathematics is open — 200 of its
 * 222 papers carry answer maps — and the scripted cursor opens it; the rest
 * show with a lock, as do the "All subjects" switches.
 */

import React, { Suspense } from 'react';
import { ProgressProvider } from '../../../contexts/ProgressContext';
import { GlassStage, type AutoStep, type GlassLocks, type GlassProps } from './GlassStage';
import { LANDING_SUBJECTS, PAPER_TRAIL_OPEN_SUBJECT } from './demoProfile';
import { openDemo } from './demoEvent';

const PaperTrail = React.lazy(() => import('../../PaperTrail'));

export const PAPERTRAIL_MODES_LIVE: { id: string; label: string }[] = [];

const LEVELS = LANDING_SUBJECTS.map(name => ({ name, level: 'higher' }));

const LOCKS: GlassLocks = {
  names: [...LANDING_SUBJECTS.filter(s => s !== PAPER_TRAIL_OPEN_SUBJECT), 'All subjects', 'Browse all subjects'],
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
            studentSubjects={[...LANDING_SUBJECTS]}
            studentLevels={LEVELS}
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
