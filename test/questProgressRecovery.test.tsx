import { renderHook } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { useQuests } from '../hooks/useQuests';
import type { UserProgress } from '../types';
import type { StreakData } from '../hooks/useStreak';

vi.mock('../firebase', () => ({ db: {} }));
vi.mock('../contexts/ProgressContext', () => ({ useProgress: () => ({
  studySessions: [], studyDebriefs: [], topicMasteryV2: { topics: {} }, unifiedMockResults: [],
  questRewards: {}, progressLoaded: true, reloadProgress: vi.fn(), updateDemoProgress: vi.fn(),
}) }));
vi.mock('../questData', () => ({
  ONBOARDING_QUESTS: [{ id: 'start', title: 'Start a module', metric: 'module-start', target: 1, rewardPoints: 5 }],
  PERSONALIZED_TEMPLATES: [], hashSeed: () => 0,
}));

describe('quest progress recovery', () => {
  it.each([false, true])('ignores null saved module entries and preserves real progress (started: %s)', started => {
    const progress = { removed: null, module: { unlockedSection: started ? 1 : 0 } } as unknown as UserProgress;
    const { result } = renderHook(() => useQuests('student', progress, [], { currentStreak: 0 } as StreakData, null, undefined));
    expect(result.current.questState?.current).toBe(started ? 1 : 0);
    expect(result.current.questState?.isCompleted).toBe(started);
    expect(progress.removed).toBeNull();
  });
});
