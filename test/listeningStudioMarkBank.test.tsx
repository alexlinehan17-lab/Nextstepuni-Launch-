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
  const mount = (subjects = [{ subjectName: 'Biology', level: 'higher' }, { subjectName: 'Music', level: 'higher' }]) => {
    const leave = vi.fn();
    render(<MarkBank studio uid="student-a" now={() => NOW} studentSubjects={subjects} onLeaveStudio={leave} />);
    return { leave };
  };
  const chosenPaper = () => screen.getByRole('region', { name: 'The paper you have chosen' });

  it('opens on the student\'s first subject with listenings, as a wall of papers', async () => {
    const { leave } = mount();
    expect(await screen.findByRole('dialog', { name: 'Listening Studio' })).toBeInTheDocument();
    await waitFor(() => expect(mocks.loadCards).toHaveBeenCalledWith('music', 'higher'));
    expect(mocks.library).not.toHaveBeenCalled();

    // The student's own listening subjects are the tabs; Biology has no listening.
    const tabs = screen.getByRole('group', { name: 'Subject' });
    expect(within(tabs).getByRole('button', { name: 'Music' })).toHaveAttribute('aria-pressed', 'true');
    expect(within(tabs).queryByRole('button', { name: 'Biology' })).not.toBeInTheDocument();

    // One tile a paper; the newest is chosen, and its sections are ready to sit.
    const wall = await screen.findByRole('group', { name: 'Music Higher papers' });
    expect(within(wall).getAllByRole('button')).toHaveLength(1);
    expect(within(wall).getByRole('button', { name: /^2025/ })).toHaveAttribute('aria-pressed', 'true');
    const paper = chosenPaper();
    expect(within(paper).getByRole('heading', { name: /2025\s*Higher/ })).toBeInTheDocument();
    expect(within(paper).getAllByRole('button', { name: /^Question \d/ })).toHaveLength(6);
    expect(within(paper).getByRole('button', { name: /^Question 5/ })).toHaveTextContent('3 extracts · 6 parts · 15 marks');
    // A paper says where its recording is: here once its sound files are uploaded, the SEC's site until then.
    const sitting = listeningSittings(MUSIC_2025)[0];
    expect(within(paper).getByText(new RegExp(sitting.playsInApp ? 'Recording plays here' : 'Recording opens on the SEC site'))).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: 'Leave Listening Studio' }));
    expect(leave).toHaveBeenCalledTimes(1);
  });

  it('offers every subject with a listening on the subject screen', async () => {
    mount();
    fireEvent.click(await screen.findByRole('button', { name: /^All \d+ subjects$/ }));
    expect(screen.getByRole('heading', { name: 'Choose a subject' })).toBeInTheDocument();
    for (const name of ['Irish', 'French', 'German', 'Spanish', 'Italian', 'Music', 'Japanese', 'Russian', 'Polish', 'Portuguese']) {
      expect(screen.getByRole('button', { name: new RegExp(`^${name}`) })).toBeInTheDocument();
    }
    expect(screen.getByRole('button', { name: /^Music/ })).toHaveTextContent('One of your subjects');
    // French is fully hosted, and the screen says how many recordings that is.
    expect(screen.getByRole('button', { name: /^French/ })).toHaveTextContent(/\d+ recordings play here/);

    fireEvent.click(screen.getByRole('button', { name: /^French/ }));
    await waitFor(() => expect(mocks.loadCards).toHaveBeenCalledWith('french', 'higher'));
    // Back on the wall, with the chosen subject beside the student's own.
    const tabs = await screen.findByRole('group', { name: 'Subject' });
    expect(within(tabs).getByRole('button', { name: 'French' })).toHaveAttribute('aria-pressed', 'true');
    expect(within(tabs).getByRole('button', { name: 'Music' })).toBeInTheDocument();
  });

  it('saves a part through Mark Bank\'s own recorder, to the same deck and card', async () => {
    mount([{ subjectName: 'Music', level: 'higher' }]);
    await screen.findByRole('group', { name: 'Music Higher papers' });
    fireEvent.click(within(chosenPaper()).getByRole('button', { name: /^Question 5/ }));
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

  it('remembers where the student left off and carries on from there', async () => {
    mount([{ subjectName: 'Music', level: 'higher' }]);
    await screen.findByRole('group', { name: 'Music Higher papers' });
    expect(screen.queryByText('Where you left off')).not.toBeInTheDocument();
    fireEvent.click(within(chosenPaper()).getByRole('button', { name: /^Question 3/ }));
    const sitting = await screen.findByRole('dialog', { name: 'Listening Studio: Music 2025 Higher, Question 3' });
    fireEvent.click(within(sitting).getByRole('button', { name: 'Leave this sitting' }));
    await waitFor(() => expect(screen.queryByRole('dialog', { name: /Question 3$/ })).not.toBeInTheDocument());

    expect(screen.getByText('Where you left off')).toBeInTheDocument();
    expect(screen.getByText('Music · 2025 Higher · Question 3')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /^Carry on/ }));
    expect(await screen.findByRole('dialog', { name: 'Listening Studio: Music 2025 Higher, Question 3' })).toBeInTheDocument();
  });
});
