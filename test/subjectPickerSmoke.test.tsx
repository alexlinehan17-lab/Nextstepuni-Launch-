/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Subject-library navigation with real content and mocked persistence.
 * Checks the profile default, searchable full picker, topic filtering and
 * explicit transition from subject choice to focused practice.
 */
import { describe, test, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';

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

// The library opens at the student's subject; all other subjects remain searchable.
describe('Catch-Up Lane subject picker', () => {
  test('opens on a matching student subject and its lessons', () => {
    render(<CatchUpLane uid="u1" studentSubjects={['Biology']} studentCycle="leaving-cert" />);
    expect(screen.getByRole('button', {name:'Choose a subject'})).toHaveTextContent('Biology');
    expect(screen.getAllByRole('button', {name:/Start lesson/}).length).toBeGreaterThan(0);
    expect(screen.getByRole('combobox', {name:'Catch-Up level'})).toHaveValue('higher');
  });
  test('can search and choose another available subject', async () => {
    render(<CatchUpLane uid="u1" studentSubjects={['Biology']} studentCycle="leaving-cert" />);
    fireEvent.click(screen.getByRole('button', {name:'Choose a subject'}));
    fireEvent.change(screen.getByRole('searchbox', {name:'Search subjects'}), {target:{value:'Chemistry'}});
    fireEvent.click(screen.getByRole('button', {name:/^Chemistry/}));
    expect(screen.getByRole('button', {name:'Choose a subject'})).toHaveTextContent('Chemistry');
    await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
  });
  test('keeps all available subjects accessible without a profile', () => {
    render(<CatchUpLane uid="u1" studentCycle="leaving-cert" />);
    fireEvent.click(screen.getByRole('button', {name:'Choose a subject'}));
    expect(screen.getByRole('button', {name:/^Biology/})).toBeInTheDocument();
    expect(screen.getByRole('button', {name:/^Chemistry/})).toBeInTheDocument();
  });
  test('searches the topic list and opens a real lesson', () => {
    render(<CatchUpLane uid="u1" studentSubjects={['Biology']} studentCycle="leaving-cert" />);
    const search = screen.getByRole('searchbox', {name:'Find the topic you missed'});
    fireEvent.change(search, {target:{value:'zzzznotatopic'}});
    expect(screen.queryByRole('button', {name:/Start lesson/})).not.toBeInTheDocument();
    fireEvent.change(search, {target:{value:''}});
    fireEvent.click(screen.getAllByRole('button', {name:/Start lesson/})[0]);
    expect(screen.queryByRole('searchbox', {name:'Find the topic you missed'})).not.toBeInTheDocument();
    expect(screen.getByRole('button', {name:/The one move/})).toBeInTheDocument();
  });
});

describe('Command-Word Reflex subject picker', () => {
  test('selects a student subject without starting practice prematurely', () => {
    render(<CommandWordReflex uid="u1" studentSubjects={['Biology']} studentCycle="leaving-cert" />);
    expect(screen.getByRole('button', {name:/^Biology/})).toHaveAttribute('aria-pressed','true');
    expect(screen.getByRole('button', {name:'Start practising'})).toBeEnabled();
    expect(screen.queryByText(/Tap the command word/i)).not.toBeInTheDocument();
  });
  test('allows a subject outside the student profile through the full picker', () => {
    render(<CommandWordReflex uid="u1" studentSubjects={['Biology']} studentCycle="leaving-cert" />);
    fireEvent.click(screen.getByRole('button', {name:'All subjects'}));
    fireEvent.change(screen.getByRole('searchbox', {name:'Search subjects'}), {target:{value:'Chemistry'}});
    fireEvent.click(screen.getByRole('button', {name:/^Chemistry/}));
    expect(screen.getByRole('button', {name:'All subjects'})).toHaveTextContent('Chemistry');
    fireEvent.click(screen.getByRole('button', {name:'Start practising'}));
    expect(screen.getByText(/Tap the command word/i)).toBeInTheDocument();
  });
  test('keeps the full subject picker available without a profile', () => {
    render(<CommandWordReflex uid="u1" studentCycle="leaving-cert" />);
    fireEvent.click(screen.getByRole('button', {name:'All subjects'}));
    expect(screen.getByRole('dialog', {name:'All subjects'})).toBeInTheDocument();
    expect(screen.getAllByRole('button', {name:/^Biology/}).length).toBeGreaterThan(0);
    expect(screen.getAllByRole('button', {name:/^Chemistry/}).length).toBeGreaterThan(0);
  });
  test('starts the selected subject in the focused practice screen', () => {
    render(<CommandWordReflex uid="u1" studentSubjects={['Biology']} studentCycle="leaving-cert" />);
    fireEvent.click(screen.getByRole('button', {name:'Start practising'}));
    expect(screen.getByText(/Tap the command word/i)).toBeInTheDocument();
    expect(screen.queryByRole('heading', {name:'Choose your subject'})).not.toBeInTheDocument();
  });
});
