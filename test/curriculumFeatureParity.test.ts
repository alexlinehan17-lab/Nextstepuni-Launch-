/** @license SPDX-License-Identifier: Apache-2.0 */
import { describe, expect, it } from 'vitest';
import { getSyllabusTopicRefs } from '../components/syllabusTopics';
import {
  examinationYearFromDate,
  resolveCurriculumSpecification,
  specificationContainsId,
} from '../curriculumRegistry';

describe('curriculum feature parity', () => {
  it.each([
    ['Biology', '2026-06-05'],
    ['Biology', '2027-06-05'],
    ['Chemistry', '2027-06-05'],
    ['Geography', '2027-06-05'],
    ['Geography', '2028-06-05'],
    ['Construction Technology', '2028-06-05'],
    ['Engineering', '2028-06-05'],
    ['LCPE', '2028-06-05'],
    ['LCVP', '2028-06-05'],
    ['Religious Education', '2027-06-05'],
  ])('War Room coverage resolves only nodes in %s for %s', (subject, examDate) => {
    const specification = resolveCurriculumSpecification(subject, examinationYearFromDate(examDate))!;
    expect(specification.status).toBe('verified');
    const nodes = getSyllabusTopicRefs(subject, examDate);
    expect(nodes.length).toBeGreaterThan(0);
    for (const node of nodes) {
      expect(specificationContainsId(specification, node.id), `${node.id} escaped ${specification.id}`).toBe(true);
      expect(node.specificationId).toBe(specification.id);
    }
  });

  it('switches taxonomy at a redevelopment boundary instead of mixing cohorts', () => {
    const outgoing = getSyllabusTopicRefs('Geography', '2027-06-05');
    const replacement = getSyllabusTopicRefs('Geography', '2028-06-05');

    expect(new Set(outgoing.map(({ specificationId }) => specificationId))).toEqual(new Set(['geography:outgoing']));
    expect(new Set(replacement.map(({ specificationId }) => specificationId))).toEqual(new Set(['geography:2028']));
    expect(replacement.some(({ id }) => outgoing.some((node) => node.id === id))).toBe(false);
  });

  it('does not expose an expired map while a replacement is still being verified', () => {
    expect(resolveCurriculumSpecification('History', 2029)).toBeUndefined();
    expect(getSyllabusTopicRefs('History', '2029-06-05')).toEqual([]);
    expect(resolveCurriculumSpecification('English', 2029)).toBeUndefined();
    expect(getSyllabusTopicRefs('English', '2029-06-05')).toEqual([]);
  });
});
