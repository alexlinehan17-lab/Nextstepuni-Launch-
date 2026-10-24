/** @license SPDX-License-Identifier: Apache-2.0 */
import { describe, expect, it } from 'vitest';
import authored from '../components/MarkBank/cards/geography/authored.json';
import { CARDS as HIGHER } from '../components/MarkBank/cards/geography/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/geography/ordinary';
import { GEOGRAPHY_STRANDS } from '../components/MarkBank/deck';
import census from '../scripts/markbank/authored/geography-census.json';
import {
  geographyMarks,
  geographyScoreId,
  suggestRubricGrade,
} from '../components/MarkBank/SessionScreen';
import { geographyRowScoreId, geographySrpScoreId } from '../components/MarkBank/geographyScoring';
import { isRubricCard, tariffReconciles, type SecRubricCard } from '../types/markBank';

const ALL: SecRubricCard[] = [...HIGHER, ...ORDINARY];
const byId = new Map(ALL.map(card => [card.id, card]));

const levelRef = (level: string) => level === 'higher' ? 'HL' : 'OL';

describe('complete answerable 2021–2026 Geography corpus', () => {
  it('accounts for every paper task before finite route expansion', () => {
    expect(census.paperBaseTasks).toBe(648);
    expect(census.includedBaseTasks).toBe(563);
    expect(census.excludedBaseTasks).toBe(85);
    expect(census.includedBaseTasks + census.excludedBaseTasks)
      .toBe(census.paperBaseTasks);
    expect(census.authoredCards).toBe(754);
    expect(census.baseTasks).toHaveLength(648);
    expect(census.baseTasks.filter(task => task.status === 'authored')).toHaveLength(563);
    expect(census.baseTasks.filter(task => task.status === 'excluded')).toHaveLength(85);
    expect(census.exclusions).toHaveLength(85);
    expect(census.sittings).toHaveLength(12);

    const expected = {
      '2021-higher': 75, '2021-ordinary': 49,
      '2022-higher': 73, '2022-ordinary': 49,
      '2023-higher': 78, '2023-ordinary': 52,
      '2024-higher': 66, '2024-ordinary': 49,
      '2025-higher': 80, '2025-ordinary': 52,
      '2026-higher': 73, '2026-ordinary': 58,
    } as const;
    for (const [sitting, cards] of Object.entries(expected)) {
      const [year, level] = sitting.split('-');
      expect(ALL.filter(card => card.year === Number(year) && card.level === level), sitting)
        .toHaveLength(cards);
    }
  });

  it('maps the generated manifest one-to-one to the live decks', () => {
    expect(HIGHER).toHaveLength(445);
    expect(ORDINARY).toHaveLength(309);
    expect(ALL).toHaveLength(754);
    expect(authored.meta.cardCount).toBe(754);
    expect(new Set(ALL.map(card => card.id)).size).toBe(754);
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
    expect(census.selectionAudit).toHaveLength(76);
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
        .test(card.questionText));
    expect(companionTasks.length).toBeGreaterThan(0);
    expect(companionTasks.every(card => card.year === 2026)).toBe(true);
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
      expect(generated.questionText.length, generated.id).toBeGreaterThanOrEqual(40);
      expect(generated.questionText, generated.id).not.toMatch(furniture);
      expect(generated.paperPage, generated.id).toBeGreaterThan(0);
      expect(generated.schemePage, generated.id).toBeGreaterThan(0);
      expect(generated.schemeGuidance.length, generated.id).toBeGreaterThan(0);
      expect(runtime.paperFileid, generated.id).toBe(resolvePaperFileid(
        'geography', generated.year, generated.level, String(generated.part)));
    }
  });

  it('shows the official page for every embedded map, chart, image or source task', () => {
    const expectedSourced = ALL.filter(card => card.section === '1'
      || / Part 2 Q(?:[1-9]|1[0-2])A(?: ·|$)/.test(card.questionRef));
    expect(expectedSourced).toHaveLength(226);
    expect(expectedSourced.filter(card => !card.sourceMaterial).map(card => card.id)).toEqual([]);

    const nonStandardSourced = ALL.filter(card => card.sourceMaterial
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
      'geography-2026-hl-p2-q9c',
      'geography-2026-hl-p2-q12c',
      'geography-2022-ol-p2-q2c',
      'geography-2022-ol-p2-q12c',
      'geography-2026-ol-p2-q9b',
      'geography-2026-ol-p2-q11c',
    ]);
    expect(ALL.filter(card => card.sourceMaterial)).toHaveLength(242);

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
        expect(source.sourceFileid, card.id).toMatch(/^LC005CLP(?:C00|003|004)EV$/);
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

    for (const card of ALL) {
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
    expect(ALL.filter(card => card.rubric.system === 'geography'
      && card.rubric.criteria[0].guidanceKind === 'exact')).toHaveLength(226);
    expect(ALL.filter(card => card.rubric.system === 'geography'
      && card.rubric.criteria[0].guidanceKind === 'srp')).toHaveLength(528);
  });

  it('turns a single published allocation into the scheduler grade where the scheme is still prose', () => {
    // An 80-mark option is not yet cut into rows, so it is placed as one number.
    const card = HIGHER.find(entry => entry.id === 'geography-2021-hl-p2-q13')!;
    expect(card.rubric.system === 'geography' && card.rubric.criteria[0].allocation).toBeUndefined();
    const scoreId = geographyScoreId('published-allocation');
    expect(geographyMarks(card, { [scoreId]: 56 })).toBe(56);
    expect(suggestRubricGrade(card, { [scoreId]: 56 })).toBe('got');
    expect(geographyMarks(card, { [scoreId]: 999 })).toBe(card.totalMarks);
  });

  it('scores a structured card row by row, SRPs by count, capped at the paper', () => {
    const card = ORDINARY.find(entry => entry.id === 'geography-2023-ol-p2-q3a')!;
    if (card.rubric.system !== 'geography') throw new Error('wrong rubric');
    const criterion = card.rubric.criteria[0];
    const allocation = criterion.allocation!;
    const [magnitude, plates, effects, epicentre] = allocation.groups;
    expect(magnitude.prompt).toBe('What was the magnitude of the earthquake in Afghanistan?');
    expect(magnitude.rows).toEqual([{ id: 'r1', text: '6.1', marks: 3 }]);
    expect(plates.rows[0]).toMatchObject({ text: 'Indian plate and Eurasian plate', marks: 6, steps: [3, 6] });
    expect(effects.rows.map(row => row.text)).toEqual(['People killed', 'People injured', 'Homes destroyed']);
    expect(epicentre.srp[0]).toMatchObject({ label: 'Brief explanation', count: 2, marks: 3 });

    const scores = {
      [geographyRowScoreId(criterion.id, 'r1')]: 3,
      [geographyRowScoreId(criterion.id, plates.rows[0].id)]: 3,
      [geographySrpScoreId(criterion.id, epicentre.srp[0].id)]: 2,
    };
    expect(geographyMarks(card, scores)).toBe(12);
    expect(suggestRubricGrade(card, scores)).toBe('shaky');
    // A claim the scheme does not print for the row counts for nothing.
    expect(geographyMarks(card, { [geographyRowScoreId(criterion.id, plates.rows[0].id)]: 5 })).toBe(0);
    // Counting more SRPs than the part allows stops at the part.
    expect(geographyMarks(card, { [geographySrpScoreId(criterion.id, epicentre.srp[0].id)]: 9 })).toBe(6);
    // The single-placement id is ignored once the card is structured.
    expect(geographyMarks(card, { [geographyScoreId(criterion.id)]: 30 })).toBe(0);
  });

  it('shows the scheme\'s own words where it prices an answer it does not print', () => {
    const card = ORDINARY.find(entry => entry.id === 'geography-2022-ol-p2-q1c')!;
    if (card.rubric.system !== 'geography') throw new Error('wrong rubric');
    const allocation = card.rubric.criteria[0].allocation!;
    expect(allocation.groups[0].rows[0]).toEqual({ id: 'r1', text: 'Tectonic plate named', marks: 3, tariffOnly: true });
    expect(allocation.groups[1].srp[0]).toMatchObject({ label: 'Description/Explanation', count: 9, marks: 3 });
    expect(allocation.directions).toEqual([
      'At least one SRP for explanation',
      'Allow one SRP for relevant annotated diagram',
      "Relevant information, additional to the text, given on diagrams can be awarded SRP's",
    ]);
  });

  it('shares an SRP pool between parts the scheme prices as a range', () => {
    const card = HIGHER.find(entry => entry.id === 'geography-2021-hl-p2-q3c')!;
    if (card.rubric.system !== 'geography') throw new Error('wrong rubric');
    const criterion = card.rubric.criteria[0];
    const allocation = criterion.allocation!;
    expect(allocation.srpPool).toEqual({ count: 13, marks: 2 });
    const [rock1, rock2] = allocation.groups[0].srp;
    expect(rock1).toMatchObject({ count: 7, min: 6 });
    const scores = {
      [geographySrpScoreId(criterion.id, rock1.id)]: 7,
      [geographySrpScoreId(criterion.id, rock2.id)]: 7,
    };
    // 14 counted, 13 shared: the pool caps the pair.
    expect(geographyMarks(card, scores)).toBe(26);
  });

  it('repeats a unit the scheme prices once and asks for several times', () => {
    const card = HIGHER.find(entry => entry.id === 'geography-2021-hl-p2-q4a')!;
    if (card.rubric.system !== 'geography') throw new Error('wrong rubric');
    const criterion = card.rubric.criteria[0];
    const allocation = criterion.allocation!;
    const features = allocation.groups.find(group => group.repeat)!;
    expect(features.repeat).toEqual({ count: 4, unit: '4 features', marks: 4 });
    expect(features.rows.map(row => [row.text, row.marks])).toEqual([['Shown', 2], ['Named', 2]]);
    const scores = Object.fromEntries([1, 2, 3, 4].map(unit => [geographyRowScoreId(criterion.id, features.rows[1].id, unit), 2]));
    expect(geographyMarks(card, scores)).toBe(8);
  });

  it('files every card under the canonical Geography syllabus', () => {
    const topicIds = new Set(GEOGRAPHY_STRANDS.flatMap(strand =>
      strand.topics.map(topic => topic.id)));
    expect(topicIds.size).toBeGreaterThan(40);
    expect(ALL.filter(card => !topicIds.has(card.topicId)).map(card =>
      `${card.id}: ${card.topicId}`)).toEqual([]);
    expect(new Set(ALL.map(card => card.topicId)).size).toBe(40);
  });
});
