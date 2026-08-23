/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, test, vi } from 'vitest';
import { DEMO_STUDENT_UID } from '@/data/devStudent';
import { ProgressProvider, useProgress } from '@/contexts/ProgressContext';

const fixtures = vi.hoisted(() => {
  const demoProfile = {
    subjects: [],
    examStartDate: '2027-06-09',
    restDays: ['Saturday'],
    createdAt: '2026-08-23T00:00:00.000Z',
    updatedAt: '2026-08-23T00:00:00.000Z',
  };
  return {
    demoProfile,
    loadedData: {
      userProgress: {},
      northStar: null,
      studentProfile: demoProfile,
      needsOnboarding: false,
      unlockedAvatarSeeds: [],
      unlockedThemes: [],
      unlockedCardStyles: [],
      dismissedGuides: {},
      timetableCompletions: {},
      rawProgressDoc: {
        subjectProfile: demoProfile,
        pointsData: { totalEarned: 100, totalSpent: 0 },
      },
    },
  };
});

vi.mock('@/contexts/AuthContext', () => ({
  useAuth: () => ({
    user: { uid: DEMO_STUDENT_UID, name: 'Demo Student', avatar: 'Charlie' },
    isLoadingAuth: false,
    loadedData: fixtures.loadedData,
    loadedDataUid: DEMO_STUDENT_UID,
    loadedDataStatus: 'loaded',
  }),
}));

const renderSnapshots: string[] = [];

const DemoProgressProbe: React.FC = () => {
  const { pointsData, studentProfile, updateDemoProgress } = useProgress();
  const snapshot = `${pointsData.balance}|${studentProfile?.restDays.join(',') ?? ''}`;
  renderSnapshots.push(snapshot);
  return (
    <>
      <span>{snapshot}</span>
      <button
        type="button"
        onClick={() => updateDemoProgress(current => ({
          ...current,
          pointsData: { totalEarned: 150, totalSpent: 0 },
          subjectProfile: {
            ...fixtures.demoProfile,
            restDays: ['Sunday'],
          },
        }))}
      >
        Update demo
      </button>
    </>
  );
};

describe('ProgressContext Demo Account updates', () => {
  beforeEach(() => {
    localStorage.clear();
    renderSnapshots.length = 0;
  });

  test('updates raw points and convenience profile state in the same render batch', async () => {
    render(<ProgressProvider><DemoProgressProbe /></ProgressProvider>);
    await waitFor(() => expect(screen.getByText('100|Saturday')).toBeInTheDocument());
    const beforeUpdate = renderSnapshots.length;

    fireEvent.click(screen.getByRole('button', { name: 'Update demo' }));
    await waitFor(() => expect(screen.getByText('150|Sunday')).toBeInTheDocument());

    expect(renderSnapshots.slice(beforeUpdate)).not.toContain('150|Saturday');
  });
});
