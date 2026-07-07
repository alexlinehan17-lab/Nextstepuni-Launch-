/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Coach — "your next 20 minutes", composed across every tool's signals.
 *
 * A pure composer (unit-tested, clock injected) that reads what already exists —
 * the review deck, the student's flashcards, the Examiner's Chair calibration
 * state (misses, codex recall, the Daily Mark) and the self-mark weakness map —
 * and turns it into 2–3 concrete next actions, most valuable first. Every
 * number comes from the student's own practice; when there is no signal there
 * is no card. Composition only — each destination tool owns its own logic.
 */

import { deckStats } from './reviewStore';
import { cardStats } from './flashcardStore';
import { computeProgress } from './progressStats';
import { topicLabel } from './topics';
import { codexDue, dailyDone, loadChair, topMisses } from '../ExaminersChair/store';

/** Where a coach item sends the student. Paper Trail views are handled
 * in-tool; 'chair' opens The Examiner's Chair via cross-tool routing. */
export type CoachRoute = 'review' | 'cards' | 'revise' | 'mock' | 'chair';

export interface CoachItem {
  id: string;
  /** Short imperative headline, e.g. "Clear 6 due reviews". */
  title: string;
  /** One-line why-this-now, in plain words. */
  sub: string;
  route: CoachRoute;
  /** Rough minutes, for the 20-minute budget line. */
  minutes: number;
}

/** Compose tonight's session — up to `n` actions, most valuable first. */
export function composeCoach(uid: string | undefined, now: number, n = 3): CoachItem[] {
  const items: CoachItem[] = [];

  // 1. Due spaced reviews decay fastest — they always lead.
  const deck = deckStats(uid, now);
  if (deck.due > 0) {
    items.push({
      id: 'review-due',
      title: `Clear ${deck.due} due review${deck.due === 1 ? '' : 's'}`,
      sub: 'Spaced retrieval — these are scheduled for today, and waiting makes them harder.',
      route: 'review',
      minutes: Math.max(2, Math.min(10, Math.ceil(deck.due * 0.5))),
    });
  }

  // 2. The student's own flashcards, if any are due.
  const cards = cardStats(uid, now);
  if (cards.due > 0) {
    items.push({
      id: 'cards-due',
      title: `Flip ${cards.due} of your own card${cards.due === 1 ? '' : 's'}`,
      sub: 'Cards you wrote yourself — due for recall today.',
      route: 'cards',
      minutes: Math.max(2, Math.min(8, Math.ceil(cards.due * 0.4))),
    });
  }

  // 3. Calibration: the Daily Mark keeps the streak; a known blind spot beats a
  //    random drill.
  const chair = loadChair(uid);
  const misses = topMisses(chair, 1);
  const codexRecallDue = codexDue(chair, chair.codex, now).length;
  if (!dailyDone(chair, now) && (chair.daily.streak > 0 || chair.codex.length > 0)) {
    items.push({
      id: 'daily-mark',
      title: 'The Daily Mark',
      sub: chair.daily.streak > 0
        ? `One shared script — your calibration streak is ${chair.daily.streak} day${chair.daily.streak === 1 ? '' : 's'}.`
        : 'One shared script a day keeps your marking eye calibrated.',
      route: 'chair',
      minutes: 4,
    });
  }
  if (misses.length > 0) {
    const m = misses[0];
    const generous = m.over >= m.under;
    items.push({
      id: 'blind-spot',
      title: `Re-mark your blind spot: ${m.label}`,
      sub: `You ${generous ? 'over-credit' : 'under-credit'} this rule more than any other — drill it in the Examiner's Chair.`,
      route: 'chair',
      minutes: 6,
    });
  } else if (codexRecallDue > 0) {
    items.push({
      id: 'codex-recall',
      title: `Recall ${codexRecallDue} marking rule${codexRecallDue === 1 ? '' : 's'}`,
      sub: 'Codex rules due for spaced re-testing in the Examiner’s Chair.',
      route: 'chair',
      minutes: 3,
    });
  }

  // 4. Weakest topic with enough attempts to be a real signal.
  const p = computeProgress(uid, now);
  const weak = p.weakestTopics.find(t => t.count >= 2 && t.avg < 66);
  if (weak) {
    items.push({
      id: 'weak-topic',
      title: `Drill ${topicLabel(weak.subtopicId)} (${weak.avg}%)`,
      sub: `Your weakest measured topic — ${weak.count} attempts say the marks are here.`,
      route: 'revise',
      minutes: 8,
    });
  }

  // 5. If timing is the dominant marks-killer, prescribe a clock.
  const lossTotal = Object.values(p.gapLoss).reduce((a, b) => a + b, 0);
  if (lossTotal > 0 && p.gapLoss.timing >= lossTotal / 2 && p.gaps.timing >= 2) {
    items.push({
      id: 'timing',
      title: 'One timed mock set',
      sub: 'Most of your lost marks die to the clock — practise against it, not just the content.',
      route: 'mock',
      minutes: 15,
    });
  }

  return items.slice(0, n);
}
