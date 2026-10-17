/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Year islands: the classmate-visible projection of a student's paper island.
 *
 * `/islandPublic/{uid}` is the ONLY copy of a student's island that another
 * student can read. Classmates in the same school AND the same year group may
 * read it (firestore.rules); only the Cloud Functions in islandProjectionSync.ts
 * write it. It holds exactly what a read-only island renderer needs plus a
 * first name and an avatar, and nothing a classmate could use to infer study
 * activity:
 *
 *   kept:     tile position, kind, ink-edge stamp, capybara appearance, Wonder id
 *   dropped:  Journey Points (balance, earned, spent), each tile's cost and id,
 *             placement order, credits, ranks, undo, request ids, revision,
 *             kept stickers, met/claimed visitors, treasures opened, the North
 *             Star (category and statement), every timestamp
 *
 * Schema 1 (2026-04) projected the legacy `islandState` to the whole school.
 * Schema 2 (2026-10-17) projects the current `paperIsland` to one year group
 * and honours the student's "Show my island to my year" choice. See
 * compliance/PEER_ISLAND_REFACTOR_PLAN.md §9 and compliance/DPIA.md R1.
 *
 * Pure and framework-free: the triggers, the backfill script
 * (scripts/backfill-year-islands.mjs, through functions/lib) and the web client
 * all share these definitions.
 */

import { tileById, type TileKind } from "./paperCatalogue";
import { axialDistance } from "./paperGeometry";
import { PAPER_EDGES, PAPER_ISLAND_VERSION } from "./paperIslandModel";
import { isPaperVisitorId, type PaperVisitorId } from "./paperVisitors";

export const YEAR_ISLAND_SCHEMA_VERSION = 2;
/** The doc is fanned out to a whole year group; keep it small whatever the island. */
export const MAX_PUBLIC_TILES = 500;
const MAX_NAME_LENGTH = 40;
const MAX_AVATAR_LENGTH = 100;
const MAX_COORDINATE = 4096;

/** Year groups whose students can see each other. Graduates have left school. */
export const PEER_YEAR_GROUPS = ["1st", "2nd", "3rd", "TY", "5th", "6th", "LCA1", "LCA2"] as const;
export type PeerYearGroup = (typeof PEER_YEAR_GROUPS)[number];
export const isPeerYearGroup = (value: unknown): value is PeerYearGroup =>
  typeof value === "string" && (PEER_YEAR_GROUPS as readonly string[]).includes(value);

/**
 * `users/{uid}.islandVisibility`. Absent means "year": sharing with the year is
 * the default, and a student can switch it off at any time from Journey.
 */
export const ISLAND_VISIBILITY_FIELD = "islandVisibility";
export const ISLAND_VISIBILITY_VALUES = ["year", "hidden"] as const;
export type IslandVisibility = (typeof ISLAND_VISIBILITY_VALUES)[number];
export const islandVisibilityOf = (user: Record<string, unknown> | undefined): IslandVisibility =>
  user?.[ISLAND_VISIBILITY_FIELD] === "hidden" ? "hidden" : "year";

export interface YearIslandTile {
  q: number;
  r: number;
  kind: TileKind;
  edge?: { variant: (typeof PAPER_EDGES)[number]; seed: number };
  appearance?: "capybara";
  wonderId?: PaperVisitorId;
}

export interface YearIslandProjection {
  schemaVersion: typeof YEAR_ISLAND_SCHEMA_VERSION;
  /** First name only. */
  name: string;
  avatar: string;
  school: string;
  yearGroup: PeerYearGroup;
  /** Nearest the home tile first, at most MAX_PUBLIC_TILES. */
  tiles: YearIslandTile[];
  /** Every tile on the island, including any beyond the cap. */
  tileCount: number;
}

export type YearIslandExclusion =
  | "no-user"
  | "no-progress"
  | "staff"
  | "disabled"
  | "hidden"
  | "no-school"
  | "no-year"
  | "graduated"
  | "no-island";

export type YearIslandPlan =
  | { projection: YearIslandProjection; excluded?: undefined }
  | { projection: null; excluded: YearIslandExclusion };

type Data = Record<string, unknown> | undefined;

const firstName = (value: unknown): string => {
  if (typeof value !== "string") return "";
  const first = value.trim().split(/\s+/)[0] ?? "";
  return [...first].slice(0, MAX_NAME_LENGTH).join("");
};

const isCoordinate = (value: unknown): value is number =>
  Number.isSafeInteger(value) && Math.abs(value as number) <= MAX_COORDINATE;

function isStaffProfile(user: Record<string, unknown>) {
  return user.role === "gc" || user.role === "staff" || user.role === "admin" || user.isAdmin === true;
}

/**
 * The year a student is in: the users doc wins; older accounts that only
 * recorded it in onboarding's subject profile fall back to that.
 */
export function studentYearGroup(user: Data, progress: Data): unknown {
  if (typeof user?.yearGroup === "string" && user.yearGroup) return user.yearGroup;
  const profile = progress?.subjectProfile as { yearGroup?: unknown } | undefined;
  return profile?.yearGroup;
}

