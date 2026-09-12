import React from 'react';
import { Pause, Play, X } from 'lucide-react';
import { MotionDiv, useReducedMotion } from '../Motion';
import { PROMPT_AUTO_DISMISS_SECONDS } from '../../studySessionData';
import './study-session.css';

interface StudySessionTimerProps {
  subject: string;
  subjectColor: string;
  type: string;
  totalSeconds: number;
  elapsedSeconds: number;
  paused: boolean;
  onLeave: () => void;
  onTogglePause: () => void;
  prompt: { strategyName: string; prompt: string } | null;
  onCompletePrompt: () => void;
  onSkipPrompt: () => void;
}

const formatTime = (seconds: number) => `${Math.floor(seconds / 60).toString().padStart(2, '0')}:${Math.floor(seconds % 60).toString().padStart(2, '0')}`;

export default function StudySessionTimer({ subject, subjectColor, type, totalSeconds, elapsedSeconds, paused, onLeave, onTogglePause, prompt, onCompletePrompt, onSkipPrompt }: StudySessionTimerProps) {
  const remaining = Math.max(0, totalSeconds - elapsedSeconds);
  const progress = totalSeconds > 0 ? Math.min(100, elapsedSeconds / totalSeconds * 100) : 0;
  const reduceMotion = useReducedMotion();
  return (
    <div className="ss-timer-content" style={{ '--ss-subject': subjectColor } as React.CSSProperties}>
      <header className="ss-timer-navigation"><span className="ss-eyebrow">The study room</span><button type="button" onClick={onLeave} aria-label="Leave study session"><X size={20} aria-hidden="true" /></button></header>
      <main className="ss-timer-main">
        <p className="ss-timer-subject"><i aria-hidden="true" />{subject}</p>
        <p className="ss-timer-type">{type} · {Math.ceil(totalSeconds / 60)} min</p>
        <p className="ss-timer-digits" role="timer" aria-label={`${formatTime(remaining)} remaining`}>{formatTime(remaining)}</p>
        <p className="ss-timer-status">{paused ? 'Session paused' : 'Time remaining'}</p>
        <button type="button" className="ss-timer-pause" onClick={onTogglePause} aria-label={paused ? 'Resume study session' : 'Pause study session'}>{paused ? <Play size={19} fill="currentColor" aria-hidden="true" /> : <Pause size={19} aria-hidden="true" />}{paused ? 'Resume' : 'Pause'}</button>
      </main>
      {prompt && <section className="ss-coaching" aria-label="Study strategy prompt" key={prompt.prompt}>
        <div className="ss-coaching-heading"><p className="ss-eyebrow">Put it into practice</p><span>{prompt.strategyName}</span></div>
        <p className="ss-coaching-prompt">{prompt.prompt}</p>
        <div className="ss-coaching-actions"><button type="button" onClick={onCompletePrompt}>Done</button><button type="button" onClick={onSkipPrompt}>Skip</button></div>
        {!reduceMotion && <MotionDiv className="ss-prompt-countdown" initial={{ scaleX: 1 }} animate={{ scaleX: 0 }} transition={{ duration: PROMPT_AUTO_DISMISS_SECONDS, ease: 'linear' }} />}
      </section>}
      <footer className="ss-timer-footer"><div className="ss-timer-track" role="progressbar" aria-label="Session progress" aria-valuenow={Math.round(progress)} aria-valuemin={0} aria-valuemax={100}><span style={{ width: `${progress}%` }} /></div><div><span>{formatTime(elapsedSeconds)} elapsed</span><span>{formatTime(totalSeconds)} planned</span></div></footer>
    </div>
  );
}
