/**
 * School identifiers accepted by the server-side school-binding callable.
 *
 * Join credentials deliberately do not live in source code. Guidance
 * counsellors generate high-entropy codes; only their SHA-256 hashes are kept
 * in the default-deny studentAccessSecrets collection.
 */

export const SUPPORTED_SCHOOL_IDS = [
  "marino",
  "joeys",
  "larkin",
  "oconnells",
  "mountcarmel",
  "rosmini",
  "pwc",
] as const;

export function isSupportedSchoolId(value: unknown): value is typeof SUPPORTED_SCHOOL_IDS[number] {
  return typeof value === "string"
    && (SUPPORTED_SCHOOL_IDS as readonly string[]).includes(value);
}
