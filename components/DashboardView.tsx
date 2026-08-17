/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useMemo, useState } from 'react';
import { ArrowRight, Moon, Sun } from 'lucide-react';
import { MotionDiv } from './Motion';
import PageHeader from './ui/PageHeader';
import { type CategoryType } from './KnowledgeTree';
import { type CourseData } from './Library';
import { type StreakData } from '../hooks/useStreak';
import { type FocusRecommendation } from '../hooks/useTodaysFocus';
import { type DebriefEntry } from './StudyDebrief';
import { type StudentSubjectProfile } from './subjectData';
import {
  type StudyReflection,
  type TopicMasteryV2,
  type UnifiedMockResult,
} from '../types';
import { type StudySessionRecord } from '../utils/strategyRegistry';
import MountainLandscape, { type WorldProgress } from './MountainLandscape';
import { type WorldId } from './WorldIconBlob';
import {
  allocateSessions,
  computeSubjectPriorities,
  computeWeeksUntilExam,
  generateWeeklyTimetable,
} from './timetableAlgorithm';
import {
  ActivityChart,
  ConfidenceChart,
  MasteryBar,
  MockTrajectoryChart,
  RankedBarChart,
  SessionMixChart,
  StudyRhythmChart,
} from './dashboard/DashboardCharts';
import {
  averageConfidence,
  buildActivityBuckets,
  buildMasterySummary,
  buildMockSeries,
  buildSessionMix,
  buildStrategyUsage,
  buildStudyRhythm,
  buildSubjectAllocation,
  collectConfidenceObservations,
  confidenceInRange,
  filterSessions,
  getRangeBounds,
  toLocalDateKey,
  type ActivityMetric,
  type DashboardRange,
} from './dashboard/dashboardAnalytics';

type UserProgress = Record<string, { unlockedSection: number }>;
type DashboardTab = 'overview' | 'study' | 'confidence' | 'practice';

interface QuestSummary {
  quest: { title: string; description: string; rewardPoints: number; target: number };
  current: number;
  isCompleted: boolean;
  isClaimed: boolean;
  dayNumber: number;
  isOnboarding: boolean;
}

interface DashboardViewProps {
  userProgress: UserProgress;
  allCourses: CourseData[];
  categoryTitles: Record<CategoryType, string>;
  streak: StreakData;
  recommendation: FocusRecommendation | null;
  onSelectModule: (moduleId: string) => void;
  onBack: () => void;
  pointsEarned: number;
  studentProfile?: StudentSubjectProfile | null;
  studySessions?: StudySessionRecord[];
  studyDebriefs?: DebriefEntry[];
  studyReflections?: StudyReflection[];
  topicMastery?: TopicMasteryV2;
  mockResults?: UnifiedMockResult[];
  timetableCompletions?: Record<string, string[]>;
  questState?: QuestSummary | null;
  onClaimQuestReward?: () => void;
  onStartStudy?: () => void;
  darkMode?: boolean;
  onToggleTheme?: () => void;
}

const WORLD_TO_CATEGORY: Record<WorldId, CategoryType> = {
  mind: 'architecture-mindset',
  growth: 'science-growth',
  learn: 'learning-cheat-codes',
  decode: 'subject-specific-science',
  exam: 'exam-zone',
};

const WORLD_LABEL: Record<WorldId, string> = {
  mind: 'Mind',
  growth: 'Growth',
  learn: 'Learn',
  decode: 'Decode',
  exam: 'Exam',
};

const WORLD_ORDER: WorldId[] = ['mind', 'growth', 'learn', 'decode', 'exam'];
const TABS: Array<{ id: DashboardTab; label: string }> = [
  { id: 'overview', label: 'Overview' },
  { id: 'study', label: 'Study' },
  { id: 'confidence', label: 'Confidence' },
  { id: 'practice', label: 'Practice' },
];

const RANGE_OPTIONS: Array<{ id: DashboardRange; label: string }> = [
  { id: 'week', label: 'Week' },
  { id: 'month', label: 'Month' },
  { id: 'year', label: 'Year' },
];

