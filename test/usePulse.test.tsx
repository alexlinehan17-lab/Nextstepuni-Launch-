/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The timer must not outlive the component.
 *
 * `setFlash(true); setTimeout(() => setFlash(false), 550)` was written by hand
 * across the app with the timer never held, so it fired whether or not the
 * component was still mounted. React 19 makes that a no-op in the browser,
 * which is why it went unnoticed — under jsdom it lands after the environment
 * has torn down and setState reaches for a `window` that is gone. That failed a
 * CI run in which all 2,550 tests passed.
 */
import { describe, expect, it, vi, beforeEach, afterEach } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import React from 'react';

import { usePulse } from '../hooks/usePulse';

const Probe: React.FC<{ ms?: number }> = ({ ms = 500 }) => {
  const [on, pulse, cancel] = usePulse(ms);
  return (
    <div>
      <span data-testid="state">{on ? 'on' : 'off'}</span>
      <button onClick={pulse}>pulse</button>
      <button onClick={cancel}>cancel</button>
    </div>
  );
};

describe('usePulse', () => {
  beforeEach(() => vi.useFakeTimers());
  afterEach(() => vi.useRealTimers());

  it('turns on, then off again after the delay', () => {
    render(<Probe />);
    expect(screen.getByTestId('state').textContent).toBe('off');
    act(() => { screen.getByText('pulse').click(); });
    expect(screen.getByTestId('state').textContent).toBe('on');
    act(() => { vi.advanceTimersByTime(499); });
    expect(screen.getByTestId('state').textContent).toBe('on');
    act(() => { vi.advanceTimersByTime(2); });
    expect(screen.getByTestId('state').textContent).toBe('off');
  });

  it('restarts rather than stacking, so a second pulse holds it on', () => {
    render(<Probe />);
    act(() => { screen.getByText('pulse').click(); });
    act(() => { vi.advanceTimersByTime(400); });
    act(() => { screen.getByText('pulse').click(); });
    // The FIRST timer would have fired here had it not been cleared.
    act(() => { vi.advanceTimersByTime(200); });
    expect(screen.getByTestId('state').textContent).toBe('on');
    act(() => { vi.advanceTimersByTime(400); });
    expect(screen.getByTestId('state').textContent).toBe('off');
  });

  it('cancel clears it immediately', () => {
    render(<Probe />);
    act(() => { screen.getByText('pulse').click(); });
    act(() => { screen.getByText('cancel').click(); });
    expect(screen.getByTestId('state').textContent).toBe('off');
    expect(vi.getTimerCount()).toBe(0);
  });

  it('leaves no timer behind when the component unmounts mid-pulse', () => {
    const { unmount } = render(<Probe />);
    act(() => { screen.getByText('pulse').click(); });
    expect(vi.getTimerCount()).toBe(1);
    unmount();
    // This is the whole point: a timer still pending here fires into a torn-down
    // environment, which is what failed CI.
    expect(vi.getTimerCount()).toBe(0);
  });
});
