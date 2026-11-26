/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 5 of the design build: Modules (boards c-modules-pick, r5-modules). One card picks up where
 * the student left off and goes straight to their step; five worlds you press; search, the starting
 * points and the notebook keep today's results and routes.
 */
import React from 'react';
import { afterEach, describe, expect, test, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';

const device = vi.hoisted(() => ({ phone: false }));
vi.mock('@/hooks/useCompactLayout', () => ({ useCompactLayout: () => device.phone }));
vi.mock('@/components/WorldIconBlob', () => ({ WorldIconBlob: () => <span aria-hidden="true" /> }));

import { ModulesView } from '@/components/ModulesView';
import ModuleShowcase, { ModuleWorldScreen } from '@/components/ModuleShowcase';
import { requestedModuleResume, clearModuleResumeRequest } from '@/components/learning/intents';
import { ALL_COURSES } from '@/courseData';
import type { UserProgress } from '@/types';

afterEach(() => { cleanup(); device.phone = false; });

const agency = ALL_COURSES.find(course => course.id === 'agency-architecture-protocol')!;
const progress: UserProgress = {
  [agency.id]: { unlockedSection: 3, reading: { sectionsByMode: { full: [] }, lastSectionId: 'x', lastSectionIndex: 3, lastMode: 'full', lastVisitedAt: '2026-11-20T10:00:00.000Z' } },
} as UserProgress;
const senior = ALL_COURSES.filter(course => course.curriculum !== 'junior');

function renderModules(props: Partial<React.ComponentProps<typeof ModulesView>> = {}) {
  const onSelectModule = vi.fn(); const onSelectCategory = vi.fn();
  render(<ModulesView onBack={vi.fn()} onSelectCategory={onSelectCategory} onSelectModule={onSelectModule}
    allCourses={senior} categoryTitles={{} as never} userProgress={progress} {...props} />);
  return { onSelectModule, onSelectCategory };
}

describe('Modules', () => {
  test('one card picks up where you left off, and Continue reading goes straight to your step', () => {
    clearModuleResumeRequest(agency.id);
    const { onSelectModule } = renderModules();
    const card = screen.getByRole('region', { name: 'Pick up where you left off' });
    expect(within(card).getByRole('heading', { name: agency.title })).toBeInTheDocument();
    expect(within(card).getByText(/Section 4 of 5/)).toBeInTheDocument();
    fireEvent.click(within(card).getByRole('button', { name: 'Continue reading' }));
    expect(onSelectModule).toHaveBeenCalledWith(agency.id);
    expect(requestedModuleResume(agency.id)).toBe(true);
    // there is one Continue on the page, not two
    expect(screen.getAllByRole('button', { name: /^Continue/ })).toHaveLength(1);
  });

  test('five worlds, each a box you press with its number, words and progress, open their world', () => {
    const { onSelectCategory } = renderModules();
    expect(screen.getByRole('heading', { name: 'Five worlds' })).toBeInTheDocument();
    const doors = screen.getAllByRole('button', { name: /^Open (Mind|Growth|Learn|Decode|Exam): \d+ of \d+ done$/ });
    expect(doors).toHaveLength(5);
    expect(screen.getByText('01 · The Architecture')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /^Open Mind:/ }));
    expect(onSelectCategory).toHaveBeenCalledWith('architecture-mindset');
  });

  test('on a laptop search is a field in the bar and finds modules and sections', () => {
    renderModules();
    fireEvent.change(screen.getByRole('searchbox', { name: 'Search all your modules and sections' }), { target: { value: 'recall' } });
    expect(screen.getByRole('status')).toHaveTextContent(/matching module/);
  });

  test('on a phone search opens from the bar', () => {
    device.phone = true;
    renderModules();
    expect(screen.queryByRole('searchbox')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Search modules and sections' }));
    expect(screen.getByRole('searchbox', { name: 'Search all your modules and sections' })).toBeInTheDocument();
  });

  test('on a phone Find a starting point rises in a sheet, each need opening its three lessons', () => {
    device.phone = true;
    const { onSelectModule } = renderModules();
    fireEvent.click(screen.getByRole('button', { name: /Find a starting point/ }));
    const sheet = screen.getByRole('dialog', { name: 'Find a starting point' });
    fireEvent.click(within(sheet).getByRole('button', { name: /I forget what I study/ }));
    fireEvent.click(within(sheet).getByRole('button', { name: /Mastering Active Recall/ }));
    expect(onSelectModule).toHaveBeenCalledWith('mastering-active-recall-protocol');
  });

  test('the Notebook opens over the page', () => {
    renderModules();
    fireEvent.click(screen.getByRole('button', { name: /Notebook/ }));
    expect(screen.getByRole('dialog', { name: 'Your notebook' })).toBeInTheDocument();
  });
});

