import type { TopicHistoryActions } from './topics/TopicDetailCard';
import { recordedSubjectActivity, sameStudySubject, studyTopicSelection } from '../services/studyTopicHistory';
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect, useMemo, useState } from 'react';
import { collection, doc, getDoc, getDocs } from 'firebase/firestore';
import { db } from '../firebase';
import {
  type StudentSubjectProfile,
  type TimetableCompletions,
  getBlockId,
} from './subjectData';
import {
  allocateSessions,
  computeSubjectPriorities,
  computeWeeksUntilExam,
  generateWeeklyTimetable,
  type SubjectSM2State,
} from './timetableAlgorithm';
import { type DebriefEntry } from './StudyDebrief';
import { type StudySessionRecord } from '../utils/strategyRegistry';
import { parseDateKey, startOfWeek, toDateKey } from '../utils/weekDates';
import { useLocalDateKey } from '../hooks/useLocalDateKey';
import { useInnovationData } from '../contexts/InnovationDataContext';
import {
  type MockResult,
  type TopicEntry,
  type TopicMap,
  computeCurrentTotal,
} from './war-room/warRoomShared';
import BriefingPanel from './war-room/BriefingPanel';
import CountdownPanel from './war-room/CountdownPanel';
import CoveragePanel from './war-room/CoveragePanel';
import SubjectBoardPanel from './war-room/SubjectBoardPanel';
import LearningLedgerPanel from './war-room/LearningLedgerPanel';
import LearningRecordCard from './war-room/LearningRecordCard';
import SignatureCard from './ui/SignatureCard';
import KobraScope, { Button, Tabs, TabsContent, TabsList, TabsTrigger } from './approved-ui-runtime';
import './war-room/war-room.css';
import TrajectoryPanel from './war-room/TrajectoryPanel';
import { useOptionalProgress } from '../contexts/ProgressContext';
import { DEMO_STUDENT_UID } from '../data/devStudent';
import { type ProgressDocument } from '../services/progressRepository';

export interface WarRoomStudyBlock {
  subject: string;
  sessionType: 'new-learning' | 'practice' | 'revision';
  durationMinutes: number;
  dateKey: string;
  blockId: string;
}

interface WarRoomProps extends TopicHistoryActions {
  uid: string;
  profile: StudentSubjectProfile;
  timetableCompletions: TimetableCompletions;
  todayBlocks?: WarRoomStudyBlock[];
  skippedSessions?: string[];
  onStudyNow?: (block: WarRoomStudyBlock) => void;
  /** Compatibility entry for links that previously opened Syllabus X-Ray. */
  initialMode?: WorkspaceMode;
  initialReviewPanel?: ReviewPanelId;
}

type WorkspaceMode = 'focus' | 'review';
type ReviewPanelId = 'subjects' | 'trajectory' | 'time';

type WarRoomPanel = 'today' | 'subjects' | 'record' | 'time';
const PANELS: { id: WarRoomPanel; label: string }[] = [
  { id: 'today', label: 'Today' }, { id: 'subjects', label: 'Subjects' },
  { id: 'record', label: 'Learning record' }, { id: 'time', label: 'Time plan' },
];

const EMPTY_STUDY_SESSIONS: StudySessionRecord[] = [];
const EMPTY_DEBRIEFS: DebriefEntry[] = [];
const EMPTY_PROGRESS_DOC: ProgressDocument = {};

function getCurrentWeekDateKeys(reference = new Date()): Set<string> {
  const monday = startOfWeek(reference);

  return new Set(Array.from({ length: 7 }, (_, offset) => {
    const date = new Date(monday);
    date.setDate(monday.getDate() + offset);
    return toDateKey(date);
  }));
}

function calendarDayNumber(date: Date): number {
  return Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()) / 86400000;
}

