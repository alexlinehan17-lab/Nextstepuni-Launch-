/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The source reader names the document its pages come from (illustrationDocument).
 */

import { describe, expect, test } from 'vitest';

import { illustrationDocument } from '@/components/MarkBank/SourceMaterialReader';

describe('the source reader names the document its pages come from', () => {
  test('a page of the card\'s own question paper is the question paper, in any subject', () => {
    // Economics, Agricultural Science and the sciences were all called an "illustration sheet".
    expect(illustrationDocument('economics', { label: 'OFFICIAL QUESTION PAGE' })).toBe('question paper');
    expect(illustrationDocument('geography', { label: 'PART 1 · Q1' })).toBe('question paper');
    expect(illustrationDocument('economics', { label: 'IRISH QUESTION PAGE', sourceFileid: 'LC034ALP000IV' })).toBe('question paper');
  });

  test('a separate companion is named by subject', () => {
    expect(illustrationDocument('art', { label: 'ILLUSTRATION SHEET · Q2', sourceFileid: 'LC014ALP004EV' })).toBe('illustration sheet');
    expect(illustrationDocument('classical-studies', { label: 'PAPER X — Photograph E', sourceFileid: 'LC008ALP004EV' })).toBe('Paper X');
    expect(illustrationDocument('geography', { label: 'OS MAP', sourceFileid: 'LC005CLP003EV' })).toBe('OS map');
    expect(illustrationDocument('geography', { label: 'AERIAL PHOTOGRAPH', sourceFileid: 'LC005CLP004EV' })).toBe('aerial photograph');
    expect(illustrationDocument('geography', { label: 'MAP LEGEND', sourceFileid: 'LC005CLPC00EV' })).toBe('map legend');
  });
});
