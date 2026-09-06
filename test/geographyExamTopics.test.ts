/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import reference from '../data/examTopics/geography.json';
import crosswalk from '../data/examTopics/geography-curriculum-crosswalk.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import {
  browseTopicIdsForQuestion,
  topicsForSubject,
} from '../components/PaperTrail/topics';
import {
  curriculumNodeIdsForExamTopic,
  examQuestionTopicMappingsForSubject,
  examTopicTaxonomyFor,
} from '../data/examTopics/registry';
import { resolveCurriculumSpecification } from '../curriculumRegistry';

const variants = ['higher', 'ordinary', 'higher-new-course', 'ordinary-new-course'] as const;
const referenceTopics = variants.flatMap(variant => reference.variants[variant].topics);

describe('Geography exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('geography')!;

  it('pins the complete outgoing and 2028 reference hierarchy', () => {
    const expectedGroups = variants.flatMap((variant) => {
      const source = reference.variants[variant];
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
            id: `geography-${variant}`,
            label: source.label,
            level,
            course,
            topicIds: source.topics.map(topic => topic.id),
          }];
    });
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups).toEqual(expectedGroups);
    expect(taxonomy.groups).toHaveLength(10);
    expect(taxonomy.topics.map(topic => [topic.id, topic.label, topic.sourcePath]))
      .toEqual(referenceTopics.map(topic => [topic.id, topic.label, topic.sourcePath]));
    expect(topicsForSubject('geography')).toHaveLength(96);
  });

  it('reconciles all 9,907 displayed associations without importing provider content', () => {
    expect(referenceTopics).toHaveLength(96);
    expect(reference.totals).toEqual({
      reported: 9907,
      state: 5475,
      mock: 4432,
      providerSample: 0,
      sourceLabelConflicts: 0,
    });
    for (const topic of referenceTopics) {
      expect(
        topic.officialQuestionHeadings.length
        + topic.mockQuestionCount
        + topic.providerSampleQuestionCount,
        topic.id,
      ).toBe(topic.reportedQuestionCount);
      expect(topic.officialQuestionHeadings.some(heading => /mock/i.test(heading)), topic.id)
        .toBe(false);
    }
  });

  it('keeps outgoing and replacement curriculum bridges cohort-safe', () => {
    const outgoingIds = new Set(
      CURRICULUM.find(subject => subject.id === 'geography')!
        .strands.flatMap(strand => strand.subtopics.map(topic => topic.id)),
    );
    const replacement = resolveCurriculumSpecification('Geography', 2028)!;
    const replacementIds = new Set(
      replacement.groups.flatMap(group => group.topics.map(topic => topic.id)),
    );
    expect(replacement.id).toBe('geography:2028');
    expect(Object.keys(crosswalk)).toHaveLength(96);
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids, topic.id).toEqual(crosswalk[topic.id as keyof typeof crosswalk]);
      expect(ids.length, topic.id).toBeGreaterThan(0);
      const validIds = topic.course === 'new' ? replacementIds : outgoingIds;
      expect(ids.filter(id => !validIds.has(id)), topic.id).toEqual([]);
    }
  });

  it('keeps every existing Geography SEC card in outgoing-course topics', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'geography');
    expect(papers).toHaveLength(60);
    expect(papers.reduce((sum, paper) => sum + paper.q.length, 0)).toBe(720);
    expect(examQuestionTopicMappingsForSubject('geography')).toHaveLength(1317);
    const taxonomyById = new Map(taxonomy.topics.map(topic => [topic.id, topic]));
    for (const paper of papers) {
      for (const question of paper.q) {
        const ids = browseTopicIdsForQuestion(paper, question);
        expect(ids.length, `${paper.year} ${paper.level} ${paper.lang} Q${question.n}`)
          .toBeGreaterThan(0);
        expect(ids.every(id => taxonomyById.get(id)?.course === 'old')).toBe(true);
      }
    }
  });
});
