/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The quick check after a saved session: answer first, reveal the scheme, tick
 * what the examiner would have given, and every grade reaches the Mark Bank
 * review deck. Nothing to ask means stepping aside without a word.
 */

import React from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, test, vi } from 'vitest';
import type { SecCard, SecQuestionCard } from '@/types/markBank';
import type * as Deck from '@/components/MarkBank/deck';

const mocks = vi.hoisted(() => ({
  loadCards: vi.fn(async (): Promise<SecCard[]> => []),
  ensureDeck: vi.fn(),
  commitReview: vi.fn(),
  play: vi.fn(),
  setEnabled: vi.fn(),
}));

vi.mock('@/components/MarkBank/deck', async importOriginal => ({
  ...(await importOriginal<typeof Deck>()),
  loadCards: mocks.loadCards,
}));
vi.mock('@/components/MarkBank/store', async () => {
  const { NEW_CARD } = await import('@/components/MarkBank/scheduler');
  const empty = () => ({ v: 1, cards: {}, updatedAt: 0 });
  return {
    readLocal: empty,
    memoryFor: (deck: { cards: Record<string, unknown> }, id: string) => deck.cards[id] ?? NEW_CARD,
    ensureDeck: mocks.ensureDeck,
    commitReview: mocks.commitReview.mockImplementation(empty),
  };
});

