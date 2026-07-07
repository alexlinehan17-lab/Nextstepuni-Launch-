/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the SINGLE SOURCE OF TRUTH: Syllabus X-Ray (syllabusData / syllabusMeta)
 * must derive entirely from curriculum.ts, so its topics/subtopics are the exact
 * same nodes — by stable id — that Catch-Up Lane and Command-Word use. This test
 * fails if the overlay ever references a subject/strand that isn't in the
 * curriculum, or if a Syllabus X-Ray topic stops resolving to a curriculum strand.
 */
import { describe, it, expect } from 'vitest';
import { CURRICULUM } from '../curriculum';
import { SYLLABUS_META, XRAY_EXCLUDED_STRANDS } from '../syllabusMeta';
import { SYLLABUS_DATA } from '../components/syllabusData';

const subjectById = new Map(CURRICULUM.map((s) => [s.id, s]));
const strandIdsBySubject = new Map(
  CURRICULUM.map((s) => [s.id, new Set(s.strands.map((st) => st.id))]),
);
const allStrandIds = new Set(CURRICULUM.flatMap((s) => s.strands.map((st) => st.id)));
const allSubtopicIds = new Set(CURRICULUM.flatMap((s) => s.strands.flatMap((st) => st.subtopics.map((t) => t.id))));

describe('Syllabus single source of truth', () => {
  it('every SYLLABUS_META subject id is a real curriculum subject', () => {
    for (const subjectId of Object.keys(SYLLABUS_META)) {
      expect(subjectById.has(subjectId), `overlay subject "${subjectId}" not in curriculum`).toBe(true);
    }
  });

  it('every overlay strand key resolves to a real curriculum strand of that subject', () => {
    for (const [subjectId, meta] of Object.entries(SYLLABUS_META)) {
      const valid = strandIdsBySubject.get(subjectId)!;
      for (const strandId of Object.keys(meta.strands)) {
        expect(valid.has(strandId), `overlay strand "${strandId}" not a strand of "${subjectId}"`).toBe(true);
      }
    }
  });

  it('every curriculum strand of an overlaid subject has overlay metadata OR a documented exclusion (no silent blind spots)', () => {
    for (const subjectId of Object.keys(SYLLABUS_META)) {
      const subject = subjectById.get(subjectId)!;
      const meta = SYLLABUS_META[subjectId];
      for (const strand of subject.strands) {
        const covered = meta.strands[strand.id] !== undefined || XRAY_EXCLUDED_STRANDS[strand.id] !== undefined;
        expect(covered, `strand "${strand.id}" of "${subjectId}" has neither overlay nor documented exclusion`).toBe(true);
      }
    }
  });

  it('X-Ray exclusions are real strands, carry a reason, and are not also overlaid', () => {
    for (const [strandId, reason] of Object.entries(XRAY_EXCLUDED_STRANDS)) {
      expect(allStrandIds.has(strandId), `excluded strand "${strandId}" is not a curriculum strand`).toBe(true);
      expect(reason.trim().length, `excluded strand "${strandId}" has no reason`).toBeGreaterThan(10);
      for (const meta of Object.values(SYLLABUS_META)) {
        expect(meta.strands[strandId], `"${strandId}" is both excluded and overlaid`).toBeUndefined();
      }
    }
  });

  it('Syllabus X-Ray topics + subtopics are real curriculum strand + subtopic ids', () => {
    for (const subject of SYLLABUS_DATA) {
      expect(subjectById.has(subject.subjectId), `X-Ray subject "${subject.subjectId}" not in curriculum`).toBe(true);
      for (const topic of subject.topics) {
        expect(allStrandIds.has(topic.id), `X-Ray topic "${topic.id}" is not a curriculum strand`).toBe(true);
        for (const st of topic.subtopics) {
          expect(allSubtopicIds.has(st.id), `X-Ray subtopic "${st.id}" is not a curriculum subtopic`).toBe(true);
        }
      }
    }
  });

  it('overlay metadata is well-formed (sane ranges, a tip)', () => {
    for (const [subjectId, meta] of Object.entries(SYLLABUS_META)) {
      expect(meta.totalMarks, `${subjectId}: bad totalMarks`).toBeGreaterThan(0);
      for (const [strandId, m] of Object.entries(meta.strands)) {
        expect(m.examFrequency >= 1 && m.examFrequency <= 10, `${strandId}: examFrequency out of range`).toBe(true);
        expect(m.difficulty >= 1 && m.difficulty <= 5, `${strandId}: difficulty out of range`).toBe(true);
        expect(m.studyHours, `${strandId}: bad studyHours`).toBeGreaterThan(0);
        expect(m.tip.trim().length, `${strandId}: empty tip`).toBeGreaterThan(0);
      }
    }
  });
});
