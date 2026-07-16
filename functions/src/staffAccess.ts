import { onCall, HttpsError } from "firebase-functions/v2/https";
import { logger } from "firebase-functions/v2";
import { getFirestore } from "firebase-admin/firestore";
import { timingSafeEqual } from "crypto";

/**
 * Staff-access provisioning — the trust anchor for the Staff Dashboard.
 *
 * A teacher redeems their school's staff code to gain `role: 'staff'` (full
 * guidance-counsellor parity — owner decision 2026-07-16, see
 * compliance/STAFF_DASHBOARD_PLAN.md). Verification happens SERVER-SIDE: the
 * code lives in gcSettings/{school}.staffCode (GC-writable, student-unreadable),
 * and only this function — running with the Admin SDK — can both read the code
 * AND set the `role` field (which the Firestore /users update rule makes
 * client-immutable). So a client can never self-assign 'staff'.
 *
 * The code is a shared secret the GC distributes and can rotate at will
 * (rewriting gcSettings.staffCode from the dashboard). Because it is
 * brute-forceable in principle, the code is generated with high entropy and
 * this function should be paired with per-caller rate-limiting / App Check
 * before wide rollout (security review 2026-07-16, L-7).
 */

/** Constant-time string compare that never throws on length mismatch. */
function safeEqual(a: string, b: string): boolean {
  const ba = Buffer.from(a, "utf8");
  const bb = Buffer.from(b, "utf8");
  if (ba.length !== bb.length) return false;
  return timingSafeEqual(ba, bb);
}

export const claimStaffAccess = onCall({ cors: true }, async (request) => {
  if (!request.auth) {
    throw new HttpsError("unauthenticated", "Must be logged in.");
  }

  const { school, code } = request.data as { school?: string; code?: string };
  if (!school || typeof school !== "string" || school.length > 50) {
    throw new HttpsError("invalid-argument", "A valid school is required.");
  }
  if (!code || typeof code !== "string" || code.length < 6 || code.length > 64) {
    throw new HttpsError("invalid-argument", "A valid staff code is required.");
  }

  const db = getFirestore();
  const uid = request.auth.uid;

  // Never downgrade or re-role an existing staff/admin account.
  const userRef = db.collection("users").doc(uid);
  const userSnap = await userRef.get();
  const existingRole = userSnap.data()?.role;
  if (existingRole === "admin" || request.auth.token.email === "admin@nextstep.app") {
    throw new HttpsError("failed-precondition", "Admin accounts do not redeem staff codes.");
  }
  if (existingRole === "gc" || existingRole === "staff") {
    // Already staff — treat as success (idempotent), but keep their school.
    return { success: true, alreadyStaff: true };
  }

  // Brute-force throttle (security review 2026-07-16, L-7): the staff code is a
  // guessable shared secret and a correct guess grants full access to minors'
  // data, so cap failed attempts per caller. Server-side state in a
  // client-unreadable doc (default-deny covers staffClaimAttempts). Counts only
  // failures; a success clears the record.
  const WINDOW_MS = 15 * 60 * 1000;
  const MAX_FAILURES = 6;
  const attemptsRef = db.collection("staffClaimAttempts").doc(uid);
  const now = Date.now();
  const attempt = (await attemptsRef.get()).data() || {};
  let failCount = typeof attempt.count === "number" ? attempt.count : 0;
  let windowStart = typeof attempt.windowStart === "number" ? attempt.windowStart : now;
  if (now - windowStart > WINDOW_MS) { failCount = 0; windowStart = now; }
  if (failCount >= MAX_FAILURES) {
    throw new HttpsError("resource-exhausted", "Too many attempts. Please wait a few minutes and try again.");
  }

  const recordFailure = async () => {
    await attemptsRef.set({ count: failCount + 1, windowStart, updatedAt: now }).catch(() => {});
  };

  // Read the school's staff code (Admin SDK bypasses the student-deny rule).
  const settingsSnap = await db.collection("gcSettings").doc(school).get();
  const staffCode = settingsSnap.exists ? (settingsSnap.data()?.staffCode as string | undefined) : undefined;
  if (!staffCode || typeof staffCode !== "string") {
    await recordFailure();
    throw new HttpsError("permission-denied", "No staff access is set up for this school. Ask your school's counsellor to generate a code.");
  }

  if (!safeEqual(code.trim(), staffCode.trim())) {
    await recordFailure();
    logger.info(`claimStaffAccess: bad code attempt by ${uid} for school "${school}" (${failCount + 1}/${MAX_FAILURES})`);
    throw new HttpsError("permission-denied", "That staff code is not correct.");
  }

  // Grant staff. role is set here (server-side) because the /users rule forbids
  // clients from writing role themselves. Clear the throttle record on success.
  await userRef.set({ role: "staff", school }, { merge: true });
  await attemptsRef.delete().catch(() => {});
  logger.info(`claimStaffAccess: granted staff to ${uid} for school "${school}"`);
  return { success: true };
});
