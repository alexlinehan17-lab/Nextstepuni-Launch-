/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Who the platform administrator is — one definition, used everywhere.
 *
 * ─── WHY IT MOVED (2026-08-17) ─────────────────────────────────────────────
 *
 * The administrator was `admin@nextstep.app`, an address at a domain with no
 * mailbox behind it. That meant password reset was impossible: the Firebase
 * console's only option emails a link into the void, and it offers no way to
 * set a password directly. The account had not been signed into since
 * February. Losing that password would have locked the platform owner out of
 * the feedback inbox, the launch-day funnel and counsellor-login recovery,
 * permanently and with no route back.
 *
 * It is now a real mailbox the owner controls, so "forgot password" simply
 * works — the same argument that applies to the shared gc-* logins.
 *
 * ─── HOW ADMIN IS DETERMINED ───────────────────────────────────────────────
 *
 * By the VERIFIED AUTH EMAIL on the ID token, never by a field on a Firestore
 * document. A document can be written; the token cannot be forged. Any change
 * here must be mirrored in three places or access will silently disagree with
 * itself:
 *
 *   1. this file                      — the client's routing decision
 *   2. functions/src/adminIdentity.ts — server-side callable checks
 *   3. firestore.rules `isAdmin()`    — what the database will actually allow
 *
 * The rules are the only one that is load-bearing for security. The other two
 * decide what the UI offers; the database decides what is permitted.
 */

/** The platform administrator's sign-in address. */
export const ADMIN_EMAIL = 'nextstepuniinfo@gmail.com';

/**
 * Addresses no one may register through the app.
 *
 * `admin@nextstep.app` stays reserved even though it is no longer privileged:
 * the Auth account still exists, and letting someone claim that address would
 * be needlessly confusing. The gc-* pattern is reserved because those logins
 * are provisioned, never self-registered.
 */
const RESERVED_GC_PATTERN = /^gc-.*@nextstep\.app$/;
/** Staff-room logins are provisioned the same way, so the same reservation applies. */
const RESERVED_STAFF_PATTERN = /^staff-.*@nextstep\.app$/;
const RETIRED_ADMIN_EMAIL = 'admin@nextstep.app';

/** True if this is the administrator. Case-insensitive; addresses are not. */
export function isAdminEmail(email: string | null | undefined): boolean {
  if (!email) return false;
  return email.trim().toLowerCase() === ADMIN_EMAIL;
}

/**
 * Client routing is privileged only when the signed token carries the
 * server-issued admin claim and Firebase has verified the exact mailbox.
 * Firestore rules and callable functions repeat the same check.
 */
export function isVerifiedAdminSession(
  user: { email?: string | null; emailVerified?: boolean },
  claims: Record<string, unknown>,
): boolean {
  return user.emailVerified === true && claims.admin === true && isAdminEmail(user.email);
}

/** True if this address may not be used to register a new account. */
export function isReservedEmail(email: string | null | undefined): boolean {
  if (!email) return false;
  const normalised = email.trim().toLowerCase();
  return normalised === ADMIN_EMAIL
    || normalised === RETIRED_ADMIN_EMAIL
    || RESERVED_GC_PATTERN.test(normalised)
    || RESERVED_STAFF_PATTERN.test(normalised);
}
