import type { InkStamp } from "./inkVariants";
// All surfaces and neighbours use these same vertices. No per-image footprint.
export const TILE_WIDTH = 168;
export const TILE_HEIGHT = 112;
export const PAPER_DEPTH = 21;
export type Point = { x: number; y: number };
export const centre = (q: number, r: number): Point => ({
  x: TILE_WIDTH * (q + r / 2),
  y: TILE_HEIGHT * 0.75 * r,
});
export function vertices(x = 0, y = 0): Point[] {
  return [
    { x, y: y - 56 },
    { x: x + 84, y: y - 28 },
    { x: x + 84, y: y + 28 },
    { x, y: y + 56 },
    { x: x - 84, y: y + 28 },
    { x: x - 84, y: y - 28 },
  ];
}
export const points = (x = 0, y = 0) =>
  vertices(x, y)
    .map((p) => `${p.x},${p.y}`)
    .join(" ");
export const edgeKey = (a: Point, b: Point) =>
  [`${a.x},${a.y}`, `${b.x},${b.y}`].sort().join("|");
export type GroundCell = {
  key: string;
  x: number;
  y: number;
  inkEdge?: InkStamp;
  groundColor?: string;
};
export function boundaryEdges(cells: GroundCell[]) {
  const edges = new Map<
    string,
    { a: Point; b: Point; owners: number; cellKey: string; side: number }
  >();
  for (const c of cells) {
    const v = vertices(c.x, c.y);
    for (let i = 0; i < 6; i++) {
      const a = v[i],
        b = v[(i + 1) % 6],
        key = edgeKey(a, b);
      const edge = edges.get(key);
      if (edge) edge.owners++;
      else edges.set(key, { a, b, owners: 1, cellKey: c.key, side: i });
    }
  }
  return [...edges.values()].filter((e) => e.owners === 1);
}
export function allEdges(cells: GroundCell[]) {
  const edges = new Map<string, { a: Point; b: Point }>();
  for (const c of cells) {
    const v = vertices(c.x, c.y);
    for (let i = 0; i < 6; i++) {
      const a = v[i],
        b = v[(i + 1) % 6];
      edges.set(edgeKey(a, b), { a, b });
    }
  }
  return [...edges.values()];
}
