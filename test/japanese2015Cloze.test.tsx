import React from 'react';
import { describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import SessionScreen from '../components/MarkBank/SessionScreen';
import { CARDS } from '../components/MarkBank/cards/japanese/ordinary';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

describe('Japanese 2015 Ordinary published cloze reuse conditions', () => {
  it('allows each bank word once across its printed alternative positions and restores it when deselected', () => {
    const card = CARDS.find(card => card.id === 'ja-2015-ol-4')!;
    const onGrade = vi.fn();
    render(<SessionScreen cards={[card]} subjectLabel="Japanese" onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    expect(screen.getAllByText(/Original bank: 日本りょうり; scheme \(i\): 日本りようり; scheme \(iv\) alternative: 日本料理/)).toHaveLength(2);
    for (const word of ['日本りょうり', '学校', 'バスで', '大好き']) {
      const options = screen.getAllByRole('button', { name: new RegExp(`^${word}`) });
      expect(options).toHaveLength(2);
      expect(options[0]).toBeEnabled();
      expect(options[1]).toBeEnabled();
      fireEvent.click(options[0]);
      expect(options[0]).toHaveAttribute('aria-pressed', 'true');
      expect(options[1]).toBeDisabled();
      fireEvent.click(options[1]);
      expect(options[1]).toHaveAttribute('aria-pressed', 'false');
      fireEvent.click(options[0]);
      expect(options[1]).toBeEnabled();
      fireEvent.click(options[1]);
      expect(options[0]).toBeDisabled();
      fireEvent.click(options[1]);
      expect(options[0]).toBeEnabled();
    }
    fireEvent.click(screen.getAllByRole('button', { name: /^日本りょうり/ })[0]);
    fireEvent.click(screen.getByRole('button', { name: 'Shaky' }));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({ marksClaimed: 3, marksAvailable: 30 }));
  });
});
