import { doc, onSnapshot } from 'firebase/firestore';
import { getFunctions, httpsCallable } from 'firebase/functions';
import app, { db } from '../firebase';
import { PRIVACY_POLICY_VERSION, TERMS_VERSION } from '../functions/src/legalAgreementPolicy';

// An email-registration checkbox is a real action, but is not proof of a
// server record. Hand it to the same server endpoint used by all other routes.
const pending = new Set<string>();
export function rememberRegistrationAgreement(uid: string): void { pending.add(uid); }
export function takeRegistrationAgreement(uid: string): boolean { return pending.delete(uid); }

export function watchLegalAcceptance(uid: string, onValue: (value: unknown) => void, onError: () => void): () => void {
  return onSnapshot(doc(db, 'users', uid), snapshot => {
    if (!snapshot.exists()) { onError(); return; }
    onValue(snapshot.data().legalAcceptance);
  }, onError);
}

export async function recordLegalAcceptance(studentAgeConfirmed: boolean): Promise<void> {
  const accept = httpsCallable(getFunctions(app), 'acceptLegalDocuments');
  const result = await accept({
    privacyVersion: PRIVACY_POLICY_VERSION,
    termsVersion: TERMS_VERSION,
    agreeTerms: true,
    acknowledgePrivacy: true,
    studentAgeConfirmed,
  });
  const data = result.data as { success?: boolean; privacyVersion?: string; termsVersion?: string };
  if (data.success !== true || data.privacyVersion !== PRIVACY_POLICY_VERSION || data.termsVersion !== TERMS_VERSION) {
    throw new Error('Agreement was not confirmed for the current documents.');
  }
}
