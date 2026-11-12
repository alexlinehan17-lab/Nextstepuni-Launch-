import { describe, expect, it } from 'vitest';
import review2011 from '../scripts/markbank/authoring/reviews/japanese-2011-hl.json';
import review2012 from '../scripts/markbank/authoring/reviews/japanese-2012-hl.json';
import { assertJapaneseConditionLabel, matchesNamedLanguageCondition } from '../scripts/markbank/japanese-source-rules.mjs';

it('accepts only the literal 2014 Ordinary fractional romaji/script condition', () => {
  const printed = '(1/2 marks if answered in romaji or Japanese script)';
  expect(matchesNamedLanguageCondition('Japanese', printed)).toBe(true);
  expect(matchesNamedLanguageCondition('English', printed)).toBe(false);
  expect(matchesNamedLanguageCondition('Japanese', printed.replace('1/2', 'full'))).toBe(false);
  expect(matchesNamedLanguageCondition('Japanese', printed.replace('Japanese', 'English'))).toBe(false);
});

describe('Japanese source-bound named-language conditions', () => {
  it('accepts the exact 2016 Ordinary romaji/Japanese-script clause only for Japanese', () => {
    const printed = '(Half marks if answered in romaji or Japanese script)';
    expect(matchesNamedLanguageCondition('Japanese', printed)).toBe(true);
    expect(matchesNamedLanguageCondition('English', printed)).toBe(false);
    expect(matchesNamedLanguageCondition('Japanese', '(Half marks if answered in romaji or English script)')).toBe(false);
    expect(matchesNamedLanguageCondition('Japanese', '(Full marks if answered in romaji or Japanese script)')).toBe(false);
    expect(matchesNamedLanguageCondition('Japanese', 'Japanese script is accepted.')).toBe(false);
    expect(matchesNamedLanguageCondition('French', printed)).toBe(false);
    expect(matchesNamedLanguageCondition('Japanese', '')).toBe(false);
  });
  it('retains existing explicit English and Japanese source clauses', () => {
    expect(matchesNamedLanguageCondition('English', 'Half marks if answered in English.')).toBe(true);
    expect(matchesNamedLanguageCondition('Japanese', 'Half marks if answered in Japanese.')).toBe(true);
    expect(matchesNamedLanguageCondition('Japanese', 'Half marks if marked in Japanese.')).toBe(true);
    expect(matchesNamedLanguageCondition('English', 'Half marks if answered in Japanese.')).toBe(false);
  });
});


describe('2012 Higher Q3B exact combined source condition', () => {
  const original = review2012.cards.find(card => card.id === 'ja-2012-hl-3b-1')!;
  it('binds all five tasks to the complete original condition clause', () => {
    const affected = review2012.cards.filter(card => card.id.startsWith('ja-2012-hl-3b-'));
    expect(affected).toHaveLength(5);
    for (const card of affected) expect(() => assertJapaneseConditionLabel(card, review2012)).not.toThrow();
  });
  it('rejects a mutated, removed, broadened or source-mismatched condition', () => {
    for (const patch of [
      { conditionLabel: 'containing extraneous material' },
      { conditionLabel: 'quotation without manipulation' },
      { conditionLabel: undefined },
      { sourceText: original.extraneousMaterialRule!.sourceText + ' altered' },
      { schemePages: [10] },
    ]) {
      const card = { ...original, extraneousMaterialRule: { ...original.extraneousMaterialRule, ...patch } };
      expect(() => assertJapaneseConditionLabel(card, review2012)).toThrow(/exact 2012/);
    }
    expect(() => assertJapaneseConditionLabel({ ...original, id: 'ja-2012-hl-3a-1-a' }, review2012)).toThrow();
    expect(() => assertJapaneseConditionLabel({ ...original, year: 2013 }, review2012)).toThrow();
  });
  it('rejects an unbound selector, wrong original page or changed source digest', () => {
    const without = { ...review2012, selectors: review2012.selectors.filter(selector => selector.text !== original.extraneousMaterialRule!.sourceText) };
    expect(() => assertJapaneseConditionLabel(original, without)).toThrow();
    const wrongPage = { ...review2012, selectors: review2012.selectors.map(selector => selector.text === original.extraneousMaterialRule!.sourceText ? { ...selector, page: 10 } : selector) };
    expect(() => assertJapaneseConditionLabel(original, wrongPage)).toThrow();
    const wrongHash = { ...review2012, sources: review2012.sources.map(source => ({ ...source, sha256: 'changed' })) };
    expect(() => assertJapaneseConditionLabel(original, wrongHash)).toThrow();
  });
  it('leaves earlier default rules unchanged and rejects a missing 2012 rule', () => {
    expect(() => assertJapaneseConditionLabel({ id: 'ja-2025-hl-3b-1', year: 2025, level: 'higher', extraneousMaterialRule: { multiplier: 0.5, sourceText: 'Original earlier rule', schemePages: [11] } }, {})).not.toThrow();
    expect(() => assertJapaneseConditionLabel({ ...original, extraneousMaterialRule: undefined }, review2012)).toThrow();
  });
});

describe('2011 Higher exact local combined conditions', () => {
  it('binds only the three Q1C, three Q2B and four Q3B tasks to their own original pages', () => {
    const affected = review2011.cards.filter(card => card.extraneousMaterialRule);
    expect(affected).toHaveLength(10);
    for (const card of affected) expect(() => assertJapaneseConditionLabel(card, review2011)).not.toThrow();
    expect(affected.map(card => card.extraneousMaterialRule!.schemePages[0])).toEqual([8, 8, 8, 10, 10, 10, 11, 11, 11, 11]);
  });
  it('rejects changed clauses, scope, selector coordinates, pages and source hashes', () => {
    for (const id of ['ja-2011-hl-1c-1', 'ja-2011-hl-2b-1', 'ja-2011-hl-3b-1']) {
      const original = review2011.cards.find(card => card.id === id)!;
      const rule = original.extraneousMaterialRule!;
      for (const patch of [
        { conditionLabel: 'containing extraneous material' }, { conditionLabel: undefined },
        { sourceText: rule.sourceText.replace('where manipulation required', '') },
        { schemePages: [rule.schemePages[0] + 1] }, { multiplier: 0 },
      ]) expect(() => assertJapaneseConditionLabel({ ...original, extraneousMaterialRule: { ...rule, ...patch } }, review2011)).toThrow();
      expect(() => assertJapaneseConditionLabel({ ...original, id: 'ja-2011-hl-3a-1' }, review2011)).toThrow();
      expect(() => assertJapaneseConditionLabel({ ...original, extraneousMaterialRule: undefined }, review2011)).toThrow();
      expect(() => assertJapaneseConditionLabel(original, { ...review2011, selectors: review2011.selectors.filter(selector => selector.text !== rule.sourceText) })).toThrow();
      expect(() => assertJapaneseConditionLabel(original, { ...review2011, selectors: review2011.selectors.map(selector => selector.text === rule.sourceText ? { ...selector, page: 19 } : selector) })).toThrow();
      expect(() => assertJapaneseConditionLabel(original, { ...review2011, selectors: review2011.selectors.map(selector => selector.text === rule.sourceText ? { ...selector, parts: [{ row: 0, group: 0 }] } : selector) })).toThrow();
      expect(() => assertJapaneseConditionLabel(original, { ...review2011, sources: review2011.sources.map(source => ({ ...source, sha256: 'changed' })) })).toThrow();
      expect(() => assertJapaneseConditionLabel(original, review2012)).toThrow();
    }
  });
});
