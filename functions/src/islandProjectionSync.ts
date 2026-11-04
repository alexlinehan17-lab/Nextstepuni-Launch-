/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Keep `/islandPublic/{uid}` equal to planYearIsland(users/{uid}, progress/{uid}).
 *
 * Both triggers (progress writes and users writes) and the backfill call this,
 * and it always works from a FRESH transactional read of both source documents,
 * never from the event payload. Triggers run in no guaranteed order, so a
 * projection built from a payload could resurrect an island its owner had just
 * hidden. Reading inside a transaction means whichever run commits last wrote
 * the current truth, and a "hide my island" write can never be overtaken.
 *
 * Type-only Admin SDK import, so scripts/backfill-year-islands.mjs can load the
 * compiled module with its own Firestore instance.
 */

import type { Firestore } from "firebase-admin/firestore";
import {
  planYearIsland,
  progressProjectionKey,
  sameProjection,
  userProjectionKey,
  YEAR_ISLAND_SOURCE_FIELDS,
  type YearIslandExclusion,
} from "./islandProjection";

export type YearIslandSyncOutcome =
  | { action: "written" | "unchanged" }
  | { action: "deleted" | "absent"; excluded: YearIslandExclusion };

// One mask serves all three reads (a path a document lacks is simply not
// returned), so a progress doc's study data never leaves Firestore here. A
// schema 1 projection differs in schemaVersion, so it is replaced in full by
// set() and its old fields (category, placements, score, updatedAt) go with it.
const FIELD_MASK = [...new Set<string>([
  ...YEAR_ISLAND_SOURCE_FIELDS.users,
  ...YEAR_ISLAND_SOURCE_FIELDS.progress,
  "schemaVersion", "name", "avatar", "school", "yearGroup", "tiles", "tileCount",
])];

export async function syncYearIsland(
  db: Firestore,
  uid: string,
  { dryRun = false }: { dryRun?: boolean } = {},
): Promise<YearIslandSyncOutcome> {
  const userRef = db.collection("users").doc(uid);
  const progressRef = db.collection("progress").doc(uid);
  const publicRef = db.collection("islandPublic").doc(uid);
  const decide = async (
    read: typeof db.getAll,
    write?: { set: (data: Record<string, unknown>) => void; remove: () => void },
  ): Promise<YearIslandSyncOutcome> => {
    const [userSnap, progressSnap, publicSnap] = await read(userRef, progressRef, publicRef, { fieldMask: FIELD_MASK });
    const plan = planYearIsland(
      userSnap.exists ? userSnap.data() : undefined,
      progressSnap.exists ? progressSnap.data() : undefined,
    );
    if (!plan.projection) {
      if (!publicSnap.exists) return { action: "absent", excluded: plan.excluded };
      write?.remove();
      return { action: "deleted", excluded: plan.excluded };
    }
    if (publicSnap.exists && sameProjection(publicSnap.data(), plan.projection)) return { action: "unchanged" };
    write?.set({ ...plan.projection });
    return { action: "written" };
  };
  if (dryRun) return decide(db.getAll.bind(db));
  return db.runTransaction(transaction => decide(
    transaction.getAll.bind(transaction) as typeof db.getAll,
    {
      set: data => { transaction.set(publicRef, data); },
      remove: () => { transaction.delete(publicRef); },
    },
  ));
}

type Data = Record<string, unknown> | undefined;

/**
 * onProgressWritten. progress/{uid} is written many times a session (points,
 * study data, module progress); only a change to the island's tiles, its
 * version, or the onboarding year fallback can change the projection, so
 * every other write returns null before reading anything.
 */
export function syncAfterProgressWrite(db: Firestore, uid: string, before: Data, after: Data) {
  if (before && after && progressProjectionKey(before) === progressProjectionKey(after)) return Promise.resolve(null);
  return syncYearIsland(db, uid);
}

/**
 * onUserWritten. Only first name, avatar, school, year group, role,
 * disablement or the sharing switch can change the projection.
 */
export function syncAfterUserWrite(db: Firestore, uid: string, before: Data, after: Data) {
  if (before && after && userProjectionKey(before) === userProjectionKey(after)) return Promise.resolve(null);
  return syncYearIsland(db, uid);
}
