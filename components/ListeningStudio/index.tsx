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
import { ArrowRight, ChevronLeft } from 'lucide-react';
import { LEVEL_LABEL, levelsFor, type Level } from '../MarkBank/deck';
import type { CardMemory } from '../MarkBank/scheduler';
import type { SessionCardResult } from '../MarkBank/SessionScreen';
import type { SecCard } from '../../types/markBank';
import { useNativeStatusBarAppearance } from '../../hooks/useNativeStatusBarAppearance';
import { useBackStep, useOptionalNavigation } from '../../contexts/NavigationContext';
import { Button, IconButton, TextButton } from '../ui/Button';
import { SelectionBar, SelectionMark } from '../ui/Choice';
import { List, PressBox, Row } from '../ui/List';
import { Menu } from '../ui/Menu';
import SubjectAvatar from '../SubjectAvatar';
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

/** The laptop layout from 1024px (boards r5-listening-studio and c-tools2-listening; below that the sidebar
 *  leaves too little room for two panels). Without
 *  matchMedia (a test, an old browser) the page is the wide one, as a laptop browser would be. */
function useBeside() {
  const query = '(min-width: 1024px)';
  const [beside, setBeside] = useState(() => typeof window === 'undefined' || typeof window.matchMedia !== 'function' || window.matchMedia(query).matches);
  useEffect(() => {
    if (typeof window.matchMedia !== 'function') return undefined;
    const media = window.matchMedia(query);
    const update = () => setBeside(media.matches);
    media.addEventListener?.('change', update);
    return () => media.removeEventListener?.('change', update);
  }, []);
  return beside;
}

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
  const beside = useBeside();
  const nav = useOptionalNavigation();
  const returnTo = useRef<HTMLElement | null>(null);
  const paperRef = useRef<HTMLElement | null>(null);
  const sittings = useMemo(() => listeningSittings(cards), [cards]);
  const [view, setView] = useState<'wall' | 'subjects'>('wall');
  const [selected, setSelected] = useState<string | null>(null);
  const [open, setOpen] = useState<{ sitting: string; section: string } | null>(null);
  const [leftOff, setLeftOff] = useState<LeftOff | null>(() => readLeftOff(uid));
  const [carrying, setCarrying] = useState<LeftOff | null>(null);
  // The Studio is a page of the Launchpad now (sidebar B beside it on a laptop, the tab bar under it
  // on a phone): its one Back is the bar's on a phone and the panel's on a laptop, and it returns to
  // where the student came from, as the app's Back does; the subject screen steps back to the papers.
  const leave = () => { if (nav) nav.goBack(); else onLeave?.(); };
  useBackStep(view === 'subjects', () => setView('wall'));

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

  const barNote = held === total ? `Every ${subjectLabel} recording plays here`
    : held === 0 ? 'Recordings open on the SEC site for now' : `${held} of ${total} recordings play here`;
  const ALL = '__all__';

  // The subjects: on a laptop today's words in a row (the one chosen in ink, with its character) and
  // All N subjects; on a phone one menu with the character, whose last line opens All N subjects
  // (boards r5-listening-studio and c-tools2-listening).
  const subjectControls = beside ? (
    <div className="ls7-subjects-row">
      <div className="ls7-tabs" role="group" aria-label="Subject">
        {tabs.map(subject => (
          <TextButton key={subject.id} className="ls7-tab" aria-pressed={subject.id === subjectId} onClick={() => chooseSubject(subject.id)}>
            <span className="ls7-tab-art" aria-hidden="true"><SubjectAvatar subject={subject.title} bare /></span>{subject.title}
          </TextButton>
        ))}
      </div>
      {subjects.length > tabs.length && <Button onClick={() => setView('subjects')}>All {subjects.length} subjects</Button>}
    </div>
  ) : (
    <Menu label="Subject" className="ls7-subject-menu" value={subjectId}
      face={<span className="ls7-menu-face"><span className="ls7-tab-art" aria-hidden="true"><SubjectAvatar subject={subjectLabel} bare /></span>{subjectLabel}</span>}
      options={[...tabs.map(subject => ({ value: subject.id, label: subject.title })), ...(subjects.length > tabs.length ? [{ value: ALL, label: `All ${subjects.length} subjects` }] : [])]}
      onChange={value => { if (value === ALL) setView('subjects'); else chooseSubject(value); }} />
  );

  const levelControl = levels.length > 1
    ? <SelectionBar label="Paper level" size="md" className="ls7-levels" value={level} onChange={value => chooseLevel(value)} options={levels.map(value => ({ value, label: LEVEL_LABEL[value] }))} />
    : null;

  const wall = (
    <div className="ls7-col">
      <div className="ls7-controls">
        {subjectControls}
        <div className="ls7-level-row">
          {levelControl}
          {beside && !loading && !error && total > 0 && <span className="t-meta">{barNote}</span>}
        </div>
      </div>

      {error ? (
        <div className="ls7-state" role="alert">
          <p className="t-body">These papers could not be loaded.</p>
          <Button onClick={onRetry}>Try again</Button>
        </div>
      ) : loading ? (
        <p className="ls7-state t-sub" role="status">Loading the {subjectLabel} papers…</p>
      ) : sittings.length === 0 ? (
        <p className="ls7-state t-sub">There are no {subjectLabel} {LEVEL_LABEL[level]} listening papers here yet.</p>
      ) : (
        <>
          <div className="ls7-wall" role="group" aria-label={`${subjectLabel} ${LEVEL_LABEL[level]} papers`}>
            {sittings.map(sitting => {
              const done = satCount(sitting);
              const here = leftOffHere?.key === sitting.key;
              const chosen = sitting.key === current?.key;
              return (
                <PressBox key={sitting.key} className="ls7-year" pressed={chosen} onPress={() => choose(sitting)}>
                  <span className="ls7-year-top">
                    <span className="ls7-year-n">{here ? <i className="ls7-here" aria-hidden="true" /> : null}{sitting.year}</span>
                    {beside && chosen ? <SelectionMark on /> : null}
                  </span>
                  {sitting.deferred && <span className="t-meta">Deferred sitting</span>}
                  <span className="ls7-strokes" aria-hidden="true">
                    {sitting.sections.map(section => <i key={section.key} data-on={sat(section) || undefined} />)}
                  </span>
                  <span className="t-meta">
                    {done > 0 ? `${done} of ${sitting.sections.length} sat`
                      : sitting.recordings.held === sitting.recordings.total ? 'Plays here'
                      : sitting.recordings.held === 0 ? 'SEC site' : 'Part plays here'}
                  </span>
                </PressBox>
              );
            })}
          </div>
          <p className="t-meta ls7-note">{beside ? 'A stroke is a section of the paper. A filled stroke is one you have sat.'
            : `${barNote}. A stroke is a section of the paper; a filled stroke is one you have sat.`}</p>
        </>
      )}
    </div>
  );

  const subjectScreen = (
    <div className="ls7-col">
      <header className="ls7-sh-head">
        <h2 className="t-heading">Choose a subject</h2>
        <p className="t-sub">{plural(subjects.length, 'subject has', 'subjects have')} a listening. Each shows how many of its recordings play inside the app.</p>
      </header>
      <List className="ls7-subject-list">
        {subjects.map(subject => {
          const count = hostedRecordingCount(subject.id);
          return (
            <Row key={subject.id} art={<SubjectAvatar subject={subject.title} bare />} title={subject.title}
              selected={subject.id === subjectId}
              meta={<>{mySubjectIds.includes(subject.id) ? <span className="ls7-mine">One of your subjects</span> : null}
                <span>{count > 0 ? `${plural(count, 'recording plays', 'recordings play')} here` : 'Recordings open on the SEC site for now'}</span></>}
              onPress={() => { chooseSubject(subject.id); setView('wall'); }} />
          );
        })}
      </List>
    </div>
  );

  const resume = leftOff ? (
    <div className="ls7-resume">
      <span className="t-label">Where you left off</span>
      <strong className="ls7-resume-what"><i className="ls7-here" aria-hidden="true" />{leftOff.subjectLabel} · {leftOff.sittingTitle} · {leftOff.sectionTitle}</strong>
      <Button size="sm" arrow="forward" onClick={carryOn}>Carry on</Button>
    </div>
  ) : null;

  return (
    <section className="ls7" aria-label="Listening Studio" data-view={view}>
      <section className="ls7-paper" aria-label="The paper you have chosen" ref={paperRef}>
        {beside && (
          <header className="ls7-panel-top">
            <IconButton label="Back" onClick={leave} icon={<ChevronLeft className="ui-icon" width={24} height={24} strokeWidth={1.75} aria-hidden="true" focusable="false" />} />
            <span className="ls7-panel-name">Listening Studio</span>
          </header>
        )}
        {current && !loading && !error ? (
          <>
            <div className="ls7-sleeve">
              <p className="ls7-subj">{subjectLabel}{beside ? null : ' · the paper you will sit'}</p>
              <h2 className="ls7-big">{current.year}<span className="ls7-break"> </span>{LEVEL_LABEL[current.level]}</h2>
              {current.deferred && <p className="ls7-subj">Deferred sitting</p>}
              <p className="ls7-meta">{beside ? <>
                {plural(current.sections.reduce((sum, section) => sum + section.cards.length, 0), 'part', 'parts')}
                {' · '}{plural(current.sections.reduce((sum, section) => sum + section.marks, 0), 'mark', 'marks')}
                {' · '}{recordingLine(current)}.
              </> : <>{plural(current.sections.length, 'section', 'sections')} · {recordingLine(current).replace(/^Recording/, 'the recording').replace(/^Part of/, 'part of')}</>}</p>
            </div>
            <div className="ls7-whole">
              <Button kind="main" size="lg" block arrow="forward" onClick={event => sit(current, current.sections[0], event.currentTarget)}>Sit the whole paper</Button>
            </div>
            <div className="ls7-sections">
              {!beside && <h3 className="t-heading">Or one section</h3>}
              <List className="ls7-srows">
                {current.sections.map(section => (
                  <SectionRow key={section.key} title={section.title}
                    here={leftOffHere?.key === current.key && leftOff?.section === section.key}
                    detail={<>{section.extracts.length > 1 && `${plural(section.extracts.length, 'extract', 'extracts')} · `}
                      {plural(section.cards.length, 'part', 'parts')}
                      {section.marks > 0 && ` · ${plural(section.marks, 'mark', 'marks')}`}
                      {sat(section) && ' · sat'}</>}
                    onSit={from => sit(current, section, from)} />
                ))}
              </List>
            </div>
          </>
        ) : null}
        {resume}
      </section>

      <section className="ls7-sheet" aria-label={view === 'wall' ? 'Choose a paper' : 'Choose a subject'}>
        {view === 'wall' ? wall : subjectScreen}
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
    </section>
  );
};

/** One section of the paper: the whole row sits it, its "Sit" drawn as the row's own button (board). */
const SectionRow: React.FC<{ title: string; detail: React.ReactNode; here: boolean; onSit: (from: HTMLElement) => void }> = ({ title, detail, here, onSit }) => (
  <li className="ui-row-item">
    <button type="button" className="ui-part ui-row ls7-srow" onClick={event => onSit(event.currentTarget)}>
      <span className="ui-row-body">
        <span className="ui-row-title">{here ? <i className="ls7-here" aria-hidden="true" /> : null}{title}</span>
        <span className="ui-row-meta">{detail}</span>
      </span>
      <span className="ls7-sit-pill">Sit <ArrowRight width={16} height={16} strokeWidth={2} aria-hidden="true" /></span>
    </button>
  </li>
);

export default ListeningStudio;
