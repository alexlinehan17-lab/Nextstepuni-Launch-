import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as higher } from '../components/MarkBank/cards/japanese/higher';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import rawCards from '../components/MarkBank/cards/japanese/reviewed.json';
import aliases from '../components/MarkBank/cards/japanese/aliases.json';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import census from '../scripts/markbank/authoring/reviews/japanese-2019-hl-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2019-hl.json';
import { tariffReconciles } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
import { languageCriterionValue, languagePointsMarks, languageWritingMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = higher.filter(card => card.year === 2019);
const idFor = (key: (string | number | null)[]) => `ja-2019-hl-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2019-hl-${suffix}`)!;
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
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2019/${fileid}.json`), 'utf8'));

describe('Japanese 2019 Higher independent source review', () => {
  it('covers all 69 independent tasks and every physical source page', () => {
    expect(cards).toHaveLength(69);
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

  it('adds 69 new tasks while keeping the frozen 600 identities and original files', () => {
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
    expect(originalIds.some(id => id.startsWith('ja-2019-'))).toBe(false);
    expect(review.consolidations).toEqual([]);
    expect(Object.keys(aliases)).toHaveLength(391);
    expect(rawCards.filter(card => !originalIds.includes(card.id))).toHaveLength(1288);
    expect(live.size).toBe(600 + 1288 - 391);
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
    expect(links.rubric.groups.map(group => group.rows[0].text)).toEqual(['8', '7', '10', '3', '6', '9']);
    const pairs = card('3c');
    if (pairs.kind !== 'rubric' || pairs.rubric.system !== 'language-points') throw new Error('Expected pairs');
    expect(pairs.rubric.groups.map(group => group.rows.map(row => row.marks))).toEqual(Array(5).fill([1, 1]));
    expect(card('2c-2').questionText).toContain('__________________ら');
    expect(card('3d').questionText).toContain('(vii)');
  });

  it('keeps printed examples unpriced, exact components and sister-only partial credit', () => {
    expect(point('2a-1').taskGroups?.map(group => group.marks)).toEqual([4, 4]);
    expect(point('2a-1').rows.map(row => row.marks)).toEqual([1, 1, null, 1, 1, null]);
    expect(point('2a-1').rows.map(row => row.verbatim).join(' ')).not.toContain('Boys');
    expect(point('2a-1').rows.map(row => row.verbatim).join(' ')).not.toContain('Kyoto');
    expect(point('2a-1').rows[5].group?.options).toEqual(['sailor style', 'ribbon', 'white top', 'navy top', 'navy skirt']);
    expect(point('2a-4').rows).toHaveLength(5);
    expect(point('2a-4').rows.every(row => row.marks === 1)).toBe(true);
    expect(point('1a-5-i').rows.map(row => row.marks)).toEqual([2, 2]);
    expect(point('1b-2-i').rows[0]).toMatchObject({ verbatim: 'Her older sister', marks: 2, permittedMarks: [0, 1, 2] });
    expect(point('1b-2-i').rows[0].contextNote).toContain('sister = 1 mark');
    expect(point('1b-1-i').rows.map(row => row.verbatim)).toEqual(['He lost sight', 'in left eye']);
    expect(point('1b-2-ii').rows.map(row => row.verbatim)).toEqual(['Bronze medal', 'in Rio (Paralympics)']);
    expect(point('3a-1-ii').questionText).toContain('write a diary');
    expect(census.sourceDiscrepancies).toHaveLength(3);
  });

  it('supports complete listening table and mutually exclusive generic partials without double halving', () => {
    const table = point('la');
    expect(table.taskGroups).toHaveLength(12);
    expect(table.rows).toHaveLength(14);
    expect(table.taskGroups?.map(group => group.marks)).toEqual([1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]);
    expect(table.taskGroups?.flatMap(group => group.rowIds)).toEqual(table.rows.map(row => row.id));
    expect(table.rows[11].verbatim).toBe('From Monday 1 mark to Wednesday 1 mark (3 times a week = 1 mark)');
    const manual = point('ld-i');
    expect(manual.rows).toHaveLength(1);
    expect(manual.rows[0].contextNote).toContain('Languages = 1 mark');
    for (const [found, row] of [[table, table.rows[11]], [manual, manual.rows[0]]] as const) {
      const attainable = [0, 0.5, 1, 1.5, 2];
      expect(row.permittedMarks).toEqual(attainable);
      expect(row.contextNote).toContain('never both');
      expect(found.answerLanguageRule).toBeUndefined();
      for (const score of attainable) expect(marksClaimed(found, { [row.id!]: score }, {})).toBe(score);
      for (const invalid of [0.25, 0.75, 2.5, 3]) expect(marksClaimed(found, { [row.id!]: invalid }, {})).toBe(0);
    }
    const full = Object.fromEntries(table.rows.map(row => [row.id!, row.marks!]));
    expect(marksClaimed(table, full)).toBe(18);
    expect(marksClaimed(table, Object.fromEntries(table.rows.map(row => [row.id!, row.marks! / 2])))).toBe(9);
    expect(marksClaimed(table, { ...full, 'r-12': 1.5 })).toBe(17.5);
    expect(marksClaimed(table, { ...full, 'r-12': 0.5 })).toBe(16.5);
    for (const row of table.rows) expect(row.contextNote).toContain('Do not halve it again');
  });

  it('retains whole phone, every required direction, descending pools and source-specific zero/partial guidance', () => {
    expect(point('lb-1-v').rows[0]).toMatchObject({ verbatim: '03-3562-9704', marks: 3 });
    expect(point('lb-1-v').rows[0].parts).toBeUndefined();
    expect(point('lb-1-v').rows[0].permittedMarks).toBeUndefined();
    expect(point('lb-1-iii').rows.map(row => row.verbatim)).toEqual(['(Go out of) the north exit (of station)', 'go straight about 5 minutes', 'it’s at the end of the road']);
    for (const suffix of ['2a-3-ii', 'lb-2-i', 'lb-2-iii', 'lc-2-ii']) {
      expect(point(suffix).rows[0]).toMatchObject({ kind: 'anyN', group: { claimMax: 2, perOptionSteps: [2, 1] } });
    }
    expect(point('lc-1-i').rows[0].contextNote).toContain('Feels sick = 0 marks');
    expect(point('lc-1-ii').rows[0].group).toEqual({ claimMax: 2, perOption: 1, options: ['At a yakiniku', 'restaurant', 'out with a friend'] });
    expect(point('lc-1-ii').rows[0].contextNote).toContain('(out with a friend 1 mark)');
    expect(marksClaimed(point('lc-1-ii'), {}, { 'r-1': [0, 1, 2] })).toBe(2);
    expect(point('ld-vii').rows.map(row => row.marks)).toEqual([1, 1]);
  });

  it('binds only the 31 printed Japanese conditions, with two manual calculations and three extraneous rules', () => {
    const language = cards.filter(card => card.answerLanguageRule);
    expect(language).toHaveLength(29);
    for (const found of language) {
      const rule = found.answerLanguageRule!;
      expect(rule.otherLanguageMultiplier).toBe(0.5);
      expect(rule.penalizedLanguage).toBe('Japanese');
      expect(review.selectors.some(selector => selector.document === 'scheme' && rule.schemePages.includes(selector.page) && selector.text === rule.sourceText)).toBe(true);
      expect(rule.sourceText).toContain('answered in Japanese');
    }
    const manual = review.cards.filter(card => card.sourceEvidence.manualLanguageCalculation);
    expect(manual.map(card => card.id)).toEqual(['ja-2019-hl-la', 'ja-2019-hl-ld-i']);
    for (const found of manual) {
      const rule = found.sourceEvidence.manualLanguageCalculation!;
      expect(rule).toMatchObject({ penalizedLanguage: 'Japanese', schemePages: [4] });
      expect(review.selectors.some(selector => selector.document === 'scheme' && selector.page === 4 && selector.text === rule.sourceText)).toBe(true);
    }
    for (const found of cards.filter(card => !card.id.startsWith('ja-2019-hl-l') && !card.id.startsWith('ja-2019-hl-1b-'))) expect(found.answerLanguageRule, found.id).toBeUndefined();
    const extraneous = cards.filter(card => card.extraneousMaterialRule);
    expect(extraneous.map(card => card.id)).toEqual(['i', 'ii', 'iii'].map(roman => `ja-2019-hl-2a-2-${roman}`));
    for (const found of extraneous) {
      expect(found.extraneousMaterialRule).toMatchObject({ multiplier: 0.5, schemePages: [8] });
      expect(found.answerLanguageRule).toBeUndefined();
    }
  });

  it('preserves each roman-then-letter printed listening reference and its distinct identity', () => {
    for (const roman of ['ii', 'v']) for (const letter of ['a', 'b']) {
      const found = point(`ld-${letter}-${roman}`);
      expect(found.questionRef).toBe(`2019 HL Section LD(${roman})(${letter})`);
      expect(found.totalMarks).toBe(2);
      const task = census.tasks.find(task => idFor(task.key) === found.id)!;
      expect(task.paperRef).toBe(found.questionRef);
      expect(task.key).toEqual(['LD', null, letter, roman]);
    }
  });

  it('applies the distinct 40/60 writing allocations and both exact expression thresholds', () => {
    expect(writing('4').criteria.map(criterion => criterion.maxMarks)).toEqual([9, 9, 1, 1, 20]);
    expect(writing('5').criteria.map(criterion => criterion.maxMarks)).toEqual([6, 6, 6, 6, 4, 1, 1, 30]);
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

  it('retains all 28 written and four listening Atlas anchors and source crops', () => {
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(11);
    const tags = ['japanese.json', 'japanese-written-2019-2022.json'].flatMap(file => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/topic-tags/tags/${file}`), 'utf8')));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      expect(task.paperPages, runtime.id).toContain(group.pP);
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2019 && paper.fileid === task.atlas.fileid);
      expect(tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber).primary, runtime.id).toBe(runtime.topicId);
      expect(sidecar.band).toEqual([1, 20]);
    }
    expect(map('LC058ALP000BV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 28 }, (_, i) => String(i + 1)));
    expect(map('LC058ALPA00BV.pdf').q.map(question => question.n)).toEqual(['1', '2', '3', '4']);
  });
});

