import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import SessionScreen from '../components/MarkBank/SessionScreen';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { isQuizCard, quizPool } from '../components/study/quiz/studyQuizPlan';
import { isRubricCard, UNPRINTED_ANSWER } from '../types/markBank';

// The released section IDs stay on their first question after Alex's approved
// split. These checks replace the superseded confidence-only expectations.
const sources = [
  { suffix: 'se', marks: 30, answer: null },
  { suffix: 'l1', marks: 4, answer: /2 bottles of sparkling water.*2m/ },
  { suffix: 'l2', marks: 4, answer: /Started training at the age of 8.*2m/ },
  { suffix: 'l3', marks: 4, answer: /Visit surroundings of Barcelona.*2m/ },
  { suffix: 'l4', marks: 6, answer: /Young Russian video blogger.*2m/ },
] as const;

function sourceCard(suffix: string) {
  const card = REVIEWED_CARDS.find(candidate => candidate.id === `ru-2020-hl-${suffix}`);
  if (!card || !isRubricCard(card)) throw new Error(`Missing approved source card ${suffix}`);
  return card;
}

afterEach(cleanup);

describe('Russian 2020 approved source-scoring integration', () => {
  it('retains the essay in numeric quizzes while listening remains in its audio session', () => {
    const cards = sources.map(({ suffix }) => sourceCard(suffix));
    expect(cards.map(card => card.totalMarks)).toEqual(sources.map(source => source.marks));
    expect(cards.map(isQuizCard)).toEqual([true, false, false, false, false]);
    expect(cards.slice(1).every(card => Boolean(card.audioMaterial))).toBe(true);
    expect(quizPool(cards, cards.flatMap(card => [card.topicId, ...(card.additionalTopicIds ?? [])])))
      .toEqual([sourceCard('se')]);
  });

  it.each(sources.flatMap(source => [false, true].map(paperLayout => ({ ...source, paperLayout }))))(
    'retains source guidance and saves the approved marks for $suffix in paper layout=$paperLayout',
    async ({ suffix, marks, answer, paperLayout }) => {
      const card = sourceCard(suffix);
      const onGrade = vi.fn();
      render(<SessionScreen paperLayout={paperLayout} cards={[card]} subjectLabel="Russian"
        onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);

      expect(screen.queryByText(/^Confidence review/)).not.toBeInTheDocument();
      fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
      if (answer === null) {
        expect(card.rubric.system).toBe('language-writing');
        await waitFor(() => expect(screen.getByText(UNPRINTED_ANSWER, { exact: false })).toBeVisible());
        expect(screen.getByText('Communication/content (C)')).toBeVisible();
        expect(screen.getByText('Language/expression (E)')).toBeVisible();
        expect(screen.getAllByText(/Deduct 1\/2 marks/)[0]).toBeVisible();
      } else {
        expect(card.rubric.system).toBe('language-points');
        await waitFor(() => expect(screen.getByText(/Two marks per complete requested detail are inferred/)).toBeVisible());
        fireEvent.click(screen.getByRole('button', { name: 'Answer 1' }));
        fireEvent.click(screen.getByRole('button', { name: answer }));
      }
      expect(screen.queryByText(/^Confidence review/)).not.toBeInTheDocument();
      fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
      expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({
        cardId: card.id, grade: 'got', marksClaimed: answer === null ? 0 : 2, marksAvailable: marks,
      }));
    },
  );
});
