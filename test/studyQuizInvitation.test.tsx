import React from 'react';
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, expect, test, vi } from 'vitest';
import type { LoadedQuiz } from '@/components/study/quiz/studyQuizPlan';

const mocks = vi.hoisted(() => ({ loadQuiz: vi.fn(), opened: vi.fn() }));
vi.mock('@/components/study/quiz/studyQuizPlan', () => ({ loadQuiz: mocks.loadQuiz }));
vi.mock('@/components/study/quiz/StudySessionQuiz', () => ({ default: (props: { initialQuiz: LoadedQuiz; onDone: () => void; onSkip: () => void }) => {
  mocks.opened(props.initialQuiz);
  return <div role="dialog" aria-label="Topic questions"><button onClick={props.onDone}>Finish sample questions</button><button onClick={props.onSkip}>Leave sample questions</button></div>;
} }));
import StudySessionCompletion from '@/components/study/StudySessionCompletion';

const quiz = { deck: { subjectId: 'maths', level: 'higher', title: 'Mathematics', deckId: 'maths-higher' }, cards: [{ id: 'sample' }], poolTotal: 1, topicLabel: 'Concepts of probability' } as LoadedQuiz;
const props = {
  uid: 'demo-student', subject: 'Mathematics', seconds: 1500, points: 30, quizEnabled: true,
  topicSelection: { subjectId: 'mathematics', specificationId: 'mathematics:current', topicIds: ['sample-topic'] },
  onIsland: vi.fn(), onStudyAgain: vi.fn(),
  onInvitationOpen: vi.fn(),
};
beforeEach(() => { vi.clearAllMocks(); mocks.loadQuiz.mockResolvedValue(quiz); });
afterEach(() => { cleanup(); vi.useRealTimers(); });

test('the invitation precedes the questions and the final saved screen', async () => {
  render(<StudySessionCompletion {...props} />);
  expect(screen.queryByRole('heading', { name: 'Session saved.' })).not.toBeInTheDocument();
  const yes = await screen.findByRole('button', { name: 'Yes, test me' });
  expect(screen.getByRole('dialog', { name: 'What stayed with you?' })).toBeInTheDocument();
  expect(screen.queryByRole('heading', { name: 'Session saved.' })).not.toBeInTheDocument();
  expect(mocks.opened).not.toHaveBeenCalled();
  expect(props.onInvitationOpen).toHaveBeenCalledOnce();
  expect(mocks.loadQuiz).toHaveBeenCalledWith(expect.objectContaining({ uid: props.uid, topicSelection: props.topicSelection }));
  fireEvent.click(yes);
  expect(screen.getByRole('dialog', { name: 'Topic questions' })).toBeInTheDocument();
  expect(mocks.opened).toHaveBeenCalledWith(quiz);
  expect(screen.queryByRole('dialog', { name: 'What stayed with you?' })).not.toBeInTheDocument();
  expect(screen.queryByRole('heading', { name: 'Session saved.' })).not.toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Finish sample questions' }));
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  expect(screen.queryByRole('button', { name: 'Yes, test me' })).not.toBeInTheDocument();
  expect(screen.getByRole('heading', { name: 'Session saved.' })).toHaveFocus();
  expect(screen.getByLabelText('Session details')).toHaveTextContent('+30JP');
});

test('Not now goes straight to the final saved session and its navigation', async () => {
  const view = render(<StudySessionCompletion {...props} />);
  const decline = await screen.findByRole('button', { name: 'Not now' });
  decline.focus();
  fireEvent.click(decline);
  view.rerender(<StudySessionCompletion {...props} />);
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  expect(mocks.opened).not.toHaveBeenCalled();
  expect(screen.queryByRole('button', { name: 'Yes, test me' })).not.toBeInTheDocument();
  expect(screen.getByRole('heading', { name: 'Session saved.' })).toHaveFocus();
  expect(screen.getByLabelText('Session details')).toHaveTextContent('+30JP');
  fireEvent.click(screen.getByRole('button', { name: /Spend them on your island/ }));
  expect(props.onIsland).toHaveBeenCalledOnce();
  fireEvent.click(screen.getByRole('button', { name: 'Back to the study room' }));
  expect(props.onStudyAgain).toHaveBeenCalledOnce();
});

