/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { getAuth } from "firebase-admin/auth";
import { getFirestore, FieldValue } from "firebase-admin/firestore";
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

  const { email, password: supplied } = request.data as { email?: string; password?: string };
  const target = gcAddressToReset(email);
  if (!target) {
    throw new HttpsError(
      "invalid-argument",
      "This can only reset a guidance-counsellor login (gc-…@nextstep.app).",
    );
  }

  const auth = getAuth();
  let uid: string;
  try {
    uid = (await auth.getUserByEmail(target)).uid;
  } catch {
    throw new HttpsError("not-found", "No counsellor account exists for that school yet.");
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
  try {
    await auth.updateUser(uid, { password });
  } catch (err) {
    logger.error(`adminResetGcPassword: updateUser failed for ${target}`, err);
    throw new HttpsError("internal", "Could not set the new password.");
  }

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
  const schoolId = schoolIdFromGcAddress(target);
  if (schoolId) {
    const db = getFirestore();
    const userRef = db.collection("users").doc(uid);
    const existing = (await userRef.get()).data() || {};
    const patch: Record<string, unknown> = { role: "gc", school: schoolId };
    if (typeof existing.name !== "string" || existing.name.trim() === "") {
      patch.name = `${SCHOOL_NAMES[schoolId] ?? schoolId} Guidance`;
    }
    await userRef.set(patch, { merge: true });
    // Mirror into the signed token so firestore.rules' isSchoolStaff() resolves
    // from the claim rather than an extra document read on every request.
    await syncAuthorizationClaims(uid, { role: "gc", school: schoolId });
    logger.info(`adminResetGcPassword: provisioned ${target} as gc for "${schoolId}"`);
  }

  // Audit trail. Client-unreadable (default-deny covers this collection), and
  // deliberately records WHO/WHICH/WHEN but never the password.
  await getFirestore().collection("gcPasswordResets").add({
    targetEmail: target,
    targetUid: uid,
    resetBy: request.auth.uid,
    passwordGenerated: generated,
    resetAt: FieldValue.serverTimestamp(),
  }).catch(err => logger.error("adminResetGcPassword: audit write failed", err));

  logger.info(`adminResetGcPassword: reset ${target} by ${request.auth.uid} (${generated ? "generated" : "chosen"})`);
  return { success: true as const, email: target, password, generated };
});
