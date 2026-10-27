/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A criterion row priced in named components (MarkRow.parts, from
 * construction_rows.py): how it reconciles, scores and renders.
 */
import { describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen, within } from '@testing-library/react';
import SessionScreen, { claimableTotal, marksClaimed, partClaimId, partsMarksClaimed } from '@/components/MarkBank/SessionScreen';
import { isPointCard, rowPartsReconcile, tariffReconciles, type MarkRow, type SecCard, type SecQuestionCard } from '@/types/markBank';
import { CARDS as CONSTRUCTION_HIGHER } from '@/components/MarkBank/cards/construction-studies/higher';

vi.mock('@/components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

const byId = (id: string) => {
  const card = CONSTRUCTION_HIGHER.find(candidate => candidate.id === id);
  if (!card || !isPointCard(card)) throw new Error(`no point card ${id}`);
  return card as SecQuestionCard;
};

describe('a row priced in named components', () => {
  test('carries the components as parts that add up to it, on printed steps, under the unchanged row', () => {
    const card = byId('cons-2017-hl-q2-b');
    const row = card.rows.find(item => item.id === 'advantage-1')!;
    expect(row.verbatim).toBe('Advantage 1 (3 for point, 3 for discussion)');
    expect([row.marks, row.permittedMarks]).toEqual([6, [0, 1, 2, 3, 4, 5, 6]]);
    expect(row.parts).toEqual([
      { id: 'point', verbatim: 'point', marks: 3, permittedMarks: [0, 1, 2, 3] },
      { id: 'discussion', verbatim: 'discussion', marks: 3, permittedMarks: [0, 1, 2, 3] },
    ]);
    expect(rowPartsReconcile(row)).toBe(true);
    expect(tariffReconciles(card)).toBe(true);
    // The printed ladder, where the note gives one: scale and drafting, each excellent 4, good 3, fair 2.
    const presentation = byId('cons-2018-hl-q1-a').rows.find(item => item.id === 'presentation')!;
    expect(presentation.parts!.map(part => [part.verbatim, part.marks, part.permittedMarks])).toEqual([['Scale', 4, [0, 2, 3, 4]], ['Drafting', 4, [0, 2, 3, 4]]]);
  });

  test('refuses parts that do not add up, repeat an id or step outside their marks', () => {
    const base: MarkRow = { id: 'r', kind: 'criterion', verbatim: 'Item (2 for point, 4 for discussion)', marks: 6, permittedMarks: [0, 1, 2, 3, 4, 5, 6] };
    const part = (id: string, marks: number, steps = Array.from({ length: marks + 1 }, (_, i) => i)) => ({ id, verbatim: id, marks, permittedMarks: steps });
    expect(rowPartsReconcile({ ...base, parts: [part('point', 2), part('discussion', 4)] })).toBe(true);
    expect(rowPartsReconcile({ ...base, parts: [part('point', 2), part('discussion', 3)] })).toBe(false);
    expect(rowPartsReconcile({ ...base, parts: [part('point', 2), part('point', 4)] })).toBe(false);
    expect(rowPartsReconcile({ ...base, parts: [part('point', 2), part('discussion', 4, [0, 2, 5])] })).toBe(false);
    expect(rowPartsReconcile({ ...base, parts: [part('point', 6)] })).toBe(false);
    expect(rowPartsReconcile({ ...base, permittedMarks: undefined, parts: [part('point', 2), part('discussion', 4)] })).toBe(false);
  });

  test('scores what was placed on each part, only at its printed steps, never above the row', () => {
    const card = byId('cons-2017-hl-q2-b');
    const row = card.rows.find(item => item.id === 'advantage-1')!;
    expect(partsMarksClaimed(row, 'advantage-1', { [partClaimId('advantage-1', 'point')]: 3, [partClaimId('advantage-1', 'discussion')]: 2 })).toBe(5);
    expect(partsMarksClaimed(row, 'advantage-1', { [partClaimId('advantage-1', 'point')]: 7 })).toBe(0);
    expect(partsMarksClaimed(row, 'advantage-1', { [partClaimId('advantage-1', 'point')]: 'yes' })).toBe(3);
    expect(marksClaimed(card, { [partClaimId('advantage-1', 'point')]: 3, [partClaimId('advantage-2', 'discussion')]: 1 }, {})).toBe(4);
    // The row's own claim no longer counts: the parts are the row.
    expect(marksClaimed(card, { 'advantage-1': 6 }, {})).toBe(0);
    expect(claimableTotal(card)).toBe(card.totalMarks);
  });

  test('renders each part with its own mark buttons and a running total for the row', () => {
    const card = byId('cons-2017-hl-q2-b');
    render(<SessionScreen cards={[card as SecCard]} subjectLabel="Construction Studies" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    const criterion = screen.getByRole('region', { name: 'Marking criterion 1' });
    expect(within(criterion).getByText('0m of 6m')).toBeInTheDocument();
    fireEvent.click(within(criterion).getByRole('button', { name: 'Award 3 marks for point · Advantage 1 (3 for point, 3 for discussion)' }));
    fireEvent.click(within(criterion).getByRole('button', { name: 'Award 2 marks for discussion · Advantage 1 (3 for point, 3 for discussion)' }));
    expect(within(criterion).getByText('5m of 6m')).toBeInTheDocument();
    expect(within(criterion).getByRole('button', { name: /Award 3 marks for point/ })).toHaveAttribute('aria-pressed', 'true');
  });
});
