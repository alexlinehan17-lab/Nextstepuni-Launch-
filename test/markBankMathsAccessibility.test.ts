/** @license SPDX-License-Identifier: Apache-2.0 */
import { describe, expect, it } from 'vitest';
import { CARDS as HIGHER } from '../components/MarkBank/cards/maths/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/maths/ordinary';

const ALL = [...HIGHER, ...ORDINARY];
const byId = new Map(ALL.map(card => [card.id, card]));

describe('Maths question presentation', () => {
  it('never ships the old hard-cut question-crop description', () => {
    const figures = ALL.flatMap(card =>
      'questionFigure' in card && card.questionFigure
        ? [[card, card.questionFigure] as const]
        : []);
    expect(figures.length).toBeGreaterThan(800);
    expect(figures.filter(([, figure]) => figure.alt.length === 259)
      .map(([card]) => card.id)).toEqual([]);

    const repairedLegacy = figures.filter(([, figure]) =>
      figure.alt.includes('Full card prompt:'));
    expect(repairedLegacy.length).toBeGreaterThan(400);
    for (const [card, figure] of repairedLegacy) {
      expect(figure.alt, card.id).toContain(card.questionText);
    }
  });

  it('keeps the five visually verified 2025 prompts complete', () => {
    const checks = [
      ['maths-2025-hl-p1-q10-e-i', 'H(n + 1) = H(n) + 2n + 3'],
      ['maths-2025-hl-p2-q8-a-i', '|OB| = 3√2 m'],
      ['maths-2025-hl-p2-q8-a-ii', 'total area of the four triangular faces'],
      ['maths-2025-hl-p2-q8-a-iii', 'Construct the rest of the scaled diagram'],
      ['maths-2025-hl-p2-q10-e', 'largest value that the expected value could be'],
    ] as const;
    for (const [id, wording] of checks) {
      const card = byId.get(id);
      const questionFigure = card && 'questionFigure' in card
        ? card.questionFigure
        : undefined;
      expect(card?.questionText, id).toContain(wording);
      expect(questionFigure?.alt, id).toContain('The question as printed on the paper');
      expect(questionFigure?.src, id).toContain('/maths/markbank/');
    }
  });
});
