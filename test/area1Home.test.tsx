/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 1, Home (agreed 24-26 Nov 2026: d-look, r5-home, c-desk-home). On a
 * phone Home takes the frame's bar and Today's plan sits straight under the
 * charcoal Start button; every door Home had stays. The two shared parts the
 * phone Home needed: a Row with a drawn subject and its own accessible name,
 * and a bare Sheet for the quick tour.
 */
import React from 'react';
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import StudentHomeContent from '@/components/StudentHomeContent';
import HomeNextStep from '@/components/HomeNextStep';
import { List, Row } from '@/components/ui/List';
import { Sheet } from '@/components/ui/Sheet';
import type { CourseData } from '@/components/Library';

afterEach(cleanup);
beforeEach(() => { window.scrollTo = vi.fn(); });

const course = { id: 'agency', title: 'Controlling the Controllables', subtitle: 'The Attribution Retraining Guide', category: 'architecture-mindset', sectionsCount: 5 } as unknown as CourseData;

describe('Home on a phone', () => {
  const props = () => ({
    uid: 'student-a', userName: 'Aoife Byrne', allCourses: [course], categoryTitles: { 'architecture-mindset': 'The Architecture of your Mindset' },
    userProgress: { agency: { unlockedSection: 3 } }, onSelectModule: vi.fn(), onGoToStudy: vi.fn(), onGoToModules: vi.fn(), onGoToDashboard: vi.fn(),
    onGoToLearningPaths: vi.fn(), onGoToJourney: vi.fn(), onGoToInnovationZone: vi.fn(), onOpenMobileProfile: vi.fn(), onOpenFeedback: vi.fn(),
  });

  it('puts Today’s plan straight under the Start button, then the week, the module, and Go to', () => {
    const p = props();
    render(<StudentHomeContent {...p} layout="phone"
      plan={<HomeNextStep part="today" blocks={[{ subjectName: 'Irish', sessionType: 'practice', durationMinutes: 45 }]} completions={[]} hasProfile onStudy={vi.fn()} onPlan={vi.fn()} onProgress={vi.fn()} />} />);
    const headings = screen.getAllByRole('heading').map(heading => heading.textContent);
    expect(headings[0]).toMatch(/^Good (morning|afternoon|evening), Aoife\.$/);
    expect(headings.slice(1)).toEqual(['Today’s plan', 'Your week so far', 'Pick up where you left off', 'Go to']);
    const start = screen.getByRole('button', { name: 'Start a study session' });
    expect(start).toHaveClass('ui-btn--main', 'ui-btn--lg');
    // Start comes before Today's plan in the reading order.
    expect(start.compareDocumentPosition(screen.getByRole('heading', { name: 'Today’s plan' })) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    fireEvent.click(start);
    expect(p.onGoToStudy).toHaveBeenCalledOnce();
  });

  it('keeps every door: the account, the module, the five worlds, Progress, Learning Paths, My Island, Launchpad and Feedback', () => {
    const p = props();
    render(<StudentHomeContent {...p} layout="phone" />);
    const account = screen.getByRole('button', { name: 'Open profile and settings' });
    expect(account).toHaveAttribute('data-coach', 'help');
    fireEvent.click(account);
    fireEvent.click(screen.getByRole('button', { name: 'Continue learning: Controlling the Controllables' }));
    expect(p.onSelectModule).toHaveBeenCalledWith('agency');
    expect(screen.getByText('3 of 5 read · 2 to go')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Browse all five module worlds' }));
    fireEvent.click(screen.getByRole('button', { name: 'Progress' }));
    fireEvent.click(screen.getByRole('button', { name: 'Learning Paths: Find your path' }));
    fireEvent.click(screen.getByRole('button', { name: 'My Island: Build your island' }));
    const launchpad = screen.getByRole('button', { name: 'Launchpad: Open your toolkit' });
    expect(launchpad).toHaveAttribute('data-coach', 'launchpad');
    fireEvent.click(launchpad);
    fireEvent.click(screen.getByRole('button', { name: 'Feedback' }));
    for (const fn of [p.onOpenMobileProfile, p.onGoToModules, p.onGoToDashboard, p.onGoToLearningPaths, p.onGoToJourney, p.onGoToInnovationZone, p.onOpenFeedback]) {
      expect(fn).toHaveBeenCalledOnce();
    }
  });

  it('draws the plan and the weekly goal apart, so each can sit where the phone Home puts it', () => {
    const gamification = { currentRank: { id: 'driven' }, weeklyGoalProgress: { sessions: 6 } } as never;
    const today = render(<HomeNextStep part="today" blocks={[]} completions={[]} hasProfile gamification={gamification} onStudy={vi.fn()} onProgress={vi.fn()} />);
    expect(screen.getByRole('heading', { name: 'Today’s plan' })).toBeInTheDocument();
    expect(screen.queryByRole('region', { name: 'Weekly study goal' })).toBeNull();
    // An empty day is laid on the page with one action, not painted as a patch.
    expect(screen.getByRole('button', { name: 'Start a session' })).toHaveClass('ui-btn');
    today.unmount();
    render(<HomeNextStep part="goal" blocks={[]} completions={[]} hasProfile gamification={gamification} onProgress={vi.fn()} />);
    expect(screen.queryByRole('heading', { name: 'Today’s plan' })).toBeNull();
    expect(screen.getByRole('region', { name: 'Weekly study goal' })).toBeInTheDocument();
  });
});

describe('the shared parts Home needed', () => {
  it('a Row can carry a drawn subject, its own accessible name and a tour stop', () => {
    const press = vi.fn();
    render(<List><Row title="Irish" meta="Practice · 45 min" art={<span data-testid="art" />} label="Study Irish: Practice, 45 minutes" coach="study" onPress={press} /></List>);
    const row = screen.getByRole('button', { name: 'Study Irish: Practice, 45 minutes' });
    expect(row).toHaveAttribute('data-coach', 'study');
    expect(within(row).getByTestId('art').parentElement).toHaveClass('ui-row-art');
    fireEvent.click(row);
    expect(press).toHaveBeenCalledOnce();
  });

  it('a bare Sheet has no handle and no header, names itself, and can leave the dimming to its caller', () => {
    const close = vi.fn();
    render(<Sheet open bare dim={false} title="Quick tour" onClose={close} footer={<button type="button">Next</button>}><p>Words</p></Sheet>);
    const sheet = screen.getByRole('dialog', { name: 'Quick tour' });
    expect(sheet).toHaveClass('ui-sheet--bare', 'frame-sheet');
    expect(sheet.querySelector('.ui-sheet-grab, .ui-sheet-head')).toBeNull();
    expect(screen.queryByRole('button', { name: 'Close' })).toBeNull();
    expect(document.querySelector('.ui-scrim')).toBeNull();
    fireEvent.keyDown(document, { key: 'Escape' });
    expect(close).toHaveBeenCalledOnce();
  });
});
