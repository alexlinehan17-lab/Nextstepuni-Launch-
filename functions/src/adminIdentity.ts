/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Server-side definition of the platform administrator.
 *
 * Deliberately duplicated from utils/adminIdentity.ts rather than imported:
 * functions/ compiles under its own tsconfig with its own rootDir, and reaching
 * up into the app tree would drag the client bundle into the deploy. The two
 * files must be changed together — see the note in utils/adminIdentity.ts for
 * the three places that have to agree (client, functions, firestore.rules).
 *
 * Checked against the VERIFIED email on the ID token, never a Firestore field:
 * a document can be written, a token cannot be forged.
 */

/** The platform administrator's sign-in address. */
export const ADMIN_EMAIL = "nextstepuniinfo@gmail.com";

/**
 * True if this caller is the administrator.
 *
 * Takes the token's email claim. Case-folded because address comparison is
 * case-insensitive, but nothing else is normalised — this is an exact
 * identifier and a near-match must fail closed.
 */
export function isAdminEmail(email: unknown): boolean {
  if (typeof email !== "string") return false;
  return email.trim().toLowerCase() === ADMIN_EMAIL;
}
