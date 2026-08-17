/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the single curriculum source of truth used by War Room Subject
 * Coverage. Student-facing nodes must come directly from a verified,
 * cohort-resolved registry record and must not regain unsupported scoring
 * overlays such as frequency, difficulty or marks-per-hour estimates.
 */
import { describe, expect, it } from 'vitest';
import { getSyllabusTopicRefs } from '../components/syllabusTopics';
import {
  CURRICULUM_SPECIFICATIONS,
  resolveCurriculumSpecification,
} from '../curriculumRegistry';

function representativeYear(firstExamYear?: number, lastExamYear?: number): number {
  if (firstExamYear !== undefined) return firstExamYear;
  if (lastExamYear !== undefined) return lastExamYear;
  return 2027;
}

describe('War Room curriculum source of truth', () => {
  it('reproduces exactly the declared coverage nodes for every active verified specification', () => {
    let checked = 0;
    for (const specification of CURRICULUM_SPECIFICATIONS.filter(({ status }) => status === 'verified')) {
      const examYear = representativeYear(specification.firstExamYear, specification.lastExamYear);
      if (resolveCurriculumSpecification(specification.subjectId, examYear)?.id !== specification.id) continue;

      const expected = specification.coverageNodeLevel === 'topic'
        ? specification.groups.flatMap((group) => group.topics.map(({ id, title, code }) => ({
            id,
            name: title,
            code,
            specificationId: specification.id,
          })))
        : specification.groups.map(({ id, title, code }) => ({
            id,
            name: title,
            code,
            specificationId: specification.id,
          }));
      const actual = getSyllabusTopicRefs(specification.subjectId, `${examYear}-06-05`);
      expect(actual, specification.id).toEqual(expected);
      checked += 1;
    }
    expect(checked).toBeGreaterThan(20);
  });

  it('hides active audit-required imports instead of presenting them as official', () => {
    let hidden = 0;
    for (const specification of CURRICULUM_SPECIFICATIONS.filter(({ status }) => status !== 'verified')) {
      const examYear = representativeYear(specification.firstExamYear, specification.lastExamYear);
      if (resolveCurriculumSpecification(specification.subjectId, examYear)?.id !== specification.id) continue;
      expect(getSyllabusTopicRefs(specification.subjectId, `${examYear}-06-05`), specification.id).toEqual([]);
      hidden += 1;
    }
    expect(hidden).toBeGreaterThan(0);
  });

  it('contains no unsupported predictive fields in student-facing coverage nodes', () => {
    const forbidden = ['examFrequency', 'difficulty', 'studyHours', 'markWeight', 'marksPerHour', 'efficiency'];
    for (const subject of ['Biology', 'English', 'Geography', 'Engineering', 'Mathematics']) {
      for (const node of getSyllabusTopicRefs(subject, '2028-06-05')) {
        for (const field of forbidden) expect(node, `${subject} unexpectedly exposes ${field}`).not.toHaveProperty(field);
      }
    }
  });
});
