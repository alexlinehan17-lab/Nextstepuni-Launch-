/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { getAuth } from "firebase-admin/auth";
import { getFirestore, FieldValue } from "firebase-admin/firestore";
import { HttpsError, onCall } from "firebase-functions/v2/https";
import { logger } from "firebase-functions/v2";
import { randomInt } from "crypto";
import { buildPassword, gcAddressToReset } from "./gcPasswordPolicy";

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
 *   • caller must be admin@nextstep.app
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
  if (request.auth.token.email !== "admin@nextstep.app") {
    throw new HttpsError("permission-denied", "Only the administrator can reset a counsellor login.");
  }

  const { email } = request.data as { email?: string };
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

  const password = buildPassword(randomInt);
  try {
    await auth.updateUser(uid, { password });
  } catch (err) {
    logger.error(`adminResetGcPassword: updateUser failed for ${target}`, err);
    throw new HttpsError("internal", "Could not set the new password.");
  }

  // Audit trail. Client-unreadable (default-deny covers this collection), and
  // deliberately records WHO/WHICH/WHEN but never the password.
  await getFirestore().collection("gcPasswordResets").add({
    targetEmail: target,
    targetUid: uid,
    resetBy: request.auth.uid,
    resetAt: FieldValue.serverTimestamp(),
  }).catch(err => logger.error("adminResetGcPassword: audit write failed", err));

  logger.info(`adminResetGcPassword: reset ${target} by ${request.auth.uid}`);
  return { success: true as const, email: target, password };
});
