/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The countdown has run out: keep going on the same session, or finish and log
 * it. Asked for by a student who needed five more minutes for an Irish oral and
 * had to start a whole new session (feedback, 5 Oct 2026).
 */

import React from 'react';
import { ArrowRight } from 'lucide-react';
import { SESSION_EXTENSION_MINUTES, STUDY_SESSION_POINTS } from '../../studySessionData';
import { formatStudyTime } from '../../utils/studyTime';
import './study-session.css';

interface Props {
  subject: string;
  elapsedSeconds: number;
  extendedMinutes: number;
  /** JP already earned for finishing added time on this session. */
  extensionBonus: number;
  /** JP this session will earn on saving, before any debrief. */
  sessionPoints: number;
  onKeepGoing: (minutes: number) => void;
  onFinish: () => void;
}

export default function StudyTimeUp({ subject, elapsedSeconds, extendedMinutes, extensionBonus, sessionPoints, onKeepGoing, onFinish }: Props) {
  const keptGoing = extendedMinutes > 0;
  return (
    // The same full-screen room as the running timer.
    <div className="ss-timer-view">
    <section className="ss-timer-content ss-room-ink ss-timeup" aria-labelledby="ss-timeup-title">
      <header className="ss-timer-navigation"><span className="ss-eyebrow">The study room</span></header>
      <main className="ss-timer-main">
        <p className="ss-timer-subject"><i aria-hidden="true" />{subject}</p>
        <h1 id="ss-timeup-title" className="ss-timeup-title">{keptGoing ? 'You kept going.' : 'Time’s up.'}</h1>
        <p className="ss-timeup-summary">
          {formatStudyTime(elapsedSeconds)} studied · {sessionPoints} JP on saving
          {extensionBonus > 0 && <><br /><strong>+{extensionBonus} JP for finishing your extra time</strong></>}
        </p>
        <div className="ss-timeup-choices" role="group" aria-labelledby="ss-keep-going">
          <p id="ss-keep-going" className="ss-timer-status">Keep going on the same session</p>
          <div>
            {SESSION_EXTENSION_MINUTES.map(minutes => (
              <button key={minutes} type="button" className="ss-timeup-extend" onClick={() => onKeepGoing(minutes)} aria-label={`Keep going for ${minutes} more minutes`}>
                +{minutes} min
              </button>
            ))}
          </div>
          <p className="ss-timeup-note">The extra minutes count towards your JP. Finish them and earn +{STUDY_SESSION_POINTS.EXTENSION_COMPLETED} JP.</p>
        </div>
        <button type="button" className="ss-timer-pause ss-timeup-finish" onClick={onFinish}>
          Finish and log <ArrowRight size={18} aria-hidden="true" />
        </button>
      </main>
    </section>
    </div>
  );
}
