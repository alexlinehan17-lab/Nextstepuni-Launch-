/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React from 'react';
import { describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';

vi.mock('@capacitor/core', () => ({
  Capacitor: {
    getPlatform: () => 'ios',
    isNativePlatform: () => true,
  },
}));

vi.mock('@/components/WorldIconBlob', () => ({
  WorldIconBlob: () => <span aria-hidden="true" />,
}));

import { ModulesView } from '@/components/ModulesView';
import ModuleShowcase from '@/components/ModuleShowcase';
import { type CourseData } from '@/components/Library';

const courses: CourseData[] = [
  {
    id: 'mind-one',
    category: 'architecture-mindset',
    title: 'Mind One',
    subtitle: 'Start with your thinking',
    description: 'A first module about mindset.',
    sectionsCount: 4,
    tags: ['Mindset'],
    gradient: '',
    accentColor: '',
    pillBgColor: '',
  },
  {
    id: 'learn-one',
    category: 'learning-cheat-codes',
    title: 'Learn One',
    subtitle: 'Build a study system',
    description: 'A practical module about learning.',
    sectionsCount: 5,
    tags: ['Study'],
    gradient: '',
    accentColor: '',
    pillBgColor: '',
  },
];

describe('native iOS module selection', () => {
  test('opens a world directly from the compact world list', () => {
    const onSelectCategory = vi.fn();

    render(
      <ModulesView
        onBack={vi.fn()}
        onSelectCategory={onSelectCategory}
        onSelectModule={vi.fn()}
        allCourses={courses}
        categoryTitles={{} as never}
        userProgress={{ 'mind-one': { unlockedSection: 2 } }}
      />,
    );

    expect(screen.getByText('Choose a world')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Open Learn world' }));
    expect(onSelectCategory).toHaveBeenCalledWith('learning-cheat-codes');
  });

  test('opens a module directly from the compact module list', () => {
    const onSelectCourse = vi.fn();

    render(
      <ModuleShowcase
        courses={courses.filter(course => course.category === 'architecture-mindset')}
        categoryTitle="Mind"
        categoryId="architecture-mindset"
        userProgress={{ 'mind-one': { unlockedSection: 2 } }}
        onSelectCourse={onSelectCourse}
      />,
    );

    expect(screen.getByText('Choose a module')).toBeInTheDocument();
    expect(screen.getByText('Continue · 50%')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Mind One/i }));
    expect(onSelectCourse).toHaveBeenCalledWith('mind-one');
  });
});
