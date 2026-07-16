import { createHash } from "crypto";

/**
 * Public projection of a teach-back — the anonymity fix (security review
 * 2026-07-16, M-7).
 *
 * Teach-backs are presented to students as anonymous ("A classmate shared…"),
 * but the source `teachbacks/{id}` doc carries `authorUid` and the old read
 * rule let every same-school peer read the whole doc — so a peer could
 * de-anonymise who wrote what. The source doc is now readable only by its
 * author; peers read this projection instead, which carries NO raw author
 * identifier.
 *
 * `authorHash` is a one-way SHA-256 (64-bit) of the author uid, present ONLY so
 * a reader can filter out their OWN teach-backs (by comparing against the hash
 * of their own uid). It is not reversible to a name, and no other student's uid
 * is exposed anywhere in the app, so it can't be used to de-anonymise a peer.
 */

export interface TeachbackPublic {
  subject: string;
  school: string;
  explanation: string;
  helpfulCount: number;
  authorHash: string;
}

export function teachbackAuthorHash(uid: string): string {
  return createHash("sha256").update(uid).digest("hex").slice(0, 16);
}

/**
 * Build the projection from a source teach-back doc. Returns null if the doc is
 * missing required fields (in which case the caller should ensure no projection
 * exists).
 */
export function buildTeachbackPublic(
  data: Record<string, unknown> | undefined,
): TeachbackPublic | null {
  if (!data) return null;
  const subject = data.subject;
  const school = data.school;
  const explanation = data.explanation;
  const authorUid = data.authorUid;
  if (typeof subject !== "string" || typeof school !== "string" ||
      typeof explanation !== "string" || typeof authorUid !== "string") {
    return null;
  }
  const helpfulCount = typeof data.helpfulCount === "number" ? data.helpfulCount : 0;
  return {
    subject,
    school,
    explanation: explanation.slice(0, 500),
    helpfulCount,
    authorHash: teachbackAuthorHash(authorUid),
  };
}
