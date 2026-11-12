import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';
import MarkBankLibrary from '../components/MarkBank/MarkBankLibrary';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import type { SecCard } from '../types/markBank';

afterEach(cleanup);

function library(card: SecCard) {
  const onStart = vi.fn();
  render(<MarkBankLibrary subjectId="russian" level="higher" cards={[card]}
    state={{ v: 1, cards: {}, updatedAt: 0 }} now={() => Date.UTC(2026, 10, 12)}
    chooseSubject={vi.fn()} chooseLevel={vi.fn()} canSelectSubject={() => true}
    onStart={onStart} busy={false} ready loading={false} error={false}
    onRetry={vi.fn()} online />);
  const sample = screen.getByText(card.questionRef).closest('button');
  if (!sample) throw new Error('Missing startable library sample');
  return { sample, onStart };
}

it('labels the actual source conflict as confidence review before starting the full task', () => {
  const card = REVIEWED_CARDS.find(candidate => candidate.id === 'ru-2012-hl-c1-2-ii');
  if (!card) throw new Error('Missing reviewed source conflict');
  expect(card.totalMarks).toBe(6);
  const { sample, onStart } = library(card);
  expect(within(sample).getByText('Confidence review')).toBeVisible();
  expect(within(sample).queryByText('6')).not.toBeInTheDocument();
  expect(within(sample).queryByText('marks')).not.toBeInTheDocument();
  fireEvent.click(sample);
  expect(onStart).toHaveBeenCalledWith(expect.any(String), [card]);
});

it('retains the numeric preview for a source-priced task', () => {
  const card = REVIEWED_CARDS.find(candidate => candidate.id === 'ru-2012-hl-c1-1-i');
  if (!card) throw new Error('Missing priced comparison task');
  expect(card.totalMarks).toBe(4);
  const { sample } = library(card);
  expect(within(sample).getByText(String(card.totalMarks), { exact: true })).toBeVisible();
  expect(within(sample).getByText('marks')).toBeVisible();
  expect(within(sample).queryByText('Confidence review')).not.toBeInTheDocument();
});
