/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React from 'react';
import { describe, expect, test, vi } from 'vitest';
import { render, screen, within } from '@testing-library/react';

const navigation = vi.hoisted(() => ({
  setActiveTool: vi.fn(),
  goBack: vi.fn(),
}));

vi.mock('@/contexts/NavigationContext', () => ({
  useNavigation: () => ({
    state: { activeTool: null },
    setActiveTool: navigation.setActiveTool,
    goBack: navigation.goBack,
  }),
}));

vi.mock('@/hooks/useTopicMastery', () => ({
  useTopicMastery: () => ({ mastery: {} }),
}));

vi.mock('@/components/gc/gcNotifications', () => ({
  getNotifications: () => Promise.resolve([]),
}));

import InnovationZone from '@/components/InnovationZone';
import { createDevStudentProfile, createDevStudentSession } from '@/data/devStudent';

describe('dev student Launchpad profile handoff', () => {
  test('unlocks profile-gated tools before the unauthenticated Firestore refresh settles', () => {
    render(
      <InnovationZone
        onBack={vi.fn()}
        user={createDevStudentSession()}
        initialSubjectProfile={createDevStudentProfile(new Date('2026-08-09T12:00:00.000Z'))}
        settings={{ language: 'en', avatar: '', darkMode: false, cardStyle: 'default', defaultWorkMinutes: 25 }}
        updateSetting={vi.fn()}
      />,
    );

    const title = screen.getByRole('heading', { name: 'Spaced Repetition Timetable' });
    const card = title.closest('.cursor-pointer');
    expect(card).not.toBeNull();
    expect(within(card as HTMLElement).getByText('Launch tool')).toBeInTheDocument();
    expect(within(card as HTMLElement).queryByText('Needs Profile')).not.toBeInTheDocument();
  });
});
