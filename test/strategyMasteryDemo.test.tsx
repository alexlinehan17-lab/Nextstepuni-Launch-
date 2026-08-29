/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { renderHook, waitFor } from '@testing-library/react';
import { describe, expect, test, vi } from 'vitest';
import { DEMO_STUDENT_UID } from '@/data/devStudent';
import { createStrategyMasteryRecord, useStrategyMastery } from '@/hooks/useStrategyMastery';

const EMPTY_PROGRESS = {};
const NO_COURSES: [] = [];

const mocks = vi.hoisted(() => ({
  setDoc: vi.fn(),
  updateDemoProgress: vi.fn(),
  studySessions: [],
}));

vi.mock('@/firebase', () => ({ db: {} }));

vi.mock('firebase/firestore', () => ({
  doc: vi.fn(),
  getDocs: vi.fn(),
  setDoc: mocks.setDoc,
}));

vi.mock('@/contexts/ProgressContext', () => ({
  useProgress: () => ({
    studySessions: mocks.studySessions,
    progressLoaded: true,
    updateDemoProgress: mocks.updateDemoProgress,
  }),
}));

describe('Demo strategy mastery', () => {
  test('derives mastery without writing it back into the shared progress snapshot', async () => {
    const { result } = renderHook(() => useStrategyMastery(DEMO_STUDENT_UID, EMPTY_PROGRESS, NO_COURSES));

    await waitFor(() => expect(result.current.isLoaded).toBe(true));
    expect(mocks.updateDemoProgress).not.toHaveBeenCalled();
    expect(mocks.setDoc).not.toHaveBeenCalled();
  });

  test('omits missing milestone dates before a mastery record reaches Firestore', () => {
    const record = createStrategyMasteryRecord('learned', 0, [], {
      learnedAt: undefined,
      appliedAt: undefined,
      habitualAt: undefined,
    });

    expect(record).toEqual({ tier: 'learned', sessionCount: 0, subjectsSeen: [] });
    expect(Object.values(record)).not.toContain(undefined);
  });

  test('retains milestone dates that have been earned', () => {
    expect(createStrategyMasteryRecord('applied', 3, ['English', 'Irish'], {
      learnedAt: '2026-08-01',
      appliedAt: '2026-08-08',
    })).toEqual({
      tier: 'applied',
      sessionCount: 3,
      subjectsSeen: ['English', 'Irish'],
      learnedAt: '2026-08-01',
      appliedAt: '2026-08-08',
    });
  });
});
