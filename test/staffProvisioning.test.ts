/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The marker that stops a teacher being shown student onboarding while their
 * staff claim is still in flight. Two properties matter and pull against each
 * other: it must hold long enough to cover a cold-start callable, and it must
 * never outlive a failed attempt — a stuck marker would leave a genuine
 * student staring at a spinner instead of onboarding.
 */
import { describe, expect, it, beforeEach } from 'vitest';

import {
  beginStaffProvisioning,
  endStaffProvisioning,
  isStaffProvisioning,
} from '@/utils/staffProvisioning';

const MINUTE = 60_000;

describe('staff provisioning marker', () => {
  beforeEach(() => {
    window.sessionStorage.clear();
  });

  it('is off by default, so students are never held back', () => {
    expect(isStaffProvisioning()).toBe(false);
  });

  it('holds while the claim is in flight', () => {
    const start = 1_000_000;
    beginStaffProvisioning(start);
    expect(isStaffProvisioning(start)).toBe(true);
    // Comfortably covers the 8s user-doc wait plus a cold-start callable.
    expect(isStaffProvisioning(start + 30_000)).toBe(true);
  });

  it('is released when the claim resolves', () => {
    beginStaffProvisioning(1_000_000);
    endStaffProvisioning();
    expect(isStaffProvisioning(1_000_000)).toBe(false);
  });

  it('self-expires, so a crashed attempt cannot strand a later student', () => {
    const start = 1_000_000;
    beginStaffProvisioning(start);
    expect(isStaffProvisioning(start + 2 * MINUTE)).toBe(false);
    // And the expired marker is cleaned up rather than re-checked forever.
    expect(window.sessionStorage.getItem('nsu:staff-provisioning')).toBeNull();
  });

  it('ignores a corrupt marker rather than trusting it', () => {
    window.sessionStorage.setItem('nsu:staff-provisioning', 'not-a-number');
    expect(isStaffProvisioning()).toBe(false);
  });

  it('ignores a marker stamped in the future', () => {
    // Clock changes and restored sessions can produce this; treat as invalid
    // rather than holding the app indefinitely.
    beginStaffProvisioning(2_000_000);
    expect(isStaffProvisioning(1_000_000)).toBe(false);
  });
});
