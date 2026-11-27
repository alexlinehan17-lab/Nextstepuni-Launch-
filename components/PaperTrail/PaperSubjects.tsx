import React from 'react';
import { Bookmark, Search } from 'lucide-react';
import { Combobox, ComboboxInput, ComboboxContent, ComboboxList, ComboboxItem, ComboboxEmpty } from '../approved-ui-runtime';
import { Button } from '../ui/Button';
import { SelectionBar } from '../ui/Choice';
import { List, Row } from '../ui/List';
import ThemeArtwork from '../ThemeArtwork';
import SubjectAvatar from '../SubjectAvatar';
import { getSubjectStarCrew } from '../../data/subjectStarCrew';
import type { PaperTrailSubject, PaperLevel } from '../../types/paperTrail';

/** A subject's Star Crew character, bare on the page (no tile behind it). */
export function PaperSubjectArtwork({ label, className = 'pt-subject-art' }: { label: string; className?: string }) {
  const artwork = getSubjectStarCrew(label);
  return artwork && artwork.frame.tile === undefined
    ? <ThemeArtwork src={artwork.src} alt="" transparentBackground className={className} />
    : <SubjectAvatar subject={label} className={className} bare />;
}

type Suggestion = { subject: PaperTrailSubject; year?: number; level?: PaperLevel };

/** Find a subject or a paper, Saved, and which subjects the list shows. */
export function PaperSubjectFinder({ subjects, labelFor, scope, onScope, query, onQuery, suggestions, onSelect, onSaved }: {
  subjects: PaperTrailSubject[];
  labelFor: (subject: PaperTrailSubject) => string;
  scope: 'mine' | 'all'; onScope: (scope: 'mine' | 'all') => void;
  query: string; onQuery: (query: string) => void;
  suggestions: Suggestion[] | null;
  onSelect: (id: string, year?: number, level?: PaperLevel) => void;
  onSaved: () => void;
}) {
  const choices = (suggestions ?? subjects.map(subject => ({ subject, year: undefined, level: undefined }))).map(s => ({
    ...s, label: [labelFor(s.subject), s.year, s.level ? `${s.level[0].toUpperCase()}${s.level.slice(1)}` : undefined].filter(Boolean).join(' · '),
  }));
  return <div className="pt-finder">
    <div className="pt-find-row">
      <div className="pt-find">
        <Search className="ui-icon pt-find-glyph" width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" />
        <Combobox items={choices.map(choice => choice.label)} filter={null} value={null}
          inputValue={query} onInputValueChange={onQuery}
          onValueChange={value => { const choice = choices.find(candidate => candidate.label === value); if (choice) onSelect(choice.subject.id, choice.year, choice.level); }}>
          <ComboboxInput id="pt-subject-search" aria-label="Find a subject or paper" placeholder="Find a subject or paper" showTrigger={false} showClear />
          <ComboboxContent><ComboboxEmpty>No matches. Try another subject or year.</ComboboxEmpty><ComboboxList>{(choice: string) => <ComboboxItem key={choice} value={choice}>{choice}</ComboboxItem>}</ComboboxList></ComboboxContent>
        </Combobox>
      </div>
      <Button className="pt-icon-btn" onClick={onSaved}><Bookmark width={20} height={20} strokeWidth={1.75} aria-hidden="true" />Saved</Button>
    </div>
    <SelectionBar label="Subject selection" size="md" className="pt-scope" value={scope} onChange={onScope}
      options={[{ value: 'mine', label: 'My subjects' }, { value: 'all', label: 'All subjects' }]} />
  </div>;
}

/** One boxed list of subjects, each with its character at the left. */
export function PaperSubjects({ subjects, labelFor, levelFor, scope, onScope, query, onQuery, suggestions, onSelect }: {
  subjects: PaperTrailSubject[];
  labelFor: (subject: PaperTrailSubject) => string; levelFor: (subject: PaperTrailSubject) => string;
  scope: 'mine' | 'all'; onScope: (scope: 'mine' | 'all') => void;
  query: string; onQuery: (query: string) => void;
  suggestions: Suggestion[] | null;
  onSelect: (id: string, year?: number, level?: PaperLevel) => void;
}) {
  const filtered = query.trim().length >= 2 && suggestions ? suggestions.map(s => s.subject) : subjects;
  return <div className="pt-subject-picker">
    {filtered.length > 0 && <List boxed className="pt-subject-list" label={scope === 'mine' ? 'My subjects' : 'All subjects'}>
      {filtered.map(subject => {
        const level = `${levelFor(subject)} level${subject.cycle === 'lca' ? ' · LCA' : ''}`;
        return <Row key={subject.id} title={labelFor(subject)} meta={level} label={`${labelFor(subject)} ${level}`}
          art={<PaperSubjectArtwork label={labelFor(subject)} className="pt-row-art" />}
          onPress={() => {
            const choice = suggestions?.find(candidate => candidate.subject.id === subject.id);
            onSelect(subject.id, choice?.year, choice?.level);
          }} />;
      })}
    </List>}
    {!filtered.length && <div className="pt-empty-subjects"><p>{query.trim() ? 'No matching subjects. Try another name.' : 'Your subjects will appear here once you add them to your profile.'}</p>{scope === 'mine' && <Button onClick={() => { onQuery(''); onScope('all'); }}>Browse all subjects</Button>}</div>}
  </div>;
}
