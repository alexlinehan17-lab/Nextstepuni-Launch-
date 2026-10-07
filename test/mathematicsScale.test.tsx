import React from 'react';
import { describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import SessionScreen, { marksClaimed, showsRowMarks } from '../components/MarkBank/SessionScreen';
import { mathematicsScaleMarks, type MathematicsScaleCard } from '../components/MarkBank/MathematicsScalePanel';
import { CARDS as FOUNDATION } from '../components/MarkBank/cards/maths/foundation';
import { CARDS } from '../components/MarkBank/cards/maths/higher';
import { vaultPdf } from '../components/PaperTrail/vaultDocs';

vi.mock('../components/PaperTrail/vaultDocs', () => ({
  vaultPdf: vi.fn(() => new Promise(() => {})),
}));

const card = CARDS.find(c => c.id === 'maths-2025-hl-p1-q1-a')! as MathematicsScaleCard & typeof CARDS[number];

describe('Mathematics published credit scale', () => {
  it('awards one permitted mark and never adds the old checklist bands', () => {
    expect(card.mathematicsScale.marks).toEqual([0, 2, 4, 6, 10]);
    for (const mark of [0, 2, 4, 6, 9, 10]) expect(mathematicsScaleMarks(card, mark)).toBe(mark);
    for (const mark of [-1, 1, 3, 5, 7, 8, 11]) expect(mathematicsScaleMarks(card, mark)).toBe(0);
    expect(showsRowMarks(card)).toBe(false);
    expect(marksClaimed(card, {}, { [card.rows[0].id]: [0, 1, 2] })).toBe(0);
  });

  it('uses Foundation scale marks and labels in a real review session', () => {
    const foundation = FOUNDATION.find(c => c.id === 'maths-2025-fl-q7-c-d')!;
    const onGrade = vi.fn();
    render(<SessionScreen cards={[foundation]} subjectLabel="Mathematics"
      onGrade={onGrade} onExit={vi.fn()} onFinish={vi.fn()} />);
    expect(screen.getByText(/FOUNDATION LEVEL/)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    expect(screen.queryByRole('radio', { name: 'High partial credit, 6 of 10 marks' })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('radio', { name: 'High partial credit, 7 of 10 marks' }));
    fireEvent.click(screen.getByRole('button', { name: /^Shaky/ }));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({
      cardId: foundation.id, marksClaimed: 7, marksAvailable: 10, grade: 'shaky',
    }));
  });

  it('keeps the scheme hidden until reveal, replaces the selected award and saves it', async () => {
    const onGrade = vi.fn();
    render(<SessionScreen cards={[card]} subjectLabel="Mathematics"
      onGrade={onGrade} onExit={vi.fn()} onFinish={vi.fn()} />);
    expect(screen.queryByRole('button', { name: /Open marking scheme/ })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    expect(screen.queryByRole('button', { name: /Select all/ })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('radio', { name: 'Low partial credit, 2 of 10 marks' }));
    fireEvent.click(screen.getByRole('radio', { name: 'High partial credit, 6 of 10 marks' }));
    expect(screen.getByRole('radio', { name: 'Low partial credit, 2 of 10 marks' })).not.toBeChecked();
    expect(screen.getByRole('radio', { name: 'High partial credit, 6 of 10 marks' })).toBeChecked();
    expect(screen.getByText(/Your SEC scale award is 6 of 10 marks/)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Open marking scheme/ }));
    await waitFor(() => expect(vaultPdf).toHaveBeenCalled());
    expect(decodeURIComponent(vi.mocked(vaultPdf).mock.calls.at(-1)![0]))
      .toContain('papers/lc/mathematics/2025/scheme/LC003ALP000EV.pdf');
    fireEvent.keyDown(screen.getByRole('dialog'), { key: 'Escape' });
    fireEvent.click(screen.getByRole('button', { name: /^Shaky/ }));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({
      cardId: card.id, marksClaimed: 6, marksAvailable: 10, grade: 'shaky',
    }));
  });
});
