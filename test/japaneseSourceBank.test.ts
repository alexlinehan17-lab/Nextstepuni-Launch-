import { describe, expect, it } from 'vitest';
import { japaneseBoundBankAnswers } from '../scripts/markbank/japanese-source-answers.mjs';
import original from '../scripts/markbank/authoring/reviews/japanese-2015-ol.json';

const source = () => {
  const review = structuredClone(original);
  const card = review.cards.find(card => card.id === 'ja-2015-ol-4')!;
  if (!card.rows) throw new Error('Missing cloze rows');
  return { review, card };
};

describe('Japanese 2015 Ordinary exact cloze-bank spelling binding', () => {
  it('binds the two scheme spellings to one original bank entry and preserves their visible wording', () => {
    const { review, card } = source();
    expect([...japaneseBoundBankAnswers(card, review)]).toEqual(['日本りょうり']);
    expect(review.sourceAnswerBindings).toHaveLength(1);
    expect(review.sourceAnswerBindings[0].rowIds).toEqual(['r-1', 'r-4']);
  });

  it('rejects a changed canonical spelling or invented scheme equivalence', () => {
    for (const which of ['answer', 'scheme'] as const) {
      const { review, card } = source();
      if (which === 'answer') review.sourceAnswerBindings[0].answer = '日本食';
      else review.sourceAnswerBindings[0].schemeSelectors[1].text = '日本食';
      expect(() => japaneseBoundBankAnswers(card, review)).toThrow(/unsupported source-local/);
    }
  });

  it('requires the original paper bank and both exact scheme selectors on their physical pages', () => {
    for (const index of [0, 1, 2]) {
      const { review, card } = source();
      const binding = review.sourceAnswerBindings[0];
      const selected = [binding.paperSelector, ...binding.schemeSelectors][index];
      review.selectors = review.selectors.filter(selector => JSON.stringify(selector) !== JSON.stringify(selected));
      expect(() => japaneseBoundBankAnswers(card, review)).toThrow(/exact original selectors/);
      review.selectors.push({ ...selected, page: 99 });
      expect(() => japaneseBoundBankAnswers(card, review)).toThrow(/exact original selectors/);
    }
  });

  it('rejects widened card/row scope and hidden source wording', () => {
    const wrongPage = source();
    wrongPage.card.sourceEvidence.schemePages = [9];
    expect(() => japaneseBoundBankAnswers(wrongPage.card, wrongPage.review)).toThrow(/unsupported source-local/);
    const wrongRow = source();
    const row = wrongRow.card.rows![1];
    if (!('group' in row) || !row.group) throw new Error('Missing cloze menu');
    row.group.options.push('日本りょうり');
    expect(() => japaneseBoundBankAnswers(wrongRow.card, wrongRow.review)).toThrow(/row scope/);
    const hidden = source();
    const hiddenRow = hidden.card.rows![3];
    if (!('contextNote' in hiddenRow)) throw new Error('Missing visible bank guidance');
    hiddenRow.contextNote = 'One word only';
    expect(() => japaneseBoundBankAnswers(hidden.card, hidden.review)).toThrow(/visible original wording/);
    const unrelated = source();
    unrelated.card.id = 'ja-2014-ol-4';
    unrelated.review.sourceAnswerBindings[0].cardId = unrelated.card.id;
    expect(() => japaneseBoundBankAnswers(unrelated.card, unrelated.review)).toThrow(/unsupported source-local/);
  });

  it('does not normalize other Japanese answers when the binding is absent', () => {
    const { review, card } = source();
    review.sourceAnswerBindings = [];
    expect([...japaneseBoundBankAnswers(card, review)]).toEqual([]);
  });
});
