import { onCall, HttpsError } from "firebase-functions/v2/https";
import { onDocumentWritten } from "firebase-functions/v2/firestore";
import { logger } from "firebase-functions/v2";
import { initializeApp } from "firebase-admin/app";
import { getAuth } from "firebase-admin/auth";
import { getFirestore, FieldValue } from "firebase-admin/firestore";
import { createHash, randomInt } from "crypto";
import { buildPublicProjection } from "./islandProjection";
import { clearAuthorizationClaims, syncAuthorizationClaims } from "./authClaims";
import { CALLABLE_OPTIONS, assertSensitiveAuth, authTimeSeconds } from "./security";
import {
  RESET_LIFETIME_SECONDS,
  hashTemporaryPassword,
  resetSessionIsEligible,
  validateNewPassword,
} from "./passwordResetPolicy";

initializeApp();

// GDPR Article 15 (export) + Article 17 (erasure) — see ./dataRights.ts.
// Handlers call getFirestore()/getAuth() lazily, so they run after the
// initializeApp() above despite the import being hoisted.
export { requestAccountDeletion, exportMyData, retryFailedAccountDeletions } from "./dataRights";
// Staff-access provisioning (Staff Dashboard) — see ./staffAccess.ts.
export { claimStaffAccess } from "./staffAccess";
// Student school binding (verified join code) — see ./schoolAccess.ts.
export { claimStudentSchool } from "./schoolAccess";
// Anonymous product feedback — see ./anonymousFeedback.ts.
export { submitAnonymousFeedback } from "./anonymousFeedback";
// Admin-only reset for the derived gc-{school}@nextstep.app logins, whose
// mailboxes do not exist so the console's emailed reset goes nowhere.
export { adminResetGcPassword } from "./gcPasswordReset";
// The only path by which staff can put a notification in front of a student —
// firestore.rules denies direct staff writes. See ./staffMessagePolicy.
export { sendStaffNotification } from "./staffMessage";
export { sendKudos, sendGift, placeGift } from "./peerInteractions";
export {
  getSchoolAccessStatus,
  rotateStaffAccessCode,
  rotateStudentJoinCode,
  listStaffAccess,
  revokeStaffAccess,
} from "./staffAccess";
export {
  submitChairCohort,
  submitChairDecisions,
  submitChairDaily,
  recordFocusPresence,
} from "./aggregateCounters";

/**
 * resetStudentPassword
 *
 * Called by a Guidance Counsellor from the GC Dashboard.
 * Verifies the caller is a GC for the student's school,
 * then resets the student's password to a temporary value
 * and returns it for the GC to share with the student.
 */
