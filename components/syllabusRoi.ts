/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Syllabus X-Ray — personal ROI overlay (feature F6). Joins the X-Ray's
 * historical marks-per-strand weighting with the student's OWN Paper Trail
 * self-mark accuracy to rank where the most room to gain is: strands that
 * historically carried a lot of marks AND where the student's measured
 * accuracy is currently low.
 *
 * The join is exact, not fuzzy: Paper Trail's per-question topic tags are
 * curriculum SUBTOPIC ids (data/paperTrail/topicTags.ts), and each X-Ray
 * topic is a curriculum STRAND carrying those subtopics — both sides key off
 * curriculum.ts, so a self-mark maps to its strand via the subtopic id.
 *
 * Honesty rules (accreditation):
 *  - No prediction claims. Every number is either "this strand historically
 *    carried ~X marks" (syllabus weighting) or "your measured accuracy is Y%"
 *    (the student's own self-marks). "Room to gain" is just their product.
 *  - Only strands the student has actually self-marked appear — an
 *    unpractised strand is unknown, not "weak", so it is never ranked.
 *  - Marks whose tag doesn't resolve to an X-Ray strand are skipped; if
 *    nothing joins (or the ≥3-mark evidence gate isn't met) the result is
 *    null and the UI renders nothing rather than a fuzzy guess.
 *
 * Reads localStorage via the Paper Trail stores; the scoring core is pure so
 * it can be unit-tested with synthetic marks.
 */

import { allMarks, type StoredMark } from './PaperTrail/attemptStore';
import { topicsForPaper } from './PaperTrail/topics';
import { type SubjectSyllabus, type SyllabusTopic } from './syllabusData';
import { type PaperLang, type PaperLevel } from '../types/paperTrail';

/** Minimum self-marks in a subject before the overlay says anything at all. */
export const MIN_SUBJECT_MARKS = 3;

export interface RoiEntry {
  /** Curriculum strand id (the X-Ray topic id). */
  topicId: string;
  topicName: string;
  /** Marks this strand has historically carried (markWeight % of the total). */
  historicalMarks: number;
  /** The student's measured self-mark accuracy on this strand, 0–100. */
  accuracy: number;
  /** Self-marked questions behind that accuracy figure. */
  sampleSize: number;
  /** historicalMarks × (1 − accuracy/100) — the "most room to gain" rank key. */
  roomToGain: number;
}

export interface SubjectRoi {
  subjectId: string;
  /** Total self-marks the student has in this subject (the evidence gate). */
  totalSelfMarks: number;
  /** Measured strands with room to gain, most room first. */
  entries: RoiEntry[];
}

/** Default tag resolver: question → primary curriculum subtopic id, via the
 *  committed per-paper topic tags (same lookup topicMastery.ts uses). */
const resolvePrimaryTag = (m: StoredMark): string | undefined =>
  topicsForPaper(m.subjectId, m.year, m.level as PaperLevel, m.lang as PaperLang, m.fileid)
    ?.q.find(q => q.n === m.n)?.primary;

/** Pure core: rank a subject's X-Ray strands by room to gain, given the
 *  student's self-marks. Returns null when the evidence gate isn't met or
 *  when no mark joins onto an X-Ray strand (show nothing, never guess). */
export function roiFromMarks(
  syllabus: SubjectSyllabus,
  marks: StoredMark[],
  resolveTag: (m: StoredMark) => string | undefined = resolvePrimaryTag,
): SubjectRoi | null {
  const subjectMarks = marks.filter(m => m.subjectId === syllabus.subjectId);
  if (subjectMarks.length < MIN_SUBJECT_MARKS) return null;

  // Curriculum subtopic id → its X-Ray strand (both come from curriculum.ts).
  const strandOfSubtopic = new Map<string, SyllabusTopic>();
  for (const topic of syllabus.topics) {
    for (const st of topic.subtopics) strandOfSubtopic.set(st.id, topic);
  }

  const agg = new Map<string, { sum: number; n: number }>();
  for (const m of subjectMarks) {
    const subtopicId = resolveTag(m);
    if (!subtopicId) continue; // untagged question — no honest join
    const strand = strandOfSubtopic.get(subtopicId);
    if (!strand) continue; // tag exists but isn't an X-Ray strand — skip, don't guess
    const pct = m.max ? (m.score / m.max) * 100 : m.score;
    const cur = agg.get(strand.id) ?? { sum: 0, n: 0 };
    cur.sum += pct;
    cur.n += 1;
    agg.set(strand.id, cur);
  }
  if (agg.size === 0) return null;

  const entries: RoiEntry[] = [];
  for (const topic of syllabus.topics) {
    const a = agg.get(topic.id);
    if (!a) continue; // unpractised strand: unknown, not weak — never ranked
    const accuracy = Math.round(a.sum / a.n);
    const historicalMarks = Math.round((topic.markWeight / 100) * syllabus.totalMarks);
    const roomToGain = Math.round((historicalMarks * (100 - accuracy)) / 100);
    if (roomToGain <= 0) continue; // fully accurate here — nothing left to gain
    entries.push({
      topicId: topic.id,
      topicName: topic.name,
      historicalMarks,
      accuracy,
      sampleSize: a.n,
      roomToGain,
    });
  }
  if (entries.length === 0) return null;

  entries.sort((a, b) => b.roomToGain - a.roomToGain || a.accuracy - b.accuracy);
  return { subjectId: syllabus.subjectId, totalSelfMarks: subjectMarks.length, entries };
}

/** localStorage-backed entry point for the X-Ray UI. */
export function computeSubjectRoi(uid: string | undefined, syllabus: SubjectSyllabus): SubjectRoi | null {
  return roiFromMarks(syllabus, allMarks(uid));
}
