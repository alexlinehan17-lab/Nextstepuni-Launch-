/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React, { useMemo, useState } from 'react';
import { type StudyReflection } from '../types';
import SignatureCard from './ui/SignatureCard';
import ActionButton from './ui/ActionButton';

const SESSION_LABELS: Record<string, string> = { 'new-learning': 'New Learning', practice: 'Practice', revision: 'Revision' };
interface StudyJournalModalProps { isOpen: boolean; onClose: () => void; reflections: StudyReflection[] }

const StudyJournalModal: React.FC<StudyJournalModalProps> = ({ isOpen, onClose, reflections }) => {
  const [subjectFilter, setSubjectFilter] = useState<string | null>(null);
  const subjects = useMemo(() => Array.from(new Set(reflections.map(reflection => reflection.subjectName))).sort(), [reflections]);
  const grouped = useMemo(() => {
    const list = subjectFilter ? reflections.filter(reflection => reflection.subjectName === subjectFilter) : reflections;
    const map = new Map<string, StudyReflection[]>();
    for (const reflection of [...list].sort((a,b) => b.timestamp - a.timestamp)) {
      const entries = map.get(reflection.dateKey) || [];
      entries.push(reflection);
      map.set(reflection.dateKey, entries);
    }
    return Array.from(map.entries());
  }, [reflections,subjectFilter]);
  const formatDate = (dateKey: string) => {
    const parts = dateKey.split('-');
    return new Date(Number(parts[0]),Number(parts[1]) - 1,Number(parts[2])).toLocaleDateString('en-IE',{ weekday: 'short', month: 'short', day: 'numeric' });
  };
  const totalPoints = reflections.reduce((sum,reflection) => sum + reflection.pointsEarned,0);
  return <SignatureCard open={isOpen} onClose={onClose} title="Study Journal" eyebrow="Your study" description={`${reflections.length} reflections · ${totalPoints} JP earned`} footer={<>
    <span className="sc-small">Private to you</span><ActionButton onClick={onClose}>Back to study</ActionButton>
  </>}>
    {subjects.length > 1 && <div className="sc-filters" role="group" aria-label="Filter reflections by subject">
      <button type="button" className="sc-filter" aria-pressed={!subjectFilter} onClick={() => setSubjectFilter(null)}>All</button>
      {subjects.map(subject => <button key={subject} type="button" className="sc-filter" aria-pressed={subjectFilter === subject} onClick={() => setSubjectFilter(subjectFilter === subject ? null : subject)}>{subject}</button>)}
    </div>}
    {grouped.length === 0 ? <div className="sc-journal-empty"><p className="sc-eyebrow">Your first entry</p><h3>A place to look back.</h3><p>Complete a study session and keep a thought about what worked. Your reflections will appear here.</p></div> : grouped.map(([dateKey,entries]) => <section key={dateKey} className="sc-journal-group">
      <p className="sc-eyebrow">{formatDate(dateKey)}</p>
      {entries.map((entry,index) => <article key={`${entry.blockId}-${index}`} className="sc-journal-entry"><header><h3>{entry.subjectName}</h3><span className="sc-small">{SESSION_LABELS[entry.sessionType]} · +{entry.pointsEarned} JP</span></header><p>{entry.reflection}</p></article>)}
    </section>)}
  </SignatureCard>;
};
export default StudyJournalModal;