export const resetStudentPassword = onCall(
  CALLABLE_OPTIONS,
  async (request) => {
    // Require authentication
    if (!request.auth) {
      throw new HttpsError("unauthenticated", "Must be logged in.");
    }

    const { studentUid } = request.data as { studentUid?: string };
    if (!studentUid || typeof studentUid !== "string") {
      throw new HttpsError("invalid-argument", "studentUid is required.");
    }

    const db = getFirestore();
    const auth = getAuth();

    // Password resets are account-takeover capabilities. Require a fresh,
    // unrevoked GC session in addition to the current server-side role doc.
    await assertSensitiveAuth(request.auth);

    // Verify caller is a GC
    const callerDoc = await db.collection("users").doc(request.auth.uid).get();
    if (!callerDoc.exists) {
      throw new HttpsError("permission-denied", "Caller not found.");
    }
    const callerData = callerDoc.data()!;
    if (callerData.role !== "gc") {
      throw new HttpsError("permission-denied", "Only guidance counsellors can reset passwords.");
    }

    // Verify student exists and is in the same school
    const studentDoc = await db.collection("users").doc(studentUid).get();
    if (!studentDoc.exists) {
      throw new HttpsError("not-found", "Student not found.");
    }
    const studentData = studentDoc.data()!;
    if (studentData.school !== callerData.school) {
      throw new HttpsError("permission-denied", "Student is not in your school.");
    }
    // A GC may only reset *student* accounts — never another GC or an admin.
    // Without this a GC could pass a colleague-GC/admin uid (same school) and
    // take over that staff account. (Security review 2026-07-16, HIGH.)
    if (studentData.role === "gc" || studentData.role === "admin" || studentData.isAdmin === true) {
      throw new HttpsError("permission-denied", "You can only reset student accounts.");
    }

    // Generate a high-entropy temporary password, easy to read aloud.
    // randomInt() is a CSPRNG (crypto), not Math.random(), so the temp
    // credential isn't predictable. (Security review 2026-07-16, LOW.)
    const chars = "abcdefghjkmnpqrstuvwxyz23456789"; // no i/l/o/0/1 to avoid confusion
    let tempPassword = "";
    for (let i = 0; i < 16; i++) {
      tempPassword += chars.charAt(randomInt(chars.length));
    }

    const resetAtSeconds = Math.floor(Date.now() / 1000);
    const resetExpiresAtSeconds = resetAtSeconds + RESET_LIFETIME_SECONDS;

    // Flag first: a token issued for the old password still cannot use the
    // password-change callable because its auth_time predates resetAtSeconds.
    try {
      await db.collection("users").doc(studentUid).update({
        needsPasswordChange: true,
        passwordResetAtSeconds: resetAtSeconds,
        passwordResetExpiresAtSeconds: resetExpiresAtSeconds,
        temporaryPasswordHash: hashTemporaryPassword(tempPassword),
        passwordResetBy: request.auth.uid,
        // Firestore rules consult this cutoff on every user-scoped request.
        // Existing ID tokens therefore stop working immediately, rather than
        // remaining useful until their normal one-hour expiry.
        sessionValidAfterSeconds: resetAtSeconds,
      });
      await auth.updateUser(studentUid, { password: tempPassword });
      await auth.revokeRefreshTokens(studentUid);
      await db.collection("passwordResetAudit").add({
        studentRef: createHash("sha256").update(studentUid).digest("hex").slice(0, 20),
        school: callerData.school,
        resetBy: request.auth.uid,
        resetAt: FieldValue.serverTimestamp(),
        expiresAtSeconds: resetExpiresAtSeconds,
      });
    } catch (err) {
      console.error('Failed to reset password:', err);
      throw new HttpsError("internal", "Failed to reset password.");
    }

    return { tempPassword, studentName: studentData.name };
  }
);

/**
 * changeOwnPassword
 *
 * Called by a student who has been flagged with needsPasswordChange.
 * Uses Admin SDK to bypass the requires-recent-login restriction.
 */
