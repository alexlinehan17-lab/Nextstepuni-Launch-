"use strict";
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
Object.defineProperty(exports, "__esModule", { value: true });
exports.buildPublicProjection = buildPublicProjection;
/**
 * Build the projection from a user document and a progress document.
 * Returns null if the user is staff (GC / admin), if there is no island
 * state, or if no NorthStar category can be determined — in any of those
 * cases the caller should ensure no /islandPublic/{uid} document exists.
 */
function buildPublicProjection(userData, progressData) {
    if (!userData || !progressData)
        return null;
    // Filter out staff accounts — they don't appear in the peer view.
    const role = userData.role;
    if (role === "gc" || role === "admin" || userData.isAdmin === true) {
        return null;
    }
    const islandState = progressData.islandState;
    if (!islandState)
        return null;
    const northStar = progressData.northStar;
    const category = islandState.category ?? northStar?.category;
    if (!category)
        return null;
    const placements = islandState.placements ?? [];
    const purchaseHistory = islandState.purchaseHistory ?? [];
    const publicPlacements = placements.map((p) => {
        const projected = {
            itemId: p.itemId,
            model: p.model,
            type: p.type,
            q: p.q,
            r: p.r,
        };
        if (p.rotation !== undefined)
            projected.rotation = p.rotation;
        if (p.scale !== undefined)
            projected.scale = p.scale;
        if (p.offsetX !== undefined)
            projected.offsetX = p.offsetX;
        if (p.offsetZ !== undefined)
            projected.offsetZ = p.offsetZ;
        if (p.isStarter !== undefined)
            projected.isStarter = p.isStarter;
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
//# sourceMappingURL=islandProjection.js.map