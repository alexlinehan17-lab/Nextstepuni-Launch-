/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React from 'react';
import { describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';

const topicMastery = vi.hoisted(() => ({
  mastery: {},
  importSyllabusTopics: vi.fn(),
  getSubjectTopics: vi.fn(() => []),
  getCanonicalSubjectTopics: vi.fn(() => []),
  getTopicConfidence: vi.fn(() => 'not-started'),
  setTopicConfidence: vi.fn(),
}));

vi.mock('@/contexts/InnovationDataContext', () => ({
  useInnovationData: () => ({
    topicMastery,
    mockResults: {
      mocks: [],
      addMockResult: vi.fn(),
      removeMockResult: vi.fn(),
    },
    futureFinderPicks: [{
      id: 'target-course',
      title: 'Computer Science',
      institution: 'University College Dublin',
      typicalPoints: 500,
    }],
  }),
}));

import WarRoom from '@/components/WarRoom';
import { createDevStudentProfile } from '@/data/devStudent';

describe('War Room operational workspace', () => {
  test('opens on Briefing and supports keyboard navigation between product views', async () => {
    render(
      <WarRoom
        uid=""
        profile={createDevStudentProfile(new Date('2026-08-09T12:00:00.000Z'))}
        timetableCompletions={{}}
      />,
    );

    expect(await screen.findByRole('heading', { name: 'What needs attention now' })).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: 'Briefing' })).toHaveAttribute('aria-selected', 'true');
    expect(screen.getByRole('heading', { name: 'Exam runway' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Points position' })).toBeInTheDocument();
    expect(screen.getByText('Days to exams')).toBeInTheDocument();
    expect(screen.getByText('Start here')).toBeInTheDocument();
    expect(screen.queryByText('Highest impact')).not.toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Ranked next priorities' })).toBeInTheDocument();

    const briefingTab = screen.getByRole('tab', { name: 'Briefing' });
    briefingTab.focus();
    fireEvent.keyDown(briefingTab, { key: 'ArrowRight' });

    expect(await screen.findByRole('heading', { name: 'Coverage and confidence' })).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: 'Subjects' })).toHaveAttribute('aria-selected', 'true');

    fireEvent.click(screen.getByRole('tab', { name: 'Time plan' }));
    expect(await screen.findByRole('heading', { name: 'Where the time goes' })).toBeInTheDocument();
    expect(screen.queryByText('Strategy Briefing')).not.toBeInTheDocument();
  });
});
