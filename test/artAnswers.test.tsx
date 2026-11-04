/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Art components as rows (cards/art/answers.ts): the Notes-cell shapes the
 * parser cuts into parts, what it leaves as a note, and how the rows score
 * and render.
 */
import { fireEvent, render, screen, within } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { CARDS as HIGHER } from '../components/MarkBank/cards/art/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/art/ordinary';
import { parseArtAllocation } from '../components/MarkBank/cards/art/answers';
import ArtRubricPanel from '../components/MarkBank/ArtRubricPanel';
import { artMarks, artRowScoreId, artScoreId } from '../components/MarkBank/artScoring';
import type { ArtRubric, SecRubricCard } from '../types/markBank';

const CARDS = [...HIGHER, ...ORDINARY] as (SecRubricCard & { rubric: ArtRubric })[];
const byId = (id: string) => {
  const card = CARDS.find(candidate => candidate.id === id);
  if (!card) throw new Error(`no card ${id}`);
  return card;
};
const criterion = (id: string, label: string) => {
  const found = byId(id).rubric.criteria.find(candidate => candidate.label === label);
  if (!found) throw new Error(`no criterion ${label} on ${id}`);
  return found;
};
const row = (id: string, label: string, rowId = 'r1') => {
  const found = criterion(id, label).allocation?.rows.find(candidate => candidate.id === rowId);
  if (!found) throw new Error(`${id}/${label}/${rowId} is not structured`);
  return found;
};
const parts = (id: string, label: string, rowId = 'r1') => row(id, label, rowId).parts!.map(part => [part.text, part.marks, part.tag]);

