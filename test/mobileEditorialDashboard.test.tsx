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
  const section = screen.getByRole('combobox', { name: 'Progress section' });
  expect(within(section).getAllByRole('option')).toHaveLength(5);
  fireEvent.change(screen.getByRole('combobox', { name: 'Filter by subject' }), { target: { value: 'Irish' } });
  fireEvent.click(screen.getByRole('tab', { name: 'Month' }));
  fireEvent.change(section, { target: { value: 'confidence' } });
  expect(screen.getByRole('combobox', { name: 'Filter by subject' })).toHaveValue('Irish');
  expect(screen.getByRole('tab', { name: 'Month' })).toHaveAttribute('aria-selected', 'true');
  expect(screen.getByRole('heading', { name: 'Topic readiness' })).toBeInTheDocument();
  fireEvent.change(section, { target: { value: 'milestones' } });
  expect(screen.queryByRole('tablist', { name: 'Dashboard time range' })).not.toBeInTheDocument();
  expect(screen.queryByRole('combobox', { name: 'Filter by subject' })).not.toBeInTheDocument();
  fireEvent.change(section, { target: { value: 'study' } });
  expect(screen.getByRole('combobox', { name: 'Filter by subject' })).toHaveValue('Irish');
});
test('all seven subjects remain visible and full mocks retain their all-subject evidence', () => {
  const { container } = show();
  fireEvent.change(screen.getByRole('combobox', { name: 'Progress section' }), { target: { value: 'confidence' } });
  expect(container.querySelectorAll('.confidence-subject')).toHaveLength(7);
  fireEvent.change(screen.getByRole('combobox', { name: 'Filter by subject' }), { target: { value: 'Irish' } });
  fireEvent.change(screen.getByRole('combobox', { name: 'Progress section' }), { target: { value: 'practice' } });
  expect(screen.getByText(/Full mock totals stay all-subject/)).toBeInTheDocument();
  expect(container.querySelectorAll('.dashboard-mock-record')).toHaveLength(3);
  for (const record of container.querySelectorAll('.dashboard-mock-record')) {
    expect(record.textContent).toContain('Mathematics');
    expect(record.textContent).toContain('Irish');
  }
});
