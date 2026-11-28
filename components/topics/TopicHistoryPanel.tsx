import React, { lazy, Suspense, useState } from 'react';
import type { StudentSubjectProfile } from '../subjectData';
import type { StudySessionRecord } from '../../utils/strategyRegistry';
import { getStudyTopicOptions, sameStudySubject } from '../../services/studyTopicHistory';
import { useTopicMastery } from '../../hooks/useTopicMastery';
import { List, Row } from '../ui/List';
import SubjectAvatar from '../SubjectAvatar';
import type { TopicHistoryActions } from './TopicDetailCard';
import './topic-history.css';
const TopicDetailCard = lazy(() => import('./TopicDetailCard'));
interface Props extends TopicHistoryActions {
  uid: string; profile: StudentSubjectProfile; sessions: StudySessionRecord[];
  /** Minutes per subject in the period, for the time beside each row (My Progress). */
  minutes?: Array<{ label: string; value: number }>;
}
const formatTime = (minutes: number) => minutes >= 90 ? `${Math.floor(minutes / 60)}h${minutes % 60 ? ` ${minutes % 60}m` : ''}` : `${minutes} min`;

/** Your subjects, each a row with its character that opens its record, topic by
 *  topic (c-progress.html, "A closer look at your learning."). The record lets
 *  the student choose a topic inside it. */
export default function TopicHistoryPanel({ uid, profile, sessions, minutes = [], ...actions }: Props) {
  const [subject, setSubject] = useState<string | null>(null);
  const mastery = useTopicMastery(uid, profile.examStartDate);
  const total = minutes.reduce((sum, item) => sum + item.value, 0);
  const timeFor = (name: string) => minutes.filter(item => sameStudySubject(item.label, name)).reduce((sum, item) => sum + item.value, 0);
  const rows = profile.subjects.map(item => ({ name: item.subjectName, level: item.level, time: timeFor(item.subjectName),
    ready: getStudyTopicOptions(item.subjectName, profile.examStartDate, item.level).length > 0 }))
    .sort((a, b) => b.time - a.time || a.name.localeCompare(b.name));
  const level = profile.subjects.find(item => item.subjectName === subject)?.level;
  return <div className="topic-history-panel" aria-label="A closer look at your learning">
    <List label="Your subjects">
      {rows.map(row => <Row key={row.name} title={row.name} art={<SubjectAvatar subject={row.name} bare />}
        meta={!row.ready ? 'This topic map is being verified. Your history is kept.' : row.time && total ? `${Math.round(row.time / total * 100)}% of your time` : 'No time yet in this period'}
        value={row.time ? formatTime(row.time) : undefined}
        label={row.ready ? `View learning record: ${row.name}` : undefined}
        onPress={row.ready ? () => setSubject(row.name) : undefined} />)}
    </List>
    {subject && <Suspense fallback={<p role="status" className="t-meta">Opening your learning record…</p>}><TopicDetailCard {...actions} uid={uid} subject={subject} examDate={profile.examStartDate} level={level} sessions={sessions} mastery={mastery.canonicalMastery} onConfidence={(name, topic, confidence, id) => mastery.setTopicConfidence(name, topic, confidence, 'manual', id)} onClose={() => setSubject(null)} /></Suspense>}
  </div>;
}
