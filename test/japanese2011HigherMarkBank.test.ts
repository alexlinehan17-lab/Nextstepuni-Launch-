import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as higher } from '../components/MarkBank/cards/japanese/higher';
import rawCards from '../components/MarkBank/cards/japanese/reviewed.json';
import census from '../scripts/markbank/authoring/reviews/japanese-2011-hl-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2011-hl.json';
import { tariffReconciles } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
import { languageCriterionValue, languageLengthId, languagePointsMarks, languageWritingMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = higher.filter(card => card.year === 2011);
const idFor = (key: (string | number | null)[]) => `ja-2011-hl-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2011-hl-${suffix}`)!;
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
const pool = (suffix: string) => {
  const found = card(suffix);
  if (found.kind !== 'rubric' || found.rubric.system !== 'language-points') throw new Error(`Expected pool ${suffix}`);
  return found.rubric;
};
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2011/${fileid}.json`), 'utf8'));

describe('Japanese 2011 Higher independent original-source review', () => {
  it('covers all 56 original tasks, all 48 physical pages and the published 300 marks', () => {
    expect(cards).toHaveLength(56);
    expect(cards.map(card => card.id).sort()).toEqual(census.tasks.map(task => idFor(task.key)).sort());
    for (const task of census.tasks) {
      const found = cards.find(card => card.id === idFor(task.key))!;
      expect(found.totalMarks, found.id).toBe(task.marks);
      expect(tariffReconciles(found), found.id).toBe(true);
      expect(rawCards.find(card => card.id === found.id)!.sourceEvidence).toMatchObject({ component: task.component, paperPages: task.paperPages, schemePages: task.schemePages });
    }
    expect(census.checksums).toEqual({ reading: 120, writing: 100, listening: 80, total: 300 });
    expect(Object.values(census.pageRoles).map(pages => Object.keys(pages).length)).toEqual([20, 8, 20]);
    expect(review.sources.map(source => ({ component: source.document, path: source.path, sha256: source.sha256 }))).toEqual(census.sources);
    for (const source of review.sources) expect(source.pagesReviewed).toEqual(Object.keys(census.pageRoles[source.document as keyof typeof census.pageRoles]).map(Number));
    expect(review.consolidations).toEqual([]);
  });

  it('keeps required tables, transformations and paired kanji complete', () => {
    for (const [suffix, count] of [['1a', 8], ['1d-1', 4], ['1d-2', 4], ['2a-1', 5], ['2a-3', 5], ['2c', 10], ['3c', 12], ['3d', 10]] as const) expect(point(suffix).rows).toHaveLength(count);
    expect(point('2a-1').taskGroups?.map(group => group.marks)).toEqual([1, 1, 1, 2]);
    expect(point('2a-3').taskGroups?.map(group => group.marks)).toEqual([2, 2, 2, 2]);
    expect(point('3a-2').taskGroups?.map(group => group.marks)).toEqual([2, 2, 2, 2, 2, 2]);
    expect(point('3c').taskGroups?.map(group => group.marks)).toEqual([2, 2, 2, 2, 2, 2]);
    expect(point('3d').rows[7].verbatim).toBe('が／は');
    expect(point('2c').rows.map(row => row.verbatim)).toEqual(['する', 'もらう／もらわない', '来る／来ない', 'がんばる', 'ない', 'かえる', 'みる', 'ねる', 'きかない／きく', '出ない']);
    const scenarios = point('2a-2-iii');
    expect(scenarios.rows.map(row => row.marks)).toEqual([1, 1, 1, 1]);
    expect(scenarios.taskGroups?.map(group => group.marks)).toEqual([2, 2]);
    expect(scenarios.questionText).toContain('if he has a date');
    expect(scenarios.questionText).toContain('if he does not have a date');
    expect(marksClaimed(scenarios, { 'r-1': 'yes', 'r-2': 'yes', 'r-3': 'yes', 'r-4': 'yes' })).toBe(4);
  });

  it('retains the twelve missing voicemail cells, exact partials and unpriced given cells', () => {
    const table = point('la');
    expect(table.rows).toHaveLength(12);
    expect(table.taskGroups?.map(group => group.marks)).toEqual([2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1]);
    expect(table.rows.filter(row => row.kind === 'criterion')).toHaveLength(4);
    expect(table.rows[2].contextNote).toContain('This evening 0');
    expect(table.stem).toContain('Four cells are already given');
    expect(table.rows.map(row => row.verbatim).join(' ')).not.toContain('Tomorrow morning');
    expect(table.rows.map(row => row.verbatim).join(' ')).not.toContain('Bad weather');
    expect(table.rows[4].verbatim).toContain('sick 1 mark');
    expect(table.rows[5].verbatim).toContain('double 1 mark');
    expect(table.rows[9].verbatim).toContain('party 1 mark');
    expect(marksClaimed(table, Object.fromEntries(table.rows.map(row => [row.id, row.kind === 'criterion' ? 2 : 'yes'])))).toBe(21);
    expect(point('lb-1-i').answerVariants?.map(variant => variant.rows.map(row => row.marks))).toEqual([[1, 1], [2]]);
    expect(point('lb-1-ii').rows.map(row => row.marks)).toEqual([2, 2]);
    expect(marksClaimed(point('lb-1-ii'), { 'r-1': 'yes', 'r-2': 1 })).toBe(3);
  });

  it('enforces one pool-level manga partial without assigning it to an invented full concept', () => {
    const recruitment = point('lc-2-ii');
    expect(recruitment.rows.map(row => row.permittedMarks)).toEqual([[0, 1, 2], [0, 2]]);
    for (const row of recruitment.rows) {
      expect(row.verbatim).toContain('First online manga newspaper');
      expect(row.verbatim).toContain('homepage is manganews.com');
      expect(row.verbatim).toContain('(manga 1 mark)');
      expect(row.contextNote).toContain('ONCE across the whole task');
      expect(row.contextNote).toContain('never also score alongside an overlapping full detail');
    }
    expect(marksClaimed(recruitment, { 'r-1': 1, 'r-2': 1 })).toBe(1);
    expect(marksClaimed(recruitment, { 'r-1': 1, 'r-2': 2 })).toBe(3);
    expect(marksClaimed(recruitment, { 'r-1': 2, 'r-2': 2 })).toBe(4);
    expect(point('lc-2-iii').rows).toHaveLength(1);
    expect(point('lc-2-iii').rows[0]).toMatchObject({ verbatim: '2444-1701', marks: 2 });
    expect(point('lc-2-iii').rows[0].contextNote).toContain('No per-digit allocation');
    expect(point('lc-1-iii').rows[0].permittedMarks).toEqual([0, 1, 2]);
    expect(point('lc-1-ii').questionRef).toBe('2011 HL Section LC Q1(ii)');
    expect(point('lc-1-ii').rows[0].contextNote).toContain('scheme labels this answer (iii)');
  });

  it('counts weather and friends partials once within their two-detail quotas', () => {
    const weather = pool('lc-3');
    expect(weather.count).toBe(2);
    const scores: LanguageScores = { 'language:group:morning': 1, 'language:morning-answer': 1,
      'language:group:afternoon': 1, 'language:afternoon-answer': 1 };
    expect(languagePointsMarks(weather, scores)).toBe(2);
    scores['language:morning-answer'] = 2;
    expect(languagePointsMarks(weather, scores)).toBe(3);
    scores['language:afternoon-answer'] = 2;
    scores['language:group:temperature'] = 1; scores['language:row:temperature:answer'] = 1;
    expect(languagePointsMarks(weather, scores)).toBe(4);
    const dislikes = pool('ld-2-iii');
    const partial: LanguageScores = { 'language:group:detail-1': 1, 'language:row:detail-1:answer': 1,
      'language:group:friends': 1, 'language:friends-answer': 1 };
    expect(languagePointsMarks(dislikes, partial)).toBe(3);
    partial['language:friends-answer'] = 2;
    expect(languagePointsMarks(dislikes, partial)).toBe(4);
    expect(dislikes.markingGuideNote).toContain('original paper identifies Q2(iii)');
  });

  it('emits only source-local language and combined response conditions', () => {
    expect(cards.filter(card => card.audioMaterial)).toHaveLength(24);
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(22);
    expect(cards.filter(card => card.extraneousMaterialRule)).toHaveLength(10);
    for (const found of cards.filter(card => card.answerLanguageRule)) {
      const rule = found.answerLanguageRule!;
      expect(review.selectors.some(selector => selector.document === 'scheme' && selector.page === rule.schemePages[0] && selector.text === rule.sourceText)).toBe(true);
      if (found.id.includes('-1c-')) expect(rule.penalizedLanguage).toBe('English');
      else if (found.id.includes('-2b-') || found.id.includes('-3b-')) expect(rule.penalizedLanguage).toBeUndefined();
      else expect(rule.penalizedLanguage).toBe('Japanese');
    }
    expect(cards.filter(card => card.audioMaterial && card.answerLanguageRule).map(card => card.id)).toEqual(['ja-2011-hl-la']);
    for (const suffix of ['1a', '1d-1', '2c', '3a-1', '3c', '3d', '3e', '4', '5', 'lb-1-i', 'lc-3', 'ld-2-i']) expect(card(suffix).answerLanguageRule).toBeUndefined();
    expect(point('2b-2').rows[0].verbatim).toBe('うんどうをはじめまたほうがいいです。');
    expect(point('2b-2').rows[0].contextNote).toContain('Source discrepancy');
    expect(point('3a-2').rows.map(row => row.contextNote).join(' ')).toContain('ウェザー・ニュース・タッチ');
  });

  it('retains both writing options, individual heading tariffs and inclusive lower-E thresholds', () => {
    expect(writing('4').criteria.map(criterion => criterion.maxMarks)).toEqual([5, 5, 5, 5, 20]);
    expect(writing('5').criteria.map(criterion => criterion.maxMarks)).toEqual([5, 10, 10, 5, 30]);
    expect(card('4').questionText).toContain('great day');
    expect(card('4').questionText).toContain('terrible day');
    expect(card('5').questionText).toContain('Japan Scholarship Program');
    expect(card('5').questionText).toContain('2011 Japanese Speech Contest');
    expect(card('5').sourceMaterial?.pages).toEqual([15, 16]);
    expect(card('5').questionText).toContain('June 25th, 2011');
    expect(card('5').questionText).toContain('June 30th, 2011');
    expect(writing('3e').criteria.map(criterion => criterion.permittedMarks)).toEqual([[0, 2], [0, 2], [0, 1]]);
    for (const [suffix, normal, lower, length, threshold] of [['4', 20, 15, 150, 10], ['5', 30, 20, 200, 15]] as const) {
      const rubric = writing(suffix);
      const scores: LanguageScores = { [languageLengthId('characters')]: 500 };
      for (const criterion of rubric.criteria) scores[`language:${criterion.id}`] = criterion.maxMarks;
      expect(languageWritingMarks(rubric, scores)).toBe(normal * 2);
      scores[languageLengthId('characters')] = length - 1;
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(lower);
      scores[languageLengthId('characters')] = length;
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(normal);
      let remaining: number = threshold;
      const content = rubric.criteria.filter(criterion => criterion.id !== 'expression');
      for (const criterion of content) {
        const award = Math.min(criterion.maxMarks, remaining);
        scores[`language:${criterion.id}`] = award; remaining -= award;
      }
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(lower);
      const next = content.find(criterion => (scores[`language:${criterion.id}`] ?? 0) < criterion.maxMarks)!;
      scores[`language:${next.id}`] = (scores[`language:${next.id}`] ?? 0) + 1;
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(normal);
    }
  });

  it('preserves all 15 original Atlas IDs and adds only the three missing written anchors', () => {
    const tags = JSON.parse(readFileSync(resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'), 'utf8'));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2011 && paper.fileid === task.atlas.fileid);
      const topic = tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber);
      expect([topic.primary, topic.secondary], runtime.id).toContain(runtime.topicId);
      expect(sidecar.band).toEqual([1, 20]);
    }
    expect(map('LC058ALP000EV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 14 }, (_, i) => String(i + 1)));
    expect(map('LC058ALPA00EV.pdf').q.map(question => question.n)).toEqual(['1', '2', '3', '4']);
    expect(cards.filter(card => card.audioMaterial && card.topicId === 'japanese-6-1')).toEqual([]);
    expect(JSON.stringify(cards)).not.toContain('�');
  });
});
