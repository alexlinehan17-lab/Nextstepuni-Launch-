/**
 * Shared helper for building the public projection of a student's island
 * state. Used by:
 *   - onProgressWritten / onUserWritten Cloud Functions (in this package)
 *   - scripts/backfill-island-public.ts (the script duplicates the type
 *     definitions because it does not import from the functions build
 *     output; if you change the projection schema here, update the script
 *     too).
 *
 * The projection deliberately omits per-placement `purchasedAt` (behavioural
 * inference) and the raw `purchaseHistory` (replaced by a pre-computed
 * `score`). See compliance/PEER_ISLAND_REFACTOR_PLAN.md.
 */

export interface IslandPlacement {
  itemId: string;
  model: string;
  type: "hex" | "decoration";
  q: number;
  r: number;
  rotation?: number;
  scale?: number;
  offsetX?: number;
  offsetZ?: number;
  purchasedAt?: string;
  isStarter?: boolean;
}

export interface IslandPlacementPublic {
  itemId: string;
  model: string;
  type: "hex" | "decoration";
  q: number;
  r: number;
  rotation?: number;
  scale?: number;
  offsetX?: number;
  offsetZ?: number;
  isStarter?: boolean;
  // purchasedAt deliberately omitted
}

export interface IslandPublicProjection {
  name: string;
  avatar: string;
  school: string;
  category: string;
  placements: IslandPlacementPublic[];
  placementCount: number;
  score: number;
  schemaVersion: number;
}

/**
 * Build the projection from a user document and a progress document.
 * Returns null if the user is staff (GC / admin), if there is no island
 * state, or if no NorthStar category can be determined — in any of those
 * cases the caller should ensure no /islandPublic/{uid} document exists.
 */
export function buildPublicProjection(
  userData: Record<string, unknown> | undefined,
  progressData: Record<string, unknown> | undefined,
): IslandPublicProjection | null {
  if (!userData || !progressData) return null;

  // Filter out staff accounts — they don't appear in the peer view.
  const role = userData.role;
  if (role === "gc" || role === "admin" || userData.isAdmin === true) {
    return null;
  }

  const islandState = progressData.islandState as
    | {
        category?: string;
        placements?: IslandPlacement[];
        purchaseHistory?: string[];
      }
    | undefined;
  if (!islandState) return null;

  const northStar = progressData.northStar as { category?: string } | undefined;
  const category = islandState.category ?? northStar?.category;
  if (!category) return null;

  const placements: IslandPlacement[] = islandState.placements ?? [];
  const purchaseHistory: string[] = islandState.purchaseHistory ?? [];

  const publicPlacements: IslandPlacementPublic[] = placements.map((p) => {
    const projected: IslandPlacementPublic = {
      itemId: p.itemId,
      model: p.model,
      type: p.type,
      q: p.q,
      r: p.r,
    };
    if (p.rotation !== undefined) projected.rotation = p.rotation;
    if (p.scale !== undefined) projected.scale = p.scale;
    if (p.offsetX !== undefined) projected.offsetX = p.offsetX;
    if (p.offsetZ !== undefined) projected.offsetZ = p.offsetZ;
    if (p.isStarter !== undefined) projected.isStarter = p.isStarter;
    // purchasedAt: deliberately omitted from the public projection.
    return projected;
  });

  const placementCount = publicPlacements.filter((p) => !p.isStarter).length;
  const uniqueItems = new Set(purchaseHistory).size;
  const score = placementCount * 2 + uniqueItems * 3;

  return {
    name: typeof userData.name === "string" ? userData.name : "Student",
    avatar: typeof userData.avatar === "string" ? userData.avatar : "James",
    school: typeof userData.school === "string" ? userData.school : "",
    category,
    placements: publicPlacements,
    placementCount,
    score,
    schemaVersion: 1,
  };
}
