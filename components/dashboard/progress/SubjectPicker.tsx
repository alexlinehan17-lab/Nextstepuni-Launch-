import { useState } from 'react';
import { ChevronDown, Search, X } from 'lucide-react';
import { Checkbox } from '../../approved-ui-runtime';
import { Button } from '../../approved-ui-runtime';
import { Input } from '../../approved-ui-runtime';
import { Popover, PopoverTrigger, PopoverContent } from '../../approved-ui-runtime';
import CrewIllustration from '../../CrewIllustration';


export function SubjectPicker({ subjects, value, onChange }: { subjects: string[]; value: string[]; onChange: (subjects: string[]) => void }) {
  const [query, setQuery] = useState('');
  const visible = subjects.filter(subject => subject.toLowerCase().includes(query.toLowerCase().trim()));
  return <div className="pr-subject-picker">
    <Popover>
      <PopoverTrigger render={<Button variant="outline" className="pr-picker-trigger nsu-ink-outline" aria-label="Filter by subject" />}>
        <span>{value.length ? value.length === 1 ? value[0] : `${value.length} subjects selected` : 'All subjects'}</span><ChevronDown />
      </PopoverTrigger>
      <PopoverContent className="pr-subject-menu" align="start">
        <div className="pr-subject-search"><Search size={18} /><Input value={query} onChange={event => setQuery(event.target.value)} placeholder="Find a subject…" aria-label="Find a subject" /></div>
        <div className="pr-subject-options" role="group" aria-label="Filter by subject">{visible.map(subject => <label className="pr-subject-option" key={subject} data-selected={value.includes(subject)}>
          <Checkbox checked={value.includes(subject)} onCheckedChange={checked => onChange(checked ? [...value, subject] : value.filter(item => item !== subject))} />
          <span className="pr-subject-label">{subject}</span><CrewIllustration className="pr-subject-art" subject={subject} />
        </label>)}{!visible.length && <p className="pr-empty">No matching subjects.</p>}</div>
        <div className="pr-subject-menu-foot"><span>{value.length || 'All'} subjects</span><Button variant="ghost" size="sm" disabled={!value.length} onClick={() => onChange([])}>Clear selection</Button></div>
      </PopoverContent>
    </Popover>
    {!!value.length && <div className="pr-selected-subjects">{value.map(subject => <Button variant="ghost" key={subject} size="sm" onClick={() => onChange(value.filter(item => item !== subject))} aria-label={`Remove ${subject}`}>{subject}<X size={12} /></Button>)}</div>}
  </div>;
}
