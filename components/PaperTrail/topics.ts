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
import { CURRICULUM } from '../../curriculum';

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

// ─── revision hub (browse by topic) ────────────────────────

/** Subject ids that have any committed topic tags. */
export function taggedSubjects(): string[] {
  return [...new Set(PAPER_TOPIC_TAGS.map(p => p.subjectId))];
}

/** Distinct tagged years available for a subject — the honest denominator for a
 *  topic's "appears in N of M years" frequency. */
export function taggedYearsForSubject(subjectId: string): number {
  const years = new Set<number>();
  for (const p of PAPER_TOPIC_TAGS) if (p.subjectId === subjectId) years.add(p.year);
  return years.size;
}

export interface SubjectTopic {
  subtopicId: string;
  label: string;
  /** Questions touching this subtopic (primary or secondary) — matches the
   *  drill list `siblingsFor` returns, so the counts line up. */
  count: number;
  /** Distinct tagged years it appears in. */
  years: number;
}

/** Every topic that appears in a subject's tagged papers, with how many
 *  questions and years — the browse list for the revision hub. Busiest first. */
export function topicsForSubject(subjectId: string): SubjectTopic[] {
  const agg = new Map<string, { count: number; years: Set<number> }>();
  for (const p of PAPER_TOPIC_TAGS) {
    if (p.subjectId !== subjectId) continue;
    for (const q of p.q) {
      for (const id of [q.primary, q.secondary]) {
        if (!id) continue;
        const cur = agg.get(id) ?? { count: 0, years: new Set<number>() };
        cur.count += 1;
        cur.years.add(p.year);
        agg.set(id, cur);
      }
    }
  }
  return [...agg.entries()]
    .map(([id, v]) => ({ subtopicId: id, label: topicLabel(id), count: v.count, years: v.years.size }))
    .sort((a, b) => b.count - a.count || a.label.localeCompare(b.label));
}

/** Candidate questions for a custom set: every tagged question in the subject
 *  (subtopicIds = null) or only those touching the chosen subtopics. Deduped by
 *  paper+question so a question tagged on two topics is not double-counted. */
export function questionsForTopics(subjectId: string, subtopicIds: string[] | null): TopicSibling[] {
  const want = subtopicIds && subtopicIds.length ? new Set(subtopicIds) : null;
  const seen = new Set<string>();
  const out: TopicSibling[] = [];
  for (const p of PAPER_TOPIC_TAGS) {
    if (p.subjectId !== subjectId) continue;
    for (const q of p.q) {
      const match = want ? want.has(q.primary) || (!!q.secondary && want.has(q.secondary)) : true;
      if (!match) continue;
      const k = `${p.level}|${p.lang}|${p.year}|${p.fileid}|${q.n}`;
      if (seen.has(k)) continue;
      seen.add(k);
      out.push({ subjectId: p.subjectId, level: p.level, lang: p.lang, year: p.year, fileid: p.fileid, paperKey: p.paperKey, n: q.n });
    }
  }
  return out;
}

export type { QuestionTopicTag };

// ─── atlas aggregates (subject shelf + unit-grouped topic map) ─────

export interface SubjectAtlasStats {
  questions: number;
  topics: number;
  yearMin: number;
  yearMax: number;
  /** Tagged years ascending — the denominator timeline for the year strips. */
  years: number[];
  /** Question count per tagged year (the shelf card's fingerprint bars). */
  perYear: Map<number, number>;
}

const statsMemo = new Map<string, SubjectAtlasStats>();

export function subjectAtlasStats(subjectId: string): SubjectAtlasStats {
  let s = statsMemo.get(subjectId);
  if (s) return s;
  const perYear = new Map<number, number>();
  const topicIds = new Set<string>();
  let questions = 0;
  for (const p of PAPER_TOPIC_TAGS) {
    if (p.subjectId !== subjectId) continue;
    perYear.set(p.year, (perYear.get(p.year) ?? 0) + p.q.length);
    questions += p.q.length;
    for (const q of p.q) {
      topicIds.add(q.primary);
      if (q.secondary) topicIds.add(q.secondary);
    }
  }
  const years = [...perYear.keys()].sort((a, b) => a - b);
  s = {
    questions,
    topics: topicIds.size,
    yearMin: years[0] ?? 0,
    yearMax: years[years.length - 1] ?? 0,
    years,
    perYear,
  };
  statsMemo.set(subjectId, s);
  return s;
}

/** Which tagged years each subtopic appears in — drives the per-topic year
 *  strip (one dot per tagged year, filled where the topic was asked). */
export function topicYearSets(subjectId: string): Map<string, Set<number>> {
  const out = new Map<string, Set<number>>();
  for (const p of PAPER_TOPIC_TAGS) {
    if (p.subjectId !== subjectId) continue;
    for (const q of p.q) {
      for (const id of [q.primary, q.secondary]) {
        if (!id) continue;
        let set = out.get(id);
        if (!set) out.set(id, (set = new Set()));
        set.add(p.year);
      }
    }
  }
  return out;
}

export interface AtlasStrand {
  id: string;
  name: string;
  subtopicIds: string[];
}

/** Curriculum strand grouping for a subject's tagged topics — topics whose id
 *  matches no strand gather under a trailing "Other topics" strand so nothing
 *  silently disappears from the map. */
export function strandsFor(subjectId: string, taggedIds: string[]): AtlasStrand[] {
  const subj = CURRICULUM.find(c => c.id === subjectId);
  const tagged = new Set(taggedIds);
  const out: AtlasStrand[] = [];
  const claimed = new Set<string>();
  for (const strand of subj?.strands ?? []) {
    const ids = strand.subtopics.map(t => t.id).filter(id => tagged.has(id));
    if (!ids.length) continue;
    out.push({ id: strand.id, name: strand.name, subtopicIds: ids });
    for (const id of ids) claimed.add(id);
  }
  const rest = taggedIds.filter(id => !claimed.has(id));
  if (rest.length) out.push({ id: '__other', name: out.length ? 'Other topics' : 'Topics', subtopicIds: rest });
  return out;
}

/** Curriculum category for a subject — drives the atlas's soft identity
 *  tints (small marks only; cards and rows stay white). */
export function categoryOf(subjectId: string): string {
  return CURRICULUM.find(c => c.id === subjectId)?.category ?? 'other';
}