describe('A module world', () => {
  const learn = senior.filter(course => course.category === 'learning-cheat-codes');
  const worldProgress: UserProgress = Object.fromEntries([
    ...learn.slice(0, 2).map(course => [course.id, { unlockedSection: course.sectionsCount }]),
    [learn[2].id, { unlockedSection: 1 }],
  ]) as UserProgress;

  test('it opens on the module to read next, with one Continue that goes straight to the student\'s step', () => {
    clearModuleResumeRequest(learn[2].id);
    const onSelectCourse = vi.fn();
    render(<ModuleShowcase courses={learn} categoryTitle="Learn" categoryId="learning-cheat-codes" userProgress={worldProgress} onSelectCourse={onSelectCourse} />);
    const card = screen.getByRole('region', { name: `Up next: ${learn[2].title}` });
    expect(within(card).getByText('Up next · Module 03')).toBeInTheDocument();
    fireEvent.click(within(card).getByRole('button', { name: 'Continue' }));
    expect(onSelectCourse).toHaveBeenCalledWith(learn[2].id);
    expect(requestedModuleResume(learn[2].id)).toBe(true);
  });

  test('the rest are boxes you press, and the finished ones fold into one row that opens in place', () => {
    const onSelectCourse = vi.fn();
    render(<ModuleShowcase courses={learn} categoryTitle="Learn" categoryId="learning-cheat-codes" userProgress={worldProgress} onSelectCourse={onSelectCourse} />);
    expect(screen.getByRole('heading', { name: 'Still to read' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: new RegExp(learn[3].title) }));
    expect(onSelectCourse).toHaveBeenCalledWith(learn[3].id);
    const fold = screen.getByRole('button', { name: /2 modules finished/ });
    expect(fold).toHaveAttribute('aria-expanded', 'false');
    expect(screen.queryByRole('button', { name: new RegExp(`^01 ${learn[0].title}`) })).not.toBeInTheDocument();
    fireEvent.click(fold);
    expect(fold).toHaveAttribute('aria-expanded', 'true');
    fireEvent.click(screen.getByRole('button', { name: new RegExp(`^01 ${learn[0].title}`) }));
    expect(onSelectCourse).toHaveBeenCalledWith(learn[0].id);
  });

  test('on a laptop the module to read next keeps What’s in this module and its topics', () => {
    render(<ModuleShowcase courses={learn} categoryTitle="Learn" categoryId="learning-cheat-codes" userProgress={worldProgress} onSelectCourse={vi.fn()} />);
    expect(screen.getByText(/^Topics · /)).toBeInTheDocument();
    const whats = screen.getByRole('button', { name: 'What’s in this module' });
    fireEvent.click(whats);
    expect(screen.getByRole('list', { name: `What’s in ${learn[2].title}` })).toBeInTheDocument();
  });

  test('the world page has one Back, which leaves to where the student came from', () => {
    const onBack = vi.fn();
    render(<ModuleWorldScreen onBack={onBack} courses={learn} categoryTitle="Learn" categoryId="learning-cheat-codes" userProgress={worldProgress} onSelectCourse={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Back to Modules' }));
    expect(onBack).toHaveBeenCalledOnce();
    expect(screen.getAllByRole('button', { name: /Back/ })).toHaveLength(1);
  });
});
