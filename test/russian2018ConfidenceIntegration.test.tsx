import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import SessionScreen from '../components/MarkBank/SessionScreen';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { isQuizCard, quizPool } from '../components/study/quiz/studyQuizPlan';
import { isRubricCard } from '../types/markBank';

function sourceCard() {
  const card = REVIEWED_CARDS.find(candidate => candidate.id === 'ru-2018-hl-se');
  if (!card || isRubricCard(card)) throw new Error('Missing confidence source card');
  return card;
}

afterEach(cleanup);

describe('Russian 2018 confidence-only integration', () => {
  it('excludes the unresolved source allocation from numeric study quizzes', () => {
    const card = sourceCard();
    expect(card.totalMarks).toBe(30);
    expect(isQuizCard(card)).toBe(false);
    expect(quizPool([card], [card.topicId])).toEqual([]);
  });

  it.each([false, true])('retains both conflicting source ranges without a numeric grade in paper layout=%s', async paperLayout => {
    const card = sourceCard();
    const onGrade = vi.fn();
    render(<SessionScreen paperLayout={paperLayout} cards={[card]} subjectLabel="Russian"
      onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);

    expect(screen.getAllByText(/^Confidence review/).length).toBeGreaterThan(0);
    expect(screen.queryByText(/^30m$/)).not.toBeInTheDocument();
    expect(screen.queryByText(/^30 marks · Question/)).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    await waitFor(() => expect(screen.getByText(/Confidence review: the whole question/)).toBeVisible());
    expect(screen.getAllByText(/between 9 and 14 \(9-11; 12-14; 15-16\)/)[0]).toBeVisible();
    await waitFor(() => expect(screen.getAllByText(/lower A 15-16 lower E 12-14/)[0]).toBeVisible());
    expect(screen.queryByText(/Assess.*against.*30.mark total/)).not.toBeInTheDocument();
    expect(screen.getByText(/Review your complete answer against the source guidance/)).toBeVisible();
    expect(screen.queryByRole('button', { name: /^Claim \d+ marks/ })).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({
      cardId: card.id, grade: 'got', marksClaimed: 0, marksAvailable: 0,
    }));
  });
});
