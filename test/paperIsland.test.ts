import { describe, it, expect } from "vitest";
import {
  applyPaperCommand,
  createPaperIsland,
  canBuildPaper,
  PAPER_DISCOVERIES,
  PAPER_EDGES,
  type PaperProgress,
  type PaperCommand,
} from "../functions/src/paperIslandModel";
import { ATHLETE_RANKS } from "../gamificationConfig";
import { frontier, exploredCells, visibleDiscoveries, nextDiscovery, discoveryRoute } from "../components/journey/paper/model";
import { piece } from "../components/journey/paper/studioModel";
const account = (): PaperProgress => ({
  pointsData: { totalEarned: 300, totalSpent: 0 },
  paperIsland: createPaperIsland(),
});
const purchase = (
  revision = 0,
  requestId = "test-purchase-0001",
): Extract<PaperCommand, { action: "place" }> => ({
  action: "place",
  requestId,
  revision,
  q: -2,
  r: 0,
  kind: "water",
});
const persist = (
  result: ReturnType<typeof applyPaperCommand>,
): PaperProgress => ({
  paperIsland: result.state,
  pointsData: {
    totalEarned: result.totalEarned,
    totalSpent: result.totalSpent,
  },
});
describe("Paper Journey economy and exploration", () => {
  it("resets legacy layouts once, refunds only legacy island spending, and leaves earned JP intact", () => {
    const old = {
      pointsData: { totalEarned: 1000, totalSpent: 800 },
      islandState: { totalSpent: 600 },
    };
    const next = applyPaperCommand(old, { action: "open" });
    expect(next.state.tiles).toHaveLength(7);
    expect(next.totalSpent).toBe(200);
    expect(next.totalEarned).toBe(1000);
    const again = applyPaperCommand(
      { ...persist(next), islandState: old.islandState },
      { action: "open" },
    );
    expect(again.totalSpent).toBe(200);
    expect(again.migrated).toBe(false);
  });
  it("commits the chosen position, exact cost and approved edge; retries never charge twice", () => {
    const next = applyPaperCommand(account(), purchase(), () => 0.8);
    expect(next.totalSpent).toBe(90);
    expect(next.state.tiles.at(-1)).toMatchObject({
      q: -2,
      r: 0,
      kind: "water",
      edge: { variant: "worn-corner" },
    });
    expect(applyPaperCommand(persist(next), purchase()).totalSpent).toBe(90);
    expect(PAPER_EDGES).not.toContain("forked-line");
    expect(PAPER_EDGES).not.toContain("dry-pen");
  });
  it("rejects stale windows, duplicate positions, remote cells and insufficient JP", () => {
    const next = applyPaperCommand(account(), purchase());
    expect(() =>
      applyPaperCommand(persist(next), purchase(0, "test-purchase-0002")),
    ).toThrow("another window");
    expect(() =>
      applyPaperCommand(persist(next), purchase(1, "test-purchase-0002")),
    ).toThrow("empty spot");
    expect(() =>
      applyPaperCommand(account(), {
        ...purchase(),
        action: "place",
        q: 90,
        r: 90,
        kind: "water",
      }),
    ).toThrow("empty spot");
    expect(() =>
      applyPaperCommand(
        { ...account(), pointsData: { totalEarned: 20, totalSpent: 0 } },
        purchase(),
      ),
    ).toThrow("few more");
  });
  it("refunds only the latest confirmed placement once, restoring the explored footprint", () => {
    const initial = account(),
      next = applyPaperCommand(initial, purchase());
    const restored = applyPaperCommand(persist(next), {
      action: "undo",
      revision: 1,
      requestId: "test-undo-000001",
    });
    expect(restored.totalSpent).toBe(0);
    expect(restored.state.tiles).toEqual(initial.paperIsland!.tiles);
    expect(() =>
      applyPaperCommand(persist(restored), {
        action: "undo",
        revision: 2,
        requestId: "test-undo-000002",
      }),
    ).toThrow("no placement");
    const cells = (p: PaperProgress) =>
      exploredCells(
        p.paperIsland!.tiles.map((t) => piece(t.q, t.r, t.kind, t.edge)),
      );
    expect(cells(persist(restored))).toEqual(cells(initial));
    expect(cells(persist(next)).length).toBeGreaterThan(cells(initial).length);
  });
  it("allows all six neighbouring positions far from the original viewport and reserves creatures", () => {
    const seed = { ...createPaperIsland().tiles[0], q: -100, r: 50 };
    expect(frontier([piece(seed.q, seed.r, seed.kind)])).toHaveLength(6);
    expect(canBuildPaper([seed], -101, 50)).toBe(true);
    for (const d of PAPER_DISCOVERIES)
      expect(canBuildPaper([{ ...seed, q: d.q + 1, r: d.r }], d.q, d.r)).toBe(
        false,
      );
  });
  it("awards rank tiles exactly once, at the app rank thresholds, without auto placing them", () => {
    for (let i = 0; i < ATHLETE_RANKS.length; i++) {
      const open = applyPaperCommand(
        {
          pointsData: {
            totalEarned: ATHLETE_RANKS[i].minPoints,
            totalSpent: 0,
          },
        },
        { action: "open" },
      );
      expect(open.state.credits).toBe(i * 3);
      expect(open.state.tiles).toHaveLength(7);
      expect(
        applyPaperCommand(persist(open), { action: "open" }).state.credits,
      ).toBe(i * 3);
    }
    const opened = applyPaperCommand(
      { pointsData: { totalEarned: 400, totalSpent: 0 } },
      { action: "open" },
    );
    const built = applyPaperCommand(persist(opened), {
      action: "place",
      kind: "meadow",
      q: -2,
      r: 0,
      revision: 0,
      requestId: "credit-place-001",
    });
    expect(built.totalSpent).toBe(0);
    expect(built.state.credits).toBe(2);
    const undone = applyPaperCommand(persist(built), {
      action: "undo",
      revision: 1,
      requestId: "credit-undo-0001",
    });
    expect(undone.state.credits).toBe(3);
  });
  it("keeps only discovered stories; undo hides a discovery reached by the returned tile", () => {
    expect(() =>
      applyPaperCommand(account(), { action: "keep", id: "lantern-nautilus" }),
    ).toThrow("Build closer");
    const first = applyPaperCommand(account(), purchase());
    expect(visibleDiscoveries(first.state.tiles.map(t => piece(t.q, t.r, t.kind))).map(d => d.id)).toContain("lantern-nautilus");
    const kept = applyPaperCommand(persist(first), {
      action: "keep",
      id: "lantern-nautilus",
    });
    expect(kept.state.kept).toEqual(["lantern-nautilus"]);
    expect(
      applyPaperCommand(persist(kept), {
        action: "undo",
        revision: 1,
        requestId: "discovery-undo-001",
      }).state.kept,
    ).toEqual([]);
  });
});

