/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The loading state is the screen a brand-new student stares at for the whole
 * of account provisioning, so its easy-to-break properties are pinned here:
 * the copy is caller-supplied (the default is a RETURNING-user message and is
 * wrong during signup), the visual remains decorative, and every instance is
 * portaled to the viewport so transformed route layouts cannot shift its centre.
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
    const { baseElement } = render(<LoadingSpinner label="Setting up your account" />);
    const status = screen.getByRole('status');
    expect(status.getAttribute('aria-live')).toBe('polite');
    // The miniature dashboard is decoration; the copy already carries the state.
    expect(baseElement.querySelector('.nsu-dashboard-assembly')?.getAttribute('aria-hidden')).toBe('true');
    expect(screen.queryByRole('progressbar')).toBeNull();
  });

  it('assembles the three product-specific dashboard cards', () => {
    const { baseElement } = render(<LoadingSpinner />);
    const cards = Array.from(baseElement.querySelectorAll('[data-loader-card]'));
    expect(cards.map(card => card.getAttribute('data-loader-card'))).toEqual([
      'course',
      'calendar',
      'progress',
    ]);
  });

  it('centres every variant against the dynamic viewport', () => {
    const { rerender } = render(<LoadingSpinner />);
    const status = screen.getByRole('status');
    expect(status.className).toContain('fixed');
    expect(status.className).toContain('inset-0');
    expect(status.className).toContain('min-h-[100dvh]');
    expect(status.className).toContain('items-center');
    expect(status.className).toContain('justify-center');
    expect(status.className).toContain('z-[80]');

    rerender(<LoadingSpinner overlay />);
    expect(screen.getByRole('status').className).toContain('z-[200]');
  });

  it('escapes transformed route containers before positioning', () => {
    render(
      <div data-testid="transformed-route" style={{ transform: 'translateY(80px)' }}>
        <LoadingSpinner />
      </div>,
    );

    const route = screen.getByTestId('transformed-route');
    const status = screen.getByRole('status');
    expect(route.contains(status)).toBe(false);
    expect(status.parentElement).toBe(document.body);
    expect(status.getAttribute('data-loader-placement')).toBe('viewport');
  });
});
