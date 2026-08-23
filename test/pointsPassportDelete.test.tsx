/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { fireEvent, render, screen } from '@testing-library/react';
import { beforeEach, describe, expect, test, vi } from 'vitest';
import PointsPassport from '@/components/PointsPassport';
import type { StudentSubjectProfile } from '@/components/subjectData';
import { DEMO_STUDENT_UID } from '@/data/devStudent';

const mocks = vi.hoisted(() => ({
  removeMockResult: vi.fn(),
  showToast: vi.fn(),
}));

vi.mock('@/components/Toast', () => ({
  useToast: () => ({ showToast: mocks.showToast }),
}));

vi.mock('@/contexts/ProgressContext', () => ({
  useProgress: () => ({ rawProgressDoc: {} }),
}));

vi.mock('@/contexts/InnovationDataContext', () => ({
  useInnovationData: () => ({
    mockResults: {
      isLoaded: true,
      mocks: [{
        id: 'mock-1',
        label: 'February Mocks',
        date: '2026-02-12',
        entries: [{ subjectName: 'Mathematics', grade: 'H4', level: 'higher' }],
        totalPoints: 320,
        timestamp: 1,
      }],
      addMockResult: vi.fn(),
      removeMockResult: mocks.removeMockResult,
    },
  }),
}));

const profile: StudentSubjectProfile = {
  subjects: [{
    subjectName: 'Mathematics',
    level: 'higher',
    currentGrade: 'H4',
    targetGrade: 'H2',
  }],
  examStartDate: '2027-06-09',
  restDays: [],
  createdAt: '2026-08-23T00:00:00.000Z',
  updatedAt: '2026-08-23T00:00:00.000Z',
};

describe('Points Passport mock deletion', () => {
  beforeEach(() => {
    mocks.removeMockResult.mockReset();
    mocks.showToast.mockReset();
  });

  test('requires confirmation and names the result being removed', () => {
    render(<PointsPassport uid={DEMO_STUDENT_UID} profile={profile} initialTab="mocks" />);

    fireEvent.click(screen.getByRole('button', { name: 'Remove February Mocks' }));
    expect(mocks.removeMockResult).not.toHaveBeenCalled();
    expect(screen.getByRole('dialog', { name: 'Remove this mock result?' })).toHaveTextContent('February Mocks');

    fireEvent.click(screen.getByRole('button', { name: 'Remove result' }));
    expect(mocks.removeMockResult).toHaveBeenCalledWith('mock-1');
    expect(mocks.showToast).toHaveBeenCalledWith('February Mocks removed', 'success');
  });
});