export const changeOwnPassword = onCall(
  CALLABLE_OPTIONS,
  async (request) => {
    if (!request.auth) {
      throw new HttpsError("unauthenticated", "Must be logged in.");
    }

    const { newPassword } = request.data as { newPassword?: string };
    const passwordError = validateNewPassword(newPassword);
    if (passwordError) {
      throw new HttpsError("invalid-argument", passwordError);
    }

    const db = getFirestore();
    const auth = getAuth();
    const uid = request.auth.uid;

    // Verify the user actually needs a password change
    const userDoc = await db.collection("users").doc(uid).get();
    const reset = userDoc.data();
    if (!userDoc.exists || !reset?.needsPasswordChange) {
      throw new HttpsError("failed-precondition", "No password change required.");
    }

    await assertSensitiveAuth(request.auth);
    const nowSeconds = Math.floor(Date.now() / 1000);
    const currentAuthTime = authTimeSeconds(request.auth);
    if (!resetSessionIsEligible(
      reset.passwordResetAtSeconds,
      reset.passwordResetExpiresAtSeconds,
      currentAuthTime,
      nowSeconds,
    )) {
      throw new HttpsError(
        "failed-precondition",
        "This temporary password has expired or was not used for this sign-in. Ask your guidance counsellor for a new reset.",
      );
    }
    if (hashTemporaryPassword(newPassword as string) === reset.temporaryPasswordHash) {
      throw new HttpsError("invalid-argument", "Choose a password different from the temporary password.");
    }

    try {
      await auth.updateUser(uid, { password: newPassword as string });
      await db.collection("users").doc(uid).update({
        needsPasswordChange: false,
        passwordResetAtSeconds: FieldValue.delete(),
        passwordResetExpiresAtSeconds: FieldValue.delete(),
        temporaryPasswordHash: FieldValue.delete(),
        passwordResetBy: FieldValue.delete(),
        // Strict `auth_time > cutoff` in Firestore rejects this temporary
        // session. A subsequent sign-in with the chosen password is newer.
        sessionValidAfterSeconds: currentAuthTime,
      });
      // End every temporary-password session, including this one. The client
      // signs out and asks the student to sign in with their chosen password.
      await auth.revokeRefreshTokens(uid);
    } catch (err) {
      console.error('Failed to change password:', err);
      throw new HttpsError("internal", "Failed to change password.");
    }

    return { success: true };
  }
);

/**
 * Complete a Firebase email-link password reset after the client signs in with
 * the new password. The standard Auth reset revokes refresh tokens, but
 * Firestore otherwise has no way to reject an already-issued ID token until it
 * expires. Advancing the user-doc cutoff closes that window immediately.
 */
export const finalizeSelfServicePasswordReset = onCall(
  CALLABLE_OPTIONS,
  async (request) => {
    if (!request.auth) throw new HttpsError("unauthenticated", "Must be logged in.");
    await assertSensitiveAuth(request.auth);
    const db = getFirestore();
    const auth = getAuth();
    const userRef = db.collection("users").doc(request.auth.uid);
    if ((await userRef.get()).exists) {
      await userRef.update({
        // End this one-use finalisation session too. Firestore uses a strict
        // `auth_time > cutoff` check, so setting the exact sign-in time also
        // closes the edge case where an older token was issued in the same
        // second as the reset. The client signs out immediately after this
        // callable returns.
        sessionValidAfterSeconds: authTimeSeconds(request.auth),
        needsPasswordChange: false,
        passwordResetAtSeconds: FieldValue.delete(),
        passwordResetExpiresAtSeconds: FieldValue.delete(),
        temporaryPasswordHash: FieldValue.delete(),
        passwordResetBy: FieldValue.delete(),
      });
    }
    await auth.revokeRefreshTokens(request.auth.uid);
    return { success: true as const };
  },
);

/**
 * onProgressWritten
 *
 * Maintains /islandPublic/{uid} as a minimal public projection of a
 * student's island state. Triggered on any write to /progress/{uid}.
 *
 * The projection contains only what other students at the same school
 * see in the Peer Island feature — no academic data, no behavioural
 * timestamps. See compliance/PEER_ISLAND_REFACTOR_PLAN.md and
 * functions/src/islandProjection.ts for the field rationale.
 *
 * Behaviour:
 *   - If progress was deleted: delete the projection.
 *   - If progress exists but is for staff or has no island: delete any
 *     existing projection.
 *   - Otherwise: write/refresh the projection, joining identity fields
 *     from /users/{uid}.
 */
export const onProgressWritten = onDocumentWritten(
  "progress/{uid}",
  async (event) => {
    const uid = event.params.uid;
    const db = getFirestore();
    const islandPublicRef = db.collection("islandPublic").doc(uid);

    const progressData = event.data?.after?.data();
    if (!progressData) {
      await islandPublicRef.delete().catch((err) => {
        logger.warn(`onProgressWritten: failed to delete projection for ${uid}`, err);
      });
      return;
    }

    const userSnap = await db.collection("users").doc(uid).get();
    if (!userSnap.exists) {
      logger.warn(`onProgressWritten: user ${uid} not found; deleting any projection`);
      await islandPublicRef.delete().catch(() => {});
      return;
    }

    const projection = buildPublicProjection(userSnap.data(), progressData);
    if (!projection) {
      // Staff account, no island state, or no category — ensure no projection exists.
      await islandPublicRef.delete().catch(() => {});
      return;
    }

    await islandPublicRef.set({
      ...projection,
      updatedAt: FieldValue.serverTimestamp(),
    });
  }
);

