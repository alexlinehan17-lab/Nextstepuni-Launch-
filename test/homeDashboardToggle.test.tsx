/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The home dashboard is an intentional, persisted layer of the home screen:
 * new students begin with the quieter navigation grid, then opt into or out
 * of the dashboard from the desktop sidebar.
 */
import React from 'react';
import { beforeEach, describe, expect, test, vi } from 'vitest';
import { fireEvent, render, renderHook, screen, waitFor } from '@testing-library/react';

import { KnowledgeTree } from '@/components/KnowledgeTree';
import { useSettings } from '@/hooks/useSettings';

const noop = vi.fn();
const scrollIntoView = vi.fn();

const HomeHarness = () => {
  const { settings, updateSetting } = useSettings();

  return (
    <KnowledgeTree
      onSelectCategory={noop}
      onGoToModules={noop}
      onGoToInnovationZone={noop}
      onGoToDashboard={noop}
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
    />
  );
};

describe('home dashboard visibility', () => {
  beforeEach(() => {
    localStorage.clear();
    localStorage.setItem('nsu-coachmarks:dashboard-toggle-test', '1');
    scrollIntoView.mockClear();
    HTMLElement.prototype.scrollIntoView = scrollIntoView;
    window.scrollTo = vi.fn();
  });

  test('is off by default for a new login', () => {
    const { result } = renderHook(() => useSettings());
    expect(result.current.settings.showDashboard).toBe(false);
  });

  test('the sidebar control reveals and hides it with matching control states', async () => {
    render(<HomeHarness />);

    expect(screen.queryByRole('region', { name: 'Home dashboard' })).not.toBeInTheDocument();

    const showButton = screen.getByRole('button', { name: 'Show Dashboard' });
    expect(showButton).toHaveAttribute('aria-pressed', 'false');
    fireEvent.click(showButton);

    expect(screen.getByRole('region', { name: 'Home dashboard' })).toBeInTheDocument();
    await waitFor(() => expect(scrollIntoView).toHaveBeenCalled());
    const hideButton = screen.getByRole('button', { name: 'Hide Dashboard' });
    expect(hideButton).toHaveAttribute('aria-pressed', 'true');
    fireEvent.click(hideButton);

    expect(screen.getByRole('button', { name: 'Show Dashboard' })).toHaveAttribute('aria-pressed', 'false');
    await waitFor(() => {
      expect(screen.queryByRole('region', { name: 'Home dashboard' })).not.toBeInTheDocument();
    });
  });
});
