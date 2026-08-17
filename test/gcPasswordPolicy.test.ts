/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * adminResetGcPassword sets someone else's password, so a flaw here is account
 * takeover. The callable enforces two limits — caller is the administrator,
 * target is a gc-*@nextstep.app address — and this pins the second, which is
 * what stops the administrator (or anyone who reaches that path) from seizing
 * a student's or teacher's account and reading their work as them.
 */
import { describe, expect, it } from 'vitest';

import {
  PASSWORD_ALPHABET,
  PASSWORD_LENGTH,
  SCHOOL_NAMES,
  buildPassword,
  gcAddressToReset,
  isResettableGcAddress,
  schoolIdFromGcAddress,
} from '@/functions/src/gcPasswordPolicy';
import { SCHOOLS } from '@/schoolData';

describe('gc password reset targets', () => {
  it('allows a guidance-counsellor login for every school', () => {
    for (const id of ['marino', 'joeys', 'larkin', 'oconnells', 'mountcarmel', 'rosmini', 'pwc']) {
      expect(isResettableGcAddress(`gc-${id}@nextstep.app`), id).toBe(true);
    }
  });

  it('refuses the administrator account, live and retired', () => {
    expect(isResettableGcAddress('nextstepuniinfo@gmail.com')).toBe(false);
    expect(isResettableGcAddress('NextStepUniInfo@Gmail.com')).toBe(false);
    expect(isResettableGcAddress('admin@nextstep.app')).toBe(false);
    expect(isResettableGcAddress('ADMIN@nextstep.app')).toBe(false);
  });

  it('refuses students and teachers', () => {
    expect(isResettableGcAddress('student@gmail.com')).toBe(false);
    expect(isResettableGcAddress('teacher@school.ie')).toBe(false);
    expect(isResettableGcAddress('alexlinehan17@gmail.com')).toBe(false);
  });

  it('refuses near-misses rather than guessing', () => {
    expect(isResettableGcAddress('gc-marino@nextstep.app.evil.com')).toBe(false);
    expect(isResettableGcAddress('xgc-marino@nextstep.app')).toBe(false);
    expect(isResettableGcAddress('gc-@nextstep.app')).toBe(false);
    expect(isResettableGcAddress('gc-marino@nextstepapp')).toBe(false);
    expect(isResettableGcAddress('gc-marino@notnextstep.app')).toBe(false);
    expect(isResettableGcAddress('')).toBe(false);
    expect(isResettableGcAddress(undefined)).toBe(false);
    expect(isResettableGcAddress(42)).toBe(false);
  });

  it('normalises case and spacing before use', () => {
    expect(gcAddressToReset('  GC-Marino@NextStep.app ')).toBe('gc-marino@nextstep.app');
    expect(gcAddressToReset('student@gmail.com')).toBeNull();
  });
});

describe('generated password', () => {
  it('is the declared length, from the unambiguous alphabet', () => {
    let n = 0;
    const password = buildPassword(max => (n++) % max);
    expect(password).toHaveLength(PASSWORD_LENGTH);
    for (const character of password) expect(PASSWORD_ALPHABET).toContain(character);
  });

  it('omits glyphs that are misread down a phone', () => {
    // These get read aloud to a counsellor; O/0 and I/1/l cost a support call.
    for (const ambiguous of ['O', '0', 'I', '1', 'l', 'L']) {
      expect(PASSWORD_ALPHABET).not.toContain(ambiguous);
    }
  });

  it('is long enough for an account that opens a whole school', () => {
    // Longer than the 8-character student temp password: there is no
    // forced-change-on-first-use behind a GC login.
    expect(PASSWORD_LENGTH).toBeGreaterThanOrEqual(12);
  });
});

describe('provisioning a counsellor identity', () => {
  it('extracts the school a login belongs to', () => {
    expect(schoolIdFromGcAddress('gc-marino@nextstep.app')).toBe('marino');
    expect(schoolIdFromGcAddress('GC-MountCarmel@NextStep.app')).toBe('mountcarmel');
  });

  it('extracts nothing from an address it must not touch', () => {
    // Guards the provisioning write as well as the password: no school id
    // means no role:'gc' is ever stamped on a non-counsellor account.
    expect(schoolIdFromGcAddress('student@gmail.com')).toBeNull();
    expect(schoolIdFromGcAddress('nextstepuniinfo@gmail.com')).toBeNull();
    expect(schoolIdFromGcAddress('admin@nextstep.app')).toBeNull();
  });

  it('has a display name for every school in the picker', () => {
    // A counsellor with no name yet is seeded "<School> Guidance", and that
    // name is stamped on everything they send a student.
    for (const school of SCHOOLS) {
      expect(SCHOOL_NAMES[school.id], school.id).toBe(school.name);
    }
    expect(Object.keys(SCHOOL_NAMES).sort()).toEqual([...SCHOOLS].map(s => s.id).sort());
  });
});
