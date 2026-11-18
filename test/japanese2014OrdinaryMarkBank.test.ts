import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import rawCards from '../components/MarkBank/cards/japanese/reviewed.json';
import census from '../scripts/markbank/authoring/reviews/japanese-2014-ol-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2014-ol.json';
import { tariffReconciles } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
import { languageMarks, languagePointsMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = ordinary.filter(card => card.year === 2014);
const idFor = (key: (string | number | null)[]) => `ja-2014-ol-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2014-ol-${suffix}`)!;
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
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2014/${fileid}.json`), 'utf8'));

describe('Japanese 2014 Ordinary independent original-source review', () => {
  it('covers all 52 independently inventoried tasks and all 40 original pages', () => {
    expect(cards).toHaveLength(52);
    expect(cards.map(card => card.id).sort()).toEqual(census.tasks.map(task => idFor(task.key)).sort());
    for (const task of census.tasks) {
      const found = cards.find(card => card.id === idFor(task.key))!;
      expect(found.totalMarks, found.id).toBe(task.marks);
      expect(tariffReconciles(found), found.id).toBe(true);
      expect(rawCards.find(card => card.id === found.id)!.sourceEvidence).toMatchObject({ component: task.component, paperPages: task.paperPages, schemePages: task.schemePages });
    }
    expect(census.checksums).toEqual({ reading: 120, writing: 80, listening: 100, total: 300 });
    expect(Object.values(census.pageRoles).map(pages => Object.keys(pages).length)).toEqual([16, 8, 16]);
    expect(review.sources.map(source => ({ component: source.document, path: source.path, sha256: source.sha256 }))).toEqual(census.sources);
    for (const source of review.sources) expect(source.pagesReviewed).toEqual(Object.keys(census.pageRoles[source.document as keyof typeof census.pageRoles]).map(Number));
    expect(review.consolidations).toEqual([]);
  });

  it('preserves whole required pools, gives no marks for examples and keeps all alternatives', () => {
    expect(point('1-1').rows.map(row => row.marks)).toEqual([2, 2, 2, 2, 2]);
    expect(point('1-2').rows.map(row => row.marks)).toEqual([2, 2, 2, 2, 2]);
    expect(point('1-3-ii').rows.map(row => row.verbatim)).toEqual(['パズル', 'ネクタイ']);
    for (const [suffix, count, each] of [['2a-4', 5, 2], ['2b', 10, 1], ['2c-1', 5, 2], ['2c-2', 5, 2], ['4', 10, 3]] as const) {
      const rubric = pool(suffix);
      expect(rubric.count).toBe(count);
      expect(rubric.groups).toHaveLength(count);
      const scores: LanguageScores = {};
      for (const group of rubric.groups) {
        scores[`language:group:${group.id}`] = 1;
        for (const row of group.rows) scores[`language:row:${group.id}:${row.id}`] = 1;
      }
      expect(languagePointsMarks(rubric, scores)).toBe(count * each);
    }
    expect(pool('2a-4').groups.map(group => group.rows.map(row => row.marks))).toEqual(Array(5).fill([1, 1]));
    expect(pool('2c-1').groups[1].rows[0].text).toContain('じゃありません');
    expect(pool('2c-1').groups[1].rows[0].text).toContain('ではありません');
    expect(pool('2c-1').groups[1].rows[0].text).toContain('ではないです');
    expect(pool('2c-1').groups[1].rows[0].text).toContain('じゃないです');
    expect(point('3-1').rows.map(row => row.verbatim)).toEqual(['Malaysia', 'Brazil', 'Ireland', 'Kyoto']);
    expect(point('3-4-i').questionText).toContain('ワールド・カップ');
    expect(point('3-4-ii').questionText).toContain('すんでいます');
    expect(point('3-4-ii').rows[0].contextNote).toContain('どこにすねいますか');
    expect(point('3-4-ii').rows[0].verbatim).toBe('かわさきにすんでいます。');
    expect(card('4').questionText).toContain('お元気');
    expect(pool('4').groups).toHaveLength(10);
    expect(pool('4').groups.map(group => group.rows[0].text)).not.toContain('お元気');
  });

  it('keeps each complete profile within the choose-two quota and its printed 1/1/1/2 tariff', () => {
    const rubric = pool('2a-3');
    expect(rubric.count).toBe(2);
    expect(rubric.groups).toHaveLength(4);
    expect(rubric.groups.map(group => group.rows.map(row => row.marks))).toEqual(Array(4).fill([1, 1, 1, 2]));
    expect(rubric.groups.some(group => group.label.includes('Okawa'))).toBe(false);
    const scores: LanguageScores = {};
    for (const group of rubric.groups) {
      scores[`language:group:${group.id}`] = 1;
      for (const row of group.rows) scores[`language:row:${group.id}:${row.id}`] = 1;
    }
    expect(languagePointsMarks(rubric, scores)).toBe(10);
    const mixed = { ...scores };
    for (const row of rubric.groups[0].rows) mixed[`language:other-language:row:person-1:${row.id}`] = 1;
    expect(languageMarks(languageCard('2a-3'), mixed)).toBe(7.5);
  });

  it('prices exactly the four missing phone digits and the printed partial dislike response', () => {
    const culture = point('2d');
    expect(culture.rows[0]).toMatchObject({ kind: 'criterion', unprinted: true, marks: 3 });
    expect(culture.rows[0].parts?.map(part => [part.marks, part.permittedMarks])).toEqual([[2, [0, 2]], [1, [0, 1]]]);
    expect(marksClaimed(culture, { 'r-1:point': 2, 'r-1:discretionary': 1 })).toBe(3);
    expect(marksClaimed(culture, { 'r-1:point': 0, 'r-1:discretionary': 1 })).toBe(1);
    expect(marksClaimed(culture, { 'r-1:point': 1, 'r-1:discretionary': 0 })).toBe(0);
    const phone = point('lb-1-iii');
    expect(phone.rows.map(row => [row.verbatim, row.marks])).toEqual([['8', 1], ['4', 1], ['0', 1], ['5', 1]]);
    expect(phone.rows.every(row => row.contextNote?.includes('1 mark for each correct number'))).toBe(true);
    expect(marksClaimed(phone, { 'r-1': 1, 'r-2': 1, 'r-3': 1, 'r-4': 1 })).toBe(4);
    const dislike = point('ld-5');
    expect(dislike.rows[0]).toMatchObject({ kind: 'criterion', marks: 4, permittedMarks: [0, 2, 4] });
    expect(dislike.rows[0].contextNote).toContain('teachers / strict 2 marks');
    expect(marksClaimed(dislike, { 'r-1': 2 })).toBe(2);
    expect(marksClaimed(dislike, { 'r-1': 3 })).toBe(0);
    expect(point('lb-3').rows[0].contextNote).toContain('without a subsidiary number');
    expect(point('lb-3').questionRef).toBe('2014 OL Section LB Q3');
  });

  it('keeps compound dishes as two components of one chosen dish', () => {
    const rubric = pool('lc-2-ii');
    expect(rubric.count).toBe(2);
    expect(rubric.groups.map(group => group.rows.map(row => row.marks))).toEqual([[2], [1, 1], [1, 1], [2]]);
    expect(rubric.groups[1].rows.map(row => row.text)).toEqual(['teriyaki', 'salmon']);
    expect(rubric.groups[2].rows.map(row => row.text)).toEqual(['toufu', 'salad']);
    expect(rubric.groups[3].rows[0].text).toBe('sashimi, raw fish');
    const partial = { 'language:group:dish-1': 1, 'language:row:dish-1:part-1': 1 };
    expect(languageMarks(languageCard('lc-2-ii'), partial)).toBe(1);
    expect(languageMarks(languageCard('lc-2-ii'), { ...partial, 'language:other-language:row:dish-1:part-1': 1 })).toBe(0.5);
    const full: LanguageScores = {};
    for (const group of rubric.groups) {
      full[`language:group:${group.id}`] = 1;
      for (const row of group.rows) full[`language:row:${group.id}:${row.id}`] = 1;
    }
    expect(languagePointsMarks(rubric, full)).toBe(4);
  });

  it('keeps all writing bands, local component guidance and independent expression caps', () => {
    const rubric = pool('5');
    expect(rubric.count).toBe(5);
    expect(rubric.groups).toHaveLength(7);
    for (const group of rubric.groups) {
      const [content, expression] = group.criteria!;
      expect(content.bands?.map(band => band.marks)).toEqual([[1], [2], [3, 4], [5]]);
      expect(expression.bands?.map(band => band.marks)).toEqual([[1], [2, 3], [4, 5]]);
      expect(content.permittedMarks).toEqual([0, 1, 2, 3, 4, 5]);
      const scores = { [`language:group:${group.id}`]: 1, [`language:${content.id}`]: 3, [`language:${expression.id}`]: 5 };
      expect(languagePointsMarks(rubric, scores)).toBe(6);
      expect(languagePointsMarks(rubric, { ...scores, [`language:${content.id}`]: 4 })).toBe(9);
    }
    for (const group of rubric.groups.slice(3, 5)) {
      expect(group.criteria![0].guidance.join(' ')).toContain('(3 marks)');
      expect(group.criteria![0].guidance.join(' ')).toContain('(2 marks)');
      for (const partial of [1, 2, 3, 4]) expect(languagePointsMarks(rubric, {
        [`language:group:${group.id}`]: 1, [`language:${group.criteria![0].id}`]: partial,
      })).toBe(partial);
    }
    expect(languagePointsMarks(rubric, { 'language:group:item-1': 1, 'language:item-1-content': 3, 'language:item-1-expression': 5,
      'language:group:item-2': 1, 'language:item-2-content': 4, 'language:item-2-expression': 5 })).toBe(15);
  });

  it('binds all 23 reading and 27 listening language conditions and no writing penalty', () => {
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(50);
    expect(cards.filter(card => card.audioMaterial)).toHaveLength(27);
    for (const found of cards.filter(card => card.answerLanguageRule)) {
      const rule = found.answerLanguageRule!;
      expect(rule.otherLanguageMultiplier).toBe(0.5);
      expect(rule.schemePages).toEqual([found.audioMaterial ? 3 : 5]);
      expect(rule.penalizedLanguage).toBe(found.audioMaterial ? 'Japanese' : undefined);
      expect(review.selectors.some(selector => selector.document === 'scheme' && selector.page === rule.schemePages[0] && selector.text === rule.sourceText)).toBe(true);
    }
    expect(cards.some(card => card.extraneousMaterialRule)).toBe(false);
    for (const suffix of ['4', '5']) expect(card(suffix).answerLanguageRule).toBeUndefined();
  });

  it('retains all 30 Atlas anchors and source-bound glyph proof without requiring local PDFs in unit tests', () => {
    const proof = readFileSync(resolve(__dirname, '..', review.glyphRecovery.path));
    expect(createHash('sha256').update(proof).digest('hex')).toBe(review.glyphRecovery.sha256);
    expect(JSON.parse(proof.toString()).sha256).toBe(census.sources.find(source => source.component === 'scheme')!.sha256);
    expect(JSON.stringify([cards, review.selectors])).not.toContain('�');
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(9);
    const tags = JSON.parse(readFileSync(resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'), 'utf8'));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      expect(task.paperPages, runtime.id).toContain(group.pP);
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2014 && paper.fileid === task.atlas.fileid);
      const topic = tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber);
      expect([topic.primary, topic.secondary], runtime.id).toContain(runtime.topicId);
      expect(sidecar.band).toEqual([1, 16]);
    }
    expect(map('LC058GLP000EV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 16 }, (_, i) => String(i + 1)));
    expect(map('LC058GLPA00EV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 14 }, (_, i) => String(i + 1)));
  });
});
