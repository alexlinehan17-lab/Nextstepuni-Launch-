import React, { useId, useMemo } from 'react';
import { Combobox, ComboboxInput, ComboboxContent, ComboboxList, ComboboxItem, ComboboxEmpty } from '../approved-ui-runtime';
import { getStudyTopicOptions, type StudyTopicOption } from '../../services/studyTopicHistory';

interface Props {
  subject: string; examDate?: string | null; level?: string;
  selected: string[]; onChange: (ids: string[]) => void;
}

export default function StudyTopicPicker({ subject, examDate, level, selected, onChange }: Props) {
  const id = useId();
  const options = useMemo(() => getStudyTopicOptions(subject, examDate, level), [subject, examDate, level]);
  if (!subject) return null;
  if (!options.length) return <p className="ks-copy">You can record subject time. Topic selection will be available when this cohort’s map is verified.</p>;
  const value = options.filter(option => selected.includes(option.id));
  return <div className="study-topic-picker">
    <label htmlFor={id}>Topics for this session <span className="ks-copy">(optional)</span></label>
    <Combobox items={options} multiple value={value}
      itemToStringLabel={(option: StudyTopicOption) => option.kind === 'area' ? `${option.name} · whole area` : `${option.name} · ${option.groupName}`}
      isItemEqualToValue={(a: StudyTopicOption, b: StudyTopicOption) => a.id === b.id}
      onValueChange={(items: StudyTopicOption[]) => onChange(items.map(item => item.id))}>
      <ComboboxInput id={id} placeholder="Search your syllabus…" />
      <ComboboxContent><ComboboxEmpty>No matching topics.</ComboboxEmpty><ComboboxList>
        {(option: StudyTopicOption) => <ComboboxItem key={option.id} value={option}>{option.name}<small>{option.kind === 'area' ? 'Whole area' : option.groupName}</small></ComboboxItem>}
      </ComboboxList></ComboboxContent>
    </Combobox>
    {value.length > 0 && <ul aria-label="Selected study topics" className="study-topic-chips">{value.map(option => <li key={option.id}><button type="button" onClick={() => onChange(selected.filter(topicId => topicId !== option.id))} aria-label={`Remove ${option.name}`}>{option.name} <span aria-hidden="true">×</span></button></li>)}</ul>}
    <p className="ks-copy">Time is shared between your selected topics. You can adjust the split when you finish.</p>
  </div>;
}
