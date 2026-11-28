/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The shared menu (components/ui/Menu.tsx) applies a choice on a TAP, with no
 * focus anywhere.
 *
 * The named fault (audit 03, F.3): on an iPhone a tapped button never takes
 * focus. A hand-built menu that closes when focus leaves it sees the focus go
 * at touch-down (a focusout whose relatedTarget is null), closes, and is gone
 * before the tap's click arrives, so nothing is ever chosen. These tests drive
 * the menu the way WebKit on iOS does: touch pointer events, focus dropped to
 * the page at touch-down, no element ever focused by the tap, then the click.
 */
import { useState } from 'react';
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, expect, test, vi } from 'vitest';
import { Menu, menuCollisionPadding } from '@/components/ui/Menu';
import ProgressSectionPicker from '@/components/dashboard/ProgressSectionPicker';

afterEach(cleanup);

const OPTIONS = [
  { value: 'all', label: 'All subjects' },
  { value: 'acc', label: 'Accounting' },
  { value: 'bio', label: 'Biology' },
  { value: 'iri', label: 'Irish' },
];

function Harness({ onChange }: { onChange: (value: string) => void }) {
  const [value, setValue] = useState('all');
  return <Menu label="Subject" value={value} options={OPTIONS} onChange={next => { setValue(next); onChange(next); }} />;
}

/** One finger tap as WebKit on iOS delivers it: no element takes focus, and
 *  whatever had focus loses it to the page at touch-down. */
async function tap(element: Element) {
  const touch = { pointerType: 'touch', pointerId: 1, isPrimary: true, button: 0, buttons: 1, bubbles: true };
  // Each event is its own act(), as the browser delivers each as its own task:
  // whatever React does on one event (closing a menu) happens before the next.
  fireEvent.pointerDown(element, touch);
  // Focus leaves whatever had it, to nowhere (relatedTarget null), at touch-down.
  const had = document.activeElement;
  if (had && had !== document.body) {
    fireEvent.focusOut(had, { relatedTarget: null });
    fireEvent.blur(had, { relatedTarget: null });
    (had as HTMLElement).blur();
  }
  fireEvent.pointerUp(element, { ...touch, buttons: 0 });
  fireEvent.mouseDown(element, { button: 0 });
  fireEvent.mouseUp(element, { button: 0 });
  fireEvent.click(element, { button: 0, detail: 1 });
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 20)); });
}

test('a tap opens the menu, and a tap on an option applies it at once and closes it, with nothing focused', async () => {
  const onChange = vi.fn();
  render(<Harness onChange={onChange} />);
  const button = screen.getByRole('button', { name: /Subject:\s*All subjects/ });

  await tap(button);
  const menu = await screen.findByRole('menu');
  expect(menu).toBeInTheDocument();
  // The current option carries the tick.
  expect(screen.getByRole('menuitemradio', { name: 'All subjects' })).toHaveAttribute('aria-checked', 'true');

  // Focus is somewhere other than the option we are about to tap (the page, or
  // the menu's own first row): the tap itself gives the option no focus.
  const option = screen.getByRole('menuitemradio', { name: 'Biology' });
  expect(document.activeElement).not.toBe(option);
  await tap(option);

  expect(onChange).toHaveBeenCalledTimes(1);
  expect(onChange).toHaveBeenCalledWith('bio');
  expect(screen.getByRole('button', { name: /Subject:\s*Biology/ })).toBeInTheDocument();
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 400)); });
  expect(screen.queryByRole('menu')).not.toBeInTheDocument();
});

test('control: the same tap on today\'s hand-built picker (My Progress) chooses nothing, so the tap above is the iPhone fault', async () => {
  const onChange = vi.fn();
  const sections = [
    { id: 'overview', label: 'Overview' }, { id: 'study', label: 'Study' }, { id: 'confidence', label: 'Confidence' },
  ] as const;
  render(<ProgressSectionPicker value="overview" options={[...sections]} onChange={onChange} />);
  await tap(screen.getByRole('button', { name: 'Progress section' }));
  expect(screen.getByRole('listbox')).toBeInTheDocument();
  await tap(screen.getByRole('option', { name: /Study/ }));
  // Focus left the open menu for nowhere at touch-down; it closed before the click.
  expect(onChange).not.toHaveBeenCalled();
  expect(screen.queryByRole('listbox')).not.toBeInTheDocument();
});

test('focus leaving to nowhere (a touch-down outside any control) does not close the menu', async () => {
  render(<Harness onChange={vi.fn()} />);
  await tap(screen.getByRole('button', { name: /Subject/ }));
  const menu = await screen.findByRole('menu');
  await act(async () => {
    const had = document.activeElement ?? document.body;
    fireEvent.focusOut(had, { relatedTarget: null });
    fireEvent.blur(had, { relatedTarget: null });
    await new Promise(resolve => setTimeout(resolve, 50));
  });
  expect(menu).toBeInTheDocument();
  expect(screen.getByRole('menu')).toBeInTheDocument();
});

test('Escape closes it without choosing', async () => {
  const onChange = vi.fn();
  render(<Harness onChange={onChange} />);
  await tap(screen.getByRole('button', { name: /Subject/ }));
  const menu = await screen.findByRole('menu');
  await act(async () => {
    fireEvent.keyDown(menu, { key: 'Escape' });
    await new Promise(resolve => setTimeout(resolve, 400));
  });
  expect(screen.queryByRole('menu')).not.toBeInTheDocument();
  expect(onChange).not.toHaveBeenCalled();
});

test('it opens inside the safe box: the insets, the tab bar and a gap are its collision padding', () => {
  document.documentElement.style.setProperty('--sat', '59px');
  document.documentElement.style.setProperty('--sab', '34px');
  document.documentElement.style.setProperty('--tabbar-h', '64px');
  document.documentElement.style.setProperty('--safe-top', 'var(--sat)');
  document.documentElement.style.setProperty('--safe-bottom', 'var(--sab)');
  try {
    const padding = menuCollisionPadding();
    // jsdom does not resolve var() chains in padding, so the inset part is only
    // checked in a real browser (the parts sheet on the simulated iPhone); here
    // the tab bar and the gap are.
    expect(padding.bottom).toBeGreaterThanOrEqual(64 + 8);
    expect(padding.top).toBeGreaterThanOrEqual(8);
  } finally {
    for (const name of ['--sat', '--sab', '--tabbar-h', '--safe-top', '--safe-bottom']) document.documentElement.style.removeProperty(name);
  }
});

test('a face shows in the button instead of the value: a row that opens a menu of choices (Modules on a laptop)', async () => {
  const onChange = vi.fn();
  render(<Menu label="Find a starting point" value="none" onChange={onChange} face={<span>Find a starting point</span>}
    options={[{ value: 'remember', label: 'I forget what I study' }, { value: 'start', label: 'I keep putting it off' }]} />);
  const button = screen.getByRole('button', { name: 'Find a starting point' });
  expect(button).not.toHaveTextContent('I forget what I study');
  fireEvent.click(button);
  const option = await screen.findByRole('menuitemradio', { name: 'I keep putting it off' });
  fireEvent.click(option);
  expect(onChange).toHaveBeenCalledWith('start');
});
