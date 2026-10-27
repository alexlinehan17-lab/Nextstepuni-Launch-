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
import { SCHEME_CORRECTIONS, withSchemeCorrections } from '../components/MarkBank/cards/politics-and-society/corrections';
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

  it('prices one criterion in the sub-tariff headings the scheme prints in its margin', () => {
    // 2018 HL Q1(c): "(c) (i) One fact 2 marks", "(c) (ii) One fact 1 mark", "(c) (iii) One fact 1 mark" (corrections.ts
    // restores the prices the block lost); the two-mark ladder prices part (i), the one-mark facts are claimed.
    const facts = allocationOf('politics-2018-hl-q1-c');
    expect(facts.parts.map(part => [part.caption, part.max, part.bands ? 'bands' : part.rows![0].text.split(':')[0]])).toEqual([
      ['One fact', 2, 'bands'], ['One fact', 1, 'Inalienable'], ['One fact', 1, 'Indivisible'],
    ]);
    expect(ladder(facts)).toEqual([['Good description', [2]], ['Fair description', [1]], ['Irrelevant description', [0]]]);
    expect(facts.examples[0]).toMatch(/^Universal: everyone is born with the same rights.*equally\.$/);
    expect(facts.directions).toEqual(['Note: If part (i) is awarded 1M or less mark part (ii) / (iii) out of 2M']);
    // 2019 OL Q1(f): "One supranational body named 2 marks" is the tariff row, "Valid explanation of the role 3 marks" its ladder.
    const body = allocationOf('politics-2019-ol-q1-f');
    expect(body.parts.map(part => [part.max, part.caption ?? part.rows![0].text, part.rows?.[0].tariffOnly ?? 'bands'])).toEqual([
      [2, 'One supranational body named', true], [3, 'Valid explanation of the role', 'bands'],
    ]);
    expect(ladder(body, 1).map(([, marks]) => marks)).toEqual([[3], [2], [1], [0]]);
  });

  it('restores the scheme lines a block lost, and refuses a block that no longer holds the line it corrects', () => {
    expect(byId('politics-2018-hl-q1-c').rubric.schemeGuidance!.join('\n').split('\n')).toEqual(expect.arrayContaining(['(c) (i) One fact 2 marks', '(c) (ii) One fact 1 mark', '(c) (iii) One fact 1 mark']));
    expect(SCHEME_CORRECTIONS['politics-2019-ol-q1-f'].scheme).toMatch(/2019, Ordinary Level marking scheme, p\. 5/);
    const card = byId('politics-2019-ol-q1-f');
    const regenerated = { ...card, rubric: { ...card.rubric, schemeGuidance: ['(f) One supranational body named 2 marks\nValid explanation of the role 3 marks'] } };
    expect(() => withSchemeCorrections(regenerated)).toThrow(/scheme line "One supranational body named" \(occurrence 1\) is not in its block/);
  });

  it('places the printed marks of a split tariff on the answer sentence that carries it', () => {
    // "The European Court of Human Rights is responsible for ensuring 1 mark + 1 mark" / "the implementation of…"
    const cloze = allocationOf('politics-2018-ol-q1-b-i');
    expect(cloze.parts).toHaveLength(1);
    expect(cloze.parts[0].bands).toEqual([{
      label: 'The European Court of Human Rights is responsible for ensuring', marks: [1, 2],
      descriptor: 'the implementation of the European Convention on Human Rights (ECHR).',
    }]);
    // A ladder priced in the tariff ("3 marks + 2 marks" then one ladder) is still cut per term.
    expect(allocationOf('politics-2021-hl-q1-d').parts.map(part => part.max)).toEqual([3, 2]);
  });

  it('takes the alternative the question offers as the answer, and a bare "Name" as the two-mark tariff', () => {
    expect(allocationOf('politics-2018-ol-q1-o-i').parts[0].rows).toEqual([{ id: 'r1', text: 'Quantitative data', marks: 1 }]);
    expect(allocationOf('politics-2019-ol-q1-u-i').parts[0].rows).toEqual([{ id: 'r1', text: 'Quantitative', marks: 1 }]);
    expect(allocationOf('politics-2018-ol-q1-t-statement-2').parts[0]).toMatchObject({ caption: 'True or False statements', rows: [{ text: 'True', marks: 2 }] });
    expect(allocationOf('politics-2018-ol-q1-k-example').parts[0].rows).toEqual([{ id: 'r1', text: 'Name', marks: 2, tariffOnly: true }]);
  });

  it('reads a criterion’s label heading its ladder, and tariff terms beside a ladder another criterion captions', () => {
    expect(allocationOf('politics-2021-hl-q2-g').parts.map(part => [part.label, part.max, part.bands!.length])).toEqual([['Evaluation', 30, 4], ['Use of documents', 20, 4]]);
    const pieces = allocationOf('politics-2019-ol-q3-c');
    expect(pieces.parts.map(part => [part.label, part.max, part.rows?.[0].text ?? part.caption])).toEqual([
      ['First piece of information', 5, '2 key pieces of information'], ['Second piece of information', 5, '2 key pieces of information'], ['Description', 5, 'Valid description'],
    ]);
  });

  it('starts a shared block at the card’s own ask when a sibling’s answer and tariff come first', () => {
    const observations = allocationOf('politics-2021-ol-q1-q-iii');
    expect(observations.parts.map(part => [part.label, part.rows![0].text, part.rows![0].tariffOnly])).toEqual([
      ['First observation', 'Two observations about the presentation of data in the graphic.', true],
      ['Second observation', 'Two observations about the presentation of data in the graphic.', true],
    ]);
    expect(observations.directions).toContain('71.5% think Level 5 restrictions are appropriate.');
    // The sibling's answer no longer scores the advantage card, and the strength card no longer wears the sibling's caption.
    expect(allocationOf('politics-2021-ol-q1-q-ii-advantage').parts[0].rows).toEqual([{ id: 'r1', text: 'Advantage', marks: 2, tariffOnly: true }]);
    expect(allocationOf('politics-2018-ol-q1-e-ii-strength').parts[0].caption).toBeUndefined();
  });

  it('structures every Politics card', () => {
    expect(cards.filter(card => !card.rubric.allocation).map(card => card.id)).toEqual([]);
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
