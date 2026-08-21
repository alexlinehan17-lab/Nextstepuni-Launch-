/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guard: registration must never destroy a live session from a background
 * callback.
 *
 * The bug this exists to prevent (found 2026-08-17, live since the flow was
 * written): `writeUserDoc` waits up to 8s for the `users/{uid}` write to be
 * acknowledged, then lets registration proceed so a slow network can't hang the
 * sign-up screen. Its third argument runs if the answer arrives LATER and is a
 * rejection — and that handler called `deleteUser()`.
 *
 * By then the student is signed in and part-way through onboarding. Deleting
 * the account signed them out mid-flow, dropped them on the login screen, and
 * destroyed the account they had just created — no error, no explanation, and
 * only for the subset of students whose write happened to be slow AND rejected.
 * An orphaned user doc is a cosmetic problem for the GC dashboard; this was a
 * student losing their account at the moment of acquisition.
 *
 * A source scan rather than a runtime test, matching firestorePayloadSafety:
 * the failure is a timing race that a unit test cannot reliably reproduce, but
 * the shape that causes it is trivially detectable and must never reappear.
 */
import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const LOGIN_PAGE = resolve(__dirname, '..', 'components', 'LoginPage.tsx');

/** Body of the first `{...}` block at or after `from`, brace-balanced. */
function blockAt(source: string, from: number): string {
  const open = source.indexOf('{', from);
  if (open === -1) return '';
  let depth = 0;
  for (let i = open; i < source.length; i++) {
    if (source[i] === '{') depth++;
    else if (source[i] === '}') {
      depth--;
      if (depth === 0) return source.slice(open, i + 1);
    }
  }
  return source.slice(open);
}

/**
 * Every `const <name> = (err...) => {` in the file — the shape used for the
 * rollback / late-rejection callbacks handed to writeUserDoc and
 * saveInBackground. These run detached from the sign-up flow, potentially
 * long after the student has moved on.
 */
function errorCallbackBodies(source: string): { name: string; body: string }[] {
  const found: { name: string; body: string }[] = [];
  const declaration = /const\s+(\w+)\s*=\s*\(\s*(?:err|error)\w*\s*:/g;
  let match: RegExpExecArray | null;
  while ((match = declaration.exec(source)) !== null) {
    found.push({ name: match[1], body: blockAt(source, match.index) });
  }
  return found;
}

describe('registration session safety', () => {
  const source = readFileSync(LOGIN_PAGE, 'utf8');

  it('finds the error callbacks it is meant to be scanning', () => {
    // If a refactor renames or reshapes these, the scan below would silently
    // pass over nothing at all. Fail loudly instead.
    expect(errorCallbackBodies(source).length).toBeGreaterThan(0);
  });

  it('never deletes the account from a background error callback', () => {
    const offenders = errorCallbackBodies(source)
      .filter(callback => /\bdeleteUser\s*\(/.test(callback.body))
      .map(callback => callback.name);

    expect(
      offenders,
      `${offenders.join(', ')} calls deleteUser() from an error callback. That callback can ` +
        'run after the student is signed in and onboarding, so it destroys a live account and ' +
        'dumps them on the login screen. Retry the write instead — setDoc(merge) is idempotent. ' +
        'Orphaned auth accounts should be reaped server-side, where they cannot race a live user.',
    ).toEqual([]);
  });

  it('still reaps an orphan when registration fails before the /users write', () => {
    // The synchronous path is correct and must stay: a wrong join code leaves a
    // half-made Auth account, and removing it lets the student retry the same
    // email instead of colliding with auth/email-already-in-use.
    expect(source).toMatch(/await deleteUser\(createdUser\)/);
  });

  it('guards the synchronous cleanup so it cannot delete a live account', () => {
    // This test previously asserted an UNGUARDED `catch ... deleteUser`, on the
    // assumption that any synchronous failure means the student is still on the
    // registration screen. That assumption was wrong, and it is the second half
    // of the 2026-08-17 bug: the /users write can reject INSIDE the 8s window,
    // by which point the student is signed in and AuthContext -- which follows
    // onAuthStateChanged, not the registration callback -- has already routed
    // them into onboarding. Deleting there destroys a live account exactly as
    // the late-rejection path did.
    //
    // So the call must be gated on shouldReapAccount(), which is false once the
    // /users write has been reached.
    const deletion = source.indexOf('await deleteUser(createdUser)');
    expect(deletion, 'the synchronous rollback disappeared entirely').toBeGreaterThan(-1);

    const preceding = source.slice(Math.max(0, deletion - 300), deletion);
    expect(
      preceding,
      'deleteUser(createdUser) is no longer guarded by shouldReapAccount(). Unguarded, it ' +
        'deletes the account of a student who is already signed in and onboarding whenever ' +
        'the /users write rejects within the 8s window.',
    ).toMatch(/shouldReapAccount\(/);
  });
});
