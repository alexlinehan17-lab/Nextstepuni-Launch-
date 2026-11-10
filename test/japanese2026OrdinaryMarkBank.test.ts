import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import reviewed from '../components/MarkBank/cards/japanese/reviewed.json';
import census from '../scripts/markbank/authoring/reviews/japanese-2026-ol-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2026-ol.json';
import census2014 from '../scripts/markbank/authoring/reviews/japanese-2014-ol-census.json';
import census2015 from '../scripts/markbank/authoring/reviews/japanese-2015-ol-census.json';
import { languagePointsMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import { tariffReconciles, UNPRINTED_ANSWER, type LanguagePointsRubric } from '../types/markBank';
import type { PaperAnswerMap } from '../types/paperTrail';

const idFor = (key: (string | number | null)[]) => `ja-2026-ol-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const cards = ordinary.filter(card => card.year === 2026);
const card = (suffix: string) => cards.find(card => card.id === `ja-2026-ol-${suffix}`)!;
const rawById = new Map(reviewed.map(card => [card.id, card]));
const points = (suffix: string): LanguagePointsRubric => {
  const result = card(suffix);
  if (result.kind !== 'rubric' || result.rubric.system !== 'language-points') throw new Error(`Expected grouped rubric: ${suffix}`);
  return result.rubric;
};
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2026/${fileid}.json`), 'utf8'));

