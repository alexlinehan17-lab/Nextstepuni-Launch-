/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Politics and Society schemes as ladders and rows
 * (cards/politics-and-society/answers.ts): the shapes the parser reads, the
 * cards it leaves alone, and how the parts score and render.
 */
import { fireEvent, render, screen, within } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { CARDS as HIGHER } from '../components/MarkBank/cards/politics-and-society/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/politics-and-society/ordinary';
import PoliticsRubricPanel, { politicsMarks } from '../components/MarkBank/PoliticsRubricPanel';
import { politicsPartScoreId, politicsRowScoreId } from '../components/MarkBank/politicsScoring';
import type { PoliticsAllocation, PoliticsRubric, SecRubricCard } from '../types/markBank';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

type Card = SecRubricCard & { rubric: PoliticsRubric };
const cards = [...HIGHER, ...ORDINARY] as Card[];
const byId = (id: string): Card => {
  const card = cards.find(candidate => candidate.id === id);
  if (!card) throw new Error(`no card ${id}`);
  return card;
};
const allocationOf = (id: string): PoliticsAllocation => {
  const allocation = byId(id).rubric.allocation;
  if (!allocation) throw new Error(`${id} is not structured`);
  return allocation;
};
const ladder = (allocation: PoliticsAllocation, index = 0) => allocation.parts[index].bands!.map(band => [band.label, band.marks] as const);

describe('Politics scheme blocks become ladders and rows', () => {
  it('reads a quality ladder with mark ranges, keeping the scheme’s own caption', () => {
    const allocation = allocationOf('politics-2021-hl-q1-f');
    expect(allocation.parts).toHaveLength(1);
    expect(allocation.parts[0]).toMatchObject({ label: 'Complete response', caption: 'Explanation of the term ‘localisation’.', max: 5 });
    expect(ladder(allocation)).toEqual([
      ['Very good explanation', [4, 5]], ['Good explanation', [2, 3]], ['Fair explanation', [0, 1]],
    ]);
  });

  it('lists the scheme’s indicative points apart from the ladder', () => {
    const allocation = allocationOf('politics-2024-ol-q1-m');
    expect(allocation.examples).toEqual(['Irish language', 'Education', 'Sport', 'Description of a relevant example']);
    expect(ladder(allocation)).toEqual([['Very good description', [8, 9, 10]], ['Good description', [4, 5, 6, 7]], ['Fair description', [0, 1, 2, 3]]]);
  });

  it('splits "3 marks + 2 marks" ladders printed interleaved into two parts of one response', () => {
    const allocation = allocationOf('politics-2019-ol-q1-d');
    expect(allocation.parts.map(part => [part.max, part.bands!.map(band => band.marks[0])])).toEqual([[3, [3, 2, 1, 0]], [2, [2, 1, 0]]]);
    expect(allocation.directions).toContain('Note: If the first point is awarded 2M or less, mark the second description out of 3M');
    // Two criteria of their own tops take their own ladders.
    expect(allocationOf('politics-2025-hl-q1-i').parts.map(part => [part.label, part.max])).toEqual([['First function', 3], ['Second function', 2]]);
  });

  it('shares one printed ladder between parallel criteria, and reads labelled sections', () => {
    expect(allocationOf('politics-2021-ol-q3-a').parts.map(part => [part.label, part.max, part.bands!.length])).toEqual([['First reason', 5, 3], ['Second reason', 5, 3]]);
    const sections = allocationOf('politics-2026-hl-q2-g');
    expect(sections.parts.map(part => [part.label, part.max])).toEqual([['Conclusions', 30], ['Use of documents', 20]]);
    expect(sections.parts[0].bands![0]).toEqual({ label: 'Very Good', marks: [24, 25, 26, 27, 28, 29, 30], descriptor: 'focused, insightful' });
  });

  it('makes exact answers rows: a priced answer, a keyed list, bullets under a sub-allocation', () => {
    expect(allocationOf('politics-2018-ol-q1-f').parts[0]).toMatchObject({ max: 5, count: 1, rows: [{ text: 'European Parliament', marks: 5 }, { text: 'Two answers ticked', marks: 0 }] });
    const acronyms = allocationOf('politics-2021-ol-q1-l').parts[0];
    expect(acronyms).toMatchObject({ max: 10, count: 5 });
    expect(acronyms.rows!.map(row => row.marks)).toEqual(Array(9).fill(2));
    expect(acronyms.rows![0].text).toBe('UNCRC: United Nations Convention on the Rights of the Child');
    const example = allocationOf('politics-2026-ol-q1-q-example').parts[0];
    expect(example.rows!.map(row => row.text)).toEqual(['Child under UNCRC', 'Citizen under the constitution', 'Workers under employment law']);
  });

  it('builds essay parts from the criteria’s own bands', () => {
    const essay = allocationOf('politics-2018-hl-q3');
    expect(essay.parts.map(part => [part.label, part.max, part.bands!.length])).toEqual([
      ['Introduction', 10, 5], ['Knowledge', 20, 5], ['Evidence', 20, 5], ['Analysis and Synthesis', 15, 5], ['Evaluation', 15, 5], ['Cohesion', 20, 5],
    ]);
    expect(essay.parts[1].bands![0]).toMatchObject({ label: 'Excellent', marks: [18, 19, 20] });
  });

  it('leaves alone a card whose block carries only a sibling’s ladder', () => {
    expect(byId('politics-2018-hl-q1-c').rubric.allocation).toBeUndefined();
  });
});

describe('Politics parts score and render', () => {
  it('scores a band by the mark placed on it, rows by claims up to the count, and ignores legacy ids', () => {
    const card = byId('politics-2019-ol-q1-d');
    expect(politicsMarks(card, { [politicsPartScoreId('p1')]: 3, [politicsPartScoreId('p2')]: 1 })).toBe(4);
    expect(politicsMarks(card, { [politicsPartScoreId('p1')]: 3, [politicsPartScoreId('p2')]: 3 })).toBe(3);
    expect(politicsMarks(card, { 'politics:criterion-1': 5 })).toBe(0);
    const acronyms = byId('politics-2021-ol-q1-l');
    const six = Object.fromEntries(['r1', 'r2', 'r3', 'r4', 'r5', 'r6'].map(row => [politicsRowScoreId('p1', row), 1]));
    expect(politicsMarks(acronyms, six)).toBe(10);
    expect(politicsMarks(acronyms, { [politicsRowScoreId('p1', 'r2')]: 1 })).toBe(2);
  });

  it('renders bands as rows with their marks as buttons and the points as a visible list', () => {
    const card = byId('politics-2024-ol-q1-m');
    const onScore = vi.fn();
    render(<PoliticsRubricPanel card={card} scores={{ [politicsPartScoreId('p1')]: 9 }} onScore={onScore} />);
    const points = screen.getByRole('region', { name: 'Points the scheme lists' });
    expect(within(points).getByText('Irish language')).toBeInTheDocument();
    expect(screen.queryByRole('combobox')).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Clear 9 marks for Very good description' })).toHaveAttribute('aria-pressed', 'true');
    fireEvent.click(screen.getByRole('button', { name: 'Claim 6 marks for Good description' }));
    expect(onScore).toHaveBeenCalledWith(politicsPartScoreId('p1'), 6);
    expect(screen.getByText('9 / 10')).toBeInTheDocument();
  });
});
