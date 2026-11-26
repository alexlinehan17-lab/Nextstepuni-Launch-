/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Things that come up over the screen (components/ui/Sheet.tsx and
 * Message.tsx): the sheet locks the page, keeps focus inside and closes on
 * Escape; the confirm puts the safe choice first; the toast is placed by the
 * frame so it clears the tab bar edge, and only one shows at a time.
 */
import { useState } from 'react';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, expect, test, vi } from 'vitest';
import { Sheet, Confirm } from '@/components/ui/Sheet';
import { Button } from '@/components/ui/Button';
import { MessageHost, dismissMessage, showMessage } from '@/components/ui/Message';
import { resetBodyScrollLock } from '@/utils/bodyScrollLock';

afterEach(() => { cleanup(); act(() => dismissMessage()); resetBodyScrollLock(); vi.useRealTimers(); });

function Harness({ onClose = vi.fn() }: { onClose?: () => void }) {
  const [open, setOpen] = useState(false);
  return (
    <>
      <button type="button" onClick={() => setOpen(true)}>Open the sheet</button>
      <Sheet open={open} title="What are you studying?" onClose={() => { onClose(); setOpen(false); }}
        footer={<Button kind="main" block>Choose Mathematics</Button>}>
        <button type="button">Accounting</button>
        <button type="button">Biology</button>
      </Sheet>
    </>
  );
}

test('the sheet locks the page behind it, and lets it go when it closes', async () => {
  render(<Harness />);
  expect(document.body).not.toHaveAttribute('data-scroll-lock');
  fireEvent.click(screen.getByRole('button', { name: 'Open the sheet' }));
  expect(await screen.findByRole('dialog', { name: 'What are you studying?' })).toBeInTheDocument();
  expect(document.body).toHaveAttribute('data-scroll-lock');
  // The frame's own lock also holds while a sheet layer is on the page.
  expect(document.querySelector('.frame-sheet-backdrop')).not.toBeNull();
  fireEvent.keyDown(window, { key: 'Escape' });
  await waitFor(() => expect(document.body).not.toHaveAttribute('data-scroll-lock'));
});

test('focus moves into the sheet and stays inside it; Tab from the last control comes back to the first', async () => {
  render(<Harness />);
  const opener = screen.getByRole('button', { name: 'Open the sheet' });
  opener.focus();
  fireEvent.click(opener);
  const dialog = await screen.findByRole('dialog');
  const close = screen.getByRole('button', { name: 'Close' });
  await waitFor(() => expect(document.activeElement).toBe(close));
  const last = screen.getByRole('button', { name: 'Choose Mathematics' });
  last.focus();
  fireEvent.keyDown(window, { key: 'Tab' });
  expect(document.activeElement).toBe(close);
  fireEvent.keyDown(window, { key: 'Tab', shiftKey: true });
  expect(document.activeElement).toBe(last);
  expect(dialog.contains(document.activeElement)).toBe(true);
});

test('Escape closes it, the dimmed page closes it, and focus returns to what opened it', async () => {
  const onClose = vi.fn();
  render(<Harness onClose={onClose} />);
  const opener = screen.getByRole('button', { name: 'Open the sheet' });
  opener.focus();
  fireEvent.click(opener);
  await screen.findByRole('dialog');
  fireEvent.keyDown(window, { key: 'Escape' });
  expect(onClose).toHaveBeenCalledTimes(1);
  await waitFor(() => expect(document.activeElement).toBe(opener));
  fireEvent.click(opener);
  await screen.findByRole('dialog');
  fireEvent.click(document.querySelector('.ui-scrim') as Element);
  expect(onClose).toHaveBeenCalledTimes(2);
});

test('one way out at the top left: Close, or Cancel with Save when there are changes', async () => {
  const save = vi.fn();
  const { rerender } = render(<Sheet open title="This week's goal" onClose={vi.fn()}><p>Body</p></Sheet>);
  expect(screen.getByRole('button', { name: 'Close' })).toBeInTheDocument();
  expect(screen.queryByRole('button', { name: 'Cancel' })).toBeNull();
  rerender(<Sheet open title="This week's goal" onClose={vi.fn()} save={{ label: 'Save', onPress: save }}><p>Body</p></Sheet>);
  expect(screen.queryByRole('button', { name: 'Close' })).toBeNull();
  const head = document.querySelector('.ui-sheet-head') as HTMLElement;
  expect(head.firstElementChild).toHaveTextContent('Cancel');
  fireEvent.click(screen.getByRole('button', { name: 'Save' }));
  expect(save).toHaveBeenCalled();
});

