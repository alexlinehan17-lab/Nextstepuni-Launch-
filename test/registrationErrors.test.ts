import { beforeEach, describe, expect, it } from 'vitest';
import { getRegistrationErrorCode, registrationErrorField, registrationErrorMessage } from '../utils/registrationErrors';
import { stashRegistrationError, takeRegistrationError } from '../utils/registrationProvisioning';

beforeEach(() => sessionStorage.clear());

describe('registration failure explanations', () => {
  it.each([
    ['functions/invalid-argument', 'A valid join code is required.'],
    ['functions/permission-denied', 'That join code is not correct.'],
  ])('identifies a rejected school code (%s)', (code, message) => {
    const reason = getRegistrationErrorCode({ code, message });
    expect(reason).toBe('bad-join-code');
    expect(registrationErrorMessage(reason)).toMatch(/school join code is not correct/i);
    expect(registrationErrorField(reason)).toEqual({ step: 2, id: 'register-join-code' });
  });

  it.each([
    [{ code: 'functions/invalid-argument', message: 'A valid school is required.' }, 'invalid-school', /choose your school again/i],
    [{ code: 'functions/failed-precondition', message: 'Student access has not been set up for this school.' }, 'school-unconfigured', /ask your teacher or guidance counsellor/i],
    [{ code: 'auth/email-already-in-use' }, 'email-in-use', /try signing in/i],
    [{ code: 'auth/weak-password' }, 'weak-password', /password must be at least/i],
    [{ code: 'auth/invalid-email' }, 'invalid-email', /email address is not valid/i],
    [{ code: 'auth/network-request-failed' }, 'network-error', /check your internet connection/i],
    [{ code: 'functions/deadline-exceeded' }, 'timeout', /took too long to respond/i],
    [{ code: 'functions/unavailable' }, 'service-unavailable', /temporarily unavailable/i],
    [{ code: 'functions/resource-exhausted' }, 'too-many-attempts', /wait a few minutes/i],
    [{ code: 'auth/too-many-requests' }, 'too-many-attempts', /wait a few minutes/i],
    [{ code: 'functions/unauthenticated' }, 'session-unverified', /session could not be verified/i],
    [{ code: 'auth/operation-not-allowed' }, 'signup-unavailable', /account creation is currently unavailable/i],
    [{ code: 'functions/permission-denied', message: 'This account is disabled.' }, 'access-denied', /access.*denied/i],
  ] as const)('explains %j and survives the rollback handoff', (error, expected, explanation) => {
    const reason = getRegistrationErrorCode(error);
    expect(reason).toBe(expected);
    stashRegistrationError(reason);
    const restored = takeRegistrationError();
    expect(restored).toBe(reason);
    expect(registrationErrorMessage(restored!)).toMatch(explanation);
    expect(takeRegistrationError()).toBeNull();
  });

  it.each([null, undefined, { message: '<script>private server detail</script>' }, { code: 'functions/internal' }])('does not invent a cause or expose unknown server details (%j)', error => {
    const reason = getRegistrationErrorCode(error);
    expect(reason).toBe('generic');
    expect(registrationErrorMessage(reason)).toMatch(/contact your school for help/i);
    expect(registrationErrorMessage(reason)).not.toMatch(/script|private server detail|join code/i);
    expect(registrationErrorField(reason)).toBeUndefined();
  });
});
