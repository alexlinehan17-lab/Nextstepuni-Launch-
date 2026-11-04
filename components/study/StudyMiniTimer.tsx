/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The minimised study timer: it keeps counting while a student uses Mark Bank,
 * Paper Trail, the Topic Atlas or anything else in the app, and opens the study
 * room again on tap. Same ink palette as the room. Docked bottom-right, above
 * the phone tab bar.
 */

import React from 'react';
import { createPortal } from 'react-dom';
import { Maximize2, Pause, Play } from 'lucide-react';
import { useSharedStudySession } from '../../contexts/StudySessionContext';
import { formatTime } from './StudySessionTimer';
import './study-mini-timer.css';

export default function StudyMiniTimer({ onOpen, view }: { onOpen: () => void; view: string }) {
  const session = useSharedStudySession();
  if (!session || session.phase === 'idle' || typeof document === 'undefined') return null;
  const done = session.phase === 'complete';
  const paused = session.phase === 'paused';
  const ranOut = done && !session.openEnded && session.elapsedSeconds >= session.totalDuration;
  const shown = session.openEnded ? session.elapsedSeconds : Math.max(0, session.totalDuration - session.elapsedSeconds);
  const progress = session.openEnded || !session.totalDuration ? 0 : Math.min(100, session.elapsedSeconds / session.totalDuration * 100);
  const status = done ? (ranOut ? 'Time’s up' : 'Ready to log') : paused ? 'Paused' : session.openEnded ? 'Studying' : 'Remaining';
  const spoken = done ? status : `${formatTime(shown)} ${session.openEnded ? 'studied' : 'remaining'}${paused ? ', paused' : ''}`;

  return createPortal(
    <aside className="study-mini" data-state={done ? 'done' : paused ? 'paused' : 'running'} data-view={view} aria-label="Study timer">
      <button type="button" className="study-mini-open" onClick={onOpen} aria-label={`Open the study timer: ${session.subject}, ${spoken}`}>
        <i className="study-mini-dot" aria-hidden="true" />
        <span className="study-mini-label"><strong>{session.subject}</strong><small>{status}</small></span>
        {!done && <span className="study-mini-digits" aria-hidden="true">{formatTime(shown)}</span>}
        <Maximize2 className="study-mini-expand" size={15} aria-hidden="true" />
      </button>
      {!done && (
        <button type="button" className="study-mini-toggle" onClick={paused ? session.resumeSession : session.pauseSession} aria-label={paused ? 'Resume study session' : 'Pause study session'}>
          {paused ? <Play size={16} fill="currentColor" aria-hidden="true" /> : <Pause size={16} aria-hidden="true" />}
        </button>
      )}
      {ranOut && <button type="button" className="study-mini-action" onClick={() => session.extendSession(5)} aria-label="Keep going for 5 more minutes">+5 min</button>}
      {done && <button type="button" className="study-mini-action study-mini-log" onClick={onOpen}>Log it</button>}
      {progress > 0 && <i className="study-mini-progress" style={{ width: `${progress}%` }} aria-hidden="true" />}
    </aside>,
    document.body,
  );
}
