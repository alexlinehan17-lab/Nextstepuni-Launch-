/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — progress aggregation (feature C1). One place that reads the
 * student's self-marks, review deck and streak and turns them into the numbers
 * the dashboard renders: overall accuracy, accuracy by subject, weakest topics,
 * where marks are lost, deck status and streak. Reads localStorage (via the
 * stores); the clock is injected so it stays deterministic in tests.
 */

import { allMarks, type GapKind } from './attemptStore';
import { topicsForPaper } from './topics';
import { deckStats, type DeckStats } from './reviewStore';
import { getStreak, type StreakSummary } from './streakStore';
import { type PaperLang, type PaperLevel } from '../../types/paperTrail';

export interface SubjectAccuracy {
  subjectId: string;
  /** Questions self-marked in this subject. */
  n: number;
  /** Mean self-mark %, 0–100. */
  avg: number;
}

export interface WeakTopic {
  subjectId: string;
  subtopicId: string;
  count: number;
  avg: number;
}

export interface ProgressStats {
  /** Self-marked questions in total. */
  totalMarks: number;
  /** Mean self-mark % across every marked question. */
  overallAvg: number;
  /** Distinct papers the student has self-marked at least one question in. */
  papersPractised: number;
  subjects: SubjectAccuracy[];
  weakestTopics: WeakTopic[];
  gaps: Record<GapKind, number>;
  deck: DeckStats;
  streak: StreakSummary;
}

const ZERO_GAPS = (): Record<GapKind, number> => ({ content: 0, process: 0, careless: 0, timing: 0 });

export function computeProgress(uid: string | undefined, now: number): ProgressStats {
  const marks = allMarks(uid);
  const gaps = ZERO_GAPS();
  const papers = new Set<string>();
  const bySubject = new Map<string, { sum: number; n: number }>();
  const byTopic = new Map<string, { subjectId: string; subtopicId: string; sum: number; n: number }>();
  let sum = 0;

  for (const m of marks) {
    const pct = m.max ? (m.score / m.max) * 100 : m.score;
    sum += pct;
    if (m.gap) gaps[m.gap]++;
    papers.add(`${m.subjectId}|${m.year}|${m.level}|${m.lang}|${m.fileid}`);

    const s = bySubject.get(m.subjectId) ?? { sum: 0, n: 0 };
    s.sum += pct;
    s.n += 1;
    bySubject.set(m.subjectId, s);

    const tags = topicsForPaper(m.subjectId, m.year, m.level as PaperLevel, m.lang as PaperLang, m.fileid);
    const tag = tags?.q.find(q => q.n === m.n);
    if (tag) {
      const key = `${m.subjectId}|${tag.primary}`;
      const t = byTopic.get(key) ?? { subjectId: m.subjectId, subtopicId: tag.primary, sum: 0, n: 0 };
      t.sum += pct;
      t.n += 1;
      byTopic.set(key, t);
    }
  }

  const subjects: SubjectAccuracy[] = [...bySubject.entries()]
    .map(([subjectId, v]) => ({ subjectId, n: v.n, avg: Math.round(v.sum / v.n) }))
    .sort((a, b) => b.n - a.n || a.avg - b.avg);

  const weakestTopics: WeakTopic[] = [...byTopic.values()]
    .map(v => ({ subjectId: v.subjectId, subtopicId: v.subtopicId, count: v.n, avg: Math.round(v.sum / v.n) }))
    .sort((a, b) => a.avg - b.avg || b.count - a.count);

  return {
    totalMarks: marks.length,
    overallAvg: marks.length ? Math.round(sum / marks.length) : 0,
    papersPractised: papers.size,
    subjects,
    weakestTopics,
    gaps,
    deck: deckStats(uid, now),
    streak: getStreak(uid, now),
  };
}
