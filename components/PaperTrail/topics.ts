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
import {
  curriculumNodeIdsForExamQuestion,
  examTopicDefinition,
  examTopicIdsForQuestion,
  examTopicLabel,
  examTopicTaxonomyFor,
  examQuestionTopicMappingsForSubject,
} from '../../data/examTopics/registry';
import { PAPER_TRAIL_INDEX } from '../../paperTrailData';

/** Normalise a paper label to a stable slot so P1 and P2 topic pools stay
 *  separate in the frequency counts. */
export const paperKeyOf = (label: string): string =>
  /\baural|listening\b/i.test(label)
    ? 'aural'
    : /\boral\b/i.test(label)
      ? 'oral'
      : /\b(two|2|ii)\b/i.test(label)
        ? 'p2'
        : /\b(one|1|i)\b/i.test(label)
          ? 'p1'
          : 'single';

/** One printed-question identity with translated editions collapsed. Art and
 * Music have independently selectable components that restart at Q1; legacy
 * Spanish uses one paper slot for both written and aural cards. Their
 * normalised booklet id must therefore remain in the logical key to prevent
 * false deduplication. */
export const logicalQuestionIdentity = (question: Pick<
  TopicSibling,
  'subjectId' | 'level' | 'year' | 'paperKey' | 'fileid' | 'n'
>): string => [
  question.subjectId,
  question.level,
  question.year,
  question.paperKey,
  question.subjectId === 'art' || question.subjectId === 'music' || question.subjectId === 'spanish'
    ? question.fileid.replace(/(?:EV|IV)(?=\.pdf$)/i, 'BV')
    : '',
  question.n,
].join('|');

export const topicLabel = (id: string): string => examTopicLabel(id) ?? TOPIC_LABELS[id] ?? id;

const canonicalTopicIds = (q: QuestionTopicTag): string[] =>
  [q.primary, q.secondary].filter((id): id is string => Boolean(id));

/**
 * Topic identities used by the student-facing Atlas.  Subjects move to their
 * audited exam taxonomy atomically: until a subject has one, its canonical
 * curriculum tags remain the browse structure.  Once registered, every local
 * question must have an explicit exam-topic association (policed by tests), so
 * no unclassified question can silently leak into or disappear from the UI.
 */
export function browseTopicIdsForQuestion(
  paper: Pick<PaperTopicTags, 'subjectId' | 'level' | 'year' | 'paperKey' | 'lang' | 'fileid'>,
  question: QuestionTopicTag,
): string[] {
  if (!examTopicTaxonomyFor(paper.subjectId)) return canonicalTopicIds(question);
  return examTopicIdsForQuestion(
    paper.subjectId,
    paper.level,
    paper.year,
    'main',
    question.n,
    paper.paperKey,
    paper.lang,
    paper.fileid,
  );
}

const questionHasTopic = (paper: PaperTopicTags, question: QuestionTopicTag, topicId: string): boolean => {
  if (examTopicDefinition(topicId)) return browseTopicIdsForQuestion(paper, question).includes(topicId);
  return question.primary === topicId || question.secondary === topicId;
};

// ─── indices (built once) ───────────────────────────────────

const paperId = (subjectId: string, year: number, level: string, lang: string, fileid: string) =>
  `${subjectId}|${year}|${level}|${lang}|${fileid}`;

/**
 * Merge a completed exam-topic audit into the local corpus without mutating or
 * replacing the verified canonical tag source.  This is what lets a newly
 * audited year become browsable immediately while retaining every pre-existing
 * tag verbatim. Multi-paper subjects join on an explicit paper slot so, for
 * example, a written Q1 can never collide with an aural Q1.
 */
const runtimePapersById = new Map<string, PaperTopicTags>();
// These three audited taxonomies have valid local cards deliberately retained
// outside the StudyClix reference, and one question booklet per paper slot.
// Other subjects can have separately numbered components even when an index
// entry appears singular, so their supplementation must remain file-scoped.
const FILELESS_RETENTION_SUBJECTS = new Set([
  'agricultural-science',
  'classical-studies',
  'politics-and-society',
]);
for (const source of PAPER_TOPIC_TAGS) {
  runtimePapersById.set(
    paperId(source.subjectId, source.year, source.level, source.lang, source.fileid),
    { ...source, q: source.q.map(question => ({ ...question })) },
  );
}

