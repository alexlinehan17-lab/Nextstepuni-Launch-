import { tileById, type TileKind } from "./paperCatalogue";

export const PAPER_ISLAND_VERSION = 1;
// A sticker comes into view one placement sooner, while the wider atlas stays hidden.
export const PAPER_DISCOVERY_RADIUS = 2;
export const NEIGHBOURS = [
  [1, 0],
  [0, 1],
  [-1, 1],
  [-1, 0],
  [0, -1],
  [1, -1],
] as const;
export const PAPER_EDGES = [
  "long-nick",
  "twin-strokes",
  "small-bite",
  "worn-corner",
] as const;
export const PAPER_DISCOVERIES = [
  { id: "lantern-nautilus", q: -4, r: 1 },
  { id: "cloud-angler-spirit", q: 1, r: -4 },
  { id: "ember-wyrm", q: 4, r: 0 },
  { id: "folded-leviathan", q: -1, r: 4 },
  { id: "roaming-observatory", q: -7, r: 0 },
  { id: "runaway-windmill", q: 3, r: -7 },
  { id: "mountain-pilgrim", q: 7, r: -3 },
  { id: "teacup-citadel", q: 5, r: 4 },
  { id: "moon-ferryman", q: -5, r: 7 },
  { id: "tide-tailor", q: -8, r: 6 },
] as const;
// Small, authored destinations stay hidden until the student's shore reaches them.
export const PAPER_LANDMARKS: {
  id: string;
  q: number;
  r: number;
  kind: TileKind;
  name: string;
}[] = [
  { id: "hush-arch", q: -5, r: -2, kind: "ruins", name: "Hushwater ruins" },
  { id: "hush-meadow", q: -6, r: -1, kind: "meadow", name: "Hushwater ruins" },
  {
    id: "hush-treasure",
    q: -6,
    r: -2,
    kind: "treasure",
    name: "The Hushwater chest",
  },
  { id: "far-castle", q: 7, r: 1, kind: "castle", name: "The far shore" },
  { id: "far-garden", q: 6, r: 2, kind: "orchard", name: "The far shore" },
  {
    id: "far-treasure",
    q: 7,
    r: 2,
    kind: "treasure",
    name: "The far shore chest",
  },
];
export function knownLandmarks(tiles: { q: number; r: number }[]) {
  const known = new Set<string>();
  let changed = true;
  while (changed) {
    changed = false;
    for (const d of PAPER_LANDMARKS)
      if (
        !known.has(d.id) &&
        [...tiles, ...PAPER_LANDMARKS.filter((l) => known.has(l.id))].some(
          (t) => axialDistance(t, d) <= 1,
        )
      ) {
        known.add(d.id);
        changed = true;
      }
  }
  return PAPER_LANDMARKS.filter((d) => known.has(d.id));
}
export type PaperDiscoveryId = (typeof PAPER_DISCOVERIES)[number]["id"];
export interface PaperTile {
  id: string;
  q: number;
  r: number;
  kind: TileKind;
  edge: { variant: (typeof PAPER_EDGES)[number]; seed: number };
  cost: number;
}
export interface PaperIsland {
  version: 1;
  revision: number;
  tiles: PaperTile[];
  kept: PaperDiscoveryId[];
  undo: { tileId: string; cost: number; usedCredit: boolean } | null;
  claimedCaches?: string[];
  lastRequest: string;
  credits: number;
  rewardedRank: number;
}
export type PaperCommand =
  | { action: "open" }
  | {
      action: "place";
      requestId: string;
      revision: number;
      q: number;
      r: number;
      kind: TileKind;
    }
  | { action: "undo"; requestId: string; revision: number }
  | { action: "keep"; id: PaperDiscoveryId }
  | { action: "claim"; id: string };
export interface PaperProgress {
  paperIsland?: PaperIsland;
  islandState?: { totalSpent?: number };
  pointsData?: { totalEarned?: number; totalSpent?: number };
}
export class PaperIslandError extends Error {}
export const axialDistance = (
  a: { q: number; r: number },
  b: { q: number; r: number },
) =>
  Math.max(
    Math.abs(a.q - b.q),
    Math.abs(a.r - b.r),
    Math.abs(a.q + a.r - b.q - b.r),
  );
