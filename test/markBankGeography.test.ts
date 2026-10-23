/** @license SPDX-License-Identifier: Apache-2.0 */
import { createHash } from 'node:crypto';
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import authored from '../components/MarkBank/cards/geography/authored.json';
import { CARDS as HIGHER } from '../components/MarkBank/cards/geography/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/geography/ordinary';
import { GEOGRAPHY_STRANDS } from '../components/MarkBank/deck';
import census from '../scripts/markbank/authored/geography-census.json';
import reviewAudit from '../scripts/markbank/authored/geography-reviewed-audit.json';
import reviewedRuntime from '../data/examTopics/geography-reviewed-question-runtime.json';
import shippedRuntime from '../data/examTopics/geography-question-runtime.json';
import { examTopicDefinition, examTopicIdsForQuestion } from '../data/examTopics/registry';
import {
  geographyMarks,
  geographyScoreId,
  suggestRubricGrade,
} from '../components/MarkBank/SessionScreen';
import { isRubricCard, tariffReconciles, type SecRubricCard } from '../types/markBank';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import { waysInSourceFromMarkBank } from '../components/WaysIn/sources';
import { paperRegionFor, questionsInDisplayOrder } from '../components/PaperTrail/paperRegion';
import { questionLabel, questionsForTopics } from '../components/PaperTrail/topics';
import type { PaperAnswerMap } from '../types/paperTrail';

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
// Every paper task is carded since the 2021 Ordinary review, so the census's
// exclusions array is empty (and JSON would type it never[]); keep its row shape.
type CensusExclusion = { year: number; level: string; part: number; questionRef: string; reason: string };
const EXCLUSIONS = census.exclusions as CensusExclusion[];
// The exact-question Atlas join that shipped before the review (English editions).
const shippedAtlasTopics = (
  level: string, year: number, paperKey: string, fileid: string, n: string,
): Set<string> => new Set(shippedRuntime.questionMappings
  .filter(row => row[0] === (level === 'higher' ? 'h' : 'o') && row[1] === 'e'
    && row[2] === year && row[3] === paperKey && row[4] === fileid && String(row[5]) === n)
  .flatMap(row => (row[6] as number[]).map(index => shippedRuntime.topicIds[index])));

