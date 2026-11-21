/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Listening Studio's front page: the "Year wall" (approved by Alex, 20 Nov 2026).
 *
 * The same ground and sheet as a sitting. On the sheet: the student's subjects
 * as tabs, the level, and one tile for every paper of that subject and level,
 * each showing how much of it has been sat. On the ground: the paper that is
 * chosen, with its sections ready to sit, where the recording will be once a
 * sitting opens. "All subjects" turns the sheet into the subject screen.
 *
 * The cards, the student's review memory and the recorder are Mark Bank's own,
 * handed in by MarkBank.tsx, so a part sat here is the same card, with the same
 * history, as it was in a review.
 */

import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { ArrowRight, X } from 'lucide-react';
import { LEVEL_LABEL, levelsFor, type Level } from '../MarkBank/deck';
import type { CardMemory } from '../MarkBank/scheduler';
import type { SessionCardResult } from '../MarkBank/SessionScreen';
import type { SecCard } from '../../types/markBank';
import { useModal } from '../../hooks/useModal';
import { useNativeStatusBarAppearance } from '../../hooks/useNativeStatusBarAppearance';
import {
  hostedRecordingCount, listeningSittings, type StudioSection, type StudioSitting as Sitting,
} from './model';
import StudioSitting from './StudioSitting';
import './listening-studio.css';

export interface ListeningStudioProps {
  uid?: string;
  subjectId: string;
  subjectLabel: string;
  level: Level;
  /** Every subject with listenings that this student may open. */
  subjects: { id: string; title: string }[];
  /** The ones on the student's own profile: they are the tabs. */
  mySubjectIds: string[];
  chooseSubject: (id: string) => void;
  chooseLevel: (level: Level) => void;
  /** The whole deck for this subject and level; the Studio takes the cards with a recording. */
  cards: SecCard[];
  memories: Record<string, CardMemory>;
  loading: boolean;
  error: boolean;
  onRetry: () => void;
  onGrade: (result: SessionCardResult) => string | void;
  /** Back to the Launchpad. */
  onLeave?: () => void;
}

/** The last section a student opened, so the Studio can offer it again. */
interface LeftOff {
  subjectId: string;
  subjectLabel: string;
  level: Level;
  sitting: string;
  sittingTitle: string;
  section: string;
  sectionTitle: string;
}

const leftOffKey = (uid?: string) => `ls:left-off:${uid ?? 'anon'}`;
const readLeftOff = (uid?: string): LeftOff | null => {
  try {
    const saved = JSON.parse(window.localStorage.getItem(leftOffKey(uid)) ?? 'null') as LeftOff | null;
    return saved && typeof saved.sitting === 'string' && typeof saved.section === 'string' ? saved : null;
  } catch {
    return null;
  }
};
const writeLeftOff = (uid: string | undefined, value: LeftOff) => {
  try {
    window.localStorage.setItem(leftOffKey(uid), JSON.stringify(value));
  } catch {
    /* Private browsing: the Studio simply does not offer to carry on. */
  }
};

const noop = () => {};
const plural = (count: number, one: string, many: string) => `${count} ${count === 1 ? one : many}`;
const recordingLine = (sitting: Sitting) =>
  sitting.recordings.held === sitting.recordings.total ? 'Recording plays here'
    : sitting.recordings.held === 0 ? 'Recording opens on the SEC site'
    : 'Part of the recording plays here';

