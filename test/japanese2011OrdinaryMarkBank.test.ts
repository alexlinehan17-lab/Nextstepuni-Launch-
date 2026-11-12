import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import rawCards from '../components/MarkBank/cards/japanese/reviewed.json';
import census from '../scripts/markbank/authoring/reviews/japanese-2011-ol-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2011-ol.json';
import higherReview from '../scripts/markbank/authoring/reviews/japanese-2011-hl.json';
import audioRegistry from '../data/japaneseAudio.json';
import { assertJapaneseNaebaException } from '../scripts/markbank/japanese-source-rules.mjs';
import { japaneseBoundBankAnswers, assertJapanese2011ListeningCorrection } from '../scripts/markbank/japanese-source-answers.mjs';
import { tariffReconciles } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
import { languageCriterionValue, languageLengthId, languagePointsMarks, languageWritingMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = ordinary.filter(card => card.year === 2011);
const idFor = (key: (string | number | null)[]) => `ja-2011-ol-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2011-ol-${suffix}`)!;
const point = (suffix: string) => {
  const found = card(suffix);
  if (found.kind !== 'question') throw new Error(`Expected point card ${suffix}`);
  return found;
};
const writing = (suffix: string) => {
  const found = card(suffix);
  if (found.kind !== 'rubric' || found.rubric.system !== 'language-writing') throw new Error(`Expected writing ${suffix}`);
  return found.rubric;
};
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2011/${fileid}.json`), 'utf8'));

describe('Japanese 2011 Ordinary original-source review', () => {
  it('covers all 49 independently inventoried tasks, 37 physical pages and 300 marks', () => {
    expect(cards).toHaveLength(49);
    expect(cards.map(card => card.id).sort()).toEqual(census.tasks.map(task => idFor(task.key)).sort());
    for (const task of census.tasks) {
      const found = cards.find(card => card.id === idFor(task.key))!;
      expect(found.totalMarks, found.id).toBe(task.marks);
      expect(tariffReconciles(found), found.id).toBe(true);
      expect(rawCards.find(card => card.id === found.id)!.sourceEvidence).toMatchObject({ component: task.component, paperPages: task.paperPages, schemePages: task.schemePages });
    }
    expect(census.checksums).toEqual({ reading: 120, writing: 80, listening: 100, total: 300 });
    expect(Object.values(census.pageRoles).map(pages => Object.keys(pages).length)).toEqual([16, 8, 13]);
    expect(review.sources.map(source => ({ component: source.document, path: source.path, sha256: source.sha256 }))).toEqual(census.sources);
    for (const source of review.sources) expect(source.pagesReviewed).toEqual(Object.keys(census.pageRoles[source.document as keyof typeof census.pageRoles]).map(Number));
    expect(review.consolidations).toEqual([]);
  });

  it('retains all required pools, given cells and original source stimuli', () => {
    for (const [suffix, count] of [['1-1', 8], ['2a', 9], ['2b', 16], ['2c', 16], ['3a-1', 8], ['3b-1', 5], ['3b-2', 5]] as const) expect(point(suffix).rows).toHaveLength(count);
    expect(point('2a').taskGroups?.map(group => group.marks)).toEqual([2, 3, 1, 3]);
    expect(point('2a').rows.map(row => row.verbatim)).not.toContain('Paris Café');
    expect(point('2a').rows.map(row => row.verbatim)).not.toContain('French');
    expect(point('2a').rows.map(row => row.verbatim)).not.toContain('Wednesday');
    expect(point('2b').taskGroups?.map(group => group.marks)).toEqual(Array(8).fill(2));
    expect(point('2c').taskGroups?.map(group => group.marks)).toEqual(Array(8).fill(2));
    expect(point('3b-2').rows.map(row => row.marks)).toEqual([2, 2, 2, 2, 1]);
    expect(point('3b-2').rows[2].verbatim).toBe('おもしろい プログラム でした。');
    for (const [suffix, page] of [['1-1', 2], ['2a', 4], ['2b', 4], ['2c', 4], ['3a-1', 8]] as const) expect(card(suffix).sourceMaterial?.pages).toEqual([page]);
    expect(point('1-3-iii').questionText).toContain('The Script');
    expect(point('1-3-iii').questionText).toContain('McFly');
    expect(point('1-3-iii').rows.map(row => row.verbatim)).toEqual(['Red Hot Chilli Peppers', 'The Strokes']);
    expect(point('1-3-i').rows.map(row => row.verbatim)).toEqual(['13 / 14', 'August']);
  });

  it('binds Naeba whole-response 0/.5/1 and the explicit Hiragana zero without double reduction', () => {
    const found = point('1-2-ii');
    expect(found.answerLanguageRule).toBeUndefined();
    expect(found.rows).toHaveLength(1);
    expect(found.rows[0]).toMatchObject({ kind: 'criterion', marks: 1, permittedMarks: [0, 0.5, 1], verbatim: 'Naeba (0 marks if written in Hiragana)' });
    expect(found.rows[0].contextNote).toContain('0 for Hiragana or incorrect content');
    expect(found.rows[0].contextNote).toContain('otherwise correct content');
    expect(found.rows[0].contextNote).toContain('excluding Hiragana');
    for (const value of [0, 0.5, 1]) expect(marksClaimed(found, { 'r-1': value })).toBe(value);
    expect(marksClaimed(found, { 'r-1': 0.25 })).toBe(0);
    const original = review.cards.find(card => card.id === found.id)!;
    expect(() => assertJapaneseNaebaException(original, review)).not.toThrow();
    for (const patch of [
      { id: 'ja-2011-ol-1-2-i' }, { year: 2012 }, { totalMarks: 2 },
      { questionText: 'An unrelated source question' },
      { answerLanguageRule: { otherLanguageMultiplier: 0.5, sourceText: 'Half marks', schemePages: [6] } },
      { sourceEvidence: { ...original.sourceEvidence, schemePages: [5] } },
      { sourceEvidence: { ...original.sourceEvidence, component: 'aural' } },
      { rows: [{ ...original.rows![0], permittedMarks: [0, 1] }] },
      { rows: [{ ...original.rows![0], contextNote: original.rows![0].contextNote!.replace('0 for Hiragana', '0.5 for Hiragana') }] },
    ]) expect(() => assertJapaneseNaebaException({ ...original, ...patch }, review)).toThrow();
    for (const changed of [
      { ...review, selectors: review.selectors.filter(selector => !('parts' in selector) || !selector.text.startsWith('(Half marks if not answered')) },
      { ...review, selectors: review.selectors.map(selector => ({ ...selector, page: selector.page === 6 ? 5 : selector.page })) },
      { ...review, sources: review.sources.map(source => ({ ...source, sha256: 'changed' })) },
      { ...review, sources: review.sources.map(source => ({ ...source, path: 'wrong-source.pdf' })) },
      { ...review, selectors: review.selectors.map(selector => 'parts' in selector ? { ...selector, parts: [{ row: 0, group: 0 }] } : selector) },
    ]) expect(() => assertJapaneseNaebaException(original, changed)).toThrow();
  });

  it('applies the general half-language rule only to reading, with no invented listening penalty', () => {
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(23);
    for (const found of cards.filter(card => card.answerLanguageRule)) expect(found.answerLanguageRule).toEqual({ otherLanguageMultiplier: 0.5, sourceText: '(Half marks if not answered in the appropriate language)', schemePages: [6] });
    expect(cards.filter(card => card.audioMaterial)).toHaveLength(24);
    for (const found of cards.filter(card => card.audioMaterial || card.id === 'ja-2011-ol-4')) expect(found.answerLanguageRule).toBeUndefined();
    expect(cards.filter(card => card.extraneousMaterialRule)).toEqual([]);
  });

  it('keeps exact printed choice-label discrepancies visible', () => {
    expect(point('1-4-iii').questionText).toContain('c. Fred');
    expect(point('1-4-iii').questionText).toContain('c. Naruto');
    expect(point('3b-1').rows[4].verbatim).toBe('d. で');
    expect(point('3b-1').rows[4].contextNote).toContain('paper labels it b');
    expect(point('2c').rows[0].verbatim).toBe('b. にほん');
    expect(point('2c').rows[0].contextNote).toContain('b.  にはん');
    expect(point('2c').rows[0].contextNote).toContain('b. にほん');
  });

  it('binds the single kanji correction to both literal sources and the same option letter', () => {
    const original = review.cards.find(card => card.id === 'ja-2011-ol-2c')!;
    expect([...japaneseBoundBankAnswers(original, review)]).toEqual(['b. にほん']);
    for (const changed of [
      { ...review, sourceAnswerBindings: [] },
      { ...review, sourceAnswerBindings: review.sourceAnswerBindings.map(binding => ({ ...binding, answer: 'a. にはん' })) },
      { ...review, selectors: review.selectors.filter(selector => selector.text !== 'b. にほん') },
      { ...review, selectors: review.selectors.filter(selector => selector.text !== 'b.  にはん') },
      { ...review, selectors: review.selectors.map(selector => selector.page === 8 ? { ...selector, page: 7 } : selector) },
      { ...review, sources: review.sources.map(source => ({ ...source, sha256: 'changed' })) },
    ]) expect(() => japaneseBoundBankAnswers(original, changed)).toThrow();
    for (const patch of [
      { verbatim: 'a. にはん' }, { marks: 2 },
      { contextNote: original.rows![0].contextNote!.replace('b.  にはん', 'b. にほん') },
      { contextNote: original.rows![0].contextNote!.replace('b. にほん', 'an unspecified option') },
    ]) expect(() => japaneseBoundBankAnswers({ ...original, rows: [{ ...original.rows![0], ...patch }, ...original.rows!.slice(1)] }, review)).toThrow();
  });

  it('scores the required listening pairs and whole phone blocks at their printed tariffs', () => {
    expect(point('lb-2-ii').questionText).toContain('What kind of donut');
    expect(point('lb-2-ii').questionText).toContain('What drink');
    expect(point('lb-2-ii').rows.map(row => row.marks)).toEqual([3, 3]);
    expect(marksClaimed(point('lb-2-ii'), { 'r-1': 'yes', 'r-2': 'yes' })).toBe(6);
    const phone = point('lc-2-ii');
    expect(phone.rows.map(row => row.verbatim)).toEqual(['2 (4) 44', '17(0)1']);
    expect(phone.rows.map(row => row.marks)).toEqual([2, 2]);
    expect(phone.questionFigure?.includesPrompt).toBe(true);
    expect(marksClaimed(phone, { 'r-1': 'yes' })).toBe(2);
    expect(marksClaimed(phone, { 'r-1': 'yes', 'r-2': 'yes' })).toBe(4);
  });

  it('retains all twelve listening statements and binds the corroborated positive answer', () => {
    const found = card('ld');
    if (found.kind !== 'rubric' || found.rubric.system !== 'language-points') throw new Error('Expected listening pool');
    const rubric = found.rubric;
    expect(rubric.count).toBe(8);
    expect(rubric.groups).toHaveLength(12);
    expect(rubric.groups.map(group => group.rows[0].text)).toEqual(['F', 'T', 'T', 'F', 'T', 'T', 'F', 'F', 'T', 'True', 'T', 'F']);
    expect(rubric.groups[9].label).toBe('Kenichi is allowed to use the internet.');
    expect(rubric.markingGuideNote).toContain('Kenichi is not allowed to use the internet.');
    expect(rubric.markingGuideNote).toContain('can use internet');
    expect(rubric.markingGuideNote).toContain('not direct audio listening verification');
    const scores: LanguageScores = {};
    for (const group of rubric.groups) { scores[`language:group:${group.id}`] = 1; scores[`language:row:${group.id}:answer`] = 1; }
    expect(languagePointsMarks(rubric, scores)).toBe(24);
    const original = review.cards.find(card => card.id === found.id)!;
    const recording = audioRegistry.find(record => record.year === 2011)!;
    expect(() => assertJapanese2011ListeningCorrection(original, review, higherReview, recording)).not.toThrow();
    for (const changed of [
      { ...review, sourceCorrections: [] },
      { ...review, sourceCorrections: review.sourceCorrections.map(correction => ({ ...correction, resolvedAnswer: 'F' })) },
      { ...review, selectors: review.selectors.filter(selector => selector.text !== 'Kenichi is allowed to use the internet.') },
      { ...review, selectors: review.selectors.filter(selector => selector.text !== '(x) Kenichi is not allowed to use the internet.') },
      { ...review, sources: review.sources.map(source => ({ ...source, sha256: 'changed' })) },
    ]) expect(() => assertJapanese2011ListeningCorrection(original, changed, higherReview, recording)).toThrow();
    for (const changed of [
      { ...higherReview, selectors: higherReview.selectors.filter(selector => !selector.text.includes('can use internet')) },
      { ...higherReview, sources: higherReview.sources.map(source => ({ ...source, sha256: 'changed' })) },
      { ...higherReview, cards: higherReview.cards.filter(card => card.id !== 'ja-2011-hl-ld-2-ii') },
    ]) expect(() => assertJapanese2011ListeningCorrection(original, review, changed, recording)).toThrow();
    for (const changed of [
      { ...recording, paperFileids: ['LC058GLPA00EV.pdf'] },
      { ...recording, source: { ...recording.source, secFileid: 'another.mp3' } },
      { ...recording, verification: { ...recording.verification, sha256: 'changed' } },
    ]) expect(() => assertJapanese2011ListeningCorrection(original, review, higherReview, changed)).toThrow();
    expect(() => assertJapanese2011ListeningCorrection({ ...original, rubric: { ...original.rubric, groups: original.rubric!.groups!.map(group => group.id === 'item-10' ? { ...group, rows: [{ id: 'answer', text: 'F', marks: 3 }] } : group) } }, review, higherReview, recording)).toThrow();
  });

  it('keeps both complete writing options and applies the exact content/length boundaries', () => {
    const rubric = writing('4');
    expect(card('4').sourceMaterial?.pages).toEqual([11, 12]);
    expect(card('4').questionText).toContain('at least five');
    expect(card('4').questionText).toContain('any five');
    expect(card('4').questionText).toContain('何曜（よう）日ですか');
    expect(card('4').questionText).toContain('名前（なまえ）は何ですか');
    expect(rubric.criteria.map(c => c.maxMarks)).toEqual([7, 7, 7, 7, 7, 5, 40]);
    expect(rubric.criteria.at(-1)?.bands?.map(band => [band.marks[0], band.marks.at(-1)])).toEqual([[0, 9], [10, 27], [28, 40]]);
    expect(rubric.criteria.at(-1)?.limits?.[0].bands?.map(band => [band.marks[0], band.marks.at(-1)])).toEqual([[0, 6], [7, 16], [17, 26]]);
    const scores: LanguageScores = { [languageLengthId('characters')]: 150 };
    for (const c of rubric.criteria) scores[`language:${c.id}`] = c.maxMarks;
    expect(languageWritingMarks(rubric, scores)).toBe(80);
    scores[languageLengthId('characters')] = 149;
    expect(languageCriterionValue(rubric, 'expression', scores)).toBe(26);
    scores[languageLengthId('characters')] = 150;
    expect(languageCriterionValue(rubric, 'expression', scores)).toBe(40);
    for (const c of rubric.criteria.filter(c => c.id !== 'expression')) scores[`language:${c.id}`] = 0;
    Object.assign(scores, { 'language:question-1': 7, 'language:question-2': 7, 'language:question-3': 1, 'language:discretionary': 5 });
    expect(languageCriterionValue(rubric, 'expression', scores)).toBe(26);
    scores['language:question-3'] = 2;
    expect(languageCriterionValue(rubric, 'expression', scores)).toBe(40);
    expect(writing('2d').criteria.map(c => c.permittedMarks)).toEqual([[0, 2], [0, 2], [0, 1]]);
  });

  it('preserves all nine original Atlas anchors and adds the four missing task groups', () => {
    const tags = JSON.parse(readFileSync(resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'), 'utf8'));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2011 && paper.fileid === task.atlas.fileid);
      const topic = tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber);
      expect([topic.primary, topic.secondary], runtime.id).toContain(runtime.topicId);
      expect(sidecar.band).toEqual([1, 13]);
    }
    const written = map('LC058GLP000EV.pdf');
    expect(written.q.map(question => question.n)).toEqual(Array.from({ length: 9 }, (_, i) => String(i + 1)));
    // Original scheme p8 places D's heading at .404 and its prompt at .455.
    expect(written.q.find(q => q.n === '6')?.region).toEqual([{ p: 8, r: [0, 0.39, 1, 1] }]);
    expect(written.q.find(q => q.n === '9')?.paperRegion?.map(region => region.p)).toEqual([11, 12]);
    expect(map('LC058GLPA00EV.pdf').q.map(question => question.n)).toEqual(['1', '2', '3', '4']);
    expect(cards.filter(card => card.audioMaterial && card.topicId === 'japanese-6-1')).toEqual([]);
    expect(JSON.stringify(cards)).not.toContain('�');
  });
});
