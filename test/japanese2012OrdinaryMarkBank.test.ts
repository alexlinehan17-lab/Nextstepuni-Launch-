import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import rawCards from '../components/MarkBank/cards/japanese/reviewed.json';
import census from '../scripts/markbank/authoring/reviews/japanese-2012-ol-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2012-ol.json';
import { tariffReconciles, UNPRINTED_ANSWER } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
import { languageMarks, languagePointsMarks, languageWritingMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = ordinary.filter(card => card.year === 2012);
const idFor = (key: (string | number | null)[]) => `ja-2012-ol-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2012-ol-${suffix}`)!;
const point = (suffix: string) => {
  const found = card(suffix);
  if (found.kind !== 'question') throw new Error(`Expected point card ${suffix}`);
  return found;
};
const pool = () => {
  const found = card('5');
  if (found.kind !== 'rubric' || found.rubric.system !== 'language-points') throw new Error('Expected writing pool');
  return found.rubric;
};
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2012/${fileid}.json`), 'utf8'));

describe('Japanese 2012 Ordinary independent original-source review', () => {
  it('covers all 59 independent tasks and all 32 physical original pages', () => {
    expect(cards).toHaveLength(59);
    expect(cards.map(card => card.id).sort()).toEqual(census.tasks.map(task => idFor(task.key)).sort());
    for (const task of census.tasks) {
      const found = cards.find(card => card.id === idFor(task.key))!;
      expect(found.totalMarks, found.id).toBe(task.marks);
      expect(tariffReconciles(found), found.id).toBe(true);
      expect(rawCards.find(card => card.id === found.id)!.sourceEvidence).toMatchObject({ component: task.component, paperPages: task.paperPages, schemePages: task.schemePages });
    }
    expect(census.checksums).toEqual({ reading: 120, writing: 80, listening: 100, total: 300 });
    expect(Object.values(census.pageRoles).map(pages => Object.keys(pages).length)).toEqual([12, 8, 12]);
    expect(review.sources.map(source => ({ component: source.document, path: source.path, sha256: source.sha256 }))).toEqual(census.sources);
    for (const source of review.sources) expect(source.pagesReviewed).toEqual(Object.keys(census.pageRoles[source.document as keyof typeof census.pageRoles]).map(Number));
    expect(review.consolidations).toEqual([]);
    expect(JSON.stringify([cards, review.selectors])).not.toContain('�');
  });

  it('keeps complete required tables, paired decisions/evidence, kanji and grammar tasks', () => {
    for (const [suffix, count] of [['1-1', 8], ['2a', 9], ['2b', 16], ['3b', 10], ['3c-1', 5], ['3c-2', 5], ['4', 10]] as const) {
      expect(point(suffix).rows, suffix).toHaveLength(count);
      expect(marksClaimed(point(suffix), Object.fromEntries(point(suffix).rows.map(row => [row.id, 'yes']))), suffix).toBe(point(suffix).totalMarks);
    }
    expect(point('2a').taskGroups?.map(group => group.marks)).toEqual([2, 3, 2, 2]);
    expect(point('2a').stem).toContain('Tanaka, Ginza and Labrador are already supplied');
    expect(point('2b').taskGroups?.map(group => group.marks)).toEqual(Array(8).fill(2));
    expect(point('3a-2').rows[0].group).toMatchObject({ claimMax: 2, perOption: 2, options: ['America', 'England', 'China'] });
    expect(point('4').rows[2].contextNote).toContain('町');
    expect(point('4').rows[2].contextNote).toContain('まち');
    expect(point('4').rows.every(row => row.kind === 'point')).toBe(true);
    expect(review.sourceAnswerBindings).toEqual([]);
  });

  it('preserves the literal cake1/drink3 whole-response scale without adding an unprinted 2 or 4', () => {
    const found = point('1-5');
    expect(found.totalMarks).toBe(3);
    expect(found.rows).toHaveLength(1);
    expect(found.rows[0]).toMatchObject({ kind: 'criterion', verbatim: 'Cake & Drink', marks: 3, permittedMarks: [0, 1, 3] });
    expect(found.rows[0].contextNote).toContain('(cake, 1 mark; drink 3 marks)');
    for (const allowed of [0, 1, 3]) expect(marksClaimed(found, { 'r-1': allowed })).toBe(allowed);
    expect(marksClaimed(found, { 'r-1': 2 })).toBe(0);
    expect(marksClaimed(found, { 'r-1': 4 })).toBe(0);
  });

  it('preserves all listening alternatives, exact partials and six phone blanks', () => {
    expect(point('lb-1-ii').rows[0].group).toMatchObject({ claimMax: 1, perOption: 3 });
    expect(point('lb-1-ii').rows[0].group?.options).toHaveLength(4);
    expect(marksClaimed(point('lb-1-ii'), {}, { 'r-1': [0, 1, 2, 3] })).toBe(3);
    expect(point('lc-2-ii').rows[0].verbatim).toContain('age from 20/ to 26 years old/');
    expect(point('lc-2-ii').rows[0].verbatim).toContain('Have a working holiday visa');
    expect(point('lc-2-ii').rows).toHaveLength(1);
    const phone = point('lc-2-iii');
    expect(phone.rows.map(row => row.verbatim)).toEqual(['8', '3', '5', '3', '9', '6']);
    expect(phone.rows.every(row => row.marks === 1)).toBe(true);
    expect(phone.rows[0].contextNote).toContain('03-8353-4969');
    expect(phone.rows[0].contextNote).toContain('printed 03, 4 and final 9 are given');
    expect(marksClaimed(phone, Object.fromEntries(phone.rows.map(row => [row.id, 'yes'])))).toBe(6);
    for (const [suffix, allowed, literal] of [
      ['ld-1-ii', [0, 2, 4], 'People are nice, 2 marks'],
      ['ld-1-iii', [0, 1, 4], 'Internet, 1 mark'],
      ['ld-2-ii', [0, 1, 4], 'Tokyo, 1 mark'],
    ] as const) {
      const found = point(suffix);
      expect(found.rows).toHaveLength(1);
      expect(found.rows[0].permittedMarks).toEqual(allowed);
      expect(found.rows[0].verbatim).toContain(literal);
      for (const score of allowed) expect(marksClaimed(found, { 'r-1': score })).toBe(score);
      expect(marksClaimed(found, { 'r-1': 3 })).toBe(0);
    }
  });

  it('retains the unprinted culture answer with its exact two comparisons and discretionary credit', () => {
    const found = card('3d');
    if (found.kind !== 'rubric' || found.rubric.system !== 'language-writing') throw new Error('Expected culture rubric');
    expect(found.rubric.markingGuideNote).toContain(UNPRINTED_ANSWER);
    expect(found.rubric.criteria.map(criterion => criterion.permittedMarks)).toEqual([[0, 2], [0, 2], [0, 1, 2]]);
    expect(languageWritingMarks(found.rubric, { 'language:point-1': 2, 'language:point-2': 2, 'language:discretionary': 2 })).toBe(6);
    expect(languageWritingMarks(found.rubric, { 'language:point-1': 1 })).toBe(0);
    expect(languageMarks(found, { 'language:point-1': 2, 'language:other-language:response': 1 })).toBe(1);
  });

  it('keeps all seven paper prompts under the common any-five bands and does not invent an expression cap', () => {
    const rubric = pool();
    expect(rubric.count).toBe(5);
    expect(rubric.groups).toHaveLength(7);
    expect(rubric.groups[4].label.replace(/\s+/g, '')).toContain('先生');
    expect(rubric.markingGuideNote).toContain('omitting that prompt');
    expect(rubric.markingGuideNote).toContain('No lower-expression cap is printed');
    const full: LanguageScores = {};
    for (const group of rubric.groups) {
      const [content, expression] = group.criteria!;
      expect(content.bands?.map(band => band.marks)).toEqual([[1], [2, 3], [4], [5]]);
      expect(expression.bands?.map(band => band.marks)).toEqual([[1], [2, 3], [4, 5]]);
      expect(expression.limits).toBeUndefined();
      expect(languagePointsMarks(rubric, { [`language:group:${group.id}`]: 1, [`language:${content.id}`]: 1, [`language:${expression.id}`]: 5 })).toBe(6);
      full[`language:group:${group.id}`] = 1;
      full[`language:${content.id}`] = full[`language:${expression.id}`] = 5;
    }
    expect(languagePointsMarks(rubric, full)).toBe(50);
  });

  it('binds only the printed reading/listening language conditions and retains all original Atlas identities', () => {
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(57);
    for (const found of cards.filter(card => card.answerLanguageRule)) {
      const rule = found.answerLanguageRule!;
      expect(rule.otherLanguageMultiplier).toBe(0.5);
      expect(rule.schemePages).toEqual([found.audioMaterial ? 3 : 5]);
      expect(rule.penalizedLanguage).toBe(found.audioMaterial ? 'Japanese' : undefined);
      expect(review.selectors.some(selector => selector.document === 'scheme' && selector.page === rule.schemePages[0] && selector.text === rule.sourceText)).toBe(true);
    }
    expect(cards.some(card => card.extraneousMaterialRule)).toBe(false);
    for (const suffix of ['4', '5']) expect(card(suffix).answerLanguageRule).toBeUndefined();
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(10);
    const tags = JSON.parse(readFileSync(resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'), 'utf8'));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      expect(task.paperPages).toContain(group.pP);
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2012 && paper.fileid === task.atlas.fileid);
      const topic = tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber);
      expect([topic.primary, topic.secondary], runtime.id).toContain(runtime.topicId);
      expect(sidecar.band).toEqual([1, 12]);
    }
    expect(map('LC058GLP000EV.pdf').q).toHaveLength(19);
    expect(map('LC058GLPA00EV.pdf').q).toHaveLength(4);
    expect(map('LC058GLPA00EV.pdf').q[3].region).toEqual([{ p: 4, r: [0, .5691, 1, 1] }, { p: 5, r: [0, .04, 1, .238] }]);
    expect(card('2a').topicId).toBe('japanese-5-0');
    expect(card('3a-1-i').topicId).toBe('japanese-5-2');
  });
});
