/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React from 'react';
import { describe, expect, test, vi } from 'vitest';
import { render, screen, within, fireEvent } from '@testing-library/react';

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

    const card = screen.getByRole('button', { name: 'Open Planner & Study' });
    expect(card).toBeEnabled();
    expect(within(card).getByRole('heading', { name: 'Planner & Study' })).toBeInTheDocument();
    expect(within(card as HTMLElement).queryByText('Needs Profile')).not.toBeInTheDocument();
  });
  test('filters the desktop catalogue by task as well as tool name', () => {
    render(<InnovationZone onBack={vi.fn()} user={createDevStudentSession()} initialSubjectProfile={createDevStudentProfile(new Date('2026-08-09T12:00:00.000Z'))} settings={{language:'en',avatar:'',darkMode:false,cardStyle:'default',defaultWorkMinutes:25}} updateSetting={vi.fn()} />);
    fireEvent.change(screen.getByRole('searchbox', {name:'Find a tool or task'}), {target:{value:'Paper Trail'}});
    expect(screen.getByRole('button', {name:'Open Paper Trail'})).toBeInTheDocument();
    expect(screen.queryByRole('button', {name:'Open Planner & Study'})).not.toBeInTheDocument();
  });

});
