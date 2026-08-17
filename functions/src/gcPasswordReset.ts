/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { getAuth } from "firebase-admin/auth";
import { getFirestore, FieldValue } from "firebase-admin/firestore";
import type { UserRecord } from "firebase-admin/auth";
import { HttpsError, onCall } from "firebase-functions/v2/https";
import { logger } from "firebase-functions/v2";
import { randomInt } from "crypto";
import {
  MIN_SUPPLIED_PASSWORD_LENGTH,
  SCHOOL_NAMES,
  buildPassword,
  checkSuppliedPassword,
  gcAddressToReset,
  schoolIdFromGcAddress,
} from "./gcPasswordPolicy";
import { syncAuthorizationClaims } from "./authClaims";
import { isAdminEmail } from "./adminIdentity";

/**
 * adminResetGcPassword
 *
 * Set a new password for a guidance-counsellor login and return it once to the
 * administrator, who passes it to the school.
 *
 * Needed because GC logins live at derived addresses (gc-{schoolId}@nextstep.app)
 * whose mailboxes do not exist, so the console's emailed reset link goes
 * nowhere and the console has no way to set a password directly.
 *
 * The dangerous capability here is setting someone else's password, so the
 * limits are enforced server-side and repeated in ./gcPasswordPolicy:
 *
 *   • caller must be the administrator (functions/src/adminIdentity.ts)
 *   • target must be a gc-*@nextstep.app address — never a student, never a
 *     teacher, never the admin account itself
 *
 * Every reset is written to gcPasswordResets/{id}, which no client can read
 * (default-deny), so there is a record of who reset which login and when. The
 * password itself is never stored — only returned in the response.
 */
