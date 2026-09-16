import { describe, expect, test } from 'vitest';
import { buildSubjectShowcase } from '@/components/landing/subjectShowcaseSource';
import catalogue from '@/components/landing/subjectShowcase.json';
import sizes from '@/components/MarkBank/cards/sizes.json';

describe('published subject inventory', () => {
  test('matches the current shipped content and uses unique subject identities', () => {
    const current = buildSubjectShowcase();
    expect(catalogue).toEqual(current);
    expect(new Set(current.map(item => item.id)).size).toBe(current.length);
    expect(new Set(current.map(item => item.cycle))).toEqual(new Set(['lc', 'jc', 'lca']));
    const totalCards = Object.values(sizes).flatMap(levels => Object.values(levels)).reduce((sum, value) => sum + value, 0);
    expect(current.reduce((sum, subject) => sum + subject.markBankCards, 0)).toBe(totalCards);
    expect(current.every(item => item.markBankCards || item.atlasQuestions || item.paperCount)).toBe(true);
  });
});
