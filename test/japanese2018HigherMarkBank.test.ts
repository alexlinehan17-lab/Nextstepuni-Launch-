import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as higher } from '../components/MarkBank/cards/japanese/higher';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import rawCards from '../components/MarkBank/cards/japanese/reviewed.json';
import aliases from '../components/MarkBank/cards/japanese/aliases.json';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import census from '../scripts/markbank/authoring/reviews/japanese-2018-hl-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2018-hl.json';
import { tariffReconciles } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
import { languageCriterionValue, languagePointsMarks, languageWritingMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = higher.filter(card => card.year === 2018);
const idFor = (key: (string | number | null)[]) => `ja-2018-hl-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2018-hl-${suffix}`)!;
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
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2018/${fileid}.json`), 'utf8'));

describe('Japanese 2018 Higher independent source review', () => {
  it('covers all 61 independent tasks and every physical source page', () => {
    expect(cards).toHaveLength(61);
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

  it('adds 61 new tasks while keeping the frozen 600 identities and original files', () => {
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
    expect(originalIds.some(id => id.startsWith('ja-2018-'))).toBe(false);
    expect(review.consolidations).toEqual([]);
    expect(Object.keys(aliases)).toHaveLength(391);
    expect(rawCards.filter(card => !originalIds.includes(card.id))).toHaveLength(845);
    expect(live.size).toBe(600 + 845 - 391);
  });

  it('keeps every required pool whole and every original alternative', () => {
    for (const [suffix, count] of [['1a-1', 6], ['2b', 5], ['2c', 10], ['3c-1', 5], ['3c-2', 5], ['3d-1', 5], ['3d-2', 5]] as const) {
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
    }
    const pairs = card('2b');
    if (pairs.kind !== 'rubric' || pairs.rubric.system !== 'language-points') throw new Error('Expected pairs');
    expect(pairs.rubric.groups.map(group => group.rows.map(row => row.marks))).toEqual(Array(5).fill([1, 1]));
    expect(pairs.rubric.groups.map(group => group.rows[0].text)).toEqual(['(b)', '(d)', '(a)', '(c)', '(a)']);
    const grammar = card('2c');
    if (grammar.kind !== 'rubric' || grammar.rubric.system !== 'language-points') throw new Error('Expected grammar');
    expect(grammar.rubric.groups.map(group => group.rows[0].text)).toEqual(['に／へ', 'に／から／の', 'を', 'と', 'の', 'に／には', 'で', 'から', 'まで', 'より']);
  });

  it('preserves nine unfilled accommodation cells and the complete twelve-cell listening table', () => {
    expect(point('2a').rows).toHaveLength(9);
    expect(point('2a').taskGroups?.map(group => group.marks)).toEqual([4, 4, 3]);
    expect(point('2a').rows.map(row => row.verbatim)).not.toContain('Asakusa');
    expect(point('2a').rows.map(row => row.verbatim)).not.toContain('alone');
    expect(point('2a').rows.map(row => row.verbatim)).not.toContain('Lives abroad');
    expect(point('2a').rows[2].group?.options).toEqual(['Yoshi-san is friendly', 'owns a ramen shop']);
    const table = point('la');
    expect(table.rows).toHaveLength(12);
    expect(table.taskGroups?.map(group => group.marks)).toEqual([1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2]);
    expect(table.rows[10].group?.options.map(option => option.trim())).toEqual(['Online shopping', 'shopping for clothes', 'camera or take photos']);
    expect(table.rows[11].verbatim).toBe('Using phone while driving/walking & using phone/talking loudly on subway');
  });

  it('keeps sunrise-only partial credit within one selected location concept', () => {
    const found = card('2a-2-iii');
    if (found.kind !== 'rubric' || found.rubric.system !== 'language-points') throw new Error('Expected location pool');
    const rubric = found.rubric;
    expect(rubric.count).toBe(2);
    expect(rubric.groups).toHaveLength(4);
    expect(rubric.groups[3].criteria?.[0]).toMatchObject({ id: 'sea-or-sunrise', maxMarks: 2, permittedMarks: [0, 1, 2] });
    expect(rubric.groups[3].criteria?.[0].guidance).toEqual([expect.stringContaining('sea (sunrise 1 mark)')]);
    const scores: LanguageScores = { 'language:group:location-1': 1, 'language:row:location-1:answer': 1, 'language:group:location-4': 1, 'language:sea-or-sunrise': 1 };
    expect(languagePointsMarks(rubric, scores)).toBe(3);
    scores['language:sea-or-sunrise'] = 2;
    expect(languagePointsMarks(rubric, scores)).toBe(4);
    scores['language:group:location-2'] = 1;
    scores['language:row:location-2:answer'] = 1;
    expect(languagePointsMarks(rubric, scores)).toBe(4);
    expect(rubric.markingGuideNote).toContain('do not select both as different details');
  });

  it('keeps source partials, the whole phone tariff and all component awards', () => {
    for (const suffix of ['lb-1-i', 'lb-2-i']) {
      const found = point(suffix);
      expect(found.rows[0].permittedMarks).toEqual([0, 1, 2]);
      expect(marksClaimed(found, { 'r-1': 1 })).toBe(1);
      expect(marksClaimed(found, { 'r-1': 2 })).toBe(2);
    }
    expect(point('lb-1-i').rows[0].contextNote).toContain('rugby/World Cup, 1 mark');
    expect(point('lb-2-i').rows[0].contextNote).toBe('(guitar, 1 mark)');
    expect(point('lb-1-iv').rows[0]).toMatchObject({ verbatim: '03-3573-8205', marks: 2 });
    expect(point('lb-1-iv').rows[0].parts).toBeUndefined();
    expect(point('lb-1-iv').rows[0].permittedMarks).toBeUndefined();
    expect(point('lb-1-iii').rows.map(row => [row.verbatim, row.marks])).toEqual([['14th', 1], ['July', 1]]);
    expect(point('lb-2-ii').rows[0].group?.options.at(-1)).toContain('any 2 types required');
    expect(point('lc-1-ii').rows[0].group).toMatchObject({ claimMax: 3, perOption: 2 });
    expect(point('lc-2-ii').rows.map(row => row.marks)).toEqual([2, 2]);
    expect(point('ld-1-iii').rows.map(row => [row.verbatim, row.marks])).toEqual([['Kyoto', 2], ['Medicine', 2]]);
    expect(point('ld-2-i').rows.map(row => row.marks)).toEqual([2, 2]);
    expect(point('ld-2-i').rows[1].verbatim).toContain('for next Monday');
    expect(point('2a-3').rows.map(row => row.marks)).toEqual([1, 1, 1, 1]);
  });

  it('binds only four reading and twenty-two listening Japanese rules plus three extraneous rules', () => {
    const language = cards.filter(card => card.answerLanguageRule);
    expect(language).toHaveLength(26);
    for (const found of language) {
      const rule = found.answerLanguageRule!;
      expect(rule).toMatchObject({ otherLanguageMultiplier: 0.5, penalizedLanguage: 'Japanese', schemePages: [found.audioMaterial ? 3 : 7] });
      expect(review.selectors.some(selector => selector.document === 'scheme' && rule.schemePages.includes(selector.page) && selector.text === rule.sourceText)).toBe(true);
    }
    for (const found of cards.filter(card => !card.audioMaterial && !card.id.startsWith('ja-2018-hl-1b-'))) expect(found.answerLanguageRule).toBeUndefined();
    expect(cards.filter(card => card.extraneousMaterialRule).map(card => card.id)).toEqual(['i', 'ii', 'iii'].map(roman => `ja-2018-hl-2a-1-${roman}`));
    for (const found of cards.filter(card => card.extraneousMaterialRule)) expect(found.extraneousMaterialRule).toMatchObject({ multiplier: 0.5, schemePages: [8] });
  });

  it('applies the distinct 40/60 writing allocations and both exact expression thresholds', () => {
    expect(writing('4').criteria.map(criterion => criterion.maxMarks)).toEqual([9, 9, 1, 1, 20]);
    expect(writing('4').criteria.map(criterion => criterion.id)).toEqual(['point-i', 'point-ii', 'discretionary-i', 'discretionary-ii', 'expression']);
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
    expect(card('4').questionText.replace(/\s+/g, ' ')).toContain('(a) OR (b)');
    expect(card('5').questionText.replace(/\s+/g, ' ')).toContain('ANY 4');
    expect(card('5').questionText.replace(/\s+/g, ' ')).toContain('320 Japanese characters');
  });

  it('retains all 29 written and four listening Atlas anchors and source crops', () => {
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(11);
    const tags = ['japanese.json'].flatMap(file => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/topic-tags/tags/${file}`), 'utf8')));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      expect(task.paperPages, runtime.id).toContain(group.pP);
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2018 && paper.fileid === task.atlas.fileid);
      expect(tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber).primary, runtime.id).toBe(runtime.topicId);
      expect(sidecar.band).toEqual([1, 20]);
    }
    expect(map('LC058ALP000EV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 29 }, (_, i) => String(i + 1)));
    expect(map('LC058ALPA00EV.pdf').q.map(question => question.n)).toEqual(['1', '2', '3', '4']);
    expect(map('LC058ALPA00EV.pdf').q.find(question => question.n === '4')?.region).toEqual([{ p: 5, r: [0, 0.6129, 1, 1] }, { p: 6, r: [0, 0, 1, 0.34] }]);
  });
});
