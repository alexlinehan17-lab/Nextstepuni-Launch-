/** @license SPDX-License-Identifier: Apache-2.0 */

import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import { PAPER_TRAIL_SUBJECTS } from '../paperTrailData';
import snapshotJson from '../data/examTopics/studyclix-subject-taxonomy.json';
import { STUDYCLIX_SUBJECT_MAP } from '../data/examTopics/studyclixSubjectMap';

interface SnapshotTopic {
  id: string;
  label: string;
  sourcePath: string;
  groupId: string | null;
}

interface SnapshotVariant {
  sourcePath: string;
  subjectSlug: string;
  variant: string;
  groups: Array<{ id: string; label: string; topicIds: string[] }>;
  topics: SnapshotTopic[];
}

const snapshot = snapshotJson as { variants: SnapshotVariant[] };

describe('StudyClix subject/topic structure snapshot', () => {
  it('pins the complete audited subject skeleton', () => {
    expect(snapshot.variants).toHaveLength(84);
    expect(new Set(snapshot.variants.map(variant => variant.subjectSlug)).size).toBe(35);
    expect(snapshot.variants.reduce((sum, variant) => sum + variant.groups.length, 0)).toBe(99);
    expect(snapshot.variants.reduce((sum, variant) => sum + variant.topics.length, 0)).toBe(1747);
    expect(snapshot.variants.filter(variant => variant.topics.length === 0)).toEqual([]);
  });

  it('has a unique, labelled topic path inside every course/level variant', () => {
    for (const variant of snapshot.variants) {
      expect(variant.sourcePath).toMatch(/^\/leaving-certificate\//);
      expect(new Set(variant.topics.map(topic => topic.sourcePath)).size, variant.sourcePath).toBe(variant.topics.length);
      expect(new Set(variant.topics.map(topic => topic.id)).size, variant.sourcePath).toBe(variant.topics.length);
      expect(variant.topics.filter(topic => !topic.label.trim()), variant.sourcePath).toEqual([]);
    }
  });

  it('keeps every nested group internally complete', () => {
    for (const variant of snapshot.variants) {
      const byGroup = new Map<string, string[]>();
      for (const topic of variant.topics) {
        if (!topic.groupId) continue;
        const ids = byGroup.get(topic.groupId) ?? [];
        ids.push(topic.id);
        byGroup.set(topic.groupId, ids);
      }
      for (const group of variant.groups) {
        expect(group.label.trim(), `${variant.sourcePath}|${group.id}`).not.toBe('');
        expect(group.topicIds, `${variant.sourcePath}|${group.id}`).toEqual(byGroup.get(group.id));
      }
      expect(new Set(variant.groups.map(group => group.id))).toEqual(new Set(byGroup.keys()));
    }
  });

  it('maps every reference subject explicitly, including future no-paper subjects', () => {
    const slugs = [...new Set(snapshot.variants.map(variant => variant.subjectSlug))].sort();
    expect(Object.keys(STUDYCLIX_SUBJECT_MAP).sort()).toEqual(slugs);

    const paperIds = new Set(PAPER_TRAIL_SUBJECTS.map(subject => subject.id));
    const curriculumIds = new Set(CURRICULUM.map(subject => subject.id));
    for (const [slug, mapping] of Object.entries(STUDYCLIX_SUBJECT_MAP)) {
      if (mapping.paperTrailSubjectId) {
        expect(paperIds.has(mapping.paperTrailSubjectId), `${slug} Paper Trail mapping`).toBe(true);
      }
      if (mapping.curriculumSubjectId) {
        expect(curriculumIds.has(mapping.curriculumSubjectId), `${slug} curriculum mapping`).toBe(true);
      }
      if (mapping.status !== 'future-no-sec-paper') {
        expect(mapping.paperTrailSubjectId, `${slug} should have a current SEC corpus`).toBeTruthy();
        expect(mapping.curriculumSubjectId, `${slug} should have a curriculum link`).toBeTruthy();
      }
    }
  });
});

