import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import SessionScreen from '../components/MarkBank/SessionScreen';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { isQuizCard, quizPool } from '../components/study/quiz/studyQuizPlan';
import { isRubricCard } from '../types/markBank';

const sources = [
  { suffix: 'se', marks: 30, knownGuidance: /Deduct 1\/2 marks/ },
  { suffix: 'l1', marks: 20, knownGuidance: /Assign one mark: station/ },
  { suffix: 'l2', marks: 20, knownGuidance: /Award one mark: skating/ },
  { suffix: 'l3', marks: 20, knownGuidance: /Assign no marks: comedy/ },
  { suffix: 'l4', marks: 20, knownGuidance: /Accept answers written in Russian/ },
] as const;

function sourceCard(suffix: string) {
  const card = REVIEWED_CARDS.find(candidate => candidate.id === `ru-2019-hl-${suffix}`);
  if (!card || isRubricCard(card) || card.tariffModel.kind !== 'questionTotal') {
    throw new Error(`Missing confidence-only source card ${suffix}`);
  }
  return card;
}

afterEach(cleanup);

describe('Russian 2019 confidence-only integration', () => {
  it('excludes all five unresolved whole tasks from numeric quizzes', () => {
    const cards = sources.map(({ suffix }) => sourceCard(suffix));
    expect(cards.map(card => card.totalMarks)).toEqual(sources.map(source => source.marks));
    expect(cards.every(card => !isQuizCard(card))).toBe(true);
    expect(quizPool(cards, cards.flatMap(card => [card.topicId, ...(card.additionalTopicIds ?? [])]))).toEqual([]);
  });

  it.each(sources.flatMap(source => [false, true].map(paperLayout => ({ ...source, paperLayout }))))(
    'retains source guidance without a numeric grade for $suffix in paper layout=$paperLayout',
    async ({ suffix, marks, knownGuidance, paperLayout }) => {
      const card = sourceCard(suffix);
      const onGrade = vi.fn();
      render(<SessionScreen paperLayout={paperLayout} cards={[card]} subjectLabel="Russian"
        onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);

      expect(screen.getAllByText(/^Confidence review/).length).toBeGreaterThan(0);
      expect(screen.queryByText(new RegExp(`^${marks}m$`))).not.toBeInTheDocument();
      expect(screen.queryByText(new RegExp(`^${marks} marks · Question`))).not.toBeInTheDocument();
      fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
      await waitFor(() => expect(screen.getByText(suffix === 'se'
        ? /Neither interpretation is selected/
        : /The scheme does not supply full per-answer tariffs/)).toBeVisible());
      await waitFor(() => expect(screen.getAllByText(knownGuidance)[0]).toBeVisible());
      expect(screen.queryByText(new RegExp(`Assess.*against.*${marks}.mark total`))).not.toBeInTheDocument();
      expect(screen.getByText(/Review your complete answer against the source guidance/)).toBeVisible();
      expect(screen.queryByRole('button', { name: /^Claim \d+ marks/ })).not.toBeInTheDocument();

      fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
      expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({
        cardId: card.id, grade: 'got', marksClaimed: 0, marksAvailable: 0,
      }));
    },
  );
});
