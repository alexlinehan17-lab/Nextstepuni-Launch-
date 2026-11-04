/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Why a sign-in failed, in words a student can act on.
 *
 * Every failure used to read "Invalid email or password." — a locked-out
 * account, a dropped connection and a malformed email alike. At the Marino
 * workshop (12 Oct 2026) 60 accounts were created between 10:00 and 11:30 and
 * 287 sign-ins failed in the same window: students who were locked out after a
 * few wrong tries were told their password was wrong, so they kept trying and
 * kept the lock on. Firebase keeps no per-attempt record, so the reason is also
 * reported (anonymously) to find out which of these really happens in a class.
 */

import { Capacitor } from '@capacitor/core';
import { getFunctions, httpsCallable } from 'firebase/functions';
import app from '../firebase';

export type SignInFailureKind =
  | 'credentials'
  | 'too-many-requests'
  | 'network'
  | 'invalid-email'
  | 'disabled'
  | 'profile-read'
  | 'other';

const errorCode = (err: unknown) => String((err as { code?: unknown } | null)?.code ?? '');

/** The sign-in call itself failed. */
export function classifySignInError(err: unknown): SignInFailureKind {
  switch (errorCode(err)) {
    case 'auth/invalid-credential':
    case 'auth/invalid-login-credentials':
    case 'auth/wrong-password':
    case 'auth/user-not-found':
      return 'credentials';
    case 'auth/too-many-requests':
      return 'too-many-requests';
    case 'auth/network-request-failed':
      return 'network';
    case 'auth/invalid-email':
      return 'invalid-email';
    case 'auth/user-disabled':
      return 'disabled';
    default:
      return 'other';
  }
}

/**
 * The reason worth telling the student when several attempts failed (a
 * username is tried as typed, then as username@nextstep.app). A lockout or a
 * connection problem outranks "wrong password": either one makes a correct
 * password fail too.
 */
export function strongestFailure(kinds: SignInFailureKind[]): SignInFailureKind {
  const order: SignInFailureKind[] = ['too-many-requests', 'network', 'disabled', 'profile-read', 'credentials', 'invalid-email', 'other'];
  for (const kind of order) if (kinds.includes(kind)) return kind;
  return 'other';
}

/** How long the Sign in button rests after Firebase locks the account. */
export const SIGN_IN_LOCKOUT_MS = 60_000;

export function signInFailureMessage(kind: SignInFailureKind): string | null {
  switch (kind) {
    case 'too-many-requests':
      return 'Too many tries on this account, so it’s paused for a few minutes. Wait a little before trying again, or reset your password to get straight back in.';
    case 'network':
      return 'We can’t reach NextStepUni. Check your Wi-Fi or connection, then try again.';
    case 'invalid-email':
      return 'Check the email address, for example you@school.ie.';
    case 'disabled':
      return 'This account has been turned off. Email nextstepuniinfo@gmail.com for help.';
    case 'profile-read':
      return 'Your password was right, but we couldn’t open your account just now. Check your connection and try again.';
    case 'other':
      return 'We couldn’t sign you in just now. Try again in a moment.';
    default:
      // Wrong email or password: the caller has its own email/username wording.
      return null;
  }
}

/**
 * Report a failed sign-in for diagnosis: only the reason, the platform and
 * whether an email or a username was typed. Never the email, the password or
 * an account id. Fire-and-forget; a failed report changes nothing for the
 * student.
 */
export function reportSignInFailure(kind: SignInFailureKind, input: 'email' | 'username'): void {
  try {
    const platform = Capacitor.getPlatform();
    void httpsCallable(getFunctions(app), 'reportSignInFailure')({ kind, input, platform }).catch(() => {});
  } catch {
    // Diagnostics must never surface to the student.
  }
}
