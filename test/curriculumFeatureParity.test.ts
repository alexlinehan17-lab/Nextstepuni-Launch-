/** @license SPDX-License-Identifier: Apache-2.0 */
import { describe, expect, it } from 'vitest';
import { getSyllabusForSubject } from '../components/syllabusData';
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
    ['Chemistry', '2026-06-05'],
    ['Chemistry', '2027-06-05'],
    ['Religious Education', '2027-06-05'],
  ])('War Room coverage resolves only nodes in %s for %s', (subject, examDate) => {
    const spec = resolveCurriculumSpecification(subject, examinationYearFromDate(examDate))!;
    for (const node of getSyllabusTopicRefs(subject, examDate)) {
      expect(specificationContainsId(spec, node.id), `${node.id} escaped ${spec.id}`).toBe(true);
      expect(node.specificationId).toBe(spec.id);
    }
  });

  it('does not apply outgoing Syllabus X-Ray metadata to redeveloped specifications', () => {
    expect(getSyllabusForSubject('Biology', '2026-06-05')).toBeDefined();
    expect(getSyllabusForSubject('Biology', '2027-06-05')).toBeUndefined();
    expect(getSyllabusForSubject('Chemistry', '2027-06-05')).toBeUndefined();
  });

  it('only exposes X-Ray overlay nodes belonging to the resolved specification', () => {
    for (const subject of ['Biology', 'Chemistry', 'Religious Education']) {
      const examDate = '2026-06-05';
      const spec = resolveCurriculumSpecification(subject, examinationYearFromDate(examDate));
      const xray = getSyllabusForSubject(subject, examDate);
      if (!spec || !xray) continue;
      for (const topic of xray.topics) expect(specificationContainsId(spec, topic.id)).toBe(true);
    }
  });
});
