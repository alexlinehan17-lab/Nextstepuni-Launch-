import React from 'react';
import { describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import SourceMaterialReader from '../components/MarkBank/SourceMaterialReader';
import { CARDS } from '../components/MarkBank/cards/maths/higher';
import { vaultPdf } from '../components/PaperTrail/vaultDocs';

vi.mock('../components/PaperTrail/vaultDocs', () => ({
  vaultPdf: vi.fn(() => new Promise(() => {})),
}));

describe('Mathematics original question reader', () => {
  it('opens the correct corpus, zooms, navigates and returns focus to the task', async () => {
    const card = CARDS.find(card => card.id === 'maths-2025-hl-p1-q8-e-iii')!;
    render(<SourceMaterialReader source={card.sourceMaterial!} subjectId={card.subjectId}
      year={card.year} paperFileid={card.paperFileid!} />);
    const trigger = screen.getByRole('button', { name: /open question pages/i });
    fireEvent.click(trigger);
    expect(screen.getByRole('dialog')).toBeInTheDocument();
    await waitFor(() => expect(vaultPdf).toHaveBeenCalled());
    const url = vi.mocked(vaultPdf).mock.calls.at(-1)![0];
    expect(decodeURIComponent(url)).toContain('papers/lc/mathematics/2025/paper/LC003ALP100EV.pdf');
    fireEvent.click(screen.getByRole('button', { name: 'Zoom in' }));
    expect(screen.getByText('125%')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Next source page' }));
    expect(screen.getByRole('button', { name: 'Go to source page 2' })).toHaveAttribute('aria-current', 'page');
    fireEvent.keyDown(screen.getByRole('dialog'), { key: 'Escape' });
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    await waitFor(() => expect(trigger).toHaveFocus());
  });
});