const formatMinutes = (minutes: number) => {
  if (minutes < 60) return `${minutes}m`;
  const hours = Math.floor(minutes / 60);
  const remainder = minutes % 60;
  return remainder === 0 ? `${hours}h` : `${hours}h ${remainder}m`;
};

const Panel: React.FC<{
  eyebrow: string;
  title: string;
  detail?: string;
  action?: React.ReactNode;
  className?: string;
  children: React.ReactNode;
}> = ({ eyebrow, title, detail, action, className = '', children }) => (
  <article className={`rounded-[18px] border border-[var(--outline-soft)] bg-[var(--surface-paper)] ${className}`}>
    <div className="flex flex-wrap items-start justify-between gap-3 border-b border-[var(--outline-soft)] px-5 py-4 sm:px-6">
      <div className="min-w-0">
        <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-[var(--ink-muted)]">{eyebrow}</p>
        <h2 className="mt-1 font-serif text-xl font-semibold tracking-[-0.015em] text-[var(--ink-primary)] sm:text-2xl">{title}</h2>
        {detail && <p className="mt-1 max-w-xl text-xs leading-relaxed text-[var(--ink-muted)]">{detail}</p>}
      </div>
      {action && <div className="shrink-0">{action}</div>}
    </div>
    <div className="px-5 py-4 sm:px-6 sm:py-5">{children}</div>
  </article>
);

const StatCell: React.FC<{ eyebrow: string; value: string; meta: string; accent?: boolean }> = ({ eyebrow, value, meta, accent }) => (
  <div className="min-w-0 lg:border-l lg:border-[var(--outline-soft)] lg:pl-5 lg:first:border-l-0 lg:first:pl-0">
    <p className="truncate text-[9px] font-bold uppercase tracking-[0.16em] text-[var(--ink-muted)] sm:text-[10px]">{eyebrow}</p>
    <p className={`mt-2 truncate font-serif text-[clamp(24px,3vw,34px)] font-semibold leading-none tabular-nums ${accent ? 'text-[var(--accent-hex)]' : 'text-[var(--ink-primary)]'}`}>{value}</p>
    <p className="mt-2 truncate text-[10px] text-[var(--ink-muted)] sm:text-[11px]">{meta}</p>
  </div>
);

const SegmentedControl = <T extends string>({
  label,
  value,
  options,
  onChange,
}: {
  label: string;
  value: T;
  options: Array<{ id: T; label: string }>;
  onChange: (value: T) => void;
}) => (
  <div className="inline-flex rounded-xl border border-[var(--outline-soft)] bg-[var(--surface-soft)] p-1" role="group" aria-label={label}>
    {options.map(option => (
      <button
        key={option.id}
        type="button"
        aria-pressed={value === option.id}
        onClick={() => onChange(option.id)}
        className={`min-h-8 rounded-lg px-3 text-[11px] font-semibold transition-colors ${
          value === option.id
            ? 'bg-[var(--ink-primary)] text-[var(--surface-paper)]'
            : 'text-[var(--ink-secondary)] hover:text-[var(--ink-primary)]'
        }`}
      >
        {option.label}
      </button>
    ))}
  </div>
);

