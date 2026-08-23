import React from 'react';
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen, within } from '@testing-library/react';
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

describe('student analytics dashboard', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date(2026, 7, 14, 12));
  });

  afterEach(() => vi.useRealTimers());

  test('renders recorded session, confidence and programme data without replacing Five Climbs', () => {
    render(
      <DashboardView
        userProgress={{ 'mind-1': { unlockedSection: 2 } }}
        allCourses={COURSES}
        categoryTitles={{} as never}
        streak={{ currentStreak: 4, longestStreak: 9, lastActiveDate: '2026-08-14' }}
        recommendation={null}
        onSelectModule={vi.fn()}
        onBack={vi.fn()}
        pointsEarned={240}
        studySessions={[
          makeSession('1', 'Biology', 25, 4),
          makeSession('2', 'English', 10, 5),
        ]}
      />,
    );

    expect(screen.getByText('35m')).toBeInTheDocument();
    expect(screen.getByText('4.5')).toBeInTheDocument();
    expect(screen.getByTestId('five-climbs')).toBeInTheDocument();
    expect(screen.getByRole('img', { name: 'Study activity bar chart showing sessions' })).toBeInTheDocument();
    expect(screen.getByText('Active Recall')).toBeInTheDocument();
  });

  test('switches the activity measure and subject filter without changing the source data', () => {
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
        studySessions={[
          makeSession('1', 'Biology', 25, 4),
          makeSession('2', 'English', 10, 5),
        ]}
      />,
    );

    fireEvent.click(screen.getByRole('button', { name: 'Minutes' }));
    expect(screen.getByRole('img', { name: 'Study activity bar chart showing minutes' })).toBeInTheDocument();

    fireEvent.change(screen.getByRole('combobox', { name: 'Filter by subject' }), { target: { value: 'Biology' } });
    expect(screen.getByText('25m')).toBeInTheDocument();
  });

  test('reveals confidence insights for the visible filters and keeps the chart in view', () => {
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
      />,
    );

    expect(screen.getAllByText('Insights')).toHaveLength(3);
    const confidenceCard = screen.getByRole('heading', { name: 'Confidence over time' }).closest('article');
    expect(confidenceCard).not.toBeNull();
    const card = within(confidenceCard as HTMLElement);
    const toggle = card.getByRole('button', { name: 'Show confidence chart insights' });

    fireEvent.click(toggle);

    expect(toggle).toHaveAttribute('aria-expanded', 'true');
    expect(card.getByRole('region', { name: 'Chart insights' })).toBeInTheDocument();
    expect(card.getByRole('heading', { name: 'Biology' })).toBeInTheDocument();
    expect(card.getByText('Trending upward')).toBeInTheDocument();
    expect(card.getByRole('img', { name: 'Confidence over time by subject' })).toBeInTheDocument();
  });

  test('keeps full-mock totals comparable and scopes mock guidance to the subject filter', () => {
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
      />,
    );

    const mockCardElement = screen.getByRole('heading', { name: 'Mock trajectory' }).closest('article');
    expect(mockCardElement).not.toBeNull();
    const mockCard = within(mockCardElement as HTMLElement);
    expect(mockCard.getByRole('img', { name: 'Mock exam total points trajectory' }).querySelectorAll('[role="button"]')).toHaveLength(2);

    fireEvent.click(mockCard.getByRole('button', { name: 'Show mock trajectory insights' }));
    expect(mockCard.getByRole('heading', { name: 'Total points' })).toBeInTheDocument();
    expect(mockCard.getByText(/2 full mock sittings/)).toBeInTheDocument();

    fireEvent.change(screen.getByRole('combobox', { name: 'Filter by subject' }), { target: { value: 'Biology' } });
    expect(mockCard.getByRole('heading', { name: 'Biology results' })).toBeInTheDocument();
    expect(mockCard.queryByRole('heading', { name: 'Subject movement' })).not.toBeInTheDocument();
    expect(mockCard.getByText(/3 results/)).toBeInTheDocument();
  });

  test('lights up every analytics section with the localhost demo history', () => {
    const demo = createDemoStudentLoadedData(new Date(2026, 7, 14, 12));

    render(
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
      />,
    );

    expect(screen.getByRole('img', { name: 'Study activity bar chart showing sessions' })).toBeInTheDocument();
    expect(screen.getByRole('img', { name: 'Confidence over time by subject' })).toBeInTheDocument();
    expect(screen.getByRole('img', { name: 'Mock exam total points trajectory' })).toBeInTheDocument();
    expect(screen.getByRole('img', { name: 'uses ranked bar chart' })).toBeInTheDocument();

    fireEvent.click(screen.getByRole('tab', { name: 'Confidence' }));
    expect(screen.getByRole('img', { name: 'Topic readiness breakdown' })).toBeInTheDocument();

    fireEvent.click(screen.getByRole('tab', { name: 'Study' }));
    expect(screen.getByRole('img', { name: 'Thirteen week study rhythm calendar' })).toBeInTheDocument();
    expect(screen.getByRole('img', { name: 'Session type allocation' })).toBeInTheDocument();
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
    expect(screen.getByRole('heading', { name: 'Three useful targets' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Strategy milestones' })).toBeInTheDocument();
    expect(screen.getByText('Active Recall')).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Best efforts' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Achievements' })).toBeInTheDocument();
  });
});
