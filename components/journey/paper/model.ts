import { catalogue, tileById, type TileKind } from "./catalogue";
import { piece, type StudioPiece } from "./studioModel";
import {
  PAPER_DISCOVERIES,
  PAPER_LANDMARKS,
} from "../../../functions/src/paperIslandModel";
export const discoveries = PAPER_DISCOVERIES;
export type IslandState = {
  placed: StudioPiece[];
  balance: number;
  credits: number;
  history: unknown[];
  log: { kind: TileKind; cost: number }[];
};
const neighbours = [
  [1, 0],
  [0, 1],
  [-1, 1],
  [-1, 0],
  [0, -1],
  [1, -1],
];
export function frontier(placed: StudioPiece[]) {
  const occupied = new Set([
      ...placed.map((c) => c.key),
      ...discoveries.map((d) => `${d.q},${d.r}`),
      ...PAPER_LANDMARKS.map((d) => `${d.q},${d.r}`),
    ]),
    open = new Map<string, StudioPiece>();
  for (const cell of placed)
    for (const [dq, dr] of neighbours) {
      const q = cell.q + dq,
        r = cell.r + dr,
        key = `${q},${r}`;
      if (!occupied.has(key) && !open.has(key))
        open.set(key, piece(q, r, "meadow"));
    }
  return [...open.values()].sort((a, b) => a.r - b.r || a.q - b.q);
}
export const distance = (
  a: { q: number; r: number },
  b: { q: number; r: number },
) =>
  Math.max(
    Math.abs(a.q - b.q),
    Math.abs(a.r - b.r),
    Math.abs(a.q + a.r - b.q - b.r),
  );
export const visibleDiscoveries = (placed: StudioPiece[]) =>
  discoveries.filter((d) => placed.some((c) => distance(c, d) <= 1));
export function exploredCells(placed: StudioPiece[]) {
  const cells = new Map<string, { key: string; q: number; r: number }>();
  placed.forEach((cell) =>
    [[0, 0], ...neighbours].forEach(([dq, dr]) => {
      const q = cell.q + dq,
        r = cell.r + dr,
        key = `${q},${r}`;
      cells.set(key, { key, q, r });
    }),
  );
  return [...cells.values()];
}
export const shelfGroups = [
  "All tiles",
  "Terrain",
  "Buildings",
  "Little places",
] as const;
export type ShelfGroup = (typeof shelfGroups)[number];
const nature = new Set(["Terrain", "Landscapes"]);
const first = [
  "meadow",
  "woodland",
  "water",
  "wildflowers",
  "treehouse",
  "castle",
  "mountain",
  "waterfall",
  "volcano",
  "lighthouse",
];
export const buildable = catalogue
  .filter((t) => t.id !== "treasure" && t.id !== "home")
  .slice()
  .sort((a, b) => {
    const ai = first.indexOf(a.id),
      bi = first.indexOf(b.id);
    return (ai < 0 ? 99 : ai) - (bi < 0 ? 99 : bi);
  });
export const groupFor = (kind: TileKind): ShelfGroup => {
  const item = tileById[kind];
  return nature.has(item.category) ||
    ["meadow", "woodland", "water"].includes(kind)
    ? "Terrain"
    : ["Buildings", "Destinations"].includes(item.category)
      ? "Buildings"
      : "Little places";
};
