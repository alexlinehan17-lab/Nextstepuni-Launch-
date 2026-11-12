import { claimMatches, comparableScheme } from './schemeText.mjs';

/** Include every selectable route in the ordinary whole-scheme answer check. */
export const japaneseAnswerRows = card => [
  ...(card.rows ?? []),
  ...(card.answerVariants ?? []).flatMap(variant => variant.rows),
];

/** Explicit reviewed cloze-bank spellings, never a general normalization. */
export function japaneseBoundBankAnswers(card, review) {
  const bindings = (review.sourceAnswerBindings ?? []).filter(binding => binding.cardId === card.id);
  if (card.id === 'ja-2011-ol-2c') return japanese2011KanjiAnswer(card, review, bindings);
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


/** One editorial reading correction, supported by the same printed option b.
 * The scheme's literal typo remains visible; this cannot normalize another row.
 */
function japanese2011KanjiAnswer(card, review, bindings) {
  const same = (left, right) => JSON.stringify(left) === JSON.stringify(right);
  const expected = {
    cardId: 'ja-2011-ol-2c', answer: 'b. にほん', rowIds: ['r-1'],
    paperSelector: { document: 'paper', page: 6, row: 7, group: 2, text: 'b. にほん' },
    schemeSelectors: [{ document: 'scheme', page: 8, row: 3, group: 1, text: 'b.  にはん' }],
  };
  const row = card.rows?.[0];
  const sources = [
    ['paper', 'examiner-reports/japanese/papers/2011-ol-000-paper.pdf', '8f3cc484584f2f3d92d8ff527ea504244f3cdecd7bb9a317050a6c18f3788a6d'],
    ['scheme', 'examiner-reports/japanese/schemes/2011-ol.pdf', 'bd5bd566ecfa9376f427f74b7d727ad568ac2d948bddc6845a12eda9eefef2a4'],
  ];
  if (!same(bindings, [expected]) || review.sitting !== '2011-ol'
    || card.year !== 2011 || card.level !== 'ordinary' || card.kind !== 'question'
    || card.tariffModel?.kind !== 'fixed' || card.totalMarks !== 16 || card.rows?.length !== 16
    || card.answerVariants?.length || card.questionRef !== '2011 OL Section 2C'
    || card.sourceEvidence?.component !== 'paper'
    || !same(card.sourceEvidence?.paperPages, [6]) || !same(card.sourceEvidence?.schemePages, [8])
    || row.id !== 'r-1' || row.verbatim !== expected.answer || row.marks !== 1
    || !row.contextNote?.includes(expected.paperSelector.text)
    || !row.contextNote.includes(expected.schemeSelectors[0].text)
    || !row.contextNote.includes('same printed option letter b')
    || !sources.every(([document, path, sha256]) => review.sources?.some(source => source.document === document && source.path === path && source.sha256 === sha256))
    || ![expected.paperSelector, ...expected.schemeSelectors].every(selector => review.selectors.some(actual => same(actual, selector)))) {
    throw new Error(`${card.id}: kanji reading correction is not bound to both exact 2011 Ordinary sources`);
  }
  return new Set([expected.answer]);
}

/** The positive Ordinary statement and negative scheme statement are reconciled
 * by the same-year Higher answer and the explicitly shared recording identity.
 * This is one cross-source correction, never an automatic inversion of a key.
 */
export function assertJapanese2011ListeningCorrection(card, review, higher, recording) {
  const corrections = (review.sourceCorrections ?? []).filter(item => item.cardId === card.id);
  if (card.id !== 'ja-2011-ol-ld' && !corrections.length) return;
  const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
  const paperSelector = { document: 'aural', page: 5, row: 32, group: null, text: 'Kenichi is allowed to use the internet.' };
  const schemeSelectors = [
    { document: 'scheme', page: 5, row: 11, group: 0, text: '(x) Kenichi is not allowed to use the internet.' },
    { document: 'scheme', page: 5, row: 11, group: 1, text: 'F' },
  ];
  const higherSelector = { document: 'scheme', page: 6, row: 12, group: 0, text: 'It’s quiet; he can study; can read lots; can use internet; he likes books' };
  const higherSource = { path: 'examiner-reports/japanese/schemes/2011-hl.pdf', sha256: 'b074b5846c2f41ce7a4476795922fd4570334c44536924c8484a4aed02238f81', selector: higherSelector };
  const audio = {
    paperFileids: ['LC058ALPA00EV.pdf', 'LC058GLPA00EV.pdf'],
    canonicalUrl: 'https://www.examinations.ie/archive/exampapers/2011/LC058ZLP017EV.mp3',
    secFileid: 'LC058ZLP017EV.mp3', sha256: '8e57addb698916e39d2edcc911638dd7c6377ac498b0f64a5760c64649ab81cb',
  };
  const expected = { cardId: 'ja-2011-ol-ld', groupId: 'item-10', resolvedAnswer: 'True',
    paperSelector, schemeSelectors, corroboratingReview: 'scripts/markbank/authoring/reviews/japanese-2011-hl.json',
    corroboratingCardId: 'ja-2011-hl-ld-2-ii', corroboratingSource: higherSource, audio };
  const group = card.rubric?.groups?.find(group => group.id === 'item-10');
  const higherCard = higher?.cards?.find(card => card.id === expected.corroboratingCardId);
  const guide = card.rubric?.markingGuideNote ?? '';
  const sources = [
    ['aural', 'examiner-reports/japanese/papers/2011-ol-A00-paper.pdf', '309948b6752e84404c0643b54cb99d0caf72ec7b46193ef1cbc84e2a33b718d8'],
    ['scheme', 'examiner-reports/japanese/schemes/2011-ol.pdf', 'bd5bd566ecfa9376f427f74b7d727ad568ac2d948bddc6845a12eda9eefef2a4'],
  ];
  if (!same(corrections, [expected]) || review.sitting !== '2011-ol'
    || card.id !== expected.cardId || card.year !== 2011 || card.level !== 'ordinary'
    || card.questionRef !== '2011 OL Section LD' || card.totalMarks !== 24
    || card.rubric?.system !== 'language-points' || card.rubric.count !== 8 || card.rubric.groups.length !== 12
    || group?.label !== paperSelector.text || !same(group.rows, [{ id: 'answer', text: 'True', marks: 3 }]) || group.criteria?.length
    || card.sourceEvidence?.component !== 'aural'
    || !same(card.sourceEvidence?.paperPages, [5]) || !same(card.sourceEvidence?.schemePages, [5])
    || ![paperSelector, ...schemeSelectors].every(selector => review.selectors.some(actual => same(actual, selector)))
    || !sources.every(([document, path, sha256]) => review.sources.some(source => source.document === document && source.path === path && source.sha256 === sha256))
    || higher?.sitting !== '2011-hl' || !higher.selectors?.some(selector => same(selector, higherSelector))
    || !higher.sources?.some(source => source.document === 'scheme' && source.path === higherSource.path && source.sha256 === higherSource.sha256)
    || higherCard?.year !== 2011 || higherCard.level !== 'higher'
    || higherCard.questionRef !== '2011 HL Section LD Q2(ii)'
    || !same(higherCard?.sourceEvidence?.schemePages, [6])
    || !higherCard.rows?.some(row => row.kind === 'anyN' && row.group?.options?.includes('can use internet'))
    || recording?.year !== 2011 || !same(recording.paperFileids, audio.paperFileids)
    || recording.source?.canonicalUrl !== audio.canonicalUrl || recording.source?.secFileid !== audio.secFileid
    || recording.verification?.status !== 'full-file-verified' || recording.verification?.sha256 !== audio.sha256
    || ![paperSelector.text, schemeSelectors[0].text, higherSelector.text, '→ F', 'not direct audio listening verification'].every(text => guide.includes(text))) {
    throw new Error(`${card.id}: listening correction is not bound to the exact 2011 paper, both schemes and shared recording`);
  }
}
