/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the SINGLE SOURCE OF TRUTH: Syllabus X-Ray (syllabusData / syllabusMeta)
 * must derive entirely from the versioned registry, so its topics/subtopics are the exact
 * same nodes — by stable id — that Catch-Up Lane and Command-Word use. This test
 * fails if the overlay ever references a subject/strand that isn't in the
 * curriculum, or if a Syllabus X-Ray topic stops resolving to a curriculum strand.
 */
import { describe, it, expect } from 'vitest';
import {
  CURRICULUM_SPECIFICATIONS,
  specificationContainsId,
  specificationsForSubject,
} from '../curriculumRegistry';
import { SYLLABUS_META, XRAY_EXCLUDED_STRANDS } from '../syllabusMeta';
import { SYLLABUS_DATA } from '../components/syllabusData';

const subjectIds = new Set(CURRICULUM_SPECIFICATIONS.map((specification) => specification.subjectId));
const allNodeIds = new Set(CURRICULUM_SPECIFICATIONS.flatMap((specification) =>
  specification.groups.flatMap((group) => [group.id, ...group.topics.map((topic) => topic.id)])));

describe('Syllabus single source of truth', () => {
  it('every SYLLABUS_META subject id is a real curriculum subject', () => {
    for (const subjectId of Object.keys(SYLLABUS_META)) {
      expect(subjectIds.has(subjectId), `overlay subject "${subjectId}" not in registry`).toBe(true);
    }
  });

  it('every overlay strand key resolves to a real curriculum strand of that subject', () => {
    for (const [subjectId, meta] of Object.entries(SYLLABUS_META)) {
      for (const strandId of Object.keys(meta.strands)) {
        expect(specificationsForSubject(subjectId).some((specification) => specificationContainsId(specification, strandId)),
          `overlay strand "${strandId}" not in any specification for "${subjectId}"`).toBe(true);
      }
    }
  });

  it('every curriculum strand of an overlaid subject has overlay metadata OR a documented exclusion (no silent blind spots)', () => {
    for (const subjectId of Object.keys(SYLLABUS_META)) {
      const meta = SYLLABUS_META[subjectId];
      const compatible = specificationsForSubject(subjectId).find((specification) =>
        Object.keys(meta.strands).every((id) => specificationContainsId(specification, id)));
      expect(compatible, `${subjectId} has no specification compatible with its X-Ray overlay`).toBeDefined();
      for (const group of compatible?.groups ?? []) {
        const covered = meta.strands[group.id] !== undefined || XRAY_EXCLUDED_STRANDS[group.id] !== undefined;
        expect(covered, `group "${group.id}" of "${subjectId}" has neither overlay nor documented exclusion`).toBe(true);
      }
    }
  });

  it('X-Ray exclusions are real strands, carry a reason, and are not also overlaid', () => {
    for (const [strandId, reason] of Object.entries(XRAY_EXCLUDED_STRANDS)) {
      expect(allNodeIds.has(strandId), `excluded group "${strandId}" is not a registry node`).toBe(true);
      expect(reason.trim().length, `excluded strand "${strandId}" has no reason`).toBeGreaterThan(10);
      for (const meta of Object.values(SYLLABUS_META)) {
        expect(meta.strands[strandId], `"${strandId}" is both excluded and overlaid`).toBeUndefined();
      }
    }
  });

  it('Syllabus X-Ray topics + subtopics are real curriculum strand + subtopic ids', () => {
    for (const subject of SYLLABUS_DATA) {
      const specification = CURRICULUM_SPECIFICATIONS.find((entry) => entry.id === subject.specificationId);
      expect(specification, `X-Ray specification "${subject.specificationId}" not in registry`).toBeDefined();
      for (const topic of subject.topics) {
        expect(specificationContainsId(specification!, topic.id), `X-Ray topic "${topic.id}" is not in ${subject.specificationId}`).toBe(true);
        for (const st of topic.subtopics) {
          expect(specificationContainsId(specification!, st.id), `X-Ray subtopic "${st.id}" is not in ${subject.specificationId}`).toBe(true);
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
