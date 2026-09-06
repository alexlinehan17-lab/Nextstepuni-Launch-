/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Final three whole-subject StudyClix hierarchy migrations.
 */

import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import homeReference from '../data/examTopics/home-economics.json';
import homeCrosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import mathsReference from '../data/examTopics/mathematics.json';
import mathsCrosswalk from '../data/examTopics/mathematics-curriculum-crosswalk.json';
import peReference from '../data/examTopics/physical-education.json';
import peCrosswalk from '../data/examTopics/physical-education-curriculum-crosswalk.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { browseTopicIdsForQuestion, topicsForSubject } from '../components/PaperTrail/topics';
import {
  curriculumNodeIdsForExamTopic,
  examQuestionTopicMappingsForSubject,
  examTopicTaxonomyFor,
  type ExamTopicTaxonomy,
} from '../data/examTopics/registry';
import { resolveCurriculumSpecification } from '../curriculumRegistry';

const expectEveryExistingCardMapped = (
  subjectId: string,
  expectedPapers: number,
  expectedPhysicalCards: number,
  expectedLogicalMappings: number,
  taxonomy: ExamTopicTaxonomy,
) => {
  const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === subjectId);
  expect(papers).toHaveLength(expectedPapers);
  expect(papers.reduce((sum, paper) => sum + paper.q.length, 0)).toBe(expectedPhysicalCards);
  expect(examQuestionTopicMappingsForSubject(subjectId)).toHaveLength(expectedLogicalMappings);
  const taxonomyIds = new Set(taxonomy.topics.map(topic => topic.id));
  for (const paper of papers) {
    for (const question of paper.q) {
      const ids = browseTopicIdsForQuestion(paper, question);
      expect(ids.length, `${paper.year} ${paper.level} ${paper.lang} ${paper.paperKey} Q${question.n}`)
        .toBeGreaterThan(0);
      expect(ids.filter(id => !taxonomyIds.has(id))).toEqual([]);
    }
  }
};

describe('Home Economics exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('home-economics-s-and-s')!;
  const referenceTopics = [
    ...homeReference.variants.higher.topics,
    ...homeReference.variants.ordinary.topics,
  ];

  it('pins and reconciles the exact 54-topic two-level hierarchy', () => {
    expect(taxonomy.groups).toEqual([
      {
        id: 'home-economics-s-and-s-higher',
        label: 'Higher Level',
        level: 'higher',
        topicIds: homeReference.variants.higher.topics.map(topic => topic.id),
      },
      {
        id: 'home-economics-s-and-s-ordinary',
        label: 'Ordinary Level',
        level: 'ordinary',
        topicIds: homeReference.variants.ordinary.topics.map(topic => topic.id),
      },
    ]);
    expect(taxonomy.topics.map(topic => [topic.id, topic.label, topic.sourcePath]))
      .toEqual(referenceTopics.map(topic => [topic.id, topic.label, topic.sourcePath]));
    expect(homeReference.totals).toEqual({
      reported: 2901,
      state: 1561,
      mock: 1340,
      providerSample: 0,
      sourceLabelConflicts: 0,
    });
    expect(referenceTopics.reduce((sum, topic) => sum + topic.reportedQuestionCount, 0)).toBe(2901);
    expect(topicsForSubject('home-economics-s-and-s')).toHaveLength(54);
  });

  it('bridges every shelf to Home Economics curriculum and preserves every card', () => {
    const canonicalIds = new Set(
      CURRICULUM.find(subject => subject.id === 'home-economics')!
        .strands.flatMap(strand => strand.subtopics.map(topic => topic.id)),
    );
    expect(Object.keys(homeCrosswalk)).toHaveLength(54);
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids).toEqual(homeCrosswalk[topic.id as keyof typeof homeCrosswalk]);
      expect(ids.length).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id))).toEqual([]);
    }
    expectEveryExistingCardMapped('home-economics-s-and-s', 51, 484, 908, taxonomy);
  });
});

describe('Mathematics exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('mathematics')!;
  const referenceTopics = [
    ...mathsReference.variants.higher.topics,
    ...mathsReference.variants.ordinary.topics,
    ...mathsReference.variants.foundation.topics,
  ];

  it('pins and reconciles all Higher, Ordinary and Foundation topics', () => {
    expect(taxonomy.groups.map(group => [group.id, group.label, group.level])).toEqual([
      ['mathematics-higher', 'Higher Level', 'higher'],
      ['mathematics-ordinary', 'Ordinary Level', 'ordinary'],
      ['mathematics-foundation', 'Foundation Level', 'foundation'],
    ]);
    expect(taxonomy.topics.map(topic => [topic.id, topic.label, topic.sourcePath]))
      .toEqual(referenceTopics.map(topic => [topic.id, topic.label, topic.sourcePath]));
    expect(mathsReference.totals).toEqual({
      reported: 2946,
      state: 1768,
      mock: 1178,
      providerSample: 0,
      sourceLabelConflicts: 0,
    });
    expect(referenceTopics).toHaveLength(55);
    expect(topicsForSubject('mathematics')).toHaveLength(55);
  });

  it('bridges every shelf to Mathematics curriculum and preserves every card', () => {
    const canonicalIds = new Set(
      CURRICULUM.find(subject => subject.id === 'mathematics')!
        .strands.flatMap(strand => strand.subtopics.map(topic => topic.id)),
    );
    expect(Object.keys(mathsCrosswalk)).toHaveLength(55);
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids).toEqual(mathsCrosswalk[topic.id as keyof typeof mathsCrosswalk]);
      expect(ids.length).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id))).toEqual([]);
    }
    expectEveryExistingCardMapped('mathematics', 140, 1281, 1632, taxonomy);
  });
});

