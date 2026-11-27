/** @license SPDX-License-Identifier: Apache-2.0 */
import React, { useMemo, useState } from 'react';
import { Button } from '../ui/Button';
import { SearchField } from '../ui/Field';
import { Menu } from '../ui/Menu';
import { generatedCardsForLevel } from '../MarkBank/cards/politics-and-society/factory';
import PoliticsRubricPanel from '../MarkBank/PoliticsRubricPanel';
import SourceMaterialReader from '../MarkBank/SourceMaterialReader';
import { POLITICS_EXAM_TASKS, politicsExamTopicIdsForTask } from '../../data/examTopics/registry';
import type { PoliticsRubric, SecRubricCard } from '../../types/markBank';

type PoliticsCard = SecRubricCard & { rubric: PoliticsRubric };
const cards = [...generatedCardsForLevel('higher'), ...generatedCardsForLevel('ordinary')] as PoliticsCard[];
const taskTopics = new Map(POLITICS_EXAM_TASKS.map(task => [task.id, politicsExamTopicIdsForTask(task)]));

const Task: React.FC<{ card: PoliticsCard }> = ({ card }) => {
  const [revealed, setRevealed] = useState(false);
  const [scores, setScores] = useState<Record<string, number>>({});
  return <article className="pt-politics-task" aria-label={card.questionRef}>
    <div className="pt-politics-task-head">
      <h3>{card.questionRef}</h3>
      <span className="ui-readout">{card.totalMarks} marks</span>
    </div>
    {card.stem && <p className="pt-politics-stem">{card.stem}</p>}
    <p className={`pt-politics-question ${card.section === 'C' ? '' : 'whitespace-pre-line'}`}>{card.questionText}</p>
    {card.sourceMaterial && <SourceMaterialReader subjectId={card.subjectId} year={card.year!}
      paperFileid={card.paperFileid!} source={card.sourceMaterial} />}
    <Button className="pt-politics-guide" aria-expanded={revealed} onClick={() => setRevealed(value => !value)}>
      {revealed ? 'Hide marking guide' : 'Show marking guide'}
    </Button>
    {revealed && <div className="pt-politics-rubric"><PoliticsRubricPanel card={card} scores={scores}
      onScore={(id, value) => setScores(previous => ({ ...previous, [id]: value }))} /></div>}
  </article>;
};

const PoliticsTopicFeed: React.FC<{ topicId: string }> = ({ topicId }) => {
  const [year, setYear] = useState('all');
  const [query, setQuery] = useState('');
  const [limit, setLimit] = useState(20);
  const matching = useMemo(() => cards.filter(card => taskTopics.get(card.id)?.includes(topicId))
    .sort((a, b) => b.year! - a.year! || a.questionRef.localeCompare(b.questionRef, undefined, { numeric: true })), [topicId]);
  const years = [...new Set(matching.map(card => card.year!))];
  const shown = matching.filter(card => (year === 'all' || String(card.year) === year) &&
    `${card.questionRef} ${card.questionText}`.toLowerCase().includes(query.toLowerCase()));
  return <div className="mark-bank-theme pt-politics-feed">
    <p className="pt-politics-count">{matching.length} practice tasks · {years.length} years. Each part and printed answer route keeps its original marks and sources.</p>
    <div className="pt-politics-filters">
      <Menu label="Practice year" value={year} onChange={value => { setYear(value); setLimit(20); }}
        options={[{ value: 'all', label: 'All years' }, ...years.map(value => ({ value: String(value), label: String(value) }))]} />
      <SearchField label="Search practice tasks" placeholder="Search tasks"
        value={query} onChange={event => { setQuery(event.target.value); setLimit(20); }} />
    </div>
    <p className="pt-politics-matching" aria-live="polite">{shown.length} matching tasks</p>
    {shown.slice(0, limit).map(card => <Task key={card.id} card={card} />)}
    {limit < shown.length && <Button className="pt-politics-more" onClick={() => setLimit(value => value + 20)}>Show 20 more tasks</Button>}
  </div>;
};
export default PoliticsTopicFeed;
