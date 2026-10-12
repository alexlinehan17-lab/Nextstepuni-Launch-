/** @license SPDX-License-Identifier: Apache-2.0 */
import { describe, expect, it } from 'vitest';
import authored from '../components/MarkBank/cards/geography/authored.json';
import { CARDS as HIGHER } from '../components/MarkBank/cards/geography/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/geography/ordinary';
import { GEOGRAPHY_STRANDS } from '../components/MarkBank/deck';
import census from '../scripts/markbank/authored/geography-census.json';
import reviewAudit from '../scripts/markbank/authored/geography-reviewed-audit.json';
import reviewedRuntime from '../data/examTopics/geography-reviewed-question-runtime.json';
import { examTopicIdsForQuestion } from '../data/examTopics/registry';
import {
  geographyMarks,
  geographyScoreId,
  suggestRubricGrade,
} from '../components/MarkBank/SessionScreen';
import { isRubricCard, tariffReconciles, type SecRubricCard } from '../types/markBank';

const ALL: SecRubricCard[] = [...HIGHER, ...ORDINARY];
const byId = new Map(ALL.map(card => [card.id, card]));

const levelRef = (level: string) => level === 'higher' ? 'HL' : 'OL';

type ReviewedTask = (typeof reviewAudit.reviewedSittings)[number]['tasks'][number];
const REVIEWED_SITTINGS = new Set(reviewAudit.reviewedSittings
  .map(sitting => `${sitting.year}-${sitting.level}`));
const isReviewed = (card: { year: number; level: string }) =>
  REVIEWED_SITTINGS.has(`${card.year}-${card.level}`);
const LEGACY = ALL.filter(card => !isReviewed(card));
const REVIEWED = ALL.filter(isReviewed);
const authoredById = new Map(authored.cards.map(card => [card.id, card]));