/**
 * onUserWritten
 *
 * Refreshes /islandPublic/{uid} when identity fields (name, avatar,
 * school) or role change on /users/{uid}. Also handles the cases where
 * a user is deleted or becomes staff (projection is deleted).
 *
 * Does NOT create a projection from scratch — that requires progress
 * data. If no projection exists when this trigger fires, it does
 * nothing; the progress trigger will create one when relevant data
 * arrives.
 */
export const onUserWritten = onDocumentWritten(
  "users/{uid}",
  async (event) => {
    const uid = event.params.uid;
    const db = getFirestore();
    const islandPublicRef = db.collection("islandPublic").doc(uid);

    const beforeData = event.data?.before?.data();
    const userData = event.data?.after?.data();
    if (!userData) {
      await islandPublicRef.delete().catch(() => {});
      await clearAuthorizationClaims(uid).catch((err) => {
        // Account deletion may already have removed the Auth user.
        if ((err as { code?: string }).code !== "auth/user-not-found") {
          logger.error(`onUserWritten: failed to clear authorization claims for ${uid}`, err);
        }
      });
      await getAuth().revokeRefreshTokens(uid).catch(() => {});
      return;
    }

    const wasPrivileged = beforeData?.role === "gc" || beforeData?.role === "staff";
    const authorizationChanged = !beforeData
      || beforeData.role !== userData.role
      || beforeData.school !== userData.school
      || beforeData.accountDisabled !== userData.accountDisabled;
    if (authorizationChanged) {
      await syncAuthorizationClaims(uid, userData).catch((err) => {
        logger.error(`onUserWritten: failed to sync authorization claims for ${uid}`, err);
      });
      // Revoke on demotion, school transfer or disablement. A first promotion
      // does not need revocation (rules already require the document) and
      // revoking it would race the newly promoted client's first token refresh.
      if (wasPrivileged || userData.accountDisabled === true) {
        await getAuth().revokeRefreshTokens(uid).catch((err) => {
          logger.error(`onUserWritten: failed to revoke stale sessions for ${uid}`, err);
        });
      }
    }

    if (userData.role === "gc" || userData.role === "staff" || userData.role === "admin" || userData.isAdmin === true) {
      await islandPublicRef.delete().catch(() => {});
      return;
    }

    const islandPublicSnap = await islandPublicRef.get();
    if (!islandPublicSnap.exists) {
      // No projection to refresh; the progress trigger will create one
      // if/when an island appears. Avoid creating an empty/stub doc.
      return;
    }

    const progressSnap = await db.collection("progress").doc(uid).get();
    if (!progressSnap.exists) {
      // Existing projection but progress now missing — refresh identity
      // fields only. (Edge case: progress was deleted out-of-band.)
      const first = typeof userData.name === "string" && userData.name.trim()
        ? userData.name.trim().split(/\s+/)[0] : "Student";
      await islandPublicRef.update({
        name: first,
        avatar: typeof userData.avatar === "string" ? userData.avatar : "James",
        school: typeof userData.school === "string" ? userData.school : "",
        updatedAt: FieldValue.serverTimestamp(),
      });
      return;
    }

    const projection = buildPublicProjection(userData, progressSnap.data());
    if (!projection) {
      await islandPublicRef.delete().catch(() => {});
      return;
    }

    await islandPublicRef.set({
      ...projection,
      updatedAt: FieldValue.serverTimestamp(),
    });
  }
);
