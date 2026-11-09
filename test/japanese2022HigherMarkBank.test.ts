import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as higher } from '../components/MarkBank/cards/japanese/higher';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import rawCards from '../components/MarkBank/cards/japanese/reviewed.json';
import aliases from '../components/MarkBank/cards/japanese/aliases.json';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import census from '../scripts/markbank/authoring/reviews/japanese-2022-hl-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2022-hl.json';
import resolvedExclusions from '../scripts/markbank/authoring/reviews/japanese-2022-hl-resolved-exclusions.json';
import activeExclusions from '../scripts/markbank/authoring/exclusions/japanese.json';
import { tariffReconciles } from '../types/markBank';
import { languageCriterionValue, languagePointsMarks, languageWritingMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = higher.filter(card => card.year === 2022);
const idFor = (key: (string | number | null)[]) => `ja-2022-hl-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2022-hl-${suffix}`)!;
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
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2022/${fileid}.json`), 'utf8'));

describe('Japanese 2022 Higher independent source review', () => {
  it('covers all 66 independently counted tasks and the published 120/100/80 tariffs', () => {
    expect(cards).toHaveLength(66);
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
    expect(rawCards.filter(card => !originalIds.includes(card.id))).toHaveLength(1179);
    expect(live.size).toBe(600 + 1179 - 391);
    expect(originalIds.filter(id => id.startsWith('ja-2022-hl-'))).toHaveLength(67);
    expect(cards.filter(card => originalIds.includes(card.id))).toHaveLength(24);
    expect(cards.filter(card => !originalIds.includes(card.id))).toHaveLength(42);
  });

  it('binds exactly 43 original fragment aliases to seven complete source tasks', () => {
    const expected = Object.fromEntries(review.consolidations.flatMap(entry => entry.legacyIds.map(id => [id, entry.canonicalId])));
    const sittingAliases = Object.fromEntries(Object.entries(aliases).filter(([id]) => id.startsWith('ja-2022-hl-')));
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
    expect(activeExclusions.filter(entry => entry.ref.startsWith('2022 HL'))).toEqual([]);
    expect(resolvedExclusions.resolved).toHaveLength(44);
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

  it('retains every finite printed option with the original quota', () => {
    expect(point('1a-1').rows).toHaveLength(6);
    for (const [suffix, count, available] of [['2b-1', 5, 6], ['2b-2', 5, 6], ['2c-1', 5, 6], ['2c-2', 5, 6], ['3c', 5, 6], ['3d', 10, 12]] as const) {
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
  });

  it('binds only the printed language and extraneous-material conditions', () => {
    const language = cards.filter(card => card.answerLanguageRule);
    expect(language).toHaveLength(58);
    expect(language.filter(card => card.answerLanguageRule!.penalizedLanguage === 'Japanese')).toHaveLength(50);
    expect(language.filter(card => card.answerLanguageRule!.penalizedLanguage === 'English').map(card => card.id).sort()).toEqual([
      '2a-2-i', '2a-2-ii', '2a-2-iii', '2a-2-iv', '3b-1', '3b-2', '3b-3', '3b-4',
    ].map(suffix => `ja-2022-hl-${suffix}`).sort());
    for (const found of language) {
      const rule = found.answerLanguageRule!;
      expect(rule.otherLanguageMultiplier).toBe(0.5);
      expect(rule.sourceText).toContain(`answered in ${rule.penalizedLanguage}`);
      expect(review.selectors.some(selector => selector.document === 'scheme' && rule.schemePages.includes(selector.page) && selector.text === rule.sourceText)).toBe(true);
    }
    const extraneous = cards.filter(card => card.extraneousMaterialRule);
    expect(extraneous.map(card => card.id).sort()).toEqual(['i', 'ii', 'iii', 'iv'].map(roman => `ja-2022-hl-2a-2-${roman}`).sort());
    for (const found of extraneous) {
      expect(found.extraneousMaterialRule).toMatchObject({ multiplier: 0.5, schemePages: [8] });
      expect(found.extraneousMaterialRule!.sourceText).toBe(found.answerLanguageRule!.sourceText);
      expect(found.extraneousMaterialRule!.sourceText).toContain('strong evidence of extraneous material');
    }
    expect(card('4').answerLanguageRule).toBeUndefined();
    expect(card('5').extraneousMaterialRule).toBeUndefined();
  });

  it('retains complete tables and the actual local row tariffs despite contradictory headings', () => {
    expect(point('1a-1').rows.map(row => row.verbatim)).toEqual(['6', '3', '8', '7', '4', '5']);
    expect(point('1a-1').rows[0].contextNote).toContain('website prints 1–10');
    expect(point('1a-6').rows.map(row => row.kind === 'anyN' ? row.group.perOption : row.marks)).toEqual([1, 1, 2, 1, 1, 1, 1]);
    expect(point('1a-6').taskGroups?.map(group => group.rowIds.length)).toEqual([2, 1, 2, 2]);
    expect(point('1a-6').taskGroups?.map(group => group.marks)).toEqual([2, 2, 2, 2]);
    expect(point('1a-6').taskGroups?.flatMap(group => group.rowIds)).toEqual(point('1a-6').rows.map(row => row.id));
    expect(point('2a-1').totalMarks).toBe(9);
    const opening = point('2a-3-ii').rows[0];
    expect(opening).toMatchObject({ kind: 'anyN', group: { claimMax: 2, options: ['7am', '9pm'], perOptionSteps: [2, 1] } });
    expect(point('2a-4').rows.map(row => row.marks)).toEqual([2, 2]);
    expect(['3b-1', '3b-2', '3b-3', '3b-4'].map(suffix => card(suffix).totalMarks)).toEqual([1, 1, 2, 2]);
    expect(point('3b-1').rows[0].contextNote).toContain('1 + 1 + 2 + 2 = 6');
    expect(cards.filter(card => ['3A', '3B', '3C', '3D'].some(section => card.questionRef.includes(`Section ${section}`))).reduce((total, card) => total + card.totalMarks, 0)).toBe(38);
  });

  it('keeps profiles, paired weather, partial teacher credit and constrained ingredients intact', () => {
    expect(['la-1', 'la-2', 'la-3'].map(suffix => point(suffix).totalMarks)).toEqual([7, 7, 7]);
    expect(point('la-1').rows).toHaveLength(6);
    expect(point('la-2').rows[0]).toMatchObject({ kind: 'anyN', group: { options: ['School Japan day', 'Calligraphy', 'yukata'], claimMax: 2 } });
    expect(point('la-3').rows.map(row => row.kind === 'anyN' ? row.group.claimMax : row.marks)).toEqual([2, 1, 1, 1, 1, 1]);
    expect(point('lb-2-i').rows.map(row => row.kind === 'anyN' ? row.group.claimMax : row.marks)).toEqual([2, 2]);
    expect(point('lb-1-v').rows[0]).toMatchObject({ verbatim: '0120-923-915', marks: 2 });
    expect(point('lb-1-v').rows[0].parts).toBeUndefined();
    expect(point('lc-3-i').rows[0]).toMatchObject({ marks: 2, permittedMarks: [0, 1, 2] });
    expect(point('lc-3-i').rows[0].verbatim).toContain('teacher 1 mark');
    expect(point('ld-1-ii').rows[0]).toMatchObject({ marks: 3, permittedMarks: [0, 1, 2, 3] });
    expect(point('ld-1-ii').rows[0].contextNote).toContain('three ingredient examples alone therefore earn at most 2');
    expect(point('ld-2-i').rows.map(row => row.marks)).toEqual([1, 1]);
    expect(point('ld-2-ii').rows.map(row => row.marks)).toEqual([1, 1]);
    expect(point('ld-2-iii').rows[0]).toMatchObject({ kind: 'anyN', group: { claimMax: 2, perOptionSteps: [2, 1] } });
  });

  it('binds both nested directions to exact paper labels despite the shifted scheme numbering', () => {
    const nested = census.tasks.filter(task => 'paperRef' in task);
    expect(nested).toHaveLength(2);
    for (const task of nested) expect(cards.find(card => card.id === idFor(task.key))!.questionRef).toBe(task.paperRef);
    expect(card('ld-1-a-iii').questionRef).toBe('2022 HL Section LD Q1(iii)(a)');
    expect(card('ld-1-b-iii').questionRef).toBe('2022 HL Section LD Q1(iii)(b)');
    expect(card('ld-1-a-iii').totalMarks).toBe(1);
    expect(card('ld-1-b-iii').totalMarks).toBe(3);
    expect(card('ld-1-iv').questionText).toContain('What time do they arrange to meet?');
  });

  it('keeps both offered writing tasks and the exact common expression cap', () => {
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
    expect(writing('4').criteria.map(criterion => criterion.maxMarks)).toEqual([11, 11, 1, 1, 1, 25]);
    expect(writing('5').criteria.map(criterion => criterion.maxMarks)).toEqual([5, 1, 5, 1, 5, 1, 5, 1, 1, 25]);
    expect(card('5').questionText).toContain('The weather');
    expect(writing('5').markingGuideNote).toContain('weather last');
    expect(card('4').questionText).toContain('200 Japanese characters');
    expect(card('5').questionText).toContain('320 Japanese characters');
  });

  it('retains complete original figures and all existing Atlas identities', () => {
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(14);
    const tags = ['japanese.json', 'japanese-written-2019-2022.json'].flatMap(file => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/topic-tags/tags/${file}`), 'utf8')));
    for (const task of census.tasks) {
      const group = map(task.atlas.fileid).q.find(question => question.n === task.atlas.questionNumber)!;
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      expect(task.paperPages, runtime.id).toContain(group.pP);
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2022 && paper.fileid === task.atlas.fileid);
      expect(tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber).primary, runtime.id).toBe(runtime.topicId);
    }
    expect(map('LC058ALPA00BV.pdf').q.find(question => question.n === '4')!.region.map(region => region.p)).toEqual([5, 6]);
    expect(map('LC058ALP000BV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 28 }, (_, i) => String(i + 1)));
  });
});
