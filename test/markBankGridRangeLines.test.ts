/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The marking-grid gate's band-range-line form (schemeText.mjs ADDED FORMS, 3):
 * the 2022 Portuguese schemes print each Communication band's range in a side
 * cell centred against a wrapped bullet (Higher p11), so the text layer sets
 * "10 - 13 marks" between the bullet's two halves.
 */

import { describe, expect, test } from 'vitest';
import { readFileSync } from 'node:fs';
import {
  claimMatches,
  comparableScheme,
  comparableSchemeWithoutRangeLines,
  rangeLabelFault,
} from '../scripts/markbank/schemeText.mjs';

const SPLIT = [
  'Comprehensible for Portuguese language native speaker although with a few mistakes',
  'Comprehensible for Portuguese language native speaker although with some mistakes',
  'Portuguese language native speaker would have difficulty understanding',
];

describe('the scheme with its band-range lines lifted out', () => {
  for (const level of ['hl', 'ol']) {
    test(`the three split bullets trace in it, and not in the plain form (2022 ${level})`, () => {
      const raw = readFileSync(`examiner-reports/portuguese/schemes/2022-${level}.md`, 'utf8');
      for (const line of SPLIT) {
        expect(claimMatches(comparableScheme(raw), line), line).toBe(false);
        expect(claimMatches(comparableSchemeWithoutRangeLines(raw), line), line).toBe(true);
      }
    });
  }

  test('a range inside a line of prose is untouched', () => {
    const raw = 'Answer\nAward 10 - 13 marks where the message is clear\nNext';
    expect(claimMatches(comparableSchemeWithoutRangeLines(raw), 'Award 10 - 13 marks where the message is clear')).toBe(true);
    expect(claimMatches(comparableSchemeWithoutRangeLines('Answer\n10 - 13 marks\nNext'), '10 - 13 marks')).toBe(false);
  });

  test('a band label printed as a range still traces in the plain form, as before', () => {
    const raw = readFileSync('examiner-reports/portuguese/schemes/2022-hl.md', 'utf8');
    expect(claimMatches(comparableScheme(raw), '10 - 13')).toBe(true);
    expect(claimMatches(comparableScheme(raw), '0 - 4')).toBe(true);
  });

  test('rangeLabelFault still holds a band named by a range to that range', () => {
    expect(rangeLabelFault({ label: '10 - 13', marks: [10, 11, 12, 13] })).toBeNull();
    expect(rangeLabelFault({ label: '10 - 13', marks: [9, 10, 11, 12, 13] })).toMatch(/not the 10-13/);
  });
});
