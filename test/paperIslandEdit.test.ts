/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Remove and replace placed tiles. Workshop feedback (12 Oct 2026): "Being able
 * to delete and replace the blocks in the game" and "i have made a mistake on my
 * island and i cannot delete it". Undo only ever covered the last placement.
 */
import { describe, expect, it } from "vitest";
import {
  applyPaperCommand,
  createPaperIsland,
  paperRemovalBlock,
  paperReplaceCost,
  paperTileRefund,
  type PaperCommand,
  type PaperIsland,
  type PaperProgress,
} from "../functions/src/paperIslandModel";

let seq = 0;
const id = () => `edit-request-${String(++seq).padStart(4, "0")}`;
// Rank rewards already paid out, so the only meadow credits are the ones a test sets.
const account = (earned = 1000, island: PaperIsland = createPaperIsland()): PaperProgress => ({
  pointsData: { totalEarned: earned, totalSpent: 0 },
  paperIsland: { ...island, rewardedRank: 7 },
});
const persist = (result: ReturnType<typeof applyPaperCommand>): PaperProgress => ({
  paperIsland: result.state,
  pointsData: { totalEarned: result.totalEarned, totalSpent: result.totalSpent },
});
// Omit distributed over the command union, so each action keeps its own fields.
type EditCommand<C> = C extends unknown ? Omit<C, "requestId" | "revision"> : never;
const run = (progress: PaperProgress, command: EditCommand<Extract<PaperCommand, { requestId: string }>>) =>
  persist(applyPaperCommand(progress, { requestId: id(), revision: progress.paperIsland!.revision, ...command } as PaperCommand, () => 0.5));
const tileAt = (progress: PaperProgress, q: number, r: number) => progress.paperIsland!.tiles.find(t => t.q === q && t.r === r)!;
const spent = (progress: PaperProgress) => progress.pointsData!.totalSpent;

describe("removing a placed tile", () => {
  it("refunds exactly what the tile cost when placed, not today's price", () => {
    let p = run(account(), { action: "place", q: -2, r: 0, kind: "water" });
    expect(spent(p)).toBe(90);
    // A tile bought before a price change still refunds what was paid.
    p.paperIsland!.tiles = p.paperIsland!.tiles.map(t => t.q === -2 && t.r === 0 ? { ...t, cost: 75 } : t);
    p = run(p, { action: "remove", tileId: tileAt(p, -2, 0).id });
    expect(tileAt(p, -2, 0)).toBeUndefined();
    expect(spent(p)).toBe(15);
  });

  it("returns an earned meadow tile, not Journey Points, for a meadow placed with a credit", () => {
    let p = account(1000, { ...createPaperIsland(), credits: 1 });
    p = run(p, { action: "place", q: -2, r: 0, kind: "meadow" });
    expect(p.paperIsland!.credits).toBe(0);
    expect(spent(p)).toBe(0);
    const meadow = tileAt(p, -2, 0);
    expect(paperTileRefund(meadow)).toEqual({ jp: 0, credit: true });
    p = run(p, { action: "remove", tileId: meadow.id });
    expect(p.paperIsland!.credits).toBe(1);
    expect(spent(p)).toBe(0);
  });

  it("lets a starter tile go for nothing back, and never the home tile", () => {
    let p = account();
    const picnic = tileAt(p, -1, 1);
    expect(paperTileRefund(picnic)).toEqual({ jp: 0, credit: false });
    p = run(p, { action: "remove", tileId: picnic.id });
    expect(tileAt(p, -1, 1)).toBeUndefined();
    expect(spent(p)).toBe(0);
    const home = tileAt(p, 0, 0);
    expect(paperRemovalBlock(p.paperIsland!.tiles, home.id)).toBe("Your home stays at the heart of your island.");
    expect(() => run(p, { action: "remove", tileId: home.id })).toThrow("Your home stays at the heart of your island.");
    expect(() => run(p, { action: "replace", tileId: home.id, kind: "meadow" })).toThrow("Your home stays at the heart of your island.");
  });

  it("never splits the island: a tile holding others to home can be replaced but not removed", () => {
    let p = run(account(), { action: "place", q: -2, r: 0, kind: "water" });
    p = run(p, { action: "place", q: -3, r: 0, kind: "water" });
    const bridge = tileAt(p, -2, 0);
    expect(paperRemovalBlock(p.paperIsland!.tiles, bridge.id)).toBe("Remove the tiles beyond it first, or replace it.");
    expect(() => run(p, { action: "remove", tileId: bridge.id })).toThrow("Remove the tiles beyond it first, or replace it.");
    p = run(p, { action: "replace", tileId: bridge.id, kind: "wildflowers" });
    expect(tileAt(p, -2, 0)).toMatchObject({ kind: "wildflowers", edge: bridge.edge });
    // Taking the outer tile first frees the bridge.
    p = run(p, { action: "remove", tileId: tileAt(p, -3, 0).id });
    expect(paperRemovalBlock(p.paperIsland!.tiles, tileAt(p, -2, 0).id)).toBeNull();
  });

  it("keeps stickers already found when the tile that reached them goes", () => {
    let p = run(account(), { action: "place", q: -2, r: 0, kind: "water" });
    p = persist(applyPaperCommand(p, { action: "keep", id: "lantern-nautilus" }));
    p = run(p, { action: "remove", tileId: tileAt(p, -2, 0).id });
    expect(p.paperIsland!.kept).toContain("lantern-nautilus");
  });

  it("puts a removed Wonder back among the student's unplaced gifts", () => {
    let p = account(1000, { ...createPaperIsland(), claimedVisitors: ["luma"] });
    p = run(p, { action: "placeWonder", id: "luma", q: -2, r: 0 });
    const wonder = tileAt(p, -2, 0);
    expect(wonder.wonderId).toBe("luma");
    p = run(p, { action: "remove", tileId: wonder.id });
    expect(p.paperIsland!.tiles.some(t => t.wonderId === "luma")).toBe(false);
    expect(p.paperIsland!.claimedVisitors).toContain("luma");
    expect(spent(p)).toBe(0);
    p = run(p, { action: "placeWonder", id: "luma", q: -2, r: 0 });
    expect(tileAt(p, -2, 0).wonderId).toBe("luma");
  });
});

