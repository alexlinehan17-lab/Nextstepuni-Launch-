/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The real Command-Word Reflex (components/CommandWordReflex), signed out.
 * "My Subjects" shows the sample student's seven and "All Subjects" the lot;
 * Biology and Mathematics are open in both, the rest locked. Progress runs
 * through ProgressProvider, which idles without an account.
 */

import React from 'react';
import CommandWordReflex from '../../CommandWordReflex';
import { ProgressProvider } from '../../../contexts/ProgressContext';
import { commandSubjects } from '../../../commandWordData';
import { displayName } from '../../shared/subjectNames';
import { GlassStage, type GlassLocks, type GlassProps } from './GlassStage';
import { DEMO_SUBJECT_NAMES, isFree } from './demoProfile';

export const REFLEX_SUBJECTS_LIVE: { id: string; label: string }[] = [];

const REFLEX_NAMES = new Set(commandSubjects().map(s => displayName(s.subjectLabel)));

const LOCKS: GlassLocks = {
  test: (name, el) => REFLEX_NAMES.has(name) && el.matches('div.grid > button') && !isFree(name),
};

const ReflexGlass: React.FC<GlassProps> = ({ active, height = 640, logicalWidth }) => (
  <GlassStage active={active} height={height} logicalWidth={logicalWidth} locks={LOCKS} canSelectSubject={isFree}>
    {active && (
      <div className="landing-glass-pad">
        <ProgressProvider>
          <CommandWordReflex uid={undefined} studentSubjects={[...DEMO_SUBJECT_NAMES]} studentCycle="leaving-cert" />
        </ProgressProvider>
      </div>
    )}
  </GlassStage>
);

export default ReflexGlass;
