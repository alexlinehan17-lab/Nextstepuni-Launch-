/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the invariant that a failed registration never deletes a live account.
 *
 * Students were landing back on the login screen part-way through onboarding
 * with their account destroyed. Registration signs the student in, then writes
 * `users/{uid}`; if that write failed, the catch called `deleteUser()` on the
 * signed-in, actively-onboarding account. Firebase fired
 * `onAuthStateChanged(null)` and they were dumped to login with no way back in.
 *
 * The late-rejection half of this was fixed on 2026-08-17 by retrying instead.
 * The synchronous half — the same race landing inside the 8s write window
 * rather than after it — was still deleting, which is what these lock down.
 */
import { describe, test, expect } from 'vitest';
import { shouldReapAccount } from '@/utils/registrationRollback';

describe('shouldReapAccount', () => {
  test('reaps an orphan: the account never reached the /users write', () => {
    // The common case is a wrong school join code, which throws before the
    // write. Reaping frees the email so the student can retry with it.
    expect(shouldReapAccount({ hasAccount: true, userDocStarted: false })).toBe(true);
  });

  test('NEVER reaps once the /users write has been attempted', () => {
    // The regression. The auth account is valid here and the student may
    // already be in onboarding, so deleting destroys a live account.
    expect(shouldReapAccount({ hasAccount: true, userDocStarted: true })).toBe(false);
  });

  test('has nothing to reap when no account was created', () => {
    // createUserWithEmailAndPassword itself failed (weak password, email in
    // use); there is no account, and deleteUser would throw on null.
    expect(shouldReapAccount({ hasAccount: false, userDocStarted: false })).toBe(false);
    expect(shouldReapAccount({ hasAccount: false, userDocStarted: true })).toBe(false);
  });
});
