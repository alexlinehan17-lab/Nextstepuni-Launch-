/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Re-authenticating the current user before a destructive action.
 *
 * Firebase requires a recent login before it will delete an account. The
 * original implementation assumed everyone had a password:
 *
 *     reauthenticateWithCredential(user, EmailAuthProvider.credential(email, pw))
 *
 * On iOS the app hides Google and offers Sign in with Apple, so an iPhone user
 * who signed up that way has NO password. That call could only ever fail, and it
 * failed as "Incorrect password" — leaving them unable to delete their account at
 * all. App Store Guideline 5.1.1(v) requires that deletion be possible, so this
 * was both a real defect for those users and a rejection waiting to happen.
 *
 * The provider the user actually holds decides how they prove it is them.
 */

import {
  EmailAuthProvider,
  GoogleAuthProvider,
  reauthenticateWithCredential,
  reauthenticateWithPopup,
  type User,
} from 'firebase/auth';
import { authorizeWithApple } from './appleAuth';

export type ReauthMethod = 'password' | 'apple' | 'google' | 'unsupported';

/**
 * How this user can prove who they are.
 *
 * Reads providerData rather than assuming: an account may hold several, and the
 * password provider is preferred when present because it needs no round trip.
 */
export function reauthMethodFor(user: User | null): ReauthMethod {
  if (!user) return 'unsupported';
  const ids = new Set(user.providerData.map(p => p.providerId));
  if (ids.has('password')) return 'password';
  if (ids.has('apple.com')) return 'apple';
  if (ids.has('google.com')) return 'google';
  return 'unsupported';
}

/**
 * Prove it is really this user, then refresh the ID token so the deletion
 * function sees a recent `auth_time`.
 *
 * `password` is required only for the password method and ignored otherwise.
 * Throws on failure; the caller decides what to show.
 */
export async function reauthenticateCurrentUser(user: User, password?: string): Promise<void> {
  const method = reauthMethodFor(user);

  switch (method) {
    case 'password': {
      if (!user.email) throw new Error('This account has no email address to verify against.');
      if (!password) throw new Error('Password required.');
      await reauthenticateWithCredential(user, EmailAuthProvider.credential(user.email, password));
      break;
    }
    case 'apple': {
      // Re-run the native authorization. Apple shows its own confirmation sheet,
      // which IS the identity check — there is no password to ask for.
      const { credential } = await authorizeWithApple();
      await reauthenticateWithCredential(user, credential);
      break;
    }
    case 'google': {
      // Web only; Google is hidden on native.
      await reauthenticateWithPopup(user, new GoogleAuthProvider());
      break;
    }
    default:
      throw new Error('This account cannot be verified automatically. Please contact support.');
  }

  // Force a fresh token so the callable sees the new auth_time.
  await user.getIdToken(true);
}
