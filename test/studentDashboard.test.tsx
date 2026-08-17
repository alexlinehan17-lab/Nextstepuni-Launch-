import React from 'react';
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import { ALL_COURSES } from '@/courseData';
import { createDemoStudentLoadedData } from '@/data/devStudent';
import type { StudySessionRecord } from '@/utils/strategyRegistry';

vi.mock('@/components/MountainLandscape', () => ({
  default: () => <div data-testid="five-climbs">Five Climbs panorama</div>,
}));

import DashboardView from '@/components/DashboardView';

const COURSES = [
  { id: 'mind-1', category: 'architecture-mindset', title: 'Mind', subtitle: '', description: '', sectionsCount: 2, tags: [] },
  { id: 'learn-1', category: 'learning-cheat-codes', title: 'Learn', subtitle: '', description: '', sectionsCount: 2, tags: [] },
] as never;

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
});
