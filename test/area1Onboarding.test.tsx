/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 1, onboarding (r5-onboarding, agreed 26 Nov 2026). The look changed
 * (bold capital titles in the one typeface, white tiles with a thin line, the
 * ink outline and the drawn tick, a charcoal Continue); the flow, the questions,
 * the answers saved and the step count did not. The white steps now follow the
 * phone's dark setting; the orange pages stay orange.
 */
import React from 'react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import Onboarding from '@/components/Onboarding';
import { buildNorthStar, buildProfile, draftKey, initialDraft, type SetupDraft } from '@/components/onboarding/model';

vi.mock('@/utils/funnel', () => ({ trackFunnel: vi.fn() }));
const device = vi.hoisted(() => ({ mobile: true }));
vi.mock('@/hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => device.mobile }));

const uid = 'area1-onboarding';
function finished(): SetupDraft {
  return { ...initialDraft(), step: 'summary', year: '6th', category: 'college-learning', vision: ['campus'], subjects: ['English', 'Irish'],
    configs: { English: { level: 'ordinary', current: 'O2', target: 'O1', reviewed: true }, Irish: { level: 'higher', current: 'H3', target: 'H1', reviewed: true } },
    date: '2030-06-05', dateEdited: true, rest: ['Saturday', 'Sunday'], gradeSubject: 'English' };
}
function mount(draft?: SetupDraft, complete = vi.fn()) {
  if (draft) localStorage.setItem(draftKey(uid, 'fresh'), JSON.stringify(draft));
  return render(<Onboarding userId={uid} userName="Aoife Byrne" onComplete={complete} onSkip={vi.fn()} />);
}
function prefersDark(dark: boolean) {
  window.matchMedia = vi.fn().mockImplementation((query: string) => ({
    matches: dark && query.includes('prefers-color-scheme: dark'), media: query, onchange: null,
    addEventListener: vi.fn(), removeEventListener: vi.fn(), addListener: vi.fn(), removeListener: vi.fn(), dispatchEvent: vi.fn(),
  }));
}

beforeEach(() => { localStorage.clear(); device.mobile = true; prefersDark(false); document.documentElement.classList.remove('dark'); });
afterEach(cleanup);

describe.each([['phone', true], ['laptop', false]])('onboarding on a %s', (_name, mobile) => {
  beforeEach(() => { device.mobile = mobile; });

  it('saves the same answers and reaches the same end', async () => {
    const complete = vi.fn().mockResolvedValue(undefined);
    const draft = finished();
    mount(draft, complete);
    fireEvent.click(screen.getByRole('button', { name: 'Start learning' }));
    await waitFor(() => expect(complete).toHaveBeenCalledOnce());
    const stamp = { createdAt: expect.any(String), updatedAt: expect.any(String) };
    expect(complete.mock.calls[0][0]).toEqual({ ...buildProfile(draft), ...stamp });
    const { createdAt: _c, updatedAt: _u, reviewedAt: _r, ...star } = buildNorthStar(draft) as unknown as Record<string, unknown>;
    expect(complete.mock.calls[0][1]).toMatchObject(star);
    expect(complete.mock.calls[0][2]).toBe(false);
  });

  it('names the missing step in the sentence above Continue, then lets it go once chosen', () => {
    mount();
    fireEvent.click(screen.getByRole('button', { name: 'Get started' }));
    const next = screen.getByRole('button', { name: 'Continue' });
    expect(next).toBeDisabled();
    expect(next).toHaveAttribute('aria-describedby', 'setup-validation');
    expect(document.getElementById('setup-validation')).toHaveTextContent('Choose your school year to continue.');
    fireEvent.click(screen.getByRole('button', { name: '6th Year' }));
    expect(next).toBeEnabled();
    expect(document.getElementById('setup-validation')).toHaveTextContent('');
  });

  it('marks a chosen tile as chosen for assistive technology, and only that one', () => {
    mount();
    fireEvent.click(screen.getByRole('button', { name: 'Get started' }));
    fireEvent.click(screen.getByRole('button', { name: '6th Year' }));
    const sixth = screen.getByRole('button', { name: '6th Year' });
    expect(sixth).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByRole('button', { name: '5th Year' })).toHaveAttribute('aria-pressed', 'false');
    // The drawn tick is decoration for the eye; the state is in aria-pressed.
    const mark = sixth.querySelector('.ui-mark');
    expect(mark).toHaveAttribute('aria-hidden', 'true');
    expect(mark).toHaveAttribute('data-mark', 'on');
    expect(screen.getByRole('button', { name: '5th Year' }).querySelector('.ui-mark')).toHaveAttribute('data-mark', 'off');
  });
});

describe('onboarding and the phone’s dark setting', () => {
  it('turns the white steps dark when the phone is dark, and keeps the orange pages orange', () => {
    prefersDark(true);
    const view = mount();
    const flow = view.container.querySelector('.setup-flow');
    expect(flow).toHaveAttribute('data-surface', 'orange');
    expect(flow).not.toHaveClass('dark');
    fireEvent.click(screen.getByRole('button', { name: 'Get started' }));
    expect(flow).toHaveAttribute('data-surface', 'paper');
    expect(flow).toHaveClass('dark');
  });

  it('stays light when the phone is light', () => {
    const view = mount();
    fireEvent.click(screen.getByRole('button', { name: 'Get started' }));
    expect(view.container.querySelector('.setup-flow')).not.toHaveClass('dark');
  });
});
