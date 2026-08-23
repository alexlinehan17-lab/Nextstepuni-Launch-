/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React from 'react';
import { beforeEach, describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';

vi.mock('@/contexts/AuthContext', () => ({
  useAuth: () => ({ user: { uid: 'student-1' }, authResolved: true }),
}));

import { NavigationProvider, useNavigation } from '@/contexts/NavigationContext';

const NavigationProbe: React.FC = () => {
  const nav = useNavigation();

  return (
    <>
      <output data-testid="view">{nav.state.viewState}</output>
      <output data-testid="dashboard-section">{nav.state.dashboardSection}</output>
      <output data-testid="journey-origin">{String(nav.state.cameFromJourney)}</output>
      <button onClick={() => nav.navigateToInnovationZone('journey')}>Open journey</button>
      <button onClick={() => nav.navigateToModule('focus-module', 'innovation-zone', null)}>
        Open profile focus
      </button>
      <button onClick={() => nav.navigateToModule('journey-module', 'innovation-zone', null, true)}>
        Open journey result module
      </button>
      <button onClick={() => nav.navigateToDashboard()}>Open progress</button>
      <button onClick={() => nav.setDashboardSection('milestones')}>Show milestones</button>
    </>
  );
};

describe('module journey provenance', () => {
  beforeEach(() => {
    window.history.replaceState({}, '', '/');
  });

  test('does not infer a journey return route for a global profile recommendation', () => {
    render(<NavigationProvider><NavigationProbe /></NavigationProvider>);

    fireEvent.click(screen.getByRole('button', { name: 'Open journey' }));
    expect(screen.getByTestId('view')).toHaveTextContent('innovation-zone');

    fireEvent.click(screen.getByRole('button', { name: 'Open profile focus' }));
    expect(screen.getByTestId('view')).toHaveTextContent('module');
    expect(screen.getByTestId('journey-origin')).toHaveTextContent('false');
    expect(window.location.search).not.toContain('from=journey');
  });

  test('retains the journey return route when the caller marks it explicitly', () => {
    render(<NavigationProvider><NavigationProbe /></NavigationProvider>);

    fireEvent.click(screen.getByRole('button', { name: 'Open journey' }));
    fireEvent.click(screen.getByRole('button', { name: 'Open journey result module' }));

    expect(screen.getByTestId('journey-origin')).toHaveTextContent('true');
    expect(window.location.search).toContain('from=journey');
  });

  test('redirects retired Training Hub links to My Progress', () => {
    window.history.replaceState({}, '', '/?view=gamification-hub');

    render(<NavigationProvider><NavigationProbe /></NavigationProvider>);

    expect(screen.getByTestId('view')).toHaveTextContent('dashboard');
    expect(screen.getByTestId('dashboard-section')).toHaveTextContent('milestones');
    expect(window.location.search).toContain('view=dashboard');
    expect(window.location.search).toContain('section=milestones');
    expect(window.location.search).not.toContain('gamification-hub');
  });

  test('normalizes a synced retired Training Hub entry without adding a replacement step', () => {
    window.history.replaceState({
      __navSynced: true,
      viewState: 'gamification-hub',
      currentCategory: null,
      currentModuleId: null,
      cameFromJourney: false,
      activeTool: null,
    }, '', '/?view=gamification-hub');

    render(<NavigationProvider><NavigationProbe /></NavigationProvider>);

    expect(screen.getByTestId('view')).toHaveTextContent('dashboard');
    expect(screen.getByTestId('dashboard-section')).toHaveTextContent('milestones');
    expect(window.history.state).toMatchObject({
      __navSynced: true,
      viewState: 'dashboard',
      dashboardSection: 'milestones',
    });
    expect(window.location.search).toBe('?view=dashboard&section=milestones');
  });

  test.each([
    ['synced', {
      __navSynced: true,
      viewState: 'gamification-hub',
      currentCategory: null,
      currentModuleId: null,
      cameFromJourney: false,
      activeTool: null,
    }],
    ['unsynced', {}],
  ])('canonicalizes a %s retired Training Hub entry restored by browser navigation', (_kind, historyState) => {
    render(<NavigationProvider><NavigationProbe /></NavigationProvider>);
    window.history.pushState(historyState, '', '/?view=gamification-hub');

    fireEvent(window, new PopStateEvent('popstate', { state: historyState }));

    expect(screen.getByTestId('view')).toHaveTextContent('dashboard');
    expect(screen.getByTestId('dashboard-section')).toHaveTextContent('milestones');
    expect(window.history.state).toMatchObject({
      __navSynced: true,
      viewState: 'dashboard',
      dashboardSection: 'milestones',
    });
    expect(window.location.search).toBe('?view=dashboard&section=milestones');
  });

  test('does not add a duplicate entry when reloading a non-dashboard page reached from Milestones', () => {
    window.history.replaceState({
      __navSynced: true,
      viewState: 'study-session',
      dashboardSection: 'milestones',
      currentCategory: null,
      currentModuleId: null,
      cameFromJourney: false,
      activeTool: null,
    }, '', '/?view=study-session');
    const pushState = vi.spyOn(window.history, 'pushState');

    render(<NavigationProvider><NavigationProbe /></NavigationProvider>);

    expect(screen.getByTestId('view')).toHaveTextContent('study-session');
    expect(pushState).not.toHaveBeenCalled();
    pushState.mockRestore();
  });

  test('replaces the current dashboard entry when changing sections', () => {
    render(<NavigationProvider><NavigationProbe /></NavigationProvider>);
    fireEvent.click(screen.getByRole('button', { name: 'Open progress' }));
    const pushState = vi.spyOn(window.history, 'pushState');
    const replaceState = vi.spyOn(window.history, 'replaceState');

    fireEvent.click(screen.getByRole('button', { name: 'Show milestones' }));

    expect(screen.getByTestId('dashboard-section')).toHaveTextContent('milestones');
    expect(window.location.search).toBe('?view=dashboard&section=milestones');
    expect(replaceState).toHaveBeenCalledOnce();
    expect(pushState).not.toHaveBeenCalled();
    replaceState.mockRestore();
    pushState.mockRestore();
  });
});
