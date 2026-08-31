/**
 * Resolve the exact cards a Mark Bank sitting will contain, plus the small
 * pieces of copy that describe that sitting. Keeping these together prevents
 * the board, reviewer and close screen from inventing three different counts.
 */

import type { SecCard } from '../../types/markBank';
import {
  NEW_CARD,
  planSession,
  retrievability,
  type CardMemory,
} from './scheduler';

export const MARK_BANK_SESSION_SIZE = 12;

/**
 * Cards which share this key are questions for one listening section. They
 * stay separate for marking and spaced-repetition history, but must enter a
 * sitting together so the reviewer can keep one recording mounted while every
 * question for it remains visible.
 */
export function listeningExerciseKey(card: SecCard): string | null {
  if (!card.audioMaterial) return null;
  return [
    card.subjectId,
    card.year,
    card.level,
    card.topicId,
    card.audioMaterial.playbackUrl,
  ].join(':');
}

/**
 * The scheduler keeps each separately marked listening extract as a real card,
 * but the reviewer presents all extracts which share one recording section as
 * one exercise. Return the representatives the student should actually see,
 * preserving the scheduler's order without discarding any underlying cards.
 */
export function visibleSessionExercises(cards: SecCard[]): SecCard[] {
  const seen = new Set<string>();
  return cards.filter(card => {
    const key = listeningExerciseKey(card) ?? card.id;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

export const sessionExerciseCount = (cards: SecCard[]): number =>
  visibleSessionExercises(cards).length;

/** Complete each selected listening section without breaking the session cap. */
export function completeListeningExercises(
  planned: SecCard[],
  pool: SecCard[],
  size = MARK_BANK_SESSION_SIZE,
): SecCard[] {
  const groups = new Map<string, SecCard[]>();
  for (const card of pool) {
    const key = listeningExerciseKey(card);
    if (!key) continue;
    const group = groups.get(key) ?? [];
    group.push(card);
    groups.set(key, group);
  }

  const completed: SecCard[] = [];
  const seen = new Set<string>();
  for (const seed of planned) {
    if (seen.has(seed.id)) continue;
    const key = listeningExerciseKey(seed);
    const unit = key ? groups.get(key) ?? [seed] : [seed];
    const fresh = unit.filter(card => !seen.has(card.id));
    if (completed.length > 0 && completed.length + fresh.length > size) continue;
    for (const card of fresh) {
      completed.push(card);
      seen.add(card.id);
    }
    if (completed.length >= size) break;
  }
  return completed;
}

export function resolveSessionQueue(
  pool: SecCard[],
  memories: Record<string, CardMemory | undefined>,
  now: number,
  examTs?: number,
  size = MARK_BANK_SESSION_SIZE,
): SecCard[] {
  if (!pool.length || size <= 0) return [];

  const byId = new Map(pool.map(card => [card.id, card]));
  const plan = planSession(pool.map(card => card.id), memories, now, { size, examTs });
  const planned = plan.queue
    .map(id => byId.get(id))
    .filter((card): card is SecCard => Boolean(card));

  if (planned.length) return completeListeningExercises(planned, pool, size);

  // A deliberate practice tap should always open something. When every card is
  // already met and none is due, serve the weakest memories instead of making
  // the button appear broken.
  const fallback = [...pool]
    .sort((a, b) => {
      const difference = retrievability(memories[a.id] ?? NEW_CARD, now)
        - retrievability(memories[b.id] ?? NEW_CARD, now);
      return difference || a.id.localeCompare(b.id);
    })
    .slice(0, size);
  return completeListeningExercises(fallback, pool, size);
}

export interface TopicSessionSummary {
  primary: string;
  secondary?: string;
}

/** Copy for a topic row: distinguish the next sitting from the whole topic. */
export function topicSessionSummary(totalCards: number, nextSessionCards: number): TopicSessionSummary {
  if (totalCards <= 0) return { primary: 'No cards' };
  if (nextSessionCards > 0 && nextSessionCards < totalCards) {
    return {
      primary: `${nextSessionCards}-card review`,
      secondary: `${totalCards} total`,
    };
  }
  return { primary: `${totalCards} ${totalCards === 1 ? 'card' : 'cards'}` };
}

/** Copy for the close screen, derived from the queue the button will open. */
export function nextSessionActionLabel(
  nextSessionCards: number,
  topicSpecific: boolean,
  subjectLabel: string,
): string {
  const noun = nextSessionCards === 1 ? 'card' : 'cards';
  return topicSpecific
    ? `Review ${nextSessionCards} ${noun} from this topic`
    : `Review ${nextSessionCards} ${noun} across ${subjectLabel}`;
}
