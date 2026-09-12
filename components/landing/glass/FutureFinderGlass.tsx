/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The real Future Finder (components/FutureFinderRevamped) for a sample
 * student who has already finished the quiz: the results list, with three
 * courses queued for comparison, and the scripted cursor pressing Compare.
 * The finished state is seeded on-device under the demo student's key, which
 * is the one uid whose progress never touches Firestore.
 */

import React, { useEffect, useState } from 'react';
import { ArrowUpRight, ChevronDown } from 'lucide-react';
import FutureFinderRevamped, { computeAnalysis } from '../../FutureFinderRevamped';
import { RIASEC_ITEMS, VALUE_ITEMS } from '../../futureFinderRiasecItems';
import { computeTargetCAOPoints, RECOMMENDATION_RANKING_VERSION } from '../../futureFinderRecommendation';
import type { FutureFinderRevampedState } from '../../../hooks/useFutureFinderRevamped';
import { ProgressProvider } from '../../../contexts/ProgressContext';
import { DEMO_STUDENT_UID } from '../../../data/devStudent';
import { GlassStage, type AutoStep, type GlassProps } from './GlassStage';
import { DEMO_PROFILE } from './demoProfile';
import { APP_URL } from '../theme';

export const FUTUREFINDER_MODES_LIVE: { id: string; label: string }[] = [];

/** An investigative, hands-on profile — the kind that ranks science and engineering courses. */
const INTEREST: Record<string, number> = { I: 5, R: 4, C: 3, S: 3, A: 2, E: 2 };
const VALUES: Record<string, number> = { achievement: 5, independence: 4, recognition: 3, relationships: 3, 'working-conditions': 3, support: 2 };
const KEY = `nextstepuni:future-finder:v1:${DEMO_STUDENT_UID}`;

export const seedFutureFinder = (): void => {
  const responses: Record<string, number> = {};
  RIASEC_ITEMS.forEach((it, i) => { responses[it.id] = Math.max(1, Math.min(5, INTEREST[it.scale] + (i % 4 === 0 ? -1 : 0))); });
  const valueResponses: Record<string, number> = {};
  VALUE_ITEMS.forEach(v => { valueResponses[v.id] = VALUES[v.value] ?? 3; });
  const points = computeTargetCAOPoints(DEMO_PROFILE);
  const ranked = computeAnalysis(responses, valueResponses, points, DEMO_PROFILE.subjects.map(s => s.subjectName));
  const top = ranked.shown.slice(0, 10).map(x => x.course.code);
  const now = new Date().toISOString();
  const state: FutureFinderRevampedState = {
    rankingVersion: RECOMMENDATION_RANKING_VERSION,
    length: 'full',
    responses,
    valueResponses,
    picks: [],
    topMatches: top,
    compareCodes: top.slice(0, 3),
    completedAt: now,
    updatedAt: now,
  };
  try { localStorage.setItem(KEY, JSON.stringify(state)); } catch { /* storage may be unavailable */ }
};

/** Compare the three queued courses, sit with the page, come back, go again. */
const AUTO: AutoStep[] = [
  { text: 'Compare', before: 2400, hold: 12000, then: 'top' },
  { text: 'Back to results', before: 400, hold: 5000, then: 'top' },
];

export function SampleResultsSign() {
  const [open, setOpen] = useState(false);
  return <aside className="landing-results-sign">
    <button type="button" aria-expanded={open} aria-controls="sample-results-note" onClick={() => setOpen(value => !value)}>
      <span><small>Take a look around</small><strong>This is what a results screen looks like!</strong><span className="landing-results-sign-hint">A sample student. Plenty to explore. <ChevronDown size={17} aria-hidden="true" /></span></span>
      <img src="/assets/landing/starguy-512.png" alt="" width="86" height="108" />
    </button>
    {open && <div id="sample-results-note"><p>We’ve filled this one in for a sample student. Tap a course, try the filters or compare a few favourites. Your own interests and choices will shape your results.</p><a href={APP_URL}>Find your own direction <ArrowUpRight size={16} aria-hidden="true" /></a></div>}
  </aside>;
}

const FutureFinderGlass: React.FC<GlassProps> = ({ active, height = 720, logicalWidth }) => {
  const [seeded, setSeeded] = useState(false);
  useEffect(() => { seedFutureFinder(); setSeeded(true); }, []);
  return (
    <GlassStage active={active} height={height} logicalWidth={logicalWidth} auto={AUTO}>
      {active && seeded && (
        <ProgressProvider>
          <div className="landing-glass-pad landing-glass-pad--airy">
            <SampleResultsSign />
            <FutureFinderRevamped uid={DEMO_STUDENT_UID} profile={DEMO_PROFILE} />
          </div>
        </ProgressProvider>
      )}
    </GlassStage>
  );
};

export default FutureFinderGlass;
