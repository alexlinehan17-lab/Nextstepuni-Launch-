/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect, useMemo, useRef, useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { collection, doc, getDoc, getDocs } from 'firebase/firestore';
import { db } from '../firebase';
import { MotionDiv } from './Motion';
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
import TrajectoryPanel from './war-room/TrajectoryPanel';

export interface WarRoomStudyBlock {
  subject: string;
  sessionType: 'new-learning' | 'practice' | 'revision';
  durationMinutes: number;
  dateKey: string;
  blockId: string;
}

interface WarRoomProps {
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

const MODE_TABS: Array<{ id: WorkspaceMode; label: string }> = [
  { id: 'focus', label: 'Focus' },
  { id: 'review', label: 'Review' },
];

const ALL_REVIEW_TABS: Array<{ id: ReviewPanelId; label: string }> = [
  { id: 'subjects', label: 'Subjects' },
  { id: 'trajectory', label: 'Results' },
  { id: 'time', label: 'Time plan' },
];

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

const WarRoom: React.FC<WarRoomProps> = ({
  uid,
  profile,
  timetableCompletions,
  todayBlocks,
  skippedSessions = [],
  onStudyNow,
  initialMode = 'focus',
  initialReviewPanel = 'subjects',
}) => {
  const [mode, setMode] = useState<WorkspaceMode>(initialMode);
  const [reviewPanel, setReviewPanel] = useState<ReviewPanelId>(initialReviewPanel);
  const [studySessions, setStudySessions] = useState<StudySessionRecord[]>([]);
  const [debriefs, setDebriefs] = useState<DebriefEntry[]>([]);
  const [sm2States, setSm2States] = useState<SubjectSM2State[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const modeTabRefs = useRef<Array<HTMLButtonElement | null>>([]);
  const reviewTabRefs = useRef<Array<HTMLButtonElement | null>>([]);

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
      setSm2States([]);
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
        if (data.studyDebriefs) setDebriefs(data.studyDebriefs as DebriefEntry[]);
      } catch (error) {
        console.error('Failed to load War Room data:', error);
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    };

    void load();
    return () => { cancelled = true; };
  }, [uid]);

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

  const hoursStudiedMap = useMemo(() => {
    const recordedHours: Record<string, Record<string, number>> = {};
    const timetableHours: Record<string, Record<string, number>> = {};
    const dateKeys = new Set<string>();

    for (const session of studySessions) {
      const dateKey = session.date.slice(0, 10);
      dateKeys.add(dateKey);
      recordedHours[dateKey] = recordedHours[dateKey] ?? {};
      recordedHours[dateKey][session.subject] = (recordedHours[dateKey][session.subject] ?? 0) + session.actualSeconds / 3600;
    }
    for (const [dateKey, blockIds] of Object.entries(timetableCompletions)) {
      dateKeys.add(dateKey);
      timetableHours[dateKey] = timetableHours[dateKey] ?? {};
      for (const blockId of blockIds) {
        const subject = blockId.split('|')[0];
        if (subject) {
          timetableHours[dateKey][subject] = (timetableHours[dateKey][subject] ?? 0) + blockDuration / 60;
        }
      }
    }

    const map: Record<string, number> = {};
    for (const subject of subjects) {
      map[subject.subjectName] = Array.from(dateKeys).reduce((total, dateKey) => (
        total + Math.max(
          recordedHours[dateKey]?.[subject.subjectName] ?? 0,
          timetableHours[dateKey]?.[subject.subjectName] ?? 0,
        )
      ), 0);
    }
    return map;
  }, [blockDuration, studySessions, subjects, timetableCompletions]);

  const reviewTabs = useMemo(() => ALL_REVIEW_TABS.filter(tab => {
    if (tab.id === 'trajectory') return hasGradeData;
    if (tab.id === 'time') return parsedExamDate !== null;
    return true;
  }), [hasGradeData, parsedExamDate]);
  const activeReviewPanel = reviewTabs.some(tab => tab.id === reviewPanel)
    ? reviewPanel
    : 'subjects';

  useEffect(() => {
    if (activeReviewPanel !== reviewPanel) setReviewPanel(activeReviewPanel);
  }, [activeReviewPanel, reviewPanel]);

  const selectMode = (nextMode: WorkspaceMode, focus = false) => {
    setMode(nextMode);
    if (focus) {
      const index = MODE_TABS.findIndex(tab => tab.id === nextMode);
      modeTabRefs.current[index]?.focus();
    }
  };

  const handleModeKeyDown = (event: React.KeyboardEvent, index: number) => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    let nextIndex = index;
    if (event.key === 'ArrowLeft') nextIndex = (index - 1 + MODE_TABS.length) % MODE_TABS.length;
    if (event.key === 'ArrowRight') nextIndex = (index + 1) % MODE_TABS.length;
    if (event.key === 'Home') nextIndex = 0;
    if (event.key === 'End') nextIndex = MODE_TABS.length - 1;
    selectMode(MODE_TABS[nextIndex].id, true);
  };

  const selectReviewPanel = (id: ReviewPanelId, focus = false) => {
    setReviewPanel(id);
    if (focus) {
      const index = reviewTabs.findIndex(tab => tab.id === id);
      reviewTabRefs.current[index]?.focus();
    }
  };

  const handleReviewKeyDown = (event: React.KeyboardEvent, index: number) => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    let nextIndex = index;
    if (event.key === 'ArrowLeft') nextIndex = (index - 1 + reviewTabs.length) % reviewTabs.length;
    if (event.key === 'ArrowRight') nextIndex = (index + 1) % reviewTabs.length;
    if (event.key === 'Home') nextIndex = 0;
    if (event.key === 'End') nextIndex = reviewTabs.length - 1;
    selectReviewPanel(reviewTabs[nextIndex].id, true);
  };

  const openSubjectReview = () => {
    setReviewPanel('subjects');
    setMode('review');
  };

  const dataStillLoading = isLoading
    || topicMastery.isLoaded === false
    || mockResultsHook.isLoaded === false;
  const strategyFacts = [
    ...(daysUntilExam !== null ? [{ value: daysUntilExam, label: `${daysUntilExam === 1 ? 'day' : 'days'} to exams` }] : []),
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

  return (
    <section className="war-room-workspace pb-16" aria-label="War Room strategy workspace">
      <div className="flex flex-col gap-3 border-y border-[var(--outline-soft)] py-3 sm:flex-row sm:items-center sm:justify-between sm:gap-4 sm:py-4">
        <ul className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-[var(--ink-secondary)]" aria-label="Strategy context">
          {strategyFacts.map((fact, index) => (
            <li key={fact.label} className="whitespace-nowrap">
              {index > 0 && <span aria-hidden="true" className="mr-3 hidden text-[var(--outline-strong)] sm:inline">·</span>}
              <span className="font-semibold text-[var(--ink-primary)]">{fact.value}</span> {fact.label}
            </li>
          ))}
        </ul>

        <div
          role="tablist"
          aria-label="War Room mode"
          className="inline-grid w-full grid-cols-2 rounded-[10px] border border-[var(--outline-soft)] bg-[var(--surface-soft)] p-1 sm:w-[210px] sm:shrink-0"
        >
          {MODE_TABS.map((tab, index) => {
            const selected = mode === tab.id;
            return (
              <button
                key={tab.id}
                ref={element => { modeTabRefs.current[index] = element; }}
                id={`war-room-mode-tab-${tab.id}`}
                type="button"
                role="tab"
                aria-selected={selected}
                aria-controls={`war-room-mode-panel-${tab.id}`}
                tabIndex={selected ? 0 : -1}
                onClick={() => selectMode(tab.id)}
                onKeyDown={event => handleModeKeyDown(event, index)}
                className={`min-h-9 rounded-[7px] px-4 text-xs font-semibold transition-[background-color,color,box-shadow] duration-200 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--outline-strong)] ${
                  selected
                    ? 'bg-[var(--surface-paper)] text-[var(--ink-primary)] shadow-[0_1px_3px_rgba(0,0,0,.08)]'
                    : 'text-[var(--ink-muted)] hover:text-[var(--ink-primary)]'
                }`}
              >
                {tab.label}
              </button>
            );
          })}
        </div>
      </div>

      <AnimatePresence mode="wait" initial={false}>
        <MotionDiv
          key={mode}
          id={`war-room-mode-panel-${mode}`}
          role="tabpanel"
          aria-labelledby={`war-room-mode-tab-${mode}`}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -5 }}
          transition={{ duration: 0.24, ease: [0.22, 1, 0.36, 1] }}
          className="pt-6 sm:pt-10"
        >
          {mode === 'focus' ? (
            <BriefingPanel
              subjects={subjects}
              topicMap={derivedTopicMap}
              mockResults={derivedMockResults}
              allocations={allocations}
              blockDuration={blockDuration}
              completedThisWeek={completedThisWeek}
              todayBlocks={actionableTodayBlocks}
              onStudyNow={onStudyNow}
              onReviewSubjects={openSubjectReview}
            />
          ) : (
            <div>
              <header className="max-w-2xl">
                <h2 className="font-sans text-[24px] font-semibold leading-tight tracking-[-0.025em] text-[var(--ink-primary)] sm:text-[28px]">
                  See the detail when you need it
                </h2>
                <p className="mt-2 max-w-xl text-sm leading-relaxed text-[var(--ink-secondary)]">
                  Check coverage, results and the shape of your study plan without crowding the decision in front of you.
                </p>
              </header>

              {reviewTabs.length > 1 && (
                <div className="mt-6 border-b border-[var(--outline-soft)]">
                  <div
                    role="tablist"
                    aria-label="Review views"
                    className="grid gap-1"
                    style={{ gridTemplateColumns: `repeat(${reviewTabs.length}, minmax(0, 1fr))` }}
                  >
                    {reviewTabs.map((tab, index) => {
                      const selected = activeReviewPanel === tab.id;
                      return (
                        <button
                          key={tab.id}
                          ref={element => { reviewTabRefs.current[index] = element; }}
                          id={`war-room-review-tab-${tab.id}`}
                          type="button"
                          role="tab"
                          aria-selected={selected}
                          aria-controls={`war-room-review-panel-${tab.id}`}
                          tabIndex={selected ? 0 : -1}
                          onClick={() => selectReviewPanel(tab.id)}
                          onKeyDown={event => handleReviewKeyDown(event, index)}
                          className={`relative min-h-11 px-3 pb-3 text-xs font-semibold transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-[var(--outline-strong)] ${
                            selected ? 'text-[var(--ink-primary)]' : 'text-[var(--ink-muted)] hover:text-[var(--ink-primary)]'
                          }`}
                        >
                          {tab.label}
                          {selected && (
                            <MotionDiv
                              layoutId="war-room-review-indicator"
                              className="absolute inset-x-3 -bottom-px h-0.5 bg-[var(--outline-strong)]"
                            />
                          )}
                        </button>
                      );
                    })}
                  </div>
                </div>
              )}

              <AnimatePresence mode="wait" initial={false}>
                <MotionDiv
                  key={activeReviewPanel}
                  id={`war-room-review-panel-${activeReviewPanel}`}
                  role="tabpanel"
                  aria-labelledby={reviewTabs.length > 1 ? `war-room-review-tab-${activeReviewPanel}` : undefined}
                  aria-label={reviewTabs.length === 1 ? 'Subjects review' : undefined}
                  initial={{ opacity: 0, y: 6 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -4 }}
                  transition={{ duration: 0.2, ease: [0.22, 1, 0.36, 1] }}
                  className="pt-8"
                >
                  {activeReviewPanel === 'subjects' && (
                    <CoveragePanel
                      subjects={subjects}
                      topicMastery={topicMastery}
                      debriefs={debriefs}
                      examDate={profile.examStartDate}
                    />
                  )}
                  {activeReviewPanel === 'trajectory' && hasGradeData && (
                    <TrajectoryPanel
                      subjects={subjects}
                      mockResults={derivedMockResults}
                      mockResultsHook={mockResultsHook}
                      daysUntilExam={daysUntilExam ?? 0}
                    />
                  )}
                  {activeReviewPanel === 'time' && daysUntilExam !== null && (
                    <CountdownPanel
                      daysUntilExam={daysUntilExam}
                      subjects={subjects}
                      allocations={allocations}
                      weeksUntilExam={weeksUntilExam}
                      hoursStudiedMap={hoursStudiedMap}
                      blockDuration={blockDuration}
                      mockResults={derivedMockResults}
                      targetCourse={targetCourse}
                      currentPoints={hasGradeData ? currentPoints : undefined}
                    />
                  )}
                </MotionDiv>
              </AnimatePresence>
            </div>
          )}
        </MotionDiv>
      </AnimatePresence>
    </section>
  );
};

export default WarRoom;