for (const [subjectId, entries] of Object.entries(PAPER_TRAIL_INDEX)) {
  if (!examTopicTaxonomyFor(subjectId)) continue;
  const mappings = examQuestionTopicMappingsForSubject(subjectId)
    .filter(mapping => mapping.sitting === 'main');
  for (const entry of entries) {
    for (const item of entry.papers) {
      const itemPaperKey = paperKeyOf(item.label);
      const candidateQuestions = mappings.filter(mapping =>
        mapping.year === entry.year
        && mapping.level === entry.level
        && mapping.paperKey === itemPaperKey
        && (mapping.lang === 'any' || mapping.lang === entry.lang));
      const fileQuestions = candidateQuestions.filter(mapping => mapping.fileid === item.doc.f);
      // Supplementation requires exact booklet-scoped evidence. Coarser
      // year/question mappings remain useful for classifying frozen source
      // cards, but using them to invent cards would merge independently
      // numbered components (for example Biology A/B vs C or Technology A
      // vs B/C).
      // A fileless mapping is safe only when this entry has exactly one
      // answer-mapped booklet in the slot. This retains explicitly audited
      // reference omissions on single-paper subjects without reintroducing
      // the Biology/Technology bug where several same-numbered component
      // booklets were merged together.
      const answerMappedSlotCount = entry.papers.filter(candidate =>
        candidate.answers === 1 && paperKeyOf(candidate.label) === itemPaperKey).length;
      const safeFilelessQuestions = FILELESS_RETENTION_SUBJECTS.has(subjectId)
        && answerMappedSlotCount === 1
        ? candidateQuestions.filter(mapping => !mapping.fileid)
        : [];
      // Exact StudyClix-derived mappings and retained local omissions are
      // complementary. A booklet can contain both, so do not discard its
      // safe fileless retention rows merely because at least one exact row
      // exists for the same paper.
      const questions = [...fileQuestions, ...safeFilelessQuestions];
      if (!questions.length) continue;
      // Atlas question jumps require a verified answer-map anchor. A full
      // paper remains available in Paper Trail even when its per-question
      // sidecar is not ready, but inventing rows would create dead jumps.
      if (item.answers !== 1) continue;
      const id = paperId(subjectId, entry.year, entry.level, entry.lang, item.doc.f);
      // Preserve every committed source question unchanged and append only
      // audited cards that are present in the same verified answer sidecar.
      // This closes genuine coverage gaps without replacing Mark Bank history.
      const paper = runtimePapersById.get(id) ?? {
        subjectId,
        level: entry.level,
        lang: entry.lang,
        year: entry.year,
        fileid: item.doc.f,
        paperKey: itemPaperKey,
        q: [],
      };
      if (!runtimePapersById.has(id)) runtimePapersById.set(id, paper);
      for (const mapping of questions) {
        // Comma/colon identities describe a grouped reference heading or a
        // semantic sub-task, not a selectable sidecar card. Their individual
        // cards are already represented by the source tags/crosswalk target.
        if (/[:,]/.test(mapping.n)) continue;
        if (paper.q.some(question => question.n === mapping.n)) continue;
        const canonicalIds = curriculumNodeIdsForExamQuestion(
          subjectId,
          entry.level,
          entry.year,
          'main',
          mapping.n,
          itemPaperKey,
          entry.lang,
          item.doc.f,
        );
        if (!canonicalIds[0]) continue;
        paper.q.push({
          n: mapping.n,
          primary: canonicalIds[0],
          secondary: canonicalIds[1],
        });
      }
      paper.q.sort((a, b) => Number(a.n) - Number(b.n));
    }
  }
}

