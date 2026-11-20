/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A listening card is its own exercise unless it is Irish.
 *
 * Live defect, 20 Nov 2026. Music was missing from a hand-kept list of the
 * subjects whose listening cards are scored alone, so every Music card that
 * shared a sitting, topic and sound file collapsed into one exercise. The
 * reviewer printed all of their questions under one player, showed the first
 * card's scheme only, graded that card only and never showed the others:
 * 1,110 of Music's 1,337 listening cards (2,569 of 3,056 marks) could not be
 * reached. 2025 Higher Question 5 A showed parts (a) to (f) together with a
 * scheme of one row, "Sean-nós", for 1 mark.
 *
 * Only Irish listening has a combined marking sheet, so only Irish is grouped
 * (sessionPlanning.ts). These tests hold Music to that card by card, and hold
 * every deck to it, so that a subject carded later cannot fall into the gap.
 */
import React from 'react';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import SessionScreen from '../components/MarkBank/SessionScreen';
import { CARDS as MUSIC_HIGHER } from '../components/MarkBank/cards/music/higher';
import { builtDecks, loadCards } from '../components/MarkBank/deck';
import {
  completeListeningExercises, listeningExerciseKey, sessionExerciseCount, visibleSessionExercises,
} from '../components/MarkBank/sessionPlanning';
import { isPointCard, isRubricCard, type SecQuestionCard } from '../types/markBank';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));
afterEach(cleanup);

// 2025 Higher Listening Question 5 A: one sound file, one topic, six printed parts worth 15 marks.
const PARTS = ['a', 'b', 'c', 'd', 'e', 'f']
  .map(part => MUSIC_HIGHER.find(card => card.id === `mus-2025-hl-l-q5-a-${part}`) as SecQuestionCard);

describe('Music listening cards stand alone', () => {
  it('keeps every printed part of one sound file its own exercise', () => {
    expect(PARTS.every(card => card && isPointCard(card) && card.audioMaterial)).toBe(true);
    expect(new Set(PARTS.map(card => card.audioMaterial?.playbackUrl)).size).toBe(1);
    expect(new Set(PARTS.map(card => card.topicId)).size).toBe(1);
    expect(PARTS.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(15);

    expect(PARTS.map(listeningExerciseKey)).toEqual(PARTS.map(() => null));
    expect(sessionExerciseCount(PARTS)).toBe(6);
    expect(visibleSessionExercises(PARTS).map(card => card.id)).toEqual(PARTS.map(card => card.id));
    // Choosing one part no longer drags its five siblings into the sitting behind it.
    expect(completeListeningExercises([PARTS[0]], PARTS).map(card => card.id)).toEqual([PARTS[0].id]);
  });

  it('shows each part with its own question, scheme and grade', () => {
    const onGrade = vi.fn();
    const [first, second] = PARTS;
    render(<SessionScreen cards={[first, second]} subjectLabel="Music"
      onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);

    // Part (a): the recording, the listening booklet's page, and this part's question alone.
    expect(screen.getAllByText(/official audio/i)).toHaveLength(1);
    expect(screen.getByRole('button', { name: /Listening — Question 5/ })).toBeInTheDocument();
    expect(screen.getByTestId('mark-bank-question-text')).toHaveTextContent(first.questionText);
    expect(screen.queryByText(/Questions for this recording/i)).not.toBeInTheDocument();
    expect(screen.queryByTestId('mark-bank-listening-questions')).not.toBeInTheDocument();
    expect(screen.queryByText(second.questionText)).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    expect(screen.getByText('Sean-nós')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
    expect(onGrade).toHaveBeenCalledTimes(1);
    expect(onGrade).toHaveBeenLastCalledWith(expect.objectContaining({ cardId: first.id }));

    // Part (b) follows as its own exercise: it was never shown or graded before.
    expect(screen.getAllByText(/official audio/i)).toHaveLength(1);
    expect(screen.getByRole('button', { name: /Listening — Question 5/ })).toBeInTheDocument();
    expect(screen.getByTestId('mark-bank-question-text')).toHaveTextContent(second.questionText);
    expect(screen.queryByText(first.questionText)).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    expect(screen.getByText(/Features of sean-nós singing/)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
    expect(onGrade).toHaveBeenCalledTimes(2);
    expect(onGrade).toHaveBeenLastCalledWith(expect.objectContaining({ cardId: second.id }));
  });
});

describe('every deck: only a card the combined sheet can mark is grouped by recording', () => {
  it('groups Irish rubric cards and nothing else', async () => {
    const perSubject = new Map<string, { cards: number; exercises: number }>();
    const wronglyGrouped: string[] = [];
    for (const deck of builtDecks()) {
      const listening = (await loadCards(deck.subjectId, deck.level)).filter(card => card.audioMaterial);
      if (!listening.length) continue;
      const tally = perSubject.get(deck.subjectId) ?? { cards: 0, exercises: 0 };
      tally.cards += listening.length;
      tally.exercises += sessionExerciseCount(listening);
      perSubject.set(deck.subjectId, tally);
      for (const card of listening) {
        if (listeningExerciseKey(card) === null) continue;
        // The combined sheet is built from Irish rubric criteria (SessionScreen's
        // combinedListeningAssessment); a grouped card of any other kind is never marked.
        const combinable = isRubricCard(card) && card.rubric.system === 'irish';
        if (!combinable) wronglyGrouped.push(card.id);
      }
    }
    expect(wronglyGrouped).toEqual([]);

    // Irish is still presented one recording section at a time.
    const irish = perSubject.get('irish') as { cards: number; exercises: number };
    expect(irish.exercises).toBeLessThan(irish.cards);
    // Every other subject with recordings shows every one of its listening cards.
    const hidden = [...perSubject].filter(([subjectId, tally]) =>
      subjectId !== 'irish' && tally.exercises !== tally.cards).map(([subjectId]) => subjectId);
    expect(hidden).toEqual([]);
    const music = perSubject.get('music') as { cards: number; exercises: number };
    expect(music.cards).toBeGreaterThan(1300);
    expect(music.exercises).toBe(music.cards);
  }, 180_000);
});
