/** @license SPDX-License-Identifier: Apache-2.0 */
import React, { useMemo, useState } from 'react';
import { generatedCardsForLevel } from '../MarkBank/cards/politics-and-society/factory';
import PoliticsRubricPanel from '../MarkBank/PoliticsRubricPanel';
import SourceMaterialReader from '../MarkBank/SourceMaterialReader';
import { POLITICS_EXAM_TASKS, politicsExamTopicIdsForTask } from '../../data/examTopics/registry';
import type { PoliticsRubric, SecRubricCard } from '../../types/markBank';

type PoliticsCard = SecRubricCard & { rubric: PoliticsRubric };
const cards = [...generatedCardsForLevel('higher'), ...generatedCardsForLevel('ordinary')] as PoliticsCard[];
const taskTopics = new Map(POLITICS_EXAM_TASKS.map(task => [task.id, politicsExamTopicIdsForTask(task)]));
const control = 'rounded-lg border-2 border-[#383838] bg-white px-3 py-2 text-sm font-semibold text-[#1a1a1a] hover:border-[#F26B1F] focus-visible:outline-2 focus-visible:outline-[#F26B1F]';

const Task: React.FC<{ card: PoliticsCard }> = ({ card }) => {
  const [revealed, setRevealed] = useState(false);
  const [scores, setScores] = useState<Record<string, number>>({});
  return <article className="border-b border-[#d8d3cc] py-6" aria-label={card.questionRef}>
    <div className="mb-3 flex items-start justify-between gap-4">
      <h3 className="font-semibold text-[#1a1a1a]">{card.questionRef}</h3>
      <span className="shrink-0 text-sm tabular-nums">{card.totalMarks} marks</span>
    </div>
    {card.stem && <p className="mb-3 whitespace-pre-line text-sm leading-relaxed">{card.stem}</p>}
    <p className={`mb-4 leading-relaxed ${card.section === 'C' ? '' : 'whitespace-pre-line'}`}>{card.questionText}</p>
    {card.sourceMaterial && <SourceMaterialReader subjectId={card.subjectId} year={card.year!}
      paperFileid={card.paperFileid!} source={card.sourceMaterial} />}
    <button className={`${control} mt-4`} aria-expanded={revealed} onClick={() => setRevealed(value => !value)}>
      {revealed ? 'Hide marking guide' : 'Show marking guide'}
    </button>
    {revealed && <div className="mt-4"><PoliticsRubricPanel card={card} scores={scores}
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
  return <div className="mark-bank-theme">
    <p className="mb-4 text-sm text-[#5a5550]">{matching.length} practice tasks · {years.length} years. Each part and printed answer route keeps its original marks and sources.</p>
    <div className="flex flex-wrap gap-3">
      <select className={control} aria-label="Practice year" value={year} onChange={event => { setYear(event.target.value); setLimit(20); }}>
        <option value="all">All years</option>{years.map(value => <option key={value}>{value}</option>)}
      </select>
      <input className={control} type="search" aria-label="Search practice tasks" placeholder="Search tasks"
        value={query} onChange={event => { setQuery(event.target.value); setLimit(20); }} />
    </div>
    <p className="mt-3 text-sm" aria-live="polite">{shown.length} matching tasks</p>
    {shown.slice(0, limit).map(card => <Task key={card.id} card={card} />)}
    {limit < shown.length && <button className={`${control} mt-6`} onClick={() => setLimit(value => value + 20)}>Show 20 more tasks</button>}
  </div>;
};
export default PoliticsTopicFeed;
