/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The marker that stops a student being shown onboarding while their
 * registration is still provisioning — the window in which a rejected join
 * code or callable can still roll the account back with deleteUser().
 *
 * The property that matters most here is not "does it hold" but "can it ever
 * fail to release". A marker read only during render, in a component with no
 * state of its own, can leave a student on a spinner with nothing to end it —
 * so the expiry, the cross-reload invalidation and the remaining-time signal
 * that lets the reader schedule its own repaint are all load-bearing.
 */
import { describe, expect, it, beforeEach } from 'vitest';

import {
  beginRegistrationProvisioning,
  endRegistrationProvisioning,
  isRegistrationProvisioning,
  registrationHoldRemainingMs,
  stashRegistrationError,
  takeRegistrationError,
} from '@/utils/registrationProvisioning';

const KEY = 'nsu:registration-provisioning';
const MINUTE = 60_000;

describe('registration provisioning marker', () => {
  beforeEach(() => {
    window.sessionStorage.clear();
  });

  it('is off by default, so an ordinary sign-in is never held', () => {
    expect(isRegistrationProvisioning()).toBe(false);
  });

  it('holds while the registration is in flight', () => {
    const start = 1_000_000;
    beginRegistrationProvisioning(start);
    expect(isRegistrationProvisioning(start)).toBe(true);
    // Must cover claimStudentSchool cold-starting plus the forced token refresh.
    expect(isRegistrationProvisioning(start + 30_000)).toBe(true);
  });

  it('is released when the registration resolves', () => {
    beginRegistrationProvisioning(1_000_000);
    endRegistrationProvisioning();
    expect(isRegistrationProvisioning(1_000_000)).toBe(false);
  });

  it('self-expires, so a crashed attempt cannot strand a later student', () => {
    const start = 1_000_000;
    beginRegistrationProvisioning(start);
    expect(isRegistrationProvisioning(start + 2 * MINUTE)).toBe(false);
    expect(window.sessionStorage.getItem(KEY)).toBeNull();
  });

  it('reports the time left, so the reader can schedule its own repaint', () => {
    const start = 1_000_000;
    beginRegistrationProvisioning(start);
    // Without this, expiry is only noticed if something else happens to render.
    expect(registrationHoldRemainingMs(start)).toBe(90_000);
    expect(registrationHoldRemainingMs(start + 30_000)).toBe(60_000);
    expect(registrationHoldRemainingMs(start + 2 * MINUTE)).toBe(0);
  });

  it('ignores a marker written by a previous page load', () => {
    // A reload (or a duplicated tab, which inherits sessionStorage) leaves a
    // marker whose registration died with its JS context. Holding for it could
    // only hang the new page, and nothing would ever clear it.
    window.sessionStorage.setItem(KEY, `some-other-context:${Date.now()}`);
    expect(isRegistrationProvisioning()).toBe(false);
    expect(window.sessionStorage.getItem(KEY)).toBeNull();
  });

  it('ignores a corrupt marker rather than trusting it', () => {
    window.sessionStorage.setItem(KEY, 'not-a-number');
    expect(isRegistrationProvisioning()).toBe(false);
  });

  it('ignores a marker stamped in the future', () => {
    beginRegistrationProvisioning(2_000_000);
    expect(isRegistrationProvisioning(1_000_000)).toBe(false);
  });

  it('does not collide with the staff marker', () => {
    window.sessionStorage.setItem('nsu:staff-provisioning', String(1_000_000));
    expect(isRegistrationProvisioning(1_000_000)).toBe(false);
  });
});

describe('registration error hand-off', () => {
  beforeEach(() => {
    window.sessionStorage.clear();
  });

  it('carries the reason across the remount the rollback causes', () => {
    // The reap signs the student out, which can unmount the LoginPage whose
    // setError would have shown this. Without the hand-off they get a blank form.
    stashRegistrationError('bad-join-code');
    expect(takeRegistrationError()).toBe('bad-join-code');
  });

  it('is read-once, so it cannot haunt a later visit', () => {
    stashRegistrationError('generic');
    takeRegistrationError();
    expect(takeRegistrationError()).toBeNull();
  });

  it('returns null when nothing was stashed', () => {
    expect(takeRegistrationError()).toBeNull();
  });

  it('stores a code, never rendered copy', () => {
    // Persisting the message meant writing a string built from
    // MIN_PASSWORD_LENGTH into storage — a clear-text-storage finding, and UI
    // copy has no business being durable state.
    stashRegistrationError('weak-password');
    const stored = window.sessionStorage.getItem('nsu:registration-error');
    expect(stored).toBe('weak-password');
    expect(stored).not.toMatch(/password must be|characters/i);
  });

  it('ignores an unrecognised value rather than rendering it', () => {
    // Another build's code, or a hand-edited one, must not reach the UI.
    window.sessionStorage.setItem('nsu:registration-error', '<img src=x onerror=alert(1)>');
    expect(takeRegistrationError()).toBeNull();
  });
});
