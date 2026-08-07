import { getAuth } from "firebase-admin/auth";

export interface ClaimSource {
  role?: unknown;
  school?: unknown;
  isAdmin?: unknown;
}

/** Synchronise the authorization subset of users/{uid} into signed ID tokens. */
export async function syncAuthorizationClaims(uid: string, source: ClaimSource): Promise<void> {
  const auth = getAuth();
  const user = await auth.getUser(uid);
  const existing = user.customClaims || {};
  const role = source.isAdmin === true ? "admin" : source.role;
  const next = { ...existing };

  if (role === "admin" || role === "gc" || role === "staff") next.role = role;
  else delete next.role;

  if (typeof source.school === "string" && source.school.length > 0) next.school = source.school;
  else delete next.school;

  await auth.setCustomUserClaims(uid, next);
}
