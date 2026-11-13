import React from 'react';
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, expect, test, vi } from 'vitest';
import type { LoadedQuiz } from '@/components/study/quiz/studyQuizPlan';

const moduleLoad = vi.hoisted(() => {
  let resolve!: () => void;
  return { ready: new Promise<void>(done => { resolve = done; }), finish: () => resolve() };
});
vi.mock('@/components/study/quiz/studyQuizPlan', () => ({ loadQuiz: async () => ({ cards: [{ id: 'sample' }], topicLabel: 'Probability' } as LoadedQuiz) }));
vi.mock('@/components/study/quiz/StudySessionQuiz', async () => {
  await moduleLoad.ready;
  return { default: () => <div role="dialog" aria-label="Topic questions">The first question</div> };
});
import StudySessionCompletion from '@/components/study/StudySessionCompletion';

afterEach(cleanup);

test('a cold quiz interface stays escapable, then opens immediately once prepared', async () => {
  const props = { uid: 'demo-student', subject: 'Mathematics', seconds: 1500, points: 30, quizEnabled: true, onStudyAgain: vi.fn() };
  const view = render(<StudySessionCompletion {...props} />);
  // The cards are ready but the interface is still downloading.
  expect(screen.queryByRole('button', { name: 'Yes, test me' })).not.toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Continue without questions' }));
  expect(screen.getByRole('heading', { name: 'Session saved.' })).toHaveFocus();
  await act(async () => { moduleLoad.finish(); await vi.dynamicImportSettled(); });
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  view.unmount();

  render(<StudySessionCompletion {...props} />);
  fireEvent.click(await screen.findByRole('button', { name: 'Yes, test me' }));
  expect(screen.getByRole('dialog', { name: 'Topic questions' })).toBeInTheDocument();
  expect(screen.queryByRole('status')).not.toBeInTheDocument();
});
