import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as higher } from '../components/MarkBank/cards/japanese/higher';
import rawCards from '../components/MarkBank/cards/japanese/reviewed.json';
import census from '../scripts/markbank/authoring/reviews/japanese-2013-hl-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2013-hl.json';
import { tariffReconciles } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
import { languageCriterionValue, languageLengthId, languagePointsMarks, languageWritingMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = higher.filter(card => card.year === 2013);
const idFor = (key: (string | number | null)[]) => `ja-2013-hl-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2013-hl-${suffix}`)!;
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
const pool = (suffix: string) => {
  const found = card(suffix);
  if (found.kind !== 'rubric' || found.rubric.system !== 'language-points') throw new Error(`Expected complete pool ${suffix}`);
  return found.rubric;
};
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2013/${fileid}.json`), 'utf8'));

describe('Japanese 2013 Higher independent original-source review', () => {
  it('covers all 40 independently counted tasks and all 44 original pages', () => {
    expect(cards).toHaveLength(40);
    expect(cards.map(card => card.id).sort()).toEqual(census.tasks.map(task => idFor(task.key)).sort());
    for (const task of census.tasks) {
      const found = cards.find(card => card.id === idFor(task.key))!;
      expect(found.totalMarks, found.id).toBe(task.marks);
      expect(tariffReconciles(found), found.id).toBe(true);
      expect(rawCards.find(card => card.id === found.id)!.sourceEvidence).toMatchObject({ component: task.component, paperPages: task.paperPages, schemePages: task.schemePages });
    }
    expect(census.checksums).toEqual({ reading: 120, writing: 100, listening: 80, total: 300 });
    expect(Object.values(census.pageRoles).map(pages => Object.keys(pages).length)).toEqual([20, 8, 16]);
    expect(review.sources.map(source => ({ component: source.document, path: source.path, sha256: source.sha256 }))).toEqual(census.sources);
    for (const source of review.sources) expect(source.pagesReviewed).toEqual(Object.keys(census.pageRoles[source.document as keyof typeof census.pageRoles]).map(Number));
    expect(review.consolidations).toEqual([]);
  });

  it('preserves whole required pools, nested question identity and every alternative', () => {
    expect(point('1aa').rows.map(row => row.marks)).toEqual([2, 2, 2, 2, 2]);
    expect(point('1ab-1').rows.map(row => row.marks)).toEqual([2, 2, 2]);
    expect(point('1ab-1').rows.slice(1).map(row => row.parts?.map(part => part.marks))).toEqual([[1, 1], [1, 1]]);
    const biography = point('1b');
    expect(biography.rows).toHaveLength(5);
    expect(biography.rows[3]).toMatchObject({ kind: 'criterion', marks: 2, permittedMarks: [0, 1, 2] });
    for (const text of ['Jean Paul', 'Gaultier', 'Grand prix']) expect(biography.rows[3].verbatim).toContain(text);
    expect(marksClaimed(biography, { 'r-4': 1 })).toBe(1);
    expect(marksClaimed(biography, { 'r-4': 2 })).toBe(2);
    expect(point('2a-1').rows).toHaveLength(11);
    expect(point('2a-1').taskGroups?.map(group => [group.label, group.marks])).toEqual([['Adam', 3], ['Bashir', 3], ['Max', 3], ['Mei', 2]]);
    expect(point('2a-1').rows.every(row => row.marks === 1)).toBe(true);
    expect(point('2a-1').rows.some(row => row.verbatim.includes('6000'))).toBe(false);
    for (const [suffix, count] of [['2b', 5], ['2c-1', 10], ['2c-2', 5], ['2c-3', 5], ['3b-1', 5], ['3b-2', 5]] as const) {
      const rubric = pool(suffix);
      expect(rubric.count).toBe(count);
      expect(rubric.groups).toHaveLength(count);
      const scores: LanguageScores = {};
      for (const group of rubric.groups) {
        scores[`language:group:${group.id}`] = 1;
        for (const row of group.rows) scores[`language:row:${group.id}:${row.id}`] = 1;
      }
      expect(languagePointsMarks(rubric, scores)).toBe(card(suffix).totalMarks);
    }
    expect(pool('2b').groups.map(group => group.rows.map(row => row.marks))).toEqual(Array(5).fill([1, 1]));
    expect(pool('3b-2').markingGuideNote).toContain('(iv) and (v)');
    expect(pool('3b-2').markingGuideNote).toContain('(vi) and (vii)');
  });

  it('retains the repeated discussion number and literal two-versus-24-hour discrepancy', () => {
    expect(card('2a-2').questionRef).toBe('2013 HL Section 2A Q2');
    expect(card('2a-2-i').questionRef).toBe('2013 HL Section 2A Q2(i)');
    expect(writing('2a-2').criteria).toHaveLength(4);
    expect(writing('2a-2').criteria.every(criterion => criterion.maxMarks === 2 && JSON.stringify(criterion.permittedMarks) === '[0,2]')).toBe(true);
    expect(writing('2a-2').markingGuideNote).toContain('both hotels');
    expect(writing('2a-2').markingGuideNote).toContain('repeats Q2');
    const row = point('2a-2-ii').rows[0];
    if (row.kind !== 'anyN') throw new Error('Expected internet-cafe pool');
    expect(row.group.claimMax).toBe(2);
    expect(row.group.options).toContain('２時間オープン');
    expect(row.contextNote).toContain('24時間オープン');
    expect(review.selectors.some(selector => selector.document === 'paper' && selector.page === 5 && selector.text.includes('24 時間オープン'))).toBe(true);
    expect(review.selectors.some(selector => selector.document === 'scheme' && selector.page === 7 && selector.text.includes('２時間オープン'))).toBe(true);
  });

  it('keeps each exact published comprehension partial and rejects unprinted awards', () => {
    for (const [suffix, maximum, allowed, invalid] of [
      ['3a-2-i', 3, [0, 1, 2, 3], 4], ['3a-2-ii', 4, [0, 1, 2, 4], 3], ['3a-3', 5, [0, 2, 5], 3],
    ] as const) {
      const found = point(suffix);
      expect(found.rows[0]).toMatchObject({ kind: 'criterion', marks: maximum, permittedMarks: [...allowed] });
      for (const mark of allowed) expect(marksClaimed(found, { 'r-1': mark })).toBe(mark);
      expect(marksClaimed(found, { 'r-1': invalid })).toBe(0);
    }
    expect(point('3a-2-i').rows[0].contextNote).toContain('She fights with her parents, 0 marks');
    expect(point('3a-1-ii').rows.map(row => row.marks)).toEqual([2, 2]);
  });

  it('retains both complete listening tables, exact partials and the given phone prefix', () => {
    const first = point('la');
    expect(first.rows).toHaveLength(12);
    expect(first.rows.map(row => row.marks)).toEqual([1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2]);
    expect(first.stem).toContain('Tom');
    expect(first.stem).toContain('Haru');
    expect(first.rows.filter(row => row.kind === 'criterion').map(row => row.permittedMarks)).toEqual([[0, 1, 2], [0, 1, 2]]);
    expect(point('lb-1').rows.map(row => row.marks)).toEqual([2, 2, 2, 2]);
    expect(point('lb-1').rows.filter(row => row.kind === 'criterion').map(row => row.permittedMarks)).toEqual([[0, 1, 2], [0, 1, 2]]);
    expect(point('lb-2-i').rows.map(row => row.marks)).toEqual([1, 1]);
    const phone = point('lb-2-iv');
    expect(phone.rows).toHaveLength(1);
    expect(phone.rows[0]).toMatchObject({ verbatim: '06-810-4545', marks: 2 });
    expect(phone.rows[0].contextNote).toContain('seven missing digits');
    expect(phone.rows[0].contextNote).toContain('no per-digit tariff');
    expect(phone.questionRef).toBe('2013 HL Section LB Q2(iv)');
    const interview = point('ld');
    expect(interview.taskGroups?.map(group => group.marks)).toEqual([2, 2, 4, 2, 2, 2, 2, 2, 2]);
    expect(interview.rows.some(row => row.verbatim.includes('Kenta'))).toBe(false);
    expect(interview.rows.slice(2, 4).map(row => [row.verbatim, row.marks])).toEqual([['Surfing', 3], ['blogs', 1]]);
  });

  it('retains all seven pool details, descending tariffs and the compound directions quota', () => {
    const poolRow = point('lb-2-ii').rows[0];
    if (poolRow.kind !== 'anyN') throw new Error('Expected seven-detail pool');
    expect(poolRow.group.options.map(text => text.trim())).toHaveLength(7);
    expect(poolRow.group.options.map(text => text.trim())).toContain('beautiful view');
    expect(poolRow.group.options.map(text => text.trim())).toContain('can see the sea');
    expect(poolRow.group).toMatchObject({ claimMax: 2, perOption: 2 });
    expect(marksClaimed(point('lb-2-ii'), {}, { 'r-1': [0] })).toBe(2);
    expect(marksClaimed(point('lb-2-ii'), {}, { 'r-1': [0, 1, 2, 3, 4, 5, 6] })).toBe(4);
    for (const suffix of ['lc-2-iii', 'lc-2-iv']) {
      const row = point(suffix).rows[0];
      expect(row.kind === 'anyN' && row.group.perOptionSteps).toEqual([2, 1]);
      expect(marksClaimed(point(suffix), {}, { 'r-1': [0] })).toBe(2);
      expect(marksClaimed(point(suffix), {}, { 'r-1': [0, 1, 2] })).toBe(3);
    }
    const directions = point('lc-3-ii');
    expect(directions.rows[0]).toMatchObject({ marks: 2, verbatim: 'Turn right (at next corner)' });
    const rest = directions.rows[1];
    expect(rest.kind === 'anyN' && rest.group).toMatchObject({ claimMax: 2, perOption: 1 });
    expect(rest.kind === 'anyN' && rest.group.options).toHaveLength(3);
    expect(marksClaimed(directions, {}, { 'r-2': [0, 1, 2] })).toBe(2);
    expect(marksClaimed(directions, { 'r-1': 'yes' }, { 'r-2': [0, 1, 2] })).toBe(4);
  });

  it('binds language and extraneous conditions only to their printed scope', () => {
    expect(cards.filter(card => card.audioMaterial)).toHaveLength(15);
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(20);
    expect(cards.filter(card => !card.audioMaterial && card.answerLanguageRule).map(card => card.id)).toEqual(['1ab-1', '1ab-2-i', '1ab-2-ii', '1ab-2-iii', '1b'].map(suffix => `ja-2013-hl-${suffix}`));
    for (const found of cards.filter(card => card.answerLanguageRule)) {
      const rule = found.answerLanguageRule!;
      expect(rule).toMatchObject({ otherLanguageMultiplier: 0.5, penalizedLanguage: 'Japanese', schemePages: [found.audioMaterial ? 3 : 6] });
      expect(review.selectors.some(selector => selector.document === 'scheme' && selector.page === rule.schemePages[0] && selector.text === rule.sourceText)).toBe(true);
    }
    expect(cards.filter(card => card.extraneousMaterialRule).map(card => card.id)).toEqual(['i', 'ii', 'iii'].map(roman => `ja-2013-hl-2a-2-${roman}`));
    for (const found of cards.filter(card => card.extraneousMaterialRule)) {
      const rule = found.extraneousMaterialRule!;
      expect(rule).toMatchObject({ multiplier: 0.5, schemePages: [7] });
      expect(review.selectors.some(selector => selector.document === 'scheme' && selector.page === 7 && selector.text === rule.sourceText)).toBe(true);
    }
    expect(card('2a-2').extraneousMaterialRule).toBeUndefined();
    for (const suffix of ['1aa', '4', '5']) expect(card(suffix).answerLanguageRule).toBeUndefined();
  });

  it('keeps one writing scenario, local discretionary marks and strict expression thresholds', () => {
    expect(writing('4').criteria.map(criterion => criterion.maxMarks)).toEqual([18, 1, 1, 20]);
    expect(writing('5').criteria.map(criterion => criterion.maxMarks)).toEqual([6, 1, 6, 1, 6, 1, 6, 1, 1, 1, 30]);
    expect(card('4').questionText).toContain('find a job');
    expect(card('4').questionText).toContain('go to college');
    expect(card('5').questionText).toContain('any four');
    expect(card('5').questionText).toContain('だれと会');
    expect(writing('5').markingGuideNote).toContain('Do not mix headings');
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
    }
  });

  it('retains all original Atlas anchors and complete source contexts', () => {
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(14);
    const tags = JSON.parse(readFileSync(resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'), 'utf8'));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      if (task.component === 'aural') expect(task.paperPages).toContain(group.pP);
      else {
        const span = census.atlasSourceSpans[`written${task.atlas.questionNumber}` as keyof typeof census.atlasSourceSpans];
        expect(span).toContain(group.pP);
        expect(task.paperPages.every(page => span.includes(page))).toBe(true);
      }
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2013 && paper.fileid === task.atlas.fileid);
      const topic = tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber);
      expect([topic.primary, topic.secondary], runtime.id).toContain(runtime.topicId);
      expect(sidecar.band).toEqual([1, 16]);
    }
    expect(map('LC058ALP000EV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 8 }, (_, i) => String(i + 1)));
    expect(map('LC058ALPA00EV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 4 }, (_, i) => String(i + 1)));
    expect(JSON.stringify(cards)).not.toContain('�');
  });
});
