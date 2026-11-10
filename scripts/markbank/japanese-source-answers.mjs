import { claimMatches, comparableScheme } from './schemeText.mjs';

/** Include every selectable route in the ordinary whole-scheme answer check. */
export const japaneseAnswerRows = card => [
  ...(card.rows ?? []),
  ...(card.answerVariants ?? []).flatMap(variant => variant.rows),
];

/** Explicit reviewed cloze-bank spellings, never a general normalization. */
export function japaneseBoundBankAnswers(card, review) {
  const bindings = (review.sourceAnswerBindings ?? []).filter(binding => binding.cardId === card.id);
  if (!bindings.length) return new Set();
  if (card.id === 'ja-2013-ol-4') return japanese2013BankAnswers(card, review, bindings);
  const expected = {
    cardId: 'ja-2015-ol-4', answer: '日本りょうり', rowIds: ['r-1', 'r-4'],
    paperSelector: { document: 'paper', page: 11, row: 17, group: 1, text: '日本りょうり' },
    schemeSelectors: [
      { document: 'scheme', page: 10, row: 2, group: 1, text: '日本りようり' },
      { document: 'scheme', page: 10, row: 7, group: 0, text: '（大好き/日本料理  accepted if not used elsewhere）' },
    ],
  };
  const same = (left, right) => JSON.stringify(left) === JSON.stringify(right);
  if (bindings.length !== 1 || !same(bindings[0], expected)
    || review.sitting !== '2015-ol' || card.kind !== 'question' || card.tariffModel?.kind !== 'fixed'
    || card.answerVariants?.length || card.rows?.length !== 10 || card.sourceEvidence?.component !== 'paper'
    || !same(card.sourceEvidence?.paperPages, [11]) || !same(card.sourceEvidence?.schemePages, [10])) {
    throw new Error(`${card.id}: unsupported source-local bank spelling binding`);
  }
  const evidence = [expected.paperSelector, ...expected.schemeSelectors];
  if (!evidence.every(selector => review.selectors.some(actual => same(actual, selector)))) {
    throw new Error(`${card.id}: bank spelling is not bound to the exact original selectors`);
  }
  const matching = (card.rows ?? []).filter(row => row.verbatim === expected.answer
    || (row.kind === 'anyN' && row.group.options.includes(expected.answer)));
  if (!same(matching.map(row => row.id), expected.rowIds)
    || !matching.every(row => row.kind === 'anyN' && row.contextNote?.includes('日本りようり')
      && row.contextNote.includes('日本料理') && row.contextNote.includes('only once'))
    || !matching[1].contextNote.includes(expected.schemeSelectors[1].text)) {
    throw new Error(`${card.id}: bank spelling lost its row scope or visible original wording`);
  }
  return new Set([expected.answer]);
}

function japanese2013BankAnswers(card, review, bindings) {
  const same = (left, right) => JSON.stringify(left) === JSON.stringify(right);
  const schemeSelectors = [
    { document: 'scheme', page: 9, row: 10, group: 1, text: 'ともだち/ せんせい/ ２年生/クラス' },
    { document: 'scheme', page: 9, row: 1, group: null, text: 'Q.4     （30 marks）The same word may not be used twice.' },
  ];
  const expected = [
    { cardId: 'ja-2013-ol-4', answer: '先生', rowIds: ['r-5', 'r-9'],
      paperSelector: { document: 'paper', page: 12, row: 20, group: 0, text: '先生' }, schemeSelectors },
    { cardId: 'ja-2013-ol-4', answer: '二年生', rowIds: ['r-2', 'r-9'],
      paperSelector: { document: 'paper', page: 12, row: 15, group: 1, text: '二年生' }, schemeSelectors },
  ];
  if (!same(bindings, expected) || review.sitting !== '2013-ol'
    || card.kind !== 'question' || card.tariffModel?.kind !== 'fixed'
    || card.answerVariants?.length || card.rows?.length !== 10
    || card.sourceEvidence?.component !== 'paper'
    || !same(card.sourceEvidence?.paperPages, [12]) || !same(card.sourceEvidence?.schemePages, [9])) {
    throw new Error(`${card.id}: unsupported source-local bank spelling binding`);
  }
  for (const binding of expected) {
    if (![binding.paperSelector, ...binding.schemeSelectors].every(selector => review.selectors.some(actual => same(actual, selector)))) {
      throw new Error(`${card.id}: bank spelling is not bound to the exact original selectors`);
    }
    const matching = card.rows.filter(row => row.kind === 'anyN' && row.group.options.includes(binding.answer));
    if (!same(matching.map(row => row.id), binding.rowIds)
      || !matching.every(row => row.contextNote?.includes('せんせい/先生')
        && row.contextNote.includes('２年生/二年生') && row.contextNote.includes('only once')
        && row.contextNote.includes(schemeSelectors[0].text))) {
      throw new Error(`${card.id}: bank spelling lost its row scope or visible original wording`);
    }
  }
  return new Set(expected.map(binding => binding.answer));
}

/** A selectable route must also bind to this task's reviewed physical pages. */
export function assertJapaneseVariantSources(card, selectors, unprintedAnswer) {
  if (!card.answerVariants?.length) return;
  const pages = card.sourceEvidence?.schemePages ?? [];
  const source = comparableScheme(selectors.filter(selector => selector.document === 'scheme'
    && pages.includes(selector.page)).map(selector => selector.text).join('\n'));
  for (const variant of card.answerVariants ?? []) {
    for (const row of variant.rows) {
      if (row.unprinted) {
        if (row.verbatim !== unprintedAnswer) throw new Error(`${card.id}/${variant.id}: unprinted route invents an answer`);
        continue;
      }
      const answers = row.kind === 'anyN' ? row.group.options : [row.verbatim];
      const unsupported = answers.filter(answer => !answer?.trim() || !claimMatches(source, answer));
      if (unsupported.length) throw new Error(`${card.id}/${variant.id}: variant answer is not bound to its task's reviewed scheme pages: ${JSON.stringify(unsupported)}`);
    }
  }
}
