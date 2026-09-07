/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A live, non-interactive glimpse of a real surface for the chapter frames —
 * the same glasses the playground runs, mounted only while on screen and
 * shown behind a pointer-events shield so the reader looks but does not poke
 * (the chapter's "Try it in the playground" link is the way in). The
 * scripted cursors still run, so the glimpses move on their own.
 */

import React, { useRef } from 'react';
import { useInView } from 'framer-motion';
import type { ChapterId } from '../copy';
import type { GlassProps } from './GlassStage';
import MarkBankGlass from './MarkBankGlass';
import PaperTrailGlass from './PaperTrailGlass';
import AtlasGlass from './AtlasGlass';
import PlannerGlass from './PlannerGlass';
import FutureFinderGlass from './FutureFinderGlass';

const GLIMPSE: Partial<Record<ChapterId, { Glass: React.FC<GlassProps>; sub: string; height: number }>> = {
  markbank: { Glass: MarkBankGlass, sub: 'Biology', height: 640 },
  papertrail: { Glass: PaperTrailGlass, sub: '', height: 640 },
  atlas: { Glass: AtlasGlass, sub: 'biology-higher-old-course-ecology', height: 640 },
  planner: { Glass: PlannerGlass, sub: '', height: 640 },
  launchpad: { Glass: FutureFinderGlass, sub: '', height: 640 },
};

export const hasGlimpse = (id: ChapterId): boolean => id in GLIMPSE;

export const LiveGlimpse: React.FC<{ id: ChapterId }> = ({ id }) => {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { amount: 0.15, margin: '200px 0px' as never });
  const g = GLIMPSE[id];
  if (!g) return null;
  return (
    <div ref={ref} aria-hidden="true" style={{ position: 'relative', pointerEvents: 'none', userSelect: 'none' }}>
      <g.Glass sub={g.sub} active={inView} height={g.height} logicalWidth={820} />
    </div>
  );
};

export default LiveGlimpse;
