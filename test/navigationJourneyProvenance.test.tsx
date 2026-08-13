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
      <output data-testid="journey-origin">{String(nav.state.cameFromJourney)}</output>
      <button onClick={() => nav.navigateToInnovationZone('journey')}>Open journey</button>
      <button onClick={() => nav.navigateToModule('focus-module', 'innovation-zone', null)}>
        Open profile focus
      </button>
      <button onClick={() => nav.navigateToModule('journey-module', 'innovation-zone', null, true)}>
        Open journey result module
      </button>
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
});
