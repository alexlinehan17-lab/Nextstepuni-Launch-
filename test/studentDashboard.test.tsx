import React from 'react';
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';
import { act, fireEvent, render, screen, within } from '@testing-library/react';
import { ALL_COURSES } from '@/courseData';
import { createDemoStudentLoadedData } from '@/data/devStudent';
import type { StudySessionRecord } from '@/utils/strategyRegistry';
import type { UnifiedMockResult } from '@/types';
import { ATHLETE_RANKS, type GamificationState } from '@/gamificationConfig';

vi.mock('@/components/MountainLandscape', () => ({
  default: () => <div data-testid="five-climbs">Five Climbs panorama</div>,
}));

import DashboardView from '@/components/DashboardView';

const COURSES = [
  { id: 'mind-1', category: 'architecture-mindset', title: 'Mind', subtitle: '', description: '', sectionsCount: 2, tags: [] },
  { id: 'learn-1', category: 'learning-cheat-codes', title: 'Learn', subtitle: '', description: '', sectionsCount: 2, tags: [] },
] as never;

const GAMIFICATION_STATE: GamificationState = {
  totalPointsEarned: 650,
  currentStreak: 4,
  longestStreak: 9,
  modulesCompleted: 1,
  sectionsCompleted: 12,
  categoriesCompleted: 0,
  totalReflections: 3,
  totalTimetableSessions: 5,
  northStarCategory: null,
  currentRank: ATHLETE_RANKS[1],
  nextRank: ATHLETE_RANKS[2],
  rankProgress: 31,
  unlockedAchievements: [],
  achievementTimestamps: {},
  weeklyGoalProgress: { sections: 2, sessions: 1, reflections: 1 },
  weekStartDate: '2026-08-10',
  personalBests: {
    bestDayPoints: 120,
    bestDaySections: 4,
    bestDayReflections: 2,
    bestWeekPoints: 420,
    bestWeekSessions: 6,
  },
  journeyMilestones: 2,
  streakShields: 0,
};

function makeSession(id: string, subject: string, minutes: number, confidenceAfter: number): StudySessionRecord {
  const completedAt = new Date(2026, 7, 14, 12 + Number(id)).getTime();
  const labels = ['lost', 'shaky', 'okay', 'good', 'confident'] as const;
  return {
    id,
    date: '2026-08-14',
    subject,
    sessionType: 'practice',
    plannedMinutes: minutes,
    actualSeconds: minutes * 60,
    startedAt: completedAt - (minutes * 60_000),
    completedAt,
    pointsEarned: 20,
    hadReflection: true,
    confidenceAfter,
    confidenceLabel: labels[confidenceAfter - 1],
    reflectionMode: 'quick',
    strategiesShown: ['mastering-active-recall-protocol'],
  };
}

/** One subject at a time from the shared menu (the agreed board: "a short menu with a tick"). */
async function chooseSubject(subject: string) {
  fireEvent.click(screen.getByRole('button', { name: /Filter by subject/ }));
  fireEvent.click(await screen.findByRole('menuitemradio', { name: subject }));
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 30)); });
}
/** A sheet leaves in 320ms; wait until it has gone before using the page under it. */
async function closeSheet() {
  fireEvent.click(screen.getByRole('button', { name: 'Close' }));
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 400)); });
}
const total = (container: HTMLElement) => container.querySelector('.pr-focus-total')?.textContent;