test.each(['close', 'escape'])('%s dismisses the invitation as Not now', async action => {
  render(<StudySessionCompletion {...props} />);
  await screen.findByRole('dialog', { name: 'What stayed with you?' });
  if (action === 'close') fireEvent.click(screen.getByRole('button', { name: 'Not now, show my saved session' }));
  else fireEvent.keyDown(window, { key: 'Escape' });
  expect(mocks.opened).not.toHaveBeenCalled();
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  expect(screen.getByRole('heading', { name: 'Session saved.' })).toHaveFocus();
});

test('leaving questions early still shows the final saved session', async () => {
  render(<StudySessionCompletion {...props} />);
  fireEvent.click(await screen.findByRole('button', { name: 'Yes, test me' }));
  fireEvent.click(await screen.findByRole('button', { name: 'Leave sample questions' }));
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  expect(screen.getByLabelText('Session details')).toHaveTextContent('+30JP');
  expect(screen.getByRole('heading', { name: 'Session saved.' })).toHaveFocus();
});

test('turning off post-study questions bypasses the invitation and deck loading', () => {
  render(<StudySessionCompletion {...props} quizEnabled={false} />);
  expect(mocks.loadQuiz).not.toHaveBeenCalled();
  expect(props.onInvitationOpen).not.toHaveBeenCalled();
  expect(screen.queryByRole('button', { name: 'Yes, test me' })).not.toBeInTheDocument();
  expect(screen.getByRole('heading', { name: 'Session saved.' })).toBeInTheDocument();
});

test.each(['empty', 'failed'])('an %s question load leaves the saved receipt usable', async kind => {
  if (kind === 'empty') mocks.loadQuiz.mockResolvedValue(null);
  else mocks.loadQuiz.mockRejectedValue(new Error('offline'));
  render(<StudySessionCompletion {...props} />);
  await waitFor(() => expect(mocks.loadQuiz).toHaveBeenCalledOnce());
  await screen.findByRole('heading', { name: 'Session saved.' });
  expect(screen.queryByRole('button', { name: 'Yes, test me' })).not.toBeInTheDocument();
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  expect(screen.getByRole('button', { name: 'Back to the study room' })).toBeEnabled();
});

test('students can continue immediately while questions load, and late results cannot reopen the invitation', async () => {
  let resolveQuiz!: (value: LoadedQuiz) => void;
  mocks.loadQuiz.mockReturnValue(new Promise<LoadedQuiz>(resolve => { resolveQuiz = resolve; }));
  render(<StudySessionCompletion {...props} />);
  await waitFor(() => expect(mocks.loadQuiz).toHaveBeenCalledOnce());
  const continueButton = screen.getByRole('button', { name: 'Continue without questions' });
  continueButton.focus();
  fireEvent.click(continueButton);
  expect(screen.getByRole('heading', { name: 'Session saved.' })).toHaveFocus();
  await act(async () => { resolveQuiz(quiz); });
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  expect(screen.getByLabelText('Session details')).toHaveTextContent('+30JP');
  expect(mocks.opened).not.toHaveBeenCalled();
});

test('a stalled question load falls back to the saved session, ignoring results after the deadline', async () => {
  vi.useFakeTimers();
  let resolveQuiz!: (value: LoadedQuiz) => void;
  mocks.loadQuiz.mockReturnValue(new Promise<LoadedQuiz>(resolve => { resolveQuiz = resolve; }));
  render(<StudySessionCompletion {...props} />);
  await act(async () => { await vi.dynamicImportSettled(); });
  expect(screen.getByRole('button', { name: 'Continue without questions' })).toBeEnabled();
  await act(async () => { await vi.advanceTimersByTimeAsync(8000); });
  expect(screen.getByRole('heading', { name: 'Session saved.' })).toHaveFocus();
  await act(async () => { resolveQuiz(quiz); });
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  expect(screen.getByRole('button', { name: 'Back to the study room' })).toBeEnabled();
});
