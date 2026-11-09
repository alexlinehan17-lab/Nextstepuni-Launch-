import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import reviewed from '../components/MarkBank/cards/japanese/reviewed.json';
import aliases from '../components/MarkBank/cards/japanese/aliases.json';
import census from '../scripts/markbank/authoring/reviews/japanese-2016-ol-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2016-ol.json';
import { languagePointsMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
import { tariffReconciles, UNPRINTED_ANSWER } from '../types/markBank';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = ordinary.filter(card => card.year === 2016);
const idFor = (key: (string | number | null)[]) => `ja-2016-ol-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2016-ol-${suffix}`)!;
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
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2016/${fileid}.json`), 'utf8'));

describe('Japanese 2016 Ordinary independent source review', () => {
  it('covers all 52 independent tasks and all 40 original physical pages', () => {
    expect(cards).toHaveLength(52);
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
      '9377b217ba808b6320baa90d17f5fa0a1a33c65cb520f363a4cdef944067e4b7',
      'acacbc404fed69359b1e90797d1263307fc7a2cbbd0c6ea0124c9e6e98d163e1',
      'd9cf9b92a4cebec8e58be494bd8388efddd680651e1271d1a08bfe42dadea3c5',
    ]);
    for (const source of review.sources) expect(source.pagesReviewed).toEqual(Object.keys(census.pageRoles[source.document as keyof typeof census.pageRoles]).map(Number));
  });

  it('adds 52 independently reviewed cards without inventing original aliases', () => {
    const original = readFileSync(resolve(__dirname, '../components/MarkBank/cards/japanese/ordinary.ts'), 'utf8');
    expect(createHash('sha256').update(original).digest('hex')).toBe('83a3b57745ae80882d11a3346ab34cefba7b70d801701b87202493e0650983ef');
    const originalIds = [...original.matchAll(/^ {4}id: "([^"]+)"/gm)].map(match => match[1]);
    expect(originalIds).toHaveLength(261);
    expect(originalIds.some(id => id.startsWith('ja-2016-'))).toBe(false);
    expect(cards.every(card => !originalIds.includes(card.id))).toBe(true);
    expect(review.consolidations).toEqual([]);
    expect(Object.keys(aliases)).toHaveLength(391);
    expect(Object.keys(aliases).filter(id => id.startsWith('ja-2016-'))).toEqual([]);
  });

  it('keeps all required pools, grammar context, exact source spelling and cloze words', () => {
    for (const [suffix, quota, total] of [['2a-4', 5, 15], ['2b-1', 5, 10], ['2b-2', 5, 10], ['2c', 10, 10], ['4', 10, 30]] as const) {
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
    expect(points('2a-4').groups.map(group => group.rows.map(row => row.marks))).toEqual(Array(5).fill([1, 2]));
    expect(points('2a-4').groups.map(group => group.rows[0].text)).toEqual(['False', 'True', 'False', 'True', 'True']);
    expect(points('2c').groups.map(group => group.rows[0].text)).toEqual(['(a)', '(d)', '(c)', '(d)', '(b)', '(c)', '(a)', '(b)', '(d)', '(b)']);
    expect(points('2b-1').groups.map(group => group.rows[0].text)).toEqual(['たべます。', 'おもしいです。', 'しんせつです。', '買いました。', 'でした。']);
    expect(points('2b-1').markingGuideNote).toContain('visibly omitting ろ');
    expect(card('2b-1').questionText).toContain('フリーマーケットはおもしろくないです。');
    expect(card('2b-2').questionText).toContain('大好きです。');
    expect(card('2b-2').questionText).toContain('5 分です。');
    expect(points('2b-2').groups.map(group => group.rows[0].text)).toEqual(['(a) を', '(c) が', '(c) に', '(b)   は', '(a)  まで']);
    expect(points('4').groups.map(group => group.rows[0].text)).toEqual(['しゅみ', 'あります', '学校', '木曜日', '4 時', 'います', '父', 'なまえ', '好きな', 'よろしく']);
    expect(card('4').questionText.replace(/\s+/g, ' ')).toContain('A word should be used only once.');
  });

  it('retains complete required times/rooms/events/matching and the day-month split', () => {
    expect(point('1-1').rows.map(row => row.verbatim)).toEqual(['3:00', '11:30', '2:00', '11:30', '10:00']);
    expect(point('1-1').rows.map(row => row.marks)).toEqual(Array(5).fill(2));
    expect(point('1-2').rows.map(row => [row.verbatim, row.marks])).toEqual([['12th', 1], ['of July', 1]]);
    expect(point('1-3').rows.map(row => [row.verbatim, row.marks])).toEqual([['Hall 1', 2], ['Hall 2', 2]]);
    expect(point('1-5').rows.map(row => [row.verbatim, row.marks])).toEqual([['Ireland workshop', 2], ['Kids festival', 2], ['Christmas fair', 2]]);
    expect(point('2a-1').rows.map(row => row.verbatim)).toEqual(['Takeshita street', 'Yoyogi Park', 'Harajuku']);
    expect(point('2a-1').rows.map(row => row.marks)).toEqual([3, 3, 3]);
  });

  it('retains each finite choice and the unprinted culture point plus discretionary mark', () => {
    for (const [suffix, quota, available, marks] of [['1-4', 2, 3, 2], ['1-6', 2, 3, 2], ['2a-2', 1, 2, 3], ['2a-3-i', 1, 4, 2], ['2a-3-ii', 1, 4, 2], ['3a-2-i', 2, 4, 2], ['3a-2-ii', 1, 2, 2]] as const) {
      const found = point(suffix);
      expect(found.rows[0].group).toMatchObject({ claimMax: quota, perOption: marks });
      expect(found.rows[0].group?.options).toHaveLength(available);
      expect(marksClaimed(found, {}, { 'r-1': Array.from({ length: available }, (_, i) => i) })).toBe(quota * marks);
    }
    const culture = point('3b');
    expect(culture.rows).toHaveLength(1);
    expect(culture.rows[0]).toMatchObject({ verbatim: UNPRINTED_ANSWER, unprinted: true, marks: 3, permittedMarks: [0, 1, 2, 3] });
    expect(culture.rows[0].parts).toEqual([
      { id: 'point', verbatim: '2 mark for any point', marks: 2, permittedMarks: [0, 2] },
      { id: 'discretionary', verbatim: '1 discretionary mark', marks: 1, permittedMarks: [0, 1] },
    ]);
    expect(marksClaimed(culture, { 'r-1:point': 2, 'r-1:discretionary': 1 })).toBe(3);
    expect(marksClaimed(culture, { 'r-1:point': 0, 'r-1:discretionary': 1 })).toBe(1);
    expect(marksClaimed(culture, { 'r-1:point': 2, 'r-1:discretionary': 0 })).toBe(2);
    expect(point('3a-4-iii').questionRef).toBe('2016 OL Section 3A Q4(iii)');
    expect(point('3a-4-iii').questionText).toBe('先生はどんな人ですか。');
    expect(point('3a-4-iii').rows[0].contextNote).toContain('scheme repeats (ii)');
  });

  it('prices four missing phone digits, car components and whole weather responses accurately', () => {
    const phone = point('lc-1-iii');
    expect(phone.rows.map(row => [row.verbatim, row.marks])).toEqual([['5', 1], ['6', 1], ['4', 1], ['1', 1]]);
    expect(phone.rows.every(row => row.contextNote?.includes('0570–064–110'))).toBe(true);
    expect(phone.questionRef).toBe('2016 OL Section LC Q1(iii)');
    expect(marksClaimed(phone, Object.fromEntries(phone.rows.map(row => [row.id, 1])))).toBe(4);
    const car = point('la-1-i');
    expect(car.rows[0]).toMatchObject({ verbatim: 'Car', marks: 1 });
    expect(car.rows[1].group).toMatchObject({ options: ['Toyota', 'new', 'red', 'sports'], perOption: 1, claimMax: 1 });
    expect(marksClaimed(car, { 'r-1': 1 }, { 'r-2': [0, 1, 2, 3] })).toBe(2);
    expect(point('la-2-i').rows[0].group).toMatchObject({ options: ['Asia', 'Vietnam'], claimMax: 1, perOption: 2 });
    for (const suffix of ['lc-3-i', 'lc-3-ii']) {
      const weather = point(suffix);
      expect(weather.rows[0].group).toMatchObject({ claimMax: 1, perOption: 4 });
      expect(marksClaimed(weather, {}, { 'r-1': [0, 1, 2, 3] })).toBe(4);
      expect(weather.rows[0].contextNote).toContain('no separate per-detail allocation');
    }
    expect(point('lc-3-i').rows[0].group?.options).toEqual(['Sunny', 'nice', 'Clear skies', '28 degrees']);
    expect(point('lc-3-ii').rows[0].group?.options).toEqual(['rain', '32 degrees', 'humid']);
  });

  it('keeps all seven summer-holiday prompts and independent five-response expression caps', () => {
    const rubric = points('5');
    expect(rubric.count).toBe(5);
    expect(rubric.groups).toHaveLength(7);
    expect(rubric.groups[6].label).toContain('何をしますか。');
    expect(rubric.groups[0].criteria?.[1].bands?.[0].guidance.join(' ')).toContain('Vocabulary very inadequate');
    expect(rubric.groups[0].criteria?.[1].bands?.[2].guidance.join(' ')).toContain('Good use of Genkouyoushi');
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

  it('binds exactly24 reading and26 listening conditions to the original source selectors', () => {
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(50);
    expect(cards.filter(card => card.answerLanguageRule?.penalizedLanguage === 'Japanese')).toHaveLength(26);
    for (const found of cards.filter(card => card.answerLanguageRule)) {
      const rule = found.answerLanguageRule!;
      expect(review.selectors.some(selector => selector.document === 'scheme' && selector.text === rule.sourceText && rule.schemePages.includes(selector.page))).toBe(true);
      expect(rule.otherLanguageMultiplier).toBe(0.5);
      expect(rule.sourceText).toBe(found.audioMaterial ? '(Half marks if answered in romaji or Japanese script)' : '(Half marks if not answered in the appropriate language)');
    }
    expect(cards.some(card => card.extraneousMaterialRule)).toBe(false);
    expect(card('4').answerLanguageRule).toBeUndefined();
    expect(card('5').answerLanguageRule).toBeUndefined();
  });

  it('retains all19 written and14 aural Atlas anchors and eight full source crops', () => {
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(8);
    const tags = JSON.parse(readFileSync(resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'), 'utf8'));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      expect(task.paperPages, runtime.id).toContain(group.pP);
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2016 && paper.fileid === task.atlas.fileid);
      expect(tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber).primary, runtime.id).toBe(runtime.topicId);
      expect(sidecar.band).toEqual([1, 16]);
    }
    expect(map('LC058GLP000EV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 19 }, (_, i) => String(i + 1)));
    expect(map('LC058GLPA00EV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 14 }, (_, i) => String(i + 1)));
  });
});
