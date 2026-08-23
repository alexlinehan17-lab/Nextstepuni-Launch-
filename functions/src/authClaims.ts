import { getAuth } from "firebase-admin/auth";

export interface ClaimSource {
  role?: unknown;
  school?: unknown;
}

/** Synchronise the authorization subset of users/{uid} into signed ID tokens. */
export async function syncAuthorizationClaims(uid: string, source: ClaimSource): Promise<void> {
  const auth = getAuth();
  const user = await auth.getUser(uid);
  const existing = user.customClaims || {};
  const role = source.role;
  const next = { ...existing };

  // The platform-admin claim is provisioned out of band and is never derived
  // from a Firestore document. Only school-scoped roles are mirrored here.
  if (role === "gc" || role === "staff") next.role = role;
  else delete next.role;

  // School is useful in a signed token only alongside a current staff role.
  // Student tenancy is always resolved from the live server-owned profile;
  // mirroring it into a long-lived token creates needless stale authority.
  if (
    (role === "gc" || role === "staff")
    && typeof source.school === "string"
    && source.school.length > 0
  ) next.school = source.school;
  else delete next.school;

  await auth.setCustomUserClaims(uid, next);
}

/** Remove all school-scoped authorization from a deleted/revoked profile. */
export async function clearAuthorizationClaims(uid: string): Promise<void> {
  const auth = getAuth();
  const user = await auth.getUser(uid);
  const next = { ...(user.customClaims || {}) };
  delete next.role;
  delete next.school;
  await auth.setCustomUserClaims(uid, next);
}
