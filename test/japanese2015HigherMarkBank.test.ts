import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as higher } from '../components/MarkBank/cards/japanese/higher';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import rawCards from '../components/MarkBank/cards/japanese/reviewed.json';
import aliases from '../components/MarkBank/cards/japanese/aliases.json';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import census from '../scripts/markbank/authoring/reviews/japanese-2015-hl-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2015-hl.json';
import { tariffReconciles } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
import { languageCriterionValue, languageLengthId, languageMarks, languagePointsMarks, languageWritingMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = higher.filter(card => card.year === 2015);
const idFor = (key: (string | number | null)[]) => `ja-2015-hl-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2015-hl-${suffix}`)!;
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
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2015/${fileid}.json`), 'utf8'));

describe('Japanese 2015 Higher independent source review', () => {
  it('covers all 60 independent tasks and every physical source page', () => {
    expect(cards).toHaveLength(60);
    expect(cards.map(card => card.id).sort()).toEqual(census.tasks.map(task => idFor(task.key)).sort());
    for (const task of census.tasks) {
      const found = cards.find(card => card.id === idFor(task.key))!;
      expect(found.totalMarks, found.id).toBe(task.marks);
      expect(tariffReconciles(found), found.id).toBe(true);
      expect(rawCards.find(card => card.id === found.id)!.sourceEvidence).toMatchObject({ component: task.component, paperPages: task.paperPages, schemePages: task.schemePages });
    }
    expect(census.checksums).toEqual({ reading: 120, writing: 100, listening: 80, total: 300 });
    expect(census.candidateMaximum).toMatchObject({ written: 220, listening: 80, total: 300 });
    expect(Object.values(census.pageRoles).map(pages => Object.keys(pages).length)).toEqual([20, 8, 20]);
    expect(review.sources.map(source => ({ component: source.document, path: source.path, sha256: source.sha256 }))).toEqual(census.sources);
    for (const source of review.sources) expect(source.pagesReviewed).toEqual(Object.keys(census.pageRoles[source.document as keyof typeof census.pageRoles]).map(Number));
  });

  it('adds 60 new tasks while keeping the frozen 600 identities and original files', () => {
    const frozen = [
      ['higher', 339, 'c8acca0df611e18fae7ccb646809ec4b23533e316aacf4aae021120db37a8a54'],
      ['ordinary', 261, '83a3b57745ae80882d11a3346ab34cefba7b70d801701b87202493e0650983ef'],
    ] as const;
    const originalIds = frozen.flatMap(([level, count, sha256]) => {
      const text = readFileSync(resolve(__dirname, `../components/MarkBank/cards/japanese/${level}.ts`), 'utf8');
      expect(createHash('sha256').update(text).digest('hex')).toBe(sha256);
      const ids = [...text.matchAll(/^ {4}id: "([^"]+)"/gm)].map(match => match[1]);
      expect(ids).toHaveLength(count);
      return ids;
    });
    const live = new Set([...higher, ...ordinary].map(card => card.id));
    for (const id of originalIds) expect(live.has(id) || live.has(CARD_ID_ALIASES[id]), id).toBe(true);
    expect(originalIds.some(id => id.startsWith('ja-2015-'))).toBe(false);
    expect(review.consolidations).toEqual([]);
    expect(Object.keys(aliases)).toHaveLength(391);
    // Add independently reviewed2011OL49,2010HL66 and2010OL61; frozen600/391 stay unchanged.
    expect(rawCards.filter(card => !originalIds.includes(card.id))).toHaveLength(1556 + 49 + 66 + 61);
    expect(live.size).toBe(600 + 1556 + 49 + 66 + 61 - 391);
  });

  it('keeps every required link, kanji and grammar pool whole', () => {
    for (const [suffix, count] of [['1a-1', 6], ['2b-1', 5], ['2b-2', 5], ['2c-1', 5], ['2c-2', 5], ['3c', 5], ['3d', 10]] as const) {
      const found = card(suffix);
      if (found.kind !== 'rubric' || found.rubric.system !== 'language-points') throw new Error('Expected required pool');
      expect(found.rubric.count).toBe(count);
      expect(found.rubric.groups).toHaveLength(count);
      const scores: LanguageScores = {};
      for (const group of found.rubric.groups) {
        scores[`language:group:${group.id}`] = 1;
        for (const row of group.rows) scores[`language:row:${group.id}:${row.id}`] = 1;
      }
      expect(languagePointsMarks(found.rubric, scores)).toBe(found.totalMarks);
    }
    for (const continuation of ['から、日本語の勉強をします。', 'ことがありません。', 'でしょう。', 'りしないでください。']) {
      expect(card('2c-2').questionText).toContain(continuation);
    }
    expect(card('3c').questionText).toContain('がいこくじん');
    const kanji = card('3c');
    if (kanji.kind !== 'rubric' || kanji.rubric.system !== 'language-points') throw new Error('Expected pairs');
    expect(kanji.rubric.groups.map(group => group.rows.map(row => row.marks))).toEqual(Array(5).fill([1, 1]));
  });

  it('retains both complete tables and the exact separately priced components', () => {
    const courses = point('2a-1');
    expect(courses.rows).toHaveLength(12);
    expect(courses.taskGroups?.map(group => group.marks)).toEqual([1, 2, 1, 1, 1, 2, 1, 1, 1, 1]);
    expect(courses.rows.every(row => row.marks === 1)).toBe(true);
    expect(courses.rows.map(row => row.verbatim)).toEqual(['Osaka', 'Tuesday', 'Thursday', '9,500 yen', 'Chinese', 'Kobe', 'Friday', 'Saturday', '14,000 yen', 'Kyoto', '23,000 yen', 'Korean']);
    const speeches = point('la');
    expect(speeches.taskGroups).toHaveLength(12);
    expect(speeches.taskGroups?.map(group => group.marks)).toEqual([2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1]);
    expect(speeches.rows.slice(0, 2).map(row => [row.verbatim, row.marks])).toEqual([['Italian', 1], ['teacher', 1]]);
    expect(speeches.rows.find(row => row.verbatim.includes('Game developer'))).toMatchObject({ marks: 2 });
    expect(point('1b-4').rows.map(row => [row.verbatim, row.marks])).toEqual([['Sausage', 1], ['muffin', 1]]);
    expect(point('2a-4').rows.map(row => row.marks)).toEqual([2, 2]);
  });

  it('keeps descending detail pools, one-person choice and the published partials', () => {
    for (const suffix of ['3a-1-i', '3b-1', 'lb-3-i', 'lb-3-ii', 'lc-1-iii', 'lc-2-i', 'ld-2', 'ld-3']) {
      const found = point(suffix);
      expect(found.rows[0].group?.perOptionSteps).toEqual([2, 1]);
      expect(marksClaimed(found, {}, { 'r-1': [0] })).toBe(2);
      expect(marksClaimed(found, {}, { 'r-1': [0, 1, 2] })).toBe(3);
    }
    const people = point('3a-3-i');
    expect(people.answerVariants?.map(variant => variant.label)).toEqual(['Nicole', 'Michael']);
    expect(people.answerVariants?.map(variant => variant.rows[0].group?.options.length)).toEqual([7, 5]);
    for (const variant of people.answerVariants!) {
      const selected = { ...people, rows: variant.rows };
      expect(tariffReconciles(selected)).toBe(true);
      expect(selected.rows).toHaveLength(1);
      expect(marksClaimed(selected, {}, { 'r-1': [0], 'r-2': [0] })).toBe(2);
      expect(marksClaimed(selected, {}, { 'r-1': [0, 1, 2], 'r-2': [0, 1] })).toBe(3);
      for (const option of selected.rows[0].group!.options) {
        expect(review.selectors.some(selector => selector.document === 'scheme' && selector.page === 10 && selector.text.includes(option))).toBe(true);
      }
    }
    expect(point('3a-1-ii').rows[0]).toMatchObject({ kind: 'criterion', marks: 2, permittedMarks: [0, 1, 2] });
    expect(point('3a-1-ii').rows[0].contextNote).toContain('studying media and Japanese 1 mark');
    expect(point('3b-2').rows[0]).toMatchObject({ kind: 'criterion', marks: 3, permittedMarks: [0, 2, 3] });
    expect(point('lc-1-i').rows[0].contextNote).toContain('sick 1 mark');
    expect(point('lb-1-v').rows[0]).toMatchObject({ marks: 3, verbatim: '03-6576-8180' });
    expect(point('lb-1-v').rows[0].contextNote).toContain('no per-digit allocation');
  });

  it('preserves the unpriced three-item task for confidence review with exact visible language guidance', () => {
    const found = point('lb-1-iv');
    expect(found.totalMarks).toBe(3);
    expect(found.tariffModel).toEqual({ kind: 'questionTotal' });
    expect(found.rows).toHaveLength(1);
    expect(found.rows[0].marks).toBeNull();
    expect(found.rows[0].permittedMarks).toBeUndefined();
    expect(found.rows[0].group).toBeUndefined();
    expect(found.rows[0].verbatim.split('/').map(text => text.trim())).toEqual(['Kimono', 'clothes', 'books', 'DVDs', 'computer games', 'bicycles']);
    expect(found.questionText).toBe('Name three items you can get there.');
    expect(found.rows[0].contextNote).toContain('Marks are not calculated because the response split is unpublished');
    expect(found.rows[0].contextNote).toContain('(1/2 marks if answered in Japanese, romaji or Japanese script)');
    expect(found.answerLanguageRule).toBeUndefined();
    expect(found.qa?.gates).not.toContain('tariff');
    expect(found.qa?.gates).toContain('source-tariff-unresolved');
    expect(review.unresolvedSourceIssues).toEqual([expect.objectContaining({ cardId: found.id, resolution: null })]);
    expect(rawCards.find(card => card.id === found.id)!.sourceEvidence.generalSchemePages).toEqual([3]);
  });

  it('assesses three distinct Peter Frankl responses with the unattached one-mark partial and independent language flags', () => {
    const found = card('lb-2');
    if (found.kind !== 'rubric' || found.rubric.system !== 'language-points') throw new Error('Expected manual response pool');
    expect(found.rubric.count).toBe(3);
    expect(found.rubric.groups).toHaveLength(3);
    for (const group of found.rubric.groups) {
      expect(group.rows).toEqual([]);
      expect(group.criteria?.[0].permittedMarks).toEqual([0, 1, 2]);
      const text = group.criteria![0].guidance.join(' ');
      for (const answer of ['Maths teacher', 'famous foreigner', 'won maths Olympics', 'speaks lots of languages', 'speaks 12 languages', 'street performer', 'juggler', 'appears on TV', 'popular (1 mark)']) expect(text).toContain(answer);
    }
    expect(found.rubric.markingGuideNote).toContain('count that language concept once');
    expect(found.rubric.markingGuideNote).toContain('no exclusive association is inferred');
    expect(found.rubric.markingGuideNote).toContain('do not count a partial and full version of the same answer twice');
    const scores: LanguageScores = { 'language:group:response-1': 1, 'language:response-1': 1, 'language:group:response-2': 1, 'language:response-2': 2, 'language:group:response-3': 1, 'language:response-3': 2 };
    expect(languageMarks(found, scores)).toBe(5);
    expect(languageMarks(found, { ...scores, 'language:other-language:group:response-1': 1 })).toBe(4.5);
    expect(languageMarks(found, { ...scores, 'language:response-1': 2 })).toBe(6);
    expect(languageMarks(found, { ...scores, 'language:group:response-1': 0 })).toBe(4);
  });

  it('limits reading language reductions to the twelve Question 1 tasks and extraneous material to four Q2 responses', () => {
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(34);
    const readingRules = cards.filter(card => !card.audioMaterial && card.answerLanguageRule);
    expect(readingRules).toHaveLength(12);
    for (const found of readingRules) {
      expect(found.id).toMatch(/ja-2015-hl-1[ab]-/);
      expect(found.answerLanguageRule?.sourceText).toContain('Half marks if answered in the incorrect language');
      expect(found.answerLanguageRule?.schemePages).toEqual([5]);
      expect(found.answerLanguageRule?.penalizedLanguage).toBeUndefined();
    }
    for (const found of cards.filter(card => card.answerLanguageRule)) {
      expect(review.selectors.some(selector => selector.document === 'scheme' && selector.text === found.answerLanguageRule?.sourceText)).toBe(true);
      if (found.audioMaterial) expect(found.answerLanguageRule?.penalizedLanguage).toBe('Japanese');
    }
    expect(cards.filter(card => card.extraneousMaterialRule).map(card => card.id)).toEqual(['i', 'ii', 'iii', 'iv'].map(roman => `ja-2015-hl-2a-2-${roman}`));
    for (const found of cards.filter(card => /ja-2015-hl-[2345]/.test(card.id))) expect(found.answerLanguageRule).toBeUndefined();
  });

  it('keeps discretionary writing credit global and applies the exact inclusive content thresholds', () => {
    expect(writing('4').criteria.map(criterion => criterion.maxMarks)).toEqual([8, 8, 2, 1, 1, 20]);
    expect(writing('5').criteria.map(criterion => criterion.maxMarks)).toEqual([6, 6, 6, 6, 4, 1, 1, 30]);
    for (const [suffix, normal, lower, length, threshold] of [['4', 20, 15, 150, 10], ['5', 30, 20, 200, 15]] as const) {
      const rubric = writing(suffix);
      const scores: LanguageScores = { [languageLengthId('characters')]: 500 };
      for (const criterion of rubric.criteria) scores[`language:${criterion.id}`] = criterion.maxMarks;
      expect(languageWritingMarks(rubric, scores)).toBe(normal * 2);
      scores[languageLengthId('characters')] = length - 1;
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(lower);
      scores[languageLengthId('characters')] = length;
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(normal);
      const content = rubric.criteria.filter(criterion => criterion.id !== 'expression');
      let remaining: number = threshold;
      for (const criterion of content) {
        const award = Math.min(criterion.maxMarks, remaining);
        scores[`language:${criterion.id}`] = award;
        remaining -= award;
      }
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(lower);
      const next = content.find(criterion => scores[`language:${criterion.id}`] < criterion.maxMarks)!;
      scores[`language:${next.id}`] += 1;
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(normal);
      const expression = rubric.criteria.find(criterion => criterion.id === 'expression')!;
      for (const band of [...expression.bands!, ...expression.limits![0].bands!]) expect(band.guidance.join(' ').length).toBeGreaterThan(100);
    }
    expect(card('4').questionText).toContain('concert this weekend');
    expect(card('4').questionText).toContain('restaurant this weekend');
    expect(card('5').questionText).toContain('ANY 4');
    expect(card('5').questionText).toContain('Your future plans');
  });

  it('retains all 23 written and 15 aural Atlas anchors and eleven complete question crops', () => {
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(11);
    const tags = JSON.parse(readFileSync(resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'), 'utf8'));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      expect(task.paperPages, runtime.id).toContain(group.pP);
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2015 && paper.fileid === task.atlas.fileid);
      for (const number of [task.atlas.questionNumber, ...('additionalQuestionNumbers' in task.atlas ? task.atlas.additionalQuestionNumbers ?? [] : [])]) {
        expect(tagged.q.find((question: { n: string }) => question.n === number).primary, runtime.id).toBe(runtime.topicId);
      }
      expect(sidecar.band).toEqual([1, 20]);
    }
    expect(map('LC058ALP000EV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 23 }, (_, i) => String(i + 1)));
    expect(map('LC058ALPA00EV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 15 }, (_, i) => String(i + 1)));
    expect(JSON.stringify(cards)).not.toContain('�');
  });
});
