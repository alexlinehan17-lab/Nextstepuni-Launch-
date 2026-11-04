/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Italian answers priced in halves (it_rows.py): each half is its own row, and a
 * shorter answer the scheme prices is a step the student can place.
 */
import { describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen, within } from '@testing-library/react';
import SessionScreen, { marksClaimed } from '@/components/MarkBank/SessionScreen';
import { isPointCard, tariffReconciles, type SecCard, type SecQuestionCard } from '@/types/markBank';
import { CARDS as ITALIAN_HIGHER } from '@/components/MarkBank/cards/italian/higher';
import { CARDS as ITALIAN_ORDINARY } from '@/components/MarkBank/cards/italian/ordinary';

vi.mock('@/components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

const byId = (id: string) => {
  const card = [...ITALIAN_HIGHER, ...ITALIAN_ORDINARY].find(candidate => candidate.id === id);
  if (!card || !isPointCard(card)) throw new Error(`no point card ${id}`);
  return card as SecQuestionCard;
};

describe('an Italian answer priced in halves', () => {
  test('is two rows at the printed prices that still add up to the card', () => {
    const card = byId('it-2021-hl-b2b-1-a');
    expect(card.rows.map(row => [row.id, row.kind, row.verbatim, row.marks])).toEqual([
      ['r-1-1', 'point', 'Erano stati compagni', 1], ['r-1-2', 'point', 'di scuola', 4],
    ]);
    expect(tariffReconciles(card)).toBe(true);
    expect(marksClaimed(card, { 'r-1-2': 'yes' }, {})).toBe(4);
  });

  test('renders each half as its own claim', () => {
    const card = byId('it-2021-hl-b2b-1-a');
    render(<SessionScreen cards={[card as SecCard]} subjectLabel="Italian" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    expect(screen.getByText('Erano stati compagni')).toBeInTheDocument();
    expect(screen.getByText('di scuola')).toBeInTheDocument();
  });

  test('a shorter answer the scheme prices is a step on the row, named in its note', () => {
    const card = byId('it-2022-ol-b1-3-b');
    const row = card.rows[0];
    expect([row.kind, row.verbatim, row.marks, row.permittedMarks]).toEqual(['criterion', 'Turin', 2, [0, 1, 2]]);
    expect(row.contextNote).toContain('“Italy” 1 mark');
    render(<SessionScreen cards={[card as SecCard]} subjectLabel="Italian" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    const criterion = screen.getByRole('region', { name: 'Marking criterion 1' });
    fireEvent.click(within(criterion).getByRole('button', { name: 'Award 1 marks for Turin' }));
    expect(within(criterion).getByRole('button', { name: 'Award 1 marks for Turin' })).toHaveAttribute('aria-pressed', 'true');
    expect(within(criterion).getByText(/“Italy” 1 mark/)).toBeInTheDocument();
  });
});
