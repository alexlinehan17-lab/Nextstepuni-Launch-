import { describe, expect, it } from 'vitest';
import { matchesNamedLanguageCondition } from '../scripts/markbank/japanese-source-rules.mjs';

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
