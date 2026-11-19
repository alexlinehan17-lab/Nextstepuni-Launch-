import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import SessionScreen from '../components/MarkBank/SessionScreen';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { isQuizCard, quizPool } from '../components/study/quiz/studyQuizPlan';
import { isRubricCard } from '../types/markBank';

function sourceCard() {
  const card = REVIEWED_CARDS.find(candidate => candidate.id === 'ru-2012-hl-c1-2-ii');
  if (!card || isRubricCard(card)) throw new Error('Missing confidence source card');
  return card;
}

afterEach(cleanup);

describe('Russian 2012 confidence-only integration', () => {
  it('excludes the unresolved source allocation from numeric study quizzes', () => {
    const card = sourceCard();
    expect(card.totalMarks).toBe(6);
    expect(isQuizCard(card)).toBe(false);
    expect(quizPool([card], [card.topicId])).toEqual([]);
  });

  it.each([false, true])('retains the source conflict without suggesting an agreed maximum in paper layout=%s', async paperLayout => {
    const card = sourceCard();
    const onGrade = vi.fn();
    render(<SessionScreen paperLayout={paperLayout} cards={[card]} subjectLabel="Russian"
      onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);

    expect(screen.getAllByText(/^Confidence review/).length).toBeGreaterThan(0);
    expect(screen.queryByText(/^6m$/)).not.toBeInTheDocument();
    expect(screen.queryByText(/^6 marks · Question/)).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    await waitFor(() => expect(screen.getByText(/Source allocation ambiguity:/)).toBeVisible());
    expect(screen.getAllByText(/COMPULSORY: reference must be made/)[0]).toBeVisible();
    expect(screen.getAllByText(/2 x 2 = 6/).length).toBeGreaterThan(0);
    expect(screen.queryByText(/Assess.*against.*6.mark total/)).not.toBeInTheDocument();
    expect(screen.getByText(/Review your complete answer against the source guidance/)).toBeVisible();
    expect(screen.queryByRole('button', { name: /^Claim \d+ marks/ })).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({
      cardId: card.id, grade: 'got', marksClaimed: 0, marksAvailable: 0,
    }));
  });
});
