import React from 'react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import HorizontalTabs from '../components/ui/HorizontalTabs';

const settings = vi.hoisted(() => ({ mobile: true, reduced: false }));
vi.mock('../hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => settings.mobile }));
vi.mock('../components/Motion', () => ({ useReducedMotion: () => settings.reduced }));
const scrollTo = vi.fn();
const options = [{ value: 'all', label: 'All' }, { value: 'practice', label: 'Practice' }, { value: 'plan', label: 'Plan' }];
function Harness() {
  const [value, setValue] = React.useState('all');
  return <HorizontalTabs options={options} value={value} onChange={setValue} label="Categories" />;
}
beforeEach(() => {
  settings.mobile = true;
  settings.reduced = false;
  scrollTo.mockClear();
  Object.defineProperty(HTMLElement.prototype, 'scrollTo', { configurable: true, value: scrollTo });
});

describe('mobile and tablet tab navigation', () => {
  it('supports roving keyboard focus, arrows, Home and End', () => {
    render(<Harness />);
    const all = screen.getByRole('tab', { name: 'All' });
    const practice = screen.getByRole('tab', { name: 'Practice' });
    const plan = screen.getByRole('tab', { name: 'Plan' });
    expect(practice).toHaveAttribute('tabindex', '-1');
    all.focus();
    fireEvent.keyDown(all, { key: 'ArrowRight' });
    expect(practice).toHaveFocus();
    expect(practice).toHaveAttribute('aria-selected', 'true');
    fireEvent.keyDown(practice, { key: 'End' });
    expect(plan).toHaveFocus();
    fireEvent.keyDown(plan, { key: 'ArrowRight' });
    expect(all).toHaveFocus();
    fireEvent.keyDown(all, { key: 'ArrowLeft' });
    expect(plan).toHaveFocus();
    fireEvent.keyDown(plan, { key: 'Home' });
    expect(all).toHaveFocus();
  });
  it('does not animate the initial rail positioning', () => {
    render(<Harness />);
    expect(scrollTo).toHaveBeenLastCalledWith(expect.objectContaining({ behavior: 'auto' }));
    fireEvent.click(screen.getByRole('tab', { name: 'Plan' }));
    expect(scrollTo).toHaveBeenLastCalledWith(expect.objectContaining({ behavior: 'smooth' }));
  });
  it('respects reduced motion when switching categories', () => {
    settings.reduced = true;
    render(<Harness />);
    fireEvent.click(screen.getByRole('tab', { name: 'Plan' }));
    expect(scrollTo).toHaveBeenLastCalledWith(expect.objectContaining({ behavior: 'auto' }));
  });
  it('leaves desktop focus and scrolling behavior unchanged', () => {
    settings.mobile = false;
    render(<Harness />);
    expect(screen.getByRole('tab', { name: 'Practice' })).not.toHaveAttribute('tabindex');
    expect(scrollTo).toHaveBeenLastCalledWith(expect.objectContaining({ behavior: 'smooth' }));
  });
});
