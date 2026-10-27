/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { describe, expect, it, vi } from 'vitest';
import { classifySignInError, signInFailureMessage, strongestFailure } from '@/utils/signInFailure';
import { validSignInFailure } from '../functions/src/signInDiagnostics';

vi.mock('@/firebase', () => ({ default: {} }));

const err = (code: string) => Object.assign(new Error(code), { code });

describe('reading a sign-in failure', () => {
  it('separates a wrong password from a lockout, a dropped connection and a bad address', () => {
    expect(classifySignInError(err('auth/invalid-credential'))).toBe('credentials');
    expect(classifySignInError(err('auth/wrong-password'))).toBe('credentials');
    expect(classifySignInError(err('auth/too-many-requests'))).toBe('too-many-requests');
    expect(classifySignInError(err('auth/network-request-failed'))).toBe('network');
    expect(classifySignInError(err('auth/invalid-email'))).toBe('invalid-email');
    expect(classifySignInError(err('auth/user-disabled'))).toBe('disabled');
    expect(classifySignInError(new Error('?'))).toBe('other');
  });

  it('lets a lockout or a connection problem outrank a wrong password', () => {
    expect(strongestFailure(['credentials', 'too-many-requests'])).toBe('too-many-requests');
    expect(strongestFailure(['invalid-email', 'network'])).toBe('network');
    expect(strongestFailure([])).toBe('other');
  });

  it('leaves the wrong-password wording to the form, which knows email from username', () => {
    expect(signInFailureMessage('credentials')).toBeNull();
    expect(signInFailureMessage('too-many-requests')).toMatch(/reset your password/);
  });
});

describe('the anonymous sign-in failure report', () => {
  it('accepts only values from its fixed lists, so it can carry no personal data', () => {
    expect(validSignInFailure({ kind: 'too-many-requests', input: 'email', platform: 'ios' }))
      .toEqual({ kind: 'too-many-requests', input: 'email', platform: 'ios' });
    expect(validSignInFailure({ kind: 'credentials', input: 'username', platform: 'web', email: 'a@b.ie' }))
      .toEqual({ kind: 'credentials', input: 'username', platform: 'web' });
    expect(validSignInFailure({ kind: 'aoife@marinocollege.ie', input: 'email', platform: 'web' })).toBeNull();
    expect(validSignInFailure({ kind: 'credentials', input: 'password123', platform: 'web' })).toBeNull();
    expect(validSignInFailure({ kind: 'credentials', input: 'email', platform: 'windows' })).toBeNull();
    expect(validSignInFailure(null)).toBeNull();
    expect(validSignInFailure('credentials')).toBeNull();
  });
});
