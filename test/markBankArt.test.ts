/** @license SPDX-License-Identifier: Apache-2.0 */
import { describe, expect, it } from 'vitest';
import census from '../scripts/markbank/authored/art-census.json';
import { CARDS as HIGHER } from '../components/MarkBank/cards/art/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/art/ordinary';
import { ART_STRANDS } from '../components/MarkBank/deck';
import { tariffReconciles } from '../types/markBank';
import { artMarks, suggestRubricGrade } from '../components/MarkBank/SessionScreen';

const CARDS = [...HIGHER, ...ORDINARY];

describe('complete 2021–2025 Art corpus', () => {
  it('cards every separately marked task on all ten papers', () => {
    expect(HIGHER).toHaveLength(202);
    expect(ORDINARY).toHaveLength(192);
    expect(CARDS).toHaveLength(394);
    expect(new Set(CARDS.map(card => card.id)).size).toBe(394);

    const censusIds = census.papers.flatMap(paper => paper.cards.map(card => card.cardId));
    expect([...CARDS.map(card => card.id)].sort()).toEqual([...censusIds].sort());
    expect(census.papers).toHaveLength(10);
    expect(census.papers.reduce((total, paper) => total + paper.expectedCards, 0)).toBe(394);
  });

  it('keeps the audited task census for each paper', () => {
    const expected = {
      '2021-higher': 62,
      '2021-ordinary': 57,
      '2022-higher': 62,
      '2022-ordinary': 57,
      '2023-higher': 26,
      '2023-ordinary': 26,
      '2024-higher': 26,
      '2024-ordinary': 26,
      '2025-higher': 26,
      '2025-ordinary': 26,
    } as const;
    for (const [paper, count] of Object.entries(expected)) {
      const [year, level] = paper.split('-');
      expect(CARDS.filter(card => card.year === Number(year) && card.level === level), paper)
        .toHaveLength(count);
    }
  });

  it('splits separately marked parts and keeps a printed choice as one card unless its options span Atlas headings', () => {
    const legacy = HIGHER.filter(card => card.id.startsWith('art-2021-hl-q1-task'));
    expect(legacy.map(card => card.totalMarks)).toEqual([30, 20]);
    expect(legacy.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(50);

    const sectionA = HIGHER.filter(card => card.id.startsWith('art-2023-hl-q1-'));
    expect(sectionA.map(card => card.id)).toEqual(['art-2023-hl-q1-a', 'art-2023-hl-q1-b']);
    expect(sectionA.map(card => card.totalMarks)).toEqual([5, 5]);

    // The student chooses one movement: one card with the printed question.
    const movements = HIGHER.filter(card => card.questionRef === '2025 HL Q12');
    expect(movements.map(card => card.id)).toEqual(['art-2025-hl-q12-fauvism']);
    expect(movements[0].questionText).toContain(
      'Discuss the development of one of the following: Fauvism, Expressionism, Cubism, Bauhaus, Surrealism.');

    // Any two of five headings: one card with the printed instruction.
    const embroidery = ORDINARY.filter(card => card.questionRef.startsWith('2025 OL Q4(a)'));
    expect(embroidery.map(card => card.id)).toEqual(['art-2025-ol-q4-a']);
    expect(embroidery[0].questionText).toBe(
      '(a) Describe this embroidery using any two of the following headings: colour, texture, line, pattern, shape.');
    expect(embroidery[0].totalMarks).toBe(6);
    expect(ORDINARY.filter(card => card.id === 'art-2025-ol-q4-b')).toHaveLength(1);

    // A named-artist choice under one heading keeps every printed artist on its one card.
    const artists = HIGHER.find(card => card.questionRef === '2022 HL Q7')!;
    for (const artist of ['James Barry (1741-1806)', 'Colin Davidson (b.1968)']) {
      expect(artists.questionText).toContain(artist);
    }

    // Options under different Atlas headings keep a card each: the printed
    // question verbatim, the option in the reference, its own heading.
    const movements2021 = HIGHER.filter(card => card.questionRef.startsWith('2021 HL Q15(a) · '));
    expect(movements2021.map(card => card.questionRef.split(' · ')[1])).toEqual(['Baroque', 'Rococo', 'Cubism', 'Futurism']);
    expect(new Set(movements2021.map(card => card.questionText)).size).toBe(1);
    expect(movements2021[0].questionText).toContain('one of the following art styles or movements');
    expect(movements2021.map(card => card.topicId)).toEqual(['art-4-2', 'art-4-2', 'art-4-4', 'art-4-4']);
    for (const ref of ['2021 HL Q14(a)', '2021 HL Q15(a)', '2022 HL Q14(a)', '2022 HL Q15(a)', '2021 OL Q14(a)', '2022 OL Q14(a)']) {
      const [year, level] = [Number(ref.slice(0, 4)), ref.includes(' HL ') ? 'higher' : 'ordinary'];
      const family = CARDS.filter(card => card.year === year && card.level === level && card.questionRef.startsWith(`${ref} · `));
      expect(family.length, ref).toBeGreaterThan(1);
      expect(new Set(family.map(card => card.topicId)).size, ref).toBeGreaterThan(1);
      expect(new Set(family.map(card => card.questionText)).size, ref).toBe(1);
    }

    // Guard: no two cards for one printed task (same paper and question).
    const seen = new Map<string, string>();
    for (const card of CARDS) {
      const key = `${card.year} ${card.level} ${card.questionRef}`;
      expect(seen.get(key), `${card.id} repeats ${seen.get(key)}`).toBeUndefined();
      seen.set(key, card.id);
      expect(card.stem ?? '', card.id).not.toMatch(/^Printed choice:/);
    }
  });

  it('uses real paper prompts without page furniture or fabricated screens', () => {
    const bad = CARDS.filter(card =>
      card.questionText.length < 20
      || /Leaving Certificate Examination|Optional (?:Planning|Answer) Space|Acknowledgements|Copyright notice|Do not write on this page|There is no examination material/i.test(card.questionText));
    expect(bad.map(card => card.id)).toEqual([]);
    expect(CARDS.every(card => card.questionRef.startsWith(
      `${card.year} ${card.level === 'higher' ? 'HL' : 'OL'} Q${card.id.match(/q(\d+)/)![1]}`)))
      .toBe(true);
  });

  it('models the published Art marking grammar and reconciles every tariff', () => {
    expect(CARDS.every(card => card.rubric.system === 'art')).toBe(true);
    expect(CARDS.every(tariffReconciles)).toBe(true);

    for (const card of CARDS) {
      if (card.rubric.system !== 'art') throw new Error(`${card.id}: wrong rubric`);
      expect(card.rubric.taskRequirements.length, card.id).toBeGreaterThan(0);
      expect(card.rubric.criteria.reduce((sum, criterion) => sum + criterion.maxMarks, 0), card.id)
        .toBe(card.totalMarks);

      if (card.year <= 2022) {
        expect(card.totalMarks).toBeGreaterThan(0);
        expect(card.totalMarks).toBeLessThanOrEqual(50);
        expect(card.rubric.criteria.every(criterion => criterion.bands === undefined)).toBe(true);
      } else if (card.section === 'A') {
        expect([4, 5, 6]).toContain(card.totalMarks);
        expect(card.rubric.criteria).toHaveLength(1);
        expect(card.rubric.criteria.every(criterion => criterion.bands?.length === 3)).toBe(true);
      } else {
        expect(card.totalMarks).toBe(50);
        expect(card.rubric.criteria.map(criterion => criterion.maxMarks)).toEqual([10, 20, 10, 10]);
        expect(card.rubric.criteria.every(criterion => criterion.bands?.length === 3)).toBe(true);
      }
    }
  });

  it('adds the independently awarded criteria and drives the review grade', () => {
    const card = HIGHER.find(entry => entry.id === 'art-2025-hl-q8')!;
    const scores = {
      'art:coherence-focus': 7,
      'art:subject-knowledge': 14,
      'art:relevant-examples': 7,
      'art:visual-language': 7,
    } as const;
    expect(artMarks(card, scores)).toBe(35);
    expect(suggestRubricGrade(card, scores)).toBe('got');
    expect(artMarks(card, { ...scores, 'art:subject-knowledge': 999 })).toBe(50);
  });

  it('opens every required image from the separate official illustration booklet', () => {
    const requiringIllustration = CARDS.filter(card =>
      /accompanying sheet/i.test(`${card.stem ?? ''} ${card.questionText}`));
    const withIllustration = CARDS.filter(card => card.sourceMaterial);
    expect(requiringIllustration).toHaveLength(140);
    expect(withIllustration).toHaveLength(147);
    expect(requiringIllustration.filter(card => !card.sourceMaterial).map(card => card.id)).toEqual([]);

    for (const card of withIllustration) {
      expect(card.sourceMaterial).toMatchObject({
        kind: 'source-illustration',
        pages: [expect.any(Number)],
      });
      expect(card.sourceMaterial!.pages[0]).toBeGreaterThanOrEqual(1);
      expect(card.sourceMaterial!.pages[0]).toBeLessThanOrEqual(2);
      expect(card.sourceMaterial!.sourceFileid).toMatch(/^LC014[AG]LP004BV$/);
      expect(card.sourceMaterial!.sourceFileid).not.toBe(card.paperFileid);
    }
  });

  it('files every card under the canonical written Art content areas', () => {
    expect(CARDS.every(card => /^art-[456]-\d+$/.test(card.topicId))).toBe(true);
    expect(new Set(CARDS.map(card => card.topicId)).size).toBeGreaterThanOrEqual(17);

    const displayedTopics = ART_STRANDS.flatMap(strand => strand.topics.map(topic => topic.id));
    expect(displayedTopics).toHaveLength(17);
    expect(displayedTopics).not.toContain('art-6-4');
    expect(new Set(CARDS.map(card => card.topicId))).toEqual(new Set(displayedTopics));
  });
});
