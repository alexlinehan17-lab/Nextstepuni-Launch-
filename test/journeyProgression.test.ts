import { describe, expect, it } from 'vitest';
import { getJourneyProgress } from '../journeyProgression';

describe('Journey progression', () => {
  it('gives new students a short, concrete foundation path', () => {
    const progress = getJourneyProgress({ completedModules: 0, nonStarterPlacements: 0, claimedRewards: 0, inventoryItems: 0 });
    expect(progress.stage.name).toBe('Trailhead');
    expect(progress.foundationCompletedCount).toBe(1);
    expect(progress.modulesToNext).toBe(2);
  });

  it('advances stages without losing first-week progress', () => {
    const progress = getJourneyProgress({ completedModules: 7, nonStarterPlacements: 3, claimedRewards: 2, inventoryItems: 1 });
    expect(progress.stage.name).toBe('Settler');
    expect(progress.nextStage?.name).toBe('Pathfinder');
    expect(progress.foundationComplete).toBe(true);
    expect(progress.unplacedCount).toBe(1);
  });

  it('caps the final stage at complete', () => {
    const progress = getJourneyProgress({ completedModules: 53, nonStarterPlacements: 10, claimedRewards: 10, inventoryItems: 0 });
    expect(progress.stage.name).toBe('Landmark');
    expect(progress.nextStage).toBeNull();
    expect(progress.progress).toBe(1);
  });
});
