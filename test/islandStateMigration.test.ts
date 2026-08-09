import { describe, expect, it } from 'vitest';
import type { IslandState } from '../types';
import {
  ISLAND_SCHEMA_VERSION,
  getPlacementRules,
  inferPlacementLayer,
  migrateIslandState,
} from '../services/islandStateMigration';

const legacyState: IslandState = {
  category: 'independence',
  placements: [
    { itemId: 'starter', model: 'grass.glb', type: 'hex', q: 0, r: 0 },
    { itemId: 'house', model: 'building-house.glb', type: 'hex', q: 0, r: 0 },
    { itemId: 'tree', model: 'tree_oak.glb', type: 'decoration', q: 1, r: 0 },
  ],
  totalSpent: 100,
  purchaseHistory: ['house'],
  lastPurchaseTimestamp: '2026-08-01T00:00:00.000Z',
};

describe('Journey island schema migration', () => {
  it('preserves placements while assigning stable IDs and layers', () => {
    const migrated = migrateIslandState(legacyState);
    expect(migrated.changed).toBe(true);
    expect(migrated.state.schemaVersion).toBe(ISLAND_SCHEMA_VERSION);
    expect(migrated.state.placements).toHaveLength(3);
    expect(migrated.state.placements.map(p => p.layer)).toEqual(['terrain', 'structure', 'decoration']);
    expect(new Set(migrated.state.placements.map(p => p.placementId)).size).toBe(3);
    expect(migrated.state.totalSpent).toBe(100);
    expect(migrated.state.purchaseHistory).toEqual(['house']);
  });

  it('is deterministic and idempotent', () => {
    const first = migrateIslandState(legacyState).state;
    const second = migrateIslandState(first);
    expect(second.changed).toBe(false);
    expect(second.state).toEqual(first);
  });

  it('repairs duplicate placement IDs without discarding either object', () => {
    const duplicated: IslandState = {
      ...legacyState,
      schemaVersion: ISLAND_SCHEMA_VERSION,
      placements: legacyState.placements.slice(0, 2).map(p => ({ ...p, placementId: 'same' })),
    };
    const migrated = migrateIslandState(duplicated);
    expect(migrated.state.placements).toHaveLength(2);
    expect(new Set(migrated.state.placements.map(p => p.placementId)).size).toBe(2);
  });

  it('blocks ordinary buildings and decorations from mountains and water by default', () => {
    const building = getPlacementRules({
      id: 'house', name: 'House', description: '', model: 'building-house.glb',
      category: 'building', type: 'hex', price: 100,
    });
    expect(building.layer).toBe('structure');
    expect(building.blockedTerrain).toEqual(['mountain', 'water']);
  });

  it('recognises legacy layers without relying on catalogue availability', () => {
    expect(inferPlacementLayer({ model: 'grass.glb', type: 'hex' })).toBe('terrain');
    expect(inferPlacementLayer({ model: 'building-castle.glb', type: 'hex' })).toBe('structure');
    expect(inferPlacementLayer({ model: 'sign.glb', type: 'decoration' })).toBe('decoration');
    expect(inferPlacementLayer({ model: 'path-corner.glb', type: 'hex' })).toBe('structure');
  });

  it('upgrades version two paths to a movable surface layer', () => {
    const versionTwo: IslandState = {
      ...legacyState,
      schemaVersion: 2,
      placements: [{
        placementId: 'old-path', itemId: 'path', model: 'path-straight.glb', type: 'hex',
        layer: 'terrain', q: 0, r: 0,
      }],
      inventory: [],
      claimedRewards: [],
    };
    const migrated = migrateIslandState(versionTwo);
    expect(migrated.changed).toBe(true);
    expect(migrated.state.placements[0].layer).toBe('structure');
  });
});
