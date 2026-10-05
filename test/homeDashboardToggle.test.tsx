/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The former inline home dashboard has been consolidated into My Progress.
 * The sidebar control now navigates there and legacy persisted visibility
 * settings must not resurrect duplicate analytics on home.
 */
import React from 'react';
import { beforeEach, describe, expect, test, vi } from 'vitest';
import { fireEvent, render, renderHook, screen } from '@testing-library/react';

import { KnowledgeTree } from '@/components/KnowledgeTree';
import { useSettings } from '@/hooks/useSettings';
import NextStepUniSidebar from '@/components/navigation/NextStepUniSidebar';
import { NavigationProvider, useNavigation } from '@/contexts/NavigationContext';

// Keep the real shared sidebar and navigation; avoid account network services.
vi.mock('@/components/GetPointsButton', () => ({ default: () => null }));
vi.mock('@/components/NotificationBell', () => ({ default: () => null }));

const noop = vi.fn();
const goToDashboard = vi.fn();

const NavigationLocation = () => <output aria-label="Current app view">{useNavigation().state.viewState}</output>;

const HomeHarness = () => {
  const { settings, updateSetting } = useSettings();

  return (
    <NavigationProvider><NavigationLocation /><NextStepUniSidebar
      user={{ uid: 'dashboard-toggle-test', name: 'Demo Student', avatar: '' }}
      settings={settings} updateSetting={updateSetting} onLogout={noop}
      onOpenSettings={noop} onOpenPassport={noop} onOpenSiteGuide={noop}
      onOpenFeedback={noop} onUnreadCountChange={noop} completedCount={0}
      totalCount={0} unreadCount={0}
    ><KnowledgeTree
      onSelectCategory={noop}
      onGoToModules={noop}
      onGoToInnovationZone={noop}
      onGoToDashboard={goToDashboard}
      onGoToLearningPaths={noop}
      onGoToJourney={noop}
      onSelectModule={noop}
      allCourses={[]}
      categoryTitles={{} as never}
      userProgress={{}}
      onLogout={noop}
      onOpenSettings={noop}
      onOpenPassport={noop}
      settings={settings}
      updateSetting={updateSetting}
      completedCount={0}
      totalCount={0}
      uid="dashboard-toggle-test"
    /></NextStepUniSidebar></NavigationProvider>
  );
};

describe('home dashboard navigation', () => {
  beforeEach(() => {
    localStorage.clear();
    localStorage.setItem('nsu-coachmarks:dashboard-toggle-test', '1');
    goToDashboard.mockClear();
    window.scrollTo = vi.fn();
    window.history.replaceState(null, '', '/');
  });

  test('is off by default for a new login', () => {
    const { result } = renderHook(() => useSettings());
    expect(result.current.settings.showDashboard).toBe(false);
  });

  test('the sidebar control enters My Progress without rendering duplicate analytics', () => {
    render(<HomeHarness />);

    expect(screen.queryByRole('region', { name: 'Home dashboard' })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'My Progress' }));
    expect(screen.getByLabelText('Current app view')).toHaveTextContent('dashboard');
    expect(screen.queryByRole('region', { name: 'Home dashboard' })).not.toBeInTheDocument();
  });

  test('a legacy showDashboard preference cannot reopen the retired home panel', () => {
    localStorage.setItem('nextstep-settings', JSON.stringify({ showDashboard: true }));
    render(<HomeHarness />);
    expect(screen.queryByRole('region', { name: 'Home dashboard' })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'My Progress' })).toBeInTheDocument();
  });
});
