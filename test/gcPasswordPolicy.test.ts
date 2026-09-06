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

import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

import {
  MIN_SUPPLIED_PASSWORD_LENGTH,
  PASSWORD_ALPHABET,
  PASSWORD_LENGTH,
  SCHOOL_NAMES,
  checkSuppliedPassword,
  buildPassword,
  gcAddressToReset,
  isResettableGcAddress,
  schoolIdFromGcAddress,
  schoolLoginToReset,
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
    // A shared school credential needs substantial entropy even though a GC
    // rotation does not use the student's forced-change-on-first-use flow.
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

describe('an administrator-typed password', () => {
  it('accepts a long enough one exactly as typed', () => {
    // Not trimmed: spaces are legitimate characters, and silently altering the
    // input would mean the password written down is not the one that was set.
    expect(checkSuppliedPassword('correct horse battery')).toEqual({
      ok: true, password: 'correct horse battery',
    });
    expect(checkSuppliedPassword(' padded1234 ')).toEqual({ ok: true, password: ' padded1234 ' });
  });

  it('rejects one that is too short for an account that opens a school', () => {
    expect(checkSuppliedPassword('short').ok).toBe(false);
    expect(checkSuppliedPassword('a'.repeat(MIN_SUPPLIED_PASSWORD_LENGTH - 1)).ok).toBe(false);
    expect(checkSuppliedPassword('a'.repeat(MIN_SUPPLIED_PASSWORD_LENGTH)).ok).toBe(true);
  });

  it('rejects blank, absurd and non-string input', () => {
    expect(checkSuppliedPassword('           ')).toEqual({ ok: false, reason: 'blank' });
    expect(checkSuppliedPassword('a'.repeat(200))).toEqual({ ok: false, reason: 'long' });
    expect(checkSuppliedPassword(undefined)).toEqual({ ok: false, reason: 'type' });
    expect(checkSuppliedPassword(12345678901)).toEqual({ ok: false, reason: 'type' });
  });

  it('is comfortably above Firebase\'s own 6-character floor', () => {
    expect(MIN_SUPPLIED_PASSWORD_LENGTH).toBeGreaterThanOrEqual(12);
  });

  it('agrees with the copy of the rule in the admin panel', () => {
    // The panel duplicates the constant so the client never imports server
    // code. A drift would show the typist one rule and enforce another.
    const panel = readFileSync(
      resolve(__dirname, '..', 'components', 'AdminGcAccessPanel.tsx'), 'utf8',
    );
    expect(panel).toContain(`const MIN_SUPPLIED_PASSWORD_LENGTH = ${MIN_SUPPLIED_PASSWORD_LENGTH};`);
  });
});

describe('the admin panel reports what actually happened', () => {
  const panel = readFileSync(
    resolve(__dirname, '..', 'components', 'AdminGcAccessPanel.tsx'), 'utf8',
  );

  it('decides "set as typed" from the response, not from the request', () => {
    // Hosting and functions deploy as separate CI jobs, so the client can be
    // newer than the callable for a few minutes. An older callable ignores the
    // supplied password and returns no `generated` field; trusting that field
    // reported "set as typed" for a password the server had generated —
    // which ends with a school being handed a password that does not work.
    expect(panel).toContain('const setAsTyped = password !== undefined && returned === password;');
    expect(panel, 'must not trust the server flag alone')
      .not.toMatch(/generated:\s*response\.data\.generated\s*,/);
  });

  it('tells the administrator when their typed password was not used', () => {
    expect(panel).toContain('The server generated a password instead');
  });
});

describe('school login reset targets (gc and staff)', () => {
  it('resolves both shared logins for every school', () => {
    for (const id of ['marino', 'joeys', 'larkin', 'oconnells', 'mountcarmel', 'rosmini', 'pwc']) {
      expect(schoolLoginToReset(`gc-${id}@nextstep.app`)).toEqual({
        address: `gc-${id}@nextstep.app`, kind: 'gc', schoolId: id,
      });
      expect(schoolLoginToReset(`staff-${id}@nextstep.app`)).toEqual({
        address: `staff-${id}@nextstep.app`, kind: 'staff', schoolId: id,
      });
    }
  });

  it('normalises case and spacing like the gc-only path', () => {
    expect(schoolLoginToReset('  STAFF-Marino@NextStep.app ')).toEqual({
      address: 'staff-marino@nextstep.app', kind: 'staff', schoolId: 'marino',
    });
  });

  it('refuses the administrator accounts', () => {
    expect(schoolLoginToReset('nextstepuniinfo@gmail.com')).toBe(null);
    expect(schoolLoginToReset('admin@nextstep.app')).toBe(null);
  });

  it("refuses students, teachers' own accounts, and near-misses", () => {
    expect(schoolLoginToReset('teacher@school.ie')).toBe(null);
    expect(schoolLoginToReset('student@gmail.com')).toBe(null);
    expect(schoolLoginToReset('staff-marino@nextstep.app.evil.com')).toBe(null);
    expect(schoolLoginToReset('xstaff-marino@nextstep.app')).toBe(null);
    expect(schoolLoginToReset('staff-@nextstep.app')).toBe(null);
    expect(schoolLoginToReset('staffmarino@nextstep.app')).toBe(null);
    expect(schoolLoginToReset('')).toBe(null);
    expect(schoolLoginToReset(undefined)).toBe(null);
    expect(schoolLoginToReset(42)).toBe(null);
  });

  it('agrees with the gc-only validator on every gc address', () => {
    for (const address of ['gc-marino@nextstep.app', 'gc-@nextstep.app', 'gc-marino@notnextstep.app']) {
      expect(schoolLoginToReset(address) !== null).toBe(isResettableGcAddress(address));
    }
  });
});
