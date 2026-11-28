/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 0, the frame: one Back, built once in the app's navigation state
 * (contexts/NavigationContext.tsx, goBack). Back returns to the screen you
 * came from; with no history (a reload, a deep link) it goes to the screen's
 * parent, in place; a step inside a screen (a subject inside a tool) is gone
 * back through first; a place shows no leave control at all.
 */
import React from 'react';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';

vi.mock('@/contexts/AuthContext', () => ({
  useAuth: () => ({ user: { uid: 'student-1' }, authResolved: true }),
}));

import { NavigationProvider, useBackStep, useNavigation } from '@/contexts/NavigationContext';
import PageHeader from '@/components/ui/PageHeader';
import BackButton from '@/components/ui/BackButton';

const Probe: React.FC<{ step?: () => void }> = ({ step }) => {
  const nav = useNavigation();
  useBackStep(Boolean(step), step ?? (() => {}));
  return (
    <>
      <output data-testid="view">{nav.state.viewState}</output>
      <output data-testid="tool">{nav.state.activeTool ?? ''}</output>
      <output data-testid="category">{nav.state.currentCategory ?? ''}</output>
      <button onClick={() => nav.navigateToModules()}>Modules</button>
      <button onClick={() => nav.navigateToCategory('exam-zone')}>World</button>
      <button onClick={() => nav.navigateToInnovationZone('paper-trail')}>Paper Trail</button>
      <button onClick={() => nav.navigateToSettings()}>Settings</button>
      <button onClick={() => nav.goBack()}>Go back</button>
      <PageHeader onBack={nav.goBack} eyebrow="The Programme" title="Screen" />
    </>
  );
};

beforeEach(() => {
  window.scrollTo = vi.fn();
  window.history.replaceState(null, '', '/');
});
afterEach(cleanup);

describe('one Back', () => {
  test('returns to the screen you came from, not to a fixed parent', async () => {
    render(<NavigationProvider><Probe /></NavigationProvider>);
    fireEvent.click(screen.getByRole('button', { name: 'Paper Trail' }));
    fireEvent.click(screen.getByRole('button', { name: 'Modules' }));
    expect(screen.getByTestId('view')).toHaveTextContent('modules');
    // The parent of Modules is Home; the screen it was opened from is Paper Trail.
    fireEvent.click(screen.getByRole('button', { name: 'Back' }));
    await waitFor(() => expect(screen.getByTestId('view')).toHaveTextContent('innovation-zone'));
    expect(screen.getByTestId('tool')).toHaveTextContent('paper-trail');
  });

  test('falls back to the parent when there is no history (a deep link), without growing history', () => {
    window.history.replaceState(null, '', '/?view=category&cat=exam-zone');
    render(<NavigationProvider><Probe /></NavigationProvider>);
    expect(screen.getByTestId('view')).toHaveTextContent('category');
    const before = window.history.length;
    fireEvent.click(screen.getByRole('button', { name: 'Back' }));
    expect(screen.getByTestId('view')).toHaveTextContent('modules');
    expect(window.location.search).toBe('?view=modules');
    expect(window.history.length).toBe(before);
    // Modules' own parent is Home.
    fireEvent.click(screen.getByRole('button', { name: 'Back' }));
    expect(screen.getByTestId('view')).toHaveTextContent('tree');
  });

  test('a tool deep-linked with no history goes back to the Launchpad', () => {
    window.history.replaceState(null, '', '/?view=innovation-zone&tool=paper-trail');
    render(<NavigationProvider><Probe /></NavigationProvider>);
    fireEvent.click(screen.getByRole('button', { name: 'Back' }));
    expect(screen.getByTestId('view')).toHaveTextContent('innovation-zone');
    expect(screen.getByTestId('tool')).toHaveTextContent('');
  });

  test('goes back through a step inside the screen before leaving it', () => {
    window.history.replaceState(null, '', '/?view=innovation-zone&tool=paper-trail');
    const step = vi.fn();
    render(<NavigationProvider><Probe step={step} /></NavigationProvider>);
    fireEvent.click(screen.getByRole('button', { name: 'Back' }));
    expect(step).toHaveBeenCalledTimes(1);
    expect(screen.getByTestId('tool')).toHaveTextContent('paper-trail');
  });

  test('Settings is a page with its own URL, and Back leaves it', async () => {
    render(<NavigationProvider><Probe /></NavigationProvider>);
    fireEvent.click(screen.getByRole('button', { name: 'Settings' }));
    expect(screen.getByTestId('view')).toHaveTextContent('settings');
    expect(window.location.search).toBe('?view=settings');
    fireEvent.click(screen.getByRole('button', { name: 'Back' }));
    await waitFor(() => expect(screen.getByTestId('view')).toHaveTextContent('tree'));
  });
});

