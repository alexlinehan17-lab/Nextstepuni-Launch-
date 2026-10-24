/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Keep going (with a bonus for finishing the added time), open-ended sessions,
 * the minimised timer, and the island link after saving (feedback, Oct 2026).
 */

import React, { useState } from 'react';
import { act, fireEvent, render, renderHook, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';
import { useStudySession } from '@/hooks/useStudySession';
import { StudySessionProvider, useSharedStudySession } from '@/contexts/StudySessionContext';
import StudyMiniTimer from '@/components/study/StudyMiniTimer';
import StudySessionView from '@/components/study/StudySessionView';
import { readActiveStudySession, writeActiveStudySession } from '@/services/studySessionStore';
import { OPEN_ENDED_CAP_MINUTES, STUDY_SESSION_POINTS } from '@/studySessionData';
import { createDemoStudentSession } from '@/data/devStudent';
import type * as Firestore from 'firebase/firestore';

const mocks = vi.hoisted(() => ({
  studySessions: [] as unknown[],
  rawProgressDoc: {},
  addStudySession: vi.fn(),
  reloadProgress: vi.fn(),
  batchSet: vi.fn(),
  commit: vi.fn(),
}));

vi.mock('@/firebase', () => ({ db: {} }));
vi.mock('firebase/firestore', async original => ({
  ...await original<typeof Firestore>(),
  doc: (_db: unknown, ...path: string[]) => ({ path: path.join('/') }),
  getDoc: vi.fn(async () => ({ exists: () => false, data: () => ({}) })),
  increment: (n: number) => ({ increment: n }),
  writeBatch: () => ({ set: mocks.batchSet, commit: mocks.commit }),
}));
vi.mock('@/contexts/ProgressContext', () => ({
  useProgress: () => ({
    studySessions: mocks.studySessions,
    progressLoaded: true,
    updateDemoProgress: vi.fn(),
    addStudySession: mocks.addStudySession,
    reloadProgress: mocks.reloadProgress,
    rawProgressDoc: mocks.rawProgressDoc,
  }),
}));
vi.mock('@/hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => false }));
vi.mock('@/hooks/useStudyTransitionSound', () => ({ useStudyTransitionSound: () => ({ play: vi.fn(), muted: false }) }));

const UID = 'student-1';
const MINUTE = 60_000;
const NOW = new Date('2026-10-14T16:00:00Z').getTime();
const savedRecord = () => mocks.batchSet.mock.calls.find(([ref]) => String(ref.path).includes('/sessions/'))?.[1];
const savedPoints = () => mocks.batchSet.mock.calls.find(([ref]) => ref.path === `progress/${UID}`)?.[1];

beforeEach(() => {
  vi.useFakeTimers();
  vi.setSystemTime(NOW);
  window.sessionStorage.clear();
  for (const fn of [mocks.addStudySession, mocks.reloadProgress, mocks.batchSet, mocks.commit]) fn.mockReset();
  mocks.commit.mockResolvedValue(undefined);
});
afterEach(() => vi.useRealTimers());

describe('Keep going', () => {
  test('adds time to the same session and pays a bonus for finishing it', async () => {
    const { result } = renderHook(() => useStudySession(UID, {}, []));
    act(() => { result.current.startSession('Irish', 'practice', 25); });
    act(() => { vi.advanceTimersByTime(25 * MINUTE); });
    expect(result.current.phase).toBe('complete');
    expect(result.current.extensionBonus).toBe(0);

    act(() => { expect(result.current.extendSession(10)).toBe(true); });
    expect(result.current.phase).toBe('active');
    expect(result.current.totalDuration).toBe(35 * 60);
    expect(result.current.plannedSeconds).toBe(25 * 60);
    act(() => { vi.advanceTimersByTime(10 * MINUTE); });
    expect(result.current.phase).toBe('complete');
    expect(result.current.extensionBonus).toBe(STUDY_SESSION_POINTS.EXTENSION_COMPLETED);

    await act(async () => { await result.current.saveSession(0); });
    // 35 minutes: three full 10-minute blocks, plus the bonus for finishing the added time.
    expect(savedRecord()).toMatchObject({ actualSeconds: 35 * 60, plannedMinutes: 25, extendedMinutes: 10, extensionBonus: 10, pointsEarned: 40 });
    expect(savedPoints()).toEqual({ pointsData: { totalEarned: { increment: 40 } } });
  });

  test('ending the added time early keeps the minutes but forfeits the bonus', async () => {
    const { result } = renderHook(() => useStudySession(UID, {}, []));
    act(() => { result.current.startSession('Irish', 'practice', 25); });
    act(() => { vi.advanceTimersByTime(25 * MINUTE); });
    act(() => { result.current.extendSession(15); });
    act(() => { vi.advanceTimersByTime(6 * MINUTE); });
    act(() => { expect(result.current.endSession()).toBe(true); });
    expect(result.current.extensionBonus).toBe(0);

    await act(async () => { await result.current.saveSession(0); });
    expect(savedRecord()).toMatchObject({ actualSeconds: 31 * 60, extendedMinutes: 15, extensionBonus: 0, pointsEarned: 30 });
  });

  test('is only offered when the countdown ran out, in the offered sizes', () => {
    const { result } = renderHook(() => useStudySession(UID, {}, []));
    act(() => { result.current.startSession('Irish', 'practice', 25); });
    act(() => { vi.advanceTimersByTime(10 * MINUTE); });
    act(() => { result.current.endSession(); });
    act(() => { expect(result.current.extendSession(5)).toBe(false); });

    act(() => { result.current.cancelSession(); result.current.startSession('Irish', 'practice', 15); });
    act(() => { vi.advanceTimersByTime(15 * MINUTE); });
    act(() => { expect(result.current.extendSession(7)).toBe(false); });
    expect(result.current.phase).toBe('complete');
  });

  test('added time survives a reload', () => {
    const { result, unmount } = renderHook(() => useStudySession(UID, {}, []));
    act(() => { result.current.startSession('Irish', 'practice', 25); });
    act(() => { vi.advanceTimersByTime(25 * MINUTE); });
    act(() => { result.current.extendSession(10); });
    act(() => { vi.advanceTimersByTime(3 * MINUTE); });
    expect(readActiveStudySession(UID)).toMatchObject({ extendedMinutes: 10, phase: 'active' });
    unmount();

    vi.setSystemTime(Date.now() + 2 * MINUTE);
    const restored = renderHook(() => useStudySession(UID, {}, []));
    expect(restored.result.current.totalDuration).toBe(35 * 60);
    expect(restored.result.current.elapsedSeconds).toBe(30 * 60);
    expect(restored.result.current.phase).toBe('active');
  });
});

describe('Open-ended sessions', () => {
  test('count up until the student finishes, recording the time as the plan', async () => {
    const { result } = renderHook(() => useStudySession(UID, {}, []));
    act(() => { result.current.startSession('Biology', 'revision', 0, undefined, { openEnded: true }); });
    expect(result.current.openEnded).toBe(true);
    act(() => { vi.advanceTimersByTime(47 * MINUTE); });
    expect(result.current.phase).toBe('active');
    expect(result.current.elapsedSeconds).toBe(47 * 60);
    act(() => { expect(result.current.endSession()).toBe(true); });
    act(() => { expect(result.current.extendSession(5)).toBe(false); });

    await act(async () => { await result.current.saveSession(0); });
    expect(savedRecord()).toMatchObject({ openEnded: true, plannedMinutes: 47, actualSeconds: 47 * 60, pointsEarned: 40 });
    expect(savedRecord()).not.toHaveProperty('extensionBonus');
  });

  test('complete themselves at the cap', () => {
    const { result } = renderHook(() => useStudySession(UID, {}, []));
    act(() => { result.current.startSession('Biology', 'revision', 0, undefined, { openEnded: true }); });
    act(() => { vi.advanceTimersByTime((OPEN_ENDED_CAP_MINUTES + 5) * MINUTE); });
    expect(result.current.phase).toBe('complete');
    expect(result.current.elapsedSeconds).toBe(OPEN_ENDED_CAP_MINUTES * 60);
  });
});

describe('The minimised timer', () => {
  function Shell() {
    const [room, setRoom] = useState(true);
    const session = useSharedStudySession();
    return <>
      <button onClick={() => setRoom(value => !value)}>{room ? 'Leave room' : 'Open room'}</button>
      {room && session && <button onClick={() => session.startSession('Chemistry', 'practice', 25)}>Start</button>}
      {!room && <StudyMiniTimer onOpen={() => setRoom(true)} view="mark-bank" />}
    </>;
  }

  test('keeps counting across views, pauses, and opens the room again', () => {
    render(<StudySessionProvider uid={UID} userProgress={{}} allCourses={[]}><Shell /></StudySessionProvider>);
    fireEvent.click(screen.getByRole('button', { name: 'Start' }));
    fireEvent.click(screen.getByRole('button', { name: 'Leave room' }));
    act(() => { vi.advanceTimersByTime(4 * MINUTE); });
    const open = screen.getByRole('button', { name: /Open the study timer: Chemistry, 21:00 remaining/ });
    expect(screen.getByRole('complementary', { name: 'Study timer' })).toHaveAttribute('data-view', 'mark-bank');

    fireEvent.click(screen.getByRole('button', { name: 'Pause study session' }));
    act(() => { vi.advanceTimersByTime(5 * MINUTE); });
    expect(screen.getByRole('button', { name: /21:00 remaining, paused/ })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Resume study session' }));

    fireEvent.click(open);
    expect(screen.queryByRole('complementary', { name: 'Study timer' })).not.toBeInTheDocument();
  });

  test('says when time is up and can keep going from there', () => {
    render(<StudySessionProvider uid={UID} userProgress={{}} allCourses={[]}><Shell /></StudySessionProvider>);
    fireEvent.click(screen.getByRole('button', { name: 'Start' }));
    fireEvent.click(screen.getByRole('button', { name: 'Leave room' }));
    act(() => { vi.advanceTimersByTime(25 * MINUTE); });
    expect(screen.getByRole('button', { name: /Chemistry, Time’s up/ })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Log it' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Keep going for 5 more minutes' }));
    expect(screen.getByRole('button', { name: /05:00 remaining/ })).toBeInTheDocument();
  });

  test('a different student signing in on the tab starts clean', () => {
    function Probe() { const session = useSharedStudySession(); return <p>{session?.phase ?? 'none'}:{session?.subject ?? ''}</p>; }
    const view = render(<StudySessionProvider uid={UID} userProgress={{}} allCourses={[]}><Probe /></StudySessionProvider>);
    writeActiveStudySession(UID, { subject: 'Physics', sessionType: 'practice', plannedMinutes: 25, startedAt: NOW, phase: 'active', elapsedSeconds: 0, completedPrompts: [] });
    view.rerender(<StudySessionProvider uid="student-2" userProgress={{}} allCourses={[]}><Probe /></StudySessionProvider>);
    expect(screen.getByText('idle:')).toBeInTheDocument();
    view.rerender(<StudySessionProvider uid={UID} userProgress={{}} allCourses={[]}><Probe /></StudySessionProvider>);
    expect(screen.getByText('active:Physics')).toBeInTheDocument();
  });
});

describe('Time’s up, then the island', () => {
  test('keep going, finish, save, and spend the points on the island', async () => {
    const user = { ...createDemoStudentSession(), uid: UID };
    writeActiveStudySession(UID, { subject: 'Mathematics', sessionType: 'revision', plannedMinutes: 25, startedAt: NOW - 25 * MINUTE, phase: 'active', elapsedSeconds: 0, completedPrompts: [] });
    const onGoToIsland = vi.fn();
    render(<StudySessionView user={user} studentProfile={null} userProgress={{}} allCourses={[]} pointsReload={vi.fn()} streak={{ currentStreak: 0, longestStreak: 0, lastActiveDate: '' }} onBack={vi.fn()} dismissedGuides={{ 'points-explainer': 'seen' }} onGoToIsland={onGoToIsland} />);

    expect(screen.getByRole('heading', { name: 'Time’s up.' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Keep going for 5 more minutes' }));
    expect(screen.getByRole('timer')).toHaveTextContent('05:00');
    act(() => { vi.advanceTimersByTime(5 * MINUTE); });
    expect(screen.getByRole('heading', { name: 'You kept going.' })).toBeInTheDocument();
    expect(screen.getByText(`+${STUDY_SESSION_POINTS.EXTENSION_COMPLETED} JP for finishing your extra time`)).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: /Finish and log/ }));
    fireEvent.click(screen.getByRole('button', { name: 'Skip this step' }));
    await act(async () => { fireEvent.click(screen.getByRole('button', { name: 'Save without a debrief' })); });

    // 30 minutes (three 10-minute blocks) plus the finishing bonus.
    expect(screen.getByRole('heading', { name: '+40 JP' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Spend them on your island/ }));
    expect(onGoToIsland).toHaveBeenCalledTimes(1);
    fireEvent.click(screen.getByRole('button', { name: 'Back to the study room' }));
    expect(screen.getByRole('button', { name: 'Start Session' })).toBeInTheDocument();
  });
});
