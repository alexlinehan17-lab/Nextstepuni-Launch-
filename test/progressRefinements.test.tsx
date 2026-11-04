import React from 'react';
import { describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import DashboardInsights from '../components/dashboard/DashboardInsights';
import { ProgressBreakdown, ProgressSections } from '../components/dashboard/progress/ProgressRefinements';
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

  it('supports arrow-key navigation through the paper tabs', () => {
    const onChange = vi.fn();
    render(<ProgressSections value="study" options={[{ id: 'overview', label: 'Overview' }, { id: 'study', label: 'Study' }, { id: 'confidence', label: 'Confidence' }]} onChange={onChange} />);
    fireEvent.keyDown(screen.getByRole('tab', { name: 'Study' }), { key: 'ArrowRight' });
    expect(onChange).toHaveBeenLastCalledWith('confidence');
    expect(screen.getByRole('tab', { name: 'Confidence' })).toHaveFocus();
    fireEvent.keyDown(screen.getByRole('tab', { name: 'Confidence' }), { key: 'Home' });
    expect(onChange).toHaveBeenLastCalledWith('overview');
  });

  it('calculates ruled rows from recorded counts and handles an empty period', () => {
    const { rerender } = render(<ProgressBreakdown kind="mix" values={[{ id: 'practice', label: 'Practice', value: 3 }, { id: 'revision', label: 'Revision', value: 1 }]} />);
    const practice = screen.getByRole('button', { name: /Practice/ });
    expect(practice).toHaveTextContent('75%');
    fireEvent.click(practice);
    expect(screen.getByRole('status')).toHaveTextContent('Putting what you know to work.');
    rerender(<ProgressBreakdown kind="readiness" summary={{ total: 0, notStarted: 0, shaky: 0, solid: 0 }} />);
    expect(screen.getByRole('status')).toHaveTextContent('No topics recorded yet.');
    expect(screen.getAllByRole('button').every(button => button.textContent?.includes('0%'))).toBe(true);
  });

  it('keeps daily and weekly records distinct and preserves the achievement gallery', () => {
    render(<ProgressMilestones state={state} streak={{ currentStreak: 4, longestStreak: 9, lastActiveDate: '' }} sessions={[]} strategyMastery={{}} curriculumLevel="senior" />);
    const day = screen.getByRole('heading', { name: 'In a day' }).closest('section')!;
    const week = screen.getByRole('heading', { name: 'In a week' }).closest('section')!;
    expect(within(day).getByText('112')).toBeInTheDocument();
    expect(within(day).getByText('8')).toBeInTheDocument();
    expect(within(week).getByText('486')).toBeInTheDocument();
    expect(within(week).getByText('11')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Save term review' })).toBeDisabled();
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
