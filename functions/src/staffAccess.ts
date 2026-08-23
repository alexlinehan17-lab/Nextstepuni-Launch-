import { getAuth } from "firebase-admin/auth";
import { getFirestore, FieldValue } from "firebase-admin/firestore";
import { HttpsError, onCall } from "firebase-functions/v2/https";
import { logger } from "firebase-functions/v2";
import { clearAuthorizationClaims, syncAuthorizationClaims } from "./authClaims";
import { generateAccessCode, hashAccessCode, safeHashEqual } from "./accessCodes";
import { isSupportedSchoolId } from "./schoolJoinPolicy";
import { CALLABLE_OPTIONS, assertSensitiveAuth, assertUnrevokedAuth, isVerifiedAdminToken } from "./security";

const WINDOW_MS = 15 * 60 * 1000;
const MAX_FAILURES = 6;

async function currentGuidanceCounsellor(auth: NonNullable<Parameters<typeof assertSensitiveAuth>[0]>) {
  const db = getFirestore();
  const snap = await db.collection("users").doc(auth.uid).get();
  const data = snap.data();
  if (!snap.exists || data?.role !== "gc" || data?.accountDisabled === true) {
    throw new HttpsError("permission-denied", "Only the school's guidance counsellor can manage access.");
  }
  if (typeof data.school !== "string" || !data.school) {
    throw new HttpsError("failed-precondition", "Your account is not linked to a school.");
  }
  return { db, school: data.school };
}

async function recordFailedAttempt(uid: string, collectionName: string): Promise<number> {
  const db = getFirestore();
  const ref = db.collection(collectionName).doc(uid);
  const now = Date.now();
  return db.runTransaction(async transaction => {
    const current = (await transaction.get(ref)).data() || {};
    const start = typeof current.windowStart === "number" && now - current.windowStart <= WINDOW_MS
      ? current.windowStart
      : now;
    const count = start === current.windowStart && typeof current.count === "number" ? current.count : 0;
    if (count >= MAX_FAILURES) {
      throw new HttpsError("resource-exhausted", "Too many attempts. Please wait a few minutes and try again.");
    }
    transaction.set(ref, {
      count: count + 1,
      windowStart: start,
      updatedAt: now,
      expiresAt: new Date(now + 48 * 60 * 60 * 1000),
    });
    return count + 1;
  });
}

/** Redeem a server-held, rotatable staff invitation code. */
export const claimStaffAccess = onCall(CALLABLE_OPTIONS, async (request) => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Must be logged in.");
  await assertUnrevokedAuth(request.auth, true);
  const { school, code } = request.data as { school?: unknown; code?: unknown };
  if (!isSupportedSchoolId(school)) {
    throw new HttpsError("invalid-argument", "A valid school is required.");
  }
  if (typeof code !== "string" || code.length < 10 || code.length > 64) {
    throw new HttpsError("invalid-argument", "A valid staff code is required.");
  }

  const db = getFirestore();
  const auth = getAuth();
  const uid = request.auth.uid;
  const userRef = db.collection("users").doc(uid);
  const userSnap = await userRef.get();
  const user = userSnap.data() || {};
  if (user.accountDisabled === true) throw new HttpsError("permission-denied", "This account has been revoked.");
  if (user.role === "admin" || isVerifiedAdminToken(request.auth.token)) {
    throw new HttpsError("failed-precondition", "Admin accounts do not redeem staff codes.");
  }
  if (user.role === "gc" || user.role === "staff") {
    if (user.school !== school) throw new HttpsError("permission-denied", "This account belongs to another school.");
    await syncAuthorizationClaims(uid, { role: user.role, school: user.school });
    return { success: true as const, alreadyStaff: true };
  }

  const secretRef = db.collection("staffAccessSecrets").doc(school);
  const secret = (await secretRef.get()).data();
  const suppliedHash = hashAccessCode(code);
  if (typeof secret?.codeHash !== "string" || !safeHashEqual(suppliedHash, secret.codeHash)) {
    const count = await recordFailedAttempt(uid, "staffClaimAttempts");
    logger.info(`claimStaffAccess: rejected code by ${uid} for ${school} (${count}/${MAX_FAILURES})`);
    throw new HttpsError("permission-denied", "That staff code is not correct.");
  }

  const authUser = await auth.getUser(uid);
  if (!authUser.email || authUser.emailVerified !== true) {
    throw new HttpsError("failed-precondition", "Verify your email address before joining the staff dashboard.");
  }

  // A staff code is an invitation, not a permanent shared password. Consume it
  // in the same transaction that grants the role so two concurrent redemptions
  // cannot both succeed. The GC generates a fresh invitation for each teacher.
  await db.runTransaction(async transaction => {
    const freshSecret = (await transaction.get(secretRef)).data();
    const freshUser = (await transaction.get(userRef)).data() || {};
    if (freshUser.role === "gc" || freshUser.role === "staff") {
      throw new HttpsError("already-exists", "This account already has staff access.");
    }
    if (
      typeof freshSecret?.codeHash !== "string"
      || !safeHashEqual(suppliedHash, freshSecret.codeHash)
    ) {
      throw new HttpsError("failed-precondition", "That staff invitation has already been used or rotated.");
    }
    transaction.set(userRef, { role: "staff", school, accountDisabled: false }, { merge: true });
    transaction.set(db.collection("staffAccessMemberships").doc(school).collection("members").doc(uid), {
      uid,
      school,
      email: authUser.email,
      name: typeof freshUser.name === "string" ? freshUser.name.trim().slice(0, 50) : "Staff member",
      status: "active",
      joinedAt: FieldValue.serverTimestamp(),
      codeVersion: freshSecret.version || 1,
    }, { merge: true });
    transaction.update(secretRef, {
      codeHash: FieldValue.delete(),
      active: false,
      consumedAt: FieldValue.serverTimestamp(),
      consumedBy: uid,
    });
    transaction.delete(db.collection("staffClaimAttempts").doc(uid));
  });
  await syncAuthorizationClaims(uid, { role: "staff", school });
  logger.info(`claimStaffAccess: granted staff to ${uid} for ${school}`);
  return { success: true as const };
});

