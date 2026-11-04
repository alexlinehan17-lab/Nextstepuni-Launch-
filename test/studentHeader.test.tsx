import React from 'react';
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { beforeEach, describe, expect, test, vi } from 'vitest';
import TrainingPulse from '@/components/TrainingPulse';
import NotificationBell from '@/components/NotificationBell';
import { getNotifications, markAllRead, markNotificationRead, type AppNotification } from '@/components/gc/gcNotifications';
import { getRankForPoints, getNextRank, getRankProgress, DEFAULT_PERSONAL_BESTS, type GamificationState } from '@/gamificationConfig';
import { staffMessageText } from '@/data/staffEncouragement';

vi.mock('@/components/gc/gcNotifications', () => ({
  getNotifications: vi.fn(),
  markNotificationRead: vi.fn().mockResolvedValue(undefined),
  markAllRead: vi.fn().mockResolvedValue(undefined),
  STAFF_ORIGINATED: new Set(['gc-recommendation', 'gc-kudos', 'gc-broadcast']),
}));

function stateFor(totalPointsEarned: number): GamificationState {
  const currentRank = getRankForPoints(totalPointsEarned);
  const nextRank = getNextRank(currentRank);
  return {
    totalPointsEarned, currentRank, nextRank, rankProgress: getRankProgress(totalPointsEarned, currentRank, nextRank),
    currentStreak: 18, longestStreak: 18, modulesCompleted: 0, sectionsCompleted: 0, categoriesCompleted: 0,
    totalReflections: 0, totalTimetableSessions: 0, northStarCategory: null, unlockedAchievements: [], achievementTimestamps: {},
    weeklyGoalProgress: {}, weekStartDate: '', personalBests: DEFAULT_PERSONAL_BESTS, journeyMilestones: 0, streakShields: 0,
  };
}

describe('Star Crew rank control', () => {
  test('uses the chosen avatar and earned rank while separately displaying spendable points', () => {
    const onOpenProgress = vi.fn();
    const props = { gamificationState: stateFor(6200), onOpenProgress, streak: { currentStreak: 18, longestStreak: 18, lastActiveDate: '' }, pointsBalance: 5065, avatar: 'star-crew:maker' };
    const { container, rerender } = render(<TrainingPulse {...props} />);
    expect(container.querySelector('img')).toHaveAttribute('src', '/assets/star-crew/personal/07-maker.png');
    expect(screen.getByText('69% to Elite')).toBeInTheDocument();
    expect(screen.getByText('5,065')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Driven; 69% to Elite/ }));
    expect(onOpenProgress).toHaveBeenCalledOnce();
    rerender(<TrainingPulse {...props} avatar="star-crew:stargazer" pointsBalance={10} />);
    expect(container.querySelector('img')).toHaveAttribute('src', '/assets/star-crew/personal/08-stargazer.png');
    expect(screen.getByText('69% to Elite')).toBeInTheDocument();
    expect(screen.getByRole('button')).toHaveAccessibleName(/10 Journey Points/);
  });

  test('handles the highest rank without inventing another level', () => {
    render(<TrainingPulse gamificationState={stateFor(21000)} onOpenProgress={vi.fn()} streak={{ currentStreak: 0, longestStreak: 0, lastActiveDate: '' }} pointsBalance={0} avatar="star-crew:reader" />);
    expect(screen.getByRole('button')).toHaveAccessibleName(/Legend; Highest rank reached; 0 day streak; 0 Journey Points/);
    expect(screen.getByText('Highest rank reached')).toBeInTheDocument();
  });
});

const notes: AppNotification[] = [
  { id: 'note-1', type: 'gc-kudos', title: 'Untrusted staff title', body: 'Untrusted staff body', messageId: 'se1', timestamp: Date.now(), read: false },
  { id: 'note-2', type: 'study-insight', title: 'A good week of practice', body: 'Your practice sessions are adding up.', timestamp: Date.now(), read: false },
];

describe('Folded-note notifications', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(getNotifications).mockResolvedValue(notes.map(note => ({ ...note })));
  });

  test('opens full messages safely, persists read state, clears the badge and returns keyboard focus', async () => {
    const onUnreadCountChange = vi.fn();
    render(<NotificationBell uid="student-1" onUnreadCountChange={onUnreadCountChange} />);
    const toggle = screen.getByRole('button', { name: 'Open notifications' });
    await waitFor(() => expect(toggle).toHaveAttribute('title', '2 unread notifications'));
    fireEvent.click(toggle);
    const panel = screen.getByRole('region', { name: 'Notifications' });
    expect(within(panel).queryByText('Untrusted staff title')).not.toBeInTheDocument();
    expect(within(panel).queryByText('Untrusted staff body')).not.toBeInTheDocument();
    fireEvent.click(within(panel).getByRole('button', { name: /Words of encouragement/ }));
    expect(within(panel).getByRole('heading', { name: 'Words of encouragement' })).toBeInTheDocument();
    expect(within(panel).getByText(staffMessageText('se1'))).toBeInTheDocument();
    expect(markNotificationRead).toHaveBeenCalledWith('student-1', 'note-1');
    expect(onUnreadCountChange).toHaveBeenLastCalledWith(1);
    fireEvent.click(within(panel).getByRole('button', { name: '← All updates' }));
    fireEvent.click(within(panel).getByRole('button', { name: 'Mark all as read' }));
    expect(markAllRead).toHaveBeenCalledWith('student-1');
    expect(onUnreadCountChange).toHaveBeenLastCalledWith(0);
    expect(toggle).toHaveAttribute('title', 'Notifications');
    expect(within(toggle).queryByText(/^[0-9]/)).not.toBeInTheDocument();
    fireEvent.keyDown(document, { key: 'Escape' });
    expect(toggle).toHaveAttribute('aria-expanded', 'false');
    expect(toggle).toHaveFocus();
  });
});
