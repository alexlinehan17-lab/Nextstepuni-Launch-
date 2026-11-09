import React from 'react';
import { beforeEach, expect, test, vi } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import type { SecCard, SecQuestionCard } from '@/types/markBank';
import type * as Deck from '@/components/MarkBank/deck';

const mocks = vi.hoisted(() => ({ loadCards: vi.fn(async (): Promise<SecCard[]> => []), commitReview: vi.fn(), track: vi.fn() }));
vi.mock('@/components/MarkBank/deck', async importOriginal => ({ ...(await importOriginal<typeof Deck>()), loadCards: mocks.loadCards }));
vi.mock('@/components/MarkBank/store', () => {
  const empty = () => ({ v: 1, cards: {}, updatedAt: 0 });
  return { readChoice: vi.fn(() => null), writeChoice: vi.fn(), readLocal: empty, writeLocal: vi.fn(),
    ensureDeck: empty, fetchDeck: vi.fn(async () => empty()), mergeDecks: empty, commitReview: mocks.commitReview.mockImplementation(empty) };
});
vi.mock('@/components/MarkBank/MarkBankLibrary', () => ({ default: ({ ready, onStart }: { ready: boolean; onStart: () => void }) =>
  <button disabled={!ready} onClick={() => onStart()}>Start test review</button> }));
vi.mock('@/utils/programmeAnalytics', () => ({ trackProgrammeEvent: mocks.track }));
vi.mock('@/components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));
import MarkBank from '@/components/MarkBank/MarkBank';
import { REVIEWED_CARDS } from '@/components/MarkBank/cards/japanese/reviewed';

const original = REVIEWED_CARDS.find(card => card.id === 'ja-2022-ol-lb-1-v')! as SecQuestionCard;
beforeEach(() => { vi.clearAllMocks(); localStorage.clear(); mocks.loadCards.mockResolvedValue([original]); });
const start = async () => {
  render(<MarkBank uid="student-a" studentSubjects={[{ subjectName: 'Japanese', level: 'ordinary' }]} now={() => 1_700_000_000_000} />);
  const button = await screen.findByRole('button', { name: 'Start test review' });
  // The real shell waits for both the deck and local review state.
  await waitFor(() => expect(button).toBeEnabled());
  fireEvent.click(button);
  fireEvent.click(await screen.findByRole('button', { name: 'Reveal the marking scheme' }));
};

test('an unpriced source review is retained without zero-score analytics or a perfect-score summary', async () => {
  await start();
  fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
  expect(await screen.findByText('Your review is complete.')).toBeInTheDocument();
  expect(screen.getByText('1 answer review had no calculated marks.')).toBeInTheDocument();
  expect(screen.queryByText('Every mark banked.')).not.toBeInTheDocument();
  expect(screen.queryByText('Marks banked')).not.toBeInTheDocument();
  expect(mocks.commitReview).toHaveBeenCalledTimes(1);
  expect(mocks.track).not.toHaveBeenCalled();
});

test.each([false, true])('a priced answer still reports its assessed accuracy when claimed=%s', async claimed => {
  const priced: SecQuestionCard = { ...original, id: 'synthetic-priced-card', questionText: 'Synthetic priced response',
    audioMaterial: undefined, questionFigure: undefined, tariffModel: { kind: 'fixed' }, totalMarks: 4,
    rows: [{ id: 'answer', kind: 'point', verbatim: 'Synthetic complete answer', marks: 4 }] };
  mocks.loadCards.mockResolvedValue([priced]);
  await start();
  if (claimed) fireEvent.click(screen.getByRole('button', { name: /Synthetic complete answer/ }));
  fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
  expect(await screen.findByText(claimed ? 'Every mark banked.' : 'Good work. Keep building.')).toBeInTheDocument();
  expect(screen.getByText('Marks banked')).toBeInTheDocument();
  expect(mocks.track).toHaveBeenCalledWith('practice_attempt_completed', expect.objectContaining({ accuracyBand: claimed ? 'full' : 'none' }));
});

test('mixed sessions retain both reviews while reporting only the priced answer in numeric totals', async () => {
  const priced: SecQuestionCard = { ...original, id: 'synthetic-priced-card', questionText: 'Synthetic priced response',
    audioMaterial: undefined, questionFigure: undefined, tariffModel: { kind: 'fixed' }, totalMarks: 4,
    rows: [{ id: 'answer', kind: 'point', verbatim: 'Synthetic complete answer', marks: 4 }] };
  mocks.loadCards.mockResolvedValue([original, priced]);
  await start();
  for (let index = 0; index < 2; index++) {
    const answer = screen.queryByRole('button', { name: /Synthetic complete answer/ });
    if (answer) fireEvent.click(answer);
    fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
    if (index === 0) fireEvent.click(await screen.findByRole('button', { name: 'Reveal the marking scheme' }));
  }
  expect(await screen.findByText('Every mark banked.')).toBeInTheDocument();
  expect(screen.getByText('1 answer review had no calculated marks and is excluded from these totals.')).toBeInTheDocument();
  expect(screen.getByText(/2 questions reviewed/)).toBeInTheDocument();
  expect(mocks.commitReview).toHaveBeenCalledTimes(2);
  expect(mocks.track).toHaveBeenCalledTimes(1);
  expect(mocks.track).toHaveBeenCalledWith('practice_attempt_completed', expect.objectContaining({ accuracyBand: 'full' }));
});
