import { describe, expect, it } from 'vitest';
import type { IslandState, ShopItem } from '../types';
import { getBuildCells } from '../components/journey/build/islandBuildModel';

const state: IslandState = {
  schemaVersion: 2,
  category: 'independence',
  placements: [
    { placementId: 'grass', itemId: 'grass', model: 'grass.glb', type: 'hex', layer: 'terrain', q: 0, r: 0 },
    { placementId: 'mountain', itemId: 'mountain', model: 'stone-mountain.glb', type: 'hex', layer: 'terrain', q: 1, r: 0 },
    { placementId: 'house', itemId: 'house', model: 'building-house.glb', type: 'hex', layer: 'structure', q: 0, r: 0 },
  ],
  totalSpent: 0,
  purchaseHistory: [],
  lastPurchaseTimestamp: '',
};

const house: ShopItem = { id: 'new-house', name: 'House', description: '', model: 'building-house.glb', category: 'building', type: 'hex', price: 100 };
const grass: ShopItem = { id: 'new-grass', name: 'Grass', description: '', model: 'grass.glb', category: 'terrain', type: 'hex', price: 25 };
const dock: ShopItem = { id: 'dock', name: 'Dock', description: '', model: 'building-dock.glb', category: 'building', type: 'hex', price: 100 };
const oak: ShopItem = { id: 'oak', name: 'Oak', description: '', model: 'tree_oak.glb', category: 'nature', type: 'decoration', price: 25 };

describe('Journey Build Mode placement model', () => {
  it('explains occupied and mountain cells while leaving neither valid', () => {
    const cells = getBuildCells(state, house);
    expect(cells.find(c => c.q === 0 && c.r === 0)).toMatchObject({ valid: false, reason: 'This tile already has a structure' });
    expect(cells.find(c => c.q === 1 && c.r === 0)).toMatchObject({ valid: false, reason: 'Mountains cannot be built on' });
  });

  it('offers only adjacent empty cells for terrain expansion', () => {
    const cells = getBuildCells(state, grass);
    expect(cells).toHaveLength(8);
    expect(cells.every(c => c.valid && c.frontier)).toBe(true);
    expect(cells.some(c => c.q === 0 && c.r === 0)).toBe(false);
    expect(cells.some(c => c.q === 4 && c.r === 4)).toBe(false);
  });

  it('only offers coastal cells for docks', () => {
    const enclosed: IslandState = {
      ...state,
      placements: [
        { placementId: 'centre', itemId: 'grass', model: 'grass.glb', type: 'hex', layer: 'terrain', q: 0, r: 0 },
        ...[[1, 0], [-1, 0], [0, 1], [0, -1], [1, -1], [-1, 1]].map(([q, r], index) => ({
          placementId: `ring-${index}`, itemId: 'grass', model: 'grass.glb', type: 'hex' as const,
          layer: 'terrain' as const, q, r,
        })),
      ],
    };
    expect(getBuildCells(enclosed, dock).find(cell => cell.q === 0 && cell.r === 0)).toMatchObject({
      valid: false,
      reason: 'This item must sit beside the water',
    });
    expect(getBuildCells(enclosed, dock).some(cell => cell.valid)).toBe(true);
  });

  it('keeps trees off stone and marks grass as recommended', () => {
    const cells = getBuildCells(state, oak);
    expect(cells.find(cell => cell.q === 1 && cell.r === 0)?.valid).toBe(false);
    expect(cells.find(cell => cell.q === 0 && cell.r === 0)).toMatchObject({ valid: true, recommended: true });
  });
});
