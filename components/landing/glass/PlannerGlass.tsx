/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Planner & Study: the real spaced-repetition timetable
 * (components/SpacedRepetitionTimetable) built for the sample sixth-year —
 * seven subjects, Sundays off, exams from 2 June 2027 — and, from any of
 * today's blocks, the real study screen (components/study/StudySessionView)
 * with a way back to the week. The study screen runs as the demo student,
 * whose progress hooks stay on-device; no uid reaches Firestore.
 */

import React, { Suspense, useMemo, useState } from 'react';
import { ProgressProvider } from '../../../contexts/ProgressContext';
import { InnovationDataProvider } from '../../../contexts/InnovationDataContext';
import { createDemoModuleProgress, createDemoStudentSession } from '../../../data/devStudent';
import { ALL_COURSES } from '../../../courseData';
import { filterCoursesForStudent } from '../../../utils/courseVisibility';
import type { TimetableBlockInfo } from '../../SpacedRepetitionTimetable';
import { GlassStage, type GlassProps } from './GlassStage';
import { DEMO_PROFILE } from './demoProfile';

const SpacedRepetitionTimetable = React.lazy(() => import('../../SpacedRepetitionTimetable'));
const StudySessionView = React.lazy(() => import('../../study/StudySessionView'));

export const PLANNER_MODES_LIVE: { id: string; label: string }[] = [];

const NO_STREAK = { currentStreak: 0, lastActiveDate: '', longestStreak: 0 };
/** First-run guides (the Journey Points explainer) stay closed in the window; they belong to a real first session. */
const GUIDES_SEEN: Record<string, string> = { 'points-explainer': 'landing', 'study-session-intro': 'landing' };

const PlannerGlass: React.FC<GlassProps> = ({ active, height = 720, logicalWidth }) => {
  const [block, setBlock] = useState<TimetableBlockInfo | null>(null);
  const demoUser = useMemo(() => createDemoStudentSession(), []);
  const progress = useMemo(() => createDemoModuleProgress(DEMO_PROFILE), []);
  const courses = useMemo(() => filterCoursesForStudent(ALL_COURSES, demoUser.curriculumLevel, DEMO_PROFILE), [demoUser]);
  return (
    <GlassStage active={active} height={height} logicalWidth={logicalWidth}>
      {active && (
        <ProgressProvider>
          <InnovationDataProvider uid={undefined} subjectProfile={DEMO_PROFILE}>
            <Suspense fallback={null}>
              <div className="landing-glass-pad landing-glass-pad--airy">
                {block ? (
                  <StudySessionView
                    user={demoUser}
                    studentProfile={DEMO_PROFILE}
                    userProgress={progress}
                    allCourses={courses}
                    pointsReload={() => undefined}
                    streak={NO_STREAK}
                    onBack={() => setBlock(null)}
                    timetableBlock={block}
                    onTimetableBlockComplete={() => setBlock(null)}
                    dismissedGuides={GUIDES_SEEN}
                  />
                ) : (
                  <SpacedRepetitionTimetable profile={DEMO_PROFILE} uid={undefined} onOpenSettings={() => undefined} onStudyNow={setBlock} />
                )}
              </div>
            </Suspense>
          </InnovationDataProvider>
        </ProgressProvider>
      )}
    </GlassStage>
  );
};

export default PlannerGlass;
