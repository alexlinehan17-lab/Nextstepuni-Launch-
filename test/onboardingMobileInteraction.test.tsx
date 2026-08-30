/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';

import Onboarding from '@/components/Onboarding';

vi.mock('@/utils/funnel', () => ({ trackFunnel: vi.fn() }));

const draftKey = 'nextstepuni:onboarding-draft:v1:mobile-qa:fresh';

function renderOnboarding() {
  return render(
    <Onboarding
      userId="mobile-qa"
      userName="Alex"
      onComplete={vi.fn()}
      onSkip={vi.fn()}
    />,
  );
}

function touchMove(target: Element, x: number, y: number): Event {
  const event = new Event('touchmove', { bubbles: true, cancelable: true });
  Object.defineProperty(event, 'touches', { value: [{ clientX: x, clientY: y }] });
  target.dispatchEvent(event);
  return event;
}

describe('mobile onboarding interaction', () => {
  beforeEach(() => localStorage.clear());

  it('opens every new stage at the top and persists it synchronously', () => {
    renderOnboarding();
    const scrollRegion = screen.getByTestId('onboarding-scroll-region');
    scrollRegion.scrollTop = 240;

    fireEvent.click(screen.getByRole('button', { name: 'Get Started' }));

    expect(scrollRegion.scrollTop).toBe(0);
    expect(JSON.parse(localStorage.getItem(draftKey) ?? '{}')).toMatchObject({
      version: 1,
      step: 2,
    });
  });

  it('absorbs an outward pull at the top without blocking an ordinary upward scroll', () => {
    renderOnboarding();
    const scrollRegion = screen.getByTestId('onboarding-scroll-region');
    Object.defineProperties(scrollRegion, {
      clientHeight: { configurable: true, value: 600 },
      scrollHeight: { configurable: true, value: 1200 },
    });

    fireEvent.touchStart(scrollRegion, { touches: [{ clientX: 80, clientY: 100 }] });
    expect(touchMove(scrollRegion, 80, 145).defaultPrevented).toBe(true);

    fireEvent.touchStart(scrollRegion, { touches: [{ clientX: 80, clientY: 145 }] });
    expect(touchMove(scrollRegion, 80, 95).defaultPrevented).toBe(false);
  });
});
