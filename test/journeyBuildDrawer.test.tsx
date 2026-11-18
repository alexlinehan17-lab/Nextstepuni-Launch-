import React from 'react';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import BuildDrawer from '../components/journey/BuildDrawer';

afterEach(() => { cleanup(); vi.restoreAllMocks(); });

function setup(narrow = false) {
  vi.spyOn(HTMLElement.prototype, 'clientHeight', 'get').mockReturnValue(760);
  const originalMedia = window.matchMedia;
  vi.spyOn(window, 'matchMedia').mockImplementation(query => ({ ...originalMedia(query), matches: narrow }));
  return render(<BuildDrawer open><input aria-label="Selected tile" defaultValue="Library" /></BuildDrawer>);
}

describe('Journey drawer resizing', () => {
  it.each([false, true])('keeps keyboard resizing within the usable range (phone: %s)', narrow => {
    setup(narrow);
    const slider = screen.getByRole('slider', { name: 'Build drawer height' });
    const value = () => Number(slider.getAttribute('aria-valuenow'));
    const start = value();
    fireEvent.keyDown(slider, { key: 'ArrowDown' });
    expect(value()).toBe(start - 24);
    fireEvent.keyDown(slider, { key: 'Home' });
    expect(value()).toBe(Number(slider.getAttribute('aria-valuemin')));
    fireEvent.keyDown(slider, { key: 'ArrowDown' });
    expect(value()).toBe(Number(slider.getAttribute('aria-valuemin')));
    fireEvent.keyDown(slider, { key: 'End' });
    fireEvent.keyDown(slider, { key: 'ArrowUp' });
    expect(value()).toBe(Number(slider.getAttribute('aria-valuemax')));
  });

  it('preserves work when compacting, expanding, and leaving build mode', () => {
    const view = setup();
    fireEvent.change(screen.getByLabelText('Selected tile'), { target: { value: 'Pond' } });
    fireEvent.click(screen.getByRole('button', { name: 'Make build drawer smaller' }));
    expect(screen.getByRole('slider')).toHaveAttribute('aria-valuenow', '176');
    fireEvent.click(screen.getByRole('button', { name: 'Expand build drawer' }));
    expect(screen.getByLabelText('Selected tile')).toHaveValue('Pond');
    view.rerender(<BuildDrawer open={false}><input aria-label="Selected tile" defaultValue="Library" /></BuildDrawer>);
    expect(screen.queryByRole('slider')).toBeNull();
    view.rerender(<BuildDrawer open><input aria-label="Selected tile" defaultValue="Library" /></BuildDrawer>);
    expect(screen.getByLabelText('Selected tile')).toHaveValue('Pond');
  });
});