const WarRoomWorkspace: React.FC<WarRoomProps> = ({
  uid,
  onStudyTopic, onPracticeTopic,
  profile,
  timetableCompletions,
  todayBlocks,
  skippedSessions = [],
  onStudyNow,
  initialMode = 'focus',
  initialReviewPanel = 'subjects',
}) => {
  const progress = useOptionalProgress();
  const sharedStudySessions = progress?.studySessions ?? EMPTY_STUDY_SESSIONS;
  const sharedDebriefs = progress?.studyDebriefs ?? EMPTY_DEBRIEFS;
  const rawProgressDoc = progress?.rawProgressDoc ?? EMPTY_PROGRESS_DOC;
  const isDemo = uid === DEMO_STUDENT_UID;
  const [panel, setPanel] = useState<WarRoomPanel>(initialMode === 'focus' ? 'today' : initialReviewPanel === 'trajectory' ? 'record' : initialReviewPanel === 'time' ? 'time' : 'subjects');
  const [detail, setDetail] = useState<{ subject: string; nodeId?: string }>();
  const [coverageSubject, setCoverageSubject] = useState<string>();
  const [resultsOpen, setResultsOpen] = useState(initialMode === 'review' && initialReviewPanel === 'trajectory');
  const [studySessions, setStudySessions] = useState<StudySessionRecord[]>([]);
  const [debriefs, setDebriefs] = useState<DebriefEntry[]>([]);
  const [sm2States, setSm2States] = useState<SubjectSM2State[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const { topicMastery, mockResults: mockResultsHook, futureFinderPicks } = useInnovationData();
  const targetCourse = futureFinderPicks[0] ?? null;
  const currentDateKey = useLocalDateKey();
  const currentDate = useMemo(() => parseDateKey(currentDateKey), [currentDateKey]);

  const derivedTopicMap: TopicMap = useMemo(() => {
    const map: TopicMap = {};
    for (const [subject, topics] of Object.entries(topicMastery.mastery)) {
      map[subject] = Object.entries(topics).map(([name, entry]) => ({
        id: `${subject}-${name}`,
        name,
        confidence: entry.confidence as TopicEntry['confidence'],
        updatedAt: entry.updatedAt,
      }));
    }
    return map;
  }, [topicMastery.mastery]);

  const derivedMockResults: MockResult[] = useMemo(() => {
    const results: MockResult[] = [];
    for (const mock of mockResultsHook.mocks) {
      for (const entry of mock.entries) {
        results.push({
          id: `${mock.id}-${entry.subjectName}`,
          subject: entry.subjectName,
          grade: entry.grade,
          date: mock.date,
          label: mock.label,
          timestamp: mock.timestamp,
        });
      }
    }
    return results;
  }, [mockResultsHook.mocks]);

  useEffect(() => {
    if (!uid) {
      setStudySessions([]);
      setDebriefs([]);
      setSm2States([]);
      setIsLoading(false);
      return;
    }

    if (isDemo) {
      setStudySessions(sharedStudySessions);
      setDebriefs(sharedDebriefs);
      setSm2States((rawProgressDoc.sm2States as SubjectSM2State[] | undefined) ?? []);
      setIsLoading(false);
      return;
    }

    let cancelled = false;
    setIsLoading(true);
    const load = async () => {
      try {
        const [sessionsSnap, docSnap] = await Promise.all([
          getDocs(collection(db, 'progress', uid, 'sessions')),
          getDoc(doc(db, 'progress', uid)),
        ]);
        if (cancelled) return;
        setStudySessions(sessionsSnap.docs.map(result => result.data() as StudySessionRecord));
        const data = docSnap.data() || {};
        setSm2States((data.sm2States as SubjectSM2State[] | undefined) ?? []);
        setDebriefs((data.studyDebriefs as DebriefEntry[] | undefined) ?? []);
      } catch (error) {
        console.error('Failed to load War Room data:', error);
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    };

    void load();
    return () => { cancelled = true; };
  }, [uid, isDemo, sharedStudySessions, sharedDebriefs, rawProgressDoc.sm2States]);

  const subjects = profile.subjects;
  const blockDuration = profile.defaultBlockDuration ?? 45;
  const parsedExamDate = useMemo(() => {
    if (!profile.examStartDate) return null;
    const date = parseDateKey(profile.examStartDate);
    return Number.isNaN(date.getTime()) ? null : date;
  }, [profile.examStartDate]);
  const daysUntilExam = useMemo(() => (
    parsedExamDate
      ? Math.max(0, calendarDayNumber(parsedExamDate) - calendarDayNumber(currentDate))
      : null
  ), [currentDate, parsedExamDate]);
  const weeksUntilExam = useMemo(() => (
    profile.examStartDate && parsedExamDate
      ? computeWeeksUntilExam(profile.examStartDate)
      : 22
  ), [currentDateKey, parsedExamDate, profile.examStartDate]);
  const allocations = useMemo(() => {
    const priorities = computeSubjectPriorities(
      subjects,
      topicMastery.mastery,
      profile.examStartDate,
    );
    return allocateSessions(priorities, weeksUntilExam, sm2States, blockDuration);
  }, [blockDuration, profile.examStartDate, sm2States, subjects, topicMastery.mastery, weeksUntilExam]);
  const plannedSessions = allocations.reduce((total, item) => total + item.sessions, 0);
  const hasGradeData = subjects.some(subject => Boolean(subject.currentGrade && subject.targetGrade));
  const currentPoints = hasGradeData ? computeCurrentTotal(subjects) : 0;

  const generatedTodayBlocks = useMemo((): WarRoomStudyBlock[] => {
    const todayKey = currentDateKey;
    const todayDayIndex = currentDate.getDay() === 0 ? 6 : currentDate.getDay() - 1;
    const timetable = generateWeeklyTimetable(
      allocations,
      weeksUntilExam,
      0,
      (profile.restDays ?? []).slice(0, 3),
      blockDuration,
      sm2States,
      topicMastery.mastery,
    );
    const completedIds = timetableCompletions[todayKey] ?? [];
    const skippedIds = new Set(skippedSessions);

    return (timetable[todayDayIndex]?.blocks ?? []).flatMap((block, blockIndex) => {
      const blockId = getBlockId(block, blockIndex);
      if (completedIds.includes(blockId) || skippedIds.has(`${todayKey}|${blockId}`)) return [];
      return [{
        subject: block.subjectName,
        sessionType: block.sessionType,
        durationMinutes: block.durationMinutes,
        dateKey: todayKey,
        blockId,
      }];
    });
  }, [allocations, blockDuration, currentDate, currentDateKey, profile.restDays, skippedSessions, sm2States, timetableCompletions, topicMastery.mastery, weeksUntilExam]);
  const actionableTodayBlocks = todayBlocks ?? generatedTodayBlocks;

  const completedThisWeek = useMemo(() => {
    const weekKeys = getCurrentWeekDateKeys(currentDate);
    const timetableCounts: Record<string, Record<string, number>> = {};
    const recordedSessionCounts: Record<string, Record<string, number>> = {};

    for (const [dateKey, blockIds] of Object.entries(timetableCompletions)) {
      if (!weekKeys.has(dateKey)) continue;
      timetableCounts[dateKey] = timetableCounts[dateKey] ?? {};
      for (const blockId of blockIds) {
        const subject = blockId.split('|')[0];
        if (subject) {
          timetableCounts[dateKey][subject] = (timetableCounts[dateKey][subject] ?? 0) + 1;
        }
      }
    }

    for (const session of studySessions) {
      const dateKey = session.date.slice(0, 10);
      if (!weekKeys.has(dateKey)) continue;
      if (session.actualSeconds < session.plannedMinutes * 60) continue;
      recordedSessionCounts[dateKey] = recordedSessionCounts[dateKey] ?? {};
      recordedSessionCounts[dateKey][session.subject] = (recordedSessionCounts[dateKey][session.subject] ?? 0) + 1;
    }

    const counts: Record<string, number> = {};
    for (const subject of subjects) {
      counts[subject.subjectName] = Array.from(weekKeys).reduce((total, dateKey) => (
        total + Math.max(
          timetableCounts[dateKey]?.[subject.subjectName] ?? 0,
          recordedSessionCounts[dateKey]?.[subject.subjectName] ?? 0,
        )
      ), 0);
    }
    return counts;
  }, [currentDate, studySessions, subjects, timetableCompletions]);

  const hoursStudiedMap = useMemo(() => Object.fromEntries(subjects.map(subject => [
    subject.subjectName, recordedSubjectActivity(studySessions, subject.subjectName).seconds / 3600,
  ])), [studySessions, subjects]);

  const tabs = PANELS.filter(tab => tab.id !== 'time' || parsedExamDate !== null);
  const activePanel = tabs.some(tab => tab.id === panel) ? panel : 'subjects';
  const coverageProfile = subjects.find(subject => subject.subjectName === coverageSubject);
  useEffect(() => { if (activePanel !== panel) setPanel(activePanel); }, [activePanel, panel]);
  useEffect(() => { if (coverageSubject && !coverageProfile) setCoverageSubject(undefined); }, [coverageProfile, coverageSubject]);
  useEffect(() => { if (!hasGradeData) setResultsOpen(false); }, [hasGradeData]);
  const openRecord = (subject: string, nodeId?: string) => setDetail({ subject, nodeId });
  const canStudy = (subject: string) => Boolean(
    (onStudyNow && actionableTodayBlocks.some(block => sameStudySubject(block.subject, subject))) ||
    (onStudyTopic && studyTopicSelection(subject, [], profile.examStartDate, subjects.find(item => sameStudySubject(item.subjectName, subject))?.level))
  );
  const studySubject = (subject: string) => {
    const block = actionableTodayBlocks.find(item => sameStudySubject(item.subject, subject));
    if (block && onStudyNow) { onStudyNow(block); return; }
    const selected = subjects.find(item => sameStudySubject(item.subjectName, subject));
    const selection = studyTopicSelection(subject, [], profile.examStartDate, selected?.level);
    if (selection) onStudyTopic?.(selection);
  };

  const dataStillLoading = isLoading
    || topicMastery.isLoaded === false
    || mockResultsHook.isLoaded === false;
  const strategyFacts = [
    ...(daysUntilExam !== null && activePanel !== 'today' ? [{ value: daysUntilExam, label: `${daysUntilExam === 1 ? 'day' : 'days'} to exams` }] : []),
    { value: plannedSessions, label: `${plannedSessions === 1 ? 'session' : 'sessions'} this week` },
    ...(hasGradeData ? [{ value: currentPoints, label: 'current points' }] : []),
  ];

  if (dataStillLoading) {
    return (
      <div className="flex min-h-[280px] items-center justify-center" role="status" aria-label="Loading strategy data">
        <span className="h-7 w-7 animate-spin rounded-full border-2 border-[var(--outline-soft)] border-t-[#F26B1F]" />
      </div>
    );
  }

  return <KobraScope sound={false} className="war-room-workspace">
    <section aria-label="War Room strategy workspace">
      <ul className="wr-strategy-context" aria-label="Strategy context">{strategyFacts.map(fact => <li key={fact.label}><strong>{fact.value}</strong> {fact.label}</li>)}</ul>
      <Tabs value={activePanel} onValueChange={value => { if (tabs.some(tab => tab.id === value)) setPanel(value as WarRoomPanel); }}>
        <TabsList activateOnFocus variant="line" className="wr-nav" aria-label="War Room sections">{tabs.map(tab => <TabsTrigger key={tab.id} value={tab.id}>{tab.label}</TabsTrigger>)}</TabsList>
        <TabsContent value="today"><BriefingPanel subjects={subjects} topicMap={derivedTopicMap} mockResults={derivedMockResults} allocations={allocations} blockDuration={blockDuration} completedThisWeek={completedThisWeek} todayBlocks={actionableTodayBlocks} onStudyNow={onStudyNow} onReviewSubjects={() => setPanel('subjects')} onOpenRecord={openRecord} studySessions={studySessions} daysUntilExam={daysUntilExam} examDate={parsedExamDate} currentDate={currentDate} /></TabsContent>
        <TabsContent value="subjects"><SubjectBoardPanel profile={profile} sessions={studySessions} mastery={topicMastery} onOpenRecord={openRecord} onBrowseTopics={setCoverageSubject} onStudy={studySubject} canStudy={canStudy} /></TabsContent>
        <TabsContent value="record"><LearningLedgerPanel uid={uid} profile={profile} sessions={studySessions} mastery={topicMastery} onOpenRecord={openRecord} onResults={hasGradeData ? () => setResultsOpen(true) : undefined} /></TabsContent>
        {daysUntilExam !== null && <TabsContent value="time"><section className="wr-section-intro"><div><p className="wr-eyebrow">Your time plan / This week</p><h2>Build a week<br /><em>you can keep.</em></h2></div><p>Small sessions. Space to rest.<br />A plan that works around you.</p></section><CountdownPanel daysUntilExam={daysUntilExam} subjects={subjects} allocations={allocations} weeksUntilExam={weeksUntilExam} hoursStudiedMap={hoursStudiedMap} blockDuration={blockDuration} mockResults={derivedMockResults} targetCourse={targetCourse} /></TabsContent>}
      </Tabs>
      <footer className="wr-product-footer"><span>A beginning, built around you.</span>{activePanel !== 'today' && <Button variant="ghost" size="sm" onClick={() => setPanel('today')}>Daily brief</Button>}</footer>
    </section>
    {detail && <LearningRecordCard key={`${detail.subject}:${profile.examStartDate}:${detail.nodeId}`} uid={uid} subject={detail.subject} nodeId={detail.nodeId} level={subjects.find(item => sameStudySubject(item.subjectName, detail.subject))?.level} examDate={profile.examStartDate} sessions={studySessions} mastery={topicMastery} onStudyTopic={onStudyTopic} onPracticeTopic={onPracticeTopic} onClose={() => setDetail(undefined)} />}
    {coverageProfile && <SignatureCard open wide onClose={() => setCoverageSubject(undefined)} title="Your topics." eyebrow={`${coverageProfile.subjectName} / Your subject board`} footer={<KobraScope sound={false}><Button variant="outline" onClick={() => setCoverageSubject(undefined)}>Back to subjects</Button></KobraScope>}><CoveragePanel uid={uid} studySessions={studySessions} onStudyTopic={onStudyTopic} onPracticeTopic={onPracticeTopic} subjects={[coverageProfile]} topicMastery={topicMastery} debriefs={debriefs} examDate={profile.examStartDate} /></SignatureCard>}
    {resultsOpen && hasGradeData && <SignatureCard open wide onClose={() => setResultsOpen(false)} title="Your results." eyebrow="Your grades / On record" footer={<KobraScope sound={false}><Button variant="outline" onClick={() => setResultsOpen(false)}>Back to learning record</Button></KobraScope>}><TrajectoryPanel subjects={subjects} mockResults={derivedMockResults} mockResultsHook={mockResultsHook} daysUntilExam={daysUntilExam ?? 0} /></SignatureCard>}
  </KobraScope>;
};

// Account changes remount the workspace, including loaded records and open cards.
const WarRoom: React.FC<WarRoomProps> = props => <WarRoomWorkspace key={props.uid} {...props} />;
export default WarRoom;
