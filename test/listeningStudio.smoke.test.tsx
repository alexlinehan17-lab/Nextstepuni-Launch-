/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A Listening Studio sitting, from the first answer to the saved marks.
 *
 * The sheet shows one extract's questions together; marking shows every part
 * of the section with ITS OWN scheme (the Mark Bank reviewer, embedded), and
 * saving hands Mark Bank one result per part: the result a review of that card
 * would have recorded. A part the student never reached is left unrecorded.
 */
import React from 'react';
import { cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import StudioSitting from '../components/ListeningStudio/StudioSitting';
import {
  listeningSittings, type ListeningCard, type StudioSection, type StudioSitting as Sitting,
} from '../components/ListeningStudio/model';
import { loadCards } from '../components/MarkBank/deck';
import { CARDS as IRISH_HIGHER } from '../components/MarkBank/cards/irish/higher';
import { CARDS as MUSIC_HIGHER } from '../components/MarkBank/cards/music/higher';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

let play: ReturnType<typeof vi.spyOn>;
beforeEach(() => {
  play = vi.spyOn(HTMLMediaElement.prototype, 'play').mockImplementation(() => Promise.resolve());
  vi.spyOn(HTMLMediaElement.prototype, 'pause').mockImplementation(() => {});
  window.sessionStorage.clear();
});
afterEach(() => { cleanup(); vi.restoreAllMocks(); });

const paperOf = (sittings: Sitting[], year: number) =>
  sittings.find(sitting => sitting.year === year && !sitting.deferred) as Sitting;

/** The same section on a recording the app holds no copy of. Which real
 *  recordings are hosted changes as they are uploaded, so the tests that need
 *  an unhosted one name a file the SEC archive does not have. */
const UNHOSTED = 'https://www.examinations.ie/archive/exampapers/2099/LC067ZLP999EV.mp3';
const unhosted = (section: StudioSection): StudioSection => {
  const recast = (card: ListeningCard) => ({
    ...card, audioMaterial: { ...card.audioMaterial, playbackUrl: UNHOSTED, canonicalUrl: UNHOSTED, secFileid: 'LC067ZLP999EV.mp3' },
  }) as ListeningCard;
  return {
    ...section,
    cards: section.cards.map(recast),
    extracts: section.extracts.map(extract => ({
      ...extract, cards: extract.cards.map(recast),
      audio: { ...extract.audio, playbackUrl: UNHOSTED, canonicalUrl: UNHOSTED, secFileid: 'LC067ZLP999EV.mp3' },
    })),
  };
};

describe('Music 2025 Higher, Question 5', () => {
  const paper = paperOf(listeningSittings(MUSIC_HIGHER), 2025);
  const question = paper.sections[4];
  const mount = () => {
    const onGrade = vi.fn();
    const onClose = vi.fn();
    render(<StudioSitting subjectLabel="Music" sittingLabel={paper.title} section={question} onGrade={onGrade} onClose={onClose} />);
    return { onGrade, onClose, dialog: screen.getByRole('dialog', { name: 'Listening Studio: Music 2025 Higher, Question 5' }) };
  };

  it('shows one excerpt at a time with all of its parts, and steps through the three', () => {
    const { dialog } = mount();
    expect(within(dialog).getByRole('heading', { name: 'Excerpt 1' })).toBeInTheDocument();
    expect(screen.getAllByTestId('listening-studio-part')).toHaveLength(3);
    expect(screen.getByText('Identify the style of singing in this excerpt.')).toBeInTheDocument();
    expect(screen.getByText('Using letters, write down the form of the music in this excerpt.')).toBeInTheDocument();
    expect(screen.queryByText('Name two instruments which play the melody in this excerpt.')).not.toBeInTheDocument();
    // The printed instruction is shown once for the excerpt, not once a part.
    expect(screen.getAllByText(/Excerpt 1, played three times\./)).toHaveLength(1);

    fireEvent.click(screen.getByRole('button', { name: 'Next: Excerpt 2' }));
    expect(screen.getAllByTestId('listening-studio-part')).toHaveLength(2);
    // The stepper on the recording side goes straight to any excerpt.
    fireEvent.click(within(screen.getByRole('group', { name: 'Extracts in this section' })).getByRole('button', { name: 'Excerpt 3' }));
    expect(screen.getAllByTestId('listening-studio-part')).toHaveLength(1);
    expect(screen.getByRole('button', { name: 'Mark my answers' })).toBeInTheDocument();
  });

  it('offers the SEC\'s own page while the recording has no copy in the app', () => {
    render(<StudioSitting subjectLabel="Music" sittingLabel={paper.title} section={unhosted(question)} onGrade={vi.fn()} onClose={vi.fn()} />);
    const dialog = screen.getByRole('dialog', { name: 'Listening Studio: Music 2025 Higher, Question 5' });
    expect(within(dialog).getByText('This recording is not in the app yet.')).toBeInTheDocument();
    expect(within(dialog).getByRole('link', { name: /Open the SEC recording/ })).toHaveAttribute('href', UNHOSTED);
    // No player is drawn that could only fail, and nothing is requested from the SEC.
    expect(screen.queryByRole('button', { name: 'Play the recording' })).not.toBeInTheDocument();
    expect(document.querySelector('audio')).not.toHaveAttribute('src');
    expect(play).not.toHaveBeenCalled();
  });

  it('marks every part against its own scheme and saves only the parts that were sat', async () => {
    const { onGrade } = mount();
    fireEvent.change(screen.getByRole('textbox', { name: 'Your answer to part (a)' }), { target: { value: 'the old unaccompanied style' } });
    fireEvent.click(screen.getByRole('button', { name: 'Next: Excerpt 2' }));
    fireEvent.click(screen.getByRole('button', { name: 'Next: Excerpt 3' }));
    fireEvent.click(screen.getByRole('button', { name: 'Mark my answers' }));

    // All six parts, each with the student's answer and its own marking points.
    expect(screen.getAllByTestId('listening-studio-marking-part')).toHaveLength(6);
    expect(screen.getByText('the old unaccompanied style')).toBeInTheDocument();
    expect(screen.getAllByText('No answer written')).toHaveLength(5);
    expect(screen.getByText('Sean-nós')).toBeInTheDocument();
    expect(screen.getByText('AABA')).toBeInTheDocument();
    expect(screen.getByText('Slip Jig')).toBeInTheDocument();
    // The reviewer's own chrome stays out: no grade buttons, no second recording.
    expect(screen.queryByRole('button', { name: 'Got it' })).not.toBeInTheDocument();
    expect(screen.queryByText(/official audio/i)).not.toBeInTheDocument();
    await waitFor(() => expect(screen.getByLabelText('0 of 15 marks')).toBeInTheDocument());

    fireEvent.click(screen.getByText('Sean-nós'));
    await waitFor(() => expect(screen.getByLabelText('1 of 15 marks')).toBeInTheDocument());
    fireEvent.click(screen.getByText('AABA'));
    await waitFor(() => expect(screen.getByLabelText('3 of 15 marks')).toBeInTheDocument());

    fireEvent.click(screen.getByRole('button', { name: 'Save 3 of 15 to Mark Bank' }));
    // (a) was answered and marked, (c) was marked: two cards recorded, four left alone.
    expect(onGrade).toHaveBeenCalledTimes(2);
    expect(onGrade).toHaveBeenNthCalledWith(1, { cardId: 'mus-2025-hl-l-q5-a-a', grade: 'got', marksClaimed: 1, marksAvailable: 1 });
    expect(onGrade).toHaveBeenNthCalledWith(2, { cardId: 'mus-2025-hl-l-q5-a-c', grade: 'got', marksClaimed: 2, marksAvailable: 2 });
    expect(screen.getByRole('status')).toHaveTextContent('Saved to Mark Bank: 2 parts.');
    // Saved marks are frozen.
    expect(screen.getByText('Sean-nós').closest('button')).toBeDisabled();
  });

  it('asks before leaving once there is work that would be lost', async () => {
    const { onClose } = mount();
    fireEvent.click(screen.getByRole('button', { name: 'Leave this sitting' }));
    expect(onClose).toHaveBeenCalledTimes(1);

    cleanup();
    const second = mount();
    fireEvent.change(screen.getByRole('textbox', { name: 'Your answer to part (b)' }), { target: { value: 'ornamentation' } });
    fireEvent.click(screen.getByRole('button', { name: 'Leave this sitting' }));
    expect(second.onClose).not.toHaveBeenCalled();
    const confirm = screen.getByRole('alertdialog', { name: 'Leave this sitting?' });
    fireEvent.click(within(confirm).getByRole('button', { name: 'Stay' }));
    // The confirm is the shared one now (area 7b): it leaves with its short fade.
    await waitFor(() => expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument());
    fireEvent.click(screen.getByRole('button', { name: 'Leave this sitting' }));
    fireEvent.click(within(screen.getByRole('alertdialog')).getByRole('button', { name: 'Leave' }));
    expect(second.onClose).toHaveBeenCalledTimes(1);
  });
});

describe('a recording the app holds a copy of', () => {
  it('plays from the app\'s copy, with a seek bar, and only on a tap', async () => {
    const paper = paperOf(listeningSittings(await loadCards('french', 'higher')), 2024);
    const section = paper.sections[0];
    expect(paper.playsInApp).toBe(true);
    render(<StudioSitting subjectLabel="French" sittingLabel={paper.title} section={section} onGrade={vi.fn()} onClose={vi.fn()} />);

    expect(screen.queryByText('This recording is not in the app yet.')).not.toBeInTheDocument();
    const source = document.querySelector('audio')?.getAttribute('src') ?? '';
    expect(source).toContain('LC010');
    expect(source).not.toMatch(/examinations\.ie/);
    expect(screen.getByRole('slider', { name: 'Position in the recording' })).toBeInTheDocument();
    expect(play).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole('button', { name: 'Play the recording' }));
    expect(play).toHaveBeenCalledTimes(1);

    // French parts are marked on the language grid, each on its own card.
    fireEvent.click(screen.getByRole('button', { name: 'Mark my answers' }));
    expect(screen.getAllByTestId('listening-studio-marking-part')).toHaveLength(section.cards.length);
    await waitFor(() => expect(screen.getByLabelText(`0 of ${section.marks} marks`)).toBeInTheDocument());
  });
});

describe('Irish', () => {
  it('sits Cuid A as its two fógraí and marks each on the Irish scheme', async () => {
    const paper = paperOf(listeningSittings(IRISH_HIGHER), 2024);
    const cuid = paper.sections[0];
    render(<StudioSitting subjectLabel="Irish" sittingLabel={paper.title} section={cuid} onGrade={vi.fn()} onClose={vi.fn()} />);
    expect(screen.getByRole('heading', { name: 'Fógra a hAon' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Next: Fógra a Dó' }));
    fireEvent.click(screen.getByRole('button', { name: 'Mark my answers' }));
    expect(screen.getAllByTestId('listening-studio-marking-part')).toHaveLength(cuid.cards.length);
    await waitFor(() => expect(screen.getByLabelText(`0 of ${cuid.marks} marks`)).toBeInTheDocument());
  });
});
