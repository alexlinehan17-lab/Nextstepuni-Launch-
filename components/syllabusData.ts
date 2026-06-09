/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Syllabus X-Ray data — now DERIVED from the single source of truth (curriculum.ts)
 * plus the prioritisation overlay (syllabusMeta.ts). Every topic here is a real
 * curriculum STRAND (with its subtopics), keyed by the same stable id that
 * Catch-Up Lane and Command-Word use — so the three tools can never describe the
 * syllabus differently. A guard test (test/syllabusSourceOfTruth.test.ts) asserts
 * every overlay key resolves to a curriculum node.
 */
import { CURRICULUM } from '../curriculum';
import { SYLLABUS_META } from '../syllabusMeta';

// ─── Types ───────────────────────────────────────────────────────────────────

export interface SyllabusSubtopic {
  id: string;
  name: string;
}

export interface SyllabusTopic {
  id: string;                // curriculum STRAND id (single source of truth)
  name: string;              // strand name
  section: string;           // paper/section label
  markWeight: number;        // approximate % of total marks this strand can occupy
  examFrequency: number;     // 1-10 (10 = appears every year)
  difficulty: number;        // 1-5 (5 = very hard)
  studyHours: number;        // estimated hours to study thoroughly
  tip: string;               // brief exam-specific advice
  subtopics: SyllabusSubtopic[];  // curriculum subtopics under this strand
}

export interface PaperInfo {
  name: string;
  marks: number;
  duration: string;
}

export interface SubjectSyllabus {
  subject: string;           // display name (curriculum subject name)
  subjectId: string;         // curriculum subject id
  totalMarks: number;
  papers: PaperInfo[];
  topics: SyllabusTopic[];
  keyAdvice: string;
}

// ─── Efficiency score: marks-per-hour weighted by exam frequency ─────────────

export function computeEfficiency(topic: SyllabusTopic, totalMarks: number): number {
  const potentialMarks = (topic.markWeight / 100) * totalMarks;
  const marksPerHour = potentialMarks / Math.max(1, topic.studyHours);
  const frequencyMultiplier = topic.examFrequency / 10;
  return Math.round(marksPerHour * frequencyMultiplier * 10) / 10;
}

export function getQuadrant(topic: SyllabusTopic): 'start-here' | 'high-value' | 'worth-knowing' | 'only-if-time' {
  const freqHigh = topic.examFrequency >= 7;
  const weightHigh = topic.markWeight >= 12;
  if (freqHigh && weightHigh) return 'start-here';
  if (freqHigh || weightHigh) return 'high-value';
  if (topic.examFrequency >= 4) return 'worth-knowing';
  return 'only-if-time';
}

export const QUADRANT_LABELS: Record<string, { label: string; color: string; bg: string }> = {
  'start-here': { label: 'Start Here', color: 'text-emerald-600 dark:text-emerald-400', bg: 'bg-emerald-100 dark:bg-emerald-900/30' },
  'high-value': { label: 'High Value', color: 'text-blue-600 dark:text-blue-400', bg: 'bg-blue-100 dark:bg-blue-900/30' },
  'worth-knowing': { label: 'Worth Knowing', color: 'text-amber-600 dark:text-amber-400', bg: 'bg-amber-100 dark:bg-amber-900/30' },
  'only-if-time': { label: 'Only If Time', color: 'text-zinc-500 dark:text-zinc-400', bg: 'bg-zinc-100 dark:bg-zinc-800' },
};

// ─── Subject Data — BUILT from curriculum.ts + syllabusMeta.ts ───────────────
// Single source of truth: a subject appears in Syllabus X-Ray iff it has both a
// curriculum entry and a prioritisation overlay. Topics = curriculum strands.

export const SYLLABUS_DATA: SubjectSyllabus[] = CURRICULUM
  .filter((subject) => SYLLABUS_META[subject.id])
  .map((subject) => {
    const meta = SYLLABUS_META[subject.id];
    const topics: SyllabusTopic[] = subject.strands
      .filter((strand) => meta.strands[strand.id])
      .map((strand) => {
        const sm = meta.strands[strand.id];
        return {
          id: strand.id,
          name: strand.name,
          section: sm.section,
          markWeight: sm.markWeight,
          examFrequency: sm.examFrequency,
          difficulty: sm.difficulty,
          studyHours: sm.studyHours,
          tip: sm.tip,
          subtopics: strand.subtopics.map((t) => ({ id: t.id, name: t.name })),
        };
      });
    return {
      subject: subject.name,
      subjectId: subject.id,
      totalMarks: meta.totalMarks,
      papers: meta.papers,
      topics,
      keyAdvice: meta.keyAdvice,
    };
  });

// ─── Helpers ─────────────────────────────────────────────────────────────────

export const AVAILABLE_SUBJECTS = SYLLABUS_DATA.map((s) => s.subject);

export function getSyllabusForSubject(subject: string): SubjectSyllabus | undefined {
  return SYLLABUS_DATA.find((s) => s.subject === subject || s.subjectId === subject);
}

// ─── Fuzzy Topic Matcher ────────────────────────────────────────────────────

function normalizeStr(s: string): string {
  return s.toLowerCase().replace(/[^a-z0-9\s]/g, '').trim();
}

function tokenize(s: string): string[] {
  return normalizeStr(s).split(/\s+/).filter((t) => t.length > 0);
}

export function fuzzyMatchTopic(subject: string, input: string): SyllabusTopic | null {
  if (!input || input.trim().length < 3) return null;
  const syllabus = getSyllabusForSubject(subject);
  if (!syllabus) return null;

  const normInput = normalizeStr(input);
  const inputTokens = tokenize(input);

  // 1. Exact match (normalized) — topic name or any subtopic name
  for (const topic of syllabus.topics) {
    if (normalizeStr(topic.name) === normInput) return topic;
    if (topic.subtopics.some((st) => normalizeStr(st.name) === normInput)) return topic;
  }

  // 2. Substring match (either direction)
  for (const topic of syllabus.topics) {
    const normTopic = normalizeStr(topic.name);
    if (normTopic.includes(normInput) || normInput.includes(normTopic)) return topic;
    if (topic.subtopics.some((st) => { const n = normalizeStr(st.name); return n.includes(normInput) || normInput.includes(n); })) return topic;
  }

  // 3. Token overlap (2+ shared tokens) against topic + subtopic names
  let bestMatch: SyllabusTopic | null = null;
  let bestOverlap = 0;
  for (const topic of syllabus.topics) {
    const topicTokens = tokenize([topic.name, ...topic.subtopics.map((st) => st.name)].join(' '));
    const overlap = inputTokens.filter((t) => topicTokens.some((tt) => tt.includes(t) || t.includes(tt))).length;
    if (overlap >= 2 && overlap > bestOverlap) {
      bestOverlap = overlap;
      bestMatch = topic;
    }
  }

  return bestMatch;
}
