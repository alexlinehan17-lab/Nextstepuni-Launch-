/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Ways In turns a question into planning rows, and the count comes only from
 * wording the paper itself prints. Two failures are pinned here.
 *
 * The one that shipped: the pattern admitted only `distinct` and `different`
 * between the number and its noun, but papers write "two possible economic
 * effects", "three safety precautions", "two other factors". 380 cards across
 * nine subjects printed their own answer count and got a single row anyway —
 * 109 of them in Economics, whose house style is exactly that construction.
 *
 * The one that must never ship: a measurement is not an answer count. "Correct
 * to two decimal places" and "the first 2.5 minutes" print a number in front of
 * a noun and mean nothing of the kind. The noun allowlist is the whole defence,
 * so the measurement cases below are the ones worth failing loudly.
 */
import { describe, expect, it } from 'vitest';

import { findPrintedPlanShape } from '@/components/WaysIn/questionModel';

const count = (text: string) => findPrintedPlanShape(text);

describe('printed answer counts', () => {
  it('reads a count through the modifiers papers actually use', () => {
    expect(count('Outline two positive impacts of globalisation.')).toMatchObject({ count: 2, basis: 'printed' });
    expect(count('Outline two possible advantages to Ireland of remaining a member of the EU.')).toMatchObject({ count: 2 });
    expect(count('Outline two economic measures that could be taken by the Irish government.')).toMatchObject({ count: 2 });
    expect(count('Outline three safety precautions he should take when spreading the slurry.')).toMatchObject({ count: 3 });
    expect(count('Discuss four guidelines consumers should follow to reduce household costs.')).toMatchObject({ count: 4 });
  });

  it('sums separate demands made under one instruction', () => {
    // Two asks, so two rows. Before, only the half whose noun happened to be
    // listed was seen, and the question planned as one.
    expect(count('Describe one benefit and one challenge of privatisation for the government.'))
      .toMatchObject({ count: 2, basis: 'printed' });
    expect(count('Briefly describe two advantages and two disadvantages of Artificial Insemination in cattle.'))
      .toMatchObject({ count: 4, basis: 'printed' });
  });

  it('never mistakes a measurement for an answer count', () => {
    expect(count('Calculate, correct to two decimal places, the pH of the solution.').basis).toBe('flexible');
    expect(count('Would you expect the average rate over the first 2.5 minutes to increase?').basis).toBe('flexible');
    expect(count('The image of the cell was 2 cm wide. What is the actual width of this cell?').basis).toBe('flexible');
    expect(count('Fill in the three missing values to complete the table above').basis).toBe('flexible');
  });

  it('still refuses to read a count off a subject rather than an answer', () => {
    // "the two stages" names what the question is about; the ask is one
    // difference. The preceding-word guard has to keep catching this now that
    // `stages` is a counted noun.
    expect(count('Describe the difference between the two stages in terms of energy released.').basis).toBe('flexible');
  });

  it('keeps preferring the selectable set in a nested count', () => {
    expect(count('Suggest one reason for any three treatments listed above.'))
      .toMatchObject({ count: 3, basis: 'printed' });
  });

  it('does not let a greedy modifier run swallow the noun it counts', () => {
    // Regression: `two functions of product` matched with "functions of" as
    // modifiers and `product` as the noun, and rejecting that lost the plain
    // `two functions` underneath it.
    expect(count('Outline two functions of product packaging.')).toMatchObject({ count: 2, basis: 'printed' });
    expect(count('Name one factor that causes the pulse rate to increase:')).toMatchObject({ count: 1, basis: 'printed' });
  });
});
