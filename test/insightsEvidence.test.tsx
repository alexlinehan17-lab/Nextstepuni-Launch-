import React from 'react';
import { renderHook, render, screen, fireEvent, cleanup } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import type { StudySessionRecord } from '@/studySessionData';
import type { StreakData } from '@/hooks/useStreak';
const state = vi.hoisted(() => ({ sessions: [] as StudySessionRecord[] }));
vi.mock('@/contexts/ProgressContext', () => ({ useProgress: () => ({ studySessions: state.sessions, studyDebriefs: [], progressLoaded: true }) }));
import { useInsights } from '@/hooks/useInsights';
import InsightsView from '@/components/InsightsView';
const streak = { currentStreak: 2 } as StreakData;
afterEach(() => { cleanup(); state.sessions = []; });
describe('insights grounded in recorded evidence', () => {
  it('labels frequency as a timing pattern and streak growth as another active day', () => {
    state.sessions = Array.from({ length: 5 }, (_, index) => ({ date: '2026-09-07', startedAt: new Date(`2026-09-07T09:0${index}:00+01:00`).getTime(), actualSeconds: 1800, plannedMinutes: 30, subject: 'Mathematics', pointsEarned: 2, strategiesShown: [] } as unknown as StudySessionRecord));
    const { result } = renderHook(() => useInsights('demo', streak, {}));
    const timing = result.current.insights.find(item => item.id === 'best-time');
    expect(timing?.title).toBe('You usually study on weekday mornings');
    expect(timing?.description).toContain('5 of your 5 recorded sessions');
    expect(result.current.insights.find(item => item.id === 'streak-milestone')?.description).toContain('extra sessions on the same day do not add a day');
    expect(result.current.insights.find(item => item.id === 'completion-rate')?.description).toContain('150 of 150 planned minutes');
  });
  it('offers a working study action when there is not enough recorded data', () => {
    const onAction = vi.fn();
    render(<InsightsView uid="demo" streak={{currentStreak: 0} as StreakData} strategyMastery={{}} onBack={() => {}} onAction={onAction} />);
    expect(screen.getByText('Start with one session.')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Plan a study session' }));
    expect(onAction).toHaveBeenCalledWith('study');
  });
});
