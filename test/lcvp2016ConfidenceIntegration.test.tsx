import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import SessionScreen from '../components/MarkBank/SessionScreen';
import { CARDS } from '../components/MarkBank/cards/lcvp/common';
import { isQuizCard, quizPool } from '../components/study/quiz/studyQuizPlan';
import { isRubricCard } from '../types/markBank';

const sources = [
  { suffix: 'b2a', marks: 6, knownGuidance: /If not linked; mark both and disallow the lower mark/ },
  { suffix: 'c3d', marks: 9, knownGuidance: /4 @ 2m \(0\/2\)/ },
] as const;

function sourceCard(suffix: string) {
  const card = CARDS.find(candidate => candidate.id === `lcvp-2016-cl-${suffix}`);
  if (!card || isRubricCard(card) || card.tariffModel.kind !== 'questionTotal') {
    throw new Error(`Missing confidence-only source card ${suffix}`);
  }
  return card;
}

afterEach(cleanup);

describe('LCVP 2016 unresolved whole tasks in actual Session and quiz flows', () => {
  it('retains both printed totals while excluding the tasks from numeric quizzes', () => {
    const cards = sources.map(({ suffix }) => sourceCard(suffix));
    expect(cards.map(card => card.totalMarks)).toEqual([6, 9]);
    expect(cards.every(card => !isQuizCard(card))).toBe(true);
    expect(quizPool(cards, cards.flatMap(card => [card.topicId, ...(card.additionalTopicIds ?? [])]))).toEqual([]);
  });

  it.each(sources.flatMap(source => [false, true].map(paperLayout => ({ ...source, paperLayout }))))(
    'keeps source guidance without a numeric grade for $suffix in paper layout=$paperLayout',
    async ({ suffix, marks, knownGuidance, paperLayout }) => {
      const card = sourceCard(suffix);
      const onGrade = vi.fn();
      render(<SessionScreen paperLayout={paperLayout} cards={[card]} subjectLabel="LCVP Link Modules"
        onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);
      expect(screen.getAllByText(/^Confidence review/).length).toBeGreaterThan(0);
      expect(screen.queryByText(new RegExp(`^${marks}m$`))).not.toBeInTheDocument();
      expect(screen.queryByText(new RegExp(`^${marks} marks · Question`))).not.toBeInTheDocument();
      fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
      await waitFor(() => expect(screen.getAllByText(knownGuidance)[0]).toBeVisible());
      expect(screen.getByText(/Review your complete answer against the source guidance/)).toBeVisible();
      expect(screen.queryByRole('button', { name: /^Claim \d+ marks/ })).not.toBeInTheDocument();
      fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
      expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({
        cardId: card.id, grade: 'got', marksClaimed: 0, marksAvailable: 0,
      }));
    },
  );
});
