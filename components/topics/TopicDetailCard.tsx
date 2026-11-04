import React, { useState } from 'react';
import SignatureCard from '../ui/SignatureCard';
import ActionButton from '../ui/ActionButton';
import { evidenceForCurriculumNode } from '../PaperTrail/topicEvidence';
import { recordedSubjectActivity, recordedTopicActivity, getStudyTopicOptions, unallocatedStudySeconds, studyTopicSelection } from '../../services/studyTopicHistory';
import { examinationYearFromDate, resolveCurriculumSpecification } from '../../curriculumRegistry';
import { formatStudyTime } from '../../utils/studyTime';
import type { StudySessionRecord } from '../../utils/strategyRegistry';
import type { TopicMasteryV2, UnifiedConfidence } from '../../types';
import type { StudyTopicSelection } from '../../types/studyTopics';
import { canonicalMasteryKey } from '../../services/topicMasteryMigration';
import './topic-history.css';

export interface TopicHistoryActions {
  onStudyTopic?: (selection: StudyTopicSelection) => void;
  onPracticeTopic?: (subjectId: string, topicId: string, level?: string) => void;
}
interface Props extends TopicHistoryActions {
  uid?: string; subject: string; nodeId?: string; examDate?: string | null; level?: string;
  sessions: StudySessionRecord[]; mastery?: TopicMasteryV2;
  onConfidence?: (subject: string, name: string, confidence: UnifiedConfidence, nodeId: string) => void;
  onClose: () => void;
}
export default function TopicDetailCard({ uid, subject, nodeId, examDate, level, sessions, mastery, onConfidence, onClose, onStudyTopic, onPracticeTopic }: Props) {
  const [showPractice, setShowPractice] = useState(false);
  const [focusedNodeId, setFocusedNodeId] = useState(nodeId ?? '');
  const [recordLimit, setRecordLimit] = useState(10);
  const spec = resolveCurriculumSpecification(subject, examinationYearFromDate(examDate));
  if (!spec || spec.status !== 'verified') return null;
  const node = spec.groups.flatMap(group => [{ id: group.id, title: group.title }, ...group.topics]).find(item => item.id === focusedNodeId);
  const activity = focusedNodeId ? recordedTopicActivity(sessions, spec, focusedNodeId) : undefined;
  const total = recordedSubjectActivity(sessions, subject);
  const evidence = evidenceForCurriculumNode(uid, spec, focusedNodeId || undefined, level);
  const confidence = focusedNodeId ? mastery?.topics[canonicalMasteryKey(spec.id, focusedNodeId)] : undefined;
  const selection = studyTopicSelection(subject, focusedNodeId ? [focusedNodeId] : [], examDate, level);
  const records = activity?.records ?? total.records.map(session => ({ session, seconds: session.actualSeconds })).sort((a, b) => b.session.completedAt - a.session.completedAt);
  return <SignatureCard open wide onClose={onClose} eyebrow={`${spec.subjectName} / Your learning record`} title={node?.title ?? 'The subject, on record.'} description={spec.title}
    footer={<><ActionButton intent="secondary" disabled={!evidence.topics.some(topic => topic.count > 0) || !onPracticeTopic} onClick={() => setShowPractice(value => !value)}>Practise questions</ActionButton><ActionButton intent="accent" disabled={!selection || !onStudyTopic} onClick={() => { if (selection) onStudyTopic?.(selection); }}>Start studying</ActionButton></>}>
    <label className="topic-record-picker">Look at<select value={focusedNodeId} onChange={event => { setFocusedNodeId(event.target.value); setShowPractice(false); setRecordLimit(10); }}><option value="">Whole subject</option>{getStudyTopicOptions(subject, examDate, level).map(option => <option value={option.id} key={option.id}>{option.name}{option.kind === 'area' ? ' · whole area' : ` · ${option.groupName}`}</option>)}</select></label>
    {node && <section className="topic-history-section"><h3>Your confidence</h3><p>How this topic feels to you.</p><div className="topic-confidence-options">{(['not-started', 'shaky', 'solid'] as const).map(value => <button key={value} type="button" aria-pressed={(confidence?.confidence ?? 'not-started') === value} disabled={!onConfidence} onClick={() => onConfidence?.(subject, node.title, value, node.id)}>{value === 'not-started' ? 'Not started' : value === 'shaky' ? 'Shaky' : 'Solid'}</button>)}</div>{confidence && <p>Updated {new Date(confidence.updatedAt).toLocaleDateString('en-IE')}</p>}</section>}
    <section className="topic-history-section"><h3>Recorded activity</h3><strong className="topic-history-total">{formatStudyTime(activity?.seconds ?? total.seconds)}</strong><p>{records.length} saved session{records.length === 1 ? '' : 's'}{node ? ' for this topic' : ' for this subject'}.</p>
      <p>{formatStudyTime(unallocatedStudySeconds(sessions, subject))} of subject time has no recorded topics.</p>
      <ul>{records.slice(0, recordLimit).map(({ session, seconds }) => <li key={session.id}><time dateTime={session.date}>{new Date(session.completedAt).toLocaleDateString('en-IE')}</time><span>{session.sessionType.replace('-', ' ')}</span><strong>{formatStudyTime(seconds)}</strong></li>)}</ul>
      {records.length > recordLimit && <button type="button" className="crew-link" onClick={() => setRecordLimit(value => value + 10)}>Show more sessions ({records.length - recordLimit} remaining)</button>}
    </section>
    <section className="topic-history-section"><h3>Question evidence</h3><p>{evidence.marks.length ? `${evidence.accuracy}% average self-mark · ${evidence.marks.length} scored question${evidence.marks.length === 1 ? '' : 's'}. Latest: ${new Date(evidence.marks[0].ts).toLocaleDateString('en-IE')}.` : 'No self-marked questions recorded here yet.'}</p><p>{evidence.reviewed.length} question cards reviewed{evidence.reviewed.length ? ` · latest ${new Date(Math.max(...evidence.reviewed.map(card => card.lastTs))).toLocaleDateString('en-IE')}` : ''}.</p><p>Topic Atlas self-marks and review cards on this device. Kept separately from confidence and study time.</p>
      {showPractice && <ul className="topic-practice-links">{evidence.topics.map(topic => <li key={topic.subtopicId}><button type="button" disabled={!topic.count} onClick={() => onPracticeTopic?.(evidence.practiceSubjectId, topic.subtopicId, level?.toLowerCase())}>{topic.label} <span>{topic.count} mapped questions →</span></button></li>)}</ul>}
      {!evidence.topics.some(topic => topic.count > 0) && <p>No questions are mapped to this topic yet. You can still study it.</p>}
    </section>
  </SignatureCard>;
}