describe('the leave control by kind of screen', () => {
  test('a place shows no leave control; a page shows one Back, top left', () => {
    window.history.replaceState(null, '', '/?view=dashboard');
    const { unmount } = render(<NavigationProvider><Probe /></NavigationProvider>);
    expect(screen.queryByRole('button', { name: 'Back' })).toBeNull();
    expect(screen.getByRole('heading', { name: 'Screen' })).toBeInTheDocument();
    unmount();
    window.history.replaceState(null, '', '/?view=modules');
    render(<NavigationProvider><Probe /></NavigationProvider>);
    const back = screen.getByRole('button', { name: 'Back' });
    expect(back.closest('header')?.className).toContain('frame-bar');
    expect(back.querySelector('svg')).not.toBeNull();
    expect(back.textContent).toBe('');
  });

  test('the shared back button is a bare chevron, and is not drawn on a place', () => {
    window.history.replaceState(null, '', '/?view=study-session');
    const onClick = vi.fn();
    const { unmount } = render(<NavigationProvider><BackButton onClick={onClick} label="Back to home" showLabel /></NavigationProvider>);
    expect(screen.queryByRole('button', { name: 'Back to home' })).toBeNull();
    unmount();
    window.history.replaceState(null, '', '/?view=module&mod=x');
    render(<NavigationProvider><BackButton onClick={onClick} label="Back to modules" showLabel /></NavigationProvider>);
    const back = screen.getByRole('button', { name: 'Back to modules' });
    expect(back.className).toContain('ui-icon-btn');
    expect(back.textContent).toBe('');
    act(() => { fireEvent.click(back); });
    expect(onClick).toHaveBeenCalledTimes(1);
  });
});

describe('second ways out are gone from the shared headers', () => {
  const read = (file: string) => readFileSync(join(process.cwd(), file), 'utf8');
  test('no "Back to home", "Back to Launchpad" or labelled back in the shared headers', () => {
    expect(read('components/ui/PageHeader.tsx')).not.toMatch(/Back to home/);
    expect(read('components/InnovationZone.tsx')).not.toMatch(/'Back to Launchpad'|'Back to home'|<BackButton/);
    expect(read('components/ui/BackButton.tsx')).not.toMatch(/ArrowLeft|showLabel && /);
    expect(read('components/AppRouter.tsx')).not.toMatch(/journey-return-bar/);
    expect(read('components/PaperTrail/PaperSelection.tsx')).not.toMatch(/'Paper Trail'\}\s*<\/button>/);
  });
  test('the app passes its one Back to every page', () => {
    const router = read('components/AppRouter.tsx');
    expect(router).toMatch(/const handleBack = \(\) => \{ nav\.goBack\(\); \};/);
    for (const page of ['InsightsView', 'LearningPathsView', 'YearPlansView', 'YourSetupView', 'AccreditationPage', 'ModulesView', 'MyDirection']) {
      expect(router).toMatch(new RegExp(`<${page}[\\s\\S]{0,400}?onBack=\\{handleBack\\}`));
    }
  });
});