test('the sheet is built on the frame primitives, so it cannot reach the island or the home indicator', async () => {
  render(<Sheet open title="Details" onClose={vi.fn()}><p>Body</p></Sheet>);
  const dialog = await screen.findByRole('dialog');
  expect(dialog).toHaveClass('frame-sheet');
  expect(dialog.closest('.frame-sheet-backdrop')).not.toBeNull();
  // Portalled to the end of <body>, so no host's stacking context can trap it.
  expect(dialog.closest('#root, [data-testid]')).toBeNull();
});

test('the confirm puts focus on the safe choice; Escape and the dimmed page choose it', async () => {
  const keep = vi.fn();
  const danger = vi.fn();
  render(<Confirm open sentence="Delete your account?" detail="It cannot be brought back."
    keepLabel="Keep my account" onKeep={keep} dangerLabel="Delete account" onDanger={danger} />);
  const dialog = await screen.findByRole('alertdialog', { name: 'Delete your account?' });
  expect(dialog).toHaveAccessibleDescription('It cannot be brought back.');
  await waitFor(() => expect(document.activeElement).toBe(screen.getByRole('button', { name: 'Keep my account' })));
  fireEvent.keyDown(window, { key: 'Escape' });
  fireEvent.click(document.querySelector('.ui-confirm-layer .ui-scrim') as Element);
  expect(keep).toHaveBeenCalledTimes(2);
  expect(danger).not.toHaveBeenCalled();
  fireEvent.click(screen.getByRole('button', { name: 'Delete account' }));
  expect(danger).toHaveBeenCalledTimes(1);
});

test('the toast stack clears the tab bar edge: it is placed by the frame from --edge-bottom, which includes the tab bar', () => {
  render(<MessageHost />);
  act(() => { showMessage('Saved to your plan'); });
  const toast = document.querySelector('.ui-toast') as HTMLElement;
  expect(toast).toHaveTextContent('Saved to your plan');
  expect(toast).toHaveClass('frame-float', 'frame-float-bottom');
  const frame = readFileSync(join(process.cwd(), 'components/ui/frame.css'), 'utf8');
  expect(frame).toMatch(/\.frame-float-bottom\s*\{\s*bottom:\s*calc\(var\(--frame-float-gap, 16px\) \+ var\(--edge-bottom\)\);/);
  expect(frame).toMatch(/--edge-bottom:\s*calc\(var\(--safe-bottom\) \+ var\(--tabbar-h\)\);/);
  expect(frame).toMatch(/html\[data-tabbar\]\s*\{\s*--tabbar-h:\s*50px;/);
  // Above every page layer, and read out politely.
  const parts = readFileSync(join(process.cwd(), 'components/ui/parts.css'), 'utf8');
  expect(parts).toMatch(/\.ui-toast\s*\{[^}]*z-index:\s*var\(--z-toast\)/);
  expect(screen.getByRole('status')).toHaveTextContent('Saved to your plan');
});

test('one message at a time: a new one replaces the one showing, and each goes after four seconds', () => {
  vi.useFakeTimers();
  render(<MessageHost />);
  act(() => { showMessage('First'); });
  act(() => { showMessage('Second', { action: { label: 'Undo', onPress: vi.fn() } }); });
  act(() => { vi.advanceTimersByTime(200); });
  expect(document.querySelectorAll('.ui-toast')).toHaveLength(1);
  expect(document.querySelector('.ui-toast')).toHaveTextContent('Second');
  expect(screen.queryByText('First')).toBeNull();
  act(() => { vi.advanceTimersByTime(3700); });
  expect(document.querySelector('.ui-toast')).toHaveTextContent('Second');
  act(() => { vi.advanceTimersByTime(400); });   // four seconds: it starts to leave
  expect(document.querySelector('.ui-toast')).toHaveAttribute('data-state', 'leaving');
  act(() => { vi.advanceTimersByTime(200); });   // it has faded and gone
  expect(document.querySelector('.ui-toast')).toBeNull();
});

test('a sheet can carry its title at the left and a quiet status word at the right (a module’s Notes)', () => {
  render(<Sheet open titleAlign="start" titleSize="small" status="Saved" title="Notes" onClose={() => {}}><p>Body</p></Sheet>);
  const head = document.querySelector('.ui-sheet-head');
  expect(head).toHaveClass('ui-sheet-head--start');
  expect(screen.getByText('Saved')).toHaveClass('ui-sheet-status');
  expect(screen.getByRole('dialog', { name: 'Notes' })).toBeInTheDocument();
});
