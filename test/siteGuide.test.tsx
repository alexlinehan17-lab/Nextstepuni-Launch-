/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The product tour must show the product that actually exists. These checks
 * prevent a hand-built preview or missing monogram tile from quietly replacing
 * a real app capture again, and pin the two top-level destinations added during
 * the walkthrough audit.
 */
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

const device = vi.hoisted(() => ({ mobile: true }));
vi.mock('@/hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => device.mobile }));

import SiteGuide from '@/components/SiteGuide';

const cards = [
  ['A little room for what’s next.', 'home'],
  ['Five worlds. Your own pace.', 'modules'],
  ['Learning Paths', 'learning-paths'],
  ['Make some time.', 'study'],
  ['The Launchpad', 'launchpad'],
  ['Paper Trail', 'paper-trail'],
  ['Mark Bank', 'mark-bank'],
  ['My Progress', 'progress'],
  ['Points Passport', 'points-passport'],
  ['An island of your own.', 'journey'],
] as const;

describe('SiteGuide', () => {
  it.each([true, false])('uses current real app captures (mobile=%s)', async (mobile) => {
    device.mobile = mobile;
    render(<SiteGuide open onClose={() => {}} onGo={() => {}} />);

    for (const [index, [title, id]] of cards.entries()) {
      if (index > 0) {
        fireEvent.click(screen.getByRole('button', { name: 'Next page' }));
      }

      await waitFor(() => {
        const capture = screen.getByRole('img', { name: `${title} — screenshot from the app` });
        expect(capture).toHaveAttribute('src', `/assets/guide/2026-09-15/${mobile ? 'mobile' : 'desktop'}/${id}.webp`);
        expect(capture).toHaveAttribute('data-guide-capture', 'real-app');
        const file = readFileSync(resolve('public', capture.getAttribute('src')!.slice(1)));
        expect(file.subarray(0, 4).toString()).toBe('RIFF');
        expect(file.subarray(8, 12).toString()).toBe('WEBP');
      });
      expect(screen.queryByText('Screen capture unavailable')).not.toBeInTheDocument();
    }
  });

  it('resets screenshot expansion when moving between cards', () => {
    render(<SiteGuide open onClose={() => {}} onGo={() => {}} />);
    fireEvent.click(screen.getByRole('button', { name: /Expand .* screenshot/ }));
    expect(screen.getByRole('button', { name: /Collapse .* screenshot/ })).toHaveAttribute('aria-expanded', 'true');
    fireEvent.keyDown(window, { key: 'ArrowRight' });
    expect(screen.getByRole('button', { name: /Expand .* screenshot/ })).toHaveAttribute('aria-expanded', 'false');
    fireEvent.click(screen.getByRole('button', { name: 'Previous page' }));
    expect(screen.getByRole('button', { name: /Expand .* screenshot/ })).toHaveAttribute('aria-expanded', 'false');
  });

  it('deep-links Learning Paths and My Journey from their guide cards', async () => {
    const onClose = vi.fn();
    const onGo = vi.fn();
    render(<SiteGuide open onClose={onClose} onGo={onGo} />);

    for (let i = 0; i < 2; i++) fireEvent.click(screen.getByRole('button', { name: 'Next page' }));
    await waitFor(() => expect(screen.getByRole('button', { name: 'Explore Learning Paths' })).toBeInTheDocument());
    fireEvent.click(screen.getByRole('button', { name: 'Explore Learning Paths' }));
    expect(onGo).toHaveBeenLastCalledWith('learning-paths');

    for (let i = 0; i < 7; i++) fireEvent.click(screen.getByRole('button', { name: 'Next page' }));
    await waitFor(() => expect(screen.getByRole('button', { name: 'Visit My Island' })).toBeInTheDocument());
    fireEvent.click(screen.getByRole('button', { name: 'Visit My Island' }));
    expect(onGo).toHaveBeenLastCalledWith('journey');
    expect(onClose).toHaveBeenCalledTimes(2);
  });
});
