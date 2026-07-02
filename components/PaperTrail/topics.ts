/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — topic-tag runtime helpers: look up a paper's tags, compute a
 * subtopic's cross-year frequency within its (subject, level, paper-slot) pool,
 * and gather every sibling question for cross-year jumping.
 */

import { PAPER_TOPIC_TAGS, TOPIC_LABELS } from '../../data/paperTrail/topicTags';
import { type PaperTopicTags, type QuestionTopicTag } from '../../types/paperTrailTopics';
import { type PaperLang, type PaperLevel } from '../../types/paperTrail';

/** Normalise a paper label to a stable slot so P1 and P2 topic pools stay
 *  separate in the frequency counts. */
export const paperKeyOf = (label: string): string =>
  /\b(two|2|ii)\b/i.test(label) ? 'p2' : /\b(one|1|i)\b/i.test(label) ? 'p1' : 'single';

export const topicLabel = (id: string): string => TOPIC_LABELS[id] ?? id;

// ─── indices (built once) ───────────────────────────────────

const byPaper = new Map<string, PaperTopicTags>();
const paperId = (subjectId: string, year: number, level: string, lang: string, fileid: string) =>
  `${subjectId}|${year}|${level}|${lang}|${fileid}`;
for (const p of PAPER_TOPIC_TAGS) {
  byPaper.set(paperId(p.subjectId, p.year, p.level, p.lang, p.fileid), p);
}

export function topicsForPaper(
  subjectId: string,
  year: number,
  level: PaperLevel,
  lang: PaperLang,
  fileid: string,
): PaperTopicTags | null {
  return byPaper.get(paperId(subjectId, year, level, lang, fileid)) ?? null;
}

// ─── frequency (within a subject/level/paper-slot pool) ─────

export interface TopicFrequency {
  /** Distinct tagged years in this pool where the subtopic appears. */
  yearsWith: number[];
  /** Distinct tagged years in this pool (the denominator). */
  totalYears: number;
}

/** How often `subtopicId` appears across the tagged years of the same subject,
 *  level and paper-slot — the honest "appeared in N of M tagged years". */
export function frequencyFor(
  subjectId: string,
  level: PaperLevel,
  paperKey: string,
  subtopicId: string,
): TopicFrequency {
  const yearsAll = new Set<number>();
  const yearsHit = new Set<number>();
  for (const p of PAPER_TOPIC_TAGS) {
    if (p.subjectId !== subjectId || p.level !== level || p.paperKey !== paperKey) continue;
    yearsAll.add(p.year);
    if (p.q.some(q => q.primary === subtopicId || q.secondary === subtopicId)) yearsHit.add(p.year);
  }
  return { yearsWith: [...yearsHit].sort((a, b) => b - a), totalYears: yearsAll.size };
}

// ─── siblings (cross-year jump) ─────────────────────────────

export interface TopicSibling {
  subjectId: string;
  level: PaperLevel;
  lang: PaperLang;
  year: number;
  fileid: string;
  paperKey: string;
  n: string;
}

/** Every question tagged with `subtopicId` across the subject's tagged papers —
 *  the "drill this topic across years" set. Newest first. */
export function siblingsFor(subjectId: string, subtopicId: string): TopicSibling[] {
  const out: TopicSibling[] = [];
  for (const p of PAPER_TOPIC_TAGS) {
    if (p.subjectId !== subjectId) continue;
    for (const q of p.q) {
      if (q.primary === subtopicId || q.secondary === subtopicId) {
        out.push({
          subjectId: p.subjectId,
          level: p.level,
          lang: p.lang,
          year: p.year,
          fileid: p.fileid,
          paperKey: p.paperKey,
          n: q.n,
        });
      }
    }
  }
  return out.sort((a, b) => b.year - a.year || a.level.localeCompare(b.level) || Number(a.n) - Number(b.n));
}

export type { QuestionTopicTag };