/** Copy only the visual fields of each tile, nearest the home tile first. */
export function publicTiles(rawTiles: unknown): { tiles: YearIslandTile[]; tileCount: number } {
  const source = Array.isArray(rawTiles) ? rawTiles : [];
  const seen = new Set<string>();
  const tiles: YearIslandTile[] = [];
  for (const raw of source) {
    if (!raw || typeof raw !== "object") continue;
    const tile = raw as Record<string, unknown>;
    if (!isCoordinate(tile.q) || !isCoordinate(tile.r)) continue;
    if (typeof tile.kind !== "string" || !Object.prototype.hasOwnProperty.call(tileById, tile.kind)) continue;
    const key = `${tile.q},${tile.r}`;
    if (seen.has(key)) continue;
    seen.add(key);
    const projected: YearIslandTile = { q: tile.q, r: tile.r, kind: tile.kind as TileKind };
    const edge = tile.edge as { variant?: unknown; seed?: unknown } | undefined;
    if (
      edge
      && (PAPER_EDGES as readonly unknown[]).includes(edge.variant)
      && Number.isSafeInteger(edge.seed)
      && (edge.seed as number) >= 0
      && (edge.seed as number) <= 0xffffffff
    ) {
      projected.edge = { variant: edge.variant as (typeof PAPER_EDGES)[number], seed: edge.seed as number };
    }
    if (tile.kind === "water" && tile.appearance === "capybara") projected.appearance = "capybara";
    if (isPaperVisitorId(tile.wonderId)) projected.wonderId = tile.wonderId;
    tiles.push(projected);
  }
  // Distance from home, then position: a cap keeps the island's connected core,
  // and the order says nothing about when each tile was placed.
  const origin = { q: 0, r: 0 };
  tiles.sort((a, b) => axialDistance(a, origin) - axialDistance(b, origin) || a.r - b.r || a.q - b.q);
  return { tiles: tiles.slice(0, MAX_PUBLIC_TILES), tileCount: tiles.length };
}

/** Decide whether this student has a classmate-visible island, and build it. */
export function planYearIsland(user: Data, progress: Data): YearIslandPlan {
  if (!user) return { projection: null, excluded: "no-user" };
  if (!progress) return { projection: null, excluded: "no-progress" };
  if (isStaffProfile(user)) return { projection: null, excluded: "staff" };
  if (user.accountDisabled === true) return { projection: null, excluded: "disabled" };
  if (islandVisibilityOf(user) === "hidden") return { projection: null, excluded: "hidden" };
  if (typeof user.school !== "string" || !user.school) return { projection: null, excluded: "no-school" };
  const yearGroup = studentYearGroup(user, progress);
  if (yearGroup === "graduated") return { projection: null, excluded: "graduated" };
  if (!isPeerYearGroup(yearGroup)) return { projection: null, excluded: "no-year" };
  const island = progress.paperIsland as { version?: unknown; tiles?: unknown } | undefined;
  if (!island || island.version !== PAPER_ISLAND_VERSION) return { projection: null, excluded: "no-island" };
  const { tiles, tileCount } = publicTiles(island.tiles);
  if (!tiles.length) return { projection: null, excluded: "no-island" };
  return {
    projection: {
      schemaVersion: YEAR_ISLAND_SCHEMA_VERSION,
      name: firstName(user.name) || "Student",
      avatar: typeof user.avatar === "string" && user.avatar ? user.avatar.slice(0, MAX_AVATAR_LENGTH) : "James",
      school: user.school,
      yearGroup,
      tiles,
      tileCount,
    },
  };
}

/** Every field the projection reads, for Firestore field masks. */
export const YEAR_ISLAND_SOURCE_FIELDS = {
  users: ["name", "avatar", "school", "yearGroup", "role", "isAdmin", "accountDisabled", ISLAND_VISIBILITY_FIELD],
  progress: ["paperIsland.version", "paperIsland.tiles", "subjectProfile.yearGroup"],
} as const;

const stableJson = (value: unknown): string => JSON.stringify(value, (_key, v: unknown) =>
  v && typeof v === "object" && !Array.isArray(v)
    ? Object.fromEntries(Object.entries(v as Record<string, unknown>).sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0)))
    : v);

/** What a progress write can change about the projection. Unchanged → no work. */
export function progressProjectionKey(progress: Data): string {
  const island = progress?.paperIsland as { version?: unknown; tiles?: unknown } | undefined;
  const profile = progress?.subjectProfile as { yearGroup?: unknown } | undefined;
  return stableJson([island?.version ?? null, island?.tiles ?? null, profile?.yearGroup ?? null]);
}

/** What a users write can change about the projection. Unchanged → no work. */
export function userProjectionKey(user: Data): string {
  return stableJson(YEAR_ISLAND_SOURCE_FIELDS.users.map(field => user?.[field] ?? null));
}

/** True when a stored projection already says exactly this. */
export function sameProjection(stored: Data, next: YearIslandProjection): boolean {
  return !!stored && stableJson(stored) === stableJson(next);
}
