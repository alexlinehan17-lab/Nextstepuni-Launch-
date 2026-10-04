import React, { useState } from 'react';
import { ArrowRight, ArrowUpRight } from 'lucide-react';
import { Button, Input } from '../approved-ui-runtime';
import SubjectAvatar from '../SubjectAvatar';
import { formatStudyTime } from '../../utils/studyTime';
import { subjectLearningDetails, confidenceLabel, levelLabel } from './learningRecordModel';
import type { StudentSubjectProfile } from '../subjectData';
import type { useTopicMastery } from '../../hooks/useTopicMastery';
import type { StudySessionRecord } from '../../utils/strategyRegistry';

interface Props {
  profile: StudentSubjectProfile;
  sessions: StudySessionRecord[];
  mastery: ReturnType<typeof useTopicMastery>;
  onOpenRecord: (subject: string, nodeId?: string) => void;
  onBrowseTopics: (subject: string) => void;
  onStudy: (subject: string) => void;
  canStudy: (subject: string) => boolean;
}

export default function SubjectBoardPanel({ profile, sessions, mastery, onOpenRecord, onBrowseTopics, onStudy, canStudy }: Props) {
  const [query, setQuery] = useState('');
  const subjects = profile.subjects.filter(subject => subject.subjectName.toLocaleLowerCase().includes(query.trim().toLocaleLowerCase()));
  return <>
    <section className="wr-section-intro"><div><p className="wr-eyebrow">{profile.subjects.length} subjects / Your subject board</p><h2>Your subjects.<br /><em>Your next moves.</em></h2></div><p>Start a session, revisit a topic,<br />or see your learning record.</p></section>
    {profile.subjects.length > 0 && <label className="wr-board-search">Find a subject<Input type="search" value={query} onChange={event => setQuery(event.target.value)} placeholder="Search your subjects" /></label>}
    <div className="wr-subjects">{subjects.map((subject, index) => {
      const { activity, latest } = subjectLearningDetails(subject, profile.examStartDate, sessions, mastery);
      const current = subject.currentGrade ?? subject.currentBand;
      const target = subject.targetGrade ?? subject.targetBand;
      return <article className="wr-subject-card" key={subject.subjectName} aria-label={`${subject.subjectName} subject card`}>
        <div className="wr-subject-top"><span className="wr-eyebrow">{String(index + 1).padStart(2, '0')} / {levelLabel(subject.level)}</span><SubjectAvatar subject={subject.subjectName} className="wr-subject-art" /></div>
        <h3>{subject.subjectName}</h3>
        {current && target ? <div className="wr-subject-grade"><span>{current}</span><ArrowRight size={16} /><strong>{target}</strong><small>your target</small></div> : <p className="wr-muted">Your grades can be set in Settings.</p>}
        <div className="wr-rule" /><dl><div><dt>Recorded study</dt><dd>{formatStudyTime(activity.seconds)}</dd></div><div><dt>Latest topic confidence</dt><dd>{confidenceLabel(latest?.entry?.confidence)}</dd></div></dl>
        <p className="wr-subject-topic">{latest ? latest.option.name : 'Open your topics to record how they feel.'}</p>
        <div className="wr-card-actions"><Button variant="outline" className="nsu-ink-outline" size="sm" onClick={() => onOpenRecord(subject.subjectName)}>Learning record <ArrowUpRight size={15} /></Button><Button variant="ghost" size="icon-sm" aria-label={`Study ${subject.subjectName}`} disabled={!canStudy(subject.subjectName)} onClick={() => onStudy(subject.subjectName)}><ArrowRight size={18} /></Button></div>
        <Button variant="link" className="wr-topic-link" onClick={() => onBrowseTopics(subject.subjectName)}>Browse topics</Button>
      </article>;
    })}</div>
    {!subjects.length && <div className="wr-empty"><p>{profile.subjects.length ? 'No subjects match your search.' : 'Add your subjects in Settings to begin.'}</p>{query && <Button variant="link" onClick={() => setQuery('')}>Clear search</Button>}</div>}
  </>;
}
