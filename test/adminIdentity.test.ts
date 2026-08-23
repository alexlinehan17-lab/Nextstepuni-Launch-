/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The administrator identity decides who can read every student's record, so
 * it is defined once and checked against the verified auth email.
 *
 * The reason it moved off admin@nextstep.app (2026-08-17): that domain has no
 * mailbox, so the password could never be reset and a lost password meant the
 * owner was permanently locked out of the feedback inbox, the launch funnel and
 * counsellor-login recovery. It is now an address the owner actually receives
 * mail at.
 *
 * Three definitions have to agree — this file, functions/src/adminIdentity.ts,
 * and firestore.rules `isAdmin()`. The last one is the load-bearing one, and
 * test/rules/firebaseRules.test.ts imports ADMIN_EMAIL from here so a change in
 * one cannot silently diverge from the database.
 */
import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

import {
  ADMIN_EMAIL,
  isAdminEmail,
  isReservedEmail,
  isVerifiedAdminSession,
} from '@/utils/adminIdentity';

const root = resolve(__dirname, '..');
const read = (p: string) => readFileSync(resolve(root, p), 'utf8');

describe('admin identity', () => {
  it('is a real, resettable mailbox — not an address at a domain with no inbox', () => {
    expect(ADMIN_EMAIL).toBe('nextstepuniinfo@gmail.com');
    expect(ADMIN_EMAIL).not.toMatch(/@nextstep\.app$/);
  });

  it('recognises the administrator, whatever the casing', () => {
    expect(isAdminEmail(ADMIN_EMAIL)).toBe(true);
    expect(isAdminEmail('NextStepUniInfo@Gmail.com')).toBe(true);
    expect(isAdminEmail('  nextstepuniinfo@gmail.com  ')).toBe(true);
  });

  it('requires the exact verified mailbox and a server-issued admin claim', () => {
    const verifiedUser = { email: ADMIN_EMAIL, emailVerified: true };
    expect(isVerifiedAdminSession(verifiedUser, { admin: true })).toBe(true);
    expect(isVerifiedAdminSession(verifiedUser, {})).toBe(false);
    expect(isVerifiedAdminSession({ ...verifiedUser, emailVerified: false }, { admin: true })).toBe(false);
    expect(isVerifiedAdminSession({ email: 'admin@nextstep.app', emailVerified: true }, { admin: true })).toBe(false);
  });

  it('grants nothing to the retired address or to look-alikes', () => {
    expect(isAdminEmail('admin@nextstep.app')).toBe(false);
    expect(isAdminEmail('nextstepuniinfo@gmail.com.evil.com')).toBe(false);
    expect(isAdminEmail('nextstepuniinfo@gmail.co')).toBe(false);
    expect(isAdminEmail('xnextstepuniinfo@gmail.com')).toBe(false);
    expect(isAdminEmail('')).toBe(false);
    expect(isAdminEmail(null)).toBe(false);
    expect(isAdminEmail(undefined)).toBe(false);
  });

  it('keeps the administrator and provisioned logins unregisterable', () => {
    expect(isReservedEmail(ADMIN_EMAIL)).toBe(true);
    // Still reserved though no longer privileged — the Auth account exists.
    expect(isReservedEmail('admin@nextstep.app')).toBe(true);
    expect(isReservedEmail('gc-marino@nextstep.app')).toBe(true);
    expect(isReservedEmail('gc-pwc@nextstep.app')).toBe(true);
    expect(isReservedEmail('student@gmail.com')).toBe(false);
  });

  it('agrees with the two definitions that are not this one', () => {
    // A mismatch here means the UI offers something the database refuses, or
    // worse, the database allows someone the UI does not show as admin.
    expect(read('functions/src/adminIdentity.ts')).toContain(ADMIN_EMAIL);
    expect(read('firestore.rules')).toContain(`request.auth.token.email == '${ADMIN_EMAIL}'`);
    expect(read('firestore.rules')).toContain('request.auth.token.admin == true');
    expect(read('firestore.rules')).toContain('request.auth.token.email_verified == true');
  });

  it('leaves no hardcoded admin check outside the shared helpers', () => {
    // Every privileged check must route through isAdminEmail()/isAdmin(), so a
    // future identity change is one edit rather than twenty.
    for (const file of [
      'contexts/AuthContext.tsx',
      'components/LoginPage.tsx',
      'functions/src/dataRights.ts',
      'functions/src/staffAccess.ts',
      'functions/src/schoolAccess.ts',
      'functions/src/gcPasswordReset.ts',
    ]) {
      const source = read(file).replace(/^\s*(\/\/|\*).*$/gm, ''); // ignore comments
      expect(source, `${file} still compares an admin address inline`)
        .not.toMatch(/email\s*[=!]==?\s*["']admin@nextstep\.app["']/);
    }
  });
});
