/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { fireEvent, render, screen } from '@testing-library/react';
import { beforeEach, describe, expect, test, vi } from 'vitest';
import StudySessionView from '@/components/study/StudySessionView';
import { createDemoStudentSession } from '@/data/devStudent';

const mocks = vi.hoisted(() => ({
  endSession: vi.fn(),
  cancelSession: vi.fn(),
  startSession: vi.fn(),
  phase: 'active' as 'idle' | 'active',
  canRecordSession: true,
  mobile: false,
}));

vi.mock('@/hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => mocks.mobile }));

vi.mock('@/hooks/useStudySession', () => ({
  MIN_STUDY_SESSION_MINUTES: 5,
  useStudySession: () => ({
    phase: mocks.phase,
    subject: 'Mathematics',
    sessionType: 'revision',
    plannedMinutes: 25,
    elapsedSeconds: 60,
    totalDuration: 1500,
    currentPrompt: null,
    promptShownAt: 0,
    todaySessions: [],
    basePointsEarned: 0,
    canRecordSession: mocks.canRecordSession,
    pauseSession: vi.fn(),
    resumeSession: vi.fn(),
    startSession: mocks.startSession,
    endSession: mocks.endSession,
    cancelSession: mocks.cancelSession,
    completePrompt: vi.fn(),
    dismissPrompt: vi.fn(),
    getTrackedStrategies: () => [],
    todayTotalMinutes: 0,
  }),
}));

vi.mock('@/contexts/ProgressContext', () => ({
  useProgress: () => ({ rawProgressDoc: {}, updateDemoProgress: vi.fn() }),
}));

const renderActiveSession = () => render(
  <StudySessionView
    user={createDemoStudentSession()}
    studentProfile={null}
    userProgress={{}}
    allCourses={[]}
    pointsReload={vi.fn()}
    streak={{ currentStreak: 0, longestStreak: 0, lastActiveDate: '' }}
    onBack={vi.fn()}
  />,
);

describe.each([false, true])('study-session exit choices (mobile: %s)', mobile => {
  beforeEach(() => {
    mocks.mobile = mobile;
    mocks.endSession.mockReset();
    mocks.cancelSession.mockReset();
    mocks.startSession.mockReset();
    mocks.phase = 'active';
    mocks.canRecordSession = true;
  });

  test('ending early enters the completion and debrief flow', () => {
    renderActiveSession();

    fireEvent.click(screen.getByRole('button', { name: 'Leave study session' }));
    fireEvent.click(screen.getByRole('button', { name: 'End early and debrief' }));

    expect(mocks.endSession).toHaveBeenCalledTimes(1);
    expect(mocks.cancelSession).not.toHaveBeenCalled();
  });

  test('discarding remains a separate unsaved action', () => {
    renderActiveSession();

    fireEvent.click(screen.getByRole('button', { name: 'Leave study session' }));
    fireEvent.click(screen.getByRole('button', { name: 'Discard without saving' }));

    expect(mocks.cancelSession).toHaveBeenCalledTimes(1);
    expect(mocks.endSession).not.toHaveBeenCalled();
  });

  test('does not offer a recordable early end before five minutes', () => {
    mocks.canRecordSession = false;
    renderActiveSession();

    fireEvent.click(screen.getByRole('button', { name: 'Leave study session' }));

    expect(screen.getByText(/Study for at least 5 minutes/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'End early after 5 min' })).toBeDisabled();
    expect(screen.getByRole('button', { name: 'Discard without saving' })).toBeEnabled();
  });

  test('labels and enforces the five-minute custom duration floor', () => {
    mocks.phase = 'idle';
    renderActiveSession();

    const duration = screen.getByRole('spinbutton', { name: 'Custom study duration in minutes' });
    expect(duration).toHaveAttribute('min', '5');
    fireEvent.change(duration, { target: { value: '1' } });
    expect(duration).toHaveValue(1);
    expect(duration).toHaveAttribute('aria-invalid', 'true');
    expect(screen.getByText('Minimum 5 minutes')).toBeInTheDocument();
    fireEvent.change(duration, { target: { value: '5' } });
    expect(duration).toHaveValue(5);
    expect(duration).toHaveAttribute('aria-invalid', 'false');
  });
});
