/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useMemo, useState } from 'react';
import './dashboard/dashboard-refined.css';
import { useMobileAppDesign } from '../hooks/useMobileAppDesign';
import { ArrowRight, Check, Moon, Sun } from 'lucide-react';
import { MotionDiv } from './Motion';
import PageHeader from './ui/PageHeader';
import HorizontalTabs from './ui/HorizontalTabs';
import { type CategoryType } from './KnowledgeTree';
import { type CourseData } from './Library';
import { type StreakData } from '../hooks/useStreak';
import { type FocusRecommendation } from '../hooks/useTodaysFocus';
import { type DebriefEntry } from './StudyDebrief';
import { type StudentSubjectProfile } from './subjectData';
import {
  type StudyReflection,
  type StrategyMasteryMap,
  type MasteryTier,
  type TopicMasteryV2,
  type UnifiedMockResult,
} from '../types';
import { STRATEGY_REGISTRY, type StudySessionRecord } from '../utils/strategyRegistry';
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
import DashboardInsights, { InsightsToggle } from './dashboard/DashboardInsights';
import {
  buildActivityInsights,
  buildConfidenceInsights,
  buildMockInsights,
} from './dashboard/dashboardInsightAnalytics';
import { resolveMockResultKind } from '../services/mockResultsRepository';
import {
  generateWeeklyGoals,
  getWeekNumber,
  type GamificationState,
} from '../gamificationConfig';
import { type WeeklyChallengeState } from '../hooks/useWeeklyChallenge';
import AchievementGallery from './AchievementGallery';
import { type CurriculumLevel } from '../utils/authUtils';
import { getAchievementsForCurriculum } from '../achievementData';
import { type DashboardSection } from '../contexts/NavigationContext';

type UserProgress = Record<string, { unlockedSection: number }>;
type DashboardTab = DashboardSection;
type InsightPanelId = 'activity' | 'confidence' | 'mock';

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

const MASTERY_TIER_LABELS: Record<MasteryTier, string> = {
  none: 'Not started',
  learned: 'Learned',
  practiced: 'Practised',
  applied: 'Applied',
  habitual: 'Habitual',
};

const MASTERY_TIER_INDEX: Record<MasteryTier, number> = {
  none: 0,
  learned: 1,
  practiced: 2,
  applied: 3,
  habitual: 4,
};

