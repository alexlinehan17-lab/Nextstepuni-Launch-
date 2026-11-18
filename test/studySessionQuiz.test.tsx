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
import StudySessionCompletion from '@/components/study/StudySessionCompletion';
import { studyPlannerSample } from '@/data/studyPlannerSamples';
import { createStudyPlan, readStudyPlan } from '@/services/studyPlanStore';
import { profilePlanSettings } from '@/services/studyPlanEngine';
import { recordStudyQuizResults } from '@/services/studyQuizEvidence';

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
  test.each(['leave', 'finish'])('returns focus to the saved confirmation after the real quiz: %s', async action => {
    mocks.loadCards.mockResolvedValue(cards.slice(0, 1));
    render(<StudySessionCompletion uid="student-a" subject="Chemistry" seconds={1500} points={30} topicSelection={selection} profileSubjects={profile} quizEnabled onStudyAgain={vi.fn()} />);
    fireEvent.click(await screen.findByRole('button', { name: 'Yes, test me' }));
    if (action === 'leave') fireEvent.click(await screen.findByRole('button', { name: 'Close practice' }));
    else {
      fireEvent.click(await screen.findByRole('button', { name: 'Skip question' }));
      fireEvent.click(await screen.findByRole('button', { name: /^Done/ }));
    }
    await waitFor(() => expect(screen.getByRole('heading', { name: 'Session saved.' })).toHaveFocus());
    expect(screen.getByLabelText('Session details')).toHaveTextContent('+30JP');
    expect(mocks.commitReview).not.toHaveBeenCalled();
  });

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

function quizPlan(scope: string) {
  const input = studyPlannerSample('sixth');
  input.profile = { ...input.profile, subjects: profile, examStartDate: '2027-06-07' };
  input.settings = profilePlanSettings(input.profile);
  input.evidence = []; input.cards = []; input.deadlines = []; input.requirements = [];
  return createStudyPlan(scope, input, '2026-11-09', '2026-11-09', true);
}
const quizNow = new Date('2026-11-09T12:00:00Z').getTime();
const assessed = (c: SecCard, marks: number) => ({ card: c, result: {
  cardId: c.id, marksClaimed: marks, marksAvailable: c.totalMarks, grade: marks === c.totalMarks ? 'got' as const : 'missed' as const,
} });

test('the real quiz updates topic follow-up immediately, including when the student closes before finishing', async () => {
  const scope = 'quiz-planner-integration';
  quizPlan(scope);
  render(<StudySessionQuiz uid={scope} subject="Chemistry" topicSelection={selection} profileSubjects={profile} onDone={vi.fn()} onSkip={vi.fn()} now={() => quizNow} />);
  fireEvent.click(await screen.findByRole('button', { name: /Reveal the marking scheme/ }));
  fireEvent.click(screen.getByRole('button', { name: /planar/ }));
  fireEvent.click(screen.getByRole('button', { name: 'Next question' }));
  expect(readStudyPlan(scope)!.inputs.evidence).toEqual([expect.objectContaining({
    topicId: 'chem-2-2', result: 'self-assessed', dueOn: '2026-11-12', successfulReviews: 0,
    assessment: expect.objectContaining({ source: 'study-quiz', questionCount: 1, marksClaimed: 6, marksAvailable: 6 }),
  })]);
  // No marks claimed for the next answered question; the topic now needs practice.
  fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/ }));
  fireEvent.click(screen.getByRole('button', { name: 'Next question' }));
  const saved = readStudyPlan(scope)!;
  expect(saved.inputs.evidence[0]).toMatchObject({ result: 'partial', dueOn: '2026-11-11', assessment: { questionCount: 2 } });
  expect(saved.plan.tasks.some(t => t.topicKey === `${chemistry.id}::chem-2-2` && t.kind === 'practice' && t.date >= '2026-11-11')).toBe(true);
  fireEvent.click(screen.getByRole('button', { name: 'Close practice' }));
  expect(readStudyPlan(scope)!.inputs.evidence[0].assessment!.questionCount).toBe(2);
  expect(mocks.commitReview).toHaveBeenCalledTimes(2);
});

test('quiz evidence is account scoped, idempotent and never awards independent successes', () => {
  const scope = 'quiz-evidence-dedup';
  quizPlan(scope); quizPlan('quiz-other-account');
  recordStudyQuizResults(scope, selection, [assessed(cards[0], 6), assessed(cards[0], 6)], 'session-one', quizNow);
  const first = readStudyPlan(scope);
  recordStudyQuizResults(scope, selection, [assessed(cards[0], 6)], 'session-one', quizNow);
  expect(readStudyPlan(scope)).toBe(first);
  recordStudyQuizResults(scope, selection, [assessed(cards[0], 6)], 'session-two', quizNow + 1000);
  expect(readStudyPlan(scope)!.inputs.evidence[0]).toMatchObject({ result: 'self-assessed', successfulReviews: 0, dueOn: '2026-11-12' });
  expect(readStudyPlan('quiz-other-account')!.inputs.evidence).toEqual([]);
});

test('skipped, invalid, ambiguous and wrong-cohort questions do not create topic evidence', () => {
  const scope = 'quiz-evidence-guards';
  quizPlan(scope);
  recordStudyQuizResults(scope, selection, [], 'skip', quizNow);
  recordStudyQuizResults(scope, selection, [assessed(cards[0], 999)], 'invalid', quizNow);
  const other = chemistry.groups.flatMap(g => g.topics).find(t => t.id !== 'chem-2-2')!;
  recordStudyQuizResults(scope, selection, [assessed({ ...cards[0], additionalTopicIds: [other.id] }, 6)], 'ambiguous', quizNow);
  recordStudyQuizResults(scope, selection, [assessed({ ...cards[0], additionalTopicIds: ['unmatched-topic'] }, 6)], 'partly-unmatched', quizNow);
  recordStudyQuizResults(scope, { ...selection, specificationId: 'wrong-cohort' }, [assessed(cards[0], 6)], 'wrong', quizNow);
  expect(readStudyPlan(scope)!.inputs.evidence).toEqual([]);
  recordStudyQuizResults(scope, selection, [assessed(cards[0], 0)], 'missed', quizNow);
  expect(readStudyPlan(scope)!.inputs.evidence[0]).toMatchObject({ result: 'failed', dueOn: '2026-11-10' });
});

test('a registry alias and its canonical topic are one topic, not an ambiguous question', () => {
  const scope = 'quiz-canonical-alias';
  const input = studyPlannerSample('sixth');
  input.profile = { ...input.profile, subjects: [{ subjectName: 'Business', level: 'higher' }], examStartDate: '2027-06-07' };
  input.settings = profilePlanSettings(input.profile);
  input.evidence = []; input.cards = []; input.deadlines = []; input.requirements = [];
  createStudyPlan(scope, input, '2026-11-09', '2026-11-09', true);
  const spec = CURRICULUM_SPECIFICATIONS.find(s => s.id === 'business:2027')!;
  const [alias, canonical] = Object.entries(spec.legacyTopicAliases!)[0];
  const question = { ...cards[0], subjectId: 'business', topicId: alias };
  recordStudyQuizResults(scope, { subjectId: 'business', specificationId: spec.id, topicIds: [canonical] }, [assessed(question, 6)], 'alias', quizNow);
  expect(readStudyPlan(scope)!.inputs.evidence).toEqual([expect.objectContaining({ topicId: canonical, specificationId: spec.id, result: 'self-assessed' })]);
});
