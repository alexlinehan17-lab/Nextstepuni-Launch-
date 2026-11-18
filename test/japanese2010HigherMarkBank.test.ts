import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as higher } from '../components/MarkBank/cards/japanese/higher';
import rawCards from '../components/MarkBank/cards/japanese/reviewed.json';
import census from '../scripts/markbank/authoring/reviews/japanese-2010-hl-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2010-hl.json';
import glyphs from '../scripts/markbank/authoring/glyphmap-japanese-2010-hl.json';
import glyphProof from '../scripts/markbank/authoring/reviews/japanese-2010-hl-glyph-proof.json';
import { assertJapaneseSelectedContent, assertJapanese2010ManualResponses, assertJapaneseSourceOnlyFigure } from '../scripts/markbank/japanese-source-rules.mjs';
import { assertJapaneseVariantSources } from '../scripts/markbank/japanese-source-answers.mjs';
import figures from '../components/MarkBank/figures-japanese.json';
import { tariffReconciles } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
import { languageMarks, languagePointsAllocation, type LanguageScores } from '../components/MarkBank/languageScoring';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = higher.filter(card => card.year === 2010);
const idFor = (key: (string | number | null)[]) => `ja-2010-hl-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2010-hl-${suffix}`)!;
const point = (suffix: string) => {
  const found = card(suffix);
  if (found.kind !== 'question') throw new Error(`Expected point card ${suffix}`);
  return found;
};
const writing = (suffix: string) => {
  const found = card(suffix);
  if (found.kind !== 'rubric' || found.rubric.system !== 'language-points') throw new Error(`Expected writing pool ${suffix}`);
  return { ...found, rubric: found.rubric };
};
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2010/${fileid}.json`), 'utf8'));

describe('Japanese 2010 Higher original-source review', () => {
  it('covers the independent 66 tasks, all 43 physical pages and six-question 300-mark allocation', () => {
    expect(cards).toHaveLength(66);
    expect(cards.map(card => card.id).sort()).toEqual(census.tasks.map(task => idFor(task.key)).sort());
    for (const task of census.tasks) {
      const found = cards.find(card => card.id === idFor(task.key))!;
      expect(found.totalMarks, found.id).toBe(task.marks);
      expect(tariffReconciles(found), found.id).toBe(true);
      expect(rawCards.find(card => card.id === found.id)!.sourceEvidence).toMatchObject({ component: task.component, paperPages: task.paperPages, schemePages: task.schemePages });
    }
    expect(census.checksums).toEqual({ reading: 100, grammar: 20, writing: 100, listening: 80, total: 300 });
    expect(Object.values(census.pageRoles).map(pages => Object.keys(pages).length)).toEqual([20, 8, 15]);
    expect(review.sources.map(source => ({ component: source.document, path: source.path, sha256: source.sha256 }))).toEqual(census.sources);
    for (const source of review.sources) expect(source.pagesReviewed).toEqual(Object.keys(census.pageRoles[source.document as keyof typeof census.pageRoles]).map(Number));
    expect(review.consolidations).toEqual([]);
  });

  it('pins the portable original-image glyph proof without requiring ignored PDFs in ordinary CI', () => {
    const digest = (path: string) => createHash('sha256').update(readFileSync(resolve(__dirname, '..', path))).digest('hex');
    expect(review.glyphRecovery.sha256).toBe(digest(review.glyphRecovery.path));
    expect(glyphs.sha256).toBe(review.sources.find(source => source.document === 'scheme')!.sha256);
    expect(Object.values(glyphs.repairs).reduce((sum, font) => sum + Object.keys(font).length, 0)).toBe(314);
    expect(glyphs.unresolvedImageOnly).toEqual([]);
    expect(glyphProof.glyphs).toHaveLength(311);
    expect(glyphProof.blankGlyphs).toHaveLength(3);
    const entries = Object.entries(glyphs.repairs).flatMap(([font, repairs]) => Object.entries(repairs).map(([gid, entry]) => ({ font, gid, ...entry })));
    const proofDigest = digest('scripts/markbank/authoring/reviews/japanese-2010-hl-glyph-proof.json');
    for (const item of glyphProof.glyphs) {
      const entry = entries.find(entry => entry.font === item.font && entry.gid === String(item.gid))!;
      expect(entry.text).toBe(item.text);
      expect(entry.evidence[0]).toMatchObject({ sha256: proofDigest, page: item.page, origin: item.origin, imageSha256: item.imageSha256 });
    }
    for (const sheet of glyphProof.sheets) expect(digest(sheet.path)).toBe(sheet.sha256);
    expect(glyphs.repairs.MSMincho['6595'].text).toBe('末');
    expect(glyphs.repairs['MS-Gothic']['2070'].text).toBe('イ');
    for (const [gid, text] of [['16934', 'っ'], ['16935', 'つ'], ['16988', 'ァ'], ['16989', 'ア'], ['16990', 'ィ'], ['16991', 'イ'], ['17022', 'ッ']] as const) expect(glyphs.repairs['MS-PMincho'][gid].text).toBe(text);
    expect(JSON.stringify([cards, review.selectors])).not.toContain('�');
  });

  it('keeps the complete listening table in confidence review with all fifteen missing-cell identities', () => {
    const table = point('la');
    expect(table.totalMarks).toBe(18);
    expect(table.tariffModel).toEqual({ kind: 'questionTotal' });
    expect(table.rows.map(row => row.id)).toEqual(['tom-age', 'tom-hobby', 'tom-reason', 'tara-birthday', 'tara-current', 'tara-reason', 'mike-age', 'mike-birthday', 'mike-current', 'mike-hobby', 'mike-reason', 'sophie-birthday', 'sophie-current', 'sophie-hobby', 'sophie-reason']);
    for (const row of table.rows) {
      expect(row.marks).toBeNull();
      expect(row.contextNote).toContain('Printed allocation:');
    }
    expect(table.rows[0].contextNote).toContain('gives no rule for combining');
    expect(table.rows[0].contextNote).toContain('no quarter mark');
    expect(table.rows[0].contextNote).toContain('1/2 marks if answered in Japanese');
    expect(table.rows.find(row => row.id === 'sophie-current')?.verbatim).toContain('Studying fashion design in university');
    expect(table.rows.find(row => row.id === 'sophie-hobby')?.verbatim).toContain('Designing clothes');
    expect(table.answerLanguageRule).toBeUndefined();
    expect(table.extraneousMaterialRule).toBeUndefined();
    expect(table.questionFigure?.includesPrompt).toBe(true);
    expect(table.audioMaterial).toBeDefined();
    expect(table.topicId).toBe('japanese-6-1');
    expect(marksClaimed(table, Object.fromEntries(table.rows.map(row => [row.id, 'yes'])))).toBe(0);
  });

  it('retains the seven webpage prompts beside their source-only figure and all required answer pools', () => {
    expect(point('1aa').rows).toHaveLength(7);
    expect(point('1aa').taskGroups?.map(group => group.marks)).toEqual(Array(7).fill(1));
    expect(point('1aa').questionFigure?.includesPrompt).toBe(false);
    expect(point('1aa').sourceMaterial?.pages).toEqual([2]);
    for (const [suffix, count] of [['1b-1', 6], ['2d-1', 4], ['2d-2', 4], ['3c', 14], ['4a', 6], ['4b', 8], ['lc2-3', 3], ['ld-4', 5]] as const) expect(point(suffix).rows).toHaveLength(count);
    expect(point('1ab-2').rows.map(row => row.marks)).toEqual([2, 1, 1]);
    expect(point('1ab-2').taskGroups?.map(group => group.marks)).toEqual([2, 2]);
    expect(point('3c').taskGroups?.map(group => group.marks)).toEqual(Array(7).fill(2));
    expect(point('4b').rows[6].verbatim).toContain('で');
    expect(point('4b').rows[6].verbatim).toContain('の');
    expect(point('4b').rows[6].verbatim).toContain('から');
    expect(point('4b').taskGroups?.map(group => group.marks)).toEqual([1, 2, 1, 2, 2]);
    expect(point('4b').taskGroups?.map(group => group.rowIds)).toEqual([
      ['r-1'], ['r-2', 'r-3'], ['r-4'], ['r-5', 'r-6'], ['r-7', 'r-8'],
    ]);
  });

  it('keeps all three Q2 heading discrepancies and the whole three-item response thresholds', () => {
    const question2 = cards.filter(card => /^ja-2010-hl-2[abcd]/.test(card.id));
    expect(question2.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(29);
    for (const found of question2) expect(found.stem).toContain('A=4, B=8 and C=9');
    for (const suffix of ['2b-3', '2b-4']) {
      const found = point(suffix);
      expect(found.rows).toHaveLength(1);
      expect(found.rows[0].permittedMarks).toEqual([0, 1, 2]);
      expect(found.rows[0].contextNote).toContain('one correct item earns 0; two earn 1; three earn 2');
      expect(marksClaimed(found, { 'r-1': 1 })).toBe(1);
      expect(marksClaimed(found, { 'r-1': 2 })).toBe(2);
    }
  });

  it('keeps Q3 half awards response-scoped and one discretionary mark in either exclusive placement', () => {
    const affected = review.cards.filter(card => /^ja-2010-hl-3(?:a-[1-9]|b|c)$/.test(card.id));
    expect(affected).toHaveLength(11);
    for (const found of affected) expect(() => assertJapanese2010ManualResponses(found, review)).not.toThrow();
    const joint = point('3b');
    expect(joint.totalMarks).toBe(4);
    expect(joint.answerVariants?.map(variant => variant.id)).toEqual(['bonus-under-1', 'bonus-under-2']);
    for (const [index, variant] of joint.answerVariants!.entries()) {
      expect(variant.rows.map(row => row.permittedMarks)).toEqual([[0, 0.5, 1], [0, 1, 2], [0, 0.5, 1]]);
      expect(variant.rows[2].contextNote).toContain(`assigned under question ${index + 1}`);
      expect(variant.rows[1].contextNote).toContain('solely the printed half award');
      expect(marksClaimed({ ...joint, rows: variant.rows }, { 'r-1': 0.5, 'r-2': 2, 'r-3': index === 0 ? 0.5 : 1 })).toBe(index === 0 ? 3 : 3.5);
      expect(marksClaimed({ ...joint, rows: variant.rows }, { 'r-1': 1, 'r-2': 1, 'r-3': index === 0 ? 1 : 0.5 })).toBe(index === 0 ? 3 : 2.5);
      expect(marksClaimed({ ...joint, rows: variant.rows }, { 'r-1': 1, 'r-2': 2, 'r-3': 1 })).toBe(4);
      expect(marksClaimed({ ...joint, rows: variant.rows }, { 'r-1': 0.25, 'r-2': 0.5, 'r-3': 0.25 })).toBe(0);
    }
    expect(point('3a-4').rows[0].verbatim).toContain('デイズニーランドへ行きましたか。');
    expect(point('3a-4').rows[0].contextNote).toContain('without silently rewriting');
    expect(point('ld-1-b').rows[0].permittedMarks).toEqual([0, 0.5, 1]);
    expect(point('ld-1-b').answerLanguageRule).toBeUndefined();
  });

  it('uses actual selected Q5 content and discretionary marks at both printed expression boundaries', () => {
    const found = writing('5');
    const rubric = found.rubric;
    expect(rubric.count).toBe(4);
    expect(rubric.allocationCap?.maxMarks).toBe(16);
    expect(rubric.groups.find(group => group.id === 'school')?.criteria?.map(criterion => criterion.permittedMarks)).toEqual([[0, 2], [0, 2]]);
    expect(rubric.markingGuideNote).toContain('four distinct questions');
    expect(rubric.markingGuideNote).toContain('Do not mix options');
    const scores: LanguageScores = { 'language:group:school': 1, 'language:school-location': 2, 'language:school-nearby': 2,
      'language:group:slot-2': 1, 'language:answer-2': 4, 'language:discretionary': 2,
      'language:expression': 20, 'language:length:characters': 150 };
    expect(languagePointsAllocation(rubric, scores)).toBe(8);
    expect(languageMarks(found, scores)).toBe(25);
    expect(languageMarks(found, { ...scores, 'language:discretionary': 3 })).toBe(31);
    expect(languageMarks(found, { ...scores, 'language:discretionary': 3, 'language:length:characters': 149 })).toBe(26);
    expect(languageMarks(found, { ...scores, 'language:discretionary': 3, 'language:group:school': 0 })).toBe(22);
    expect(languageMarks(found, { ...scores, 'language:group:first': 1, 'language:first-answer': 4 })).toBe(21);
    const full = { ...scores, 'language:discretionary': 4, 'language:group:slot-3': 1, 'language:answer-3': 4, 'language:group:slot-4': 1, 'language:answer-4': 4 };
    expect(languageMarks(found, full)).toBe(40);
    expect(rubric.criteria?.find(criterion => criterion.id === 'expression')?.bands?.map(band => [band.marks[0], band.marks.at(-1)])).toEqual([[0, 5], [6, 14], [15, 20]]);
  });

  it.each(['birthday', 'country'] as const)('uses only the selected Q6 %s option with its different required and discretionary tariffs', option => {
    const found = writing('6');
    const rubric = found.rubric;
    expect(rubric.count).toBe(1);
    expect(rubric.groups.map(group => group.criteria?.map(criterion => criterion.maxMarks))).toEqual([[3, 20, 7], [5, 20, 5]]);
    const scores: LanguageScores = { [`language:group:${option}`]: 1,
      [`language:${option}-required`]: option === 'birthday' ? 3 : 5, [`language:${option}-selected`]: 10,
      'language:birthday-discretionary': option === 'birthday' ? 2 : 7, 'language:country-discretionary': option === 'country' ? 0 : 5,
      'language:expression': 30, 'language:length:characters': 200 };
    expect(languageMarks(found, scores)).toBe(35);
    const above = { ...scores, [`language:${option}-discretionary`]: option === 'birthday' ? 3 : 1 };
    expect(languageMarks(found, above)).toBe(46);
    expect(languageMarks(found, { ...above, 'language:length:characters': 199 })).toBe(36);
    expect(languageMarks(found, { ...above, [`language:group:${option}`]: 0 })).toBe(20);
    expect(languageMarks(found, { ...above, [`language:${option}-selected`]: 20, [`language:${option}-discretionary`]: option === 'birthday' ? 7 : 5 })).toBe(60);
    expect(rubric.markingGuideNote).toContain('プレセント');
    expect(rubric.criteria?.[0].bands?.map(band => [band.marks[0], band.marks.at(-1)])).toEqual([[0, 7], [8, 20], [21, 30]]);
  });

  it('rejects unsupported selected-content thresholds, sources, locations and automatic language reductions', () => {
    for (const suffix of ['5', '6']) {
      const original = review.cards.find(card => card.id === `ja-2010-hl-${suffix}`)!;
      expect(() => assertJapaneseSelectedContent(original, review)).not.toThrow();
      for (const patch of [{ id: 'ja-2010-hl-4' }, { totalMarks: 99 }, { answerLanguageRule: { otherLanguageMultiplier: 0.5 } }]) expect(() => assertJapaneseSelectedContent({ ...original, ...patch }, review)).toThrow();
      for (const changedReview of [
        { ...review, selectors: [] },
        { ...review, sources: review.sources.map(source => ({ ...source, sha256: 'changed' })) },
        { ...review, selectors: review.selectors.map(selector => ({ ...selector, page: 15 })) },
        { ...review, selectors: review.selectors.map(selector => ({ ...selector, text: selector.text + ' changed' })) },
      ]) expect(() => assertJapaneseSelectedContent(original, changedReview)).toThrow();
      const changed = structuredClone(original);
      const expression = changed.rubric?.criteria?.find(criterion => criterion.id === 'expression');
      if (!expression?.limits) throw new Error('Missing bound expression criterion');
      expression.limits[0].maxMarks += 1;
      expect(() => assertJapaneseSelectedContent(changed, review)).toThrow();
    }
  });

  it('rejects unbound Q3 half awards, quarter marks, an extra bonus and altered bonus placement', () => {
    const original = review.cards.find(card => card.id === 'ja-2010-hl-3b')!;
    expect(() => assertJapanese2010ManualResponses(original, { ...review, selectors: [] })).toThrow();
    expect(() => assertJapanese2010ManualResponses(original, { ...review, sources: review.sources.map(source => ({ ...source, sha256: 'changed' })) })).toThrow();
    expect(() => assertJapanese2010ManualResponses(original, { ...review, selectors: review.selectors.map(selector => ({ ...selector, page: 10 })) })).toThrow();
    for (const patch of [
      { answerLanguageRule: { otherLanguageMultiplier: 0.5 } }, { extraneousMaterialRule: { multiplier: 0.5 } },
      { sourceEvidence: { ...original.sourceEvidence, schemePages: [10] } },
      { rows: original.rows!.map(row => ({ ...row, permittedMarks: [0, 0.25, 0.5, row.marks] })) },
      { rows: [...original.rows!, original.rows![2]] }, { answerVariants: undefined },
      { answerVariants: original.answerVariants!.map(variant => ({ ...variant, rows: variant.rows.map(row => ({ ...row, contextNote: 'Unbound guidance' })) })) },
    ]) expect(() => assertJapanese2010ManualResponses({ ...original, ...patch }, review)).toThrow();
    expect(() => assertJapaneseVariantSources(original, review.selectors, '')).not.toThrow();
    const changed = structuredClone(original);
    changed.answerVariants![1].rows[1].verbatim = 'An invented answer absent from this original scheme';
    expect(() => assertJapaneseVariantSources(changed, review.selectors, '')).toThrow();
    expect(() => assertJapaneseVariantSources(original, review.selectors.filter(selector => selector.page !== 9), '')).toThrow();
  });

  it('requires the source-only figure flag so missing metadata cannot hide the seven next-page questions', () => {
    const original = review.cards.find(card => card.id === 'ja-2010-hl-1aa')!;
    const figure = figures['ja-2010-hl-web-buttons'];
    expect(() => assertJapaneseSourceOnlyFigure(original, review, figure)).not.toThrow();
    for (const patch of [{ questionFigureIncludesPrompt: undefined }, { questionFigureIncludesPrompt: true }, { questionFigureKey: undefined }, { id: 'ja-2010-hl-1ab-1' }, { questionText: ' ' }]) expect(() => assertJapaneseSourceOnlyFigure({ ...original, ...patch }, review, figure)).toThrow();
    expect(() => assertJapaneseSourceOnlyFigure(original, review, { ...figure, source: { ...figure.source, page: 3 } })).toThrow();
    expect(() => assertJapaneseSourceOnlyFigure(original, { ...review, sources: [] }, figure)).toThrow();
    expect(() => assertJapaneseSourceOnlyFigure({ id: 'ja-2026-hl-1a' }, {}, undefined)).not.toThrow();
  });

  it('binds only the forty published named-language conditions and preserves the explicit greetings exception', () => {
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(40);
    expect(cards.filter(card => card.audioMaterial)).toHaveLength(29);
    expect(cards.filter(card => card.audioMaterial && card.topicId === 'japanese-6-1').map(card => card.id)).toEqual(['ja-2010-hl-la']);
    expect(cards.filter(card => card.audioMaterial && card.topicId === 'japanese-6-0')).toHaveLength(28);
    for (const found of cards.filter(card => card.answerLanguageRule)) {
      expect(found.answerLanguageRule!.otherLanguageMultiplier).toBe(0.5);
      expect(found.answerLanguageRule!.sourceText).toContain(`answered in ${found.answerLanguageRule!.penalizedLanguage}`);
      expect(found.answerLanguageRule!.penalizedLanguage).toBe(found.id.startsWith('ja-2010-hl-2a') ? 'English' : 'Japanese');
    }
    for (const found of cards.filter(card => /ja-2010-hl-(?:3[abc]|1ac|ld-1-|la$|[56]$)/.test(card.id))) expect(found.answerLanguageRule).toBeUndefined();
  });

  it('resolves every task to complete source groups while preserving all twelve original Atlas anchors', () => {
    const tags = JSON.parse(readFileSync(resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'), 'utf8'));
    for (const [fileid, anchors] of Object.entries(census.originalAtlasAnchors)) {
      const current = map(fileid);
      for (const anchor of anchors) {
        const found = current.q.find(question => question.n === anchor.n)!;
        expect({ n: found.n, pP: found.pP, pY: found.pY, region: found.region }).toEqual(anchor);
      }
    }
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2010 && paper.fileid === task.atlas.fileid);
      const topic = tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber);
      expect([topic.primary, topic.secondary], runtime.id).toContain(runtime.topicId);
      expect(sidecar.band).toEqual([1, 15]);
    }
    expect(map('LC058ALP000EV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 10 }, (_, i) => String(i + 1)));
    const aural = map('LC058ALPA00EV.pdf');
    expect(aural.q.map(question => question.n)).toEqual(Array.from({ length: 13 }, (_, i) => String(i + 1)));
    for (const anchor of aural.q.slice(0, 9)) expect(anchor.label).toContain('Original source anchor');
  });
});