const ListeningStudio: React.FC<ListeningStudioProps> = ({
  uid, subjectId, subjectLabel, level, subjects, mySubjectIds, chooseSubject, chooseLevel,
  cards, memories, loading, error, onRetry, onGrade, onLeave,
}) => {
  useNativeStatusBarAppearance('dark');
  const dialogRef = useRef<HTMLDivElement | null>(null);
  const returnTo = useRef<HTMLElement | null>(null);
  const paperRef = useRef<HTMLElement | null>(null);
  const sittings = useMemo(() => listeningSittings(cards), [cards]);
  const [view, setView] = useState<'wall' | 'subjects'>('wall');
  const [selected, setSelected] = useState<string | null>(null);
  const [open, setOpen] = useState<{ sitting: string; section: string } | null>(null);
  const [leftOff, setLeftOff] = useState<LeftOff | null>(() => readLeftOff(uid));
  const [carrying, setCarrying] = useState<LeftOff | null>(null);
  useModal(true, onLeave ?? noop, dialogRef, { initialFocus: 'dialog' });

  // A new subject or level has its own papers.
  useEffect(() => { setOpen(null); setSelected(null); }, [subjectId, level]);

  // Carrying on with a paper of another subject or level: go there, then open it.
  useEffect(() => {
    if (!carrying) return;
    if (carrying.subjectId !== subjectId) return;
    if (carrying.level !== level) { chooseLevel(carrying.level); return; }
    if (loading) return;
    if (sittings.some(sitting => sitting.key === carrying.sitting
      && sitting.sections.some(section => section.key === carrying.section))) {
      setSelected(carrying.sitting);
      setOpen({ sitting: carrying.sitting, section: carrying.section });
    }
    setCarrying(null);
  }, [carrying, subjectId, level, loading, sittings, chooseLevel]);

  // A section counts as sat once at least half of its parts have a saved review.
  const reviewed = useCallback(
    (section: StudioSection) => section.cards.filter(card => (memories[card.id]?.reps ?? 0) > 0).length,
    [memories],
  );
  const sat = (section: StudioSection) => reviewed(section) * 2 >= section.cards.length;
  const satCount = (sitting: Sitting) => sitting.sections.filter(sat).length;

  const leftOffHere = leftOff && leftOff.subjectId === subjectId && leftOff.level === level
    ? sittings.find(sitting => sitting.key === leftOff.sitting) : undefined;
  const current: Sitting | undefined = sittings.find(sitting => sitting.key === selected) ?? leftOffHere ?? sittings[0];
  const levels = levelsFor(subjectId);
  const tabs = subjects.filter(subject => mySubjectIds.includes(subject.id) || subject.id === subjectId);
  const held = sittings.reduce((sum, sitting) => sum + sitting.recordings.held, 0);
  const total = sittings.reduce((sum, sitting) => sum + sitting.recordings.total, 0);

  const openSitting = open ? sittings.find(sitting => sitting.key === open.sitting) : undefined;
  const openIndex = openSitting ? openSitting.sections.findIndex(section => section.key === open?.section) : -1;
  const openSection = openSitting && openIndex >= 0 ? openSitting.sections[openIndex] : undefined;
  const nextSection = openSitting && openIndex >= 0 ? openSitting.sections[openIndex + 1] : undefined;

  const sit = (sitting: Sitting, section: StudioSection, from?: HTMLElement) => {
    if (from) returnTo.current = from;
    const place: LeftOff = {
      subjectId, subjectLabel, level,
      sitting: sitting.key, sittingTitle: sitting.title, section: section.key, sectionTitle: section.title,
    };
    writeLeftOff(uid, place);
    setLeftOff(place);
    setOpen({ sitting: sitting.key, section: section.key });
  };
  const close = () => {
    setOpen(null);
    requestAnimationFrame(() => returnTo.current?.focus());
  };
  // On a phone the chosen paper sits below the wall, so choosing a year brings it into view.
  const choose = (sitting: Sitting) => {
    setSelected(sitting.key);
    if (typeof window.matchMedia !== 'function' || !window.matchMedia('(max-width: 900px)').matches) return;
    const calm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    requestAnimationFrame(() => paperRef.current?.scrollIntoView?.({ block: 'start', behavior: calm ? 'auto' : 'smooth' }));
  };
  const carryOn = () => {
    if (!leftOff) return;
    setView('wall');
    setCarrying(leftOff);
    if (leftOff.subjectId !== subjectId) chooseSubject(leftOff.subjectId);
  };

  const wall = (
    <div className="ls-col ls-front-col">
      <div className="ls-tabs" role="group" aria-label="Subject">
        {tabs.map(subject => (
          <button type="button" className="ls-tab" key={subject.id} aria-pressed={subject.id === subjectId}
            onClick={() => chooseSubject(subject.id)}>{subject.title}</button>
        ))}
        {subjects.length > tabs.length && (
          <button type="button" className="ls-btn" onClick={() => setView('subjects')}>All {subjects.length} subjects</button>
        )}
      </div>

      <div className="ls-bar">
        {levels.length > 1 ? (
          <div className="ls-levels" role="group" aria-label="Paper level">
            {levels.map(value => (
              <button type="button" key={value} aria-pressed={value === level} onClick={() => chooseLevel(value)}>{LEVEL_LABEL[value]}</button>
            ))}
          </div>
        ) : <span />}
        {!loading && !error && total > 0 && (
          <span className="ls-bar-note">
            {held === total ? 'Every recording plays here' : held === 0 ? 'Recordings open on the SEC site for now' : `${held} of ${total} recordings play here`}
          </span>
        )}
      </div>

      {error ? (
        <div className="ls-state" role="alert">
          <p>These papers could not be loaded.</p>
          <button type="button" className="ls-btn" onClick={onRetry}>Try again</button>
        </div>
      ) : loading ? (
        <p className="ls-state" role="status">Loading the {subjectLabel} papers…</p>
      ) : sittings.length === 0 ? (
        <p className="ls-state">There are no {subjectLabel} {LEVEL_LABEL[level]} listening papers here yet.</p>
      ) : (
        <>
          <div className="ls-wall" role="group" aria-label={`${subjectLabel} ${LEVEL_LABEL[level]} papers`}>
            {sittings.map(sitting => {
              const done = satCount(sitting);
              const here = leftOffHere?.key === sitting.key;
              return (
                <button type="button" className="ls-year" key={sitting.key} aria-pressed={sitting.key === current?.key}
                  onClick={() => choose(sitting)}>
                  <b className={here ? 'ls-here' : undefined}>{sitting.year}</b>
                  {sitting.deferred && <em>Deferred sitting</em>}
                  <span className="ls-ticks" aria-hidden="true">
                    {sitting.sections.map(section => <span key={section.key} className={sat(section) ? 'is-on' : undefined} />)}
                  </span>
                  <small>
                    {done > 0 ? `${done} of ${sitting.sections.length} sat`
                      : sitting.recordings.held === sitting.recordings.total ? 'Plays here'
                      : sitting.recordings.held === 0 ? 'SEC site' : 'Part plays here'}
                  </small>
                </button>
              );
            })}
          </div>
          <p className="ls-note">A stroke is a section of the paper. A filled stroke is one you have sat.</p>
        </>
      )}
    </div>
  );

  const subjectScreen = (
    <div className="ls-col ls-front-col">
      <header className="ls-sh-head">
        <h2>Choose a subject</h2>
        <p>{plural(subjects.length, 'subject has', 'subjects have')} a listening. Each shows how many of its recordings play inside the app.</p>
      </header>
      <div className="ls-subjects">
        {subjects.map(subject => {
          const count = hostedRecordingCount(subject.id);
          return (
            <button type="button" className="ls-subject" key={subject.id} aria-pressed={subject.id === subjectId}
              onClick={() => { chooseSubject(subject.id); setView('wall'); }}>
              <b>{subject.title}</b>
              <span>{mySubjectIds.includes(subject.id) ? 'One of your subjects' : ''}</span>
              <span className="ls-subject-rec">
                {count > 0 ? `${plural(count, 'recording plays', 'recordings play')} here` : 'Recordings open on the SEC site for now'}
              </span>
            </button>
          );
        })}
      </div>
      <div className="ls-nav">
        <button type="button" className="ls-btn" onClick={() => setView('wall')}>Back to {subjectLabel}</button>
      </div>
    </div>
  );

  const paper = current && !loading && !error ? (
    <div className="ls-sleeve">
      <div>
        <p className="ls-sleeve-sub">{subjectLabel}</p>
        <h1>{current.year}<br />{LEVEL_LABEL[current.level]}</h1>
        {current.deferred && <p className="ls-sleeve-sub">Deferred sitting</p>}
      </div>
      <p className="ls-sleeve-meta">
        {plural(current.sections.reduce((sum, section) => sum + section.cards.length, 0), 'part', 'parts')}
        {' · '}{plural(current.sections.reduce((sum, section) => sum + section.marks, 0), 'mark', 'marks')}
        {' · '}{recordingLine(current)}.
      </p>
      <div className="ls-srows">
        {current.sections.map(section => (
          <button type="button" className="ls-srow" key={section.key}
            onClick={event => sit(current, section, event.currentTarget)}>
            <span className={`ls-srow-t${leftOffHere?.key === current.key && leftOff?.section === section.key ? ' ls-here' : ''}`}>{section.title}</span>
            <span className="ls-srow-d">
              {section.extracts.length > 1 && `${plural(section.extracts.length, 'extract', 'extracts')} · `}
              {plural(section.cards.length, 'part', 'parts')}
              {section.marks > 0 && ` · ${plural(section.marks, 'mark', 'marks')}`}
              {sat(section) && ' · sat'}
            </span>
            <span className="ls-go">Sit <ArrowRight aria-hidden="true" /></span>
          </button>
        ))}
      </div>
      <button type="button" className="ls-btn-primary" onClick={event => sit(current, current.sections[0], event.currentTarget)}>
        Sit the whole paper
      </button>
    </div>
  ) : <div className="ls-sleeve" />;

  return createPortal(
    <div className="ls-root ls-front" role="dialog" aria-modal="true" aria-label="Listening Studio" tabIndex={-1} ref={dialogRef}>
      <header className="ls-front-top">
        <h1>Listening Studio</h1>
        {onLeave && (
          <button type="button" className="ls-btn ls-btn-icon" aria-label="Leave Listening Studio" onClick={onLeave}>
            <X aria-hidden="true" />
          </button>
        )}
      </header>

      <section className="ls-sheet ls-front-sheet mark-bank-theme" aria-label={view === 'wall' ? 'Choose a paper' : 'Choose a subject'}>
        {view === 'wall' ? wall : subjectScreen}
      </section>

      <section className="ls-front-paper" aria-label="The paper you have chosen" ref={paperRef}>
        {paper}
        {leftOff && (
          <div className="ls-resume">
            <span>Where you left off</span>
            <strong className="ls-here">{leftOff.subjectLabel} · {leftOff.sittingTitle} · {leftOff.sectionTitle}</strong>
            <button type="button" className="ls-btn" onClick={carryOn}>Carry on <ArrowRight aria-hidden="true" /></button>
          </div>
        )}
      </section>

      {openSitting && openSection && (
        <StudioSitting
          key={openSection.key}
          subjectLabel={subjectLabel}
          sittingLabel={openSitting.title}
          section={openSection}
          nextSectionTitle={nextSection?.title}
          onNextSection={nextSection ? () => sit(openSitting, nextSection) : undefined}
          onGrade={onGrade}
          onClose={close}
        />
      )}
    </div>,
    document.body,
  );
};

export default ListeningStudio;
