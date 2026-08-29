/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The product tour must show the product that actually exists. These checks
 * prevent a hand-built preview or missing monogram tile from quietly replacing
 * a real app capture again, and pin the two top-level destinations added during
 * the walkthrough audit.
 */
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import SiteGuide from '@/components/SiteGuide';

const cards = [
  ['Home — your base camp', 'home'],
  ['Modules & the Library', 'modules'],
  ['Learning Paths', 'learning-paths'],
  ['Study Session & Focus', 'study'],
  ['The Launchpad', 'launchpad'],
  ['Paper Trail', 'paper-trail'],
  ['Mark Bank', 'mark-bank'],
  ['My Progress', 'progress'],
  ['Points Passport', 'points-passport'],
  ['My Journey', 'journey'],
] as const;

describe('SiteGuide', () => {
  it('uses one real app capture for every walkthrough card', async () => {
    render(<SiteGuide open onClose={() => {}} onGo={() => {}} />);

    for (const [index, [title, id]] of cards.entries()) {
      if (index > 0) {
        fireEvent.click(screen.getByRole('button', { name: `Go to card ${index + 1}: ${title}` }));
      }

      await waitFor(() => {
        const capture = screen.getByRole('img', { name: `${title} — real screenshot from the app` });
        expect(capture).toHaveAttribute('src', `/assets/guide/${id}.jpg`);
        expect(capture).toHaveAttribute('data-guide-capture', 'real-app');
      });
      expect(screen.queryByText('Screen capture unavailable')).not.toBeInTheDocument();
    }
  });

  it('deep-links Learning Paths and My Journey from their guide cards', async () => {
    const onClose = vi.fn();
    const onGo = vi.fn();
    render(<SiteGuide open onClose={onClose} onGo={onGo} />);

    fireEvent.click(screen.getByRole('button', { name: 'Go to card 3: Learning Paths' }));
    await waitFor(() => expect(screen.getByRole('button', { name: 'Explore Learning Paths' })).toBeInTheDocument());
    fireEvent.click(screen.getByRole('button', { name: 'Explore Learning Paths' }));
    expect(onGo).toHaveBeenLastCalledWith('learning-paths');

    fireEvent.click(screen.getByRole('button', { name: 'Go to card 10: My Journey' }));
    await waitFor(() => expect(screen.getByRole('button', { name: 'Visit My Journey' })).toBeInTheDocument());
    fireEvent.click(screen.getByRole('button', { name: 'Visit My Journey' }));
    expect(onGo).toHaveBeenLastCalledWith('journey');
    expect(onClose).toHaveBeenCalledTimes(2);
  });
});
