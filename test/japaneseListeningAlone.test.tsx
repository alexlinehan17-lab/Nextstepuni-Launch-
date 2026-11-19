/**
 * Japanese listening: one card per printed question, as German's live cards work.
 *
 * Codex's japanese-continuation branch (02d1e9919) grouped every Japanese
 * listening card of a recording and topic into one exercise: the student heard
 * the recording and saw all ten 2025 Higher Section A and C questions, but after
 * the reveal only the first card's answers appeared and only that card was
 * graded. In the release Japanese (and Russian) listening cards are scored alone
 * (sessionPlanning.ts LISTENING_SCORED_ALONE): each printed question is its own
 * exercise with its own player for the same recording, its own answers, its own
 * grade, and the sitting's printed wrong-language rule under its scheme.
 */
import React from 'react';
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import SessionScreen from '../components/MarkBank/SessionScreen';
import { CARDS as JAPANESE_HIGHER } from '../components/MarkBank/cards/japanese/higher';
import { CARDS as GERMAN_HIGHER } from '../components/MarkBank/cards/german/higher';
import { listeningExerciseKey, sessionExerciseCount, visibleSessionExercises } from '../components/MarkBank/sessionPlanning';
import { isPointCard, type SecQuestionCard } from '../types/markBank';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));
afterEach(cleanup);

// 2025 Higher Sections A and C: one recording, one topic, ten printed questions.
const GROUP = ['la-1', 'la-2', 'la-3', 'lc-1', 'lc-2', 'lc-3', 'lc-4', 'lc-5', 'lc-6', 'lc-7']
  .map(suffix => JAPANESE_HIGHER.find(card => card.id === `ja-2025-hl-${suffix}`) as SecQuestionCard);

describe('Japanese listening cards stand alone, as German listening cards do', () => {
  it('shares one recording but keeps every printed question its own exercise', () => {
    expect(GROUP.every(card => card && isPointCard(card) && card.audioMaterial)).toBe(true);
    expect(new Set(GROUP.map(card => card.audioMaterial?.playbackUrl)).size).toBe(1);
    expect(GROUP.map(listeningExerciseKey)).toEqual(GROUP.map(() => null));
    expect(sessionExerciseCount(GROUP)).toBe(10);
    expect(visibleSessionExercises(GROUP).map(card => card.id)).toEqual(GROUP.map(card => card.id));
    const german = GERMAN_HIGHER.filter(card => card.audioMaterial).slice(0, 3);
    expect(german.map(listeningExerciseKey)).toEqual([null, null, null]);
  });

  it('shows each question with its own player, answers and grade', () => {
    const onGrade = vi.fn();
    const [first, second] = [GROUP[3], GROUP[4]];
    render(<SessionScreen cards={[first, second]} subjectLabel="Japanese"
      onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);
    expect(screen.getAllByText(/official audio/i)).toHaveLength(1);
    expect(screen.getByTestId('mark-bank-question-text')).toHaveTextContent(first.questionText.slice(0, 30));
    expect(screen.queryByText(/Questions for this recording/i)).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    // This card's own answers, and the sitting's printed wrong-language rule under them.
    expect(screen.getByText(first.answerLanguageRule!.sourceText)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
    expect(onGrade).toHaveBeenCalledTimes(1);
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({ cardId: first.id }));
    // The next printed question follows with the same recording mounted again.
    expect(screen.getAllByText(/official audio/i)).toHaveLength(1);
    const question = screen.getByTestId('mark-bank-question-text');
    expect(within(question.parentElement ?? question).queryByText(first.questionText)).not.toBeInTheDocument();
    expect(question).toHaveTextContent(second.questionText.slice(0, 30));
  });
});