vi.mock('@/components/immersiveDeck/useDeckSound', () => ({ useDeckSound: () => ({ play: mocks.play, setEnabled: mocks.setEnabled }) }));
vi.mock('@/components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));
import { CURRICULUM_SPECIFICATIONS } from '@/curriculumRegistry';
import { CARDS as politicsCards } from '@/components/MarkBank/cards/politics-and-society/higher';
import StudySessionQuiz from '@/components/study/quiz/StudySessionQuiz';

const base = {
  source: 'sec' as const, subjectId: 'chemistry', level: 'ordinary' as const, year: 2021, paperFileid: 'LC022GLP000EV',
  section: 'B' as const, specVersion: 'chemistry:2022', conceptId: 'c',
  schemeCitation: 'Marking points quoted from the SEC marking scheme, Chemistry 2021 Ordinary Level — © State Examinations Commission.',
  qa: { gates: [], humanReviewedBy: 'test', humanReviewedAt: '2026-10-23' },
};
const card = (id: string, text: string, rows: SecQuestionCard['rows'], extra: Partial<SecQuestionCard> = {}): SecQuestionCard => ({
  ...base, kind: 'question', id, topicId: 'chem-2-2', questionRef: `2021 OL ${id}`, questionText: text,
  tariffModel: { kind: 'fixed' }, totalMarks: rows.reduce((n, row) => n + (row.marks ?? 0), 0), rows, ...extra,
});

const cards: SecCard[] = [
  card('q1', 'Is ethene planar or tetrahedral?', [{ id: 'q1-r1', kind: 'point', verbatim: 'planar', marks: 6 }]),
  card('q2', 'Name two alkenes.', [{ id: 'q2-r1', kind: 'anyN', verbatim: 'Any two', marks: 6, group: { claimMax: 2, perOption: 3, options: ['ethene', 'propene', 'butene'] } }]),
  card('q3', 'Draw the molecule.', [{ id: 'q3-r1', kind: 'point', verbatim: 'correct shape', marks: 3 }, { id: 'q3-r2', kind: 'point', verbatim: 'bond angle', marks: 3 }], {
    figure: { candId: 'f', src: '/exam-figures/chemistry/solution.png', srcHash: 'x', alt: 'The printed solution', lettersVisible: [], attribution: 'SEC © State Examinations Commission', solution: true },
  }),
];

const chemistry = CURRICULUM_SPECIFICATIONS.find(spec => spec.subjectId === 'chemistry' && spec.groups.some(group => group.topics.some(topic => topic.id === 'chem-2-2')))!;
const selection = { subjectId: 'chemistry', specificationId: chemistry.id, topicIds: ['chem-2-2'] };

const profile = [{ subjectName: 'Chemistry', level: 'ordinary' as const }];

beforeEach(() => {
  vi.clearAllMocks();
  mocks.loadCards.mockResolvedValue(cards);
});

describe('the quick check', () => {
  test('answers first, then marks against the scheme, then returns to the saved session', async () => {
    const onDone = vi.fn();
    render(<StudySessionQuiz uid="student-a" subject="Chemistry" topicSelection={selection} profileSubjects={profile} onDone={onDone} onSkip={vi.fn()} now={() => 1_700_000_000_000} />);

    expect(await screen.findByText('Is ethene planar or tetrahedral?')).toBeInTheDocument();
    expect(screen.getByText(/Question 1 of 3/)).toBeInTheDocument();
    // The scheme stays hidden until the student has had a go.
    expect(screen.queryByText('planar')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/ }));
    fireEvent.click(screen.getByRole('button', { name: /planar/ }));
    expect(screen.getByText('6 / 6 self-assessed marks')).toBeInTheDocument();
    expect(screen.getByText(/© State Examinations Commission/)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Next question/ }));
    expect(mocks.ensureDeck).toHaveBeenCalledWith('student-a', 'chemistry-ordinary', 1_700_000_000_000);
    expect(mocks.commitReview).toHaveBeenLastCalledWith('student-a', 'chemistry-ordinary', 'q1', expect.anything(), 1_700_000_000_000);

    // A bounded group caps at "any two".
    expect(await screen.findByText('Name two alkenes.')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/ }));
    fireEvent.click(screen.getByRole('button', { name: /ethene/ }));
    fireEvent.click(screen.getByRole('button', { name: /propene/ }));
    expect(screen.getByRole('button', { name: /butene/ })).toBeDisabled();
    fireEvent.click(screen.getByRole('button', { name: /Next question/ }));

    // A solution crop is held back until reveal, and an untouched card is a miss.
    expect(await screen.findByText('Draw the molecule.')).toBeInTheDocument();
    expect(screen.queryByAltText('The printed solution')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/ }));
    expect(screen.getByAltText('The printed solution')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /See review summary/ }));

    expect(await screen.findByText('That’s your review.')).toBeInTheDocument();
    expect(screen.getByText(/^self-assessed marks$/).parentElement).toHaveTextContent('12 / 18');
    expect(screen.getByText(/2021 OL q3 · Worth another look/)).toBeInTheDocument();
    expect(mocks.commitReview).toHaveBeenCalledTimes(3);
    fireEvent.click(screen.getByRole('button', { name: /^Done/ }));
    expect(onDone).toHaveBeenCalledTimes(1);
    expect(onDone.mock.calls[0][0]).toMatchObject([
      { cardId: 'q1', marksClaimed: 6, marksAvailable: 6, grade: 'got' },
      { cardId: 'q2', marksClaimed: 6, marksAvailable: 6, grade: 'got' },
      { cardId: 'q3', marksClaimed: 0, marksAvailable: 6, grade: 'missed' },
    ]);
  });

  test('can be skipped at any point without touching the review deck', async () => {
    const onSkip = vi.fn();
    render(<StudySessionQuiz uid="student-a" subject="Chemistry" topicSelection={selection} profileSubjects={profile} onDone={onSkip} onSkip={onSkip} />);
    fireEvent.click(await screen.findByRole('button', { name: 'Close practice' }));
    expect(onSkip).toHaveBeenCalledTimes(1);
    expect(mocks.commitReview).not.toHaveBeenCalled();
  });

  test('steps aside when there is nothing worth asking', async () => {
    mocks.loadCards.mockResolvedValue([]);
    const onDone = vi.fn();
    render(<StudySessionQuiz uid="student-a" subject="Chemistry" topicSelection={selection} profileSubjects={profile} onDone={onDone} onSkip={vi.fn()} />);
    await waitFor(() => expect(onDone).toHaveBeenCalledWith([]));
    expect(screen.queryByRole('button', { name: /Reveal/ })).not.toBeInTheDocument();
  });

  test('a subject with no Mark Bank deck steps aside too', async () => {
    const onDone = vi.fn();
    render(<StudySessionQuiz uid="student-a" subject="Hebrew Studies" profileSubjects={[]} onDone={onDone} onSkip={vi.fn()} />);
    await waitFor(() => expect(onDone).toHaveBeenCalledWith([]));
    expect(mocks.loadCards).not.toHaveBeenCalled();
  });
});


