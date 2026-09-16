/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, test, vi } from 'vitest';
import StudySessionView from '@/components/study/StudySessionView';
import { createDemoStudentSession } from '@/data/devStudent';

const mocks = vi.hoisted(() => ({
  endSession: vi.fn(),
  cancelSession: vi.fn(),
  startSession: vi.fn(),
  phase: 'active' as 'idle' | 'active' | 'paused' | 'complete',
  resumeSession: vi.fn(),
  saveSession: vi.fn().mockResolvedValue(true),
  resetSession: vi.fn(),
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
    resumeSession: mocks.resumeSession,
    saveSession: mocks.saveSession,
    resetSession: mocks.resetSession,
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
    mocks.resumeSession.mockReset();
    mocks.saveSession.mockClear();
    mocks.resetSession.mockReset();
    localStorage.clear();
    mocks.phase = 'active';
    mocks.canRecordSession = true;
  });

  test('a paused session shows the break and resumes through the existing timer action', () => {
    mocks.phase = 'paused';
    renderActiveSession();
    expect(screen.getByRole('heading', { name: 'Even stars take a moment.' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Back to study' }));
    expect(mocks.resumeSession).toHaveBeenCalledOnce();
    expect(mocks.saveSession).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole('button', { name: 'Finish for now' }));
    expect(screen.getByRole('dialog', { name: 'End this study session?' })).toBeInTheDocument();
  });

  test('the receipt saves quick debrief metadata through the existing session handler', async () => {
    mocks.phase = 'complete';
    renderActiveSession();
    fireEvent.click(screen.getByRole('button', { name: 'Skip this step' }));
    expect(screen.getByRole('article', { name: 'Your study receipt' })).toHaveTextContent('Mathematics');
    fireEvent.click(screen.getByRole('button', { name: 'Good' }));
    fireEvent.click(screen.getByRole('button', { name: 'Keep this session' }));
    await waitFor(() => expect(mocks.saveSession).toHaveBeenCalledWith(10, [], {
      confidenceAfter: 4, confidenceLabel: 'good', reflectionMode: 'quick',
    }));
    expect(mocks.resetSession).toHaveBeenCalledOnce();
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

describe.each([false, true])('study setup selections (mobile: %s)', mobile => {
  beforeEach(() => {
    mocks.mobile = mobile;
    mocks.phase = 'idle';
    mocks.startSession.mockReset();
    mocks.resumeSession.mockReset();
    mocks.saveSession.mockClear();
    mocks.resetSession.mockReset();
    localStorage.clear();
  });

  test('prefills a timetable block and starts with the edited type and duration', () => {
    render(
      <StudySessionView
        user={createDemoStudentSession()}
        studentProfile={null}
        userProgress={{}}
        allCourses={[]}
        pointsReload={vi.fn()}
        streak={{ currentStreak: 0, longestStreak: 0, lastActiveDate: '' }}
        onBack={vi.fn()}
        dismissedGuides={{ 'points-explainer': 'seen' }}
        todayBlocks={[{ subject: 'Mathematics', sessionType: 'revision', durationMinutes: 45, dateKey: '2026-09-12', blockId: 'sample-block' }]}
      />,
    );
    const colourSwitch = screen.getByRole('switch', { name: 'I want my timer to have more colour!' });
    const subjectsHeading = screen.getByRole('heading', { name: 'What are you studying?' });
    expect(colourSwitch.compareDocumentPosition(subjectsHeading) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    fireEvent.click(colourSwitch);
    expect(colourSwitch).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByRole('button', { name: 'Start Session' })).toBeDisabled();
    fireEvent.click(screen.getByRole('button', { name: 'Set up Mathematics, 45 minutes' }));
    expect(screen.getByRole('button', { name: '45 min' })).toHaveAttribute('aria-pressed', 'true');
    fireEvent.click(screen.getByRole('button', { name: 'Practice Work through questions' }));
    fireEvent.change(screen.getByRole('spinbutton', { name: 'Custom study duration in minutes' }), { target: { value: '3' } });
    expect(screen.getByRole('button', { name: 'Start Session' })).toBeDisabled();
    fireEvent.change(screen.getByRole('spinbutton', { name: 'Custom study duration in minutes' }), { target: { value: '35' } });
    fireEvent.click(screen.getByRole('button', { name: 'Start Session' }));
    expect(mocks.startSession).toHaveBeenCalledWith('Mathematics', 'practice', 35);
  });
});
