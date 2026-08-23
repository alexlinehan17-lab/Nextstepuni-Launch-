/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { act, renderHook, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, test, vi } from 'vitest';
import { useIslandShop } from '@/hooks/useIslandShop';
import { MILESTONE_REWARDS } from '@/islandShopData';
import { createDemoStudentNorthStar, DEMO_STUDENT_UID } from '@/data/devStudent';
import type { ProgressDocument } from '@/services/progressRepository';
import { getBuildCells } from '@/components/journey/build/islandBuildModel';

const mocks = vi.hoisted(() => ({
  progressDoc: {} as ProgressDocument,
  reloadProgress: vi.fn(),
  updateDemoProgress: vi.fn(),
  setDoc: vi.fn(),
  updateDoc: vi.fn(),
}));

vi.mock('@/contexts/ProgressContext', () => ({
  useProgress: () => ({
    reloadProgress: mocks.reloadProgress,
    rawProgressDoc: mocks.progressDoc,
    progressLoaded: true,
    updateDemoProgress: mocks.updateDemoProgress,
  }),
}));

vi.mock('@/hooks/useFreshProgress', () => ({
  useFreshProgress: () => ({ doc: null, loaded: true }),
}));

vi.mock('@/firebase', () => ({ db: {} }));

vi.mock('firebase/firestore', () => ({
  doc: vi.fn(() => ({})),
  setDoc: mocks.setDoc,
  updateDoc: mocks.updateDoc,
  increment: vi.fn((value: number) => value),
  arrayUnion: vi.fn((...values: unknown[]) => values),
}));

describe('useIslandShop Demo Account', () => {
  beforeEach(() => {
    mocks.progressDoc = { pointsData: { totalEarned: 6240, totalSpent: 1175 } };
    mocks.reloadProgress.mockReset();
    mocks.setDoc.mockReset();
    mocks.updateDoc.mockReset();
    mocks.updateDemoProgress.mockReset();
    mocks.updateDemoProgress.mockImplementation((updater: (current: ProgressDocument) => ProgressDocument) => {
      mocks.progressDoc = updater(mocks.progressDoc);
    });
  });

  test('keeps a claimed reward in shared in-memory progress without writing to Firestore', async () => {
    const northStar = createDemoStudentNorthStar();
    const reward = MILESTONE_REWARDS[northStar.category]?.[0];
    expect(reward).toBeDefined();
    if (!reward) return;

    const firstMount = renderHook(() => useIslandShop(DEMO_STUDENT_UID, northStar, 25));
    await waitFor(() => expect(firstMount.result.current.isLoading).toBe(false));

    let claimed = false;
    await act(async () => {
      claimed = await firstMount.result.current.claimReward(reward);
    });

    expect(claimed).toBe(true);
    expect(firstMount.result.current.milestoneRewards[0].status).toBe('claimed');
    expect(firstMount.result.current.islandState?.inventory).toEqual([
      expect.objectContaining({ itemId: reward.item.id, source: 'milestone' }),
    ]);
    expect(mocks.progressDoc.islandState?.claimedRewards).toContain(reward.id);
    expect(mocks.setDoc).not.toHaveBeenCalled();
    expect(mocks.updateDoc).not.toHaveBeenCalled();

    const claimedItem = firstMount.result.current.islandState?.inventory?.[0];
    const placementCell = firstMount.result.current.islandState
      ? getBuildCells(firstMount.result.current.islandState, reward.item).find(cell => cell.valid)
      : undefined;
    expect(claimedItem).toBeDefined();
    expect(placementCell).toBeDefined();
    if (!claimedItem || !placementCell) return;

    let placed = false;
    await act(async () => {
      placed = await firstMount.result.current.placeInventoryItem(
        claimedItem.inventoryId,
        placementCell.q,
        placementCell.r,
      );
    });
    expect(placed).toBe(true);
    expect(firstMount.result.current.islandState?.inventory).toHaveLength(0);
    expect(firstMount.result.current.islandState?.placements).toContainEqual(
      expect.objectContaining({ itemId: reward.item.id, q: placementCell.q, r: placementCell.r }),
    );
    expect(mocks.updateDoc).not.toHaveBeenCalled();

    firstMount.unmount();
    const secondMount = renderHook(() => useIslandShop(DEMO_STUDENT_UID, northStar, 25));
    await waitFor(() => expect(secondMount.result.current.isLoading).toBe(false));
    expect(secondMount.result.current.milestoneRewards[0].status).toBe('claimed');
    expect(secondMount.result.current.islandState?.inventory).toHaveLength(0);
    expect(secondMount.result.current.islandState?.placements).toContainEqual(
      expect.objectContaining({ itemId: reward.item.id, q: placementCell.q, r: placementCell.r }),
    );
  });
});
