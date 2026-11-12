import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as higher } from '../components/MarkBank/cards/japanese/higher';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import reviewed from '../components/MarkBank/cards/japanese/reviewed.json';
import census from '../scripts/markbank/authoring/reviews/japanese-2026-hl-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2026-hl.json';
import aliases from '../components/MarkBank/cards/japanese/aliases.json';
import figures from '../components/MarkBank/figures-japanese.json';
import { languageCriterionValue, languagePointsMarks, languageWritingMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import { tariffReconciles, type LanguageWritingRubric, type LanguagePointsRubric } from '../types/markBank';
import type { PaperAnswerMap } from '../types/paperTrail';

const idFor = (key: (string | number | null)[]) => `ja-2026-hl-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const cards = higher.filter(card => card.year === 2026);
const rawById = new Map(reviewed.map(card => [card.id, card]));
const writing = (id: string) => {
  const card = cards.find(card => card.id === `ja-2026-hl-${id}`)!;
  if (card.kind !== 'rubric' || card.rubric.system !== 'language-writing') throw new Error('Expected writing rubric');
  return card.rubric as LanguageWritingRubric;
};
const points = (id: string) => {
  const card = cards.find(card => card.id === `ja-2026-hl-${id}`)!;
  if (card.kind !== 'rubric' || card.rubric.system !== 'language-points') throw new Error('Expected grouped points');
  return card.rubric as LanguagePointsRubric;
};
const readMap = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2026/${fileid}.json`), 'utf8'));

