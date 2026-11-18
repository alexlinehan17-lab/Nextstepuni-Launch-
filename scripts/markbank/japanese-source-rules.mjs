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

const selectedContentScheme = '7a71fa81c9f4dcdf00223ec1774c8e8c1fe86ce8ddffa61c04cb207c896d6628';

/** This webpage is stimulus only; its seven questions are on the next page.
 * Requiring the explicit false value prevents a missing field hiding prompts.
 */
export function assertJapaneseSourceOnlyFigure(card, review, figure) {
  const named = card.id === 'ja-2010-hl-1aa';
  if (!named && card.questionFigureIncludesPrompt === undefined) return;
  if (!named || card.questionFigureIncludesPrompt !== false || card.year !== 2010 || card.level !== 'higher'
    || card.totalMarks !== 7 || card.questionFigureKey !== 'ja-2010-hl-web-buttons'
    || figure?.source?.document !== 'paper' || figure.source.page !== 2
    || JSON.stringify(card.sourceEvidence?.paperPages) !== '[3]'
    || JSON.stringify(card.sourceMaterial?.pages) !== '[2]'
    || !card.questionText?.trim() || review?.sitting !== '2010-hl'
    || !review.sources?.some(source => source.document === 'paper'
      && source.path === 'examiner-reports/japanese/papers/2010-hl-000-paper.pdf'
      && source.sha256 === 'a8431333d349dc9c686ae8bad56a92ea1800e1e0186af3c6850ea4599b28f629')) {
    throw new Error(`${card.id}: source-only figure is not bound to the original 2010 webpage task`);
  }
}

const selectedContentBindings = [
  {
    question: 5, page: 12, paperPage: 12, total: 40, content: 10, length: 150, expression: 20, lower: 15,
    criterionIds: ['discretionary'],
    parts: [{ row: 9, group: 1 }, { row: 10, group: 0 }, { row: 11, group: 0 }, { row: 12, group: 0 }],
    sourceText: 'Marked out of 20  or 15. If the content mark is 10 or less, or the composition is too short (less than 150 characters), mark expression out of 15 and write ‘lower E’ to indicate this. Use the numbering (1-6) when showing individual content points, display total content points (C =…)and add E/Lower E to give total marks for the composition.',
  },
  {
    question: 6, page: 14, paperPage: 16, total: 60, content: 15, length: 200, expression: 30, lower: 20,
    criterionIds: [],
    parts: [{ row: 9, group: 1 }, { row: 10, group: 0 }, { row: 11, group: 0 }, { row: 12, group: 0 }, { row: 13, group: 0 }],
    sourceText: 'Marked out of 30  or 20. If the content mark is 15` or less, or the composition is too short (less than 200 characters), mark expression out of 20 and write ‘lower E’ to indicate this. Use the numbering (i) a- f, and (ii)a –d,  when showing individual content points, display total content points (C =…) and add E/Lower E to give total marks for the composition.',
  },
];

/** Selected content may lower E only for these two original 2010 writing grids.
 * The source verifier separately rereads every exact selector from the original.
 * Other sittings cannot inherit this feature through an unrelated rubric edit.
 */