export function createPaperIsland(): PaperIsland {
  const starter: [number, number, TileKind][] = [
    [0, 0, "home"],
    [-1, 0, "meadow"],
    [0, -1, "woodland"],
    [1, -1, "treehouse"],
    [1, 0, "water"],
    [0, 1, "wildflowers"],
    [-1, 1, "picnic"],
  ];
  return {
    version: 1,
    revision: 0,
    tiles: starter.map(([q, r, kind], i) => ({
      id: `starter-${i}`,
      q,
      r,
      kind,
      edge: { variant: PAPER_EDGES[i % 4], seed: i * 73291 },
      cost: 0,
    })),
    kept: [],
    undo: null,
    lastRequest: "",
    credits: 0,
    rewardedRank: 0,
  };
}
export function canBuildPaper(tiles: PaperTile[], q: number, r: number) {
  return (
    Number.isSafeInteger(q) &&
    Number.isSafeInteger(r) &&
    !tiles.some((t) => t.q === q && t.r === r) &&
    !PAPER_DISCOVERIES.some((d) => d.q === q && d.r === r) &&
    !PAPER_LANDMARKS.some((d) => d.q === q && d.r === r) &&
    [...tiles, ...knownLandmarks(tiles)].some(
      (t) => axialDistance(t, { q, r }) === 1,
    )
  );
}
// Server and demo share this reducer. The caller commits state and JP in one transaction.
export function applyPaperCommand(
  progress: PaperProgress,
  command: PaperCommand,
  random: () => number = Math.random,
) {
  const earned = Math.max(0, Math.trunc(progress.pointsData?.totalEarned ?? 0));
  let spent = Math.max(0, Math.trunc(progress.pointsData?.totalSpent ?? 0));
  const migrated = progress.paperIsland?.version !== PAPER_ISLAND_VERSION;
  let state: PaperIsland = migrated
    ? createPaperIsland()
    : progress.paperIsland!;
  if (migrated)
    spent -= Math.min(
      spent,
      Math.max(0, Math.trunc(progress.islandState?.totalSpent ?? 0)),
    );
  state = { ...state };
  // Each newly earned rank gives three meadow tiles to choose and place yourself.
  const rank = [400, 1200, 2400, 4000, 7200, 12000, 20000].filter(
    (n) => earned >= n,
  ).length;
  if (rank > state.rewardedRank)
    state = {
      ...state,
      credits: state.credits + 3 * (rank - state.rewardedRank),
      rewardedRank: rank,
    };
  if (command.action === "place" || command.action === "undo") {
    if (!/^[a-zA-Z0-9-]{12,80}$/.test(command.requestId))
      throw new PaperIslandError("Please try that placement again.");
    if (state.lastRequest === command.requestId)
      return { state, totalEarned: earned, totalSpent: spent, migrated };
    if (command.revision !== state.revision)
      throw new PaperIslandError(
        "Your island changed in another window. Please choose a spot again.",
      );
    if (command.action === "place") {
      if (
        !Object.prototype.hasOwnProperty.call(tileById, command.kind) ||
        command.kind === "home" ||
        command.kind === "treasure"
      )
        throw new PaperIslandError("Choose a tile from your collection.");
      if (!canBuildPaper(state.tiles, command.q, command.r))
        throw new PaperIslandError(
          "Choose an empty spot next to your island. Creature spaces are reserved.",
        );
      // Keep the single document comfortably below Firestore’s size limit.
      if (state.tiles.length >= 3000)
        throw new PaperIslandError("This island has reached its tile limit.");
      const usedCredit = command.kind === "meadow" && state.credits > 0;
      const cost = usedCredit ? 0 : tileById[command.kind].price;
      if (cost > earned - spent)
        throw new PaperIslandError(
          "You need a few more Journey Points for this tile.",
        );
      const tile: PaperTile = {
        id: command.requestId,
        q: command.q,
        r: command.r,
        kind: command.kind,
        cost,
        edge: {
          variant: PAPER_EDGES[Math.min(3, Math.floor(random() * 4))],
          seed: Math.floor(random() * 0x100000000) >>> 0,
        },
      };
      spent += cost;
      state = {
        ...state,
        tiles: [...state.tiles, tile],
        credits: state.credits - (usedCredit ? 1 : 0),
        undo: { tileId: tile.id, cost, usedCredit },
      };
    } else {
      if (!state.undo || !state.tiles.some((t) => t.id === state.undo?.tileId))
        throw new PaperIslandError("There is no placement to undo.");
      spent = Math.max(0, spent - state.undo.cost);
      const tiles = state.tiles.filter((t) => t.id !== state.undo?.tileId);
      state = {
        ...state,
        tiles,
        kept: state.kept.filter((id) => {
          const d = PAPER_DISCOVERIES.find((item) => item.id === id);
          return (
            d &&
            [...tiles, ...knownLandmarks(tiles)].some(
              (t) => axialDistance(t, d) <= PAPER_DISCOVERY_RADIUS,
            )
          );
        }),
        credits: state.credits + (state.undo.usedCredit ? 1 : 0),
        undo: null,
      };
    }
    state = {
      ...state,
      revision: state.revision + 1,
      lastRequest: command.requestId,
    };
  } else if (command.action === "claim") {
    const found = knownLandmarks(state.tiles).find(
      (d) => d.id === command.id && d.kind === "treasure",
    );
    if (!found)
      throw new PaperIslandError("Build closer to reach this treasure.");
    if (!(state.claimedCaches ?? []).includes(found.id))
      state = {
        ...state,
        claimedCaches: [...(state.claimedCaches ?? []), found.id],
        credits: state.credits + 2,
        undo: null,
        revision: state.revision + 1,
      };
  } else if (command.action === "keep") {
    const found = PAPER_DISCOVERIES.find((d) => d.id === command.id);
    if (
      !found ||
      ![...state.tiles, ...knownLandmarks(state.tiles)].some(
        (t) => axialDistance(t, found) <= PAPER_DISCOVERY_RADIUS,
      )
    )
      throw new PaperIslandError("Build closer to discover this story.");
    state = { ...state, kept: [...new Set([...state.kept, command.id])] };
  } else if (command.action !== "open")
    throw new PaperIslandError("Unknown island action.");
  return { state, totalEarned: earned, totalSpent: spent, migrated };
}
