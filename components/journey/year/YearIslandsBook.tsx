/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React, { useId } from 'react';
import { ArrowUpRight, RotateCw } from 'lucide-react';
import Avatar from '../../Avatar';
import { IslandPreview } from './IslandPreview';
import { possessive, type YearIsland } from './yearIslands';
import type { YearIslandsStatus } from '../../../hooks/useYearIslands';
import type { IslandVisibility } from '../../../functions/src/islandProjection';

export interface YearIslandsBookProps {
  /** "5th Year at Marino" */
  cohort: string;
  /** "Marino", for the eyebrow. */
  school: string;
  status: YearIslandsStatus;
  classmates: YearIsland[];
  visibility: IslandVisibility;
  visibilityKnown: boolean;
  visibilityError: string;
  onVisibility: (next: IslandVisibility) => void;
  onVisit: (classmate: YearIsland) => void;
  onRetry: () => void;
  /** Where to set a missing school year, when the app can take the student there. */
  onOpenSetup?: () => void;
  /** Demo Account: the classmates are invented. */
  sample?: boolean;
}

const tilesLabel = (count: number) => `${count} ${count === 1 ? 'tile' : 'tiles'}`;

export function YearIslandsBook(props: YearIslandsBookProps) {
  const { cohort, school, status, classmates, onVisit, onRetry, onOpenSetup, sample } = props;
  const loading = status === 'idle' || status === 'loading';
  return (
    <section className="year-book" aria-label="Your year" aria-busy={loading}>
      <div className="year-book-heading">
        <span className="eyebrow">YOUR YEAR{school ? ` / ${school.toUpperCase()}` : ''}</span>
        <h2>{cohort || 'Your year'}<span>.</span></h2>
        <p>Visit the islands your classmates are building. Visits are look only: nobody can build on, change or take anything from someone else’s island.</p>
      </div>
      {status !== 'no-school' && status !== 'graduated' && (props.visibilityKnown || loading) && <SharingSwitch {...props} />}
      {sample && <p className="year-book-sample">Sample classmates for the Demo Account. None of these are real students.</p>}
      {loading && (
        <div className="year-card-grid" role="status" aria-label="Finding your classmates’ islands">
          {[0, 1, 2].map(i => <span key={i} className="year-card-placeholder" aria-hidden="true"><span /><span /><span /></span>)}
        </div>
      )}
      {status === 'error' && (
        <div className="year-book-message" role="alert">
          <strong>Your year could not be loaded just now.</strong>
          <p>Check your connection, then try again.</p>
          <button type="button" className="year-action" onClick={onRetry}><RotateCw size={16} /> Try again</button>
        </div>
      )}
      {status === 'no-school' && (
        <div className="year-book-message">
          <strong>Join your school to see your year.</strong>
          <p>Your year’s islands appear once your account is linked to your school with its join code. Ask your teacher or guidance counsellor for it.</p>
        </div>
      )}
      {status === 'graduated' && (
        <div className="year-book-message">
          <strong>Your island is yours to keep.</strong>
          <p>Year islands are for students who are still in school, so yours is no longer shared and you will not see a year group here.</p>
        </div>
      )}
      {status === 'no-year' && (
        <div className="year-book-message">
          <strong>Add your school year to see your year.</strong>
          <p>We only show you the islands of classmates in the same year as you, so we need to know which year you are in.</p>
          {onOpenSetup && <button type="button" className="year-action" onClick={onOpenSetup}>Set my school year <ArrowUpRight size={16} /></button>}
        </div>
      )}
      {status === 'ready' && (classmates.length ? (
        <>
          <span className="year-book-count">{classmates.length} {classmates.length === 1 ? 'classmate is' : 'classmates are'} sharing an island</span>
          <ul className="year-card-grid">
            {classmates.map(classmate => (
              <li key={classmate.uid}>
                <button type="button" className="year-classmate-card" onClick={() => onVisit(classmate)} aria-label={`Visit ${possessive(classmate.name)} island, ${tilesLabel(classmate.tileCount)}`}>
                  <IslandPreview tiles={classmate.tiles} label={`${possessive(classmate.name)} island`} />
                  <span className="year-classmate-who">
                    <span className="year-classmate-avatar"><Avatar seed={classmate.avatar} alt="" /></span>
                    <span>
                      <strong>{classmate.name}</strong>
                      <small>{tilesLabel(classmate.tileCount)}</small>
                    </span>
                  </span>
                  <span className="year-visit-cta" aria-hidden="true">Visit island <ArrowUpRight size={15} /></span>
                </button>
              </li>
            ))}
          </ul>
        </>
      ) : (
        <div className="year-book-message">
          <strong>No classmates are sharing an island yet.</strong>
          <p>When classmates in {cohort || 'your year'} open their island, it will appear here.</p>
        </div>
      ))}
      <p className="year-book-foot">Only students in your year at your school can see this list. Classmates see a first name, an avatar and the island itself, never Journey Points, study time or anything you have written.</p>
    </section>
  );
}

function SharingSwitch({ cohort, visibility, visibilityKnown, visibilityError, onVisibility }: YearIslandsBookProps) {
  const known = visibilityKnown, on = known && visibility === 'year', id = useId();
  return (
    <div className="year-sharing">
      <div className="year-sharing-copy">
        <strong id={`${id}-title`}>Show my island to my year</strong>
        <span id={`${id}-detail`}>
          {!known
            ? 'Checking your choice…'
            : on
              ? `Classmates in ${cohort || 'your year'} can find and visit your island.`
              : 'Your island is hidden. Classmates cannot find or visit it.'}
        </span>
        {visibilityError && <span className="year-sharing-error" role="alert">{visibilityError}</span>}
      </div>
      <button
        type="button"
        role="switch"
        className="year-switch"
        aria-checked={on}
        aria-labelledby={`${id}-title`}
        aria-describedby={`${id}-detail`}
        disabled={!known}
        onClick={() => onVisibility(on ? 'hidden' : 'year')}
      >
        <span className="year-switch-track" aria-hidden="true"><span className="year-switch-knob" /></span>
        <span className="year-switch-state">{!known ? '' : on ? 'On' : 'Off'}</span>
      </button>
    </div>
  );
}