export const adminResetGcPassword = onCall({ cors: true }, async (request) => {
  if (!request.auth) {
    throw new HttpsError("unauthenticated", "Must be logged in.");
  }
  // The one caller allowed. Checked against the token, not a Firestore field,
  // so it cannot be granted by writing a document.
  if (!isAdminEmail(request.auth.token.email)) {
    throw new HttpsError("permission-denied", "Only the administrator can reset a counsellor login.");
  }

  const { email, password: supplied, adoptExisting } = request.data as {
    email?: string; password?: string; adoptExisting?: boolean;
  };
  const target = gcAddressToReset(email);
  if (!target) {
    throw new HttpsError(
      "invalid-argument",
      "This can only reset a guidance-counsellor login (gc-…@nextstep.app).",
    );
  }

  // The address pattern alone is not enough. gc-{anything}@nextstep.app matches
  // the regex, so without this a reset could provision role:'gc' for a school
  // that does not exist — or, worse, for an address an outsider had registered.
  const schoolId = schoolIdFromGcAddress(target);
  if (!schoolId || !(schoolId in SCHOOL_NAMES)) {
    throw new HttpsError("invalid-argument", "That is not one of this platform's schools.");
  }

  const auth = getAuth();
  const db = getFirestore();

  // ─── WHO ARE WE ABOUT TO HAND THIS SCHOOL TO? (security review 2026-08-17) ──
  //
  // This function used to adopt whatever Auth account happened to own the
  // address. Nothing reserves gc-*@nextstep.app server-side — isReservedEmail
  // is enforced only in LoginPage, and the public signUp endpoint accepts any
  // address — so an outsider could register the login for a school that had no
  // counsellor account yet (gc-pwc@nextstep.app was in exactly that state, with
  // a Reset button offered for it), wait, and be handed role:'gc' plus the whole
  // school's student records the moment the administrator clicked Reset. The
  // users-doc fallback in firestore.rules' isSchoolStaff() meant the grant took
  // effect on their EXISTING token, and resetStudentPassword authorises off that
  // same doc — so it escalated to taking over any student account in the school.
  //
  // So: only ever touch an account this platform owns. Either we create it now,
  // or gcAccounts/{schoolId} records that we provisioned it before. An account
  // that exists but is not on record is adopted ONLY when the administrator
  // confirms it explicitly, having been shown when it was created.
  const registryRef = db.collection("gcAccounts").doc(schoolId);
  const recordedUid = (await registryRef.get()).data()?.uid as string | undefined;

  // getUserByEmail throws when there is no such account; that is the
  // create-it-now case, not an error.
  const existing: UserRecord | null = await auth.getUserByEmail(target).catch(() => null);

  if (existing && recordedUid && existing.uid !== recordedUid) {
    // The address changed hands since we provisioned it. Never silently re-adopt.
    logger.error(`adminResetGcPassword: ${target} is now uid ${existing.uid}, expected ${recordedUid}`);
    throw new HttpsError(
      "failed-precondition",
      "This login is held by a different account than the one this platform created. "
        + "Do not reset it — check the Firebase console first.",
    );
  }

  if (existing && !recordedUid && !adoptExisting) {
    throw new HttpsError(
      "failed-precondition",
      `An account already exists for this login, created ${existing.metadata.creationTime}, `
        + "and this platform did not create it. Confirm you recognise it before adopting.",
    );
  }

  // The administrator may type a password (so it can be agreed with the school
  // in advance) or let one be generated. Validated HERE, not just in the
  // dashboard: a client-side check is a courtesy to the typist, never a
  // control. The password is never logged, on either path.
  let password: string;
  let generated: boolean;
  if (supplied === undefined || supplied === null) {
    password = buildPassword(randomInt);
    generated = true;
  } else {
    const check = checkSuppliedPassword(supplied);
    if (!check.ok) {
      throw new HttpsError(
        "invalid-argument",
        check.reason === "long"
          ? "That password is too long."
          : `Choose a password of at least ${MIN_SUPPLIED_PASSWORD_LENGTH} characters.`,
      );
    }
    password = check.password;
    generated = false;
  }
  let uid: string;
  try {
    if (existing) {
      uid = existing.uid;
      await auth.updateUser(uid, { password });
    } else {
      // No account yet — create it, so the platform owns this login from birth
      // rather than adopting whoever registered the address first.
      uid = (await auth.createUser({ email: target, password })).uid;
      logger.info(`adminResetGcPassword: created ${target}`);
    }
  } catch (err) {
    logger.error(`adminResetGcPassword: could not set the password for ${target}`, err);
    throw new HttpsError("internal", "Could not set the new password.");
  }

  // Terminate existing sessions (security review 2026-08-17).
  //
  // updateUser alone leaves already-issued ID tokens valid for the rest of
  // their ~1 hour life, and nothing here verifies tokens with checkRevoked. For
  // a SHARED per-school credential being rotated precisely because it may be
  // compromised, that hour is the whole point of the rotation — and it is the
  // window that made the adoption attack above practical. The dashboard tells
  // the administrator the old password stops working immediately; this is what
  // makes that true.
  await auth.revokeRefreshTokens(uid).catch(err =>
    logger.error(`adminResetGcPassword: revokeRefreshTokens failed for ${target}`, err));

  // Record the account as ours, so a later reset can tell if the address has
  // changed hands. Written before the role grant: if anything below fails we
  // still know which uid holds this login.
  await registryRef.set({
    uid,
    school: schoolId,
    email: target,
    provisionedBy: request.auth.uid,
    provisionedAt: FieldValue.serverTimestamp(),
  }, { merge: true });

  // Provision the counsellor's Firestore identity as well as their password.
  //
  // Creating the Auth account was never enough: AppRouter only routes to the
  // Staff Dashboard when users/{uid} carries BOTH role:'gc' and school, and
  // nothing ever seeded those docs. A counsellor who signed in was treated as
  // a student with no profile and dropped into student onboarding — which, if
  // they completed it, wrote a subjectProfile onto a staff account. It went
  // unnoticed because no counsellor had signed in since May 2026.
  //
  // Done here because resetting a login should hand back a login that WORKS.
  // Idempotent: merge:true re-affirms an already-correct doc rather than
  // disturbing it, and `name` is only set when there is nothing there, so a
  // counsellor who has set their own name keeps it. role and school are
  // client-immutable in the /users rules, so this is the only way they can be
  // written at all.
  {
    const userRef = db.collection("users").doc(uid);
    const existingDoc = (await userRef.get()).data() || {};
    const patch: Record<string, unknown> = { role: "gc", school: schoolId };
    if (typeof existingDoc.name !== "string" || existingDoc.name.trim() === "") {
      patch.name = `${SCHOOL_NAMES[schoolId]} Guidance`;
    }
    await userRef.set(patch, { merge: true });
    // Mirror into the signed token so firestore.rules' isSchoolStaff() resolves
    // from the claim rather than an extra document read on every request.
    await syncAuthorizationClaims(uid, { role: "gc", school: schoolId });
    logger.info(`adminResetGcPassword: provisioned ${target} as gc for "${schoolId}"`);
  }

  // Audit trail. Client-unreadable (default-deny covers this collection), and
  // deliberately records WHO/WHICH/WHEN but never the password.
  await db.collection("gcPasswordResets").add({
    targetEmail: target,
    targetUid: uid,
    resetBy: request.auth.uid,
    passwordGenerated: generated,
    resetAt: FieldValue.serverTimestamp(),
  }).catch(err => logger.error("adminResetGcPassword: audit write failed", err));

  logger.info(`adminResetGcPassword: reset ${target} by ${request.auth.uid} (${generated ? "generated" : "chosen"})`);
  return { success: true as const, email: target, password, generated };
});
