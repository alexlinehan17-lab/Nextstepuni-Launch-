/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 7a: the direction, points and planning tools in the agreed look keep their behaviour.
 * Planner: tapping a block opens its next small step where you are.
 */
import React from 'react';
import { cleanup, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';
import PlannerWorkbench, { plannerEntries } from '@/components/launchpad/PlannerWorkbench';
import { DAYS_OF_WEEK, type WeeklyTimetable } from '@/components/subjectData';

const originalMatchMedia = window.matchMedia;
afterEach(() => { cleanup(); window.matchMedia = originalMatchMedia; });
beforeEach(() => localStorage.clear());

describe('Planner & Study', () => {
  const timetable: WeeklyTimetable = DAYS_OF_WEEK.map((day, index) => ({ day, blocks: index === 2 ? [{ subjectName: 'Geography', sessionType: 'practice', durationMinutes: 45 }, { subjectName: 'Mathematics', sessionType: 'practice', durationMinutes: 45 }] : [] }));
  const weekStart = new Date(2026, 10, 23);
  const props = () => ({ uid: 'student-a', timetable, subjects: ['Geography', 'Mathematics'], weekStart, weekOffset: 0, onWeekChange: vi.fn(), restDays: ['Sunday'], duration: 45, onSettings: vi.fn(), onPlanSettingsChange: vi.fn(), isComplete: () => false, isSkipped: () => false, onComplete: vi.fn(), onSkip: vi.fn(), onStudy: vi.fn(), schoolEvents: [], hints: {}, cues: {}, onCueSave: vi.fn(), explanation: <p>Why.</p> });

  test('on a phone, tapping a block opens its next small step over the week, and Study this block starts that block', async () => {
    const original = window.matchMedia;
    window.matchMedia = ((query: string) => ({ matches: false, media: query, addEventListener: () => {}, removeEventListener: () => {} })) as unknown as typeof window.matchMedia;
    try {
      const handlers = props(); const user = userEvent.setup();
      render(<PlannerWorkbench {...handlers} />);
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
      expect(screen.getByRole('heading', { level: 1, name: 'A little room for what’s next.' })).toBeInTheDocument();
      await user.click(screen.getByRole('button', { name: /Mathematics Practice/ }));
      const sheet = screen.getByRole('dialog', { name: 'Wednesday · Your next small step' });
      const step = within(sheet).getByRole('complementary', { name: 'Selected study block' });
      expect(within(step).getByRole('heading', { name: 'Mathematics' })).toBeInTheDocument();
      expect(within(step).getByText('Choose one question to work through')).toBeInTheDocument();
      await user.click(within(sheet).getByRole('button', { name: 'Study this block' }));
      expect(handlers.onStudy).toHaveBeenCalledWith(plannerEntries(timetable, weekStart)[1]);
    } finally { window.matchMedia = original; }
  });

  test('on a laptop the chosen block is marked in ink and its step sits beside the week, with the ⌘↵ shortcut', async () => {
    window.matchMedia = ((query: string) => ({ matches: true, media: query, addEventListener: () => {}, removeEventListener: () => {} })) as unknown as typeof window.matchMedia;
    const handlers = props(); const user = userEvent.setup();
    render(<PlannerWorkbench {...handlers} />);
    const maths = screen.getByRole('button', { name: /Mathematics Practice/ });
    await user.click(maths);
    expect(maths).toHaveAttribute('aria-pressed', 'true');
    expect(await within(screen.getByRole('complementary', { name: 'Selected study block' })).findByRole('heading', { name: 'Mathematics' })).toBeInTheDocument();
    window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', metaKey: true }));
    expect(handlers.onStudy).toHaveBeenCalledWith(plannerEntries(timetable, weekStart)[1]);
  });
});
