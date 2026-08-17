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

  if (planned.length) return planned;

  // A deliberate practice tap should always open something. When every card is
  // already met and none is due, serve the weakest memories instead of making
  // the button appear broken.
  return [...pool]
    .sort((a, b) => {
      const difference = retrievability(memories[a.id] ?? NEW_CARD, now)
        - retrievability(memories[b.id] ?? NEW_CARD, now);
      return difference || a.id.localeCompare(b.id);
    })
    .slice(0, size);
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
