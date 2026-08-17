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

  it('still cleans up synchronously when registration itself fails', () => {
    // The synchronous path is correct and must stay: if sign-up fails while the
    // student is still on the registration screen, the half-made Auth account
    // should be removed rather than left orphaned.
    expect(source).toMatch(/catch[\s\S]{0,200}?await deleteUser\(createdUser\)/);
  });
});
