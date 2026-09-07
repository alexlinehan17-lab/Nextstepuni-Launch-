/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The real Paper Trail (components/PaperTrail), signed out, with the sample
 * student's seven subjects under "My subjects". Biology and Mathematics are
 * open — the cursor opens Mathematics, 200 of whose 222 papers carry answer
 * maps; the other five show with a lock, as do the "All subjects" switches.
 */

import React, { Suspense } from 'react';
import { ProgressProvider } from '../../../contexts/ProgressContext';
import { GlassStage, type AutoStep, type GlassLocks, type GlassProps } from './GlassStage';
import { DEMO_LEVELS, DEMO_SUBJECT_NAMES, PAPER_TRAIL_OPEN_SUBJECT, isFree } from './demoProfile';
import { openDemo } from './demoEvent';

const PaperTrail = React.lazy(() => import('../../PaperTrail'));

export const PAPERTRAIL_MODES_LIVE: { id: string; label: string }[] = [];

/** Search finds every subject; only Biology and Mathematics results open. */
const searchSubject = (el: HTMLElement): string | undefined =>
  el.matches('.pt-search-results > button') ? el.querySelector('span')?.textContent?.replace(/ · LCA$/, '').trim() || undefined : undefined;
const LOCKS: GlassLocks = {
  names: [...DEMO_SUBJECT_NAMES.filter(s => !isFree(s)), 'All subjects', 'Browse all subjects'],
  nameOf: el => el.querySelector('.pt-subject-name')?.textContent?.trim() || searchSubject(el) || undefined,
  test: (name, el) => {
    if (el.matches('.pt-search-results > button')) return !isFree(name);
    if (el.matches('.pt-continue')) {
      const last = el.closest('.pt-resume')?.querySelector('.pt-resume-name')?.textContent?.split(' · ')[0]?.trim() ?? '';
      return !isFree(last);
    }
    return false;
  },
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
