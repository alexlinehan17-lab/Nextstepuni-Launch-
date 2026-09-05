import React from 'react';
import { afterEach, beforeEach, expect, test, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import FirstVisitCoachMarks from '@/components/FirstVisitCoachMarks';

const device = vi.hoisted(() => ({ mobile: true }));
vi.mock('@/hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => device.mobile }));

beforeEach(() => {
  device.mobile = true;
  vi.spyOn(HTMLElement.prototype, 'getBoundingClientRect').mockImplementation(function (this: HTMLElement) {
    return this.hasAttribute('hidden')
      ? new DOMRect(0, 0, 0, 0)
      : new DOMRect(20, 100, 180, 44);
  });
});
afterEach(() => vi.restoreAllMocks());

const renderTour = (onFinish = vi.fn()) => render(<>
  <button data-coach="modules">Modules</button>
  <button data-coach="launchpad">Launchpad</button>
  <button data-coach="help" hidden>Hidden sidebar help</button>
  <button data-coach="help">Profile help</button>
  <FirstVisitCoachMarks uid="mobile-coach-test" onFinish={onFinish} onOpenGuide={vi.fn()} />
</>);

test('mobile tour finds visible help and keeps the caption bounded with touch-sized controls', () => {
  const onFinish = vi.fn();
  renderTour(onFinish);
  fireEvent.click(screen.getByRole('button', { name: 'Next →' }));
  fireEvent.click(screen.getByRole('button', { name: 'Next →' }));
  const heading = screen.getByRole('heading', { name: 'Help is always here' });
  expect(heading.parentElement).toHaveClass('overflow-y-auto');
  expect(heading.parentElement?.style.maxHeight).toMatch(/^calc\(100dvh/);
  expect(screen.getByRole('button', { name: 'Skip' })).toHaveClass('min-h-11', 'min-w-11');
  expect(screen.getByRole('button', { name: 'Take the full tour' })).toHaveClass('min-h-11');
  fireEvent.click(screen.getByRole('button', { name: 'Done' }));
  expect(onFinish).toHaveBeenCalledOnce();
});

test('desktop retains its original tour copy and caption styling', () => {
  device.mobile = false;
  renderTour();
  fireEvent.click(screen.getByRole('button', { name: 'Next →' }));
  fireEvent.click(screen.getByRole('button', { name: 'Next →' }));
  const heading = screen.getByRole('heading', { name: 'Lost? Press this anytime' });
  expect(heading.parentElement).not.toHaveClass('overflow-y-auto');
  expect(screen.getByRole('button', { name: 'Skip' })).not.toHaveClass('min-h-11');
});
