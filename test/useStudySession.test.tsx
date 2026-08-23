/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { act, renderHook } from '@testing-library/react';
import { beforeEach, describe, expect, test, vi } from 'vitest';
import { DEMO_STUDENT_UID } from '@/data/devStudent';
import { MIN_RECORDABLE_SESSION_SECONDS, useStudySession } from '@/hooks/useStudySession';

const mocks = vi.hoisted(() => ({
  studySessions: [],
  updateDemoProgress: vi.fn(),
}));

vi.mock('@/contexts/ProgressContext', () => ({
  useProgress: () => ({
    studySessions: mocks.studySessions,
    progressLoaded: true,
    updateDemoProgress: mocks.updateDemoProgress,
  }),
}));

describe('useStudySession', () => {
  beforeEach(() => {
    vi.useRealTimers();
    mocks.updateDemoProgress.mockReset();
  });

  test('cancels an unfinished session without recording it or awarding points', () => {
    const { result } = renderHook(() => useStudySession(DEMO_STUDENT_UID, {}, []));

    act(() => {
      result.current.startSession('Mathematics', 'revision', 25);
    });
    expect(result.current.phase).toBe('active');

    act(() => {
      result.current.cancelSession();
    });

    expect(result.current.phase).toBe('idle');
    expect(result.current.elapsedSeconds).toBe(0);
    expect(result.current.todaySessions).toEqual([]);
    expect(mocks.updateDemoProgress).not.toHaveBeenCalled();
  });

  test('cannot end or save an accidental session before five real minutes', async () => {
    vi.useFakeTimers();
    const { result } = renderHook(() => useStudySession(DEMO_STUDENT_UID, {}, []));

    act(() => {
      result.current.startSession('Mathematics', 'revision', 25);
      vi.advanceTimersByTime((MIN_RECORDABLE_SESSION_SECONDS - 1) * 1000);
    });

    expect(result.current.canRecordSession).toBe(false);
    act(() => {
      expect(result.current.endSession()).toBe(false);
    });
    expect(result.current.phase).toBe('active');

    let saved = true;
    await act(async () => {
      saved = await result.current.saveSession(10);
    });
    expect(saved).toBe(false);
    expect(result.current.todaySessions).toEqual([]);
    expect(mocks.updateDemoProgress).not.toHaveBeenCalled();
  });

  test('allows an early end once five real minutes have elapsed', () => {
    vi.useFakeTimers();
    const { result } = renderHook(() => useStudySession(DEMO_STUDENT_UID, {}, []));

    act(() => {
      result.current.startSession('Mathematics', 'revision', 25);
      vi.advanceTimersByTime(MIN_RECORDABLE_SESSION_SECONDS * 1000);
    });

    expect(result.current.canRecordSession).toBe(true);
    act(() => {
      expect(result.current.endSession()).toBe(true);
    });
    expect(result.current.phase).toBe('complete');
  });
});
