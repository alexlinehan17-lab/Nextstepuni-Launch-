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
  it('cards every separately marked task and finite printed route on all ten papers', () => {
    expect(HIGHER).toHaveLength(222);
    expect(ORDINARY).toHaveLength(240);
    expect(CARDS).toHaveLength(462);
    expect(new Set(CARDS.map(card => card.id)).size).toBe(462);

    const censusIds = census.papers.flatMap(paper => paper.cards.map(card => card.cardId));
    expect([...CARDS.map(card => card.id)].sort()).toEqual([...censusIds].sort());
    expect(census.papers).toHaveLength(10);
    expect(census.papers.reduce((total, paper) => total + paper.expectedCards, 0)).toBe(462);
  });

  it('keeps the audited task census for each paper', () => {
    const expected = {
      '2021-higher': 72,
      '2021-ordinary': 78,
      '2022-higher': 68,
      '2022-ordinary': 75,
      '2023-higher': 26,
      '2023-ordinary': 26,
      '2024-higher': 26,
      '2024-ordinary': 26,
      '2025-higher': 30,
      '2025-ordinary': 35,
    } as const;
    for (const [paper, count] of Object.entries(expected)) {
      const [year, level] = paper.split('-');
      expect(CARDS.filter(card => card.year === Number(year) && card.level === level), paper)
        .toHaveLength(count);
    }
  });

  it('does not collapse separately practicable parts or printed alternatives', () => {
    const legacy = HIGHER.filter(card => card.id.startsWith('art-2021-hl-q1-task'));
    expect(legacy.map(card => card.totalMarks)).toEqual([30, 20]);
    expect(legacy.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(50);

    const sectionA = HIGHER.filter(card => card.id.startsWith('art-2023-hl-q1-'));
    expect(sectionA.map(card => card.id)).toEqual(['art-2023-hl-q1-a', 'art-2023-hl-q1-b']);
    expect(sectionA.map(card => card.totalMarks)).toEqual([5, 5]);

    const movements = HIGHER.filter(card => card.id.startsWith('art-2025-hl-q12-'));
    expect(movements).toHaveLength(5);
    expect(new Set(movements.map(card => card.questionText)).size).toBe(5);
    expect(movements.map(card => card.questionText)).toEqual(expect.arrayContaining([
      expect.stringContaining('development of Fauvism'),
      expect.stringContaining('development of Surrealism'),
    ]));

    const embroideryHeadings = ORDINARY.filter(card =>
      card.questionRef.startsWith('2025 OL Q4(a)'));
    expect(embroideryHeadings).toHaveLength(10);
    expect(embroideryHeadings.map(card => card.id)).toContain('art-2025-ol-q4-a');
    expect(new Set(embroideryHeadings.map(card => card.questionText)).size).toBe(10);
    expect(embroideryHeadings.every(card => card.totalMarks === 6)).toBe(true);
    expect(embroideryHeadings.map(card => card.questionText)).toEqual(expect.arrayContaining([
      expect.stringContaining('headings: colour and texture'),
      expect.stringContaining('headings: pattern and shape'),
    ]));
    expect(ORDINARY.filter(card => card.id === 'art-2025-ol-q4-b')).toHaveLength(1);
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
    expect(requiringIllustration).toHaveLength(149);
    expect(withIllustration).toHaveLength(156);
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
