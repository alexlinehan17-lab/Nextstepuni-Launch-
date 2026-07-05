/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — the "Daily 10" builder (feature E3). A daily retrieval set is
 * every card due today, topped up — when fewer than the target are due — with
 * real questions drawn from the student's weakest topics, so a session is always
 * a meaningful chunk of active recall rather than an empty "all caught up". The
 * top-up questions are added to the FSRS deck, so today's weakness becomes
 * tomorrow's scheduled review. All content is genuine SEC questions.
 */

import { computeProgress } from './progressStats';
import { siblingsFor } from './topics';
import { addCard, dueCards, hasCard } from './reviewStore';

export const DAILY_TARGET = 10;

/** Top the due set up to `target` from the weakest topics first. Returns how many
 *  cards were added. No-op once enough are already due, or when there's nothing
 *  weak to draw from (a brand-new student with no self-marks). */
export function topUpDaily(uid: string | undefined, now: number, target: number = DAILY_TARGET): number {
  let needed = target - dueCards(uid, now).length;
  if (needed <= 0) return 0;
  let added = 0;
  for (const topic of computeProgress(uid, now).weakestTopics) {
    if (needed <= 0) break;
    for (const sib of siblingsFor(topic.subjectId, topic.subtopicId)) {
      if (needed <= 0) break;
      const id = { subjectId: sib.subjectId, year: sib.year, level: sib.level, lang: sib.lang, fileid: sib.fileid, n: sib.n };
      if (hasCard(uid, id)) continue;
      addCard(uid, id, topic.subtopicId, now);
      added += 1;
      needed -= 1;
    }
  }
  return added;
}
