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

  test('generates human-readable high-entropy codes', () => {
    const samples = Array.from({ length: 100 }, () => generateAccessCode());
    expect(new Set(samples).size).toBe(samples.length);
    for (const code of samples) {
      expect(code).toMatch(/^[A-HJ-KM-NP-Z2-9]{4}-[A-HJ-KM-NP-Z2-9]{4}-[A-HJ-KM-NP-Z2-9]{4}$/);
      expect(normaliseAccessCode(code)).toHaveLength(12);
    }
  });

  test('cannot embed a school name, by construction', () => {
    // This replaces a substring scan over random output, which flaked at about
    // 3% per CI run and blocked a deploy: 'pwc' is a real school id and only
    // three characters, so a 12-character code drawn from a 31-character
    // alphabet contains it by chance roughly once in thirty runs. Testing
    // randomness for the absence of a short string tests the wrong thing.
    //
    // What actually matters is that a code is not DERIVED from the school, the
    // way the pre-2026-08-23 scheme was. Two deterministic checks establish it:
    // the generator takes no school argument, so it structurally cannot embed
    // one; and repeated calls differ, which a school-derived code would not.
    expect(generateAccessCode.length).toBe(0);
    expect(new Set(Array.from({ length: 50 }, () => generateAccessCode())).size).toBe(50);

    // Longer ids are still worth scanning: a chance collision on five or more
    // characters is about one run in thirty thousand, so a hit would be a real
    // signal rather than noise.
    const scannable = SCHOOLS.map(s => s.id).filter(id => id.length >= 5);
    expect(scannable.length).toBeGreaterThan(0);
    for (const code of Array.from({ length: 100 }, () => generateAccessCode())) {
      for (const id of scannable) expect(code.toLowerCase()).not.toContain(id);
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
