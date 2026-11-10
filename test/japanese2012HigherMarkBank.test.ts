import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as higher } from '../components/MarkBank/cards/japanese/higher';
import rawCards from '../components/MarkBank/cards/japanese/reviewed.json';
import census from '../scripts/markbank/authoring/reviews/japanese-2012-hl-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2012-hl.json';
import { tariffReconciles } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
import { languageCriterionValue, languageLengthId, languagePointsMarks, languageWritingMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = higher.filter(card => card.year === 2012);
const idFor = (key: (string | number | null)[]) => `ja-2012-hl-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2012-hl-${suffix}`)!;
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
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2012/${fileid}.json`), 'utf8'));

describe('Japanese 2012 Higher independent original-source review', () => {
  it('covers all 62 independently counted tasks and all 48 original pages', () => {
    expect(cards).toHaveLength(62);
    expect(cards.map(card => card.id).sort()).toEqual(census.tasks.map(task => idFor(task.key)).sort());
    for (const task of census.tasks) {
      const found = cards.find(card => card.id === idFor(task.key))!;
      expect(found.totalMarks, found.id).toBe(task.marks);
      expect(tariffReconciles(found), found.id).toBe(true);
      expect(rawCards.find(card => card.id === found.id)!.sourceEvidence).toMatchObject({ component: task.component, paperPages: task.paperPages, schemePages: task.schemePages });
      if ('paperRef' in task && task.paperRef) expect(found.questionRef).toBe(task.paperRef);
    }
    expect(census.checksums).toEqual({ reading: 120, writing: 100, listening: 80, total: 300 });
    expect(Object.values(census.pageRoles).map(pages => Object.keys(pages).length)).toEqual([20, 8, 20]);
    expect(review.sources.map(source => ({ component: source.document, path: source.path, sha256: source.sha256 }))).toEqual(census.sources);
    for (const source of review.sources) expect(source.pagesReviewed).toEqual(Object.keys(census.pageRoles[source.document as keyof typeof census.pageRoles]).map(Number));
    expect(review.consolidations).toEqual([]);
  });

  it('keeps all required links, dog cells, kanji and grammar blanks in complete tasks', () => {
    for (const [suffix, count] of [['1a', 8], ['1b-1', 9], ['1b-4-i', 4], ['2d-1', 5], ['2d-2', 5], ['2e-1', 10], ['2e-2', 10], ['3c', 12]] as const) {
      expect(point(suffix).rows).toHaveLength(count);
      expect(point(suffix).rows.every(row => row.marks === 1)).toBe(true);
    }
    expect(point('1b-1').taskGroups?.map(group => group.marks)).toEqual([3, 3, 3]);
    expect(point('3c').taskGroups?.map(group => group.marks)).toEqual([2, 2, 2, 2, 2, 2]);
    expect(point('1a').rows[6].contextNote).toContain('ブログ 0 marks');
    expect(point('1b-1').rows[8].verbatim).toBe('Blond / gold & Brown');
    expect(point('2d-2').rows.map(row => row.verbatim)).toEqual(['き', 'やす', 'で', 'はな', 'おも']);
    expect(point('2e-1').rows.map(row => row.contextNote)).toEqual(['a', 'b', 'c(i)', 'c(ii)', 'd', 'e', 'f(i)', 'f(ii)', 'g', 'h']);
    expect(point('2e-2').rows.map(row => row.verbatim)).toEqual(['言う／いう', '来た ／きた', '学校だ', 'きびしくない', 'ない', 'する', 'いかない', 'だった', 'もらった', 'すんでいる']);
  });

  it('preserves comprehension quotas, zero responses and only published partial credit', () => {
    for (const [suffix, count, marks] of [['2a-1', 3, 1], ['2a-2', 2, 1], ['2a-3', 2, 1], ['2a-6', 3, 1], ['3a-2', 2, 2]] as const) {
      expect(point(suffix).rows).toHaveLength(count);
      expect(point(suffix).rows.every(row => row.kind === 'criterion' && JSON.stringify(row.permittedMarks) === JSON.stringify([0, marks]))).toBe(true);
      expect(marksClaimed(point(suffix), Object.fromEntries(point(suffix).rows.map(row => [row.id, marks])))).toBe(count * marks);
    }
    expect(point('2a-1').rows[0].contextNote).toContain('He is Irish. 0 marks');
    expect(point('2a-2').rows[0].contextNote?.replace(/\s+/g, ' ')).toContain('Good atmosphere, 0 marks');
    expect(point('2a-4').rows[0].verbatim).toContain('Sea/ Mountain/ Park, 1 mark');
    expect(point('3a-1-b').rows[0].verbatim).toContain('Germany 1 mark');
    for (const suffix of ['2a-4', '3a-1-b']) {
      expect(marksClaimed(point(suffix), { 'r-1': 1 })).toBe(1);
      expect(marksClaimed(point(suffix), { 'r-1': 2 })).toBe(2);
    }
    expect(marksClaimed(point('3a-2'), { 'r-1': 1 })).toBe(0);
    expect(point('2b-3').answerVariants).toHaveLength(2);
    expect(point('2b-3').answerVariants?.every(variant => variant.rows.length === 2 && variant.rows.every(row => row.marks === 1))).toBe(true);
    const countries = point('3b-4').rows[0];
    expect(countries.kind === 'anyN' && countries.group).toMatchObject({ claimMax: 2, perOption: 1, options: ['イギリス', 'アメリカ', 'ブラジル', 'フランス', '南アフリカ'] });
    expect(point('3b-5').rows.map(row => row.marks)).toEqual([2, 2]);
  });

  it('retains all 14 listening table cells and its exact one-mark partials', () => {
    const table = point('la');
    expect(table.taskGroups).toHaveLength(14);
    expect(table.rows).toHaveLength(15);
    expect(table.taskGroups?.map(group => group.marks)).toEqual([1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2]);
    expect(table.rows[0].contextNote).toContain('Japanese test (0 marks)');
    expect(table.stem).toContain('already printed');
    expect(table.rows.some(row => row.verbatim.includes('Leave the mobile phone'))).toBe(false);
    const partials = table.rows.filter(row => row.kind === 'criterion');
    expect(partials).toHaveLength(2);
    expect(partials.map(row => row.permittedMarks)).toEqual([[0, 1, 2], [0, 1, 2]]);
    expect(partials.map(row => row.contextNote).join(' ')).toContain('Dublin (1 mark)');
    expect(partials.map(row => row.contextNote).join(' ')).toContain('In 5 minutes (1 mark)');
    expect(marksClaimed(table, Object.fromEntries(table.rows.map(row => [row.id, row.kind === 'criterion' ? 2 : 'yes'])))).toBe(19);
  });

  it('counts full and partial versions once inside the two-direction and two-detail caps', () => {
    const directions = pool('lb-1-ii');
    expect(directions.count).toBe(2);
    expect(directions.groups).toHaveLength(4);
    const scores: LanguageScores = { 'language:group:direction-1': 1, 'language:row:direction-1:answer': 1,
      'language:group:direction-2': 1, 'language:elevator': 1 };
    expect(languagePointsMarks(directions, scores)).toBe(3);
    scores['language:elevator'] = 2;
    expect(languagePointsMarks(directions, scores)).toBe(4);
    scores['language:group:direction-3'] = 1; scores['language:row:direction-3:answer'] = 1;
    expect(languagePointsMarks(directions, scores)).toBe(4);
    const enjoyed = pool('ld-1-iii');
    expect(enjoyed.count).toBe(2);
    expect(enjoyed.groups.map(group => group.id)).toEqual(['mountains', 'people', 'spring']);
    const twoPartial: LanguageScores = { 'language:group:people': 1, 'language:people-answer': 1, 'language:group:spring': 1, 'language:spring-answer': 1 };
    expect(languagePointsMarks(enjoyed, twoPartial)).toBe(2);
    twoPartial['language:people-answer'] = 2;
    expect(languagePointsMarks(enjoyed, twoPartial)).toBe(3);
    twoPartial['language:spring-answer'] = 2;
    expect(languagePointsMarks(enjoyed, twoPartial)).toBe(4);
  });

  it('keeps survey identity, whole phone tariff, weather components and alternative Skype route', () => {
    expect(card('lc-1-a-i').questionRef).toBe('2012 HL Section LC Q1(i)(a)');
    expect(card('lc-1-b-i').questionRef).toBe('2012 HL Section LC Q1(i)(b)');
    for (const suffix of ['lc-1-a-i', 'lc-1-b-i']) {
      expect(point(suffix).rows).toHaveLength(2);
      expect(point(suffix).rows.every(row => JSON.stringify(row.permittedMarks) === '[0,2]')).toBe(true);
    }
    const phone = point('lc-2-iii');
    expect(phone.rows).toHaveLength(1);
    expect(phone.rows[0]).toMatchObject({ verbatim: '03-8353  - 4969', marks: 3 });
    expect(phone.rows[0].contextNote).toContain('no per-digit tariff');
    expect(point('lc-3-i').rows.map(row => row.marks)).toEqual([1, 1, 1]);
    expect(point('lc-3-ii').rows).toHaveLength(1);
    expect(point('lc-3-ii').rows[0].marks).toBe(2);
    expect(point('ld-1-iv').answerVariants?.map(variant => variant.rows.map(row => row.marks))).toEqual([[2], [1, 1]]);
    expect(point('ld-1-v').rows.map(row => row.marks)).toEqual([1, 1]);
    expect(point('ld-2-v').rows.map(row => row.marks)).toEqual([1, 1]);
    expect(point('ld-2-ii').rows[0].contextNote).toContain('Friends, 0 marks');
    expect(point('ld-2-iii').rows[0].contextNote).toContain('Tokyo, 0 marks');
  });

  it('binds half-credit rules only to listening A/B and the five Q3B tasks', () => {
    expect(cards.filter(card => card.audioMaterial)).toHaveLength(27);
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(14);
    const expected = ['la', 'lb-1-i', 'lb-1-ii', 'lb-2-i', 'lb-2-ii', 'lb-2-iii', 'lb-3-i', 'lb-3-ii', 'lb-3-iii', '3b-1', '3b-2', '3b-3', '3b-4', '3b-5'];
    expect(cards.filter(card => card.answerLanguageRule).map(card => card.id).sort()).toEqual(expected.map(suffix => `ja-2012-hl-${suffix}`).sort());
    for (const found of cards.filter(card => card.answerLanguageRule)) {
      const rule = found.answerLanguageRule!;
      expect(rule.penalizedLanguage).toBe(found.audioMaterial ? 'Japanese' : 'English');
      expect(review.selectors.some(selector => selector.document === 'scheme' && selector.page === rule.schemePages[0] && selector.text === rule.sourceText)).toBe(true);
    }
    const affected = review.cards.filter(card => card.extraneousMaterialRule);
    expect(affected).toHaveLength(5);
    for (const found of affected) {
      expect(found.id).toMatch(/^ja-2012-hl-3b-[1-5]$/);
      expect(found.extraneousMaterialRule).toMatchObject({ multiplier: 0.5, schemePages: [11], conditionLabel: 'quotation without manipulation where manipulation required or containing extraneous material' });
    }
    for (const suffix of ['lc-1-a-i', 'ld-1-i', '1a', '2a-1', '4', '5']) expect(card(suffix).answerLanguageRule).toBeUndefined();
  });

  it('retains aggregate discretionary content and inclusive lower-expression boundaries', () => {
    expect(writing('4').criteria.map(criterion => criterion.maxMarks)).toEqual([15, 5, 20]);
    expect(writing('5').criteria.map(criterion => criterion.maxMarks)).toEqual([6, 6, 6, 6, 6, 30]);
    expect(card('4').questionText).toContain('best day');
    expect(card('4').questionText).toContain('worst day');
    expect(card('5').questionText).toContain('any four');
    expect(writing('5').markingGuideNote).toContain('global across headings');
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
        scores[`language:${criterion.id}`] = award;
        remaining -= award;
      }
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(lower);
      const next = content.find(criterion => (scores[`language:${criterion.id}`] ?? 0) < criterion.maxMarks)!;
      scores[`language:${next.id}`] = (scores[`language:${next.id}`] ?? 0) + 1;
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(normal);
    }
  });

  it('retains all 27 original Atlas anchors and complete source contexts', () => {
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
        expect(task.paperPages.every(page => span.includes(page))).toBe(true);
      }
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2012 && paper.fileid === task.atlas.fileid);
      const topic = tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber);
      expect([topic.primary, topic.secondary], runtime.id).toContain(runtime.topicId);
      expect(sidecar.band).toEqual([1, 20]);
    }
    expect(map('LC058ALP000EV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 23 }, (_, i) => String(i + 1)));
    expect(map('LC058ALPA00EV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 4 }, (_, i) => String(i + 1)));
    expect(JSON.stringify(cards)).not.toContain('�');
  });
});
