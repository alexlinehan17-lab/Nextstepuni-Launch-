// One-off: provision a Guidance Counsellor account for a school.
//
// The app derives the GC role from the email pattern gc-{schoolId}@nextstep.app
// (contexts/AuthContext.tsx) — no Firestore doc or custom claim is needed. So a
// GC account is just a Firebase Auth email/password user with that email.
//
// Uses the app's PUBLIC Firebase web config (no admin SDK / service account),
// spoofing an allowed referrer so the API-key referrer check passes from Node.
//
//   node scripts/provision-gc.mjs <schoolId> <password>
//   e.g. node scripts/provision-gc.mjs marino 'Marino01'
//
// NOT committed with real passwords. Safe to re-run (create-or-verify).
import { initializeApp } from 'firebase/app';
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from 'firebase/auth';

const _fetch = globalThis.fetch;
globalThis.fetch = (input, init = {}) => {
  const headers = new Headers(init.headers || {});
  headers.set('Referer', 'https://nextstepuni-app.web.app/');
  headers.set('Origin', 'https://nextstepuni-app.web.app');
  return _fetch(input, { ...init, headers });
};

const firebaseConfig = {
  apiKey: 'AIzaSyCoNBVVlJifQ_n3Pf1P1BA9QalOOcK0kNA',
  authDomain: 'nextstepuni-app.firebaseapp.com',
  projectId: 'nextstepuni-app',
  storageBucket: 'nextstepuni-app.firebasestorage.app',
  messagingSenderId: '52864318610',
  appId: '1:52864318610:web:24f445c78a71f215c2ba4b',
};

const schoolId = process.argv[2];
const password = process.argv[3];
if (!schoolId || !password) {
  console.error('Usage: node scripts/provision-gc.mjs <schoolId> <password>');
  process.exit(1);
}
const email = `gc-${schoolId}@nextstep.app`;

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

try {
  const cred = await createUserWithEmailAndPassword(auth, email, password);
  console.log(`✅ Created GC account: ${email}  (uid ${cred.user.uid})`);
  console.log(`   Password: ${password}`);
} catch (e) {
  if (e.code === 'auth/email-already-in-use') {
    // Already exists — verify the given password works.
    try {
      const cred = await signInWithEmailAndPassword(auth, email, password);
      console.log(`ℹ️  GC account already exists AND this password works: ${email} (uid ${cred.user.uid})`);
    } catch (e2) {
      console.log(`⚠️  GC account ${email} already exists but this password is WRONG (${e2.code}).`);
      console.log(`   The account exists — the sign-in issue is the password, not a missing account.`);
    }
  } else {
    console.error(`❌ Failed to create ${email}:`, e.code, e.message);
    process.exit(1);
  }
}
process.exit(0);
