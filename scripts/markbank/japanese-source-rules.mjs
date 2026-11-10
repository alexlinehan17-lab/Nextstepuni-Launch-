/** Named-language conditions accepted only when supported by the printed clause.
 * The publisher separately requires exact source-selector and page bindings.
 */
export function matchesNamedLanguageCondition(language, sourceText) {
  if (!['English', 'Japanese'].includes(language) || typeof sourceText !== 'string') return false;
  return ['answered', 'marked'].some(verb => sourceText.includes(`${verb} in ${language}`))
    || (language === 'Japanese' && [
      '(Half marks if answered in romaji or Japanese script)',
      '(1/2 marks if answered in romaji or Japanese script)',
    ].includes(sourceText));
}

/** The five 2012 Higher Q3B tasks share this exact combined printed condition.
 * This source-local binding does not authorize condition labels on other tasks.
 */
export function assertJapaneseConditionLabel(card, review) {
  const rule = card.extraneousMaterialRule;
  const expectedTask = card.year === 2012 && card.level === 'higher'
    && /^ja-2012-hl-3b-[1-5]$/.test(card.id);
  if (!expectedTask && rule?.conditionLabel === undefined) return;
  const condition = 'quotation without manipulation where manipulation required or containing extraneous material';
  const sourceText = `(Evidence needed that candidates have understood the text; ${condition}: half marks.`;
  const expectedParts = [{ row: 14, group: 1 }, { row: 15, group: 0 }];
  const bound = review?.sitting === '2012-hl'
    && review.sources?.some(source => source.document === 'scheme'
      && source.sha256 === 'f976e52a9df6dfb58cd5887e5d003fe5fe2307907d71d0cf515f083fd184e6d5')
    && review.selectors?.some(selector => selector.document === 'scheme' && selector.page === 11
      && selector.text === sourceText && JSON.stringify(selector.parts) === JSON.stringify(expectedParts));
  if (!expectedTask || card.questionRef !== `2012 HL Section 3B Q${card.id.slice(-1)}`
    || rule?.conditionLabel !== condition || rule.sourceText !== sourceText || rule.multiplier !== 0.5
    || JSON.stringify(rule.schemePages) !== '[11]'
    || !card.sourceEvidence?.generalSchemePages?.includes(11) || !bound) {
    throw new Error(`${card.id}: combined response condition is not bound to the exact 2012 Higher Q3B source`);
  }
}
