/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "I would like to see the points bars where I'm currently at and what my goal
 * points are" (student feedback, 12 Oct 2026).
 */
import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, test, vi } from 'vitest';
import KobraScope from '@/components/approved-ui-runtime';
import { caoGapLabel, caoGoalStanding } from '@/components/dashboard/progress/caoGoal';
import { ProgressPointsGoal } from '@/components/dashboard/progress/ProgressPointsGoal';
import type { StudentSubjectProfile } from '@/components/subjectData';
import type { UnifiedMockResult } from '@/types';

const UPDATED = '2026-09-01T12:00:00.000Z';
const profile = (overrides: Partial<StudentSubjectProfile> = {}): StudentSubjectProfile => ({
  subjects: [
    { subjectName: 'English', level: 'higher', currentGrade: 'H3', targetGrade: 'H2' },
    { subjectName: 'Irish', level: 'higher', currentGrade: 'H4', targetGrade: 'H3' },
    { subjectName: 'Mathematics', level: 'higher', currentGrade: 'H4', targetGrade: 'H2' },
    { subjectName: 'Biology', level: 'higher', currentGrade: 'H3', targetGrade: 'H1' },
    { subjectName: 'Chemistry', level: 'higher', currentGrade: 'H5', targetGrade: 'H3' },
    { subjectName: 'French', level: 'ordinary', currentGrade: 'O2', targetGrade: 'O1' },
    { subjectName: 'Geography', level: 'higher', currentGrade: 'H4', targetGrade: 'H2' },
  ],
  examStartDate: '2027-06-02', restDays: [], yearGroup: '6th', createdAt: UPDATED, updatedAt: UPDATED,
  ...overrides,
});
const mock = (date: string, entries: [string, string][]): UnifiedMockResult => ({
  id: date, label: 'Christmas mocks', date, timestamp: Date.parse(`${date}T15:00:00Z`), totalPoints: 0, resultKind: 'full',
  entries: entries.map(([subjectName, grade]) => ({ subjectName, grade, level: grade.startsWith('H') ? 'higher' : 'ordinary' })),
});

describe('CAO points against the student\'s goal', () => {
  test('best six from the grades they gave us, with the Higher Maths bonus', () => {
    // Now: Maths 66+25, English 77, Biology 77, Irish 66, Geography 66, Chemistry 56 (French 46 dropped).
    // Goal: Maths 88+25, Biology 100, English 88, Geography 88, Irish 77, Chemistry 77 (French 56 dropped).
    expect(caoGoalStanding(profile())).toEqual({
      status: 'ready', current: 433, goal: 543, gap: 110, evidence: { fromMocks: 0, fromProfile: 7, latestMockLabel: undefined },
    });
  });

  test('a mock newer than their grades is the better evidence; an older one is not', () => {
    const newer = mock('2026-10-10', [['Biology', 'H1'], ['Chemistry', 'H3']]);
    const older = mock('2026-08-01', [['Biology', 'H8'], ['Chemistry', 'H8']]);
    const standing = caoGoalStanding(profile(), [older, newer]);
    expect(standing).toMatchObject({ status: 'ready', current: 477, goal: 543, evidence: { fromMocks: 2, fromProfile: 5, latestMockLabel: 'Christmas mocks' } });
    expect(caoGoalStanding(profile(), [older])).toMatchObject({ current: 433 });
  });

  test('no target grades yet invites a goal instead of inventing one', () => {
    const subjects = profile().subjects.map(({ targetGrade: _t, ...subject }) => subject);
    expect(caoGoalStanding(profile({ subjects }))).toEqual({ status: 'no-goal' });
  });

  test('a goal with no current evidence asks for a result', () => {
    const subjects = profile().subjects.map(({ currentGrade: _c, ...subject }) => subject);
    expect(caoGoalStanding(profile({ subjects }))).toEqual({ status: 'no-current', goal: 543 });
  });

  test('Junior Cycle, LCA and missing profiles have no CAO points, so nothing shows', () => {
    expect(caoGoalStanding(null)).toEqual({ status: 'hidden' });
    expect(caoGoalStanding(profile(), [], 'junior')).toEqual({ status: 'hidden' });
    expect(caoGoalStanding(profile({ yearGroup: 'LCA2', subjects: [{ subjectName: 'Social Education', level: 'common' }] }))).toEqual({ status: 'hidden' });
  });

  test('the gap is always said in words', () => {
    expect(caoGapLabel(62)).toBe('62 points to go');
    expect(caoGapLabel(1)).toBe('1 point to go');
    expect(caoGapLabel(0)).toBe('Right on your goal');
    expect(caoGapLabel(-12)).toBe('12 points above your goal');
  });

  test('the bar reads the numbers aloud and its buttons go where grades and mocks live', () => {
    const onEditGrades = vi.fn(), onAddMockResult = vi.fn();
    render(<KobraScope sound={false}><ProgressPointsGoal standing={caoGoalStanding(profile())} onEditGrades={onEditGrades} onAddMockResult={onAddMockResult} /></KobraScope>);
    expect(screen.getByRole('img', { name: '433 points now, goal 543 points, out of 625. 110 points to go.' })).toBeTruthy();
    expect(screen.getByText('110 points to go')).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: 'Add a mock result' }));
    fireEvent.click(screen.getByRole('button', { name: 'Update your grades' }));
    expect(onAddMockResult).toHaveBeenCalledTimes(1);
    expect(onEditGrades).toHaveBeenCalledTimes(1);
  });

  test('without a goal the student is sent to set target grades', () => {
    const onEditGrades = vi.fn();
    render(<KobraScope sound={false}><ProgressPointsGoal standing={{ status: 'no-goal' }} onEditGrades={onEditGrades} /></KobraScope>);
    fireEvent.click(screen.getByRole('button', { name: 'Set your target grades' }));
    expect(onEditGrades).toHaveBeenCalled();
  });
});
