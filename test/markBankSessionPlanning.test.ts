import { describe, expect, test } from 'vitest';

import {
  MARK_BANK_SESSION_SIZE,
  listeningExerciseKey,
  nextSessionActionLabel,
  resolveSessionQueue,
  sessionExerciseCount,
  topicSessionSummary,
  visibleSessionExercises,
} from '@/components/MarkBank/sessionPlanning';
import { CARDS as IRISH_HIGHER } from '@/components/MarkBank/cards/irish/higher';
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

  test('never selects only part of an Irish listening section', () => {
    const conversations = IRISH_HIGHER.filter(card => card.topicId === 'irish-1-1');
    const queue = resolveSessionQueue(conversations, {}, NOW);

    expect(queue.length).toBeLessThanOrEqual(MARK_BANK_SESSION_SIZE);
    const selectedGroups = new Set(queue.map(listeningExerciseKey));
    for (const key of selectedGroups) {
      const selected = queue.filter(card => listeningExerciseKey(card) === key);
      const published = conversations.filter(card => listeningExerciseKey(card) === key);
      expect(selected.map(card => card.id)).toEqual(published.map(card => card.id));
    }
  });

  test('presents sibling listening cards as one visible exercise without deleting their ids', () => {
    const announcements = IRISH_HIGHER.filter(card =>
      card.year === 2025 && card.topicId === 'irish-1-0');

    expect(announcements).toHaveLength(2);
    expect(visibleSessionExercises(announcements).map(card => card.id)).toEqual([
      'irish-2025-hl-p1-listening-a-f1',
    ]);
    expect(sessionExerciseCount(announcements)).toBe(1);
    expect(new Set(announcements.map(card => card.id)).size).toBe(2);
  });
});
