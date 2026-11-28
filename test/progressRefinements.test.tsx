import React from 'react';
import { describe, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import DashboardInsights from '../components/dashboard/DashboardInsights';
import DashboardView from '../components/DashboardView';
import { ReadinessStrip } from '../components/dashboard/progress/ProgressParts';
import { toLocalDateKey } from '../components/dashboard/dashboardAnalytics';
import type { StudySessionRecord } from '../utils/strategyRegistry';
import { ProgressMilestones } from '../components/dashboard/progress/ProgressMilestones';
import { ATHLETE_RANKS, type GamificationState } from '../gamificationConfig';

const state: GamificationState = {
  totalPointsEarned: 650, currentStreak: 4, longestStreak: 9, modulesCompleted: 1,
  sectionsCompleted: 12, categoriesCompleted: 0, totalReflections: 3, totalTimetableSessions: 5,
  northStarCategory: null, currentRank: ATHLETE_RANKS[1], nextRank: ATHLETE_RANKS[2], rankProgress: 31,
  unlockedAchievements: [], achievementTimestamps: {}, weeklyGoalProgress: {}, weekStartDate: '',
  personalBests: { bestDayReflections: 2, bestDayPoints: 112, bestDaySections: 8, bestWeekPoints: 486, bestWeekSessions: 11 },
  journeyMilestones: 0, streakShields: 0,
};

describe('selected Progress designs', () => {
  it('reads one insight at a time and recovers when the subject filter changes', () => {
    const items = [
      { id: 'maths', title: 'Mathematics', trend: 'upward' as const, evidence: 'Recent ratings rose.', guidance: 'Try a recall task.' },
      { id: 'irish', title: 'Irish', trend: 'building' as const, evidence: 'One recorded check-in.', guidance: 'Add another debrief.' },
    ];
    const { rerender } = render(<DashboardInsights id="insights" context="This week" items={items} />);
    expect(screen.getByText('Recent ratings rose.')).toBeInTheDocument();
    expect(screen.queryByText('One recorded check-in.')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Irish/ }));
    expect(screen.getByText('One recorded check-in.')).toBeInTheDocument();
    expect(screen.queryByText('Recent ratings rose.')).not.toBeInTheDocument();
    rerender(<DashboardInsights id="insights" context="This week · Mathematics" items={items.slice(0, 1)} />);
    expect(screen.getByText('Recent ratings rose.')).toBeInTheDocument();
  });

  it('moves between the parts with the one menu on a laptop too: no row of tabs', () => {
    render(<DashboardView userProgress={{}} allCourses={[]} categoryTitles={{} as never} streak={{ currentStreak: 0, longestStreak: 0, lastActiveDate: '' }}
      recommendation={null} onSelectModule={vi.fn()} onBack={vi.fn()} pointsEarned={0} activeTab="study" />);
    expect(screen.queryByRole('tab', { name: 'Study' })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Progress section/ })).toHaveTextContent(/Study\s*·?\s*2 of 5/);
  });

  it('works out the learning mix from recorded counts, and an empty readiness strip says zero', () => {
    const today = toLocalDateKey(new Date());
    const session = (id: string, sessionType: StudySessionRecord['sessionType']): StudySessionRecord => ({
      id, subject: 'Irish', date: today, sessionType, plannedMinutes: 25, actualSeconds: 1500,
      startedAt: Date.now() - 1500000, completedAt: Date.now(), pointsEarned: 10, hadReflection: false,
    });
    render(<DashboardView userProgress={{}} allCourses={[]} categoryTitles={{} as never} streak={{ currentStreak: 1, longestStreak: 1, lastActiveDate: today }}
      recommendation={null} onSelectModule={vi.fn()} onBack={vi.fn()} pointsEarned={0} activeTab="study"
      studySessions={[session('1', 'practice'), session('2', 'practice'), session('3', 'practice'), session('4', 'revision')]} />);
    const mix = within(screen.getByRole('group', { name: 'Session types' }));
    expect(mix.getByText('Practice').closest('.mp-bar')).toHaveTextContent('3 sessions · 75%');
    expect(mix.getByText('Revision').closest('.mp-bar')).toHaveTextContent('1 session · 25%');
    expect(mix.getByText('Putting what you know to work.')).toBeInTheDocument();
    cleanup();
    render(<ReadinessStrip summary={{ total: 0, notStarted: 0, shaky: 0, solid: 0 }} />);
    expect(screen.getByRole('img', { name: 'Of 0 topics: 0 solid, 0 shaky, 0 not started' })).toBeInTheDocument();
  });

  it('keeps daily and weekly records distinct and preserves the achievement gallery', () => {
    render(<ProgressMilestones state={state} streak={{ currentStreak: 4, longestStreak: 9, lastActiveDate: '' }} sessions={[]} strategyMastery={{}} curriculumLevel="senior" />);
    const day = screen.getByRole('heading', { name: 'In a day' }).closest('section')!;
    const week = screen.getByRole('heading', { name: 'In a week' }).closest('section')!;
    expect(within(day).getByText('112')).toBeInTheDocument();
    expect(within(day).getByText('8')).toBeInTheDocument();
    expect(within(week).getByText('486')).toBeInTheDocument();
    expect(within(week).getByText('11')).toBeInTheDocument();
    // The shared Button has no silent disabled state: unavailable says why (aria-disabled).
    expect(screen.getByRole('button', { name: 'Save term review' })).toHaveAttribute('aria-disabled', 'true');
    fireEvent.click(screen.getByRole('button', { name: 'Open achievement gallery' }));
    expect(screen.getByRole('region', { name: 'Achievement collection' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Close gallery' }));
    expect(screen.queryByRole('region', { name: 'Achievement collection' })).not.toBeInTheDocument();
  });
  it('claims a completed weekly challenge and refreshes the points balance', async () => {
    const claimReward = vi.fn().mockResolvedValue(undefined);
    const pointsReload = vi.fn();
    render(<ProgressMilestones state={state} streak={{ currentStreak: 4, longestStreak: 9, lastActiveDate: '' }} sessions={[]} strategyMastery={{}} curriculumLevel="senior" pointsReload={pointsReload} weeklyChallenge={{
      challenge: { id: 'focus', title: 'Focus Master', description: 'Use Deep Focus in four sessions.', metric: 'strategy-sessions', target: 4, rewardPoints: 100, icon: 'Brain' },
      current: 4, isCompleted: true, isClaimed: false, isLoaded: true, claimReward, reload: vi.fn(),
    }} />);
    fireEvent.click(screen.getByText('Focus Master').closest('summary')!);
    fireEvent.click(screen.getByRole('button', { name: 'Claim 100 JP' }));
    expect(claimReward).toHaveBeenCalledTimes(1);
    await waitFor(() => expect(pointsReload).toHaveBeenCalledTimes(1));
  });

});
