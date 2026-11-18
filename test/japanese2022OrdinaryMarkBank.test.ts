import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import reviewed from '../components/MarkBank/cards/japanese/reviewed.json';
import aliases from '../components/MarkBank/cards/japanese/aliases.json';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import census from '../scripts/markbank/authoring/reviews/japanese-2022-ol-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2022-ol.json';
import resolvedExclusions from '../scripts/markbank/authoring/reviews/japanese-2022-ol-resolved-exclusions.json';
import activeExclusions from '../scripts/markbank/authoring/exclusions/japanese.json';
import { languagePointsMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import { tariffReconciles, UNPRINTED_ANSWER } from '../types/markBank';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = ordinary.filter(card => card.year === 2022);
const idFor = (key: (string | number | null)[]) => `ja-2022-ol-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2022-ol-${suffix}`)!;
const point = (suffix: string) => {
  const found = card(suffix);
  if (found.kind !== 'question') throw new Error(`Expected point card: ${suffix}`);
  return found;
};
const points = (suffix: string) => {
  const found = card(suffix);
  if (found.kind !== 'rubric' || found.rubric.system !== 'language-points') throw new Error(`Expected grouped rubric: ${suffix}`);
  return found.rubric;
};
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2022/${fileid}.json`), 'utf8'));

describe('Japanese 2022 Ordinary independent source review', () => {
  it('covers all 58 independent tasks and the 121/80/100 local tariffs, with the printed Q2 discrepancy recorded', () => {
    expect(cards).toHaveLength(58);
    expect(cards.map(card => card.id).sort()).toEqual(census.tasks.map(task => idFor(task.key)).sort());
    for (const task of census.tasks) {
      const found = cards.find(card => card.id === idFor(task.key))!;
      expect(found.totalMarks, found.id).toBe(task.marks);
      expect(tariffReconciles(found), found.id).toBe(true);
      expect(reviewed.find(card => card.id === found.id)!.sourceEvidence).toMatchObject({ component: task.component, paperPages: task.paperPages, schemePages: task.schemePages });
    }
    const total = (selected: typeof cards) => selected.reduce((sum, card) => sum + card.totalMarks, 0);
    expect(total(cards.filter(card => !card.audioMaterial && !['4', 'Q5'].includes(card.section!)))).toBe(121);
    expect(total(cards.filter(card => ['4', 'Q5'].includes(card.section!)))).toBe(80);
    expect(total(cards.filter(card => card.audioMaterial))).toBe(100);
    expect(total(cards)).toBe(301);
    expect(Object.values(census.pageRoles).map(pages => Object.keys(pages).length)).toEqual([16, 8, 16]);
    expect(review.sources.map(source => ({ component: source.document, path: source.path, sha256: source.sha256 }))).toEqual(census.sources);
    expect(review.sources.map(source => source.sha256)).toEqual([
      'f74fee39f437d293d101cb9f8ee3743eb1c268f7bc01950fa3016f59baaa32f1',
      '0967cbf965a69d1d695174b6104824c174b13ff582c7cb379a39e8c209de5ad8',
      'e348bdf1ac02f46c9c73350d1b7fbde4505a8d4f0dc0ff406ed4ac2d4e11093d',
    ]);
    for (const source of review.sources) expect(source.pagesReviewed).toEqual(Object.keys(census.pageRoles[source.document as keyof typeof census.pageRoles]).map(Number));
  });

  it('preserves the frozen Ordinary file and maps 41 original fragments to exactly six whole tasks', () => {
    const original = readFileSync(resolve(__dirname, '../components/MarkBank/cards/japanese/ordinary.ts'), 'utf8');
    expect(createHash('sha256').update(original).digest('hex')).toBe('83a3b57745ae80882d11a3346ab34cefba7b70d801701b87202493e0650983ef');
    const originalIds = [...original.matchAll(/^ {4}id: "([^"]+)"/gm)].map(match => match[1]);
    expect(originalIds).toHaveLength(261);
    expect(cards.filter(card => originalIds.includes(card.id))).toHaveLength(18);
    expect(cards.filter(card => !originalIds.includes(card.id))).toHaveLength(40);
    const sittingAliases = Object.fromEntries(Object.entries(aliases).filter(([id]) => id.startsWith('ja-2022-ol-')));
    expect(sittingAliases).toEqual(Object.fromEntries(review.consolidations.flatMap(entry => entry.legacyIds.map(id => [id, entry.canonicalId]))));
    expect(Object.keys(sittingAliases)).toHaveLength(41);
    expect(new Set(Object.values(sittingAliases)).size).toBe(6);
    for (const [old, target] of Object.entries(sittingAliases)) {
      expect(originalIds).toContain(old);
      expect(cards.some(card => card.id === old)).toBe(false);
      expect(cards.some(card => card.id === target)).toBe(true);
      expect(CARD_ID_ALIASES[old]).toBe(target);
      expect(target in aliases).toBe(false);
    }
    for (const entry of review.consolidations) {
      expect(idFor(entry.taskKey)).toBe(entry.canonicalId);
      for (const [document, evidence] of [['paper', entry.paperEvidence], ['scheme', entry.schemeEvidence]] as const) {
        expect(review.selectors.some(selector => selector.document === document && selector.page === evidence.page && selector.text === evidence.text)).toBe(true);
      }
    }
  });

  it('replaces all 52 historical exclusions with actual source-reviewed tasks', () => {
    expect(activeExclusions.filter(entry => entry.ref.startsWith('2022 OL'))).toEqual([]);
    expect(resolvedExclusions.resolved).toHaveLength(52);
    for (const entry of resolvedExclusions.resolved) {
      expect(entry.previousExclusion.evidence).toBeTruthy();
      expect(entry.reviewedCardIds.length).toBeGreaterThan(0);
      for (const id of entry.reviewedCardIds) expect(cards.some(card => card.id === id), entry.previousExclusion.ref).toBe(true);
    }
  });

  it('retains every finite option and the exact published selection quota', () => {
    for (const [suffix, quota, available, total] of [['2b', 5, 6, 15], ['2c', 10, 13, 10], ['3a-5', 3, 4, 9], ['3b-1', 5, 6, 10], ['3b-2', 5, 6, 10], ['4', 10, 12, 40]] as const) {
      const rubric = points(suffix);
      expect(rubric.count).toBe(quota);
      expect(rubric.groups).toHaveLength(available);
      const scores: LanguageScores = {};
      for (const group of rubric.groups) {
        scores[`language:group:${group.id}`] = 1;
        for (const row of group.rows) scores[`language:row:${group.id}:${row.id}`] = 1;
      }
      expect(languagePointsMarks(rubric, scores)).toBe(total);
    }
    expect(points('2b').groups[1].rows.map(row => row.marks)).toEqual([1, 2]);
    expect(points('2b').groups[1].rows[1].text).toContain('日本人も外国人もヨドバシ – AKIBA が大好きです。');
    expect(points('3b-2').groups.map(group => group.rows[0].text)).toEqual(['b. から', 'a が', 'c. は', 'a. で', 'c. に', 'b. と']);
    expect(points('4').groups.map(group => group.rows[0].marks)).toEqual(Array(12).fill(4));
    expect(card('4').questionText).toContain('A word should be used only once.');
  });

  it('keeps required sale-table cells, exact local tariffs and open culture credit', () => {
    expect(point('1-1').rows.map(row => row.verbatim)).toEqual(['6', '4', '3', '5', '9', '10']);
    expect(point('1-1').rows.map(row => row.marks)).toEqual(Array(6).fill(2));
    expect(point('1-6').rows.map(row => row.kind === 'anyN' ? row.group.perOption : row.marks)).toEqual([1, 1, 1, 1, 1, 2]);
    expect(point('1-6').totalMarks).toBe(7);
    expect(point('1-6').questionText).toContain('How to log in:');
    const q2 = cards.filter(card => card.questionRef.startsWith('2022 OL Section 2'));
    expect(q2.reduce((total, card) => total + card.totalMarks, 0)).toBe(43);
    expect(point('2a-1').rows[0].contextNote).toContain('A14 + B15 + C10 + D4 = 43');
    expect(points('2b').markingGuideNote).toContain('printed section total of 120');
    expect(point('2d').rows[0]).toMatchObject({ verbatim: UNPRINTED_ANSWER, unprinted: true, marks: 4, permittedMarks: [0, 2, 4] });
    expect(point('2d').rows[0].parts?.map(part => part.marks)).toEqual([2, 2]);
    expect(point('3a-2').rows[0]).toMatchObject({ kind: 'anyN', group: { claimMax: 2, perOptionSteps: [2, 1] } });
  });

  it('shows the literal phone conflict without fabricating a per-digit allocation', () => {
    const phone = point('lb-1-v').rows[0];
    expect(point('lb-1-v').tariffModel).toEqual({ kind: 'questionTotal' });
    expect(point('lb-1-v').totalMarks).toBe(4);
    expect(phone).toMatchObject({ kind: 'point', marks: null });
    expect(phone.permittedMarks).toBeUndefined();
    expect(phone.verbatim).toContain('0120-923-915');
    expect(phone.verbatim.replace(/\s+/g, ' ')).toContain('any two digits, 1 mark each');
    expect(phone.parts).toBeUndefined();
    expect(phone.contextNote).toContain('eight missing digits');
    expect(phone.contextNote).toContain('inconsistent');
    expect(phone.contextNote).toContain('Unresolved source scoring conflict');
    expect(phone.contextNote).toContain('no per-digit allocation or partial-credit scale is inferred');
    expect(point('lb-1-v').qa?.gates).not.toContain('tariff');
    expect(point('lb-1-v').qa?.gates).toContain('source-tariff-unresolved');
    expect(review.status).toBe('source-captured-with-unresolved-tariff');
    expect(review.unresolvedSourceIssues).toEqual([expect.objectContaining({ cardId: 'ja-2022-ol-lb-1-v', resolution: null })]);
    expect(point('lc-3-iii').questionRef).toBe('2022 OL Section LC Q3(iii)');
    expect(point('lc-3-iii').rows[0].verbatim).toBe('(c) A volleyball match');
    expect(point('ld-1-iv').rows[0]).toMatchObject({ verbatim: '2:30', marks: 2 });
    expect(point('ld-2-i').rows[0]).toMatchObject({ kind: 'anyN', group: { claimMax: 1, perOption: 3, options: ['Sausage', 'hamburger'] } });
  });

  it('assesses C4 and E4 independently for each of five chosen weekend responses', () => {
    const rubric = points('5');
    expect(rubric.count).toBe(5);
    expect(rubric.groups).toHaveLength(8);
    const scores: LanguageScores = {};
    for (const group of rubric.groups) {
      scores[`language:group:${group.id}`] = 1;
      expect(group.criteria?.map(criterion => criterion.maxMarks)).toEqual([4, 4]);
      for (const criterion of group.criteria!) scores[`language:${criterion.id}`] = 4;
    }
    expect(languagePointsMarks(rubric, scores)).toBe(40);
    scores['language:item-1-expression'] = 1;
    expect(languagePointsMarks(rubric, scores)).toBe(37);
    expect(rubric.groups[0].criteria![1].bands?.map(band => band.marks)).toEqual([[1], [2, 3], [4]]);
    expect(card('5').answerLanguageRule).toBeUndefined();
    expect(rubric.groups[6].label).toContain('どんな食べ物を食べますか。');
    expect(rubric.groups[7].label).toContain('何時にねますか。');
    for (const suffix of ['4', '5']) expect(card(suffix).questionText).toContain('Answer either Question 4 or Question 5.');
    expect(census.candidateMaximum).toMatchObject({ publishedWritten: 160, publishedListening: 100, publishedTotal: 260, sumOfLocalTariffs: 261 });
  });

  it('binds 55 scoring conditions and the numeric phone guidance to the original source selectors', () => {
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(55);
    for (const found of cards) {
      expect(found.extraneousMaterialRule).toBeUndefined();
      if (['4', 'Q5'].includes(found.section!)) {
        expect(found.answerLanguageRule).toBeUndefined();
        continue;
      }
      const page = found.audioMaterial ? 3 : 5;
      const source = review.selectors.find(selector => selector.document === 'scheme' && selector.page === page && selector.row === 1)!;
      if (found.id === 'ja-2022-ol-lb-1-v') {
        expect(found.answerLanguageRule).toBeUndefined();
        expect(point('lb-1-v').rows[0].contextNote).toContain(source.text);
        continue;
      }
      expect(found.answerLanguageRule).toEqual({ otherLanguageMultiplier: 0.5, sourceText: source.text, schemePages: [page], ...(found.audioMaterial ? { penalizedLanguage: 'Japanese' } : {}) });
    }
  });

  it('retains every multiple-choice alternative and complete reviewed source crops', () => {
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(8);
    for (const suffix of ['la-1-i', 'la-1-ii', 'la-2-i', 'la-3-i', 'la-3-iii', 'lb-1-i', 'lb-1-iv', 'lb-2-ii', 'lc-1-i', 'lc-2-i', 'lc-3-i', 'lc-3-ii', 'lc-3-iii', 'ld-1-ii', 'ld-1-iii', 'ld-2-iii', 'ld-2-iv']) {
      for (const label of ['a', 'b', 'c', 'd']) expect(card(suffix).questionText, suffix).toContain(`(${label})`);
    }
    expect(card('la-3-i').questionText).toContain('Where does Andrea want to go to college?');
    expect(card('lc-2-ii').questionText).toContain('What will the receptionist do if she finds the item?');
    expect(card('3a-5').questionRef).toBe('2022 OL Section 3A Q5');
    expect(card('3b-1').questionRef).toBe('2022 OL Section 3B Q1');
  });

  it('preserves every original Atlas identity and aligns all task topics and source pages', () => {
    const tags = ['japanese.json', 'japanese-written-2019-2022.json'].flatMap(file => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/topic-tags/tags/${file}`), 'utf8')));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      expect(task.paperPages, runtime.id).toContain(group.pP);
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2022 && paper.fileid === task.atlas.fileid);
      expect(tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber).primary, runtime.id).toBe(runtime.topicId);
      expect(sidecar.band).toEqual([1, 16]);
    }
    expect(map('LC058GLP000BV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 24 }, (_, i) => String(i + 1)));
    expect(map('LC058GLP000BV.pdf').q.find(question => question.n === '19')!.label).toBe('Q3 A · 5 (Answer in Japanese)');
    expect(map('LC058GLP000BV.pdf').q.find(question => question.n === '24')!.region.map(region => region.p)).toEqual([9, 10]);
  });
});
