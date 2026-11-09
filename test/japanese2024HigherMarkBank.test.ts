import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as higher } from '../components/MarkBank/cards/japanese/higher';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import rawCards from '../components/MarkBank/cards/japanese/reviewed.json';
import aliases from '../components/MarkBank/cards/japanese/aliases.json';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import census from '../scripts/markbank/authoring/reviews/japanese-2024-hl-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2024-hl.json';
import resolvedExclusions from '../scripts/markbank/authoring/reviews/japanese-2024-hl-resolved-exclusions.json';
import activeExclusions from '../scripts/markbank/authoring/exclusions/japanese.json';
import { tariffReconciles } from '../types/markBank';
import { languageCriterionValue, languagePointsMarks, languageWritingMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = higher.filter(card => card.year === 2024);
const idFor = (key: (string | number | null)[]) => `ja-2024-hl-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2024-hl-${suffix}`)!;
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
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2024/${fileid}.json`), 'utf8'));

describe('Japanese 2024 Higher independent source review', () => {
  it('covers all 72 independently counted tasks and the published 120/100/80 tariffs', () => {
    expect(cards).toHaveLength(72);
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
    expect(Object.values(census.pageRoles).map(pages => Object.keys(pages).length)).toEqual([20, 8, 19]);
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
    expect(rawCards.filter(card => !originalIds.includes(card.id))).toHaveLength(906);
    expect(live.size).toBe(600 + 906 - 391);
    expect(cards.filter(card => originalIds.includes(card.id))).toHaveLength(20);
  });

  it('binds exactly 44 original fragment aliases to seven complete source tasks', () => {
    const expected = Object.fromEntries(review.consolidations.flatMap(entry => entry.legacyIds.map(id => [id, entry.canonicalId])));
    const sittingAliases = Object.fromEntries(Object.entries(aliases).filter(([id]) => id.startsWith('ja-2024-hl-')));
    expect(sittingAliases).toEqual(expected);
    expect(Object.keys(sittingAliases)).toHaveLength(44);
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
    expect(activeExclusions.filter(entry => entry.ref.startsWith('2024 HL'))).toEqual([]);
    expect(resolvedExclusions.resolved).toHaveLength(43);
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

  it('limits language and extraneous-material conditions to their separate printed headings', () => {
    const extraneous = ['2a-3-i', '2a-3-ii', '2a-3-iii', '3b-1', '3b-2', '3b-3', '3b-4'];
    expect(cards.filter(card => card.extraneousMaterialRule).map(card => card.id).sort()).toEqual(extraneous.map(suffix => `ja-2024-hl-${suffix}`).sort());
    for (const suffix of extraneous) {
      const found = point(suffix);
      const expectedPage = suffix.startsWith('2a') ? 7 : 10;
      expect(found.extraneousMaterialRule).toMatchObject({ multiplier: 0.5, schemePages: [expectedPage] });
      expect(found.extraneousMaterialRule!.sourceText).toContain('strong evidence of extraneous material');
      expect(found.answerLanguageRule).toBeUndefined();
      expect(review.selectors.some(selector => selector.document === 'scheme' && selector.page === expectedPage && selector.text === found.extraneousMaterialRule!.sourceText)).toBe(true);
    }
    const language = cards.filter(card => card.id.startsWith('ja-2024-hl-l') || card.id.startsWith('ja-2024-hl-1b-'));
    expect(language).toHaveLength(36);
    expect(cards.filter(card => card.answerLanguageRule).map(card => card.id)).toEqual(language.map(card => card.id));
    for (const found of language) {
      expect(found.answerLanguageRule!.penalizedLanguage).toBe('Japanese');
      expect(found.answerLanguageRule!.otherLanguageMultiplier).toBe(0.5);
      expect(found.answerLanguageRule!.sourceText).toContain('answered in Japanese');
      expect(found.extraneousMaterialRule).toBeUndefined();
    }
    expect(card('la-1').answerLanguageRule!.sourceText).toBe('(1/2 marks if answered in Japanese)');
  });

  it('preserves printed discrepancies, separately priced cells and dependent alternatives', () => {
    expect(point('1a-3-ii').rows.map(row => row.marks)).toEqual([1, 1, 1, 1]);
    expect(point('2a-1').totalMarks).toBe(7);
    expect(point('2a-1').questionText).toContain('Where is the main office?');
    expect(point('2a-1').questionText).toContain('Akihabara');
    expect(point('lc-1-ii').questionText).toBe('What two activities can you enjoy at Odori park?');
    expect(point('lc-1-ii').rows[0]).toMatchObject({ group: { claimMax: 3, perOption: 1 } });
    expect(point('lc-1-ii').rows[0].contextNote).toContain('any three details, 1 mark each');
    expect(['i', 'ii', 'iii'].map(roman => point(`ld-1-${roman}`).totalMarks)).toEqual([2, 3, 2]);
    expect(point('ld-1-i').rows.map(row => row.verbatim)).toEqual(['6:30', 'pm']);
    expect(point('2a-4').questionRef).toBe('2024 HL Section 2A Q4');
    expect(point('2a-4').rows.map(row => row.marks)).toEqual([1, 1, 1, 1]);
    expect(point('lb-7').rows.map(row => row.kind === 'anyN' ? row.group.perOption : row.marks)).toEqual([2, 1]);
    const grammar = card('3d');
    if (grammar.kind !== 'rubric' || grammar.rubric.system !== 'language-points') throw new Error('Expected grammar pool');
    expect(grammar.rubric.groups[2].rows[0].text).toBe('で(accept まで if の is used in the previous particle)');
    expect(point('ld-3-iii').rows[0]).toMatchObject({ group: { claimMax: 2, options: ['Sake (for dad)', 'yukata (for mum)', 'macha KitKat (for Anna)'] } });
  });

  it('retains literal roman-then-letter references on all six independently inventoried listening subparts', () => {
    const nested = census.tasks.filter(task => 'paperRef' in task);
    expect(nested).toHaveLength(6);
    for (const task of nested) {
      const found = cards.find(card => card.id === idFor(task.key))!;
      expect(found.questionRef).toBe(task.paperRef);
      const [section, q, letter, roman] = task.key;
      expect(found.questionRef).toBe(`2024 HL Section ${section} Q${q}(${roman})(${letter})`);
    }
    expect(card('lc-1-a-iv').totalMarks).toBe(1);
    expect(card('lc-1-b-iv').totalMarks).toBe(2);
    expect(card('ld-3-a-ii').totalMarks).toBe(1);
    expect(card('ld-3-b-ii').totalMarks).toBe(3);
  });

  it('uses the distinct 2024 writing bands and lower-expression conditions', () => {
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
    expect(card('lb-1').questionText).toBe('At age 10, Sky Brown became a professional athlete in which sport?');
    expect(card('lc-2-ii').questionText).toBe('What advice is given for people going to the festival at the weekend?');
    expect(point('ld-1-iii').rows[0].verbatim).toBe('085-2418139');
    expect(card('la-3').questionText).toContain('When did they start their hobby?');
    const tags = JSON.parse(readFileSync(resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'), 'utf8'));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      expect(group, runtime.id).toBeDefined();
      expect(task.paperPages, runtime.id).toContain(group.pP);
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2024 && paper.fileid === task.atlas.fileid);
      expect(tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber).primary, runtime.id).toBe(runtime.topicId);
    }
  });
});
