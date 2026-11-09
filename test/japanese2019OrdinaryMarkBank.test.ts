import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import reviewed from '../components/MarkBank/cards/japanese/reviewed.json';
import aliases from '../components/MarkBank/cards/japanese/aliases.json';
import census from '../scripts/markbank/authoring/reviews/japanese-2019-ol-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2019-ol.json';
import { languagePointsMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import { tariffReconciles, UNPRINTED_ANSWER } from '../types/markBank';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = ordinary.filter(card => card.year === 2019);
const idFor = (key: (string | number | null)[]) => `ja-2019-ol-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2019-ol-${suffix}`)!;
const point = (suffix: string) => {
  const found = card(suffix);
  if (found.kind !== 'question') throw new Error(`Expected point card: ${suffix}`);
  return found;
};
const points = (suffix: string) => {
  const found = card(suffix);
  if (found.kind !== 'rubric' || found.rubric.system !== 'language-points') throw new Error(`Expected grouped rubric: ${suffix}`);
  return found.rubric;
};
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2019/${fileid}.json`), 'utf8'));

describe('Japanese 2019 Ordinary independent source review', () => {
  it('covers all 56 independent tasks and all 40 original physical pages', () => {
    expect(cards).toHaveLength(56);
    expect(cards.map(card => card.id).sort()).toEqual(census.tasks.map(task => idFor(task.key)).sort());
    for (const task of census.tasks) {
      const found = cards.find(card => card.id === idFor(task.key))!;
      expect(found.totalMarks, found.id).toBe(task.marks);
      expect(tariffReconciles(found), found.id).toBe(true);
      expect(reviewed.find(card => card.id === found.id)!.sourceEvidence).toMatchObject({ component: task.component, paperPages: task.paperPages, schemePages: task.schemePages });
    }
    const total = (selected: typeof cards) => selected.reduce((sum, card) => sum + card.totalMarks, 0);
    expect(total(cards.filter(card => !card.audioMaterial && !['4', 'Q5'].includes(card.section!)))).toBe(120);
    expect(total(cards.filter(card => ['4', 'Q5'].includes(card.section!)))).toBe(80);
    expect(total(cards.filter(card => card.audioMaterial))).toBe(102);
    expect(total(cards)).toBe(302);
    expect(census.candidateMaximum).toMatchObject({ publishedWritten: 200, publishedListening: 100, publishedTotal: 300, sumOfLocalTariffs: 302 });
    expect(Object.values(census.pageRoles).map(pages => Object.keys(pages).length)).toEqual([16, 8, 16]);
    expect(review.sources.map(source => ({ component: source.document, path: source.path, sha256: source.sha256 }))).toEqual(census.sources);
    expect(review.sources.map(source => source.sha256)).toEqual([
      '00e95d69d8ba77dcdb1e9650678e2120708bbba9fdf9cd1c395845ad11cd38e0',
      'da32fc28efe1458022116587a0b9cf72cff589496459bfdab41457458e752639',
      'be1782b438ce07304d7c624fde74c23d533b6f4a3ba0522613b38571d6c4b0f8',
    ]);
    for (const source of review.sources) expect(source.pagesReviewed).toEqual(Object.keys(census.pageRoles[source.document as keyof typeof census.pageRoles]).map(Number));
  });

  it('adds 56 independently reviewed cards without inventing original aliases', () => {
    const original = readFileSync(resolve(__dirname, '../components/MarkBank/cards/japanese/ordinary.ts'), 'utf8');
    expect(createHash('sha256').update(original).digest('hex')).toBe('83a3b57745ae80882d11a3346ab34cefba7b70d801701b87202493e0650983ef');
    const originalIds = [...original.matchAll(/^ {4}id: "([^"]+)"/gm)].map(match => match[1]);
    expect(originalIds).toHaveLength(261);
    expect(originalIds.some(id => id.startsWith('ja-2019-'))).toBe(false);
    expect(cards.every(card => !originalIds.includes(card.id))).toBe(true);
    expect(review.consolidations).toEqual([]);
    expect(Object.keys(aliases)).toHaveLength(391);
    expect(Object.keys(aliases).filter(id => id.startsWith('ja-2019-'))).toEqual([]);
  });

  it('retains all required answers and exact quotas without inventing optional items', () => {
    for (const [suffix, quota, total] of [['2b', 5, 15], ['2c', 10, 10], ['3a-5', 3, 9], ['3b-1', 5, 10], ['3b-2', 5, 10], ['4', 10, 30]] as const) {
      const rubric = points(suffix);
      expect(rubric.count).toBe(quota);
      expect(rubric.groups).toHaveLength(quota);
      const scores: LanguageScores = {};
      for (const group of rubric.groups) {
        scores[`language:group:${group.id}`] = 1;
        for (const row of group.rows) scores[`language:row:${group.id}:${row.id}`] = 1;
      }
      expect(languagePointsMarks(rubric, scores)).toBe(total);
    }
    expect(points('2b').groups.map(group => group.rows.map(row => row.marks))).toEqual(Array(5).fill([1, 2]));
    expect(points('2b').groups[1].rows.map(row => row.text)).toEqual(['False', '1 万いじょうのキャラクター・グッズがあります。']);
    expect(points('2c').groups[9].rows[0].text).toBe('want to buy (d)');
    expect(points('3b-1').groups[3].rows[0].text).toBe('買（か）いませんでした。');
    expect(points('3b-2').groups.map(group => group.rows[0].text)).toEqual(['c. に', 'a. は', 'b.で', 'a. から', 'a. と']);
  });

  it('preserves the cloze alternatives alongside the printed use-once restriction', () => {
    expect(points('4').groups.map(group => group.rows[0].marks)).toEqual(Array(10).fill(3));
    expect(points('4').groups[7].rows[0].text).toBe('買い物 / パーティー');
    expect(points('4').groups[8].rows[0].text).toBe('パーティー');
    expect(card('4').questionText).toContain('A word should be used only once.');
    expect(points('4').markingGuideNote).toContain('do not award the same パーティー token twice');
  });

  it('retains complete link/event tables, descending choices and separate component tariffs', () => {
    expect(point('1-1').rows.map(row => row.verbatim)).toEqual(['3', '10', '7', '4', '2']);
    expect(point('1-1').rows.map(row => row.marks)).toEqual(Array(5).fill(2));
    for (const suffix of ['1-2', '1-4']) expect(point(suffix).rows[0]).toMatchObject({ kind: 'anyN', group: { claimMax: 2, perOptionSteps: [2, 1] } });
    expect(point('1-5').rows.map(row => row.verbatim)).toEqual(['24th', 'July', 'Wednesday', '20th', 'August', 'Tuesday']);
    expect(point('1-5').rows.map(row => row.marks)).toEqual(Array(6).fill(1));
    expect(point('1-5').taskGroups?.map(group => group.marks)).toEqual([3, 3]);
    expect(point('1-6-iii').rows.map(row => [row.verbatim, row.marks])).toEqual([['6', 1], ['8', 1]]);
    expect(point('3a-1').rows[0]).toMatchObject({ verbatim: '2nd / 5th', marks: 2 });
    expect(point('3a-2').rows.map(row => [row.verbatim, row.marks])).toEqual([['His dad’s', 1], ['car', 2]]);
    expect(point('2d').rows[0]).toMatchObject({ verbatim: UNPRINTED_ANSWER, unprinted: true, marks: 5 });
    expect(point('2d').rows[0].parts?.map(part => part.marks)).toEqual([2, 2, 1]);
  });

  it('prices only the four missing phone digits and discloses the scheme subtotal contradiction', () => {
    const phone = point('lb-1-v');
    expect(phone.totalMarks).toBe(4);
    expect(phone.rows.map(row => [row.verbatim, row.marks])).toEqual([['5', 1], ['6', 1], ['9', 1], ['7', 1]]);
    for (const row of phone.rows) {
      expect(row.contextNote).toContain('03-3562-9704 (1 mark for each correct number)');
      expect(row.contextNote).toContain('misprinted(vi)');
    }
    expect(phone.questionRef).toBe('2019 OL Section LB Q1(v)');
    const hotel = cards.filter(card => card.id.startsWith('ja-2019-ol-lb-1-'));
    expect(hotel).toHaveLength(5);
    expect(hotel.map(card => card.totalMarks)).toEqual(Array(5).fill(4));
    const partB = cards.filter(card => card.id.startsWith('ja-2019-ol-lb-'));
    expect(partB.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(28);
    for (const found of partB) {
      if (found.kind !== 'question') throw new Error('Expected listening point task');
      for (const row of found.rows) expect(row.contextNote).toContain('Local listening tariffs add to 102 rather than the printed 100');
    }
  });

  it('scores five independent C5/E5 responses without inheriting a later expression cap', () => {
    const rubric = points('5');
    expect(rubric.count).toBe(5);
    expect(rubric.groups).toHaveLength(7);
    const scores: LanguageScores = {};
    for (const group of rubric.groups) {
      scores[`language:group:${group.id}`] = 1;
      expect(group.criteria?.map(criterion => criterion.maxMarks)).toEqual([5, 5]);
      for (const criterion of group.criteria!) scores[`language:${criterion.id}`] = 5;
    }
    expect(languagePointsMarks(rubric, scores)).toBe(50);
    for (let content = 0; content <= 5; content++) {
      scores['language:item-1-content'] = content;
      expect(languagePointsMarks(rubric, scores)).toBe(45 + content);
    }
    scores['language:item-1-content'] = 0;
    scores['language:item-1-expression'] = 1;
    expect(languagePointsMarks(rubric, scores)).toBe(41);
    scores['language:item-6-content'] = 0;
    expect(languagePointsMarks(rubric, scores)).toBe(41);
    expect(rubric.groups[0].criteria![1].bands?.map(band => band.marks)).toEqual([[1], [2, 3], [4, 5]]);
    expect(rubric.groups[2].label).toContain('たいへん');
    expect(rubric.markingGuideNote).not.toContain('cannot be higher');
  });

  it('binds exactly 26 reading and 28 listening language rules to the published selectors', () => {
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(54);
    expect(cards.filter(card => card.answerLanguageRule?.penalizedLanguage === 'Japanese')).toHaveLength(28);
    for (const found of cards) {
      expect(found.extraneousMaterialRule).toBeUndefined();
      if (['4', 'Q5'].includes(found.section!)) {
        expect(found.answerLanguageRule).toBeUndefined();
        continue;
      }
      const page = found.audioMaterial ? 10 : 4;
      const source = review.selectors.find(selector => selector.document === 'scheme' && selector.page === page && selector.row === 1)!;
      expect(found.answerLanguageRule).toEqual({ otherLanguageMultiplier: 0.5, sourceText: source.text, schemePages: [page], ...(found.audioMaterial ? { penalizedLanguage: 'Japanese' } : {}) });
    }
  });

  it('retains all multiple-choice alternatives and eight source crops', () => {
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(8);
    for (const suffix of ['la-1-ii', 'la-1-iii', 'la-2-ii', 'la-2-iii', 'la-3-ii', 'lb-1-i', 'lb-1-iii', 'lb-2-i', 'lb-2-ii', 'lc-1-i', 'lc-1-ii', 'lc-1-iii', 'lc-1-iv', 'lc-2-i', 'lc-2-ii', 'ld-i', 'ld-iii', 'ld-iv', 'ld-v', 'ld-vii']) {
      for (const label of ['a', 'b', 'c', 'd']) expect(card(suffix).questionText, suffix).toContain(`(${label})`);
    }
    for (const roman of ['i', 'ii', 'iii', 'iv']) for (const label of ['a', 'b', 'c', 'd']) expect(card(`3a-4-${roman}`).questionText).toContain(`${label}.`);
    expect(card('lc-1-i').stem?.replace(/\s+/g, ' ')).toContain('You will hear a conversation between Yoshiko and her mother.');
  });

  it('retains original Atlas identities, source crops and all scheme pages', () => {
    const tags = ['japanese.json', 'japanese-written-2019-2022.json'].flatMap(file => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/topic-tags/tags/${file}`), 'utf8')));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      expect(task.paperPages, runtime.id).toContain(group.pP);
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2019 && paper.fileid === task.atlas.fileid);
      expect(tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber).primary, runtime.id).toBe(runtime.topicId);
      expect(sidecar.band).toEqual([1, 16]);
    }
    expect(map('LC058GLP000BV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 23 }, (_, i) => String(i + 1)));
    expect(map('LC058GLPA00BV.pdf').q.map(question => question.n)).toEqual(['1', '2', '3', '4']);
  });
});
