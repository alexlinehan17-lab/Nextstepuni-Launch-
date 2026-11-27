/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 9, the sweep: the leftovers closed through the shared parts.
 * - One offline notice, the shared message at the foot of the screen (it was an amber bar over the
 *   top, and a second card from the toast provider under it), in today's words.
 * - A sheet that opens by itself or from a tap places its focus quietly (no ring); a key press
 *   brings the ring back.
 * - A menu row's own glyph (MenuAction's chevron) is not hidden by the rule that hides an unticked tick.
 */
import { useState } from 'react';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, expect, test, vi } from 'vitest';
import OfflineBanner from '@/components/OfflineBanner';
import { ToastProvider } from '@/components/Toast';
import { Sheet } from '@/components/ui/Sheet';
import { resetBodyScrollLock } from '@/utils/bodyScrollLock';

afterEach(() => { cleanup(); resetBodyScrollLock(); vi.useRealTimers(); });

test('offline shows one notice, the shared charcoal message at the foot, in today\'s words; back online says so', () => {
  vi.useFakeTimers();
  render(<ToastProvider><OfflineBanner /></ToastProvider>);
  expect(document.querySelector('.ui-toast')).toBeNull();
  act(() => { window.dispatchEvent(new Event('offline')); });
  act(() => { vi.advanceTimersByTime(50); });
  const notices = document.querySelectorAll('.ui-toast');
  expect(notices).toHaveLength(1);
  expect(notices[0]).toHaveTextContent('You\'re offline — changes will sync when you reconnect');
  expect(notices[0]).toHaveClass('frame-float', 'frame-float-bottom', 'ui-toast--standing');
  // The toast provider's own offline card (a second notice) is gone.
  expect(screen.queryByText(/some features may not work/)).toBeNull();
  expect(screen.getAllByRole('status').some(el => el.textContent?.includes('You\'re offline'))).toBe(true);
  act(() => { window.dispatchEvent(new Event('online')); });
  expect(document.querySelector('.ui-toast')).toHaveTextContent('Back online — syncing your changes');
  act(() => { vi.advanceTimersByTime(3000); });     // three seconds: it starts to leave
  expect(document.querySelector('.ui-toast')).toHaveAttribute('data-state', 'leaving');
  act(() => { vi.advanceTimersByTime(200); });      // it has faded and gone
  expect(document.querySelector('.ui-toast')).toBeNull();
});

function Opens({ startOpen = false }: { startOpen?: boolean }) {
  const [open, setOpen] = useState(startOpen);
  return (
    <>
      <button type="button" onClick={() => setOpen(true)}>Open the sheet</button>
      <Sheet open={open} title="Welcome" onClose={() => setOpen(false)}><button type="button">Explore</button></Sheet>
    </>
  );
}

test('a sheet that opens by itself takes focus without a ring; a key press brings the ring back', async () => {
  render(<Opens startOpen />);
  const close = await screen.findByRole('button', { name: 'Close' });
  await waitFor(() => expect(document.activeElement).toBe(close));
  expect(close).toHaveAttribute('data-quiet-focus');
  fireEvent.keyDown(window, { key: 'Tab' });
  expect(close).not.toHaveAttribute('data-quiet-focus');
  const focus = readFileSync(join(process.cwd(), 'design/quiet-focus.css'), 'utf8');
  expect(focus).toMatch(/\[data-quiet-focus\]:focus-visible\s*\{\s*outline:\s*none !important;/);
});

test('a sheet opened from the keyboard keeps its ring', async () => {
  render(<Opens />);
  const open = screen.getByRole('button', { name: 'Open the sheet' });
  fireEvent.keyDown(window, { key: 'Enter' });
  fireEvent.click(open);
  const close = await screen.findByRole('button', { name: 'Close' });
  await waitFor(() => expect(document.activeElement).toBe(close));
  expect(close).not.toHaveAttribute('data-quiet-focus');
});

test('a menu row\'s chevron shows: the rule that shows it comes after the rule that hides unticked ticks', () => {
  const parts = readFileSync(join(process.cwd(), 'components/ui/parts.css'), 'utf8');
  const hide = parts.indexOf('.ui-menu-item .ui-icon { visibility: hidden; }');
  const show = parts.indexOf('.ui-menu-item--row .ui-icon { visibility: visible; }');
  expect(hide).toBeGreaterThan(0);
  expect(show).toBeGreaterThan(hide);
});
