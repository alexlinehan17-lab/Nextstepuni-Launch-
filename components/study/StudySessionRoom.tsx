import React, { useLayoutEffect, useRef, useState } from 'react';
import { useReducedMotion } from '../Motion';
import { useStudyTransitionSound } from '../../hooks/useStudyTransitionSound';
import StudySessionTimer, { type StudySessionTimerProps } from './StudySessionTimer';
import StudyBreak from './StudyBreak';
import StudySoundToggle from './StudySoundToggle';
import { animateStudyChange, studyControlOrigin } from './studyMotion';
import './study-motion.css';

interface Props extends Omit<StudySessionTimerProps, 'onTogglePause' | 'soundControl'> {
  onPause: () => void;
  onResume: () => void;
}

export default function StudySessionRoom({ onPause, onResume, onLeave, paused, ...timerProps }: Props) {
  const [transition, setTransition] = useState<{ toBreak: boolean; origin: { x: number; y: number } } | null>(null);
  const timerPage = useRef<HTMLDivElement>(null), breakPage = useRef<HTMLDivElement>(null);
  const busy = useRef(false), focusFrame = useRef(0);
  const actions = useRef({ onResume });
  actions.current = { onResume };
  const reduced = useReducedMotion();
  const sound = useStudyTransitionSound();
  const showBreak = transition ? transition.toBreak : paused;

  const change = (toBreak: boolean, event: React.MouseEvent<HTMLButtonElement>) => {
    if (busy.current) return;
    busy.current = true;
    sound.play(toBreak ? 'pause' : 'return');
    setTransition({ toBreak, origin: studyControlOrigin(event.currentTarget) });
    // Stop the real clock immediately; resume only when the return has settled.
    if (toBreak) onPause();
  };

  useLayoutEffect(() => {
    if (!transition || !timerPage.current || !breakPage.current) return;
    const to = transition.toBreak ? breakPage.current : timerPage.current;
    const from = transition.toBreak ? timerPage.current : breakPage.current;
    return animateStudyChange({ from, to, origin: transition.origin, reduced: Boolean(reduced), onFinish: () => {
      if (!transition.toBreak) actions.current.onResume();
      busy.current = false;
      setTransition(null);
      focusFrame.current = requestAnimationFrame(() => to.querySelector<HTMLButtonElement>(transition.toBreak ? '.crew-primary' : '.ss-timer-pause')?.focus({ preventScroll: true }));
    } });
  }, [transition, reduced]);
  useLayoutEffect(() => () => cancelAnimationFrame(focusFrame.current), []);

  return <div className="study-room-stage" data-transitioning={Boolean(transition)}>
    <div ref={timerPage} className="study-room-page" data-front={!showBreak} hidden={showBreak && !transition} inert={showBreak || Boolean(transition)} aria-hidden={showBreak || Boolean(transition)}>
      <StudySessionTimer {...timerProps} paused={paused && showBreak} onLeave={onLeave} onTogglePause={event => change(true, event)} soundControl={<StudySoundToggle muted={sound.muted} />} />
    </div>
    <div ref={breakPage} className="study-room-page study-room-break-page" data-front={showBreak} hidden={!showBreak && !transition} inert={!showBreak || Boolean(transition)} aria-hidden={!showBreak || Boolean(transition)}>
      <StudyBreak subject={timerProps.subject} elapsedSeconds={timerProps.elapsedSeconds} onResume={event => change(false, event)} onLeave={onLeave} sound={sound} />
    </div>
  </div>;
}