describe('Art rows come from the printed table', () => {
  it('makes each printed row a placement at its Marks cell, and keeps the component total', () => {
    const part = criterion('art-2010-hl-q1-task1', 'Part B');
    expect(part.allocation).toEqual({ rows: [{ id: 'r1', text: 'Description and discussion of the Broighter Collar referring to form, function, materials, decoration and techniques used.', marks: 15 }] });
    const two = criterion('art-2022-hl-q2-task2', 'Part C').allocation!;
    expect(two.rows.map(item => [item.text, item.marks])).toEqual([
      ['1. Name of one other named example of Irish stone carving from the Iron Age.', 5],
      ['2. Brief description and discussion of one other example of Irish stone carving from the Iron Age.', 10],
    ]);
  });

  it('cuts "N for X" cells into parts that add up to the row', () => {
    expect(parts('art-2020-hl-q2-task2', 'Part C')).toEqual([['name', 5, undefined], ['description & discussion', 10, undefined]]);
    expect(parts('art-2015-ol-q1-b', 'Part B')).toEqual([['Location', 5, undefined], ['Function', 5, undefined], ['Structure', 15, undefined]]);
    expect(parts('art-2021-hl-q6-task2', 'Part C')).toEqual([['name of the work', 3, undefined], ['name of artist', 2, undefined], ['description & discussion', 10, undefined]]);
  });

  it('tells the same word priced twice apart by order, and counts "2 x 5 for functions"', () => {
    expect(parts('art-2022-hl-q1-task1', 'Part A', 'r2')).toEqual([['names', 3, '1st'], ['names', 2, '2nd']]);
    expect(parts('art-2018-hl-q2-task2', 'Part D')).toEqual([['functions', 5, '1 of 2'], ['functions', 5, '2 of 2']]);
    expect(parts('art-2018-hl-q4-task2', 'Part C')).toEqual([['name', 5, undefined], ['features', 5, '1 of 2'], ['features', 5, '2 of 2']]);
    expect(parts('art-2017-ol-q16-a', 'Part A')).toEqual([
      ['name', 5, undefined], ['description and discussion of each artefact', 10, '1st'], ['description and discussion of each artefact', 10, '2nd'],
    ]);
  });

  it('gives a remainder the note leaves unlabelled the row’s own words', () => {
    expect(parts('art-2014-hl-q14-c-gislebertus', 'Part C')).toEqual([['name', 5, undefined], ['Brief description and discussion of one other named work', 10, undefined]]);
  });

  it('maps a bare split onto the headings the row prints, splitting a heading on "and" when the split does', () => {
    expect(parts('art-2020-ol-q9-a', 'Part A')).toEqual([['subject matter and symbolism', 10, undefined], ['composition and pattern', 10, undefined], ['materials and techniques', 10, undefined]]);
    expect(parts('art-2019-ol-q12-a', 'Part A')).toEqual([['subject matter', 6, undefined], ['composition', 6, undefined], ['colour', 6, undefined], ['techniques used', 7, undefined]]);
    expect(parts('art-2019-ol-q2-b', 'Part B')).toEqual([['material', 6, undefined], ['techniques', 7, undefined], ['decoration', 7, undefined]]);
    expect(parts('art-2019-hl-q4-task2', 'Part D')).toEqual([['part B', 5, undefined], ['part C', 5, undefined]]);
    const named = row('art-2021-ol-q8-a', 'Part A');
    expect(named.parts!.map(part => [part.text, part.marks])).toEqual([['name', 5], ['function', 6], ['subject matter', 7], ['treatment of the human figure', 7]]);
    expect(named.note).toBe('max 3 for partially correct name');
  });

  it('keeps a rule, a cap, a count without a noun and a cell of alternatives as a note under the whole row', () => {
    expect(row('art-2021-ol-q4-a-castletown-house', 'Part A')).toEqual({ id: 'r1', text: 'Name the architect/s of chosen building.', marks: 5, note: 'Max 3 for partially correct name' });
    expect(row('art-2014-ol-q9-a', 'Part A').note).toBe('3 points for 30 marks and 2 detailed points for 26 marks maximum');
    expect(row('art-2014-hl-q2-task1', 'Part A').note).toBe('2 for Lunula,3 for Gleninsheen Gorget, 2 for Gorget only');
    expect(row('art-2020-hl-q16-task2', 'Part C')).toMatchObject({ marks: 15, note: '5/5/5' });
    const sentence = row('art-2014-hl-q16-c', 'Part C');
    expect(sentence.parts!.map(part => [part.text, part.marks])).toEqual([['feature 1', 5], ['feature 2', 5]]);
    expect(sentence.note).toBe('Features must be relevant to the question');
  });

  it('refuses a table that does not reconcile', () => {
    const base = { guidance: ['Name.', 'Describe.'], maxMarks: 15, permittedMarks: Array.from({ length: 16 }, (_, mark) => mark) };
    expect(parseArtAllocation({ ...base, rowMarks: [5, 5] })).toEqual({ ok: false, reason: 'rows do not add up to the component' });
    expect(parseArtAllocation({ ...base, rowMarks: [15] })).toEqual({ ok: false, reason: 'marks column does not match the rows' });
    expect(parseArtAllocation({ ...base, rowMarks: [5, 10], permittedMarks: [0, 5, 10, 15] })).toEqual({ ok: false, reason: 'permitted marks are not every mark' });
    expect(parseArtAllocation({ ...base })).toEqual({ ok: false, reason: 'no marks column' });
    expect(parseArtAllocation({ ...base, rowMarks: [5, 10], rowNotes: ['', '4 for name, 4 for discussion'] })).toMatchObject({
      ok: true, allocation: { rows: [{ id: 'r1', marks: 5 }, { id: 'r2', marks: 10, parts: [{ text: 'name', marks: 4 }, { text: 'discussion', marks: 4 }, { text: 'Describe.', marks: 2 }] }] },
    });
  });

  it('leaves 2023+ descriptor criteria to their bands', () => {
    expect(criterion('art-2023-hl-q1-a', 'Part (a)').allocation).toBeUndefined();
    expect(byId('art-2025-hl-q8').rubric.criteria.every(item => !item.allocation && item.bands?.length === 3)).toBe(true);
  });
});

