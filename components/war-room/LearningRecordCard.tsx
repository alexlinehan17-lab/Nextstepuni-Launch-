import React, { lazy, Suspense } from 'react';
import SignatureCard from '../ui/SignatureCard';
import KobraScope, { Button } from '../approved-ui-runtime';
import '../topics/topic-history.css';
import { examinationYearFromDate, resolveCurriculumSpecification } from '../../curriculumRegistry';
import { recordedSubjectActivity } from '../../services/studyTopicHistory';
import { formatStudyTime } from '../../utils/studyTime';
import type { TopicHistoryActions } from '../topics/TopicDetailCard';
import type { useTopicMastery } from '../../hooks/useTopicMastery';
import type { StudySessionRecord } from '../../utils/strategyRegistry';

const TopicDetailCard = lazy(() => import('../topics/TopicDetailCard'));
interface Props extends TopicHistoryActions {
  uid: string; subject: string; nodeId?: string; level?: string; examDate?: string | null;
  sessions: StudySessionRecord[]; mastery: ReturnType<typeof useTopicMastery>; onClose: () => void;
}
export default function LearningRecordCard({ uid, subject, nodeId, level, examDate, sessions, mastery, onClose, onStudyTopic, onPracticeTopic }: Props) {
  const spec = resolveCurriculumSpecification(subject, examinationYearFromDate(examDate));
  if (spec?.status === 'verified') return <Suspense fallback={<SignatureCard open wide onClose={onClose} title="Your learning record." eyebrow={`${subject} / Your learning record`} footer={<KobraScope sound={false}><Button variant="outline" onClick={onClose}>Back to War Room</Button></KobraScope>}><p role="status">Opening your record…</p></SignatureCard>}><TopicDetailCard uid={uid} subject={subject} nodeId={nodeId} level={level} examDate={examDate} sessions={sessions} mastery={mastery.canonicalMastery} onConfidence={(name, topic, value, id) => mastery.setTopicConfidence(name, topic, value, 'manual', id)} onStudyTopic={onStudyTopic} onPracticeTopic={onPracticeTopic} onClose={onClose} /></Suspense>;
  const activity = recordedSubjectActivity(sessions, subject);
  return <SignatureCard open onClose={onClose} title="The subject, on record." eyebrow={`${subject} / Your learning record`} footer={<KobraScope sound={false}><Button variant="outline" onClick={onClose}>Back to War Room</Button></KobraScope>}>
    <p className="wr-muted">A verified topic map is not available for this subject yet. Your saved study remains on record.</p><section className="topic-history-section"><h3>Recorded activity</h3><strong className="topic-history-total">{formatStudyTime(activity.seconds)}</strong><p>{activity.count} saved {activity.count === 1 ? 'session' : 'sessions'}.</p><ul>{[...activity.records].sort((a, b) => b.completedAt - a.completedAt).map(record => <li key={record.id}><time dateTime={record.date}>{new Date(record.completedAt).toLocaleDateString('en-IE')}</time><span>{record.sessionType.replace('-', ' ')}</span><strong>{formatStudyTime(record.actualSeconds)}</strong></li>)}</ul></section>
  </SignatureCard>;
}
