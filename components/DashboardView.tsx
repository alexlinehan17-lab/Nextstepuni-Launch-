import { sameStudySubject } from '../services/studyTopicHistory';
import TopicHistoryPanel from './topics/TopicHistoryPanel';
import type { TopicHistoryActions } from './topics/TopicDetailCard';
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect, useMemo, useState } from 'react';
import KobraScope from './approved-ui-runtime';
import { ProgressPointsGoal } from './dashboard/progress/ProgressPointsGoal';
import { caoGoalStanding } from './dashboard/progress/caoGoal';
import { ProgressConfidence, ProgressMocks } from './dashboard/progress/ProgressCharts';
import { MethodJournal } from './dashboard/progress/MethodJournal';
import { Artwork } from './dashboard/progress/shared';
import { buildMethodJournal, selectSubjects } from './dashboard/progress/progressData';
import './dashboard/progress/my-progress.css';
import { ProgressMilestones } from './dashboard/progress/ProgressMilestones';
import { ProgressGraph, formatMinutes } from './dashboard/progress/ProgressGraph';
import { Bar, ConfidenceScale, Duration, Figures, NextPart, ReadinessStrip, Section, SubjectBars, confidenceWord, type Figure } from './dashboard/progress/ProgressParts';
import SubjectAvatar from './SubjectAvatar';
import { Button, TextButton } from './ui/Button';
import { SelectionWords, Switch } from './ui/Choice';
import { Menu } from './ui/Menu';
import { Sheet } from './ui/Sheet';
import { List, Row } from './ui/List';
import { TopBar } from './ui/Bars';
import { LoadingShape } from './ui/States';

import { useMobileAppDesign } from '../hooks/useMobileAppDesign';
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
import { useDatedStudyPlan } from '../hooks/useDatedStudyPlan';
import { getBlockId } from './subjectData';
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
  /** Opens Change subjects, where current and target grades live. */
  onEditGrades?: () => void;
  /** Opens the Points Passport, where mock results are recorded. */
  onAddMockResult?: () => void;
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

