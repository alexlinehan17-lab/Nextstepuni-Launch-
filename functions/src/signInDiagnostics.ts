/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Why sign-ins fail, counted without knowing who.
 *
 * Firebase Auth keeps no record of why a password sign-in failed, and the
 * request counts showed 287 failures against 12 successes while 60 accounts
 * were being created at one school (12 Oct 2026). This is the only way to tell
 * a locked-out account from a typo from a network that cannot reach Firebase.
 *
 * It has to accept callers who are not signed in, so it accepts nothing an
 * open endpoint could misuse: three values from fixed lists, written as one
 * log line. No free text, no email, no account id, no Firestore write.
 */

import { onCall } from "firebase-functions/v2/https";
import { logger } from "firebase-functions/v2";
import { CALLABLE_OPTIONS } from "./security";

const KINDS = new Set(["credentials", "too-many-requests", "network", "invalid-email", "disabled", "profile-read", "other"]);
const INPUTS = new Set(["email", "username"]);
const PLATFORMS = new Set(["web", "ios", "android"]);

export interface SignInFailureReport {
  kind: string;
  input: string;
  platform: string;
}

/** The report, if every field is one of the expected values; otherwise null. */
export function validSignInFailure(data: unknown): SignInFailureReport | null {
  if (!data || typeof data !== "object") return null;
  const { kind, input, platform } = data as Record<string, unknown>;
  if (typeof kind !== "string" || !KINDS.has(kind)) return null;
  if (typeof input !== "string" || !INPUTS.has(input)) return null;
  if (typeof platform !== "string" || !PLATFORMS.has(platform)) return null;
  return { kind, input, platform };
}

export const reportSignInFailure = onCall(
  { ...CALLABLE_OPTIONS, maxInstances: 2 },
  async request => {
    const report = validSignInFailure(request.data);
    // A malformed report is dropped silently: there is nothing to tell a
    // caller who is not using the app.
    if (report) logger.info("sign_in_failure", report);
    return { ok: true };
  },
);
