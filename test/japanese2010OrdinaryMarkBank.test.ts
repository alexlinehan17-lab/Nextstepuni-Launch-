import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import rawCards from '../components/MarkBank/cards/japanese/reviewed.json';
import census from '../scripts/markbank/authoring/reviews/japanese-2010-ol-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2010-ol.json';
import glyphs from '../scripts/markbank/authoring/glyphmap-japanese-2010-ol.json';
import glyphProof from '../scripts/markbank/authoring/reviews/japanese-2010-ol-glyph-proof.json';
import figures from '../components/MarkBank/figures-japanese.json';
import { assertJapanese2010OrdinaryRules, assertJapaneseSourceOnlyFigure } from '../scripts/markbank/japanese-source-rules.mjs';
import { japaneseBoundBankAnswers } from '../scripts/markbank/japanese-source-answers.mjs';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
import { languageCriterionValue, languageLengthId, languageWritingMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import { tariffReconciles } from '../types/markBank';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = ordinary.filter(card => card.year === 2010);
const idFor = (key: (string | number | null)[]) => `ja-2010-ol-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2010-ol-${suffix}`)!;
const point = (suffix: string) => {
  const found = card(suffix);
  if (found.kind !== 'question') throw new Error(`Expected point card ${suffix}`);
  return found;
};
const writing = (suffix: string) => {
  const found = card(suffix);
  if (found.kind !== 'rubric' || found.rubric.system !== 'language-writing') throw new Error(`Expected manual writing ${suffix}`);
  return found.rubric;
};
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2010/${fileid}.json`), 'utf8'));

describe('Japanese 2010 Ordinary original-source review', () => {
  it('covers all61 whole tasks and all32 original pages with the printed300 marks', () => {
    expect(cards).toHaveLength(61);
    expect(cards.map(card => card.id).sort()).toEqual(census.tasks.map(task => idFor(task.key)).sort());
    expect(census.checksums).toEqual({ reading: 120, writing: 80, listening: 100, total: 300 });
    expect(Object.values(census.pageRoles).map(pages => Object.keys(pages).length)).toEqual([12, 8, 12]);
    expect(census.tasks.filter(task => task.component === 'paper')).toHaveLength(31);
    for (const task of census.tasks) {
      const found = cards.find(card => card.id === idFor(task.key))!;
      expect(found.totalMarks, found.id).toBe(task.marks);
      expect(tariffReconciles(found), found.id).toBe(true);
      expect(rawCards.find(card => card.id === found.id)!.sourceEvidence).toMatchObject({ component: task.component, paperPages: task.paperPages, schemePages: task.schemePages });
    }
    expect(review.sources.map(source => ({ component: source.document, path: source.path, sha256: source.sha256 }))).toEqual(census.sources);
    for (const source of review.sources) expect(source.pagesReviewed).toEqual(Object.keys(census.pageRoles[source.document as keyof typeof census.pageRoles]).map(Number));
    expect(review.consolidations).toEqual([]);
  });

  it('pins every original glyph proof while ordinary CI remains independent of ignored PDFs', () => {
    const digest = (path: string) => createHash('sha256').update(readFileSync(resolve(__dirname, '..', path))).digest('hex');
    expect(review.glyphRecovery.sha256).toBe(digest(review.glyphRecovery.path));
    expect(glyphs.sha256).toBe(review.sources.find(source => source.document === 'scheme')!.sha256);
    expect(Object.values(glyphs.repairs).reduce((sum, font) => sum + Object.keys(font).length, 0)).toBe(156);
    expect(glyphProof.glyphs).toHaveLength(154);
    expect(glyphProof.blankGlyphs).toHaveLength(2);
    expect(glyphs.unresolvedImageOnly).toEqual([]);
    const entries = Object.entries(glyphs.repairs).flatMap(([font, repairs]) => Object.entries(repairs).map(([gid, entry]) => ({ font, gid, ...entry })));
    const proofDigest = digest('scripts/markbank/authoring/reviews/japanese-2010-ol-glyph-proof.json');
    for (const item of glyphProof.glyphs) {
      const entry = entries.find(entry => entry.font === item.font && entry.gid === String(item.gid))!;
      expect(entry.text).toBe(item.text);
      expect(entry.evidence[0]).toMatchObject({ sha256: proofDigest, page: item.page, origin: item.origin, imageSha256: item.imageSha256 });
    }
    for (const sheet of glyphProof.sheets) expect(digest(sheet.path)).toBe(sheet.sha256);
    expect(glyphs.repairs.MSMincho['3494'].text).toBe('午');
    expect(glyphs.repairs.MSMincho['5141'].text).toBe('年');
    expect(point('2-3-ii').rows[0].verbatim).toContain('午後');
    expect(point('2-5-ii').rows[0].verbatim).toContain('20 年間');
    expect(JSON.stringify([cards, review.selectors])).not.toContain('�');
  });

  it('keeps full matching, price, grammar and true/false exercises with every required group', () => {
    for (const [suffix, groups, rows, marks] of [['1-1', 5, 5, 5], ['1-2', 6, 6, 6], ['2-1', 4, 4, 8],
      ['3a-1', 5, 5, 10], ['3a-2', 6, 12, 12], ['3b', 5, 5, 5], ['3c', 3, 3, 6], ['3d', 10, 10, 10], ['lb', 10, 10, 30]] as const) {
      const found = point(suffix);
      expect(found.taskGroups, suffix).toHaveLength(groups);
      expect(found.rows, suffix).toHaveLength(rows);
      expect(found.totalMarks).toBe(marks);
    }
    for (const suffix of ['3a-2', 'lb']) {
      const found = point(suffix);
      expect(marksClaimed(found, Object.fromEntries(found.rows.map(row => [row.id, 'yes'])))).toBe(found.totalMarks);
      const original = review.cards.find(card => card.id === found.id)!;
      expect(() => assertJapanese2010OrdinaryRules({ ...original, rows: original.rows!.slice(1) }, review)).toThrow();
      expect(() => assertJapanese2010OrdinaryRules({ ...original, totalMarks: 3 }, review)).toThrow();
    }
    const weather = point('3a-1').rows[3];
    expect(weather.kind).toBe('anyN');
    if (weather.kind !== 'anyN') throw new Error('Missing weather alternatives');
    expect(weather.group.claimMax).toBe(1);
    expect(weather.group.options).toEqual(['Play baseball with his friends', 'Go to the beach']);
  });

  it('keeps all food alternatives and partial directions in one confidence-only task', () => {
    const found = point('2-3-iii');
    expect(found.totalMarks).toBe(4);
    expect(found.tariffModel).toEqual({ kind: 'questionTotal' });
    expect(found.rows.map(row => row.verbatim)).toEqual(['Steak', 'Teriyaki Chicken', 'Raw fish', 'Potato fries', 'Ceaser salad', '(chicken, fish, salad;  half marks)']);
    for (const row of found.rows) {
      expect(row.marks).toBeNull();
      expect(row.contextNote).toContain('marks are not calculated');
      expect(row.contextNote).toContain('Half marks if answered in the inappropriate language');
    }
    expect(found.answerLanguageRule).toBeUndefined();
    expect(marksClaimed(found, Object.fromEntries(found.rows.map(row => [row.id, 'yes'])))).toBe(0);
    const original = review.cards.find(card => card.id === found.id)!;
    for (const patch of [{ tariffModel: { kind: 'fixed' } }, { rows: original.rows!.slice(1) },
      { answerLanguageRule: { otherLanguageMultiplier: 0.5, sourceText: 'half', schemePages: [6] } },
      { sourceEvidence: { ...original.sourceEvidence, schemePages: [7] } }]) {
      expect(() => assertJapanese2010OrdinaryRules({ ...original, ...patch }, review)).toThrow();
    }
    expect(() => assertJapanese2010OrdinaryRules(original, { ...review, selectors: review.selectors.filter(selector => !selector.text.includes('chicken, fish, salad')) })).toThrow();
  });

  it('binds the single c10 correction to both literal keys and the original case quantity', () => {
    const original = review.cards.find(card => card.id === 'ja-2010-ol-1-3-iii')!;
    expect([...japaneseBoundBankAnswers(original, review)]).toEqual(['(c)  10']);
    expect(point('1-3-iii').rows[0].contextNote).toContain('(iii) (d) 10');
    expect(point('1-3-iii').rows[0].contextNote).toContain('1 ケース十本');
    for (const changed of [{ ...review, sourceAnswerBindings: [] },
      { ...review, selectors: review.selectors.filter(selector => selector.text !== '(iii) (d) 10') },
      { ...review, selectors: review.selectors.filter(selector => selector.text !== '(c)  10') },
      { ...review, selectors: review.selectors.filter(selector => !selector.text.includes('1 ケース十本')) },
      { ...review, sourceAnswerBindings: review.sourceAnswerBindings.map(binding => ({ ...binding, corroboratingPaperSelector: { ...binding.corroboratingPaperSelector, text: '1 ケース十二本です。' } })) },
      { ...review, sources: review.sources.map(source => ({ ...source, sha256: 'changed' })) }]) {
      expect(() => japaneseBoundBankAnswers(original, changed)).toThrow();
    }
    for (const patch of [{ year: 2011 }, { level: 'higher' },
      { sourceEvidence: { ...original.sourceEvidence, paperPages: [2] } }]) {
      expect(() => japaneseBoundBankAnswers({ ...original, ...patch }, review)).toThrow();
    }
    for (const patch of [{ verbatim: '(d) 10' }, { marks: 1 }, { contextNote: 'No discrepancy' }]) {
      expect(() => japaneseBoundBankAnswers({ ...original, rows: [{ ...original.rows![0], ...patch }] }, review)).toThrow();
    }
    expect(() => japaneseBoundBankAnswers({ ...original, id: 'ja-2010-ol-1-3-iv' }, {
      ...review, sourceAnswerBindings: review.sourceAnswerBindings.map(binding => ({ ...binding, cardId: 'ja-2010-ol-1-3-iv' })),
    })).toThrow();
  });

  it('keeps the five webpage prompts visible beside their stimulus-only original image', () => {
    const found = point('1-1');
    expect(found.questionFigure?.includesPrompt).toBe(false);
    expect(found.sourceMaterial?.pages).toEqual([2]);
    for (const word of ['Help', 'Home', 'Shopping cart', 'Auction', 'Sale']) expect(found.questionText).toContain(word);
    const original = review.cards.find(card => card.id === found.id)!;
    const figure = figures['ja-2010-ol-web'];
    expect(() => assertJapaneseSourceOnlyFigure(original, review, figure)).not.toThrow();
    for (const patch of [{ questionFigureIncludesPrompt: true }, { questionFigureIncludesPrompt: undefined }, { id: 'ja-2010-ol-1-2' }]) {
      expect(() => assertJapaneseSourceOnlyFigure({ ...original, ...patch }, review, figure)).toThrow();
    }
    expect(() => assertJapaneseSourceOnlyFigure(original, review, { ...figure, source: { ...figure.source, page: 3 } })).toThrow();
  });

  it('restricts the21 language conditions to their local clauses and preserves the printed MC exceptions', () => {
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(21);
    for (const original of review.cards) expect(() => assertJapanese2010OrdinaryRules(original, review), original.id).not.toThrow();
    for (const suffix of ['1-3-i', '3a-2', '3b', '4', 'la-1', 'lb', 'lc-1-1', 'ld-1', 'ld-2']) expect(card(suffix).answerLanguageRule).toBeUndefined();
    const original = review.cards.find(card => card.id === 'ja-2010-ol-2-2-i')!;
    expect(() => assertJapanese2010OrdinaryRules({ ...original, answerLanguageRule: undefined }, review)).toThrow();
    expect(() => assertJapanese2010OrdinaryRules({ ...original, id: 'ja-2010-ol-3b' }, review)).toThrow();
    expect(point('ld-1').rows[0].verbatim).toContain('tadaima');
    expect(point('ld-2').rows[0].verbatim).toContain('okaerinasai');
    expect(point('ld-1').rows[0].contextNote).toContain('Selecting the correct original option earns its published 2 marks');
    expect(point('ld-3').answerLanguageRule?.penalizedLanguage).toBe('Japanese');
  });

  it('retains the fourth directions option, paired D fields and the John/Jack source discrepancy', () => {
    expect(card('lc-2-3').questionText).toContain('(d) ask someone.');
    expect(point('lc-2-3').rows[0].contextNote).toContain('four alternatives');
    expect(point('ld-4').taskGroups?.map(group => group.marks)).toEqual([2, 2]);
    expect(point('ld-4').rows.map(row => row.verbatim)).toEqual(['20', '0']);
    expect(point('ld-8').taskGroups?.map(group => group.marks)).toEqual([2, 2]);
    expect(point('ld-8').rows[1].contextNote).toContain('scheme repeats (a)');
    expect(card('ld-9').questionText).toContain('John');
    expect(point('ld-9').rows[0].contextNote).toContain('Will Jack have to buy');
    expect(point('ld-9').rows[0].verbatim).toBe('No');
    expect(cards.filter(card => card.audioMaterial)).toHaveLength(30);
    expect(cards.filter(card => card.audioMaterial && card.topicId === 'japanese-6-1')).toHaveLength(12);
  });

  it('retains both complete writing options and the exact content/length expression boundary', () => {
    const rubric = writing('4');
    expect(card('4').sourceMaterial?.pages).toEqual([10, 11]);
    expect(card('4').questionText).toContain('approximately 200');
    expect(card('4').questionText).toContain('any five of the 8 questions');
    expect(card('4').questionText).toContain('学校の後');
    expect(card('4').questionText).toContain('他（ほか）の 趣味');
    expect(rubric.criteria.map(criterion => criterion.maxMarks)).toEqual([7, 7, 7, 7, 7, 5, 40]);
    expect(rubric.criteria.at(-1)?.bands?.map(band => [band.marks[0], band.marks.at(-1)])).toEqual([[0, 9], [10, 27], [28, 40]]);
    const scores: LanguageScores = { [languageLengthId('characters')]: 150 };
    for (const criterion of rubric.criteria) scores[`language:${criterion.id}`] = criterion.maxMarks;
    expect(languageWritingMarks(rubric, scores)).toBe(80);
    scores[languageLengthId('characters')] = 149;
    expect(languageCriterionValue(rubric, 'expression', scores)).toBe(26);
    scores[languageLengthId('characters')] = 150;
    expect(languageCriterionValue(rubric, 'expression', scores)).toBe(40);
    for (const criterion of rubric.criteria.filter(criterion => criterion.id !== 'expression')) scores[`language:${criterion.id}`] = 0;
    Object.assign(scores, { 'language:question-1': 7, 'language:question-2': 7, 'language:question-3': 1, 'language:discretionary': 5 });
    expect(languageCriterionValue(rubric, 'expression', scores)).toBe(26);
    scores['language:question-3'] = 2;
    expect(languageCriterionValue(rubric, 'expression', scores)).toBe(40);
    expect(writing('3e').criteria.map(criterion => criterion.permittedMarks)).toEqual([[0, 2], [0, 2], [0, 1], [0, 1]]);
  });

  it('resolves every task to the complete Atlas source group and retains all14 original anchors', () => {
    const tags = JSON.parse(readFileSync(resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'), 'utf8'));
    for (const [fileid, anchors] of Object.entries(census.originalAtlasAnchors)) {
      const current = map(fileid);
      for (const anchor of anchors) {
        const found = current.q.find(question => question.n === anchor.n)!;
        expect({ n: found.n, pP: found.pP, pY: found.pY, region: found.region }).toEqual(anchor);
      }
    }
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      expect(task.schemePages.every(page => group.region.some(region => region.p === page))).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2010 && paper.fileid === task.atlas.fileid);
      const topic = tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber);
      expect([topic.primary, topic.secondary]).toContain(cards.find(card => card.id === idFor(task.key))!.topicId);
      expect(sidecar.band).toEqual([1, 12]);
    }
    expect(map('LC058GLP000EV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 15 }, (_, i) => String(i + 1)));
    expect(map('LC058GLPA00EV.pdf').q.map(question => question.n)).toEqual(['1', '2', '3', '4']);
    expect(map('LC058GLP000EV.pdf').q.find(question => question.n === '15')?.paperRegion?.map(region => region.p)).toEqual([10, 11]);
  });
});
