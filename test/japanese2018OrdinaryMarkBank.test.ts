import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import reviewed from '../components/MarkBank/cards/japanese/reviewed.json';
import aliases from '../components/MarkBank/cards/japanese/aliases.json';
import census from '../scripts/markbank/authoring/reviews/japanese-2018-ol-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2018-ol.json';
import { languagePointsMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
import { tariffReconciles, UNPRINTED_ANSWER } from '../types/markBank';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = ordinary.filter(card => card.year === 2018);
const idFor = (key: (string | number | null)[]) => `ja-2018-ol-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2018-ol-${suffix}`)!;
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
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2018/${fileid}.json`), 'utf8'));

describe('Japanese 2018 Ordinary independent source review', () => {
  it('covers all 57 independent tasks and all 40 original physical pages', () => {
    expect(cards).toHaveLength(57);
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
      'd4350996bef8795c53d2fb0f1e68f763a27bcdb6a4980e30a4ce83127208cef0',
      '6f7464db7f617ae9c35aea8f4891b4ec0d7518c2ab5d9e893910b2b4d86c455b',
      '8140e430a7c93568637fba566e37a27e6928a56eddb2272264b0d93fe195f8a5',
    ]);
    for (const source of review.sources) expect(source.pagesReviewed).toEqual(Object.keys(census.pageRoles[source.document as keyof typeof census.pageRoles]).map(Number));
  });

  it('adds 57 independently reviewed cards without inventing original aliases', () => {
    const original = readFileSync(resolve(__dirname, '../components/MarkBank/cards/japanese/ordinary.ts'), 'utf8');
    expect(createHash('sha256').update(original).digest('hex')).toBe('83a3b57745ae80882d11a3346ab34cefba7b70d801701b87202493e0650983ef');
    const originalIds = [...original.matchAll(/^ {4}id: "([^"]+)"/gm)].map(match => match[1]);
    expect(originalIds).toHaveLength(261);
    expect(originalIds.some(id => id.startsWith('ja-2018-'))).toBe(false);
    expect(cards.every(card => !originalIds.includes(card.id))).toBe(true);
    expect(review.consolidations).toEqual([]);
    expect(Object.keys(aliases)).toHaveLength(391);
    expect(Object.keys(aliases).filter(id => id.startsWith('ja-2018-'))).toEqual([]);
  });

  it('retains every required pool and its source answers', () => {
    for (const [suffix, quota, total] of [['2a-1', 3, 3], ['2b', 5, 15], ['2c', 10, 10], ['3c-1', 5, 10], ['3c-2', 5, 10], ['4', 10, 30]] as const) {
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
    expect(points('2a-1').groups.map(group => group.rows[0].text)).toEqual(['Yukio', 'Hiroshi', 'Michiko']);
    expect(points('2b').groups.map(group => group.rows.map(row => row.marks))).toEqual(Array(5).fill([1, 2]));
    expect(points('2b').groups.map(group => group.rows[0].text)).toEqual(['False', 'True', 'False', 'True', 'False']);
    expect(points('2b').groups[2].rows[1].text).toBe('福岡のコンサート。');
    expect(points('2c').groups.map(group => group.rows[0].text)).toEqual(['b', 'a', 'c', 'd', 'd', 'b', 'c', 'a', 'b', 'a']);
    expect(points('3c-1').groups.map(group => group.rows[0].text)).toEqual(['ありました。', 'でした。', 'おいしかったです。', '買いました。', 'じゃありませんでした。']);
    expect(points('3c-2').groups.map(group => group.rows[0].text)).toEqual(['b. は', 'c. と', 'a. まで', 'a. が', 'b. に']);
    expect(points('4').groups.map(group => group.rows[0].text)).toEqual(['かんじ', 'とても', '好き', '6 時', 'ともだち', '日本語', '一人で', 'バスケット', '行きます', '食べます']);
    expect(card('4').questionText.replace(/\s+/g, ' ')).toContain('A word should be used only once.');
  });

  it('keeps complete tables, fixed components and the printed descending choice tariff', () => {
    expect(point('1-1').rows.map(row => row.verbatim)).toEqual(['8', '6', '4', '9', '3', '10']);
    expect(point('1-1').rows.map(row => row.marks)).toEqual(Array(6).fill(2));
    expect(point('1-3').rows.map(row => row.verbatim)).toEqual(['31st', 'July', 'Tuesday', '25th', 'August', 'Saturday']);
    expect(point('1-3').rows.map(row => row.marks)).toEqual([1, 1, 2, 1, 1, 2]);
    expect(point('1-3').taskGroups?.map(group => group.marks)).toEqual([4, 4]);
    expect(point('1-4').rows.map(row => [row.verbatim, row.marks])).toEqual([['Night', 1], ['film festival', 1]]);
    for (const suffix of ['1-5', '1-6']) expect(point(suffix).rows[0].group).toMatchObject({ claimMax: 3, perOption: 2, options: expect.any(Array) });
    expect(point('1-6').rows[0].group?.options).toHaveLength(7);
    expect(point('1-6').rows[0].group?.options).toContain('Kimono, yukata');
    expect(point('2a-4').rows[0].group).toMatchObject({ claimMax: 2, perOptionSteps: [2, 1], options: ['Su', 'Yui', 'Moa'] });
    expect(marksClaimed(point('2a-4'), {}, { 'r-1': [0] })).toBe(2);
    expect(marksClaimed(point('2a-4'), {}, { 'r-1': [0, 1] })).toBe(3);
    expect(marksClaimed(point('2a-4'), {}, { 'r-1': [0, 1, 2] })).toBe(3);
    expect(point('2d').rows[0]).toMatchObject({ verbatim: UNPRINTED_ANSWER, unprinted: true, marks: 4, permittedMarks: [0, 2, 4] });
    expect(point('2d').rows[0].parts?.map(part => part.marks)).toEqual([2, 2]);
    expect(point('3a-3-i').rows[0].verbatim).toBe('Japanese');
    expect(point('3a-3-ii').rows[0].verbatim).toBe('Irish');
  });

  it('prices the four missing phone digits, iPhone components and wind-only partial exactly', () => {
    const phone = point('lb-1-iii');
    expect(phone.rows.map(row => [row.verbatim, row.marks])).toEqual([['5', 1], ['7', 1], ['8', 1], ['2', 1]]);
    expect(phone.rows.every(row => row.contextNote?.includes('03-3573-8205'))).toBe(true);
    expect(phone.questionRef).toBe('2018 OL Section LB Q1(iii)');
    expect(point('la-1-i').rows.map(row => [row.verbatim, row.marks])).toEqual([['iPhone', 1], ['8', 1]]);
    const wind = point('lb-3-i');
    expect(wind.rows[0]).toMatchObject({ kind: 'criterion', marks: 4, permittedMarks: [0, 2, 4], contextNote: 'A typhoon (wind 2 marks)' });
    expect(marksClaimed(wind, { 'r-1': 2 })).toBe(2);
    expect(marksClaimed(wind, { 'r-1': 4 })).toBe(4);
    expect(marksClaimed(wind, { 'r-1': 1 })).toBe(0);
    expect(point('lb-2-iii').rows[0].group).toMatchObject({ claimMax: 1, perOption: 2, options: ['traditional', 'rock', 'classical', 'jazz'] });
  });

  it('keeps seven paper writing prompts, first-response components and independent expression limits', () => {
    const rubric = points('5');
    expect(rubric.count).toBe(5);
    expect(rubric.groups).toHaveLength(7);
    expect(rubric.groups[0].criteria?.map(criterion => criterion.maxMarks)).toEqual([2, 2, 1, 5]);
    expect(rubric.groups[0].criteria?.map(criterion => criterion.permittedMarks)).toEqual([[0, 2], [0, 2], [0, 1], [0, 1, 2, 3, 4, 5]]);
    for (const group of rubric.groups.slice(1)) expect(group.criteria?.map(criterion => criterion.maxMarks)).toEqual([5, 5]);
    expect(rubric.groups[2].label).toContain('何をしますか');
    expect(rubric.groups[3].label).toContain('何が好きですか');
    expect(rubric.markingGuideNote).toContain('repeats age at(iv)');
    expect(rubric.markingGuideNote).toContain('not an extra or replacement question');
    const scores: LanguageScores = {};
    for (const group of rubric.groups) {
      scores[`language:group:${group.id}`] = 1;
      for (const criterion of group.criteria!) scores[`language:${criterion.id}`] = criterion.maxMarks;
    }
    expect(languagePointsMarks(rubric, scores)).toBe(50);
    scores['language:item-1-age'] = 0;
    expect(languagePointsMarks(rubric, scores)).toBe(46); // C3/E3, other four remain C5/E5.
    scores['language:item-1-age'] = 2;
    scores['language:item-1-discretionary'] = 0;
    expect(languagePointsMarks(rubric, scores)).toBe(49); // C4 restores E5.
    scores['language:item-2-content'] = 3;
    expect(languagePointsMarks(rubric, scores)).toBe(45);
    scores['language:item-2-content'] = 4;
    expect(languagePointsMarks(rubric, scores)).toBe(48);
    scores['language:item-6-content'] = 0;
    expect(languagePointsMarks(rubric, scores)).toBe(48); // Sixth response is outside the five chosen quota.
    scores['language:group:item-1'] = 0;
    expect(languagePointsMarks(rubric, scores)).toBe(42); // Sixth now contributes C0/E3, no effect on other groups.
    expect(rubric.groups[1].criteria?.[1].bands?.map(band => band.marks)).toEqual([[1], [2, 3], [4, 5]]);
  });

  it('binds exactly 26 reading and 29 listening language conditions to original source selectors', () => {
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(55);
    expect(cards.filter(card => card.answerLanguageRule?.penalizedLanguage === 'Japanese')).toHaveLength(29);
    for (const found of cards) {
      expect(found.extraneousMaterialRule).toBeUndefined();
      if (['4', 'Q5'].includes(found.section!)) { expect(found.answerLanguageRule).toBeUndefined(); continue; }
      const page = found.audioMaterial ? 3 : 5;
      const source = review.selectors.find(selector => selector.document === 'scheme' && selector.page === page && selector.row === 1)!;
      expect(found.answerLanguageRule).toEqual({ otherLanguageMultiplier: 0.5, sourceText: source.text, schemePages: [page], ...(found.audioMaterial ? { penalizedLanguage: 'Japanese' } : {}) });
    }
  });

  it('retains all multiple-choice options, source instructions and eight source crops', () => {
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(8);
    for (const suffix of ['la-1-ii', 'la-1-iii', 'la-2-ii', 'la-2-iii', 'la-3-ii', 'lb-1-ii', 'lb-2-ii', 'lb-3-ii', 'lc-1-ii', 'lc-1-iii', 'lc-1-iv', 'lc-2-i', 'lc-2-ii', 'ld-1-i', 'ld-1-iii', 'ld-2-ii', 'ld-2-iii']) {
      for (const label of ['a', 'b', 'c', 'd']) expect(card(suffix).questionText, suffix).toContain(`(${label})`);
    }
    for (const roman of ['i', 'ii', 'iii']) for (const label of ['a', 'b', 'c', 'd']) expect(card(`3a-4-${roman}`).questionText).toContain(`${label}.`);
    expect(card('lb-1-i').stem?.replace(/\s+/g, ' ')).toContain('item will be played three times: first right through, then in segments with pauses, and finally right through again.');
  });

  it('retains all eight written and four listening Atlas identities and source regions', () => {
    const tags = JSON.parse(readFileSync(resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'), 'utf8'));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      expect([...task.paperPages, ...(runtime.sourceMaterial?.pages ?? [])], runtime.id).toContain(group.pP);
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2018 && paper.fileid === task.atlas.fileid);
      expect(tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber).primary, runtime.id).toBe(runtime.topicId);
      expect(sidecar.band).toEqual([1, 16]);
    }
    expect(map('LC058GLP000EV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 8 }, (_, i) => String(i + 1)));
    expect(map('LC058GLPA00EV.pdf').q.map(question => question.n)).toEqual(['1', '2', '3', '4']);
  });
});
