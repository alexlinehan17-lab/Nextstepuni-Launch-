/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The year-line added form of the scheme (schemeText.mjs comparableScheme):
 * a scheme line that is exactly a four-digit year, once its marks cell and the
 * page furniture are gone, traces on its own (2023 Portuguese Ordinary p6,
 * "2018 ⟨1 mark⟩"); every other single numeric line stays excluded as an
 * ambiguous mark or page cell.
 */

import { describe, expect, test } from 'vitest';
import { readFileSync } from 'node:fs';
import { claimMatches, comparableScheme } from '../scripts/markbank/schemeText.mjs';

describe('a scheme line that is only a year', () => {
  test('traces: Portuguese 2023 Ordinary Q2(a) "2018"', () => {
    const scheme = comparableScheme(readFileSync('examiner-reports/portuguese/schemes/2023-ol.md', 'utf8'));
    expect(claimMatches(scheme, '2018')).toBe(true);
  });

  test('traces once its marks cell is stripped', () => {
    expect(claimMatches(comparableScheme('Answer\n2018 ⟨1 mark⟩\nNext question'), '2018')).toBe(true);
    expect(claimMatches(comparableScheme('Answer\n1999\nNext question'), '1999')).toBe(true);
  });

  test('a single line of one to three digits still does not trace', () => {
    for (const n of ['7', '42', '123']) {
      expect(claimMatches(comparableScheme(`Answer\n${n} ⟨2 marks⟩\nNext question`), n), n).toBe(false);
    }
  });

  test('nothing longer than a year, and no other century, qualifies', () => {
    expect(claimMatches(comparableScheme('Answer\n12018\nNext question'), '12018')).toBe(false);
    expect(claimMatches(comparableScheme('Answer\n1850\nNext question'), '1850')).toBe(false);
  });
});