describe("replacing a placed tile", () => {
  it("pays the new price less the old tile's refund, in either direction", () => {
    let p = run(account(), { action: "place", q: -2, r: 0, kind: "water" });
    expect(paperReplaceCost(p.paperIsland!, tileAt(p, -2, 0).id, "capybara")).toMatchObject({ cost: 120, net: 30 });
    p = run(p, { action: "replace", tileId: tileAt(p, -2, 0).id, kind: "capybara" });
    expect(tileAt(p, -2, 0)).toMatchObject({ kind: "water", appearance: "capybara", cost: 120 });
    expect(spent(p)).toBe(120);
    p = run(p, { action: "replace", tileId: tileAt(p, -2, 0).id, kind: "meadow" });
    expect(tileAt(p, -2, 0)).toMatchObject({ kind: "meadow", cost: 60 });
    expect(spent(p)).toBe(60);
  });

  it("swaps a credit meadow for a credit meadow's worth: the returned credit pays for a new meadow", () => {
    let p = account(1000, { ...createPaperIsland(), credits: 1 });
    p = run(p, { action: "place", q: -2, r: 0, kind: "meadow" });
    p = run(p, { action: "replace", tileId: tileAt(p, -2, 0).id, kind: "water" });
    expect(p.paperIsland!.credits).toBe(1);
    expect(spent(p)).toBe(90);
  });

  it("refuses a swap the student cannot afford, and a swap for the same tile", () => {
    const p = run(account(100), { action: "place", q: -2, r: 0, kind: "water" });
    const water = tileAt(p, -2, 0);
    expect(paperReplaceCost(p.paperIsland!, water.id, "castle")!.net).toBeGreaterThan(10);
    expect(() => run(p, { action: "replace", tileId: water.id, kind: "castle" })).toThrow("You need a few more Journey Points for this swap.");
    expect(() => run(p, { action: "replace", tileId: water.id, kind: "water" })).toThrow("Choose a different tile to replace it with.");
    expect(() => run(p, { action: "replace", tileId: water.id, kind: "home" })).toThrow("Choose a tile from your collection.");
    expect(spent(p)).toBe(90);
  });
});

describe("edit safety", () => {
  it("applies a retried request once and rejects a stale window", () => {
    let p = run(account(), { action: "place", q: -2, r: 0, kind: "water" });
    const command = { action: "remove", requestId: "edit-retry-000001", revision: p.paperIsland!.revision, tileId: tileAt(p, -2, 0).id } as const;
    const once = persist(applyPaperCommand(p, command));
    const twice = persist(applyPaperCommand(once, command));
    expect(spent(twice)).toBe(0);
    expect(twice.paperIsland!.revision).toBe(once.paperIsland!.revision);
    expect(() => applyPaperCommand(once, { ...command, requestId: "edit-stale-0000001" })).toThrow("Your island changed in another window.");
    p = once;
    expect(() => run(p, { action: "remove", tileId: "not-a-tile" })).toThrow("That tile is no longer on your island.");
  });

  it("undoes a removal: the tile, its place in the order, its cost and its credit all come back", () => {
    let p = account(1000, { ...createPaperIsland(), credits: 1 });
    p = run(p, { action: "place", q: -2, r: 0, kind: "meadow" });
    p = run(p, { action: "place", q: -2, r: 1, kind: "water" });
    const before = p.paperIsland!.tiles.map(t => t.id);
    p = run(p, { action: "remove", tileId: tileAt(p, -2, 0).id });
    expect(p.paperIsland!.credits).toBe(1);
    p = run(p, { action: "undo" });
    expect(p.paperIsland!.tiles.map(t => t.id)).toEqual(before);
    expect(p.paperIsland!.credits).toBe(0);
    expect(spent(p)).toBe(90);
    expect(p.paperIsland!.undo).toBeNull();
  });

  it("undoes a replacement back to the original tile and price", () => {
    let p = run(account(), { action: "place", q: -2, r: 0, kind: "water" });
    const water = tileAt(p, -2, 0);
    p = run(p, { action: "replace", tileId: water.id, kind: "castle" });
    p = run(p, { action: "undo" });
    expect(tileAt(p, -2, 0)).toEqual(water);
    expect(spent(p)).toBe(90);
  });
});
