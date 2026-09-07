/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The real Topic Atlas feed (components/PaperTrail/ReviseByTopic), opened
 * straight on one Biology topic: real printed-question crops from the SEC
 * papers, each with its marking scheme one tap away. No providers, no
 * sign-in — the papers are world-readable and the scheme crops render
 * on the fly. Mounted only while on screen: each card pulls a real PDF.
 */

import React from 'react';
import ReviseByTopic from '../../PaperTrail/ReviseByTopic';
import { APP_URL } from '../theme';
import { GlassStage } from './GlassStage';

export const ATLAS_TOPICS_LIVE: { id: string; label: string }[] = [
  { id: 'biology-higher-old-course-genetics-dna-evolution', label: 'Genetics & DNA' },
  { id: 'biology-higher-old-course-ecology', label: 'Ecology' },
  { id: 'biology-higher-old-course-cell-metabolism-enzymes', label: 'Enzymes' },
  { id: 'biology-higher-old-course-food-food-tests', label: 'Food tests' },
  { id: 'biology-higher-new-course-31-ecology-ecosystems-and-biodiversity', label: '3.1 Ecosystems (new spec)' },
];

const SUBJECTS = [{ id: 'biology', label: 'Biology' }];
const AUTO = [{ text: 'Show the marking scheme', hold: 5200, before: 2600 }];

const AtlasGlass: React.FC<{ sub: string; active: boolean }> = ({ sub, active }) => (
  <GlassStage active={active} auto={AUTO} height={700}>
    {active && (
      <div className="landing-glass-pad">
        <ReviseByTopic
          key={sub}
          subjects={SUBJECTS}
          mineIds={['biology']}
          uid={undefined}
          subjectLabel={() => 'Biology'}
          restore={{ subjectId: 'biology', subtopicId: sub }}
          onOpenQuestion={() => { window.location.href = APP_URL; }}
          onBack={() => undefined}
        />
      </div>
    )}
  </GlassStage>
);

export default AtlasGlass;