describe('complete answerable Geography corpus, 2021–2026 and each reviewed earlier sitting', () => {
  it('accounts for every paper task before finite route expansion', () => {
    // 2026-10-11/12: every sitting, 2021-2026 Higher and Ordinary, was
    // independently reviewed. Their printed base tasks became separately
    // priced tasks (2026 HL 60 -> 113, 2026 OL 48 -> 126, 2025 HL 60 -> 115,
    // 2025 OL 48 -> 119, 2024 HL 60 -> 111, 2024 OL 48 -> 132, 2023 HL
    // 60 -> 119, 2023 OL 48 -> 120, 2022 HL 60 -> 118, 2022 OL 48 -> 128,
    // 2021 HL 60 -> 116, 2021 OL 48 -> 126), and every companion-held task is
    // now carded with the official map, legend and aerial: 1,443 base tasks,
    // none held. An earlier sitting joins only with its own review ledger:
    // 2020 Higher adds 114 tasks and 2020 Ordinary 120. 2019 Higher, the first single-booklet sitting, adds 113,
    // 2019 Ordinary 127, 2018 Higher 122, 2018 Ordinary 124, 2017 Higher
    // 110, 2017 Ordinary 122, 2016 Higher 106, 2016 Ordinary 118, 2015
    // Higher 105, 2015 Ordinary 102, 2014 Higher 103, 2014 Ordinary 111, 2013
    // Higher 104, 2013 Ordinary 95, 2012 Higher 106, 2012 Ordinary 108 and
    // 2011 Higher 96, 2011 Ordinary 119, 2010 Higher 99 and 2010 Ordinary
    // 102: 3,869 base tasks, every one carded. The seven parts once held (the
    // 2011 legend was never published; 2010 OL Part One Q4 is answered by the
    // scheme's labelled drawing; 2020 OL 9C is priced 27 of its printed 30)
    // are carded with exactly what the paper and scheme print.
    expect(census.paperBaseTasks).toBe(3869);
    expect(census.includedBaseTasks).toBe(3869);
    expect(census.excludedBaseTasks).toBe(0);
    expect(census.includedBaseTasks + census.excludedBaseTasks)
      .toBe(census.paperBaseTasks);
    expect(census.authoredCards).toBe(4153);
    expect(census.baseTasks).toHaveLength(3869);
    expect(census.baseTasks.filter(task => task.status === 'authored')).toHaveLength(3869);
    expect(census.baseTasks.filter(task => task.status === 'excluded')).toHaveLength(0);
    expect(EXCLUSIONS).toEqual([]);
    expect(census.sittings).toHaveLength(34);

    const expected = {
      '2010-higher': 106, '2010-ordinary': 114,
      '2011-higher': 101, '2011-ordinary': 133,
      '2012-higher': 110, '2012-ordinary': 115,
      '2013-higher': 111, '2013-ordinary': 102,
      '2014-higher': 110, '2014-ordinary': 125,
      '2015-higher': 113, '2015-ordinary': 107,
      '2016-higher': 108, '2016-ordinary': 128,
      '2017-higher': 125, '2017-ordinary': 130,
      '2018-higher': 130, '2018-ordinary': 131,
      '2019-higher': 121, '2019-ordinary': 138,
      '2020-higher': 125, '2020-ordinary': 126,
      '2021-higher': 121, '2021-ordinary': 134,
      '2022-higher': 130, '2022-ordinary': 134,
      '2023-higher': 132, '2023-ordinary': 128,
      '2024-higher': 119, '2024-ordinary': 140,
      '2025-higher': 127, '2025-ordinary': 127,
      '2026-higher': 118, '2026-ordinary': 134,
    } as const;
    for (const [sitting, cards] of Object.entries(expected)) {
      const [year, level] = sitting.split('-');
      expect(ALL.filter(card => card.year === Number(year) && card.level === level), sitting)
        .toHaveLength(cards);
    }
  });

  it('maps the generated manifest one-to-one to the live decks', () => {
    expect(HIGHER).toHaveLength(2007);
    expect(ORDINARY).toHaveLength(2146);
    expect(ALL).toHaveLength(4153);
    expect(authored.meta.cardCount).toBe(4153);
    expect(new Set(ALL.map(card => card.id)).size).toBe(4153);
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

  it('expands every closed choose-one route and keeps every choose-N pool as one card', () => {
    // 152 printed choose-one / (i)-or-(ii) routings; 85 choose-N-of-M pools
    // (N >= 2), each one card (choice is not a route).
    expect(census.selectionAudit).toHaveLength(237);
    expect(census.selectionAudit.filter(entry => entry.classification === 'finite-expanded'))
      .toHaveLength(152);
    expect(census.selectionAudit.filter(entry => entry.classification === 'single-card-choice'))
      .toHaveLength(85);
    for (const selection of census.selectionAudit) {
      const variants = ALL.filter(card => card.questionRef === selection.questionRef
        || card.questionRef.startsWith(`${selection.questionRef} ·`));
      expect(variants, selection.questionRef).toHaveLength(selection.variants);
      // Each route names its printed option in questionRef.
      expect(new Set(variants.map(card => card.questionRef)).size, selection.questionRef)
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

  it('holds no companion task back and ships each with its official map, legend or aerial', () => {
    // Every task is carded: nothing is held, for a missing source or anything else.
    expect(EXCLUSIONS).toEqual([]);

    for (const exclusion of EXCLUSIONS) {
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

describe('parts whose source or allocation the SEC left incomplete', () => {
  const rubricOf = (id: string) => {
    const card = byId.get(id)!;
    if (card.rubric.system !== 'geography') throw new Error(`${id}: wrong rubric`);
    return card.rubric;
  };
  const LEGEND = /^The SEC did not publish a legend for the 2011 Ordnance Survey map/;

  it('cards the 2011 symbol and sketch parts with the scheme answers and a no-legend note', () => {
    const expectations: Array<[string, string[]]> = [
      ['geography-2011-hl-p1-q2', ['Q.2 · (i) · Clós, Ráth, Lios, Enclosure, Ringfort.']],
      ['geography-2011-hl-p1-q2-iii', ['(iii) · Yes']],
      ['geography-2011-ol-p1-q11', ['(i) · Parking · 2 marks', 'Boating activities · 2 marks']],
      ['geography-2011-ol-p2-q1a', ['Limits/frame = · 1 mark', 'Showing = · 3 marks graded']],
      ['geography-2011-ol-p2-q7a', ['Limits/frame = · 1 mark', 'Showing = · 3 marks graded']],
    ];
    for (const [id, lines] of expectations) {
      const rubric = rubricOf(id);
      expect(rubric.markingGuideNote, id).toMatch(LEGEND);
      expect(rubric.criteria.flatMap(c => c.guidance), id).toEqual(expect.arrayContaining(lines));
      const card = byId.get(id)!;
      // The official map, never a stand-in for the legend that does not exist.
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])].map(s => s?.sourceFileid), id)
        .toEqual(['LC005CLP003EV']);
    }
    // The sketches keep the scheme's itemised allocation, as every other year's do.
    for (const id of ['geography-2011-ol-p2-q1a', 'geography-2011-ol-p2-q7a']) {
      expect(rubricOf(id).criteria.map(c => c.maxMarks), id).toEqual([1, 2, 2, 5, 5, 5, 5, 5]);
    }
    expect(rubricOf('geography-2011-ol-p2-q1a').criteria.map(c => c.label)).toContain('A lighthouse');
  });

  it('asks 2010 OL Q4 with the paper\'s own diagram and shows the scheme\'s labelled drawing only after the reveal', () => {
    const card = byId.get('geography-2010-ol-p1-q4')!;
    // The question is the paper's print: instruction, the five printed terms, the diagram.
    expect(card.questionFigure?.src).toBe('/exam-figures/geography/markbank/geography-2010-ol-p1-q4-paper-diagram.png');
    expect(card.questionFigure?.solution).toBeUndefined();
    expect(card.questionText).toBe('Examine the diagram below. Use the following terms to fill in the blanks on '
      + 'the diagram:\nVent · Crater · Magma chamber · Lava flow · Caldera lake');
    // The answer is the scheme's labelled drawing, held back until the reveal.
    expect(card.figure?.src).toBe('/exam-figures/geography/markbank/geography-2010-ol-p1-q4-scheme-diagram.png');
    expect(card.figure?.solution).toBe(true);
    expect(card.sourceMaterial?.pages).toEqual([4]);
    // Ways In runs before the reveal: it gets the paper's diagram, never the scheme's.
    expect(waysInSourceFromMarkBank(card, 'Geography').figure?.src).toMatch(/q4-paper-diagram\.png$/);
    expect(waysInSourceFromMarkBank(byId.get('geography-2011-hl-p1-q2')!, 'Geography').figure?.alt)
      .toMatch(/^Crop of the official 2011/);
    // Each printed term is its own scheme line, as the drawing's boxes print them.
    expect(rubricOf('geography-2010-ol-p1-q4').criteria.map(c => [c.label, c.maxMarks, c.guidance])).toEqual([
      ['Vent', 2, ['Five terms @ 2 marks each as follows:', 'Vent']], ['Crater', 2, ['Crater']],
      ['Magma Chamber', 2, ['Magma Chamber']], ['Lava Flow', 2, ['Lava Flow']], ['Caldera Lake', 2, ['Caldera Lake']],
    ]);
  });

  it('cards 2020 OL 9C with its two priced lines against the printed 30, leaving the unpublished 3 unpriced', () => {
    const card = byId.get('geography-2020-ol-p2-q9c')!;
    const rubric = rubricOf(card.id);
    expect(card.totalMarks).toBe(30);
    expect(rubric.criteria.map(c => [c.label, c.maxMarks, c.permittedMarks, c.guidance])).toEqual([
      ['Impact identified', 3, [0, 3], ['Impact identified 1 SRP · 3m']],
      ['Explanation', 24, [0, 3, 6, 9, 12, 15, 18, 21, 24], ['Explanation 8 SRP’s @ 3m each · 24m']],
    ]);
    expect(rubric.unpricedMarks).toBe(3);
    // The printed tariff still reconciles: 3 + 24 priced, 3 declared unpriced.
    expect(tariffReconciles(card)).toBe(true);
    expect(tariffReconciles({ ...card, rubric: { ...rubric, unpricedMarks: undefined } })).toBe(false);
    expect(rubric.markingGuideNote).toMatch(/^The published scheme prices 27 of the printed 30 marks .* at most 27 of the 30\./);
    // Every SRP awarded: the placement stops at the 27 the scheme prices.
    const full = Object.fromEntries(rubric.criteria.map(c => [geographyScoreId(c.id), c.maxMarks]));
    expect(geographyMarks(card, full)).toBe(27);
  });

  it('binds only real crops of official documents, each on disk with its recorded hash', () => {
    const crops = ALL.flatMap(card => [card.questionFigure, card.figure]
      .filter(figure => figure !== undefined).map(figure => ({ id: card.id, figure: figure! })));
    expect(crops.map(({ figure }) => figure.candId).sort()).toEqual([
      'geography-2010-ol-p1-q4-paper-diagram', 'geography-2010-ol-p1-q4-scheme-diagram',
      'geography-2011-hl-p1-q2-i-map-crop', 'geography-2011-hl-p1-q2-iii-map-crop',
      'geography-2011-ol-p1-q11-i-map-crop',
    ]);
    const files = new Set<string>();
    for (const { id, figure } of crops) {
      expect(figure.src, id).toMatch(/^\/exam-figures\/geography\/markbank\/[a-z0-9-]+\.png$/);
      const path = resolve(__dirname, '..', 'public', figure.src.replace(/^\//, ''));
      expect(existsSync(path), id).toBe(true);
      expect(createHash('md5').update(readFileSync(path)).digest('hex'), id).toBe(figure.srcHash);
      expect(figure.attribution, id).toMatch(/State Examinations Commission/);
      expect(figure.alt.length, id).toBeGreaterThan(80);
      files.add(figure.src.split('/').pop()!);
    }
    // Every crop in the folder is bound to a card (the PNGs are committed, not ignored).
    const folder = resolve(__dirname, '..', 'public', 'exam-figures', 'geography', 'markbank');
    expect(readdirSync(folder).filter(name => name.endsWith('.png')).sort()).toEqual([...files].sort());
    expect(byId.get('geography-2011-hl-p1-q2')!.figure?.solution).toBeUndefined();
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
    // Since the 2021 Ordinary review every card comes from a reviewed sitting,
    // whose source checks are pinned task by task below; no unreviewed card
    // remains to fall back on the generic reader.
    expect(LEGACY).toEqual([]);

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
      // Map (003), legend (C00) and aerial (004); 2010's legend sheet is the
      // common-level JPEG LC005CLP000EV.jpg.
      for (const source of card.additionalSourceMaterials ?? []) {
        expect(source.sourceFileid, card.id).toMatch(/^LC005CLP(?:C00|000|003|004)EV(?:\.jpg)?$/);
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

    // No card falls back on a single whole-question allocation any more:
    // every card carries the scheme's own allocation lines.
    expect(ALL.filter(card => card.rubric.system === 'geography'
      && card.rubric.criteria.some(criterion => criterion.id === 'published-allocation'))
      .map(card => card.id)).toEqual([]);
  });

  it('turns the published allocation lines into the scheduler grade', () => {
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
    // 51 since the 2022 Higher review files 6C (industrial decline) under the
    // Dynamics of Regions.
    expect(new Set(ALL.map(card => card.topicId)).size).toBe(51);
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
    expect(review.cardCount).toBe(118);
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
    });
  });

  it.each([
    [2026, 'higher', 73, 53, 'geography-2026-hl-p1-q2'],
    [2026, 'ordinary', 58, 78, 'geography-2026-ol-p2-q1c'],
    [2025, 'higher', 80, 63, 'geography-2025-hl-p1-q1'],
    [2025, 'ordinary', 52, 79, 'geography-2025-ol-p2-q3b-freeze-thaw-action-carbonation'],
    [2024, 'higher', 66, 61, 'geography-2024-hl-p1-q2'],
    [2024, 'ordinary', 49, 93, 'geography-2024-ol-p2-q1b'],
  ] as const)('keeps every shipped %s %s id (live or progress-aliased) and adds only newly separated parts',
    (year, level, legacy, added, corrected) => {
      const review = sitting(year, level);
      const ids = new Set(ALL.filter(card => card.year === year && card.level === level)
        .map(card => card.id));
      expect(review.legacyIds).toHaveLength(legacy);
      // A shipped combination card of a choose-N pool is withdrawn and its
      // progress aliased to the pool's one card; every other shipped id is live.
      const aliased = new Map<string, string>((review.aliases as { id: string; canonicalId: string }[])
        .map(row => [row.id, row.canonicalId] as [string, string]));
      for (const id of review.legacyIds as string[]) {
        expect(ids.has(id) || ids.has(aliased.get(id) ?? ''), id).toBe(true);
        expect(ids.has(id) && aliased.has(id), id).toBe(false);
      }
      expect(review.addedIds).toHaveLength(added);
      expect(new Set([...review.legacyIds.filter((id: string) => !aliased.has(id)), ...review.addedIds]))
        .toEqual(ids);
      expect(review.idCorrections.map((row: { id: string }) => row.id)).toContain(corrected);
    });

  it('pins the 2026 Ordinary review: every page, every priced roman, every route', () => {
    const review = sitting(2026, 'ordinary');
    expect(review.taskCount).toBe(126);
    expect(review.cardCount).toBe(134);
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
    expect(REVIEWED).toHaveLength(4153);
    expect(REVIEWED.filter(card => card.rubric.system === 'geography' && card.rubric.unpricedMarks)
      .map(card => card.id)).toEqual(['geography-2020-ol-p2-q9c']);
    for (const card of REVIEWED) {
      if (card.rubric.system !== 'geography') throw new Error(`${card.id}: wrong rubric`);
      const { criteria } = card.rubric;
      expect(criteria.length, card.id).toBeGreaterThan(0);
      // Only a printed remainder the scheme allocates to no line stays out of
      // the criteria (2020 OL 9C, 3 of 30); it is never derived into one.
      const unpriced = card.rubric.unpricedMarks ?? 0;
      expect(criteria.reduce((sum, c) => sum + c.maxMarks, 0) + unpriced, card.id).toBe(card.totalMarks);
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

  it('never repeats the question as an examiner direction', () => {
    // Most 2017-2021 Ordinary schemes reprint each question above its
    // allocation; 369 cards once listed that reprint as an examiner direction
    // (and 2019 HL Q1(iii) listed part (iv)'s answer). A direction is the
    // scheme's guidance, never the question again.
    const words = (value: string) => value.toLowerCase().replace(/[^\p{L}\p{N}_]+/gu, ' ').trim();
    const unlabel = (value: string) => value.trim().replace(/^\((?:i|ii|iii|iv|v|vi|vii|viii|ix|x)\)\s*(?:·\s*)?/, '');
    let directions = 0;
    for (const card of authored.cards) {
      const lines = new Set(card.questionText.split('\n').map(line => words(unlabel(line))));
      const asked = ` ${words(card.questionText)} `;
      for (const direction of card.directions ?? []) {
        directions += 1;
        const said = words(unlabel(direction));
        expect(lines.has(said), `${card.id}: ${direction}`).toBe(false);
        if (said.split(' ').length >= 4) expect(asked.includes(` ${said} `), `${card.id}: ${direction}`).toBe(false);
      }
    }
    expect(directions).toBeGreaterThan(0);
    expect(authoredById.get('geography-2019-hl-p1-q1-iii')?.directions).toEqual([]);
    expect(authoredById.get('geography-2019-ol-p2-q3b-ii')?.directions).toEqual([
      'Allow one SRP for relevant annotated diagram.',
      'Relevant information, additional to the text, given on the diagrams can be awarded SRP’s.',
      'At least one SRP for explanation.',
    ]);
  });

  it('pins the 2025 Higher review and its newly wired Oughterard companions', () => {
    const review = sitting(2025, 'higher');
    expect(review.taskCount).toBe(115);
    expect(review.cardCount).toBe(127);
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
      '2025 HL Part 2 Q5C': 2, '2025 HL Part 2 Q9B': 3, '2025 HL Part 2 Q11C': 3,
    });
    // Previously held: these tasks name the separate map, legend or aerial.
    for (const id of ['geography-2025-hl-p1-q7', 'geography-2025-hl-p1-q8', 'geography-2025-hl-p1-q9',
      'geography-2025-hl-p2-q1a', 'geography-2025-hl-p2-q7a', 'geography-2025-hl-p2-q8b',
      'geography-2025-hl-p2-q10a', 'geography-2025-hl-p2-q12b']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
    expect(EXCLUSIONS.filter(row => row.year === 2025 && row.level === 'higher')).toEqual([]);
  });

  it('pins the 2025 Ordinary review: every priced roman and its Oughterard companions', () => {
    const review = sitting(2025, 'ordinary');
    expect(review.taskCount).toBe(119);
    expect(review.cardCount).toBe(127);
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
      '2025 OL Part 2 Q7C': 3,
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
    expect(EXCLUSIONS.filter(row => row.year === 2025 && row.level === 'ordinary')).toEqual([]);
  });

  it('pins the 2024 Higher review and its newly wired Bantry companions', () => {
    const review = sitting(2024, 'higher');
    expect(review.taskCount).toBe(111);
    expect(review.cardCount).toBe(119);
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
      '2024 HL Part 2 Q5B': 2, '2024 HL Part 2 Q10B': 2,
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
    expect(EXCLUSIONS.filter(row => row.year === 2024 && row.level === 'higher')).toEqual([]);
  });

  it('pins the 2024 Ordinary review: every priced roman, the 12B/12C tariffs and the Bantry companions', () => {
    const review = sitting(2024, 'ordinary');
    expect(review.taskCount).toBe(132);
    expect(review.cardCount).toBe(140);
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
      '2024 OL Part 2 Q8C': 3,
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
    expect(EXCLUSIONS.filter(row => row.year === 2024)).toEqual([]);
  });

  it('pins the 2023 Higher review and its newly wired Cavan companions', () => {
    const review = sitting(2023, 'higher');
    expect(review.taskCount).toBe(119);
    expect(review.cardCount).toBe(132);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(48);
    expect(Object.keys(review.pageReview.paper2)).toHaveLength(20);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(64);
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.pdf', bytes: 4959287 });
    expect(review.sources.legend).toMatchObject({ fileid: 'LC005CLPC00EV.pdf', bytes: 836095 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.jpg', bytes: 5597283 });
    expect(review.legacyIds).toHaveLength(78);
    expect(review.addedIds).toHaveLength(68);
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2023 HL Part 2 Q2B': 4, '2023 HL Part 2 Q2C': 2, '2023 HL Part 2 Q3B': 3,
      '2023 HL Part 2 Q3C': 4, '2023 HL Part 2 Q8B': 3, '2023 HL Part 2 Q11B': 3,
    });
    // Part One Q6(ii) prices its two statements at 1 mark each.
    expect(byId.get('geography-2023-hl-p1-q6-ii-a')?.totalMarks).toBe(1);
    expect(byId.get('geography-2023-hl-p1-q6-ii-b')?.totalMarks).toBe(1);
    // Previously held: these tasks name the separate map, legend or aerial.
    for (const id of ['geography-2023-hl-p1-q1', 'geography-2023-hl-p1-q7', 'geography-2023-hl-p1-q8',
      'geography-2023-hl-p1-q9', 'geography-2023-hl-p2-q1a', 'geography-2023-hl-p2-q7a',
      'geography-2023-hl-p2-q8c', 'geography-2023-hl-p2-q10a', 'geography-2023-hl-p2-q12b']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
    expect(EXCLUSIONS.filter(row => row.year === 2023 && row.level === 'higher')).toEqual([]);
  });

  it('pins the 2023 Ordinary review: every priced roman and the Cavan companions', () => {
    const review = sitting(2023, 'ordinary');
    expect(review.taskCount).toBe(120);
    expect(review.cardCount).toBe(128);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(40);
    expect(Object.keys(review.pageReview.paper2)).toHaveLength(20);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(40);
    expect(review.legacyIds).toHaveLength(52);
    expect(review.addedIds).toHaveLength(80);
    for (const [question, marks] of Object.entries(review.questionTotals)) {
      const expected = question.startsWith('Part 1') ? 10 : /Q\d+B$/.test(question) ? 40 : 30;
      expect(marks, question).toBe(expected);
    }
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2023 OL Part 2 Q2C': 4, '2023 OL Part 2 Q3B': 2, '2023 OL Part 2 Q3C': 3, '2023 OL Part 2 Q9C': 3,
    });
    // Part One Q2 prints (i) and (ii) in one part-completed table; each roman keeps its own rows.
    expect(byId.get('geography-2023-ol-p1-q2')?.totalMarks).toBe(4);
    expect(byId.get('geography-2023-ol-p1-q2-ii')?.totalMarks).toBe(6);
    // 2B(i) is separately priced; the shipped 2B id now holds the 36m choose-two card.
    expect(byId.get('geography-2023-ol-p2-q2b-i')?.totalMarks).toBe(4);
    expect(byId.get('geography-2023-ol-p2-q2b-onion-weathering-carbonation')?.totalMarks).toBe(36);
    for (const id of ['geography-2023-ol-p1-q6', 'geography-2023-ol-p1-q7', 'geography-2023-ol-p1-q8',
      'geography-2023-ol-p2-q1a', 'geography-2023-ol-p2-q7a', 'geography-2023-ol-p2-q8b',
      'geography-2023-ol-p2-q10a', 'geography-2023-ol-p2-q11b']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
    expect(EXCLUSIONS.filter(row => row.year === 2023)).toEqual([]);
  });

  it('pins the 2022 Higher review and its newly wired Clonmel companions', () => {
    const review = sitting(2022, 'higher');
    expect(review.taskCount).toBe(118);
    expect(review.cardCount).toBe(130);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(48);
    expect(Object.keys(review.pageReview.paper2)).toHaveLength(20);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(64);
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.pdf', bytes: 5462059 });
    // In 2022 the SEC publishes the legend, like the aerial photograph, only as a JPEG.
    expect(review.sources.legend).toMatchObject({ fileid: 'LC005CLPC00EV.jpg', bytes: 4251010 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.jpg', bytes: 5185646 });
    expect(review.legacyIds).toHaveLength(73);
    expect(review.addedIds).toHaveLength(67);
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2022 HL Part 2 Q1C': 4, '2022 HL Part 2 Q2B': 4, '2022 HL Part 2 Q3C': 3, '2022 HL Part 2 Q4C': 2,
      '2022 HL Part 2 Q9B': 3, '2022 HL Part 2 Q10B': 2,
    });
    // The papers print their ticks in Wingdings 2; the card shows the tick.
    expect(byId.get('geography-2022-hl-p1-q1-ii')?.questionText).toContain('ticking (✓)');
    for (const id of ['geography-2022-hl-p1-q6', 'geography-2022-hl-p1-q7', 'geography-2022-hl-p1-q8',
      'geography-2022-hl-p2-q1a', 'geography-2022-hl-p2-q7a', 'geography-2022-hl-p2-q8c',
      'geography-2022-hl-p2-q10a', 'geography-2022-hl-p2-q12c']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
    expect(EXCLUSIONS.filter(row => row.year === 2022 && row.level === 'higher')).toEqual([]);
  });

  it('pins the 2022 Ordinary review: printed tariffs, every priced roman and the Clonmel companions', () => {
    const review = sitting(2022, 'ordinary');
    expect(review.taskCount).toBe(128);
    expect(review.cardCount).toBe(134);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(40);
    expect(Object.keys(review.pageReview.paper2)).toHaveLength(24);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(40);
    expect(review.legacyIds).toHaveLength(49);
    expect(review.addedIds).toHaveLength(89);
    // In 2022 the paper prints 40 marks on these parts and 30 on the rest.
    const forty = ['1B', '2C', '3B', '4B', '5B', '6C', '7C', '8C', '9B', '10B', '11B', '12C'];
    for (const [question, marks] of Object.entries(review.questionTotals)) {
      const expected = question.startsWith('Part 1') ? 10
        : forty.some(part => question.endsWith(`Q${part}`)) ? 40 : 30;
      expect(marks, question).toBe(expected);
    }
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2022 OL Part 2 Q1B': 2, '2022 OL Part 2 Q2B': 3, '2022 OL Part 2 Q3C': 4,
    });
    // 10C prices each reason as aerial-photograph evidence (1) plus three 3-mark SRPs.
    const clonmel = byId.get('geography-2022-ol-p2-q10c')!;
    if (clonmel.rubric.system !== 'geography') throw new Error('wrong rubric');
    expect(clonmel.rubric.criteria[0].permittedMarks).toEqual([0, 1, 3, 4, 6, 7, 9, 10]);
    for (const id of ['geography-2022-ol-p1-q7', 'geography-2022-ol-p1-q8', 'geography-2022-ol-p1-q9',
      'geography-2022-ol-p2-q1a', 'geography-2022-ol-p2-q7a', 'geography-2022-ol-p2-q8c',
      'geography-2022-ol-p2-q10c', 'geography-2022-ol-p2-q11c', 'geography-2022-ol-p2-q12a']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
    expect(EXCLUSIONS.filter(row => row.year === 2022)).toEqual([]);
  });

  it('pins the 2021 Higher review and its newly wired Foxford companions', () => {
    const review = sitting(2021, 'higher');
    expect(review.taskCount).toBe(116);
    expect(review.cardCount).toBe(121);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(48);
    expect(Object.keys(review.pageReview.paper2)).toHaveLength(24);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(64);
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.pdf', bytes: 5155375 });
    expect(review.sources.legend).toMatchObject({ fileid: 'LC005CLPC00EV.pdf', bytes: 784643 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.jpg', bytes: 5536812 });
    expect(review.legacyIds).toHaveLength(75);
    expect(review.addedIds).toHaveLength(65);
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2021 HL Part 2 Q1B': 4, '2021 HL Part 2 Q2C': 3,
    });
    // 6C keeps the bare id it shipped with; its nine combination ids alias to it.
    expect(byId.get('geography-2021-hl-p2-q6c')?.questionText).toContain('Rural development');
    // Q9's location B is printed on the paper, so the scheme prices four rows.
    expect(byId.get('geography-2021-hl-p1-q9')?.totalMarks).toBe(8);
    for (const id of ['geography-2021-hl-p1-q1', 'geography-2021-hl-p1-q7', 'geography-2021-hl-p1-q8',
      'geography-2021-hl-p1-q9', 'geography-2021-hl-p2-q1a', 'geography-2021-hl-p2-q7a',
      'geography-2021-hl-p2-q8c', 'geography-2021-hl-p2-q10a', 'geography-2021-hl-p2-q11c']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
    expect(EXCLUSIONS.filter(row => row.year === 2021 && row.level === 'higher')).toEqual([]);
  });

  it('pins the 2021 Ordinary review: printed tariffs, every priced roman and the Foxford companions', () => {
    const review = sitting(2021, 'ordinary');
    expect(review.taskCount).toBe(126);
    expect(review.cardCount).toBe(134);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(40);
    expect(Object.keys(review.pageReview.paper2)).toHaveLength(20);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(36);
    expect(review.sources.legend).toMatchObject({ fileid: 'LC005CLPC00EV.pdf', bytes: 784643 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.jpg', bytes: 5536812 });
    expect(review.legacyIds).toHaveLength(49);
    expect(review.addedIds).toHaveLength(87);
    // In 2021 the paper prints 40 marks on these parts and 30 on the rest.
    const forty = ['1B', '2B', '3B', '4B', '5C', '6B', '7B', '8B', '9B', '10B', '11B', '12C'];
    for (const [question, marks] of Object.entries(review.questionTotals)) {
      const expected = question.startsWith('Part 1') ? 10
        : forty.some(part => question.endsWith(`Q${part}`)) ? 40 : 30;
      expect(marks, question).toBe(expected);
    }
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2021 OL Part 2 Q2B': 2, '2021 OL Part 2 Q2C': 4, '2021 OL Part 2 Q3C': 3, '2021 OL Part 2 Q8C': 3,
    });
    // 4C and 6B are one card each, every printed item shown.
    expect(byId.get('geography-2021-ol-p2-q4c')?.questionText).toContain('Cultural regions defined by religion.');
    for (const id of ['geography-2021-ol-p1-q6', 'geography-2021-ol-p1-q7', 'geography-2021-ol-p1-q8',
      'geography-2021-ol-p2-q1a', 'geography-2021-ol-p2-q8a', 'geography-2021-ol-p2-q9b',
      'geography-2021-ol-p2-q10a', 'geography-2021-ol-p2-q11c', 'geography-2021-ol-p2-q12c']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
  });

  it('pins the 2020 Higher review: no shipped cards, the Arklow companions, every priced part', () => {
    const review = sitting(2020, 'higher');
    expect(review.taskCount).toBe(114);
    expect(review.cardCount).toBe(125);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(48);
    expect(Object.keys(review.pageReview.paper2)).toHaveLength(20);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(52);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005ALP042EV.pdf', bytes: 3120862 });
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005ALP000EV.pdf', bytes: 689712 });
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.pdf', bytes: 4637231 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.jpg', bytes: 6218552 });
    expect(review.legacyIds).toEqual([]);
    expect(review.addedIds).toHaveLength(125);
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2020 HL Part 2 Q2B': 4, '2020 HL Part 2 Q3C': 4, '2020 HL Part 2 Q6C': 2,
      '2020 HL Part 2 Q9B': 3, '2020 HL Part 2 Q12C': 3,
    });
    for (const id of ['geography-2020-hl-p1-q6', 'geography-2020-hl-p1-q7', 'geography-2020-hl-p1-q8',
      'geography-2020-hl-p1-q9', 'geography-2020-hl-p2-q1a', 'geography-2020-hl-p2-q7a',
      'geography-2020-hl-p2-q8c', 'geography-2020-hl-p2-q10a', 'geography-2020-hl-p2-q11c']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
  });

  it('pins the 2020 Ordinary review: printed tariffs, every priced roman, and 9C against its printed total', () => {
    const review = sitting(2020, 'ordinary');
    expect(review.taskCount).toBe(120);
    expect(review.cardCount).toBe(126);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(40);
    expect(Object.keys(review.pageReview.paper2)).toHaveLength(20);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(32);
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005GLP000EV.pdf' });
    expect(review.legacyIds).toEqual([]);
    expect(review.addedIds).toHaveLength(126);
    // In 2020 the paper prints 40 marks on these parts and 30 on the rest.
    const forty = ['1B', '2B', '3B', '4B', '5C', '6B', '7B', '8B', '9B', '10C', '11C', '12C'];
    for (const [question, marks] of Object.entries(review.questionTotals)) {
      const expected = question.startsWith('Part 1') ? 10
        : forty.some(part => question.endsWith(`Q${part}`)) ? 40 : 30;
      expect(marks, question).toBe(expected);
    }
    // 9C is carded against its printed 30 marks (the scheme prices 27 of them).
    expect(review.questionTotals['Part 2 Q9C']).toBe(30);
    expect(ALL.filter(card => card.questionRef.startsWith('2020 OL Part 2 Q9C')).map(card => card.id))
      .toEqual(['geography-2020-ol-p2-q9c']);
    expect('held' in review).toBe(false);
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2020 OL Part 2 Q1C': 3, '2020 OL Part 2 Q2B': 2, '2020 OL Part 2 Q2C': 4,
    });
    for (const id of ['geography-2020-ol-p1-q5', 'geography-2020-ol-p1-q6', 'geography-2020-ol-p1-q7',
      'geography-2020-ol-p2-q1a', 'geography-2020-ol-p2-q7a', 'geography-2020-ol-p2-q8b',
      'geography-2020-ol-p2-q10b', 'geography-2020-ol-p2-q11a', 'geography-2020-ol-p2-q12c']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
  });

  it('pins the 2015 Ordinary review: one shared booklet, the Kenmare companions, every priced roman', () => {
    const review = sitting(2015, 'ordinary');
    expect(review.taskCount).toBe(102);
    expect(review.cardCount).toBe(107);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(28);
    expect(review.pageReview.paper2).toEqual(review.pageReview.paper1);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(40);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005GLP000EV.pdf', bytes: 2955016 });
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005GLP000EV.pdf', bytes: 568844 });
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.pdf', bytes: 6859305 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.pdf', bytes: 2647375 });
    expect(review.legacyIds).toEqual([]);
    expect(review.addedIds).toHaveLength(107);
    // In 2015 the paper prints 40 marks on these parts and 30 on the rest.
    const forty = ['1B', '2B', '3B', '4B', '5B', '6C', '7B', '8B', '9C', '10B', '11B', '12C'];
    for (const [question, marks] of Object.entries(review.questionTotals)) {
      const expected = question.startsWith('Part 1') ? 10
        : forty.some(part => question.endsWith(`Q${part}`)) ? 40 : 30;
      expect(marks, question).toBe(expected);
    }
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2015 OL Part 2 Q1B': 2, '2015 OL Part 2 Q3C': 3, '2015 OL Part 2 Q8C': 3,
    });
    // 4B and 6C price "Naming a region" outside their romans; it is carded with part (i).
    for (const id of ['geography-2015-ol-p2-q4b', 'geography-2015-ol-p2-q6c']) {
      const card = byId.get(id)!;
      if (card.rubric.system !== 'geography') throw new Error('wrong rubric');
      expect(card.rubric.criteria[0].guidance, id).toEqual(['Naming a region · 1m']);
    }
    for (const id of ['geography-2015-ol-p1-q5', 'geography-2015-ol-p1-q6', 'geography-2015-ol-p1-q7',
      'geography-2015-ol-p2-q1a', 'geography-2015-ol-p2-q7a', 'geography-2015-ol-p2-q9c',
      'geography-2015-ol-p2-q10c', 'geography-2015-ol-p2-q11a', 'geography-2015-ol-p2-q12c']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
  });

  it('pins the 2015 Higher review: one shared booklet, the Kenmare companions, every priced part', () => {
    const review = sitting(2015, 'higher');
    expect(review.taskCount).toBe(105);
    expect(review.cardCount).toBe(113);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(32);
    expect(review.pageReview.paper2).toEqual(review.pageReview.paper1);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(48);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005ALP000EV.pdf', bytes: 3601749 });
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005ALP000EV.pdf', bytes: 893788 });
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.pdf', bytes: 6859305 });
    expect(review.sources.legend).toMatchObject({ fileid: 'LC005CLPC00EV.pdf', bytes: 2156988 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.pdf', bytes: 2647375 });
    expect(review.legacyIds).toEqual([]);
    expect(review.addedIds).toHaveLength(113);
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2015 HL Part 2 Q1B': 4, '2015 HL Part 2 Q3B': 2, '2015 HL Part 2 Q3C': 4, '2015 HL Part 2 Q4C': 2,
    });
    // Part One prices by question in its heading, so every Part One card carries that line.
    for (const card of ALL.filter(card => card.id.startsWith('geography-2015-hl-p1-'))) {
      if (card.rubric.system !== 'geography') throw new Error('wrong rubric');
      expect(card.rubric.criteria[0].guidance[0], card.id).toMatch(/^Q\.(1, 2, 6|3, 4, 5, 7, 8, 9, 12|10|11):/);
    }
    for (const id of ['geography-2015-hl-p1-q7', 'geography-2015-hl-p1-q8', 'geography-2015-hl-p1-q9',
      'geography-2015-hl-p2-q2a', 'geography-2015-hl-p2-q8a', 'geography-2015-hl-p2-q9b',
      'geography-2015-hl-p2-q10a', 'geography-2015-hl-p2-q11b', 'geography-2015-hl-p2-q12c']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
  });

  it('pins the 2010 Ordinary review: one shared booklet, the Carrick-on-Suir JPEG companions, every priced roman', () => {
    const review = sitting(2010, 'ordinary');
    expect(review.taskCount).toBe(102);
    expect(review.cardCount).toBe(114);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(28);
    expect(review.pageReview.paper2).toEqual(review.pageReview.paper1);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(36);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005GLP000EV.pdf', bytes: 3266667 });
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005GLP000EV.pdf', bytes: 503193 });
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP004EV.jpg', bytes: 2806497 });
    expect(review.sources.legend).toMatchObject({ fileid: 'LC005CLP000EV.jpg', bytes: 1636000 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP003EV.jpg', bytes: 4062934 });
    expect('held' in review).toBe(false);
    expect(review.legacyIds).toEqual([]);
    expect(review.addedIds).toHaveLength(114);
    // In 2010 the paper prints 40 marks on these parts and 30 on the rest.
    const forty = ['1C', '2B', '3B', '4B', '5B', '6C', '7C', '8B', '9C', '10C', '11B', '12B'];
    for (const [question, marks] of Object.entries(review.questionTotals)) {
      const expected = question.startsWith('Part 1') ? 10
        : forty.some(part => question.endsWith(`Q${part}`)) ? 40 : 30;
      expect(marks, question).toBe(expected);
    }
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2010 OL Part 2 Q1B': 4, '2010 OL Part 2 Q1C': 4, '2010 OL Part 2 Q2C': 3, '2010 OL Part 2 Q3C': 2,
      '2010 OL Part 2 Q6B': 2, '2010 OL Part 2 Q9C': 3,
    });
    for (const id of ['geography-2010-ol-p1-q5', 'geography-2010-ol-p1-q7', 'geography-2010-ol-p2-q2a',
      'geography-2010-ol-p2-q8a', 'geography-2010-ol-p2-q9b', 'geography-2010-ol-p2-q10c',
      'geography-2010-ol-p2-q11b', 'geography-2010-ol-p2-q12a']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
  });

  it('pins the 2010 Higher review: one shared booklet, the Carrick-on-Suir JPEG companions, every priced part', () => {
    const review = sitting(2010, 'higher');
    expect(review.taskCount).toBe(99);
    expect(review.cardCount).toBe(106);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(32);
    expect(review.pageReview.paper2).toEqual(review.pageReview.paper1);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(41);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005ALP000EV.pdf', bytes: 3619088 });
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005ALP000EV.pdf', bytes: 855544 });
    // The SEC's 2010 names are swapped relative to later years (checked by eye).
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP004EV.jpg', bytes: 2806497 });
    expect(review.sources.legend).toMatchObject({ fileid: 'LC005CLP000EV.jpg', bytes: 1636000 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP003EV.jpg', bytes: 4062934 });
    expect(review.legacyIds).toEqual([]);
    expect(review.addedIds).toHaveLength(106);
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2010 HL Part 2 Q1B': 3, '2010 HL Part 2 Q3B': 3, '2010 HL Part 2 Q6B': 3, '2010 HL Part 2 Q20': 2,
    });
    // Part One Q9(ii)'s second answer is a lone printed "2", kept by its slice.
    const q9 = byId.get('geography-2010-hl-p1-q9-ii')!;
    if (q9.rubric.system !== 'geography') throw new Error('wrong rubric');
    expect(q9.rubric.criteria.map(c => c.guidance.at(-1))).toEqual(['(ii) 1', '2']);
    const option = byId.get('geography-2010-hl-p2-q13')!;
    if (option.rubric.system !== 'geography') throw new Error('wrong rubric');
    expect(option.rubric.criteria.map(c => c.maxMarks)).toEqual([32, 48]);
    for (const id of ['geography-2010-hl-p1-q2', 'geography-2010-hl-p1-q4', 'geography-2010-hl-p1-q8',
      'geography-2010-hl-p2-q1a', 'geography-2010-hl-p2-q7b', 'geography-2010-hl-p2-q9a',
      'geography-2010-hl-p2-q10c', 'geography-2010-hl-p2-q12c']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
  });

  it('pins the 2011 Ordinary review: one shared booklet, the Dingle map and photograph, no legend published', () => {
    const review = sitting(2011, 'ordinary');
    expect(review.taskCount).toBe(119);
    expect(review.cardCount).toBe(133);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(32);
    expect(review.pageReview.paper2).toEqual(review.pageReview.paper1);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(40);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005GLP000EV.pdf', bytes: 1469613 });
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005GLP000EV.pdf', bytes: 347448 });
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.pdf', bytes: 2360445 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.pdf', bytes: 726238 });
    expect('legend' in review.sources).toBe(false);
    expect('held' in review).toBe(false);
    expect(review.legacyIds).toEqual([]);
    expect(review.addedIds).toHaveLength(133);
    // In 2011 the paper prints 40 marks on these parts and 30 on the rest.
    const forty = ['1B', '2B', '3B', '4B', '5C', '6B', '7B', '8C', '9B', '10B', '11B', '12B'];
    for (const [question, marks] of Object.entries(review.questionTotals)) {
      const expected = question.startsWith('Part 1') ? 10
        : forty.some(part => question.endsWith(`Q${part}`)) ? 40 : 30;
      expect(marks, question).toBe(expected);
    }
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2011 OL Part 2 Q1B': 4, '2011 OL Part 2 Q2B(i)': 2, '2011 OL Part 2 Q2B(iii)': 2, '2011 OL Part 2 Q2C': 3,
      '2011 OL Part 2 Q7B(i)': 2, '2011 OL Part 2 Q7B(ii)': 2, '2011 OL Part 2 Q7B(iii)': 2, '2011 OL Part 2 Q7B(iv)': 2,
      '2011 OL Part 2 Q11C(ii)': 4,
    });
    for (const id of ['geography-2011-ol-p1-q10', 'geography-2011-ol-p1-q11-ii', 'geography-2011-ol-p1-q12',
      'geography-2011-ol-p2-q8b', 'geography-2011-ol-p2-q12a', 'geography-2011-ol-p2-q12b']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
  });

  it('pins the 2011 Higher review: one shared booklet, the Dingle map and photograph, no legend published', () => {
    const review = sitting(2011, 'higher');
    expect(review.taskCount).toBe(96);
    expect(review.cardCount).toBe(101);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(32);
    expect(review.pageReview.paper2).toEqual(review.pageReview.paper1);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(48);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005ALP000EV.pdf', bytes: 4390619 });
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005ALP000EV.pdf', bytes: 1286377 });
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.pdf', bytes: 2360445 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.pdf', bytes: 726238 });
    // The SEC published no 2011 legend sheet: no source and no card names one.
    expect('legend' in review.sources).toBe(false);
    expect(ALL.filter(card => card.year === 2011)
      .flatMap(card => [card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])])
      .filter(source => source?.sourceFileid?.startsWith('LC005CLPC00'))).toEqual([]);
    expect('held' in review).toBe(false);
    expect(review.legacyIds).toEqual([]);
    expect(review.addedIds).toHaveLength(101);
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2011 HL Part 2 Q1C': 3, '2011 HL Part 2 Q2B': 4,
    });
    const option = byId.get('geography-2011-hl-p2-q13')!;
    if (option.rubric.system !== 'geography') throw new Error('wrong rubric');
    expect(option.rubric.criteria.map(c => c.maxMarks)).toEqual([32, 48]);
    for (const id of ['geography-2011-hl-p1-q2-ii', 'geography-2011-hl-p1-q3', 'geography-2011-hl-p2-q1a',
      'geography-2011-hl-p2-q7b', 'geography-2011-hl-p2-q8a', 'geography-2011-hl-p2-q10a',
      'geography-2011-hl-p2-q11c', 'geography-2011-hl-p2-q12c']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
  });

  it('pins the 2012 Ordinary review: one shared booklet, the Carrick-on-Shannon companions, every priced roman', () => {
    const review = sitting(2012, 'ordinary');
    expect(review.taskCount).toBe(108);
    expect(review.cardCount).toBe(115);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(28);
    expect(review.pageReview.paper2).toEqual(review.pageReview.paper1);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(36);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005GLP000EV.pdf', bytes: 1496544 });
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005GLP000EV.pdf', bytes: 454708 });
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.pdf', bytes: 1738631 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.pdf', bytes: 3193770 });
    expect(review.legacyIds).toEqual([]);
    expect(review.addedIds).toHaveLength(115);
    // In 2012 the paper prints 40 marks on these parts and 30 on the rest.
    const forty = ['1B', '2B', '3C', '4C', '5B', '6B', '7B', '8C', '9C', '10B', '11C', '12B'];
    for (const [question, marks] of Object.entries(review.questionTotals)) {
      const expected = question.startsWith('Part 1') ? 10
        : forty.some(part => question.endsWith(`Q${part}`)) ? 40 : 30;
      expect(marks, question).toBe(expected);
    }
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2012 OL Part 2 Q1B(iii)': 2, '2012 OL Part 2 Q2B': 2, '2012 OL Part 2 Q3B': 3, '2012 OL Part 2 Q9B': 4,
    });
    // The legend omitted the forestry symbols; the scheme awards that sketch item to all candidates.
    const q1a = byId.get('geography-2012-ol-p2-q1a')!;
    if (q1a.rubric.system !== 'geography') throw new Error('wrong rubric');
    expect(q1a.rubric.criteria.flatMap(c => c.guidance))
      .toContain('Mixed woodland shown and named · award 5 marks to all candidates');
    for (const id of ['geography-2012-ol-p1-q4', 'geography-2012-ol-p1-q6', 'geography-2012-ol-p2-q1a',
      'geography-2012-ol-p2-q7a', 'geography-2012-ol-p2-q8b', 'geography-2012-ol-p2-q10b',
      'geography-2012-ol-p2-q11a', 'geography-2012-ol-p2-q11b']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
  });

  it('pins the 2012 Higher review: one shared booklet, the Carrick-on-Shannon companions, every priced part', () => {
    const review = sitting(2012, 'higher');
    expect(review.taskCount).toBe(106);
    expect(review.cardCount).toBe(110);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(32);
    expect(review.pageReview.paper2).toEqual(review.pageReview.paper1);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(48);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005ALP000EV.pdf', bytes: 2999085 });
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005ALP000EV.pdf', bytes: 1089373 });
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.pdf', bytes: 1738631 });
    expect(review.sources.legend).toMatchObject({ fileid: 'LC005CLPC00EV.pdf', bytes: 267008 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.pdf', bytes: 3193770 });
    expect(review.legacyIds).toEqual([]);
    expect(review.addedIds).toHaveLength(110);
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2012 HL Part 2 Q2B': 2, '2012 HL Part 2 Q2C': 3, '2012 HL Part 2 Q8C': 2,
    });
    // Q12(iv) prints "Accept all answers for 2 marks"; Q8(ii) is priced whole (no split printed).
    const q12 = byId.get('geography-2012-hl-p1-q12-iv')!;
    const q8 = byId.get('geography-2012-hl-p1-q8-ii')!;
    if (q12.rubric.system !== 'geography' || q8.rubric.system !== 'geography') throw new Error('wrong rubric');
    expect(q12.rubric.criteria[0].guidance).toContain('(iv) Accept all answers for 2 marks');
    expect(q8.rubric.criteria[0].permittedMarks).toEqual([0, 2]);
    const option = byId.get('geography-2012-hl-p2-q13')!;
    if (option.rubric.system !== 'geography') throw new Error('wrong rubric');
    expect(option.rubric.criteria.map(c => c.maxMarks)).toEqual([32, 48]);
    for (const id of ['geography-2012-hl-p1-q8', 'geography-2012-hl-p1-q9', 'geography-2012-hl-p2-q1a',
      'geography-2012-hl-p2-q7b', 'geography-2012-hl-p2-q9a', 'geography-2012-hl-p2-q11b',
      'geography-2012-hl-p2-q12b']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
  });

  it('pins the 2013 Ordinary review: one shared booklet, the Enniscorthy companions, every priced roman', () => {
    const review = sitting(2013, 'ordinary');
    expect(review.taskCount).toBe(95);
    expect(review.cardCount).toBe(102);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(28);
    expect(review.pageReview.paper2).toEqual(review.pageReview.paper1);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(32);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005GLP000EV.pdf', bytes: 3000630 });
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005GLP000EV.pdf', bytes: 493862 });
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.pdf', bytes: 1340745 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.pdf', bytes: 1646330 });
    expect(review.legacyIds).toEqual([]);
    expect(review.addedIds).toHaveLength(102);
    // In 2013 the paper prints 40 marks on these parts and 30 on the rest.
    const forty = ['1B', '2B', '3C', '4B', '5C', '6B', '7C', '8C', '9C', '10B', '11B', '12C'];
    for (const [question, marks] of Object.entries(review.questionTotals)) {
      const expected = question.startsWith('Part 1') ? 10
        : forty.some(part => question.endsWith(`Q${part}`)) ? 40 : 30;
      expect(marks, question).toBe(expected);
    }
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2013 OL Part 2 Q1C': 4, '2013 OL Part 2 Q2C': 2, '2013 OL Part 2 Q3B': 3, '2013 OL Part 2 Q3C': 2,
    });
    // 6B prints "Two factors explained @ 20 marks each" over lines that price 1 + 21 + 18.
    const q6b = byId.get('geography-2013-ol-p2-q6b')!;
    if (q6b.rubric.system !== 'geography') throw new Error('wrong rubric');
    expect(q6b.rubric.criteria.map(c => c.maxMarks)).toEqual([1, 21, 18]);
    for (const id of ['geography-2013-ol-p1-q5', 'geography-2013-ol-p1-q7', 'geography-2013-ol-p2-q3a',
      'geography-2013-ol-p2-q7a', 'geography-2013-ol-p2-q8b', 'geography-2013-ol-p2-q10a',
      'geography-2013-ol-p2-q10c', 'geography-2013-ol-p2-q11b']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
  });

  it('pins the 2013 Higher review: one shared booklet, the Enniscorthy companions, every priced part', () => {
    const review = sitting(2013, 'higher');
    expect(review.taskCount).toBe(104);
    expect(review.cardCount).toBe(111);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(32);
    expect(review.pageReview.paper2).toEqual(review.pageReview.paper1);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(48);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005ALP000EV.pdf', bytes: 3686604 });
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005ALP000EV.pdf', bytes: 1035658 });
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.pdf', bytes: 1340745 });
    expect(review.sources.legend).toMatchObject({ fileid: 'LC005CLPC00EV.pdf', bytes: 1167773 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.pdf', bytes: 1646330 });
    expect(review.legacyIds).toEqual([]);
    expect(review.addedIds).toHaveLength(111);
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2013 HL Part 2 Q2A(ii)': 2, '2013 HL Part 2 Q2B': 2, '2013 HL Part 2 Q2C': 4, '2013 HL Part 2 Q3B': 2,
      '2013 HL Part 2 Q7A(v)': 2,
    });
    // Options print two schemes (3 @ 27 + 27 + 26 or 4 @ 20) with coherence graded inside
    // each aspect; either gives identifying + coherence 32 marks and 24 discussion SRPs.
    const option = byId.get('geography-2013-hl-p2-q13')!;
    if (option.rubric.system !== 'geography') throw new Error('wrong rubric');
    expect(option.rubric.criteria.map(c => c.maxMarks)).toEqual([32, 48]);
    for (const [id, marks] of [['geography-2013-hl-p2-q18', [27, 27, 26]], ['geography-2013-hl-p2-q24', [20, 20, 20, 20]]] as const) {
      const card = byId.get(id)!;
      if (card.rubric.system !== 'geography') throw new Error('wrong rubric');
      expect(card.rubric.criteria.map(c => c.maxMarks), id).toEqual(marks);
    }
    for (const id of ['geography-2013-hl-p1-q5', 'geography-2013-hl-p1-q6', 'geography-2013-hl-p2-q1a',
      'geography-2013-hl-p2-q7b', 'geography-2013-hl-p2-q8a', 'geography-2013-hl-p2-q10b',
      'geography-2013-hl-p2-q12b']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
  });

  it('pins the 2014 Ordinary review: one shared booklet, the Dungarvan companions, every priced roman', () => {
    const review = sitting(2014, 'ordinary');
    expect(review.taskCount).toBe(111);
    expect(review.cardCount).toBe(125);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(28);
    expect(review.pageReview.paper2).toEqual(review.pageReview.paper1);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(36);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005GLP000EV.pdf', bytes: 2451016 });
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005GLP000EV.pdf', bytes: 156491 });
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.pdf', bytes: 4043493 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.pdf', bytes: 2196383 });
    expect(review.legacyIds).toEqual([]);
    expect(review.addedIds).toHaveLength(125);
    // In 2014 the paper prints 40 marks on these parts and 30 on the rest.
    const forty = ['1B', '2B', '3B', '4B', '5C', '6B', '7C', '8B', '9B', '10C', '11C', '12B'];
    for (const [question, marks] of Object.entries(review.questionTotals)) {
      const expected = question.startsWith('Part 1') ? 10
        : forty.some(part => question.endsWith(`Q${part}`)) ? 40 : 30;
      expect(marks, question).toBe(expected);
    }
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2014 OL Part 2 Q1C': 4, '2014 OL Part 2 Q2C': 3, '2014 OL Part 2 Q3B': 4, '2014 OL Part 2 Q8B(i)': 2,
      '2014 OL Part 2 Q8B(ii)': 2, '2014 OL Part 2 Q8B(iii)': 2, '2014 OL Part 2 Q9C': 4,
    });
    // 5C and 6B price naming an Irish region outside their romans; it is carded with part (i).
    expect(authoredById.get('geography-2014-ol-p2-q5c')?.criteria[0].guidance).toEqual(['Name an Irish region · 1 mark']);
    expect(authoredById.get('geography-2014-ol-p2-q6b')?.criteria[0].guidance).toEqual(['Name one Irish region · 2 marks']);
    // Neither the Wingdings "¾" nor 10C's stray control character (U+0003) reaches a card.
    const text14 = JSON.stringify(authored.cards.filter(card => card.id.startsWith('geography-2014-ol-')));
    expect(text14).not.toContain('¾');
    expect(text14).not.toContain(String.fromCharCode(3));
    for (const id of ['geography-2014-ol-p1-q1', 'geography-2014-ol-p1-q3', 'geography-2014-ol-p2-q3a',
      'geography-2014-ol-p2-q8c', 'geography-2014-ol-p2-q9a', 'geography-2014-ol-p2-q10a',
      'geography-2014-ol-p2-q11b', 'geography-2014-ol-p2-q12c']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
  });

  it('pins the 2014 Higher review: one shared booklet, the Dungarvan companions, every priced part', () => {
    const review = sitting(2014, 'higher');
    expect(review.taskCount).toBe(103);
    expect(review.cardCount).toBe(110);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(32);
    expect(review.pageReview.paper2).toEqual(review.pageReview.paper1);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(48);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005ALP000EV.pdf', bytes: 1649594 });
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005ALP000EV.pdf', bytes: 456897 });
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.pdf', bytes: 4043493 });
    expect(review.sources.legend).toMatchObject({ fileid: 'LC005CLPC00EV.pdf', bytes: 587436 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.pdf', bytes: 2196383 });
    expect(review.legacyIds).toEqual([]);
    expect(review.addedIds).toHaveLength(110);
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2014 HL Part 2 Q1C': 3, '2014 HL Part 2 Q2B': 2, '2014 HL Part 2 Q7C': 3, '2014 HL Part 2 Q12C': 3,
    });
    // Part One prices every question in one heading; each card carries its line.
    for (const card of ALL.filter(card => card.id.startsWith('geography-2014-hl-p1-'))) {
      if (card.rubric.system !== 'geography') throw new Error('wrong rubric');
      expect(card.rubric.criteria[0].guidance[0], card.id)
        .toMatch(/^(4 parts @ 2 marks each or 8 parts @ 1 mark each|Q4\(iv\), Q9\(iv\), Q11\(iv\) & Q12\(iv\) @ 1 \+ 1 mark)$/);
    }
    // Q4(ii) was awarded to every candidate; the card carries that printed line.
    const q4ii = byId.get('geography-2014-hl-p1-q4-ii')!;
    if (q4ii.rubric.system !== 'geography') throw new Error('wrong rubric');
    expect(q4ii.rubric.criteria[0].guidance).toContain('(ii) Award 2m (ambiguous wording)');
    // The scheme's Wingdings note bullets are repaired from their glyph id, never left as "¾".
    const text = JSON.stringify(authored.cards.filter(card => card.id.startsWith('geography-2014-hl-')));
    expect(text).not.toContain('¾');
    expect(authoredById.get('geography-2014-hl-p2-q1b')?.directions)
      .toContain('• Credit 3rd named igneous rock for 1 x SRP.');
    for (const id of ['geography-2014-hl-p1-q7', 'geography-2014-hl-p1-q8', 'geography-2014-hl-p2-q1a',
      'geography-2014-hl-p2-q8a', 'geography-2014-hl-p2-q9b', 'geography-2014-hl-p2-q10a',
      'geography-2014-hl-p2-q11b', 'geography-2014-hl-p2-q12b']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
  });

  it('pins the 2016 Ordinary review: one shared booklet, the Westport companions, every priced roman', () => {
    const review = sitting(2016, 'ordinary');
    expect(review.taskCount).toBe(118);
    expect(review.cardCount).toBe(128);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(32);
    expect(review.pageReview.paper2).toEqual(review.pageReview.paper1);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(40);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005GLP000EV.pdf', bytes: 3794462 });
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005GLP000EV.pdf', bytes: 437943 });
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.pdf', bytes: 327650 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.pdf', bytes: 5761875 });
    expect(review.legacyIds).toEqual([]);
    expect(review.addedIds).toHaveLength(128);
    // In 2016 the paper prints 40 marks on these parts and 30 on the rest.
    const forty = ['1B', '2B', '3C', '4B', '5B', '6C', '7C', '8B', '9C', '10B', '11C', '12C'];
    for (const [question, marks] of Object.entries(review.questionTotals)) {
      const expected = question.startsWith('Part 1') ? 10
        : forty.some(part => question.endsWith(`Q${part}`)) ? 40 : 30;
      expect(marks, question).toBe(expected);
    }
    // "tourism or financial services" runs through every roman of 8B.
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2016 OL Part 2 Q1B': 2, '2016 OL Part 2 Q1C': 3, '2016 OL Part 2 Q3B': 4,
      '2016 OL Part 2 Q8B(i)': 2, '2016 OL Part 2 Q8B(ii)': 2, '2016 OL Part 2 Q8B(iii)': 2,
      '2016 OL Part 2 Q8B(iv)': 2,
    });
    // The text layer drops the raised "o" the paper prints as a degree sign.
    expect(byId.get('geography-2016-ol-p1-q11')!.questionText).toContain('(°C)');
    for (const id of ['geography-2016-ol-p1-q1', 'geography-2016-ol-p1-q2', 'geography-2016-ol-p1-q3',
      'geography-2016-ol-p2-q2a', 'geography-2016-ol-p2-q7a', 'geography-2016-ol-p2-q9c',
      'geography-2016-ol-p2-q10a', 'geography-2016-ol-p2-q11b', 'geography-2016-ol-p2-q12c']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
  });

  it('pins the 2016 Higher review: one shared booklet, the Westport companions, every priced part', () => {
    const review = sitting(2016, 'higher');
    expect(review.taskCount).toBe(106);
    expect(review.cardCount).toBe(108);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(32);
    expect(review.pageReview.paper2).toEqual(review.pageReview.paper1);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(48);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005ALP000EV.pdf', bytes: 2378315 });
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005ALP000EV.pdf', bytes: 1250063 });
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.pdf', bytes: 327650 });
    expect(review.sources.legend).toMatchObject({ fileid: 'LC005CLPC00EV.pdf', bytes: 745443 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.pdf', bytes: 5761875 });
    expect(review.legacyIds).toEqual([]);
    expect(review.addedIds).toHaveLength(108);
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2016 HL Part 2 Q2B': 2, '2016 HL Part 2 Q5C': 2,
    });
    // Part One Q4(i), Q5 and Q7 price each printed row with both its answers.
    for (const id of ['geography-2016-hl-p1-q4', 'geography-2016-hl-p1-q5', 'geography-2016-hl-p1-q7']) {
      const card = byId.get(id)!;
      if (card.rubric.system !== 'geography') throw new Error('wrong rubric');
      expect(card.rubric.criteria.every(c => c.maxMarks === 2 && c.permittedMarks.join() === '0,1,2'), id)
        .toBe(true);
    }
    // Option 18 prints only the "3 @ 20 marks each" outline.
    const biome = byId.get('geography-2016-hl-p2-q18')!;
    if (biome.rubric.system !== 'geography') throw new Error('wrong rubric');
    expect(biome.rubric.criteria.map(c => c.label)).toEqual(['Aspects (3 @ 20 marks)', 'Overall coherence']);
    for (const id of ['geography-2016-hl-p1-q5', 'geography-2016-hl-p1-q6', 'geography-2016-hl-p1-q7',
      'geography-2016-hl-p1-q8', 'geography-2016-hl-p2-q1a', 'geography-2016-hl-p2-q7a',
      'geography-2016-hl-p2-q8c', 'geography-2016-hl-p2-q10b', 'geography-2016-hl-p2-q11a']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
  });

  it('pins the 2017 Ordinary review: one shared booklet, the Macroom companions, every priced roman', () => {
    const review = sitting(2017, 'ordinary');
    expect(review.taskCount).toBe(122);
    expect(review.cardCount).toBe(130);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(28);
    expect(review.pageReview.paper2).toEqual(review.pageReview.paper1);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(40);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005GLP000EV.pdf', bytes: 2623267 });
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005GLP000EV.pdf', bytes: 603572 });
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.pdf', bytes: 352988 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.pdf', bytes: 602913 });
    expect(review.legacyIds).toEqual([]);
    expect(review.addedIds).toHaveLength(130);
    // In 2017 the paper prints 40 marks on these parts and 30 on the rest.
    const forty = ['1B', '2B', '3B', '4B', '5B', '6B', '7C', '8B', '9C', '10C', '11B', '12C'];
    for (const [question, marks] of Object.entries(review.questionTotals)) {
      const expected = question.startsWith('Part 1') ? 10
        : forty.some(part => question.endsWith(`Q${part}`)) ? 40 : 30;
      expect(marks, question).toBe(expected);
    }
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2017 OL Part 2 Q2B': 2, '2017 OL Part 2 Q2C': 4, '2017 OL Part 2 Q3C': 3, '2017 OL Part 2 Q9B': 3,
    });
    for (const id of ['geography-2017-ol-p1-q5', 'geography-2017-ol-p1-q6', 'geography-2017-ol-p1-q7',
      'geography-2017-ol-p2-q1a', 'geography-2017-ol-p2-q7a', 'geography-2017-ol-p2-q9c',
      'geography-2017-ol-p2-q10b', 'geography-2017-ol-p2-q11a', 'geography-2017-ol-p2-q12b']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
  });

  it('pins the 2017 Higher review: one shared booklet, the Macroom companions, every priced part', () => {
    const review = sitting(2017, 'higher');
    expect(review.taskCount).toBe(110);
    expect(review.cardCount).toBe(125);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(32);
    expect(review.pageReview.paper2).toEqual(review.pageReview.paper1);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(52);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005ALP000EV.pdf', bytes: 4054502 });
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005ALP000EV.pdf', bytes: 1065118 });
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.pdf', bytes: 352988 });
    expect(review.sources.legend).toMatchObject({ fileid: 'LC005CLPC00EV.pdf', bytes: 745443 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.pdf', bytes: 602913 });
    expect(review.legacyIds).toEqual([]);
    expect(review.addedIds).toHaveLength(125);
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2017 HL Part 2 Q1C': 3, '2017 HL Part 2 Q2B': 2, '2017 HL Part 2 Q2C': 3,
      '2017 HL Part 2 Q3A(v)': 2, '2017 HL Part 2 Q3B': 4, '2017 HL Part 2 Q9B': 3,
      '2017 HL Part 2 Q11C': 4, '2017 HL Part 2 Q12C': 2,
    });
    // Options 13, 16 and 18 print only the "3 @ 20 marks" outline.
    for (const q of [13, 16, 18]) {
      const card = byId.get(`geography-2017-hl-p2-q${q}`)!;
      if (card.rubric.system !== 'geography') throw new Error('wrong rubric');
      expect(card.rubric.criteria.map(c => c.label), String(q))
        .toEqual(['Aspects (3 @ 20 marks)', 'Overall coherence']);
    }
    for (const id of ['geography-2017-hl-p1-q6', 'geography-2017-hl-p1-q8', 'geography-2017-hl-p1-q9',
      'geography-2017-hl-p2-q1a', 'geography-2017-hl-p2-q7b', 'geography-2017-hl-p2-q8a',
      'geography-2017-hl-p2-q10a', 'geography-2017-hl-p2-q12c-aerial-photograph']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
  });

  it('pins the 2018 Ordinary review: one shared booklet, printed tariffs, every priced roman', () => {
    const review = sitting(2018, 'ordinary');
    expect(review.taskCount).toBe(124);
    expect(review.cardCount).toBe(131);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(32);
    expect(review.pageReview.paper2).toEqual(review.pageReview.paper1);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(40);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005GLP000EV.pdf', bytes: 1700593 });
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005GLP000EV.pdf', bytes: 389474 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.pdf', bytes: 6573219 });
    expect(review.legacyIds).toEqual([]);
    expect(review.addedIds).toHaveLength(131);
    // In 2018 the paper prints 40 marks on these parts and 30 on the rest.
    const forty = ['1C', '2B', '3B', '4B', '5C', '6B', '7B', '8B', '9B', '10C', '11C', '12C'];
    for (const [question, marks] of Object.entries(review.questionTotals)) {
      const expected = question.startsWith('Part 1') ? 10
        : forty.some(part => question.endsWith(`Q${part}`)) ? 40 : 30;
      expect(marks, question).toBe(expected);
    }
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2018 OL Part 2 Q1B(iii)': 2, '2018 OL Part 2 Q2B': 2, '2018 OL Part 2 Q2C': 4,
      '2018 OL Part 2 Q3C': 3,
    });
    for (const id of ['geography-2018-ol-p1-q9', 'geography-2018-ol-p1-q10', 'geography-2018-ol-p1-q11',
      'geography-2018-ol-p2-q3a', 'geography-2018-ol-p2-q8b', 'geography-2018-ol-p2-q9a',
      'geography-2018-ol-p2-q10a', 'geography-2018-ol-p2-q11c', 'geography-2018-ol-p2-q12b']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
  });

  it('pins the 2018 Higher review: one shared booklet, the Sligo companions, every priced part', () => {
    const review = sitting(2018, 'higher');
    expect(review.taskCount).toBe(122);
    expect(review.cardCount).toBe(130);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(32);
    expect(review.pageReview.paper2).toEqual(review.pageReview.paper1);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(48);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005ALP000EV.pdf', bytes: 2443729 });
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005ALP000EV.pdf', bytes: 774570 });
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.jpg', bytes: 11172454 });
    expect(review.sources.legend).toMatchObject({ fileid: 'LC005CLPC00EV.jpg', bytes: 4184180 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.pdf', bytes: 6573219 });
    expect(review.legacyIds).toEqual([]);
    expect(review.addedIds).toHaveLength(130);
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2018 HL Part 2 Q1B': 2, '2018 HL Part 2 Q2C': 2, '2018 HL Part 2 Q3B': 4,
      '2018 HL Part 2 Q5B': 2, '2018 HL Part 2 Q8C': 3,
    });
    // Part One Q3 prints eight true/false statements, each priced at 1 mark;
    // the scheme credits either answer to (vi).
    expect(ALL.filter(card => card.questionRef.startsWith('2018 HL Part 1 Q3')).map(card => card.totalMarks))
      .toEqual([1, 1, 1, 1, 1, 1, 1, 1]);
    for (const id of ['geography-2018-hl-p1-q1', 'geography-2018-hl-p1-q2', 'geography-2018-hl-p1-q3',
      'geography-2018-hl-p2-q2c-route-i', 'geography-2018-hl-p2-q3a', 'geography-2018-hl-p2-q7a',
      'geography-2018-hl-p2-q9c', 'geography-2018-hl-p2-q10a', 'geography-2018-hl-p2-q11b']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
  });

  it('pins the 2019 Higher review: one shared booklet, the Templemore companions, every priced part', () => {
    const review = sitting(2019, 'higher');
    expect(review.taskCount).toBe(113);
    expect(review.cardCount).toBe(121);
    // Both parts are printed in one 32-page booklet, reviewed once.
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(32);
    expect(review.pageReview.paper2).toEqual(review.pageReview.paper1);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(52);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005ALP000EV.pdf', bytes: 3445591 });
    expect(review.sources.paper2).toEqual(review.sources.paper1);
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005ALP000EV.pdf', bytes: 981191 });
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.jpg', bytes: 7718516 });
    expect(review.sources.legend).toMatchObject({ fileid: 'LC005CLPC00EV.pdf', bytes: 836095 });
    expect(review.sources.aerial).toMatchObject({ fileid: 'LC005CLP004EV.jpg', bytes: 5264592 });
    expect(review.legacyIds).toEqual([]);
    expect(review.addedIds).toHaveLength(121);
    expect(ALL.filter(card => card.year === 2019 && card.level === 'higher')
      .every(card => card.paperFileid === 'LC005ALP000EV')).toBe(true);
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2019 HL Part 2 Q1B': 4, '2019 HL Part 2 Q2C': 3, '2019 HL Part 2 Q6C': 2,
      '2019 HL Part 2 Q15': 3,
    });
    for (const id of ['geography-2019-hl-p1-q6', 'geography-2019-hl-p1-q7', 'geography-2019-hl-p1-q8',
      'geography-2019-hl-p1-q9', 'geography-2019-hl-p2-q1a', 'geography-2019-hl-p2-q8a',
      'geography-2019-hl-p2-q9b', 'geography-2019-hl-p2-q10a', 'geography-2019-hl-p2-q12b']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
  });

  it('pins the 2019 Ordinary review: one shared booklet, printed tariffs, every priced roman', () => {
    const review = sitting(2019, 'ordinary');
    expect(review.taskCount).toBe(127);
    expect(review.cardCount).toBe(138);
    expect(Object.keys(review.pageReview.paper1)).toHaveLength(28);
    expect(review.pageReview.paper2).toEqual(review.pageReview.paper1);
    expect(Object.keys(review.pageReview.scheme)).toHaveLength(36);
    expect(review.sources.paper1).toMatchObject({ fileid: 'LC005GLP000EV.pdf', bytes: 3739580 });
    expect(review.sources.paper2).toEqual(review.sources.paper1);
    expect(review.sources.scheme).toMatchObject({ fileid: 'LC005GLP000EV.pdf', bytes: 550626 });
    expect(review.sources.map).toMatchObject({ fileid: 'LC005CLP003EV.jpg', bytes: 7718516 });
    expect(review.legacyIds).toEqual([]);
    expect(review.addedIds).toHaveLength(138);
    // In 2019 the paper prints 40 marks on these parts and 30 on the rest.
    const forty = ['1B', '2C', '3B', '4B', '5C', '6B', '7C', '8B', '9B', '10C', '11B', '12C'];
    for (const [question, marks] of Object.entries(review.questionTotals)) {
      const expected = question.startsWith('Part 1') ? 10
        : forty.some(part => question.endsWith(`Q${part}`)) ? 40 : 30;
      expect(marks, question).toBe(expected);
    }
    const routed = review.tasks.filter((task: ReviewedTask) => task.routes.length);
    expect(Object.fromEntries(routed.map((task: ReviewedTask) =>
      [task.questionRef, task.cards.length]))).toEqual({
      '2019 OL Part 2 Q1B': 2, '2019 OL Part 2 Q1C': 4, '2019 OL Part 2 Q2B': 3,
      '2019 OL Part 2 Q7B': 3, '2019 OL Part 2 Q8C': 4,
    });
    // 12B(ii) prints one 6m allocation for two land-uses and no per-item split.
    const landUses = byId.get('geography-2019-ol-p2-q12b-ii')!;
    if (landUses.rubric.system !== 'geography') throw new Error('wrong rubric');
    expect(landUses.rubric.criteria.map(c => [c.maxMarks, c.permittedMarks])).toEqual([[6, [0, 6]]]);
    for (const id of ['geography-2019-ol-p1-q5', 'geography-2019-ol-p1-q6', 'geography-2019-ol-p1-q7',
      'geography-2019-ol-p2-q1a', 'geography-2019-ol-p2-q7a', 'geography-2019-ol-p2-q8b',
      'geography-2019-ol-p2-q11a', 'geography-2019-ol-p2-q12c']) {
      const card = byId.get(id)!;
      expect([card.sourceMaterial, ...(card.additionalSourceMaterials ?? [])]
        .some(source => source?.sourceFileid), id).toBe(true);
    }
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
    // 2019-2025 aerial photographs (the 2018-2019 maps and the 2018 and 2022 legends) are
    // published by the SEC only as JPEGs; Paper Trail files the 2018 aerial photograph as a PDF.
    const aerial: Record<number, string> = {
      2010: 'LC005CLP003EV.jpg', 2011: 'LC005CLP004EV', 2012: 'LC005CLP004EV', 2013: 'LC005CLP004EV', 2014: 'LC005CLP004EV', 2015: 'LC005CLP004EV', 2016: 'LC005CLP004EV', 2017: 'LC005CLP004EV', 2018: 'LC005CLP004EV', 2019: 'LC005CLP004EV.jpg', 2020: 'LC005CLP004EV.jpg', 2021: 'LC005CLP004EV.jpg', 2022: 'LC005CLP004EV.jpg', 2023: 'LC005CLP004EV.jpg',
      2024: 'LC005CLP004EV.jpg', 2025: 'LC005CLP004EV.jpg', 2026: 'LC005CLP004EV',
    };
    // 2010's JPEG names are swapped: CLP004 is the map, CLP003 the photograph, CLP000 the legend.
    const legend: Record<number, string> = {
      2010: 'LC005CLP000EV.jpg', 2018: 'LC005CLPC00EV.jpg', 2022: 'LC005CLPC00EV.jpg',
    };
    const map: Record<number, string> = {
      2010: 'LC005CLP004EV.jpg', 2018: 'LC005CLP003EV.jpg', 2019: 'LC005CLP003EV.jpg',
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
          page: 'page', map: map[review.year] ?? 'LC005CLP003EV', legend: legend[review.year] ?? 'LC005CLPC00EV',
          aerial: aerial[review.year],
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
    [2023, 'higher', 36, 'LC005ALP042EV.pdf', 'LC005ALP043EV.pdf'],
    [2023, 'ordinary', 24, 'LC005GLP042EV.pdf', 'LC005GLP043EV.pdf'],
    [2022, 'higher', 36, 'LC005ALP042EV.pdf', 'LC005ALP043EV.pdf'],
    [2022, 'ordinary', 24, 'LC005GLP042EV.pdf', 'LC005GLP043EV.pdf'],
    [2021, 'higher', 36, 'LC005ALP042EV.pdf', 'LC005ALP043EV.pdf'],
    [2021, 'ordinary', 24, 'LC005GLP042EV.pdf', 'LC005GLP043EV.pdf'],
    [2020, 'higher', 36, 'LC005ALP042EV.pdf', 'LC005ALP043EV.pdf'],
    [2020, 'ordinary', 24, 'LC005GLP042EV.pdf', 'LC005GLP043EV.pdf'],
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
      const filed = examTopicIdsForQuestion('geography', level, year, 'main', n, `p${part}`, 'ev', fileid);
      // Every topic the reviewed tasks prove is filed.
      expect(filed, `Part ${part} Q${n}`).toEqual(expect.arrayContaining([...ids]));
      // The review adds and never removes: every current-course topic the
      // shipped exact-question join gave this question is still filed, and
      // nothing is filed that neither source gives.
      const shipped = shippedAtlasTopics(level, year, `p${part}`, fileid, n);
      expect(filed, `Part ${part} Q${n} keeps the shipped join`).toEqual(expect.arrayContaining(
        [...shipped].filter(id => examTopicDefinition(id)?.course !== 'new')));
      expect(filed.filter(id => !ids.has(id) && !shipped.has(id)), `Part ${part} Q${n}`).toEqual([]);
    }
    // The reference snapshot omitted Higher Part One Q5; the reviewed runtime adds it.
    expect(reviewedRuntime.questionMappings.some(row =>
      row[4] === 'LC005ALP042EV.pdf' && row[5] === '5')).toBe(true);
  });

  // Before 2020 both parts share one booklet and Part Two restarts at Q1. Part
  // Two keeps its printed number under the 'single' paper key (Paper Trail's
  // Viewer chips number it so); Part One files as its own question, n = 1000 +
  // its printed number. The booklet's Irish edition mirrors both identities.
  it.each([
    [2019, 'higher', 24, 'LC005ALP000EV.pdf'],
    [2019, 'ordinary', 12, 'LC005GLP000EV.pdf'],
    [2018, 'higher', 24, 'LC005ALP000EV.pdf'],
    [2018, 'ordinary', 12, 'LC005GLP000EV.pdf'],
    [2017, 'higher', 24, 'LC005ALP000EV.pdf'],
    [2017, 'ordinary', 12, 'LC005GLP000EV.pdf'],
    [2016, 'higher', 24, 'LC005ALP000EV.pdf'],
    [2016, 'ordinary', 12, 'LC005GLP000EV.pdf'],
    [2015, 'higher', 24, 'LC005ALP000EV.pdf'],
    [2015, 'ordinary', 12, 'LC005GLP000EV.pdf'],
    [2014, 'higher', 24, 'LC005ALP000EV.pdf'],
    [2014, 'ordinary', 12, 'LC005GLP000EV.pdf'],
    [2013, 'higher', 24, 'LC005ALP000EV.pdf'],
    [2013, 'ordinary', 12, 'LC005GLP000EV.pdf'],
    [2012, 'higher', 24, 'LC005ALP000EV.pdf'],
    [2012, 'ordinary', 12, 'LC005GLP000EV.pdf'],
    [2011, 'higher', 24, 'LC005ALP000EV.pdf'],
    [2011, 'ordinary', 12, 'LC005GLP000EV.pdf'],
    [2010, 'higher', 24, 'LC005ALP000EV.pdf'],
    [2010, 'ordinary', 12, 'LC005GLP000EV.pdf'],
  ] as const)('files every reviewed %s %s task of the shared booklet as its own Atlas question',
    (year, level, questions, fileid) => {
    const review = sitting(year, level);
    const unions = { '1': new Map<string, Set<string>>(), '2': new Map<string, Set<string>>() };
    for (const task of review.tasks as ReviewedTask[]) {
      for (const cardId of task.cards) {
        expect(authoredById.get(cardId)?.atlasTopicIds, cardId).toBeDefined();
      }
      const [, part, n] = task.questionRef.match(/Part (\d) Q(\d+)/)! as unknown as [string, '1' | '2', string];
      const ids = unions[part].get(n) ?? new Set<string>();
      for (const id of task.atlasTopicIds) ids.add(id);
      unions[part].set(n, ids);
    }
    expect(unions['2'].size).toBe(questions);
    expect(unions['1'].size).toBe(12);
    const ivFileid = fileid.replace('EV.pdf', 'IV.pdf');
    const rows = reviewedRuntime.questionMappings.filter(row =>
      row[0] === levelRef(level)[0].toLowerCase() && row[2] === year);
    expect(rows.filter(row => row[1] === 'e')).toHaveLength(questions + 12);
    expect(rows.filter(row => row[1] === 'i')).toHaveLength(24);
    expect(rows.every(row => row[3] === 'single' && row[4] === (row[1] === 'e' ? fileid : ivFileid))).toBe(true);
    for (const [n, ids] of unions['1']) {
      const atlasN = String(1000 + Number(n));
      const shipped = shippedAtlasTopics(level, year, 'single', fileid, n);
      for (const [lang, file] of [['ev', fileid], ['iv', ivFileid]] as const) {
        // Part One's row carries its own reviewed topics, plus only the
        // shipped-join topics the crosswalk attributes to Part One.
        const filed = examTopicIdsForQuestion('geography', level, year, 'main', atlasN, 'single', lang, file);
        expect(filed, `${lang} Part One Q${n}`).toEqual(expect.arrayContaining([...ids]));
        expect(filed.filter(id => !ids.has(id) && !shipped.has(id)), `${lang} Part One Q${n}`).toEqual([]);
      }
    }
    for (const [n, ids] of unions['2']) {
      const filed = examTopicIdsForQuestion('geography', level, year, 'main', n, 'single', 'ev', fileid);
      expect(filed, `Part Two Q${n}`).toEqual(expect.arrayContaining([...ids]));
      if (Number(n) <= 12) {
        expect(examTopicIdsForQuestion('geography', level, year, 'main', n, 'single', 'iv', ivFileid),
          `iv Part Two Q${n}`).toEqual(expect.arrayContaining([...ids]));
      }
      // The shipped join filed Part One and Part Two under one number: each of
      // its current-course topics is still filed, on this row or on Part One's.
      const partOne = Number(n) <= 12
        ? examTopicIdsForQuestion('geography', level, year, 'main', String(1000 + Number(n)), 'single', 'ev', fileid)
        : [];
      const shipped = shippedAtlasTopics(level, year, 'single', fileid, n);
      expect([...shipped].filter(id => examTopicDefinition(id)?.course !== 'new'
        && !filed.includes(id) && !partOne.includes(id)), `Part Two Q${n} keeps the shipped join`).toEqual([]);
      expect(filed.filter(id => !ids.has(id) && !shipped.has(id)), `Part Two Q${n}`).toEqual([]);
    }
  });

  it('files every card under its own printed question, listed under each of its headings', () => {
    // 2026-10-23: the 649 cards of 2010-2019 Part One once resolved to the
    // Part Two question sharing their number; now every card has its own.
    const listed = new Map<string, Set<string>>();
    const under = (topic: string) => {
      if (!listed.has(topic)) {
        listed.set(topic, new Set(questionsForTopics('geography', [topic])
          .filter(q => q.lang === 'ev').map(q => `${q.year}|${q.level}|${q.paperKey}|${q.fileid}|${q.n}`)));
      }
      return listed.get(topic)!;
    };
    let partOne = 0;
    const missing: string[] = [];
    for (const card of ALL) {
      const [, part, printed] = card.questionRef.match(/Part ([12]) Q(\d+)/)!;
      const shared = card.year < 2020;
      const paperKey = shared ? 'single' : `p${part}`;
      const n = shared && part === '1' ? String(1000 + Number(printed)) : printed;
      if (shared && part === '1') partOne += 1;
      const fileid = `${card.paperFileid}.pdf`;
      const filed = examTopicIdsForQuestion('geography', card.level as 'higher' | 'ordinary', card.year, 'main', n,
        paperKey, 'ev', fileid);
      for (const topic of authoredById.get(card.id)?.atlasTopicIds ?? []) {
        if (!filed.includes(topic)) missing.push(`${card.id}: ${topic} not filed for Q${n}`);
        else if (!under(topic).has(`${card.year}|${card.level}|${paperKey}|${fileid}|${n}`)) {
          missing.push(`${card.id}: Q${n} not listed under ${topic}`);
        }
      }
    }
    expect(partOne).toBe(649);
    expect(missing).toEqual([]);
  });

  it('anchors both parts of every shared booklet for the Atlas without moving a Viewer chip', () => {
    const outside: string[] = [];
    for (let year = 2010; year <= 2019; year++) {
      for (const fileid of ['LC005ALP000EV.pdf', 'LC005GLP000EV.pdf', 'LC005ALP000IV.pdf', 'LC005GLP000IV.pdf']) {
        const read = (dir: string) => JSON.parse(readFileSync(
          resolve(__dirname, '..', dir, String(year), `${fileid}.json`), 'utf-8')) as PaperAnswerMap;
        const hosted = read('public/paper-anchors');
        const sidecar = read('scripts/paper-trail/answers');
        const partTwo = hosted.q.filter(q => Number(q.n) < 1000);
        const partOneAnchors = hosted.q.filter(q => Number(q.n) > 1000);
        // Part Two: the Viewer sidecar's own numbers, pages and bands (a merge
        // from the Atlas into the Viewer's map changes nothing).
        expect(partTwo.map(q => [q.n, q.pP, q.pY, q.label]), `${year}/${fileid}`)
          .toEqual(sidecar.q.map(q => [q.n, q.pP, q.pY, q.label]));
        expect(partOneAnchors.map(q => q.n)).toEqual(Array.from({ length: 12 }, (_, i) => String(1001 + i)));
        for (const q of partOneAnchors) {
          expect(q.label, `${year}/${fileid} ${q.n}`).toBe(questionLabel({ subjectId: 'geography', fileid, n: q.n }));
          expect(q.paperRegion?.length, `${year}/${fileid} ${q.n}`).toBeGreaterThan(0);
        }
        // Print order: all of Part One, then Part Two.
        expect(questionsInDisplayOrder(hosted.q).map(q => q.n))
          .toEqual([...partOneAnchors, ...partTwo].map(q => q.n));
        if (fileid.endsWith('IV.pdf')) continue;
        // Every English card's own page lies inside its question's Atlas crop.
        const level = fileid.startsWith('LC005A') ? 'higher' : 'ordinary';
        for (const card of ALL.filter(c => c.year === year && c.level === level)) {
          const [, part, printed] = card.questionRef.match(/Part ([12]) Q(\d+)/)!;
          const n = part === '1' ? String(1000 + Number(printed)) : printed;
          const region = paperRegionFor(hosted.q, n, hosted.maxCropPages ?? 3) ?? [];
          const page = authoredById.get(card.id)!.paperPage;
          if (!region.some(segment => segment.p === page)) {
            outside.push(`${card.id} p${page} not in Q${n} ${region.map(segment => segment.p)}`);
          }
        }
      }
    }
    expect(outside).toEqual([]);
  });
});

