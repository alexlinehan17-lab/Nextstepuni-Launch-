/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The loading state is the screen a brand-new student stares at for the whole
 * of account provisioning, so its two easy-to-break properties are pinned here:
 * the copy is caller-supplied (the default is a RETURNING-user message and is
 * wrong during signup), and the overlay variant actually covers the viewport
 * (an inline spinner there left the app header and points pill visible behind
 * it, which read as a half-loaded app).
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
    // The rule is decoration; the copy above already carries the message.
    expect(container.querySelector('.nsu-loader-rail')?.getAttribute('aria-hidden')).toBe('true');
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
