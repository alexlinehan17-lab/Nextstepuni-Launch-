/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Whether a failed registration may delete the auth account it just created.
 *
 * Students were being thrown back to the login screen part-way through
 * onboarding with their account gone (diagnosed 2026-08-17). Registration
 * signs the student in, then writes `users/{uid}`. If that write failed, the
 * catch deleted the auth account — but by then the student is signed in and
 * AuthContext has routed them into onboarding, because AuthContext follows
 * `onAuthStateChanged`, not the registration handler's own success callback.
 * Deleting signed them out mid-flow and destroyed a perfectly valid account,
 * with no error that explained it. Because it is a timing race it hit only
 * some students, which is what made it so hard to see.
 *
 * The rollback exists to reap ORPHANS — an auth account whose registration
 * never completed, e.g. a wrong school join code. Reaping those is right: it
 * lets the student retry with the same email instead of colliding with
 * `auth/email-already-in-use`. The rollback simply could not tell an orphan
 * from a live user, so it raced them.
 *
 * The dividing line is whether the `/users` write was reached. Before it, the
 * account never became usable. From that point on the account is valid and a
 * failed write is retried instead — `setDoc(merge)` is idempotent, and
 * AuthContext's no-user-doc fallback carries the student until it lands.
 */
export interface RollbackContext {
  /** An auth account was created and is signed in. */
  hasAccount: boolean;
  /** The `users/{uid}` write was reached (whether or not it succeeded). */
  userDocStarted: boolean;
}

export function shouldReapAccount({ hasAccount, userDocStarted }: RollbackContext): boolean {
  return hasAccount && !userDocStarted;
}