export function assertJapaneseSelectedContent(card, review) {
  const criteria = [...(card.rubric?.criteria ?? []), ...(card.rubric?.groups ?? []).flatMap(group => group.criteria ?? [])];
  const uses = criteria.flatMap(criterion => (criterion.limits ?? []).flatMap(limit =>
    (limit.when?.any ?? []).filter(condition => condition.includeSelectedGroupMarks !== undefined)
      .map(condition => ({ criterion, limit, condition }))));
  const binding = selectedContentBindings.find(item => card.id === `ja-2010-hl-${item.question}`);
  if (!binding && !uses.length) return;
  const use = uses[0];
  const expectedWhen = { any: [
    { criterionIds: binding?.criterionIds, atMost: binding?.content, includeSelectedGroupMarks: true },
    { length: 'characters', below: binding?.length },
  ] };
  const bound = binding && review?.sitting === '2010-hl'
    && review.sources?.some(source => source.document === 'scheme'
      && source.path === 'examiner-reports/japanese/schemes/2010-hl.pdf' && source.sha256 === selectedContentScheme)
    && review.selectors?.some(selector => selector.document === 'scheme' && selector.page === binding.page
      && selector.text === binding.sourceText && JSON.stringify(selector.parts) === JSON.stringify(binding.parts));
  if (!binding || !bound || uses.length !== 1 || card.year !== 2010 || card.level !== 'higher'
    || card.questionRef !== `2010 HL Section ${binding.question}` || card.kind !== 'rubric'
    || card.rubric?.system !== 'language-points' || card.totalMarks !== binding.total
    || card.rubric.count !== (binding.question === 5 ? 4 : 1) || card.answerLanguageRule !== undefined
    || !card.rubric.criteria?.includes(use.criterion) || use.criterion.id !== 'expression'
    || use.criterion.maxMarks !== binding.expression || use.limit.maxMarks !== binding.lower
    || JSON.stringify(use.limit.when) !== JSON.stringify(expectedWhen)
    || !use.limit.guidance?.includes(binding.sourceText)
    || JSON.stringify(card.sourceEvidence?.paperPages) !== JSON.stringify([binding.paperPage])
    || JSON.stringify(card.sourceEvidence?.schemePages) !== JSON.stringify([binding.page - 1, binding.page])) {
    throw new Error(`${card.id}: selected-content expression scale is not bound to the exact 2010 Higher source`);
  }
}

const manualQ3Condition = '(Evidence needed that candidates have understood the text; quotation without manipulation where manipulation required or containing extraneous material: half marks. Answers in language not specified = half marks)';
/** Keep the 2010 Q3 response conditions local, including the shared bonus.
 * Manual half values are the published reduction of an otherwise earned award,
 * never an extra base partial or a value to reduce again with an automatic flag.
 */
export function assertJapanese2010ManualResponses(card, review) {
  if (!/^ja-2010-hl-3(?:a-[1-9]|b|c)$/.test(card.id)) return;
  const expected = card.id.endsWith('3b') ? [1, 2, 1] : card.id.endsWith('3c') ? Array(14).fill(1)
    : /3a-(?:2|9)$/.test(card.id) ? [1, 1] : [2];
  const parts = [{ row: 1, group: 0 }, { row: 2, group: 0 }, { row: 3, group: 0 }];
  const bound = review?.sitting === '2010-hl'
    && review.sources?.some(source => source.document === 'scheme' && source.sha256 === selectedContentScheme)
    && review.selectors?.some(selector => selector.document === 'scheme' && selector.page === 9
      && selector.text === manualQ3Condition && JSON.stringify(selector.parts) === JSON.stringify(parts));
  const validRows = rows => rows?.length === expected.length && rows.every((row, index) =>
    row.kind === 'criterion' && row.marks === expected[index]
    && JSON.stringify(row.permittedMarks) === JSON.stringify([0, expected[index] / 2, expected[index]])
    && row.contextNote?.includes(manualQ3Condition));
  const bonus = card.id.endsWith('3b');
  if (!bound || card.year !== 2010 || card.level !== 'higher' || card.kind !== 'question'
    || card.tariffModel?.kind !== 'fixed' || card.totalMarks !== expected.reduce((sum, mark) => sum + mark, 0)
    || card.answerLanguageRule !== undefined || card.extraneousMaterialRule !== undefined
    || card.sourceEvidence?.component !== 'paper'
    || JSON.stringify(card.sourceEvidence?.paperPages) !== (card.id.endsWith('3c') ? '[10]' : '[9]')
    || JSON.stringify(card.sourceEvidence?.schemePages) !== (card.id.endsWith('3c') ? '[10]' : '[9]')
    || !card.sourceEvidence?.generalSchemePages?.includes(9) || !validRows(card.rows)
    || (bonus && (card.answerVariants?.length !== 2 || !card.answerVariants.every((variant, index) =>
      variant.id === `bonus-under-${index + 1}` && validRows(variant.rows)
      && variant.rows[2].contextNote.includes(`assigned under question ${index + 1}`))))
    || (!bonus && card.answerVariants !== undefined)) {
    throw new Error(`${card.id}: manual half-credit responses are not bound to the exact 2010 Higher Q3 source`);
  }
}
