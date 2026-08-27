/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The marker that stops a student being shown onboarding while their
 * registration is still provisioning — the window in which a rejected join
 * code or callable can still roll the account back with deleteUser(). Same two
 * properties as the staff marker, pulling against each other: it must hold
 * long enough to cover a cold-start callable plus a forced token refresh, and
 * it must never outlive a failed attempt, or a genuine student would be left
 * on a spinner instead of onboarding.
 */
import { describe, expect, it, beforeEach } from 'vitest';

import {
  beginRegistrationProvisioning,
  endRegistrationProvisioning,
  isRegistrationProvisioning,
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
    // Must cover claimStudentSchool cold-starting plus the forced ID-token refresh.
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

  it('ignores a corrupt marker rather than trusting it', () => {
    window.sessionStorage.setItem(KEY, 'not-a-number');
    expect(isRegistrationProvisioning()).toBe(false);
  });

  it('ignores a marker stamped in the future', () => {
    beginRegistrationProvisioning(2_000_000);
    expect(isRegistrationProvisioning(1_000_000)).toBe(false);
  });

  it('does not collide with the staff marker', () => {
    // The two holds are independent: a staff claim must not suppress the
    // student gate, and vice versa.
    window.sessionStorage.setItem('nsu:staff-provisioning', String(1_000_000));
    expect(isRegistrationProvisioning(1_000_000)).toBe(false);
  });
});