describe('Physical Education exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('physical-education')!;
  const variants = ['higher', 'ordinary', 'higher-new-course', 'ordinary-new-course'] as const;
  const referenceTopics = variants.flatMap(variant => peReference.variants[variant].topics);

  it('pins all 88 outgoing and replacement-course topics and their nested groups', () => {
    const expectedGroups = variants.flatMap((variant) => {
      const source = peReference.variants[variant];
      const level = variant.startsWith('higher') ? 'higher' : 'ordinary';
      const course = variant.endsWith('new-course') ? 'new' : 'old';
      return source.groups.length
        ? source.groups.map(group => ({
            id: group.id,
            label: `${source.label} · ${group.label}`,
            level,
            course,
            topicIds: group.topicIds,
          }))
        : [{
            id: `physical-education-${variant}`,
            label: source.label,
            level,
            course,
            topicIds: source.topics.map(topic => topic.id),
          }];
    });
    expect(taxonomy.groups).toEqual(expectedGroups);
    expect(taxonomy.groups).toHaveLength(8);
    expect(taxonomy.topics.map(topic => [topic.id, topic.label, topic.sourcePath]))
      .toEqual(referenceTopics.map(topic => [topic.id, topic.label, topic.sourcePath]));
    expect(referenceTopics).toHaveLength(88);
    expect(topicsForSubject('physical-education')).toHaveLength(88);
  });

  it('reconciles every reachable page and records both broken reference pages honestly', () => {
    expect(peReference.totals).toEqual({
      reported: 1803,
      state: 1265,
      mock: 538,
      providerSample: 0,
      sourceLabelConflicts: 0,
      sourceUnavailableTopics: 2,
    });
    const unavailable = referenceTopics.filter(
      (topic): topic is typeof topic & { sourceUnavailable: string } =>
        'sourceUnavailable' in topic && typeof topic.sourceUnavailable === 'string',
    );
    expect(unavailable).toHaveLength(2);
    expect(unavailable.map(topic => topic.id)).toEqual([
      'physical-education-higher-new-course-21-apply-the-components-of-fitness-in-terms-of-physical-activity-performance',
      'physical-education-ordinary-new-course-21-apply-the-components-of-fitness-in-terms-of-physical-activity-performance',
    ]);
    expect(unavailable.every(topic => topic.sourceUnavailable.includes('HTTP 500'))).toBe(true);
    expect(taxonomy.topics.filter(topic => topic.referenceUnavailable)).toHaveLength(2);
    expect(referenceTopics.filter(topic => !('sourceUnavailable' in topic)).every(topic => (
      topic.officialQuestionHeadings.length
      + topic.mockQuestionCount
      + topic.providerSampleQuestionCount === topic.reportedQuestionCount
    ))).toBe(true);
  });

  it('keeps outgoing and 2028 curriculum bridges separate and preserves every card', () => {
    const outgoingIds = new Set(
      CURRICULUM.find(subject => subject.id === 'physical-education')!
        .strands.flatMap(strand => strand.subtopics.map(topic => topic.id)),
    );
    const replacement = resolveCurriculumSpecification('physical-education', 2028)!;
    const replacementIds = new Set(replacement.groups.map(group => group.id));
    expect(replacement.id).toBe('physical-education:2028');
    expect(replacement.coverageNodeLevel).toBe('group');
    expect(Object.keys(peCrosswalk)).toHaveLength(88);
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids).toEqual(peCrosswalk[topic.id as keyof typeof peCrosswalk]);
      expect(ids.length).toBeGreaterThan(0);
      const validIds = topic.course === 'new' ? replacementIds : outgoingIds;
      expect(ids.filter(id => !validIds.has(id))).toEqual([]);
    }
    expectEveryExistingCardMapped('physical-education', 16, 286, 429, taxonomy);
    expect(examQuestionTopicMappingsForSubject('physical-education').every(mapping => (
      mapping.topicIds.every(id => taxonomy.topics.find(topic => topic.id === id)?.course === 'old')
    ))).toBe(true);
  });
});
