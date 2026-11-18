/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A Mark Bank figure opens full screen to be zoomed (components/MarkBank/FigureZoom.tsx).
 */

import { describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';

import SessionScreen from '@/components/MarkBank/SessionScreen';
import { CARDS as ECONOMICS_HIGHER } from '@/components/MarkBank/cards/economics/higher';

vi.mock('@/components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

// Economics 2023 HL Section A Q10: the National Accounts table, 1972 px wide.
const tableCard = ECONOMICS_HIGHER.find(card => card.id === 'econ-2023-hl-sa-q10')!;
const renderTable = () => render(
  <SessionScreen cards={[tableCard]} subjectLabel="Economics" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />,
);

describe('a figure can be enlarged', () => {
  test('the card shows the crop as before, with a visible Enlarge control beside its attribution', () => {
    renderTable();
    if (tableCard.kind !== 'question' || !tableCard.figure) throw new Error('Missing table figure');
    const img = screen.getByAltText(tableCard.figure.alt);
    const figure = img.closest('figure')!;
    expect(within(figure).getByText(tableCard.figure.attribution)).toBeInTheDocument();
    expect(within(figure).getByRole('button', { name: 'Enlarge: Figure' })).toHaveTextContent('Enlarge');
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });

  test('opens full screen, zooms with buttons and keys, and closes with Escape back to the control', async () => {
    renderTable();
    const open = screen.getByRole('button', { name: 'Enlarge: Figure' });
    fireEvent.click(open);
    const viewer = screen.getByRole('dialog', { name: 'Figure, enlarged' });
    expect(within(viewer).getByRole('button', { name: /Zoomed to 100%/ })).toBeDisabled();
    expect(within(viewer).getByRole('button', { name: 'Zoom out' })).toBeDisabled();
    fireEvent.click(within(viewer).getByRole('button', { name: 'Zoom in' }));
    expect(within(viewer).getByRole('button', { name: /Zoomed to 150%/ })).toBeEnabled();
    fireEvent.keyDown(document.body, { key: '+' });
    expect(within(viewer).getByRole('button', { name: /Zoomed to 225%/ })).toBeInTheDocument();
    fireEvent.keyDown(document.body, { key: '0' });
    expect(within(viewer).getByRole('button', { name: /Zoomed to 100%/ })).toBeInTheDocument();
    expect(document.body).toHaveAttribute('data-scroll-lock');
    fireEvent.keyDown(document.body, { key: 'Escape' });
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    expect(document.body).not.toHaveAttribute('data-scroll-lock');
    await waitFor(() => expect(open).toHaveFocus());
    // Escape closed the viewer only, not the review.
    expect(screen.getByRole('button', { name: /Reveal the marking scheme/i })).toBeInTheDocument();
  });

  test('tapping the crop itself opens it too, and the close button closes it', () => {
    renderTable();
    if (tableCard.kind !== 'question' || !tableCard.figure) throw new Error('Missing table figure');
    fireEvent.click(screen.getByAltText(tableCard.figure.alt));
    const viewer = screen.getByRole('dialog', { name: 'Figure, enlarged' });
    fireEvent.click(within(viewer).getByRole('button', { name: 'Close enlarged figure' }));
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });
});
