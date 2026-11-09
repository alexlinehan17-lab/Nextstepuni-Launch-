import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as higher } from '../components/MarkBank/cards/japanese/higher';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import rawCards from '../components/MarkBank/cards/japanese/reviewed.json';
import aliases from '../components/MarkBank/cards/japanese/aliases.json';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import census from '../scripts/markbank/authoring/reviews/japanese-2025-hl-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2025-hl.json';
import resolvedExclusions from '../scripts/markbank/authoring/reviews/japanese-2025-hl-resolved-exclusions.json';
import activeExclusions from '../scripts/markbank/authoring/exclusions/japanese.json';
import { tariffReconciles } from '../types/markBank';
import { languageCriterionValue, languagePointsMarks, languageWritingMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = higher.filter(card => card.year === 2025);
const idFor = (key: (string | number | null)[]) => `ja-2025-hl-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2025-hl-${suffix}`)!;
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
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2025/${fileid}.json`), 'utf8'));

describe('Japanese 2025 Higher independent source review', () => {
  it('covers all 69 independently counted tasks and the published 120/100/80 tariffs', () => {
    expect(cards).toHaveLength(69);
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
    expect(Object.values(census.pageRoles).map(pages => Object.keys(pages).length)).toEqual([20, 8, 24]);
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
    expect(rawCards.filter(card => !originalIds.includes(card.id))).toHaveLength(501);
    expect(live.size).toBe(600 + 501 - 352);
    expect(cards.filter(card => originalIds.includes(card.id))).toHaveLength(29);
  });

  it('binds exactly 42 original fragment aliases to seven complete source tasks', () => {
    const expected = Object.fromEntries(review.consolidations.flatMap(entry => entry.legacyIds.map(id => [id, entry.canonicalId])));
    const sittingAliases = Object.fromEntries(Object.entries(aliases).filter(([id]) => id.startsWith('ja-2025-hl-')));
    expect(sittingAliases).toEqual(expected);
    expect(Object.keys(sittingAliases)).toHaveLength(42);
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
    expect(activeExclusions.filter(entry => entry.ref.startsWith('2025 HL'))).toEqual([]);
    expect(resolvedExclusions.resolved).toHaveLength(41);
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
    expect(point('1a-1').rows).toHaveLength(5);
    for (const suffix of ['2b-1', '2b-2', '2c-1', '2c-2']) {
      const row = point(suffix).rows[0];
      if (row.kind !== 'anyN') throw new Error('Expected choice pool');
      expect(row.group).toMatchObject({ claimMax: 5, perOption: 1 });
      expect(row.group.options).toHaveLength(6);
    }
    for (const [suffix, count, available] of [['3c', 5, 6], ['3d', 10, 12]] as const) {
      const found = card(suffix);
      if (found.kind !== 'rubric' || found.rubric.system !== 'language-points') throw new Error('Expected complete pool');
      expect(found.rubric.count).toBe(count);
      expect(found.rubric.groups).toHaveLength(available);
      const scores: LanguageScores = {};
      for (const group of found.rubric.groups) {
        scores[`language:group:${group.id}`] = 1;
        for (const row of group.rows) scores[`language:row:${group.id}:${row.id}`] = 1;
      }
      expect(languagePointsMarks(found.rubric, scores)).toBe(10);
    }
  });

  it('limits language and extraneous-material conditions to the printed scope', () => {
    const extraneous = ['2a-1-a', '2a-1-b', '2a-1-c', '2a-1-d', '3b-1', '3b-2', '3b-3', '3b-4'];
    expect(cards.filter(card => card.extraneousMaterialRule).map(card => card.id).sort()).toEqual(extraneous.map(suffix => `ja-2025-hl-${suffix}`).sort());
    for (const suffix of extraneous) {
      const found = point(suffix);
      const expectedPage = suffix.startsWith('2a') ? 8 : 11;
      expect(found.extraneousMaterialRule).toMatchObject({ multiplier: 0.5, schemePages: [expectedPage] });
      expect(found.extraneousMaterialRule!.sourceText).toContain('strong evidence of extraneous material');
      expect(found.answerLanguageRule!.sourceText).toContain('answered in English.');
      expect(found.answerLanguageRule!.penalizedLanguage).toBe('English');
      expect(review.selectors.some(selector => selector.document === 'scheme' && selector.page === expectedPage && selector.text === found.extraneousMaterialRule!.sourceText)).toBe(true);
    }
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(60);
    for (const suffix of ['2a-3', '2b-1', '2b-2', '2c-1', '2c-2', '3c', '3d', '4', '5']) expect(card(suffix).answerLanguageRule).toBeUndefined();
    expect(card('1b-3').answerLanguageRule!.schemePages).toEqual([7]);
    for (const found of cards.filter(card => card.answerLanguageRule && !card.extraneousMaterialRule)) expect(found.answerLanguageRule!.penalizedLanguage).toBe('Japanese');
    expect(card('la-1').answerLanguageRule!.sourceText).toBe('(1/2 marks if answered in Japanese, romaji or Japanese script)');
  });

  it('preserves separate published partial answers and non-additive alternatives', () => {
    expect(point('2a-1-b').rows[0]).toMatchObject({ marks: 2, permittedMarks: [0, 1, 2] });
    expect(point('2a-1-b').rows[0].verbatim).toContain('男の人二人 1 mark');
    expect(point('ld-3-a').rows[0]).toMatchObject({ marks: 3, permittedMarks: [0, 1, 2, 3] });
    expect(point('ld-3-a').rows[0].verbatim).toContain('any 2, 2 marks + 1 mark');
    expect(point('ld-3-a').rows[0].verbatim).toContain('no uniform 1 mark');
    expect(point('la-2').rows[1]).toMatchObject({ kind: 'point', marks: 2 });
    expect(point('la-2').rows[1].verbatim).toBe('Wednesdays from 2pm / Saturdays from 8:30 am');
    expect(point('la-3').rows[3]).toMatchObject({ kind: 'point', marks: 2, verbatim: 'easy / can watch new films for free.' });
    const directions = point('lb-1-e').rows;
    expect(directions[0]).toMatchObject({ marks: 1, verbatim: 'north exit' });
    expect(directions[1]).toMatchObject({ group: { claimMax: 2, perOptionSteps: [2, 1] } });
    expect(point('lb-1-d').rows[0]).toMatchObject({ group: { claimMax: 2, options: ['see the Tokyo night view /see the wonderful night view', 'Tokyo Tower', 'go to lounge'] } });
  });

  it('uses the distinct 2025 writing bands and lower-expression conditions', () => {
    for (const [suffix, content, maximum, lower, length] of [['4', 20, 20, 15, 150], ['5', 30, 30, 20, 200]] as const) {
      const rubric = writing(suffix);
      const scores: LanguageScores = Object.fromEntries(rubric.criteria.map(criterion => [`language:${criterion.id}`, criterion.maxMarks]));
      scores['language:length:characters'] = 320;
      expect(languageWritingMarks(rubric, scores)).toBe(content + maximum);
      scores['language:length:characters'] = length - 1;
      expect(languageWritingMarks(rubric, scores)).toBe(content + lower);
      const expression = rubric.criteria.find(criterion => criterion.id === 'expression')!;
      expect(languageCriterionValue(rubric, expression.id, scores)).toBe(lower);
    }
    expect(writing('5').criteria.find(criterion => criterion.id === 'expression')!.limits![0].bands!.map(band => band.marks)).toEqual([
      [0, 1, 2, 3, 4], [5, 6, 7, 8, 9, 10, 11, 12], [13, 14, 15, 16, 17, 18, 19, 20],
    ]);
    expect(writing('5').criteria.filter(criterion => criterion.id.startsWith('heading-'))).toHaveLength(4);
    expect(card('4').questionText).toContain('200 Japanese characters');
    expect(card('5').questionText).toContain('320 Japanese characters');
  });

  it('retains source figures, listening continuation lines and original Atlas anchors', () => {
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(11);
    expect(card('lb-1-b').questionText).toBe('Mention two groups of people who use this hotel.');
    expect(card('ld-2-b-ii').questionText).toBe('How does Akemi persuade Chris to go to tea ceremony?');
    expect(point('lb-1-f').rows[0].verbatim).toBe('050-1807-3493');
    expect(point('lc-5').rows.map(row => row.contextNote)).toEqual(['Ireland', 'Europe', 'Japan']);
    const tags = JSON.parse(readFileSync(resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'), 'utf8'));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      expect(group, runtime.id).toBeDefined();
      expect(task.paperPages, runtime.id).toContain(group.pP);
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2025 && paper.fileid === task.atlas.fileid);
      expect(tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber).primary, runtime.id).toBe(runtime.topicId);
    }
  });
});
