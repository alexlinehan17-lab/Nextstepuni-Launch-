/**
 * Shared server-side authorization checks for sensitive callable functions.
 *
 * Firebase verifies that a callable's ID token is signed, but an otherwise
 * valid ID token can live for up to an hour after refresh-token revocation.
 * Password resets, account deletion and role changes therefore also compare
 * the token's auth_time with the Auth user's tokensValidAfterTime.
 */
import { getAuth } from "firebase-admin/auth";
import { getFirestore } from "firebase-admin/firestore";
import { HttpsError } from "firebase-functions/v2/https";
import { defineBoolean } from "firebase-functions/params";
import { ADMIN_EMAIL } from "./adminIdentity";

export interface CallableAuth {
  uid: string;
  token: Record<string, unknown>;
}

/**
 * Enable enforcement only after web, iOS and Android providers are registered.
 * A typed deploy parameter is used instead of a runtime process.env lookup so
 * the value is embedded correctly in the callable deployment manifest.
 */
export const ENFORCE_APP_CHECK = defineBoolean("ENFORCE_APP_CHECK", {
  default: false,
  description: "Reject callable requests without a valid Firebase App Check token.",
});

export const CALLABLE_OPTIONS = {
  cors: true,
  enforceAppCheck: ENFORCE_APP_CHECK,
} as const;

export function authTimeSeconds(auth: CallableAuth): number {
  const value = auth.token.auth_time;
  if (typeof value !== "number" || !Number.isFinite(value) || value <= 0) {
    throw new HttpsError("unauthenticated", "This sign-in cannot be verified. Please sign in again.");
  }
  return Math.floor(value);
}

export function isVerifiedAdminToken(token: Record<string, unknown>): boolean {
  return token.admin === true
    && token.email_verified === true
    && typeof token.email === "string"
    && token.email.trim().toLowerCase() === ADMIN_EMAIL;
}

export function assertRecentAuth(auth: CallableAuth, maxAgeSeconds = 300): void {
  const issuedAt = authTimeSeconds(auth);
  const now = Math.floor(Date.now() / 1000);
  if (issuedAt > now + 60 || now - issuedAt > maxAgeSeconds) {
    throw new HttpsError(
      "failed-precondition",
      "For your security, please verify your sign-in and try again.",
    );
  }
}

/**
 * Reject an ID token issued before the user's latest revocation boundary.
 * This closes the normal one-hour grace period for sensitive operations.
 */
export async function assertUnrevokedAuth(
  auth: CallableAuth,
  allowMissingProfile = false,
): Promise<void> {
  const [record, profileSnap] = await Promise.all([
    getAuth().getUser(auth.uid),
    getFirestore().collection("users").doc(auth.uid).get(),
  ]);
  const validAfterMs = Date.parse(record.tokensValidAfterTime || "");
  // Both ID-token auth_time and Firebase's revocation check have second-level
  // semantics. Comparing against the millisecond remainder would incorrectly
  // reject a genuinely new token issued later in the same displayed second.
  const validAfterSeconds = Math.floor(validAfterMs / 1000);
  if (Number.isFinite(validAfterMs) && authTimeSeconds(auth) < validAfterSeconds) {
    throw new HttpsError("unauthenticated", "This session has ended. Please sign in again.");
  }
  if (record.disabled) {
    throw new HttpsError("permission-denied", "This account is disabled.");
  }
  if (!profileSnap.exists) {
    if (allowMissingProfile && !isVerifiedAdminToken(auth.token)) return;
    throw new HttpsError("permission-denied", "This account profile is not active.");
  }
  const profile = profileSnap.data() || {};
  if (profile.accountDisabled === true) {
    throw new HttpsError("permission-denied", "This account is disabled.");
  }
  const cutoff = profile.sessionValidAfterSeconds;
  if (typeof cutoff === "number" && authTimeSeconds(auth) <= cutoff) {
    throw new HttpsError("unauthenticated", "This session has ended. Please sign in again.");
  }
}

export async function assertSensitiveAuth(auth: CallableAuth, maxAgeSeconds = 300): Promise<void> {
  assertRecentAuth(auth, maxAgeSeconds);
  await assertUnrevokedAuth(auth);
}
