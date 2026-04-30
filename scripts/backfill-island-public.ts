/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * One-shot backfill: read every /progress/{uid} document, build the
 * /islandPublic/{uid} projection, and write it.
 *
 * Run modes:
 *   - Default (no flags):       dry-run only. Prints "would write N".
 *   - --apply:                  performs writes, but ONLY against the
 *                               local emulator unless --allow-production
 *                               is also passed.
 *   - --allow-production --apply: required to write against production
 *                               Firestore. Refuses without both flags.
 *
 * Emulator usage:
 *   FIRESTORE_EMULATOR_HOST=localhost:8080 \
 *     GCLOUD_PROJECT=nextstepuni-app \
 *     npx tsx scripts/backfill-island-public.ts --apply
 *
 * Production usage (requires explicit confirmation from Alex first):
 *   GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json \
 *     GCLOUD_PROJECT=nextstepuni-app \
 *     npx tsx scripts/backfill-island-public.ts --apply --allow-production
 *
 * The projection schema and the buildPublicProjection() logic mirror
 * functions/src/islandProjection.ts. They are duplicated here because
 * this script does not import from the functions build output. If you
 * change the projection schema, update both places.
 */

import { initializeApp, getApps, applicationDefault } from "firebase-admin/app";
import { getFirestore, FieldValue } from "firebase-admin/firestore";

interface IslandPlacement {
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

interface IslandPlacementPublic {
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
}

interface PublicProjection {
  name: string;
  avatar: string;
  school: string;
  category: string;
  placements: IslandPlacementPublic[];
  placementCount: number;
  score: number;
  schemaVersion: number;
}

function buildPublicProjection(
  userData: Record<string, unknown> | undefined,
  progressData: Record<string, unknown> | undefined,
): PublicProjection | null {
  if (!userData || !progressData) return null;

  const role = userData.role;
  if (role === "gc" || role === "admin" || userData.isAdmin === true) {
    return null;
  }

  const islandState = progressData.islandState as
    | { category?: string; placements?: IslandPlacement[]; purchaseHistory?: string[] }
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

async function main(): Promise<void> {
  const argv = process.argv.slice(2);
  const apply = argv.includes("--apply");
  const allowProd = argv.includes("--allow-production");

  const isEmulator = !!process.env.FIRESTORE_EMULATOR_HOST;
  const projectId = process.env.GCLOUD_PROJECT ?? process.env.FIREBASE_PROJECT ?? "<not-set>";

  console.log("== backfill-island-public ==");
  console.log(`  apply:              ${apply}`);
  console.log(`  allow-production:   ${allowProd}`);
  console.log(`  emulator:           ${isEmulator} (FIRESTORE_EMULATOR_HOST=${process.env.FIRESTORE_EMULATOR_HOST ?? "<unset>"})`);
  console.log(`  project:            ${projectId}`);
  console.log("");

  if (apply && !isEmulator && !allowProd) {
    console.error("REFUSED: --apply against production Firestore requires --allow-production.");
    console.error("Either set FIRESTORE_EMULATOR_HOST=localhost:8080 (recommended) or pass --allow-production.");
    process.exit(2);
  }

  if (getApps().length === 0) {
    if (isEmulator) {
      // Emulator path: no real credentials needed. The Admin SDK will
      // honour FIRESTORE_EMULATOR_HOST automatically once initialised
      // with a project ID.
      initializeApp({ projectId });
    } else {
      initializeApp({ credential: applicationDefault(), projectId });
    }
  }

  const db = getFirestore();

  const progressSnap = await db.collection("progress").get();
  console.log(`Read ${progressSnap.size} progress documents.`);

  let willWrite = 0;
  let willSkip = 0;
  let written = 0;
  let errors = 0;

  for (const progressDoc of progressSnap.docs) {
    const uid = progressDoc.id;
    try {
      const userSnap = await db.collection("users").doc(uid).get();
      if (!userSnap.exists) {
        willSkip++;
        continue;
      }

      const projection = buildPublicProjection(userSnap.data(), progressDoc.data());
      if (!projection) {
        willSkip++;
        continue;
      }

      if (apply) {
        await db.collection("islandPublic").doc(uid).set({
          ...projection,
          updatedAt: FieldValue.serverTimestamp(),
        });
        written++;
      } else {
        willWrite++;
      }
    } catch (err) {
      errors++;
      console.error(`Error processing ${uid}:`, err);
    }
  }

  console.log("");
  console.log("== summary ==");
  if (apply) {
    console.log(`  written: ${written}`);
    console.log(`  skipped: ${willSkip}`);
    console.log(`  errors:  ${errors}`);
  } else {
    console.log(`  would write: ${willWrite}`);
    console.log(`  would skip:  ${willSkip}`);
    console.log(`  errors:      ${errors}`);
    console.log("");
    console.log("Re-run with --apply to perform the writes.");
  }

  if (errors > 0) process.exit(1);
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
