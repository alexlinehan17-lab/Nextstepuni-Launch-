/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Smoke tests locking the subject-picker behaviour shared by Catch-Up Lane and
 * Command-Word Reflex (and, next, Paper Trail): the My Subjects / All Subjects
 * scope toggle, the cream tile grid, the no-profile fallback (no toggle, all
 * tiles), the coming-soon note, and tile-click navigation into the tool. The
 * persistence hooks + InnovationData context are mocked so the tools render
 * without Firebase, but the real content data modules drive the tiles.
 */
import { describe, test, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';

vi.mock('@/hooks/useCatchUpLane', () => ({
  useCatchUpLane: () => ({
    state: { recoveredTopicIds: [], shakyTopicIds: [], attempts: 0, absences: [], updatedAt: '' },
    isLoaded: true,
    markRecovered: vi.fn(),
    markShaky: vi.fn(),
    logAbsence: vi.fn(),
    saveComeback: vi.fn(),
    setFirstWeekDay: vi.fn(),
    marksProtected: 0,
  }),
}));
vi.mock('@/hooks/useCommandWordReflex', () => ({
  useCommandWordReflex: () => ({
    state: { seenIds: [], firstTryIds: [], wordsMet: [], attempts: 0, updatedAt: '' },
    isLoaded: true,
    recordResult: vi.fn(),
  }),
}));
vi.mock('@/contexts/InnovationDataContext', () => ({
  useInnovationData: () => ({
    topicMastery: { setTopicConfidence: vi.fn() },
  }),
}));

import CatchUpLane from '@/components/CatchUpLane';
import CommandWordReflex from '@/components/CommandWordReflex';

/** Catch-Up Lane opens on a two-arm hub; the picker is behind the content arm. */
const openCatchUpPicker = (props: React.ComponentProps<typeof CatchUpLane>) => {
  render(<CatchUpLane {...props} />);
  fireEvent.click(screen.getByRole('button', { name: /Catch up on what you missed/i }));
};

describe('Catch-Up Lane subject picker', () => {
  test('with matching studentSubjects: toggle visible, only my subjects tiled, coming-soon note shown', () => {
    openCatchUpPicker({ uid: 'u1', studentSubjects: ['Biology', 'Latin'], studentCycle: 'leaving-cert' });
    // Scope toggle is present (student has ≥1 subject with content).
    expect(screen.getByRole('button', { name: 'My Subjects' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'All Subjects' })).toBeInTheDocument();
    // Default scope 'mine': Biology tiled, other-cycle/other subjects not.
    expect(screen.getByRole('button', { name: /^Biology/ })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /^Chemistry/ })).not.toBeInTheDocument();
    // Subjects without content yet get the honest coming-soon note.
    expect(screen.getByText(/More of your subjects are on the way: Latin/i)).toBeInTheDocument();
  });

  test('switching scope to All shows more tiles', () => {
    openCatchUpPicker({ uid: 'u1', studentSubjects: ['Biology'], studentCycle: 'leaving-cert' });
    expect(screen.queryByRole('button', { name: /^Chemistry/ })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'All Subjects' }));
    expect(screen.getByRole('button', { name: /^Biology/ })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^Chemistry/ })).toBeInTheDocument();
  });

  test('with no studentSubjects: no toggle, all tiles shown', () => {
    openCatchUpPicker({ uid: 'u1', studentCycle: 'leaving-cert' });
    expect(screen.queryByRole('button', { name: 'My Subjects' })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'All Subjects' })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^Biology/ })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^Chemistry/ })).toBeInTheDocument();
  });

  test('clicking a tile opens that subject (topic queue)', () => {
    openCatchUpPicker({ uid: 'u1', studentSubjects: ['Biology'], studentCycle: 'leaving-cert' });
    fireEvent.click(screen.getByRole('button', { name: /^Biology/ }));
    expect(screen.getByText(/Tap a topic you missed/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /All subjects/i })).toBeInTheDocument(); // back link
  });
});

describe('Command-Word Reflex subject picker', () => {
  test('with matching studentSubjects: toggle visible, only my subjects tiled, coming-soon note shown', () => {
    render(<CommandWordReflex uid="u1" studentSubjects={['Biology', 'Latin']} studentCycle="leaving-cert" />);
    expect(screen.getByRole('button', { name: 'My Subjects' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'All Subjects' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^Biology/ })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /^Chemistry/ })).not.toBeInTheDocument();
    expect(screen.getByText(/More of your subjects are coming/i)).toBeInTheDocument();
  });

  test('switching scope to All shows more tiles', () => {
    render(<CommandWordReflex uid="u1" studentSubjects={['Biology']} studentCycle="leaving-cert" />);
    expect(screen.queryByRole('button', { name: /^Chemistry/ })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'All Subjects' }));
    expect(screen.getByRole('button', { name: /^Biology/ })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^Chemistry/ })).toBeInTheDocument();
  });

  test('with no studentSubjects: no toggle, all tiles shown', () => {
    render(<CommandWordReflex uid="u1" studentCycle="leaving-cert" />);
    expect(screen.queryByRole('button', { name: 'My Subjects' })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'All Subjects' })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^Biology/ })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^Chemistry/ })).toBeInTheDocument();
  });

  test('clicking a tile opens that subject (play view)', () => {
    render(<CommandWordReflex uid="u1" studentSubjects={['Biology']} studentCycle="leaving-cert" />);
    fireEvent.click(screen.getByRole('button', { name: /^Biology/ }));
    expect(screen.getByText(/Tap the command word/i)).toBeInTheDocument();
  });
});
