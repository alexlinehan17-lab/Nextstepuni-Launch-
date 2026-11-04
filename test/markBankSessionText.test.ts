/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Mark Bank session screen's own wording (components/MarkBank/sessionText.ts).
 */

import { describe, expect, test } from 'vitest';
import { anyNHeading, marksWord, unclaimedName, UNCLAIMED_NAME_MAX } from '@/components/MarkBank/sessionText';

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

describe('the "Not claimed yet" band names each row sensibly', () => {
  test('working keeps its minus signs (Economics 2023 HL Section A Q4(a))', () => {
    // Shipped as "82 = 26 • 152 ÷ 4 = 38 • 152 – 108 = 44": everything after the last " - ".
    expect(unclaimedName('• 82 ÷ 2 = 41 • 108 - 82 = 26 • 152 ÷ 4 = 38 • 152 – 108 = 44'))
      .toBe('82 ÷ 2 = 41 • 108 - 82 = 26 • 152 ÷ 4 = 38 • 152 – 108 = 44');
    expect(unclaimedName('x² ÷ (2.5 - x)² = 1')).toBe('x² ÷ (2.5 - x)² = 1');
  });

  test('a long text row starts where the scheme starts and is cut at a word (Engineering 2021 HL Q1(c))', () => {
    // Shipped as "1951) was an Austrian-German automotive engineer …".
    const name = unclaimedName('Ferdinand Porsche (1875 - 1951) was an Austrian-German automotive engineer and founder of the Porsche car company. He is best known for creating the first gasoline-electric hybrid vehicle');
    expect(name.startsWith('Ferdinand Porsche (1875 - 1951) was an')).toBe(true);
    expect(name.endsWith('…')).toBe(true);
    expect(name.length).toBeLessThanOrEqual(UNCLAIMED_NAME_MAX + 1);
    expect(name).not.toMatch(/\s…$/);
  });

  test('a single "Label — " prefix is still stripped', () => {
    expect(unclaimedName('Scald — Inflammation (of the skin between the digits)')).toBe('Inflammation (of the skin between the digits)');
    expect(unclaimedName('Low prices - the firm sells its products at the lowest possible prices.')).toBe('the firm sells its products at the lowest possible prices.');
  });

  test('where the tail names nothing on its own the label stays', () => {
    expect(unclaimedName('A — false')).toBe('A — false');
    expect(unclaimedName('Gestation length (days) — 280 - 283')).toBe('Gestation length (days) — 280 - 283');
    expect(unclaimedName('Plantain — 3/5 = 60%')).toBe('Plantain — 3/5 = 60%');
    expect(unclaimedName('Parents — Hh x Hh')).toBe('Parents — Hh x Hh');
  });

  test('a row of several label — answer pairs is named whole, not by its last answer', () => {
    // Shipped as "Stationary".
    expect(unclaimedName('Name stage A — Lag / Name stage B — Log / Name stage C — Stationary', 200))
      .toBe('Name stage A — Lag / Name stage B — Log / Name stage C — Stationary');
  });

  test('case is kept as printed', () => {
    expect(unclaimedName('Gamete — R')).toBe('Gamete — R');
  });
});
