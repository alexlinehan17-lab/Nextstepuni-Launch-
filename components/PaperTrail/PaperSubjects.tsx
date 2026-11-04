import React from 'react';
import { ArrowRight } from 'lucide-react';
import { Button } from '../approved-ui-runtime';
import { Combobox, ComboboxInput, ComboboxContent, ComboboxList, ComboboxItem, ComboboxEmpty } from '../approved-ui-runtime';
import { ToggleGroup, ToggleGroupItem } from '../approved-ui-runtime';
import ThemeArtwork from '../ThemeArtwork';
import SubjectAvatar from '../SubjectAvatar';
import { getSubjectStarCrew } from '../../data/subjectStarCrew';
import type { PaperTrailSubject, PaperLevel } from '../../types/paperTrail';

export function PaperSubjectArtwork({ label }: { label: string }) {
  const artwork = getSubjectStarCrew(label);
  return artwork && artwork.frame.tile === undefined
    ? <ThemeArtwork src={artwork.src} alt="" className="pt-subject-art" />
    : <SubjectAvatar subject={label} className="pt-subject-art" />;
}

export function PaperSubjects({ subjects, selected, labelFor, levelFor, scope, onScope, query, onQuery, suggestions, onSelect }: {
  subjects: PaperTrailSubject[]; selected?: string;
  labelFor: (subject: PaperTrailSubject) => string; levelFor: (subject: PaperTrailSubject) => string;
  scope: 'mine' | 'all'; onScope: (scope: 'mine' | 'all') => void;
  query: string; onQuery: (query: string) => void;
  suggestions: { subject: PaperTrailSubject; year?: number; level?: PaperLevel }[] | null;
  onSelect: (id: string, year?: number, level?: PaperLevel) => void;
}) {
  const choices = (suggestions ?? subjects.map(subject => ({ subject, year: undefined, level: undefined }))).map(s => ({
    ...s, label: [labelFor(s.subject), s.year, s.level ? `${s.level[0].toUpperCase()}${s.level.slice(1)}` : undefined].filter(Boolean).join(' · '),
  }));
  const filtered = query.trim().length >= 2 && suggestions ? suggestions.map(s => s.subject) : subjects;
  return <div className="pt-subject-picker">
    <label className="pt-control-label" htmlFor="pt-subject-search">Choose an exam subject</label>
    <Combobox items={choices.map(choice => choice.label)} filter={null} value={null}
      inputValue={query} onInputValueChange={onQuery}
      onValueChange={value => { const choice = choices.find(candidate => candidate.label === value); if (choice) onSelect(choice.subject.id, choice.year, choice.level); }}>
      <ComboboxInput id="pt-subject-search" aria-label="Find a subject or paper" placeholder="Find a subject or paper" showClear />
      <ComboboxContent><ComboboxEmpty>No matches. Try another subject or year.</ComboboxEmpty><ComboboxList>{(choice: string) => <ComboboxItem key={choice} value={choice}>{choice}</ComboboxItem>}</ComboboxList></ComboboxContent>
    </Combobox>
    <ToggleGroup className="pt-subject-scope" aria-label="Subject selection" value={[scope]} variant="outline" onValueChange={value => value.length > 0 && onScope(value[0] as 'mine' | 'all')}>
      <ToggleGroupItem value="mine">My subjects</ToggleGroupItem><ToggleGroupItem value="all">All subjects</ToggleGroupItem>
    </ToggleGroup>
    <div className="pt-subject-shortlist" aria-label={scope === 'mine' ? 'My subjects' : 'All subjects'}>
      {filtered.map(subject => <Button key={subject.id} variant="ghost" className="pt-subject-choice" aria-pressed={selected === subject.id}
        aria-label={`${labelFor(subject)} ${levelFor(subject)} level${subject.cycle === 'lca' ? ' · LCA' : ''}`} onClick={() => {
          const choice = suggestions?.find(candidate => candidate.subject.id === subject.id);
          onSelect(subject.id, choice?.year, choice?.level);
        }}>
        <PaperSubjectArtwork label={labelFor(subject)} />
        <span className="pt-subject-choice-copy"><strong>{labelFor(subject)}</strong><span>{levelFor(subject)} level{subject.cycle === 'lca' ? ' · LCA' : ''}</span></span>
        {selected === subject.id ? <span className="pt-selected-label">Selected</span> : <ArrowRight size={18} />}
      </Button>)}
    </div>
    {!filtered.length && <div className="pt-empty-subjects"><p>{query.trim() ? 'No matching subjects. Try another name.' : 'Your subjects will appear here once you add them to your profile.'}</p>{scope === 'mine' && <Button variant="outline" onClick={() => { onQuery(''); onScope('all'); }}>Browse all subjects</Button>}</div>}
  </div>;
}
