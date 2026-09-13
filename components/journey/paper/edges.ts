import { edgeKey, type Point } from "./geometry";

export const edgeDirections = [
  {
    id: "classic",
    name: "The clean cut",
    tag: "CURRENT DIRECTION",
    description:
      "The familiar cream slab. A crisp silhouette and a few small pen marks.",
    character: "Quiet, simple, graphic.",
    note: "A useful reference for judging how much character the alternatives add.",
  },
  {
    id: "deckled",
    name: "Torn sketchbook",
    tag: "MY STARTING PICK",
    description:
      "A softly torn underside, little paper fibres and irregular cream layers. Still light; a little less perfect.",
    character: "Loose, tactile, hand-made.",
    note: "The closest extension of the drawing style. I’d start here, with a few layered edges mixed in.",
  },
  {
    id: "layers",
    name: "Pages of a story",
    tag: "LAYERED PAPER",
    description:
      "A little stack of uneven sketchbook pages. Fine lines follow the island; an orange page occasionally peeks through.",
    character: "Bookish, detailed, playful.",
    note: "A strong fit for a world earned through learning. Keep the layers sparse at small map sizes.",
  },
  {
    id: "folded",
    name: "Folded & tucked",
    tag: "PAPER CONSTRUCTION",
    description:
      "Faceted card, tucked corners and a few loose folds. More like a little model built on a desk.",
    character: "Sculptural, crisp, crafted.",
    note: "Gives the tiles more structure while keeping the paper-world idea very clear.",
  },
  {
    id: "earth",
    name: "Roots below",
    tag: "A LIVING CROSS-SECTION",
    description:
      "Warm ochre earth, wandering roots and small buried pebbles beneath the grass.",
    character: "Organic, earthy, exploratory.",
    note: "A good way to suggest life below the surface. Could be reserved for woodland and garden regions.",
  },
  {
    id: "chalk",
    name: "Little chalk cliffs",
    tag: "DRAWN ROCK",
    description:
      "Pale fractured faces and an uneven lower outline. A few deeper notches give the island a rocky silhouette.",
    character: "Adventurous, weighty, coastal.",
    note: "Worth trying on remote islands and destination edges, where extra depth makes the place feel special.",
  },
  {
    id: "felt",
    name: "Stitched together",
    tag: "SOFT PATCHWORK",
    description:
      "A rounded, softly scalloped edge with small running stitches and the occasional orange repair.",
    character: "Cosy, toy-like, unexpected.",
    note: "The biggest departure: a world that feels stitched and collected rather than cut from a sheet.",
  },
  {
    id: "wild",
    name: "The wandering edge",
    tag: "A LITTLE OVERGROWN",
    description:
      "Cream paper under a wandering fringe of moss. Small roots and leaves spill over different sections.",
    character: "Lively, unruly, growing.",
    note: "Useful as a subtle companion to torn paper. Keep the overgrowth varied so it never becomes a repeated border.",
  },
] as const;
export type EdgeStyle = (typeof edgeDirections)[number]["id"] | "ink";
export type EdgeDirection = {
  id: EdgeStyle;
  name: string;
  tag: string;
  description: string;
  character: string;
  note: string;
};
export const edgeById = {
  ...Object.fromEntries(edgeDirections.map((s) => [s.id, s])),
  ink: {
    id: "ink",
    name: "Loose ink · four variations",
    tag: "RANDOM ON PLACEMENT",
    description:
      "Four variations of the same cream edge, with loose charcoal nicks and small chips.",
    character: "A familiar edge, a different little mark.",
    note: "The edge is drawn once when a tile is placed, then stays with it.",
  },
} as Record<EdgeStyle, EdgeDirection>;
export function grain(key: string, seed = 0) {
  let h = 2166136261;
  for (const c of `${seed}:${key}`) {
    h ^= c.charCodeAt(0);
    h = Math.imul(h, 16777619);
  }
  h ^= h >>> 16;
  h = Math.imul(h, 0x85ebca6b);
  h ^= h >>> 13;
  h = Math.imul(h, 0xc2b2ae35);
  h ^= h >>> 16;
  return (h >>> 0) / 4294967295;
}
const amplitude: Record<EdgeStyle, number> = {
  ink: 0.02,
  classic: 0,
  deckled: 0.14,
  layers: 0.075,
  folded: 0.05,
  earth: 0.12,
  chalk: 0.24,
  felt: 0.08,
  wild: 0.12,
};
export function vertexDepth(
  p: Point,
  style: EdgeStyle,
  depth: number,
  variation: number,
  seed: number,
) {
  return (
    depth *
    (1 + (grain(`${p.x},${p.y}`, seed) - 0.5) * amplitude[style] * variation)
  );
}
export function lowerEdge(
  a: Point,
  b: Point,
  style: EdgeStyle,
  depth: number,
  variation = 1,
  seed = 0,
): Point[] {
  const key = edgeKey(a, b),
    start = vertexDepth(a, style, depth, variation, seed),
    end = vertexDepth(b, style, depth, variation, seed);
  return Array.from({ length: 13 }, (_, i) => {
    const t = i / 12,
      base = start + (end - start) * t,
      rough =
        i === 0 || i === 12
          ? 0
          : (grain(`${key}:${i}`, seed) - 0.5) *
            depth *
            amplitude[style] *
            variation *
            2;
    return {
      x: a.x + (b.x - a.x) * t,
      y: a.y + (b.y - a.y) * t + base + rough,
    };
  });
}
export function sidePath(a: Point, b: Point, bottom: Point[], soft = false) {
  const reverse = [...bottom].reverse();
  if (!soft)
    return `M${a.x} ${a.y}L${b.x} ${b.y}${reverse.map((p) => `L${p.x} ${p.y}`).join("")}Z`;
  return `M${a.x} ${a.y}L${b.x} ${b.y}L${reverse[0].x} ${reverse[0].y}${reverse
    .slice(1, -1)
    .map((p, i) => {
      const next = reverse[i + 2];
      return `Q${p.x} ${p.y} ${(p.x + next.x) / 2} ${(p.y + next.y) / 2}`;
    })
    .join("")}L${reverse.at(-1)!.x} ${reverse.at(-1)!.y}Z`;
}
