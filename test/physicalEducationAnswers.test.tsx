/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * PE guidance as bands and rows (cards/physical-education/answers.ts): the
 * shapes the parser reads, what it leaves alone, and how the rows score and
 * render.
 */
import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/physical-education/factory';
import { parsePhysicalEducationAnswers } from '../components/MarkBank/cards/physical-education/answers';
import PhysicalEducationRubricPanel from '../components/MarkBank/PhysicalEducationRubricPanel';
import { physicalEducationMarks, physicalEducationRowScoreId } from '../components/MarkBank/physicalEducationScoring';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

const byId = (id: string) => {
  const card = REVIEWED_CARDS.find(candidate => candidate.id === id);
  if (!card) throw new Error(`no card ${id}`);
  return card;
};
const criterion = (id: string, label: string) => {
  const found = byId(id).rubric.criteria.find(candidate => candidate.label === label);
  if (!found) throw new Error(`no criterion ${label} on ${id}`);
  return found;
};
const allocationOf = (id: string, label: string) => {
  const allocation = criterion(id, label).allocation;
  if (!allocation) throw new Error(`${id}/${label} is not structured`);
  return allocation;
};

describe('PE guidance becomes bands and rows', () => {
  it('reads a quality ladder with ranges and keeps the rule after it as a note', () => {
    const allocation = allocationOf('pe-2020-hl-q11d', 'Discussion');
    expect(allocation.bands).toEqual([
      { label: 'Very good', marks: [7, 8] }, { label: 'good', marks: [5, 6] }, { label: 'fair', marks: [3, 4] }, { label: 'poor', marks: [1, 2] },
    ]);
    expect(allocation.notes).toEqual(['Do NOT accept implications on performer.']);
    expect(allocationOf('pe-2024-ol-q13bii', 'Description').bands).toEqual([
      { label: 'Clear and accurate description', marks: [3, 4] }, { label: 'somewhat clear and accurate', marks: [1, 2] },
    ]);
  });

  it('keeps a leading sentence as the caption, and bands whose top is the criterion', () => {
    const allocation = allocationOf('pe-2020-hl-q4', 'First explanation');
    expect(allocation.caption).toBe('Must be appropriate for an athlete with a visual impairment');
    expect(allocation.bands!.map(band => [band.label, band.marks])).toEqual([['Very good', [3]], ['good', [2]], ['fair', [1]]]);
  });

  it('reads components that add up as rows, and a component followed by a ladder', () => {
    expect(allocationOf('pe-2021-hl-q16b', 'Principle 1').rows).toEqual([
      { id: 'r1', text: 'Principle identified', marks: 1 }, { id: 'r2', text: 'brief description', marks: 1 },
    ]);
    const phase = allocationOf('pe-2021-hl-q13e', 'Phase 1');
    expect(phase.rows).toEqual([{ id: 'r1', text: 'Phase named', marks: 1 }]);
    expect(phase.bands).toEqual([{ label: 'good', marks: [2] }, { label: 'fair', marks: [1] }]);
    expect(phase.caption).toBe('contribution of the relevant energy systems explained');
  });

  it('reads counted allocations as stepped rows and named items as rows', () => {
    expect(allocationOf('pe-2020-hl-q11aii', 'Reasons').rows).toEqual([{ id: 'r1', text: 'Relevant reasons suggested', marks: 6, steps: [4, 6] }]);
    expect(allocationOf('pe-2020-hl-q4', 'Types named').rows).toEqual([{ id: 'r1', text: 'Two types of feedback', marks: 2, steps: [1, 2] }]);
    expect(allocationOf('pe-2020-hl-q5b', 'Labels').rows!.map(row => [row.text, row.marks])).toEqual([['Load: javelin', 2], ['effort: tricep', 2], ['fulcrum: elbow', 2]]);
  });

  it('makes a one-sentence criterion a single row at its maximum, and names published ranges', () => {
    expect(allocationOf('pe-2022-hl-q8c', 'Velocity').rows).toEqual([{ id: 'r1', text: 'Vector', marks: 1 }]);
    expect(allocationOf('pe-2020-hl-q10', 'Analysis').bands!.map(band => band.label)).toEqual(['10–12', '7–9', '4–6', '1–3']);
  });

  it('leaves alone guidance whose marks it cannot reach exactly', () => {
    const left = criterion('pe-2020-hl-q13a', 'Characteristics');
    expect(left.allocation).toBeUndefined();
    expect(parsePhysicalEducationAnswers(left)).toEqual({ ok: false, reason: 'prose over several permitted marks' });
  });
});

describe('PE rows score and render', () => {
  it('adds the placed band and the claimed rows, never above the criterion', () => {
    const phase = byId('pe-2021-hl-q13e');
    const id = phase.rubric.criteria[0].id;
    expect(physicalEducationMarks(phase, { [`pe:${id}`]: 2, [physicalEducationRowScoreId(id, 'r1')]: 1 })).toBe(3);
    expect(physicalEducationMarks(phase, { [`pe:${id}`]: 5 })).toBe(0);
    const labels = byId('pe-2020-hl-q5b');
    const labelsId = labels.rubric.criteria.find(item => item.label === 'Labels')!.id;
    expect(physicalEducationMarks(labels, { [physicalEducationRowScoreId(labelsId, 'r1')]: 1, [physicalEducationRowScoreId(labelsId, 'r3')]: 1 })).toBe(4);
    const reasons = byId('pe-2020-hl-q11aii');
    const reasonsId = reasons.rubric.criteria.find(item => item.label === 'Reasons')!.id;
    expect(physicalEducationMarks(reasons, { [physicalEducationRowScoreId(reasonsId, 'r1')]: 4 })).toBe(4);
    expect(physicalEducationMarks(reasons, { [physicalEducationRowScoreId(reasonsId, 'r1')]: 5 })).toBe(0);
  });

  it('renders bands as rows with their marks as buttons', () => {
    const card = byId('pe-2020-hl-q11d');
    const onScore = vi.fn();
    render(<PhysicalEducationRubricPanel card={card} scores={{ 'pe:c1': 6 }} onScore={onScore} />);
    expect(screen.getByRole('button', { name: 'Clear 6 marks for good' })).toHaveAttribute('aria-pressed', 'true');
    fireEvent.click(screen.getByRole('button', { name: 'Claim 8 marks for Very good' }));
    expect(onScore).toHaveBeenCalledWith('pe:c1', 8);
    expect(screen.getByText('Do NOT accept implications on performer.')).toBeInTheDocument();
    expect(screen.getByText('6 / 8')).toBeInTheDocument();
  });
});
