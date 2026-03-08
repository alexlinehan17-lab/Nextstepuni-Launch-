/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * Kenney hex tiles: 1.0 wide (X), 1.155 tall (Z) — pointy-top orientation.
 *
 * Using offset coordinates (odd-r offset):
 * - Each row shifts right by 0.5 for odd r values
 * - Row spacing = 0.75 * height = 0.866
 * - Column spacing = width = 1.0
 *
 * But we'll use axial coordinates (q, r) for simplicity:
 * Pointy-top axial → world:
 *   x = size * (sqrt(3) * q + sqrt(3)/2 * r)
 *   z = size * (3/2 * r)
 * where size = distance from center to vertex
 *
 * For our tiles: flat-to-flat = 1.0, so size = 1/sqrt(3) ≈ 0.577
 * But actually, looking at the bounds, the hex is:
 *   X: [-0.5, 0.5] = 1.0 wide
 *   Z: [-0.577, 0.577] = 1.155 tall
 * This is a flat-top hex (wider in X than Z... no wait, Z > X means pointy-top)
 *
 * Actually Z (1.155) > X (1.0), so this is pointy-top:
 *   flat-to-flat width = 1.0 (in X)
 *   vertex-to-vertex height = 1.155 (in Z)
 *   inner radius = 0.5 (half the flat-to-flat)
 *   outer radius = 0.577 (half the vertex-to-vertex)
 *
 * Pointy-top spacing with axial coords:
 *   x = sqrt(3) * (q + r/2) * outer_radius = 1.0 * (q + r/2)
 *   z = 3/2 * r * outer_radius = 0.866 * r
 *
 * Wait that gives x = q + r/2 which doesn't match. Let me just compute:
 *   For pointy-top, center-to-center horizontal = sqrt(3) * outer_radius = 1.0
 *   Center-to-center vertical = 1.5 * outer_radius = 0.866
 */

export function hexToWorld(q: number, r: number): [number, number] {
  // Pointy-top hex, axial coordinates
  // horizontal distance between centers = 1.0 (= sqrt(3) * outerRadius)
  // vertical distance between rows = 0.866 (= 1.5 * outerRadius)
  const x = (q + r * 0.5) * 1.0;
  const z = r * 0.866;
  return [x, z];
}

/** Returns the 6 axial neighbors of hex (q, r) */
export function hexNeighbors(q: number, r: number): [number, number][] {
  return [
    [q + 1, r], [q - 1, r],
    [q, r + 1], [q, r - 1],
    [q + 1, r - 1], [q - 1, r + 1],
  ];
}

function hexKey(q: number, r: number): string {
  return `${q},${r}`;
}

/** Find the best unoccupied neighbor hex — prefers spots with the most existing neighbors (compact growth) */
export function findBestLandPlacement(occupied: Set<string>): { q: number; r: number } {
  if (occupied.size === 0) return { q: 0, r: 0 };

  let bestQ = 0, bestR = 1, bestScore = -1;

  for (const key of occupied) {
    const [oq, or] = key.split(',').map(Number);
    for (const [nq, nr] of hexNeighbors(oq, or)) {
      if (occupied.has(hexKey(nq, nr))) continue;
      // Score = how many existing neighbors this candidate has
      let score = 0;
      for (const [nnq, nnr] of hexNeighbors(nq, nr)) {
        if (occupied.has(hexKey(nnq, nnr))) score++;
      }
      if (score > bestScore) {
        bestScore = score;
        bestQ = nq;
        bestR = nr;
      }
    }
  }

  return { q: bestQ, r: bestR };
}

function isBuilding(model: string): boolean {
  return model.startsWith('building-') || model.startsWith('unit-') || model === 'bridge.glb';
}

/** Find a terrain tile (not already a building) to place a building on, preferring outer positions */
export function findBuildingPlacement(
  placements: { model: string; type: string; q: number; r: number }[]
): { q: number; r: number } | null {
  // Collect terrain-only hex positions (tiles that aren't buildings)
  const hexByPos = new Map<string, { q: number; r: number; hasBuilding: boolean }>();
  for (const p of placements) {
    if (p.type !== 'hex') continue;
    const key = hexKey(p.q, p.r);
    const existing = hexByPos.get(key);
    if (!existing) {
      hexByPos.set(key, { q: p.q, r: p.r, hasBuilding: isBuilding(p.model) });
    } else if (isBuilding(p.model)) {
      existing.hasBuilding = true;
    }
  }

  // Find terrain tiles without buildings, prefer outer positions (fewer neighbors)
  const occupied = new Set(hexByPos.keys());
  let best: { q: number; r: number } | null = null;
  let bestNeighborCount = Infinity;

  for (const entry of hexByPos.values()) {
    if (entry.hasBuilding) continue;
    let neighborCount = 0;
    for (const [nq, nr] of hexNeighbors(entry.q, entry.r)) {
      if (occupied.has(hexKey(nq, nr))) neighborCount++;
    }
    if (neighborCount < bestNeighborCount) {
      bestNeighborCount = neighborCount;
      best = { q: entry.q, r: entry.r };
    }
  }

  // If no free terrain tile, place on a new hex
  if (!best) {
    const newPos = findBestLandPlacement(occupied);
    return newPos;
  }

  return best;
}

/** Find a tile with <3 decorations, add small random offset */
export function findDecorationPlacement(
  placements: { type: string; q: number; r: number }[]
): { q: number; r: number; offsetX: number; offsetZ: number } | null {
  // Count decorations per hex position
  const decoCount = new Map<string, number>();
  const hexPositions: { q: number; r: number }[] = [];

  for (const p of placements) {
    const key = hexKey(p.q, p.r);
    if (p.type === 'hex') {
      if (!decoCount.has(key)) {
        hexPositions.push({ q: p.q, r: p.r });
        decoCount.set(key, 0);
      }
    } else if (p.type === 'decoration') {
      decoCount.set(key, (decoCount.get(key) ?? 0) + 1);
    }
  }

  // Find tile with fewest decorations (< 3)
  let best: { q: number; r: number } | null = null;
  let bestCount = Infinity;

  for (const pos of hexPositions) {
    const key = hexKey(pos.q, pos.r);
    const count = decoCount.get(key) ?? 0;
    if (count < 3 && count < bestCount) {
      bestCount = count;
      best = pos;
    }
  }

  if (!best) {
    // All tiles have 3+ decorations, pick any hex
    if (hexPositions.length > 0) best = hexPositions[0];
    else return null;
  }

  // Small random offset within the hex
  const offsetX = (Math.random() - 0.5) * 0.3;
  const offsetZ = (Math.random() - 0.5) * 0.3;

  return { q: best.q, r: best.r, offsetX, offsetZ };
}
