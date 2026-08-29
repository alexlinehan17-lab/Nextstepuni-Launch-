/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The loading state is the screen a brand-new student stares at for the whole
 * of account provisioning, so its easy-to-break properties are pinned here:
 * the copy is caller-supplied (the default is a RETURNING-user message and is
 * wrong during signup), the visual remains decorative, and the overlay variant
 * actually covers the viewport (an inline loader there left the app header and
 * points pill visible behind it, which read as a half-loaded app).
 */
import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import { LoadingSpinner } from '@/components/LoadingSpinner';

describe('LoadingSpinner', () => {
  it('defaults to the returning-user copy', () => {
    render(<LoadingSpinner />);
    expect(screen.getByText('Loading your workspace')).toBeTruthy();
    expect(screen.getByText('Opening')).toBeTruthy();
  });

  it('lets the signup path replace copy that would be wrong for a new account', () => {
    render(<LoadingSpinner kicker="One moment" label="Setting up your account" />);
    expect(screen.getByText('Setting up your account')).toBeTruthy();
    expect(screen.queryByText('Loading your workspace')).toBeNull();
  });

  it('announces itself once, and does not narrate the animation', () => {
    const { container } = render(<LoadingSpinner label="Setting up your account" />);
    const status = screen.getByRole('status');
    expect(status.getAttribute('aria-live')).toBe('polite');
    // The miniature dashboard is decoration; the copy already carries the state.
    expect(container.querySelector('.nsu-dashboard-assembly')?.getAttribute('aria-hidden')).toBe('true');
    expect(screen.queryByRole('progressbar')).toBeNull();
  });

  it('assembles the three product-specific dashboard cards', () => {
    const { container } = render(<LoadingSpinner />);
    const cards = Array.from(container.querySelectorAll('[data-loader-card]'));
    expect(cards.map(card => card.getAttribute('data-loader-card'))).toEqual([
      'course',
      'calendar',
      'progress',
    ]);
  });

  it('covers the viewport only in the overlay variant', () => {
    const { container: inline } = render(<LoadingSpinner />);
    expect(inline.firstElementChild?.className).toContain('min-h-[45vh]');
    expect(inline.firstElementChild?.className).not.toContain('fixed');

    const { container: overlay } = render(<LoadingSpinner overlay />);
    expect(overlay.firstElementChild?.className).toContain('fixed');
    expect(overlay.firstElementChild?.className).toContain('inset-0');
  });
});
