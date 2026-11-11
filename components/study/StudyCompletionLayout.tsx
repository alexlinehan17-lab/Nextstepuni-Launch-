import React from 'react';
import KobraScope from '../approved-ui-runtime';
import CrewIllustration from '../CrewIllustration';
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
  return <KobraScope className="nsu-study-completion">
    <main className={`sc-page sc-${kind}`}>
      <section className="sc-layout" aria-labelledby={titleId}>
        <header className="sc-heading" data-study-arrive>
          <div>
            <p className="sc-eyebrow">The study room <span aria-hidden="true">/</span> {kind === 'saved' ? 'Your record' : 'Session complete'}</p>
            <h1 id={titleId} tabIndex={-1}>{title}</h1>
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
