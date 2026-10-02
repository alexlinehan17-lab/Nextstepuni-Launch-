import React from 'react';
import { afterEach, beforeEach, expect, test, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import DashboardView from '../components/DashboardView';
import { createDemoStudentLoadedData } from '../data/devStudent';
import { ALL_COURSES } from '../courseData';
vi.mock('../hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => true }));
vi.mock('../components/MountainLandscape', () => ({ default: () => <div>Programme mountains</div> }));
beforeEach(() => { vi.useFakeTimers(); vi.setSystemTime(new Date(2026, 8, 20, 12)); });
afterEach(() => { cleanup(); vi.useRealTimers(); });
function chooseSubject(subject: string) {
  fireEvent.click(screen.getByRole('button', { name: 'Filter by subject' }));
  fireEvent.click(within(screen.getByRole('group', { name: 'Filter by subject' })).getByRole('checkbox', { name: subject }));
  fireEvent.click(screen.getByRole('button', { name: 'Filter by subject' }));
}

function chooseSection(label: string) {
  fireEvent.click(screen.getByRole('button', { name: 'Progress section' }));
  fireEvent.click(screen.getByRole('option', { name: new RegExp(label) }));
}
function show() {
  const demo = createDemoStudentLoadedData(new Date());
  return render(<DashboardView userProgress={demo.userProgress} allCourses={ALL_COURSES} categoryTitles={{} as never}
    streak={{ currentStreak: 18, longestStreak: 42, lastActiveDate: '2026-09-20' }} recommendation={null}
    onSelectModule={vi.fn()} onBack={vi.fn()} pointsEarned={6240} studentProfile={demo.studentProfile}
    studySessions={demo.rawProgressDoc.studySessions} studyDebriefs={demo.rawProgressDoc.studyDebriefs}
    studyReflections={demo.rawProgressDoc.reflections} topicMastery={demo.rawProgressDoc.topicMasteryV2}
    mockResults={demo.rawProgressDoc.unifiedMockResults} />);
}
test('section changes preserve subject and range; milestones removes period controls', () => {
  show();
  const section = screen.getByRole('button', { name: 'Progress section' });
  fireEvent.click(section);
  expect(within(screen.getByRole('listbox', { name: 'Progress sections' })).getAllByRole('option')).toHaveLength(5);
  fireEvent.keyDown(screen.getByRole('listbox'), { key: 'Escape' });
  chooseSubject('Irish');
  fireEvent.click(screen.getByRole('tab', { name: 'Month' }));
  chooseSection('Confidence');
  expect(screen.getByRole('button', { name: 'Filter by subject' })).toHaveTextContent('Irish');
  expect(screen.getByRole('tab', { name: 'Month' })).toHaveAttribute('aria-selected', 'true');
  expect(screen.getByRole('heading', { name: 'Topic readiness' })).toBeInTheDocument();
  chooseSection('Milestones');
  expect(screen.queryByRole('tablist', { name: 'Dashboard time range' })).not.toBeInTheDocument();
  expect(screen.queryByRole('button', { name: 'Filter by subject' })).not.toBeInTheDocument();
  chooseSection('Study');
  expect(screen.getByRole('button', { name: 'Filter by subject' })).toHaveTextContent('Irish');
});
test('all seven subjects remain visible and full mocks retain their all-subject evidence', () => {
  const { container } = show();
  chooseSection('Confidence');
  expect(within(screen.getByRole('group', { name: 'Subjects to compare' })).getAllByRole('checkbox')).toHaveLength(7);
  fireEvent.click(screen.getByRole('tab', { name: 'By subject' }));
  expect(container.querySelectorAll('.pr-confidence-grid > article')).toHaveLength(7);
  chooseSubject('Irish');
  chooseSection('Practice');
  expect(screen.getByText(/Full mock totals stay all-subject/)).toBeInTheDocument();
  fireEvent.click(screen.getByRole('tab', { name: 'The record' }));
  expect(container.querySelectorAll('.dashboard-mock-record')).toHaveLength(3);
  for (const record of container.querySelectorAll('.dashboard-mock-record')) {
    expect(record.textContent).toContain('Mathematics');
    expect(record.textContent).toContain('Irish');
  }
});

test('section menu supports keyboard selection and escape, and the programme belongs only to Overview', () => {
  show();
  const trigger = screen.getByRole('button', { name: 'Progress section' });
  fireEvent.keyDown(trigger, { key: 'ArrowDown' });
  expect(screen.getByRole('option', { name: /Overview/ })).toHaveFocus();
  fireEvent.keyDown(screen.getByRole('listbox'), { key: 'End' });
  expect(screen.getByRole('option', { name: /Milestones/ })).toHaveFocus();
  fireEvent.keyDown(screen.getByRole('listbox'), { key: 'Escape' });
  expect(trigger).toHaveFocus();
  expect(trigger).toHaveAttribute('aria-expanded', 'false');
  expect(screen.getByText('Five climbs, all your own.')).toBeInTheDocument();
  chooseSection('Confidence');
  expect(screen.queryByText('Five climbs, all your own.')).not.toBeInTheDocument();
});
