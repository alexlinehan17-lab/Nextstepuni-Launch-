/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Answer Architect — the mark-earning SKELETON of a top answer, browsable by
 * subject. Where Marking Lens (data/markingLens) answers "where did the 60 marks
 * go?" in situ beside one paper's crop, Answer Architect re-lenses the SAME
 * verified spine into the ordered BEATS a full-marks answer is built from: the
 * shape of the answer, then each beat you have to hit, in sequence.
 *
 * SOURCE OF TRUTH — DERIVED, NOT HAND-AUTHORED. This module is a read-only
 * projection of `MARKING_LENS` (data/markingLens), whose every entry is authored
 * ONLY from a filed SEC marking scheme (examiner-reports/) and machine-checked to
 * sum to its Available-Marks line. Answer Architect invents NO marking content of
 * its own — it maps each multi-part `QuestionLens` to an `AnswerSkeleton`, so it
 * can never drift from the schemes it mirrors: fix a lens entry at its source and
 * the skeleton follows. It carries the same SEC `source` attribution.
 *
 * Only genuinely multi-beat questions (parts.length >= 2) are projected: a
 * single-part 10-mark "short" is a mark-ladder, not an answer structure, and
 * belongs to Marking Lens alone. A subject with no multi-beat questions (e.g.
 * Geography, whose lens entries are all one-part) is simply not listed — exactly
 * as Diagram Vault only lists subjects that have verified figures.
 */

import { MARKING_LENS } from '../markingLens';
import type { QuestionLens } from '../markingLens/types';

/** Human labels for the lens subject ids (labels are not SEC claims). */
const SUBJECT_LABELS: Record<string, string> = {
  business: 'Business',
  physics: 'Physics',
  chemistry: 'Chemistry',
  'agricultural-science': 'Agricultural Science',
  biology: 'Biology',
  geography: 'Geography',
  economics: 'Economics',
  'home-economics-s-and-s': 'Home Economics',
  engineering: 'Engineering',
  'construction-studies': 'Construction Studies',
  'design-and-communication-graphics': 'Design & Communication Graphics',
};

const LEVEL_LABEL: Record<string, string> = {
  higher: 'Higher',
  ordinary: 'Ordinary',
  foundation: 'Foundation',
  common: 'Common',
};

/** One beat of the skeleton — a question part as an ordered build step. */
export interface AnswerBeat {
  /** 1-based position in the answer sequence. */
  order: number;
  /** Part label as printed on the paper, e.g. "(A)(ii)". May be empty. */
  part: string;
  /** What this beat must deliver (from the scheme's task line). */
  requirement: string;
  /** What actually earns the marks here — never more than the scheme allocates. */
  earns: string;
  /** Marks this beat carries. */
  marks: number;
}

/** The full-marks skeleton for one real past-paper question. */
export interface AnswerSkeleton {
  /** Stable id: subject|year|level|lang|fileid|n. */
  id: string;
  subjectId: string;
  subjectLabel: string;
  year: number;
  /** 'higher' | 'ordinary' | 'foundation' | 'common'. */
  level: string;
  /** e.g. "Question 1". */
  questionRef: string;
  /** The shape of the answer — one line, from the scheme's marking model. */
  structure: string;
  /** The ordered mark-earning beats. */
  beats: AnswerBeat[];
  /** Total marks — equals the sum of the beats (machine-checked). */
  totalMarks: number;
  /** SEC attribution string. */
  source: string;
  /** An examiner-documented beat students skip, when the lens carries one. */
  pitfall?: { text: string; cite: string };
}

const idFor = (subjectId: string, e: QuestionLens): string =>
  `${subjectId}|${e.year}|${e.level}|${e.lang}|${e.fileid}|${e.n}`;

const skeletonFrom = (subjectId: string, e: QuestionLens): AnswerSkeleton => ({
  id: idFor(subjectId, e),
  subjectId,
  subjectLabel: SUBJECT_LABELS[subjectId] ?? subjectId,
  year: e.year,
  level: e.level,
  questionRef: `Question ${e.n}`,
  structure: e.headline,
  beats: e.parts.map((p, i) => ({
    order: i + 1,
    part: p.part,
    requirement: p.task,
    earns: p.decoded,
    marks: p.marks,
  })),
  totalMarks: e.totalMarks,
  source: `${e.cite} — © State Examinations Commission`,
  pitfall: e.pitfall,
});

// Project only multi-beat questions (parts.length >= 2). The EV/IV language
// mirror in the lens data means one exam appears twice (ev + iv); we keep only
// one skeleton per (subject, year, level, question) so the browser shows each
// real question once. EV is preferred; an IV-only question still surfaces.
const bySkeletonKey = new Map<string, AnswerSkeleton>();
for (const s of MARKING_LENS) {
  for (const e of s.entries) {
    if ((e.parts?.length ?? 0) < 2) continue;
    const dedupeKey = `${s.subjectId}|${e.year}|${e.level}|${e.n}`;
    const existing = bySkeletonKey.get(dedupeKey);
    if (existing && e.lang !== 'ev') continue; // keep the first / prefer EV
    if (!existing || e.lang === 'ev') bySkeletonKey.set(dedupeKey, skeletonFrom(s.subjectId, e));
  }
}

/** All answer skeletons, ordered subject → year desc → question. */
export const ANSWER_SKELETONS: AnswerSkeleton[] = [...bySkeletonKey.values()].sort(
  (a, b) =>
    a.subjectLabel.localeCompare(b.subjectLabel) ||
    b.year - a.year ||
    a.questionRef.localeCompare(b.questionRef, undefined, { numeric: true }),
);

export interface ArchitectSubject {
  id: string;
  label: string;
  count: number;
}

/** Subjects that have at least one skeleton, with counts, alphabetical. */
export function architectSubjects(): ArchitectSubject[] {
  const m = new Map<string, ArchitectSubject>();
  for (const s of ANSWER_SKELETONS) {
    const found = m.get(s.subjectId);
    if (found) found.count += 1;
    else m.set(s.subjectId, { id: s.subjectId, label: s.subjectLabel, count: 1 });
  }
  return [...m.values()].sort((a, b) => a.label.localeCompare(b.label));
}

/** The skeletons for one subject, newest first. */
export function skeletonsForSubject(subjectId: string): AnswerSkeleton[] {
  return ANSWER_SKELETONS.filter(s => s.subjectId === subjectId);
}

/** A short human label for a skeleton's level, e.g. "Higher". */
export function levelLabel(level: string): string {
  return LEVEL_LABEL[level] ?? level;
}
