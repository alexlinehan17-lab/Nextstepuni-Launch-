import { doc, onSnapshot } from 'firebase/firestore';
import { getFunctions, httpsCallable } from 'firebase/functions';
import app, { db } from '../firebase';
import { PRIVACY_POLICY_VERSION, TERMS_VERSION } from '../functions/src/legalAgreementPolicy';

// An email-registration checkbox is a real action, but is not proof of a
// server record. Hand it to the same server endpoint used by all other routes.
// Keep the action for this account until the server confirms it, including
// across connection retries or a remount during the onboarding handoff.
const pending = new Set<string>();
export function rememberRegistrationAgreement(uid: string): void { pending.add(uid); }
export function hasRegistrationAgreement(uid: string): boolean { return pending.has(uid); }
export function clearRegistrationAgreement(uid: string): void { pending.delete(uid); }

export function watchLegalAcceptance(uid: string, onValue: (value: unknown) => void, onError: () => void): () => void {
  return onSnapshot(doc(db, 'users', uid), { includeMetadataChanges: true }, snapshot => {
    // An initial cached profile may predate signup's agreement save. Wait for
    // the server before deciding that another review (or a missing-account
    // error) is needed; metadata-only updates must also release this wait.
    if (snapshot.metadata.fromCache) return;
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