describe('choice is not a route (bank-wide layout rule, 2026-10-12)', () => {
  it('never publishes a card per combination of a choose-N-of-M pool', () => {
    // A route label names ONE printed option; "A + B" would be a combination.
    expect(ALL.filter(card => card.questionRef.split(' · ').slice(1)
      .some(label => label.includes(' + '))).map(card => card.id)).toEqual([]);
    // Every choose-N pool is one card showing every printed item.
    const pools = census.selectionAudit.filter(row => row.classification === 'single-card-choice');
    expect(pools).toHaveLength(85);
    for (const row of pools) {
      const cards = ALL.filter(card => card.questionRef === row.questionRef
        || card.questionRef.startsWith(`${row.questionRef} ·`));
      expect(cards, row.questionRef).toHaveLength(row.variants);
      for (const card of cards) {
        const bullets = card.questionText.split('\n').filter(line => line.startsWith('• '));
        // A pool printed as table cells is one row of " · " cells (above or below its instruction).
        const table = Math.max(...card.questionText.split('\n').map(line => line.split(' · ').length));
        expect(Math.max(bullets.length, table), card.id).toBeGreaterThanOrEqual(3);
      }
    }
  });

  it('shows siblings the printed question verbatim, the option named only in questionRef', () => {
    // Sibling routes of one printed question share its verbatim text; only the
    // paper's own (i)/(ii) parts, each with its own scheme, differ.
    const families = new Map<string, Set<string>>();
    for (const card of ALL) {
      const [base, ...labels] = card.questionRef.split(' · ');
      const printedPart = labels.find(label => /^Route \((?:i|ii)\)$/.test(label)) ?? '';
      const key = `${base}|${printedPart}`;
      families.set(key, (families.get(key) ?? new Set()).add(card.questionText));
    }
    expect([...families].filter(([, texts]) => texts.size > 1).map(([key]) => key)).toEqual([]);
  });

  it('carries every withdrawn combination card to its one card through a progress alias', () => {
    const geography = Object.entries(CARD_ID_ALIASES).filter(([id]) => id.startsWith('geography-'));
    expect(geography).toHaveLength(93);
    expect(Object.fromEntries(geography)).toEqual(Object.fromEntries(
      census.aliases.map(row => [row.id, row.canonicalId])));
    for (const [oldId, canonicalId] of geography) {
      expect(byId.has(oldId), oldId).toBe(false);
      expect(byId.has(canonicalId), canonicalId).toBe(true);
    }
    // Before -> after, per family: 2025 Higher Q9B kept one card per printed
    // activity (a choose-one route) and folded each factor pair into it.
    const familySize = (ref: string) => ALL.filter(card => card.questionRef === ref
      || card.questionRef.startsWith(`${ref} ·`)).length;
    expect(familySize('2021 HL Part 2 Q6C')).toBe(1);
    expect(familySize('2022 HL Part 2 Q9B')).toBe(3);
    expect(familySize('2025 HL Part 2 Q9B')).toBe(3);
    expect(familySize('2023 HL Part 2 Q6B')).toBe(1);
    expect(familySize('2024 HL Part 2 Q4C')).toBe(1);
    expect(familySize('2026 HL Part 2 Q5C')).toBe(1);
    expect(familySize('2021 OL Part 2 Q6B')).toBe(1);
  });
});
