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

const noop = vi.fn();
const goToDashboard = vi.fn();

const HomeHarness = () => {
  const { settings, updateSetting } = useSettings();

  return (
    <KnowledgeTree
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
    />
  );
};

describe('home dashboard navigation', () => {
  beforeEach(() => {
    localStorage.clear();
    localStorage.setItem('nsu-coachmarks:dashboard-toggle-test', '1');
    goToDashboard.mockClear();
    window.scrollTo = vi.fn();
  });

  test('is off by default for a new login', () => {
    const { result } = renderHook(() => useSettings());
    expect(result.current.settings.showDashboard).toBe(false);
  });

  test('the sidebar control enters My Progress without rendering duplicate analytics', () => {
    render(<HomeHarness />);

    expect(screen.queryByRole('region', { name: 'Home dashboard' })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'My Progress' }));
    expect(goToDashboard).toHaveBeenCalledTimes(1);
    expect(screen.queryByRole('region', { name: 'Home dashboard' })).not.toBeInTheDocument();
  });

  test('a legacy showDashboard preference cannot reopen the retired home panel', () => {
    localStorage.setItem('nextstep-settings', JSON.stringify({ showDashboard: true }));
    render(<HomeHarness />);
    expect(screen.queryByRole('region', { name: 'Home dashboard' })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'My Progress' })).toBeInTheDocument();
  });
});
