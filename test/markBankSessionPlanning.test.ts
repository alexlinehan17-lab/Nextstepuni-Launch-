import { describe, expect, test } from 'vitest';

import {
  MARK_BANK_SESSION_SIZE,
  nextSessionActionLabel,
  resolveSessionQueue,
  topicSessionSummary,
} from '@/components/MarkBank/sessionPlanning';
import type { CardMemory } from '@/components/MarkBank/scheduler';
import type { SecCard } from '@/types/markBank';

const NOW = Date.UTC(2026, 7, 14, 12);

const cards = (count: number): SecCard[] => Array.from({ length: count }, (_, index) => ({
  id: `card-${String(index + 1).padStart(2, '0')}`,
} as SecCard));

const settledMemory = (): CardMemory => ({
  s: 30,
  d: 5,
  last: NOW,
  reps: 1,
  lapses: 0,
  state: 2,
});

describe('Mark Bank session counts stay consistent across every screen', () => {
  test('a 23-card topic advertises the 12-card sitting and the full inventory separately', () => {
    const pool = cards(23);
    const queue = resolveSessionQueue(pool, {}, NOW);

    expect(queue).toHaveLength(MARK_BANK_SESSION_SIZE);
    expect(topicSessionSummary(pool.length, queue.length)).toEqual({
      primary: '12-card review',
      secondary: '23 total',
    });
  });

  test('the next button uses the actual 11-card queue, never a hard-coded twelve', () => {
    const pool = cards(23);
    const memories = Object.fromEntries(
      pool.slice(0, 12).map(card => [card.id, settledMemory()]),
    );
    const queue = resolveSessionQueue(pool, memories, NOW);

    expect(queue).toHaveLength(11);
    expect(nextSessionActionLabel(queue.length, true, 'Business')).toBe(
      'Review 11 cards from this topic',
    );
  });

  test('short topics expose their real size without implying a twelve-card sitting', () => {
    const pool = cards(7);
    const queue = resolveSessionQueue(pool, {}, NOW);

    expect(queue).toHaveLength(7);
    expect(topicSessionSummary(pool.length, queue.length)).toEqual({ primary: '7 cards' });
    expect(nextSessionActionLabel(queue.length, true, 'Business')).toBe(
      'Review 7 cards from this topic',
    );
  });

  test('subject-wide practice says that it may cross topics', () => {
    expect(nextSessionActionLabel(12, false, 'Business')).toBe(
      'Review 12 cards across Business',
    );
  });
});