describe('Japanese 2026 Higher source review', () => {
  it('covers the independently inventoried 71 tasks and all 300 printed marks', () => {
    expect(cards).toHaveLength(71);
    expect(cards.map(card => card.id).sort()).toEqual(census.tasks.map(task => idFor(task.key)).sort());
    for (const task of census.tasks) {
      const card = cards.find(card => card.id === idFor(task.key))!;
      expect(card.totalMarks, card.id).toBe(task.marks);
      expect(tariffReconciles(card), card.id).toBe(true);
      const evidence = rawById.get(card.id)!.sourceEvidence;
      expect(evidence.component).toBe(task.component);
      expect(evidence.paperPages.every(page => task.paperPages.includes(page)), card.id).toBe(true);
      expect(evidence.schemePages.every(page => task.schemePages.includes(page)), card.id).toBe(true);
    }
    const total = (selected: typeof cards) => selected.reduce((sum, card) => sum + card.totalMarks, 0);
    expect(total(cards.filter(card => !card.audioMaterial && !['4', 'Q5'].includes(card.section!)))).toBe(120);
    expect(total(cards.filter(card => ['4', 'Q5'].includes(card.section!)))).toBe(100);
    expect(total(cards.filter(card => card.audioMaterial))).toBe(80);
    expect(total(cards)).toBe(300);
    expect(Object.values(census.pageRoles).map(pages => Object.keys(pages).length)).toEqual([20, 8, 24]);
  });

  it('retains all 600 previously served cards while adding the reviewed sitting', () => {
    const originalIds = ['higher', 'ordinary'].flatMap(level => [...readFileSync(resolve(__dirname, `../components/MarkBank/cards/japanese/${level}.ts`), 'utf8').matchAll(/^ {4}id: "([^"]+)"/gm)].map(match => match[1]));
    const live = new Set([...higher, ...ordinary].map(card => card.id));
    const aliasMap: Record<string, string> = aliases;
    expect(originalIds).toHaveLength(600);
    for (const id of originalIds) expect(live.has(id) || live.has(aliasMap[id]), id).toBe(true);
    const newIds = reviewed.filter(card => !originalIds.includes(card.id));
    expect(newIds).toHaveLength(1671); // +66 independently reviewed 2010 Higher tasks; frozen600/391 remain unchanged.
    expect(Object.keys(aliases)).toHaveLength(391);
    expect(live.size).toBe(600 + newIds.length - Object.keys(aliases).length);
    // Both were absent from the shipped literal baseline; the independently reviewed 2021 sitting now covers them.
    expect(originalIds.some(id => ['ja-2021-ol-2b-ii', 'ja-2021-ol-3a-4-iv'].includes(id))).toBe(false);
  });

  it('emits the verified half-credit convention only for this source-reviewed sitting', () => {
    const source = review.selectors.find(selector => selector.document === 'scheme' && selector.page === 3 && selector.row === 11 && selector.group === 1)!;
    const sourceText = source.text.normalize('NFKC');
    expect(sourceText).toBe('Where answers are in the language other than specified, award half marks.');
    for (const card of cards) {
      expect(card.answerLanguageRule, card.id).toEqual({ otherLanguageMultiplier: 0.5, sourceText, schemePages: [3] });
    }
    expect(higher.filter(card => !rawById.has(card.id)).some(card => card.answerLanguageRule)).toBe(false);
    expect(ordinary.filter(card => !rawById.has(card.id)).some(card => card.answerLanguageRule)).toBe(false);
  });

  it('retains full bilingual-line continuations, the translation and gift-table example', () => {
    expect(rawById.get('ja-2026-hl-1a-4-b')!.questionText).toBe('What should first-time buyers do before buying either ring?');
    expect(rawById.get('ja-2026-hl-2a-3')!.questionText).toContain('すばらしい思い出になります。');
    expect(rawById.get('ja-2026-hl-3a-1-c-iii')!.sourceMaterial?.pages).toEqual([10, 11]);
    expect(points('3a-1-c-iii').groups.map(group => group.rows.map(row => row.marks))).toEqual([[1, 1], [1, 1], [1, 1]]);
  });

  it('keeps every printed choice pool whole, with its original question artwork', () => {
    for (const id of ['2b-1', '2b-2', '2c-1', '2c-2']) {
      const card = cards.find(card => card.id === `ja-2026-hl-${id}`)!;
      expect(card.kind).toBe('question');
      if (card.kind !== 'question') continue;
      expect(card.rows[0].kind).toBe('anyN');
      if (card.rows[0].kind === 'anyN') expect(card.rows[0].group).toMatchObject({ claimMax: 5, perOption: 1 });
      expect(card.questionFigure).toBeDefined();
    }
    expect(points('3b')).toMatchObject({ count: 5 });
    expect(points('3b').groups).toHaveLength(6);
    expect(points('3c')).toMatchObject({ count: 10 });
    expect(points('3c').groups).toHaveLength(12);
    expect(writing('4').taskRequirements.join(' ')).toContain('1 OR 2 OR 3');
    expect(writing('5').criteria.filter(criterion => criterion.id.startsWith('heading-'))).toHaveLength(4);
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(8);
    for (const figure of Object.values(figures)) {
      expect(createHash('md5').update(readFileSync(resolve(__dirname, '../public', figure.src.slice(1)))).digest('hex')).toBe(figure.md5);
    }
  });

  it('scores reading and meaning separately without allowing a sixth kanji', () => {
    const rubric = points('3b');
    const scores: LanguageScores = {};
    for (const group of rubric.groups) {
      scores[`language:group:${group.id}`] = 1;
      scores[`language:row:${group.id}:reading`] = 1;
    }
    expect(languagePointsMarks(rubric, scores)).toBe(5);
    scores['language:row:item-1:meaning'] = 1;
    expect(languagePointsMarks(rubric, scores)).toBe(6);
    for (const group of rubric.groups) scores[`language:row:${group.id}:meaning`] = 1;
    expect(languagePointsMarks(rubric, scores)).toBe(10);
  });

  it('applies Q4 lower expression at C10 or 149 characters, but not C11 and 150', () => {
    const rubric = writing('4');
    const scores: LanguageScores = { 'language:opening': 1, 'language:part-a': 9, 'language:part-b': 0, 'language:closing': 0, 'language:expression': 20, 'language:length:characters': 200 };
    expect(languageWritingMarks(rubric, scores)).toBe(25);
    scores['language:part-b'] = 1;
    scores['language:length:characters'] = 149;
    expect(languageCriterionValue(rubric, 'expression', scores)).toBe(15);
    scores['language:length:characters'] = 150;
    expect(languageWritingMarks(rubric, scores)).toBe(31);
    // The prompt's 200-character instruction is distinct from the scheme's 150 threshold.
    expect(rubric.taskRequirements.join(' ')).toContain('200');
  });

  it('applies Q5 lower expression at C15 or 199 characters, but not C16 and 200', () => {
    const rubric = writing('5');
    const scores: LanguageScores = { 'language:heading-1': 7, 'language:heading-2': 7, 'language:heading-3': 1, 'language:expression': 30, 'language:length:characters': 320 };
    expect(languageWritingMarks(rubric, scores)).toBe(35);
    scores['language:heading-3'] = 2;
    scores['language:length:characters'] = 199;
    expect(languageCriterionValue(rubric, 'expression', scores)).toBe(20);
    scores['language:length:characters'] = 200;
    expect(languageWritingMarks(rubric, scores)).toBe(46);
    expect(rubric.taskRequirements.join(' ')).toContain('320');
  });

  it('binds all 27 listening tasks to the verified recording and original aural booklet', () => {
    const listening = cards.filter(card => card.audioMaterial);
    expect(listening).toHaveLength(27);
    for (const card of listening) {
      expect(card.paperFileid).toBe('LC058ALPA00BV');
      expect(card.audioMaterial?.secFileid).toBe('LC058ZLP017BV.mp3');
      expect(card.sourceMaterial?.sourceFileid).toBe('LC058ALPA00BV');
      expect(card.sourceMaterial?.presentationNote).toBeUndefined();
    }
    expect(listening.filter(card => card.questionRef.includes('Section LA')).map(card => card.totalMarks)).toEqual([7, 7, 7]);
  });

  it('maps every task to its original Topic Atlas paper and scheme group without renumbering', () => {
    const tags = JSON.parse(readFileSync(resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'), 'utf8'));
    for (const task of census.tasks) {
      const map = readMap(task.atlas.fileid);
      const group = map.q.find(question => question.n === task.atlas.questionNumber)!;
      const card = rawById.get(idFor(task.key))!;
      expect(group, card.id).toBeDefined();
      expect(card.sourceEvidence.paperPages, card.id).toContain(group.pP);
      expect(card.sourceEvidence.schemePages.every(page => group.region.some(region => region.p === page)), card.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2026 && paper.fileid === task.atlas.fileid);
      expect(tagged.q.find((question: { n: string }) => question.n === group.n).primary, card.id).toBe(card.topicId);
    }
  });
});
