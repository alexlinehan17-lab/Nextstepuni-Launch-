import React, { useEffect, useLayoutEffect, useRef } from 'react';
import KobraScope from '../approved-ui-runtime';
import CrewIllustration from '../CrewIllustration';
import { useReducedMotion } from '../Motion';
import { useMobileAppDesign } from '../../hooks/useMobileAppDesign';
import { TopBar } from '../ui/Bars';
import './study-completion.css';
import './study-after.css';

interface Props {
  kind: 'timeup' | 'saved';
  title: string;
  description: string;
  subject: string;
  seconds: number;
  points: number;
  character?: string;
  /** Time's up: the session's to-dos, between the figures and what comes next. */
  todos?: React.ReactNode;
  /** A phone's pinned footer (Time's up: Finish and log), after the page. */
  footer?: React.ReactNode;
  children: React.ReactNode;
}

/** The figure for a length of time: the number large, its unit small beside it. */
function TimeFigure({ seconds }: { seconds: number }) {
  const whole = Math.max(0, seconds);
  const minutes = Math.floor(whole / 60), rest = Math.floor(whole % 60);
  return rest
    ? <>{minutes}<small> min</small> {rest}<small> sec</small></>
    : <>{minutes}<small>{minutes === 1 ? ' minute' : ' minutes'}</small></>;
}

/** Time's up and Session saved (c-study-dots and r5-post-session, agreed 26 Nov
 *  2026): the label in the bar, the headline (and the character beside it once
 *  saved), the subject, then the time and the points in a line. */
export default function StudyCompletionLayout({ kind, title, description, subject, seconds, points, character, todos, footer, children }: Props) {
  const titleId = `study-${kind}-title`;
  const titleRef = useRef<HTMLHeadingElement>(null);
  const layoutRef = useRef<HTMLElement>(null);
  const reduced = useReducedMotion();
  const phone = useMobileAppDesign();
  useEffect(() => {
    // Run after the outgoing modal releases its focus trap and restores focus.
    if (kind === 'saved') titleRef.current?.focus({ preventScroll: true });
  }, [kind]);
  useLayoutEffect(() => {
    const layout = layoutRef.current;
    if (kind !== 'saved' || reduced || document.hidden || !layout?.animate) return;
    const animation = layout.animate([
      { opacity: 0, transform: 'translateY(6px)' },
      { opacity: 1, transform: 'translateY(0)' },
    ], { duration: 360, easing: 'cubic-bezier(.22,1,.36,1)' });
    const settle = () => animation.cancel();
    // A suspended background animation must never hide the confirmation.
    const timeout = window.setTimeout(settle, 560);
    void animation.finished.catch(() => {}).then(() => { window.clearTimeout(timeout); });
    return () => { window.clearTimeout(timeout); settle(); };
  }, [kind, reduced]);
  const label = kind === 'saved' ? 'Your record' : 'Session complete';
  return <KobraScope className="nsu-study-completion">
    <main className={`sc-page sc-${kind}${phone ? ' sc-page--phone' : ' sc-page--desk'}`}>
      {phone && <TopBar className="sc-bar" placeLabel={label} />}
      <section ref={layoutRef} className="sc-layout" aria-labelledby={titleId}>
        <header className="sc-heading" data-study-arrive>
          {!phone && <p className="t-label sc-eyebrow">{label}</p>}
          <div className="sc-headrow">
            <h1 ref={titleRef} id={titleId} tabIndex={-1} className="t-display">{title}</h1>
            {kind === 'saved' && <div className="sc-art"><CrewIllustration character={character} /></div>}
          </div>
          <p className="t-sub sc-description">{description}</p>
        </header>
        <dl className="sc-stats" aria-label="Session details" data-study-arrive>
          <div className="sc-stat-subject"><dt>Subject</dt><dd>{subject}</dd></div>
          <div><dt>Time studied</dt><dd className="sc-figure"><TimeFigure seconds={seconds} /></dd></div>
          <div><dt>{kind === 'saved' ? 'Journey Points earned' : 'Journey Points on saving'}</dt><dd className="sc-figure sc-points">{kind === 'saved' ? '+' : ''}{points}<small>JP</small></dd></div>
        </dl>
        {todos}
        <div className="sc-next">{children}</div>
      </section>
      {footer}
    </main>
  </KobraScope>;
}
