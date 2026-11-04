/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Client side of year islands: read a classmate's /islandPublic projection
 * (functions/src/islandProjection.ts) defensively and turn it into the pieces
 * the existing island renderer draws.
 */
import { getSchoolName } from "../../../schoolData";
import { knownLandmarks } from "../../../functions/src/paperIslandModel";
import {
  isPeerYearGroup,
  MAX_PUBLIC_TILES,
  type PeerYearGroup,
  type YearIslandTile,
} from "../../../functions/src/islandProjection";
import { isPaperVisitorId } from "../../../functions/src/paperVisitors";
import { tileById, type TileKind } from "../paper/catalogue";
import { piece, type StudioPiece } from "../paper/studioModel";
import type { IslandState } from "../paper/model";

export type { PeerYearGroup };

export interface YearIsland {
  uid: string;
  name: string;
  avatar: string;
  yearGroup: PeerYearGroup;
  tiles: YearIslandTile[];
  tileCount: number;
}

const EDGE_VARIANTS = new Set(["long-nick", "twin-strokes", "small-bite", "worn-corner"]);

/**
 * Validate one projection document. The server already sanitises it; this
 * guards an installed app whose tile catalogue is older than the server's
 * (an unknown kind is drawn as meadow, so the island keeps its shape).
 */
export function parseYearIsland(uid: string, data: Record<string, unknown> | undefined): YearIsland | null {
  if (!data || data.schemaVersion !== 2 || !isPeerYearGroup(data.yearGroup) || !Array.isArray(data.tiles)) return null;
  const tiles: YearIslandTile[] = [];
  for (const raw of data.tiles.slice(0, MAX_PUBLIC_TILES)) {
    if (!raw || typeof raw !== "object") continue;
    const tile = raw as Record<string, unknown>;
    if (!Number.isSafeInteger(tile.q) || !Number.isSafeInteger(tile.r)) continue;
    const known = typeof tile.kind === "string" && Object.prototype.hasOwnProperty.call(tileById, tile.kind);
    const next: YearIslandTile = { q: tile.q as number, r: tile.r as number, kind: known ? tile.kind as TileKind : "meadow" };
    const edge = tile.edge as { variant?: unknown; seed?: unknown } | undefined;
    if (edge && typeof edge.variant === "string" && EDGE_VARIANTS.has(edge.variant) && Number.isSafeInteger(edge.seed))
      next.edge = { variant: edge.variant as NonNullable<YearIslandTile["edge"]>["variant"], seed: edge.seed as number };
    if (tile.appearance === "capybara" && next.kind === "water") next.appearance = "capybara";
    if (isPaperVisitorId(tile.wonderId)) next.wonderId = tile.wonderId;
    tiles.push(next);
  }
  if (!tiles.length) return null;
  return {
    uid,
    name: typeof data.name === "string" && data.name ? data.name : "Student",
    avatar: typeof data.avatar === "string" && data.avatar ? data.avatar : "James",
    yearGroup: data.yearGroup,
    tiles,
    tileCount: typeof data.tileCount === "number" && data.tileCount >= tiles.length ? data.tileCount : tiles.length,
  };
}

/** Alphabetical by first name; two Aoifes keep a stable order. */
export const byName = (a: YearIsland, b: YearIsland) =>
  a.name.localeCompare(b.name, "en-IE", { sensitivity: "base" }) || (a.uid < b.uid ? -1 : a.uid > b.uid ? 1 : 0);

export function yearLabel(yearGroup: string | undefined): string {
  switch (yearGroup) {
    case "1st": return "1st Year";
    case "2nd": return "2nd Year";
    case "3rd": return "3rd Year";
    case "TY": return "Transition Year";
    case "5th": return "5th Year";
    case "6th": return "6th Year";
    case "LCA1": return "LCA Year 1";
    case "LCA2": return "LCA Year 2";
    default: return "";
  }
}

/** "5th Year at Marino", or just the school or year when one is missing. */
export function cohortLabel(school: string | undefined, yearGroup: string | undefined): string {
  const year = isPeerYearGroup(yearGroup) ? yearLabel(yearGroup) : "";
  const place = school ? getSchoolName(school) : "";
  return year && place ? `${year} at ${place}` : year || place;
}

/** The same pieces JourneyView draws for its own island, landmarks included. */
export function islandPieces(tiles: YearIslandTile[]): StudioPiece[] {
  const ground = tiles.map(t => ({ q: t.q, r: t.r }));
  return [
    ...tiles.map(t => piece(t.q, t.r, t.kind === "water" && t.appearance === "capybara" ? "capybara" : t.kind, t.edge, t.wonderId)),
    ...knownLandmarks(ground).map(t => piece(t.q, t.r, t.kind)),
  ];
}

/** A look-only world: nothing to spend, nothing to undo. */
export function readOnlyWorld(placed: StudioPiece[]): IslandState {
  return { placed, balance: 0, credits: 0, history: [], log: [] };
}

/** "Aoife’s island" */
export const possessive = (name: string) => `${name}’s`;
