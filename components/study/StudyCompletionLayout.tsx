import React, { useEffect, useLayoutEffect, useRef } from 'react';
import KobraScope from '../approved-ui-runtime';
import CrewIllustration from '../CrewIllustration';
import { useReducedMotion } from '../Motion';
import { formatStudyTime } from '../../utils/studyTime';
import './study-completion.css';

interface Props {
  kind: 'timeup' | 'saved';
  title: string;
  description: string;
  subject: string;
  seconds: number;
  points: number;
  character?: string;
  children: React.ReactNode;
}

/** Shared live completion screens. Review appearances use the same controls and state. */
export default function StudyCompletionLayout({ kind, title, description, subject, seconds, points, character, children }: Props) {
  const titleId = `study-${kind}-title`;
  const titleRef = useRef<HTMLHeadingElement>(null);
  const layoutRef = useRef<HTMLElement>(null);
  const reduced = useReducedMotion();
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
  return <KobraScope className="nsu-study-completion">
    <main className={`sc-page sc-${kind}`}>
      <section ref={layoutRef} className="sc-layout" aria-labelledby={titleId}>
        <header className="sc-heading" data-study-arrive>
          <div>
            <p className="sc-eyebrow">The study room <span aria-hidden="true">/</span> {kind === 'saved' ? 'Your record' : 'Session complete'}</p>
            <h1 ref={titleRef} id={titleId} tabIndex={-1}>{title}</h1>
            <p className="sc-description">{description}</p>
          </div>
          {kind === 'saved' && <div className="sc-art"><CrewIllustration character={character} /></div>}
        </header>
        <dl className="sc-stats" aria-label="Session details" data-study-arrive>
          <div className="sc-stat-subject"><dt>Subject</dt><dd>{subject}</dd></div>
          <div><dt>Time studied</dt><dd>{formatStudyTime(seconds)}</dd></div>
          <div><dt>{kind === 'saved' ? 'Journey Points earned' : 'Journey Points on saving'}</dt><dd className="sc-points">{kind === 'saved' ? '+' : ''}{points}<small>JP</small></dd></div>
        </dl>
        <div className="sc-next">{children}</div>
      </section>
    </main>
  </KobraScope>;
}
