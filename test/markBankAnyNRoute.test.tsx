import React from 'react';
import { expect, test, vi } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import SessionScreen, { committedRoute, marksClaimed, type SessionResponse } from '@/components/MarkBank/SessionScreen';
import { emptyWaysInWork } from '@/components/MarkBank/WaysInPanel';
import { CARDS as PHYSICS } from '@/components/MarkBank/cards/physics/higher';
import { REVIEWED_CARDS as JAPANESE } from '@/components/MarkBank/cards/japanese/reviewed';
import { isPointCard, type SecQuestionCard } from '@/types/markBank';

vi.mock('@/components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

const japanese = JAPANESE.find(card => card.id === 'ja-2016-hl-3a-2')!;
if (japanese.kind !== 'question') throw new Error('Expected original Japanese point question');
// Explicitly synthetic route fixture; the source cards below independently
// exercise the same shared scorer against real published alternatives.
const synthetic: SecQuestionCard = {
  ...japanese, id: 'synthetic-exclusive-person-routes', questionText: 'Choose one person and give two details.',
  answerLanguageRule: undefined, questionFigure: undefined, sourceMaterial: undefined, audioMaterial: undefined,
  totalMarks: 4, rows: [
    { id: 'a', kind: 'anyN', route: 'A', marks: null, verbatim: 'Person A',
      group: { claimMax: 2, perOption: 1, perOptionSteps: [2, 1], options: ['First A detail', 'Second A detail'] } },
    { id: 'b', kind: 'anyN', route: 'B', marks: null, verbatim: 'Person B',
      group: { claimMax: 2, perOption: 1, perOptionSteps: [2, 1], options: ['First B detail', 'Second B detail'] } },
    { id: 'common', kind: 'point', marks: 1, verbatim: 'Common source point' },
  ],
};

test('exclusive menus cannot add together even in previously saved conflicting picks', () => {
  expect(committedRoute(synthetic, {}, { a: [0], b: [0] })).toBe('A');
  expect(marksClaimed(synthetic, {}, { a: [0], b: [0] })).toBe(2);
  expect(marksClaimed(synthetic, { common: 'yes' }, { a: [0, 1], b: [0, 1] })).toBe(4);
  expect(committedRoute(synthetic, {}, { a: [], b: [1] })).toBe('B');
  expect(marksClaimed(synthetic, {}, { a: [], b: [1] })).toBe(2);
});

test('invalid stored option indices do not select a route or manufacture marks', () => {
  expect(committedRoute(synthetic, {}, { a: [-1, 8, 0.5] })).toBeNull();
  expect(marksClaimed(synthetic, {}, { a: [-1, 8, 0.5] })).toBe(0);
  expect(marksClaimed(synthetic, {}, { a: [0, 0, 8] })).toBe(2);
});

test('the published Physics primary-colour alternatives remain one route', () => {
  const card = PHYSICS.find(candidate => candidate.id === 'phys-2021-hl-q6-h')!;
  expect(isPointCard(card)).toBe(true);
  expect(marksClaimed(card, {}, { r1: [0, 1], r3: [0, 1], r5: [0, 1] })).toBe(4);
  // Keep an explicitly claimed point's existing route priority in restored
  // work; options from a different route cannot supplement it.
  expect(committedRoute(card, { r4: 'yes' }, { r1: [0], r3: [0, 1] })).toBe('side-b');
  expect(marksClaimed(card, { r4: 'yes' }, { r1: [0], r3: [0, 1] })).toBe(7);
});

test('the published Japanese partial detail selects route B without its full point', () => {
  expect(committedRoute(japanese, {}, { 'r-3': [0] })).toBe('B');
  expect(marksClaimed(japanese, {}, { 'r-3': [0] })).toBe(1);
  expect(marksClaimed(japanese, { 'r-1': 'yes' }, { 'r-3': [0] })).toBe(3);
});

test('picking either route locks the other menu, clearing it allows a deliberate switch', async () => {
  const onGrade = vi.fn();
  render(<SessionScreen cards={[synthetic]} subjectLabel="Fixture" onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);
  fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
  const firstA = await screen.findByRole('button', { name: 'First A detail' });
  const firstB = await screen.findByRole('button', { name: 'First B detail' });
  fireEvent.click(firstB);
  expect(firstA).toBeDisabled();
  expect(screen.getByRole('button', { name: 'Second A detail' })).toBeDisabled();
  expect(screen.getByText(/The examiner marks one route or the other/)).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: /Common source point/ }));
  expect(screen.getByText(/You claimed 3 of 4 marks/)).toBeInTheDocument();
  fireEvent.click(firstB);
  expect(firstA).toBeEnabled();
  fireEvent.click(firstA);
  fireEvent.click(screen.getByRole('button', { name: 'Second A detail' }));
  expect(firstB).toBeDisabled();
  fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
  expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({ marksClaimed: 4, marksAvailable: 4 }));
});

test('an ordinary point locks a different routed menu on the original Japanese card', async () => {
  render(<SessionScreen cards={[japanese]} subjectLabel="Japanese" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
  fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
  fireEvent.click(await screen.findByRole('button', { name: /Studying hard for Cambridge/ }));
  expect(screen.getByRole('button', { name: 'when she watches films with friends' })).toBeDisabled();
});

test('saved competing picks remain visible in read-only review without crediting both routes', async () => {
  const response: SessionResponse = { claims: {}, picks: { a: [0], b: [0] }, rubricScores: {},
    draft: '', requirementChecks: {}, answerVariantId: null, waysInWork: emptyWaysInWork() };
  render(<SessionScreen cards={[synthetic]} subjectLabel="Fixture" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()}
    studyReview={{ banner: null, topicTitle: () => 'Fixture', onCue: vi.fn(), onResponse: vi.fn(), revisit: true,
      responses: { [synthetic.id]: response } }} />);
  const firstA = await screen.findByRole('button', { name: 'First A detail' });
  const firstB = await screen.findByRole('button', { name: 'First B detail' });
  await waitFor(() => expect(firstA).toHaveAttribute('aria-pressed', 'true'));
  expect(firstB).toHaveAttribute('aria-pressed', 'true');
  // The recap deliberately locks all answers; this repair does not make a
  // historical review editable or erase the original selections.
  expect(firstA).toBeDisabled();
  expect(firstB).toBeDisabled();
  expect(screen.getByRole('button', { name: 'Second B detail' })).toBeDisabled();
  expect(marksClaimed(synthetic, response.claims, response.picks)).toBe(2);
});
