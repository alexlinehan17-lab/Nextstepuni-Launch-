import React from 'react';
import { afterEach, beforeEach, expect, test, vi } from 'vitest';
import { act, cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import DashboardView from '../components/DashboardView';
import { createDemoStudentLoadedData } from '../data/devStudent';
import { ALL_COURSES } from '../courseData';
vi.mock('../hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => true }));
vi.mock('../components/MountainLandscape', () => ({ default: () => <div>Programme mountains</div> }));
// Only the date is fixed: the shared menu's own timers run (it opens and closes as on a phone).
beforeEach(() => { vi.useFakeTimers({ toFake: ['Date'] }); vi.setSystemTime(new Date(2026, 8, 20, 12)); });
afterEach(() => { cleanup(); vi.useRealTimers(); });
/** One tap as WebKit on iOS delivers it (see test/sharedPartsMenu.test.tsx): the agreed
 *  menus (the shared Menu) open and choose on a tap with nothing focused. */
async function tap(element: Element) {
  const touch = { pointerType: 'touch', pointerId: 1, isPrimary: true, button: 0, buttons: 1, bubbles: true };
  fireEvent.pointerDown(element, touch);
  fireEvent.pointerUp(element, { ...touch, buttons: 0 });
  fireEvent.mouseDown(element, { button: 0 });
  fireEvent.mouseUp(element, { button: 0 });
  fireEvent.click(element, { button: 0, detail: 1 });
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 30)); });
}
const sectionButton = () => screen.getByRole('button', { name: /Progress section/ });
const subjectButton = () => screen.getByRole('button', { name: /Filter by subject/ });
/** One subject at a time, from a short menu with a tick (the agreed board, area-3 checklist). */
async function chooseSubject(subject: string) {
  await tap(subjectButton());
  await tap(await screen.findByRole('menuitemradio', { name: subject }));
}
async function chooseSection(label: string) {
  await tap(sectionButton());
  await tap(await screen.findByRole('menuitemradio', { name: label }));
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
test('section changes preserve subject and range; milestones removes period controls', async () => {
  show();
  expect(sectionButton()).toHaveTextContent(/Overview.*1 of 5/);
  await tap(sectionButton());
  const menu = await screen.findByRole('menu');
  expect(within(menu).getAllByRole('menuitemradio')).toHaveLength(5);
  expect(within(menu).getByRole('menuitemradio', { name: 'Overview' })).toHaveAttribute('aria-checked', 'true');
  await act(async () => { fireEvent.keyDown(menu, { key: 'Escape' }); await new Promise(resolve => setTimeout(resolve, 400)); });
  await chooseSubject('Irish');
  fireEvent.click(screen.getByRole('radio', { name: 'Month' }));
  await chooseSection('Confidence');
  expect(sectionButton()).toHaveTextContent(/Confidence.*3 of 5/);
  expect(subjectButton()).toHaveTextContent('Irish');
  expect(screen.getByRole('radio', { name: 'Month' })).toHaveAttribute('aria-checked', 'true');
  // Topic readiness sits on Practice (and Overview) on the agreed board.
  await chooseSection('Practice');
  expect(screen.getByRole('heading', { name: 'Topic readiness' })).toBeInTheDocument();
  await chooseSection('Milestones');
  expect(screen.queryByRole('radiogroup', { name: 'Dashboard time range' })).not.toBeInTheDocument();
  expect(screen.queryByRole('button', { name: /Filter by subject/ })).not.toBeInTheDocument();
  await chooseSection('Study');
  expect(subjectButton()).toHaveTextContent('Irish');
});
test('all seven subjects remain visible and full mocks retain their all-subject evidence', async () => {
  const { container } = show();
  await chooseSection('Confidence');
  expect(within(screen.getByRole('group', { name: 'Subjects to compare' })).getAllByRole('checkbox')).toHaveLength(7);
  fireEvent.click(screen.getByRole('radio', { name: 'By subject' }));
  expect(container.querySelectorAll('.pr-confidence-grid > article')).toHaveLength(7);
  await chooseSubject('Irish');
  await chooseSection('Practice');
  expect(screen.getByText(/Full mock totals stay all-subject/)).toBeInTheDocument();
  // The record is the first view on the agreed board: one row per sitting, each opening its subjects.
  const records = container.querySelectorAll('.dashboard-mock-record');
  expect(records).toHaveLength(3);
  for (const record of records) {
    fireEvent.click(within(record as HTMLElement).getByRole('button'));
    expect(record.textContent).toContain('Mathematics');
    expect(record.textContent).toContain('Irish');
  }
});

test('the next part is named at the foot, and the programme belongs only to Overview', async () => {
  show();
  expect(screen.getByText('Five climbs, all your own.')).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: /Next · 2 of 5\s*Study/ }));
  expect(sectionButton()).toHaveTextContent(/Study.*2 of 5/);
  expect(screen.queryByText('Five climbs, all your own.')).not.toBeInTheDocument();
  await chooseSection('Confidence');
  expect(screen.queryByText('Five climbs, all your own.')).not.toBeInTheDocument();
  await chooseSection('Milestones');
  expect(screen.queryByRole('button', { name: /^Next/ })).not.toBeInTheDocument();
});
