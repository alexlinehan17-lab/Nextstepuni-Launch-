import React, { Suspense, lazy, useEffect, useId, useMemo, useState } from 'react';
import { ArrowUpRight } from 'lucide-react';
import { Button, Combobox, ComboboxInput, ComboboxContent, ComboboxEmpty, ComboboxList, ComboboxItem, ToggleGroup, ToggleGroupItem } from '../approved-ui-runtime';
import SubjectAvatar from '../SubjectAvatar';
import { formatStudyTime } from '../../utils/studyTime';
import { uniqueStudySessions } from '../../services/studyTopicHistory';
import { subjectLearningDetails, confidenceLabel, levelLabel, compactStudyTime } from './learningRecordModel';
import type { StudentSubjectProfile } from '../subjectData';
import type { useTopicMastery } from '../../hooks/useTopicMastery';
import type { StudySessionRecord } from '../../utils/strategyRegistry';
import type { UnifiedConfidence } from '../../types';

interface Props {
  uid: string;
  profile: StudentSubjectProfile;
  sessions: StudySessionRecord[];
  mastery: ReturnType<typeof useTopicMastery>;
  onOpenRecord: (subject: string, nodeId?: string) => void;
  onResults?: () => void;
}

const QuestionEvidenceSummary = lazy(() => import('./QuestionEvidenceSummary'));
export default function LearningLedgerPanel({ uid, profile, sessions, mastery, onOpenRecord, onResults }: Props) {
  const [chosenSubject, setChosenSubject] = useState(profile.subjects[0]?.subjectName ?? '');
  const [limit, setLimit] = useState(10);
  const subject = profile.subjects.find(item => item.subjectName === chosenSubject) ?? profile.subjects[0];
  const subjectNames = profile.subjects.map(item => item.subjectName);
  const id = useId();
  useEffect(() => { if (subject && subject.subjectName !== chosenSubject) setChosenSubject(subject.subjectName); }, [chosenSubject, subject]);
  const records = useMemo(() => uniqueStudySessions(sessions).sort((a, b) => b.completedAt - a.completedAt), [sessions]);
  const seconds = records.reduce((sum, record) => sum + Math.max(0, record.actualSeconds), 0);
  const details = subject ? subjectLearningDetails(subject, profile.examStartDate, sessions, mastery) : undefined;
  const topic = details?.latest?.option ?? details?.options.find(option => option.kind === 'topic');
  const entry = topic && subject ? mastery.getCanonicalSubjectTopics(subject.subjectName)[topic.id] : undefined;

  return <>
    <section className="wr-ledger-opening"><div><p className="wr-eyebrow">Your learning record</p><h2>The small steps.<br /><em>On record.</em></h2><p>A clear view of the work you’ve put in.</p></div><div className="wr-ledger-total"><strong aria-label={formatStudyTime(seconds)}>{compactStudyTime(seconds)}</strong><span>recorded study / {records.length} saved {records.length === 1 ? 'session' : 'sessions'}</span></div></section>
    <div className="wr-record-layout"><section className="wr-record-list"><header className="wr-section-heading"><span>01</span><h3>Your subjects, on record.</h3></header>{profile.subjects.map((item, index) => {
      const activity = subjectLearningDetails(item, profile.examStartDate, sessions, mastery).activity;
      return <Button variant="ghost" className="wr-ledger-row" key={item.subjectName} onClick={() => onOpenRecord(item.subjectName)}><span className="wr-row-number">{String(index + 1).padStart(2, '0')}</span><SubjectAvatar subject={item.subjectName} /><span className="wr-row-subject"><strong>{item.subjectName}</strong><small>{activity.count} saved {activity.count === 1 ? 'session' : 'sessions'} · {levelLabel(item.level)}</small></span><span className="wr-row-time">{formatStudyTime(activity.seconds)}</span><ArrowUpRight size={18} /></Button>;
    })}{!profile.subjects.length && <p className="wr-muted">Add your subjects in Settings to see their records here.</p>}
      {onResults && <div className="wr-results-link"><h4>Your grades, on record.</h4><p className="wr-muted">Review your results and add a single grade or a full mock.</p><Button variant="outline" className="nsu-ink-outline" onClick={onResults}>Results and grades <ArrowUpRight size={16} /></Button></div>}
    </section>
    <section className="wr-confidence"><header className="wr-section-heading"><span>02</span><h3>How does it feel?</h3></header>{subject ? <>
      <div className="wr-subject-chooser"><label htmlFor={id}>Look at a subject</label><Combobox items={subjectNames} value={subject.subjectName} onValueChange={value => { if (value) setChosenSubject(value); }}><ComboboxInput id={id} showClear={false} /><ComboboxContent className="nsu-floating-layer"><ComboboxEmpty>No subjects found.</ComboboxEmpty><ComboboxList>{(item: string) => <ComboboxItem key={item} value={item}>{item}</ComboboxItem>}</ComboboxList></ComboboxContent></Combobox></div>
      {topic ? <><p className="wr-topic-name">{topic.name}</p><ToggleGroup value={[entry?.confidence ?? 'not-started']} onValueChange={values => { if (values[0]) mastery.setTopicConfidence(subject.subjectName, topic.name, values[0] as UnifiedConfidence, 'manual', topic.id); }} className="wr-confidence-controls" aria-label="Topic confidence">{(['not-started', 'shaky', 'solid'] as const).map(value => <ToggleGroupItem key={value} value={value}>{confidenceLabel(value)}</ToggleGroupItem>)}</ToggleGroup>{entry && <p className="wr-muted">Updated {new Date(entry.updatedAt).toLocaleDateString('en-IE')}</p>}</> : <p className="wr-muted">Topic confidence is available when this subject has a verified curriculum map.</p>}
      <p className="wr-muted">Your confidence is kept separately from study time and question marks.</p><div className="wr-rule" /><h4>Question evidence</h4><Suspense fallback={<p className="wr-muted" role="status">Opening question evidence…</p>}><QuestionEvidenceSummary uid={uid} subject={subject.subjectName} nodeId={topic?.id} examDate={profile.examStartDate} level={subject.level} /></Suspense><Button variant="link" onClick={() => onOpenRecord(subject.subjectName, topic?.id)}>Open {topic ? 'this topic' : 'the subject'} <ArrowUpRight size={16} /></Button>
    </> : <p className="wr-muted">Your subjects will appear here after setup.</p>}</section></div>
    <section className="wr-recent"><header className="wr-section-heading"><span>03</span><h3>Recently, you made time for…</h3></header><div className="wr-history">{records.slice(0, limit).map(record => <Button variant="ghost" className="wr-history-row" key={record.id} onClick={() => onOpenRecord(record.subject)}><time dateTime={record.date}>{new Date(record.completedAt).toLocaleDateString('en-IE', { day: '2-digit', month: 'short' })}</time><strong>{record.subject}</strong><span>{record.sessionType.replace('-', ' ')}</span><span>{formatStudyTime(Math.max(0, record.actualSeconds))}</span><ArrowUpRight size={16} /></Button>)}</div>
      {!records.length && <p className="wr-muted">No saved sessions yet. Your completed study will build a record here.</p>}
      {records.length > limit && <Button variant="link" onClick={() => setLimit(value => value + 10)}>Show more sessions ({records.length - limit} remaining)</Button>}
    </section>
  </>;
}
