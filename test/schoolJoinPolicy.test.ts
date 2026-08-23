/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import { describe, expect, test } from 'vitest';

import { SCHOOLS } from '@/schoolData';
import {
  SUPPORTED_SCHOOL_IDS,
  isSupportedSchoolId,
} from '@/functions/src/schoolJoinPolicy';
import {
  generateAccessCode,
  hashAccessCode,
  normaliseAccessCode,
  safeHashEqual,
} from '@/functions/src/accessCodes';

describe('school access policy', () => {
  test('the server allowlist stays aligned with the school picker', () => {
    expect([...SUPPORTED_SCHOOL_IDS].sort()).toEqual(SCHOOLS.map(school => school.id).sort());
  });

  test('accepts only canonical school identifiers', () => {
    for (const school of SCHOOLS) expect(isSupportedSchoolId(school.id)).toBe(true);
    expect(isSupportedSchoolId('Marino')).toBe(false);
    expect(isSupportedSchoolId('unknown-school')).toBe(false);
    expect(isSupportedSchoolId('')).toBe(false);
    expect(isSupportedSchoolId(null)).toBe(false);
  });

  test('generates human-readable high-entropy codes without embedding school names', () => {
    const samples = Array.from({ length: 100 }, () => generateAccessCode());
    expect(new Set(samples).size).toBe(samples.length);
    for (const code of samples) {
      expect(code).toMatch(/^[A-HJ-KM-NP-Z2-9]{4}-[A-HJ-KM-NP-Z2-9]{4}-[A-HJ-KM-NP-Z2-9]{4}$/);
      expect(normaliseAccessCode(code)).toHaveLength(12);
      expect(code.toLowerCase()).not.toMatch(/marino|joeys|larkin|pwc/);
    }
  });

  test('compares only one-way hashes and tolerates printed separators', () => {
    const hash = hashAccessCode('ABCD-EFGH-JK23');
    expect(hash).toMatch(/^[a-f0-9]{64}$/);
    expect(hash).not.toContain('ABCD');
    expect(safeHashEqual(hash, hashAccessCode('abcd efgh jk23'))).toBe(true);
    expect(safeHashEqual(hash, hashAccessCode('ABCD-EFGH-JK24'))).toBe(false);
  });
});
