import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as higher } from '../components/MarkBank/cards/japanese/higher';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import rawCards from '../components/MarkBank/cards/japanese/reviewed.json';
import aliases from '../components/MarkBank/cards/japanese/aliases.json';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import census from '../scripts/markbank/authoring/reviews/japanese-2014-hl-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2014-hl.json';
import { tariffReconciles } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
import { languageCriterionValue, languageLengthId, languageMarks, languagePointsMarks, languageWritingMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = higher.filter(card => card.year === 2014);
const idFor = (key: (string | number | null)[]) => `ja-2014-hl-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2014-hl-${suffix}`)!;
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
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2014/${fileid}.json`), 'utf8'));

describe('Japanese 2014 Higher independent source review', () => {
  it('covers all 57 independent tasks and every physical source page', () => {
    expect(cards).toHaveLength(57);
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

  it('adds 57 new tasks while keeping the frozen 600 identities and original files', () => {
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
    expect(originalIds.some(id => id.startsWith('ja-2014-'))).toBe(false);
    expect(review.consolidations).toEqual([]);
    expect(Object.keys(aliases)).toHaveLength(391);
    // Add independently reviewed2011OL49,2010HL66 and2010OL61; frozen600/391 stay unchanged.
    expect(rawCards.filter(card => !originalIds.includes(card.id))).toHaveLength(1556 + 49 + 66 + 61);
    expect(live.size).toBe(600 + 1556 + 49 + 66 + 61 - 391);
  });

  it('keeps all required link, kanji and grammar pools complete', () => {
    for (const [suffix, count] of [['1a-1', 6], ['2b-1', 5], ['2b-2', 5], ['2c-1', 5], ['2c-2', 5], ['3c', 5], ['3d', 10]] as const) {
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
    for (const continuation of ['たい です。', '前に、大', 'かもしれません。', 'り、音', 'ください。']) expect(card('2c-2').questionText).toContain(continuation);
    const pairs = card('3c');
    if (pairs.kind !== 'rubric' || pairs.rubric.system !== 'language-points') throw new Error('Expected pairs');
    expect(pairs.rubric.groups.map(group => group.rows.map(row => row.marks))).toEqual(Array(5).fill([1, 1]));
    expect(pairs.rubric.groups.map(group => group.rows[0].text)).toEqual(['だします', 'いま', 'たかい', 'にんき', 'でんしゃ']);
    for (const literal of ['a. にんき', 'b. にんき', 'b. でんしゃ', 'a. でんしゃ']) expect(pairs.rubric.markingGuideNote).toContain(literal);
    expect(census.sourceDiscrepancies.find(item => item.task === 'Q3C')?.description).toContain('hiragana readings agree');
  });

  it('retains both complete tables with given cells, partial credit and distinct descending details', () => {
    const profiles = point('2a-1');
    expect(profiles.taskGroups?.map(group => group.marks)).toEqual([2, 2, 1, 2, 1, 2, 2]);
    expect(profiles.rows).toHaveLength(9);
    expect(profiles.rows.filter(row => row.kind === 'criterion').map(row => row.permittedMarks)).toEqual([[0, 1, 2], [0, 1, 2]]);
    expect(profiles.questionText).toContain('Makoto Hayashi');
    expect(JSON.stringify(profiles.rows)).toContain('Makoto Takashi');
    expect(JSON.stringify(profiles.rows)).toContain('Africa 0 marks');
    expect(profiles.rows.map(row => row.verbatim)).not.toContain('Kildare');
    expect(profiles.rows.map(row => row.verbatim)).not.toContain('December');
    const holidays = point('la');
    expect(holidays.taskGroups?.map(group => group.marks)).toEqual([1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 3, 1]);
    const trips = holidays.rows.filter(row => row.kind === 'anyN' && row.group.perOptionSteps);
    expect(trips.map(row => row.kind === 'anyN' && row.group.perOptionSteps)).toEqual([[2, 1], [2, 1]]);
    const cycling = holidays.rows.filter(row => row.kind === 'criterion');
    expect(cycling.map(row => row.marks)).toEqual([2, 1]);
    expect(cycling.map(row => row.kind === 'criterion' && row.permittedMarks)).toEqual([[0, 1, 2], [0, 1]]);
    expect(cycling.every(row => row.contextNote?.includes('cycled 1 mark'))).toBe(true);
    expect(cycling.every(row => row.contextNote?.includes('never count a partial and full version'))).toBe(true);
  });

  it('prices nested amenities only at zero or two and caps the complete Sky Tree pool at two concepts', () => {
    const found = card('lb-1-ii');
    if (found.kind !== 'rubric' || found.rubric.system !== 'language-points') throw new Error('Expected nested pool');
    const rubric = found.rubric;
    expect(rubric.count).toBe(2);
    expect(rubric.groups.map(group => group.id)).toEqual(['record', 'height', 'amenities']);
    expect(rubric.groups[1].rows[0].text).toBe('630 meters');
    expect(rubric.groups[2].criteria?.[0]).toMatchObject({ maxMarks: 2, permittedMarks: [0, 2], guidance: ['has restaurants, shops and cafes (must have any two)'] });
    const selected: LanguageScores = { 'language:group:amenities': 1 };
    for (const invalid of [0, 1, 3]) expect(languageMarks(found, { ...selected, 'language:amenities': invalid })).toBe(0);
    expect(languageMarks(found, { ...selected, 'language:amenities': 2 })).toBe(2);
    expect(languageMarks(found, { ...selected, 'language:amenities': 2, 'language:other-language:group:amenities': 1 })).toBe(1);
    const all: LanguageScores = { ...selected, 'language:amenities': 2, 'language:group:record': 1, 'language:row:record:answer': 1, 'language:group:height': 1, 'language:row:height:answer': 1 };
    expect(languageMarks(found, all)).toBe(4);
    expect(languageMarks(found, { ...selected, 'language:amenities': 2, 'language:group:height': 1, 'language:row:height:answer': 1 })).toBe(4);
    expect(review.selectors.some(selector => selector.document === 'scheme' && selector.page === 3 && selector.text.includes('must have any two'))).toBe(true);
  });

  it('retains published full and partial tariffs without adding awards', () => {
    expect(point('1a-5-ii').rows.map(row => [row.verbatim, row.marks])).toEqual([['Eddy / Edii', 1], ['Jones / Jyoonuzu', 1]]);
    expect(point('1b-1').rows.map(row => row.marks)).toEqual([1, 1]);
    expect(point('1b-2').rows[0]).toMatchObject({ kind: 'criterion', marks: 2, permittedMarks: [0, 1, 2] });
    expect(point('3a-3-i').rows[0]).toMatchObject({ kind: 'criterion', marks: 3, permittedMarks: [0, 1, 3] });
    expect(marksClaimed(point('3a-3-i'), { 'r-1': 2 })).toBe(0);
    expect(marksClaimed(point('3a-3-i'), { 'r-1': 1 })).toBe(1);
    expect(point('2a-2-iii').rows.map(row => row.marks)).toEqual([1, 1]);
    expect(point('2a-3-iii').answerVariants?.map(variant => variant.rows.map(row => row.marks))).toEqual([[1, 1], [2]]);
    expect(point('2a-4').rows.map(row => row.marks)).toEqual([2, 2]);
    expect(point('lb-1-i').rows.map(row => row.marks)).toEqual([1, 1, 1]);
    expect(point('lb-1-iii').rows.map(row => row.marks)).toEqual([2, 1]);
    const phone = point('lb-1-iv');
    expect(phone.rows).toHaveLength(1);
    expect(phone.rows[0]).toMatchObject({ marks: 3 });
    expect(phone.rows[0].verbatim.replace(/[–\s]/g, '')).toBe('0358226405');
    expect(phone.rows[0].contextNote).toContain('no separate published tariff');
    expect(point('lc-1-ii').rows.map(row => row.marks)).toEqual([2, 1]);
    expect(point('lc-1-ii').rows[0]).toMatchObject({ kind: 'criterion', permittedMarks: [0, 1, 2] });
    expect(point('ld-v').rows.map(row => row.marks)).toEqual([1, 1]);
    for (const suffix of ['3a-1-i', 'lb-3-i', 'lb-3-ii', 'lc-2-i', 'lc-2-ii']) {
      const row = point(suffix).rows[0];
      expect(row.kind === 'anyN' && row.group.perOptionSteps).toEqual([2, 1]);
    }
    const performer = card('lb-2');
    if (performer.kind !== 'rubric' || performer.rubric.system !== 'language-points') throw new Error('Expected performer pool');
    expect(performer.rubric.groups).toHaveLength(3);
    expect(performer.rubric.groups.every(group => group.criteria?.[0].guidance?.join(' ').includes('He was on America’s got talent'))).toBe(true);
    expect(languageMarks(performer, { 'language:group:response-1': 1, 'language:response-1': 1, 'language:group:response-2': 1, 'language:response-2': 2 })).toBe(3);
  });

  it('binds language and extraneous-material rules only to the printed scope', () => {
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(23);
    expect(cards.filter(card => card.audioMaterial)).toHaveLength(19);
    const readingRules = cards.filter(card => !card.audioMaterial && card.answerLanguageRule);
    expect(readingRules.map(card => card.id)).toEqual([1, 2, 3, 4].map(q => `ja-2014-hl-1b-${q}`));
    for (const found of cards.filter(card => card.answerLanguageRule)) {
      expect(found.answerLanguageRule?.penalizedLanguage).toBe('Japanese');
      expect(found.answerLanguageRule?.otherLanguageMultiplier).toBe(0.5);
      expect(review.selectors.some(selector => selector.document === 'scheme' && selector.page === (found.audioMaterial ? 3 : 7) && selector.text === found.answerLanguageRule?.sourceText)).toBe(true);
      if (found.audioMaterial) expect(found.answerLanguageRule?.sourceText).toContain('romaji or Japanese script');
    }
    expect(cards.filter(card => card.extraneousMaterialRule).map(card => card.id)).toEqual(['i', 'ii', 'iii', 'iv'].map(roman => `ja-2014-hl-2a-2-${roman}`));
    for (const found of cards.filter(card => card.extraneousMaterialRule)) expect(found.extraneousMaterialRule?.schemePages).toEqual([7]);
    for (const found of cards.filter(card => /ja-2014-hl-(?:1a|[2345])/.test(card.id))) expect(found.answerLanguageRule).toBeUndefined();
  });

  it('keeps all eight speech headings, local discretionary marks and strict lower-expression thresholds', () => {
    expect(writing('4').criteria.map(criterion => criterion.maxMarks)).toEqual([6, 6, 6, 2, 20]);
    expect(writing('5').criteria.map(criterion => criterion.maxMarks)).toEqual([6, 1, 6, 1, 6, 1, 6, 1, 2, 30]);
    expect(card('4').questionText).toContain('Christmas day');
    expect(card('4').questionText).toContain('your birthday');
    expect(card('5').questionText).toContain('ANY 4');
    expect(card('5').questionText).toContain('Break time');
    expect(card('5').questionText).toContain('Club activities');
    expect(writing('5').markingGuideNote).toContain('headings 1-6');
    for (const [suffix, normal, lower, length, threshold] of [['4', 20, 15, 150, 10], ['5', 30, 20, 200, 15]] as const) {
      const rubric = writing(suffix);
      const scores: LanguageScores = { [languageLengthId('characters')]: 500 };
      for (const criterion of rubric.criteria) scores[`language:${criterion.id}`] = criterion.maxMarks;
      expect(languageWritingMarks(rubric, scores)).toBe(normal * 2);
      scores[languageLengthId('characters')] = length - 1;
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(lower);
      scores[languageLengthId('characters')] = length;
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(normal);
      let remaining: number = threshold - 1;
      const content = rubric.criteria.filter(criterion => criterion.id !== 'expression');
      for (const criterion of content) {
        const award = Math.min(criterion.maxMarks, remaining);
        scores[`language:${criterion.id}`] = award;
        remaining -= award;
      }
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(lower);
      const next = content.find(criterion => (scores[`language:${criterion.id}`] ?? 0) < criterion.maxMarks)!;
      scores[`language:${next.id}`] = (scores[`language:${next.id}`] ?? 0) + 1;
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(normal);
      const expression = rubric.criteria.find(criterion => criterion.id === 'expression')!;
      for (const band of [...expression.bands!, ...expression.limits![0].bands!]) expect(band.guidance.join(' ').length).toBeGreaterThan(100);
    }
  });

  it('retains eleven written and four aural Atlas anchors and eleven complete source crops', () => {
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(11);
    const tags = JSON.parse(readFileSync(resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'), 'utf8'));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      expect(task.paperPages, runtime.id).toContain(group.pP);
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2014 && paper.fileid === task.atlas.fileid);
      const topic = tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber);
      expect([topic.primary, topic.secondary], runtime.id).toContain(runtime.topicId);
      expect(sidecar.band).toEqual([1, 20]);
    }
    expect(map('LC058ALP000EV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 11 }, (_, i) => String(i + 1)));
    expect(map('LC058ALPA00EV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 4 }, (_, i) => String(i + 1)));
    expect(JSON.stringify(cards)).not.toContain('�');
  });
});
