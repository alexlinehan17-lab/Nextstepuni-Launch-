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

const naebaException = 'Naeba (0 marks if written in Hiragana)';
const naebaClauses = [
  '(Half marks if not answered in the appropriate language)',
  '2.  (5 marks) (half marks if answered in the non-specified language)',
  'Naeba (0 marks if written', 'in Hiragana)',
];
const naebaManualGuidance = `${naebaClauses.join(' ')} — Award 1 for correct Naeba in the appropriate language; 0 for Hiragana or incorrect content. Award 0.5 only for otherwise correct content in another inappropriate language, excluding Hiragana. These are whole-response marks; apply no second language reduction.`;

/** The sole explicit Hiragana-zero exception also carries a general half rule.
 * Bind its manual whole-response steps to this original task and exact clauses;
 * an automatic language flag must never override zero or reduce twice.
 */
export function assertJapaneseNaebaException(card, review) {
  const named = card.id === 'ja-2011-ol-1-2-ii';
  const carries = card.rows?.some(row => row.verbatim === naebaException);
  if (!named && !carries) return;
  const parts = [{ row: 2, group: null }, { row: 13, group: null }, { row: 15, group: 1 }, { row: 16, group: 0 }];
  const bound = review?.sitting === '2011-ol'
    && review.sources?.some(source => source.document === 'scheme'
      && source.path === 'examiner-reports/japanese/schemes/2011-ol.pdf'
      && source.sha256 === 'bd5bd566ecfa9376f427f74b7d727ad568ac2d948bddc6845a12eda9eefef2a4')
    && review.selectors?.some(selector => selector.document === 'scheme' && selector.page === 6
      && selector.text === naebaClauses.join(' ') && JSON.stringify(selector.parts) === JSON.stringify(parts));
  const row = card.rows?.[0];
  if (!named || !bound || card.year !== 2011 || card.level !== 'ordinary'
    || card.questionRef !== '2011 OL Section 1 Q2(ii)'
    || card.questionText !== 'At what ski resort will the festival take place?' || card.kind !== 'question'
    || card.tariffModel?.kind !== 'fixed' || card.totalMarks !== 1 || card.rows.length !== 1
    || row.id !== 'r-1' || row.kind !== 'criterion' || row.verbatim !== naebaException || row.marks !== 1
    || JSON.stringify(row.permittedMarks) !== '[0,0.5,1]' || row.contextNote !== naebaManualGuidance
    || card.answerLanguageRule !== undefined || card.extraneousMaterialRule !== undefined
    || card.sourceEvidence?.component !== 'paper'
    || JSON.stringify(card.sourceEvidence?.paperPages) !== '[3]'
    || JSON.stringify(card.sourceEvidence?.schemePages) !== '[6]'
    || JSON.stringify(card.sourceEvidence?.generalSchemePages) !== '[6]') {
    throw new Error(`${card.id}: Naeba exception is not bound to the exact 2011 Ordinary source and manual tariff`);
  }
}
