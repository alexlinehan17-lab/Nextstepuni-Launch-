/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The real Command-Word Reflex (components/CommandWordReflex), signed out.
 * "My Subjects" shows the sample student's six, all locked; under
 * "All Subjects" Biology, Economics and Mathematics are open. Progress runs
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

/** Which scope the tile picker is showing, read off its toggle; null once a subject is open. */
const scopeOf = (root: Element | null): 'mine' | 'all' | null => {
  const toggles = root ? Array.from(root.querySelectorAll<HTMLButtonElement>('div.p-1.rounded-xl > button')) : [];
  const scopes = toggles.filter(b => /^(My|All) Subjects$/.test(b.textContent?.trim() ?? ''));
  const on = scopes.find(b => b.classList.contains('bg-white'));
  if (!on) return null;
  return on.textContent?.trim() === 'All Subjects' ? 'all' : 'mine';
};

const LOCKS: GlassLocks = {
  test: (name, el) => {
    if (!REFLEX_NAMES.has(name) || !el.matches('div.grid > button')) return false;
    const scope = scopeOf(el.closest('.landing-glass'));
    return scope === 'mine' || (scope === 'all' && !isFree(name));
  },
};

const ReflexGlass: React.FC<GlassProps> = ({ active, height = 640, logicalWidth }) => (
  <GlassStage active={active} height={height} logicalWidth={logicalWidth} locks={LOCKS}>
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
