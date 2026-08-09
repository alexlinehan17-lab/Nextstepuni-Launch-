/** @license SPDX-License-Identifier: Apache-2.0 */
import { describe, expect, it } from 'vitest';
import {
  curriculumSubjectsForYear,
  resolveCurriculumSpecification,
} from '../curriculumRegistry';

describe('2026 live-cohort curriculum inventory', () => {
  it('resolves every selectable established Leaving Certificate subject', () => {
    const subjects = curriculumSubjectsForYear(2026, ['leaving-certificate-established']);
    const unresolved = subjects.filter((subject) =>
      !resolveCurriculumSpecification(subject.id, 2026),
    );

    expect(unresolved.map((subject) => subject.id)).toEqual([]);
  });

  it('has no unaudited established subjects in the live 2026 cohort', () => {
    const auditRequired = curriculumSubjectsForYear(2026, ['leaving-certificate-established'])
      .map((subject) => resolveCurriculumSpecification(subject.id, 2026))
      .filter((specification) => specification?.status === 'audit-required')
      .map((specification) => specification!.subjectId)
      .sort();

    expect(auditRequired).toEqual([]);
  });
});
