import React from 'react';
import { Check, Pause, Play } from 'lucide-react';
import { MotionDiv, useReducedMotion } from '../Motion';
import { PROMPT_AUTO_DISMISS_SECONDS, getSubjectHex } from '../../studySessionData';
import { TopBar } from '../ui/Bars';
import { Button } from '../ui/Button';
import StudyRule, { roomMarks } from './StudyRule';
import './study-session.css';
import './study-room.css';
import type { StudyTimerAppearance } from '../../hooks/useStudyTimerAppearance';
import { useNativeStatusBarAppearance } from '../../hooks/useNativeStatusBarAppearance';

export interface StudySessionTimerProps {
  appearance?: StudyTimerAppearance;
  subject: string;
  subjectColor: string;
  type: string;
  totalSeconds: number;
  elapsedSeconds: number;
  /** The original plan; added "Keep going" time is shown on top of it. */
  plannedSeconds?: number;
  extendedMinutes?: number;
  /** Stopwatch session: counts up and is finished by the student. */
  openEnded?: boolean;
  canFinish?: boolean;
  onFinish?: () => void;
  /** Leave the room while the timer keeps counting. */
  onMinimise?: () => void;
  paused: boolean;
  onLeave: () => void;
  onTogglePause: (event: React.MouseEvent<HTMLButtonElement>) => void;
  soundControl?: React.ReactNode;
  /** The one-time "Notify me when time's up" offer, under the controls. */
  notifyOffer?: React.ReactNode;
  prompt: { strategyName: string; prompt: string } | null;
  onCompletePrompt: () => void;
  onSkipPrompt: () => void;
}

export const formatTime = (seconds: number) => {
  const whole = Math.max(0, Math.floor(seconds));
  const clock = `${Math.floor((whole % 3600) / 60).toString().padStart(2, '0')}:${(whole % 60).toString().padStart(2, '0')}`;
  // Countdowns stay MM:SS (the longest preset is 180 min); an open-ended session can pass an hour.
  return whole >= 3600 ? `${Math.floor(whole / 3600)}:${clock}` : `${Math.floor(whole / 60).toString().padStart(2, '0')}:${(whole % 60).toString().padStart(2, '0')}`;
};

export default function StudySessionTimer({ appearance = 'ink', subject, subjectColor, type, totalSeconds, elapsedSeconds, plannedSeconds, extendedMinutes = 0, openEnded = false, canFinish = false, onFinish, onMinimise, paused, onLeave, onTogglePause, soundControl, notifyOffer, prompt, onCompletePrompt, onSkipPrompt }: StudySessionTimerProps) {
  useNativeStatusBarAppearance(paused ? 'light' : appearance === 'ink' ? 'dark' : 'light');
  const remaining = Math.max(0, totalSeconds - elapsedSeconds);
  // An open-ended session has no end to measure progress against.
  const progress = !openEnded && totalSeconds > 0 ? Math.min(100, elapsedSeconds / totalSeconds * 100) : 0;
  const shown = openEnded ? elapsedSeconds : remaining;
  const plannedMinutes = Math.ceil((plannedSeconds ?? totalSeconds) / 60);
  const length = openEnded ? 'Open-ended' : extendedMinutes > 0 ? `${plannedMinutes} + ${extendedMinutes} min` : `${Math.ceil(totalSeconds / 60)} min`;
  const reduceMotion = useReducedMotion();
  const subjectHex = getSubjectHex(subject);
  // Paint the landscape with pale tints so the dark numerals remain legible
  // even for Mathematics, whose established subject colour is near black.
  return (
    <div className={`ss-timer-content ss-room-${appearance} ${paused ? 'ss-room-paused' : ''} ${prompt ? 'ss-room-coaching' : ''}`} style={{ '--ss-subject': subjectColor, '--ss-landscape': subjectHex, '--ss-session-progress': `${progress}%` } as React.CSSProperties}>
      {appearance === 'layers' ? <div className="ss-colour-landscape" aria-hidden="true">{[0, 1, 2, 3, 4].map(band => <i key={band} style={{ '--band': band } as React.CSSProperties} />)}</div> : null}
      {/* The one bar (c-study-pause, agreed 24 Nov 2026): Close at the left puts
          the room away while the timer runs (or leaves, where the room cannot be
          put away), the sound at the right. Ending is a choice on the pause screen. */}
      <div className="ss-room-barwrap" data-study-arrive>
        <TopBar className="ss-room-bar" title="The Study Room" action={soundControl}
          leave={{ kind: 'close', onPress: onMinimise ?? onLeave, label: onMinimise ? 'Close the room. Your session keeps running.' : 'Leave study session' }} />
      </div>
      <main className="ss-timer-main">
        <p className="ss-timer-subject" data-study-arrive>{subject}</p>
        <p className="ss-timer-type" data-study-arrive>{type} · {length}</p>
        <p className="ss-timer-digits" data-study-arrive role="timer" aria-label={openEnded ? `${formatTime(shown)} studied` : `${formatTime(shown)} remaining`}>{[...formatTime(shown)].map((character, index) => <span key={index} className={character === ':' ? 'ss-timer-colon' : undefined}>{character}</span>)}</p>
        <p className="ss-timer-status" data-study-arrive>{paused ? 'Session paused' : openEnded ? 'Time studied' : extendedMinutes > 0 ? 'Extra time remaining' : 'Time remaining'}</p>
        <div className="ss-timer-actions" data-study-arrive>
          <Button kind="main" className="ss-timer-pause" onClick={onTogglePause} aria-label={paused ? 'Resume study session' : 'Pause study session'}>{paused ? <Play size={20} strokeWidth={1.75} aria-hidden="true" /> : <Pause size={20} strokeWidth={1.75} aria-hidden="true" />}{paused ? 'Resume' : 'Pause'}</Button>
          {openEnded && onFinish && <Button className="ss-timer-finish" onClick={onFinish} unavailable={canFinish ? undefined : 'Finish after 5 minutes'}><Check size={20} strokeWidth={1.75} aria-hidden="true" />Finish</Button>}
        </div>
        {notifyOffer}
      </main>
      {prompt && <section className="ss-coaching" aria-label="Study strategy prompt" key={prompt.prompt}>
        <div className="ss-coaching-heading"><p className="ss-eyebrow">Put it into practice</p><span>{prompt.strategyName}</span></div>
        <p className="ss-coaching-prompt">{prompt.prompt}</p>
        <div className="ss-coaching-actions"><Button onClick={onCompletePrompt}>Done</Button><Button onClick={onSkipPrompt}>Skip</Button></div>
        {!reduceMotion && <MotionDiv className="ss-prompt-countdown" initial={{ scaleX: 1 }} animate={{ scaleX: 0 }} transition={{ duration: PROMPT_AUTO_DISMISS_SECONDS, ease: 'linear' }} />}
      </section>}
      <footer className="ss-timer-footer"><div className="ss-timer-track" role="progressbar" aria-label="Session progress" aria-valuenow={Math.round(progress)} aria-valuemin={0} aria-valuemax={100}><StudyRule size="room" marks={roomMarks(totalSeconds, elapsedSeconds, openEnded)} /></div><div><span>{formatTime(elapsedSeconds)} elapsed</span><span>{openEnded ? 'No set end' : `${formatTime(totalSeconds)} planned`}</span></div></footer>
    </div>
  );
}
