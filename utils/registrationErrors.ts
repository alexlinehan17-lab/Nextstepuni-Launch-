import { MIN_PASSWORD_LENGTH } from './passwordPolicy';
import type { RegistrationErrorCode } from './registrationProvisioning';

/** Translate known Auth/callable failures without displaying raw server errors. */
export function getRegistrationErrorCode(error: unknown): RegistrationErrorCode {
  const failure = error && typeof error === 'object' ? error as { code?: unknown; message?: unknown } : {};
  const code = typeof failure.code === 'string' ? failure.code : '';
  const message = typeof failure.message === 'string' ? failure.message : '';

  // claimStudentSchool rejects malformed codes as invalid-argument and a
  // well-formed but incorrect code as permission-denied. Those statuses also
  // cover other failures, so match the specific reason before general codes.
  if (/join code (?:is not correct|is required)/i.test(message)) return 'bad-join-code';
  if (/valid school is required/i.test(message)) return 'invalid-school';
  if (/not been set up for this school/i.test(message)) return 'school-unconfigured';
  if (/too many attempts/i.test(message)) return 'too-many-attempts';

  switch (code) {
    case 'auth/weak-password': return 'weak-password';
    case 'auth/email-already-in-use': return 'email-in-use';
    case 'auth/invalid-email': return 'invalid-email';
    case 'auth/network-request-failed': return 'network-error';
    case 'auth/too-many-requests':
    case 'functions/resource-exhausted': return 'too-many-attempts';
    case 'auth/timeout':
    case 'functions/deadline-exceeded': return 'timeout';
    case 'functions/unavailable': return 'service-unavailable';
    case 'functions/unauthenticated':
    case 'auth/invalid-user-token':
    case 'auth/user-token-expired':
    case 'auth/requires-recent-login': return 'session-unverified';
    case 'auth/operation-not-allowed': return 'signup-unavailable';
    case 'auth/user-disabled':
    case 'functions/permission-denied': return 'access-denied';
    default: return 'generic';
  }
}

export function registrationErrorMessage(code: RegistrationErrorCode): string {
  switch (code) {
    case 'weak-password': return `Password must be at least ${MIN_PASSWORD_LENGTH} characters. Try a longer, memorable phrase.`;
    case 'email-in-use': return 'An account with this email already exists. Try signing in instead.';
    case 'invalid-email': return 'That email address is not valid. Check it and try again.';
    case 'bad-join-code': return 'That school join code is not correct. Check that you have selected the right school and enter the full code from your school.';
    case 'invalid-school': return 'That school could not be recognised. Choose your school again.';
    case 'school-unconfigured': return 'Student access has not been set up for this school. Ask your teacher or guidance counsellor for help.';
    case 'too-many-attempts': return 'Too many attempts. Please wait a few minutes before trying again.';
    case 'network-error': return 'We could not connect to finish creating your account. Check your internet connection and try again.';
    case 'timeout': return 'Account setup took too long to respond. Check your connection and try again.';
    case 'service-unavailable': return 'The account setup service is temporarily unavailable. Please try again in a few minutes.';
    case 'session-unverified': return 'Your account session could not be verified. Please try creating your account again.';
    case 'signup-unavailable': return 'Email account creation is currently unavailable. Please contact your school for help.';
    case 'access-denied': return 'Access to set up this account was denied. Please contact your school for help.';
    default: return 'We could not finish setting up your account. Please try again. If this keeps happening, contact your school for help.';
  }
}

export function registrationErrorField(code: RegistrationErrorCode): { step: 1 | 2 | 3; id: string } | undefined {
  switch (code) {
    case 'weak-password': return { step: 3, id: 'register-password' };
    case 'email-in-use':
    case 'invalid-email': return { step: 1, id: 'register-email' };
    case 'bad-join-code': return { step: 2, id: 'register-join-code' };
    case 'invalid-school':
    case 'school-unconfigured': return { step: 2, id: 'register-school' };
    default: return undefined;
  }
}
