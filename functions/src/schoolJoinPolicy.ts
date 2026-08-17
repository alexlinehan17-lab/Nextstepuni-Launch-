/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * School join codes and how a human-typed one is matched.
 *
 * Split out from schoolAccess.ts (which pulls in firebase-admin) so the
 * matching rule is unit-testable, following anonymousFeedbackPolicy.ts.
 *
 * ─── WHY THE MATCH IS PUNCTUATION-BLIND (2026-08-17) ───────────────────────
 *
 * The comparison used to be `trim().toLowerCase()`. Three of the seven codes
 * contained punctuation a phone keyboard rewrites:
 *
 *   Joey's02        iOS/Android smart punctuation types a CURLY apostrophe (’)
 *   O'Connell's04   where the code holds a straight one ('), so the strings
 *                   differ and the student is told their correct code is wrong
 *   Mount Carmel05  an internal space, which trim() does not touch
 *
 * A student who typed their code exactly as printed got "That join code is not
 * correct", with no way to see why — and six of those in fifteen minutes
 * locked them out. Registration is the one screen every student must pass, so
 * this silently gated three of seven schools.
 *
 * Folding away everything that is not a letter or digit makes every variant a
 * student can plausibly type resolve to the same value. It costs nothing in
 * entropy: these codes are low-entropy and human-shareable by design (see
 * schoolAccess.ts), so their security never came from punctuation.
 */

/**
 * Per-school join codes: the school's display name plus a sequential two-digit
 * index in SCHOOLS order. Kept plain alphanumeric so a code reads the same on
 * a printed handout, a whiteboard and a phone keyboard.
 */
export const SCHOOL_JOIN_CODES: Record<string, string> = {
  marino: "Marino01",
  joeys: "Joeys02",
  larkin: "Larkin03",
  oconnells: "OConnells04",
  mountcarmel: "MountCarmel05",
  rosmini: "Rosmini06",
  pwc: "PwC07",
};

/**
 * Fold a code to its comparable form: lowercase, letters and digits only.
 *
 * Applied to BOTH the typed code and the expected one, so the previously
 * published punctuated codes keep working — "Joey's02", "joeys 02" and
 * "JOEYS02" all reduce to "joeys02". No student holding an old handout is
 * stranded by the reissue.
 */
export function normaliseJoinCode(code: string): string {
  return code.toLowerCase().replace(/[^a-z0-9]/g, "");
}