const DashboardView: React.FC<DashboardViewProps> = ({
  userProgress,
  allCourses,
  categoryTitles: _categoryTitles,
  streak,
  recommendation,
  onSelectModule,
  onBack,
  pointsEarned,
  studentProfile = null,
  studySessions = [],
  studyDebriefs = [],
  studyReflections = [],
  topicMastery,
  mockResults = [],
  timetableCompletions = {},
  questState = null,
  onClaimQuestReward,
  onStartStudy,
  darkMode = false,
  onToggleTheme,
}) => {
  const [tab, setTab] = useState<DashboardTab>('overview');
  const [range, setRange] = useState<DashboardRange>('week');
  const [metric, setMetric] = useState<ActivityMetric>('sessions');
  const [subject, setSubject] = useState('all');

  const worldProgress = useMemo<Record<WorldId, WorldProgress>>(() => {
    const result = {} as Record<WorldId, WorldProgress>;
    for (const world of WORLD_ORDER) {
      const courses = allCourses.filter(course => course.category === WORLD_TO_CATEGORY[world]);
      result[world] = {
        total: courses.length,
        completed: courses.filter(course => {
          const progress = userProgress[course.id];
          return progress && progress.unlockedSection >= course.sectionsCount;
        }).length,
      };
    }
    return result;
  }, [allCourses, userProgress]);

  const fiveWorldTotal = WORLD_ORDER.reduce((sum, world) => sum + worldProgress[world].total, 0);
  const fiveWorldCompleted = WORLD_ORDER.reduce((sum, world) => sum + worldProgress[world].completed, 0);
  const overallPct = fiveWorldTotal > 0 ? Math.round((fiveWorldCompleted / fiveWorldTotal) * 100) : 0;

  const furthest = useMemo(() => {
    let bestWorld: WorldId = 'mind';
    let bestRatio = -1;
    for (const world of WORLD_ORDER) {
      const progress = worldProgress[world];
      const ratio = progress.total > 0 ? progress.completed / progress.total : 0;
      if (ratio > bestRatio) {
        bestWorld = world;
        bestRatio = ratio;
      }
    }
    return {
      world: bestWorld,
      percent: Math.max(0, Math.round(bestRatio * 100)),
    };
  }, [worldProgress]);

  const allConfidence = useMemo(
    () => collectConfidenceObservations(studySessions, studyDebriefs, studyReflections),
    [studySessions, studyDebriefs, studyReflections],
  );

  const subjects = useMemo(() => {
    const values = new Set<string>();
    for (const item of studentProfile?.subjects ?? []) values.add(item.subjectName);
    for (const session of studySessions) if (session.subject) values.add(session.subject);
    for (const observation of allConfidence) if (observation.subject) values.add(observation.subject);
    for (const mock of mockResults) for (const entry of mock.entries) values.add(entry.subjectName);
    return [...values].sort((a, b) => a.localeCompare(b));
  }, [studentProfile, studySessions, allConfidence, mockResults]);

  const rangeBounds = useMemo(() => getRangeBounds(range), [range]);
  const sessionsInRange = useMemo(
    () => filterSessions(studySessions, range, subject),
    [studySessions, range, subject],
  );
  const confidencePoints = useMemo(
    () => confidenceInRange(allConfidence, range, subject),
    [allConfidence, range, subject],
  );
  const activityBuckets = useMemo(
    () => buildActivityBuckets(studySessions, range, subject),
    [studySessions, range, subject],
  );
  const subjectAllocation = useMemo(
    () => buildSubjectAllocation(sessionsInRange),
    [sessionsInRange],
  );
  const strategyUsage = useMemo(
    () => buildStrategyUsage(studySessions, studyDebriefs, range, subject),
    [studySessions, studyDebriefs, range, subject],
  );
  const sessionMix = useMemo(() => buildSessionMix(sessionsInRange), [sessionsInRange]);
  const rhythm = useMemo(() => buildStudyRhythm(subject === 'all' ? studySessions : studySessions.filter(item => item.subject === subject)), [studySessions, subject]);
  const masterySummary = useMemo(() => buildMasterySummary(topicMastery, subject), [topicMastery, subject]);
  const mocks = useMemo(() => buildMockSeries(mockResults).filter(mock => {
    const timestamp = new Date(`${mock.date}T12:00:00`).getTime();
    return timestamp >= rangeBounds.start.getTime() && timestamp < rangeBounds.end.getTime();
  }), [mockResults, rangeBounds]);

  const totalMinutes = Math.round(sessionsInRange.reduce((sum, session) => sum + Math.max(0, session.actualSeconds), 0) / 60);
  const activeDays = new Set(sessionsInRange.map(session => session.date)).size;
  const avgConfidence = averageConfidence(confidencePoints);
  const todayLabel = useMemo(
    () => new Date().toLocaleDateString('en-IE', { weekday: 'long', day: 'numeric', month: 'long' }),
    [],
  );

  const todayPlan = useMemo(() => {
    if (!studentProfile?.subjects.length) return [];
    try {
      const priorities = computeSubjectPriorities(studentProfile.subjects, undefined, studentProfile.examStartDate);
      const weeksUntilExam = computeWeeksUntilExam(studentProfile.examStartDate);
      const allocations = allocateSessions(priorities, weeksUntilExam);
      const timetable = generateWeeklyTimetable(
        allocations,
        weeksUntilExam,
        0,
        studentProfile.restDays ?? [],
        studentProfile.defaultBlockDuration ?? 45,
      );
      const dayIndex = new Date().getDay() === 0 ? 6 : new Date().getDay() - 1;
      return timetable[dayIndex]?.blocks ?? [];
    } catch {
      return [];
    }
  }, [studentProfile]);

  const todayKey = toLocalDateKey(new Date());
  const completedToday = timetableCompletions[todayKey]?.length ?? 0;
  const nextBlock = completedToday < todayPlan.length ? todayPlan[completedToday] : undefined;

  const activityPanel = (
    <Panel
      eyebrow="Study activity"
      title={metric === 'sessions' ? 'Sessions logged' : 'Focused minutes'}
      detail={`${rangeBounds.label}${subject === 'all' ? ' · all subjects' : ` · ${subject}`}`}
      action={
        <SegmentedControl
          label="Study activity measure"
          value={metric}
          options={[{ id: 'sessions', label: 'Sessions' }, { id: 'minutes', label: 'Minutes' }]}
          onChange={value => setMetric(value as ActivityMetric)}
        />
      }
      className="lg:col-span-8"
    >
      <ActivityChart buckets={activityBuckets} metric={metric} />
    </Panel>
  );

  const confidencePanel = (
    <Panel
      eyebrow="Debrief signal"
      title="Confidence over time"
      detail="Each point is a confidence choice made after a completed study session."
      className="lg:col-span-7"
    >
      <ConfidenceChart observations={confidencePoints} bounds={rangeBounds} />
    </Panel>
  );

  const programmePanel = (
    <Panel
      eyebrow="Programme progress"
      title="Five climbs, all your own."
      detail={fiveWorldCompleted === 0
        ? 'Your first completed module paints the first mountain.'
        : `${fiveWorldCompleted} of ${fiveWorldTotal} modules complete · each mountain fills as you progress.`}
      className="lg:col-span-12"
    >
      <div className="-mx-5 overflow-x-auto px-5 pb-2 sm:-mx-6 sm:px-6">
        <div className="min-w-[680px] lg:min-w-0">
          <MountainLandscape progress={worldProgress} />
        </div>
      </div>
      <p className="mt-1 text-center text-[10px] text-[var(--ink-muted)] lg:hidden">Swipe across to explore all five climbs</p>
      <div className="mt-5 grid grid-cols-2 gap-x-6 gap-y-4 border-t border-[var(--outline-soft)] pt-5 sm:grid-cols-4">
        <div>
          <p className="text-[9px] font-bold uppercase tracking-[0.16em] text-[var(--ink-muted)]">Overall</p>
          <p className="mt-1 font-serif text-2xl font-semibold text-[var(--ink-primary)]">{overallPct}%</p>
        </div>
        <div>
          <p className="text-[9px] font-bold uppercase tracking-[0.16em] text-[var(--ink-muted)]">Modules</p>
          <p className="mt-1 font-serif text-2xl font-semibold text-[var(--ink-primary)]">{fiveWorldCompleted}/{fiveWorldTotal}</p>
        </div>
        <div>
          <p className="text-[9px] font-bold uppercase tracking-[0.16em] text-[var(--ink-muted)]">Furthest along</p>
          <p className="mt-1 font-serif text-2xl font-semibold text-[var(--ink-primary)]">{WORLD_LABEL[furthest.world]} · {furthest.percent}%</p>
        </div>
        <div>
          <p className="text-[9px] font-bold uppercase tracking-[0.16em] text-[var(--ink-muted)]">Longest streak</p>
          <p className="mt-1 font-serif text-2xl font-semibold text-[var(--ink-primary)]">{streak.longestStreak ?? streak.currentStreak} days</p>
        </div>
      </div>
    </Panel>
  );

  return (
    <div className="product-shell min-h-screen bg-[var(--surface-canvas)] text-[var(--ink-primary)] transition-colors duration-300">
      <div className="sticky inset-x-0 top-0 z-40 border-b border-[var(--outline-soft)] bg-[color:var(--surface-canvas)]/95 px-4 pb-4 backdrop-blur-xl md:px-10" style={{ paddingTop: 'calc(16px + var(--sat, 0px))' }}>
        <div className="mx-auto max-w-7xl">
          <PageHeader onBack={onBack} eyebrow="Student dashboard" title="My Progress" compact />
        </div>
      </div>

      <main className="mx-auto max-w-7xl px-4 pb-[calc(120px+var(--sab,0px))] pt-7 sm:px-6 md:px-10 md:pt-10">
        <MotionDiv
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
        >
          <div className="flex flex-col gap-6 border-b border-[var(--outline-strong)] pb-7 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-3xl">
              <div className="flex items-center gap-3">
                <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[var(--accent-hex)]">Your learning record</p>
                <span className="h-px w-8 bg-[var(--outline-soft)]" aria-hidden="true" />
                <p className="text-xs text-[var(--ink-muted)]">{todayLabel}</p>
              </div>
              <h1 className="mt-4 max-w-2xl font-serif text-[clamp(38px,6vw,68px)] font-semibold leading-[0.96] tracking-[-0.045em] text-[var(--ink-primary)]">
                Your learning,<br />in motion.
              </h1>
              <p className="mt-4 max-w-xl text-sm leading-relaxed text-[var(--ink-secondary)] sm:text-[15px]">
                Study rhythm, confidence and practice evidence—connected in one clear view.
              </p>
            </div>

            <div className="flex flex-wrap items-end gap-2 lg:max-w-md lg:justify-end">
              <label className="min-w-[160px] flex-1 lg:flex-none">
                <span className="sr-only">Filter by subject</span>
                <select
                  value={subject}
                  onChange={event => setSubject(event.target.value)}
                  className="h-10 w-full rounded-xl border border-[var(--outline-soft)] bg-[var(--surface-paper)] px-3 text-xs font-semibold text-[var(--ink-secondary)] outline-none focus:border-[var(--accent-hex)]"
                >
                  <option value="all">All subjects</option>
                  {subjects.map(item => <option key={item} value={item}>{item}</option>)}
                </select>
              </label>
              <SegmentedControl label="Dashboard time range" value={range} options={RANGE_OPTIONS} onChange={value => setRange(value as DashboardRange)} />
              {onToggleTheme && (
                <button
                  type="button"
                  onClick={onToggleTheme}
                  aria-label={darkMode ? 'Switch to light mode (Beta)' : 'Switch to dark mode (Beta)'}
                  className="flex h-10 w-10 items-center justify-center rounded-xl border border-[var(--outline-soft)] bg-[var(--surface-paper)] text-[var(--ink-secondary)] transition-colors hover:border-[var(--outline-strong)] hover:text-[var(--ink-primary)]"
                >
                  {darkMode ? <Sun size={17} /> : <Moon size={17} />}
                </button>
              )}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-x-4 gap-y-6 border-b border-[var(--outline-soft)] py-6 sm:grid-cols-3 lg:grid-cols-5">
            <StatCell eyebrow="Sessions" value={String(sessionsInRange.length)} meta={`${activeDays} active day${activeDays === 1 ? '' : 's'}`} accent />
            <StatCell eyebrow="Focus time" value={formatMinutes(totalMinutes)} meta={rangeBounds.label} />
            <StatCell eyebrow="Confidence" value={avgConfidence === null ? '—' : avgConfidence.toFixed(1)} meta={avgConfidence === null ? 'awaiting debriefs' : 'average out of 5'} />
            <StatCell eyebrow="Streak" value={String(streak.currentStreak)} meta="days running" />
            <StatCell eyebrow="Journey points" value={String(pointsEarned)} meta="earned to date" />
          </div>

          <div className="mb-5 mt-6 overflow-x-auto border-b border-[var(--outline-soft)]" role="tablist" aria-label="Dashboard sections">
            <div className="flex min-w-max gap-7">
              {TABS.map(item => (
                <button
                  key={item.id}
                  type="button"
                  role="tab"
                  aria-selected={tab === item.id}
                  onClick={() => setTab(item.id)}
                  className={`relative pb-3 text-xs font-semibold transition-colors ${tab === item.id ? 'text-[var(--ink-primary)]' : 'text-[var(--ink-muted)] hover:text-[var(--ink-secondary)]'}`}
                >
                  {item.label}
                  {tab === item.id && <span className="absolute inset-x-0 -bottom-px h-0.5 bg-[var(--accent-hex)]" />}
                </button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4 lg:grid-cols-12">
            {tab === 'overview' && (
              <>
                {activityPanel}
                <Panel eyebrow="Today" title={nextBlock ? nextBlock.subjectName : 'Choose your next move'} detail={nextBlock ? `${nextBlock.durationMinutes} min · ${nextBlock.sessionType.replace('-', ' ')}` : 'Keep the momentum small and specific.'} className="lg:col-span-4">
                  <div className="flex min-h-[244px] flex-col justify-between">
                    <div>
                      <p className="font-serif text-3xl font-semibold leading-tight text-[var(--ink-primary)]">
                        {recommendation?.reason === 'in-progress' ? 'Continue what you started.' : nextBlock ? 'One focused block is enough.' : 'Build evidence, one session at a time.'}
                      </p>
                      {questState && (
                        <div className="mt-6 border-t border-[var(--outline-soft)] pt-4">
                          <div className="flex items-center justify-between gap-3 text-[10px] font-bold uppercase tracking-[0.14em] text-[var(--ink-muted)]">
                            <span>{questState.isOnboarding ? `Day ${questState.dayNumber} quest` : 'Daily quest'}</span>
                            <span className="text-[var(--accent-hex)]">{questState.current}/{questState.quest.target}</span>
                          </div>
                          <p className="mt-2 text-sm font-semibold text-[var(--ink-primary)]">{questState.quest.title}</p>
                          <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-[var(--dashboard-track)]">
                            <div className="h-full rounded-full bg-[var(--accent-hex)]" style={{ width: `${Math.min(100, (questState.current / questState.quest.target) * 100)}%` }} />
                          </div>
                        </div>
                      )}
                    </div>
                    <div className="mt-7 flex flex-wrap gap-2">
                      {onStartStudy && (
                        <button onClick={onStartStudy} className="inline-flex min-h-11 items-center gap-2 rounded-xl bg-[var(--ink-primary)] px-4 text-xs font-bold text-[var(--surface-paper)] transition-transform hover:-translate-y-0.5">
                          Start studying <ArrowRight size={14} />
                        </button>
                      )}
                      {recommendation && recommendation.reason !== 'all-complete' && (
                        <button onClick={() => onSelectModule(recommendation.moduleId)} className="inline-flex min-h-11 items-center gap-2 rounded-xl border border-[var(--outline-soft)] px-4 text-xs font-bold text-[var(--ink-secondary)] hover:border-[var(--outline-strong)]">
                          Open module
                        </button>
                      )}
                      {questState?.isCompleted && !questState.isClaimed && onClaimQuestReward && (
                        <button onClick={onClaimQuestReward} className="inline-flex min-h-11 items-center rounded-xl border border-[var(--accent-hex)] px-4 text-xs font-bold text-[var(--accent-hex)]">
                          Claim {questState.quest.rewardPoints} JP
                        </button>
                      )}
                    </div>
                  </div>
                </Panel>
                {confidencePanel}
                <Panel eyebrow="Time allocation" title="Subjects studied" detail="Focused minutes across the selected period." className="lg:col-span-5">
                  <RankedBarChart values={subjectAllocation} unit="min" emptyTitle="No subject split yet" emptyDetail="Log a study session and its subject will appear here." />
                </Panel>
                {programmePanel}
                <Panel eyebrow="Learning methods" title="Techniques used" detail="Recorded prompts and self-reported study techniques." className="lg:col-span-6">
                  <RankedBarChart values={strategyUsage} unit="uses" emptyTitle="No techniques tracked yet" emptyDetail="Select the methods you used at the end of a study session." />
                </Panel>
                <Panel eyebrow="Exam evidence" title="Mock trajectory" detail="Total points from Points Passport." className="lg:col-span-6">
                  <MockTrajectoryChart mocks={mocks} />
                </Panel>
              </>
            )}

            {tab === 'study' && (
              <>
                <div className="lg:col-span-12">{React.cloneElement(activityPanel, { className: 'lg:col-span-12' })}</div>
                <Panel eyebrow="Consistency" title="Study rhythm" detail="Thirteen weeks of recorded study activity." className="lg:col-span-7">
                  <StudyRhythmChart weeks={rhythm} />
                </Panel>
                <Panel eyebrow="Time allocation" title="Subjects studied" detail="Focused minutes across the selected period." className="lg:col-span-5">
                  <RankedBarChart values={subjectAllocation} unit="min" emptyTitle="No subject split yet" emptyDetail="Log a study session and its subject will appear here." />
                </Panel>
                <Panel eyebrow="Session design" title="Learning mix" detail="How study time is being used." className="lg:col-span-6">
                  <SessionMixChart values={sessionMix} />
                </Panel>
                <Panel eyebrow="Learning methods" title="Techniques used" detail="Recorded prompts and self-reported study techniques." className="lg:col-span-6">
                  <RankedBarChart values={strategyUsage} unit="uses" emptyTitle="No techniques tracked yet" emptyDetail="Select the methods you used at the end of a study session." />
                </Panel>
              </>
            )}

            {tab === 'confidence' && (
              <>
                <div className="lg:col-span-12">{React.cloneElement(confidencePanel, { className: 'lg:col-span-12' })}</div>
                <Panel eyebrow="Current picture" title="Topic readiness" detail="Topic ratings from War Room and structured study debriefs." className="lg:col-span-12">
                  <MasteryBar summary={masterySummary} />
                </Panel>
                {programmePanel}
              </>
            )}

            {tab === 'practice' && (
              <>
                <Panel eyebrow="Exam evidence" title="Mock trajectory" detail="Total points from Points Passport." className="lg:col-span-8">
                  <MockTrajectoryChart mocks={mocks} />
                </Panel>
                <Panel eyebrow="Session design" title="Learning mix" detail="New learning, practice and revision in this period." className="lg:col-span-4">
                  <SessionMixChart values={sessionMix} />
                </Panel>
                <Panel eyebrow="Topic readiness" title="What feels secure" detail="A current snapshot, filtered by subject when selected." className="lg:col-span-6">
                  <MasteryBar summary={masterySummary} />
                </Panel>
                <Panel eyebrow="Methods in practice" title="Techniques used" detail="How often each learning method was recorded." className="lg:col-span-6">
                  <RankedBarChart values={strategyUsage} unit="uses" emptyTitle="No techniques tracked yet" emptyDetail="Select the methods you used at the end of a study session." />
                </Panel>
              </>
            )}
          </div>
        </MotionDiv>
      </main>
    </div>
  );
};

export default DashboardView;