describe('Japanese 2026 Ordinary independent source review', () => {
  it('covers all 59 independently inventoried tasks and the 120/80/100 printed tariffs', () => {
    expect(cards).toHaveLength(59);
    expect(cards.map(card => card.id).sort()).toEqual(census.tasks.map(task => idFor(task.key)).sort());
    for (const task of census.tasks) {
      const found = cards.find(card => card.id === idFor(task.key))!;
      expect(found.totalMarks, found.id).toBe(task.marks);
      expect(tariffReconciles(found), found.id).toBe(true);
      const evidence = rawById.get(found.id)!.sourceEvidence;
      expect(evidence.component).toBe(task.component);
      expect(evidence.paperPages).toEqual(task.paperPages);
      expect(evidence.schemePages).toEqual(task.schemePages);
    }
    const total = (selected: typeof cards) => selected.reduce((sum, card) => sum + card.totalMarks, 0);
    expect(total(cards.filter(card => !card.audioMaterial && !['4', 'Q5'].includes(card.section!)))).toBe(120);
    expect(total(cards.filter(card => ['4', 'Q5'].includes(card.section!)))).toBe(80);
    expect(total(cards.filter(card => card.audioMaterial))).toBe(100);
    expect(total(cards)).toBe(300);
    expect(Object.values(census.pageRoles).map(pages => Object.keys(pages).length)).toEqual([16, 8, 20]);
  });

  it('reconciles the committed source pins and retains every previously served identity', () => {
    // Mandatory authoring gate: ja_review_verify.py rereads the pinned PDFs,
    // every physical page and every selector. CI has no ignored source archive.
    expect(review.sources.map(source => ({ component: source.document, path: source.path, sha256: source.sha256 }))).toEqual(census.sources);
    expect(review.sources.map(source => source.sha256)).toEqual([
      '3e426ef7ef17020d89b812e13eabaf47efb18d3b0b97e6dd4810d966551634b7',
      '19c7f71b7308c47f20207f7f90845456ea9c445e5e64e6ba1e72f56a878181d1',
      '1781dbc10f0f34043655b1ee9a093f368726a8caa5203dad214d0c63051321cc',
    ]);
    for (const source of review.sources) {
      const pages = census.pageRoles[source.document as keyof typeof census.pageRoles];
      expect(source.pagesReviewed).toEqual(Object.keys(pages).map(Number));
      expect(Object.values(pages).every(Boolean)).toBe(true);
    }
    // Global frozen-ID/content and alias accounting is pinned independently by
    // markBankCardPreservation and the 2025/2026 Higher review tests.
    expect(ordinary.filter(card => card.year !== 2026)).toHaveLength(261 + 42 - 22 + 40 - 40 + 41 - 34 + 40 - 41 + 39 - 39 + 56 + 57 + 54 + 52 + census2015.tasks.length + census2014.tasks.length);
    expect(census2015.tasks).toHaveLength(51);
    expect(census2014.tasks).toHaveLength(52);
    expect(ordinary.filter(card => card.year === 2014).map(card => card.id).sort()).toEqual(census2014.tasks.map(task => `ja-2014-ol-${task.key.filter(part => part !== null).join('-').toLowerCase()}`).sort());
    expect(ordinary.filter(card => card.year === 2015).map(card => card.id).sort()).toEqual(census2015.tasks.map(task => `ja-2015-ol-${task.key.filter(part => part !== null).join('-').toLowerCase()}`).sort());
    expect(cards.some(card => card.questionText.trim().length === 0)).toBe(false);
  });

  it('emits the exact reviewed convention, without extending it to unreviewed sittings', () => {
    const source = review.selectors.find(selector => selector.document === 'scheme' && selector.page === 3 && selector.row === 12 && selector.group === 1)!;
    for (const found of cards) expect(found.answerLanguageRule).toEqual({ otherLanguageMultiplier: 0.5, sourceText: source.text, schemePages: [3] });
    expect(ordinary.filter(card => !rawById.has(card.id)).some(card => card.answerLanguageRule)).toBe(false);
  });

  it('retains the restaurant table, printed examples, underlines, cloze and prefilled phone number', () => {
    for (const suffix of ['1-6-c', '2b', '2c', '3b-1', '3b-2', '4', '5', 'lb-3-i']) {
      const found = card(suffix);
      expect('questionFigure' in found && found.questionFigure, suffix).toBeTruthy();
    }
    expect(card('1-6-c').sourceMaterial?.pages).toEqual([2, 3]);
    expect(card('2b').sourceMaterial?.pages).toEqual([4, 5]);
    expect(card('3a-5').sourceMaterial?.pages).toEqual([8]);
    expect(card('4').questionText).toContain('A word should be used only once.');
    expect(card('4').questionText).toContain('(12)');
    expect(card('lb-3-i').kind).toBe('question');
    if (card('lb-3-i').kind === 'question') expect(rawById.get('ja-2026-ol-lb-3-i')!.rows?.[0].verbatim).toBe('070-935-4561');
  });

  it('preserves descending tariffs and the one-plus-two partial comprehension answer', () => {
    for (const suffix of ['1-3', '1-6-b']) {
      const found = card(suffix);
      if (found.kind !== 'question' || found.rows[0].kind !== 'anyN') throw new Error('Expected descending answer pool');
      expect(found.rows[0].group.perOptionSteps).toEqual([2, 1]);
      expect(found.rows[0].group.claimMax).toBe(2);
    }
    const rubric = points('2a-5');
    const scores: LanguageScores = { 'language:group:contents': 1, 'language:row:contents:contents': 1 };
    expect(languagePointsMarks(rubric, scores)).toBe(1);
    scores['language:row:contents:interesting'] = 1;
    expect(languagePointsMarks(rubric, scores)).toBe(3);
    scores['language:group:alternative-1'] = 1;
    scores['language:row:alternative-1:answer'] = 1;
    expect(languagePointsMarks(rubric, scores)).toBe(3);
  });

  it('keeps each finite printed pool whole and counts complete selected responses', () => {
    for (const [suffix, count, available] of [['2b', 5, 6], ['2c', 10, 13], ['3a-5', 3, 4], ['3b-1', 5, 6], ['3b-2', 5, 6], ['4', 10, 12], ['5', 5, 8]] as const) {
      expect(points(suffix).count, suffix).toBe(count);
      expect(points(suffix).groups, suffix).toHaveLength(available);
    }
    const rubric = points('2c');
    const scores: LanguageScores = {};
    for (const group of rubric.groups) {
      scores[`language:group:${group.id}`] = 1;
      scores[`language:row:${group.id}:answer`] = 1;
    }
    expect(languagePointsMarks(rubric, scores)).toBe(10);
    scores['language:other-language:row:item-1:answer'] = 1;
    expect(languagePointsMarks(rubric, scores, card('2c').answerLanguageRule)).toBe(9.5);
  });

  it('scores truth and quote independently and preserves both quoted alternatives', () => {
    const rubric = points('2b');
    expect(rubric.groups[2].rows[1].text).toContain('／');
    const scores: LanguageScores = {};
    for (const group of rubric.groups) {
      scores[`language:group:${group.id}`] = 1;
      scores[`language:row:${group.id}:true-false`] = 1;
    }
    expect(languagePointsMarks(rubric, scores)).toBe(5);
    scores['language:row:item-1:quote'] = 1;
    expect(languagePointsMarks(rubric, scores)).toBe(7);
    scores['language:other-language:row:item-1:quote'] = 1;
    expect(languagePointsMarks(rubric, scores, card('2b').answerLanguageRule)).toBe(6);
  });

  it('does not invent cultural model reasons where the scheme only prices two points', () => {
    const found = card('2d');
    if (found.kind !== 'question') throw new Error('Expected unprinted criterion');
    expect(found.rows).toHaveLength(1);
    expect(found.rows[0]).toMatchObject({ kind: 'criterion', unprinted: true, verbatim: UNPRINTED_ANSWER, marks: 4, permittedMarks: [0, 2, 4], contextNote: '(any 2 points, 2 marks each)' });
    expect(found.rows[0].parts).toEqual([
      { id: 'point-1', verbatim: '1. points', marks: 2, permittedMarks: [0, 2] },
      { id: 'point-2', verbatim: '2. points', marks: 2, permittedMarks: [0, 2] },
    ]);
  });

  it('scores five chosen writing responses using independent content and expression bands', () => {
    const rubric = points('5');
    const scores: LanguageScores = {};
    for (const group of rubric.groups) {
      scores[`language:group:${group.id}`] = 1;
      for (const criterion of group.criteria!) scores[`language:${criterion.id}`] = 5;
    }
    expect(languagePointsMarks(rubric, scores)).toBe(50);
    scores['language:item-1-content'] = 1;
    scores['language:item-1-expression'] = 2;
    expect(languagePointsMarks(rubric, scores)).toBe(43);
    scores['language:other-language:group:item-1'] = 1;
    expect(languagePointsMarks(rubric, scores, card('5').answerLanguageRule)).toBe(41.5);
    // A partial or other-language response still uses exactly one selection.
    scores['language:group:item-1'] = 0;
    expect(languagePointsMarks(rubric, scores, card('5').answerLanguageRule)).toBe(50);
    expect(rubric.groups.every(group => group.criteria?.every(criterion => criterion.permittedMarks.join(',') === '0,1,2,3,4,5'))).toBe(true);
  });

  it('retains all listening question continuations and the required two-day weather answer', () => {
    expect(card('lc-1-i').questionText).toBe('What sport did Oda‐san play when he was small?');
    expect(card('lc-1-ii').questionText).toContain('he was 9 years old?');
    expect(card('lc-1-iii').questionText).toContain('Which of the following did he NOT win in 2025?');
    expect(card('lc-1-iv').questionText).toBe('How old is Oda‐san now?');
    expect(card('lc-1-v').questionText).toContain('What is his hobby?');
    const weather = card('lc-2-i');
    if (weather.kind !== 'question') throw new Error('Expected weather rows');
    expect(weather.rows.map(row => row.contextNote)).toEqual(['Saturday', 'Sunday']);
    expect(weather.rows.map(row => row.kind === 'anyN' && row.group.perOption)).toEqual([2, 2]);
    const listening = cards.filter(card => card.audioMaterial);
    expect(listening).toHaveLength(29);
    for (const found of listening) {
      expect(found.paperFileid).toBe('LC058GLPA00BV');
      expect(found.audioMaterial?.secFileid).toBe('LC058ZLP017BV.mp3');
      expect(found.sourceMaterial?.sourceFileid).toBe('LC058GLPA00BV');
      expect(found.sourceMaterial?.presentationNote).toBeUndefined();
    }
  });

  it('keeps original Atlas anchors, including all six T/F anchors and the expression page', () => {
    const tags = JSON.parse(readFileSync(resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'), 'utf8'));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const found = rawById.get(idFor(task.key))!;
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2026 && paper.fileid === task.atlas.fileid);
      const anchors = [task.atlas.questionNumber, ...('additionalQuestionNumbers' in task.atlas ? task.atlas.additionalQuestionNumbers ?? [] : [])];
      for (const anchor of anchors) {
        const group = sidecar.q.find(question => question.n === anchor)!;
        expect(group, found.id).toBeDefined();
        expect(found.sourceEvidence.paperPages).toContain(group.pP);
        expect(found.sourceEvidence.schemePages.every(page => group.region.some(region => region.p === page)), found.id).toBe(true);
        expect(tagged.q.find((question: { n: string }) => question.n === anchor).primary, found.id).toBe(found.topicId);
      }
    }
    expect(map('LC058GLP000BV.pdf').q.find(question => question.n === '29')!.region.map(region => region.p)).toEqual([11, 12]);
  });
});
