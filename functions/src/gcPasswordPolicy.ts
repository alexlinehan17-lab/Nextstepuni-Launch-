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

import { ADMIN_EMAIL } from "./adminIdentity";

/** Addresses this function is allowed to touch. Deliberately narrow. */
const GC_ADDRESS = /^gc-[a-z0-9-]{1,40}@nextstep\.app$/;

/**
 * Accounts that must never be resettable through this path.
 *
 * The live administrator, and the retired admin@nextstep.app address whose
 * Auth account still exists. Neither is a gc-* address, so the pattern below
 * already excludes them — this is belt and braces on the one function in the
 * codebase that can set someone else's password.
 */
const NEVER_RESETTABLE = [ADMIN_EMAIL, "admin@nextstep.app"];

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
  if (NEVER_RESETTABLE.includes(normalised)) return false;
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
 * Minimum length for a password the administrator types themselves.
 *
 * Shorter than the 14 we generate, because a human-chosen password gets read
 * down a phone and retyped, but well above Firebase's own 6-character floor: a
 * counsellor login opens every student record in a school, and there is no
 * forced-change-on-first-use behind it. Long beats clever here, so length is
 * the only rule — no character-class theatre that pushes people towards
 * Passw0rd! and a sticky note.
 */
export const MIN_SUPPLIED_PASSWORD_LENGTH = 10;
export const MAX_SUPPLIED_PASSWORD_LENGTH = 128;

/** Validity of an administrator-supplied password. Reason is for the UI. */
export type SuppliedPasswordCheck =
  | { ok: true; password: string }
  | { ok: false; reason: "type" | "short" | "long" | "blank" };

/**
 * Validate a typed password. Enforced on the SERVER: the dashboard checks the
 * same rule for a fast error, but a client check is a courtesy, not a control.
 *
 * Not trimmed — leading or trailing spaces are legitimate characters in a
 * password, and silently altering what someone typed would mean the password
 * they wrote down is not the one that was set.
 */
export function checkSuppliedPassword(password: unknown): SuppliedPasswordCheck {
  if (typeof password !== "string") return { ok: false, reason: "type" };
  if (password.trim() === "") return { ok: false, reason: "blank" };
  if (password.length < MIN_SUPPLIED_PASSWORD_LENGTH) return { ok: false, reason: "short" };
  if (password.length > MAX_SUPPLIED_PASSWORD_LENGTH) return { ok: false, reason: "long" };
  return { ok: true, password };
}

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

/**
 * School id → display name, for seeding a counsellor's user doc.
 *
 * Duplicated from schoolData.ts because functions/ compiles under its own
 * rootDir and cannot reach into the app tree. Keep in step with SCHOOLS.
 */
export const SCHOOL_NAMES: Record<string, string> = {
  marino: "Marino",
  joeys: "Joey's",
  larkin: "Larkin",
  oconnells: "O'Connell's",
  mountcarmel: "Mount Carmel",
  rosmini: "Rosmini",
  pwc: "PwC",
};

/** The school id inside a gc-{schoolId}@nextstep.app address, or null. */
export function schoolIdFromGcAddress(email: unknown): string | null {
  const address = gcAddressToReset(email);
  if (!address) return null;
  return address.slice("gc-".length, address.indexOf("@"));
}
