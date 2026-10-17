/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * ONE-OFF BACKFILL: year islands (schema 2 of /islandPublic/{uid}).
 *
 * The onProgressWritten / onUserWritten triggers keep each projection current
 * from the moment they deploy, but only when a student's island or profile
 * next changes. This script brings every existing account into line at once:
 *   - writes a schema 2 projection for every student who should have one
 *     (school + year group + a current island + sharing not switched off)
 *   - replaces every schema 1 (legacy, whole-school) projection
 *   - deletes every projection that should not exist (staff, disabled,
 *     graduated, hidden, no year, no current island)
 * It runs the SAME code as the triggers (functions/lib/islandProjectionSync.js),
 * so there is no second copy of the projection rules to drift. Idempotent: a
 * second run reports everything "unchanged" or "absent".
 *
 * ORDER: deploy firestore rules + indexes and the functions FIRST, then run
 * this. Running it before the triggers are live lets projections go stale
 * behind you.
 *
 * USAGE (from the repo root)
 *   npm --prefix functions ci && npm --prefix functions run build
 *
 *   Dry run, reads only (default; prints counts, writes nothing):
 *     GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json \
 *       node scripts/backfill-year-islands.mjs
 *
 *   Apply to production (both flags required):
 *     GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json \
 *       node scripts/backfill-year-islands.mjs --apply --allow-production
 *
 *   Emulator:
 *     FIRESTORE_EMULATOR_HOST=127.0.0.1:8080 node scripts/backfill-year-islands.mjs --apply
 *
 * Output is counts only, never names; --verbose adds one line per account
 * (uid and outcome) for debugging.
 */
import { createRequire } from 'node:module';
import { existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const args = process.argv.slice(2);
const APPLY = args.includes('--apply');
const ALLOW_PRODUCTION = args.includes('--allow-production');
const VERBOSE = args.includes('--verbose');
const EMULATOR = Boolean(process.env.FIRESTORE_EMULATOR_HOST);
const PROJECT = process.env.GCLOUD_PROJECT ?? 'nextstepuni-app';
const PAGE = 300;
const CONCURRENCY = 5;

// firebase-admin and the compiled projection live with the functions package.
const functionsPackage = fileURLToPath(new URL('../functions/package.json', import.meta.url));
const require = createRequire(functionsPackage);
const compiled = fileURLToPath(new URL('../functions/lib/islandProjectionSync.js', import.meta.url));
if (!existsSync(compiled)) {
  console.error('functions/lib is missing. Run: npm --prefix functions run build');
  process.exit(2);
}
const { initializeApp, applicationDefault } = require('firebase-admin/app');
const { getFirestore, FieldPath } = require('firebase-admin/firestore');
const { syncYearIsland } = require(compiled);

if (APPLY && !EMULATOR && !ALLOW_PRODUCTION) {
  console.error('REFUSED: --apply against production needs --allow-production as well.');
  console.error('Use FIRESTORE_EMULATOR_HOST for a rehearsal, or a dry run (no flags) to see the counts.');
  process.exit(2);
}

initializeApp(EMULATOR ? { projectId: PROJECT } : { credential: applicationDefault(), projectId: PROJECT });
const db = getFirestore();

/** Every document id in a collection, a page at a time, without reading fields. */
async function ids(collection) {
  const found = [];
  let last = null;
  for (;;) {
    let page = db.collection(collection).select().orderBy(FieldPath.documentId()).limit(PAGE);
    if (last) page = page.startAfter(last);
    const snapshot = await page.get();
    for (const doc of snapshot.docs) found.push(doc.id);
    if (snapshot.size < PAGE) return found;
    last = snapshot.docs[snapshot.docs.length - 1];
  }
}

console.log('== backfill-year-islands ==');
console.log(`  mode:     ${APPLY ? 'APPLY' : 'dry run (no writes)'}`);
console.log(`  target:   ${EMULATOR ? `emulator ${process.env.FIRESTORE_EMULATOR_HOST}` : `production ${PROJECT}`}`);

// A projection can exist without progress (an orphan), so cover both sets.
const uids = [...new Set([...(await ids('progress')), ...(await ids('islandPublic'))])];
console.log(`  accounts: ${uids.length}\n`);

const outcomes = new Map();
const excluded = new Map();
let errors = 0;
const bump = (map, key) => map.set(key, (map.get(key) ?? 0) + 1);

let next = 0;
await Promise.all(Array.from({ length: CONCURRENCY }, async () => {
  while (next < uids.length) {
    const uid = uids[next++];
    try {
      const outcome = await syncYearIsland(db, uid, { dryRun: !APPLY });
      bump(outcomes, outcome.action);
      if (outcome.excluded) bump(excluded, outcome.excluded);
      if (VERBOSE) console.log(`  ${uid}  ${outcome.action}${outcome.excluded ? ` (${outcome.excluded})` : ''}`);
    } catch (err) {
      errors++;
      console.error(`  error for ${uid}:`, err?.message ?? err);
    }
  }
}));

const verb = APPLY ? '' : 'would be ';
console.log('== summary ==');
console.log(`  ${verb}written:   ${outcomes.get('written') ?? 0}`);
console.log(`  unchanged:      ${outcomes.get('unchanged') ?? 0}`);
console.log(`  ${verb}deleted:   ${outcomes.get('deleted') ?? 0}`);
console.log(`  no projection:  ${outcomes.get('absent') ?? 0}`);
console.log(`  errors:         ${errors}`);
if (excluded.size) {
  console.log('  why no projection (deleted + none):');
  for (const [reason, count] of [...excluded].sort()) console.log(`    ${reason}: ${count}`);
}
if (!APPLY) console.log('\nDry run only. Re-run with --apply --allow-production to write.');
process.exit(errors ? 1 : 0);
