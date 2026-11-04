/** Framework-free release metadata shared by the documents and the server. */
export const PRIVACY_POLICY_VERSION = '2026-10-04';
export const TERMS_VERSION = '2026-10-04';
export const LEGAL_LAST_UPDATED = '4 October 2026';

export interface LegalAcceptance {
  privacyVersion: string;
  termsVersion: string;
  acceptedAt: unknown;
  method: 'explicit-checkbox';
  studentAgeConfirmed: boolean;
}

export function hasCurrentLegalAcceptance(value: unknown, student: boolean): value is LegalAcceptance {
  if (!value || typeof value !== 'object') return false;
  const record = value as Partial<LegalAcceptance>;
  return record.privacyVersion === PRIVACY_POLICY_VERSION
    && record.termsVersion === TERMS_VERSION
    && record.acceptedAt != null
    && record.method === 'explicit-checkbox'
    && (!student || record.studentAgeConfirmed === true);
}

export function validLegalAgreementRequest(value: unknown, student: boolean): boolean {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return false;
  const request = value as Record<string, unknown>;
  const keys = ['privacyVersion', 'termsVersion', 'agreeTerms', 'acknowledgePrivacy', 'studentAgeConfirmed'];
  return Object.keys(request).every(key => keys.includes(key))
    && request.privacyVersion === PRIVACY_POLICY_VERSION
    && request.termsVersion === TERMS_VERSION
    && request.agreeTerms === true
    && request.acknowledgePrivacy === true
    && typeof request.studentAgeConfirmed === 'boolean'
    && (!student || request.studentAgeConfirmed === true);
}
