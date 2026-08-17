/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React from 'react';
import { beforeEach, describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';

import { ModuleLayout } from '@/components/ModuleLayout';
import { ModulePositionProvider } from '@/contexts/ModulePositionContext';
import { type ModuleTheme } from '@/types';

const SectionIcon: React.FC<{ size?: number }> = ({ size = 16 }) => (
  <svg aria-hidden="true" width={size} height={size} />
);

const theme = {
  sidebarModuleText: '',
  sidebarProgressBg: '',
  sidebarProgressShadow: '',
  sidebarActiveBg: '',
  sidebarCompletedBg: '',
  sidebarCompletedBorder: '',
  sidebarActiveBorder: '',
  sidebarActiveText: '',
  sidebarActiveEyebrow: '',
} as ModuleTheme;

describe('module navigation sidebar', () => {
  beforeEach(() => {
    window.scrollTo = vi.fn();
  });

  test('collapses to a narrow focus rail and can be expanded again', () => {
    render(
      <ModuleLayout
        moduleNumber="10"
        moduleTitle="Overcoming Illusions of Competence"
        theme={theme}
        sections={[{ id: 'intro', title: 'The Passive Traps', eyebrow: 'Step // 1', icon: SectionIcon }]}
        onBack={vi.fn()}
        progress={{ unlockedSection: 0 }}
        onProgressUpdate={vi.fn()}
      >
        {() => <article>Module content</article>}
      </ModuleLayout>,
    );

    const navigation = screen.getByLabelText('Module navigation');
    expect(screen.getByRole('button', { name: 'Back to modules' })).toHaveAttribute('type', 'button');
    const collapse = screen.getByRole('button', { name: 'Collapse module navigation' });
    expect(collapse).toHaveAttribute('aria-expanded', 'true');
    expect(navigation).toHaveClass('w-80');

    fireEvent.click(collapse);

    const expand = screen.getByRole('button', { name: 'Expand module navigation' });
    expect(expand).toHaveAttribute('aria-expanded', 'false');
    expect(navigation).toHaveClass('w-[60px]');
    expect(document.getElementById('module-sidebar-content')).toHaveAttribute('inert');
    expect(screen.getByText('Module content')).toBeInTheDocument();

    fireEvent.click(expand);

    expect(screen.getByRole('button', { name: 'Collapse module navigation' })).toHaveAttribute('aria-expanded', 'true');
    expect(navigation).toHaveClass('w-80');
    expect(document.getElementById('module-sidebar-content')).not.toHaveAttribute('inert');
  });

  test('uses the visible selection order and consistent module terminology', () => {
    render(
      <ModulePositionProvider value={{ displayNumber: '03', position: 3, total: 8 }}>
        <ModuleLayout
          moduleNumber="04"
          moduleTitle="Exam Hall Strategies"
          theme={theme}
          sections={[{ id: 'intro', title: 'Ready', eyebrow: 'Step // 1', icon: SectionIcon }]}
          onBack={vi.fn()}
          progress={{ unlockedSection: 0 }}
          onProgressUpdate={vi.fn()}
        >
          {() => <article>Module content</article>}
        </ModuleLayout>
      </ModulePositionProvider>,
    );

    expect(screen.getAllByText('Module 03')).toHaveLength(2);
    expect(screen.queryByText('Unit 04')).not.toBeInTheDocument();
  });
});