test('skipping excludes marks and revisiting retains the answer without another review write', async () => {
  const onDone = vi.fn();
  mocks.loadCards.mockResolvedValue(cards.slice(0, 2));
  render(<StudySessionQuiz uid="student-a" subject="Chemistry" topicSelection={selection} profileSubjects={profile} onDone={onDone} onSkip={vi.fn()} />);
  await screen.findByText('Is ethene planar or tetrahedral?');
  fireEvent.change(screen.getByLabelText('Your answer'), { target: { value: 'It is planar.' } });
  expect(mocks.play).not.toHaveBeenCalled();
  fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/ }));
  expect(mocks.play).toHaveBeenLastCalledWith('complete');
  fireEvent.click(screen.getByRole('button', { name: /planar/ }));
  expect(mocks.play).toHaveBeenLastCalledWith('tap');
  fireEvent.click(screen.getByRole('button', { name: 'Next question' }));
  fireEvent.click(screen.getByRole('button', { name: 'Skip question' }));
  expect(await screen.findByText('That’s your review.')).toBeInTheDocument();
  expect(screen.getByText(/^self-assessed marks$/).parentElement).toHaveTextContent('6 / 6');
  expect(screen.getByText(/2021 OL q2 · Skipped/)).toBeInTheDocument();
  expect(mocks.commitReview).toHaveBeenCalledTimes(1);
  fireEvent.click(screen.getByRole('button', { name: 'Review questions' }));
  expect(await screen.findByLabelText('Your answer')).toHaveValue('It is planar.');
  expect(screen.getByRole('button', { name: /planar/ })).toBeDisabled();
  fireEvent.click(screen.getByRole('button', { name: 'Next question' }));
  fireEvent.click(screen.getByRole('button', { name: 'Back to summary' }));
  expect(mocks.commitReview).toHaveBeenCalledTimes(1);
  fireEvent.click(screen.getByRole('button', { name: /^Done/ }));
  expect(onDone).toHaveBeenCalledWith([expect.objectContaining({ cardId: 'q1', marksClaimed: 6, marksAvailable: 6 })]);
});

test('Power in the School uses the actual Politics clickable bands', async () => {
  const original = politicsCards.find(card => card.id === 'politics-2019-hl-q1-d')!;
  mocks.loadCards.mockResolvedValue([original]);
  render(<StudySessionQuiz uid="student-a" subject="Politics and Society" topicSelection={{ subjectId: 'politics-and-society', specificationId: 'politics-and-society:current', topicIds: ['politics-and-society-0-0'] }} onDone={vi.fn()} onSkip={vi.fn()} />);
  fireEvent.click(await screen.findByRole('button', { name: /Reveal the marking scheme/ }));
  expect(screen.getByText('Very good argument')).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: /4 marks/ }));
  expect(screen.getByText('4 / 5 self-assessed marks')).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'See review summary' }));
  expect(screen.getByText(/^self-assessed marks$/).parentElement).toHaveTextContent('4 / 5');
  expect(mocks.commitReview).toHaveBeenCalledTimes(1);
});


test('sound uses the shared mute preference', async () => {
  render(<StudySessionQuiz uid="student-a" subject="Chemistry" topicSelection={selection} profileSubjects={profile} onDone={vi.fn()} onSkip={vi.fn()} />);
  await screen.findByText('Is ethene planar or tetrahedral?');
  fireEvent.click(screen.getByRole('button', { name: 'Mute study sound' }));
  await waitFor(() => expect(mocks.setEnabled).toHaveBeenLastCalledWith(false));
  expect(screen.getByRole('button', { name: 'Turn study sound on' })).toHaveAttribute('aria-pressed', 'false');
  fireEvent.click(screen.getByRole('button', { name: 'Turn study sound on' }));
  await waitFor(() => expect(mocks.setEnabled).toHaveBeenLastCalledWith(true));
});

test('a failed deck load offers retry and can return to the safely saved session', async () => {
  mocks.loadCards.mockRejectedValueOnce(new Error('offline'));
  const onSkip = vi.fn();
  render(<StudySessionQuiz uid="student-a" subject="Chemistry" topicSelection={selection} profileSubjects={profile} onDone={vi.fn()} onSkip={onSkip} />);
  expect(await screen.findByText('Questions couldn’t load this time.')).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Try again' }));
  expect(await screen.findByText('Is ethene planar or tetrahedral?')).toBeInTheDocument();
  expect(mocks.commitReview).not.toHaveBeenCalled();
});