const RUNTIME_TOPIC_TAGS = [...runtimePapersById.values()];
const byPaper = new Map<string, PaperTopicTags>();
for (const p of RUNTIME_TOPIC_TAGS) {
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
  for (const p of RUNTIME_TOPIC_TAGS) {
    if (p.subjectId !== subjectId || p.level !== level || p.paperKey !== paperKey) continue;
    yearsAll.add(p.year);
    if (p.q.some(q => questionHasTopic(p, q, subtopicId))) yearsHit.add(p.year);
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
  for (const p of RUNTIME_TOPIC_TAGS) {
    if (p.subjectId !== subjectId) continue;
    for (const q of p.q) {
      if (questionHasTopic(p, q, subtopicId)) {
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
  return [...new Set(RUNTIME_TOPIC_TAGS.map(p => p.subjectId))];
}

/** Distinct tagged years available for a subject — the honest denominator for a
 *  topic's "appears in N of M years" frequency. */
export function taggedYearsForSubject(subjectId: string): number {
  const years = new Set<number>();
  for (const p of RUNTIME_TOPIC_TAGS) if (p.subjectId === subjectId) years.add(p.year);
  return years.size;
}

export interface SubjectTopic {
  subtopicId: string;
  label: string;
  /** Distinct printed questions touching this topic. English and Irish
   *  editions are one question, not two. */
  count: number;
  /** Distinct tagged years it appears in. */
  years: number;
}

/** Every browse topic for a subject, with how many questions and years. An
 *  audited taxonomy is authoritative for the menu, so intentionally empty
 *  reference buckets remain visible with zero counts instead of disappearing. */
export function topicsForSubject(subjectId: string): SubjectTopic[] {
  const agg = new Map<string, { questions: Set<string>; years: Set<number> }>();
  for (const topic of examTopicTaxonomyFor(subjectId)?.topics ?? []) {
    agg.set(topic.id, { questions: new Set<string>(), years: new Set<number>() });
  }
  for (const p of RUNTIME_TOPIC_TAGS) {
    if (p.subjectId !== subjectId) continue;
    for (const q of p.q) {
      const questionKey = logicalQuestionIdentity({ ...p, n: q.n });
      for (const id of browseTopicIdsForQuestion(p, q)) {
        const cur = agg.get(id) ?? { questions: new Set<string>(), years: new Set<number>() };
        cur.questions.add(questionKey);
        cur.years.add(p.year);
        agg.set(id, cur);
      }
    }
  }
  return [...agg.entries()]
    .map(([id, v]) => ({ subtopicId: id, label: topicLabel(id), count: v.questions.size, years: v.years.size }))
    .sort((a, b) => b.count - a.count || a.label.localeCompare(b.label));
}

/** Candidate questions for a custom set: every tagged question in the subject
 *  (subtopicIds = null) or only those touching the chosen subtopics. Deduped by
 *  printed paper+question so overlapping topics and translated editions do not
 *  double-count the same task. English is preferred when both editions exist. */
export function questionsForTopics(subjectId: string, subtopicIds: string[] | null): TopicSibling[] {
  const want = subtopicIds && subtopicIds.length ? new Set(subtopicIds) : null;
  const byPrintedQuestion = new Map<string, TopicSibling>();
  for (const p of RUNTIME_TOPIC_TAGS) {
    if (p.subjectId !== subjectId) continue;
    for (const q of p.q) {
      const match = want
        ? [...canonicalTopicIds(q), ...browseTopicIdsForQuestion(p, q)].some(id => want.has(id))
        : true;
      if (!match) continue;
      const k = logicalQuestionIdentity({ ...p, n: q.n });
      const candidate = { subjectId: p.subjectId, level: p.level, lang: p.lang, year: p.year, fileid: p.fileid, paperKey: p.paperKey, n: q.n };
      const current = byPrintedQuestion.get(k);
      if (!current || (current.lang !== 'ev' && candidate.lang === 'ev')) byPrintedQuestion.set(k, candidate);
    }
  }
  return [...byPrintedQuestion.values()];
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
  const perYearQuestions = new Map<number, Set<string>>();
  const topicIds = new Set<string>();
  const questions = new Set<string>();
  for (const p of RUNTIME_TOPIC_TAGS) {
    if (p.subjectId !== subjectId) continue;
    for (const q of p.q) {
      const key = logicalQuestionIdentity({ ...p, n: q.n });
      questions.add(key);
      const yearQuestions = perYearQuestions.get(p.year) ?? new Set<string>();
      yearQuestions.add(key);
      perYearQuestions.set(p.year, yearQuestions);
      for (const id of browseTopicIdsForQuestion(p, q)) topicIds.add(id);
    }
  }
  const perYear = new Map([...perYearQuestions].map(([year, ids]) => [year, ids.size]));
  const years = [...perYear.keys()].sort((a, b) => a - b);
  const auditedTopicCount = examTopicTaxonomyFor(subjectId)?.topics.length;
  s = {
    questions: questions.size,
    topics: auditedTopicCount ?? topicIds.size,
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
  for (const p of RUNTIME_TOPIC_TAGS) {
    if (p.subjectId !== subjectId) continue;
    for (const q of p.q) {
      for (const id of browseTopicIdsForQuestion(p, q)) {
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
  const tagged = new Set(taggedIds);
  const out: AtlasStrand[] = [];
  const claimed = new Set<string>();
  const examTaxonomy = examTopicTaxonomyFor(subjectId);
  if (examTaxonomy) {
    const labelCounts = new Map<string, number>();
    const levelLabelCounts = new Map<string, number>();
    for (const group of examTaxonomy.groups) {
      labelCounts.set(group.label, (labelCounts.get(group.label) ?? 0) + 1);
      const levelLabel = `${group.level}|${group.label}`;
      levelLabelCounts.set(levelLabel, (levelLabelCounts.get(levelLabel) ?? 0) + 1);
    }
    for (const group of examTaxonomy.groups) {
      const ids = group.topicIds.filter(id => tagged.has(id));
      if (!ids.length) continue;
      const qualifiers: string[] = [];
      if ((labelCounts.get(group.label) ?? 0) > 1) {
        qualifiers.push(group.level === 'higher' ? 'Higher Level' : 'Ordinary Level');
        if ((levelLabelCounts.get(`${group.level}|${group.label}`) ?? 0) > 1 && group.course) {
          qualifiers.push(group.course === 'new' ? 'New Course' : 'Old Course');
        }
      }
      out.push({
        id: group.id,
        name: qualifiers.length ? `${qualifiers.join(' · ')} · ${group.label}` : group.label,
        subtopicIds: ids,
      });
      for (const id of ids) claimed.add(id);
    }
  }
  const subj = CURRICULUM.find(c => c.id === subjectId);
  for (const strand of examTaxonomy ? [] : (subj?.strands ?? [])) {
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