/** What each kind of session is for, read out with its bar. */
const MIX_NOTES: Record<string, string> = {
  'new-learning': 'Getting started with unfamiliar material.',
  practice: 'Putting what you know to work.',
  revision: 'Returning to material you have studied.',
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
  darkMode: _darkMode = false,
  onToggleTheme: _onToggleTheme,
  onEditGrades,
  onAddMockResult,
}) => {
  const mobileAppDesign = useMobileAppDesign();
  const pointsGoal = useMemo(() => caoGoalStanding(studentProfile, mockResults, curriculumLevel), [studentProfile, mockResults, curriculumLevel]);
  const [localTab, setLocalTab] = useState<DashboardTab>('overview');
  const tab = activeTab ?? localTab;
  const [range, setRange] = useState<DashboardRange>('week');
  const [metric, setMetric] = useState<ActivityMetric>('sessions');
  const [selectedSubjects, setSelectedSubjects] = useState<string[]>([]);
  const [insights, setInsights] = useState<'activity' | 'confidence' | 'mocks' | null>(null);
  const [average, setAverage] = useState(false);
  const [readNumbers, setReadNumbers] = useState(false);
  const [climbsOpen, setClimbsOpen] = useState(false);
  const [rhythmOpen, setRhythmOpen] = useState(false);
  const [subjectOrder, setSubjectOrder] = useState<'time' | 'name'>('time');
  // The bar gains its hairline once the page has scrolled under it (tokens.md, "Bars").
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    if (!mobileAppDesign) return undefined;
    const update = () => setScrolled(window.scrollY > 4);
    update();
    window.addEventListener('scroll', update, { passive: true });
    return () => window.removeEventListener('scroll', update);
  }, [mobileAppDesign]);
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
  const dated = useDatedStudyPlan(studentProfile, uid);
  const todayPlan = useMemo(() => {
    if (dated.enabled) return dated.timetable?.[(new Date().getDay()+6)%7]?.blocks ?? [];
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
  }, [studentProfile, dated.enabled, dated.timetable, dated.today]);

  const nextBlock = todayPlan.find((block,index) => !(timetableCompletions[todayKey] ?? []).includes(getBlockId(block,index)) && !dated.saved?.plan.tasks.some(t=>t.id===block.id&&t.status==='completed'));

  const goToPart = (next: DashboardTab) => {
    if (activeTab === undefined) setLocalTab(next);
    onTabChange?.(next);
  };
  const partIndex = Math.max(0, TABS.findIndex(item => item.id === tab));
  const nextPart = TABS[partIndex + 1];
  const next = nextPart ? <NextPart position={partIndex + 2} of={TABS.length} name={nextPart.label} onPress={() => goToPart(nextPart.id)} /> : null;
  const rangeWord = range === 'year' ? 'year' : range === 'month' ? 'month' : 'week';
  const periodLabel = range === 'month' ? rangeBounds.label.replace(/\s\d{4}$/, '') : rangeBounds.label;
  const noTime = visibleSubjects.filter(name => !subjectAllocation.some(item => item.value > 0 && sameStudySubject(item.label, name)));
  const insightsFor = (key: 'activity' | 'confidence' | 'mocks') => setInsights(key);
  const activityTotal = activityBuckets.reduce((sum, bucket) => sum + bucket[metric], 0);
  const activityDays = activityBuckets.filter(bucket => bucket.sessions > 0).length;
  const activityMinutes = activityBuckets.reduce((sum, bucket) => sum + bucket.minutes, 0);
  const activitySessions = activityBuckets.reduce((sum, bucket) => sum + bucket.sessions, 0);
  const bestBucket = activityBuckets.reduce((best, bucket) => bucket.minutes > best ? bucket.minutes : best, 0);
  const mixTotal = sessionMix.reduce((sum, item) => sum + item.value, 0);
  const latestConfidence = visibleSubjects.map(name => {
    const entries = confidencePoints.filter(point => sameStudySubject(point.subject, name)).sort((a, b) => a.timestamp - b.timestamp);
    return { name, count: entries.length, latest: entries[entries.length - 1]?.score ?? null };
  });
  const confidenceRows = latestConfidence.filter(item => item.latest !== null).sort((a, b) => (b.latest ?? 0) - (a.latest ?? 0));
  const noCheckIns = latestConfidence.filter(item => item.latest === null).map(item => item.name);

  const figuresOverview: Figure[] = [
    { name: 'Sessions', value: sessionsInRange.length, description: `Across ${activeDays} active day${activeDays === 1 ? '' : 's'}. Completed sessions in the selected period and subjects.` },
    { name: 'Confidence', value: avgConfidence === null ? '–' : avgConfidence.toFixed(1), unit: avgConfidence === null ? undefined : '/ 5', description: avgConfidence === null ? 'Awaiting your first check-in' : 'Your check-in, out of 5. This is not a grade prediction.' },
    { name: 'Study streak', value: streak.currentStreak, unit: 'days', description: 'Consecutive days · all subjects. It is independent of the selected subjects and period.' },
  ];
  const figuresStudy: Figure[] = [
    { name: 'Time in total', value: <Duration minutes={activityMinutes} /> },
    { name: range === 'year' ? 'Best month' : 'Best day', value: activityMinutes ? <Duration minutes={bestBucket} /> : '–' },
    { name: 'Average session', value: activitySessions ? <Duration minutes={Math.round(activityMinutes / activitySessions)} /> : '–' },
  ];

  const journeyPoints = (
    <div className="mp-jp">
      <Artwork src="/assets/star-crew/companions/islander.png" size={76} />
      <div className="mp-jp-text">
        <p className="t-label mp-label">Journey points</p>
        <p className="mp-jp-line"><strong className="mp-jp-number">{pointsEarned.toLocaleString()}</strong> <span className="t-sub">earned to date</span></p>
        {pointsAvailable !== undefined && <p className="t-meta">{pointsAvailable.toLocaleString()} available to spend</p>}
      </div>
    </div>
  );

  const insightSheet = (
    <Sheet open={insights !== null} onClose={() => setInsights(null)} title="What the pattern suggests" titleSize="small">
      {insights === 'activity' && <>
        <div className="mp-insight-switch"><span className="t-body">Show period average</span><Switch checked={average} onChange={setAverage} label="Show period average" /></div>
        <p className="t-meta">The average covers elapsed days or months in this period. It isn’t a study target.</p>
        <DashboardInsights id="dashboard-activity-insights" items={activityInsights} context={`${rangeBounds.label} · ${subjectLabel}`} />
      </>}
      {insights === 'confidence' && <DashboardInsights id="dashboard-confidence-insights" items={confidenceInsights.length ? confidenceInsights : [{
        id: 'confidence-empty', title: 'Confidence trend', trend: 'building', evidence: 'No confidence debriefs fall inside the selected period yet.',
        guidance: 'Choose a confidence rating after your next completed session and the subject trend will begin here.',
      }]} context={`${rangeBounds.label} · ${subjectLabel}`} note="Confidence is self-reported, not a grade prediction. Every subject in the current filter is included." />}
      {insights === 'mocks' && <DashboardInsights id="dashboard-mock-insights" items={mockInsights} context={`${rangeBounds.label} · ${subjectLabel}`}
        note="Total-point trends use comparable full mock sittings only. Subject insights also include single-subject results. These are recorded results, not predictions of final grades." />}
    </Sheet>
  );

  const programme = (
    <Section label="Programme progress" title="Five climbs, all your own." className="mp-programme">
      <p className="t-sub">{fiveWorldCompleted === 0
        ? 'Your first completed module paints the first mountain.'
        : `${fiveWorldCompleted} of ${fiveWorldTotal} modules complete · each mountain fills as you progress.`}</p>
      {mobileAppDesign && <TextButton arrow="menu" aria-expanded={climbsOpen} onClick={() => setClimbsOpen(open => !open)}>{climbsOpen ? 'Hide the climbs' : 'Show the climbs'}</TextButton>}
      {(!mobileAppDesign || climbsOpen) && <>
        <div className="mp-climbs"><div className="mp-climbs-art"><MountainLandscape progress={worldProgress} /></div></div>
        {mobileAppDesign && <p className="t-meta">Swipe across to explore all five climbs.</p>}
        <Figures className="mp-figs--four" items={[
          { name: 'Overall', value: overallPct, unit: '%' },
          { name: 'Modules', value: fiveWorldCompleted, unit: `/ ${fiveWorldTotal}` },
          { name: 'Furthest along', value: WORLD_LABEL[furthest.world], unit: `${furthest.percent}%` },
          { name: 'Longest streak', value: streak.longestStreak ?? streak.currentStreak, unit: 'days' },
        ]} />
      </>}
    </Section>
  );

  const today = (
    <Section label="Today" title={nextBlock ? nextBlock.subjectName : 'Choose your next move'} className="mp-today">
      <p className="t-meta">{nextBlock ? `${nextBlock.durationMinutes} min · ${nextBlock.sessionType.replace('-', ' ')}` : 'Keep the momentum small and specific.'}</p>
      <p className="t-body">{recommendation?.reason === 'in-progress' ? 'Continue what you started.' : nextBlock ? 'One focused block is enough.' : 'Build evidence, one session at a time.'}</p>
      {questState && <div className="mp-quest">
        <Bar title={<><span className="t-label mp-label">{questState.isOnboarding ? `Day ${questState.dayNumber} quest` : 'Daily quest'}</span><span className="mp-quest-title">{questState.quest.title}</span></>}
          readout={questState.isCompleted ? 'Completed' : `${Math.min(questState.current, questState.quest.target)} / ${questState.quest.target}`}
          share={Math.min(1, questState.current / questState.quest.target)} done={questState.isCompleted} />
      </div>}
      {recommendation && recommendation.reason !== 'all-complete' && <p className="t-meta">
        {recommendation.reason === 'in-progress' ? 'Suggested because it’s already underway — finishing beats starting fresh.' : 'Suggested because it’s the next module you haven’t opened.'}
      </p>}
      <div className="mp-actions">
        {onStartStudy && <Button arrow="forward" onClick={onStartStudy}>Start studying</Button>}
        {questState?.isCompleted && !questState.isClaimed && onClaimQuestReward && <Button onClick={onClaimQuestReward}>{`Claim ${questState.quest.rewardPoints} JP`}</Button>}
        {recommendation && recommendation.reason !== 'all-complete' && <TextButton arrow="forward" onClick={() => onSelectModule(recommendation.moduleId)}>{`${recommendation.reason === 'in-progress' ? 'Continue' : 'Open'} ${recommendation.title}`}</TextButton>}
      </div>
    </Section>
  );

  const studyGraph = (
    <Section ruled={false} label={`${periodLabel} · Study activity`} title={metric === 'sessions' ? `Your ${rangeWord} in focus.` : 'The time you made.'} big className="mp-activity">
      <p className="mp-bigline"><span className="mp-big">{metric === 'sessions' ? activityTotal : <Duration minutes={activityTotal} />}</span>
        <span className="t-sub">{`${metric === 'sessions' ? (activityTotal === 1 ? 'session' : 'sessions') : 'of study'} across ${activityDays} active ${range === 'year' ? 'months' : 'days'}`}</span></p>
      {activityTotal === 0 ? <div className="mp-empty"><p className="t-body">No study sessions in this period.</p><p className="t-meta">Your next completed session will update this graph.</p>
        {onStartStudy && <Button arrow="forward" onClick={onStartStudy}>Plan your next session</Button>}</div>
        : readNumbers ? <table className="mp-table"><caption className="t-meta">{`${rangeBounds.label} · ${subjectLabel}`}</caption><thead><tr><th scope="col">Date</th><th scope="col">Sessions</th><th scope="col">Minutes</th></tr></thead>
          <tbody>{activityBuckets.map(day => <tr key={day.key}><th scope="row">{day.accessibleLabel}</th><td>{day.sessions}</td><td>{day.minutes}</td></tr>)}</tbody></table>
        : <div role="img" aria-label={`Study activity chart showing ${metric}`}><ProgressGraph buckets={activityBuckets} metric={metric} height={mobileAppDesign ? 168 : 230} average={average} /></div>}
      <Figures items={figuresStudy} />
      <div className="mp-graph-actions">
        <TextButton tone="quiet" onClick={() => setMetric(metric === 'sessions' ? 'minutes' : 'sessions')}>{metric === 'sessions' ? 'Show minutes' : 'Show sessions'}</TextButton>
        <TextButton tone="quiet" onClick={() => setReadNumbers(value => !value)}>{readNumbers ? 'Show graph' : 'Read the numbers'}</TextButton>
        <TextButton tone="quiet" aria-label="Show study activity insights" onClick={() => insightsFor('activity')}>Insights</TextButton>
      </div>
    </Section>
  );

  const mix = (
    <Section label="Session design" title="Learning mix" className="mp-mix">
      <p className="t-sub">{`How you spent your ${mixTotal} study session${mixTotal === 1 ? '' : 's'}.`}</p>
      <div className="mp-bars" role="group" aria-label="Session types">
        {sessionMix.map(item => <Bar key={item.id} title={item.label} readout={`${item.value} session${item.value === 1 ? '' : 's'} · ${mixTotal ? Math.round(item.value / mixTotal * 100) : 0}%`}
          share={mixTotal ? item.value / mixTotal : 0} note={MIX_NOTES[item.id]} />)}
      </div>
      {!mixTotal && <p className="t-meta">No sessions recorded yet.</p>}
    </Section>
  );

  const closerLook = uid && studentProfile ? (
    <Section label="Your subjects" title="A closer look at your learning." className="mp-closer">
      <p className="t-sub">Open a subject to see its record, topic by topic.</p>
      <TopicHistoryPanel uid={uid} profile={studentProfile} sessions={studySessions} minutes={subjectAllocation} onStudyTopic={onStudyTopic} onPracticeTopic={onPracticeTopic} />
    </Section>
  ) : null;

  const rhythmSection = (
    <Section label="Consistency" title="Study rhythm" className="mp-rhythm">
      <p className="t-sub">Thirteen weeks of recorded study activity.</p>
      <TextButton arrow="menu" aria-expanded={rhythmOpen} onClick={() => setRhythmOpen(open => !open)}>{rhythmOpen ? 'Hide the rhythm' : 'Show the rhythm'}</TextButton>
      {rhythmOpen && <StudyRhythmChart weeks={rhythm} />}
    </Section>
  );

  const readiness = (
    <Section ruled={false} label="Current picture · all dates" title="Topic readiness" big className="mp-readiness">
      <p className="mp-bigline"><span className="mp-big">{masterySummary.solid}</span><span className="t-sub">{`of your ${masterySummary.solid + masterySummary.shaky + masterySummary.notStarted} topics feel solid`}</span></p>
      <div role="group" aria-label="Readiness levels"><ReadinessStrip summary={masterySummary} /></div>
      <p className="t-meta">Your subject choice applies here. The dates do not.</p>
    </Section>
  );

  let part: React.ReactNode;
  if (tab === 'overview') {
    const focus = (
      <Section ruled={false} className="mp-focus" label={`${periodLabel} · Focus time`} title="Time you made for yourself." big
        aside={<Artwork src="/assets/star-crew/companions/thinker.png" size={mobileAppDesign ? 88 : 96} />}>
        <p className="mp-big mp-big--xl pr-focus-total" aria-label={formatMinutes(totalMinutes)}><Duration minutes={totalMinutes} /></p>
        <div role="group" aria-label="Focus time in the selected period"><ProgressGraph buckets={activityBuckets} metric="minutes" height={mobileAppDesign ? 168 : 230} /></div>
        <Figures items={figuresOverview} />
        {journeyPoints}
      </Section>
    );
    part = !hasLearningEvidence ? <>
      {focus}
      <Section label="Your learning record" title="Start with one focused session.">
        <p className="t-sub">This page becomes useful as soon as there is real work to reflect back to you.</p>
        <p className="t-body">Choose a subject, set a short timer and complete your first session. Your rhythm, confidence and study evidence will begin here.</p>
        {onStartStudy && <Button kind="main" arrow="forward" onClick={onStartStudy}>Start a study session</Button>}
      </Section>
      {programme}
    </> : <>
      {focus}
      <div className="mp-pair">
        <Section label="Your subjects" title="Everyone has a place." className="mp-subjects"
          aside={<TextButton tone="quiet" onClick={() => setSubjectOrder(order => order === 'time' ? 'name' : 'time')}>{subjectOrder === 'time' ? 'A–Z' : 'By time'}</TextButton>}>
          <p className="t-sub">{`${formatMinutes(subjectAllocation.reduce((sum, item) => sum + item.value, 0))} of focus, shared across your subjects.`}</p>
          {subjectAllocation.some(item => item.value > 0) ? <SubjectBars values={subjectAllocation} order={subjectOrder} /> : <p className="t-meta">Log a study session and its subject will appear here.</p>}
          {noTime.length > 0 && subjectAllocation.some(item => item.value > 0) && <p className="t-meta">{`No time yet this ${rangeWord}: ${noTime.join(', ')}.`}</p>}
        </Section>
        <Section label={`Practice · ${masterySummary.solid + masterySummary.shaky + masterySummary.notStarted} topics`} title="How your topics feel right now." className="mp-practice-glance">
          <ReadinessStrip summary={masterySummary} />
        </Section>
      </div>
      {today}
      {programme}
    </>;
  } else if (tab === 'study') {
    part = <>
      {studyGraph}
      <div className="mp-pair">{mix}{rhythmSection}</div>
      {closerLook}
      <MethodJournal methods={methodRecords} period={rangeBounds.label} />
    </>;
  } else if (tab === 'confidence') {
    part = <>
      <Section ruled={false} label={`${periodLabel} · Confidence`} title="A different story in every subject." big className="mp-confidence">
        <p className="mp-bigline"><span className="mp-big">{avgConfidence === null ? '–' : avgConfidence.toFixed(1)}</span>
          <span className="t-sub">{avgConfidence === null ? 'No check-ins in this period yet' : `out of 5, from ${confidencePoints.length} check-in${confidencePoints.length === 1 ? '' : 's'}`}</span></p>
        <p className="t-sub">How you felt after study, on a scale of 1 to 5.</p>
        {confidenceRows.length > 0 && <List label="Confidence by subject">
          {confidenceRows.map(item => <Row key={item.name} title={item.name} meta={`${confidenceWord(item.latest ?? 0)} · ${item.count} check-in${item.count === 1 ? '' : 's'}`}
            art={<SubjectAvatar subject={item.name} bare />} trailing={<span className="mp-scale-cell"><ConfidenceScale score={item.latest ?? 0} /><span className="t-readout">{`${item.latest} / 5`}</span></span>} />)}
        </List>}
        <p className="t-meta">{noCheckIns.length ? `No check-ins yet: ${noCheckIns.join(', ')}. ` : ''}Confidence is how study felt, not a prediction of your grade.</p>
      </Section>
      <ProgressConfidence observations={confidencePoints} bounds={rangeBounds} subjects={visibleSubjects} universe={subjects} onInsights={() => insightsFor('confidence')} />
    </>;
  } else if (tab === 'practice') {
    part = <>
      {readiness}
      <ProgressMocks mocks={mocks} period={rangeBounds.label} subjectLabel={subjectLabel} onInsights={() => insightsFor('mocks')} />
    </>;
  } else {
    part = gamificationState ? (
      <ProgressMilestones state={gamificationState} streak={streak} sessions={studySessions} strategyMastery={strategyMastery}
        weeklyChallenge={weeklyChallenge} pointsAvailable={pointsAvailable} pointsReload={pointsReload} curriculumLevel={curriculumLevel} />
    ) : (
      <Section ruled={false} label="Milestones" title="Progress is loading">
        <p className="t-sub">Your goals and achievements will appear here.</p>
        <LoadingShape rows={3} label="Loading your milestones" />
      </Section>
    );
  }

  return (
    <KobraScope className="nsu-progress"><div className={`mp-page ${mobileAppDesign ? 'mp-page--phone' : 'mp-page--desk'}`}>
      {mobileAppDesign ? <TopBar placeLabel="Your record" ruled={scrolled} /> : null}
      <div className="mp-col">
        {mobileAppDesign ? <h1 className="t-name mp-name">My Progress</h1> : <PageHeader onBack={onBack} eyebrow="Your record" title="My Progress" className="mp-head" />}
        <div className="mp-controls">
          <Menu label="Progress section" count numbered block value={tab} onChange={goToPart} className="mp-part-menu"
            options={TABS.map(item => ({ value: item.id, label: item.label }))} />
          {tab !== 'milestones' && <div className="mp-filters">
            <Menu label="Filter by subject" value={subject} onChange={value => setSelectedSubjects(value === 'all' ? [] : [value])} className="mp-subject-menu"
              options={[{ value: 'all', label: 'All subjects' }, ...subjects.map(name => ({ value: name, label: name }))]} />
            <SelectionWords label="Dashboard time range" value={range} onChange={value => setRange(value)} options={RANGE_OPTIONS.map(item => ({ value: item.id, label: item.label }))} />
          </div>}
        </div>
        <main className="mp-part" aria-label={TABS[partIndex].label}>
          {tab === 'overview' && pointsGoal.status !== 'hidden' && <div className="mp-goal"><ProgressPointsGoal standing={pointsGoal} onEditGrades={onEditGrades} onAddMockResult={onAddMockResult} /></div>}
          {part}
          {next ? <div className="mp-next-wrap">{next}</div> : null}
        </main>
      </div>
      {insightSheet}
    </div></KobraScope>
  );
};

export default DashboardView;
