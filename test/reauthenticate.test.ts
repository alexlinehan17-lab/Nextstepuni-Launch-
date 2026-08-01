/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the re-authentication method chosen before account deletion.
 *
 * App Review rejected 1.0 (1) under Guideline 5.1.1(v) for having no way to
 * delete an account. The flow existed, but it re-authenticated with
 * EmailAuthProvider.credential(email, password) unconditionally — and on iOS the
 * app hides Google and offers Sign in with Apple, so an iPhone user who signed up
 * that way has no password. Deletion could only ever fail for them, and it failed
 * as "Incorrect password", which reads as user error rather than a dead end.
 *
 * Nothing covered this path, which is why it stayed silent. These assert the
 * routing directly, on the provider data Firebase actually reports.
 */
import { describe, test, expect } from 'vitest';
import type { User } from 'firebase/auth';
import { reauthMethodFor } from '@/utils/reauthenticate';

/** Minimal stand-in: reauthMethodFor reads only providerData. */
const userWith = (...providerIds: string[]) =>
  ({ providerData: providerIds.map(providerId => ({ providerId })) } as unknown as User);

describe('reauthMethodFor', () => {
  test('an email/password account verifies with its password', () => {
    expect(reauthMethodFor(userWith('password'))).toBe('password');
  });

  test('an Apple-only account verifies with Apple, never a password', () => {
    // The regression: this returned 'password' by assumption, so every iPhone
    // user who signed up with Apple was locked out of deleting their account.
    expect(reauthMethodFor(userWith('apple.com'))).toBe('apple');
  });

  test('a Google-only account verifies with Google', () => {
    expect(reauthMethodFor(userWith('google.com'))).toBe('google');
  });

  test('an account holding both prefers the password — no round trip needed', () => {
    expect(reauthMethodFor(userWith('apple.com', 'password'))).toBe('password');
    expect(reauthMethodFor(userWith('google.com', 'password'))).toBe('password');
  });

  test('an unknown provider is reported, not guessed at', () => {
    // Better to route the student to support than to show them a password box
    // that cannot succeed.
    expect(reauthMethodFor(userWith('microsoft.com'))).toBe('unsupported');
    expect(reauthMethodFor(userWith())).toBe('unsupported');
  });

  test('a signed-out user is unsupported rather than a crash', () => {
    expect(reauthMethodFor(null)).toBe('unsupported');
  });
});
