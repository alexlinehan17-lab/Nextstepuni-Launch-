/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * After a session is saved: the Journey Points it earned, and a clear way to
 * spend them on the island — studying is what builds it (student feedback,
 * 12 Oct 2026: "you get it as a reward after you study"). A Kobra paper card
 * (approved review, 25 Oct 2026): the points as one big serif number.
 * Styles: study-post-session.css.
 */

import React from 'react';
import { ArrowUpRight } from 'lucide-react';
import KobraScope, { Button } from '../approved-ui-runtime';
import CrewIllustration from '../CrewIllustration';
import { formatStudyTime } from '../../utils/studyTime';
import './study-post-session.css';

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
    <KobraScope className="nsu-post-session">
      <div className="sps-page sps-solo">
        <section className="sps-card sps-saved nsu-paper-card" aria-labelledby="study-saved-title">
          <div className="sps-saved-top">
            <div>
              <p className="sps-eyebrow">Session saved</p>
              <h1 id="study-saved-title" className="sps-points"><em>+{points}</em> <small>JP</small></h1>
            </div>
            <span className="sps-art"><CrewIllustration character={character} /></span>
          </div>
          <p className="sps-lede">{formatStudyTime(seconds)} of {subject} is on the record. Your Journey Points are ready to spend.</p>
          <div className="sps-actions">
            {onIsland && (
              <Button className="sps-primary" onClick={onIsland}>
                Spend them on your island <ArrowUpRight aria-hidden="true" />
              </Button>
            )}
            <Button variant="ghost" className="sps-quiet" onClick={onStudyAgain}>Back to the study room</Button>
          </div>
        </section>
      </div>
    </KobraScope>
  );
}
