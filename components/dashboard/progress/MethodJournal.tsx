import { useState } from 'react';
import { List, Row } from '../../ui/List';
import { Menu } from '../../ui/Menu';
import SubjectAvatar from '../../SubjectAvatar';
import { Section } from './ProgressParts';
import type { MethodRecord } from './progressData';

/** "The ways you showed up.": one method at a time from a menu, its description,
 *  and each recorded use as a row with the subject's character. */
export function MethodJournal({ methods, period, className = '' }: { methods: MethodRecord[]; period: string; className?: string }) {
  const [selected, setSelected] = useState<string>();
  const current = methods.find(method => method.id === selected) ?? methods[0];
  const prompts = current?.entries.filter(entry => entry.evidence === 'prompt').length ?? 0;
  const reported = current?.entries.filter(entry => entry.evidence === 'reported').length ?? 0;
  const entries = (count: number) => `${count} ${count === 1 ? 'entry' : 'entries'}`;
  return <Section label={`Learning methods · ${period}`} title="The ways you showed up." className={`pr-method-section mp-methods ${className}`.trim()}>
    <p className="t-sub">{methods.length ? `${methods.length} ${methods.length === 1 ? 'method' : 'methods'} in your study record. Small choices worth noticing.` : 'Your recorded study methods will appear here.'}</p>
    {!current ? <div className="mp-empty"><p className="t-body">No techniques tracked yet</p><p className="t-meta">Complete a study session or record the methods you used in a debrief.</p></div> : <>
      <Menu label="Choose a method" block value={current.id} onChange={setSelected} detail={entries(current.entries.length)}
        options={methods.map(method => ({ value: method.id, label: method.name }))} />
      <h3 className="sr-only">{current.name}</h3>
      <p className="t-sub">{current.description}</p>
      <p className="t-meta">{`${entries(current.entries.length)} recorded · ${prompts} ${prompts === 1 ? 'prompt' : 'prompts'} · ${reported} self-reported`}</p>
      <List label={`${current.name}: recorded uses`}>
        {current.entries.map(entry => <Row key={entry.id} title={entry.subject} art={<SubjectAvatar subject={entry.subject} bare />}
          meta={`${new Date(`${entry.date}T12:00:00`).toLocaleDateString('en-IE', { weekday: 'short', day: 'numeric', month: 'short' })} · ${entry.sessionType === 'new-learning' ? 'New learning' : entry.sessionType === 'practice' ? 'Practice' : 'Revision'} · ${entry.evidence === 'prompt' ? 'Prompt shown' : 'Self-reported use'}`}
          value={`${entry.minutes} min`} />)}
      </List>
    </>}
    <p className="t-meta pr-evidence-note">Prompts record exposure to an approach; debriefs record self-reported use. Neither count measures mastery.</p>
  </Section>;
}
