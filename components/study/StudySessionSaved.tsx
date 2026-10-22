/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * After a session is saved: the Journey Points it earned, and a clear way to
 * spend them on the island — studying is what builds it (student feedback,
 * 12 Oct 2026: "you get it as a reward after you study").
 */

import React from 'react';
import { ArrowUpRight } from 'lucide-react';
import CrewIllustration from '../CrewIllustration';
import { formatStudyTime } from '../../utils/studyTime';
import './study-crew.css';

interface Props {
  subject: string;
  seconds: number;
  points: number;
  character?: string;
  onIsland?: () => void;
  onStudyAgain: () => void;
}

export default function StudySessionSaved({ subject, seconds, points, character, onIsland, onStudyAgain }: Props) {
  return (
    <section className="study-saved" aria-labelledby="study-saved-title">
      <CrewIllustration character={character} />
      <p className="study-crew-eyebrow">Session saved</p>
      <h1 id="study-saved-title">+{points} JP</h1>
      <p className="study-crew-intro">{formatStudyTime(seconds)} of {subject} is on the record. Your Journey Points are ready to spend.</p>
      <div className="study-saved-actions">
        {onIsland && (
          <button type="button" className="crew-primary" onClick={onIsland}>
            Spend them on your island <ArrowUpRight size={20} aria-hidden="true" />
          </button>
        )}
        <button type="button" className="crew-link" onClick={onStudyAgain}>Back to the study room</button>
      </div>
    </section>
  );
}
