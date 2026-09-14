import { piece, type StudioPiece } from '../../journey/paper/studioModel';
import type { TileKind } from '../../journey/paper/catalogue';

export const PREVIEW_TILES: TileKind[] = ['meadow', 'woodland', 'water', 'treehouse', 'lighthouse', 'waterfall'];
export const INITIAL_ISLAND = [piece(0, 0, 'home'), piece(-1, 0, 'woodland'), piece(1, -1, 'water')];

/** This visitor's island has no creature reservations or account state. */
export function openEdges(placed: StudioPiece[]) {
  const occupied = new Set(placed.map(p => p.key));
  const open = new Map<string, StudioPiece>();
  for (const cell of placed) {
    for (const [dq, dr] of [[1, 0], [0, 1], [-1, 1], [-1, 0], [0, -1], [1, -1]]) {
      const q = cell.q + dq, r = cell.r + dr, key = `${q},${r}`;
      if (!occupied.has(key)) open.set(key, piece(q, r, 'meadow'));
    }
  }
  return [...open.values()].sort((a, b) => a.r - b.r || a.q - b.q);
}

export function placePreviewTile(placed: StudioPiece[], key: string, kind: TileKind) {
  const target = openEdges(placed).find(cell => cell.key === key);
  if (!target || !PREVIEW_TILES.includes(kind)) return placed;
  return [...placed, piece(target.q, target.r, kind)];
}

/** Keep every adjacent edge in view, including when someone builds far left. */
export function previewView(placed: StudioPiece[], aspect: number) {
  const cells = [...placed, ...openEdges(placed)];
  const left = Math.min(...cells.map(c => c.x)) - 115;
  const right = Math.max(...cells.map(c => c.x)) + 115;
  const top = Math.min(...cells.map(c => c.y)) - 175;
  const bottom = Math.max(...cells.map(c => c.y)) + 90;
  const width = Math.max(right - left, (bottom - top) * aspect);
  const height = width / aspect;
  return { x: (left + right - width) / 2, y: (top + bottom - height) / 2, width, height };
}