export const getSchoolAccessStatus = onCall(CALLABLE_OPTIONS, async (request) => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Must be logged in.");
  await assertUnrevokedAuth(request.auth);
  const { db, school } = await currentGuidanceCounsellor(request.auth);
  const [staff, student] = await Promise.all([
    db.collection("staffAccessSecrets").doc(school).get(),
    db.collection("studentAccessSecrets").doc(school).get(),
  ]);
  return {
    school,
    staffConfigured: typeof staff.data()?.codeHash === "string",
    studentConfigured: typeof student.data()?.codeHash === "string",
  };
});

async function rotateCode(
  request: { auth: NonNullable<Parameters<typeof assertSensitiveAuth>[0]> },
  collectionName: "staffAccessSecrets" | "studentAccessSecrets",
) {
  await assertSensitiveAuth(request.auth);
  const { db, school } = await currentGuidanceCounsellor(request.auth);
  const code = generateAccessCode();
  const ref = db.collection(collectionName).doc(school);
  await db.runTransaction(async transaction => {
    const current = (await transaction.get(ref)).data();
    transaction.set(ref, {
      school,
      codeHash: hashAccessCode(code),
      version: typeof current?.version === "number" ? current.version + 1 : 1,
      active: true,
      rotatedAt: FieldValue.serverTimestamp(),
      rotatedBy: request.auth.uid,
    });
  });
  return { success: true as const, code };
}

export const rotateStaffAccessCode = onCall(CALLABLE_OPTIONS, async request => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Must be logged in.");
  return rotateCode({ auth: request.auth }, "staffAccessSecrets");
});

export const rotateStudentJoinCode = onCall(CALLABLE_OPTIONS, async request => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Must be logged in.");
  return rotateCode({ auth: request.auth }, "studentAccessSecrets");
});

export const listStaffAccess = onCall(CALLABLE_OPTIONS, async request => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Must be logged in.");
  await assertUnrevokedAuth(request.auth);
  const { db, school } = await currentGuidanceCounsellor(request.auth);
  const snap = await db.collection("staffAccessMemberships").doc(school).collection("members")
    .where("status", "==", "active").limit(200).get();
  return {
    members: snap.docs.map(doc => {
      const data = doc.data();
      return { uid: doc.id, name: data.name || "Staff member", email: data.email || "" };
    }),
  };
});

export const revokeStaffAccess = onCall(CALLABLE_OPTIONS, async request => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Must be logged in.");
  await assertSensitiveAuth(request.auth);
  const targetUid = (request.data as { uid?: unknown }).uid;
  if (typeof targetUid !== "string" || !targetUid || targetUid.length > 128) {
    throw new HttpsError("invalid-argument", "Choose a valid staff member.");
  }
  const { db, school } = await currentGuidanceCounsellor(request.auth);
  const targetRef = db.collection("users").doc(targetUid);
  const target = (await targetRef.get()).data();
  if (target?.role !== "staff" || target.school !== school) {
    throw new HttpsError("not-found", "That active staff member was not found in your school.");
  }

  await targetRef.update({
    role: FieldValue.delete(),
    school: FieldValue.delete(),
    accountDisabled: true,
    staffAccessRevokedAt: FieldValue.serverTimestamp(),
    staffAccessRevokedBy: request.auth.uid,
  });
  await db.collection("staffAccessMemberships").doc(school).collection("members").doc(targetUid).set({
    status: "revoked",
    revokedAt: FieldValue.serverTimestamp(),
    revokedBy: request.auth.uid,
  }, { merge: true });
  await clearAuthorizationClaims(targetUid);
  await getAuth().updateUser(targetUid, { disabled: true });
  await getAuth().revokeRefreshTokens(targetUid);
  logger.info(`revokeStaffAccess: ${request.auth.uid} revoked ${targetUid} in ${school}`);
  return { success: true as const };
});
