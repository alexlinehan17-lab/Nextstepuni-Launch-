/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect, useMemo, useRef, useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { CalendarDays, ClipboardList, Library, TrendingUp } from 'lucide-react';
import { collection, doc, getDoc, getDocs } from 'firebase/firestore';
import { db } from '../firebase';
import { MotionDiv } from './Motion';
import {
  type StudentSubjectProfile,
  type TimetableCompletions,
} from './subjectData';
import {
  allocateSessions,
  computeSubjectPriorities,
  computeWeeksUntilExam,
} from './timetableAlgorithm';
import { type DebriefEntry } from './StudyDebrief';
import { type StudySessionRecord } from '../utils/strategyRegistry';
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

interface WarRoomProps {
  uid: string;
  profile: StudentSubjectProfile;
  timetableCompletions: TimetableCompletions;
}

type PanelId = 'briefing' | 'subjects' | 'trajectory' | 'time';

const PANEL_TABS: Array<{
  id: PanelId;
  label: string;
  shortLabel: string;
  icon: React.ComponentType<{ size?: number }>;
}> = [
  { id: 'briefing', label: 'Briefing', shortLabel: 'Brief', icon: ClipboardList },
  { id: 'subjects', label: 'Subjects', shortLabel: 'Subjects', icon: Library },
  { id: 'trajectory', label: 'Trajectory', shortLabel: 'Trend', icon: TrendingUp },
  { id: 'time', label: 'Time plan', shortLabel: 'Time', icon: CalendarDays },
];

