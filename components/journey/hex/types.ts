/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

/** A hex tile placed in the island using a Kenney hex-kit GLB model */
export interface HexTile {
  q: number;
  r: number;
  /** GLB filename from hex kit (e.g. 'grass.glb', 'building-house.glb') */
  model: string;
  /** Rotation in 60° increments (0-5) for hex orientation */
  rotation?: number;
  /** Minimum milestone to appear (0 = always visible) */
  minMilestone: number;
  /** Optional label for tooltip */
  label?: string;
}

/** A standalone decoration model placed on top of a hex tile */
export interface HexDecoration {
  q: number;
  r: number;
  /** GLB filename from decorations folder (e.g. 'desk.glb') */
  model: string;
  /** Scale multiplier (default 1.0) */
  scale?: number;
  /** Y-axis rotation in radians */
  rotationY?: number;
  /** X/Z offset within the hex (default 0,0 = center) */
  offsetX?: number;
  offsetZ?: number;
  /** Minimum milestone to appear */
  minMilestone: number;
  label?: string;
}

/** Complete island layout for one North Star category */
export interface IslandLayout {
  tiles: HexTile[];
  decorations?: HexDecoration[];
  /** Water color override */
  waterColor?: string;
}
