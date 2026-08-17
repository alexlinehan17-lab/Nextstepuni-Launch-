import { onCall, HttpsError } from "firebase-functions/v2/https";
import { logger } from "firebase-functions/v2";
import { getFirestore } from "firebase-admin/firestore";
import { timingSafeEqual } from "crypto";
import { syncAuthorizationClaims } from "./authClaims";
import { SCHOOL_JOIN_CODES, normaliseJoinCode } from "./schoolJoinPolicy";

/**
 * Student school binding — the tenant-isolation trust anchor for students
 * (security review H-2, owner decision 2026-07-18).
 *
 * Previously a student typed any school name at registration and was placed in
 * that school's peer graph with no verification. School is now settable ONLY by
 * this function (running with the Admin SDK): the `/users` create rule forbids a
 * client-supplied `school`, and the update rule keeps it immutable, so a student
 * cannot self-assert or switch schools. They must present the correct per-school
 * join code, verified here, exactly mirroring the staff-code flow
 * (claimStaffAccess).
 *
 * INTERIM join-code scheme (owner decision 2026-07-18): the school's display
 * name + a sequential two-digit index by SCHOOLS order. These are low-entropy
 * and human-shareable on purpose; replace with per-school rotatable codes held
 * in gcSettings (+ App Check) before wide rollout — see security review L-7.
 */
// The codes and the matching rule live in ./schoolJoinPolicy so they can be
// unit-tested without pulling in firebase-admin. See that file for why the
// match ignores punctuation — three of the seven codes were unenterable on a
// phone keyboard until 2026-08-17.

/** Constant-time compare that never throws on length mismatch. */
function safeEqual(a: string, b: string): boolean {
  const ba = Buffer.from(a, "utf8");
  const bb = Buffer.from(b, "utf8");
  if (ba.length !== bb.length) return false;
  return timingSafeEqual(ba, bb);
}

export const claimStudentSchool = onCall({ cors: true }, async (request) => {
  if (!request.auth) {
    throw new HttpsError("unauthenticated", "Must be logged in.");
  }

  const { school, code } = request.data as { school?: string; code?: string };
  if (!school || typeof school !== "string" || !(school in SCHOOL_JOIN_CODES)) {
    throw new HttpsError("invalid-argument", "A valid school is required.");
  }
  if (!code || typeof code !== "string" || code.length > 64) {
    throw new HttpsError("invalid-argument", "A valid join code is required.");
  }

  const db = getFirestore();
  const uid = request.auth.uid;
  const userRef = db.collection("users").doc(uid);
  const existing = (await userRef.get()).data() || {};

  // Staff/admin never redeem a student join code.
  if (
    existing.role === "admin" || existing.role === "staff" || existing.role === "gc" ||
    request.auth.token.email === "admin@nextstep.app"
  ) {
    throw new HttpsError("failed-precondition", "Staff accounts do not use a student join code.");
  }

  // Already bound: idempotent if it's the same school, refuse a switch.
  if (typeof existing.school === "string" && existing.school.length > 0) {
    if (existing.school === school) {
      await syncAuthorizationClaims(uid, { school });
      return { success: true, alreadyJoined: true };
    }
    throw new HttpsError("failed-precondition", "Your account is already linked to a school.");
  }

  // Brute-force throttle (mirrors claimStaffAccess, L-7): the code is low-entropy,
  // so cap failed attempts per caller in a client-unreadable doc (default-deny
  // covers schoolClaimAttempts). Counts failures only; success clears it.
  const WINDOW_MS = 15 * 60 * 1000;
  const MAX_FAILURES = 6;
  const attemptsRef = db.collection("schoolClaimAttempts").doc(uid);
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

  const expected = SCHOOL_JOIN_CODES[school];
  if (!safeEqual(normaliseJoinCode(code), normaliseJoinCode(expected))) {
    await recordFailure();
    logger.info(`claimStudentSchool: bad code by ${uid} for "${school}" (${failCount + 1}/${MAX_FAILURES})`);
    throw new HttpsError("permission-denied", "That join code is not correct.");
  }

  // Bind the student to the school. `school` is written here (server-side)
  // because the /users rules forbid clients from writing it themselves.
  await userRef.set({ school }, { merge: true });
  await syncAuthorizationClaims(uid, { school });
  await attemptsRef.delete().catch(() => {});
  logger.info(`claimStudentSchool: bound ${uid} to "${school}"`);
  return { success: true };
});
