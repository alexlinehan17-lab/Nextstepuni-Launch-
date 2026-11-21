/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Listening Studio: where every question with a recording is sat.
 *
 * The front page lists the papers of one subject and level, newest first, each
 * as the sections the paper itself numbers. Choosing a section opens the
 * sitting (StudioSitting). The cards, the student's review memory and the
 * recorder are Mark Bank's own, handed in by MarkBank.tsx, so a part sat here
 * is the same card, with the same history, as it was in a review.
 */

import React, { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowRight } from 'lucide-react';
import KobraScope, {
  Alert, AlertAction, AlertTitle, Button,
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
  Tabs, TabsList, TabsTrigger,
} from '../approved-ui-runtime';
import { LEVEL_LABEL, levelsFor, type Level } from '../MarkBank/deck';
import type { CardMemory } from '../MarkBank/scheduler';
import type { SessionCardResult } from '../MarkBank/SessionScreen';
import type { SecCard } from '../../types/markBank';
import { listeningSittings, type StudioSection, type StudioSitting as Sitting } from './model';
import StudioSitting from './StudioSitting';
import './listening-studio.css';

export interface ListeningStudioProps {
  subjectId: string;
  subjectLabel: string;
  level: Level;
  /** The subjects this student can sit a listening in. */
  subjects: { id: string; title: string }[];
  chooseSubject: (id: string) => void;
  chooseLevel: (level: Level) => void;
  /** The whole deck for this subject and level; the Studio takes the cards with a recording. */
  cards: SecCard[];
  memories: Record<string, CardMemory>;
  loading: boolean;
  error: boolean;
  onRetry: () => void;
  onGrade: (result: SessionCardResult) => string | void;
  /** Present when the Studio was opened from Mark Bank's board. */
  onBackToMarkBank?: () => void;
}

const plural = (count: number, one: string, many: string) => `${count} ${count === 1 ? one : many}`;

const sectionDetail = (section: StudioSection) => [
  section.extracts.length > 1 ? plural(section.extracts.length, 'extract', 'extracts') : null,
  plural(section.cards.length, 'part', 'parts'),
  section.marks > 0 ? plural(section.marks, 'mark', 'marks') : null,
].filter(Boolean).join(' · ');

const ListeningStudio: React.FC<ListeningStudioProps> = ({
  subjectId, subjectLabel, level, subjects, chooseSubject, chooseLevel,
  cards, memories, loading, error, onRetry, onGrade, onBackToMarkBank,
}) => {
  const sittings = useMemo(() => listeningSittings(cards), [cards]);
  const [open, setOpen] = useState<{ sitting: string; section: string } | null>(null);
  const returnTo = useRef<HTMLElement | null>(null);
  // A new subject or level has its own papers.
  useEffect(() => { setOpen(null); }, [subjectId, level]);

  const openSitting: Sitting | undefined = open ? sittings.find(sitting => sitting.key === open.sitting) : undefined;
  const openIndex = openSitting ? openSitting.sections.findIndex(section => section.key === open?.section) : -1;
  const openSection = openSitting && openIndex >= 0 ? openSitting.sections[openIndex] : undefined;
  const nextSection = openSitting && openIndex >= 0 ? openSitting.sections[openIndex + 1] : undefined;
  const close = () => {
    setOpen(null);
    requestAnimationFrame(() => returnTo.current?.focus());
  };
  const levels = levelsFor(subjectId);
  const done = (section: StudioSection) => section.cards.filter(card => (memories[card.id]?.reps ?? 0) > 0).length;

  return (
    <KobraScope sound={false}>
      <main className="ls-home mark-bank-theme" aria-busy={loading}>
        <header className="ls-home-head">
          <h1>Listening Studio</h1>
          <p>
            Sit a listening the way the exam runs it: the recording on one side, the questions for what you are
            hearing on the other. Then mark each part against the SEC scheme.
          </p>
        </header>

        <div className="ls-home-bar">
          <div className="ls-home-field">
            <span>Subject</span>
            <Select value={subjectId} items={subjects.map(subject => ({ value: subject.id, label: subject.title }))}
              onValueChange={value => value && chooseSubject(value)}>
              <SelectTrigger aria-label="Choose subject"><SelectValue /></SelectTrigger>
              <SelectContent align="start" alignItemWithTrigger={false}>
                {subjects.map(subject => <SelectItem key={subject.id} value={subject.id}>{subject.title}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>
          {levels.length > 1 && (
            <div className="ls-home-field">
              <span>Paper level</span>
              <Tabs value={level} onValueChange={value => chooseLevel(value as Level)}>
                <TabsList aria-label="Paper level">
                  {levels.map(value => <TabsTrigger key={value} value={value}>{LEVEL_LABEL[value]}</TabsTrigger>)}
                </TabsList>
              </Tabs>
            </div>
          )}
          {onBackToMarkBank && <Button variant="outline" onClick={onBackToMarkBank}>Back to Mark Bank</Button>}
        </div>

        {error ? (
          <Alert variant="error">
            <AlertTitle>These papers could not be loaded.</AlertTitle>
            <AlertAction><Button variant="outline" onClick={onRetry}>Try again</Button></AlertAction>
          </Alert>
        ) : loading ? (
          <p className="ls-home-state" role="status">Loading the {subjectLabel} papers…</p>
        ) : sittings.length === 0 ? (
          <p className="ls-home-state">
            There are no {subjectLabel} {LEVEL_LABEL[level]} listening papers here yet.
          </p>
        ) : sittings.map(sitting => (
          <section className="ls-year" key={sitting.key} aria-label={sitting.title}>
            <div className="ls-year-h">
              <h2>{sitting.title}</h2>
              <span>{sitting.playsInApp ? 'Recording plays here' : 'Recording opens on the SEC site'}</span>
            </div>
            {sitting.sections.map(section => {
              const reviewed = done(section);
              return (
                <button type="button" className="ls-row" key={section.key}
                  onClick={event => { returnTo.current = event.currentTarget; setOpen({ sitting: sitting.key, section: section.key }); }}>
                  <span className="ls-row-t">{section.title}</span>
                  <span className="ls-row-d">
                    {sectionDetail(section)}{reviewed > 0 && ` · ${reviewed} of ${section.cards.length} done`}
                  </span>
                  <span className="ls-row-go">Sit <ArrowRight aria-hidden="true" /></span>
                </button>
              );
            })}
          </section>
        ))}
      </main>

      {openSitting && openSection && (
        <StudioSitting
          key={openSection.key}
          subjectLabel={subjectLabel}
          sittingLabel={openSitting.title}
          section={openSection}
          nextSectionTitle={nextSection?.title}
          onNextSection={nextSection ? () => setOpen({ sitting: openSitting.key, section: nextSection.key }) : undefined}
          onGrade={onGrade}
          onClose={close}
        />
      )}
    </KobraScope>
  );
};

export default ListeningStudio;
