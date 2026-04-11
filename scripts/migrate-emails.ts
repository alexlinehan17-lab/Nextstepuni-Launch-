/**
 * One-time migration: rename Firebase Auth emails from
 *   {username}@nextstep.app  →  {username}-{schoolId}@nextstep.app
 *
 * Usage:
 *   npx ts-node scripts/migrate-emails.ts
 *
 * Requires: firebase-admin credentials (set GOOGLE_APPLICATION_CREDENTIALS
 * environment variable pointing to your service account JSON).
 *
 * DRY RUN by default — set DRY_RUN=false to actually update.
 */

import { initializeApp, cert } from 'firebase-admin/app';
import { getAuth } from 'firebase-admin/auth';
import { getFirestore } from 'firebase-admin/firestore';

const DRY_RUN = process.env.DRY_RUN !== 'false';

async function main() {
  initializeApp();
  const auth = getAuth();
  const db = getFirestore();

  console.log(`Mode: ${DRY_RUN ? 'DRY RUN (no changes)' : 'LIVE — will update emails'}`);

  // List all users
  let nextPageToken: string | undefined;
  let total = 0;
  let migrated = 0;
  let skipped = 0;
  let errors = 0;

  do {
    const result = await auth.listUsers(1000, nextPageToken);
    for (const user of result.users) {
      total++;
      const email = user.email;
      if (!email || !email.endsWith('@nextstep.app')) {
        skipped++;
        continue;
      }

      // Skip GC and admin accounts
      if (email.startsWith('gc-') || email === 'admin@nextstep.app') {
        skipped++;
        continue;
      }

      // Check if already migrated (has a hyphen before @nextstep.app that matches a school ID)
      const localPart = email.split('@')[0];
      if (localPart.includes('-')) {
        // Might already be migrated — check Firestore
        const userDoc = await db.collection('users').doc(user.uid).get();
        if (userDoc.exists && userDoc.data()?.school) {
          const school = userDoc.data()!.school;
          if (localPart.endsWith(`-${school}`)) {
            skipped++;
            continue; // Already migrated
          }
        }
      }

      // Look up school from Firestore user doc
      const userDoc = await db.collection('users').doc(user.uid).get();
      if (!userDoc.exists) {
        console.log(`  SKIP ${email} — no Firestore user doc`);
        skipped++;
        continue;
      }

      const school = userDoc.data()?.school;
      if (!school) {
        console.log(`  SKIP ${email} — no school field`);
        skipped++;
        continue;
      }

      const newEmail = `${localPart}-${school}@nextstep.app`;
      console.log(`  ${DRY_RUN ? 'WOULD RENAME' : 'RENAMING'}: ${email} → ${newEmail}`);

      if (!DRY_RUN) {
        try {
          await auth.updateUser(user.uid, { email: newEmail });
          migrated++;
        } catch (err) {
          console.error(`  ERROR updating ${email}:`, err);
          errors++;
        }
      } else {
        migrated++;
      }
    }
    nextPageToken = result.pageToken;
  } while (nextPageToken);

  console.log(`\nDone. Total: ${total}, Migrated: ${migrated}, Skipped: ${skipped}, Errors: ${errors}`);
  if (DRY_RUN) console.log('This was a DRY RUN. Set DRY_RUN=false to apply changes.');
}

main().catch(console.error);