const PERSONAL_BESTS = [
  { key: 'bestDayPoints', label: 'Points in one day' },
  { key: 'bestDaySections', label: 'Sections in one day' },
  { key: 'bestWeekPoints', label: 'Points in one week' },
  { key: 'bestWeekSessions', label: 'Sessions in one week' },
] as const;

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
}> = ({ eyebrow, title, detail, action, className = '', children }) => {
  const mobileAppDesign = useMobileAppDesign();
  return (
  <article className={`${mobileAppDesign ? `dashboard-section ${eyebrow === 'Programme progress' ? 'dashboard-programme' : ''}` : 'rounded-[18px] border border-[var(--outline-soft)] bg-[var(--surface-paper)]'} ${className}`}>
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

const StatCell: React.FC<{ eyebrow: string; value: string; meta: string; accent?: boolean }> = ({ eyebrow, value, meta, accent }) => (
  <div className="w-[112px] shrink-0 border-r border-[var(--outline-soft)] pr-4 last:border-r-0 sm:w-auto sm:border-r-0 sm:pr-0 lg:border-l lg:pl-5 lg:first:border-l-0 lg:first:pl-0">
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
}) => {
  const mobileAppDesign = useMobileAppDesign();
  return (
  <div className="inline-flex rounded-xl border border-[var(--outline-soft)] bg-[var(--surface-soft)] p-1" role="group" aria-label={label}>
    {options.map(option => (
      <button
        key={option.id}
        type="button"
        aria-pressed={value === option.id}
        onClick={() => onChange(option.id)}
        className={`${mobileAppDesign ? 'min-h-11 text-[13px]' : 'min-h-8 text-[11px]'} rounded-lg px-3 font-semibold transition-colors ${
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
};

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
  const [subject, setSubject] = useState('all');
  const [achievementsOpen, setAchievementsOpen] = useState(false);
  const [openInsights, setOpenInsights] = useState<Record<InsightPanelId, boolean>>({
    activity: false,
    confidence: false,
    mock: false,
  });

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
  const todayKey = toLocalDateKey(new Date());
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
  const subjectLabel = subject === 'all' ? 'All subjects' : subject;
  const activityInsights = useMemo(
    () => buildActivityInsights(activityBuckets, metric, subjectLabel),
    [activityBuckets, metric, subjectLabel],
  );
  const confidenceInsights = useMemo(
    () => buildConfidenceInsights(confidencePoints, subject === 'all' ? subjects : [subject]),
    [confidencePoints, subject, subjects],
  );
  const mockInsights = useMemo(
    () => buildMockInsights(mockRecordsInRange, subject, todayKey),
    [mockRecordsInRange, subject, todayKey],
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

  const weeklyGoals = gamificationState
    ? generateWeeklyGoals(gamificationState.currentRank.id, getWeekNumber())
    : [];
  const currentDay = new Date().getDay();
  const daysUntilWeeklyReset = currentDay === 0 ? 1 : 8 - currentDay;
  const strategyMilestones = useMemo(() => STRATEGY_REGISTRY
    .map(strategy => ({
      ...strategy,
      record: strategyMastery[strategy.moduleId] ?? { tier: 'none' as const, sessionCount: 0, subjectsSeen: [] },
    }))
    .filter(item => item.record.tier !== 'none')
    .sort((a, b) => MASTERY_TIER_INDEX[b.record.tier] - MASTERY_TIER_INDEX[a.record.tier]),
  [strategyMastery]);
  const personalBests = useMemo(() => PERSONAL_BESTS
    .map(item => ({ ...item, value: gamificationState?.personalBests[item.key] ?? 0 }))
    .filter(item => item.value > 0),
  [gamificationState?.personalBests]);
  const achievementSummary = useMemo(() => {
    const available = getAchievementsForCurriculum(curriculumLevel);
    const unlocked = new Set(gamificationState?.unlockedAchievements ?? []);
    return {
      unlocked: available.filter(item => unlocked.has(item.id)).length,
      visible: available.filter(item => !item.isHidden || unlocked.has(item.id)).length,
    };
  }, [curriculumLevel, gamificationState?.unlockedAchievements]);

  const toggleInsights = (panel: InsightPanelId) => {
    setOpenInsights(current => ({ ...current, [panel]: !current[panel] }));
  };

  const activityPanel = (
    <Panel
      eyebrow="Study activity"
      title={metric === 'sessions' ? 'Sessions logged' : 'Focused minutes'}
      detail={`${rangeBounds.label}${subject === 'all' ? ' · all subjects' : ` · ${subject}`}`}
      action={
        <div className="flex flex-wrap justify-end gap-2">
          <SegmentedControl
            label="Study activity measure"
            value={metric}
            options={[{ id: 'sessions', label: 'Sessions' }, { id: 'minutes', label: 'Minutes' }]}
            onChange={value => setMetric(value as ActivityMetric)}
          />
          <InsightsToggle
            controls="dashboard-activity-insights"
            expanded={openInsights.activity}
            onToggle={() => toggleInsights('activity')}
            chartLabel="study activity"
          />
        </div>
      }
      className="lg:col-span-8"
    >
      {openInsights.activity && (
        <DashboardInsights
          id="dashboard-activity-insights"
          items={activityInsights}
          context={`${rangeBounds.label} · ${subjectLabel}`}
        />
      )}
      <ActivityChart buckets={activityBuckets} metric={metric} />
      {mobileAppDesign && sessionsInRange.length === 0 && onStartStudy && <div className="border-t border-[var(--outline-soft)] pt-4"><p className="text-sm text-[var(--ink-secondary)]">No sessions recorded for {subjectLabel.toLowerCase()} in this period.</p><button type="button" onClick={onStartStudy} className="mt-2 min-h-11 text-sm font-semibold underline underline-offset-4">Plan your next session</button></div>}
    </Panel>
  );

  const confidencePanel = (
    <Panel
      eyebrow="Debrief signal"
      title="Confidence over time"
      detail={mobileAppDesign ? "Your own ratings after study sessions. A reflection signal, not a grade prediction." : "Each point is a confidence choice made after a completed study session."}
      action={
        <InsightsToggle
          controls="dashboard-confidence-insights"
          expanded={openInsights.confidence}
          onToggle={() => toggleInsights('confidence')}
          chartLabel="confidence chart"
        />
      }
      className="lg:col-span-7"
    >
      {openInsights.confidence && (
        <DashboardInsights
          id="dashboard-confidence-insights"
          items={confidenceInsights.length > 0 ? confidenceInsights : [{
            id: 'confidence-empty',
            title: subject === 'all' ? 'Confidence trend' : subject,
            trend: 'building',
            evidence: 'No confidence debriefs fall inside the selected period yet.',
            guidance: 'Choose a confidence rating after your next completed session and the subject trend will begin here.',
          }]}
          context={`${rangeBounds.label} · ${subjectLabel}`}
          note="Confidence is self-reported. Use it as a reflection signal, not a grade prediction. The chart plots up to five subjects for readability; this reading includes every subject in the current filter."
        />
      )}
      <ConfidenceChart observations={confidencePoints} bounds={rangeBounds} />
    </Panel>
  );

  const mockPanel = (
    <Panel
      eyebrow="Exam evidence"
      title="Mock trajectory"
      detail={subject === 'all'
        ? 'Total points from full mock sittings in Points Passport.'
        : `Full mock totals stay all-subject · insights focus on ${subject}.`}
      action={
        <InsightsToggle
          controls="dashboard-mock-insights"
          expanded={openInsights.mock}
          onToggle={() => toggleInsights('mock')}
          chartLabel="mock trajectory"
        />
      }
      className="lg:col-span-6"
    >
      {openInsights.mock && (
        <DashboardInsights
          id="dashboard-mock-insights"
          items={mockInsights}
          context={`${rangeBounds.label} · ${subjectLabel}`}
          note={subject === 'all'
            ? 'Total-point trends use comparable full mock sittings only; single-subject results are kept out of the total. These are recorded results, not a prediction of final grades.'
            : `${subject} insights use that subject’s grades from full mocks and single results. The chart remains full-sitting totals and is not a prediction of final grades.`}
        />
      )}
      <MockTrajectoryChart mocks={mocks} />
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
              <h1 className="mt-3 max-w-2xl font-serif text-[clamp(34px,6vw,68px)] font-semibold leading-[0.97] tracking-[-0.045em] text-[var(--ink-primary)] sm:mt-4">
                Your learning,<br />in motion.
              </h1>
              <p className="mt-4 max-w-xl text-sm leading-relaxed text-[var(--ink-secondary)] sm:text-[15px]">
                Study rhythm, confidence and practice evidence—connected in one clear view.
              </p>
            </div>

            {tab !== 'milestones' && (
              <div className="flex flex-wrap items-end gap-2 lg:max-w-md lg:justify-end">
                <label className={mobileAppDesign ? "min-w-0 basis-full lg:min-w-[200px] lg:flex-1 lg:basis-auto" : "min-w-[160px] flex-1 lg:flex-none"}>
                  <span className="sr-only">Filter by subject</span>
                  <select
                    value={subject}
                    onChange={event => setSubject(event.target.value)}
                    className={`${mobileAppDesign ? "min-h-12 text-base font-medium" : "h-10 text-xs font-semibold"} w-full rounded-xl border border-[var(--outline-soft)] bg-[var(--surface-paper)] px-3 text-[var(--ink-secondary)] outline-none focus:border-[var(--accent-hex)]`}
                  >
                    <option value="all">All subjects</option>
                    {subjects.map(item => <option key={item} value={item}>{item}</option>)}
                  </select>
                </label>
                <SegmentedControl label="Dashboard time range" value={range} options={RANGE_OPTIONS} onChange={value => setRange(value as DashboardRange)} />
                {onToggleTheme && (
                  <button
                    type="button"
                    role="switch"
                    aria-checked={darkMode}
                    onClick={onToggleTheme}
                    aria-label={darkMode ? 'Switch to light mode (Beta)' : 'Switch to dark mode (Beta)'}
                    className="hidden h-10 w-10 items-center justify-center rounded-xl border border-[var(--outline-soft)] bg-[var(--surface-paper)] text-[var(--ink-secondary)] transition-colors hover:border-[var(--outline-strong)] hover:text-[var(--ink-primary)] sm:flex"
                  >
                    {darkMode ? <Sun size={17} /> : <Moon size={17} />}
                  </button>
                )}
              </div>
            )}
          </div>

          <div className="-mx-4 flex gap-5 overflow-x-auto border-b border-[var(--outline-soft)] px-4 py-5 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden sm:mx-0 sm:grid sm:grid-cols-5 sm:gap-x-4 sm:overflow-visible sm:px-0 sm:py-6">
            <StatCell eyebrow="Sessions" value={String(sessionsInRange.length)} meta={`${activeDays} active day${activeDays === 1 ? '' : 's'}`} accent />
            <StatCell eyebrow="Focus time" value={formatMinutes(totalMinutes)} meta={rangeBounds.label} />
            <StatCell eyebrow="Confidence" value={avgConfidence === null ? '—' : avgConfidence.toFixed(1)} meta={avgConfidence === null ? 'awaiting debriefs' : 'average out of 5'} />
            <StatCell eyebrow="Streak" value={String(streak.currentStreak)} meta={mobileAppDesign ? "days · all subjects" : "days running"} />
            <StatCell eyebrow="Journey points" value={String(pointsEarned)} meta="earned to date" />
          </div>

          <HorizontalTabs
            className="mb-5 mt-6"
            value={tab}
            options={TABS.map(item => ({ value: item.id, label: item.label }))}
            label="Dashboard sections"
            onChange={next => {
              if (activeTab === undefined) setLocalTab(next);
              onTabChange?.(next);
            }}
          />

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
                            <span className="text-[var(--accent-hex)]">{questState.isCompleted ? 'Completed' : `${Math.min(questState.current, questState.quest.target)}/${questState.quest.target}`}</span>
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
                          {recommendation.reason === 'in-progress' ? 'Continue' : 'Open'} {recommendation.title}
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
                {mockPanel}
                  </>
                )}
                {!hasLearningEvidence && programmePanel}
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
                {React.cloneElement(mockPanel, { className: 'lg:col-span-8' })}
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

            {tab === 'milestones' && (gamificationState ? (
              <>
                <Panel
                  eyebrow="Rank progress"
                  title={gamificationState.currentRank.title}
                  detail={gamificationState.nextRank
                    ? `${Math.max(0, gamificationState.nextRank.minPoints - gamificationState.totalPointsEarned).toLocaleString()} XP to ${gamificationState.nextRank.title}`
                    : 'Highest rank reached.'}
                  className="lg:col-span-4"
                >
                  <div className="flex items-end justify-between gap-4">
                    <div>
                      <p className="font-serif text-4xl font-semibold tabular-nums text-[var(--ink-primary)]">
                        {gamificationState.totalPointsEarned.toLocaleString()}
                      </p>
                      <p className="mt-1 text-[10px] font-bold uppercase tracking-[0.15em] text-[var(--ink-muted)]">Total XP</p>
                    </div>
                    <p className="font-serif text-2xl font-semibold tabular-nums text-[var(--accent-hex)]">{gamificationState.rankProgress}%</p>
                  </div>
                  <div className="mt-5 h-2 overflow-hidden rounded-full bg-[var(--dashboard-track)]" aria-label={`${gamificationState.rankProgress}% rank progress`}>
                    <div className="h-full rounded-full bg-[var(--accent-hex)]" style={{ width: `${gamificationState.rankProgress}%` }} />
                  </div>
                  <div className="mt-5 border-t border-[var(--outline-soft)] pt-4 text-xs leading-relaxed text-[var(--ink-muted)]">
                    <p><strong className="text-[var(--ink-secondary)]">XP</strong> is your lifetime activity score and sets your rank.</p>
                    <p className="mt-2"><strong className="text-[var(--ink-secondary)]">JP</strong> is the spendable balance used to build My Journey.</p>
                    <p className="mt-2"><strong className="text-[var(--ink-secondary)]">Passport stamps</strong> mark modules you have completed.</p>
                  </div>
                </Panel>

                <Panel
                  eyebrow="This week"
                  title="Three useful targets"
                  detail={`Resets in ${daysUntilWeeklyReset} day${daysUntilWeeklyReset === 1 ? '' : 's'}.`}
                  className="lg:col-span-8"
                >
                  <div className="space-y-4">
                    {weeklyGoals.map(goal => {
                      const current = gamificationState.weeklyGoalProgress[goal.metric] ?? 0;
                      const complete = current >= goal.target;
                      const progress = Math.min(100, Math.round((current / goal.target) * 100));
                      return (
                        <div key={goal.id}>
                          <div className="mb-1.5 flex items-center justify-between gap-4">
                            <div className="flex min-w-0 items-center gap-2">
                              {complete && <Check size={14} className="shrink-0 text-[var(--success-hex)]" aria-hidden="true" />}
                              <p className={`truncate text-xs font-semibold ${complete ? 'text-[var(--success-hex)]' : 'text-[var(--ink-secondary)]'}`}>{goal.label}</p>
                            </div>
                            <p className="shrink-0 text-xs font-bold tabular-nums text-[var(--ink-muted)]">{Math.min(current, goal.target)}/{goal.target}</p>
                          </div>
                          <div className="h-1.5 overflow-hidden rounded-full bg-[var(--dashboard-track)]">
                            <div
                              className={`h-full rounded-full ${complete ? 'bg-[var(--success-hex)]' : 'bg-[var(--accent-hex)]'}`}
                              style={{ width: `${progress}%` }}
                            />
                          </div>
                        </div>
                      );
                    })}

                    {weeklyChallenge?.isLoaded && weeklyChallenge.challenge && (
                      <div className="border-t border-[var(--outline-soft)] pt-4">
                        <div className="flex flex-wrap items-start justify-between gap-3">
                          <div className="min-w-0">
                            <p className="text-[9px] font-bold uppercase tracking-[0.16em] text-[var(--ink-muted)]">Weekly challenge</p>
                            <p className="mt-1 text-sm font-semibold text-[var(--ink-primary)]">{weeklyChallenge.challenge.title}</p>
                            <p className="mt-1 text-xs leading-relaxed text-[var(--ink-muted)]">{weeklyChallenge.challenge.description}</p>
                          </div>
                          {weeklyChallenge.isClaimed ? (
                            <span className="inline-flex min-h-9 items-center gap-1.5 text-xs font-bold text-[var(--success-hex)]">
                              <Check size={14} /> Reward claimed
                            </span>
                          ) : weeklyChallenge.isCompleted ? (
                            <button
                              type="button"
                              onClick={async () => {
                                await weeklyChallenge.claimReward();
                                pointsReload?.();
                              }}
                              className="inline-flex min-h-9 items-center rounded-xl border border-[var(--accent-hex)] px-3 text-xs font-bold text-[var(--accent-hex)]"
                            >
                              Claim {weeklyChallenge.challenge.rewardPoints} JP
                            </button>
                          ) : (
                            <span className="text-xs font-bold tabular-nums text-[var(--accent-hex)]">{weeklyChallenge.current}/{weeklyChallenge.challenge.target}</span>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                </Panel>

                <Panel
                  eyebrow="Learning methods"
                  title="Strategy milestones"
                  detail="How far learned techniques have travelled into real study sessions."
                  className="lg:col-span-7"
                >
                  {strategyMilestones.length > 0 ? (
                    <div className="divide-y divide-[var(--outline-soft)]">
                      {strategyMilestones.map(item => (
                        <div key={item.moduleId} className="py-3 first:pt-0 last:pb-0">
                          <div className="flex items-center justify-between gap-4">
                            <p className="min-w-0 truncate text-sm font-semibold text-[var(--ink-primary)]">{item.strategyName}</p>
                            <span className="shrink-0 text-[10px] font-bold uppercase tracking-[0.12em] text-[var(--accent-hex)]">{MASTERY_TIER_LABELS[item.record.tier]}</span>
                          </div>
                          <div className="mt-2 flex items-center gap-3">
                            <div className="grid flex-1 grid-cols-4 gap-1" aria-label={`${MASTERY_TIER_LABELS[item.record.tier]} mastery`}>
                              {[1, 2, 3, 4].map(level => (
                                <span key={level} className={`h-1.5 rounded-full ${level <= MASTERY_TIER_INDEX[item.record.tier] ? 'bg-[var(--accent-hex)]' : 'bg-[var(--dashboard-track)]'}`} />
                              ))}
                            </div>
                            <p className="shrink-0 text-[10px] text-[var(--ink-muted)]">{item.record.sessionCount} session{item.record.sessionCount === 1 ? '' : 's'}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-sm leading-relaxed text-[var(--ink-muted)]">Complete a strategy module, then use that technique during a study session to begin tracking it here.</p>
                  )}
                </Panel>

                <Panel
                  eyebrow="Personal records"
                  title="Best efforts"
                  detail="Your strongest recorded days and weeks—not a target you have to beat every time."
                  className="lg:col-span-5"
                >
                  {personalBests.length > 0 ? (
                    <div className="grid grid-cols-2 gap-x-5 gap-y-6">
                      {personalBests.map(item => (
                        <div key={item.key}>
                          <p className="font-serif text-3xl font-semibold tabular-nums text-[var(--ink-primary)]">{item.value.toLocaleString()}</p>
                          <p className="mt-1 text-[10px] leading-snug text-[var(--ink-muted)]">{item.label}</p>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-sm leading-relaxed text-[var(--ink-muted)]">Your first completed sessions and modules will establish personal records here.</p>
                  )}
                </Panel>

                <Panel
                  eyebrow="Recognition"
                  title="Achievements"
                  detail="Milestones earned across modules, study habits, reflection and your journey."
                  action={
                    <button
                      type="button"
                      aria-expanded={achievementsOpen}
                      onClick={() => setAchievementsOpen(open => !open)}
                      className="min-h-9 rounded-xl border border-[var(--outline-soft)] px-3 text-xs font-bold text-[var(--ink-secondary)] transition-colors hover:border-[var(--outline-strong)]"
                    >
                      {achievementsOpen ? 'Hide gallery' : 'View gallery'}
                    </button>
                  }
                  className="lg:col-span-12"
                >
                  {achievementsOpen ? (
                    <AchievementGallery
                      unlockedAchievements={gamificationState.unlockedAchievements}
                      achievementTimestamps={gamificationState.achievementTimestamps}
                      curriculumLevel={curriculumLevel}
                      showHeader={false}
                    />
                  ) : (
                    <div className="flex items-end gap-8">
                      <div>
                        <p className="font-serif text-4xl font-semibold tabular-nums text-[var(--ink-primary)]">{achievementSummary.unlocked}</p>
                        <p className="mt-1 text-[10px] font-bold uppercase tracking-[0.15em] text-[var(--ink-muted)]">Earned</p>
                      </div>
                      <div>
                        <p className="font-serif text-2xl font-semibold tabular-nums text-[var(--ink-secondary)]">{achievementSummary.visible}</p>
                        <p className="mt-1 text-[10px] font-bold uppercase tracking-[0.15em] text-[var(--ink-muted)]">Visible milestones</p>
                      </div>
                    </div>
                  )}
                </Panel>
              </>
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
    </div>
  );
};

export default DashboardView;
