/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 7a: Points Passport in the agreed look keeps its arithmetic. The same grades give the same
 * total as the points engine ("465 / 625" on one sheet), the five parts open from one menu, and What
 * if? moves the pinned number when a grade is tapped.
 */
import React from 'react';
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, describe, expect, test, vi } from 'vitest';
import PointsPassport from '@/components/PointsPassport';
import type { StudentSubjectProfile } from '@/components/subjectData';
import { computeBestSixBreakdown } from '@/components/pointsScenarioStore';
import { DEMO_STUDENT_UID } from '@/data/devStudent';

vi.mock('@/components/Toast', () => ({ useToast: () => ({ showToast: vi.fn() }) }));
vi.mock('@/contexts/ProgressContext', () => ({ useProgress: () => ({ rawProgressDoc: {}, updateDemoProgress: vi.fn() }) }));
vi.mock('@/contexts/InnovationDataContext', () => ({
  useInnovationData: () => ({
    mockResults: { isLoaded: true, mocks: [], addMockResult: vi.fn(), removeMockResult: vi.fn() },
    futureFinderPicks: [],
  }),
}));
afterEach(cleanup);

const profile: StudentSubjectProfile = {
  subjects: [
    { subjectName: 'Mathematics', level: 'higher', currentGrade: 'H4', targetGrade: 'H2' },
    { subjectName: 'English', level: 'higher', currentGrade: 'H3', targetGrade: 'H2' },
    { subjectName: 'Irish', level: 'higher', currentGrade: 'H4', targetGrade: 'H3' },
    { subjectName: 'Geography', level: 'higher', currentGrade: 'H3', targetGrade: 'H2' },
    { subjectName: 'Accounting', level: 'higher', currentGrade: 'H3', targetGrade: 'H2' },
    { subjectName: 'French', level: 'ordinary', currentGrade: 'O2', targetGrade: 'O1' },
    { subjectName: 'Biology', level: 'higher', currentGrade: 'H5', targetGrade: 'H4' },
  ],
  examStartDate: '2027-06-09', restDays: [], createdAt: '2026-08-23T00:00:00.000Z', updatedAt: '2026-08-23T00:00:00.000Z',
} as StudentSubjectProfile;

describe('Points Passport', () => {
  test('the total for these grades is the points engine\'s, written "N / 625" on one sheet', () => {
    const expected = computeBestSixBreakdown(profile.subjects.map(s => ({ subjectName: s.subjectName, grade: s.currentGrade!, level: s.level }))).total;
    render(<PointsPassport uid={DEMO_STUDENT_UID} profile={profile} />);
    const sheet = screen.getByRole('region', { name: 'Your points' });
    expect(within(sheet).getByText(String(expected))).toBeInTheDocument();
    expect(sheet.querySelector('.pp7-total')?.textContent).toBe(`${expected} / 625`);
  });

  test('the five parts open from one menu', async () => {
    render(<PointsPassport uid={DEMO_STUDENT_UID} profile={profile} />);
    const menu = screen.getByRole('button', { name: /Points Passport sections/ });
    expect(menu).toHaveTextContent('My subjects');
    expect(menu).toHaveTextContent('1 of 5');
    for (const [part, shows] of [['Scenarios', 'Scenario runway'], ['Mock Tracker', 'Record mock results'], ['Best Moves', 'Best points bargains'], ['What if?', 'Tap a grade to try it'], ['My subjects', 'Your subject contributions']] as const) {
      fireEvent.click(screen.getByRole('button', { name: /Points Passport sections/ }));
      fireEvent.click(await screen.findByRole('menuitemradio', { name: part }));
      expect(await screen.findByText(shows)).toBeInTheDocument();
    }
  });

  test('What if?: tapping a grade moves the pinned number and keeps today\'s grade marked', async () => {
    render(<PointsPassport uid={DEMO_STUDENT_UID} profile={profile} initialTab="planner" />);
    const before = computeBestSixBreakdown(profile.subjects.map(s => ({ subjectName: s.subjectName, grade: s.currentGrade!, level: s.level }))).total;
    const pinned = await screen.findByText('What if');
    const panel = pinned.closest('.pp7-wi') as HTMLElement;
    expect(panel.querySelector('.pp7-total')?.textContent).toBe(`${before} / 625`);
    fireEvent.click(screen.getByRole('radio', { name: 'Biology H1' }));
    const after = computeBestSixBreakdown(profile.subjects.map(s => ({ subjectName: s.subjectName, grade: s.subjectName === 'Biology' ? 'H1' : s.currentGrade!, level: s.level }))).total;
    expect(panel.querySelector('.pp7-total')?.textContent).toBe(`${after} / 625`);
    expect(screen.getByRole('radio', { name: 'Biology H1' })).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByRole('radio', { name: 'Biology H5' }).querySelector('.ui-ruler-dot')).not.toBeNull();
  });
});
