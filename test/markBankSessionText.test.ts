/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Mark Bank session screen's own wording (components/MarkBank/sessionText.ts).
 */

import { describe, expect, test } from 'vitest';
import { anyNHeading, marksWord } from '@/components/MarkBank/sessionText';

describe('an any-N menu states its price in good English', () => {
  test('one mark each is singular', () => {
    // Shipped as "Any 2 of these — 1 marks each" on every one-mark menu.
    expect(anyNHeading({ claimMax: 2, perOption: 1, options: ['a', 'b', 'c'] })).toBe('Any 2 of these — 1 mark each');
    expect(anyNHeading({ claimMax: 3, perOption: 1, options: ['a', 'b', 'c'] })).toBe('All 3 of these — 1 mark each');
  });

  test('more than one mark each stays plural', () => {
    expect(anyNHeading({ claimMax: 4, perOption: 3, options: ['a', 'b', 'c', 'd', 'e'] })).toBe('Any 4 of these — 3 marks each');
  });

  test('a descending tariff is stated as it is paid, and a single step of one is singular', () => {
    expect(anyNHeading({ claimMax: 2, perOption: 6, perOptionSteps: [6, 4], options: ['a', 'b', 'c'] })).toBe('Any 2 of these — 6 then 4 marks');
    expect(anyNHeading({ claimMax: 1, perOption: 1, perOptionSteps: [1], options: ['a', 'b'] })).toBe('Any 1 of these — 1 mark');
  });

  test('a menu priced only as a whole states the choice alone', () => {
    expect(anyNHeading({ claimMax: 2, options: ['a', 'b', 'c'] } as never)).toBe('Any 2 of these');
  });

  test('marksWord', () => {
    expect([0, 1, 2].map(marksWord)).toEqual(['marks', 'mark', 'marks']);
  });
});
