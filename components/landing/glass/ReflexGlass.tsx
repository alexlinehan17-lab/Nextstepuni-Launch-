/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The real Command-Word Reflex (components/CommandWordReflex), signed out.
 * It reads progress through ProgressProvider, which idles without an
 * account: nothing is stored, the visitor's taps live in React state.
 */

import React from 'react';
import CommandWordReflex from '../../CommandWordReflex';
import { ProgressProvider } from '../../../contexts/ProgressContext';
import { GlassStage } from './GlassStage';

export const REFLEX_SUBJECTS_LIVE: { id: string; label: string }[] = [
  { id: 'Business', label: 'Business' },
  { id: 'Biology', label: 'Biology' },
  { id: 'Geography', label: 'Geography' },
  { id: 'English', label: 'English' },
];

const ReflexGlass: React.FC<{ sub: string; active: boolean }> = ({ sub, active }) => (
  <GlassStage active={active} height={640}>
    {active && (
      <div className="landing-glass-pad">
        <ProgressProvider>
          <CommandWordReflex key={sub} uid={undefined} studentSubjects={[sub]} studentCycle="leaving-cert" />
        </ProgressProvider>
      </div>
    )}
  </GlassStage>
);

export default ReflexGlass;
