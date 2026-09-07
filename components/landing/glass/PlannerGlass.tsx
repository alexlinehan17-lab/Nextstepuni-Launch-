/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The real spaced-repetition timetable (components/SpacedRepetitionTimetable)
 * built for the sample sixth-year: six subjects, Sundays off, exams from
 * 2 June 2027. No uid, so nothing is read or written anywhere.
 */

import React, { Suspense } from 'react';
import { ProgressProvider } from '../../../contexts/ProgressContext';
import { InnovationDataProvider } from '../../../contexts/InnovationDataContext';
import { GlassStage, type GlassProps } from './GlassStage';
import { DEMO_PROFILE } from './demoProfile';

const SpacedRepetitionTimetable = React.lazy(() => import('../../SpacedRepetitionTimetable'));

export const PLANNER_MODES_LIVE: { id: string; label: string }[] = [];

const PlannerGlass: React.FC<GlassProps> = ({ active, height = 720, logicalWidth }) => (
  <GlassStage active={active} height={height} logicalWidth={logicalWidth}>
    {active && (
      <ProgressProvider>
      <InnovationDataProvider uid={undefined} subjectProfile={DEMO_PROFILE}>
      <Suspense fallback={null}>
        <div className="landing-glass-pad">
          <SpacedRepetitionTimetable profile={DEMO_PROFILE} uid={undefined} onOpenSettings={() => undefined} />
        </div>
      </Suspense>
      </InnovationDataProvider>
      </ProgressProvider>
    )}
  </GlassStage>
);

export default PlannerGlass;
