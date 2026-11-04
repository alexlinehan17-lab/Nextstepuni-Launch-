import { HttpsError, onCall, type CallableRequest } from 'firebase-functions/v2/https';
import { FieldValue, getFirestore } from 'firebase-admin/firestore';
import { CALLABLE_OPTIONS, assertUnrevokedAuth, isVerifiedAdminToken } from './security';
import { PRIVACY_POLICY_VERSION, TERMS_VERSION, validLegalAgreementRequest } from './legalAgreementPolicy';

/** The caller can agree only for their own account, to the published release. */
export async function saveLegalAgreement(request: CallableRequest, dependencies = {
  getDb: getFirestore, verify: assertUnrevokedAuth, timestamp: FieldValue.serverTimestamp,
}) {
  if (!request.auth) throw new HttpsError('unauthenticated', 'Please sign in first.');
  await dependencies.verify(request.auth);
  const db = dependencies.getDb();
  const userRef = db.collection('users').doc(request.auth.uid);
  const recordRef = db.collection('legalAgreementRecords')
    .doc(`${request.auth.uid}_${PRIVACY_POLICY_VERSION}_${TERMS_VERSION}`);
  await db.runTransaction(async transaction => {
    const [user, existing] = await Promise.all([transaction.get(userRef), transaction.get(recordRef)]);
    if (!user.exists || user.data()?.accountDisabled === true) {
      throw new HttpsError('failed-precondition', 'Your account profile is not ready. Please retry.');
    }
    const role = user.data()?.role;
    const student = role !== 'gc' && role !== 'staff' && !isVerifiedAdminToken(request.auth!.token);
    if (!validLegalAgreementRequest(request.data, student)) {
      throw new HttpsError('invalid-argument', 'Review the current documents and confirm the required checkboxes.');
    }
    // Preserve the first explicit action for this release on retries. A former
    // staff account becoming a student must separately confirm eligibility.
    const previous = existing.data();
    const acceptance = {
      privacyVersion: PRIVACY_POLICY_VERSION,
      termsVersion: TERMS_VERSION,
      acceptedAt: previous && (!student || previous.studentAgeConfirmed === true)
        ? previous.acceptedAt : dependencies.timestamp(),
      method: 'explicit-checkbox' as const,
      studentAgeConfirmed: student ? true : request.data.studentAgeConfirmed === true,
    };
    transaction.set(recordRef, { uid: request.auth!.uid, ...acceptance });
    transaction.update(userRef, { legalAcceptance: acceptance });
  });
  return { success: true, privacyVersion: PRIVACY_POLICY_VERSION, termsVersion: TERMS_VERSION };
}

export const acceptLegalDocuments = onCall(CALLABLE_OPTIONS, request => saveLegalAgreement(request));
