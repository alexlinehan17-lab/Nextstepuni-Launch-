/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "my study time keeps getting deleted after i log it" (workshop feedback,
 * 12 Oct 2026). iPad Safari reloads a backgrounded tab; a running session and
 * an unacknowledged save both lived only in memory.
 */

import { act, renderHook } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';
import { useStudySession } from '@/hooks/useStudySession';
import {
  flushPendingStudySessions,
  readActiveStudySession,
  readPendingStudySessions,
  withPendingStudySessions,
  writeActiveStudySession,
} from '@/services/studySessionStore';
import type { StudySessionRecord } from '@/studySessionData';

const mocks = vi.hoisted(() => ({
  studySessions: [] as unknown[],
  addStudySession: vi.fn(),
  reloadProgress: vi.fn(),
  batchSet: vi.fn(),
  commit: vi.fn(),
  getDoc: vi.fn(),
}));

vi.mock('@/firebase', () => ({ db: {} }));
vi.mock('firebase/firestore', () => ({
  doc: (_db: unknown, ...path: string[]) => ({ path: path.join('/') }),
  getDoc: mocks.getDoc,
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
  }),
}));

const UID = 'student-1';
const MINUTE = 60_000;
const NOW = new Date('2026-10-12T18:00:00Z').getTime();

const record = (id: string): StudySessionRecord => ({
  id, date: '2026-10-12', subject: 'Mathematics', sessionType: 'practice',
  plannedMinutes: 25, actualSeconds: 1500, startedAt: NOW - 25 * MINUTE,
  completedAt: NOW, pointsEarned: 20, hadReflection: false,
} as StudySessionRecord);

describe('study time survives the page reloading', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    vi.setSystemTime(NOW);
    window.sessionStorage.clear();
    mocks.studySessions = [];
    for (const fn of [mocks.addStudySession, mocks.reloadProgress, mocks.batchSet, mocks.commit, mocks.getDoc]) fn.mockReset();
    mocks.commit.mockResolvedValue(undefined);
  });
  afterEach(() => vi.useRealTimers());

  test('a running session is restored after a reload, counting the time away', () => {
    writeActiveStudySession(UID, {
      subject: 'Biology', sessionType: 'revision', plannedMinutes: 45,
      startedAt: NOW - 20 * MINUTE, phase: 'active', elapsedSeconds: 60, completedPrompts: ['active-recall'],
    });

    const { result } = renderHook(() => useStudySession(UID, {}, []));

    expect(result.current.getTrackedStrategies()).toEqual(['active-recall']);
    expect(result.current.phase).toBe('active');
    expect(result.current.subject).toBe('Biology');
    expect(result.current.elapsedSeconds).toBe(20 * 60);
    act(() => { vi.advanceTimersByTime(30_000); });
    expect(result.current.elapsedSeconds).toBe(20 * 60 + 30);
  });

  test('a session whose time ran out while away comes back finished, ready to log', () => {
    writeActiveStudySession(UID, {
      subject: 'Irish', sessionType: 'practice', plannedMinutes: 25,
      startedAt: NOW - 115 * MINUTE, phase: 'active', elapsedSeconds: 0, completedPrompts: [],
    });

    const { result } = renderHook(() => useStudySession(UID, {}, []));

    expect(result.current.phase).toBe('complete');
    expect(result.current.elapsedSeconds).toBe(25 * 60);
  });

  test('start, pause and cancel keep the stored session in step', () => {
    const { result } = renderHook(() => useStudySession(UID, {}, []));

    act(() => { result.current.startSession('English', 'new-learning', 30); });
    expect(readActiveStudySession(UID)).toMatchObject({ phase: 'active', subject: 'English', startedAt: NOW });

    act(() => { vi.advanceTimersByTime(7 * MINUTE); });
    act(() => { result.current.pauseSession(); });
    expect(readActiveStudySession(UID)).toMatchObject({ phase: 'paused', elapsedSeconds: 7 * 60 });

    act(() => { result.current.cancelSession(); });
    expect(readActiveStudySession(UID)).toBeNull();
  });

  test('a logged session shows at once and stays queued until Firestore confirms it', async () => {
    let confirm: () => void = () => {};
    mocks.commit.mockReturnValue(new Promise<void>(resolve => { confirm = resolve; }));
    const { result } = renderHook(() => useStudySession(UID, {}, []));
    act(() => { result.current.startSession('Mathematics', 'practice', 25); });
    act(() => { vi.advanceTimersByTime(25 * MINUTE); });
    expect(result.current.phase).toBe('complete');

    await act(async () => { await result.current.saveSession(5); });

    expect(mocks.addStudySession).toHaveBeenCalledWith(expect.objectContaining({ subject: 'Mathematics', actualSeconds: 1500 }));
    expect(readActiveStudySession(UID)).toBeNull();
    expect(readPendingStudySessions(UID)).toHaveLength(1);
    // Session and points are one batch, so a retry can never pay out twice.
    expect(mocks.batchSet).toHaveBeenCalledWith(expect.objectContaining({ path: expect.stringMatching(/^progress\/student-1\/sessions\/ss_/) }), expect.objectContaining({ actualSeconds: 1500 }));
    expect(mocks.batchSet).toHaveBeenCalledWith({ path: 'progress/student-1' }, { pointsData: { totalEarned: { increment: 25 } } }, { merge: true });

    await act(async () => { confirm(); await Promise.resolve(); });
    expect(readPendingStudySessions(UID)).toEqual([]);
    expect(mocks.reloadProgress).toHaveBeenCalled();
  });

  test('a failed save stays queued and still shows in the student\'s sessions', async () => {
    mocks.commit.mockRejectedValue(new Error('unavailable'));
    const { result } = renderHook(() => useStudySession(UID, {}, []));
    act(() => { result.current.startSession('Physics', 'revision', 15); });
    act(() => { vi.advanceTimersByTime(15 * MINUTE); });

    await act(async () => { await result.current.saveSession(0); await Promise.resolve(); });

    const queued = readPendingStudySessions(UID);
    expect(queued).toHaveLength(1);
    expect(withPendingStudySessions(UID, []).map(r => r.subject)).toEqual(['Physics']);
    expect(withPendingStudySessions(UID, [queued[0].record])).toHaveLength(1);
  });

  test('the retry on the next load writes only what never arrived', async () => {
    window.sessionStorage.setItem(`nextstepuni:study-outbox:v1:${UID}`, JSON.stringify([
      { record: record('ss_arrived'), points: 20 },
      { record: record('ss_lost'), points: 20 },
    ]));
    mocks.getDoc.mockImplementation(async (ref: { path: string }) => ({ exists: () => ref.path.endsWith('ss_arrived') }));

    expect(await flushPendingStudySessions(UID)).toBe(1);

    expect(mocks.commit).toHaveBeenCalledTimes(1);
    expect(mocks.batchSet).toHaveBeenCalledWith({ path: 'progress/student-1/sessions/ss_lost' }, expect.objectContaining({ id: 'ss_lost' }));
    expect(readPendingStudySessions(UID)).toEqual([]);
  });

  test('today\'s sessions use the Irish calendar day, not UTC', () => {
    vi.setSystemTime(new Date('2026-10-13T23:30:00Z')); // 00:30 on 14 Oct in Dublin
    mocks.studySessions = [{ ...record('ss_midnight'), date: '2026-10-14' }];

    const { result } = renderHook(() => useStudySession(UID, {}, []));

    expect(result.current.todaySessions.map(s => s.id)).toEqual(['ss_midnight']);
  });
});
