/** @license SPDX-License-Identifier: Apache-2.0 */

/**
 * Leaving Cert coverage nodes resolved through the versioned curriculum
 * registry.  The examination date selects the student's actual specification;
 * callers must not maintain their own subject-topic arrays.
 */
import {
  CURRICULUM_SPECIFICATIONS,
  examinationYearFromDate,
  resolveCurriculumSpecification,
  type CanonicalCurriculumSpecification,
} from '../curriculumRegistry';

export interface SyllabusCoverageTopic {
  id: string;
  name: string;
  specificationId: string;
  code?: string;
}

function coverageNodes(specification: CanonicalCurriculumSpecification): SyllabusCoverageTopic[] {
  if (specification.coverageNodeLevel === 'topic') {
    return specification.groups.flatMap((group) => group.topics.map((topic) => ({
      id: topic.id,
      name: topic.title,
      code: topic.code,
      specificationId: specification.id,
    })));
  }
  return specification.groups.map((group) => ({
    id: group.id,
    name: group.title,
    code: group.code,
    specificationId: specification.id,
  }));
}

/**
 * Canonical coverage nodes for a student's actual examination cohort.
 * Passing the exam date is strongly preferred; the current academic cohort is
 * only used as a safe fallback for older callers.
 */
export function getSyllabusTopicRefs(
  subjectName: string,
  examDate?: string | null,
): SyllabusCoverageTopic[] {
  const specification = resolveCurriculumSpecification(
    subjectName,
    examinationYearFromDate(examDate),
  );
  return specification ? coverageNodes(specification) : [];
}

/**
 * Returns the student-facing labels for the canonical coverage nodes.
 */
export function getSyllabusTopics(subjectName: string, examDate?: string | null): string[] {
  return getSyllabusTopicRefs(subjectName, examDate).map((topic) => topic.name);
}

/** Compatibility snapshot for callers that still enumerate by display name. */
export const SYLLABUS_TOPICS: Record<string, string[]> = Object.fromEntries(
  [...new Set(CURRICULUM_SPECIFICATIONS.map((specification) => specification.subjectName))]
    .map((name) => [name, getSyllabusTopics(name)]),
);