describe("hidden destinations", () => {
  it("reveals a connected landmark only when a placed tile reaches it; a chest is claimed once", () => {
    const base = createPaperIsland();
    const edge = {
      ...base.tiles[0],
      id: "approach-ruins",
      q: -4,
      r: -2,
      kind: "meadow" as const,
    };
    const result = applyPaperCommand(
      {
        paperIsland: {
          ...base,
          tiles: [...base.tiles, edge],
          undo: { tileId: edge.id, cost: 0, usedCredit: false },
        },
        pointsData: { totalEarned: 300, totalSpent: 0 },
      },
      { action: "claim", id: "hush-treasure" },
    );
    expect(result.state.credits).toBe(2);
    expect(result.state.undo).toBeNull();
    expect(
      applyPaperCommand(persist(result), {
        action: "claim",
        id: "hush-treasure",
      }).state.credits,
    ).toBe(2);
    expect(() =>
      applyPaperCommand(account(), { action: "claim", id: "hush-treasure" }),
    ).toThrow("Build closer");
    expect(canBuildPaper(result.state.tiles, -7, -1)).toBe(true);
    expect(canBuildPaper(base.tiles, -7, -1)).toBe(false);
    expect(canBuildPaper(result.state.tiles, -6, -2)).toBe(false);
  });
});


describe("sticker guidance", () => {
  it("finds a sticker after one legal placement and skips kept stories", () => {
    const placed = createPaperIsland().tiles.map(t => piece(t.q, t.r, t.kind));
    const route = nextDiscovery(placed, []);
    expect(route?.path).toHaveLength(1);
    const edge = route!.path[0];
    expect(frontier(placed).map(c => c.key)).toContain(edge.key);
    const grown = [...placed, edge];
    expect(visibleDiscoveries(grown).map(d => d.id)).toContain(route!.discovery.id);
    expect(nextDiscovery(grown, [route!.discovery.id])?.discovery.id).not.toBe(route!.discovery.id);
    expect(nextDiscovery(grown, PAPER_DISCOVERIES.map(d => d.id))).toBeNull();
  });
  it("routes around reserved creatures and landmarks without blocking adjacent building", () => {
    let placed = createPaperIsland().tiles.map(t => piece(t.q, t.r, t.kind));
    const target = PAPER_DISCOVERIES.find(d => d.id === "roaming-observatory")!;
    const route = discoveryRoute(placed, target);
    expect(route).not.toBeNull();
    for (const cell of route!) {
      expect(frontier(placed).map(c => c.key)).toContain(cell.key);
      placed = [...placed, cell];
    }
    expect(visibleDiscoveries(placed).map(d => d.id)).toContain(target.id);
    expect(discoveryRoute(placed, target)).toEqual([]);
    expect(discoveryRoute([], target)).toBeNull();
  });
});