describe('student analytics dashboard', () => {
  beforeEach(() => {
    // Only the date is fixed: the shared menu and sheet run their own timers.
    vi.useFakeTimers({ toFake: ['Date'] });
    vi.setSystemTime(new Date(2026, 7, 14, 12));
  });

  afterEach(() => vi.useRealTimers());

  test('renders recorded session, confidence and programme data without replacing Five Climbs', () => {
    const props = {
      userProgress: { 'mind-1': { unlockedSection: 2 } }, allCourses: COURSES, categoryTitles: {} as never,
      streak: { currentStreak: 4, longestStreak: 9, lastActiveDate: '2026-08-14' }, recommendation: null,
      onSelectModule: vi.fn(), onBack: vi.fn(), pointsEarned: 240,
      studySessions: [makeSession('1', 'Biology', 25, 4), makeSession('2', 'English', 10, 5)],
    };
    const { container, rerender } = render(<DashboardView {...props} />);

    expect(total(container)).toBe('35m');
    expect(screen.getByText('4.5')).toBeInTheDocument();
    expect(screen.getByTestId('five-climbs')).toBeInTheDocument();
    // The study activity graph and the methods are the Study part's (the agreed board).
    rerender(<DashboardView {...props} activeTab="study" />);
    expect(screen.getByRole('img', { name: 'Study activity chart showing sessions' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Active Recall' })).toBeInTheDocument();
  });

  test('switches the activity measure and subject filter without changing the source data', async () => {
    const props = {
      userProgress: {}, allCourses: COURSES, categoryTitles: {} as never,
      streak: { currentStreak: 0, longestStreak: 0, lastActiveDate: '' }, recommendation: null,
      onSelectModule: vi.fn(), onBack: vi.fn(), pointsEarned: 0,
      studySessions: [makeSession('1', 'Biology', 25, 4), makeSession('2', 'English', 10, 5)],
    };
    const { container, rerender } = render(<DashboardView {...props} activeTab="study" />);

    fireEvent.click(screen.getByRole('button', { name: 'Show minutes' }));
    expect(screen.getByRole('img', { name: 'Study activity chart showing minutes' })).toBeInTheDocument();

    rerender(<DashboardView {...props} activeTab="overview" />);
    await chooseSubject('Biology');
    expect(total(container)).toBe('25m');
    await chooseSubject('English');
    expect(total(container)).toBe('10m');
    expect(screen.getByRole('button', { name: /Filter by subject/ })).toHaveTextContent('English');
    await chooseSubject('All subjects');
    expect(total(container)).toBe('35m');
    expect(screen.getByRole('button', { name: /Filter by subject/ })).toHaveTextContent('All subjects');
  });

  test('reveals confidence insights for the visible filters and keeps the chart in view', async () => {
    const sessions = [2, 3, 4].map((score, index) => {
      const completed = new Date(2026, 7, 10 + (index * 2), 12).getTime();
      const record = makeSession(String(index + 1), 'Biology', 25, score);
      return {
        ...record,
        date: `2026-08-${String(10 + (index * 2)).padStart(2, '0')}`,
        startedAt: completed - (25 * 60_000),
        completedAt: completed,
      };
    });

    render(
      <DashboardView
        userProgress={{}}
        allCourses={COURSES}
        categoryTitles={{} as never}
        streak={{ currentStreak: 2, longestStreak: 2, lastActiveDate: '2026-08-14' }}
        recommendation={null}
        onSelectModule={vi.fn()}
        onBack={vi.fn()}
        pointsEarned={60}
        studySessions={sessions}
        activeTab="confidence"
      />,
    );

    const card = within(screen.getByRole('region', { name: 'Confidence over time' }));
    const toggle = card.getByRole('button', { name: 'Show confidence chart insights' });
    expect(toggle).toHaveTextContent('Insights');
    // The insights open in the shared sheet (a dialog from 640px).
    fireEvent.click(toggle);
    const sheet = within(await screen.findByRole('dialog', { name: 'What the pattern suggests' }));
    expect(sheet.getByRole('region', { name: 'Chart insights' })).toBeInTheDocument();
    expect(sheet.getByRole('heading', { name: 'Biology' })).toBeInTheDocument();
    expect(sheet.getByText('Trending upward')).toBeInTheDocument();
    await closeSheet();
    expect(card.getByRole('img', { name: 'Confidence over time by subject' })).toBeInTheDocument();
  });

  test('keeps full-mock totals comparable and scopes mock guidance to the subject filter', async () => {
    const mockResults: UnifiedMockResult[] = [
      {
        id: 'full-one', label: 'Full one', date: '2026-08-10', totalPoints: 350,
        timestamp: new Date(2026, 7, 10, 12).getTime(), resultKind: 'full',
        entries: [
          { subjectName: 'Biology', grade: 'H5', level: 'higher' },
          { subjectName: 'English', grade: 'H3', level: 'higher' },
        ],
      },
      {
        id: 'biology-paper', label: 'Biology paper', date: '2026-08-12', totalPoints: 66,
        timestamp: new Date(2026, 7, 12, 12).getTime(), resultKind: 'single',
        entries: [{ subjectName: 'Biology', grade: 'H4', level: 'higher' }],
      },
      {
        id: 'full-two', label: 'Full two', date: '2026-08-13', totalPoints: 390,
        timestamp: new Date(2026, 7, 13, 12).getTime(), resultKind: 'full',
        entries: [
          { subjectName: 'Biology', grade: 'H3', level: 'higher' },
          { subjectName: 'English', grade: 'H2', level: 'higher' },
        ],
      },
    ];

    render(
      <DashboardView
        userProgress={{}}
        allCourses={COURSES}
        categoryTitles={{} as never}
        streak={{ currentStreak: 0, longestStreak: 0, lastActiveDate: '' }}
        recommendation={null}
        onSelectModule={vi.fn()}
        onBack={vi.fn()}
        pointsEarned={0}
        mockResults={mockResults}
        activeTab="practice"
      />,
    );

    const mockCard = () => within(screen.getByRole('heading', { name: 'Mock trajectory' }).closest('section') as HTMLElement);
    // The record is first on the agreed board; the line is one tap away.
    expect(mockCard().getByText('Full one')).toBeInTheDocument();
    expect(mockCard().getByText('Full two')).toBeInTheDocument();
    expect(mockCard().queryByText('Biology paper')).not.toBeInTheDocument();
    fireEvent.click(mockCard().getByRole('button', { name: 'Show the chart' }));
    expect(mockCard().getByRole('img', { name: 'Mock exam total points trajectory' })).toBeInTheDocument();

    fireEvent.click(mockCard().getByRole('button', { name: 'Show mock trajectory insights' }));
    expect(await screen.findByRole('heading', { name: 'Total points' })).toBeInTheDocument();
    expect(screen.getByText(/2 full mock sittings/)).toBeInTheDocument();
    await closeSheet();

    await chooseSubject('Biology');
    fireEvent.click(mockCard().getByRole('button', { name: 'Show mock trajectory insights' }));
    expect(await screen.findByRole('heading', { name: 'Biology results' })).toBeInTheDocument();
    expect(screen.queryByRole('heading', { name: 'Subject movement' })).not.toBeInTheDocument();
    expect(screen.getByText(/3 results/)).toBeInTheDocument();
  });

  test('lights up every analytics section with the localhost demo history', () => {
    const demo = createDemoStudentLoadedData(new Date(2026, 7, 14, 12));
    const view = (tab: 'overview' | 'study' | 'confidence' | 'practice') => (
      <DashboardView
        userProgress={demo.userProgress}
        allCourses={ALL_COURSES}
        categoryTitles={{} as never}
        streak={{ currentStreak: 18, longestStreak: 42, lastActiveDate: '2026-08-14' }}
        recommendation={null}
        onSelectModule={vi.fn()}
        onBack={vi.fn()}
        pointsEarned={demo.rawProgressDoc.pointsData?.totalEarned ?? 0}
        studentProfile={demo.studentProfile}
        studySessions={demo.rawProgressDoc.studySessions}
        studyDebriefs={demo.rawProgressDoc.studyDebriefs}
        studyReflections={demo.rawProgressDoc.reflections}
        topicMastery={demo.rawProgressDoc.topicMasteryV2}
        mockResults={demo.rawProgressDoc.unifiedMockResults}
        timetableCompletions={demo.timetableCompletions}
        activeTab={tab}
      />
    );
    const { rerender } = render(view('overview'));
    expect(screen.getByRole('group', { name: 'Focus time in the selected period' })).toBeInTheDocument();
    expect(screen.getByRole('img', { name: /^Of \d+ topics:/ })).toBeInTheDocument();

    rerender(view('study'));
    expect(screen.getByRole('img', { name: 'Study activity chart showing sessions' })).toBeInTheDocument();
    expect(screen.getByRole('group', { name: 'Session types' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Choose a method/ })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Show the rhythm' }));
    expect(screen.getByRole('img', { name: /^Thirteen week study rhythm:/ })).toBeInTheDocument();

    rerender(view('confidence'));
    expect(screen.getByRole('img', { name: 'Confidence over time by subject' })).toBeInTheDocument();

    rerender(view('practice'));
    expect(screen.getByRole('group', { name: 'Readiness levels' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Show the chart' }));
    expect(screen.getByRole('img', { name: 'Mock exam total points trajectory' })).toBeInTheDocument();
  });

  test('keeps goals, rank, strategy milestones and achievements inside My Progress', () => {
    render(
      <DashboardView
        userProgress={{}}
        allCourses={COURSES}
        categoryTitles={{} as never}
        streak={{ currentStreak: 4, longestStreak: 9, lastActiveDate: '2026-08-14' }}
        recommendation={null}
        onSelectModule={vi.fn()}
        onBack={vi.fn()}
        pointsEarned={650}
        activeTab="milestones"
        gamificationState={GAMIFICATION_STATE}
        strategyMastery={{
          'mastering-active-recall-protocol': {
            tier: 'applied',
            sessionCount: 4,
            subjectsSeen: ['Biology', 'English'],
          },
        }}
      />,
    );

    expect(screen.getByRole('heading', { name: 'Beginner' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Three useful targets.' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'From knowing to doing.' })).toBeInTheDocument();
    expect(screen.getByText('Active Recall')).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Best efforts.' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Marks of progress.' })).toBeInTheDocument();
  });

  test('gives a new student one useful first action instead of empty analytics', () => {
    const onStartStudy = vi.fn();
    render(
      <DashboardView
        userProgress={{}}
        allCourses={COURSES}
        categoryTitles={{} as never}
        streak={{ currentStreak: 0, longestStreak: 0, lastActiveDate: '' }}
        recommendation={null}
        onSelectModule={vi.fn()}
        onBack={vi.fn()}
        onStartStudy={onStartStudy}
        pointsEarned={0}
      />,
    );

    expect(screen.getByRole('heading', { name: 'Start with one focused session.' })).toBeInTheDocument();
    expect(screen.queryByRole('img', { name: 'Study activity chart showing sessions' })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Start a study session/ }));
    expect(onStartStudy).toHaveBeenCalledTimes(1);
  });

  test('leaves the theme to the menu under the student\'s name: the agreed page has no toggle of its own', () => {
    render(
      <DashboardView
        userProgress={{}}
        allCourses={COURSES}
        categoryTitles={{} as never}
        streak={{ currentStreak: 0, longestStreak: 0, lastActiveDate: '' }}
        recommendation={null}
        onSelectModule={vi.fn()}
        onBack={vi.fn()}
        pointsEarned={0}
        darkMode
        onToggleTheme={vi.fn()}
      />,
    );

    expect(screen.queryByRole('switch', { name: /Switch to (light|dark) mode/ })).not.toBeInTheDocument();
  });
});
