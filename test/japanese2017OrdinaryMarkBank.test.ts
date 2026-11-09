import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import reviewed from '../components/MarkBank/cards/japanese/reviewed.json';
import aliases from '../components/MarkBank/cards/japanese/aliases.json';
import census from '../scripts/markbank/authoring/reviews/japanese-2017-ol-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2017-ol.json';
import { languagePointsMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
import { tariffReconciles, UNPRINTED_ANSWER } from '../types/markBank';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = ordinary.filter(card => card.year === 2017);
const idFor = (key: (string | number | null)[]) => `ja-2017-ol-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2017-ol-${suffix}`)!;
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
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2017/${fileid}.json`), 'utf8'));

describe('Japanese 2017 Ordinary independent source review', () => {
  it('covers all 54 independent tasks and all 40 original physical pages', () => {
    expect(cards).toHaveLength(54);
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
    expect(total(cards.filter(card => card.audioMaterial))).toBe(100);
    expect(total(cards)).toBe(300);
    expect(census.candidateMaximum).toMatchObject({ written: 200, listening: 100, total: 300 });
    expect(Object.values(census.pageRoles).map(pages => Object.keys(pages).length)).toEqual([16, 8, 16]);
    expect(review.sources.map(source => ({ component: source.document, path: source.path, sha256: source.sha256 }))).toEqual(census.sources);
    expect(review.sources.map(source => source.sha256)).toEqual([
      '9922a1801afe3fb3647800e0d09bac6c079a59f3f7fb5a40e6aed4bf8b738bf2',
      '3918ea5765a059289b06f22201c958a6a876369edb66b62eec976018288864ce',
      'bd72510e1ac85538e0c4fca9c479ec95ce3edec7255e00421e65243420b662af',
    ]);
    for (const source of review.sources) expect(source.pagesReviewed).toEqual(Object.keys(census.pageRoles[source.document as keyof typeof census.pageRoles]).map(Number));
  });

  it('adds 54 independently reviewed cards without inventing original aliases', () => {
    const original = readFileSync(resolve(__dirname, '../components/MarkBank/cards/japanese/ordinary.ts'), 'utf8');
    expect(createHash('sha256').update(original).digest('hex')).toBe('83a3b57745ae80882d11a3346ab34cefba7b70d801701b87202493e0650983ef');
    const originalIds = [...original.matchAll(/^ {4}id: "([^"]+)"/gm)].map(match => match[1]);
    expect(originalIds).toHaveLength(261);
    expect(originalIds.some(id => id.startsWith('ja-2017-'))).toBe(false);
    expect(cards.every(card => !originalIds.includes(card.id))).toBe(true);
    expect(review.consolidations).toEqual([]);
    expect(Object.keys(aliases)).toHaveLength(391);
    expect(Object.keys(aliases).filter(id => id.startsWith('ja-2017-'))).toEqual([]);
  });

  it('keeps complete required pools, exact alternatives and all cloze words', () => {
    for (const [suffix, quota, total] of [['2b', 5, 15], ['2c', 10, 10], ['3b-1', 5, 10], ['3b-2', 5, 10], ['4', 10, 30]] as const) {
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
    expect(points('2b').groups.map(group => group.rows[0].text)).toEqual(['False', 'True', 'True', 'False', 'False']);
    expect(points('2c').groups.map(group => group.rows[0].text)).toEqual(['Japan', 'food', 'new', 'study', 'day', 'child', 'university', 'like', 'middle', 'expensive']);
    expect(points('3b-1').groups.map(group => group.rows[0].text)).toEqual(['きびしくないです。／きびしくありません。', '好きじゃないです／じゃありません。', 'ありません。', '日本人じゃないです／じゃありません。', 'しませんでした。']);
    expect(points('3b-2').groups.map(group => group.rows[0].text)).toEqual(['b. と', 'c. は', 'c. を', 'a. が', 'c. から']);
    expect(points('4').groups.map(group => group.rows[0].text)).toEqual(['18 才の', 'パンケーキ', '行きます', 'かぞく', '大好き', 'バス', 'レストラン', '8 時に', 'あります', '20 人']);
    expect(card('4').questionText.replace(/\s+/g, ' ')).toContain('A word should be used only once.');
  });

  it('retains six explicit date components and discloses the conflicting eight-mark heading', () => {
    expect(point('1-1').rows.map(row => row.verbatim)).toEqual(['7', '3', '8', '6', '2']);
    expect(point('1-1').rows.map(row => row.marks)).toEqual(Array(5).fill(2));
    const table = point('1-5-i');
    expect(table.rows.map(row => row.verbatim)).toEqual(['25th', 'August', 'Friday', '6th', 'September', 'Wednesday']);
    expect(table.rows.map(row => row.marks)).toEqual(Array(6).fill(1));
    expect(table.taskGroups?.map(group => group.marks)).toEqual([3, 3]);
    expect(table.totalMarks).toBe(6);
    expect(table.rows[0].contextNote).toContain('heading prints 8 marks');
    expect(table.rows[0].contextNote).toContain('totalling 6');
    expect(marksClaimed(table, Object.fromEntries(table.rows.map(row => [row.id, 1])))).toBe(6);
    expect(census.sourceDiscrepancies.find(item => item.taskKey?.[0] === '1')?.evidence).toContain('six explicit components total6');
  });

  it('retains each complete finite choice and unprinted culture task without inventing tariffs', () => {
    for (const [suffix, quota, available, marks] of [['1-2', 3, 6, 2], ['1-4', 2, 6, 2], ['2a-2', 2, 3, 2], ['2a-3', 1, 2, 3], ['2a-4-ii', 1, 2, 3], ['3a-2', 1, 2, 2]] as const) {
      const found = point(suffix);
      expect(found.rows[0].group).toMatchObject({ claimMax: quota, perOption: marks });
      expect(found.rows[0].group?.options).toHaveLength(available);
      expect(marksClaimed(found, {}, { 'r-1': Array.from({ length: available }, (_, i) => i) })).toBe(quota * marks);
    }
    expect(point('2d').rows[0]).toMatchObject({ verbatim: UNPRINTED_ANSWER, unprinted: true, marks: 4, permittedMarks: [0, 2, 4] });
    expect(point('2d').rows[0].parts?.map(part => part.marks)).toEqual([2, 2]);
    expect(point('3a-4-i').rows.map(row => [row.verbatim, row.marks])).toEqual([['9 時から', 1], ['12 時まで', 1]]);
    expect(point('3a-4-ii').rows.map(row => [row.verbatim, row.marks])).toEqual([['じゅうどう / からて /けんどう', 3]]);
    expect(point('3a-4-iii').rows.map(row => [row.verbatim, row.marks])).toEqual([['4 月', 1], ['23 日', 1]]);
  });

  it('prices only the four missing phone digits and preserves the paired restaurant identity', () => {
    const phone = point('lb-1-iv');
    expect(phone.rows.map(row => [row.verbatim, row.marks])).toEqual([['5', 1], ['7', 1], ['9', 1], ['2', 1]]);
    expect(phone.rows.every(row => row.contextNote?.includes('011-547-1929'))).toBe(true);
    expect(phone.questionRef).toBe('2017 OL Section LB Q1(iv)');
    for (const roman of ['i', 'ii', 'iii']) {
      const found = point(`ld-2-${roman}`);
      expect(found.questionRef).toBe(`2017 OL Section LD Q2(${roman})`);
      expect(found.stem?.replace(/\s+/g, ' ')).toContain('(iv) At the restaurant');
      expect(found.rows[0].contextNote).toContain('facing Irish heading');
    }
    expect(point('ld-2-i').rows[0].group?.options).toHaveLength(3);
    expect(point('ld-2-ii').rows[0].group?.options).toHaveLength(5);
  });

  it('preserves all seven hobby prompts and independent five-response expression caps', () => {
    const rubric = points('5');
    expect(rubric.count).toBe(5);
    expect(rubric.groups).toHaveLength(7);
    expect(rubric.groups[6].label).toContain('他（ほか）のしゅみは何ですか。');
    expect(card('5').questionText).not.toContain('もう一つ');
    expect(rubric.markingGuideNote).toContain('もう一つのしゅみがほしいですか。何をしたいですか。');
    expect(rubric.markingGuideNote).toContain('not an extra or replacement question');
    const scores: LanguageScores = {};
    for (const group of rubric.groups) {
      expect(group.criteria?.map(criterion => criterion.maxMarks)).toEqual([5, 5]);
      scores[`language:group:${group.id}`] = 1;
      for (const criterion of group.criteria ?? []) scores[`language:${criterion.id}`] = 5;
    }
    expect(languagePointsMarks(rubric, scores)).toBe(50);
    for (const group of rubric.groups.slice(5)) scores[`language:group:${group.id}`] = 0;
    scores['language:item-1-content'] = 3;
    expect(languagePointsMarks(rubric, scores)).toBe(46);
    scores['language:item-2-content'] = 3;
    expect(languagePointsMarks(rubric, scores)).toBe(42);
    scores['language:item-1-content'] = 4;
    expect(languagePointsMarks(rubric, scores)).toBe(45);
    scores['language:group:item-2'] = 0;
    expect(languagePointsMarks(rubric, scores)).toBe(39);
  });

  it('binds only the 25 reading and 27 listening language rules to exact selectors', () => {
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(52);
    expect(cards.filter(card => card.answerLanguageRule?.penalizedLanguage === 'Japanese')).toHaveLength(27);
    for (const found of cards.filter(card => card.answerLanguageRule)) {
      expect(review.selectors.some(selector => selector.document === 'scheme' && selector.text === found.answerLanguageRule?.sourceText)).toBe(true);
      expect(found.answerLanguageRule?.otherLanguageMultiplier).toBe(0.5);
    }
    for (const suffix of ['2a-1', '2a-2', '2a-3', '2a-4-i', '2a-4-ii']) expect(point(suffix).rows[0].contextNote).toBe('A. (16 marks) Half marks if written in Japanese.');
    expect(cards.some(card => card.extraneousMaterialRule)).toBe(false);
    expect(card('4').answerLanguageRule).toBeUndefined();
    expect(card('5').answerLanguageRule).toBeUndefined();
  });

  it('retains the original twenty written and four listening Atlas anchors and eight crops', () => {
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(8);
    const tags = JSON.parse(readFileSync(resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'), 'utf8'));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      expect(task.paperPages, runtime.id).toContain(group.pP);
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2017 && paper.fileid === task.atlas.fileid);
      expect(tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber).primary, runtime.id).toBe(runtime.topicId);
      expect(sidecar.band).toEqual([1, 16]);
    }
    expect(map('LC058GLP000EV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 20 }, (_, i) => String(i + 1)));
    expect(map('LC058GLPA00EV.pdf').q.map(question => question.n)).toEqual(['1', '2', '3', '4']);
  });
});
