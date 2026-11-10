import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as higher } from '../components/MarkBank/cards/japanese/higher';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import rawCards from '../components/MarkBank/cards/japanese/reviewed.json';
import aliases from '../components/MarkBank/cards/japanese/aliases.json';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import census from '../scripts/markbank/authoring/reviews/japanese-2021-hl-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2021-hl.json';
import resolvedExclusions from '../scripts/markbank/authoring/reviews/japanese-2021-hl-resolved-exclusions.json';
import activeExclusions from '../scripts/markbank/authoring/exclusions/japanese.json';
import { tariffReconciles } from '../types/markBank';
import { languageCriterionValue, languagePointsMarks, languageWritingMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = higher.filter(card => card.year === 2021);
const idFor = (key: (string | number | null)[]) => `ja-2021-hl-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2021-hl-${suffix}`)!;
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
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2021/${fileid}.json`), 'utf8'));

describe('Japanese 2021 Higher independent source review', () => {
  it('covers all 58 independently counted tasks and the published 120/100/80 tariffs', () => {
    expect(cards).toHaveLength(58);
    expect(cards.map(card => card.id).sort()).toEqual(census.tasks.map(task => idFor(task.key)).sort());
    for (const task of census.tasks) {
      const found = cards.find(card => card.id === idFor(task.key))!;
      expect(found.totalMarks, found.id).toBe(task.marks);
      expect(tariffReconciles(found), found.id).toBe(true);
      const raw = rawCards.find(card => card.id === found.id)!;
      expect(raw.sourceEvidence).toMatchObject({ component: task.component, paperPages: task.paperPages, schemePages: task.schemePages });
    }
    expect(census.checksums).toEqual({ reading: 120, writing: 100, listening: 80, total: 300 });
    expect(cards.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(300);
    expect(Object.values(census.pageRoles).map(pages => Object.keys(pages).length)).toEqual([20, 8, 20]);
    expect(review.sources.map(source => ({ component: source.document, path: source.path, sha256: source.sha256 }))).toEqual(census.sources);
    for (const source of review.sources) expect(source.pagesReviewed).toEqual(Object.keys(census.pageRoles[source.document as keyof typeof census.pageRoles]).map(Number));
  });

  it('preserves the exact original literal files and all 600 original identities', () => {
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
    expect(rawCards.filter(card => !originalIds.includes(card.id))).toHaveLength(1379);
    expect(live.size).toBe(600 + 1379 - 391);
    expect(originalIds.filter(id => id.startsWith('ja-2021-hl-'))).toHaveLength(69);
    expect(cards.filter(card => originalIds.includes(card.id))).toHaveLength(26);
    expect(cards.filter(card => !originalIds.includes(card.id))).toHaveLength(32);
  });

  it('binds exactly 43 original fragment aliases to seven complete source tasks', () => {
    const expected = Object.fromEntries(review.consolidations.flatMap(entry => entry.legacyIds.map(id => [id, entry.canonicalId])));
    const sittingAliases = Object.fromEntries(Object.entries(aliases).filter(([id]) => id.startsWith('ja-2021-hl-')));
    expect(sittingAliases).toEqual(expected);
    expect(Object.keys(sittingAliases)).toHaveLength(43);
    expect(new Set(Object.values(sittingAliases)).size).toBe(7);
    const live = new Set(cards.map(card => card.id));
    for (const [old, target] of Object.entries(sittingAliases)) {
      expect(CARD_ID_ALIASES[old]).toBe(target);
      expect(old.startsWith(`${target}-`)).toBe(true);
      expect(live.has(old)).toBe(false);
      expect(live.has(target)).toBe(true);
      expect(target in aliases).toBe(false);
    }
    for (const entry of review.consolidations) {
      expect(idFor(entry.taskKey)).toBe(entry.canonicalId);
      for (const [document, evidence] of [['paper', entry.paperEvidence], ['scheme', entry.schemeEvidence]] as const) {
        expect(review.selectors.some(selector => selector.document === document && selector.page === evidence.page && selector.text === evidence.text)).toBe(true);
      }
    }
  });

  it('resolves every superseded exclusion to real source-reviewed tasks', () => {
    expect(activeExclusions.filter(entry => entry.ref.startsWith('2021 HL'))).toEqual([]);
    expect(resolvedExclusions.resolved).toHaveLength(42);
    for (const entry of resolvedExclusions.resolved) {
      expect(entry.previousExclusion.evidence).toBeTruthy();
      expect(entry.reviewedCardIds.length).toBeGreaterThan(0);
      for (const id of entry.reviewedCardIds) {
        const found = cards.find(card => card.id === id)!;
        expect(found, entry.previousExclusion.ref).toBeDefined();
        if (id.includes('-l')) expect(found.audioMaterial).toBeDefined();
      }
    }
  });

  it('keeps seven finite pools complete and enforces the original choice quotas', () => {
    for (const [suffix, count, available] of [['1a-1', 5, 6], ['2b-1', 5, 6], ['2b-2', 5, 6], ['2c-1', 5, 6], ['2c-2', 5, 6], ['3c', 5, 6], ['3d', 10, 12]] as const) {
      const found = card(suffix);
      if (found.kind !== 'rubric' || found.rubric.system !== 'language-points') throw new Error('Expected complete pool');
      expect(found.rubric.count).toBe(count);
      expect(found.rubric.groups).toHaveLength(available);
      const scores: LanguageScores = {};
      for (const group of found.rubric.groups) {
        scores[`language:group:${group.id}`] = 1;
        for (const row of group.rows) scores[`language:row:${group.id}:${row.id}`] = 1;
      }
      expect(languagePointsMarks(found.rubric, scores)).toBe(found.totalMarks);
    }
    const links = card('1a-1');
    if (links.kind !== 'rubric' || links.rubric.system !== 'language-points') throw new Error('Expected links pool');
    expect(links.rubric.groups.map(group => group.rows[0].text)).toEqual(['2', '6', '8', '4', '1', '7']);
    expect(links.rubric.markingGuideNote).toContain('paper presents six links');
    const negative = card('2c-1');
    if (negative.kind !== 'rubric' || negative.rubric.system !== 'language-points') throw new Error('Expected grammar pool');
    for (const alternative of ['たいへんじゃなかったです', 'たいへんじゃありませんでした', 'たいへんではありませんでした']) {
      expect(negative.rubric.groups[2].rows[0].text).toContain(alternative);
    }
    const pairs = card('3c');
    if (pairs.kind !== 'rubric' || pairs.rubric.system !== 'language-points') throw new Error('Expected paired pool');
    expect(pairs.rubric.groups.map(group => group.rows.map(row => row.marks))).toEqual(Array(6).fill([1, 1]));
    expect(pairs.questionRef).toBe('2021 HL Section 3C');
    expect(card('3d').questionRef).toBe('2021 HL Section 3D');
  });

  it('preserves the complete required tables and every printed cell tariff', () => {
    expect(point('1a-2').totalMarks).toBe(8);
    expect(point('1a-2').taskGroups?.map(group => group.marks)).toEqual([4, 4]);
    expect(point('1a-2').rows.map(row => row.kind === 'anyN' ? row.group.claimMax : row.marks)).toEqual([1, 1, 2, 1, 1, 2]);
    expect(point('1a-3').rows.map(row => row.verbatim)).toEqual(['Converse', 'sneakers']);
    expect(point('2a-1').taskGroups?.map(group => group.marks)).toEqual([5, 5]);
    expect(point('2a-1').rows[0]).toMatchObject({ verbatim: 'Ohio/ Cincinnati', marks: 1 });
    expect(point('2a-1').rows[1]).toMatchObject({ verbatim: 'Study Japanese', marks: 2 });
    expect(point('2a-1').rows.slice(4, 6).map(row => row.verbatim)).toEqual(['Resident', 'assistant']);
    expect(point('2a-4').rows.map(row => row.marks)).toEqual([1, 1, 1, 1, 1]);
    const table = point('la');
    expect(table.totalMarks).toBe(21);
    expect(table.taskGroups).toHaveLength(12);
    expect(table.rows).toHaveLength(18);
    expect(table.taskGroups?.map(group => group.marks)).toEqual([1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2]);
    expect(table.taskGroups?.flatMap(group => group.rowIds)).toEqual(table.rows.map(row => row.id));
    for (const name of ['Maria', 'Max', 'Sophie']) expect(table.questionText).toContain(name);
    expect(table.rows[15]).toMatchObject({ kind: 'criterion', marks: 2, permittedMarks: [0, 1, 2] });
    expect(table.rows[15].verbatim).toContain('Brother lives in Japan');
    expect(table.rows[15].contextNote).toContain('alternative earns only 1 mark');
    expect(point('lb-2').totalMarks).toBe(8);
    expect(point('lb-2').rows.map(row => row.kind === 'anyN' ? row.group.claimMax : row.marks)).toEqual([2, 2, 2, 2]);
    expect(point('lb-2').rows[2]).toMatchObject({ kind: 'anyN', group: { options: ['Sunny (Fine)', 'cooler than Saturday', 'am-windy', '29 degrees', 'pm- rain'] } });
  });

  it('retains the required route, descending alternatives and the whole-number phone', () => {
    expect(point('lb-1-ii').rows[0]).toMatchObject({ kind: 'anyN', group: { claimMax: 2, perOptionSteps: [2, 1] } });
    expect(point('lc-ii').rows[0]).toMatchObject({ kind: 'anyN', group: { claimMax: 3, perOptionSteps: [2, 1, 1] } });
    expect(point('lc-vi').rows[0]).toMatchObject({ verbatim: '03-4160-9725', marks: 3 });
    expect(point('lc-vi').rows[0].parts).toBeUndefined();
    expect(point('lc-vi').rows[0].permittedMarks).toBeUndefined();
    expect(point('lc-vii').rows[0]).toMatchObject({ verbatim: 'east exit', marks: 1 });
    expect(point('lc-vii').rows[1]).toMatchObject({ kind: 'anyN', group: { claimMax: 2, perOptionSteps: [2, 1], options: ['10-minute walk', '1st turn left', 'it’s on right', 'beside karaoke bar'] } });
    expect(point('ld-iii').rows.map(row => row.marks)).toEqual([2, 2]);
    expect(point('ld-iv').rows.map(row => row.marks)).toEqual([2, 2]);
    expect(point('ld-vi').rows[0]).toMatchObject({ kind: 'anyN', group: { claimMax: 2, perOptionSteps: [2, 1] } });
    expect(point('ld-vii').rows[0]).toMatchObject({ verbatim: 'Cat', marks: 1 });
    expect(point('ld-vii').rows[1]).toMatchObject({ kind: 'anyN', group: { claimMax: 2, perOption: 1, options: ['it’s selfish', 'it’s fat', 'it comes into his room'] } });
  });

  it('binds the exact language conditions and only three extraneous-material rules', () => {
    const language = cards.filter(card => card.answerLanguageRule);
    expect(language).toHaveLength(56);
    expect(language.filter(card => card.answerLanguageRule!.penalizedLanguage === 'Japanese')).toHaveLength(21);
    expect(language.filter(card => card.answerLanguageRule!.penalizedLanguage === undefined)).toHaveLength(35);
    for (const found of language) {
      const rule = found.answerLanguageRule!;
      expect(rule.otherLanguageMultiplier).toBe(0.5);
      expect(review.selectors.some(selector => selector.document === 'scheme' && rule.schemePages.includes(selector.page) && selector.text === rule.sourceText)).toBe(true);
      expect(rule.sourceText).toContain(rule.penalizedLanguage ? 'Japanese' : 'incorrect language');
    }
    for (const q of [1, 2, 3, 4]) {
      expect(point(`1b-${q}`).answerLanguageRule).toMatchObject({ schemePages: [7] });
      expect(point(`1b-${q}`).rows[0].contextNote).toBe('Part B: (9 marks) Half marks if marked in Japanese');
    }
    const extraneous = cards.filter(card => card.extraneousMaterialRule);
    expect(extraneous.map(card => card.id).sort()).toEqual(['i', 'ii', 'iii'].map(roman => `ja-2021-hl-2a-2-${roman}`).sort());
    for (const found of extraneous) {
      const rule = found.extraneousMaterialRule!;
      expect(rule).toMatchObject({ multiplier: 0.5, schemePages: [8] });
      expect(rule.sourceText).toContain('strong evidence of extraneous material');
      expect(review.selectors.some(selector => selector.document === 'scheme' && selector.page === 8 && selector.text === rule.sourceText)).toBe(true);
    }
    expect(card('4').answerLanguageRule).toBeUndefined();
    expect(card('5').extraneousMaterialRule).toBeUndefined();
  });

  it('keeps both writing alternatives and applies the exact common expression cap', () => {
    expect(census.candidateMaximum).toMatchObject({ written: 170, listening: 80, total: 250 });
    for (const suffix of ['4', '5']) {
      const rubric = writing(suffix);
      expect(card(suffix).questionText).toContain('Answer either Question 4 or Question 5.');
      const scores: LanguageScores = Object.fromEntries(rubric.criteria.map(criterion => [`language:${criterion.id}`, criterion.maxMarks]));
      scores['language:length:characters'] = 150;
      expect(languageWritingMarks(rubric, scores)).toBe(50);
      scores['language:length:characters'] = 149;
      expect(languageWritingMarks(rubric, scores)).toBe(44);
      scores['language:length:characters'] = 320;
      for (const criterion of rubric.criteria.filter(criterion => criterion.id !== 'expression')) scores[`language:${criterion.id}`] = 0;
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(19);
      const condition = rubric.criteria.find(criterion => criterion.id === 'expression')!.limits![0];
      expect(condition.when.any).toContainEqual({ length: 'characters', below: 150 });
      expect(condition.when.any.some(rule => 'criterionIds' in rule && rule.atMost === 13)).toBe(true);
    }
    expect(writing('4').criteria.map(criterion => criterion.maxMarks)).toEqual([7, 7, 7, 1, 1, 2, 25]);
    expect(writing('5').criteria.map(criterion => criterion.maxMarks)).toEqual([5, 5, 5, 5, 1, 1, 3, 25]);
    expect(card('4').questionText).toContain('200 Japanese characters');
    expect(card('5').questionText).toContain('320 Japanese characters');
    expect(card('5').questionText).toContain('Memories of your School');
    for (const suffix of ['(a)', '(b)', '(c)', '(iii)']) expect(card('4').questionText).toContain(suffix);
  });

  it('retains all original Atlas identities, source bounds and complete figures', () => {
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(13);
    const tags = ['japanese.json', 'japanese-written-2019-2022.json'].flatMap(file => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/topic-tags/tags/${file}`), 'utf8')));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      expect(task.paperPages, runtime.id).toContain(group.pP);
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2021 && paper.fileid === task.atlas.fileid);
      expect(tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber).primary, runtime.id).toBe(runtime.topicId);
      expect(sidecar.band).toEqual([1, 20]);
    }
    expect(map('LC058ALP000BV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 29 }, (_, i) => String(i + 1)));
    expect(map('LC058ALPA00BV.pdf').q.map(question => question.n)).toEqual(['1', '2', '3', '4']);
    expect(map('LC058ALP000BV.pdf').q.find(question => question.n === '29')!.label).toBe('Q5 · Essay on memories of your school');
  });
});
