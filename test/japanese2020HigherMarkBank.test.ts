import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as higher } from '../components/MarkBank/cards/japanese/higher';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import rawCards from '../components/MarkBank/cards/japanese/reviewed.json';
import aliases from '../components/MarkBank/cards/japanese/aliases.json';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import census from '../scripts/markbank/authoring/reviews/japanese-2020-hl-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2020-hl.json';
import { tariffReconciles } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
import { languageCriterionValue, languagePointsMarks, languageWritingMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = higher.filter(card => card.year === 2020);
const idFor = (key: (string | number | null)[]) => `ja-2020-hl-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2020-hl-${suffix}`)!;
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
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2020/${fileid}.json`), 'utf8'));

describe('Japanese 2020 Higher independent source review', () => {
  it('covers all 62 independent tasks and every physical source page', () => {
    expect(cards).toHaveLength(62);
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

  it('adds 62 new tasks while keeping the frozen 600 identities and original files', () => {
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
    expect(originalIds.some(id => id.startsWith('ja-2020-'))).toBe(false);
    expect(review.consolidations).toEqual([]);
    expect(Object.keys(aliases)).toHaveLength(391);
    expect(rawCards.filter(card => !originalIds.includes(card.id))).toHaveLength(1328);
    expect(live.size).toBe(600 + 1328 - 391);
  });

  it('keeps every required finite pool whole without inventing optional answers', () => {
    for (const [suffix, count] of [['1a-1', 6], ['2b-1', 5], ['2b-2', 5], ['2c-1', 5], ['2c-2', 5], ['3c', 5], ['3d', 10]] as const) {
      const found = card(suffix);
      if (found.kind !== 'rubric' || found.rubric.system !== 'language-points') throw new Error('Expected complete pool');
      expect(found.rubric.count).toBe(count);
      expect(found.rubric.groups).toHaveLength(count);
      const scores: LanguageScores = {};
      for (const group of found.rubric.groups) {
        scores[`language:group:${group.id}`] = 1;
        for (const row of group.rows) scores[`language:row:${group.id}:${row.id}`] = 1;
      }
      expect(languagePointsMarks(found.rubric, scores)).toBe(found.totalMarks);
      expect(found.answerLanguageRule).toBeUndefined();
    }
    const links = card('1a-1');
    if (links.kind !== 'rubric' || links.rubric.system !== 'language-points') throw new Error('Expected links');
    expect(links.rubric.groups.map(group => group.rows[0].text)).toEqual(['3', '8', '5', '2', '9', '7']);
    const pairs = card('3c');
    if (pairs.kind !== 'rubric' || pairs.rubric.system !== 'language-points') throw new Error('Expected pairs');
    expect(pairs.rubric.groups.map(group => group.rows.map(row => row.marks))).toEqual(Array(5).fill([1, 1]));
    expect(card('2c-2').questionText).toContain('_____________り');
    expect(card('3d').questionText).toContain('(vii)');
  });

  it('preserves exact table cells and product-specific choices', () => {
    expect(point('2a-1').taskGroups?.map(group => group.marks)).toEqual([4, 4]);
    expect(point('2a-1').rows.map(row => row.marks)).toEqual([1, 2, 1, 1, 2, 1]);
    expect(point('2a-4').rows.map(row => row.marks)).toEqual([1, 1, 1, 1]);
    const attainable = [...new Set([0, ...[0.5, 1].map(first => 2 * first), ...[0.5, 1].flatMap(first => [0.5, 1].map(second => 2 * first + second))])].sort((a, b) => a - b);
    expect(point('1b-2').rows[0]).toMatchObject({ kind: 'criterion', marks: 3, permittedMarks: attainable });
    expect(attainable).toEqual([0, 1, 1.5, 2, 2.5, 3]);
    for (const score of attainable) expect(marksClaimed(point('1b-2'), { 'r-1': score }, {})).toBe(score);
    for (const invalid of [0.5, 0.75, 4]) expect(marksClaimed(point('1b-2'), { 'r-1': invalid }, {})).toBe(0);
    expect(point('1b-2').answerLanguageRule).toBeUndefined();
    expect(point('1b-2').rows[0].contextNote).toContain('Half marks if answered in Japanese');
    expect(point('1b-2').rows[0].contextNote).toContain('do not halve the final total again');
    const manual = review.cards.find(card => card.id === 'ja-2020-hl-1b-2')!.sourceEvidence.manualLanguageCalculation!;
    expect(manual).toMatchObject({ penalizedLanguage: 'Japanese', schemePages: [8] });
    expect(review.selectors.some(selector => selector.document === 'scheme' && selector.page === 8 && selector.text === manual.sourceText)).toBe(true);
    expect(point('1b-2').rows[0].contextNote).toContain('Do not combine reasons across box and bag');
    expect(point('1b-2').rows[0].verbatim).toContain('Gift bag');
    expect(point('1b-3-ii').rows[0]).toMatchObject({ verbatim: 'Children’s birthday party', marks: 2 });
    const table = point('la');
    expect(table.taskGroups).toHaveLength(12);
    expect(table.rows).toHaveLength(13);
    expect(table.taskGroups?.map(group => group.marks)).toEqual([1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2]);
    expect(table.taskGroups?.flatMap(group => group.rowIds)).toEqual(table.rows.map(row => row.id));
    expect(table.rows[6]).toMatchObject({ kind: 'anyN', group: { claimMax: 2, options: ['Ski', 'no snow/skiing in Philippines', 'snow is beautiful'] } });
    expect(table.rows.slice(-2).map(row => row.verbatim)).toEqual(['Forgot/Lost passport', 'on shinkansen']);
  });

  it('retains the whole phone tariff, required exit, descending pools and visible conflict', () => {
    expect(point('lc-2-iii').rows[0]).toMatchObject({ verbatim: '03-7285-1966', marks: 2 });
    expect(point('lc-2-iii').rows[0].parts).toBeUndefined();
    expect(point('lc-2-iii').rows[0].permittedMarks).toBeUndefined();
    expect(point('lc-2-ii').rows[0]).toMatchObject({ verbatim: 'Leave east exit', marks: 1 });
    expect(point('lc-2-ii').rows[1]).toMatchObject({ kind: 'anyN', group: { claimMax: 2, perOption: 1, options: ['3 minute walk', 'go left', 'beside ramen shop.'] } });
    for (const suffix of ['1a-2-i', '1a-3-ii', '3a-5', 'lb-iv', 'lb-vii', 'lb-viii', 'lc-2-i', 'ld-vi']) {
      expect(point(suffix).rows[0]).toMatchObject({ kind: 'anyN', group: { claimMax: 2, perOptionSteps: [2, 1] } });
    }
    expect(point('ld-v').questionText).toContain('two negative comments');
    expect(point('ld-v').rows[0]).toMatchObject({ kind: 'anyN', group: { claimMax: 3, perOption: 1 } });
    expect(point('ld-v').rows[0].contextNote).toContain('conflicting request remains visible');
    expect(census.sourceDiscrepancies.some(issue => JSON.stringify(issue.taskKey) === JSON.stringify(['LD', null, null, 'v']))).toBe(true);
  });

  it('binds 44 automatic and one manual source-local language rule, plus three extraneous rules', () => {
    const language = cards.filter(card => card.answerLanguageRule);
    expect(language).toHaveLength(44);
    expect(language.filter(card => card.answerLanguageRule!.penalizedLanguage === 'Japanese')).toHaveLength(38);
    expect(language.filter(card => card.answerLanguageRule!.penalizedLanguage === 'English')).toHaveLength(6);
    for (const found of language) {
      const rule = found.answerLanguageRule!;
      expect(rule.otherLanguageMultiplier).toBe(0.5);
      expect(review.selectors.some(selector => selector.document === 'scheme' && rule.schemePages.includes(selector.page) && selector.text === rule.sourceText)).toBe(true);
      expect(rule.sourceText).toContain(`answered in ${rule.penalizedLanguage}`);
    }
    for (const suffix of ['1a-1', '1a-2-i', '2a-1', '2b-1', '2b-2', '2c-1', '2c-2', '3c', '3d', '4', '5']) expect(card(suffix).answerLanguageRule).toBeUndefined();
    expect(point('2a-4').answerLanguageRule).toMatchObject({ schemePages: [9], penalizedLanguage: 'Japanese' });
    const extraneous = cards.filter(card => card.extraneousMaterialRule);
    expect(extraneous.map(card => card.id)).toEqual(['i', 'ii', 'iii'].map(roman => `ja-2020-hl-2a-2-${roman}`));
    for (const found of extraneous) expect(found.extraneousMaterialRule).toMatchObject({ multiplier: 0.5, schemePages: [8] });
  });

  it('applies the distinct 40/60 writing allocations and both exact expression thresholds', () => {
    expect(writing('4').criteria.map(criterion => criterion.maxMarks)).toEqual([9, 9, 1, 1, 20]);
    expect(writing('5').criteria.map(criterion => criterion.maxMarks)).toEqual([6, 6, 6, 6, 4, 2, 30]);
    for (const [suffix, total, normal, lower, threshold, length] of [['4', 40, 20, 15, 10, 150], ['5', 60, 30, 20, 15, 200]] as const) {
      const rubric = writing(suffix);
      const scores: LanguageScores = Object.fromEntries(rubric.criteria.map(criterion => [`language:${criterion.id}`, criterion.maxMarks]));
      scores['language:length:characters'] = length;
      expect(languageWritingMarks(rubric, scores)).toBe(total);
      scores['language:length:characters'] = length - 1;
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(lower);
      scores['language:length:characters'] = 320;
      for (const criterion of rubric.criteria.filter(criterion => criterion.id !== 'expression')) scores[`language:${criterion.id}`] = 0;
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(lower);
      const first = rubric.criteria[0];
      const second = rubric.criteria[1];
      scores[`language:${first.id}`] = first.maxMarks;
      scores[`language:${second.id}`] = threshold - first.maxMarks;
      if (suffix === '5') {
        scores[`language:${second.id}`] = second.maxMarks;
        scores['language:heading-3'] = threshold - 12;
      }
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(lower);
      scores[suffix === '5' ? 'language:heading-3' : `language:${second.id}`] += 1;
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(normal);
    }
    expect(card('4').questionText).toContain('(a) OR (b)');
    expect(card('5').questionText).toContain('ANY 4');
    expect(card('5').questionText).toContain('320 Japanese characters');
  });

  it('retains all 26 written and four listening Atlas anchors and source crops', () => {
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(11);
    const tags = ['japanese.json', 'japanese-written-2019-2022.json'].flatMap(file => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/topic-tags/tags/${file}`), 'utf8')));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      expect(task.paperPages, runtime.id).toContain(group.pP);
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2020 && paper.fileid === task.atlas.fileid);
      expect(tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber).primary, runtime.id).toBe(runtime.topicId);
      expect(sidecar.band).toEqual([1, 20]);
    }
    expect(map('LC058ALP000BV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 26 }, (_, i) => String(i + 1)));
    expect(map('LC058ALPA00BV.pdf').q.map(question => question.n)).toEqual(['1', '2', '3', '4']);
  });
});

