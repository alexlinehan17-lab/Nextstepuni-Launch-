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

const combinedCondition = 'quotation without manipulation where manipulation required or containing extraneous material';
const combinedBindings = [
  {
    year: 2012, section: '3B', count: 5, page: 11,
    sha256: 'f976e52a9df6dfb58cd5887e5d003fe5fe2307907d71d0cf515f083fd184e6d5',
    parts: [{ row: 14, group: 1 }, { row: 15, group: 0 }],
    sourceText: `(Evidence needed that candidates have understood the text; ${combinedCondition}: half marks.`,
  },
  {
    year: 2011, section: '1C', count: 3, page: 8,
    sha256: 'b074b5846c2f41ce7a4476795922fd4570334c44536924c8484a4aed02238f81',
    parts: [{ row: 0, group: 0 }, { row: 1, group: 0 }, { row: 2, group: 0 }],
    sourceText: 'C:      (6 marks)  (Evidence needed that candidates have understood the text; quotation without manipulation where manipulation required or containing extraneous material: half marks.  (Half marks if answered in English)',
  },
  ...[{ section: '2B', count: 3, page: 10, row: 1 }, { section: '3B', count: 4, page: 11, row: 30 }].map(binding => ({
    ...binding, year: 2011,
    sha256: 'b074b5846c2f41ce7a4476795922fd4570334c44536924c8484a4aed02238f81',
    parts: [0, 1, 2].map(offset => ({ row: binding.row + offset, group: 0 })),
    sourceText: `(Evidence needed that candidates have understood the text; ${combinedCondition}: half marks. Answers in language not specified  = half marks)`,
  })),
];

/** Exact local printed conditions, with immutable task, page, selector and PDF bindings.
 * This does not authorize a condition label on any other Japanese task.
 */
export function assertJapaneseConditionLabel(card, review) {
  const rule = card.extraneousMaterialRule;
  const binding = combinedBindings.find(item => card.year === item.year && card.level === 'higher'
    && new RegExp(`^ja-${item.year}-hl-${item.section.toLowerCase()}-[1-${item.count}]$`).test(card.id));
  if (!binding && rule?.conditionLabel === undefined) return;
  const bound = binding && review?.sitting === `${binding.year}-hl`
    && review.sources?.some(source => source.document === 'scheme'
      && source.sha256 === binding.sha256)
    && review.selectors?.some(selector => selector.document === 'scheme' && selector.page === binding.page
      && selector.text === binding.sourceText && JSON.stringify(selector.parts) === JSON.stringify(binding.parts));
  if (!binding || card.questionRef !== `${binding.year} HL Section ${binding.section} Q${card.id.slice(-1)}`
    || rule?.conditionLabel !== combinedCondition || rule.sourceText !== binding.sourceText || rule.multiplier !== 0.5
    || JSON.stringify(rule.schemePages) !== JSON.stringify([binding.page])
    || !card.sourceEvidence?.generalSchemePages?.includes(binding.page) || !bound) {
    throw new Error(`${card.id}: combined response condition is not bound to the exact ${binding?.year ?? card.year} Higher local source`);
  }
}
