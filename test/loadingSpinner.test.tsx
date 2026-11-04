import { act, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { LoadingSpinner } from '@/components/LoadingSpinner';
import { LoadingCrewProvider } from '@/contexts/LoadingCrewContext';

const character = () => screen.getByRole('status').getAttribute('data-loading-crew');
afterEach(() => document.documentElement.classList.remove('dark'));

describe('LoadingSpinner', () => {
  it('announces the destination without narrating decorative artwork or fake progress', () => {
    const { rerender, baseElement } = render(<LoadingSpinner />);
    expect(screen.getByRole('status')).toHaveTextContent('Opening your space');
    rerender(<LoadingSpinner overlay label="Setting up your account" />);
    expect(screen.getByRole('status')).toHaveTextContent('Setting up your account');
    expect(screen.getByRole('status')).toHaveAttribute('aria-live', 'polite');
    expect(screen.getByRole('status')).toHaveAttribute('aria-atomic', 'true');
    expect(baseElement.querySelector('.crew-loading-figure')).toHaveAttribute('aria-hidden', 'true');
    expect(screen.queryByRole('progressbar')).toBeNull();
    expect(baseElement.querySelector('img[src*="star-person"]')).toBeNull();
  });

  it('escapes transformed route containers and can cover account chrome', () => {
    const { rerender } = render(<div data-testid="route" style={{ transform: 'translateY(80px)' }}><LoadingSpinner /></div>);
    const status = screen.getByRole('status');
    expect(screen.getByTestId('route').contains(status)).toBe(false);
    expect(status.parentElement).toBe(document.body);
    expect(status).toHaveAttribute('data-loader-placement', 'viewport');
    expect(status.className).toContain('min-h-[100dvh]');
    expect(status.className).toContain('z-[80]');
    rerender(<LoadingSpinner overlay />);
    expect(screen.getByRole('status').className).toContain('z-[200]');
  });

  it('keeps an existing tool header and back control available for panel waits', () => {
    render(<section data-testid="tool"><button>Back to Launchpad</button><LoadingSpinner variant="compact" placement="panel" label="Opening your planner" /></section>);
    expect(screen.getByTestId('tool').contains(screen.getByRole('status'))).toBe(true);
    expect(screen.getByRole('status')).toHaveAttribute('data-loader-placement', 'panel');
    expect(screen.getByRole('button', { name: 'Back to Launchpad' })).toBeEnabled();
  });

  it('keeps the random character through rerenders and nested fallback remounts', () => {
    const { rerender } = render(<LoadingCrewProvider transitionKey="student:planner"><LoadingSpinner key="outer" selection="random" /></LoadingCrewProvider>);
    const first = character();
    rerender(<LoadingCrewProvider transitionKey="student:planner"><LoadingSpinner key="inner" selection="random" placement="panel" label="Opening your planner" /></LoadingCrewProvider>);
    expect(character()).toBe(first);
    rerender(<LoadingCrewProvider transitionKey="student:planner"><LoadingSpinner key="inner" selection="random" label="Opening your planner" /></LoadingCrewProvider>);
    expect(character()).toBe(first);
  });

  it('honours the selected crew but never carries Hugger into another account', () => {
    const { rerender } = render(<LoadingCrewProvider transitionKey="alice:module" avatar="star-crew:hugger"><LoadingSpinner /></LoadingCrewProvider>);
    expect(character()).toBe('star-crew:hugger');
    rerender(<LoadingCrewProvider transitionKey="bob:module" avatar="Charlie"><LoadingSpinner /></LoadingCrewProvider>);
    expect(character()).not.toBe('star-crew:hugger');
    expect(character()).toMatch(/^star-crew:/);
  });

  it('draws afresh on navigation, without remounting the route subtree', () => {
    const random = vi.spyOn(Math, 'random').mockReturnValue(0);
    try {
      const { rerender } = render(<LoadingCrewProvider transitionKey="a"><input defaultValue="kept" /><LoadingSpinner selection="random" /></LoadingCrewProvider>);
      const input = screen.getByRole('textbox');
      expect(character()).toBe('star-crew:beanie');
      random.mockReturnValue(.99);
      rerender(<LoadingCrewProvider transitionKey="b"><input defaultValue="kept" /><LoadingSpinner selection="random" /></LoadingCrewProvider>);
      expect(character()).toBe('star-crew:musician');
      expect(screen.getByRole('textbox')).toBe(input);
    } finally { random.mockRestore(); }
  });

  it('keeps filled alpha artwork for tiled and standalone characters across both appearances', async () => {
    const { rerender } = render(<LoadingCrewProvider transitionKey="a" avatar="star-crew:reader"><LoadingSpinner /></LoadingCrewProvider>);
    const image = () => document.querySelector('.crew-loading img')!;
    expect(image()).toHaveAttribute('src', '/assets/dark/star-crew/personal/original-four.png');
    expect(image()).toHaveAttribute('data-artwork-appearance', 'light');
    await act(async () => { document.documentElement.classList.add('dark'); });
    expect(image()).toHaveAttribute('src', '/assets/dark/star-crew/personal/original-four.png');
    expect(image()).toHaveAttribute('data-artwork-appearance', 'dark');
    rerender(<LoadingCrewProvider transitionKey="a" avatar="star-crew:skater"><LoadingSpinner variant="compact" placement="panel" /></LoadingCrewProvider>);
    expect(image()).toHaveAttribute('src', '/assets/dark/star-crew/personal/05-skater.png');
    await act(async () => { document.documentElement.classList.remove('dark'); });
    expect(image()).toHaveAttribute('src', '/assets/dark/star-crew/personal/05-skater.png');
    expect(image()).toHaveAttribute('data-artwork-appearance', 'light');
  });

  it('handles failed artwork with one safe crew fallback and readable status', () => {
    render(<LoadingCrewProvider transitionKey="a" avatar="star-crew:hugger"><LoadingSpinner /></LoadingCrewProvider>);
    fireEvent.error(document.querySelector('.crew-loading img')!);
    expect(document.querySelector('.crew-loading img')).toHaveAttribute('src', '/assets/star-crew/personal/09-hugger.png');
    fireEvent.error(document.querySelector('.crew-loading img')!);
    expect(document.querySelector('.crew-loading img')).toHaveAttribute('src', '/assets/dark/star-crew/personal/05-skater.png');
    fireEvent.error(document.querySelector('.crew-loading img')!);
    expect(document.querySelector('.crew-loading img')).toHaveAttribute('src', '/assets/star-crew/personal/05-skater.png');
    fireEvent.error(document.querySelector('.crew-loading img')!);
    expect(document.querySelector('.crew-loading img')).toBeNull();
    expect(screen.getByRole('status')).toHaveTextContent('Opening your space');
  });
});
