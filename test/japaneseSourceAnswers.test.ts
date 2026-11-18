import { describe, expect, it } from 'vitest';
import { assertJapaneseVariantSources, japaneseAnswerRows } from '../scripts/markbank/japanese-source-answers.mjs';
import review from '../scripts/markbank/authoring/reviews/japanese-2015-hl.json';
import { UNPRINTED_ANSWER } from '../types/markBank';

// Portable committed selectors are checked here; the mandatory source verifier
// separately rereads their exact bytes, physical pages and source PDF hashes.
const sourceCard = () => {
  const card = structuredClone(review.cards.find(card => card.id === 'ja-2015-hl-3a-3-i')!);
  if (!('answerVariants' in card) || !card.answerVariants) throw new Error('Missing reviewed person routes');
  return card;
};

describe('Japanese selectable-answer source binding', () => {
  it('checks both complete source pools, including the unselected second person', () => {
    const card = sourceCard();
    expect(card.answerVariants.map(variant => variant.label)).toEqual(['Nicole', 'Michael']);
    expect(japaneseAnswerRows(card)).toHaveLength(3);
    expect(() => assertJapaneseVariantSources(card, review.selectors, UNPRINTED_ANSWER)).not.toThrow();
  });

  it('rejects a mutated answer in either route, even if the default rows are intact', () => {
    for (const index of [0, 1]) {
      const card = sourceCard();
      card.answerVariants[index].rows[0].group.options[0] = 'Unpublished lunar research occupation';
      expect(() => assertJapaneseVariantSources(card, review.selectors, UNPRINTED_ANSWER)).toThrow(/variant answer is not bound/);
    }
  });

  it('rejects answers supported only on another physical page or by unbound selector copies', () => {
    const card = sourceCard();
    const misplaced = sourceCard();
    misplaced.answerVariants[1].rows[0].group.options[0] = 'Chinese';
    expect(review.selectors.some(selector => selector.document === 'scheme' && selector.page === 7 && selector.text === 'Chinese')).toBe(true);
    expect(() => assertJapaneseVariantSources(misplaced, review.selectors, UNPRINTED_ANSWER)).toThrow(/reviewed scheme pages/);
    expect(() => assertJapaneseVariantSources(card, review.selectors.map(selector => ({ ...selector, page: 99 })), UNPRINTED_ANSWER)).toThrow(/reviewed scheme pages/);
    card.sourceEvidence.schemePages = [5];
    expect(() => assertJapaneseVariantSources(card, review.selectors, UNPRINTED_ANSWER)).toThrow(/reviewed scheme pages/);
  });

  it('rejects empty route claims instead of matching an empty string', () => {
    const card = sourceCard();
    card.answerVariants[1].rows[0].group.options[0] = ' ';
    expect(() => assertJapaneseVariantSources(card, review.selectors, UNPRINTED_ANSWER)).toThrow(/variant answer is not bound/);
  });
});
