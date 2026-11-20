/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Listenings live in Listening Studio; Mark Bank reviews everything else.
 *
 * The Studio is Mark Bank on its listening front page: the same deck, the same
 * memory of each card and the same recorder. So a part saved in the Studio is
 * written exactly where a review writes it, and Mark Bank's board and queues
 * no longer hold the cards that carry a recording.
 */
import React from 'react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import type { SecCard } from '@/types/markBank';
import type * as Deck from '@/components/MarkBank/deck';

const mocks = vi.hoisted(() => ({
  loadCards: vi.fn(async (): Promise<SecCard[]> => []), commitReview: vi.fn(), track: vi.fn(), library: vi.fn(),
}));
vi.mock('@/components/MarkBank/deck', async importOriginal => ({ ...(await importOriginal<typeof Deck>()), loadCards: mocks.loadCards }));
vi.mock('@/components/MarkBank/store', () => {
  const empty = () => ({ v: 1, cards: {}, updatedAt: 0 });
  return { readChoice: vi.fn(() => null), writeChoice: vi.fn(), readLocal: empty, writeLocal: vi.fn(),
    ensureDeck: empty, fetchDeck: vi.fn(async () => empty()), mergeDecks: empty, commitReview: mocks.commitReview.mockImplementation(empty) };
});
vi.mock('@/components/MarkBank/MarkBankLibrary', () => ({
  default: (props: { cards: SecCard[]; listeningCount?: number; onOpenListeningStudio?: () => void }) => {
    mocks.library(props);
    return <button onClick={props.onOpenListeningStudio}>Board: {props.cards.length} to review, {props.listeningCount} in the Studio</button>;
  },
}));
vi.mock('@/utils/programmeAnalytics', () => ({ trackProgrammeEvent: mocks.track }));
vi.mock('@/components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));
import MarkBank from '@/components/MarkBank/MarkBank';
import { CARDS as MUSIC_HIGHER } from '@/components/MarkBank/cards/music/higher';
import { listeningSittings } from '@/components/ListeningStudio/model';

const MUSIC_2025 = MUSIC_HIGHER.filter(card => card.year === 2025);
const RECORDED = MUSIC_2025.filter(card => card.audioMaterial);
const NOW = 1_700_000_000_000;

beforeEach(() => {
  vi.clearAllMocks();
  localStorage.clear();
  sessionStorage.clear();
  mocks.loadCards.mockResolvedValue(MUSIC_2025);
  vi.spyOn(HTMLMediaElement.prototype, 'play').mockImplementation(() => Promise.resolve());
  vi.spyOn(HTMLMediaElement.prototype, 'pause').mockImplementation(() => {});
});

describe('Mark Bank', () => {
  it('reviews the cards without a recording and points to the Studio for the rest', async () => {
    const open = vi.fn();
    render(<MarkBank uid="student-a" studentSubjects={[{ subjectName: 'Music', level: 'higher' }]} onOpenListeningStudio={open} now={() => NOW} />);
    expect(RECORDED.length).toBeGreaterThan(30);
    const board = await screen.findByRole('button', {
      name: `Board: ${MUSIC_2025.length - RECORDED.length} to review, ${RECORDED.length} in the Studio`,
    });
    const handed = mocks.library.mock.calls.at(-1)?.[0] as { cards: SecCard[] };
    expect(handed.cards.some(card => card.audioMaterial)).toBe(false);
    fireEvent.click(board);
    expect(open).toHaveBeenCalledTimes(1);
  });
});

describe('Listening Studio', () => {
  it('opens on the student\'s first subject with listenings and lists its papers by question', async () => {
    render(<MarkBank studio uid="student-a" now={() => NOW}
      studentSubjects={[{ subjectName: 'Biology', level: 'higher' }, { subjectName: 'Music', level: 'higher' }]} />);
    expect(await screen.findByRole('heading', { level: 1, name: 'Listening Studio' })).toBeInTheDocument();
    await waitFor(() => expect(mocks.loadCards).toHaveBeenCalledWith('music', 'higher'));
    const paper = await screen.findByRole('region', { name: '2025 Higher' });
    expect(within(paper).getAllByRole('button')).toHaveLength(6);
    expect(within(paper).getByRole('button', { name: /^Question 5/ })).toHaveTextContent('3 extracts · 6 parts · 15 marks');
    // A paper says where its recording is: here once its sound files are uploaded, the SEC's site until then.
    const playsHere = listeningSittings(MUSIC_2025)[0].playsInApp;
    expect(within(paper).getByText(playsHere ? 'Recording plays here' : 'Recording opens on the SEC site')).toBeInTheDocument();
    expect(mocks.library).not.toHaveBeenCalled();
  });

  it('saves a part through Mark Bank\'s own recorder, to the same deck and card', async () => {
    render(<MarkBank studio uid="student-a" studentSubjects={[{ subjectName: 'Music', level: 'higher' }]} now={() => NOW} />);
    fireEvent.click(await screen.findByRole('button', { name: /^Question 5/ }));
    const sitting = await screen.findByRole('dialog', { name: 'Listening Studio: Music 2025 Higher, Question 5' });
    fireEvent.click(within(sitting).getByRole('button', { name: 'Next: Excerpt 2' }));
    fireEvent.click(within(sitting).getByRole('button', { name: 'Next: Excerpt 3' }));
    fireEvent.click(within(sitting).getByRole('button', { name: 'Mark my answers' }));
    fireEvent.click(within(sitting).getByText('Sean-nós'));
    fireEvent.click(await within(sitting).findByRole('button', { name: 'Save 1 of 15 to Mark Bank' }));

    expect(mocks.commitReview).toHaveBeenCalledTimes(1);
    expect(mocks.commitReview).toHaveBeenCalledWith('student-a', 'music-higher', 'mus-2025-hl-l-q5-a-a', expect.anything(), NOW);
    expect(mocks.track).toHaveBeenCalledWith('practice_attempt_completed', expect.objectContaining({
      source: 'practice', subjectId: 'music', accuracyBand: 'full',
    }));
    // The next question on the paper is one tap away.
    fireEvent.click(within(sitting).getByRole('button', { name: 'Next: Question 6' }));
    expect(await screen.findByRole('dialog', { name: 'Listening Studio: Music 2025 Higher, Question 6' })).toBeInTheDocument();
  });
});