const WarRoom: React.FC<WarRoomProps> = ({ uid, profile, timetableCompletions }) => {
  const [activePanel, setActivePanel] = useState<PanelId>('briefing');
  const [studySessions, setStudySessions] = useState<StudySessionRecord[]>([]);
  const [debriefs, setDebriefs] = useState<DebriefEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const tabRefs = useRef<Array<HTMLButtonElement | null>>([]);

  const { topicMastery, mockResults: mockResultsHook, futureFinderPicks } = useInnovationData();
  const targetCourse = futureFinderPicks[0] ?? null;

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
      setIsLoading(false);
      return;
    }
    let cancelled = false;
    const load = async () => {
      try {
        const [sessionsSnap, docSnap] = await Promise.all([
          getDocs(collection(db, 'progress', uid, 'sessions')),
          getDoc(doc(db, 'progress', uid)),
        ]);
        if (cancelled) return;
        setStudySessions(sessionsSnap.docs.map(result => result.data() as StudySessionRecord));
        const data = docSnap.data() || {};
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
  const daysUntilExam = useMemo(() => {
    const examDate = new Date(profile.examStartDate);
    return Math.max(0, Math.ceil((examDate.getTime() - Date.now()) / 86400000));
  }, [profile.examStartDate]);
  const weeksUntilExam = useMemo(
    () => computeWeeksUntilExam(profile.examStartDate),
    [profile.examStartDate],
  );
  const blockDuration = profile.defaultBlockDuration ?? 45;
  const allocations = useMemo(() => {
    const priorities = computeSubjectPriorities(subjects, undefined, profile.examStartDate);
    return allocateSessions(priorities, weeksUntilExam);
  }, [profile.examStartDate, subjects, weeksUntilExam]);
  const plannedSessions = allocations.reduce((total, item) => total + item.sessions, 0);
  const currentPoints = computeCurrentTotal(subjects);
  const targetPoints = targetCourse?.typicalPoints;
  const targetGap = targetPoints === undefined ? null : Math.max(0, targetPoints - currentPoints);
  const pointsReference = targetPoints ?? 625;
  const pointsProgress = Math.min(1, currentPoints / Math.max(1, pointsReference));
  const pointsCircumference = 2 * Math.PI * 41;
  const examDateLabel = useMemo(() => {
    const examDate = new Date(profile.examStartDate);
    if (Number.isNaN(examDate.getTime())) return 'Exam date not set';
    return new Intl.DateTimeFormat('en-IE', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
    }).format(examDate);
  }, [profile.examStartDate]);

  const hoursStudiedMap = useMemo(() => {
    const map: Record<string, number> = {};
    for (const session of studySessions) {
      map[session.subject] = (map[session.subject] || 0) + session.actualSeconds / 3600;
    }
    for (const blockIds of Object.values(timetableCompletions)) {
      for (const blockId of blockIds) {
        const subjectName = blockId.split('|')[0];
        if (subjectName) map[subjectName] = (map[subjectName] || 0) + blockDuration / 60;
      }
    }
    return map;
  }, [blockDuration, studySessions, timetableCompletions]);

  const selectTab = (id: PanelId, focus = false) => {
    setActivePanel(id);
    if (focus) {
      const index = PANEL_TABS.findIndex(tab => tab.id === id);
      tabRefs.current[index]?.focus();
    }
  };

  const handleTabKeyDown = (event: React.KeyboardEvent, index: number) => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    let nextIndex = index;
    if (event.key === 'ArrowLeft') nextIndex = (index - 1 + PANEL_TABS.length) % PANEL_TABS.length;
    if (event.key === 'ArrowRight') nextIndex = (index + 1) % PANEL_TABS.length;
    if (event.key === 'Home') nextIndex = 0;
    if (event.key === 'End') nextIndex = PANEL_TABS.length - 1;
    selectTab(PANEL_TABS[nextIndex].id, true);
  };

  if (isLoading) {
    return (
      <div className="flex min-h-[280px] items-center justify-center" role="status" aria-label="Loading strategy data">
        <span className="h-7 w-7 animate-spin rounded-full border-2 border-[var(--outline-soft)] border-t-[#F26B1F]" />
      </div>
    );
  }

  return (
    <section className="war-room-workspace pb-16" aria-label="War Room strategy workspace">
      <div className="grid gap-3 lg:grid-cols-2" aria-label="Strategy snapshot">
        <section
          className="overflow-hidden rounded-[14px] border border-[var(--outline-soft)] bg-[var(--surface-paper)]"
          aria-labelledby="exam-runway-title"
        >
          <div className="grid min-h-[210px] sm:grid-cols-[0.82fr_1.18fr]">
            <div className="flex flex-col justify-between border-b border-[var(--outline-soft)] p-5 sm:border-b-0 sm:border-r sm:p-6">
              <div>
                <h2 id="exam-runway-title" className="text-[11px] font-bold uppercase tracking-[0.2em] text-[var(--ink-muted)]">Exam runway</h2>
                <p className="mt-5 font-serif text-[50px] font-semibold leading-none text-[var(--ink-primary)]">
                  {daysUntilExam}
                </p>
                <p className="mt-1.5 text-sm font-medium text-[var(--ink-secondary)]">Days to exams</p>
              </div>
              <p className="mt-6 font-mono text-[11px] text-[var(--ink-muted)]">First paper · {examDateLabel}</p>
            </div>

            <div className="flex flex-col justify-between p-5 sm:p-6">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-sm font-semibold text-[var(--ink-primary)]">{weeksUntilExam} weeks remaining</p>
                  <p className="mt-1 text-xs text-[var(--ink-secondary)]">{plannedSessions} planned study sessions each week</p>
                </div>
                <span className="font-mono text-xs font-semibold text-[#F26B1F]">{plannedSessions}/wk</span>
              </div>

              <div className="mt-8" aria-label={`${weeksUntilExam} weeks from today until exams`}>
                <div className="relative h-[72px]">
                  <div className="absolute left-0 right-0 top-[34px] h-px bg-[var(--outline-soft)]" />
                  {Array.from({ length: 7 }).map((_, index) => (
                    <span
                      key={index}
                      className="absolute top-[31px] h-[7px] w-[7px] -translate-x-1/2 rounded-full border border-[var(--outline-strong)] bg-[var(--surface-paper)]"
                      style={{ left: `${(index / 6) * 100}%` }}
                    />
                  ))}
                  <span className="absolute left-0 top-[26px] h-[17px] w-[17px] -translate-x-1/2 rounded-full border-[4px] border-[var(--surface-paper)] bg-[#F26B1F]" />
                  <span className="absolute right-0 top-[24px] h-[21px] w-px bg-[var(--ink-primary)]" />
                  <span className="absolute bottom-0 left-0 text-[10px] font-semibold uppercase tracking-[0.14em] text-[var(--ink-muted)]">Today</span>
                  <span className="absolute bottom-0 right-0 text-[10px] font-semibold uppercase tracking-[0.14em] text-[var(--ink-muted)]">Exam</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section
          className="overflow-hidden rounded-[14px] border border-[var(--outline-soft)] bg-[var(--surface-paper)]"
          aria-labelledby="points-position-title"
        >
          <div className="grid min-h-[210px] grid-cols-[1fr_auto] gap-5 p-5 sm:p-6">
            <div className="flex min-w-0 flex-col justify-between">
              <div>
                <h2 id="points-position-title" className="text-[11px] font-bold uppercase tracking-[0.2em] text-[var(--ink-muted)]">Points position</h2>
                <p className="mt-5 font-serif text-[50px] font-semibold leading-none text-[var(--ink-primary)]">
                  {currentPoints}
                </p>
                <p className="mt-1.5 text-sm font-medium text-[var(--ink-secondary)]">Current points</p>
              </div>
              <div className="mt-6 grid grid-cols-2 gap-4 border-t border-[var(--outline-soft)] pt-4">
                <div>
                  <p className="font-mono text-sm font-semibold text-[var(--ink-primary)]">{targetPoints ?? '—'}</p>
                  <p className="mt-1 text-[10px] font-semibold uppercase tracking-[0.14em] text-[var(--ink-muted)]">Course target</p>
                </div>
                <div>
                  <p className={`font-mono text-sm font-semibold ${targetGap === 0 ? 'text-[var(--success-hex)]' : 'text-[#F26B1F]'}`}>
                    {targetGap === null ? 'Not set' : targetGap === 0 ? 'On target' : targetGap}
                  </p>
                  <p className="mt-1 text-[10px] font-semibold uppercase tracking-[0.14em] text-[var(--ink-muted)]">{targetGap === null ? 'Target status' : 'Points gap'}</p>
                </div>
              </div>
            </div>

            <div className="flex w-[128px] flex-col items-center justify-center sm:w-[164px]">
              <div className="relative h-[126px] w-[126px]" aria-label={`${Math.round(pointsProgress * 100)} percent of ${targetPoints ? 'course target' : 'maximum points'}`}>
                <svg viewBox="0 0 100 100" className="h-full w-full -rotate-90" aria-hidden="true">
                  <circle cx="50" cy="50" r="41" fill="none" stroke="var(--outline-soft)" strokeWidth="10" />
                  <circle
                    cx="50"
                    cy="50"
                    r="41"
                    fill="none"
                    stroke="var(--ink-primary)"
                    strokeWidth="10"
                    strokeLinecap="butt"
                    strokeDasharray={pointsCircumference}
                    strokeDashoffset={pointsCircumference * (1 - pointsProgress)}
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="font-mono text-lg font-semibold text-[var(--ink-primary)]">{Math.round(pointsProgress * 100)}%</span>
                </div>
              </div>
              <p className="mt-2 text-center text-[10px] font-semibold uppercase tracking-[0.13em] text-[var(--ink-muted)]">
                of {targetPoints ? 'course target' : '625 max'}
              </p>
            </div>
          </div>
        </section>
      </div>

      <div className="mt-5 border-b border-[var(--outline-soft)]">
        <div
          role="tablist"
          aria-label="War Room views"
          className="war-room-tabs"
        >
          {PANEL_TABS.map((tab, index) => {
            const Icon = tab.icon;
            const selected = activePanel === tab.id;
            return (
              <button
                key={tab.id}
                ref={element => { tabRefs.current[index] = element; }}
                id={`war-room-tab-${tab.id}`}
                type="button"
                role="tab"
                aria-label={tab.label}
                aria-selected={selected}
                aria-controls={`war-room-panel-${tab.id}`}
                tabIndex={selected ? 0 : -1}
                onClick={() => selectTab(tab.id)}
                onKeyDown={event => handleTabKeyDown(event, index)}
                className="war-room-tab"
              >
                <Icon size={16} />
                <span className="hidden sm:inline">{tab.label}</span>
                <span className="sm:hidden">{tab.shortLabel}</span>
                {selected && <MotionDiv layoutId="war-room-active-tab" className="war-room-tab-indicator" />}
              </button>
            );
          })}
        </div>
      </div>

      <AnimatePresence mode="wait" initial={false}>
        <MotionDiv
          key={activePanel}
          id={`war-room-panel-${activePanel}`}
          role="tabpanel"
          aria-labelledby={`war-room-tab-${activePanel}`}
          initial={{ opacity: 0, y: 6 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -4 }}
          transition={{ duration: 0.22, ease: [0.22, 1, 0.36, 1] }}
          className="pt-7 sm:pt-9"
        >
          {activePanel === 'briefing' && (
            <BriefingPanel
              subjects={subjects}
              topicMap={derivedTopicMap}
              mockResults={derivedMockResults}
              allocations={allocations}
              hoursStudiedMap={hoursStudiedMap}
              weeksUntilExam={weeksUntilExam}
              blockDuration={blockDuration}
              daysUntilExam={daysUntilExam}
              timetableCompletions={timetableCompletions}
              onReviewSubjects={() => selectTab('subjects', true)}
            />
          )}
          {activePanel === 'subjects' && (
            <CoveragePanel
              subjects={subjects}
              topicMastery={topicMastery}
              debriefs={debriefs}
              examDate={profile.examStartDate}
            />
          )}
          {activePanel === 'trajectory' && (
            <TrajectoryPanel
              subjects={subjects}
              mockResults={derivedMockResults}
              mockResultsHook={mockResultsHook}
              daysUntilExam={daysUntilExam}
            />
          )}
          {activePanel === 'time' && (
            <CountdownPanel
              daysUntilExam={daysUntilExam}
              subjects={subjects}
              allocations={allocations}
              weeksUntilExam={weeksUntilExam}
              hoursStudiedMap={hoursStudiedMap}
              blockDuration={blockDuration}
              mockResults={derivedMockResults}
              targetCourse={targetCourse}
              currentPoints={currentPoints}
            />
          )}
        </MotionDiv>
      </AnimatePresence>
    </section>
  );
};

export default WarRoom;
