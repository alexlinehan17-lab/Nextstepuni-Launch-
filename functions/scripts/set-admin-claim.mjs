/**
 * One-time administrator claim bootstrap using Application Default
 * Credentials / Workload Identity. No service-account JSON or password is
 * accepted by this tool.
 *
 * Usage from functions/: npm run provision:admin -- <expected-auth-uid>
 */
import { applicationDefault, initializeApp } from 'firebase-admin/app';
import { getAuth } from 'firebase-admin/auth';
import { getFirestore } from 'firebase-admin/firestore';
import process from 'node:process';

const ADMIN_EMAIL = 'nextstepuniinfo@gmail.com';
const expectedUid = process.argv[2];
if (!expectedUid || !/^[A-Za-z0-9:_-]{6,128}$/.test(expectedUid)) {
  process.stderr.write('Usage: npm run provision:admin -- <expected-auth-uid>\n');
  process.exit(1);
}

initializeApp({ credential: applicationDefault() });
const auth = getAuth();
const user = await auth.getUserByEmail(ADMIN_EMAIL);
if (user.uid !== expectedUid) {
  process.stderr.write(`Refusing: ${ADMIN_EMAIL} belongs to ${user.uid}, not the confirmed uid.\n`);
  process.exit(1);
}
if (!user.emailVerified) {
  process.stderr.write(`Refusing: Firebase has not verified ${ADMIN_EMAIL}.\n`);
  process.exit(1);
}

await auth.setCustomUserClaims(user.uid, { ...(user.customClaims || {}), admin: true });
await getFirestore().collection('users').doc(user.uid).set({
  name: user.displayName || 'Admin',
  avatar: 'Charlie',
  role: 'admin',
  isAdmin: true,
  accountDisabled: false,
  sessionValidAfterSeconds: Math.floor(Date.now() / 1000),
}, { merge: true });
await auth.revokeRefreshTokens(user.uid);
process.stdout.write(`Admin claim set for verified account ${ADMIN_EMAIL} (${user.uid}). Sign in again.\n`);
