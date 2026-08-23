import { onCall, HttpsError } from "firebase-functions/v2/https";
import { logger } from "firebase-functions/v2";
import { getFirestore } from "firebase-admin/firestore";
import { isSupportedSchoolId } from "./schoolJoinPolicy";
import { hashAccessCode, safeHashEqual } from "./accessCodes";
import { CALLABLE_OPTIONS, assertUnrevokedAuth, isVerifiedAdminToken } from "./security";

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
 * Codes are high-entropy, rotatable values whose hashes live in the
 * client-unreadable studentAccessSecrets collection. The previous predictable
 * school-name codes are no longer accepted.
 */
export const claimStudentSchool = onCall(CALLABLE_OPTIONS, async (request) => {
  if (!request.auth) {
    throw new HttpsError("unauthenticated", "Must be logged in.");
  }
  // Registration binds the school before the client creates users/{uid}.
  await assertUnrevokedAuth(request.auth, true);

  const { school, code } = request.data as { school?: string; code?: string };
  if (!isSupportedSchoolId(school)) {
    throw new HttpsError("invalid-argument", "A valid school is required.");
  }
  if (!code || typeof code !== "string" || code.length < 10 || code.length > 64) {
    throw new HttpsError("invalid-argument", "A valid join code is required.");
  }

  const db = getFirestore();
  const uid = request.auth.uid;
  const userRef = db.collection("users").doc(uid);
  if (isVerifiedAdminToken(request.auth.token)) {
    throw new HttpsError("failed-precondition", "Staff accounts do not use a student join code.");
  }

  // Brute-force throttle (mirrors claimStaffAccess): even high-entropy codes
  // should have a bounded online verification surface. The attempt counter,
  // code check and school binding live in one transaction so parallel guesses
  // cannot all observe the same count and a code rotated mid-request cannot be
  // redeemed after rotation.
  const WINDOW_MS = 15 * 60 * 1000;
  const MAX_FAILURES = 6;
  const attemptsRef = db.collection("schoolClaimAttempts").doc(uid);
  const secretRef = db.collection("studentAccessSecrets").doc(school);
  const suppliedHash = hashAccessCode(code);
  const now = Date.now();
  const result = await db.runTransaction(async transaction => {
    const [userSnap, attemptSnap, secretSnap] = await Promise.all([
      transaction.get(userRef),
      transaction.get(attemptsRef),
      transaction.get(secretRef),
    ]);
    const existing = userSnap.data() || {};
    if (existing.accountDisabled === true) {
      throw new HttpsError("permission-denied", "This account is disabled.");
    }
    if (existing.role === "admin" || existing.role === "staff" || existing.role === "gc") {
      throw new HttpsError("failed-precondition", "Staff accounts do not use a student join code.");
    }

    // Already bound: idempotent if it is the same school, refuse a switch.
    if (typeof existing.school === "string" && existing.school.length > 0) {
      if (existing.school === school) return { kind: "joined" as const, alreadyJoined: true, failures: 0 };
      throw new HttpsError("failed-precondition", "Your account is already linked to a school.");
    }

    const attempt = attemptSnap.data() || {};
    let failCount = typeof attempt.count === "number" ? attempt.count : 0;
    let windowStart = typeof attempt.windowStart === "number" ? attempt.windowStart : now;
    if (now - windowStart > WINDOW_MS) { failCount = 0; windowStart = now; }
    if (failCount >= MAX_FAILURES) {
      throw new HttpsError("resource-exhausted", "Too many attempts. Please wait a few minutes and try again.");
    }

    const secret = secretSnap.data();
    if (typeof secret?.codeHash !== "string") return { kind: "unconfigured" as const, failures: failCount };
    if (!safeHashEqual(suppliedHash, secret.codeHash)) {
      const failures = failCount + 1;
      transaction.set(attemptsRef, {
        count: failures,
        windowStart,
        updatedAt: now,
        expiresAt: new Date(now + 48 * 60 * 60 * 1000),
      });
      return { kind: "invalid" as const, failures };
    }

    transaction.set(userRef, { school }, { merge: true });
    transaction.delete(attemptsRef);
    return { kind: "joined" as const, alreadyJoined: false, failures: 0 };
  });

  if (result.kind === "unconfigured") {
    throw new HttpsError(
      "failed-precondition",
      "Student access has not been set up for this school. Ask your guidance counsellor for a new join code.",
    );
  }
  if (result.kind === "invalid") {
    logger.info(`claimStudentSchool: bad code by ${uid} for "${school}" (${result.failures}/${MAX_FAILURES})`);
    throw new HttpsError("permission-denied", "That join code is not correct.");
  }

  // Student school is deliberately not copied into an ID-token claim. Rules
  // and callables resolve it from this live server-owned document, so a stale
  // token can never preserve an old tenant binding.
  logger.info(`claimStudentSchool: bound ${uid} to "${school}"`);
  return { success: true, alreadyJoined: result.alreadyJoined };
});
