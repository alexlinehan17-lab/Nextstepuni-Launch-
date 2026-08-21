/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Mark Bank build and the shipped-deck check must agree on what a
 * content-free row is. They had separate copies of the rule and had already
 * drifted in BOTH directions, so a row of the wrong shape would have been
 * written by a build that accepted it into a suite that rejected it. This holds
 * the two together.
 */
import { describe, expect, it } from 'vitest';

import { isContentFreeRow as buildRule } from '../scripts/markbank/contentFree.mjs';
import { isContentFreeRow as deckRule } from '../types/markBank';

/** Every opening either implementation has ever claimed, plus real rows. */
const CORPUS = [
  '',
  '   ',
  'Named piece of apparatus used (other than the tissue or membrane)',
  'Named piece of apparatus',
  'Control named and setup described',
  'Control named',
  'Safety precaution described',
  'Correct sketch',
  'Correct matching result',
  'Matching result for test',
  'Correct position',
  'Correct position described',
  'Correct position of leaf (or leaf disc) on lid or described',
  'Suitable time',
  'Suitable temperature.',
  'Suitable volume',
  'Left for a time',
  'Left for a suitable time',
  'Any correct animal organ, e.g. heart or lung or brain, etc.',
  'The description earns 4 marks.',
  'Description how tissue or membrane was prepared',
  '3 marks',
  '2 items, 3 marks each',
  '4 points, 2 marks each.',
  'Three items, 2 marks each.',
  'Two points, 3 marks each',
  'Six answers, 2 marks each.',
  // Real marking points, which must stay content-BEARING.
  'Xylem (tracheid or vessel) or phloem or sieve tube or companion (cell)',
  'Correct use of salt or sugar (solution).',
  'Transcription',
  'Nuclear pore',
  'Shock absorber or protects bone or reduces friction',
  '17 °C to 32 °C',
  'Uncontrolled cell division',
  'Any three of the following, 2 marks each: heart, lung, brain',
];

describe('content-free row rule', () => {
  it('is the same rule in the build and in the shipped-deck check', () => {
    for (const row of CORPUS) {
      expect(`${row} -> ${buildRule(row)}`).toBe(`${row} -> ${deckRule(row)}`);
    }
  });

  it('rejects a bare criterion but keeps one that names the thing', () => {
    expect(buildRule('Correct position')).toBe(true);
    expect(buildRule('Correct position described')).toBe(true);
    expect(buildRule('Correct position of leaf (or leaf disc) on lid or described')).toBe(false);
  });

  it('rejects a tariff written where an answer should be, in digits or words', () => {
    expect(buildRule('2 items, 3 marks each')).toBe(true);
    expect(buildRule('Three items, 2 marks each.')).toBe(true);
    expect(buildRule('Two points, 3 marks each')).toBe(true);
  });

  it('keeps rows that state an answer', () => {
    expect(buildRule('Transcription')).toBe(false);
    expect(buildRule('Correct use of salt or sugar (solution).')).toBe(false);
    expect(buildRule('Shock absorber or protects bone or reduces friction')).toBe(false);
  });
});
