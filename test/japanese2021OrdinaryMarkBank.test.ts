import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import reviewed from '../components/MarkBank/cards/japanese/reviewed.json';
import aliases from '../components/MarkBank/cards/japanese/aliases.json';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import census from '../scripts/markbank/authoring/reviews/japanese-2021-ol-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2021-ol.json';
import resolvedExclusions from '../scripts/markbank/authoring/reviews/japanese-2021-ol-resolved-exclusions.json';
import activeExclusions from '../scripts/markbank/authoring/exclusions/japanese.json';
import { languagePointsMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import { tariffReconciles, UNPRINTED_ANSWER } from '../types/markBank';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = ordinary.filter(card => card.year === 2021);
const idFor = (key: (string | number | null)[]) => `ja-2021-ol-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2021-ol-${suffix}`)!;
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
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2021/${fileid}.json`), 'utf8'));

describe('Japanese 2021 Ordinary independent source review', () => {
  it('covers all 57 independent tasks and the published120/80/100 tariffs', () => {
    expect(cards).toHaveLength(57);
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
      '9e08378aa046efa6aa546be9a143a6ed4c42037cccc146c1638a65b91af75063',
      'cd02fd8088e72e5f54b8eb89d238be0eec8e8252fc48ce2b5be7cfdbb2f44110',
      'ddc4b5bd8045f44a4a86664c7fc4c4981ed659cb1f14b83c4801cb5a4fb0b30b',
    ]);
    for (const source of review.sources) expect(source.pagesReviewed).toEqual(Object.keys(census.pageRoles[source.document as keyof typeof census.pageRoles]).map(Number));
  });

  it('preserves the frozen Ordinary file and maps 39 original fragments to exactly six whole tasks', () => {
    const original = readFileSync(resolve(__dirname, '../components/MarkBank/cards/japanese/ordinary.ts'), 'utf8');
    expect(createHash('sha256').update(original).digest('hex')).toBe('83a3b57745ae80882d11a3346ab34cefba7b70d801701b87202493e0650983ef');
    const originalIds = [...original.matchAll(/^ {4}id: "([^"]+)"/gm)].map(match => match[1]);
    expect(originalIds).toHaveLength(261);
    expect(cards.filter(card => originalIds.includes(card.id))).toHaveLength(18);
    expect(cards.filter(card => !originalIds.includes(card.id))).toHaveLength(39);
    const sittingAliases = Object.fromEntries(Object.entries(aliases).filter(([id]) => id.startsWith('ja-2021-ol-')));
    expect(sittingAliases).toEqual(Object.fromEntries(review.consolidations.flatMap(entry => entry.legacyIds.map(id => [id, entry.canonicalId]))));
    expect(Object.keys(sittingAliases)).toHaveLength(39);
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

  it('replaces all 37 historical exclusions with actual source-reviewed tasks', () => {
    expect(activeExclusions.filter(entry => entry.ref.startsWith('2021 OL'))).toEqual([]);
    expect(resolvedExclusions.resolved).toHaveLength(37);
    for (const entry of resolvedExclusions.resolved) {
      expect(entry.previousExclusion.evidence).toBeTruthy();
      expect(entry.reviewedCardIds.length).toBeGreaterThan(0);
      for (const id of entry.reviewedCardIds) expect(cards.some(card => card.id === id), entry.previousExclusion.ref).toBe(true);
    }
  });

  it('retains every finite option and the exact published selection quota', () => {
    for (const [suffix, quota, available, total] of [['2b', 5, 6, 15], ['2c', 10, 13, 10], ['3a-5', 3, 4, 6], ['3b-1', 5, 6, 10], ['3b-2', 5, 6, 10], ['4', 10, 12, 40]] as const) {
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
    expect(points('2c').groups[12].label).toContain('(d) big');
    expect(points('3b-1').groups[2].rows[0].text).toContain('好きじゃないです／じゃありません／ではありません。');
    expect(points('3b-1').groups[3].rows[0].text).toContain('たのしくないです／たのしくありません。');
    expect(points('3b-2').groups.map(group => group.rows[0].text)).toEqual(['b. の', 'a. で', 'b.は', 'c. から', 'a. を', 'a. を']);
    expect(points('4').groups.map(group => group.rows[0].marks)).toEqual(Array(12).fill(4));
    expect(points('4').groups[4].rows[0].text).toBe('サッカー／えいが');
    expect(points('4').groups[10].rows[0].text).toBe('大学生／四年生');
    expect(card('4').questionText).toContain('A word should be used only once.');
  });

  it('source-verifies both previously unshipped candidates without inventing an original alias', () => {
    const truth = points('2b').groups[1];
    expect(truth.label).toContain('53% of Japanese people use LINE.');
    expect(truth.rows.map(row => row.marks)).toEqual([1, 2]);
    expect(truth.rows[0].text).toBe('False');
    expect(truth.rows[1].text).toContain('日本人の 67％がラインを使');
    expect(review.selectors.find(selector => selector.document === 'paper' && selector.page === 5 && selector.row === 27)!.text.replace(/\u00a0/g, ' ')).toBe('53% of Japanese people use LINE.');
    expect('ja-2021-ol-2b-ii' in aliases).toBe(false);
    expect(card('3a-4-iv').questionText).toContain('Which of these is not mentioned about Kenta’s club?');
    expect(point('3a-4-iv').rows[0]).toMatchObject({ verbatim: '(c) the teacher is not strict', marks: 3 });
    expect(review.selectors).toContainEqual(expect.objectContaining({ document: 'scheme', page: 8, row: 8, group: 1, text: '(c) the teacher is not strict' }));
    expect(review.consolidations.find(entry => entry.canonicalId === 'ja-2021-ol-2b')!.legacyIds).toHaveLength(5);
    const mistaken = resolvedExclusions.resolved.find(entry => entry.previousExclusion.ref === '2021 OL Section LA Q2(iii)')!;
    expect(mistaken.reviewedCardIds).toEqual(['i', 'ii', 'iii'].map(roman => `ja-2021-ol-la-3-${roman}`));
    expect(mistaken.resolution).toContain('fabricated Q2(iii)');
  });

  it('retains the required link cells, descending pools, partial endpoints and open culture credit', () => {
    expect(point('1-1').rows.map(row => row.verbatim)).toEqual(['6', '2', '5', '10', '7']);
    expect(point('1-1').rows.map(row => row.marks)).toEqual(Array(5).fill(2));
    for (const suffix of ['1-5', '1-6', '2a-2']) {
      expect(point(suffix).rows[0]).toMatchObject({ kind: 'anyN', group: { claimMax: 2, perOptionSteps: [2, 1] } });
    }
    expect(point('1-7-i').rows.map(row => [row.verbatim, row.marks])).toEqual([['4', 1], ['11 years', 1]]);
    expect(point('1-7-ii').rows[0]).toMatchObject({ verbatim: '7,800 yen', marks: 3 });
    expect(point('3a-1').rows.map(row => [row.verbatim, row.marks])).toEqual([['3rd year', 2], ['High School', 1]]);
    expect(point('2d').rows[0]).toMatchObject({ verbatim: UNPRINTED_ANSWER, unprinted: true, marks: 4, permittedMarks: [0, 2, 4] });
    expect(point('2d').rows[0].parts?.map(part => part.marks)).toEqual([2, 2]);
    expect(point('3a-3').rows[0]).toMatchObject({ kind: 'anyN', group: { claimMax: 2, perOption: 2, options: ['Small', 'teacher is Australian', 'Teacher is funny and kind', 'club is twice a week', 'club is on Tuesdays and Thursdays', 'speak English'] } });
  });

  it('binds the four actual missing phone digits to one mark each and retains paper listening references', () => {
    const phone = point('lc-v');
    expect(phone.totalMarks).toBe(4);
    expect(phone.rows.map(row => [row.verbatim, row.marks])).toEqual([['4', 1], ['6', 1], ['9', 1], ['2', 1]]);
    for (const row of phone.rows) expect(row.contextNote).toContain('03-4160-9725 (1 mark for each correct number)');
    expect(phone.questionRef).toBe('2021 OL Section LC Q(v)');
    expect(point('ld-iv').questionRef).toBe('2021 OL Section LD Q(iv)');
    expect(point('ld-iv').rows[0].verbatim).toBe('(c) Maths');
    expect(point('ld-iv').rows[0].contextNote).toContain('misprinted(vi)');
    expect(point('la-3-iii').rows[0]).toMatchObject({ kind: 'anyN', group: { claimMax: 1, perOption: 2, options: ['Uses phone app', 'duolingo', 'practices with her brother'] } });
  });

  it('caps each chosen summer response expression at its own content mark independently', () => {
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
    for (let content = 0; content <= 4; content++) {
      scores['language:item-1-content'] = content;
      expect(languagePointsMarks(rubric, scores)).toBe(32 + 2 * content);
    }
    scores['language:item-1-expression'] = 1;
    expect(languagePointsMarks(rubric, scores)).toBe(37);
    scores['language:item-6-content'] = 0;
    expect(languagePointsMarks(rubric, scores)).toBe(37);
    expect(rubric.groups[0].criteria![1].bands?.map(band => band.marks)).toEqual([[1], [2, 3], [4]]);
    expect(rubric.markingGuideNote).toContain('Expression mark cannot be higher than content mark.');
    expect(rubric.groups[6].label).toContain('なつ休みの後');
    expect(rubric.groups[7].label).toContain('なつ休みが好きですか。');
    for (const suffix of ['4', '5']) expect(card(suffix).questionText).toContain('Answer either Question 4 or Question 5.');
    expect(census.candidateMaximum).toMatchObject({ publishedWritten: 160, publishedListening: 100, publishedTotal: 260 });
  });

  it('binds exactly 26 reading and 29 listening language rules to their original selectors', () => {
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(55);
    expect(cards.filter(card => card.answerLanguageRule?.penalizedLanguage === 'Japanese')).toHaveLength(29);
    for (const found of cards) {
      expect(found.extraneousMaterialRule).toBeUndefined();
      if (['4', 'Q5'].includes(found.section!)) {
        expect(found.answerLanguageRule).toBeUndefined();
        continue;
      }
      const page = found.audioMaterial ? 3 : 5;
      const source = review.selectors.find(selector => selector.document === 'scheme' && selector.page === page && selector.row === 1)!;
      expect(found.answerLanguageRule).toEqual({ otherLanguageMultiplier: 0.5, sourceText: source.text, schemePages: [page], ...(found.audioMaterial ? { penalizedLanguage: 'Japanese' } : {}) });
    }
  });

  it('retains every multiple-choice alternative and all seven full source crops', () => {
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(7);
    for (const suffix of ['la-1-ii', 'la-1-iii', 'la-2-ii', 'la-3-i', 'la-3-ii', 'lb-1-i', 'lb-1-iii', 'lb-1-v', 'lb-2-i', 'lb-2-ii', 'lc-i', 'lc-iii', 'lc-iv', 'lc-vi', 'lc-vii', 'ld-i', 'ld-iii', 'ld-iv', 'ld-v', 'ld-vii']) {
      for (const label of ['a', 'b', 'c', 'd']) expect(card(suffix).questionText, suffix).toContain(`(${label})`);
    }
    expect(card('la-1-i').questionText).toBe('Where does Maria live?');
    expect(card('la-2-i').questionText).toBe('What country is Max from?');
    expect(card('lc-i').stem).toContain('You will hear an interview with Mr. Tanaka, manager of Robot Restaurant.');
    expect(card('3a-5').questionRef).toBe('2021 OL Section 3A Q5');
  });

  it('retains original Atlas identities and appends the omitted Q5 expression guidance page', () => {
    const tags = ['japanese.json', 'japanese-written-2019-2022.json'].flatMap(file => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/topic-tags/tags/${file}`), 'utf8')));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      expect(task.paperPages, runtime.id).toContain(group.pP);
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2021 && paper.fileid === task.atlas.fileid);
      expect(tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber).primary, runtime.id).toBe(runtime.topicId);
      expect(sidecar.band).toEqual([1, 16]);
    }
    expect(map('LC058GLP000BV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 24 }, (_, i) => String(i + 1)));
    expect(map('LC058GLPA00BV.pdf').q.map(question => question.n)).toEqual(['1', '2', '3', '4']);
    expect(map('LC058GLP000BV.pdf').q.find(question => question.n === '24')!.region.map(region => region.p)).toEqual([10, 11]);
  });
});
