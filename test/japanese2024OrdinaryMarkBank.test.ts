import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import reviewed from '../components/MarkBank/cards/japanese/reviewed.json';
import aliases from '../components/MarkBank/cards/japanese/aliases.json';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import census from '../scripts/markbank/authoring/reviews/japanese-2024-ol-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2024-ol.json';
import resolvedExclusions from '../scripts/markbank/authoring/reviews/japanese-2024-ol-resolved-exclusions.json';
import activeExclusions from '../scripts/markbank/authoring/exclusions/japanese.json';
import { languagePointsMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import { tariffReconciles, UNPRINTED_ANSWER } from '../types/markBank';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = ordinary.filter(card => card.year === 2024);
const idFor = (key: (string | number | null)[]) => `ja-2024-ol-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2024-ol-${suffix}`)!;
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
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2024/${fileid}.json`), 'utf8'));

describe('Japanese 2024 Ordinary independent source review', () => {
  it('covers all 59 independent tasks and the 120/80/100 printed tariffs', () => {
    expect(cards).toHaveLength(59);
    expect(cards.map(card => card.id).sort()).toEqual(census.tasks.map(task => idFor(task.key)).sort());
    for (const task of census.tasks) {
      const found = cards.find(card => card.id === idFor(task.key))!;
      expect(found.totalMarks, found.id).toBe(task.marks);
      expect(tariffReconciles(found), found.id).toBe(true);
      expect(reviewed.find(card => card.id === found.id)!.sourceEvidence).toMatchObject({ component: task.component, paperPages: task.paperPages, schemePages: task.schemePages });
    }
    const total = (selected: typeof cards) => selected.reduce((sum, card) => sum + card.totalMarks, 0);
    expect(total(cards.filter(card => !card.audioMaterial && !['4', 'Q5'].includes(card.section!)))).toBe(120);
    expect(total(cards.filter(card => ['4', 'Q5'].includes(card.section!)))).toBe(80);
    expect(total(cards.filter(card => card.audioMaterial))).toBe(100);
    expect(total(cards)).toBe(300);
    expect(Object.values(census.pageRoles).map(pages => Object.keys(pages).length)).toEqual([16, 8, 17]);
    expect(review.sources.map(source => ({ component: source.document, path: source.path, sha256: source.sha256 }))).toEqual(census.sources);
    expect(review.sources.map(source => source.sha256)).toEqual([
      '4b98a657a87bff55e83fe8419ed2d9f0926738f2bab6820c976637a0bde1b14e',
      '466dda0e3f2d8e38475be8c3fd9d636db7d7490e80f99187ab9659d274750abc',
      '998990bd6cfdec27155f064a23766c1797503ac9afa11ccfa273fa2783d1dfea',
    ]);
    for (const source of review.sources) expect(source.pagesReviewed).toEqual(Object.keys(census.pageRoles[source.document as keyof typeof census.pageRoles]).map(Number));
  });

  it('preserves the frozen Ordinary file and maps 40 original fragments to exactly six whole tasks', () => {
    const original = readFileSync(resolve(__dirname, '../components/MarkBank/cards/japanese/ordinary.ts'), 'utf8');
    expect(createHash('sha256').update(original).digest('hex')).toBe('83a3b57745ae80882d11a3346ab34cefba7b70d801701b87202493e0650983ef');
    const originalIds = [...original.matchAll(/^ {4}id: "([^"]+)"/gm)].map(match => match[1]);
    expect(originalIds).toHaveLength(261);
    expect(cards.filter(card => originalIds.includes(card.id))).toHaveLength(19);
    expect(cards.filter(card => !originalIds.includes(card.id))).toHaveLength(40);
    const sittingAliases = Object.fromEntries(Object.entries(aliases).filter(([id]) => id.startsWith('ja-2024-ol-')));
    expect(sittingAliases).toEqual(Object.fromEntries(review.consolidations.flatMap(entry => entry.legacyIds.map(id => [id, entry.canonicalId]))));
    expect(Object.keys(sittingAliases)).toHaveLength(40);
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

  it('replaces all 67 historical exclusions with actual source-reviewed tasks', () => {
    expect(activeExclusions.filter(entry => entry.ref.startsWith('2024 OL'))).toEqual([]);
    expect(resolvedExclusions.resolved).toHaveLength(67);
    for (const entry of resolvedExclusions.resolved) {
      expect(entry.previousExclusion.evidence).toBeTruthy();
      expect(entry.reviewedCardIds.length).toBeGreaterThan(0);
      for (const id of entry.reviewedCardIds) expect(cards.some(card => card.id === id), entry.previousExclusion.ref).toBe(true);
    }
  });

  it('keeps all printed choice options and caps scoring at the exact quotas', () => {
    for (const [suffix, quota, available, total] of [['2b', 5, 6, 15], ['2c', 10, 13, 10], ['3a-5', 3, 4, 6], ['3b-1', 5, 6, 10], ['3b-2', 5, 6, 10], ['4', 10, 12, 30]] as const) {
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
    expect(points('2b').groups[1].rows[1].text).toContain('さむい天気の日');
    expect(points('3b-2').groups.map(group => group.rows[0].text)).toEqual(['c. に', 'b を', 'a. は', 'b. まで', 'a. の', 'c. が']);
    expect(card('4').questionText).toContain('A word should be used only once.');
    expect(points('4').groups.map(group => group.rows[0].text)).toEqual(['2 週間', 'あね', '天気', 'たのしい', 'ショッピング', 'まんが', '100 円ショップ', '食べます', 'すし', '13 日', '町（まち）', 'しんかんせん']);
  });

  it('retains whole required tables, descending tariffs and two unprinted cultural responses', () => {
    expect(point('1-1').rows.map(row => row.marks)).toEqual([2, 2, 2, 2, 2]);
    expect(point('1-6').rows.map(row => [row.verbatim, row.marks, row.contextNote])).toEqual([
      ['14 visits per year', 2, 'Gold — Conditions'], ['3000 yen', 2, 'Silver — Gift card'], ['10,000 yen', 2, 'Gold — Gift card'],
    ]);
    expect(point('2a-5').rows.map(row => [row.verbatim, row.marks])).toEqual([['11.30', 1], ['6', 1]]);
    for (const suffix of ['1-4', '1-5', '1-7', '2a-3']) {
      const row = point(suffix).rows[0];
      if (row.kind !== 'anyN') throw new Error('Expected descending answer pool');
      expect(row.group.claimMax).toBe(2);
      expect(row.group.perOptionSteps).toEqual([2, 1]);
    }
    expect(point('2d').rows).toHaveLength(1);
    expect(point('2d').rows[0]).toMatchObject({ verbatim: UNPRINTED_ANSWER, unprinted: true, marks: 4, permittedMarks: [0, 2, 4] });
    expect(point('2d').rows[0].parts?.map(part => part.marks)).toEqual([2, 2]);
  });

  it('prices only the four missing phone digits and keeps the whole two-mark arrival time', () => {
    const phone = point('ld-1-iii').rows[0];
    expect(phone).toMatchObject({ kind: 'criterion', marks: 4, permittedMarks: [0, 1, 2, 3, 4] });
    expect(phone.parts?.map(part => [part.verbatim, part.marks, part.permittedMarks])).toEqual([
      ['5', 1, [0, 1]], ['4', 1, [0, 1]], ['1', 1, [0, 1]], ['9', 1, [0, 1]],
    ]);
    expect(phone.verbatim).toContain('1 mark for each correct number');
    expect(point('ld-1-i').rows).toHaveLength(1);
    expect(point('ld-1-i').rows[0]).toMatchObject({ verbatim: '6:30', marks: 2 });
  });

  it('uses separate five-point content and expression placements for each chosen writing response', () => {
    const rubric = points('5');
    expect(rubric.count).toBe(5);
    expect(rubric.groups).toHaveLength(8);
    const scores: LanguageScores = {};
    for (const group of rubric.groups) {
      scores[`language:group:${group.id}`] = 1;
      expect(group.criteria?.map(criterion => criterion.maxMarks)).toEqual([5, 5]);
      for (const criterion of group.criteria!) scores[`language:${criterion.id}`] = 5;
    }
    expect(languagePointsMarks(rubric, scores)).toBe(50);
    scores['language:item-1-expression'] = 2;
    expect(languagePointsMarks(rubric, scores)).toBe(47);
    expect(rubric.groups[0].criteria![1].bands?.map(band => band.marks)).toEqual([[1], [2, 3], [4, 5]]);
    expect(card('5').answerLanguageRule).toBeUndefined();
  });

  it('scopes language rules to the two exact published conditions and leaves writing unchanged', () => {
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(57);
    for (const found of cards) {
      if (['4', 'Q5'].includes(found.section!)) {
        expect(found.answerLanguageRule).toBeUndefined();
        continue;
      }
      const page = found.audioMaterial ? 3 : 5;
      const source = review.selectors.find(selector => selector.document === 'scheme' && selector.page === page && selector.row === 1)!;
      expect(found.answerLanguageRule).toEqual({ otherLanguageMultiplier: 0.5, sourceText: source.text, schemePages: [page], ...(found.audioMaterial ? { penalizedLanguage: 'Japanese' } : {}) });
      expect(found.extraneousMaterialRule).toBeUndefined();
    }
  });

  it('retains complete original stimuli, listening continuations and stable Atlas anchors', () => {
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(8);
    expect(card('la-3-iii').questionText).toContain('(d)  see her photos in the paper.');
    expect(card('lb-7').questionText).toBe('Mention one thing Sky likes to do in her free time.');
    expect(card('lc-2-iii').questionText).toContain('(b) Jumper (c) Long coat (d) Hat');
    expect(point('la-2-iii').questionRef).toBe('2024 OL Section LA Q2(iii)');
    expect(point('la-2-iii').rows[0].verbatim).toBe('(d) A ninja game');
    expect(point('lc-2-iii').questionRef).toBe('2024 OL Section LC Q2(iii)');
    expect(point('lc-2-iii').rows[0].verbatim).toBe('(b) Jumper');
    expect(card('ld-3-ii').questionText).toContain('(d) Green tea KitKat');
    const tags = JSON.parse(readFileSync(resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'), 'utf8'));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      for (const number of [task.atlas.questionNumber]) {
        const group = sidecar.q.find(question => question.n === number)!;
        expect(task.paperPages, runtime.id).toContain(group.pP);
        expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
        const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2024 && paper.fileid === task.atlas.fileid);
        expect(tagged.q.find((question: { n: string }) => question.n === number).primary, runtime.id).toBe(runtime.topicId);
      }
    }
    expect(map('LC058GLP000BV.pdf').q.find(question => question.n === '25')!.region.map(region => region.p)).toEqual([10, 11]);
  });
});
