/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A live, non-interactive glimpse of a real surface for the chapter frames —
 * the same components the playground runs, mounted only while on screen and
 * shown behind a pointer-events shield so the reader looks but does not poke
 * (the chapter's "Try it in the playground" link is the way in).
 */

import React, { useRef } from 'react';
import { useInView } from 'framer-motion';
import type { ChapterId } from '../copy';
import MarkBank from '../../MarkBank/MarkBank';
import ReviseByTopic from '../../PaperTrail/ReviseByTopic';
import CommandWordReflex from '../../CommandWordReflex';
import { ProgressProvider } from '../../../contexts/ProgressContext';
import { GlassStage } from './GlassStage';

const BIOLOGY = [{ id: 'biology', label: 'Biology' }];
const MB_SUBJECTS = [{ subjectName: 'Biology', level: 'higher' }];

export const hasGlimpse = (id: ChapterId): boolean => id === 'markbank' || id === 'atlas' || id === 'launchpad';

const Surface: React.FC<{ id: ChapterId; active: boolean }> = ({ id, active }) => {
  if (!active) return null;
  if (id === 'markbank') return <MarkBank uid={undefined} studentSubjects={MB_SUBJECTS} />;
  if (id === 'atlas') {
    return (
      <ReviseByTopic
        subjects={BIOLOGY}
        mineIds={['biology']}
        uid={undefined}
        subjectLabel={() => 'Biology'}
        restore={{ subjectId: 'biology', subtopicId: 'biology-higher-old-course-ecology' }}
        onOpenQuestion={() => undefined}
        onBack={() => undefined}
      />
    );
  }
  if (id === 'launchpad') {
    return (
      <ProgressProvider>
        <CommandWordReflex uid={undefined} studentSubjects={['Business', 'Biology']} studentCycle="leaving-cert" />
      </ProgressProvider>
    );
  }
  return null;
};

export const LiveGlimpse: React.FC<{ id: ChapterId; height?: number }> = ({ id, height = 640 }) => {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { amount: 0.15, margin: '200px 0px' as never });
  return (
    <div ref={ref} aria-hidden="true" style={{ position: 'relative', pointerEvents: 'none', userSelect: 'none' }}>
      <GlassStage active={inView} height={height} logicalWidth={820}>
        <div className="landing-glass-pad">
          <Surface id={id} active={inView} />
        </div>
      </GlassStage>
    </div>
  );
};

export default LiveGlimpse;
