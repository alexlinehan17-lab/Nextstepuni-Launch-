import React, { lazy, Suspense, useState } from 'react';
import type { StudentSubjectProfile } from '../subjectData';
import type { StudySessionRecord } from '../../utils/strategyRegistry';
import { getStudyTopicOptions } from '../../services/studyTopicHistory';
import { useTopicMastery } from '../../hooks/useTopicMastery';
import ActionButton from '../ui/ActionButton';
import type { TopicHistoryActions } from './TopicDetailCard';
import './topic-history.css';
const TopicDetailCard = lazy(() => import('./TopicDetailCard'));
interface Props extends TopicHistoryActions { uid: string; profile: StudentSubjectProfile; sessions: StudySessionRecord[] }
export default function TopicHistoryPanel({ uid, profile, sessions, ...actions }: Props) {
  const [subject, setSubject] = useState(profile.subjects[0]?.subjectName ?? '');
  const [topicId, setTopicId] = useState('');
  const [open, setOpen] = useState(false);
  const mastery = useTopicMastery(uid, profile.examStartDate);
  const level = profile.subjects.find(item => item.subjectName === subject)?.level;
  const options = getStudyTopicOptions(subject, profile.examStartDate, level);
  return <section className="topic-history-panel lg:col-span-12" aria-labelledby="topic-history-heading">
    <p className="sc-eyebrow">Your subjects / Shared history</p><h3 id="topic-history-heading">A closer look at your learning.</h3>
    <label>Subject<select value={subject} onChange={event => { setSubject(event.target.value); setTopicId(''); }}>{profile.subjects.map(item => <option key={item.subjectName}>{item.subjectName}</option>)}</select></label>
    <label>Topic<select value={topicId} onChange={event => setTopicId(event.target.value)}><option value="">Whole subject</option>{options.map(item => <option key={item.id} value={item.id}>{item.name}{item.kind === 'area' ? ' · whole area' : ` · ${item.groupName}`}</option>)}</select></label>
    {!options.length && <p>This cohort’s topic map is being verified. Your saved subject history is kept.</p>}
    <ActionButton disabled={!options.length} onClick={() => setOpen(true)}>View learning record</ActionButton>
    {open && <Suspense fallback={<p role="status">Opening your learning record…</p>}><TopicDetailCard {...actions} uid={uid} subject={subject} nodeId={topicId || undefined} examDate={profile.examStartDate} level={level} sessions={sessions} mastery={mastery.canonicalMastery} onConfidence={(name, topic, confidence, id) => mastery.setTopicConfidence(name, topic, confidence, 'manual', id)} onClose={() => setOpen(false)} /></Suspense>}
  </section>;
}
