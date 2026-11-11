import React, { useLayoutEffect, useRef, useState } from 'react';
import { useReducedMotion } from '../Motion';
import type { useStudyTransitionSound } from '../../hooks/useStudyTransitionSound';
import StudySessionTimer, { type StudySessionTimerProps } from './StudySessionTimer';
import StudyBreak from './StudyBreak';
import StudySoundToggle from './StudySoundToggle';
import StudyNotifyOffer from './StudyNotifyOffer';
import { StudyFocusStatus } from './StudyFocusChoice';
import { animateStudyChange, studyControlOrigin } from './studyMotion';
import './study-motion.css';

interface Props extends Omit<StudySessionTimerProps, 'onTogglePause' | 'soundControl'> {
  onPause: () => void;
  onResume: () => void;
  sound: ReturnType<typeof useStudyTransitionSound>;
  completion?: React.ReactNode;
}

export default function StudySessionRoom({ onPause, onResume, onLeave, paused, sound, completion, ...timerProps }: Props) {
  const [transition, setTransition] = useState<{ toBreak: boolean; origin: { x: number; y: number } } | null>(null);
  const timerPage = useRef<HTMLDivElement>(null), breakPage = useRef<HTMLDivElement>(null);
  const completePage = useRef<HTMLDivElement>(null);
  const completed = Boolean(completion);
  const wasComplete = useRef(completed);
  const [arriving, setArriving] = useState(false);
  const busy = useRef(false), focusFrame = useRef(0);
  const actions = useRef({ onResume });
  actions.current = { onResume };
  const reduced = useReducedMotion();
  const showBreak = transition ? transition.toBreak : paused;

  const change = (toBreak: boolean, event: React.MouseEvent<HTMLButtonElement>) => {
    if (busy.current) return;
    busy.current = true;
    sound.prepare();
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
  useLayoutEffect(() => {
    const justFinished = completed && !wasComplete.current;
    wasComplete.current = completed;
    if (!justFinished) return;
    setTransition(null);
    setArriving(true);
    // A restored or revisited completed session is already settled and silent.
    if (!document.hidden) sound.play('pause');
  }, [completed, sound.play]);
  useLayoutEffect(() => {
    if (!arriving || !completePage.current || !timerPage.current) return;
    const to = completePage.current;
    const clock = timerPage.current.querySelector<HTMLElement>('.ss-timer-digits') ?? timerPage.current;
    return animateStudyChange({ from: timerPage.current, to, origin: studyControlOrigin(clock), reduced: Boolean(reduced) || document.hidden, fadeOut: true,
      onFinish: () => {
        setArriving(false);
        focusFrame.current = requestAnimationFrame(() => to.querySelector<HTMLElement>('h1')?.focus({ preventScroll: true }));
      },
    });
  }, [arriving, reduced]);
  useLayoutEffect(() => () => cancelAnimationFrame(focusFrame.current), []);

  return <div className="study-room-stage" data-transitioning={Boolean(transition) || arriving}>
    <div ref={timerPage} className="study-room-page" data-front={!showBreak && !completed} hidden={(completed && !arriving) || (showBreak && !transition)} inert={completed || showBreak || Boolean(transition)} aria-hidden={completed || showBreak || Boolean(transition)}>
      <StudySessionTimer {...timerProps} paused={paused && showBreak} onLeave={onLeave} onTogglePause={event => change(true, event)} soundControl={<StudySoundToggle muted={sound.muted} />} notifyOffer={<><StudyNotifyOffer /><StudyFocusStatus /></>} />
    </div>
    <div ref={breakPage} className="study-room-page study-room-break-page" data-front={showBreak && !completed} hidden={completed || (!showBreak && !transition)} inert={completed || !showBreak || Boolean(transition)} aria-hidden={completed || !showBreak || Boolean(transition)}>
      <StudyBreak subject={timerProps.subject} elapsedSeconds={timerProps.elapsedSeconds} onResume={event => change(false, event)} onLeave={onLeave} sound={sound} />
    </div>
    {completed && <div ref={completePage} className="study-room-page study-room-complete-page" data-front="true" inert={arriving} aria-hidden={arriving}>{completion}</div>}
  </div>;
}
