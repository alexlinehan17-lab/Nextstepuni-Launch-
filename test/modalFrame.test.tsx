/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { describe, expect, test, vi } from 'vitest';

import ModalFrame from '@/components/ui/ModalFrame';

describe('ModalFrame focus management', () => {
  test('contains forward and reverse tabbing from the dialog boundary', async () => {
    render(
      <ModalFrame open onClose={vi.fn()} title="Focus test">
        <button type="button">First action</button>
        <button type="button">Last action</button>
      </ModalFrame>,
    );

    const dialog = screen.getByRole('dialog');
    const close = screen.getByRole('button', { name: 'Close' });
    const last = screen.getByRole('button', { name: 'Last action' });
    await waitFor(() => expect(dialog).toHaveFocus());

    fireEvent.keyDown(window, { key: 'Tab', shiftKey: true });
    expect(last).toHaveFocus();

    dialog.focus();
    fireEvent.keyDown(window, { key: 'Tab' });
    expect(close).toHaveFocus();

    last.focus();
    fireEvent.keyDown(window, { key: 'Tab' });
    expect(close).toHaveFocus();

    close.focus();
    fireEvent.keyDown(window, { key: 'Tab', shiftKey: true });
    expect(last).toHaveFocus();
  });

  test('uses the latest close callback and restores focus when closed', async () => {
    const opener = document.createElement('button');
    document.body.appendChild(opener);
    opener.focus();
    const firstClose = vi.fn();
    const latestClose = vi.fn();
    const { rerender, unmount } = render(
      <ModalFrame open onClose={firstClose} title="Focus test">Content</ModalFrame>,
    );
    await waitFor(() => expect(screen.getByRole('dialog')).toHaveFocus());

    rerender(<ModalFrame open onClose={latestClose} title="Focus test">Content</ModalFrame>);
    fireEvent.keyDown(window, { key: 'Escape' });

    expect(firstClose).not.toHaveBeenCalled();
    expect(latestClose).toHaveBeenCalledOnce();
    unmount();
    expect(opener).toHaveFocus();
    opener.remove();
  });
});