describe('complete answerable 2021–2026 Geography corpus', () => {
  it('accounts for every paper task before finite route expansion', () => {
    // 2026-10-11/12: 2026, 2025 and 2024 Higher/Ordinary were independently
    // reviewed. Their printed base tasks became separately priced tasks
    // (2026 HL 60 -> 113, 2026 OL 48 -> 126, 2025 HL 60 -> 115, 2025 OL
    // 48 -> 119, 2024 HL 60 -> 111, 2024 OL 48 -> 132), and their
    // companion-held tasks (8 per 2025 level, 8 for 2024 Higher, 9 for 2024
    // Ordinary) are now carded with the official map, legend and aerial:
    // 648 - 60 + 113 - 48 + 126 - 60 + 115 - 48 + 119 - 60 + 111 - 48 + 132
    // = 1,040 base tasks, 52 still held.
    expect(census.paperBaseTasks).toBe(1040);
    expect(census.includedBaseTasks).toBe(988);
    expect(census.excludedBaseTasks).toBe(52);
    expect(census.includedBaseTasks + census.excludedBaseTasks)
      .toBe(census.paperBaseTasks);
    expect(census.authoredCards).toBe(1186);
    expect(census.baseTasks).toHaveLength(1040);
    expect(census.baseTasks.filter(task => task.status === 'authored')).toHaveLength(988);
    expect(census.baseTasks.filter(task => task.status === 'excluded')).toHaveLength(52);
    expect(census.exclusions).toHaveLength(52);
    expect(census.sittings).toHaveLength(12);

    const expected = {
      '2021-higher': 75, '2021-ordinary': 49,
      '2022-higher': 73, '2022-ordinary': 49,
      '2023-higher': 78, '2023-ordinary': 52,
      '2024-higher': 127, '2024-ordinary': 147,
      '2025-higher': 143, '2025-ordinary': 131,
      '2026-higher': 126, '2026-ordinary': 136,
    } as const;
    for (const [sitting, cards] of Object.entries(expected)) {
      const [year, level] = sitting.split('-');
      expect(ALL.filter(card => card.year === Number(year) && card.level === level), sitting)
        .toHaveLength(cards);
    }
  });

  it('maps the generated manifest one-to-one to the live decks', () => {
    expect(HIGHER).toHaveLength(622);
    expect(ORDINARY).toHaveLength(564);
    expect(ALL).toHaveLength(1186);
    expect(authored.meta.cardCount).toBe(1186);
    expect(new Set(ALL.map(card => card.id)).size).toBe(1186);
    expect(ALL.map(card => card.id).sort())
      .toEqual(authored.cards.map(card => card.id).sort());

    for (const generated of authored.cards) {
      const runtime = byId.get(generated.id);
      expect(runtime, generated.id).toBeDefined();
      expect(runtime?.questionRef, generated.id).toBe(generated.questionRef);
      expect(runtime?.questionText, generated.id).toBe(generated.questionText);
      expect(runtime?.totalMarks, generated.id).toBe(generated.totalMarks);
      expect(runtime?.topicId, generated.id).toBe(generated.topicId);
      expect(runtime?.paperFileid, generated.id).toBe(generated.paperFileid);
      expect(runtime?.section, generated.id).toBe(String(generated.part));
      expect(runtime?.schemeCitation, generated.id).toContain(`p.${generated.schemePage}`);
    }
  });

  it('expands every closed route and choose-N instruction', () => {
    expect(census.selectionAudit).toHaveLength(79);
    expect(census.selectionAudit.every(entry => entry.classification === 'finite-expanded'))
      .toBe(true);
    for (const selection of census.selectionAudit) {
      const variants = ALL.filter(card => card.questionRef === selection.questionRef
        || card.questionRef.startsWith(`${selection.questionRef} ·`));
      expect(variants, selection.questionRef).toHaveLength(selection.variants);
      expect(new Set(variants.map(card => card.questionText)).size, selection.questionRef)
        .toBe(selection.variants);
    }

    const deposition = HIGHER.filter(card =>
      card.questionRef.startsWith('2025 HL Part 2 Q2B'));
    expect(deposition.map(card => card.questionRef)).toEqual([
      '2025 HL Part 2 Q2B · Route (i) · one fluvial landform',
      '2025 HL Part 2 Q2B · Route (i) · one coastal landform',
      '2025 HL Part 2 Q2B · Route (i) · one glacial landform',
      '2025 HL Part 2 Q2B · Route (ii)',
    ]);
    expect(deposition.map(card => card.questionText)).toEqual([
      expect.stringContaining('one fluvial landform'),
      expect.stringContaining('one coastal landform'),
      expect.stringContaining('one glacial landform'),
      expect.stringContaining('one mass movement process'),
    ]);
  });

  it('holds unavailable historical companions and ships every complete 2026 companion task', () => {
    expect(census.exclusions.every(exclusion =>
      /separate Ordnance Survey map or aerial photograph/i.test(exclusion.reason)))
      .toBe(true);

    for (const exclusion of census.exclusions) {
      const base = `${exclusion.year} ${levelRef(exclusion.level)} Part ${exclusion.part} `
        + `Q${exclusion.questionRef}`;
      const shipped = ALL.filter(card => card.questionRef === base
        || card.questionRef.startsWith(`${base} ·`));
      expect(shipped.map(card => card.id), base).toEqual([]);
    }
    const companionTasks = ALL.filter(card =>
      /accompan(?:y|ying|ies)\s+(?:this|the)\s+paper|using evidence from the aerial photograph\s+OR\s+from the\s+1:50\s*000 Ordnance Survey map/i
        .test(`${card.stem ?? ''} ${card.questionText}`));
    expect(companionTasks.length).toBeGreaterThan(0);
    // Companion tasks ship only from independently reviewed sittings, which
    // wire each sitting's own official map, legend and aerial photograph.
    expect(companionTasks.every(isReviewed)).toBe(true);
    expect(companionTasks.filter(card => {
      const sources = [card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .filter(Boolean);
      return !sources.some(source => source?.sourceFileid);
    }).map(card => card.id)).toEqual([]);
  });
});

describe('Geography prompt, source and marking integrity', () => {
  it('uses clean paper prompts and the real Part One/Part Two paper file', async () => {
    const { resolvePaperFileid } = await import('../scripts/markbank/paperIndex.mjs');
    const furniture = /Leaving Certificate Examination|Do not write|Blank Page|Copyright notice|Answer any|Instructions/i;
    for (const generated of authored.cards) {
      const runtime = byId.get(generated.id)!;
      // A reviewed card can be one short printed part ("(ii) Name the former
      // currency of Bulgaria."); its context rides in the stem.
      expect(generated.questionText.length, generated.id)
        .toBeGreaterThanOrEqual(isReviewed(generated) ? 15 : 40);
      expect(generated.questionText, generated.id).not.toMatch(furniture);
      expect(generated.paperPage, generated.id).toBeGreaterThan(0);
      expect(generated.schemePage, generated.id).toBeGreaterThan(0);
      expect(generated.schemeGuidance.length, generated.id).toBeGreaterThan(0);
      expect(runtime.paperFileid, generated.id).toBe(resolvePaperFileid(
        'geography', generated.year, generated.level, String(generated.part)));
    }
  });

  it('shows the official page for every embedded map, chart, image or source task', () => {
    const expectedSourced = LEGACY.filter(card => card.section === '1'
      || / Part 2 Q(?:[1-9]|1[0-2])A(?: ·|$)/.test(card.questionRef));
    expect(expectedSourced).toHaveLength(106);
    expect(expectedSourced.filter(card => !card.sourceMaterial).map(card => card.id)).toEqual([]);

    const nonStandardSourced = LEGACY.filter(card => card.sourceMaterial
      && !expectedSourced.some(expected => expected.id === card.id));
    expect(nonStandardSourced.map(card => card.id)).toEqual([
      'geography-2021-hl-p2-q6c',
      'geography-2021-hl-p2-q6c-population-dynamics-religion',
      'geography-2021-hl-p2-q6c-population-dynamics-urban-development',
      'geography-2021-hl-p2-q6c-population-dynamics-rural-development',
      'geography-2021-hl-p2-q6c-language-religion',
      'geography-2021-hl-p2-q6c-language-urban-development',
      'geography-2021-hl-p2-q6c-language-rural-development',
      'geography-2021-hl-p2-q6c-religion-urban-development',
      'geography-2021-hl-p2-q6c-religion-rural-development',
      'geography-2021-hl-p2-q6c-urban-development-rural-development',
      'geography-2022-ol-p2-q2c',
      'geography-2022-ol-p2-q12c',
    ]);
    expect(LEGACY.filter(card => card.sourceMaterial)).toHaveLength(118);

    for (const card of ALL.filter(entry => entry.sourceMaterial)) {
      const generated = authored.cards.find(entry => entry.id === card.id)!;
      expect(card.sourceMaterial?.kind).toBe('source-illustration');
      expect(card.sourceMaterial?.pages).toEqual(card.sourceMaterial?.sourceFileid
        ? [1]
        : [generated.paperPage]);
      expect(card.sourceMaterial!.attribution, card.id)
        .toContain('State Examinations Commission');
      expect(card.sourceMaterial!.presentationNote, card.id)
        .toMatch(/official|exact/i);
      for (const source of card.additionalSourceMaterials ?? []) {
        expect(source.sourceFileid, card.id).toMatch(/^LC005CLP(?:C00|003|004)EV(?:\.jpg)?$/);
        expect(source.pages, card.id).toEqual([1]);
        expect(source.attribution, card.id).toContain('State Examinations Commission');
      }
    }
  });

  it('keeps source-backed prompts to the actionable question text', () => {
    const volcanoes = byId.get('geography-2021-hl-p2-q3a')!;
    expect(volcanoes.questionText).toMatch(/^\(i\) Name the volcano/);
    expect(volcanoes.questionText).not.toMatch(/Java Sea Volcanoes|geology\.com|Australian Plate Trench/i);
    expect(volcanoes.sourceMaterial?.title).toBe('Official question page');

    const mapProfile = byId.get('geography-2026-hl-p1-q8')!;
    expect(mapProfile.questionText).toMatch(/^\(i\) What type of forestry/);
    expect(mapProfile.additionalSourceMaterials?.map(source => source.title)).toEqual([
      'Official 1:50 000 map extract',
      'Official Ordnance Survey legend',
    ]);
  });

  it('uses the Geography allocation grammar and reconciles every tariff', () => {
    expect(ALL.every(isRubricCard)).toBe(true);
    expect(ALL.every(card => card.rubric.system === 'geography')).toBe(true);
    expect(ALL.every(tariffReconciles)).toBe(true);

    for (const card of LEGACY) {
      if (card.rubric.system !== 'geography') throw new Error(`${card.id}: wrong rubric`);
      expect(card.rubric.criteria).toHaveLength(1);
      const criterion = card.rubric.criteria[0];
      expect(criterion.maxMarks, card.id).toBe(card.totalMarks);
      expect(criterion.permittedMarks, card.id)
        .toEqual(Array.from({ length: card.totalMarks + 1 }, (_, mark) => mark));
      expect(criterion.guidance.length, card.id).toBeGreaterThan(0);
      if (criterion.guidanceKind === 'srp') {
        expect(card.rubric.srpMarks, card.id).toBe(card.level === 'higher' ? 2 : 3);
        expect(card.rubric.markingGuideNote, card.id).toMatch(/not exhaustive/i);
      } else {
        expect(card.rubric.srpMarks, card.id).toBeUndefined();
      }
    }
    expect(LEGACY.filter(card => card.rubric.system === 'geography'
      && card.rubric.criteria[0].guidanceKind === 'exact')).toHaveLength(106);
    expect(LEGACY.filter(card => card.rubric.system === 'geography'
      && card.rubric.criteria[0].guidanceKind === 'srp')).toHaveLength(270);
  });

  it('turns a single published allocation into the scheduler grade', () => {
    const card = HIGHER.find(entry => entry.id === 'geography-2021-hl-p2-q1c')!;
    const scoreId = geographyScoreId('published-allocation');
    expect(geographyMarks(card, { [scoreId]: 21 })).toBe(21);
    expect(suggestRubricGrade(card, { [scoreId]: 21 })).toBe('got');
    expect(geographyMarks(card, { [scoreId]: 999 })).toBe(card.totalMarks);

    // A reviewed card adds its published allocation lines.
    const reviewed = HIGHER.find(entry => entry.id === 'geography-2025-hl-p2-q2b-route-ii')!;
    expect(geographyMarks(reviewed, {
      [geographyScoreId('c1')]: 4, [geographyScoreId('c2')]: 2, [geographyScoreId('c3')]: 16,
    })).toBe(22);
    expect(suggestRubricGrade(reviewed, {
      [geographyScoreId('c1')]: 4, [geographyScoreId('c2')]: 2, [geographyScoreId('c3')]: 16,
    })).toBe('got');
  });

  it('files every card under the canonical Geography syllabus', () => {
    const topicIds = new Set(GEOGRAPHY_STRANDS.flatMap(strand =>
      strand.topics.map(topic => topic.id)));
    expect(topicIds.size).toBeGreaterThan(40);
    expect(ALL.filter(card => !topicIds.has(card.topicId)).map(card =>
      `${card.id}: ${card.topicId}`)).toEqual([]);
    expect(new Set(ALL.map(card => card.topicId)).size).toBe(50);
  });
});

describe('independently reviewed Geography sittings', () => {
  const sitting = (year: number, level: string) => {
    const found = reviewAudit.reviewedSittings.find(entry =>
      entry.year === year && entry.level === level);
    if (!found) throw new Error(`${year} ${level} is not reviewed`);
    return found;
  };

  it('pins the 2026 Higher review: every page, every priced task, every route', () => {
    const review = sitting(2026, 'higher');
    expect(review.lang).toBe('ev');
    expect(review.taskCount).toBe(113);
    expect(review.cardCount).toBe(126);
    expect(review.tasks).toHaveLength(113);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(48);
    expect(Object.keys(review.pageReview.paper2)).toHaveLength(20);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(66);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005ALP042EV.pdf', pages: 48 });
    expect(review.sources.paper2).toMatchObject({ fileid: 'LC005ALP043EV.pdf', pages: 20 });
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005ALP000EV.pdf', pages: 66 });
    // Every printed question total is the paper's own tariff.
    for (const [question, marks] of Object.entries(review.questionTotals)) {
      expect(marks, question).toBe(question.startsWith('Part 1')
        ? 8 : /Q\d+A$/.test(question) ? 20 : /Q\d+[BC]$/.test(question) ? 30 : 80);
    }
    expect(Object.keys(review.questionTotals)).toHaveLength(12 + 36 + 12);
    // Finite printed routes: 2B (i) x three landform families + (ii), 3B one
    // of three, 5C C(4,2), 14 C(4,3).
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2026 HL Part 2 Q2B': 4,
      '2026 HL Part 2 Q3B': 3,
      '2026 HL Part 2 Q5C': 6,
      '2026 HL Part 2 Q14': 4,
    });
  });

  it.each([
    [2026, 'higher', 73, 53, 'geography-2026-hl-p1-q2'],
    [2026, 'ordinary', 58, 78, 'geography-2026-ol-p2-q1c'],
    [2025, 'higher', 80, 63, 'geography-2025-hl-p1-q1'],
    [2025, 'ordinary', 52, 79, 'geography-2025-ol-p2-q3b-carbonation-onion-weathering'],
    [2024, 'higher', 66, 61, 'geography-2024-hl-p1-q2'],
    [2024, 'ordinary', 49, 98, 'geography-2024-ol-p2-q1b'],
  ] as const)('keeps every shipped %s %s id and adds only newly separated parts',
    (year, level, legacy, added, corrected) => {
      const review = sitting(year, level);
      const ids = new Set(ALL.filter(card => card.year === year && card.level === level)
        .map(card => card.id));
      expect(review.legacyIds).toHaveLength(legacy);
      expect(review.legacyIds.filter((id: string) => !ids.has(id))).toEqual([]);
      expect(review.addedIds).toHaveLength(added);
      expect(new Set([...review.legacyIds, ...review.addedIds])).toEqual(ids);
      expect(review.idCorrections.map((row: { id: string }) => row.id)).toContain(corrected);
    });

  it('pins the 2026 Ordinary review: every page, every priced roman, every route', () => {
    const review = sitting(2026, 'ordinary');
    expect(review.taskCount).toBe(126);
    expect(review.cardCount).toBe(136);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(40);
    expect(Object.keys(review.pageReview.paper2)).toHaveLength(20);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(34);
    for (const [question, marks] of Object.entries(review.questionTotals)) {
      expect(marks, question).toBe(question.startsWith('Part 1')
        ? 10 : /Q\d+B$/.test(question) ? 40 : 30);
    }
    expect(Object.keys(review.questionTotals)).toHaveLength(12 + 36);
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2026 OL Part 2 Q1B': 2,
      '2026 OL Part 2 Q2C': 4,
      '2026 OL Part 2 Q3C': 3,
      '2026 OL Part 2 Q5B': 3,
      '2026 OL Part 2 Q7B': 3,
    });
    // A dependent part carries the part it depends on, lifted from the paper.
    const advantages = byId.get('geography-2026-ol-p2-q4b-ii')!;
    expect(advantages.stem).toMatch(/\(i\) Name one example of a primary economic activity/);
    // Ordinary SRPs are worth 3 marks and move in 3-mark steps.
    const igneous = byId.get('geography-2026-ol-p2-q3b-iv')!;
    if (igneous.rubric.system !== 'geography') throw new Error('wrong rubric');
    expect(igneous.rubric.criteria[0].permittedMarks).toEqual([0, 3, 6, 9, 12, 15, 18, 21, 24, 27]);
    const sketch = byId.get('geography-2026-ol-p2-q1a')!;
    if (sketch.rubric.system !== 'geography') throw new Error('wrong rubric');
    expect(sketch.rubric.criteria.map(c => c.maxMarks)).toEqual([1, 2, 2, 5, 5, 5, 5, 5]);
    expect(sketch.rubric.criteria[3].permittedMarks).toEqual([0, 1, 2, 3, 5]);
  });

  it('carries the published allocation line by line on every reviewed card', () => {
    expect(REVIEWED).toHaveLength(810);
    for (const card of REVIEWED) {
      if (card.rubric.system !== 'geography') throw new Error(`${card.id}: wrong rubric`);
      const { criteria } = card.rubric;
      expect(criteria.length, card.id).toBeGreaterThan(0);
      expect(criteria.reduce((sum, c) => sum + c.maxMarks, 0), card.id).toBe(card.totalMarks);
      for (const criterion of criteria) {
        expect(criterion.permittedMarks[0], card.id).toBe(0);
        expect(criterion.permittedMarks.at(-1), card.id).toBe(criterion.maxMarks);
        expect(criterion.guidance.length, `${card.id} ${criterion.label}`).toBeGreaterThan(0);
      }
      expect(card.qa.humanReviewedBy).toBe('independent-paper-and-scheme-review');
    }
    const routeI = byId.get('geography-2026-hl-p2-q2b-route-i-glacial-landform')!;
    const routeII = byId.get('geography-2026-hl-p2-q2b-route-ii')!;
    if (routeI.rubric.system !== 'geography' || routeII.rubric.system !== 'geography') {
      throw new Error('wrong rubric');
    }
    // The old reader gave route (i) a one-line stub and route (ii) route (i)'s
    // allocation followed by its own.
    expect(routeI.rubric.criteria.map(c => c.label))
      .toEqual(['Process of erosion identified', 'Landform named', 'Examination']);
    expect(routeII.rubric.criteria.map(c => c.label))
      .toEqual(['Factors identified', 'Mass movement process named', 'Description/explanation']);
    expect(routeII.rubric.criteria.flatMap(c => c.guidance).join(' '))
      .not.toMatch(/Process of erosion/);
    const option = byId.get('geography-2026-hl-p2-q13')!;
    if (option.rubric.system !== 'geography') throw new Error('wrong rubric');
    expect(option.rubric.criteria.map(c => [c.maxMarks, c.permittedMarks.length]))
      .toEqual([[60, 61], [20, 6]]);
    expect(option.rubric.criteria[1].permittedMarks).toEqual([0, 6, 10, 14, 17, 20]);
  });

  it('pins the 2025 Higher review and its newly wired Oughterard companions', () => {
    const review = sitting(2025, 'higher');
    expect(review.taskCount).toBe(115);
    expect(review.cardCount).toBe(143);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(48);
    expect(Object.keys(review.pageReview.paper2)).toHaveLength(20);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(70);
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.pdf', bytes: 19789910 });
    expect(review.sources.legend).toMatchObject({ fileid: 'LC005CLPC00EV.pdf', bytes: 4055991 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.jpg', bytes: 5572138 });
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2025 HL Part 2 Q2B': 4, '2025 HL Part 2 Q3B': 4, '2025 HL Part 2 Q3C': 2,
      '2025 HL Part 2 Q5C': 2, '2025 HL Part 2 Q7B': 3, '2025 HL Part 2 Q9B': 9,
      '2025 HL Part 2 Q10B': 3, '2025 HL Part 2 Q11C': 3, '2025 HL Part 2 Q14': 4,
      '2025 HL Part 2 Q16': 4,
    });
    // Previously held: these tasks name the separate map, legend or aerial.
    for (const id of ['geography-2025-hl-p1-q7', 'geography-2025-hl-p1-q8', 'geography-2025-hl-p1-q9',
      'geography-2025-hl-p2-q1a', 'geography-2025-hl-p2-q7a', 'geography-2025-hl-p2-q8b',
      'geography-2025-hl-p2-q10a', 'geography-2025-hl-p2-q12b']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
    expect(census.exclusions.filter(row => row.year === 2025 && row.level === 'higher')).toEqual([]);
  });

  it('pins the 2025 Ordinary review: every priced roman and its Oughterard companions', () => {
    const review = sitting(2025, 'ordinary');
    expect(review.taskCount).toBe(119);
    expect(review.cardCount).toBe(131);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(40);
    expect(Object.keys(review.pageReview.paper2)).toHaveLength(16);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(36);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005GLP042EV.pdf', pages: 40 });
    expect(review.sources.paper2).toMatchObject({ fileid: 'LC005GLP043EV.pdf', pages: 16 });
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005GLP000EV.pdf', pages: 36 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.jpg', bytes: 5572138 });
    for (const [question, marks] of Object.entries(review.questionTotals)) {
      expect(marks, question).toBe(question.startsWith('Part 1')
        ? 10 : /Q\d+B$/.test(question) ? 40 : 30);
    }
    expect(Object.keys(review.questionTotals)).toHaveLength(12 + 36);
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2025 OL Part 2 Q1B': 2, '2025 OL Part 2 Q1C': 4, '2025 OL Part 2 Q2C': 3,
      '2025 OL Part 2 Q3B(ii)': 3, '2025 OL Part 2 Q5B': 3, '2025 OL Part 2 Q7C': 3,
    });
    // 3B(i) is priced on its own (4m); the shipped weathering pairs keep
    // their ids on the choose-two routes of 3B(ii) (36m).
    expect(byId.get('geography-2025-ol-p2-q3b-i')?.totalMarks).toBe(4);
    expect(byId.get('geography-2025-ol-p2-q3b-freeze-thaw-action-carbonation')?.totalMarks).toBe(36);
    // Previously held: these tasks name the separate map, legend or aerial.
    for (const id of ['geography-2025-ol-p1-q5', 'geography-2025-ol-p1-q6', 'geography-2025-ol-p1-q7',
      'geography-2025-ol-p2-q1a', 'geography-2025-ol-p2-q7a', 'geography-2025-ol-p2-q8b',
      'geography-2025-ol-p2-q10a', 'geography-2025-ol-p2-q12b']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
    expect(census.exclusions.filter(row => row.year === 2025 && row.level === 'ordinary')).toEqual([]);
  });

  it('pins the 2024 Higher review and its newly wired Bantry companions', () => {
    const review = sitting(2024, 'higher');
    expect(review.taskCount).toBe(111);
    expect(review.cardCount).toBe(127);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(48);
    expect(Object.keys(review.pageReview.paper2)).toHaveLength(20);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(64);
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.pdf', bytes: 14358379 });
    expect(review.sources.legend).toMatchObject({ fileid: 'LC005CLPC00EV.pdf', bytes: 626267 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.jpg', bytes: 5609640 });
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2024 HL Part 2 Q1B': 3, '2024 HL Part 2 Q2B': 4, '2024 HL Part 2 Q4B': 2,
      '2024 HL Part 2 Q4C': 6, '2024 HL Part 2 Q5B': 2, '2024 HL Part 2 Q10B': 2,
      '2024 HL Part 2 Q17': 4,
    });
    // 10B prints a choice of evidence: each route carries only the document it names.
    expect(byId.get('geography-2024-hl-p2-q10b-aerial-photograph')?.sourceMaterial?.sourceFileid)
      .toBe('LC005CLP004EV.jpg');
    const mapRoute = byId.get('geography-2024-hl-p2-q10b-ordnance-survey-map')!;
    expect([mapRoute.sourceMaterial, ...(mapRoute.additionalSourceMaterials ?? [])]
      .map(source => source?.sourceFileid)).toEqual(['LC005CLP003EV', 'LC005CLPC00EV']);
    // Previously held: these tasks name the separate map, legend or aerial.
    for (const id of ['geography-2024-hl-p1-q1', 'geography-2024-hl-p1-q7', 'geography-2024-hl-p1-q8',
      'geography-2024-hl-p1-q9', 'geography-2024-hl-p2-q1a', 'geography-2024-hl-p2-q7a',
      'geography-2024-hl-p2-q8b', 'geography-2024-hl-p2-q10b-aerial-photograph']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
    expect(census.exclusions.filter(row => row.year === 2024 && row.level === 'higher')).toEqual([]);
  });

  it('pins the 2024 Ordinary review: every priced roman, the 12B/12C tariffs and the Bantry companions', () => {
    const review = sitting(2024, 'ordinary');
    expect(review.taskCount).toBe(132);
    expect(review.cardCount).toBe(147);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(40);
    expect(Object.keys(review.pageReview.paper2)).toHaveLength(20);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(40);
    // In 2024 the paper prints 12B at 30 marks and 12C at 40.
    for (const [question, marks] of Object.entries(review.questionTotals)) {
      const expected = question.startsWith('Part 1') ? 10
        : /Q12B$/.test(question) ? 30 : /Q12C$/.test(question) ? 40
          : /Q\d+B$/.test(question) ? 40 : 30;
      expect(marks, question).toBe(expected);
    }
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2024 OL Part 2 Q1C': 3, '2024 OL Part 2 Q2B': 2, '2024 OL Part 2 Q2C': 4,
      '2024 OL Part 2 Q4B': 3, '2024 OL Part 2 Q6C': 6, '2024 OL Part 2 Q8C': 3,
    });
    // 11C prices each reason as aerial-photograph evidence (1) plus three 3-mark SRPs.
    const bantry = byId.get('geography-2024-ol-p2-q11c')!;
    if (bantry.rubric.system !== 'geography') throw new Error('wrong rubric');
    expect(bantry.rubric.criteria[0].permittedMarks).toEqual([0, 1, 3, 4, 6, 7, 9, 10]);
    for (const id of ['geography-2024-ol-p1-q6', 'geography-2024-ol-p1-q7', 'geography-2024-ol-p1-q8',
      'geography-2024-ol-p2-q1a', 'geography-2024-ol-p2-q7a', 'geography-2024-ol-p2-q9b',
      'geography-2024-ol-p2-q10a', 'geography-2024-ol-p2-q11c', 'geography-2024-ol-p2-q12c']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
    expect(census.exclusions.filter(row => row.year === 2024)).toEqual([]);
  });

  it('attaches the right official document for every map, legend and aerial task', () => {
    const q1a = byId.get('geography-2026-hl-p2-q1a')!;
    expect([q1a.sourceMaterial, ...(q1a.additionalSourceMaterials ?? [])]
      .map(source => [source?.title, source?.sourceFileid])).toEqual([
      ['Official 1:50 000 map extract', 'LC005CLP003EV'],
      ['Official Ordnance Survey legend', 'LC005CLPC00EV'],
    ]);
    const q7a = byId.get('geography-2026-hl-p2-q7a')!;
    expect(q7a.sourceMaterial?.sourceFileid).toBe('LC005CLP004EV');
    // 2024's and 2025's aerial photographs are published by the SEC only as JPEGs.
    const aerial: Record<number, string> = {
      2024: 'LC005CLP004EV.jpg', 2025: 'LC005CLP004EV.jpg', 2026: 'LC005CLP004EV',
    };
    for (const review of reviewAudit.reviewedSittings) for (const task of review.tasks as ReviewedTask[]) {
      for (const id of task.cards) {
        const card = byId.get(id)!;
        const files = [card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
          .filter(Boolean)
          .map(source => source!.sourceFileid ?? 'page');
        // A printed evidence route ("the aerial photograph OR the map") carries only its own evidence.
        const routeSources = ('routeSources' in task ? task.routeSources : {}) as Record<string, string[]>;
        const expected = (routeSources[id] ?? task.sources).map((source: string) => ({
          page: 'page', map: 'LC005CLP003EV', legend: 'LC005CLPC00EV', aerial: aerial[review.year],
        } as Record<string, string>)[source]);
        expect(files, id).toEqual(expected);
        if (files.includes('page')) expect(card.sourceMaterial?.pages, id).toEqual([task.paperPage]);
      }
    }
  });

  it.each([
    [2026, 'higher', 36, 'LC005ALP042EV.pdf', 'LC005ALP043EV.pdf'],
    [2026, 'ordinary', 24, 'LC005GLP042EV.pdf', 'LC005GLP043EV.pdf'],
    [2025, 'higher', 36, 'LC005ALP042EV.pdf', 'LC005ALP043EV.pdf'],
    [2025, 'ordinary', 24, 'LC005GLP042EV.pdf', 'LC005GLP043EV.pdf'],
    [2024, 'higher', 36, 'LC005ALP042EV.pdf', 'LC005ALP043EV.pdf'],
    [2024, 'ordinary', 24, 'LC005GLP042EV.pdf', 'LC005GLP043EV.pdf'],
  ] as const)('files every reviewed %s %s task in the Topic Atlas under its printed question',
    (year, level, questions, part1, part2) => {
    const review = sitting(year, level);
    const union = new Map<string, Set<string>>();
    for (const task of review.tasks as ReviewedTask[]) {
      const match = task.questionRef.match(/Part (\d) Q(\d+)/)!;
      const key = `${match[1]}|${match[2]}`;
      const ids = union.get(key) ?? new Set<string>();
      for (const id of task.atlasTopicIds) ids.add(id);
      union.set(key, ids);
      for (const cardId of task.cards) {
        expect(authoredById.get(cardId)?.atlasTopicIds, cardId).toBeDefined();
      }
    }
    expect(union.size).toBe(questions);
    for (const [key, ids] of union) {
      const [part, n] = key.split('|');
      const fileid = part === '1' ? part1 : part2;
      expect(examTopicIdsForQuestion('geography', level, year, 'main', n, `p${part}`, 'ev', fileid)
        .sort(), `Part ${part} Q${n}`).toEqual([...ids].sort());
    }
    // The reference snapshot omitted Higher Part One Q5; the reviewed runtime adds it.
    expect(reviewedRuntime.questionMappings.some(row =>
      row[4] === 'LC005ALP042EV.pdf' && row[5] === '5')).toBe(true);
  });
});
