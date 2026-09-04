import { getFirestore, FieldValue } from "firebase-admin/firestore";
import { HttpsError, onCall } from "firebase-functions/v2/https";
import { generateAccessCode, hashAccessCode } from "./accessCodes";
import { CALLABLE_OPTIONS, assertSensitiveAuth, assertUnrevokedAuth } from "./security";

/**
 * ─── THE PER-TEACHER INVITATION FLOW IS RETIRED (owner decision 2026-09-04) ─
 *
 * Teachers used to join through claimStaffAccess: a one-use code the GC minted
 * per teacher, redeemed by a five-field form behind an email-verification
 * round trip. It was this product's single biggest onboarding stall, and it
 * required a client-side provisioning hold (utils/staffProvisioning) purely to
 * stop half-provisioned teachers landing in student onboarding.
 *
 * Staff now sign in the way counsellors always have: one shared per-school
 * login (staff-{schoolId}@nextstep.app) whose password the administrator sets
 * in adminResetGcPassword and hands to the school. That callable provisions
 * role:'staff' server-side BEFORE anyone signs in, so there is no window in
 * which a signed-in teacher lacks a role. Revocation = rotate the password
 * (which also ends live sessions).
 *
 * The retired callables below are TOMBSTONES, not deletions: the CI deploy
 * runs `firebase deploy --non-interactive` without --force, and deleting an
 * exported function makes that deploy prompt — and fail. A later manual
 * `functions:delete` can remove them for good.
 */

const RETIRED = () => new HttpsError(
  "failed-precondition",
  "Teacher access codes were retired. Staff now sign in with the school staff password — ask your school for it.",
);

export const claimStaffAccess = onCall(CALLABLE_OPTIONS, async () => { throw RETIRED(); });
export const rotateStaffAccessCode = onCall(CALLABLE_OPTIONS, async () => { throw RETIRED(); });
export const listStaffAccess = onCall(CALLABLE_OPTIONS, async () => { throw RETIRED(); });
export const revokeStaffAccess = onCall(CALLABLE_OPTIONS, async () => { throw RETIRED(); });

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

export const getSchoolAccessStatus = onCall(CALLABLE_OPTIONS, async (request) => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Must be logged in.");
  await assertUnrevokedAuth(request.auth);
  const { db, school } = await currentGuidanceCounsellor(request.auth);
  const student = await db.collection("studentAccessSecrets").doc(school).get();
  return {
    school,
    studentConfigured: typeof student.data()?.codeHash === "string",
  };
});

/** The student join code is unchanged: rotatable, hashed, shown only when generated. */
export const rotateStudentJoinCode = onCall(CALLABLE_OPTIONS, async request => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Must be logged in.");
  await assertSensitiveAuth(request.auth);
  const rotatedBy = request.auth.uid;
  const { db, school } = await currentGuidanceCounsellor(request.auth);
  const code = generateAccessCode();
  const ref = db.collection("studentAccessSecrets").doc(school);
  await db.runTransaction(async transaction => {
    const current = (await transaction.get(ref)).data();
    transaction.set(ref, {
      school,
      codeHash: hashAccessCode(code),
      version: typeof current?.version === "number" ? current.version + 1 : 1,
      active: true,
      rotatedAt: FieldValue.serverTimestamp(),
      rotatedBy,
    });
  });
  return { success: true as const, code };
});
