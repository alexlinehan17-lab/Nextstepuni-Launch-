import { describe, expect, it } from 'vitest';
import { claimMatches, comparableScheme } from '../scripts/markbank/schemeText.mjs';
import { tariffReconciles, type LanguageWritingRubric, type SecRubricCard } from '../types/markBank';

const source = () => ({ kind: 'rubric', totalMarks: 2, rubric: {
  system: 'language-writing', taskRequirements: [], markingGuideNote: '', criteria: [{
    id: 'expression', label: 'Expression', maxMarks: 2, permittedMarks: [0, 1, 2], guidance: [],
    bands: [{ label: 'Normal', marks: [0, 1, 2], guidance: ['Published normal descriptor.'] }],
    limits: [{ id: 'lower', maxMarks: 1, when: { any: [{ flag: 'short', prompt: 'Short response' }] }, guidance: [],
      bands: [{ label: 'Lower', marks: [0, 1], guidance: ['Published lower descriptor.'] }] }],
  }],
} }) as SecRubricCard & { rubric: LanguageWritingRubric };

describe('nonempty source evidence', () => {
  it.each(['', ' ', '\n\t', '\u00a0\u3000'])('rejects blank source claims %j', claim => {
    expect(claimMatches(comparableScheme('Published source answer.'), claim)).toBe(false);
  });

  it('preserves printed answer text, including a punctuation-only answer', () => {
    const scheme = comparableScheme('Published source answer.\n;');
    expect(claimMatches(scheme, 'Published source answer.')).toBe(true);
    expect(claimMatches(scheme, ';')).toBe(true);
    expect(claimMatches(scheme, 'Invented answer')).toBe(false);
  });

  it('rejects whitespace at every criterion guidance layer while allowing absent optional guidance', () => {
    expect(tariffReconciles(source())).toBe(true);
    for (const layer of ['criterion', 'band', 'limit', 'limitedBand']) {
      const card = source();
      const criterion = card.rubric.criteria[0];
      const target = layer === 'criterion' ? criterion : layer === 'band' ? criterion.bands![0]
        : layer === 'limit' ? criterion.limits![0] : criterion.limits![0].bands![0];
      target.guidance = ['\n\t\u3000'];
      expect(tariffReconciles(card), layer).toBe(false);
    }
  });
});
