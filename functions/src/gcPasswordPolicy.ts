/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Who may have their password reset by an administrator, and what the
 * generated password looks like.
 *
 * Split from the callable so the rules are unit-testable without
 * firebase-admin, following anonymousFeedbackPolicy / schoolJoinPolicy.
 *
 * ─── WHY THIS EXISTS (2026-08-17) ──────────────────────────────────────────
 *
 * Guidance-counsellor logins are shared per-school accounts at derived
 * addresses — gc-{schoolId}@nextstep.app — and those mailboxes do not exist.
 * So the Firebase console's only option, "Reset password", emails a link into
 * the void, and the console offers no way to set a password directly. Six of
 * the seven accounts were last used in May, with passwords set in February:
 * effectively unrecoverable, four weeks before launch.
 *
 * ─── THE BLAST RADIUS THIS CONSTRAINS ──────────────────────────────────────
 *
 * A function that sets passwords is the most dangerous thing in this codebase:
 * a flaw is full account takeover. Two hard limits, both enforced server-side:
 *
 *   1. Only the administrator may call it.
 *   2. It may only ever target a gc-*@nextstep.app address. Never a student,
 *      never a teacher, never the admin account itself. Even a caller who is
 *      already the administrator cannot use this to seize a student's account
 *      and read their work as them.
 */

/** Addresses this function is allowed to touch. Deliberately narrow. */
const GC_ADDRESS = /^gc-[a-z0-9-]{1,40}@nextstep\.app$/;

/** The one account that must never be resettable through this path. */
const ADMIN_ADDRESS = "admin@nextstep.app";

/**
 * True only for a guidance-counsellor login.
 *
 * Case-folded and trimmed because the address arrives from a form, but NOT
 * punctuation-folded: unlike a join code typed by a student, this is an exact
 * identifier and a near-match must fail closed.
 */
export function isResettableGcAddress(email: unknown): boolean {
  if (typeof email !== "string") return false;
  const normalised = email.trim().toLowerCase();
  if (normalised === ADMIN_ADDRESS) return false;
  return GC_ADDRESS.test(normalised);
}

/** Normalised form to look up, or null when the address is not resettable. */
export function gcAddressToReset(email: unknown): string | null {
  if (!isResettableGcAddress(email)) return null;
  return (email as string).trim().toLowerCase();
}

/**
 * Alphabet with no O/0/I/1/L — these passwords get read down a phone to a
 * counsellor, so ambiguous glyphs cost a support call. Mirrors the staff-code
 * generator in components/gc/StaffAccessPanel.tsx.
 */
export const PASSWORD_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789";

/**
 * 14 characters — longer than the 8 used for a student's temporary password,
 * because a GC login opens every student record in a school and there is no
 * forced-change-on-first-use step behind it.
 */
export const PASSWORD_LENGTH = 14;

/**
 * Build a password from injected randomness, so the generator is testable and
 * the callable keeps using a CSPRNG (crypto.randomInt), never Math.random.
 */
export function buildPassword(randomIndex: (max: number) => number): string {
  let password = "";
  for (let i = 0; i < PASSWORD_LENGTH; i++) {
    password += PASSWORD_ALPHABET.charAt(randomIndex(PASSWORD_ALPHABET.length));
  }
  return password;
}
