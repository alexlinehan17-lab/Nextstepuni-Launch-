/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Shared parts extended for the paper viewer (area 6a, 27 Nov 2026): the top
 * bar's second row and its split layout, a row that leaves the app, and the
 * menu panel (Tools on a laptop) with its switch and action rows.
 */
import React, { useState } from 'react';
import { describe, expect, it, vi } from 'vitest';
import { act, fireEvent, render, screen, within } from '@testing-library/react';
import { TopBar } from '../components/ui/Bars';
import { List, Row } from '../components/ui/List';
import { MenuAction, MenuLabel, MenuPanel, MenuSwitch } from '../components/ui/Menu';

describe('TopBar for an over-screen with its own controls', () => {
  it('draws a second row under the name inside the same bar', () => {
    render(<TopBar ruled leave={{ kind: 'close', onPress: () => {}, label: 'Close viewer' }} over="2025 · Higher · Exam Paper" title="Physics"
      action={<button type="button">Tools</button>} below={<button type="button">Paper</button>} />);
    const bar = screen.getByRole('banner');
    expect(bar).toHaveClass('ui-bar--below');
    expect(within(bar).getByRole('heading', { name: 'Physics' })).toBeInTheDocument();
    expect(within(bar).getByRole('button', { name: 'Close viewer' })).toBeInTheDocument();
    expect(bar.querySelector('.ui-bar-below')).toContainElement(within(bar).getByRole('button', { name: 'Paper' }));
  });

  it('keeps the name at the left and a control centred when it has both', () => {
    render(<TopBar leave={{ kind: 'close', onPress: () => {} }} title="Physics" center={<button type="button">Paper</button>} action={<button type="button">Tools</button>} />);
    const bar = screen.getByRole('banner');
    expect(bar).toHaveClass('ui-bar--split');
    const zones = bar.querySelectorAll('.ui-bar-row > *');
    expect(zones).toHaveLength(3);
    expect(zones[0]).toHaveTextContent('Physics');
    expect(zones[1]).toHaveTextContent('Paper');
    expect(zones[2]).toHaveTextContent('Tools');
  });

  it('still shows a control alone in the middle when there is no name (the island on a laptop)', () => {
    render(<TopBar center={<button type="button">Island</button>} />);
    expect(screen.getByRole('banner')).not.toHaveClass('ui-bar--split');
    expect(screen.getByRole('button', { name: 'Island' }).closest('.ui-bar-mid--control')).not.toBeNull();
  });
});

describe('Row that leaves the app', () => {
  it('opens its link in the browser and carries the up-right arrow, not a chevron', () => {
    render(<List><Row external href="https://example.org/paper.pdf" title="Download the paper" meta="Opens in your browser · PDF · 1.3 MB" /></List>);
    const link = screen.getByRole('link', { name: /Download the paper/ });
    expect(link).toHaveAttribute('target', '_blank');
    expect(link).toHaveAttribute('rel', 'noopener noreferrer');
    expect(link.querySelector('.ui-row-chev--leaves')).not.toBeNull();
  });
});

async function tap(element: Element) {
  fireEvent.pointerDown(element, { pointerType: 'touch', pointerId: 1, isPrimary: true, button: 0, buttons: 1 });
  fireEvent.pointerUp(element, { pointerType: 'touch', pointerId: 1, isPrimary: true, button: 0, buttons: 0 });
  fireEvent.mouseDown(element, { button: 0 });
  fireEvent.mouseUp(element, { button: 0 });
  fireEvent.click(element, { button: 0, detail: 1 });
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 20)); });
}

describe('MenuPanel', () => {
  function Tools({ onTriage }: { onTriage: () => void }) {
    const [on, setOn] = useState(false);
    return (
      <MenuPanel label="Tools" buttonLabel="Study tools for this paper" face="Tools" head="Tools" status={on ? '1 on' : undefined}>
        <MenuLabel>Switch on</MenuLabel>
        <MenuSwitch title="Command words" meta="Decode what each question demands" checked={on} onChange={setOn} />
        <MenuLabel>Start</MenuLabel>
        <MenuAction title="Triage" meta="Rate each question before you start" onPress={onTriage} />
        <MenuAction title="Download the paper" href="https://example.org/paper.pdf" />
      </MenuPanel>
    );
  }

  it('opens under its button, switches a thing on and stays open, and an action closes it', async () => {
    const onTriage = vi.fn();
    render(<Tools onTriage={onTriage} />);
    await tap(screen.getByRole('button', { name: 'Study tools for this paper' }));
    const menu = await screen.findByRole('menu', { name: 'Study tools for this paper' });
    const toggle = within(menu).getByRole('menuitemcheckbox', { name: /Command words/ });
    expect(toggle).toHaveAttribute('aria-checked', 'false');
    await tap(toggle);
    expect(within(screen.getByRole('menu', { name: 'Study tools for this paper' })).getByRole('menuitemcheckbox', { name: /Command words/ })).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByText('1 on')).toBeInTheDocument();
    expect(within(screen.getByRole('menu', { name: 'Study tools for this paper' })).getByRole('menuitem', { name: /Download the paper/ })).toHaveAttribute('target', '_blank');
    await tap(within(screen.getByRole('menu', { name: 'Study tools for this paper' })).getByRole('menuitem', { name: /Triage/ }));
    expect(onTriage).toHaveBeenCalledTimes(1);
  });
});
