/**
 * Backwards-compatible foundations for Journey Build Mode.
 *
 * Version 1 island documents used `type: hex` for both terrain and buildings.
 * Version 2 keeps the existing placements array (so current renderers and peer
 * projections continue to work) while assigning every placement a stable ID
 * and an explicit terrain/structure/decoration layer.
 */
import type {
  IslandPlacement,
  IslandPlacementLayer,
  IslandState,
  PlacementRules,
  ShopItem,
} from '../types';

export const ISLAND_SCHEMA_VERSION = 3;

export function inferPlacementLayer(placement: Pick<IslandPlacement, 'model' | 'type'>): IslandPlacementLayer {
  if (placement.type === 'decoration') return 'decoration';
  if (
    placement.model.startsWith('building-') ||
    placement.model.startsWith('unit-') ||
    placement.model.startsWith('path-') ||
    placement.model === 'bridge.glb'
  ) return 'structure';
  return 'terrain';
}

function stablePlacementId(placement: IslandPlacement, index: number): string {
  const source = [
    placement.itemId,
    placement.model,
    placement.q,
    placement.r,
    placement.purchasedAt ?? '',
    index,
  ].join('|');

  // Deterministic FNV-1a-style hash. Determinism prevents a partially failed
  // migration from assigning different IDs on its next attempt.
  let hash = 2166136261;
  for (let i = 0; i < source.length; i += 1) {
    hash ^= source.charCodeAt(i);
    hash = Math.imul(hash, 16777619);
  }
  return `pl_${(hash >>> 0).toString(36)}_${index.toString(36)}`;
}

export function migrateIslandState(state: IslandState): { state: IslandState; changed: boolean } {
  let changed = state.schemaVersion !== ISLAND_SCHEMA_VERSION;
  if (!Array.isArray(state.inventory) || !Array.isArray(state.purchaseHistory) || !Array.isArray(state.claimedRewards)) {
    changed = true;
  }
  const seenIds = new Set<string>();

  const placements = (state.placements ?? []).map((placement, index) => {
    let placementId = placement.placementId;
    if (!placementId || seenIds.has(placementId)) {
      placementId = stablePlacementId(placement, index);
      changed = true;
    }
    seenIds.add(placementId);

    const legacyPathLayer = (state.schemaVersion ?? 1) < 3
      && placement.model.startsWith('path-')
      && placement.layer === 'terrain';
    const layer = legacyPathLayer ? 'structure' : (placement.layer ?? inferPlacementLayer(placement));
    if (!placement.layer || legacyPathLayer) changed = true;

    return { ...placement, placementId, layer };
  });

  if (!changed) return { state, changed: false };
  return {
    changed: true,
    state: {
      ...state,
      schemaVersion: ISLAND_SCHEMA_VERSION,
      placements,
      purchaseHistory: state.purchaseHistory ?? [],
      claimedRewards: state.claimedRewards ?? [],
      inventory: state.inventory ?? [],
    },
  };
}

export function createPlacementId(): string {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return `pl_${crypto.randomUUID()}`;
  }
  return `pl_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 10)}`;
}

/** Default rules provide a safe baseline until individual catalogue entries
 * receive more specialised adjacency and footprint rules in Phase 3. */
export function getPlacementRules(item: ShopItem): PlacementRules {
  if (item.placementRules) return item.placementRules;
  if (item.category === 'terrain') {
    return { layer: 'terrain', maximumPerTile: 1 };
  }
  if (item.category === 'path') {
    return {
      layer: 'structure',
      blockedTerrain: ['mountain', 'water'],
      preferredTerrain: ['grass', 'dirt', 'stone', 'path'],
      maximumPerTile: 1,
    };
  }
  if (item.category === 'building') {
    const coastal = item.model === 'building-dock.glb' || item.model === 'building-watermill.glb';
    const farm = item.model === 'building-farm.glb';
    const landmark = item.model === 'building-castle.glb' || item.model === 'building-wizard-tower.glb';
    return {
      layer: 'structure',
      blockedTerrain: ['mountain', 'water'],
      ...(farm ? { allowedTerrain: ['grass', 'dirt'] as const } : {}),
      ...(coastal ? { requiresCoast: true } : {}),
      ...(landmark ? { minimumOpenNeighbours: 2 } : {}),
      maximumPerTile: 1,
    };
  }
  if (item.category === 'nature') {
    const isTree = item.model.startsWith('tree_');
    return {
      layer: 'decoration',
      allowedTerrain: isTree ? ['grass', 'dirt', 'hill'] : ['grass', 'dirt', 'hill', 'sand'],
      preferredTerrain: ['grass', 'dirt'],
      maximumPerTile: isTree ? 1 : 3,
    };
  }
  if (item.category === 'vehicle') {
    return {
      layer: 'decoration',
      allowedTerrain: ['grass', 'dirt', 'stone', 'path'],
      preferredTerrain: ['dirt', 'path'],
      maximumPerTile: 1,
    };
  }
  if (item.model === 'fountain-round.glb' || item.model === 'windmill.glb' || item.model === 'tent-canvas.glb') {
    return {
      layer: 'decoration',
      blockedTerrain: ['mountain', 'water'],
      preferredTerrain: item.model === 'tent-canvas.glb' ? ['grass', 'dirt', 'sand'] : ['grass', 'stone'],
      maximumPerTile: 1,
    };
  }
  return {
    layer: 'decoration',
    blockedTerrain: ['mountain', 'water'],
    maximumPerTile: 3,
  };
}
