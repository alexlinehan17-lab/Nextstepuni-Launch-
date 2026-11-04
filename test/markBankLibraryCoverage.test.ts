import { expect, test } from 'vitest';
import { builtDecks, loadCards } from '../components/MarkBank/deck';
import { libraryGroups, libraryTopicId, libraryTopicIds, libraryCardsForTopic, libraryYearsLabel } from '../components/MarkBank/libraryGroups';

test('year labels expose missing years rather than implying a continuous archive', () => {
  expect(libraryYearsLabel([2010, 2021, 2022, 2023, 2024, 2025, 2026]))
    .toBe('2010, 2021–2026');
  expect(libraryYearsLabel([2025, 2021, 2023, 2023, 2022])).toBe('2021–2023, 2025');
  expect(libraryYearsLabel([2026])).toBe('2026');
  expect(libraryYearsLabel([])).toBe('');
});

test('every published card remains reachable through the canonical subject index', async () => {
  const missing: string[] = [];
  for (const {subjectId,level} of builtDecks()) {
    const cards = await loadCards(subjectId, level);
    const visible = new Set(libraryGroups(subjectId,cards).flatMap(group=>group.topics.map(topic=>topic.id)));
    for (const card of cards) for (const topicId of libraryTopicIds(card)) if (!visible.has(topicId)) missing.push(`${card.id}: ${topicId}`);
  }
  expect(missing).toEqual([]);
}, 120000);

test('legacy Arabic aliases resolve to a startable canonical topic without changing card identity', async () => {
  const cards = await loadCards('arabic','higher');
  const legacy = cards.find(card => card.topicId === 'arabic-3-2')!;
  const topicId = libraryTopicId(legacy);
  expect(topicId).toBe('arabic-2026-reading-comprehension');
  expect(libraryCardsForTopic(topicId,cards)).toContain(legacy);
  expect(legacy.topicId).toBe('arabic-3-2');
});
