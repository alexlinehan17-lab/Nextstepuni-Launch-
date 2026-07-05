/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — topic mastery (feature E2). Turns two honest signals into a
 * single "how well do you actually own this topic" score: the student's self-
 * mark accuracy on the topic, and the FSRS memory stability of their review
 * cards for it (how long recall holds). Mastery means *proven*, not visited —
 * a topic only reads high once you've both scored well and retained it.
 *
 * Reads the same localStorage stores as the rest of the loop; the scoring core
 * is pure so it can be unit-tested.
 */

import { allMarks } from './attemptStore';
import { loadDeck } from './reviewStore';
import { topicLabel, topicsForPaper } from './topics';
import { type PaperLang, type PaperLevel } from '../../types/paperTrail';

/** Stability (days) at which a card counts as fully retained for mastery. */
export const STRONG_STABILITY_DAYS = 21;

export interface TopicMastery {
  subjectId: string;
  subtopicId: string;
  label: string;
  /** 0–100 blended mastery. */
  mastery: number;
  /** Mean self-mark accuracy %, if any marks exist. */
  accuracy?: number;
  /** Retention score 0–100 from mean FSRS stability, if any cards exist. */
  retention?: number;
  /** How much evidence backs the score (marks + reviewed cards). */
  signals: number;
}

const clamp100 = (n: number) => Math.max(0, Math.min(100, n));

/** Blend the available signals. Accuracy and retention are each 0–100; when both
 *  exist they're averaged, otherwise the one present stands alone. Returns null
 *  if there's no evidence at all. */
export function computeMastery(accuracy: number | undefined, retention: number | undefined): number | null {
  if (accuracy != null && retention != null) return clamp100(Math.round((accuracy + retention) / 2));
  if (accuracy != null) return clamp100(Math.round(accuracy));
  if (retention != null) return clamp100(Math.round(retention));
  return null;
}

const retentionScore = (meanStability: number) => clamp100((meanStability / STRONG_STABILITY_DAYS) * 100);

interface Agg {
  accSum: number;
  accN: number;
  stabSum: number;
  stabN: number;
}

/** Mastery for every topic the student has touched in a subject, strongest last-
 *  built first. Only topics with at least one signal appear. */
export function masteryForSubject(uid: string | undefined, subjectId: string): TopicMastery[] {
  const agg = new Map<string, Agg>();
  const bump = (id: string, patch: Partial<Agg>) => {
    const cur = agg.get(id) ?? { accSum: 0, accN: 0, stabSum: 0, stabN: 0 };
    agg.set(id, {
      accSum: cur.accSum + (patch.accSum ?? 0),
      accN: cur.accN + (patch.accN ?? 0),
      stabSum: cur.stabSum + (patch.stabSum ?? 0),
      stabN: cur.stabN + (patch.stabN ?? 0),
    });
  };

  // Self-mark accuracy → topic (via the paper's tags).
  for (const m of allMarks(uid)) {
    if (m.subjectId !== subjectId) continue;
    const tags = topicsForPaper(m.subjectId, m.year, m.level as PaperLevel, m.lang as PaperLang, m.fileid);
    const primary = tags?.q.find(q => q.n === m.n)?.primary;
    if (!primary) continue;
    const pct = m.max ? (m.score / m.max) * 100 : m.score;
    bump(primary, { accSum: pct, accN: 1 });
  }

  // Review-card stability → topic (only cards actually reviewed).
  for (const c of loadDeck(uid)) {
    if (c.subjectId !== subjectId || !c.topicId || c.stability == null) continue;
    bump(c.topicId, { stabSum: c.stability, stabN: 1 });
  }

  const out: TopicMastery[] = [];
  for (const [id, a] of agg) {
    const accuracy = a.accN ? a.accSum / a.accN : undefined;
    const retention = a.stabN ? retentionScore(a.stabSum / a.stabN) : undefined;
    const mastery = computeMastery(accuracy, retention);
    if (mastery == null) continue;
    out.push({
      subjectId,
      subtopicId: id,
      label: topicLabel(id),
      mastery,
      accuracy: accuracy != null ? Math.round(accuracy) : undefined,
      retention: retention != null ? Math.round(retention) : undefined,
      signals: a.accN + a.stabN,
    });
  }
  return out.sort((a, b) => b.mastery - a.mastery || a.label.localeCompare(b.label));
}

/** Mastery for a single topic, or null if untouched. */
export function masteryFor(uid: string | undefined, subjectId: string, subtopicId: string): TopicMastery | null {
  return masteryForSubject(uid, subjectId).find(t => t.subtopicId === subtopicId) ?? null;
}

/** How many topics the student has taken to mastery (≥ threshold), across every
 *  subject they've touched — a motivating headline for the dashboard. */
export function masteredCount(uid: string | undefined, threshold = 80): number {
  const subjects = new Set<string>();
  for (const c of loadDeck(uid)) subjects.add(c.subjectId);
  for (const m of allMarks(uid)) subjects.add(m.subjectId);
  let n = 0;
  for (const s of subjects) n += masteryForSubject(uid, s).filter(t => t.mastery >= threshold).length;
  return n;
}
