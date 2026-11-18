import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as higher } from '../components/MarkBank/cards/japanese/higher';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import rawCards from '../components/MarkBank/cards/japanese/reviewed.json';
import aliases from '../components/MarkBank/cards/japanese/aliases.json';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import census from '../scripts/markbank/authoring/reviews/japanese-2016-hl-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2016-hl.json';
import { tariffReconciles } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
import { languageCriterionValue, languageLengthId, languagePointsMarks, languageWritingMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = higher.filter(card => card.year === 2016);
const idFor = (key: (string | number | null)[]) => `ja-2016-hl-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2016-hl-${suffix}`)!;
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
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2016/${fileid}.json`), 'utf8'));

describe('Japanese 2016 Higher independent source review', () => {
  it('covers all 56 independent tasks and every physical source page', () => {
    expect(cards).toHaveLength(56);
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

  it('adds 56 new tasks while keeping the frozen 600 identities and original files', () => {
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
    expect(originalIds.some(id => id.startsWith('ja-2016-'))).toBe(false);
    expect(review.consolidations).toEqual([]);
    expect(Object.keys(aliases)).toHaveLength(391);
    expect(rawCards.filter(card => !originalIds.includes(card.id))).toHaveLength(1556);
    expect(live.size).toBe(600 + 1556 - 391);
  });

  it('keeps every required floor, kanji and particle pool whole', () => {
    for (const [suffix, count] of [['1a-1', 6], ['2b', 5], ['2c', 10], ['3c-1', 5], ['3c-2', 5], ['3d-1', 5], ['3d-2', 5]] as const) {
      const found = card(suffix);
      if (found.kind !== 'rubric' || found.rubric.system !== 'language-points') throw new Error('Expected required pool');
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
    const grammar = card('2c');
    if (grammar.kind !== 'rubric' || grammar.rubric.system !== 'language-points') throw new Error('Expected particles');
    expect(grammar.rubric.groups.map(group => group.rows[0].text)).toEqual(['で/ の', 'を', 'から', 'まで', 'に', 'で', 'と', 'に', 'より', 'で']);
    expect(point('1a-5').rows[0].contextNote).toContain('question 5 is explicitly printed');
    for (const continuation of ['ほうがいいです。', 'もいいですか。', '前に、おみやげを買います。']) {
      expect(card('3d-2').questionText).toContain(continuation);
    }
  });

  it('retains partial instruments and Guinness-only within their full answer slots', () => {
    for (const [suffix, count, groups, partialId, maximum] of [['1a-3-i', 2, 4, 'instrument-1', 4], ['lc-2', 4, 9, 'fact-9', 8]] as const) {
      const found = card(suffix);
      if (found.kind !== 'rubric' || found.rubric.system !== 'language-points') throw new Error('Expected choose pool');
      expect(found.rubric.count).toBe(count);
      expect(found.rubric.groups).toHaveLength(groups);
      const group = found.rubric.groups.find(group => group.id === partialId)!;
      expect(group.answerCount).toBe(1);
      expect(group.rows.map(row => row.marks)).toEqual([2, 1]);
      const scores: LanguageScores = { [`language:group:${partialId}`]: 1, [`language:row:${partialId}:partial`]: 1 };
      expect(languagePointsMarks(found.rubric, scores)).toBe(1);
      scores[`language:row:${partialId}:full`] = 1;
      expect(languagePointsMarks(found.rubric, scores)).toBe(2);
      for (const group of found.rubric.groups) {
        scores[`language:group:${group.id}`] = 1;
        scores[`language:row:${group.id}:full`] = 1;
      }
      expect(languagePointsMarks(found.rubric, scores)).toBe(maximum);
    }
    const sharran = card('lc-2');
    if (sharran.kind !== 'rubric' || sharran.rubric.system !== 'language-points') throw new Error('Expected Sharran');
    expect(sharran.rubric.groups[8].rows.map(row => row.text)).toEqual(['biggest female sportswoman in world', 'in Guinness book']);
    expect(sharran.rubric.markingGuideNote).toContain('source-context evidence');
    expect(point('2a-2-ii').rows[0]).toMatchObject({ kind: 'criterion', marks: 2, permittedMarks: [0, 1, 2] });
    expect(point('2a-2-ii').rows[0].contextNote).toContain('モデル 1 mark');
  });

  it('keeps required tables and their printed component allocations intact', () => {
    const bags = point('2a-1');
    expect(bags.rows).toHaveLength(8);
    expect(bags.taskGroups?.map(group => group.marks)).toEqual([1, 2, 1, 1, 2, 1, 1, 2]);
    expect(bags.taskGroups?.some(group => group.label.startsWith('Hitomi') && group.label.includes('Where'))).toBe(false);
    expect(bags.rows.filter(row => row.kind === 'anyN').map(row => row.group?.claimMax)).toEqual([2, 2, 2]);
    const lotto = point('la');
    expect(lotto.rows).toHaveLength(14);
    expect(lotto.taskGroups?.map(group => group.marks)).toEqual([2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1]);
    expect(lotto.rows.slice(0, 2).map(row => [row.verbatim, row.marks])).toEqual([['Buy a new / red / Toyota', 1], ['sports car', 1]]);
    expect(lotto.rows.slice(5, 7).map(row => [row.verbatim, row.marks])).toEqual([['Travel to Asia', 1], ['live in Vietnam', 1]]);
    const weather = point('lc-3');
    expect(weather.rows).toHaveLength(2);
    expect(weather.rows.map(row => row.group?.claimMax)).toEqual([2, 2]);
    expect(marksClaimed(weather, {}, { 'r-1': [0, 1, 2], 'r-2': [0, 1, 2] })).toBe(4);
    expect(weather.questionText).toContain('San Francisco');
    expect(weather.rows.some(row => JSON.stringify(row).includes('28'))).toBe(false);
  });

  it('preserves descending choices, alternative routes and the whole telephone tariff', () => {
    for (const suffix of ['2a-3-ii', '3a-4', 'lb-2-ii']) {
      const found = point(suffix);
      expect(found.rows[0].group?.perOptionSteps).toEqual([2, 1]);
      expect(marksClaimed(found, {}, { 'r-1': [0] })).toBe(2);
      expect(marksClaimed(found, {}, { 'r-1': [0, 1, 2] })).toBe(3);
    }
    expect(point('lb-2-ii').rows[0].group?.options).toHaveLength(4);
    expect(point('lb-2-ii').rows[0].group?.options[0]).toContain('(at back / far from stage)');
    expect(point('lb-1-iii').rows.map(row => row.marks)).toEqual([2, 1, 1]);
    const phone = point('lc-1-iv');
    expect(phone.rows).toHaveLength(1);
    expect(phone.rows[0]).toMatchObject({ kind: 'point', marks: 4, verbatim: '0570-064-110' });
    expect(phone.rows[0].contextNote).toContain('no per-digit allocation');
    const translation = point('2a-4');
    expect(translation.rows.map(row => row.route)).toEqual(['A', 'A', 'B', 'B']);
    expect(marksClaimed(translation, Object.fromEntries(translation.rows.map(row => [row.id, 1])))).toBe(4);
    const english = point('3a-2');
    expect(english.rows.map(row => row.route)).toEqual(['A', 'B', 'B']);
    expect(marksClaimed(english, { 'r-1': 1, 'r-2': 1 }, { 'r-3': [0, 1, 2] })).toBe(3);
    expect(marksClaimed(english, { 'r-2': 1 }, {})).toBe(2);
  });

  it('keeps location/time and item/person partials inside at most two responses', () => {
    for (const suffix of ['ld-iii', 'ld-vii']) {
      const found = card(suffix);
      if (found.kind !== 'rubric' || found.rubric.system !== 'language-points') throw new Error('Expected components');
      expect(found.questionRef).toBe(`2016 HL Section LD Q(${suffix.slice(3)})`);
      expect(found.rubric.count).toBe(2);
      const group = found.rubric.groups[1];
      expect(group.rows.map(row => row.marks)).toEqual([1, 1]);
      const scores: LanguageScores = { [`language:group:${group.id}`]: 1, [`language:row:${group.id}:${group.rows[0].id}`]: 1 };
      expect(languagePointsMarks(found.rubric, scores)).toBe(1);
      scores[`language:row:${group.id}:${group.rows[1].id}`] = 1;
      expect(languagePointsMarks(found.rubric, scores)).toBe(2);
      for (const group of found.rubric.groups) {
        scores[`language:group:${group.id}`] = 1;
        for (const row of group.rows) scores[`language:row:${group.id}:${row.id}`] = 1;
      }
      expect(languagePointsMarks(found.rubric, scores)).toBe(4);
    }
  });

  it('emits only 25 named-language and three extraneous conditions from this scheme', () => {
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(25);
    for (const found of cards.filter(card => card.answerLanguageRule)) {
      expect(found.answerLanguageRule).toMatchObject({ otherLanguageMultiplier: 0.5, penalizedLanguage: 'Japanese' });
      expect(review.selectors.some(selector => selector.document === 'scheme' && selector.text === found.answerLanguageRule?.sourceText)).toBe(true);
      expect(found.audioMaterial || found.id.startsWith('ja-2016-hl-1b-')).toBeTruthy();
    }
    expect(cards.filter(card => card.extraneousMaterialRule).map(card => card.id)).toEqual(['i', 'ii', 'iii'].map(roman => `ja-2016-hl-2a-2-${roman}`));
    for (const suffix of ['2a-3-iii', '3a-4', '3b-1', '3b-2', '4', '5']) {
      expect(card(suffix).answerLanguageRule).toBeUndefined();
      expect(card(suffix).extraneousMaterialRule).toBeUndefined();
    }
  });

  it('uses exact discretionary allocations and the strict diary content threshold', () => {
    for (const suffix of ['4', '5']) {
      const expression = writing(suffix).criteria.find(criterion => criterion.id === 'expression')!;
      for (const band of [...expression.bands!, ...expression.limits![0].bands!]) {
        expect(band.guidance.join(' ')).toContain('Vocabulary');
        expect(band.guidance.join(' ').trim().length).toBeGreaterThan(100);
      }
    }
    expect(writing('4').criteria.map(criterion => criterion.maxMarks)).toEqual([8, 8, 1, 1, 1, 1, 20]);
    expect(writing('5').criteria.map(criterion => criterion.maxMarks)).toEqual([6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 30]);
    for (const [suffix, normal, lower, length, threshold] of [['4', 20, 15, 150, 9], ['5', 30, 20, 200, 15]] as const) {
      const rubric = writing(suffix);
      const scores: LanguageScores = { [languageLengthId('characters')]: 500 };
      for (const criterion of rubric.criteria) scores[`language:${criterion.id}`] = criterion.maxMarks;
      expect(languageWritingMarks(rubric, scores)).toBe(normal * 2);
      scores[languageLengthId('characters')] = length - 1;
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(lower);
      scores[languageLengthId('characters')] = length;
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(normal);
      const content = rubric.criteria.filter(criterion => criterion.id !== 'expression');
      let remaining: number = threshold;
      for (const criterion of content) {
        const award = Math.min(criterion.maxMarks, remaining);
        scores[`language:${criterion.id}`] = award;
        remaining -= award;
      }
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(lower);
      const next = content.find(criterion => scores[`language:${criterion.id}`] < criterion.maxMarks)!;
      scores[`language:${next.id}`] += 1;
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(normal);
    }
    expect(card('4').questionText).toContain('(a) OR (b)');
    expect(card('5').questionText).toContain('ANY 4');
    expect(card('5').questionText).toContain('Things the student should bring with him/her to Ireland');
    expect(writing('4').markingGuideNote).toContain('below 10 (not at 10)');
  });

  it('preserves all 24 written and four listening Atlas anchors with 12 full crops', () => {
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(12);
    const tags = JSON.parse(readFileSync(resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'), 'utf8'));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      expect(task.paperPages, runtime.id).toContain(group.pP);
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2016 && paper.fileid === task.atlas.fileid);
      expect(tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber).primary, runtime.id).toBe(runtime.topicId);
      expect(sidecar.band).toEqual([1, 20]);
    }
    expect(map('LC058ALP000EV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 24 }, (_, i) => String(i + 1)));
    expect(map('LC058ALPA00EV.pdf').q.map(question => question.n)).toEqual(['1', '2', '3', '4']);
    expect(JSON.stringify(cards)).not.toContain('�');
  });
});
