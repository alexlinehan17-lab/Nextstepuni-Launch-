/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { renderHook, waitFor } from '@testing-library/react';
import { describe, expect, test, vi } from 'vitest';
import { DEMO_STUDENT_UID } from '@/data/devStudent';
import { useStrategyMastery } from '@/hooks/useStrategyMastery';

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
});
