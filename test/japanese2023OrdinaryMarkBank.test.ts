import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import reviewed from '../components/MarkBank/cards/japanese/reviewed.json';
import aliases from '../components/MarkBank/cards/japanese/aliases.json';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import census from '../scripts/markbank/authoring/reviews/japanese-2023-ol-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2023-ol.json';
import resolvedExclusions from '../scripts/markbank/authoring/reviews/japanese-2023-ol-resolved-exclusions.json';
import activeExclusions from '../scripts/markbank/authoring/exclusions/japanese.json';
import { languagePointsMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import { tariffReconciles, UNPRINTED_ANSWER } from '../types/markBank';
import type { PaperAnswerMap } from '../types/paperTrail';
import { topicsForPaper } from '../components/PaperTrail/topics';

const cards = ordinary.filter(card => card.year === 2023);
const idFor = (key: (string | number | null)[]) => `ja-2023-ol-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2023-ol-${suffix}`)!;
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
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2023/${fileid}.json`), 'utf8'));

describe('Japanese 2023 Ordinary independent source review', () => {
  it('covers all 58 independent tasks and the 120/80/100 printed tariffs', () => {
    expect(cards).toHaveLength(58);
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
    expect(Object.values(census.pageRoles).map(pages => Object.keys(pages).length)).toEqual([16, 8, 16]);
    expect(review.sources.map(source => ({ component: source.document, path: source.path, sha256: source.sha256 }))).toEqual(census.sources);
    expect(review.sources.map(source => source.sha256)).toEqual([
      '2307421a7a512bf54cee23213875bc1545b5616ffd7cc877aa28034232a27e3b',
      'bc4052eb76ca8ca4f0e552c4e79a1475f73ac5d223207abfb199efd32e89f9eb',
      '360f0300ec60d4920a5831f01f53f9dce2ed9169eb2f569c3f0a6760a4932425',
    ]);
    for (const source of review.sources) expect(source.pagesReviewed).toEqual(Object.keys(census.pageRoles[source.document as keyof typeof census.pageRoles]).map(Number));
  });

  it('preserves the frozen Ordinary file and maps 34 original fragments to exactly five whole tasks', () => {
    const original = readFileSync(resolve(__dirname, '../components/MarkBank/cards/japanese/ordinary.ts'), 'utf8');
    expect(createHash('sha256').update(original).digest('hex')).toBe('83a3b57745ae80882d11a3346ab34cefba7b70d801701b87202493e0650983ef');
    const originalIds = [...original.matchAll(/^ {4}id: "([^"]+)"/gm)].map(match => match[1]);
    expect(originalIds).toHaveLength(261);
    expect(cards.filter(card => originalIds.includes(card.id))).toHaveLength(17);
    expect(cards.filter(card => !originalIds.includes(card.id))).toHaveLength(41);
    const sittingAliases = Object.fromEntries(Object.entries(aliases).filter(([id]) => id.startsWith('ja-2023-ol-')));
    expect(sittingAliases).toEqual(Object.fromEntries(review.consolidations.flatMap(entry => entry.legacyIds.map(id => [id, entry.canonicalId]))));
    expect(Object.keys(sittingAliases)).toHaveLength(34);
    expect(new Set(Object.values(sittingAliases)).size).toBe(5);
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

  it('replaces all 39 historical exclusions with actual source-reviewed tasks', () => {
    expect(activeExclusions.filter(entry => entry.ref.startsWith('2023 OL'))).toEqual([]);
    expect(resolvedExclusions.resolved).toHaveLength(39);
    for (const entry of resolvedExclusions.resolved) {
      expect(entry.previousExclusion.evidence).toBeTruthy();
      expect(entry.reviewedCardIds.length).toBeGreaterThan(0);
      for (const id of entry.reviewedCardIds) expect(cards.some(card => card.id === id), entry.previousExclusion.ref).toBe(true);
    }
  });

  it('keeps all printed choice options and caps scoring at the exact quotas', () => {
    for (const [suffix, quota, available, total] of [['2b', 5, 6, 15], ['2c', 10, 13, 10], ['3a-5', 3, 4, 6], ['2d', 5, 6, 10], ['3c', 5, 6, 10], ['4', 10, 12, 30]] as const) {
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
    expect(points('2b').groups[1].rows[1].text).toContain('小学校からおんがくが大好きでした。');
    expect(points('2d').groups.map(group => group.rows[0].text)).toEqual(['b. から', 'c. は', 'a. が', 'b. で', 'a. を', 'c. の']);
    expect(card('4').questionText).toContain('A word should be used only once.');
    expect(points('4').groups[8].rows[0].text).toBe('四年生');
    expect(card('4').questionText).toContain('トレーニング');
    expect(card('4').questionText).not.toContain('四年生');
    expect(points('4').markingGuideNote).toContain('absent from the paper’s word bank');

  });

  it('retains required table cells, complete item/quantity claims and the open culture response', () => {
    expect(point('1-1').rows.map(row => row.marks)).toEqual([2, 2, 2, 2, 2]);
    expect(point('2a-1').rows.map(row => [row.verbatim, row.marks])).toEqual([
      ['10th March', 1], ['Tokushima', 1], ['6th March', 1], ['Marigold', 1],
    ]);
    expect(point('2a-1').questionText).toContain('Lemon');
    expect(point('2a-1').questionText).toContain('Hyougo');
    const items = point('1-7').rows[0];
    if (items.kind !== 'anyN') throw new Error('Expected complete item pool');
    expect(items.group).toMatchObject({ claimMax: 2, perOption: 2 });
    expect(items.group.options).toHaveLength(4);
    expect(point('3b').rows[0]).toMatchObject({ verbatim: UNPRINTED_ANSWER, unprinted: true, marks: 4, permittedMarks: [0, 2, 4] });
    expect(point('3b').rows[0].parts?.map(part => part.marks)).toEqual([2, 2]);
  });

  it('keeps the published whole-phone tariff and paper-only Part D numbering', () => {
    const phone = point('lb-1-v').rows[0];
    expect(phone).toMatchObject({ kind: 'point', verbatim: '090-785-3642', marks: 4 });
    expect(phone.parts).toBeUndefined();
    expect(phone.contextNote).toContain('no separate per-digit tariff');
    expect(point('ld-iv').questionRef).toBe('2023 OL Section LD(iv)');
    expect(point('ld-iv').rows[0]).toMatchObject({ verbatim: '(c) Sports', marks: 4 });
    expect(point('ld-vi').rows[0].verbatim).toBe('(b) July 9th');
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
    expect(rubric.groups[6].label).toContain('そのしゅみはどうですか。');
    expect(rubric.groups[7].label).toContain('あたらしいしゅみがしたいですか。');
    expect(card('5').questionText).not.toContain('なつ休みが好きですか。');
    expect(rubric.markingGuideNote).toContain('なつ休みが好きですか。');
  });

  it('scopes language rules to the two exact published conditions and leaves writing unchanged', () => {
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(56);
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
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(9);
    expect(card('la-3-ii').questionText).toContain('The lack of English signs outside the city');
    expect(card('la-3-ii').questionText).toContain('The lack of friends from the Philippines');
    expect(card('lc-1-i').questionText).toContain('What is the top dream job of primary school students in Matsue?');
    expect(card('lc-1-iii').questionText).toContain('Why do primary school students want to do their top dream job?');
    expect(card('ld-ii').questionText).toContain('He heard about the camp from a college senior');
    const tags = JSON.parse(readFileSync(resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'), 'utf8'));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      for (const number of [task.atlas.questionNumber]) {
        const group = sidecar.q.find(question => question.n === number)!;
        expect(task.paperPages, runtime.id).toContain(group.pP);
        expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
        const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2023 && paper.fileid === task.atlas.fileid);
        expect(tagged.q.find((question: { n: string }) => question.n === number).primary, runtime.id).toBe(runtime.topicId);
      }
    }
    expect(map('LC058GLP000BV.pdf').q.find(question => question.n === '24')!.region.map(region => region.p)).toEqual([10, 11]);
    const culture = map('LC058GLP000BV.pdf').q.find(question => question.n === '25')!;
    expect(topicsForPaper('japanese', 2023, 'ordinary', 'ev', 'LC058GLP000BV.pdf')?.q.find(question => question.n === '25')).toMatchObject({ primary: 'japanese-5-6' });
    expect(culture).toMatchObject({ label: 'Text 3 · B School comparison', pP: 10, region: [{ p: 8, r: [0, 0.805, 1, 0.92] }] });
    expect(map('LC058GLP000BV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 25 }, (_, i) => String(i + 1)));
  });
});
