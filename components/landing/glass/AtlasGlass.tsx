/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The real Topic Atlas feed (components/PaperTrail/ReviseByTopic), opened
 * straight on one Biology topic: real printed-question crops from the SEC
 * papers, each with its marking scheme one tap away. Back out and "My
 * subjects" holds the sample student's seven, Biology and Mathematics open
 * and the other five locked; the "All subjects" scope and each card's
 * "Full paper" link are locked too. No providers, no
 * sign-in — the papers are world-readable and the scheme crops render
 * on the fly. Mounted only while on screen: each card pulls a real PDF.
 */

import React from 'react';
import ReviseByTopic from '../../PaperTrail/ReviseByTopic';
import { APP_URL } from '../theme';
import { GlassStage, type GlassLocks, type GlassProps } from './GlassStage';
import { DEMO_ATLAS_SUBJECTS, DEMO_SUBJECT_NAMES, isFree } from './demoProfile';

export const ATLAS_TOPICS_LIVE: { id: string; label: string }[] = [
  { id: 'biology-higher-old-course-genetics-dna-evolution', label: 'Genetics & DNA' },
  { id: 'biology-higher-old-course-ecology', label: 'Ecology' },
  { id: 'biology-higher-old-course-cell-metabolism-enzymes', label: 'Enzymes' },
  { id: 'biology-higher-old-course-food-food-tests', label: 'Food tests' },
  { id: 'biology-higher-new-course-31-ecology-ecosystems-and-biodiversity', label: '3.1 Ecosystems (new spec)' },
];

const SUBJECTS = DEMO_ATLAS_SUBJECTS;
const MINE_IDS = SUBJECTS.map(s => s.id);
const LABEL = new Map(SUBJECTS.map(s => [s.id, s.label]));
const AUTO = [{ text: 'Show the marking scheme', hold: 5200, before: 2600 }];
const LOCKED_NAMES = new Set(DEMO_SUBJECT_NAMES.filter(n => !isFree(n)));
/**
 * Subject tiles carry an aria-label of "Name — 1,234 questions across …"; the
 * name is what we match. The "All subjects" that is locked is the scope
 * toggle, never the back arrow that leads to "My subjects".
 */
const LOCKS: GlassLocks = {
  nameOf: el => el.getAttribute('aria-label')?.split(' — ')[0]?.trim() || undefined,
  test: (name, el) => {
    if (name === 'All subjects') return !!el.closest('[aria-label="Subject scope"]');
    if (name === 'Full paper') return true; // opens the app's viewer, which needs an account
    return LOCKED_NAMES.has(name) && el.matches('button[aria-label]');
  },
};

const AtlasGlass: React.FC<GlassProps> = ({ sub, active, height = 700, logicalWidth }) => (
  <GlassStage active={active} auto={AUTO} height={height} logicalWidth={logicalWidth} locks={LOCKS}>
    {active && (
      <div className="landing-glass-pad">
        <ReviseByTopic
          key={sub}
          subjects={SUBJECTS}
          mineIds={MINE_IDS}
          uid={undefined}
          subjectLabel={id => LABEL.get(id) ?? id}
          restore={{ subjectId: 'biology', subtopicId: sub }}
          onOpenQuestion={() => { window.location.href = APP_URL; }}
          onBack={() => undefined}
        />
      </div>
    )}
  </GlassStage>
);

export default AtlasGlass;
