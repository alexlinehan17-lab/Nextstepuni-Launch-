import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as higher } from '../components/MarkBank/cards/japanese/higher';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import rawCards from '../components/MarkBank/cards/japanese/reviewed.json';
import aliases from '../components/MarkBank/cards/japanese/aliases.json';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import census from '../scripts/markbank/authoring/reviews/japanese-2017-hl-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2017-hl.json';
import { tariffReconciles } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
import { languageCriterionValue, languageLengthId, languagePointsMarks, languageWritingMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = higher.filter(card => card.year === 2017);
const idFor = (key: (string | number | null)[]) => `ja-2017-hl-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2017-hl-${suffix}`)!;
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
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2017/${fileid}.json`), 'utf8'));

describe('Japanese 2017 Higher independent source review', () => {
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
    expect(originalIds.some(id => id.startsWith('ja-2017-'))).toBe(false);
    expect(review.consolidations).toEqual([]);
    expect(Object.keys(aliases)).toHaveLength(391);
    // Add independently reviewed2011OL49,2010HL66 and2010OL61; frozen600/391 stay unchanged.
    expect(rawCards.filter(card => !originalIds.includes(card.id))).toHaveLength(1556 + 49 + 66 + 61);
    expect(live.size).toBe(600 + 1556 + 49 + 66 + 61 - 391);
  });

  it('preserves the roman-then-letter paper addresses and complete required pools', () => {
    expect(card('1a-2-a-ii').questionRef).toBe('2017 HL Section 1A Q2(ii)(a)');
    expect(card('1a-2-b-ii').questionRef).toBe('2017 HL Section 1A Q2(ii)(b)');
    for (const [suffix, count] of [['1a-1', 6], ['2b-1', 5], ['2b-2', 5], ['2c-1', 5], ['2c-2', 5], ['3c', 5], ['3d', 10]] as const) {
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
    const pairs = card('3c');
    if (pairs.kind !== 'rubric' || pairs.rubric.system !== 'language-points') throw new Error('Expected pairs');
    expect(pairs.rubric.groups.map(group => group.rows.map(row => row.marks))).toEqual(Array(5).fill([1, 1]));
    expect(pairs.rubric.groups.map(group => group.rows[0].text)).toEqual(['(c)', '(a)', '(c)', '(b)', '(d)']);
    const grammar = card('3d');
    if (grammar.kind !== 'rubric' || grammar.rubric.system !== 'language-points') throw new Error('Expected grammar');
    expect(grammar.rubric.groups.map(group => group.rows[0].text)).toEqual(['が／は', 'と', 'を／も', 'より', 'と', 'に／は', 'で', 'の／は', 'から', 'まで']);
  });

  it('keeps exactly ten unfilled member cells and twelve listening cells', () => {
    const table = point('2a-1');
    expect(table.rows).toHaveLength(10);
    expect(table.taskGroups?.map(group => group.marks)).toEqual([3, 2, 3, 3, 3]);
    expect(table.rows.map(row => row.verbatim)).not.toContain('Ehime');
    expect(table.rows.map(row => row.verbatim)).not.toContain('Shy as a child');
    expect(table.rows.filter(row => row.verbatim.includes('November'))).toHaveLength(1);
    expect(table.rows[0].marks).toBe(1);
    const listening = point('la');
    expect(listening.rows).toHaveLength(13);
    expect(listening.taskGroups?.map(group => group.marks)).toEqual([1, 1, 1, 2, 2, 1, 2, 2, 2, 1, 1, 2]);
    expect(listening.rows.slice(6, 8).map(row => [row.verbatim, row.marks])).toEqual([['2 / college', 1], ['friends', 1]]);
    expect(listening.rows[12].group?.options.map(option => option.trim())).toEqual(['Meet the sister', 'bus tour', 'sightseeing', 'art gallery / museum']);
    expect(listening.rows[12].contextNote).toContain('source-context interpretation');
    expect(marksClaimed(listening, {}, { 'r-13': [1, 2] })).toBe(2);
    expect(marksClaimed(listening, {}, { 'r-13': [1, 2, 3] })).toBe(2);
  });

  it('preserves descending pools, complete phone credit and exclusive partials', () => {
    for (const suffix of ['1b-4', 'lb-1-ii']) {
      const found = point(suffix);
      expect(found.rows[0].group?.claimMax).toBe(2);
      expect(found.rows[0].group?.perOptionSteps).toEqual([2, 1]);
      expect(marksClaimed(found, {}, { 'r-1': [0] })).toBe(2);
      expect(marksClaimed(found, {}, { 'r-1': [0, 1] })).toBe(3);
      expect(marksClaimed(found, {}, { 'r-1': [0, 1, 2] })).toBe(3);
    }
    expect(point('1b-4').rows[0].group?.options).toHaveLength(5);
    const phone = point('lb-1-v');
    expect(phone.totalMarks).toBe(4);
    expect(phone.rows).toHaveLength(1);
    expect(phone.rows[0]).toMatchObject({ kind: 'point', marks: 4, verbatim: '011-547-1929' });
    expect(phone.rows[0].permittedMarks).toBeUndefined();
    expect(phone.rows[0].contextNote).toContain('no per-digit tariff');
    expect(point('lb-1-iii').rows.map(row => row.marks)).toEqual([2, 1, 1]);
    const teacher = point('lc-3-iii');
    expect(teacher.rows[0]).toMatchObject({ kind: 'criterion', marks: 2, permittedMarks: [0, 1, 2], contextNote: 'Ask teacher (1 mark)' });
    expect(teacher.rows[1]).toMatchObject({ marks: 1, contextNote: 'Come back later' });
    expect(marksClaimed(teacher, { 'r-1': 1, 'r-2': 1 })).toBe(2);
    expect(marksClaimed(teacher, { 'r-1': 2, 'r-2': 1 })).toBe(3);
    const happyHour = point('ld-1-iv');
    expect(happyHour.rows).toHaveLength(1);
    expect(happyHour.rows[0].permittedMarks).toEqual([0, 1, 2]);
    expect(marksClaimed(happyHour, { 'r-1': 1 })).toBe(1);
    expect(marksClaimed(happyHour, { 'r-1': 2 })).toBe(2);
    const event = point('ld-2-ii');
    expect(event.rows.slice(0, 2).map(row => row.marks)).toEqual([1, 1]);
    expect(event.rows[2].group).toMatchObject({ claimMax: 1, perOption: 2 });
    expect(marksClaimed(event, { 'r-1': 1, 'r-2': 1 }, { 'r-3': [0, 1] })).toBe(4);
  });

  it('binds only the 26 named-language and six extraneous conditions printed here', () => {
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(26);
    for (const found of cards.filter(card => card.answerLanguageRule)) {
      expect(found.answerLanguageRule).toMatchObject({ otherLanguageMultiplier: 0.5, penalizedLanguage: 'Japanese' });
      expect(review.selectors.some(selector => selector.document === 'scheme' && selector.text === found.answerLanguageRule?.sourceText)).toBe(true);
      expect(found.audioMaterial || found.id.startsWith('ja-2017-hl-1b-')).toBeTruthy();
    }
    const scope = ['i', 'ii', 'iii'].map(roman => `ja-2017-hl-2a-2-${roman}`).concat([1, 2, 3].map(q => `ja-2017-hl-3b-${q}`));
    expect(cards.filter(card => card.extraneousMaterialRule).map(card => card.id)).toEqual(scope);
    for (const found of cards.filter(card => card.extraneousMaterialRule)) {
      expect(found.extraneousMaterialRule?.sourceText).toContain('strong evidence of extraneous material');
      expect(found.answerLanguageRule).toBeUndefined();
    }
    expect(card('4').answerLanguageRule).toBeUndefined();
    expect(card('5').answerLanguageRule).toBeUndefined();
  });

  it('uses the printed opening/closing allocations and lower expression scales', () => {
    expect(writing('4').criteria.map(criterion => criterion.maxMarks)).toEqual([9, 9, 1, 1, 20]);
    expect(writing('5').criteria.map(criterion => criterion.maxMarks)).toEqual([7, 7, 7, 7, 1, 1, 30]);
    for (const [suffix, normal, lower, length, threshold] of [['4', 20, 15, 150, 10], ['5', 30, 20, 200, 15]] as const) {
      const rubric = writing(suffix);
      const scores: LanguageScores = { [languageLengthId('characters')]: 500 };
      for (const criterion of rubric.criteria) scores[`language:${criterion.id}`] = criterion.maxMarks;
      expect(languageWritingMarks(rubric, scores)).toBe(normal * 2);
      scores[languageLengthId('characters')] = length - 1;
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(lower);
      scores[languageLengthId('characters')] = length;
      expect(languageCriterionValue(rubric, 'expression', scores)).toBe(normal);
      for (const criterion of rubric.criteria.filter(criterion => criterion.id !== 'expression')) scores[`language:${criterion.id}`] = 0;
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
      expect(rubric.criteria.some(criterion => criterion.id.includes('discretionary'))).toBe(false);
    }
    expect(card('4').questionText).toContain('(a) OR (b)');
    expect(card('5').questionText).toContain('ANY 4');
  });

  it('pins the exact glyph recovery and never emits unresolved passage glyphs', () => {
    const file = readFileSync(resolve(__dirname, '..', review.glyphRecovery.path));
    expect(createHash('sha256').update(file).digest('hex')).toBe(review.glyphRecovery.sha256);
    const recovery = JSON.parse(file.toString()) as { sha256: string; repairs: Record<string, Record<string, { text: string }>>; unresolvedImageOnly: { locations: { page: number }[] }[] };
    expect(recovery.sha256).toBe(census.sources.find(source => source.component === 'paper')!.sha256);
    expect(Object.values(recovery.repairs).flatMap(mapping => Object.keys(mapping))).toHaveLength(376);
    expect(recovery.repairs['MS-Mincho']['5251'].text).toBe('居');
    expect(recovery.unresolvedImageOnly).toHaveLength(19);
    expect(new Set(recovery.unresolvedImageOnly.flatMap(item => item.locations.map(location => location.page)))).toEqual(new Set([1, 6, 10]));
    expect(card('2c-1').questionText).toContain('中居（なかい）さんは MC になります。');
    expect(JSON.stringify(cards)).not.toContain('�');
    expect(review.selectors.some(selector => selector.text.includes('�'))).toBe(false);
  });

  it('retains all 20 written and four listening Atlas anchors with 11 complete crops', () => {
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(11);
    const tags = JSON.parse(readFileSync(resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'), 'utf8'));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      expect(task.paperPages, runtime.id).toContain(group.pP);
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2017 && paper.fileid === task.atlas.fileid);
      expect(tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber).primary, runtime.id).toBe(runtime.topicId);
      expect(sidecar.band).toEqual([1, 20]);
    }
    expect(map('LC058ALP000EV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 20 }, (_, i) => String(i + 1)));
    expect(map('LC058ALPA00EV.pdf').q.map(question => question.n)).toEqual(['1', '2', '3', '4']);
  });
});