describe('Art rows score and render', () => {
  it('adds the marks placed on rows and parts, never above a row, a component or the card', () => {
    const card = byId('art-2020-hl-q2-task2');
    const partC = criterion(card.id, 'Part C');
    expect(artMarks(card, { [artRowScoreId(partC.id, 'r1', 'p1')]: 5, [artRowScoreId(partC.id, 'r1', 'p2')]: 7 })).toBe(12);
    expect(artMarks(card, { [artRowScoreId(partC.id, 'r1', 'p1')]: 99 })).toBe(5);
    expect(artMarks(card, { [artScoreId(partC.id)]: 15 })).toBe(0);
    const whole = byId('art-2010-hl-q1-task1');
    expect(artMarks(whole, { 'art:a:row:r1': 10, 'art:b:row:r1': 15, 'art:c:row:r1': 15 })).toBe(40);
    expect(artMarks(whole, { 'art:a:row:r1': 4.5 })).toBe(0);
    expect(artMarks(byId('art-2025-hl-q8'), { 'art:subject-knowledge': 14, 'art:coherence-focus': 7 })).toBe(21);
  });

  it('renders each part as a stepped row and a long row as a slider, and reports the component total', () => {
    const card = byId('art-2021-ol-q8-a');
    const onScore = vi.fn();
    render(<ArtRubricPanel card={card} scores={{ 'art:a:row:r1:part:p1': 5 }} requirementChecks={{}} onScore={onScore} onRequirement={() => undefined} />);
    expect(screen.getByText('Place your marks on each printed row.')).toBeInTheDocument();
    const partA = screen.getByRole('region', { name: 'Part A' });
    expect(within(partA).getByText('5m of 25m')).toBeInTheDocument();
    expect(within(partA).getByText('max 3 for partially correct name')).toBeInTheDocument();
    fireEvent.click(within(partA).getByRole('button', { name: 'Claim 7 marks for subject matter' }));
    expect(onScore).toHaveBeenCalledWith('art:a:row:r1:part:p3', 7);
    fireEvent.click(within(partA).getByRole('button', { name: 'Clear 5 marks for name' }));
    expect(onScore).toHaveBeenCalledWith('art:a:row:r1:part:p1', 0);

    render(<ArtRubricPanel card={byId('art-2010-hl-q1-task1')} scores={{}} requirementChecks={{}} onScore={onScore} onRequirement={() => undefined} />);
    expect(screen.getByRole('button', { name: 'Claim 10 marks for Name illustrated objects.' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Claim 15 marks for Description and discussion of the Broighter Collar/ })).toBeInTheDocument();

    // A row above 15 marks is a slider, with its note under the row's words.
    render(<ArtRubricPanel card={byId('art-2014-ol-q9-a')} scores={{}} requirementChecks={{}} onScore={onScore} onRequirement={() => undefined} />);
    const slider = screen.getByRole('slider', { name: 'Marks for Describe/discuss using headings' });
    expect(slider).toHaveAttribute('max', '30');
    fireEvent.change(slider, { target: { value: '12' } });
    expect(onScore).toHaveBeenCalledWith('art:a:row:r1', 12);
    expect(screen.getByText('3 points for 30 marks and 2 detailed points for 26 marks maximum')).toBeInTheDocument();
  });

  it('keeps the 2023+ descriptor bands as mark buttons under their published bullets', () => {
    const onScore = vi.fn();
    render(<ArtRubricPanel card={byId('art-2025-hl-q8')} scores={{ 'art:subject-knowledge': 14 }} requirementChecks={{}} onScore={onScore} onRequirement={() => undefined} />);
    expect(screen.getByText('Place your response on the published Art scale.')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Set Subject Knowledge to 14 marks' })).toHaveAttribute('aria-pressed', 'true');
    fireEvent.click(screen.getByRole('button', { name: 'Set Coherence and Focus to 7 marks' }));
    expect(onScore).toHaveBeenCalledWith('art:coherence-focus', 7);
  });
});
