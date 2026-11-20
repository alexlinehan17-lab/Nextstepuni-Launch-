/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The marking-grid gate's two additions (build-deck.mjs spanishGridFault):
 * an ADDED scheme form with the marks cells kept in place, for grids that
 * print their marks only there (Portuguese 2023 Higher scheme p10), and the
 * rule that a band named only by its printed range carries exactly that range.
 */

import { describe, expect, test } from 'vitest';
import { readFileSync } from 'node:fs';
import {
  claimMatches,
  comparableScheme,
  comparableSchemeWithCells,
  rangeLabelFault,
} from '../scripts/markbank/schemeText.mjs';

const raw = readFileSync('examiner-reports/portuguese/schemes/2023-hl.md', 'utf8');

describe('the scheme with its marks cells kept', () => {
  test('traces grid lines whose marks are printed only in cells, which the plain form cannot', () => {
    const plain = comparableScheme(raw);
    const cells = comparableSchemeWithCells(raw);
    for (const line of [
      'Did not follow the requested structure/format. -1 mark',
      'Commented the theme, followed requested structure/format and gave information on all topics. 4 marks',
      '10 - 13',
    ]) {
      expect(claimMatches(plain, line), line).toBe(false);
      expect(claimMatches(cells, line), line).toBe(true);
    }
  });

  test('only adds: everything the plain form traces, the cells form traces too', () => {
    const cells = comparableSchemeWithCells(raw);
    for (const line of [
      'Did not follow the requested structure/format.',
      'Logical and well-structured text',
      'Commented the theme, followed requested structure/format but only gave information on 2 topics.',
    ]) {
      expect(claimMatches(comparableScheme(raw), line), line).toBe(true);
      expect(claimMatches(cells, line), line).toBe(true);
    }
  });
});

describe('a band named only by its printed range', () => {
  test('passes when its marks are exactly that range', () => {
    expect(rangeLabelFault({ label: '10 - 13', marks: [10, 11, 12, 13] })).toBeNull();
    expect(rangeLabelFault({ label: '2 - 3', marks: [2, 3] })).toBeNull();
    expect(rangeLabelFault({ label: '4', marks: [4] })).toBeNull();
  });

  test('fails when its marks differ from the range it prints', () => {
    expect(rangeLabelFault({ label: '10 - 13', marks: [9, 10, 11, 12, 13] })).toMatch(/not the 10-13/);
    expect(rangeLabelFault({ label: '4', marks: [3, 4] })).toMatch(/not the 4-4/);
  });

  test('leaves a band with a printed name alone', () => {
    expect(rangeLabelFault({ label: 'TOP', marks: [11, 12, 13, 14, 15] })).toBeNull();
    expect(rangeLabelFault({ label: 'Very good', marks: [12, 13, 14, 15] })).toBeNull();
  });
});
