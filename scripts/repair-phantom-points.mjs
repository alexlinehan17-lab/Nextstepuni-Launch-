/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * ONE-OFF REPAIR — recover points lost to the phantom "pointsData.totalEarned"
 * root field.
 *
 * WHAT HAPPENED
 *   components/InnovationZone.tsx awarded 5 points per completed timetable
 *   block with:
 *       setDoc(ref, { 'pointsData.totalEarned': increment(5) }, { merge: true })
 *   A dotted key inside setDoc is NOT a field path — the SDK treats the whole
 *   string as ONE field-name segment. So every one of those writes created (and
 *   then incremented) a root-level field literally named
 *   "pointsData.totalEarned", while the real pointsData.totalEarned map value
 *   never moved. Students saw the points locally until they reloaded; the GC
 *   dashboard, reading the real map, showed them understated — often as 0.
 *   (Dotted paths only work in updateDoc, which cannot be used there because
 *   the progress doc may not exist yet.)
 *
 * ORDER OF OPERATIONS — IMPORTANT
 *   Deploy the code fix FIRST, then run this. Running it against the old code
 *   just lets new junk accrue behind you.
 *
 * WHAT IT DOES
 *   For every progress/{uid} document holding the junk field:
 *     - adds its value into the real pointsData.totalEarned
 *     - deletes the junk field
 *   Idempotent: a second run finds nothing to do.
 *
 * USAGE
 *   Dry run (default — reports only, writes nothing):
 *     GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json \
 *       node scripts/repair-phantom-points.mjs
 *
 *   Apply:
 *     GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json \
 *       node scripts/repair-phantom-points.mjs --apply
 *
 * Requires firebase-admin (available under functions/node_modules).
 */
import { initializeApp, applicationDefault } from 'firebase-admin/app';
import { getFirestore, FieldPath, FieldValue } from 'firebase-admin/firestore';

const APPLY = process.argv.includes('--apply');
const JUNK_FIELD = 'pointsData.totalEarned';

initializeApp({ credential: applicationDefault(), projectId: 'nextstepuni-app' });
const db = getFirestore();

// The junk key contains a dot, so it MUST be addressed with an explicit
// FieldPath — passing the string would be parsed as a path to
// pointsData → totalEarned and would never match the real (flat) key.
const junkPath = new FieldPath(JUNK_FIELD);

const run = async () => {
  console.log(`${APPLY ? 'APPLYING' : 'DRY RUN'} — scanning progress/* for the phantom "${JUNK_FIELD}" field\n`);

  const snap = await db.collection('progress').get();
  let scanned = 0;
  let affected = 0;
  let pointsRecovered = 0;
  const rows = [];

  for (const docSnap of snap.docs) {
    scanned++;
    const data = docSnap.data();
    // Flat key lookup — NOT data.pointsData.totalEarned.
    const junkValue = data[JUNK_FIELD];
    if (typeof junkValue !== 'number' || junkValue === 0) continue;

    const realValue = data?.pointsData?.totalEarned ?? 0;
    affected++;
    pointsRecovered += junkValue;
    rows.push({ uid: docSnap.id, lost: junkValue, was: realValue, becomes: realValue + junkValue });

    if (APPLY) {
      // TWO SEPARATE CALLS, DELIBERATELY.
      //
      // These cannot share one payload object. The real path and the junk key
      // are the SAME STRING, so `{ 'pointsData.totalEarned': increment(n),
      // [JUNK_FIELD]: FieldValue.delete() }` collapses to a single key — the
      // later delete silently wins, the increment never runs, and because
      // update() parses a dotted string as a field PATH it would delete the
      // student's REAL nested total. Every affected student would be zeroed,
      // while the script cheerfully reported "points recovered".
      //
      // Positional update(path, value) keeps the two unambiguous:
      //   - a dotted STRING is parsed as a path      -> pointsData.totalEarned
      //   - a FieldPath with one segment is literal   -> "pointsData.totalEarned"
      await docSnap.ref.update('pointsData.totalEarned', FieldValue.increment(junkValue));
      await docSnap.ref.update(junkPath, FieldValue.delete());
    }
  }

  console.table(rows.slice(0, 50));
  if (rows.length > 50) console.log(`…and ${rows.length - 50} more`);
  console.log(`\nScanned:          ${scanned} progress documents`);
  console.log(`Affected:         ${affected} students`);
  console.log(`Points recovered: ${pointsRecovered}`);
  if (!APPLY) console.log('\nNothing was written. Re-run with --apply to commit.');
};

run().then(() => process.exit(0)).catch(err => {
  console.error('Repair failed:', err);
  process.exit(1);
});
