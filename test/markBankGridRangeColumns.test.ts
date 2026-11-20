/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The grid gate's band-range form (schemeText.mjs ADDED FORMS, 3), case (b):
 * a line whose END is exactly two range pairs after prose -- a band's Full
 * Scale and Lower Scale columns -- has the pairs cut off, so a bullet wrapped
 * after them reads whole (Portuguese 2026 Higher p10 lines 251/256/261, p11
 * lines 287/292/297). One trailing pair is never cut.
 */

import { describe, expect, test } from 'vitest';
import { readFileSync } from 'node:fs';
import {
  claimMatches,
  comparableScheme,
  comparableSchemeWithCells,
  comparableSchemeWithoutRangeLines,
} from '../scripts/markbank/schemeText.mjs';

const raw = readFileSync('examiner-reports/portuguese/schemes/2026-hl.md', 'utf8');
const SPLIT = [
  'Verb endings, tenses, agreements (number, gender, etc.) nearly always correct.',
  'Verb endings, tenses, agreements (number, gender, etc.) occasionally incorrect.',
  'Verb endings, tenses, agreements (number, gender, etc.) generally incorrect.',
];

describe('two trailing range columns cut off a line', () => {
  test('the three 2026 Higher Language descriptors trace in form 3, and in neither the plain nor the cells form', () => {
    for (const line of SPLIT) {
      expect(claimMatches(comparableScheme(raw), line), line).toBe(false);
      expect(claimMatches(comparableSchemeWithCells(raw), line), line).toBe(false);
      expect(claimMatches(comparableSchemeWithoutRangeLines(raw), line), line).toBe(true);
    }
  });

  test('a line ending in ONE range pair is untouched', () => {
    const one = 'Answer\nVery good use of language 11 – 15\nand of tenses\nNext';
    const form = comparableSchemeWithoutRangeLines(one);
    expect(claimMatches(form, 'Very good use of language and of tenses')).toBe(false);
    expect(claimMatches(form, 'Very good use of language 11 – 15')).toBe(true);
  });

  test('a line ending in three or four pairs is untouched', () => {
    const three = comparableSchemeWithoutRangeLines('Answer\nLower Ex. If C ≤ 7 Total = 7 0 - 2 3 - 5 6 - 7\nnext words\nNext');
    expect(claimMatches(three, 'Lower Ex. If C ≤ 7 Total = 7 0 - 2 3 - 5 6 - 7')).toBe(true);
    expect(claimMatches(three, 'Total = 7 0 - 2 next words')).toBe(false);
    const four = comparableSchemeWithoutRangeLines('Answer\nBands 16 – 21 10 – 15 4 - 9 0 - 3\nnext words\nNext');
    expect(claimMatches(four, 'Bands 16 – 21 10 – 15 4 - 9 0 - 3')).toBe(true);
    expect(claimMatches(four, 'Bands 16 – 21 10 – 15 next words')).toBe(false);
  });

  test('a range-only "N - M marks" line is still lifted', () => {
    const form = comparableSchemeWithoutRangeLines('Answer\nComprehensible although\n10 - 13 marks\nwith a few mistakes\nNext');
    expect(claimMatches(form, 'Comprehensible although with a few mistakes')).toBe(true);
  });

  test('a range inside a line of prose is untouched', () => {
    const form = comparableSchemeWithoutRangeLines('Answer\nAward 11 – 15 8 – 10 marks where the text is clear\nNext');
    expect(claimMatches(form, 'Award 11 – 15 8 – 10 marks where the text is clear')).toBe(true);
  });
});
