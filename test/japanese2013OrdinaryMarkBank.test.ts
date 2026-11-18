import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import rawCards from '../components/MarkBank/cards/japanese/reviewed.json';
import census from '../scripts/markbank/authoring/reviews/japanese-2013-ol-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2013-ol.json';
import { tariffReconciles } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
import { languageMarks, languagePointsMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = ordinary.filter(card => card.year === 2013);
const idFor = (key: (string | number | null)[]) => `ja-2013-ol-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2013-ol-${suffix}`)!;
const point = (suffix: string) => {
  const found = card(suffix);
  if (found.kind !== 'question') throw new Error(`Expected point card ${suffix}`);
  return found;
};
const languageCard = (suffix: string) => {
  const found = card(suffix);
  if (found.kind !== 'rubric') throw new Error(`Expected language card ${suffix}`);
  return found;
};
const pool = (suffix: string) => {
  const found = languageCard(suffix);
  if (found.rubric.system !== 'language-points') throw new Error(`Expected pool ${suffix}`);
  return found.rubric;
};
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2013/${fileid}.json`), 'utf8'));

describe('Japanese 2013 Ordinary independent original-source review', () => {
  it('covers all 51 independently inventoried tasks and all 36 original pages', () => {
    expect(cards).toHaveLength(51);
    expect(cards.map(card => card.id).sort()).toEqual(census.tasks.map(task => idFor(task.key)).sort());
    for (const task of census.tasks) {
      const found = cards.find(card => card.id === idFor(task.key))!;
      expect(found.totalMarks, found.id).toBe(task.marks);
      expect(tariffReconciles(found), found.id).toBe(true);
      expect(rawCards.find(card => card.id === found.id)!.sourceEvidence).toMatchObject({ component: task.component, paperPages: task.paperPages, schemePages: task.schemePages });
    }
    expect(census.checksums).toEqual({ reading: 120, writing: 80, listening: 100, total: 300 });
    expect(Object.values(census.pageRoles).map(pages => Object.keys(pages).length)).toEqual([16, 8, 12]);
    expect(review.sources.map(source => ({ component: source.document, path: source.path, sha256: source.sha256 }))).toEqual(census.sources);
    for (const source of review.sources) expect(source.pagesReviewed).toEqual(Object.keys(census.pageRoles[source.document as keyof typeof census.pageRoles]).map(Number));
    expect(review.consolidations).toEqual([]);
  });

  it('keeps full required pools, original examples and separate building/floor tariffs', () => {
    expect(point('1a').rows.map(row => [row.verbatim, row.marks])).toEqual([['4', 3], ['2', 3], ['1', 3], ['8', 3], ['3', 3]]);
    expect(pool('1b').groups.map(group => group.rows.map(row => [row.text, row.marks]))).toEqual([
      [['main', 2], ['9 / B1', 2]], [['annex', 2], ['1', 2]], [['main', 2], ['5', 2]], [['annex', 2], ['2', 2]], [['main', 2], ['8', 2]],
    ]);
    expect(point('2a-1').rows.map(row => row.verbatim.trim())).toEqual(['Totoro', 'Hello Kitty', 'Doraemon', 'Super Mario']);
    expect(point('3a-1').rows.map(row => row.verbatim)).toEqual(['A', 'B', 'AB', 'O']);
    for (const [suffix, count, total] of [['1b', 5, 20], ['2b', 5, 15], ['3b', 10, 10], ['3c-1', 5, 10], ['3c-2', 5, 10]] as const) {
      const rubric = pool(suffix);
      expect(rubric.count).toBe(count);
      expect(rubric.groups).toHaveLength(count);
      const scores: LanguageScores = {};
      for (const group of rubric.groups) {
        scores[`language:group:${group.id}`] = 1;
        for (const row of group.rows) scores[`language:row:${group.id}:${row.id}`] = 1;
      }
      expect(languagePointsMarks(rubric, scores)).toBe(total);
    }
    expect(pool('3c-1').groups[3].rows[0].text).toBe('おもしろいです。');
    expect(pool('3c-2').markingGuideNote).toContain('original paper labels this pool C2');
  });

  it('preserves any two of the four named character details and Sarah’s one-mark partial', () => {
    const rubric = pool('2a-2');
    expect(rubric.count).toBe(2);
    expect(rubric.groups.map(group => group.label)).toEqual(['Sarah', 'Tom', 'Susan', 'Harry']);
    expect(rubric.groups[0].criteria![0]).toMatchObject({ maxMarks: 2, permittedMarks: [0, 1, 2] });
    expect(rubric.groups[0].criteria![0].guidance.join(' ')).toContain('Electric guitar (guitar = 1 mark)');
    expect(rubric.groups.slice(1).map(group => group.rows[0].text)).toEqual(['T-shirt', 'Sayama', 'Kawasaki']);
    const partial = { 'language:group:item-1': 1, 'language:answer': 1, 'language:group:item-2': 1, 'language:row:item-2:answer': 1 };
    expect(languagePointsMarks(rubric, partial)).toBe(3);
    expect(languagePointsMarks(rubric, { ...partial, 'language:answer': 2 })).toBe(4);
    expect(languageMarks(languageCard('2a-2'), { ...partial, 'language:other-language:group:item-1': 1 })).toBe(2.5);
    const full: LanguageScores = { 'language:answer': 2 };
    for (const group of rubric.groups) { full[`language:group:${group.id}`] = 1; full[`language:row:${group.id}:answer`] = 1; }
    expect(languagePointsMarks(rubric, full)).toBe(4);
    for (const name of ['Sarah', 'Tom', 'Susan', 'Harry']) expect(card('2a-2').questionText).toContain(name);
    expect(cards.filter(card => card.id.startsWith('ja-2013-ol-2a-2'))).toHaveLength(1);
  });

  it('retains each truth/evidence allocation and discloses the literal quotation discrepancy', () => {
    const rubric = pool('2b');
    expect(rubric.groups.map(group => group.rows.map(row => row.marks))).toEqual(Array(5).fill([2, 1]));
    expect(rubric.groups.map(group => group.rows[0].text)).toEqual(['False', 'True', 'True', 'False', 'True']);
    expect(rubric.groups[4].rows[1].text).toBe('あかとくるのエレキギターです。');
    expect(rubric.markingGuideNote).toContain('黒（くろ）');
    expect(rubric.markingGuideNote).toContain('あかとくる');
    const culture = point('2c');
    expect(culture.rows[0]).toMatchObject({ kind: 'criterion', unprinted: true, marks: 5 });
    expect(culture.rows[0].parts?.map(part => [part.marks, part.permittedMarks])).toEqual([[2, [0, 2]], [2, [0, 2]], [1, [0, 1]]]);
    expect(marksClaimed(culture, { 'r-1:point-1': 2, 'r-1:point-2': 2, 'r-1:discretionary': 1 })).toBe(5);
    expect(marksClaimed(culture, { 'r-1:point-1': 1, 'r-1:point-2': 0, 'r-1:discretionary': 1 })).toBe(1);
  });

  it('prices exactly the missing phone digits and the two explicit partial responses', () => {
    const phone = point('lb-2-v');
    expect(phone.rows.map(row => [row.verbatim, row.marks])).toEqual([['0', 1], ['5', 1], ['4', 1], ['5', 1]]);
    expect(phone.rows.every(row => row.contextNote?.includes('1 mark for each correct number'))).toBe(true);
    expect(phone.rows.every(row => row.contextNote?.includes('printed 06-81 and 4 are given'))).toBe(true);
    expect(phone.questionFigure).toBeDefined();
    expect(phone.audioMaterial).toBeDefined();
    expect(marksClaimed(phone, { 'r-1': 1, 'r-2': 1, 'r-3': 1, 'r-4': 1 })).toBe(4);
    for (const [suffix, allowed, invalid] of [['3a-2-ii', [0, 2, 3], 1], ['ld-8', [0, 1, 3], 2]] as const) {
      const found = point(suffix);
      expect(found.rows[0].permittedMarks).toEqual([...allowed]);
      for (const mark of allowed) expect(marksClaimed(found, { 'r-1': mark })).toBe(mark);
      expect(marksClaimed(found, { 'r-1': invalid })).toBe(0);
    }
    expect(point('3a-2-ii').rows[0].contextNote).toContain('私のあね 2 mark');
    expect(point('ld-8').rows[0].contextNote).toContain('(restaurants, 1 mark)');
    expect(point('ld-1').rows[0]).toMatchObject({ marks: 1, verbatim: 'Chiba (close approximation of the word)' });
  });

  it('uses Ordinary’s one-direction tariff and retains every accepted listening alternative', () => {
    const row = point('lc-3-ii').rows[0];
    if (row.kind !== 'anyN') throw new Error('Expected one-direction pool');
    expect(row.group).toMatchObject({ claimMax: 1, perOption: 4 });
    expect(row.group.options.map(option => option.trim())).toEqual(['(next corner) turn right', 'walk (go straight)for 2 minutes', 'on the left', 'beside the bank']);
    expect(marksClaimed(point('lc-3-ii'), {}, { 'r-1': [1] })).toBe(4);
    expect(marksClaimed(point('lc-3-ii'), {}, { 'r-1': [0, 1, 2, 3] })).toBe(4);
    expect(point('lb-2-ii').rows[0].group?.options).toHaveLength(6);
    expect(point('lc-2-iii').rows[0].group?.options).toHaveLength(6);
    expect(cards.filter(card => card.audioMaterial)).toHaveLength(33);
  });

  it('keeps ten cloze blanks, all exact alternatives and source-local no-reuse spellings', () => {
    const found = point('4');
    expect(found.rows).toHaveLength(10);
    expect(found.rows.map(row => row.group?.options)).toEqual([
      ['好き'], ['二年生'], ['します'], ['クラス'], ['先生', 'クラス'], ['べんとう'], ['飲みます'], ['おいしい', '好き'], ['ともだち', '先生', '二年生', 'クラス'], ['何'],
    ]);
    expect(found.taskGroups?.map(group => group.rowIds)).toEqual(found.rows.map(row => [row.id]));
    expect(found.rows.every(row => row.contextNote?.includes('The same word may not be used twice.'))).toBe(true);
    for (const index of [1, 4, 8]) {
      expect(found.rows[index].contextNote).toContain('せんせい/先生');
      expect(found.rows[index].contextNote).toContain('２年生/二年生');
      expect(found.rows[index].contextNote).toContain('only once');
    }
    expect(marksClaimed(found, {}, Object.fromEntries(found.rows.map(row => [row.id, [0]])))).toBe(30);
    expect(found.rows.some(row => row.group?.options.includes('こんにちは'))).toBe(false);
    expect(review.sourceAnswerBindings.map(binding => [binding.answer, binding.rowIds])).toEqual([['先生', ['r-5', 'r-9']], ['二年生', ['r-2', 'r-9']]]);
  });

  it('keeps all writing bands, the local 2+3 instruction and independent expression caps', () => {
    const rubric = pool('5');
    expect(rubric.count).toBe(5);
    expect(rubric.groups).toHaveLength(7);
    for (const group of rubric.groups) {
      const [content, expression] = group.criteria!;
      expect(content.bands?.map(band => band.marks)).toEqual([[1], [2], [3, 4], [5]]);
      expect(expression.bands?.map(band => band.marks)).toEqual([[1], [2, 3], [4, 5]]);
      const scores = { [`language:group:${group.id}`]: 1, [`language:${content.id}`]: 3, [`language:${expression.id}`]: 5 };
      expect(languagePointsMarks(rubric, scores)).toBe(6);
      expect(languagePointsMarks(rubric, { ...scores, [`language:${content.id}`]: 4 })).toBe(9);
    }
    const six = rubric.groups[5].criteria![0];
    expect(six.guidance.join(' ')).toContain('(2 marks)');
    expect(six.guidance.join(' ')).toContain('(3 marks)');
    for (const partial of [1, 2, 3, 4]) expect(languagePointsMarks(rubric, { 'language:group:item-6': 1, [ `language:${six.id}` ]: partial })).toBe(partial);
    expect(languagePointsMarks(rubric, { 'language:group:item-1': 1, 'language:item-1-content': 3, 'language:item-1-expression': 5,
      'language:group:item-2': 1, 'language:item-2-content': 4, 'language:item-2-expression': 5 })).toBe(15);
    const full: LanguageScores = {};
    for (const group of rubric.groups) { full[`language:group:${group.id}`] = 1; for (const criterion of group.criteria!) full[`language:${criterion.id}`] = 5; }
    expect(languagePointsMarks(rubric, full)).toBe(50);
  });

  it('binds only the printed reading/listening language rules and preserves all 27 original Atlas anchors', () => {
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(49);
    for (const found of cards.filter(card => card.answerLanguageRule)) {
      const rule = found.answerLanguageRule!;
      expect(rule.otherLanguageMultiplier).toBe(0.5);
      expect(rule.schemePages).toEqual([found.audioMaterial ? 3 : 5]);
      expect(rule.penalizedLanguage).toBe(found.audioMaterial ? 'Japanese' : undefined);
      expect(review.selectors.some(selector => selector.document === 'scheme' && selector.page === rule.schemePages[0] && selector.text === rule.sourceText)).toBe(true);
    }
    expect(cards.some(card => card.extraneousMaterialRule)).toBe(false);
    for (const suffix of ['4', '5']) expect(card(suffix).answerLanguageRule).toBeUndefined();
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(12);
    const tags = JSON.parse(readFileSync(resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'), 'utf8'));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      if (task.component === 'aural') expect(task.paperPages).toContain(group.pP);
      else {
        const span = census.atlasSourceSpans[`written${task.atlas.questionNumber}` as keyof typeof census.atlasSourceSpans];
        expect(span).toContain(group.pP);
        expect(task.paperPages.every(page => (span as number[]).includes(page))).toBe(true);
      }
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2013 && paper.fileid === task.atlas.fileid);
      const topic = tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber);
      expect([topic.primary, topic.secondary], runtime.id).toContain(runtime.topicId);
      expect(sidecar.band).toEqual([1, 12]);
    }
    expect(map('LC058GLP000EV.pdf').q).toHaveLength(9);
    expect(map('LC058GLPA00EV.pdf').q).toHaveLength(18);
    expect(JSON.stringify([cards, review.selectors])).not.toContain('�');
  });
});
