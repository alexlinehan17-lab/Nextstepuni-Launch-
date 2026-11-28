/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The shared menu's row-actions pieces (area 8a, the counsellor's student rows): a bare button with no
 * chevron, plain rows that do a thing and close the menu, a destructive row, a hairline between groups,
 * and tags ticked several at a time with the square mark while the menu stays open.
 */
import React, { useState } from 'react';
import { describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import { MenuAction, MenuCheckRows, MenuPanel, MenuRule } from '../components/ui/Menu';

function Demo({ onReset }: { onReset: () => void }) {
  const [tags, setTags] = useState<string[]>(['Priority']);
  return (
    <MenuPanel label="Fionn" buttonLabel="Actions for Fionn" buttonClassName="ui-icon-btn" chevron={false} face={<span>…</span>}>
      <MenuCheckRows label="Cohort tags" options={['DEIS', 'Priority'].map(t => ({ value: t, label: t }))} values={tags}
        onToggle={(t, on) => setTags(prev => on ? [...prev, t] : prev.filter(x => x !== t))} />
      <MenuRule />
      <MenuAction plain title="Reset password" onPress={onReset} />
      <MenuAction plain tone="danger" title="Delete account" onPress={() => {}} />
    </MenuPanel>
  );
}

describe('a row\'s actions menu', () => {
  test('the button has no chevron; tags tick several and the menu stays open; a plain row acts and closes it', async () => {
    const onReset = vi.fn();
    render(<Demo onReset={onReset} />);
    const button = screen.getByRole('button', { name: 'Actions for Fionn' });
    expect(button.querySelector('svg')).toBeNull();
    fireEvent.click(button);
    const deis = await screen.findByRole('menuitemcheckbox', { name: 'DEIS' });
    expect(deis).toHaveAttribute('aria-checked', 'false');
    expect(screen.getByRole('menuitemcheckbox', { name: 'Priority' })).toHaveAttribute('aria-checked', 'true');
    expect(deis.querySelector('.ui-mark--square')).not.toBeNull();
    fireEvent.click(deis);
    expect(await screen.findByRole('menuitemcheckbox', { name: 'DEIS' })).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByRole('separator')).toHaveClass('ui-menu-rule');
    const reset = screen.getByRole('menuitem', { name: 'Reset password' });
    expect(reset.querySelector('svg')).toBeNull();
    expect(screen.getByRole('menuitem', { name: 'Delete account' })).toHaveClass('ui-menu-item--danger');
    fireEvent.click(reset);
    expect(onReset).toHaveBeenCalledTimes(1);
  });
});

describe('Escape over an over-screen (area 8a)', () => {
  test('a sheet opened over an OverScreen closes first; the screen stays', async () => {
    const { OverScreen } = await import('../components/ui/OverScreen');
    const { Sheet } = await import('../components/ui/Sheet');
    const onEscape = vi.fn();
    const onClose = vi.fn();
    // The screen is up first, and the sheet opens over it later (so its listener comes second).
    const view = render(<OverScreen label="Student profile" onEscape={onEscape}><Sheet open={false} title="Send encouragement" onClose={onClose}><p>Body</p></Sheet></OverScreen>);
    view.rerender(<OverScreen label="Student profile" onEscape={onEscape}><Sheet open title="Send encouragement" onClose={onClose}><p>Body</p></Sheet></OverScreen>);
    fireEvent.keyDown(window, { key: 'Escape' });
    expect(onClose).toHaveBeenCalledTimes(1);
    expect(onEscape).not.toHaveBeenCalled();
  });
});
