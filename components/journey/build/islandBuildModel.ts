import type {
  IslandPlacement,
  IslandState,
  IslandTerrainKind,
  ShopItem,
} from '../../../types';
import { getPlacementRules } from '../../../services/islandStateMigration';
import { hexNeighbors } from '../hex/hexGeometry';

export interface BuildCell {
  q: number;
  r: number;
  valid: boolean;
  reason?: string;
  terrain: IslandTerrainKind;
  frontier?: boolean;
  recommended?: boolean;
}

const key = (q: number, r: number) => `${q},${r}`;

export function terrainKindFromModel(model: string): IslandTerrainKind {
  if (model.includes('mountain')) return 'mountain';
  if (model.includes('hill')) return 'hill';
  if (model.startsWith('grass')) return 'grass';
  if (model.startsWith('dirt')) return 'dirt';
  if (model.startsWith('sand')) return 'sand';
  if (model.startsWith('stone')) return 'stone';
  if (model.startsWith('path-') || model === 'bridge.glb') return 'path';
  return 'unknown';
}

function layerOf(placement: IslandPlacement) {
  if (placement.layer) return placement.layer;
  if (placement.type === 'decoration') return 'decoration';
  if (placement.model.startsWith('building-') || placement.model.startsWith('unit-') || placement.model === 'bridge.glb') return 'structure';
  return 'terrain';
}

export function getBuildCells(state: IslandState, item: ShopItem): BuildCell[] {
  const rules = getPlacementRules(item);
  const terrainByCell = new Map<string, IslandPlacement>();
  const structures = new Set<string>();
  const decorationCounts = new Map<string, number>();

  for (const placement of state.placements) {
    const cellKey = key(placement.q, placement.r);
    const layer = layerOf(placement);
    if (layer === 'terrain') terrainByCell.set(cellKey, placement);
    if (layer === 'structure') structures.add(cellKey);
    if (layer === 'decoration') decorationCounts.set(cellKey, (decorationCounts.get(cellKey) ?? 0) + 1);
  }

  if (rules.layer === 'terrain') {
    const frontier = new Map<string, { q: number; r: number }>();
    for (const terrain of terrainByCell.values()) {
      for (const [q, r] of hexNeighbors(terrain.q, terrain.r)) {
        if (!terrainByCell.has(key(q, r))) frontier.set(key(q, r), { q, r });
      }
    }
    if (terrainByCell.size === 0) frontier.set('0,0', { q: 0, r: 0 });
    return [...frontier.values()].map(cell => {
      const adjacentTerrain = hexNeighbors(cell.q, cell.r)
        .map(([q, r]) => terrainByCell.get(key(q, r)))
        .filter((placement): placement is IslandPlacement => Boolean(placement))
        .map(placement => terrainKindFromModel(placement.model));
      const valid = !rules.requiresAdjacentTerrain
        || rules.requiresAdjacentTerrain.some(terrain => adjacentTerrain.includes(terrain));
      return {
        ...cell,
        valid,
        reason: valid ? undefined : 'This tile must connect to suitable terrain',
        terrain: 'water' as IslandTerrainKind,
        frontier: true,
        recommended: valid,
      };
    });
  }

  return [...terrainByCell.values()].map(terrainPlacement => {
    const cellKey = key(terrainPlacement.q, terrainPlacement.r);
    const terrain = terrainKindFromModel(terrainPlacement.model);
    const neighbours = hexNeighbors(terrainPlacement.q, terrainPlacement.r);
    const neighbourTerrain = neighbours
      .map(([q, r]) => terrainByCell.get(key(q, r)))
      .filter((placement): placement is IslandPlacement => Boolean(placement))
      .map(placement => terrainKindFromModel(placement.model));
    const openNeighbours = neighbours.length - neighbourTerrain.length;
    let reason: string | undefined;

    if (rules.blockedTerrain?.includes(terrain)) {
      reason = terrain === 'mountain' ? 'Mountains cannot be built on' : 'This terrain is unavailable';
    } else if (rules.allowedTerrain && !rules.allowedTerrain.includes(terrain)) {
      reason = 'This item needs different terrain';
    } else if (rules.layer === 'structure' && structures.has(cellKey)) {
      reason = 'This tile already has a structure';
    } else if (rules.layer === 'decoration' && (decorationCounts.get(cellKey) ?? 0) >= (rules.maximumPerTile ?? 3)) {
      reason = 'This tile is full';
    } else if (rules.requiresAdjacentTerrain && !rules.requiresAdjacentTerrain.some(value => neighbourTerrain.includes(value))) {
      reason = 'This item needs suitable terrain beside it';
    } else if (rules.requiresCoast && openNeighbours === 0) {
      reason = 'This item must sit beside the water';
    } else if (rules.minimumOpenNeighbours && openNeighbours < rules.minimumOpenNeighbours) {
      reason = `This landmark needs ${rules.minimumOpenNeighbours} open sides`;
    }

    return {
      q: terrainPlacement.q,
      r: terrainPlacement.r,
      terrain,
      valid: !reason,
      reason,
      recommended: !reason && (!rules.preferredTerrain || rules.preferredTerrain.includes(terrain)),
    };
  });
}

export function canPlaceAt(state: IslandState, item: ShopItem, q: number, r: number): boolean {
  return getBuildCells(state, item).some(cell => cell.q === q && cell.r === r && cell.valid);
}
