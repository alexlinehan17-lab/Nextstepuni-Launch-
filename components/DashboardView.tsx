import { sameStudySubject } from '../services/studyTopicHistory';
import TopicHistoryPanel from './topics/TopicHistoryPanel';
import type { TopicHistoryActions } from './topics/TopicDetailCard';
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useMemo, useState } from 'react';
import './dashboard/dashboard-refined.css';
import KobraScope from './approved-ui-runtime';
import { Button } from './approved-ui-runtime';
import { SubjectPicker } from './dashboard/progress/SubjectPicker';
import { ProgressSummary } from './dashboard/progress/ProgressSummary';
import { ProgressActivity, ProgressConfidence, ProgressSubjects, ProgressMocks } from './dashboard/progress/ProgressCharts';
import { MethodJournal } from './dashboard/progress/MethodJournal';
import { ProgressTabs } from './dashboard/progress/shared';
import { buildMethodJournal, selectSubjects } from './dashboard/progress/progressData';
import './dashboard/progress/progress.css';
import './dashboard/progress/refinements.css';
import { ProgressSections, ProgressBreakdown } from './dashboard/progress/ProgressRefinements';
import { ProgressMilestones } from './dashboard/progress/ProgressMilestones';

import { useMobileAppDesign } from '../hooks/useMobileAppDesign';
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
  type StrategyMasteryMap,
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
  StudyRhythmChart,
} from './dashboard/DashboardCharts';
import {
  averageConfidence,
  buildActivityBuckets,
  buildMasterySummary,
  buildMockSeries,
  buildSessionMix,
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
import DashboardInsights from './dashboard/DashboardInsights';
import ProgressSectionPicker from './dashboard/ProgressSectionPicker';
import {
  buildActivityInsights,
  buildConfidenceInsights,
  buildMockInsights,
} from './dashboard/dashboardInsightAnalytics';
import { resolveMockResultKind } from '../services/mockResultsRepository';
import {
  type GamificationState,
} from '../gamificationConfig';
import { type WeeklyChallengeState } from '../hooks/useWeeklyChallenge';
import { type CurriculumLevel } from '../utils/authUtils';
import { type DashboardSection } from '../contexts/NavigationContext';

type UserProgress = Record<string, { unlockedSection: number }>;
type DashboardTab = DashboardSection;

interface QuestSummary {
  quest: { title: string; description: string; rewardPoints: number; target: number };
  current: number;
  isCompleted: boolean;
  isClaimed: boolean;
  dayNumber: number;
  isOnboarding: boolean;
}

interface DashboardViewProps extends TopicHistoryActions {
  uid?: string;
  userProgress: UserProgress;
  allCourses: CourseData[];
  categoryTitles: Record<CategoryType, string>;
  streak: StreakData;
  recommendation: FocusRecommendation | null;
  onSelectModule: (moduleId: string) => void;
  onBack: () => void;
  pointsEarned: number;
  pointsAvailable?: number;
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
  gamificationState?: GamificationState | null;
  strategyMastery?: StrategyMasteryMap;
  weeklyChallenge?: WeeklyChallengeState | null;
  pointsReload?: () => void;
  curriculumLevel?: CurriculumLevel;
  activeTab?: DashboardTab;
  onTabChange?: (tab: DashboardTab) => void;
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
  { id: 'milestones', label: 'Milestones' },
];

const RANGE_OPTIONS: Array<{ id: DashboardRange; label: string }> = [
  { id: 'week', label: 'Week' },
  { id: 'month', label: 'Month' },
  { id: 'year', label: 'Year' },
];

const Panel: React.FC<{
  eyebrow: string;
  title: string;
  detail?: string;
  action?: React.ReactNode;
  className?: string;
  children: React.ReactNode;
  disclosure?: boolean;
}> = ({ eyebrow, title, detail, action, disclosure = false, className = '', children }) => {
  const mobileAppDesign = useMobileAppDesign();
  if (mobileAppDesign && disclosure) return <details className={`dashboard-disclosure ${className}`}>
    <summary>{title}<span aria-hidden="true">+</span></summary>
    {detail && <p className="dashboard-disclosure-detail">{detail}</p>}
    <div className="dashboard-disclosure-body">{children}</div>
  </details>;
  return (
  <article className={`pr-editorial-panel ${mobileAppDesign ? `dashboard-section ${eyebrow === 'Programme progress' ? 'dashboard-programme' : ''}` : 'rounded-[18px] border border-[var(--outline-soft)] bg-[var(--surface-paper)]'} ${className}`}>
    <div className="flex flex-wrap items-start justify-between gap-3 border-b border-[var(--outline-soft)] px-5 py-4 sm:px-6">
      <div className="min-w-0">
        <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-[var(--ink-muted)]">{eyebrow}</p>
        <h2 className="mt-1 font-serif text-xl font-semibold tracking-[-0.015em] text-[var(--ink-primary)] sm:text-2xl">{title}</h2>
        {detail && <p className={`mt-1 max-w-xl ${mobileAppDesign ? "text-[13px]" : "text-xs"} leading-relaxed text-[var(--ink-muted)]`}>{detail}</p>}
      </div>
      {action && <div className="shrink-0">{action}</div>}
    </div>
    <div className="px-5 py-4 sm:px-6 sm:py-5">{children}</div>
  </article>
  );
};

const DashboardView: React.FC<DashboardViewProps> = ({
  uid, onStudyTopic, onPracticeTopic,
  userProgress,
  allCourses,
  categoryTitles: _categoryTitles,
  streak,
  recommendation,
  onSelectModule,
  onBack,
  pointsEarned,
  pointsAvailable,
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
  gamificationState = null,
  strategyMastery = {},
  weeklyChallenge = null,
  pointsReload,
  curriculumLevel = 'senior',
  activeTab,
  onTabChange,
  darkMode = false,
  onToggleTheme,
}) => {
  const mobileAppDesign = useMobileAppDesign();
  const [localTab, setLocalTab] = useState<DashboardTab>('overview');
  const tab = activeTab ?? localTab;
  const [range, setRange] = useState<DashboardRange>('week');
  const [metric, setMetric] = useState<ActivityMetric>('sessions');
  const [selectedSubjects, setSelectedSubjects] = useState<string[]>([]);
  const subject = selectedSubjects.length === 1 ? selectedSubjects[0] : 'all';
  const scopedSessions = useMemo(() => selectSubjects(studySessions, selectedSubjects), [studySessions, selectedSubjects]);
  const scopedDebriefs = useMemo(() => selectSubjects(studyDebriefs, selectedSubjects), [studyDebriefs, selectedSubjects]);


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
    for (const debrief of studyDebriefs) if (debrief.subject) values.add(debrief.subject);
    for (const observation of allConfidence) if (observation.subject) values.add(observation.subject);
    for (const mock of mockResults) for (const entry of mock.entries) values.add(entry.subjectName);
    return [...values].filter((name, index, names) => names.findIndex(other => sameStudySubject(name, other)) === index).sort((a, b) => a.localeCompare(b));
  }, [studentProfile, studySessions, studyDebriefs, allConfidence, mockResults]);

  const visibleSubjects = useMemo(() => selectedSubjects.length ? subjects.filter(item => selectedSubjects.includes(item)) : subjects, [subjects, selectedSubjects]);

  const rangeBounds = useMemo(() => getRangeBounds(range), [range]);
  const todayKey = toLocalDateKey(new Date());
  const sessionsInRange = useMemo(
    () => filterSessions(scopedSessions, range),
    [scopedSessions, range],
  );
  const confidencePoints = useMemo(
    () => confidenceInRange(selectSubjects(allConfidence, selectedSubjects), range),
    [allConfidence, range, selectedSubjects],
  );
  const activityBuckets = useMemo(
    () => buildActivityBuckets(scopedSessions, range),
    [scopedSessions, range],
  );
  const subjectAllocation = useMemo(
    () => buildSubjectAllocation(sessionsInRange),
    [sessionsInRange],
  );
  const methodRecords = useMemo(() => buildMethodJournal(scopedSessions, scopedDebriefs, range), [scopedSessions, scopedDebriefs, range]);
  const sessionMix = useMemo(() => buildSessionMix(sessionsInRange), [sessionsInRange]);
  const rhythm = useMemo(() => buildStudyRhythm(scopedSessions), [scopedSessions]);
  const masterySummary = useMemo(() => selectedSubjects.length
    ? selectedSubjects.map(item => buildMasterySummary(topicMastery, item)).reduce((total, item) => ({
      notStarted: total.notStarted + item.notStarted, shaky: total.shaky + item.shaky,
      solid: total.solid + item.solid, total: total.total + item.total,
    }), { notStarted: 0, shaky: 0, solid: 0, total: 0 })
    : buildMasterySummary(topicMastery), [topicMastery, selectedSubjects]);
  const mockRecordsInRange = useMemo(() => buildMockSeries(mockResults).filter(mock => {
    const timestamp = new Date(`${mock.date}T12:00:00`).getTime();
    return mock.date <= todayKey
      && timestamp >= rangeBounds.start.getTime()
      && timestamp < rangeBounds.end.getTime();
  }), [mockResults, rangeBounds, todayKey]);
  const mocks = useMemo(
    () => mockRecordsInRange.filter(mock => resolveMockResultKind(mock) === 'full'),
    [mockRecordsInRange],
  );

  const totalMinutes = Math.round(sessionsInRange.reduce((sum, session) => sum + Math.max(0, session.actualSeconds), 0) / 60);
  const activeDays = new Set(sessionsInRange.map(session => session.date)).size;
  const avgConfidence = averageConfidence(confidencePoints);
  const hasLearningEvidence = studySessions.length > 0
    || studyDebriefs.length > 0
    || studyReflections.length > 0
    || mockResults.length > 0;
  const subjectLabel = selectedSubjects.length ? selectedSubjects.join(' · ') : 'All subjects';
  const activityInsights = useMemo(
    () => buildActivityInsights(activityBuckets, metric, subjectLabel),
    [activityBuckets, metric, subjectLabel],
  );
  const confidenceInsights = useMemo(
    () => buildConfidenceInsights(confidencePoints, visibleSubjects),
    [confidencePoints, visibleSubjects],
  );
  const mockInsights = useMemo(
    () => selectedSubjects.length > 1
      ? selectedSubjects.flatMap(item => buildMockInsights(mockRecordsInRange, item, todayKey))
      : buildMockInsights(mockRecordsInRange, subject, todayKey),
    [mockRecordsInRange, selectedSubjects, subject, todayKey],
  );
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

  const completedToday = timetableCompletions[todayKey]?.length ?? 0;
  const nextBlock = completedToday < todayPlan.length ? todayPlan[completedToday] : undefined;

  const activityPanel = <ProgressActivity className="lg:col-span-8" buckets={activityBuckets} metric={metric}
    onMetricChange={setMetric} period={rangeBounds.label} subjectLabel={subjectLabel} onStartStudy={onStartStudy}
    insights={<DashboardInsights id="dashboard-activity-insights" items={activityInsights} context={`${rangeBounds.label} · ${subjectLabel}`} />} />;
  const confidencePanel = <ProgressConfidence className="lg:col-span-12" observations={confidencePoints}
    bounds={rangeBounds} subjects={visibleSubjects} universe={subjects}
    insights={<DashboardInsights id="dashboard-confidence-insights" items={confidenceInsights.length ? confidenceInsights : [{
      id: 'confidence-empty', title: 'Confidence trend', trend: 'building', evidence: 'No confidence debriefs fall inside the selected period yet.',
      guidance: 'Choose a confidence rating after your next completed session and the subject trend will begin here.',
    }]} context={`${rangeBounds.label} · ${subjectLabel}`} note="Confidence is self-reported, not a grade prediction. Every subject in the current filter is included." />} />;
  const mockPanel = <ProgressMocks className="lg:col-span-12" mocks={mocks} period={rangeBounds.label} subjectLabel={subjectLabel}
    insights={<DashboardInsights id="dashboard-mock-insights" items={mockInsights} context={`${rangeBounds.label} · ${subjectLabel}`}
      note="Total-point trends use comparable full mock sittings only. Subject insights also include single-subject results. These are recorded results, not predictions of final grades." />} />;
  const subjectPanel = <ProgressSubjects className="lg:col-span-12" values={subjectAllocation} period={rangeBounds.label} />;
  const methodsPanel = <MethodJournal className="lg:col-span-12" methods={methodRecords} period={rangeBounds.label} />;

  const programmePanel = (
    <Panel
      disclosure
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
    <KobraScope className="nsu-progress"><div className={`${mobileAppDesign ? 'mobile-editorial dashboard-mobile ' : ''}product-shell min-h-screen bg-[var(--surface-canvas)] text-[var(--ink-primary)] transition-colors duration-300`}>
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
          <div className="dashboard-heading flex flex-col gap-6 border-b border-[var(--outline-strong)] pb-7 lg:flex-row lg:items-end lg:justify-between">
            {mobileAppDesign ? <ProgressSectionPicker value={tab} options={TABS} onChange={next => {
              if (activeTab === undefined) setLocalTab(next);
              onTabChange?.(next);
            }} /> : <div className="max-w-3xl">
              <div className="flex items-center gap-3">
                <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[var(--accent-hex)]">Your learning record</p>
                <span className="h-px w-8 bg-[var(--outline-soft)]" aria-hidden="true" />
                <p className="text-xs text-[var(--ink-muted)]">{todayLabel}</p>
                {onToggleTheme && (
                  <button
                    type="button"
                    role="switch"
                    aria-checked={darkMode}
                    onClick={onToggleTheme}
                    aria-label={darkMode ? 'Switch to light mode (Beta)' : 'Switch to dark mode (Beta)'}
                    className="pr-theme-toggle hidden h-10 w-10 items-center justify-center rounded-xl border border-[var(--outline-soft)] bg-[var(--surface-paper)] text-[var(--ink-secondary)] transition-colors hover:border-[var(--outline-strong)] hover:text-[var(--ink-primary)] sm:flex"
                  >
                    {darkMode ? <Sun size={17} /> : <Moon size={17} />}
                  </button>
                )}
              </div>
              <h1 className="pr-page-title">
                Your learning, in motion.
              </h1>
              <p className="mt-4 max-w-xl text-sm leading-relaxed text-[var(--ink-secondary)] sm:text-[15px]">
                Study rhythm, confidence and practice evidence—connected in one clear view.
              </p>
            </div>

            }
            {tab !== 'milestones' && (
              <div className="dashboard-filters">
                <SubjectPicker subjects={subjects} value={selectedSubjects} onChange={setSelectedSubjects} />
                <ProgressTabs label="Dashboard time range" value={range} options={RANGE_OPTIONS.map(item => ({ value: item.id, label: item.label }))} onChange={value => setRange(value as DashboardRange)} />

              </div>
            )}
          </div>

          {tab !== 'milestones' && (!mobileAppDesign || tab === 'overview' || tab === 'study') && <div className="pr-summary-wrap">
            <ProgressSummary period={rangeBounds.label} minutes={totalMinutes} sessions={sessionsInRange.length} activeDays={activeDays}
              confidence={avgConfidence} streak={streak.currentStreak} pointsEarned={pointsEarned} pointsAvailable={pointsAvailable} buckets={activityBuckets} />
          </div>}

          {mobileAppDesign && (tab === 'confidence' || tab === 'practice') && <p className="dashboard-period-scope">{rangeBounds.label} · {subjectLabel}</p>}
          {!mobileAppDesign && <ProgressSections
            value={tab}
            options={TABS}
            onChange={next => {
              if (activeTab === undefined) setLocalTab(next);
              onTabChange?.(next);
            }}
          />}

          <div className="grid grid-cols-1 gap-4 lg:grid-cols-12">
            {tab === 'overview' && (
              <>
                {!hasLearningEvidence ? (
                  <Panel eyebrow="Your learning record" title="Start with one focused session." detail="This dashboard becomes useful as soon as there is real work to reflect back to you." className="lg:col-span-12">
                    <div className="flex flex-col items-start justify-between gap-6 py-2 sm:flex-row sm:items-center">
                      <p className="max-w-2xl font-serif text-2xl font-semibold leading-tight text-[var(--ink-primary)]">Choose a subject, set a short timer and complete your first session. Your rhythm, confidence and study evidence will begin here.</p>
                      {onStartStudy && (
                        <button onClick={onStartStudy} className="inline-flex min-h-12 shrink-0 items-center gap-2 rounded-xl border-[1.5px] border-[var(--outline-strong)] bg-[var(--accent-hex)] px-5 text-sm font-bold text-white shadow-[3px_3px_0_0_var(--outline-strong)]">
                          Start a study session <ArrowRight size={15} />
                        </button>
                      )}
                    </div>
                  </Panel>
                ) : (
                  <>
                {activityPanel}
                <Panel eyebrow="Today" title={nextBlock ? nextBlock.subjectName : 'Choose your next move'} detail={nextBlock ? `${nextBlock.durationMinutes} min · ${nextBlock.sessionType.replace('-', ' ')}` : 'Keep the momentum small and specific.'} className="pr-today lg:col-span-4">
                  <div className="pr-today-body">
                    <div>
                      <p className="pr-today-message">
                        {recommendation?.reason === 'in-progress' ? 'Continue what you started.' : nextBlock ? 'One focused block is enough.' : 'Build evidence, one session at a time.'}
                      </p>
                      {questState && (
                        <div className="mt-6 border-t border-[var(--outline-soft)] pt-4">
                          <div className="flex items-center justify-between gap-3 text-[10px] font-bold uppercase tracking-[0.14em] text-[var(--ink-muted)]">
                            <span>{questState.isOnboarding ? `Day ${questState.dayNumber} quest` : 'Daily quest'}</span>
                            <span className="text-[var(--accent-hex)]">{questState.isCompleted ? 'Completed' : `${Math.min(questState.current, questState.quest.target)}/${questState.quest.target}`}</span>
                          </div>
                          <p className="mt-2 text-sm font-semibold text-[var(--ink-primary)]">{questState.quest.title}</p>
                          <div className="mt-3 h-2.5 overflow-hidden rounded-full bg-[var(--dashboard-track)]">
                            <div className="h-full rounded-full bg-[var(--accent-hex)]" style={{ width: `${Math.min(100, (questState.current / questState.quest.target) * 100)}%` }} />
                          </div>
                        </div>
                      )}
                    </div>
                    <div className="mt-7">
                      {recommendation && recommendation.reason !== 'all-complete' && (
                        <p className="mb-3 text-[11px] leading-relaxed text-[var(--ink-muted)]">
                          {recommendation.reason === 'in-progress'
                            ? 'Suggested because it’s already underway — finishing beats starting fresh.'
                            : 'Suggested because it’s the next module you haven’t opened.'}
                        </p>
                      )}
                      <div className="pr-today-actions">
                      {onStartStudy && (
                        <Button onClick={onStartStudy} variant="outline" className="nsu-ink-outline">
                          Start studying <ArrowRight size={14} />
                        </Button>
                      )}
                      {recommendation && recommendation.reason !== 'all-complete' && (
                        <Button onClick={() => onSelectModule(recommendation.moduleId)} variant="ghost">
                          {recommendation.reason === 'in-progress' ? 'Continue' : 'Open'} {recommendation.title}
                        </Button>
                      )}
                      {questState?.isCompleted && !questState.isClaimed && onClaimQuestReward && (
                        <Button onClick={onClaimQuestReward} variant="outline" className="nsu-ink-outline">
                          Claim {questState.quest.rewardPoints} JP
                        </Button>
                      )}
                      </div>
                    </div>
                  </div>
                </Panel>
                {!mobileAppDesign && confidencePanel}
                {!mobileAppDesign && subjectPanel}
                {programmePanel}
                {methodsPanel}
                {!mobileAppDesign && mockPanel}
                {mobileAppDesign && <nav className="dashboard-section-links" aria-label="Explore your progress">{TABS.slice(1).map(item => <button type="button" key={item.id} onClick={() => { if (activeTab === undefined) setLocalTab(item.id); onTabChange?.(item.id); }}>{item.label}<ArrowRight size={17} /></button>)}</nav>}
                  </>
                )}
                {!hasLearningEvidence && programmePanel}
              </>
            )}

            {tab === 'study' && (
              <>
                <div className="lg:col-span-12">{React.cloneElement(activityPanel, { className: 'lg:col-span-12' })}</div>
                <Panel disclosure eyebrow="Consistency" title="Study rhythm" detail="Thirteen weeks of recorded study activity." className="lg:col-span-7">
                  <StudyRhythmChart weeks={rhythm} />
                </Panel>
                <ProgressBreakdown kind="mix" values={sessionMix} period={rangeBounds.label} className="lg:col-span-5" />
                {subjectPanel}
                {uid && studentProfile && <TopicHistoryPanel uid={uid} profile={studentProfile} sessions={studySessions} onStudyTopic={onStudyTopic} onPracticeTopic={onPracticeTopic} />}
                {methodsPanel}
              </>
            )}

            {tab === 'confidence' && (
              <>
                <div className="lg:col-span-12">{React.cloneElement(confidencePanel, { className: 'lg:col-span-12' })}</div>
                <ProgressBreakdown kind="readiness" summary={masterySummary} className="lg:col-span-12" />
                {!mobileAppDesign && programmePanel}
              </>
            )}

            {tab === 'practice' && (
              <>
                {React.cloneElement(mockPanel, { className: 'lg:col-span-12' })}
                <ProgressBreakdown kind="mix" values={sessionMix} period={rangeBounds.label} className="lg:col-span-6" />
                <ProgressBreakdown kind="readiness" summary={masterySummary} className="lg:col-span-6" />
                {methodsPanel}
              </>
            )}

            {tab === 'milestones' && (gamificationState ? (
              <ProgressMilestones state={gamificationState} streak={streak} sessions={studySessions} strategyMastery={strategyMastery}
                weeklyChallenge={weeklyChallenge} pointsAvailable={pointsAvailable} pointsReload={pointsReload} curriculumLevel={curriculumLevel} />
            ) : (
              <Panel eyebrow="Milestones" title="Progress is loading" detail="Your goals and achievements will appear here." className="lg:col-span-12">
                <div className="h-2 overflow-hidden rounded-full bg-[var(--dashboard-track)]">
                  <div className="h-full w-1/3 animate-pulse rounded-full bg-[var(--accent-hex)]" />
                </div>
              </Panel>
            ))}
          </div>
        </MotionDiv>
      </main>
    </div></KobraScope>
  );
};

export default DashboardView;
