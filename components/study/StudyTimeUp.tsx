import React, { useEffect, useState } from 'react';
import { useReducedMotion } from '../Motion';
import { SESSION_EXTENSION_MINUTES, STUDY_SESSION_POINTS } from '../../studySessionData';
import { useMobileAppDesign } from '../../hooks/useMobileAppDesign';
import { PinnedFooter } from '../ui/Bars';
import { Button } from '../ui/Button';
import { CheckRow } from '../ui/List';
import StudyCompletionLayout from './StudyCompletionLayout';
import { StudyTodoDot } from './StudyTodoDot';
import { STUDY_TYPES } from './StudySessionSetup';

interface Props {
  subject: string;
  elapsedSeconds: number;
  extendedMinutes: number;
  extensionBonus: number;
  sessionPoints: number;
  onKeepGoing: (minutes: number) => void;
  onFinish: () => void;
  /** The session's to-dos, back on Time's up (c-study-dots, agreed 26 Nov 2026). */
  todos?: { label: string; done?: boolean }[];
}

export default function StudyTimeUp({ subject, elapsedSeconds, extendedMinutes, extensionBonus, sessionPoints, onKeepGoing, onFinish, todos = [] }: Props) {
  const phone = useMobileAppDesign();
  const reduced = useReducedMotion();
  // The to-dos set before the session fill green one after another as the
  // screen arrives; one the student added fills when they tap it. This is the
  // screen's own record: nothing here is saved.
  const [filled, setFilled] = useState(reduced ? todos.length : 0);
  const [ticked, setTicked] = useState<Record<number, boolean>>({});
  useEffect(() => {
    if (reduced) { setFilled(todos.length); return undefined; }
    const timers = todos.map((_, index) => window.setTimeout(() => setFilled(count => Math.max(count, index + 1)), 420 + index * 220));
    return () => timers.forEach(timer => window.clearTimeout(timer));
  }, [reduced, todos.length]);
  const isDone = (index: number) => ticked[index] ?? (Boolean(todos[index]?.done) && index < filled);
  const count = todos.filter((_, index) => isDone(index)).length;
  const finish = <Button kind="main" size="lg" block arrow="forward" className="sc-main" onClick={onFinish}>Finish and log</Button>;
  const bonusNote = extensionBonus > 0 ? `Includes +${extensionBonus} JP for finishing your extra time.` : undefined;
  return <StudyCompletionLayout kind="timeup" title={extendedMinutes > 0 ? 'You kept going.' : 'Time’s up.'}
    description="Keep going for a little longer, or save the work you’ve done."
    subject={subject} seconds={elapsedSeconds} points={sessionPoints}
    footer={phone ? <PinnedFooter ruled className="sc-finish" note={bonusNote}>{finish}</PinnedFooter> : undefined}
    todos={todos.length > 0 ? <section className="sc-todos" aria-labelledby="sc-todos-title" data-study-arrive>
      <div className="sc-todos-head"><h2 id="sc-todos-title" className="t-row">Your to-dos</h2><span className="t-readout">{count} / {todos.length}</span></div>
      <div className="sc-todos-list">
        {todos.map((step, index) => (
          <CheckRow key={`${index}-${step.label}`} className="sc-todo" checked={isDone(index)}
            onChange={value => setTicked(current => ({ ...current, [index]: value }))}
            mark={<StudyTodoDot set done={isDone(index)} />}>
            {step.label}
          </CheckRow>
        ))}
      </div>
      {todos.some((_, index) => !isDone(index)) && <p className="t-meta">{phone ? 'Tap' : 'Click'} one you finished to fill it.</p>}
    </section> : null}>
    {!phone && <div className="sc-finish-desk" data-study-arrive>{finish}{bonusNote && <p className="sc-note">{bonusNote}</p>}</div>}
    <section className="sc-extend" aria-labelledby="sc-keep-going" data-study-arrive>
      <h2 id="sc-keep-going" className="t-heading">Need a little longer?</h2>
      <p className="t-sub">Add time to this session.</p>
      <div className="sc-extensions">
        {SESSION_EXTENSION_MINUTES.map(minutes => <Button key={minutes} className="sc-second" onClick={() => onKeepGoing(minutes)} aria-label={`Keep going for ${minutes} more minutes`}>+{minutes} min</Button>)}
      </div>
      <p className="t-meta">Extra minutes count towards your JP. Finish them and earn +{STUDY_SESSION_POINTS.EXTENSION_COMPLETED} JP.</p>
    </section>
  </StudyCompletionLayout>;
}

/** The to-dos a session wrote itself (as Your session showed them), for when
 *  the student did not write their own. */
export function sessionTodosFor(subject: string, sessionType: string, plannedSeconds: number) {
  return [
    { label: subject, done: true },
    { label: STUDY_TYPES.find(type => type.id === sessionType)?.detail ?? 'Your way of working', done: true },
    { label: `${Math.round(plannedSeconds / 60)} minutes of attention`, done: true },
  ];
}
